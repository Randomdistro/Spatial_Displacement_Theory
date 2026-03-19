#ifndef SDT_GALACTIC_ROTATION_HPP
#define SDT_GALACTIC_ROTATION_HPP

#include <cmath>
#include <string>
#include <vector>
#include <optional>
#include <format>
#include <numeric>
#include <algorithm>

namespace sdt {

// ============================================================================
// SDT PURE — No G, no M as inputs. No dark matter.
// ============================================================================
// Galactic scale constants
namespace galactic_constants {
    constexpr double C = 299792458.0;                    // Speed of light [m/s]
    constexpr double KPC_TO_M = 3.086e19;                // Kiloparsec to meters
    constexpr double L_SUN = 3.828e26;                   // Solar luminosity [W]
    constexpr double EPSILON_BURN = 1e-15;               // Mass-to-light efficiency (nuclear burning)
    constexpr double R_FLAT_FACTOR = 2.5;                // Predicted R_flat/R_d ratio (Phase 24)
    constexpr double E_SATURATION = 0.64;                // Eclipse saturation value

    // NIST reference values — validation targets only, never SDT input primitives.
    // Mass is the resistance to change imparted by the spation matrix.
    constexpr double M_SUN_NIST_REF = 1.989e30;          // Solar mass [kg] (NIST reference)
}

/// @brief Point on galactic rotation curve
struct RotationPoint {
    double radius_kpc;                                   // Galactocentric radius [kpc]
    double velocity_kms;                                 // Rotational velocity [km/s]
    double occlusion_E;                                  // Eclipse function E(r)
    
    [[nodiscard]] auto radius_m() const noexcept -> double {
        return radius_kpc * galactic_constants::KPC_TO_M;
    }
    
    [[nodiscard]] auto velocity_ms() const noexcept -> double {
        return velocity_kms * 1000.0;
    }
    
    [[nodiscard]] auto is_flat_regime(double R_d_kpc) const noexcept -> bool {
        return radius_kpc >= galactic_constants::R_FLAT_FACTOR * R_d_kpc;
    }
};

/// @brief Galaxy structural parameters with luminosity
struct GalaxyParameters {
    std::string name;                                    // Galaxy name
    double R_d_kpc;                                      // Disk scale length [kpc]
    double v_flat_kms;                                   // Flat rotation velocity [km/s]
    double M_disk_solar_nist_ref;                        // Total disk mass [solar masses] — NIST validation target, not SDT input
    double R_flat_observed_kpc;                          // Observed R_flat [kpc]
    double luminosity_solar;                             // Total luminosity [L☉]
    
    [[nodiscard]] auto R_flat_predicted_kpc() const noexcept -> double {
        return galactic_constants::R_FLAT_FACTOR * R_d_kpc;
    }
    
    [[nodiscard]] auto R_flat_ratio() const noexcept -> double {
        return R_flat_observed_kpc / R_d_kpc;
    }
    
    [[nodiscard]] auto R_flat_error_percent() const noexcept -> double {
        const double predicted = R_flat_predicted_kpc();
        return std::abs(R_flat_observed_kpc - predicted) / predicted * 100.0;
    }
    
    [[nodiscard]] auto k_parameter() const noexcept -> double {
        return galactic_constants::C / (v_flat_kms * 1000.0);
    }
    
    [[nodiscard]] auto z_compactness() const noexcept -> double {
        // z = gR/c² where g = v²/R (circular orbit)
        const double R_m = R_d_kpc * galactic_constants::KPC_TO_M;
        const double v_ms = v_flat_kms * 1000.0;
        const double g = (v_ms * v_ms) / R_m;
        return (g * R_m) / (galactic_constants::C * galactic_constants::C);
    }
    
    [[nodiscard]] auto zk2_product() const noexcept -> double {
        const double k = k_parameter();
        const double z = z_compactness();
        return z * k * k;
    }
};

/// @brief Statistical validation results
struct ValidationStatistics {
    double mean_ratio;                                   // Mean R_flat/R_d
    double std_deviation;                                // Standard deviation
    double mean_error_percent;                           // Mean percentage error
    double max_error_percent;                            // Maximum percentage error
    int n_galaxies;                                      // Number of galaxies tested
    
