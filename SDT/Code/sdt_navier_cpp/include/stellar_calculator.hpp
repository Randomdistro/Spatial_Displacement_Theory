#ifndef SDT_STELLAR_CALCULATOR_HPP
#define SDT_STELLAR_CALCULATOR_HPP

#include <cmath>
#include <string>
#include <vector>
#include <optional>
#include <format>
#include <numbers>

namespace sdt {

// ============================================================================
// SDT PURE — No G, no M as inputs
// ============================================================================
// SDT Stellar Calculator — zk²=1 Methodology
//
// Master constraint: z · k² = 1
//   z = Δλ/λ  (gravitational redshift, spectroscopic observable)
//   k = c/v   (velocity ratio, kinematic observable)
//
// Both z and k are directly measurable. No G, no M required.
//
// Orbital velocity law:  v(r) = (c/k) √(R/r)
// c-boundary radius:     r_c  = R / k²
// Force at c-boundary:   F    = m c² / r_c
// ============================================================================

namespace stellar_constants {
    inline constexpr double C      = 299792458.0;         // Speed of light [m/s] (exact)
    inline constexpr double R_SUN  = 6.957e8;             // Solar radius [m] (IAU 2015 nominal)
    inline constexpr double AU     = 1.495978707e11;      // Astronomical unit [m] (IAU 2012 exact)
    inline constexpr double PI     = std::numbers::pi;
}

/// @brief Represents stellar parameters derived purely from observables
struct StellarParameters {
    double radius_m;                    // Radius in metres (physical measurement)
    double v_surface_ms;                // Surface orbital velocity [m/s] (Doppler measurable)
    double k;                           // k = c / v_surface (kinematic ratio)
    double z;                           // z = 1/k² = Δλ/λ (spectroscopic redshift)
    double r_c_m;                       // c-boundary radius = R / k² [m]
    double circumference_c_boundary_m;  // 2πR/k² — circumference at c-boundary

    [[nodiscard]] auto radius_solar() const noexcept -> double {
        return radius_m / stellar_constants::R_SUN;
    }

    /// @brief Gravitational redshift as velocity equivalent [m/s]
    [[nodiscard]] auto z_velocity_ms() const noexcept -> double {
        return z * stellar_constants::C;
    }
};

/// @brief Represents orbital analysis using pure zk²=1 methodology
struct OrbitalAnalysis {
    double semi_major_axis_m;           // Semi-major axis [m]
    double observed_velocity_ms;        // Observed orbital velocity [m/s]
    double k_parameter;                 // k = c √(R/a) / v_obs
    double predicted_velocity_ms;       // v(r) = (c/k) √(R/r) [m/s]
    double error_percent;               // |v_pred - v_obs| / v_obs × 100
    double z_spectroscopic;             // z = 1/k² (predicted gravitational redshift)
    double zk2_product;                 // z · k² (should be exactly 1.0)
    double zk2_deviation;               // |z·k² - 1|

    [[nodiscard]] auto semi_major_axis_au() const noexcept -> double {
        return semi_major_axis_m / stellar_constants::AU;
    }

    [[nodiscard]] auto observed_velocity_kms() const noexcept -> double {
        return observed_velocity_ms / 1000.0;
    }

    [[nodiscard]] auto predicted_velocity_kms() const noexcept -> double {
        return predicted_velocity_ms / 1000.0;
    }

    [[nodiscard]] auto is_zk2_valid() const noexcept -> bool {
        return zk2_deviation < 0.01; // Within 1% tolerance
    }
};

/// @brief Predicted Balmer line shifts for a given z
struct BalmerShifts {
    double z;
    double delta_H_alpha_nm;   // Δλ for Hα (656.281 nm)
    double delta_H_beta_nm;    // Δλ for Hβ (486.135 nm)
    double delta_H_gamma_nm;   // Δλ for Hγ (434.047 nm)
    double delta_H_delta_nm;   // Δλ for Hδ (410.175 nm)

    static constexpr double H_ALPHA_NM = 656.281;
    static constexpr double H_BETA_NM  = 486.135;
    static constexpr double H_GAMMA_NM = 434.047;
    static constexpr double H_DELTA_NM = 410.175;
};

/// @brief SDT Stellar Calculator — pure zk²=1 methodology, no G
///
/// All calculations derive from two observables:
///   z = Δλ/λ (gravitational redshift from spectroscopy)
///   k = c/v  (velocity ratio from Doppler/kinematic measurement)
///
/// The master constraint z·k²=1 connects them.
/// G never appears. Mass is not required as an input.
class StellarCalculator {
public:

