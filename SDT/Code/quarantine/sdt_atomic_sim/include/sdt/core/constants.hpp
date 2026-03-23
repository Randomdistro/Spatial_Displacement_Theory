#pragma once

#include <numbers>

namespace sdt::constants {

    // CODATA 2018 Fundamental Constants
    inline constexpr double C = 299792458.0;  // Speed of light (m/s), exact
    inline constexpr double H_BAR = 1.054571817e-34;  // Reduced Planck constant (J·s)
    inline constexpr double H = 6.62607015e-34;  // Planck constant (J·s)
    inline constexpr double ALPHA = 7.2973525693e-3;  // Fine structure constant
    inline constexpr double E_CHARGE = 1.602176634e-19;  // Elementary charge (C)
    inline constexpr double K_E = 8.9875517923e9;  // Coulomb constant (N·m²/C²)
    
    // Particle masses (kg)
    inline constexpr double M_E = 9.1093837015e-31;  // Electron rest mass
    inline constexpr double M_P = 1.67262192369e-27;  // Proton rest mass
    inline constexpr double M_N = 1.67492749804e-27;  // Neutron rest mass
    
    // CMB Pressure (from recombination)
    inline constexpr double P_CMB = 2.036e-2;  // Pa (CMB radiation pressure at z=1089.9)
    
    // Atomic constants
    inline constexpr double A_0 = 5.29177210903e-11;  // Bohr radius (m)
    inline constexpr double R_INF = 10973731.568160;  // Rydberg constant (m⁻¹)
    
    // Mathematical Constants
    inline constexpr double PI = std::numbers::pi_v<double>;
    inline constexpr double TWO_PI = 2.0 * PI;
    
    // Commonly used aliases for compatibility
    inline constexpr double c = C;
    inline constexpr double hbar = H_BAR;
    inline constexpr double h = H;
    inline constexpr double alpha = ALPHA;
    inline constexpr double pi = PI;
    inline constexpr double two_pi = TWO_PI;
    inline constexpr double a_0 = A_0;

} // namespace sdt::constants

