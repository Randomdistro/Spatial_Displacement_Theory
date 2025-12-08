#pragma once

#include "sdt/core/types.hpp"
#include "sdt/core/constants.hpp"
#include <vector>
#include <cmath>

namespace sdt::physics {

    // Pressure field calculator from SDT principles
    class PressureField {
    public:
        // Calculate pressure at position from a single source body
        static scalar_t pressure_at_position(
            const Vec3d& position,
            const CelestialBody& source
        ) {
            const Vec3d r_vec = position - source.position;
            const scalar_t r = r_vec.norm();
            return source.sdt_params.pressure_field(r);
        }
        
        // Calculate pressure gradient at position
        static Vec3d pressure_gradient(
            const Vec3d& position,
            const CelestialBody& source
        ) {
            const Vec3d r_vec = position - source.position;
            const scalar_t r = r_vec.norm();
            
            if (r <= 0.0) {
                return Vec3d::Zero();
            }
            
            // Pressure gradient: ∇Π = (β ρ_s / r³) * r_vec
            const scalar_t gradient_magnitude = source.sdt_params.beta * constants::rho_s / (r * r * r);
            return gradient_magnitude * r_vec;
        }
        
        // Calculate net acceleration from multiple sources
        static Vec3d net_acceleration(
            const Vec3d& position,
            const std::vector<CelestialBody>& sources,
            index_t exclude_index = static_cast<index_t>(-1)
        ) {
            Vec3d total_accel = Vec3d::Zero();
            
            for (size_t i = 0; i < sources.size(); ++i) {
                if (i == exclude_index) {
                    continue;
                }
                
                const Vec3d r_vec = position - sources[i].position;
                const scalar_t r = r_vec.norm();
                
                if (r <= 0.0) {
                    continue;
                }
                
                // Acceleration from pressure gradient: a = -∇Π / ρ_s
                // Simplified to: a = -β / r² * r_hat
                const Vec3d r_hat = r_vec.normalized();
                const scalar_t accel_mag = sources[i].sdt_params.beta / (r * r);
                total_accel -= accel_mag * r_hat;
            }
            
            return total_accel;
        }
        
        // Calculate total pressure field from multiple sources
        static scalar_t total_pressure(
            const Vec3d& position,
            const std::vector<CelestialBody>& sources
        ) {
            scalar_t total_p = constants::P_CMB;  // Background CMB pressure
            
            for (const auto& source : sources) {
                const Vec3d r_vec = position - source.position;
                const scalar_t r = r_vec.norm();
                
                if (r > 0.0) {
                    // Pressure deficit: ΔP = -β ρ_s / r
                    total_p -= source.sdt_params.beta * constants::rho_s / r;
                }
            }
            
            return total_p;
        }
        
        // Calculate mutual occlusion effect between two bodies
        // This accounts for the screening effect when bodies occlude each other's CMB access
        static scalar_t mutual_occlusion_factor(
            const CelestialBody& body1,
            const CelestialBody& body2
        ) {
            const Vec3d r_vec = body2.position - body1.position;
            const scalar_t r = r_vec.norm();
            
            if (r <= 0.0) {
                return 0.0;  // Bodies overlap - undefined
            }
            
            // Occlusion fraction ≈ solid angle / 4π
            // For small angles: Ω / 4π ≈ (π R²) / (4π r²) = R² / (4r²)
            // Simplified model: E = 1 - (R1 + R2)² / (4r²) for r >> R
            const scalar_t R_combined = body1.radius + body2.radius;
            
            if (r < R_combined) {
                return 1.0;  // Full occlusion
            }
            
            const scalar_t solid_angle_fraction = (R_combined * R_combined) / (4.0 * r * r);
            return std::max(0.0, std::min(1.0, solid_angle_fraction));
        }

        // Galactic Screening Factor (Phase 22)
        // xi_gal(r) = xi_0 * (r / R_gal)^alpha
        static scalar_t galactic_screening_factor(
            const Vec3d& position,
            scalar_t xi_0,
            scalar_t R_gal,
            scalar_t alpha
        ) {
            const scalar_t r = position.norm();
            if (r <= 0.0 || R_gal <= 0.0) return 0.0;
            
            return xi_0 * std::pow(r / R_gal, alpha);
        }

        // Calculate net acceleration from multiple sources with optional Galactic Screening
        static Vec3d net_acceleration(
            const Vec3d& position,
            const std::vector<CelestialBody>& sources,
            index_t exclude_index = static_cast<index_t>(-1),
            bool apply_galactic_screening = false,
            scalar_t xi_0 = 0.0,
            scalar_t R_gal = 1.0,
            scalar_t alpha = 1.0
        ) {
            Vec3d total_accel = Vec3d::Zero();
            
            // Pre-calculate screening for this position if enabled (scalar field approximation)
            scalar_t screening_factor = 0.0;
            if (apply_galactic_screening) {
                screening_factor = galactic_screening_factor(position, xi_0, R_gal, alpha);
                if (screening_factor > 0.99) screening_factor = 0.99; // Cap to avoid singularity
            }

            for (size_t i = 0; i < sources.size(); ++i) {
                if (i == exclude_index) {
                    continue;
                }
                
                const Vec3d r_vec = position - sources[i].position;
                const scalar_t r = r_vec.norm();
                
                if (r <= 0.0) {
                    continue;
                }
                
                // Acceleration from pressure gradient: a = -∇Π / ρ_s
                // Simplified to: a = -β / r² * r_hat
                const Vec3d r_hat = r_vec.normalized();
                
                // Apply screening: effective acceleration is reduced
                // a_eff = a_raw * (1 - screening_factor)
                const scalar_t accel_mag = (sources[i].sdt_params.beta / (r * r)) * (1.0 - screening_factor);
                total_accel -= accel_mag * r_hat;
            }
            
            return total_accel;
        }
    };

} // namespace sdt::physics

