#pragma once

#include "celestial_body.hpp"
#include "integrator.hpp"
#include <string>
#include <vector>
#include <fstream>
#include <iomanip>

namespace sdt::solar_system {

    // 3D visualization and trajectory export
    class Visualizer {
    public:
        // Export trajectory to CSV format
        static void export_to_csv(
            const SystemState& state,
            const std::string& filename
        ) {
            std::ofstream file(filename);
            if (!file.is_open()) {
                throw std::runtime_error("Cannot open file: " + filename);
            }
            
            // Write header
            file << "time";
            for (const auto& body : state.bodies) {
                file << "," << body.name << "_x," << body.name << "_y," << body.name << "_z";
                file << "," << body.name << "_vx," << body.name << "_vy," << body.name << "_vz";
            }
            file << "\n";
            
            // Write data
            file << std::scientific << std::setprecision(10) << state.current_time;
            for (const auto& body : state.bodies) {
                file << "," << body.position.x() << "," << body.position.y() << "," << body.position.z();
                file << "," << body.velocity.x() << "," << body.velocity.y() << "," << body.velocity.z();
            }
            file << "\n";
        }
        
        // Export trajectory to XYZ format (for visualization tools)
        static void export_to_xyz(
            const SystemState& state,
            const std::string& filename
        ) {
            std::ofstream file(filename);
            if (!file.is_open()) {
                throw std::runtime_error("Cannot open file: " + filename);
            }
            
            // Write header
            file << state.bodies.size() << "\n";
            file << "Time: " << state.current_time << " s\n";
            
            // Write atom positions (using body names as element symbols)
            for (const auto& body : state.bodies) {
                // Use first letter of body name as element symbol
                std::string symbol = body.name.substr(0, 1);
                if (symbol.length() > 0 && symbol[0] >= 'a' && symbol[0] <= 'z') {
                    symbol[0] = symbol[0] - 'a' + 'A';  // Uppercase
                }
                
                file << symbol << " "
                     << std::scientific << std::setprecision(10)
                     << body.position.x() / 1e9 << " "  // Convert to km
                     << body.position.y() / 1e9 << " "
                     << body.position.z() / 1e9 << "\n";
            }
        }
        
        // Export to VTK format (for ParaView)
        static void export_to_vtk(
            const SystemState& state,
            const std::string& filename
        ) {
            std::ofstream file(filename);
            if (!file.is_open()) {
                throw std::runtime_error("Cannot open file: " + filename);
            }
            
            // VTK header
            file << "# vtk DataFile Version 2.0\n";
            file << "SDT Solar System Trajectory\n";
            file << "ASCII\n";
            file << "DATASET POLYDATA\n";
            
            // Points
            file << "POINTS " << state.bodies.size() << " double\n";
            for (const auto& body : state.bodies) {
                file << std::scientific << std::setprecision(10)
                     << body.position.x() << " "
                     << body.position.y() << " "
                     << body.position.z() << "\n";
            }
            
            // Vertices (one per body)
            file << "VERTICES " << state.bodies.size() << " " 
                 << (2 * state.bodies.size()) << "\n";
            for (size_t i = 0; i < state.bodies.size(); ++i) {
                file << "1 " << i << "\n";
            }
            
            // Point data (velocities)
            file << "POINT_DATA " << state.bodies.size() << "\n";
            file << "VECTORS velocity double\n";
            for (const auto& body : state.bodies) {
                file << std::scientific << std::setprecision(10)
                     << body.velocity.x() << " "
                     << body.velocity.y() << " "
                     << body.velocity.z() << "\n";
            }
            
            // Scalars (body names as IDs)
            file << "SCALARS body_id int 1\n";
            file << "LOOKUP_TABLE default\n";
            for (size_t i = 0; i < state.bodies.size(); ++i) {
                file << i << "\n";
            }
        }
        
        // Export trajectory history to CSV
        static void export_trajectory_history(
            const std::vector<SystemState>& history,
            const std::string& filename
        ) {
            std::ofstream file(filename);
            if (!file.is_open()) {
                throw std::runtime_error("Cannot open file: " + filename);
            }
            
            if (history.empty()) {
                return;
            }
            
            // Write header
            file << "time";
            for (const auto& body : history[0].bodies) {
                file << "," << body.name << "_x," << body.name << "_y," << body.name << "_z";
            }
            file << "\n";
            
            // Write data
            for (const auto& state : history) {
                file << std::scientific << std::setprecision(10) << state.current_time;
                for (const auto& body : state.bodies) {
                    file << "," << body.position.x() << "," << body.position.y() << "," << body.position.z();
                }
                file << "\n";
            }
        }
    };

} // namespace sdt::solar_system


