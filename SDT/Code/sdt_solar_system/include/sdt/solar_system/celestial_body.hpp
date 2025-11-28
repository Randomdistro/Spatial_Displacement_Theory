#pragma once

#include <string>
#include <optional>
#include <Eigen/Dense>

namespace sdt::solar_system {

    using Vec3d = Eigen::Vector3d;
    using scalar_t = double;
    using time_t = double;

    // SDT-native parameters for celestial bodies
    // From Phase 15: a(r) = -c² R_eff / (Ϟ² r²)
    struct SDTParameters {
        scalar_t kappa = 0.0;      // Velocity factor Ϟ (dimensionless)
        scalar_t R_eff = 0.0;      // Effective radius (m)
        
        // Calculate beta parameter (for compatibility with existing code)
        // β = c² R_eff / Ϟ²
        scalar_t beta() const {
            if (kappa <= 0.0 || R_eff <= 0.0) {
                return 0.0;
            }
            constexpr double c = 299792458.0;
            return (c * c * R_eff) / (kappa * kappa);
        }
        
        // Calculate orbital velocity at radius r
        // v(r) = (c/Ϟ) √(R_eff/r)
        scalar_t orbital_velocity(scalar_t r) const {
            if (kappa <= 0.0 || R_eff <= 0.0 || r <= 0.0) {
                return 0.0;
            }
            constexpr double c = 299792458.0;
            return (c / kappa) * std::sqrt(R_eff / r);
        }
        
        // Calculate orbital period at radius r
        // T = 2πϞ √(r³/R_eff) / c
        scalar_t orbital_period(scalar_t r) const {
            if (kappa <= 0.0 || R_eff <= 0.0 || r <= 0.0) {
                return 0.0;
            }
            constexpr double c = 299792458.0;
            constexpr double two_pi = 2.0 * 3.14159265358979323846;
            return two_pi * kappa * std::sqrt(r * r * r / R_eff) / c;
        }
        
        // Calculate acceleration magnitude at distance r
        // a(r) = -c² R_eff / (Ϟ² r²)
        scalar_t acceleration_magnitude(scalar_t r) const {
            if (kappa <= 0.0 || R_eff <= 0.0 || r <= 0.0) {
                return 0.0;
            }
            constexpr double c = 299792458.0;
            return (c * c * R_eff) / (kappa * kappa * r * r);
        }
    };

    // Celestial body representation
    struct CelestialBody {
        std::string name;
        std::string type;  // "star", "planet", "moon", "asteroid", "comet"
        
        // Position and velocity (m, m/s)
        Vec3d position = Vec3d::Zero();
        Vec3d velocity = Vec3d::Zero();
        
        // Physical properties
        scalar_t radius = 0.0;  // Physical radius (m)
        scalar_t mass_conv = 0.0;  // Conventional mass (kg) - for comparison/energy calculations only
        
        // SDT-native parameters
        SDTParameters sdt_params;
        
        // Optional properties
        std::optional<scalar_t> luminosity;  // W
        std::optional<scalar_t> temperature;  // K
        std::optional<scalar_t> color_bv;  // B-V color index
        
        // Calculate orbital velocity around parent body
        scalar_t orbital_speed_around(const CelestialBody& parent) const {
            const Vec3d r_vec = position - parent.position;
            const scalar_t r = r_vec.norm();
            return parent.sdt_params.orbital_velocity(r);
        }
        
        // Calculate orbital period around parent body
        scalar_t orbital_period_around(const CelestialBody& parent) const {
            const Vec3d r_vec = position - parent.position;
            const scalar_t r = r_vec.norm();
            return parent.sdt_params.orbital_period(r);
        }
        
        // Calculate distance to another body
        scalar_t distance_to(const CelestialBody& other) const {
            return (position - other.position).norm();
        }
    };

} // namespace sdt::solar_system


