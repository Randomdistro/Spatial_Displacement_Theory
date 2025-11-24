#include <iostream>
#include <fstream>
#include <iomanip>
#include <fmt/core.h>
#include <fmt/ostream.h>

#include "sdt/core/constants.hpp"
#include "sdt/core/types.hpp"
#include "sdt/numerics/integrator.hpp"
#include "sdt/simulation/engine.hpp"
#include "sdt/io/data_loader.hpp"
#include "sdt/analysis/validator.hpp"

using namespace sdt;

int main(int argc, char* argv[]) {
    try {
        // Parse command line arguments
        std::string data_file = "SDT/data/planetary_parameters.csv";
        std::string output_file = "simulation_output.csv";
        time_t simulation_time = 365.25 * constants::day_to_sec;  // 1 year
        time_t output_interval = 1.0 * constants::day_to_sec;  // Daily output
        time_t time_step = 3600.0;  // 1 hour
        
        if (argc > 1) {
            data_file = argv[1];
        }
        if (argc > 2) {
            output_file = argv[2];
        }
        if (argc > 3) {
            simulation_time = std::stod(argv[3]);
        }
        
        fmt::print("=== SDT Orbital Mechanics Simulation ===\n");
        fmt::print("Loading system from: {}\n", data_file);
        
        // Load initial system state
        SystemState initial_state = io::PlanetarySystemLoader::load_solar_system(data_file);
        
        fmt::print("Loaded {} celestial bodies\n", initial_state.bodies.size());
        for (const auto& body : initial_state.bodies) {
            fmt::print("  - {}: type={}, R={:.2e} m, κ={:.2f}\n",
                      body.name, body.type, body.radius, body.sdt_params.kappa);
        }
        
        // Create integrator
        auto integrator = std::make_unique<numerics::SymplecticIntegrator>();
        integrator->set_dt(time_step);
        
        // Create simulation engine
        simulation::SimulationEngine engine(std::move(initial_state), std::move(integrator));
        
        // Setup output
        std::ofstream out(output_file);
        out << std::scientific << std::setprecision(10);
        out << "# SDT Orbital Simulation Output\n";
        out << "# Time(s),";
        for (const auto& body : engine.get_state().bodies) {
            out << body.name << "_x(m)," << body.name << "_y(m)," << body.name << "_z(m),";
            out << body.name << "_vx(m/s)," << body.name << "_vy(m/s)," << body.name << "_vz(m/s),";
        }
        out << "Energy(J),Angular_Momentum(kg·m²/s)\n";
        
        engine.set_output_callback([&](const SystemState& state) {
            out << state.current_time << ",";
            for (const auto& body : state.bodies) {
                out << body.position.x() << "," << body.position.y() << "," << body.position.z() << ",";
                out << body.velocity.x() << "," << body.velocity.y() << "," << body.velocity.z() << ",";
            }
            out << state.energy << "," << state.angular_momentum << "\n";
        });
        
        fmt::print("\nStarting simulation...\n");
        fmt::print("  Simulation time: {:.2e} s ({:.2f} days)\n",
                  simulation_time, simulation_time / constants::day_to_sec);
        fmt::print("  Time step: {:.1f} s\n", time_step);
        fmt::print("  Output interval: {:.1f} s\n", output_interval);
        
        // Run simulation
        const auto start_time = std::chrono::steady_clock::now();
        engine.run_until(simulation_time, output_interval);
        const auto end_time = std::chrono::steady_clock::now();
        
        const auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
            end_time - start_time
        ).count();
        
        // Final output
        const auto final_state = engine.get_state();
        out << final_state.current_time << ",";
        for (const auto& body : final_state.bodies) {
            out << body.position.x() << "," << body.position.y() << "," << body.position.z() << ",";
            out << body.velocity.x() << "," << body.velocity.y() << "," << body.velocity.z() << ",";
        }
        out << final_state.energy << "," << final_state.angular_momentum << "\n";
        out.close();
        
        fmt::print("\nSimulation complete!\n");
        fmt::print("  Steps: {}\n", engine.get_step_count());
        fmt::print("  Elapsed time: {} ms\n", elapsed);
        fmt::print("  Energy drift: {:.6e} %\n", engine.get_energy_drift());
        fmt::print("  Angular momentum drift: {:.6e} %\n", engine.get_angular_momentum_drift());
        fmt::print("  Output written to: {}\n", output_file);
        
        // Validation report
        fmt::print("\n=== Validation Report ===\n");
        fmt::print("Energy conservation: {:.6e} % drift\n", engine.get_energy_drift());
        fmt::print("Angular momentum conservation: {:.6e} % drift\n",
                  engine.get_angular_momentum_drift());
        
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}