    [[nodiscard]] auto passes_certification() const noexcept -> bool {
        return mean_error_percent < 1.0;  // <1% certification threshold (B14)
    }
};

/// @brief World-class galactic rotation calculator implementing Phase 24 disk eclipse saturation
class GalacticRotationCalculator {
public:
    /// @brief Calculate occlusion function E(r) with disk eclipse saturation
    /// @param r_kpc Galactocentric radius in kpc
    /// @param R_d_kpc Disk scale length in kpc
    /// @return Occlusion value E(r) ∈ [0, E_sat]
    [[nodiscard]] static auto calculate_occlusion(
        double r_kpc,
        double R_d_kpc
    ) noexcept -> double {
        using namespace galactic_constants;
        
        const double r_ratio = r_kpc / R_d_kpc;
        
        if (r_ratio < 1.0) {
            // Inner region: parabolic growth E ∝ r²
            return 0.5 * r_ratio * r_ratio;
        } else {
            // Outer region: exponential saturation
            // E → E_sat as r → ∞ (no additional shadowing)
            return E_SATURATION * (1.0 - std::exp(-(r_ratio - 1.0)));
        }
    }
    
    /// @brief Predict rotation velocity using disk eclipse saturation model
    /// @param r_kpc Galactocentric radius in kpc
    /// @param R_d_kpc Disk scale length in kpc
    /// @param v_flat_kms Asymptotic flat velocity in km/s
    /// @return Predicted velocity in km/s
    [[nodiscard]] static auto predict_velocity(
        double r_kpc,
        double R_d_kpc,
        double v_flat_kms
    ) noexcept -> double {
        using namespace galactic_constants;
        
        const double R_flat = R_FLAT_FACTOR * R_d_kpc;
        
        if (r_kpc < R_flat) {
            // Keplerian regime: v ∝ 1/√r
            return v_flat_kms * std::sqrt(R_flat / r_kpc);
        } else {
            // Flat regime: eclipse saturation -> constant v
            return v_flat_kms;
        }
    }
    
    /// @brief Generate complete rotation curve
    /// @param R_d_kpc Disk scale length
    /// @param v_flat_kms Flat rotation velocity
    /// @param r_max_kpc Maximum radius
    /// @param n_points Number of points to sample
    /// @return Vector of rotation curve points
    [[nodiscard]] static auto generate_rotation_curve(
        double R_d_kpc,
        double v_flat_kms,
        double r_max_kpc = 30.0,
        int n_points = 50
    ) noexcept -> std::vector<RotationPoint> {
        std::vector<RotationPoint> curve;
        curve.reserve(n_points);
        
        const double dr = (r_max_kpc - 0.5) / (n_points - 1);
        
        for (int i = 0; i < n_points; ++i) {
            const double r = 0.5 + i * dr;
            const double v = predict_velocity(r, R_d_kpc, v_flat_kms);
            const double E = calculate_occlusion(r, R_d_kpc);
            
            curve.push_back(RotationPoint{
                .radius_kpc = r,
                .velocity_kms = v,
                .occlusion_E = E
            });
        }
        
        return curve;
    }
    
    /// @brief Test R_flat ≈ 2.5 R_d correlation across multiple galaxies
    /// @param galaxies Vector of galaxy parameters
    /// @return Statistical validation results
    [[nodiscard]] static auto validate_rflat_correlation(
        const std::vector<GalaxyParameters>& galaxies
    ) noexcept -> ValidationStatistics {
        if (galaxies.empty()) {
            return ValidationStatistics{};
        }
        
        std::vector<double> ratios;
        std::vector<double> errors;
        ratios.reserve(galaxies.size());
        errors.reserve(galaxies.size());
        
        for (const auto& galaxy : galaxies) {
            ratios.push_back(galaxy.R_flat_ratio());
            errors.push_back(galaxy.R_flat_error_percent());
        }
        
        // Calculate statistics
        const double mean_ratio = std::accumulate(ratios.begin(), ratios.end(), 0.0) / ratios.size();
        
        const double variance = std::accumulate(ratios.begin(), ratios.end(), 0.0,
            [mean_ratio](double acc, double val) {
                const double diff = val - mean_ratio;
                return acc + diff * diff;
            }) / ratios.size();
        const double std_dev = std::sqrt(variance);
        
        const double mean_error = std::accumulate(errors.begin(), errors.end(), 0.0) / errors.size();
        const double max_error = *std::max_element(errors.begin(), errors.end());
        
        return ValidationStatistics{
            .mean_ratio = mean_ratio,
            .std_deviation = std_dev,
            .mean_error_percent = mean_error,
            .max_error_percent = max_error,
            .n_galaxies = static_cast<int>(galaxies.size())
        };
    }
    
#ifdef SDT_ALLOW_LEGACY_COMPARISON
    /// @brief [QUARANTINED] Dark matter halo prediction — NOT SDT.
    /// SDT explains flat rotation curves via cumulative stellar occlusion.
    /// This function is retained only for comparison against legacy models.
    [[nodiscard]] static auto dark_matter_halo_velocity(
        double r_kpc,
        double v_halo_kms,
        double r_s_kpc
    ) noexcept -> double {
        // NFW profile approximation for comparison only
        const double x = r_kpc / r_s_kpc;
        const double ln_factor = std::log(1.0 + x) - x / (1.0 + x);
        return v_halo_kms * std::sqrt(ln_factor / x);
    }
#endif // SDT_ALLOW_LEGACY_COMPARISON
    