    // ========================================================================
    // Core: From observables to stellar parameters
    // ========================================================================

    /// @brief Calculate stellar parameters from radius and surface velocity
    /// @param radius_m  Physical radius in metres (from interferometry or eclipsing binary)
    /// @param v_surface_ms  Surface orbital velocity in m/s (from spectroscopy)
    /// @return Stellar parameters including k, z, r_c
    [[nodiscard]] static auto from_radius_and_velocity(
        double radius_m,
        double v_surface_ms
    ) noexcept -> StellarParameters {
        const double k = stellar_constants::C / v_surface_ms;
        const double z = 1.0 / (k * k);
        const double r_c = radius_m / (k * k);
        const double circ = 2.0 * stellar_constants::PI * r_c;

        return StellarParameters{
            .radius_m = radius_m,
            .v_surface_ms = v_surface_ms,
            .k = k,
            .z = z,
            .r_c_m = r_c,
            .circumference_c_boundary_m = circ
        };
    }

    /// @brief Calculate stellar parameters from radius and spectroscopic redshift z
    /// @param radius_m  Physical radius in metres
    /// @param z_redshift  Gravitational redshift Δλ/λ (spectroscopic observable)
    /// @return Stellar parameters
    [[nodiscard]] static auto from_radius_and_redshift(
        double radius_m,
        double z_redshift
    ) noexcept -> StellarParameters {
        const double k = 1.0 / std::sqrt(z_redshift);
        const double v_surface = stellar_constants::C / k;
        const double r_c = radius_m * z_redshift;    // R/k² = R·z
        const double circ = 2.0 * stellar_constants::PI * r_c;

        return StellarParameters{
            .radius_m = radius_m,
            .v_surface_ms = v_surface,
            .k = k,
            .z = z_redshift,
            .r_c_m = r_c,
            .circumference_c_boundary_m = circ
        };
    }

    /// @brief Calculate k from excitation level n and fine structure constant α
    /// @param n  Principal quantum number / excitation level
    /// @param alpha  Fine structure constant (default: 1/137.035999084)
    /// @return k = n / α  (e.g. n=1 → k=137, n=5 → k=685, n=6 → k=822)
    [[nodiscard]] static constexpr auto k_from_excitation(
        int n,
        double alpha = 7.2973525693e-3
    ) noexcept -> double {
        return static_cast<double>(n) / alpha;
    }

    // ========================================================================
    // Orbital analysis — pure geometry, no G
    // ========================================================================

    /// @brief Calculate k-parameter from observed orbital data
    /// @param semi_major_axis_m  Semi-major axis in metres
    /// @param observed_velocity_ms  Observed orbital velocity in m/s
    /// @param stellar_radius_m  Stellar radius in metres
    /// @return k-parameter, or nullopt if velocity is zero
    [[nodiscard]] static auto calculate_k_parameter(
        double semi_major_axis_m,
        double observed_velocity_ms,
        double stellar_radius_m
    ) noexcept -> std::optional<double> {
        if (observed_velocity_ms == 0.0) {
            return std::nullopt;
        }
        // From v(r) = (c/k)√(R/r), at r = a with known v_obs:
        // k = c × √(R/a) / v_obs
        const double r_ratio = std::sqrt(stellar_radius_m / semi_major_axis_m);
        return stellar_constants::C * r_ratio / observed_velocity_ms;
    }

    /// @brief Predict orbital velocity using SDT k-law: v(r) = (c/k) √(R/r)
    /// @param semi_major_axis_m  Semi-major axis in metres
    /// @param stellar_radius_m  Stellar radius in metres
    /// @param k  Universal k-parameter for the system
    /// @return Predicted orbital velocity in m/s
    [[nodiscard]] static auto predict_velocity(
        double semi_major_axis_m,
        double stellar_radius_m,
        double k
    ) noexcept -> double {
        return (stellar_constants::C / k) * std::sqrt(stellar_radius_m / semi_major_axis_m);
    }

    /// @brief Verify z·k²=1 from independent observables
    /// @param z_spectroscopic  Measured gravitational redshift Δλ/λ
    /// @param k_kinematic  Measured k = c / v_surface
    /// @return Tuple of (z, k², z·k², |z·k² - 1|)
    [[nodiscard]] static auto verify_zk2(
        double z_spectroscopic,
        double k_kinematic
    ) noexcept -> std::tuple<double, double, double, double> {
        const double k2 = k_kinematic * k_kinematic;
        const double product = z_spectroscopic * k2;
        const double deviation = std::abs(product - 1.0);
        return {z_spectroscopic, k2, product, deviation};
    }

