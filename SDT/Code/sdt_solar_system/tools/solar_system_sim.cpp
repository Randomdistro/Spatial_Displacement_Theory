#include "sdt/solar_system/n_body_system.hpp"
#include "sdt/solar_system/integrator.hpp"
#include "sdt/solar_system/data_loader.hpp"
#include "sdt/solar_system/constants.hpp"
#include <fmt/core.h>
#include <iostream>
#include <string>
#include <fstream>
#include <iomanip>
#include <chrono>

using namespace sdt::solar_system;

int main(int argc, char* argv[]) {
    try {
        // Parse command line arguments
        std::string data_file = "../../data/planetary_parameters.csv";
        time_t simulation_time = constants::billion_years_to_sec;  // 1 billion years
        time_t timestep = constants::default_timestep;  // 1 day
        bool use_occlusion = false;
        std::string output_file = "trajectory.csv";
        
        if (argc > 1) {
            data_file = argv[1];
        }
        if (argc > 2) {
            simulation_time = std::stod(argv[2]) * constants::year_to_sec;  // Convert years to seconds
        }
        if (argc > 3) {
            timestep = std::stod(argv[3]) * constants::day_to_sec;  // Convert days to seconds
        }
        if (argc > 4) {
            use_occlusion = (std::string(argv[4]) == "true" || std::string(argv[4]) == "1");
        }
        if (argc > 5) {
            output_file = argv[5];
        }
        
        fmt::print("SDT Solar System N-Body Simulator\n");
        fmt::print("==================================\n");
        fmt::print("Data file: {}\n", data_file);
        fmt::print("Simulation time: {:.2e} seconds ({:.2f} years)\n", 
                   simulation_time, simulation_time / constants::year_to_sec);
        fmt::print("Time step: {:.2e} seconds ({:.2f} days)\n", 
                   timestep, timestep / constants::day_to_sec);
        fmt::print("Use occlusion: {}\n", use_occlusion ? "yes" : "no");
        fmt::print("\n");
        
        // Load solar system bodies
        fmt::print("Loading solar system data...\n");
        auto bodies = DataLoader::load_from_csv(data_file);
        fmt::print("Loaded {} bodies\n", bodies.size());
        
        // Set initial conditions
        DataLoader::set_initial_conditions(bodies);
        
        // Create initial system state
        SystemState initial_state;
        initial_state.bodies = std::move(bodies);
        initial_state.current_time = 0.0;
        initial_state.total_energy = initial_state.calculate_total_energy();
        initial_state.total_angular_momentum = initial_state.calculate_angular_momentum_magnitude();
        
        fmt::print("Initial energy: {:.6e} J\n", initial_state.total_energy);
        fmt::print("Initial angular momentum: {:.6e} kg·m²/s\n", 
                   initial_state.total_angular_momentum);
        fmt::print("\n");
        
        // Create integrator
        std::unique_ptr<Integrator> integrator;
        if (use_occlusion) {
            integrator = std::make_unique<AdaptiveSymplecticIntegrator>(
                1e-9, constants::min_timestep, constants::max_timestep, true
            );
        } else {
            integrator = std::make_unique<AdaptiveSymplecticIntegrator>(
                1e-9, constants::min_timestep, constants::max_timestep, false
            );
        }
        integrator->set_dt(timestep);
        
        // Create n-body system
        NBodySystem system(std::move(initial_state), std::move(integrator));
        
        // Set up output callback to save trajectory
        std::ofstream traj_file(output_file);
        if (traj_file.is_open()) {
            // Write header
            traj_file << "time";
            for (const auto& body : system.get_state().bodies) {
                traj_file << fmt::format(",{}_x,{}_y,{}_z,{}_vx,{}_vy,{}_vz",
                    body.name, body.name, body.name,
                    body.name, body.name, body.name);
            }
            traj_file << "\n";
            
            // Output callback
            time_t last_output_time = 0.0;
            time_t output_interval = 365.25 * constants::day_to_sec;  // 1 year
            
            system.set_output_callback([&](const SystemState& state) {
                if (state.current_time - last_output_time >= output_interval) {
                    traj_file << std::scientific << std::setprecision(10) << state.current_time;
                    for (const auto& body : state.bodies) {
                        traj_file << fmt::format(",{:.10e},{:.10e},{:.10e},{:.10e},{:.10e},{:.10e}",
                            body.position.x(), body.position.y(), body.position.z(),
                            body.velocity.x(), body.velocity.y(), body.velocity.z());
                    }
                    traj_file << "\n";
                    last_output_time = state.current_time;
                }
            });
        }
        
        // Run simulation
        fmt::print("Starting simulation...\n");
        const auto start_time = std::chrono::steady_clock::now();
        
        system.run_until(simulation_time, 365.25 * constants::day_to_sec);
        
        const auto end_time = std::chrono::steady_clock::now();
        const auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(
            end_time - start_time).count();
        
        // Final state
        const auto& final_state = system.get_state();
        
        fmt::print("\nSimulation complete!\n");
        fmt::print("Final time: {:.6e} seconds ({:.2f} years)\n",
                   final_state.current_time,
                   final_state.current_time / constants::year_to_sec);
        fmt::print("Final energy: {:.6e} J\n", final_state.total_energy);
        fmt::print("Final angular momentum: {:.6e} kg·m²/s\n", 
                   final_state.total_angular_momentum);
        fmt::print("Energy drift: {:.6f}%\n", system.get_energy_drift());
        fmt::print("Angular momentum drift: {:.6f}%\n", 
                   system.get_angular_momentum_drift());
        fmt::print("Wall clock time: {} seconds\n", elapsed);
        fmt::print("Trajectory saved to: {}\n", output_file);
        
        traj_file.close();
        
        return 0;
    } catch (const std::exception& e) {
        fmt::print(stderr, "Error: {}\n", e.what());
        return 1;
    }
}

