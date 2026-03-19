#pragma once

#include "celestial_body.hpp"
#include "constants.hpp"
#include <vector>
#include <cmath>
#include <limits>

namespace sdt::solar_system {

    // CMB pressure field calculator for n-body systems
    // From Phase 15: Π_s(r) = P_CMB - κ V_total K_bulk / (4π r)
    class PressureField {
    public:
        // Calculate pressure at position from a single source body
        // From Phase 15: Π_s(r) = P_CMB - κ V_total K_bulk / (4π r)
        // Using SDT parameters: pressure deficit = β ρ_s / r
        static scalar_t pressure_at_position(
            const Vec3d& position,
            const CelestialBody& source
        ) {
            const Vec3d r_vec = position - source.position;
            const scalar_t r = r_vec.norm();
            
            if (r <= 0.0) {
                return constants::P_CMB;  // At origin, pressure equals CMB pressure
            }
            
            // Pressure deficit: ΔΠ = -β ρ_s / r
            // From Phase 15: β = c² R_eff / Ϟ²
            const scalar_t beta = source.sdt_params.c2_R_c();
            const scalar_t pressure_deficit = beta * constants::rho_s / r;
            
            return constants::P_CMB - pressure_deficit;
        }
        
        // Calculate pressure gradient at position
        // From Phase 15: ∇Π = +κ V_total K_bulk / (4π r²) = +β ρ_s / r²
        static Vec3d pressure_gradient(
            const Vec3d& position,
            const CelestialBody& source
        ) {
            const Vec3d r_vec = position - source.position;
            const scalar_t r = r_vec.norm();
            
            if (r <= 0.0) {
                return Vec3d::Zero();
            }
            
            // Pressure gradient magnitude: dΠ/dr = +β ρ_s / r²
            const scalar_t beta = source.sdt_params.c2_R_c();
            const scalar_t gradient_magnitude = beta * constants::rho_s / (r * r);
            
            const Vec3d r_hat = r_vec.normalized();
            return gradient_magnitude * r_hat;
        }
        
        // Calculate net acceleration from multiple sources
        // From Phase 15: a(r) = -c² R_eff / (Ϟ² r²) = -β / r²
        static Vec3d net_acceleration(
            const Vec3d& position,
            const std::vector<CelestialBody>& sources,
            size_t exclude_index = std::numeric_limits<size_t>::max()
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
                
                // Acceleration from pressure gradient: a = -β / r² * r_hat
                // From Phase 15: a(r) = -c² R_eff / (Ϟ² r²)
                const Vec3d r_hat = r_vec.normalized();
                const scalar_t beta = sources[i].sdt_params.c2_R_c();
                const scalar_t accel_mag = beta / (r * r);
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
                    const scalar_t beta = source.sdt_params.c2_R_c();
                    total_p -= beta * constants::rho_s / r;
                }
            }
            
            return total_p;
        }
    };

} // namespace sdt::solar_system