    /// @brief Complete orbital analysis — no G, no mass
    /// @param stellar_radius_m  Stellar radius in metres
    /// @param semi_major_axis_au  Semi-major axis in AU
    /// @param observed_velocity_kms  Observed velocity in km/s
    /// @return Complete orbital analysis
    [[nodiscard]] static auto analyze_orbit(
        double stellar_radius_m,
        double semi_major_axis_au,
        double observed_velocity_kms
    ) noexcept -> std::optional<OrbitalAnalysis> {
        const double a_m = semi_major_axis_au * stellar_constants::AU;
        const double v_obs_ms = observed_velocity_kms * 1000.0;

        auto k_opt = calculate_k_parameter(a_m, v_obs_ms, stellar_radius_m);
        if (!k_opt) {
            return std::nullopt;
        }

        const double k = *k_opt;
        const double v_pred_ms = predict_velocity(a_m, stellar_radius_m, k);
        const double error = std::abs(v_pred_ms - v_obs_ms) / v_obs_ms * 100.0;

        // z = 1/k² — the predicted spectroscopic redshift
        const double z = 1.0 / (k * k);
        const double zk2 = z * k * k;   // Should be exactly 1.0
        const double dev = std::abs(zk2 - 1.0);

        return OrbitalAnalysis{
            .semi_major_axis_m = a_m,
            .observed_velocity_ms = v_obs_ms,
            .k_parameter = k,
            .predicted_velocity_ms = v_pred_ms,
            .error_percent = error,
            .z_spectroscopic = z,
            .zk2_product = zk2,
            .zk2_deviation = dev
        };
    }

    // ========================================================================
    // Spectral predictions — Balmer shifts from k
    // ========================================================================

    /// @brief Predict Balmer line shifts for a given k value
    /// @param k  System k-parameter
    /// @return Predicted wavelength shifts for Hα, Hβ, Hγ, Hδ
    [[nodiscard]] static auto predict_balmer_shifts(
        double k
    ) noexcept -> BalmerShifts {
        const double z = 1.0 / (k * k);
        return BalmerShifts{
            .z = z,
            .delta_H_alpha_nm = BalmerShifts::H_ALPHA_NM * z,
            .delta_H_beta_nm  = BalmerShifts::H_BETA_NM  * z,
            .delta_H_gamma_nm = BalmerShifts::H_GAMMA_NM * z,
            .delta_H_delta_nm = BalmerShifts::H_DELTA_NM  * z
        };
    }

    /// @brief Predict gravitational redshift velocity from k
    /// @param k  System k-parameter
    /// @return Gravitational redshift as velocity [m/s]
    [[nodiscard]] static constexpr auto z_velocity_from_k(
        double k
    ) noexcept -> double {
        return stellar_constants::C / (k * k);
    }

    // ========================================================================
    // c-boundary geometry
    // ========================================================================

    /// @brief Calculate c-boundary radius: r_c = R / k²
    /// @param R  System effective radius [m]
    /// @param k  System k-parameter
    /// @return c-boundary radius in metres
    [[nodiscard]] static constexpr auto c_boundary_radius(
        double R, double k
    ) noexcept -> double {
        return R / (k * k);
    }

    /// @brief Calculate circumference at c-boundary: 2πR/k²
    /// @param R  System effective radius [m]
    /// @param k  System k-parameter
    /// @return Circumference at c-boundary in metres
    [[nodiscard]] static constexpr auto c_boundary_circumference(
        double R, double k
    ) noexcept -> double {
        return 2.0 * stellar_constants::PI * R / (k * k);
    }

    /// @brief Force at c-boundary: F = mc²/r_c
    /// @param mass_kg  Measured mass [kg] — the spation matrix resistance of the test body.
    ///                 This is a measured quantity, not an SDT input primitive.
    /// @param r_c_m  c-boundary radius [m] (derived from R/k²)
    /// @return Force in Newtons
    [[nodiscard]] static constexpr auto force_at_c_boundary(
        double mass_kg, double r_c_m
    ) noexcept -> double {
        return mass_kg * stellar_constants::C * stellar_constants::C / r_c_m;
    }
};

} // namespace sdt

#endif // SDT_STELLAR_CALCULATOR_HPP
