#pragma once

#include <Eigen/Dense>
#include <complex>
#include <vector>
#include <string>
#include <chrono>
#include <optional>

namespace sdt {

    // Vector types
    using Vec3d = Eigen::Vector3d;
    using Vec3f = Eigen::Vector3f;
    using Mat3d = Eigen::Matrix3d;
    
    // Scalar types
    using scalar_t = double;
    using index_t = std::size_t;
    
    // Time types
    using time_t = double;  // Time in seconds
    using duration_t = std::chrono::duration<double>;
    
    // Physical quantities
    struct PhysicalQuantity {
        scalar_t value;
        scalar_t uncertainty = 0.0;
        std::string unit;
        
        PhysicalQuantity() = default;
        PhysicalQuantity(scalar_t val, scalar_t unc = 0.0, std::string u = "")
            : value(val), uncertainty(unc), unit(std::move(u)) {}
    };
    
    // SDT-native parameters
    struct SDTParameters {
        scalar_t kappa = 0.0;      // Velocity factor Ϟ
        scalar_t R_eff = 0.0;      // Effective radius (m)
        scalar_t beta = 0.0;       // Gravitational parameter β (m³/s²)
        scalar_t z = 0.0;          // Compactness parameter
        
        // Universal relationship: z * kappa² = 1
        void enforce_universal_relation() {
            if (kappa > 0.0 && z > 0.0) {
                // Check if relationship holds
                constexpr double tolerance = 1e-6;
                const double product = z * kappa * kappa;
                if (std::abs(product - 1.0) > tolerance) {
                    // Adjust z to satisfy relationship
                    z = 1.0 / (kappa * kappa);
                }
            }
        }
        
        // Calculate beta from kappa and R_eff
        // From: β = c² R_eff / κ²
        void calculate_beta() {
            if (kappa > 0.0 && R_eff > 0.0) {
                beta = (constants::c * constants::c * R_eff) / (kappa * kappa);
            }
        }
        
        // Calculate orbital velocity at radius r
        // From: v(r) = (c/κ) √(R_eff/r)
        scalar_t orbital_velocity(scalar_t r) const {
            if (kappa <= 0.0 || R_eff <= 0.0 || r <= 0.0) {
                return 0.0;
            }
            return (constants::c / kappa) * std::sqrt(R_eff / r);
        }
        
        // Calculate orbital period at radius r
        // From: P = 2π r / v(r) = 2πκ r / (c √(R_eff/r)) = 2πκ √(r³/R_eff) / c
        scalar_t orbital_period(scalar_t r) const {
            if (kappa <= 0.0 || R_eff <= 0.0 || r <= 0.0) {
                return 0.0;
            }
            return constants::two_pi * kappa * std::sqrt(r * r * r / R_eff) / constants::c;
        }
        
        // Calculate acceleration from pressure gradient
        // From: a(r) = -β / r²
        Vec3d acceleration(const Vec3d& position) const {
            const scalar_t r = position.norm();
            if (r <= 0.0 || beta <= 0.0) {
                return Vec3d::Zero();
            }
            const Vec3d r_hat = position.normalized();
            return -beta / (r * r) * r_hat;
        }
        
        // Calculate pressure field at position
        // From: Π(r) = P_CMB - β ρ_s / r
        scalar_t pressure_field(scalar_t r) const {
            if (r <= 0.0) {
                return constants::P_CMB;  // At origin, pressure equals CMB pressure
            }
            return constants::P_CMB - (beta * constants::rho_s) / r;
        }
    };
    
    // Celestial body representation
    struct CelestialBody {
        std::string name;
        std::string type;  // "star", "planet", "moon", "asteroid", etc.
        
        // Position and velocity
        Vec3d position = Vec3d::Zero();
        Vec3d velocity = Vec3d::Zero();
        
        // Physical properties
        scalar_t radius = 0.0;  // Physical radius (m)
        scalar_t mass_conv = 0.0;  // Conventional mass (kg) - for comparison only
        
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
    };
    
    // System state for N-body simulation
    struct SystemState {
        std::vector<CelestialBody> bodies;
        time_t current_time = 0.0;
        scalar_t energy = 0.0;
        scalar_t angular_momentum = 0.0;
        
        // Calculate total energy (kinetic + potential from pressure fields)
        scalar_t calculate_total_energy() const {
            scalar_t E = 0.0;
            
            // Kinetic energy
            for (const auto& body : bodies) {
                E += 0.5 * body.mass_conv * body.velocity.squaredNorm();
            }
            
            // Potential energy from pressure gradients
            // Simplified: E_pot = -β ρ_s / r for each pair
            for (size_t i = 0; i < bodies.size(); ++i) {
                for (size_t j = i + 1; j < bodies.size(); ++j) {
                    const Vec3d r_vec = bodies[j].position - bodies[i].position;
                    const scalar_t r = r_vec.norm();
                    if (r > 0.0) {
                        // Potential from pressure field difference
                        const scalar_t beta_eff = std::sqrt(
                            bodies[i].sdt_params.beta * bodies[j].sdt_params.beta
                        );
                        E -= beta_eff * constants::rho_s / r;
                    }
                }
            }
            
            return E;
        }
        
        // Calculate total angular momentum
        scalar_t calculate_angular_momentum() const {
            Vec3d L_total = Vec3d::Zero();
            for (const auto& body : bodies) {
                L_total += body.mass_conv * body.position.cross(body.velocity);
            }
            return L_total.norm();
        }
    };
    
} // namespace sdt

