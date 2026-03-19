#pragma once

#include <numbers>
#include <cmath>

namespace sdt::constants {

    // ========================================================================
    // SDT PURE — No G, no M as inputs
    // Mass is the resistance to change imparted by the spation matrix.
    // ========================================================================

    // CODATA 2018 Fundamental Constants
    inline constexpr double c = 299792458.0;  // Speed of light (m/s), exact
    inline constexpr double hbar = 1.054571817e-34;  // Reduced Planck constant (J·s)
    inline constexpr double alpha = 7.2973525693e-3;  // Fine structure constant
    
    // CMB Pressure (from recombination)
    inline constexpr double P_CMB = 2.036e-2;  // Pa (CMB radiation pressure at z=1089.9)
    
    // Spation Lattice Properties
    inline constexpr double r_P = 1.616255e-35;  // Planck radius (m)
    inline constexpr double K_bulk = 4.6e113;  // Bulk modulus (Pa)
    inline constexpr double rho_s = 5.2e96;  // Spation density (kg/m³)
    
    // Geometric Efficiency Factor
    inline constexpr double kappa = 1.0;  // Geometric efficiency (dimensionless, can be refined)
    
    // Mathematical Constants
    inline constexpr double pi = std::numbers::pi_v<double>;
    inline constexpr double two_pi = 2.0 * pi;
    
    // Unit Conversions
    inline constexpr double AU = 1.495978707e11;  // Astronomical unit (m)
    inline constexpr double day_to_sec = 86400.0;  // seconds per day
#ifdef SDT_ALLOW_LEGACY_COMPARISON
    // NIST reference values — validation targets only, never SDT input primitives.
    inline constexpr double G_conv = 6.67430e-11;  // Conventional G (m³/kg/s²) — NIST reference only
    inline constexpr double solar_mass_conv = 1.9885e30;  // Conventional solar mass (kg) — NIST reference only
#endif    
} // namespace sdt::constants

