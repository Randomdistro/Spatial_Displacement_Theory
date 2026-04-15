// investigate_mu_koppa.cpp — Deep numerical investigation of µ-ϟ relationship
// C++20, no external dependencies. All constants from CODATA 2018 / IAU 2015.
// Compile: cl /std:c++20 /EHsc /O2 investigate_mu_koppa.cpp

#include <cmath>
#include <cstdio>
#include <cstdlib>

// ============================================================================
// CODATA 2018 / IAU 2015 CONSTANTS (exact or best-known values)
// ============================================================================

// Speed of light (exact by definition, SI 2019)
constexpr double c       = 299'792'458.0;          // m/s
constexpr double c2      = c * c;                   // m²/s²

// Newtonian gravitational constant (CODATA 2018)
constexpr double G_N     = 6.67430e-11;             // m³ kg⁻¹ s⁻²  (±0.00015)

// Proton mass (CODATA 2018)
constexpr double m_p     = 1.67262192369e-27;       // kg (±0.00000000051)

// Electron mass (CODATA 2018)
constexpr double m_e     = 9.1093837015e-31;        // kg (±0.0000000028)

// Elementary charge (exact, SI 2019)
constexpr double e_charge = 1.602176634e-19;        // C

// Coulomb constant k_e = 1/(4πε₀) (exact in SI 2019)
constexpr double k_e     = 8.9875517923e9;          // N m² C⁻²

// Fine structure constant (CODATA 2018)
constexpr double alpha   = 7.2973525693e-3;         // dimensionless (±0.0000000011)
constexpr double inv_alpha = 1.0 / alpha;            // = 137.035999084

// Proton charge radius (CODATA 2018, muonic hydrogen consistent)
constexpr double R_p     = 0.8414e-15;              // m (±0.0019 fm)

// Bohr radius (CODATA 2018)
constexpr double a_0     = 5.29177210903e-11;       // m (±0.00000000080)

// Classical electron radius (CODATA 2018)
constexpr double r_e_classical = 2.8179403262e-15;  // m (±0.0000000013)

// Rydberg energy (CODATA 2018)
constexpr double E_Ry_eV = 13.605693122994;         // eV

// ============================================================================
// CELESTIAL BODY DATA — IAU 2015 nominal / JPL DE440
// ============================================================================

struct Body {
    const char* name;
    double GM;              // Standard gravitational parameter (m³/s²)
    double R;               // Radius (m) — polar where applicable
    double R_note;          // Which radius used
};

// GM values: IAU 2015 nominal solar, JPL for planets
constexpr Body sun     = {"Sun",     1.3271244e20,  6.957e8,      0};
constexpr Body jupiter = {"Jupiter", 1.26686534e17, 6.6854e7,     0}; // polar radius
constexpr Body saturn  = {"Saturn",  3.7931187e16,  5.4364e7,     0}; // polar radius
constexpr Body earth   = {"Earth",   3.986004418e14, 6.356752e6,  0}; // polar radius
constexpr Body mars    = {"Mars",    4.282837e13,   3.376200e6,   0}; // polar
constexpr Body venus   = {"Venus",   3.24858592e14, 6.051800e6,   0};
constexpr Body moon_body = {"Moon",  4.9048695e12,  1.7374e6,     0};

// ============================================================================
// COMPUTATIONS
// ============================================================================

struct KoppaResult {
    double v_surf;      // Surface orbital velocity
    double koppa;       // ϟ = c / v_surf
    double koppa2;      // ϟ²
    double z_grav;      // Gravitational redshift = 1/ϟ²
    double r_Koppa;     // Koppa radius = R/ϟ² (where v = c)
    double r_schwarz;   // Schwarzschild radius = 2GM/c²
    double mu_from_koppa; // µ recovered from ϟ: c²R/ϟ²
};

