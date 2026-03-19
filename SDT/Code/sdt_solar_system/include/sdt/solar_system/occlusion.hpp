#pragma once

#include "celestial_body.hpp"
#include "pressure_field.hpp"
#include "constants.hpp"
#include <cmath>
#include <algorithm>
#include <limits>

namespace sdt::solar_system {

    // Mutual occlusion calculations
    // Bodies occlude each other's access to CMB pressure field
    // From Phase 1: occlusion fraction ≈ solid angle / 4π ≈ R² / (4r²)
    class Occlusion {
    public:
        // Calculate mutual occlusion factor between two bodies
        // Returns fraction of CMB pressure that is occluded (0 to 1)
        // From Phase 1: E = R² / (4r²) for small angles
        static scalar_t mutual_occlusion_factor(
            const CelestialBody& body1,
            const CelestialBody& body2
        ) {
            const Vec3d r_vec = body2.position - body1.position;
            const scalar_t r = r_vec.norm();
            
            if (r <= 0.0) {
                return 1.0;  // Bodies overlap - full occlusion
            }
            
            // Combined radius
            const scalar_t R_combined = body1.radius + body2.radius;
            
            if (r < R_combined) {
                return 1.0;  // Bodies overlap - full occlusion
            }
            
            // Solid angle fraction: Ω / 4π ≈ (π R²) / (4π r²) = R² / (4r²)
            // For small angles, this is a good approximation
            const scalar_t solid_angle_fraction = (R_combined * R_combined) / (4.0 * r * r);
            
            // Clamp to [0, 1]
            return std::max(0.0, std::min(1.0, solid_angle_fraction));
        }
        
        // Calculate occlusion-corrected pressure at position
        // Accounts for bodies blocking CMB pressure from certain directions
        static scalar_t occlusion_corrected_pressure(
            const Vec3d& position,
            const CelestialBody& source,
            const std::vector<CelestialBody>& occluding_bodies
        ) {
            // Base pressure from source
            scalar_t pressure = PressureField::pressure_at_position(position, source);
            
            // Reduce pressure based on occlusion by other bodies
            for (const auto& occluder : occluding_bodies) {
                // Skip if occluder is the source
                if (&occluder == &source) {
                    continue;
                }
                
                // Calculate occlusion factor
                const scalar_t occlusion = mutual_occlusion_factor(occluder, source);
                
                // Reduce pressure proportionally
                // Simplified model: pressure reduction = occlusion * pressure_deficit
                const Vec3d r_vec = position - source.position;
                const scalar_t r = r_vec.norm();
                if (r > 0.0) {
                    const scalar_t beta = source.sdt_params.c2_R_c();
                    const scalar_t pressure_deficit = beta * constants::rho_s / r;
                    pressure += occlusion * pressure_deficit * 0.1;  // Small correction factor
                }
            }
            
            return pressure;
        }
        
        // Calculate net acceleration with occlusion corrections
        static Vec3d occlusion_corrected_acceleration(
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
                
                // Base acceleration
                const Vec3d r_hat = r_vec.normalized();
                const scalar_t beta = sources[i].sdt_params.c2_R_c();
                scalar_t accel_mag = beta / (r * r);
                
                // Apply occlusion corrections from other bodies
                for (size_t j = 0; j < sources.size(); ++j) {
                    if (j == i || j == exclude_index) {
                        continue;
                    }
                    
                    // Calculate how much body j occludes body i's pressure field
                    const scalar_t occlusion = mutual_occlusion_factor(sources[j], sources[i]);
                    
                    // Reduce acceleration based on occlusion
                    // Simplified: reduce by small fraction proportional to occlusion
                    accel_mag *= (1.0 - 0.05 * occlusion);  // 5% reduction per unit occlusion
                }
                
                total_accel -= accel_mag * r_hat;
            }
            
            return total_accel;
        }
    };

} // namespace sdt::solar_system

