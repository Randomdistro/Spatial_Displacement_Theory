#pragma once

/**
 * @file constants.hpp
 * @brief Physical constants for SDT-Navier simulations
 *
 * Fundamental SI constants retained here for backward compatibility.
 * All SDT-specific constants now derive from the canonical sdt_laws.hpp.
 */

#include "../sdt_laws.hpp"

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
    constexpr double NUCLEAR_MAGNETON = E_CHARGE * HBAR / (2.0 * nist_ref::M_P);  // J/T
}

// ══════════════════════════════════════════════════════════════════════
// SDT Five-Law Framework constants (canonical source: sdt_laws.hpp)
// ══════════════════════════════════════════════════════════════════════
// All SDT constants now derive from the formal 5-Law framework.
// See sdt_laws.hpp for the complete derivation chain.
// ══════════════════════════════════════════════════════════════════════

namespace sdt {
    // Fine structure constant (dimensionless)
    inline constexpr double ALPHA = sdt::laws::measured::alpha;

    // ── Law I: Convergence pressure replaces old ad-hoc pressure values ──
    // OLD: RHO_S = 5.2e96 (Phase 19, no derivation)     → REMOVED
    // OLD: P_CMB_ATOMIC = 2.036e-2 (ad-hoc)              → REPLACED by u_CMB/3
    // OLD: P_INFINITY_NUCLEAR = 1.65e31 (Phase 19)        → REPLACED by P_eff
    inline constexpr double P_CONV          = sdt::laws::law_I::P_conv;         // 2.459e48 Pa
    inline constexpr double P_EFF           = sdt::laws::law_III::P_eff;        // 5.225e31 Pa
    inline constexpr double F_TRANSFER      = sdt::laws::law_III::f_transfer;   // 2.125e-17

    // ── Proton parameters ──
    inline constexpr double R_P             = sdt::laws::measured::R_p;         // 8.414e-16 m
    inline constexpr double R_CHARGE        = sdt::laws::law_III::R_charge;     // 1.540e-15 m

    // ── Law IV: Exclusion volumes (computed, not fitted) ──
    inline constexpr double V_DISP_E        = sdt::laws::law_IV::V_disp_e;     // 9.988e-62 m³
    inline constexpr double V_DISP_P        = sdt::laws::law_IV::V_disp_p;     // 1.834e-58 m³
    inline constexpr double R_EXCL_E        = sdt::laws::law_IV::R_excl_e;     // 2.878e-21 m
    inline constexpr double R_EXCL_P        = sdt::laws::law_IV::R_excl_p;     // 3.525e-20 m

    // ── Neutron parameters (topology: proton + captured electron) ──
    inline constexpr double R_N = 8.70e-16;  // m
    inline constexpr double R_E_N = 3.00e-15;  // m (internal electron orbit)

    // ── Experimental binding energies (MeV) ──
    inline constexpr double B_DEUTERON  = sdt::laws::measured::B_deuteron;
    inline constexpr double B_TRITON    = sdt::laws::measured::B_triton;
    inline constexpr double B_HELION    = sdt::laws::measured::B_helion;
    inline constexpr double B_ALPHA     = sdt::laws::measured::B_alpha;

    // ── Experimental magnetic moments (μ_N, CODATA 2018) ──
    inline constexpr double MU_P        = sdt::laws::measured::mu_P;
    inline constexpr double MU_N        = sdt::laws::measured::mu_N;
    inline constexpr double MU_D        = sdt::laws::measured::mu_D;
    inline constexpr double MU_T        = sdt::laws::measured::mu_T;
    inline constexpr double MU_H        = sdt::laws::measured::mu_He3;
    inline constexpr double MU_ALPHA    = sdt::laws::measured::mu_alpha;
}

}  // namespace sdt_navier
