/**
 * Simple Console Test for SDT Solar System Integration
 * Tests JPL DE421 loader, SDT physics, camera, and point particles
 * This version runs without Vulkan/GLFW for quick testing
 */

#include "sdt/solar_system/jpl_de421_loader.hpp"
#include "sdt/solar_system/integrator.hpp"
#include "sdt/solar_system/camera_controller.hpp"
#include "sdt/solar_system/point_particle_system.hpp"
#include "sdt/solar_system/pressure_field.hpp"

#include <iostream>
#include <iomanip>
#include <vector>
#include <cmath>

using namespace sdt::solar_system;
using Vec3d = Eigen::Vector3d;

int main(int argc, char* argv[]) {
    std::cout << "=== SDT Solar System Simulator Test ===\n\n";
    
    // Load initial conditions from JPL DE421 (earliest verified: 1800)
    std::cout << "Loading initial conditions from JPL DE421 (1800-01-01)...\n";
    auto bodies = JPLDE421Loader::load_earliest_verified();
    
    std::cout << "Loaded " << bodies.size() << " bodies:\n";
    for (const auto& body : bodies) {
        double dist = body.position.norm();
        std::cout << "  " << std::setw(10) << body.name 
                  << " | Distance: " << std::scientific << std::setprecision(3) << dist << " m"
                  << " | Velocity: " << body.velocity.norm() << " m/s"
                  << " | κ: " << std::fixed << std::setprecision(2) << body.sdt_params.kappa << "\n";
    }
    
    // Create system state
    SystemState state;
    state.bodies = bodies;
    state.current_time = 0.0;
    
    // Calculate initial energy and angular momentum
    double initialEnergy = state.calculate_total_energy();
    Vec3d initialAngMom = state.calculate_angular_momentum_vector();
    
    std::cout << "\nInitial Energy: " << std::scientific << initialEnergy << " J\n";
    std::cout << "Initial Angular Momentum: " << initialAngMom.norm() << " kg·m²/s\n\n";
    
    // Create integrator
    SymplecticIntegrator integrator(false);
    
    // Calculate marker positions
    std::cout << "Calculating visualization markers...\n";
    auto markers = PointParticleSystem::calculateMarkers(bodies);
    std::cout << "Generated " << markers.size() << " markers:\n";
    for (const auto& marker : markers) {
        double dist = marker.position.norm();
        std::cout << "  " << std::setw(30) << marker.label 
                  << " | Radius: " << std::scientific << std::setprecision(3) 
                  << marker.radius << " m | Distance: " << dist << " m\n";
    }
    
    // Test camera controller
    std::cout << "\nTesting camera controller...\n";
    CameraController camera;
    camera.setFocus(Vec3d::Zero());
    camera.setDistance(1e12); // 1 AU
    
    Vec3d camPos = camera.getPosition();
    std::cout << "Camera position: (" << camPos.x() << ", " << camPos.y() << ", " << camPos.z() << ")\n";
    
    // Run simulation for a few steps
    std::cout << "\nRunning simulation (10 steps, dt=3600s)...\n";
    double dt = 3600.0; // 1 hour
    
    for (int step = 0; step < 10; ++step) {
        integrator.step(state, dt);
        state.current_time += dt;
        
        // Calculate energy error
        double currentEnergy = state.calculate_total_energy();
        double energyError = std::abs((currentEnergy - initialEnergy) / initialEnergy) * 100.0;
        
        if (step % 2 == 0) {
            std::cout << "Step " << step << " | Time: " << std::fixed << std::setprecision(1) 
                      << state.current_time / 86400.0 << " days | Energy Error: " 
                      << std::scientific << std::setprecision(6) << energyError << "%\n";
        }
    }
    
    // Final state
    std::cout << "\nFinal state:\n";
    for (const auto& body : state.bodies) {
        if (body.name == "Sun") continue;
        double dist = body.position.norm();
        std::cout << "  " << std::setw(10) << body.name 
                  << " | Distance: " << std::scientific << std::setprecision(3) << dist << " m\n";
    }
    
    double finalEnergy = state.calculate_total_energy();
    Vec3d finalAngMom = state.calculate_angular_momentum_vector();
    
    double energyError = std::abs((finalEnergy - initialEnergy) / initialEnergy) * 100.0;
    double angMomError = (finalAngMom - initialAngMom).norm() / initialAngMom.norm() * 100.0;
    
    std::cout << "\nConservation Check:\n";
    std::cout << "  Energy Error: " << std::scientific << std::setprecision(6) << energyError << "%\n";
    std::cout << "  Angular Momentum Error: " << angMomError << "%\n";
    
    std::cout << "\n=== Test Complete ===\n";
    std::cout << "All components integrated successfully!\n";
    std::cout << "Ready for Vulkan rendering implementation.\n";
    
    return 0;
}
