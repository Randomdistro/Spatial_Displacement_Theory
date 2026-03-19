#pragma once

#include "sdt/core/types.hpp"
#include <vector>
#include <random>

namespace sdt::core {

    // Component of a galaxy (Bulge, Disk, Halo placeholder)
    struct GalacticComponent {
        enum class Type {
            Bulge,
            Disk,
            Halo
        };

        Type type;
        scalar_t mass_eff;       // Effective mass proxy (for initialization)
        scalar_t radius;         // Characteristic radius (R_bulge or R_disk)
        scalar_t scale_height;   // For disk components
        size_t num_particles;    // Number of test particles to generate
    };

    // Galaxy definition
    struct Galaxy {
        std::string name;
        scalar_t distance;       // Distance from observer (for redshift, optional)
        
        // Central supermassive object
        CelestialBody central_black_hole;
        
        // Components
        std::vector<GalacticComponent> components;
        
        // Screening parameters (Phase 22)
        scalar_t screening_strength = 1.0e-3;  // xi_0
        scalar_t screening_radius = 1.0e21;    // R_gal (~30 kpc)
        scalar_t screening_alpha = 1.0;        // Radial dependence power
    };

    // Helper to generate test particles for a galaxy
    inline std::vector<CelestialBody> generate_galaxy_particles(const Galaxy& galaxy) {
        std::vector<CelestialBody> bodies;
        
        // Add Central Black Hole
        bodies.push_back(galaxy.central_black_hole);
        
        std::mt19937 gen(42); // Fixed seed for reproducibility
        std::normal_distribution<scalar_t> dist_z(0.0, 1.0);
        std::uniform_real_distribution<scalar_t> dist_phi(0.0, constants::two_pi);
        std::uniform_real_distribution<scalar_t> dist_u(0.0, 1.0);

        for (const auto& comp : galaxy.components) {
            for (size_t i = 0; i < comp.num_particles; ++i) {
                CelestialBody star;
                star.name = (comp.type == GalacticComponent::Type::Bulge ? "Bulge_" : "Disk_") + std::to_string(i);
                
                // Initialize positions based on component type
                scalar_t r = 0.0;
                scalar_t phi = dist_phi(gen);
                scalar_t z = 0.0;

                if (comp.type == GalacticComponent::Type::Bulge) {
                    // Bulge: Spherical distribution (Hernquist-like approximation)
                    scalar_t u = dist_u(gen);
                    r = comp.radius * u; // Simplified
                    // Random spherical
                    scalar_t theta = acos(1.0 - 2.0 * dist_u(gen));
                    scalar_t r_sphere = r; // use r as radial distance
                    
                    star.position = Vec3d(
                        r_sphere * sin(theta) * cos(phi),
                        r_sphere * sin(theta) * sin(phi),
                        r_sphere * cos(theta)
                    );
                } else if (comp.type == GalacticComponent::Type::Disk) {
                    // Disk: Exponential disk profile approximation
                    // P(r) ~ r * exp(-r/Rd)
                    // Simplified: just uniform spread up to radius for now to test rotation curve
                    // Better: Inverse transform sampling for exponential disk
                    scalar_t u = dist_u(gen);
                    r = -comp.radius * log(1.0 - u); // Inverse CDF of exponential
                    
                    // Cap at reasonable extent to avoid infinite tail
                    if (r > 5.0 * comp.radius) r = 5.0 * comp.radius;

                    z = comp.scale_height * dist_z(gen);
                    
                    star.position = Vec3d(
                        r * cos(phi),
                        r * sin(phi),
                        z
                    );
                }

                // Initialize velocity - circular orbit approximation based on SDT formula
                // v = (c/k) * sqrt(R_eff_central / r) for central domination
                // BUT we need N-body velocity initialization.
                // For now, start with 0 velocity, let the simulation or analyzer calculate v_circ
                // Or better: Set approximate Keplerian velocity to stabilize
                
                star.velocity = Vec3d::Zero(); // Will be calculated by simulation engine's orbit initializer
                
                // SDT Parameters for a star
                // Assume Sun-like for all test particles
                star.radius = 6.957e8; // Sun radius
                star.mass_param_gm = 0; // Not used
                
                // SDT specific
                star.sdt_params.R_eff = 3000.0; // Eff radius ~3km for Sun-like mass (placeholder)
                star.sdt_params.k_factor = 686.34;
                star.sdt_params.c2_R_c = (constants::c * constants::c * star.sdt_params.R_eff) / (star.sdt_params.k_factor * star.sdt_params.k_factor);
                star.sdt_params.is_active_source = true;

                bodies.push_back(star);
            }
        }
        
        return bodies;
    }

} // namespace sdt::core