    /// @brief Calculate baryonic mass from luminosity using L × k² = ε Mc²
    /// @param luminosity_solar Galaxy luminosity in solar luminosities
    /// @param k_parameter Orbital k-parameter from rotation velocity
    /// @return Predicted baryonic mass in solar masses
    [[nodiscard]] static auto calculate_mass_from_luminosity(
        double luminosity_solar,
        double k_parameter
    ) noexcept -> double {
        using namespace galactic_constants;
        
        // L × k² = ε × M × c²
        // Therefore: M = (L × k²) / (ε × c²)
        const double L_watts = luminosity_solar * L_SUN;
        const double Lk2 = L_watts * k_parameter * k_parameter;
        const double M_kg = Lk2 / (EPSILON_BURN * C * C);
        
        return M_kg / M_SUN_NIST_REF;  // Convert to solar masses (NIST reference)
    }
    
    /// @brief Validate L × k² = ε Mc² relationship
    /// @param galaxy Galaxy parameters with known mass and luminosity
    /// @return Ratio of predicted/observed mass (should be ≈ 1.0)
    [[nodiscard]] static auto validate_luminosity_mass_relation(
        const GalaxyParameters& galaxy
    ) noexcept -> double {
        const double k = galaxy.k_parameter();
        const double M_predicted = calculate_mass_from_luminosity(galaxy.luminosity_solar, k);
        return M_predicted / galaxy.M_disk_solar_nist_ref;
    }
    
    /// @brief Calculate Lk²/(Mc²) diagnostic ratio
    /// @param galaxy Galaxy parameters
    /// @return The dimensionless ratio (should be ≈ ε = 10⁻¹⁵)
    [[nodiscard]] static auto calculate_lk2_diagnostic(
        const GalaxyParameters& galaxy
    ) noexcept -> double {
        using namespace galactic_constants;
        
        const double k = galaxy.k_parameter();
        const double L_watts = galaxy.luminosity_solar * L_SUN;
        const double M_kg = galaxy.M_disk_solar_nist_ref * M_SUN_NIST_REF;
        const double Lk2 = L_watts * k * k;
        const double Mc2 = M_kg * C * C;
        
        return Lk2 / Mc2;
    }
    
    /// @brief Create standard test galaxy dataset from Tyndall (2025) paper
    /// @return Vector of well-studied galaxies for validation
    [[nodiscard]] static auto get_standard_test_galaxies() noexcept -> std::vector<GalaxyParameters> {
        return {
            GalaxyParameters{
                .name = "Milky Way",
                .R_d_kpc = 2.5,
                .v_flat_kms = 220.0,
                .M_disk_solar_nist_ref = 6.0e10,
                .R_flat_observed_kpc = 6.0,
                .luminosity_solar = 1.5e10
            },
            GalaxyParameters{
                .name = "M31 (Andromeda)",
                .R_d_kpc = 5.4,
                .v_flat_kms = 250.0,
                .M_disk_solar_nist_ref = 1.2e11,
                .R_flat_observed_kpc = 13.5,
                .luminosity_solar = 2.6e10
            },
            GalaxyParameters{
                .name = "NGC 3198",
                .R_d_kpc = 2.8,
                .v_flat_kms = 150.0,
                .M_disk_solar_nist_ref = 3.5e10,
                .R_flat_observed_kpc = 7.2,
                .luminosity_solar = 5.0e9
            },
            GalaxyParameters{
                .name = "NGC 2403",
                .R_d_kpc = 1.8,
                .v_flat_kms = 135.0,  // Updated from paper
                .M_disk_solar_nist_ref = 2.0e10,
                .R_flat_observed_kpc = 4.4,
                .luminosity_solar = 3.0e9
            },
            GalaxyParameters{
                .name = "Triangulum (M33)",
                .R_d_kpc = 1.6,
                .v_flat_kms = 130.0,
                .M_disk_solar_nist_ref = 5.0e10,
                .R_flat_observed_kpc = 4.0,
                .luminosity_solar = 5.0e9
            },
            GalaxyParameters{
                .name = "DDO 154",
                .R_d_kpc = 0.9,
                .v_flat_kms = 45.0,
                .M_disk_solar_nist_ref = 5.0e8,
                .R_flat_observed_kpc = 2.3,
                .luminosity_solar = 1.0e7
            }
        };
    }
};

} // namespace sdt

#endif // SDT_GALACTIC_ROTATION_HPP
