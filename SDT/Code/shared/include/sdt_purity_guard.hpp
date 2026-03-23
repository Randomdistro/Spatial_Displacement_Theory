#pragma once
// =============================================================================
// SDT Purity Guard — Compile-Time Enforcement Header
// =============================================================================
// Include this header in any SDT module to enforce purity at compile time.
// Violations will produce clear, descriptive static_assert failures.
//
// SDT Canonical Engine v4.0 — Primitives: c, v, z, k, R, r, kappa
// =============================================================================

// ─── Guard: Forbid G as a constant name ─────────────────────────────────────
// If any translation unit defines G_GRAVITATIONAL_CONSTANT, compilation fails.
// This catches accidental reintroduction of G = 6.674e-11.
#ifdef G_GRAVITATIONAL_CONSTANT
    static_assert(false,
        "SDT PURITY VIOLATION [R1]: G (gravitational constant) detected. "
        "SDT derives gravity from geometry: v(r) = (c/k)*sqrt(R/r). "
        "Use kappa, k, and R_c instead.");
#endif

// ─── Guard: Forbid mass as computational input ──────────────────────────────
// Define SDT_MASS_AS_INPUT before including this header to trigger the guard.
// Use this in code review: if you need to tag a function that takes mass.
#ifdef SDT_MASS_AS_INPUT
    static_assert(false,
        "SDT PURITY VIOLATION [R2]: Mass used as computational input. "
        "Mass is the resistance to change imparted by the spation matrix. "
        "It is a measured output, not a free input. Use NIST reference values "
        "in nist_ref:: namespace for validation only.");
#endif

// ─── Guard: Forbid Schwarzschild radius ─────────────────────────────────────
#ifdef SCHWARZSCHILD_RADIUS
    static_assert(false,
        "SDT PURITY VIOLATION [R9]: Schwarzschild radius detected. "
        "SDT uses c-boundary R_c = R/k^2 (pressure saturation, not event horizon).");
#endif

// ─── Guard: Forbid dark matter as entity ────────────────────────────────────
#ifdef DARK_MATTER_ENTITY
    static_assert(false,
        "SDT PURITY VIOLATION [R7]: Dark matter entity detected. "
        "SDT explains flat rotation curves via cumulative stellar pressure occlusion. "
        "Use R_occ and occlusion functions instead.");
#endif

// ─── Guard: Forbid wave functions ───────────────────────────────────────────
#ifdef QM_WAVE_FUNCTION
    static_assert(false,
        "SDT PURITY VIOLATION [R5]: Quantum mechanical wave function detected. "
        "SDT uses pressure-node standing waves in the spation medium. "
        "Replace wave_function() with admittance_profile().");
#endif

// ─── Namespace marker: SDT purity verified ──────────────────────────────────
namespace sdt::purity {
    // Compile-time tag: include this header to mark a translation unit as
    // having been reviewed for SDT compliance.
    inline constexpr bool verified = true;

    // SDT canonical primitives — the ONLY permitted input observables
    // c  — speed of light (m/s)
    // v  — observed velocity (m/s)
    // z  — geometric parameter = v²/c² = 1/k²
    // k  — velocity factor = c/v
    // R  — body radius (m, directly measured)
    // r  — orbital/observation radius (m)
    // κ  — curvature parameter = 1/R (m⁻¹)
    // α  — fine structure constant (dimensionless)
    // h  — Planck constant (J·s)
    // ħ  — reduced Planck constant (J·s)

    // Derived quantities (NOT free inputs):
    // R_c    = R/k²          c-boundary radius
    // c2_R_c = c²·R_c        acceleration scale  
    // a(r)   = c²·R_c/r²     radial acceleration
    // v(r)   = (c/k)·√(R/r)  orbital velocity
    // mass   = h/(λ_C·c)     from Compton wavelength (spation matrix resistance)
}
