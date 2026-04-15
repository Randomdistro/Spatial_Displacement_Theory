// koppa_deep_investigation.cpp — Phases 2-7 exhaustive numerical investigation
// C++20 | CODATA 2018 | IAU 2015 | No external dependencies
// Compile: cl /std:c++20 /EHsc /O2 /utf-8 koppa_deep_investigation.cpp

#include <cmath>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <array>

// ============================================================================
// CODATA 2018 / IAU 2015 CONSTANTS
// ============================================================================
constexpr double c          = 299'792'458.0;                        // m/s (exact)
constexpr double c2         = c * c;                                // 8.98755e16
constexpr double G_N        = 6.67430e-11;                          // m^3 kg^-1 s^-2
constexpr double m_p        = 1.67262192369e-27;                    // kg
constexpr double m_e        = 9.1093837015e-31;                     // kg
constexpr double e_q        = 1.602176634e-19;                      // C (exact)
constexpr double k_e        = 8.9875517923e9;                       // N m^2 C^-2
constexpr double alpha      = 7.2973525693e-3;                      // fine structure
constexpr double inv_alpha  = 1.0 / alpha;                          // 137.035999084
constexpr double R_p        = 0.8414e-15;                           // proton charge radius
constexpr double a_0        = 5.29177210903e-11;                    // Bohr radius
constexpr double r_e_CODATA = 2.8179403262e-15;                     // classical electron radius
constexpr double hbar       = 1.054571817e-34;                      // reduced Planck (exact)
constexpr double h_planck   = 6.62607015e-34;                       // Planck constant (exact)
constexpr double eV_to_J    = 1.602176634e-19;                      // eV -> Joules
constexpr double E_Ry_eV    = 13.605693122994;                      // Rydberg energy in eV
constexpr double R_inf      = 10973731.568160;                      // Rydberg constant (m^-1)

// Proton koppa computed at runtime (MSVC constexpr sqrt limitation)

// ============================================================================
// CELESTIAL DATA
// ============================================================================
struct Body { const char* name; double GM; double R; };
constexpr Body bodies[] = {
    {"Sun",     1.3271244e20,   6.957e8     },
    {"Jupiter", 1.26686534e17,  6.6854e7    },  // polar
    {"Saturn",  3.7931187e16,   5.4364e7    },  // polar
    {"Earth",   3.986004418e14, 6.356752e6  },  // polar
    {"Mars",    4.282837e13,    3.376200e6  },
    {"Venus",   3.24858592e14,  6.051800e6  },
    {"Moon",    4.9048695e12,   1.7374e6    },
};
constexpr int N_BODIES = sizeof(bodies) / sizeof(bodies[0]);

// ============================================================================
// UTILITY
// ============================================================================
void separator(const char* title, int phase) {
    std::printf("\n\n");
    std::printf("################################################################\n");
    std::printf("  PHASE %d: %s\n", phase, title);
    std::printf("################################################################\n\n");
}

void subsep(const char* title) {
    std::printf("\n--- %s ---\n\n", title);
}

