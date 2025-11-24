#pragma once

/**
 * @file constants.hpp
 * @brief Physical constants for SDT-Navier simulations
 */

namespace sdt_navier {

// Fundamental constants (CODATA 2018)
namespace constants {
    // Speed of light
    constexpr double C = 2.99792458e8;  // m/s

    // Planck constant
    constexpr double H = 6.62607015e-34;  // J·s
    constexpr double HBAR = 1.054571817e-34;  // J·s

    // Elementary charge
    constexpr double E_CHARGE = 1.602176634e-19;  // C

    // Electron mass
    constexpr double M_E = 9.1093837015e-31;  // kg

    // Proton mass
    constexpr double M_P = 1.67262192369e-27;  // kg

    // Neutron mass
    constexpr double M_N = 1.67492749804e-27;  // kg

    // Nuclear magneton
    constexpr double MU_N = E_CHARGE * HBAR / (2.0 * M_P);  // J/T
}

// SDT-specific constants (from Phase 19)
namespace sdt {
    // Spation density
    constexpr double RHO_S = 5.2e96;  // kg/m³

    // Nuclear scale pressure
    constexpr double P_INFINITY_NUCLEAR = 1.65e31;  // Pa

    // Proton parameters
    constexpr double R_P = 8.40e-16;  // m
    constexpr double KAPPA_P = 1.190e15;  // m⁻¹ (1/R_p)
    constexpr double GAMMA_P = 0.546;  // Circulation factor
    constexpr double ETA_P_BOUND = 0.0003;  // Slip (bound)

    // Neutron parameters
    constexpr double R_N = 8.70e-16;  // m
    constexpr double R_E_N = 3.00e-15;  // m (internal electron orbit)
    constexpr double KAPPA_N = 1.0 / R_N;  // m⁻¹
    constexpr double KAPPA_E_N = 3.333e14;  // m⁻¹
    constexpr double GAMMA_E_N = 0.531;  // Internal electron circulation
    constexpr double ETA_N_BOUND = 0.0019;  // Slip (bound)
    constexpr double ETA_N_FREE = 0.9981;  // Slip (free, unstable)

    // Experimental binding energies (MeV)
    constexpr double B_DEUTERON = 2.224;
    constexpr double B_TRITON = 8.482;
    constexpr double B_HELION = 7.718;
    constexpr double B_ALPHA = 28.296;

    // Experimental magnetic moments (μ_N)
    constexpr double MU_P = 2.793;
    constexpr double MU_N = -1.913;
    constexpr double MU_D = 0.857;
    constexpr double MU_T = 2.979;
    constexpr double MU_H = -2.128;
    constexpr double MU_ALPHA = 0.0;
}

}  // namespace sdt_navier

