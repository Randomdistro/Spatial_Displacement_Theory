#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include <iomanip>

#include "sdt/core/constants.hpp"
#include "sdt/core/types.hpp"
#include "sdt/core/galactic_structure.hpp"
#include "sdt/physics/pressure_field.hpp"

using namespace sdt;

// Helper to calculate orbital velocity assuming circular orbit balance
// F_centripetal = m * v^2 / r = F_sdt
// v = sqrt(r * a_sdt)
scalar_t calculate_orbital_velocity(
    const CelestialBody& body,
    const std::vector<CelestialBody>& sources,
    const core::Galaxy& galaxy
) {
    // Calculate acceleration vector
    // Exclude self (though unlikely to be in sources usually)
    Vec3d accel = physics::PressureField::net_acceleration(
        body.position, 
        sources, 
        static_cast<size_t>(-1), // No self exclusion from external list check needed here if carefully managed
        true, // Apply screening
        galaxy.screening_strength,
        galaxy.screening_radius,
        galaxy.screening_alpha
    );
    
    // Calculate radial component of acceleration
    // r_vec from center (0,0,0)
    scalar_t r = body.position.norm();
    if (r == 0) return 0.0;
    
    Vec3d r_hat = body.position.normalized();
    scalar_t a_radial = -accel.dot(r_hat); // inward acceleration is positive radial force
    
    if (a_radial <= 0) return 0.0; // Pushed outward or no force?
    
    // v = sqrt(a * r)
    return std::sqrt(a_radial * r);
}

int main() {
    std::cout << "SDT Galaxy Rotation Curve Simulator (Phase 22)" << std::endl;
    std::cout << "===============================================" << std::endl;

    // 1. Setup Synthetic Galaxy (Milky Way-like)
    core::Galaxy galaxy;
    galaxy.name = "Milky_Way_Proxy";
    galaxy.screening_strength = 1.0e-3; // Standard SDT prediction
    galaxy.screening_radius = 1.0e21;   // ~30 kpc
    galaxy.screening_alpha = 1.0;       // Linear dependence region

    // Central SMBH (Sgr A*)
    // SDT: R_eff ~ 4e9 m driven by large c²·R_c acceleration scale
    // Conventional: 4e6 Solar Masses
    galaxy.central_black_hole.name = "Sgr_A_Star";
    galaxy.central_black_hole.position = Vec3d::Zero();
    galaxy.central_black_hole.velocity = Vec3d::Zero();
    galaxy.central_black_hole.radius = 1.2e10; 
    
    // SDT Params for SMBH
    galaxy.central_black_hole.sdt_params.R_eff = 1.0e7; // Placeholder R_eff for generating strong gravity
    galaxy.central_black_hole.sdt_params.k_factor = 20.0; // Low k_factor = high gravity
    // c²·R_c = c² * R_eff / k²
    galaxy.central_black_hole.sdt_params.c2_R_c = (constants::c * constants::c * galaxy.central_black_hole.sdt_params.R_eff) / 
                                                (galaxy.central_black_hole.sdt_params.k_factor * galaxy.central_black_hole.sdt_params.k_factor);
    galaxy.central_black_hole.sdt_params.is_active_source = true;

    // Components
    // 1. Bulge
    core::GalacticComponent bulge;
    bulge.type = core::GalacticComponent::Type::Bulge;
    bulge.radius = 5.0e19; // ~1.5 kpc
    bulge.num_particles = 100; // Test points
    galaxy.components.push_back(bulge);

    // 2. Disk
    core::GalacticComponent disk;
    disk.type = core::GalacticComponent::Type::Disk;
    disk.radius = 1.0e21; // ~30 kpc
    disk.scale_height = 1.0e19;
    disk.num_particles = 400; // Test points
    galaxy.components.push_back(disk);

    // Generate stars
    std::vector<CelestialBody> stars = core::generate_galaxy_particles(galaxy);
    std::cout << "Generated " << stars.size() << " test stars." << std::endl;

    // Sources list (Central BH + maybe All Stars for Self-Gravity?)
    // For rotation curve Phase 22, fundamental curve is usually dominated by potential.
    // Let's assume Bulge+Disk mass is significant.
    // In SDT, we need to treat them as sources.
    std::vector<CelestialBody> sources;
    sources.push_back(galaxy.central_black_hole);
    // Add all stars as sources too? That's N^2.
    // For 500 stars it's fine.
    sources.insert(sources.end(), stars.begin(), stars.end());

    std::cout << "Calculating rotation curve..." << std::endl;
    
    std::ofstream out_file("rotation_curve.csv");
    out_file << "r_kpc,v_km_s,v_newtonian_km_s,screening_factor\n";

    for (const auto& star : stars) {
        if (star.name == "Sgr_A_Star") continue; // Skip central

        scalar_t r = star.position.norm();
        if (r < 1.0e16) continue; // Skip very center

        // 1. Calculate v_SDT (with screening)
        scalar_t v_sdt = calculate_orbital_velocity(star, sources, galaxy);
        
        // 2. Calculate v_raw (without screening, raw SDT potential ~ c²R_c/r)
        // Just turn off screening in the call
        core::Galaxy raw_galaxy = galaxy;
        raw_galaxy.screening_strength = 0.0;
        scalar_t v_raw = calculate_orbital_velocity(star, sources, raw_galaxy);

        scalar_t screening = physics::PressureField::galactic_screening_factor(
            star.position, 
            galaxy.screening_strength,
            galaxy.screening_radius,
            galaxy.screening_alpha
        );

        // Convert to common units
        double r_kpc = r / (3.086e19); // m to kpc
        double v_kms = v_sdt / 1000.0;
        double v_raw_kms = v_raw / 1000.0;

        out_file << r_kpc << "," << v_kms << "," << v_raw_kms << "," << screening << "\n";
    }

    out_file.close();
    std::cout << "Done. Output saved to rotation_curve.csv" << std::endl;

    return 0;
}