// ============================================================================
int main() {

    // Runtime computation of koppa_p (MSVC constexpr sqrt limitation)
    const double kp   = inv_alpha * std::sqrt(R_p / a_0);
    const double kp2  = kp * kp;
    const double kH   = inv_alpha;   // hydrogen koppa = 1/alpha
    const double kH2  = kH * kH;
    const double r_Kp = R_p / kp2;   // proton's Koppa radius

    // Electromagnetic mu
    const double mu_em = k_e * e_q * e_q / m_e;

    std::printf("================================================================\n");
    std::printf("  KOPPA DEEP INVESTIGATION — Phases 2-7\n");
    std::printf("  All constants: CODATA 2018 / IAU 2015\n");
    std::printf("================================================================\n");
    std::printf("  c       = %.0f m/s\n", c);
    std::printf("  1/alpha = %.9f\n", inv_alpha);
    std::printf("  R_p     = %.4e m\n", R_p);
    std::printf("  a_0     = %.11e m\n", a_0);
    std::printf("  r_e     = %.10e m\n", r_e_CODATA);
    std::printf("  koppa_p = %.10f\n", kp);
    std::printf("  koppa_H = %.9f\n", kH);
    std::printf("  mu_em   = %.10e m^3/s^2\n", mu_em);

    // ================================================================
    separator("HYDROGEN ORBITAL TRACK", 2);
    // ================================================================

    subsep("2A. Excitation states n=1..10");
    std::printf("Formula: v = (c/koppa_p) * sqrt(R_p / r_n)\n");
    std::printf("  where r_n = n^2 * a_0,  v_Bohr = alpha*c/n\n\n");

    std::printf("%3s %14s %14s %14s %14s %10s\n",
        "n", "r_n (m)", "v_Bohr (m/s)", "v_koppa (m/s)", "v_kep (m/s)", "error");
    for (int n = 1; n <= 10; ++n) {
        double r_n    = (double)(n*n) * a_0;
        double v_bohr = alpha * c / n;
        double v_kop  = (c / kp) * std::sqrt(R_p / r_n);
        // Also Keplerian: v = sqrt(mu_em / r_n)
        double v_kep  = std::sqrt(mu_em / r_n);
        double err    = std::abs(v_kop - v_bohr) / v_bohr * 100.0;
        std::printf("%3d %14.6e %14.6f %14.6f %14.6f %9.6f%%\n",
            n, r_n, v_bohr, v_kop, v_kep, err);
    }

    subsep("2B. Two koppa values for hydrogen");
    std::printf("koppa_H  = c/v_1 = 1/alpha           = %.9f\n", kH);
    std::printf("koppa_p  = (1/alpha)*sqrt(R_p/a_0)    = %.10f\n", kp);
    std::printf("\nRelationship:\n");
    std::printf("  koppa_p = koppa_H * sqrt(R_p/a_0)\n");
    double kp_check = kH * std::sqrt(R_p / a_0);
    std::printf("  check:    %.10f vs %.10f  ratio=%.12f\n", kp_check, kp, kp_check/kp);
    std::printf("\n  koppa_H = koppa_p * sqrt(a_0/R_p)\n");
    double kH_check = kp * std::sqrt(a_0 / R_p);
    std::printf("  check:    %.9f vs %.9f  ratio=%.12f\n", kH_check, kH, kH_check/kH);
    std::printf("\n  koppa_H / koppa_p = sqrt(a_0/R_p) = %.6f\n", std::sqrt(a_0/R_p));
    std::printf("  = 1/sqrt(R_p/a_0) = %.6f\n", 1.0/std::sqrt(R_p/a_0));

    subsep("2C. k^2 identity — two levels");
    std::printf("Body-level (proton):\n");
    std::printf("  koppa_p^2 * r_Koppa = R_p\n");
    double kp2_rK = kp2 * r_Kp;
    std::printf("  %.6f * %.10e = %.10e\n", kp2, r_Kp, kp2_rK);
    std::printf("  R_p                         = %.10e\n", R_p);
    std::printf("  Match: %.12f\n\n", kp2_rK / R_p);

    std::printf("System-level (hydrogen):\n");
    std::printf("  koppa_H^2 * r_Koppa = a_0\n");
    double kH2_rK = kH2 * r_Kp;
    std::printf("  %.4f * %.10e = %.10e\n", kH2, r_Kp, kH2_rK);
    std::printf("  a_0                         = %.10e\n", a_0);
    std::printf("  Match: %.12f\n\n", kH2_rK / a_0);

    std::printf("KEY INSIGHT: The same Koppa radius r_Koppa = %.4e m\n", r_Kp);
    std::printf("  * squared by koppa_p^2 (%.6f) -> recovers R_p (proton radius)\n", kp2);
    std::printf("  * squared by koppa_H^2 (%.4f) -> recovers a_0 (Bohr radius)\n", kH2);
    std::printf("  * r_Koppa is the classical electron radius\n");
    std::printf("  * It is the PIVOT between nuclear and atomic scales\n");

    subsep("2D. Continuum orbital track: r_e -> a_0 -> n=10");
    std::printf("At r_e (v=c boundary), moving outward:\n\n");
    std::printf("%14s %14s %14s %14s\n", "r (m)", "v_koppa (m/s)", "v/c", "koppa_local");
    double track_radii[] = {
        r_Kp,               // r_e = classical electron radius (v=c)
        r_Kp * 2,
        r_Kp * 5,
        r_Kp * 10,
        r_Kp * 100,
        R_p,                // proton charge radius
        R_p * 10,
        R_p * 100,
        a_0 / 100,
        a_0 / 10,
        a_0,                // Bohr radius (n=1)
        4.0 * a_0,          // n=2
        9.0 * a_0,          // n=3
        25.0 * a_0,         // n=5
        100.0 * a_0,        // n=10
    };
    for (double r : track_radii) {
        double v = (c / kp) * std::sqrt(R_p / r);
        std::printf("%14.6e %14.6e %14.10f %14.6f\n", r, v, v/c, c/v);
    }

    // ================================================================
    separator("ENERGY-KOPPA CHAIN", 3);
    // ================================================================

    subsep("3A. Rydberg energy from koppa");
    // E_1 = (1/2) m_e v_1^2 = (1/2) m_e (alpha*c)^2 = m_e c^2 alpha^2 / 2
    double E_1_J = 0.5 * m_e * (alpha * c) * (alpha * c);
    double E_1_eV = E_1_J / eV_to_J;
    std::printf("E_1 = (1/2) m_e v_1^2 = m_e c^2 alpha^2 / 2\n");
    std::printf("    = m_e c^2 / (2 * koppa_H^2)\n");
    double E_from_kH = m_e * c2 / (2.0 * kH2);
    std::printf("  m_e c^2          = %.10e J = %.6f eV\n", m_e * c2, m_e * c2 / eV_to_J);
    std::printf("  koppa_H^2        = %.6f\n", kH2);
    std::printf("  E_1 (computed)   = %.10e J = %.10f eV\n", E_1_J, E_1_eV);
    std::printf("  E_1 (from kop_H) = %.10e J = %.10f eV\n", E_from_kH, E_from_kH/eV_to_J);
    std::printf("  E_Ry (CODATA)    = %.10f eV\n", E_Ry_eV);
    std::printf("  Match: %.12f\n", E_1_eV / E_Ry_eV);

    subsep("3B. Ionization energy for each n");
    std::printf("E_n = E_Ry / n^2 = m_e c^2 / (2 * n^2 * koppa_H^2)\n\n");
    std::printf("%3s %14s %14s %14s %10s\n", "n", "E_koppa (eV)", "E_Bohr (eV)", "E_Ry/n^2 (eV)", "err");
    for (int n = 1; n <= 7; ++n) {
        double E_kop  = m_e * c2 / (2.0 * n * n * kH2) / eV_to_J;
        double v_n    = alpha * c / n;
        double E_bohr = 0.5 * m_e * v_n * v_n / eV_to_J;
        double E_ry_n = E_Ry_eV / (n * n);
        double err    = std::abs(E_kop - E_ry_n) / E_ry_n * 100;
        std::printf("%3d %14.6f %14.6f %14.6f %9.6f%%\n", n, E_kop, E_bohr, E_ry_n, err);
    }

    subsep("3C. Spectral lines from koppa");
    std::printf("Transition wavelength: 1/lambda = R_inf * (1/n1^2 - 1/n2^2)\n");
    std::printf("From koppa: E = m_e c^2 / (2 koppa_H^2) * (1/n1^2 - 1/n2^2)\n");
    std::printf("  lambda = h c / E\n\n");

    int transitions[][2] = {{1,2},{1,3},{2,3},{2,4},{2,5},{3,4}};
    const char* names[] = {"Ly-alpha","Ly-beta","H-alpha","H-beta","H-gamma","Pa-alpha"};
    std::printf("%12s %5s %14s %14s %10s\n", "Transition", "n1-n2", "lam_koppa(nm)","lam_Ryd(nm)","err");
    for (int i = 0; i < 6; ++i) {
        int n1 = transitions[i][0], n2 = transitions[i][1];
        double dE = m_e * c2 / (2.0 * kH2) * (1.0/(n1*n1) - 1.0/(n2*n2));
        double lam_kop = h_planck * c / dE * 1e9;  // nm
        double lam_ryd = 1.0 / (R_inf * (1.0/(n1*n1) - 1.0/(n2*n2))) * 1e9;
        double err = std::abs(lam_kop - lam_ryd) / lam_ryd * 100;
        std::printf("%12s %2d-%2d %14.4f %14.4f %9.6f%%\n", names[i], n1, n2, lam_kop, lam_ryd, err);
    }

    subsep("3D. Energy in terms of koppa_p");
    std::printf("Since koppa_p = koppa_H * sqrt(R_p/a_0):\n");
    std::printf("  koppa_H^2 = koppa_p^2 * (a_0/R_p)\n");
    std::printf("  E_Ry = m_e c^2 / (2 * koppa_p^2 * a_0/R_p)\n");
    std::printf("       = m_e c^2 R_p / (2 * koppa_p^2 * a_0)\n\n");
    double E_from_kp = m_e * c2 * R_p / (2.0 * kp2 * a_0) / eV_to_J;
    std::printf("  E_Ry (from koppa_p) = %.10f eV\n", E_from_kp);
    std::printf("  E_Ry (CODATA)       = %.10f eV\n", E_Ry_eV);
    std::printf("  Match: %.12f\n", E_from_kp / E_Ry_eV);

    // ================================================================
    separator("CROSS-SCALE UNIFICATION", 4);
    // ================================================================

    subsep("4A. The electromagnetic mu decomposition");
    std::printf("mu_em = k_e * e^2 / m_e = %.10e m^3/s^2\n", mu_em);
    std::printf("mu_em = c^2 * R_p / koppa_p^2\n");
    double mu_from_kp = c2 * R_p / kp2;
    std::printf("      = %.10e m^3/s^2\n", mu_from_kp);
    std::printf("  Match: %.12f\n\n", mu_from_kp / mu_em);

    std::printf("Therefore: k_e * e^2 / m_e = c^2 * R_p / koppa_p^2\n");
    std::printf("Rearranging: koppa_p^2 = c^2 * R_p * m_e / (k_e * e^2)\n");
    double kp2_check = c2 * R_p * m_e / (k_e * e_q * e_q);
    std::printf("  koppa_p^2 (check) = %.10f\n", kp2_check);
    std::printf("  koppa_p^2 (1/a^2 * Rp/a0) = %.10f\n", kp2);
    std::printf("  Match: %.12f\n", kp2_check / kp2);

    subsep("4B. The hierarchy ratio decomposition");
    double mu_grav = G_N * m_p;
    double hierarchy = mu_em / mu_grav;
    std::printf("mu_em / mu_grav = (k_e e^2 / m_e) / (G m_p)\n");
    std::printf("  = k_e e^2 / (G m_e m_p)\n");
    std::printf("  = %.10e\n\n", hierarchy);

    std::printf("In terms of koppa:\n");
    std::printf("  mu_em / mu_grav = (c^2 R_p / koppa_p^2) / (G m_p)\n");
    std::printf("  = c^2 R_p / (koppa_p^2 * G * m_p)\n");
    double hier_kop = c2 * R_p / (kp2 * G_N * m_p);
    std::printf("  = %.10e\n", hier_kop);
    std::printf("  Match: %.12f\n\n", hier_kop / hierarchy);

    // What is this in terms of koppa_grav?
    double koppa_grav_p = c * std::sqrt(R_p / mu_grav);
    std::printf("Gravitational koppa of proton:\n");
    std::printf("  koppa_grav = c * sqrt(R_p / (G*m_p))\n");
    std::printf("  = %.10e\n", koppa_grav_p);
    std::printf("  koppa_grav^2 / koppa_em^2 = %.10e\n", (koppa_grav_p*koppa_grav_p)/kp2);
    std::printf("  = hierarchy ratio? %.10e\n", hierarchy);
    std::printf("  Match: %.12f\n", (koppa_grav_p*koppa_grav_p/kp2) / hierarchy);

    subsep("4C. Alpha from koppa and geometry alone");
    std::printf("alpha = sqrt(R_p/a_0) / koppa_p\n");
    double alpha_from_kp = std::sqrt(R_p / a_0) / kp;
    std::printf("  = %.10e\n", alpha_from_kp);
    std::printf("  alpha (CODATA) = %.10e\n", alpha);
    std::printf("  Match: %.12f\n\n", alpha_from_kp / alpha);

    std::printf("alpha^2 = R_p / (koppa_p^2 * a_0) = r_e / a_0\n");
    double a2_from_kp = R_p / (kp2 * a_0);
    double a2_from_re = r_e_CODATA / a_0;
    std::printf("  alpha^2 (from kp)   = %.10e\n", a2_from_kp);
    std::printf("  alpha^2 (from r_e)  = %.10e\n", a2_from_re);
    std::printf("  alpha^2 (CODATA)    = %.10e\n", alpha*alpha);
    std::printf("  Match kp:  %.12f\n", a2_from_kp / (alpha*alpha));
    std::printf("  Match r_e: %.12f\n", a2_from_re / (alpha*alpha));

    // ================================================================
    separator("COMPACTNESS SPECTRUM", 5);
    // ================================================================

    subsep("5A. All bodies sorted by koppa");
    struct KEntry { const char* name; double koppa; double koppa2; double compact; };
    KEntry entries[N_BODIES + 2]; // +proton_em, +proton_H

    for (int i = 0; i < N_BODIES; ++i) {
        double v = std::sqrt(bodies[i].GM / bodies[i].R);
        double k = c / v;
        entries[i] = {bodies[i].name, k, k*k, 2.0/(k*k)};
    }
    entries[N_BODIES]   = {"H atom", kH, kH2, 2.0/kH2};
    entries[N_BODIES+1] = {"Proton", kp, kp2, 2.0/kp2};
    int N_ENTRIES = N_BODIES + 2;

    // Sort by koppa ascending
    std::sort(entries, entries + N_ENTRIES, [](const KEntry& a, const KEntry& b) {
        return a.koppa < b.koppa;
    });

    std::printf("%-12s %16s %16s %16s\n", "Body", "koppa", "koppa^2", "Compactness");
    for (int i = 0; i < N_ENTRIES; ++i) {
        std::printf("%-12s %16.6f %16.4f %16.6e\n",
            entries[i].name, entries[i].koppa, entries[i].koppa2, entries[i].compact);
    }

    subsep("5B. Koppa ratios between bodies");
    std::printf("%-12s / %-12s = %12s %12s\n", "Body A", "Body B", "koppa_ratio", "koppa2_ratio");
    const char* pairs[][2] = {{"Sun","Jupiter"},{"Sun","Earth"},{"Jupiter","Saturn"},
                              {"Earth","Moon"},{"Sun","Proton"},{"H atom","Proton"}};
    for (auto& pair : pairs) {
        KEntry* a = nullptr; KEntry* b = nullptr;
        for (int i = 0; i < N_ENTRIES; ++i) {
            if (std::strcmp(entries[i].name, pair[0]) == 0) a = &entries[i];
            if (std::strcmp(entries[i].name, pair[1]) == 0) b = &entries[i];
        }
        if (a && b) {
            std::printf("%-12s / %-12s = %12.6f %12.4f\n",
                pair[0], pair[1], a->koppa / b->koppa, a->koppa2 / b->koppa2);
        }
    }

    subsep("5C. Black hole limit");
    std::printf("When R = r_s: koppa^2 = 2R/r_s = 2, koppa = sqrt(2) = %.10f\n", std::sqrt(2.0));
    std::printf("This is where v_surf = c/sqrt(2) = v_esc = c\n");
    std::printf("A black hole has koppa = sqrt(2). Below that, no stable orbit.\n\n");
    std::printf("Neutron star (typical R=10km, M=1.4 M_sun):\n");
    double GM_ns = 1.4 * 1.3271244e20;  // approximate
    double R_ns  = 1e4; // 10 km
    double k_ns  = c / std::sqrt(GM_ns / R_ns);
    std::printf("  koppa = c/sqrt(GM/R) = %.6f\n", k_ns);
    std::printf("  Compactness = 2/koppa^2 = %.6f\n", 2.0/(k_ns*k_ns));
    std::printf("  (For comparison, BH limit: compactness = 1.0)\n");

    // ================================================================
    separator("THE k^2 IDENTITY CHAIN", 6);
    // ================================================================

    subsep("6A. koppa^2 * r_Koppa = R for all celestial bodies");
    std::printf("%-10s %14s %14s %14s %12s\n",
        "Body", "koppa^2", "r_Koppa (m)", "kp2*r_K (m)", "R (m)");
    for (int i = 0; i < N_BODIES; ++i) {
        double v = std::sqrt(bodies[i].GM / bodies[i].R);
        double k = c / v;
        double k2 = k * k;
        double rK = bodies[i].R / k2;
        std::printf("%-10s %14.4f %14.6e %14.6e %12.6e\n",
            bodies[i].name, k2, rK, k2*rK, bodies[i].R);
    }

    subsep("6B. Nested identities for hydrogen");
    std::printf("Level 0 (Koppa radius / classical electron radius):\n");
    std::printf("  r_e = %.10e m\n\n", r_Kp);

    std::printf("Level 1 (proton koppa): koppa_p^2 * r_e = R_p\n");
    std::printf("  %.6f * %.4e = %.4e (R_p = %.4e) match=%.12f\n\n",
        kp2, r_Kp, kp2*r_Kp, R_p, kp2*r_Kp/R_p);

    std::printf("Level 2 (hydrogen koppa): koppa_H^2 * r_e = a_0\n");
    std::printf("  %.4f * %.4e = %.4e (a_0 = %.4e) match=%.12f\n\n",
        kH2, r_Kp, kH2*r_Kp, a_0, kH2*r_Kp/a_0);

    std::printf("Level 3: (koppa_H / koppa_p)^2 = a_0/R_p\n");
    double ratio_k = kH / kp;
    std::printf("  (%.6f / %.6f)^2 = %.4f\n", kH, kp, ratio_k*ratio_k);
    std::printf("  a_0/R_p = %.4f\n", a_0/R_p);
    std::printf("  match = %.12f\n\n", (ratio_k*ratio_k) / (a_0/R_p));

    std::printf("CHAIN: r_e --[*kp^2]--> R_p --[*kH^2/kp^2]--> a_0\n");
    std::printf("  = r_e * kp^2 * (kH/kp)^2 = r_e * kH^2\n");

    // ================================================================
    separator("DERIVED QUANTITIES & NATURAL UNITS", 7);
    // ================================================================

    subsep("7A. G expressed via koppa");
    std::printf("G = c^2 R / (koppa^2 M)  for any body\n\n");
    // Using Earth + known mass
    double M_earth = 5.972168e24; // kg (IAU)
    double k_earth = c / std::sqrt(bodies[3].GM / bodies[3].R);
    double G_from_earth = c2 * bodies[3].R / (k_earth*k_earth * M_earth);
    std::printf("From Earth: G = c^2 * R_polar / (koppa^2 * M_earth)\n");
    std::printf("  = %.6e m^3 kg^-1 s^-2\n", G_from_earth);
    std::printf("  G (CODATA) = %.6e m^3 kg^-1 s^-2\n", G_N);
    std::printf("  Match: %.10f\n\n", G_from_earth / G_N);

    subsep("7B. Planck length from koppa");
    double l_P = std::sqrt(hbar * G_N / (c * c * c));
    std::printf("Planck length l_P = sqrt(hbar G / c^3) = %.10e m\n", l_P);
    std::printf("\nIn terms of koppa (using Earth):\n");
    double l_P_from_kop = std::sqrt(hbar * c2 * bodies[3].R / (k_earth*k_earth * M_earth * c*c*c));
    std::printf("  l_P = sqrt(hbar * c^2 R / (kop^2 M c^3))\n");
    std::printf("      = sqrt(hbar R / (kop^2 M c))\n");
    std::printf("      = %.10e m\n", l_P_from_kop);
    std::printf("  Match: %.12f\n", l_P_from_kop / l_P);

    subsep("7C. Dimensionless physics from koppa alone");
    std::printf("Given only koppa_p = %.10f, we can derive:\n\n", kp);
    std::printf("  alpha = sqrt(R_p/a_0) / koppa_p\n");
    std::printf("  But R_p/a_0 = koppa_p^2 * alpha^2 (circular)\n\n");
    std::printf("  However: alpha^2 = r_e/a_0 is INDEPENDENT of koppa\n");
    std::printf("  And koppa_p = alpha * sqrt(a_0/r_e) * sqrt(R_p/a_0)\n");
    std::printf("  = alpha * sqrt(R_p/r_e) = alpha * sqrt(R_p/(alpha^2 * a_0))\n");
    std::printf("  = sqrt(R_p/a_0) / alpha  ... (confirmed circular)\n\n");

    std::printf("KEY: koppa_p contains alpha and the geometry ratio R_p/a_0\n");
    std::printf("     They cannot be separated without external measurement.\n");
    std::printf("     koppa_p is the product: (1/alpha) * sqrt(R_p/a_0)\n");
    std::printf("     where both factors are independently measurable.\n");

    subsep("7D. The three fundamental lengths and koppa");
    std::printf("Three lengths define all of atomic physics:\n\n");
    std::printf("  r_e  = %.10e m  (classical electron radius)\n", r_e_CODATA);
    std::printf("  R_p  = %.10e m  (proton charge radius)\n", R_p);
    std::printf("  a_0  = %.10e m  (Bohr radius)\n\n", a_0);

    std::printf("Relationships:\n");
    std::printf("  R_p = koppa_p^2 * r_e   ==> R_p/r_e = koppa_p^2 = %.6f\n", kp2);
    double Rp_over_re = R_p / r_e_CODATA;
    std::printf("  R_p/r_e (measured)      = %.6f\n", Rp_over_re);
    std::printf("  Match: %.10f\n\n", kp2 / Rp_over_re);

    std::printf("  a_0 = koppa_H^2 * r_e   ==> a_0/r_e = koppa_H^2 = %.4f\n", kH2);
    double a0_over_re = a_0 / r_e_CODATA;
    std::printf("  a_0/r_e (measured)      = %.4f\n", a0_over_re);
    std::printf("  Match: %.10f\n\n", kH2 / a0_over_re);

    std::printf("  a_0 / R_p = (koppa_H / koppa_p)^2 = %.4f\n", (kH/kp)*(kH/kp));
    std::printf("  a_0/R_p (measured)      = %.4f\n", a_0/R_p);
    std::printf("  Match: %.10f\n\n", ((kH/kp)*(kH/kp)) / (a_0/R_p));

    std::printf("RESULT: The classical electron radius r_e is the PIVOT.\n");
    std::printf("  It sits at the centre of a koppa-squared ladder:\n");
    std::printf("  r_e  --[*koppa_p^2]--> R_p   (upward to nuclear scale)\n");
    std::printf("  r_e  --[*koppa_H^2]--> a_0   (upward to atomic scale)\n");
    std::printf("  The ratio a_0/R_p = (koppa_H/koppa_p)^2 = 1/alpha^2 * (a_0/R_p)\n");
    std::printf("  Wait - that's circular. The CLEAN statement:\n\n");
    std::printf("  r_e is the Koppa radius (v=c boundary) of the proton.\n");
    std::printf("  Multiplying by koppa^2 scales it to the relevant radius.\n");
    std::printf("  proton koppa gives the proton radius.\n");
    std::printf("  hydrogen koppa gives the electron orbit radius.\n");
    std::printf("  These are different koppa values for the SAME Koppa radius.\n");

    std::printf("\n\n################################################################\n");
    std::printf("  INVESTIGATION COMPLETE\n");
    std::printf("################################################################\n");

    return 0;
}
