#pragma once

#include <numbers>
#include <cmath>

namespace sdt::solar_system::constants {

    // CODATA 2018 Fundamental Constants
    inline constexpr double c = 299792458.0;  // Speed of light (m/s), exact
    inline constexpr double hbar = 1.054571817e-34;  // Reduced Planck constant (J·s)
    
    // CMB Pressure (from recombination, Phase 1)
    inline constexpr double P_CMB = 2.036e-2;  // Pa (CMB radiation pressure at z=1089.9)
    
    // Spation Lattice Properties (Phase 15)
    inline constexpr double r_P = 1.616255e-35;  // Planck radius (m)
    inline constexpr double K_bulk = 4.6e113;  // Bulk modulus (Pa)
    inline constexpr double rho_s = 5.2e96;  // Spation density (kg/m³)
    
    // Geometric Efficiency Factor
    inline constexpr double kappa_geom = 1.0;  // Geometric efficiency (dimensionless)
    
    // Mathematical Constants
    inline constexpr double pi = std::numbers::pi_v<double>;
    inline constexpr double two_pi = 2.0 * pi;
    inline constexpr double four_pi = 4.0 * pi;
    
    // Unit Conversions
    inline constexpr double AU = 1.495978707e11;  // Astronomical unit (m)
    inline constexpr double day_to_sec = 86400.0;  // seconds per day
    inline constexpr double year_to_sec = 3.15576e7;  // seconds per year (Julian year)
    inline constexpr double billion_years_to_sec = 3.15576e16;  // seconds per billion years
    
    // Simulation defaults
    inline constexpr double default_timestep = 86400.0;  // 1 day in seconds
    inline constexpr double min_timestep = 1.0;  // 1 second minimum
    inline constexpr double max_timestep = 86400.0 * 10.0;  // 10 days maximum
    
    // Energy conservation tolerance
    inline constexpr double energy_tolerance = 1e-6;  // Relative energy drift tolerance
    
} // namespace sdt::solar_system::constants


