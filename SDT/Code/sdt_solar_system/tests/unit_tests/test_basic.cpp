#include "sdt/solar_system/celestial_body.hpp"
#include "sdt/solar_system/pressure_field.hpp"
#include "sdt/solar_system/integrator.hpp"
#include "sdt/solar_system/constants.hpp"
#include <cassert>
#include <cmath>
#include <iostream>

using namespace sdt::solar_system;

void test_sdt_parameters() {
    std::cout << "Testing SDT parameters...\n";
    
    SDTParameters params;
    params.kappa = 686.42;  // Sun's kappa
    params.R_eff = 6.957e8;  // Sun's radius
    
    // Test beta calculation
    const scalar_t beta = params.beta();
    assert(beta > 0.0);
    std::cout << "  Beta: " << beta << "\n";
    
    // Test orbital velocity at 1 AU
    const scalar_t r = constants::AU;
    const scalar_t v = params.orbital_velocity(r);
    assert(v > 0.0 && v < constants::c);
    std::cout << "  Orbital velocity at 1 AU: " << v << " m/s\n";
    
    // Test orbital period
    const scalar_t T = params.orbital_period(r);
    assert(T > 0.0);
    std::cout << "  Orbital period at 1 AU: " << T / constants::year_to_sec << " years\n";
    
    std::cout << "  SDT parameters test passed!\n\n";
}

void test_pressure_field() {
    std::cout << "Testing pressure field...\n";
    
    CelestialBody sun;
    sun.name = "Sun";
    sun.position = Vec3d::Zero();
    sun.sdt_params.kappa = 686.42;
    sun.sdt_params.R_eff = 6.957e8;
    
    // Test pressure at 1 AU
    const Vec3d pos = Vec3d(constants::AU, 0.0, 0.0);
    const scalar_t pressure = PressureField::pressure_at_position(pos, sun);
    
    // Pressure should be less than CMB pressure
    assert(pressure < constants::P_CMB);
    std::cout << "  Pressure at 1 AU: " << pressure << " Pa\n";
    std::cout << "  CMB pressure: " << constants::P_CMB << " Pa\n";
    
    // Test pressure gradient
    const Vec3d gradient = PressureField::pressure_gradient(pos, sun);
    assert(gradient.norm() > 0.0);
    std::cout << "  Pressure gradient magnitude: " << gradient.norm() << " Pa/m\n";
    
    // Test acceleration
    const Vec3d accel = PressureField::net_acceleration(pos, {sun});
    assert(accel.norm() > 0.0);
    std::cout << "  Acceleration magnitude: " << accel.norm() << " m/s²\n";
    
    std::cout << "  Pressure field test passed!\n\n";
}

void test_integrator() {
    std::cout << "Testing integrator...\n";
    
    // Create simple two-body system (Sun-Earth)
    SystemState state;
    
    CelestialBody sun;
    sun.name = "Sun";
    sun.position = Vec3d::Zero();
    sun.velocity = Vec3d::Zero();
    sun.sdt_params.kappa = 686.42;
    sun.sdt_params.R_eff = 6.957e8;
    sun.mass_conv = 1.9885e30;  // For energy calculations
    
    CelestialBody earth;
    earth.name = "Earth";
    earth.position = Vec3d(constants::AU, 0.0, 0.0);
    const scalar_t v_orbital = sun.sdt_params.orbital_velocity(constants::AU);
    earth.velocity = Vec3d(0.0, v_orbital, 0.0);
    earth.sdt_params.kappa = 686.42;  // Uses Sun's kappa
    earth.sdt_params.R_eff = 6.371e6;
    earth.mass_conv = 5.972e24;
    
    state.bodies = {sun, earth};
    state.current_time = 0.0;
    
    // Calculate initial energy
    const scalar_t E0 = state.calculate_total_energy();
    std::cout << "  Initial energy: " << E0 << " J\n";
    
    // Integrate for 1 year
    SymplecticIntegrator integrator;
    const time_t dt = constants::day_to_sec;  // 1 day
    const time_t one_year = constants::year_to_sec;
    
    for (time_t t = 0; t < one_year; t += dt) {
        integrator.step(state, dt);
    }
    
    // Calculate final energy
    const scalar_t E1 = state.calculate_total_energy();
    std::cout << "  Final energy: " << E1 << " J\n";
    
    // Energy should be conserved (within numerical precision)
    const scalar_t energy_drift = std::abs((E1 - E0) / E0) * 100.0;
    std::cout << "  Energy drift: " << energy_drift << "%\n";
    assert(energy_drift < 1.0);  // Should be < 1% for symplectic integrator
    
    std::cout << "  Integrator test passed!\n\n";
}

int main() {
    std::cout << "Running SDT Solar System Unit Tests\n";
    std::cout << "===================================\n\n";
    
    try {
        test_sdt_parameters();
        test_pressure_field();
        test_integrator();
        
        std::cout << "All tests passed!\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Test failed: " << e.what() << "\n";
        return 1;
    }
}



