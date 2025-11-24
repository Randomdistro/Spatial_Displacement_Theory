#include "sdt/visualization/orbit_viewer.hpp"
#include "sdt/visualization/trajectory_loader.hpp"
#include "sdt/io/data_loader.hpp"
#include "sdt/io/spectral_loader.hpp"
#include "sdt/core/constants.hpp"
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    try {
        std::string simulation_file;
        std::string spectral_file;
        std::string body_name;
        
        if (argc < 2) {
            std::cout << "Usage: " << argv[0] << " <simulation_output.csv> [spectral_data.csv] [body_name]\n";
            std::cout << "Example: " << argv[0] << " output.csv rv_data.csv HD209458\n";
            return 1;
        }
        
        simulation_file = argv[1];
        if (argc >= 3) {
            spectral_file = argv[2];
        }
        if (argc >= 4) {
            body_name = argv[3];
        }
        
        // Create viewer
        sdt::visualization::OrbitViewer3D viewer;
        viewer.initialize(1920, 1080);
        
        // Load simulation trajectories
        std::cout << "Loading simulation data from: " << simulation_file << std::endl;
        auto trajectories = sdt::visualization::load_trajectories_from_csv(simulation_file);
        
        for (auto& traj : trajectories) {
            // Set colors based on body type
            auto colors = sdt::visualization::create_solar_system_colors();
            if (colors.count(traj.body_name)) {
                traj.color = colors[traj.body_name];
            } else {
                traj.color = viewer.get_default_color("planet");
            }
            
            viewer.add_trajectory(traj);
        }
        
        // Load spectral data if provided
        if (!spectral_file.empty()) {
            std::cout << "Loading spectral data from: " << spectral_file << std::endl;
            auto spectral_data = sdt::io::SpectralDataLoader::load(spectral_file);
            
            if (!spectral_data.empty()) {
                std::cout << "Loaded " << spectral_data.size() << " spectral data points\n";
                
                // Find orbital period from spectral data
                double period = sdt::io::SpectralDataLoader::find_orbital_period(spectral_data);
                std::cout << "Detected orbital period: " << period / sdt::constants::day_to_sec 
                         << " days\n";
                
                // Load primary body (need SDT parameters)
                // For now, create a placeholder - full implementation would load from data
                sdt::CelestialBody primary;
                primary.name = "Star";
                primary.type = "star";
                primary.sdt_params.kappa = 686.34;  // Solar value
                primary.sdt_params.R_eff = 6.957e8;  // Solar radius
                primary.sdt_params.calculate_beta();
                primary.position = sdt::Vec3d::Zero();
                
                // Convert spectral data to orbit
                if (body_name.empty()) {
                    body_name = "Planet";
                }
                
                viewer.convert_spectral_to_orbit(
                    body_name,
                    spectral_data,
                    primary,
                    period,
                    90.0  // Edge-on (typical for RV detections)
                );
                
                std::cout << "Converted spectral data to 3D orbit for: " << body_name << std::endl;
            }
        }
        
        // Setup camera for good viewing angle
        viewer.set_camera_position(5e12, 5e12, 5e12);
        viewer.set_camera_focal_point(0, 0, 0);
        viewer.set_camera_view_up(0, 0, 1);
        
        std::cout << "\n=== SDT 3D Orbit Viewer ===\n";
        std::cout << "Controls:\n";
        std::cout << "  Mouse drag: Rotate view\n";
        std::cout << "  Mouse wheel: Zoom\n";
        std::cout << "  'q' or close window: Quit\n";
        std::cout << "\nStarting interactive viewer...\n";
        
        // Render and start interaction
        viewer.render();
        viewer.start_interactor();
        
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}

