// koppa_ladder.cpp — Virial departure, bonding efficiency, chemical octave
// C++20 | CODATA 2018 | Independent calculation
// Compile: cl /std:c++20 /EHsc /O2 /utf-8 koppa_ladder.cpp

#include <cmath>
#include <cstdio>
#include <cstring>
#include <algorithm>

// ============================================================================
// CONSTANTS
// ============================================================================
constexpr double c       = 299'792'458.0;
constexpr double c2      = c * c;
constexpr double m_e     = 9.1093837015e-31;
constexpr double eV_J    = 1.602176634e-19;
constexpr double alpha   = 7.2973525693e-3;
constexpr double inv_a   = 1.0 / alpha;               // 137.036
constexpr double alpha_c = alpha * c;                  // 2,187,691 m/s
constexpr double k_e     = 8.9875517923e9;
constexpr double e_q     = 1.602176634e-19;
constexpr double a_0     = 5.29177210903e-11;          // Bohr radius
constexpr double r_e     = 2.8179403262e-15;           // classical electron radius
constexpr double hbar    = 1.054571817e-34;
constexpr double pi      = 3.14159265358979323846;

// Reduced Compton wavelength
constexpr double lambda_C_bar = hbar / (m_e * c);      // = alpha * a_0

// Coulomb potential unit: k_e * e^2 in eV*m
constexpr double ke_e2   = k_e * e_q * e_q;            // in J*m
constexpr double ke_e2_eV = ke_e2 / eV_J;              // in eV*m

// kJ/mol -> eV
constexpr double kJ_to_eV = 1.0 / 96.4853;

// ============================================================================
// BOND DATA (CRC Handbook / NIST CCCBDB)
// ============================================================================
struct Bond {
    const char* name;
    double D_kJ;        // kJ/mol
    double r_A;         // bond length in Angstroms
    int order;
    int lone_pairs;     // total lone pairs in bond region
};

constexpr Bond bonds[] = {
    {"H-H",    435.78,  0.741, 1, 0},
    {"F-F",    158.67,  1.412, 1, 6},
    {"Cl-Cl",  242.58,  1.988, 1, 6},
    {"O-O",    146.0,   1.480, 1, 4},   // peroxide O-O single
    {"O=O",    498.36,  1.208, 2, 4},
    {"N-N",    160.0,   1.450, 1, 4},
    {"N=N",    418.0,   1.250, 2, 2},
    {"N~N",    945.33,  1.098, 3, 2},   // N≡N
    {"C-C",    346.0,   1.540, 1, 0},
    {"C=C",    614.0,   1.340, 2, 0},
    {"C~C",    839.0,   1.200, 3, 0},   // C≡C
    {"O-H",    463.0,   0.958, 1, 2},
    {"N-H",    391.0,   1.012, 1, 0},
    {"C-H",    414.0,   1.087, 1, 0},
    {"H-F",    569.87,  0.917, 1, 3},
    {"C-O",    358.0,   1.430, 1, 2},
    {"C=O",    799.0,   1.210, 2, 2},
    {"N-O",    201.0,   1.440, 1, 1},
    {"Si-O",   452.0,   1.610, 1, 2},  // added for virial test
};
constexpr int N_BONDS = sizeof(bonds) / sizeof(bonds[0]);