KoppaResult compute_koppa(const Body& body) {
    KoppaResult r{};
    r.v_surf       = std::sqrt(body.GM / body.R);
    r.koppa        = c / r.v_surf;
    r.koppa2       = r.koppa * r.koppa;
    r.z_grav       = 1.0 / r.koppa2;
    r.r_Koppa      = body.R / r.koppa2;
    r.r_schwarz    = 2.0 * body.GM / c2;
    r.mu_from_koppa = c2 * body.R / r.koppa2;
    return r;
}

int main() {
    std::printf("================================================================\n");
    std::printf("   INVESTIGATION: The µ-ϟ Relationship\n");
    std::printf("   All constants: CODATA 2018 / IAU 2015\n");
    std::printf("================================================================\n\n");

    // ========================================================================
    // PART 1: Celestial bodies — compute ϟ, verify µ recovery, check r_Ϟ = r_s/2
    // ========================================================================
    std::printf("PART 1: Celestial Bodies — ϟ, µ verification, Koppa radius\n");
    std::printf("─────────────────────────────────────────────────────────────\n\n");

    const Body bodies[] = {sun, jupiter, saturn, earth, mars, venus, moon_body};
    for (const auto& body : bodies) {
        auto k = compute_koppa(body);
        std::printf("%-8s  R = %.6e m   GM = %.7e m³/s²\n", body.name, body.R, body.GM);
        std::printf("  v_surf      = %.6f m/s\n", k.v_surf);
        std::printf("  ϟ           = %.6f\n", k.koppa);
        std::printf("  ϟ²          = %.6f\n", k.koppa2);
        std::printf("  z_grav      = %.10e\n", k.z_grav);
        std::printf("  r_Koppa     = %.6e m  (R/ϟ²)\n", k.r_Koppa);
        std::printf("  r_Schwarz   = %.6e m  (2GM/c²)\n", k.r_schwarz);
        std::printf("  r_Koppa     = r_s/2 ?  ratio = %.10f\n", k.r_Koppa / (k.r_schwarz / 2.0));
        std::printf("  µ from ϟ    = %.7e  (c²R/ϟ²)\n", k.mu_from_koppa);
        std::printf("  µ known     = %.7e  (GM)\n", body.GM);
        std::printf("  µ match     = %.12f\n", k.mu_from_koppa / body.GM);
        std::printf("\n");
    }

    // ========================================================================
    // PART 2: The proton — electromagnetic µ
    // ========================================================================
    std::printf("\n================================================================\n");
    std::printf("PART 2: The Proton — Electromagnetic µ\n");
    std::printf("─────────────────────────────────────────────────────────────\n\n");

    // Koppa for the proton (from the paper)
    double koppa_p = inv_alpha * std::sqrt(R_p / a_0);
    double koppa_p2 = koppa_p * koppa_p;
    std::printf("Proton koppa ϟ = (1/α) × √(Rₚ/a₀)\n");
    std::printf("  1/α         = %.9f\n", inv_alpha);
    std::printf("  Rₚ          = %.4e m\n", R_p);
    std::printf("  a₀          = %.11e m\n", a_0);
    std::printf("  Rₚ/a₀       = %.10e\n", R_p / a_0);
    std::printf("  √(Rₚ/a₀)    = %.10e\n", std::sqrt(R_p / a_0));
    std::printf("  ϟ           = %.10f\n", koppa_p);
    std::printf("  ϟ²          = %.10f\n", koppa_p2);
    std::printf("\n");

    // µ from koppa for the proton
    double mu_koppa_proton = c2 * R_p / koppa_p2;
    std::printf("µ_koppa(proton) = c²Rₚ/ϟ²\n");
    std::printf("  = %.10e m³/s²\n", mu_koppa_proton);

    // µ from electromagnetism: k_e × e² / m_e
    double mu_em = k_e * e_charge * e_charge / m_e;
    std::printf("\nµ_em = k_e × e² / m_e\n");
    std::printf("  k_e         = %.10e N·m²/C²\n", k_e);
    std::printf("  e²          = %.10e C²\n", e_charge * e_charge);
    std::printf("  m_e         = %.10e kg\n", m_e);
    std::printf("  µ_em        = %.10e m³/s²\n", mu_em);

    std::printf("\n>>> µ_koppa / µ_em = %.12f\n", mu_koppa_proton / mu_em);
    std::printf(">>> MATCH: %s\n\n", std::abs(mu_koppa_proton / mu_em - 1.0) < 1e-3 ? "YES" : "NO");

    // Gravitational µ of the proton
    double mu_grav_proton = G_N * m_p;
    std::printf("µ_grav(proton) = G × m_p = %.6e m³/s²\n", mu_grav_proton);

    // Force ratio
    double force_ratio = mu_em / mu_grav_proton;
    std::printf("\n>>> F_em / F_grav = µ_em / µ_grav = %.6e\n", force_ratio);
    std::printf(">>> This is the electromagnetic-to-gravitational force ratio\n");
    std::printf(">>> (the 'hierarchy problem' number)\n\n");

    // ========================================================================
    // PART 3: Koppa radius = r_s/2 — the Schwarzschild connection
    // ========================================================================
    std::printf("================================================================\n");
    std::printf("PART 3: r_Koppa = r_Schwarzschild / 2\n");
    std::printf("─────────────────────────────────────────────────────────────\n\n");
    std::printf("r_Ϟ = R/ϟ²\n");
    std::printf("r_s = 2GM/c² = 2(c²R/ϟ²)/c² = 2R/ϟ²\n");
    std::printf("Therefore: r_Ϟ = r_s/2  (EXACT, algebraic)\n\n");

    std::printf("Numerical verification:\n");
    std::printf("%-10s %15s %15s %15s\n", "Body", "r_Koppa (m)", "r_s/2 (m)", "Ratio");
    for (const auto& body : bodies) {
        auto k = compute_koppa(body);
        std::printf("%-10s %15.6e %15.6e %15.12f\n",
            body.name, k.r_Koppa, k.r_schwarz / 2.0, k.r_Koppa / (k.r_schwarz / 2.0));
    }

    // Proton
    double r_Koppa_proton = R_p / koppa_p2;
    std::printf("\nProton:\n");
    std::printf("  r_Koppa = Rₚ/ϟ² = %.10e m\n", r_Koppa_proton);
    std::printf("  Classical electron radius r_e = %.10e m\n", r_e_classical);
    std::printf("  r_Koppa / r_e = %.10f\n", r_Koppa_proton / r_e_classical);

    // ========================================================================
    // PART 4: What is ϟ² dimensionally? Investigate µ/c² and R
    // ========================================================================
    std::printf("\n================================================================\n");
    std::printf("PART 4: Dimensional analysis of ϟ²\n");
    std::printf("─────────────────────────────────────────────────────────────\n\n");

    std::printf("ϟ² = c²R/µ = c²R/(GM)\n\n");
    std::printf("Since r_s = 2µ/c², we have µ/c² = r_s/2\n");
    std::printf("So ϟ² = R / (r_s/2) = 2R/r_s\n\n");
    std::printf("ϟ² is simply TWICE the ratio of the body's radius\n");
    std::printf("to its Schwarzschild radius.\n\n");

    std::printf("%-10s %15s %15s %15s\n", "Body", "ϟ²", "2R/r_s", "Match");
    for (const auto& body : bodies) {
        auto k = compute_koppa(body);
        double two_R_over_rs = 2.0 * body.R / k.r_schwarz;
        std::printf("%-10s %15.4f %15.4f %15.10f\n",
            body.name, k.koppa2, two_R_over_rs, k.koppa2 / two_R_over_rs);
    }

    // ========================================================================
    // PART 5: The proton — where does r_Koppa land?
    // ========================================================================
    std::printf("\n================================================================\n");
    std::printf("PART 5: Proton's Koppa radius and the classical electron radius\n");
    std::printf("─────────────────────────────────────────────────────────────\n\n");

    // Re-derive classical electron radius from first principles
    double r_e_derived = k_e * e_charge * e_charge / (m_e * c2);
    std::printf("Classical electron radius (derived):\n");
    std::printf("  r_e = k_e × e² / (m_e × c²) = %.10e m\n", r_e_derived);
    std::printf("  r_e (CODATA)                 = %.10e m\n", r_e_classical);
    std::printf("  Match: %.12f\n\n", r_e_derived / r_e_classical);

    // Proton Koppa radius
    std::printf("Proton Koppa radius:\n");
    std::printf("  r_Ϟ = Rₚ/ϟ² = %.4e / %.6f = %.10e m\n", R_p, koppa_p2, r_Koppa_proton);
    std::printf("  r_e (classical)              = %.10e m\n", r_e_classical);
    std::printf("  r_Ϟ / r_e = %.10f\n\n", r_Koppa_proton / r_e_classical);

    // Why does this work? Expand:
    // r_Ϟ = Rₚ/ϟ² = Rₚ / ((1/α)² × (Rₚ/a₀)) = Rₚ × α² × a₀/Rₚ = α² × a₀
    double alpha2_a0 = alpha * alpha * a_0;
    std::printf("Algebraic expansion: r_Ϟ = Rₚ/ϟ² = α² × a₀\n");
    std::printf("  α² × a₀ = %.10e m\n", alpha2_a0);
    std::printf("  r_Ϟ      = %.10e m\n", r_Koppa_proton);
    std::printf("  Match:   %.12f\n\n", alpha2_a0 / r_Koppa_proton);

    // And the classical electron radius IS α² × a₀!
    std::printf("Classical electron radius = α² × a₀ ?\n");
    std::printf("  α² × a₀  = %.10e m\n", alpha2_a0);
    std::printf("  r_e       = %.10e m\n", r_e_classical);
    std::printf("  Ratio     = %.12f\n\n", alpha2_a0 / r_e_classical);

    // ========================================================================
    // PART 6: Chain of identities
    // ========================================================================
    std::printf("================================================================\n");
    std::printf("PART 6: Chain of identities\n");
    std::printf("─────────────────────────────────────────────────────────────\n\n");

    std::printf("For ANY body:\n");
    std::printf("  µ = c²R/ϟ²              (koppa defines µ)\n");
    std::printf("  z = 1/ϟ²                (redshift from koppa)\n");
    std::printf("  r_Ϟ = R/ϟ²              (c boundary from koppa)\n");
    std::printf("  r_s = 2R/ϟ²             (Schwarzschild from koppa)\n");
    std::printf("  r_Ϟ = r_s/2             (Koppa = half Schwarzschild)\n");
    std::printf("  ϟ² = 2R/r_s             (koppa² = compactness inverse)\n\n");

    std::printf("For the proton (electromagnetic):\n");
    std::printf("  µ_em = k_e e²/m_e = c²Rₚ/ϟ²\n");
    std::printf("  r_Ϟ  = Rₚ/ϟ² = α²a₀ = r_e  (classical electron radius)\n");
    std::printf("  ϟ_em = (1/α)√(Rₚ/a₀)  = %.10f\n\n", koppa_p);

    // ========================================================================
    // PART 7: Relationship between µ and ϟ across scales
    // ========================================================================
    std::printf("================================================================\n");
    std::printf("PART 7: µ × ϟ² = c²R for all bodies\n");
    std::printf("─────────────────────────────────────────────────────────────\n\n");

    std::printf("The identity µ = c²R/ϟ² means µ × ϟ² = c²R\n");
    std::printf("i.e. µ × ϟ² is the product of c² and the body's radius.\n\n");

    std::printf("%-10s %15s %15s %15s\n", "Body", "µ × ϟ²", "c² × R", "Match");
    for (const auto& body : bodies) {
        auto k = compute_koppa(body);
        double mu_k2 = body.GM * k.koppa2;
        double c2R = c2 * body.R;
        std::printf("%-10s %15.6e %15.6e %15.10f\n",
            body.name, mu_k2, c2R, mu_k2 / c2R);
    }
    // Proton EM
    double mu_k2_proton = mu_em * koppa_p2;
    double c2Rp = c2 * R_p;
    std::printf("%-10s %15.6e %15.6e %15.10f\n",
        "Proton(EM)", mu_k2_proton, c2Rp, mu_k2_proton / c2Rp);

    // ========================================================================
    // PART 8: ϟ as a compactness measure
    // ========================================================================
    std::printf("\n================================================================\n");
    std::printf("PART 8: Physical meaning — ϟ² as compactness\n");
    std::printf("─────────────────────────────────────────────────────────────\n\n");

    std::printf("Compactness C = r_s / R = 2GM/(Rc²) = 2/ϟ²\n");
    std::printf("Therefore: ϟ = √(2/C)\n\n");

    std::printf("%-10s %15s %15s %15s\n", "Body", "Compactness", "ϟ", "√(2/C)");
    for (const auto& body : bodies) {
        auto k = compute_koppa(body);
        double C = k.r_schwarz / body.R;
        double sqrt_2_C = std::sqrt(2.0 / C);
        std::printf("%-10s %15.6e %15.6f %15.6f\n",
            body.name, C, k.koppa, sqrt_2_C);
    }

    // ========================================================================
    // PART 9: Escape velocity connection
    // ========================================================================
    std::printf("\n================================================================\n");
    std::printf("PART 9: ϟ and the escape velocity\n");
    std::printf("─────────────────────────────────────────────────────────────\n\n");

    std::printf("v_esc = √(2GM/R) = v_surf × √2\n");
    std::printf("ϟ_esc = c / v_esc = ϟ / √2\n\n");

    std::printf("%-10s %12s %12s %12s %12s\n",
        "Body", "v_surf", "v_esc", "ϟ", "ϟ/√2");
    for (const auto& body : bodies) {
        auto k = compute_koppa(body);
        double v_esc = k.v_surf * std::sqrt(2.0);
        double koppa_esc = k.koppa / std::sqrt(2.0);
        std::printf("%-10s %12.2f %12.2f %12.4f %12.4f\n",
            body.name, k.v_surf, v_esc, k.koppa, koppa_esc);
    }

    // ========================================================================
    // FINAL SUMMARY
    // ========================================================================
    std::printf("\n================================================================\n");
    std::printf("FINAL SUMMARY OF FINDINGS\n");
    std::printf("================================================================\n\n");

    std::printf("1. µ = c²R/ϟ²  — exact for all bodies (algebraic identity)\n\n");
    std::printf("2. r_Koppa = R/ϟ² = r_Schwarzschild/2  — EXACT\n");
    std::printf("   The Koppa radius is precisely HALF the Schwarzschild radius\n\n");
    std::printf("3. ϟ² = 2R/r_s  — koppa squared is the inverse compactness\n\n");
    std::printf("4. For the proton: µ_koppa = c²Rₚ/ϟ² = k_e × e²/m_e\n");
    std::printf("   Koppa's µ for the proton IS the electromagnetic parameter\n");
    std::printf("   µ_koppa = %.6e  vs  µ_em = %.6e\n", mu_koppa_proton, mu_em);
    std::printf("   Match: %.8f\n\n", mu_koppa_proton / mu_em);
    std::printf("5. The EM/gravitational force ratio falls out as:\n");
    std::printf("   µ_em / µ_grav = %.6e\n", force_ratio);
    std::printf("   This IS the hierarchy problem number.\n\n");
    std::printf("6. Proton's Koppa radius = α² × a₀ = r_e (classical electron radius)\n");
    std::printf("   r_Koppa = %.6e m\n", r_Koppa_proton);
    std::printf("   r_e     = %.6e m\n", r_e_classical);
    std::printf("   α²a₀    = %.6e m\n\n", alpha2_a0);

    return 0;
}
