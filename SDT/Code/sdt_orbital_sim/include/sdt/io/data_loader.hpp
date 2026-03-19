#pragma once

#include "sdt/core/types.hpp"
#include "sdt/core/constants.hpp"
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <regex>
#include <stdexcept>
#include <optional>
#include <map>

namespace sdt::io {

    // CSV parser utility
    class CSVParser {
    public:
        static std::vector<std::vector<std::string>> parse_file(const std::string& filename) {
            std::ifstream file(filename);
            if (!file.is_open()) {
                throw std::runtime_error("Cannot open file: " + filename);
            }
            
            std::vector<std::vector<std::string>> rows;
            std::string line;
            
            while (std::getline(file, line)) {
                // Skip empty lines and comments
                if (line.empty() || line[0] == '#') {
                    continue;
                }
                
                rows.push_back(parse_line(line));
            }
            
            return rows;
        }
        
    private:
        static std::vector<std::string> parse_line(const std::string& line) {
            std::vector<std::string> fields;
            std::stringstream ss(line);
            std::string field;
            
            while (std::getline(ss, field, ',')) {
                // Trim whitespace
                field.erase(0, field.find_first_not_of(" \t"));
                field.erase(field.find_last_not_of(" \t") + 1);
                fields.push_back(field);
            }
            
            return fields;
        }
    };
    
    // Planetary system data loader
    class PlanetarySystemLoader {
    public:
        // Load solar system from CSV
        static SystemState load_solar_system(const std::string& filename) {
            auto rows = CSVParser::parse_file(filename);
            
            if (rows.empty()) {
                throw std::runtime_error("Empty CSV file");
            }
            
            // Parse header
            std::map<std::string, size_t> column_map;
            const auto& header = rows[0];
            for (size_t i = 0; i < header.size(); ++i) {
                column_map[header[i]] = i;
            }
            
            SystemState system;
            
            // Find required columns
            auto get_column = [&](const std::string& name) -> std::optional<size_t> {
                auto it = column_map.find(name);
                if (it != column_map.end()) {
                    return it->second;
                }
                return std::nullopt;
            };
            
            const auto body_col = get_column("Body");
            const auto R_col = get_column("R");
            const auto a_col = get_column("a");
            const auto T_col = get_column("T");
            const auto k_factor_col = get_column("k_factor");
            
            if (!body_col || !R_col || !a_col || !T_col || !k_factor_col) {
                throw std::runtime_error("Missing required columns in CSV");
            }
            
            // Identify primary body (Sun)
            CelestialBody* sun = nullptr;
            for (size_t row_idx = 1; row_idx < rows.size(); ++row_idx) {
                const auto& row = rows[row_idx];
                if (row.size() <= std::max({*body_col, *R_col, *k_factor_col})) {
                    continue;
                }
                
                const std::string body_name = row[*body_col];
                const scalar_t R = parse_double(row[*R_col]);
                const scalar_t k_factor = parse_double(row[*k_factor_col]);
                
                if (body_name == "Sun" || body_name == "sun") {
                    CelestialBody body;
                    body.name = body_name;
                    body.type = "star";
                    body.radius = R;
                    body.sdt_params.kappa = k_factor;
                    body.sdt_params.R_eff = R;
                    body.sdt_params.z = 1.0 / (k_factor * k_factor);  // z * k² = 1
                    body.sdt_params.calculate_c2_R_c();
                    
                    system.bodies.push_back(body);
                    sun = &system.bodies.back();
                    break;
                }
            }
            
            if (!sun) {
                throw std::runtime_error("Primary body (Sun) not found in CSV");
            }
            
            // Load planets/satellites
            for (size_t row_idx = 1; row_idx < rows.size(); ++row_idx) {
                const auto& row = rows[row_idx];
                if (row.size() <= std::max({*body_col, *a_col, *T_col, *k_factor_col})) {
                    continue;
                }
                
                const std::string body_name = row[*body_col];
                if (body_name == "Sun" || body_name == "sun") {
                    continue;  // Already loaded
                }
                
                CelestialBody body;
                body.name = body_name;
                body.type = "planet";
                
                const scalar_t a = parse_double(row[*a_col]);
                const scalar_t T_obs = parse_double(row[*T_col]);
                
                // Use primary's k_factor for orbital calculations
                body.sdt_params.kappa = sun->sdt_params.kappa;
                body.sdt_params.R_eff = sun->radius;
                body.sdt_params.z = sun->sdt_params.z;
                body.sdt_params.c2_R_c = sun->sdt_params.c2_R_c;
                
                // Initialize orbit: circular orbit at semi-major axis
                body.position = Vec3d(a, 0.0, 0.0);
                const scalar_t v_orb = sun->sdt_params.orbital_velocity(a);
                body.velocity = Vec3d(0.0, v_orb, 0.0);
                
                // Get physical radius if available
                if (row.size() > *R_col && !row[*R_col].empty()) {
                    body.radius = parse_double(row[*R_col]);
                }
                
                system.bodies.push_back(body);
            }
            
            // Calculate initial energy and angular momentum
            system.energy = system.calculate_total_energy();
            system.angular_momentum = system.calculate_angular_momentum();
            
            return system;
        }
        
        // Load exoplanetary system
        static SystemState load_exoplanetary_system(
            const std::string& filename,
            const std::string& star_name
        ) {
            auto rows = CSVParser::parse_file(filename);
            
            if (rows.empty()) {
                throw std::runtime_error("Empty CSV file");
            }
            
            // Parse header
            std::map<std::string, size_t> column_map;
            const auto& header = rows[0];
            for (size_t i = 0; i < header.size(); ++i) {
                column_map[header[i]] = i;
            }
            
            SystemState system;
            
            // Load star (requires L, T_eff to calculate R, z, k)
            // This is simplified - full implementation would calculate from L, T_eff
            // For now, assume star parameters are provided
            
            return system;
        }
        
    private:
        static scalar_t parse_double(const std::string& str) {
            if (str.empty()) {
                return 0.0;
            }
            try {
                return std::stod(str);
            } catch (const std::exception&) {
                return 0.0;
            }
        }
    };

} // namespace sdt::io

