#ifndef SDT_STELLAR_CALCULATOR_HPP
#define SDT_STELLAR_CALCULATOR_HPP

#include <cmath>
#include <string>
#include <vector>
#include <optional>
#include <format>

namespace sdt {

// Physical constants in SI units
namespace constants {
    constexpr double C = 299792458.0;              // Speed of light [m/s]
    constexpr double G = 6.67430e-11;              // Gravitational constant [m³/kg/s²]
    constexpr double M_SUN = 1.98892e30;           // Solar mass [kg]
    constexpr double R_SUN = 6.96e8;               // Solar radius [m]
    constexpr double AU = 1.49597870700e11;        // Astronomical unit [m]
}

/// @brief Represents stellar physical parameters
struct StellarParameters {
    double mass_kg;                                 // Mass in kg
    double radius_m;                                // Radius in meters
    double beta;                                    // β = GM/c² compactness parameter
    double compactness;                             // β/R dimensionless compactness
    
    [[nodiscard]] auto mass_solar() const noexcept -> double {
        return mass_kg / constants::M_SUN;
    }
    
    [[nodiscard]] auto radius_solar() const noexcept -> double {
        return radius_m / constants::R_SUN;
    }
};

/// @brief Represents orbital parameters and predictions
struct OrbitalAnalysis {
    double semi_major_axis_m;                      // Semi-major axis [m]
    double observed_velocity_ms;                   // Observed velocity [m/s]
    double k_parameter;                            // Universal orbital k-parameter
    double predicted_velocity_ms;                  // SDT predicted velocity [m/s]
    double error_percent;                          // Prediction error [%]
    double z_compactness;                          // z = 2R_c/D compactness ratio
    double zk2_product;                            // z·k² (should be ≈ 1 for continuous mass)
    double zk2_deviation;                          // |z·k² - 1|
    
    [[nodiscard]] auto semi_major_axis_au() const noexcept -> double {
        return semi_major_axis_m / constants::AU;
    }
    
    [[nodiscard]] auto observed_velocity_kms() const noexcept -> double {
        return observed_velocity_ms / 1000.0;
    }
    
    [[nodiscard]] auto predicted_velocity_kms() const noexcept -> double {
        return predicted_velocity_ms / 1000.0;
    }
    
    [[nodiscard]] auto is_zk2_valid() const noexcept -> bool {
        return zk2_deviation < 0.05; // Within 5% tolerance
    }
};

/// @brief World-class stellar parameter calculator implementing Phase 22 SDT theory
class StellarCalculator {
public:
    /// @brief Calculate stellar compactness parameters
    /// @param mass_solar Mass in solar masses
    /// @param radius_solar Radius in solar radii
    /// @return Stellar parameters including β and compactness
    [[nodiscard]] static auto calculate_stellar_parameters(
        double mass_solar,
        double radius_solar
    ) noexcept -> StellarParameters {
        const double mass_kg = mass_solar * constants::M_SUN;
        const double radius_m = radius_solar * constants::R_SUN;
        const double beta = (constants::G * mass_kg) / (constants::C * constants::C);
        const double compactness = beta / radius_m;
        
        return StellarParameters{
            .mass_kg = mass_kg,
            .radius_m = radius_m,
            .beta = beta,
            .compactness = compactness
        };
    }
    
    /// @brief Calculate k-parameter from observed orbital data
    /// @param semi_major_axis_m Semi-major axis in meters
    /// @param observed_velocity_ms Observed orbital velocity in m/s
    /// @param stellar_radius_m Stellar radius in meters
    /// @return k-parameter or std::nullopt if velocity is zero
    [[nodiscard]] static auto calculate_k_parameter(
        double semi_major_axis_m,
        double observed_velocity_ms,
        double stellar_radius_m
    ) noexcept -> std::optional<double> {
        if (observed_velocity_ms == 0.0) {
            return std::nullopt;
        }
        
        const double r_ratio = std::sqrt(stellar_radius_m / semi_major_axis_m);
        return constants::C * r_ratio / observed_velocity_ms;
    }
    
    /// @brief Predict orbital velocity using SDT k-law: v = (c/k)√(β/a)
    /// @param semi_major_axis_m Semi-major axis in meters
    /// @param beta Stellar β-parameter in meters
    /// @param k Universal k-parameter
    /// @return Predicted orbital velocity in m/s
    [[nodiscard]] static auto predict_velocity(
        double semi_major_axis_m,
        double beta,
        double k
    ) noexcept -> double {
        return (constants::C / k) * std::sqrt(beta / semi_major_axis_m);
    }
    
    /// @brief Verify z·k² = 1 relationship for continuous mass distributions
    /// @param stellar_radius_m Stellar radius in meters
    /// @param semi_major_axis_m Orbital semi-major axis in meters
    /// @param k Universal k-parameter
    /// @return Tuple of (z, k², z·k², deviation from 1.0)
    [[nodiscard]] static auto verify_zk2_relation(
        double stellar_radius_m,
        double semi_major_axis_m,
        double k
    ) noexcept -> std::tuple<double, double, double, double> {
        const double z = 2.0 * stellar_radius_m / (2.0 * semi_major_axis_m);
        const double k_squared = k * k;
        const double zk2_product = z * k_squared;
        const double deviation = std::abs(zk2_product - 1.0);
        
        return {z, k_squared, zk2_product, deviation};
    }
    
    /// @brief Complete orbital analysis for a planetary system
    /// @param stellar_params Stellar physical parameters
    /// @param semi_major_axis_au Semi-major axis in AU
    /// @param observed_velocity_kms Observed velocity in km/s
    /// @return Complete orbital analysis
    [[nodiscard]] static auto analyze_orbit(
        const StellarParameters& stellar_params,
        double semi_major_axis_au,
        double observed_velocity_kms
    ) noexcept -> std::optional<OrbitalAnalysis> {
        const double a_m = semi_major_axis_au * constants::AU;
        const double v_obs_ms = observed_velocity_kms * 1000.0;
        
        auto k_opt = calculate_k_parameter(a_m, v_obs_ms, stellar_params.radius_m);
        if (!k_opt) {
            return std::nullopt;
        }
        
        const double k = *k_opt;
        const double v_pred_ms = predict_velocity(a_m, stellar_params.beta, k);
        const double error = std::abs(v_pred_ms - v_obs_ms) / v_obs_ms * 100.0;
        
        auto [z, k2, zk2, dev] = verify_zk2_relation(stellar_params.radius_m, a_m, k);
        
        return OrbitalAnalysis{
            .semi_major_axis_m = a_m,
            .observed_velocity_ms = v_obs_ms,
            .k_parameter = k,
            .predicted_velocity_ms = v_pred_ms,
            .error_percent = error,
            .z_compactness = z,
            .zk2_product = zk2,
            .zk2_deviation = dev
        };
    }
};

} // namespace sdt

#endif // SDT_STELLAR_CALCULATOR_HPP
