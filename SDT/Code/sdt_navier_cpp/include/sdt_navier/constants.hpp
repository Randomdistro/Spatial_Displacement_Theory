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

    // ──────────────────────────────────────────────────────────────
    // SDT: Mass = resistance to change imparted by the spation matrix
    //      m = h / (λ_C · c)  where λ_C is the Compton wavelength
    //      These are NIST reference values for validation, not inputs.
    // ──────────────────────────────────────────────────────────────

    // Compton wavelengths — the primary SDT-observable quantities
    constexpr double LAMBDA_C_E = 2.42631023867e-12;  // m  (electron)
    constexpr double LAMBDA_C_P = 1.32141002140e-15;  // m  (proton)
    constexpr double LAMBDA_C_N = 1.31959090581e-15;  // m  (neutron)

    // NIST reference masses — derived from m = h/(λ_C·c)
    // Used ONLY as validation targets, never as computational inputs
    namespace nist_ref {
        constexpr double M_E = 9.1093837015e-31;   // kg (electron)
        constexpr double M_P = 1.67262192369e-27;   // kg (proton)
        constexpr double M_N = 1.67492749804e-27;   // kg (neutron)
    }

    // Nuclear magneton — derived from NIST reference proton mass
    constexpr double MU_N = E_CHARGE * HBAR / (2.0 * nist_ref::M_P);  // J/T
}

// SDT-specific constants (from Phase 19)
namespace sdt {
    // Spation density
    constexpr double RHO_S = 5.2e96;  // kg/m³

    // Nuclear density (from SDT compendium)
    constexpr double RHO_N = 2.342e17;  // kg/m³

    // Fine structure constant (dimensionless)
    constexpr double ALPHA = 7.2973525693e-3;

    // Atomic-scale CMB pressure (Pa)
    constexpr double P_CMB_ATOMIC = 2.036e-2;

    // Nuclear scale pressure
    constexpr double P_INFINITY_NUCLEAR = 1.65e31;  // Pa

    // Hydrogen reference electron density (m^-3)
    constexpr double N_E_HYDROGEN = 2.718281828e29;

    // Proton parameters
    constexpr double R_P = 8.40e-16;  // m
    constexpr double KAPPA_P = 1.0 / R_P;  // m⁻¹ (exact reciprocal)
    constexpr double GAMMA_P = 0.546;  // Circulation factor
    constexpr double ETA_P_BOUND = 0.0003;  // Slip (bound)

    // Neutron parameters
    constexpr double R_N = 8.70e-16;  // m
    constexpr double R_E_N = 3.00e-15;  // m (internal electron orbit)
    constexpr double KAPPA_N = 1.0 / R_N;  // m⁻¹
    constexpr double KAPPA_E_N = 1.0 / R_E_N;  // m⁻¹ (exact reciprocal)
    constexpr double GAMMA_E_N = 0.531;  // Internal electron circulation
    constexpr double ETA_N_BOUND = 0.0019;  // Slip (bound)
    constexpr double ETA_N_FREE = 0.9981;  // Slip (free, unstable)

    // Experimental binding energies (MeV)
    constexpr double B_DEUTERON = 2.224;
    constexpr double B_TRITON = 8.482;
    constexpr double B_HELION = 7.718;
    constexpr double B_ALPHA = 28.296;

    // Experimental magnetic moments (μ_N, CODATA 2018 / benchmark data)
    constexpr double MU_P = 2.79284734462;   // Proton
    constexpr double MU_N = -1.91304272;     // Neutron (negative from reversed circulation)
    constexpr double MU_D = 0.857421;        // Deuteron (p+n with damping)
    constexpr double MU_T = 2.979;           // Triton
    constexpr double MU_H = -2.128;          // Helion
    constexpr double MU_ALPHA = 0.0;         // Alpha (spin-0)
}

}  // namespace sdt_navier

