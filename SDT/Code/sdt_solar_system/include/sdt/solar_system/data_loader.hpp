#pragma once

#include "celestial_body.hpp"
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <cmath>

namespace sdt::solar_system {

    // Load solar system bodies from CSV file
    class DataLoader {
    public:
        // Load bodies from planetary_parameters.csv
        // Format: Body,R,a,T,v_orbital,k_factor,SDT_predicted_T,Error
        static std::vector<CelestialBody> load_from_csv(const std::string& filename) {
            std::vector<CelestialBody> bodies;
            
            std::ifstream file(filename);
            if (!file.is_open()) {
                throw std::runtime_error("Cannot open file: " + filename);
            }
            
            std::string line;
            bool first_line = true;
            
            while (std::getline(file, line)) {
                // Skip comments and empty lines
                if (line.empty() || line[0] == '#') {
                    continue;
                }
                
                // Skip header line
                if (first_line) {
                    first_line = false;
                    continue;
                }
                
                // Parse CSV line
                std::istringstream iss(line);
                std::string token;
                std::vector<std::string> tokens;
                
                while (std::getline(iss, token, ',')) {
                    tokens.push_back(token);
                }
                
                if (tokens.size() < 6) {
                    continue;  // Skip incomplete lines
                }
                
                CelestialBody body;
                body.name = tokens[0];
                
                // Parse values
                try {
                    body.radius = std::stod(tokens[1]);  // R (m)
                    const scalar_t a = std::stod(tokens[2]);  // Semi-major axis (m)
                    const scalar_t T = std::stod(tokens[3]);  // Period (s)
                    const scalar_t v_orbital = std::stod(tokens[4]);  // Orbital velocity (m/s)
                    const scalar_t k_factor = std::stod(tokens[5]);  // Ϟ (kappa)
                    
                    // Set SDT parameters
                    body.sdt_params.kappa = k_factor;
                    
                    // For primary bodies (Sun, planets), R_eff = R
                    // For satellites, R_eff is the primary's radius
                    if (body.radius > 0.0) {
                        body.sdt_params.R_eff = body.radius;
                    } else {
                        // Satellite - need to find primary
                        // For now, use Sun's R_eff as default
                        body.sdt_params.R_eff = 6.957e8;  // Sun's radius
                    }
                    
                    // Determine body type from name
                    if (body.name == "Sun") {
                        body.type = "star";
                    } else if (body.name.find("Moon") != std::string::npos ||
                               body.name == "Io" || body.name == "Europa" ||
                               body.name == "Ganymede" || body.name == "Callisto" ||
                               body.name == "Titan" || body.name == "Enceladus" ||
                               body.name == "Phobos" || body.name == "Deimos" ||
                               body.name == "Triton" || body.name == "Miranda" ||
                               body.name == "Ariel" || body.name == "Umbriel" ||
                               body.name == "Titania" || body.name == "Oberon") {
                        body.type = "moon";
                    } else if (body.name.find("Comet") != std::string::npos ||
                               body.name.find("Halley") != std::string::npos ||
                               body.name.find("Hale") != std::string::npos ||
                               body.name.find("Churyumov") != std::string::npos ||
                               body.name.find("Encke") != std::string::npos) {
                        body.type = "comet";
                    } else if (body.name == "Ceres" || body.name == "Vesta" ||
                               body.name == "Pallas" || body.name == "Hygiea" ||
                               body.name.find("asteroid") != std::string::npos) {
                        body.type = "asteroid";
                    } else {
                        body.type = "planet";
                    }
                    
                    // Set initial position (circular orbit assumption)
                    // Place at semi-major axis along x-axis
                    if (a > 0.0) {
                        body.position = Vec3d(a, 0.0, 0.0);
                        
                        // Set initial velocity (circular orbit)
                        // v = 2πa / T or use orbital velocity directly
                        if (v_orbital > 0.0) {
                            body.velocity = Vec3d(0.0, v_orbital, 0.0);
                        } else if (T > 0.0) {
                            const scalar_t v = 2.0 * 3.14159265358979323846 * a / T;
                            body.velocity = Vec3d(0.0, v, 0.0);
                        }
                    }
                    
                    // Estimate mass from radius (for energy calculations)
                    // Rough approximation: density ~ 5000 kg/m³ for planets
                    if (body.radius > 0.0) {
                        const scalar_t volume = (4.0 / 3.0) * 3.14159265358979323846 * 
                                              body.radius * body.radius * body.radius;
                        body.mass_conv = 5000.0 * volume;  // Rough estimate
                    }
                    
                    bodies.push_back(body);
                } catch (const std::exception& e) {
                    // Skip lines with parse errors
                    continue;
                }
            }
            
            return bodies;
        }
        
        // Load initial conditions from JPL ephemerides format
        // Simplified: just set positions and velocities from orbital elements
        static void set_initial_conditions(
            std::vector<CelestialBody>& bodies,
            const std::string& sun_name = "Sun"
        ) {
            // Find Sun
            CelestialBody* sun = nullptr;
            for (auto& body : bodies) {
                if (body.name == sun_name) {
                    sun = &body;
                    break;
                }
            }
            
            if (!sun) {
                // No sun found, place Sun at origin
                for (auto& body : bodies) {
                    if (body.type == "star") {
                        body.position = Vec3d::Zero();
                        body.velocity = Vec3d::Zero();
                        sun = &body;
                        break;
                    }
                }
            }
            
            if (!sun) {
                throw std::runtime_error("No Sun found in bodies list");
            }
            
            // Set Sun at origin
            sun->position = Vec3d::Zero();
            sun->velocity = Vec3d::Zero();
            
            // For other bodies, use their orbital parameters
            // This is a simplified version - full implementation would use
            // proper orbital elements (a, e, i, Ω, ω, M)
            for (auto& body : bodies) {
                if (&body == sun) {
                    continue;
                }
                
                // Use existing position/velocity if already set
                // Otherwise calculate from orbital parameters
                if (body.position.norm() > 0.0 && body.velocity.norm() > 0.0) {
                    continue;  // Already set
                }
                
                // Simplified: circular orbits
                const scalar_t r = body.position.norm();
                if (r > 0.0) {
                    // Calculate orbital velocity from SDT parameters
                    const scalar_t v = sun->sdt_params.orbital_velocity(r);
                    const Vec3d r_hat = body.position.normalized();
                    const Vec3d v_hat = Vec3d(-r_hat.y(), r_hat.x(), 0.0).normalized();
                    body.velocity = v * v_hat;
                }
            }
        }
    };

} // namespace sdt::solar_system