// ============================================================================
int main() {

    std::printf("================================================================\n");
    std::printf("  THE KOPPA LADDER — Virial, Efficiency, Chemical Octave\n");
    std::printf("  All constants: CODATA 2018\n");
    std::printf("================================================================\n");

    // ================================================================
    std::printf("\n\n################################################################\n");
    std::printf("  PHASE 1: THE THREE ELECTRON SCALES\n");
    std::printf("################################################################\n\n");

    std::printf("Three characteristic lengths of the electron:\n\n");
    std::printf("  r_e           = %.10e m  (classical electron radius)\n", r_e);
    std::printf("  lambda_C_bar  = %.10e m  (reduced Compton wavelength)\n", lambda_C_bar);
    std::printf("  a_0           = %.10e m  (Bohr radius)\n\n", a_0);

    std::printf("Ratios:\n");
    std::printf("  lambda_C_bar / r_e  = %.10f  (claim: 1/alpha = %.6f)\n",
        lambda_C_bar / r_e, inv_a);
    std::printf("  a_0 / lambda_C_bar  = %.10f  (claim: 1/alpha = %.6f)\n",
        a_0 / lambda_C_bar, inv_a);
    std::printf("  a_0 / r_e           = %.10f  (claim: 1/alpha^2 = %.4f)\n",
        a_0 / r_e, 1.0/(alpha*alpha));

    std::printf("\nVerify: r_e = alpha^2 * a_0\n");
    double re_check = alpha * alpha * a_0;
    std::printf("  alpha^2 * a_0 = %.10e m\n", re_check);
    std::printf("  r_e (CODATA)  = %.10e m\n", r_e);
    std::printf("  Match: %.12f\n", re_check / r_e);

    std::printf("\nVerify: lambda_C_bar = alpha * a_0\n");
    double lc_check = alpha * a_0;
    std::printf("  alpha * a_0     = %.10e m\n", lc_check);
    std::printf("  lambda_C_bar    = %.10e m\n", lambda_C_bar);
    std::printf("  Match: %.12f\n", lc_check / lambda_C_bar);

    // Koppa values for the three scales
    // v = (c/kp) * sqrt(R_p/r), so at radius r, kappa_local = c/v
    // But for the electron ladder, the reference is the Bohr system:
    // v_n = alpha*c/n, so kappa = c / v = n/alpha = n * 137.036
    // For the three lengths, what kappa corresponds to each?
    // r_e: this is where v = c, so kappa = 1
    // lambda_C_bar: v at this radius = c * sqrt(r_e / lambda_C_bar) = c * sqrt(alpha) 
    //   so kappa = c / v = 1/sqrt(alpha)
    // a_0: v = alpha*c, so kappa = 1/alpha = 137.036

    double kappa_re = 1.0;
    double kappa_lc = 1.0 / std::sqrt(alpha);
    double kappa_a0 = inv_a;

    std::printf("\nKoppa values on the ladder:\n");
    std::printf("  r_e:           kappa = %.6f  (v = c)\n", kappa_re);
    std::printf("  lambda_C_bar:  kappa = %.6f  (v = c*sqrt(alpha) = %.0f m/s)\n",
        kappa_lc, c * std::sqrt(alpha));
    std::printf("  a_0:           kappa = %.6f  (v = alpha*c = %.0f m/s)\n",
        kappa_a0, alpha_c);

    std::printf("\nNote: kappa_lc / kappa_re = %.6f = 1/sqrt(alpha)\n", kappa_lc);
    std::printf("      kappa_a0 / kappa_lc = %.6f = 1/sqrt(alpha)\n", kappa_a0/kappa_lc);
    std::printf("      Each step is 1/sqrt(alpha) = %.6f on the ladder\n", 1.0/std::sqrt(alpha));

    // Actually, the user claims each step is 1/alpha. Let me check:
    std::printf("\nUser claims each step multiplies by 1/alpha:\n");
    std::printf("  r_e * (1/alpha) = %.10e  vs lambda_C_bar = %.10e  ratio=%.10f\n",
        r_e / alpha, lambda_C_bar, (r_e/alpha)/lambda_C_bar);
    std::printf("  lambda_C_bar * (1/alpha) = %.10e  vs a_0 = %.10e  ratio=%.10f\n",
        lambda_C_bar / alpha, a_0, (lambda_C_bar/alpha)/a_0);
    std::printf("  YES: in LENGTH, each step is 1/alpha\n");
    std::printf("  In KAPPA (velocity), each step is sqrt(1/alpha) because v ~ 1/sqrt(r)\n");

    // ================================================================
    std::printf("\n\n################################################################\n");
    std::printf("  PHASE 2: VIRIAL THEOREM IN KOPPA LANGUAGE\n");
    std::printf("################################################################\n\n");

    std::printf("For Bohr orbits: kappa_r = kappa_E must hold if virial is exact.\n\n");
    std::printf("Define:\n");
    std::printf("  kappa_r = sqrt(a_0 / r_n) / alpha  (from radius)\n");
    std::printf("    where r_n = n^2 * a_0, so kappa_r = 1/(n*alpha) = n * 137.036\n");
    std::printf("    Wait, that's not right. Let me be careful.\n\n");

    std::printf("At Bohr level n:  r_n = n^2 * a_0,  v_n = alpha*c/n\n");
    std::printf("  kappa_n = c/v_n = n/alpha = n * %.6f\n\n", inv_a);

    std::printf("Energy: E_n = m_e c^2 / (2 kappa_n^2)\n");
    std::printf("  so kappa_E = sqrt(m_e c^2 / (2 E_n))\n\n");

    std::printf("%3s %12s %12s %12s %12s %10s\n",
        "n", "r_n (m)", "E_n (eV)", "kappa_r", "kappa_E", "kr/kE");
    for (int n = 1; n <= 5; ++n) {
        double r_n = (double)(n*n) * a_0;
        double v_n = alpha_c / n;
        double kappa_r = c / v_n;
        double E_n = 0.5 * m_e * v_n * v_n / eV_J;
        double kappa_E = std::sqrt(m_e * c2 / (2.0 * E_n * eV_J));
        std::printf("%3d %12.4e %12.6f %12.4f %12.4f %10.6f\n",
            n, r_n, E_n, kappa_r, kappa_E, kappa_r/kappa_E);
    }

    // ================================================================
    std::printf("\n\n################################################################\n");
    std::printf("  PHASE 3: MOLECULAR VIRIAL DEPARTURE — kappa_r vs kappa_E\n");
    std::printf("################################################################\n\n");

    std::printf("For each molecular bond:\n");
    std::printf("  kappa_r = from bond length r: kappa_r = sqrt(a_0/r) / alpha\n");
    std::printf("    No — need to use the right formula.\n");
    std::printf("  In the Bohr system, r = a_0 * (kappa * alpha)^2\n");
    std::printf("  So kappa_r = sqrt(r / a_0) / alpha\n");
    std::printf("  E = m_e c^2 / (2 kappa_E^2)\n");
    std::printf("  kappa_E = c / sqrt(2E/m_e)\n\n");

    // Actually, let me think about what kappa_r and kappa_E mean carefully.
    // In Bohr: r_n = n^2 * a_0, and kappa = n * (1/alpha)
    // So r = (kappa * alpha)^2 * a_0 = kappa^2 * alpha^2 * a_0 = kappa^2 * r_e
    // Therefore: kappa_r = sqrt(r / r_e)

    // For energy: E = m_e c^2 / (2 kappa_E^2)
    // kappa_E = sqrt(m_e c^2 / (2E)) = c / sqrt(2E/m_e) = c / v_bond

    std::printf("CORRECTED definitions:\n");
    std::printf("  kappa_r = sqrt(r / r_e)              (position on ladder from r)\n");
    std::printf("  kappa_E = c / sqrt(2*D_bond / m_e)   (position on ladder from energy)\n");
    std::printf("  For Bohr: kappa_r = kappa_E = n/alpha (virial exact)\n\n");

    // Verify for Bohr levels first
    std::printf("Bohr verification:\n");
    std::printf("%3s %12s %12s %10s\n", "n", "kappa_r", "kappa_E", "kr/kE");
    for (int n = 1; n <= 3; ++n) {
        double r_n = (double)(n*n) * a_0;
        double E_n = 0.5 * m_e * (alpha_c/n) * (alpha_c/n);
        double kr = std::sqrt(r_n / r_e);
        double kE = c / std::sqrt(2.0 * E_n / m_e);
        std::printf("%3d %12.4f %12.4f %10.6f\n", n, kr, kE, kr/kE);
    }

    std::printf("\nMolecular bonds:\n");
    std::printf("%-8s %8s %8s %10s %10s %10s %12s\n",
        "Bond", "r(A)", "D(eV)", "kappa_r", "kappa_E", "kr/kE", "category");
    for (int i = 0; i < N_BONDS; ++i) {
        double r_m = bonds[i].r_A * 1e-10;  // Angstroms to meters
        double D_eV = bonds[i].D_kJ * kJ_to_eV;
        double D_J = D_eV * eV_J;

        double kr = std::sqrt(r_m / r_e);
        double kE = c / std::sqrt(2.0 * D_J / m_e);

        const char* cat;
        double ratio = kr / kE;
        if (ratio < 0.95) cat = "COMPRESSED";
        else if (ratio > 1.05) cat = "STRETCHED";
        else cat = "~VIRIAL";

        std::printf("%-8s %8.3f %8.4f %10.4f %10.4f %10.4f %12s\n",
            bonds[i].name, bonds[i].r_A, D_eV, kr, kE, ratio, cat);
    }

    // ================================================================
    std::printf("\n\n################################################################\n");
    std::printf("  PHASE 4: BONDING EFFICIENCY f = D*r / (k_e*e^2/2)\n");
    std::printf("################################################################\n\n");

    // f measures what fraction of the Coulomb interaction the bond captures
    // For a pure Coulomb system: V = -k_e*e^2/r, and virial gives E = V/2
    // So the "available" binding at distance r is k_e*e^2/(2r)
    // Bonding efficiency: f = D / (k_e*e^2/(2r)) = 2*D*r / (k_e*e^2)

    double half_ke_e2_eV_A = ke_e2_eV * 1e10 / 2.0;  // in eV*Angstrom (k_e*e^2/2 in eV*A)
    std::printf("Reference: k_e*e^2/2 = %.6f eV*A\n\n", half_ke_e2_eV_A);

    std::printf("%-8s %8s %8s %10s %10s\n",
        "Bond", "D(eV)", "r(A)", "D*r(eV*A)", "f = 2Dr/kee2");
    for (int i = 0; i < N_BONDS; ++i) {
        double D_eV = bonds[i].D_kJ * kJ_to_eV;
        double Dr = D_eV * bonds[i].r_A;
        double f = Dr / half_ke_e2_eV_A;
        std::printf("%-8s %8.4f %8.3f %10.4f %10.4f\n",
            bonds[i].name, D_eV, bonds[i].r_A, Dr, f);
    }

    // Sort by f for clarity
    std::printf("\nSorted by bonding efficiency f:\n\n");
    struct FEntry { const char* name; double f; double D; double r; int lp; };
    FEntry fentries[N_BONDS];
    for (int i = 0; i < N_BONDS; ++i) {
        double D_eV = bonds[i].D_kJ * kJ_to_eV;
        double Dr = D_eV * bonds[i].r_A;
        fentries[i] = {bonds[i].name, Dr / half_ke_e2_eV_A, D_eV, bonds[i].r_A, bonds[i].lone_pairs};
    }
    std::sort(fentries, fentries + N_BONDS, [](const FEntry& a, const FEntry& b){
        return a.f < b.f;
    });

    std::printf("%-8s %10s %8s %8s %4s\n", "Bond", "f", "D(eV)", "r(A)", "LP");
    for (int i = 0; i < N_BONDS; ++i) {
        std::printf("%-8s %10.4f %8.4f %8.3f %4d\n",
            fentries[i].name, fentries[i].f, fentries[i].D, fentries[i].r, fentries[i].lp);
    }

    // ================================================================
    std::printf("\n\n################################################################\n");
    std::printf("  PHASE 5: THE CHEMICAL OCTAVE — WHERE BONDS SIT ON THE LADDER\n");
    std::printf("################################################################\n\n");

    std::printf("Bohr reference levels:\n");
    for (int n = 1; n <= 5; ++n) {
        double kE = (double)n * inv_a;
        double E = m_e * c2 / (2.0 * kE * kE) / eV_J;
        std::printf("  n=%d: kappa = %10.3f,  E = %8.4f eV\n", n, kE, E);
    }

    std::printf("\nMolecular bonds on the kappa_E ladder:\n\n");
    struct LEntry { const char* name; double kE; double D; };
    LEntry lentries[N_BONDS];
    for (int i = 0; i < N_BONDS; ++i) {
        double D_eV = bonds[i].D_kJ * kJ_to_eV;
        double D_J = D_eV * eV_J;
        double kE = c / std::sqrt(2.0 * D_J / m_e);
        lentries[i] = {bonds[i].name, kE, D_eV};
    }
    std::sort(lentries, lentries + N_BONDS, [](const LEntry& a, const LEntry& b){
        return a.kE < b.kE;
    });

    std::printf("%-8s %10s %8s %20s\n", "Bond", "kappa_E", "D(eV)", "Bohr region");
    for (int i = 0; i < N_BONDS; ++i) {
        const char* region;
        if (lentries[i].kE < inv_a * 1.5) region = "below n=1 to ~n=1.5";
        else if (lentries[i].kE < inv_a * 2.0) region = "n=1 to n=2";
        else if (lentries[i].kE < inv_a * 3.0) region = "n=2 to n=3";
        else if (lentries[i].kE < inv_a * 4.0) region = "n=3 to n=4";
        else region = "above n=4";

        std::printf("%-8s %10.2f %8.4f %20s\n",
            lentries[i].name, lentries[i].kE, lentries[i].D, region);
    }

    std::printf("\nChemical octave boundaries:\n");
    std::printf("  n=1: kappa = %.3f,  E = %.4f eV\n", inv_a, 13.6);
    std::printf("  n=2: kappa = %.3f,  E = %.4f eV\n", 2*inv_a, 13.6/4);
    std::printf("  n=3: kappa = %.3f,  E = %.4f eV\n", 3*inv_a, 13.6/9);
    std::printf("  Most bonds fall between n=1 and n=3 (kappa %.0f to %.0f)\n",
        inv_a, 3*inv_a);

    // ================================================================
    std::printf("\n\n################################################################\n");
    std::printf("  PHASE 6: THE MOLECULAR zk^2 CONSTRAINT\n");
    std::printf("################################################################\n\n");

    std::printf("At nuclear/celestial scale: z * kappa^2 = 1  (gravitational redshift)\n");
    std::printf("At Bohr orbit: z * kappa^2 = alpha^2\n");
    std::printf("  z = 1/kappa^2,  kappa = n/alpha\n");
    std::printf("  z * kappa^2 = (1/kappa^2) * kappa^2 = 1  ??\n\n");

    std::printf("Wait — for Bohr orbits, the 'z' is the energy ratio:\n");
    std::printf("  z_n = E_n / (m_e c^2) = alpha^2 / (2n^2)\n");
    std::printf("  kappa_n^2 = n^2 / alpha^2\n");
    std::printf("  z_n * kappa_n^2 = (alpha^2/(2n^2)) * (n^2/alpha^2) = 1/2\n\n");

    std::printf("Verification:\n");
    for (int n = 1; n <= 5; ++n) {
        double z_n = alpha * alpha / (2.0 * n * n);
        double k2_n = (double)(n*n) / (alpha*alpha);
        std::printf("  n=%d: z = %.10e, kappa^2 = %.4f, z*k^2 = %.10f\n",
            n, z_n, k2_n, z_n * k2_n);
    }

    std::printf("\nFor molecular bonds:\n");
    std::printf("  z_bond = D / (m_e c^2) = D / 510999 eV\n");
    std::printf("  kappa_E^2 = m_e c^2 / (2D)\n");
    std::printf("  z_bond * kappa_E^2 = (D/(m_e c^2)) * (m_e c^2 / (2D)) = 1/2  ALWAYS!\n\n");
    std::printf("  This is TRIVIALLY true — it's the definition of kappa_E.\n");
    std::printf("  The non-trivial statement is about z * kappa_r^2:\n\n");

    std::printf("%-8s %10s %12s %12s %12s\n",
        "Bond", "z_bond", "kappa_r^2", "z*kr^2", "z*kr^2 / 0.5");
    for (int i = 0; i < N_BONDS; ++i) {
        double D_eV = bonds[i].D_kJ * kJ_to_eV;
        double r_m = bonds[i].r_A * 1e-10;
        double z = D_eV / (m_e * c2 / eV_J);
        double kr2 = r_m / r_e;
        std::printf("%-8s %10.4e %12.4f %12.6e %12.6f\n",
            bonds[i].name, z, kr2, z*kr2, z*kr2 / 0.5);
    }

    std::printf("\nInterpretation: z*kr^2 / 0.5 = (kr/kE)^2 = virial departure squared\n");
    std::printf("For pure Coulomb virial: z*kr^2 = 0.5 exactly\n");
    std::printf("Departure from 0.5 measures how far the bond is from 1/r virial\n");

    // ================================================================
    std::printf("\n\n################################################################\n");
    std::printf("  PHASE 7: COMPLETE KOPPA LADDER — NUCLEAR TO CELESTIAL\n");
    std::printf("################################################################\n\n");

    struct LadderEntry { const char* name; double kappa; double r_m; double v; };
    LadderEntry ladder[] = {
        {"Proton (EM)",   0.5464, 8.414e-16, c/0.5464},
        {"c-boundary",    1.0, r_e, c},
        {"Compton",       1.0/std::sqrt(alpha), lambda_C_bar, c*std::sqrt(alpha)},
        {"Bohr n=1",      inv_a, a_0, alpha_c},
        {"Bohr n=2",      2*inv_a, 4*a_0, alpha_c/2},
        {"Bohr n=3",      3*inv_a, 9*a_0, alpha_c/3},
        {"Sun",           686.4, 6.957e8, c/686.4},
        {"Jupiter",       6887.0, 6.685e7, c/6887.0},
        {"Earth",         37859.0, 6.357e6, c/37859.0},
        {"Moon",          178425.0, 1.737e6, c/178425.0},
    };
    int N_LADDER = sizeof(ladder) / sizeof(ladder[0]);

    // Add molecular bonds to ladder
    std::printf("%-16s %14s %14s %14s %14s\n",
        "Name", "kappa", "kappa^2", "r (m)", "v (m/s)");
    std::printf("%-16s %14s %14s %14s %14s\n",
        "----", "-----", "-------", "-----", "-------");

    // Sort everything by kappa
    struct FullEntry { const char* name; double kappa; };
    FullEntry full[50];
    int nf = 0;

    for (int i = 0; i < N_LADDER; ++i) {
        full[nf++] = {ladder[i].name, ladder[i].kappa};
    }
    // Add molecular bonds using kappa_E
    for (int i = 0; i < N_BONDS; ++i) {
        double D_J = bonds[i].D_kJ * kJ_to_eV * eV_J;
        double kE = c / std::sqrt(2.0 * D_J / m_e);
        full[nf++] = {bonds[i].name, kE};
    }

    std::sort(full, full + nf, [](const FullEntry& a, const FullEntry& b){
        return a.kappa < b.kappa;
    });

    for (int i = 0; i < nf; ++i) {
        double k = full[i].kappa;
        double r = k * k * r_e;
        double v = c / k;
        std::printf("%-16s %14.4f %14.4f %14.4e %14.2f\n",
            full[i].name, k, k*k, r, v);
    }

    // ================================================================
    std::printf("\n\n################################################################\n");
    std::printf("  PHASE 8: THE COOPERATIVE PENALTY — INDEPENDENT CHECK\n");
    std::printf("################################################################\n\n");

    double CC1 = 346.0, CC2 = 614.0, CC3 = 839.0;  // kJ/mol
    double NN1 = 160.0, NN2 = 418.0, NN3 = 945.33;

    std::printf("C-C series:\n");
    double c_sigma = CC1 * kJ_to_eV;
    double c_pi1 = (CC2 - CC1) * kJ_to_eV;
    double c_pi2 = (CC3 - CC2) * kJ_to_eV;
    double c_additive = c_sigma + 2.0 * c_pi1;
    std::printf("  sigma:     %.4f eV\n", c_sigma);
    std::printf("  pi-1:      %.4f eV\n", c_pi1);
    std::printf("  pi-2:      %.4f eV\n", c_pi2);
    std::printf("  If additive:  sigma + 2*pi1 = %.4f eV\n", c_additive);
    std::printf("  Actual C~C:  %.4f eV\n", CC3 * kJ_to_eV);
    std::printf("  Penalty:     %.4f eV (actual is LESS than additive)\n",
        c_additive - CC3 * kJ_to_eV);
    std::printf("  This is a PACKING PENALTY — second pi competes for space\n\n");

    std::printf("N-N series:\n");
    double n_sigma = NN1 * kJ_to_eV;
    double n_pi1 = (NN2 - NN1) * kJ_to_eV;
    double n_pi2 = (NN3 - NN2) * kJ_to_eV;
    std::printf("  sigma:     %.4f eV\n", n_sigma);
    std::printf("  pi-1:      %.4f eV\n", n_pi1);
    std::printf("  pi-2:      %.4f eV\n", n_pi2);
    std::printf("  pi-1 > sigma by %.1f%%: COOPERATIVE\n", (n_pi1/n_sigma - 1)*100);
    std::printf("  pi-2 > pi-1 by %.1f%%: MORE COOPERATIVE\n", (n_pi2/n_pi1 - 1)*100);
    std::printf("  Total amplification: triple/single = %.4f (additive = 3.0)\n\n",
        NN3 / NN1);

    std::printf("WHY THE DIFFERENCE?\n");
    std::printf("  C-C: 0 lone pairs. pi-bonds compete with each other only.\n");
    std::printf("  N-N single: 4 lone pairs WEAKEN the sigma bond.\n");
    std::printf("  N=N triple: lone pairs move EXTERNAL to bond cage.\n");
    std::printf("  The 'cooperation' is partly the REMOVAL of LP repulsion,\n");
    std::printf("  not just pi-channel reinforcement.\n");
    std::printf("  Evidence: N-N single (%.4f eV) is weaker than C-C single (%.4f eV)\n",
        n_sigma, c_sigma);
    std::printf("  but N~N triple (%.4f eV) EXCEEDS C~C triple (%.4f eV).\n",
        NN3*kJ_to_eV, CC3*kJ_to_eV);

    std::printf("\n\n################################################################\n");
    std::printf("  INVESTIGATION COMPLETE\n");
    std::printf("################################################################\n");

    return 0;
}
