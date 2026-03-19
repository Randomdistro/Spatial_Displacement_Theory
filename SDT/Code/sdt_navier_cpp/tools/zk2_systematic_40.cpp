// zk2_systematic_40.cpp — Uniform z·k²=1 analysis for first 40 stable isotopes
// NO cherry-picking. Every element treated identically. Failures shown honestly.
// SDT / James Tyndall — March 2026
// C++20, no external dependencies.

#include <cmath>
#include <cstdio>
#include <array>
#include <string>
#include <algorithm>
#include <vector>
#include <numeric>

// ═══════════════════════════════════════════════════════════════════
// SECTION 0: Physical constants (CODATA 2018)
// ═══════════════════════════════════════════════════════════════════
namespace constants {
    constexpr double c       = 299'792'458.0;               // m/s (exact)
    constexpr double h       = 6.626'070'15e-34;            // J·s (exact)
    constexpr double hbar    = 1.054'571'817e-34;           // J·s (exact)
    constexpr double m_e     = 9.109'383'7015e-31;          // kg
    constexpr double m_p     = 1.672'621'923'69e-27;        // kg
    constexpr double e_charge= 1.602'176'634e-19;           // C (exact)
    constexpr double alpha   = 7.297'352'5693e-3;           // fine structure
    constexpr double alpha_inv = 137.035'999'084;           // 1/alpha
    constexpr double a0      = 5.291'772'109'03e-11;        // Bohr radius [m]
    constexpr double r_e     = 2.817'940'3262e-15;          // classical electron radius [m]
    constexpr double Ry_eV   = 13.605'693'122'994;          // Rydberg energy [eV]
    constexpr double eV_to_J = 1.602'176'634e-19;           // eV → J (exact)
    constexpr double m_u     = 1.660'539'066'60e-27;        // atomic mass unit [kg]
    constexpr double pi      = 3.14159265358979323846;
}

// ═══════════════════════════════════════════════════════════════════
// SECTION 1: Isotope data — NIST measured values
// Each entry: Z, A, symbol, name, I1 (eV), atomic_mass (u),
//             BE/A (MeV), nuclear_spin, abundance%
// ═══════════════════════════════════════════════════════════════════
struct IsotopeData {
    int Z;
    int A;
    const char* symbol;
    const char* name;
    double I1_eV;           // First ionisation energy [eV] (NIST)
    double atomic_mass_u;   // Atomic mass [u]
    double BE_per_A_MeV;    // Nuclear binding energy per nucleon [MeV]
    double nuclear_spin;    // Nuclear spin I
    double abundance_pct;   // Natural abundance [%]
    bool is_most_abundant;  // Bold in output
};

// First 40 stable isotopes ordered by (Z, A).
// NIST ASD for I1, AME2020 for masses/BE, NNDC for spins.
static constexpr std::array<IsotopeData, 40> isotopes = {{
    // Z  A   sym    name          I1(eV)    mass(u)        BE/A(MeV) I    abund%  bold
    {  1,  1, "H",   "Hydrogen",   13.5984,  1.00782503,    0.000,   0.5, 99.9885, true },
    {  1,  2, "D",   "Deuterium",  13.6025,  2.01410178,    1.112,   1.0,  0.0115, false},
    {  2,  3, "He3", "Helium-3",   24.5874,  3.01602932,    2.573,   0.5,  0.0001, false},
    {  2,  4, "He",  "Helium-4",   24.5874,  4.00260325,    7.074,   0.0, 99.9999, true },
    {  3,  6, "Li6", "Lithium-6",   5.3917,  6.01512280,    5.333,   1.0,  7.59,   false},
    {  3,  7, "Li",  "Lithium-7",   5.3917,  7.01600344,    5.606,   1.5, 92.41,   true },
    {  4,  9, "Be",  "Beryllium-9", 9.3227,  9.01218307,    6.463,   1.5,100.0,    true },
    {  5, 10, "B10", "Boron-10",    8.2980,  10.0129369,    6.475,   3.0, 19.9,    false},
    {  5, 11, "B",   "Boron-11",    8.2980,  11.0093054,    6.928,   1.5, 80.1,    true },
    {  6, 12, "C",   "Carbon-12",  11.2603,  12.0000000,    7.680,   0.0, 98.93,   true },
    {  6, 13, "C13", "Carbon-13",  11.2603,  13.0033548,    7.470,   0.5,  1.07,   false},
    {  7, 14, "N",   "Nitrogen-14",14.5341,  14.0030740,    7.476,   1.0, 99.636,  true },
    {  7, 15, "N15", "Nitrogen-15",14.5341,  15.0001089,    7.699,   0.5,  0.364,  false},
    {  8, 16, "O",   "Oxygen-16",  13.6181,  15.9949146,    7.976,   0.0, 99.757,  true },
    {  8, 17, "O17", "Oxygen-17",  13.6181,  16.9991318,    7.751,   2.5,  0.038,  false},
    {  8, 18, "O18", "Oxygen-18",  13.6181,  17.9991610,    7.767,   0.0,  0.205,  false},
    {  9, 19, "F",   "Fluorine-19",17.4228,  18.9984032,    7.779,   0.5,100.0,    true },
    { 10, 20, "Ne",  "Neon-20",    21.5646,  19.9924402,    8.032,   0.0, 90.48,   true },
    { 10, 21, "Ne21","Neon-21",    21.5646,  20.9938853,    7.972,   1.5,  0.27,   false},
    { 10, 22, "Ne22","Neon-22",    21.5646,  21.9913851,    8.081,   0.0,  9.25,   false},
    { 11, 23, "Na",  "Sodium-23",   5.1391,  22.9897693,    8.112,   1.5,100.0,    true },
    { 12, 24, "Mg",  "Magnesium-24",7.6462,  23.9850419,    8.261,   0.0, 78.99,   true },
    { 12, 25, "Mg25","Magnesium-25",7.6462,  24.9858370,    8.223,   2.5, 10.00,   false},
    { 12, 26, "Mg26","Magnesium-26",7.6462,  25.9825930,    8.334,   0.0, 11.01,   false},
    { 13, 27, "Al",  "Aluminium-27",5.9858,  26.9815385,    8.332,   2.5,100.0,    true },
    { 14, 28, "Si",  "Silicon-28",  8.1517,  27.9769265,    8.448,   0.0, 92.223,  true },
    { 14, 29, "Si29","Silicon-29",  8.1517,  28.9764947,    8.449,   0.5,  4.685,  false},
    { 14, 30, "Si30","Silicon-30",  8.1517,  29.9737702,    8.521,   0.0,  3.092,  false},
    { 15, 31, "P",   "Phosphorus-31",10.4867,30.9737634,    8.481,   0.5,100.0,    true },
    { 16, 32, "S",   "Sulfur-32",  10.3600,  31.9720707,    8.493,   0.0, 94.99,   true },
    { 16, 33, "S33", "Sulfur-33",  10.3600,  32.9714585,    8.498,   1.5,  0.75,   false},
    { 16, 34, "S34", "Sulfur-34",  10.3600,  33.9678670,    8.584,   0.0,  4.25,   false},
    { 16, 36, "S36", "Sulfur-36",  10.3600,  35.9670807,    8.576,   0.0,  0.01,   false},
    { 17, 35, "Cl",  "Chlorine-35",12.9676,  34.9688527,    8.520,   1.5, 75.76,   true },
    { 17, 37, "Cl37","Chlorine-37",12.9676,  36.9659026,    8.570,   1.5, 24.24,   false},
    { 18, 36, "Ar36","Argon-36",   15.7596,  35.9675451,    8.520,   0.0,  0.3336, false},
    { 18, 38, "Ar38","Argon-38",   15.7596,  37.9627322,    8.614,   0.0,  0.0629, false},
    { 18, 40, "Ar",  "Argon-40",   15.7596,  39.9623831,    8.595,   0.0, 99.6035, true },
    { 19, 39, "K",   "Potassium-39",4.3407,  38.9637065,    8.557,   1.5, 93.2581, true },
    { 20, 40, "Ca",  "Calcium-40",  6.1132,  39.9625909,    8.551,   0.0, 96.941,  true },
}};

// ═══════════════════════════════════════════════════════════════════
// SECTION 2: Electron configuration data (for n and Z_eff)
// ═══════════════════════════════════════════════════════════════════
struct ShellInfo {
    int n;          // principal quantum number of valence shell
    int l;          // angular momentum quantum number of valence
    int valence_e;  // electrons in valence subshell
    const char* config; // electron configuration string
};

// Valence shell info for Z=1 to Z=20
static constexpr std::array<ShellInfo, 20> shell_info = {{
    {1, 0, 1, "1s1"},           // H
    {1, 0, 2, "1s2"},           // He
    {2, 0, 1, "[He]2s1"},       // Li
    {2, 0, 2, "[He]2s2"},       // Be
    {2, 1, 1, "[He]2s2 2p1"},   // B
    {2, 1, 2, "[He]2s2 2p2"},   // C
    {2, 1, 3, "[He]2s2 2p3"},   // N
    {2, 1, 4, "[He]2s2 2p4"},   // O
    {2, 1, 5, "[He]2s2 2p5"},   // F
    {2, 1, 6, "[He]2s2 2p6"},   // Ne
    {3, 0, 1, "[Ne]3s1"},       // Na
    {3, 0, 2, "[Ne]3s2"},       // Mg
    {3, 1, 1, "[Ne]3s2 3p1"},   // Al
    {3, 1, 2, "[Ne]3s2 3p2"},   // Si
    {3, 1, 3, "[Ne]3s2 3p3"},   // P
    {3, 1, 4, "[Ne]3s2 3p4"},   // S
    {3, 1, 5, "[Ne]3s2 3p5"},   // Cl
    {3, 1, 6, "[Ne]3s2 3p6"},   // Ar
    {4, 0, 1, "[Ar]4s1"},       // K
    {4, 0, 2, "[Ar]4s2"},       // Ca
}};

// ═══════════════════════════════════════════════════════════════════
// SECTION 3: Core calculations — NO shortcuts, NO approximations
// ═══════════════════════════════════════════════════════════════════

struct ZK2Result {
    // Inputs
    int Z, A;
    const char* symbol;
    double I1_eV;
    int n_valence;
    
    // Derived from z·k²=1
    double Z_eff;           // from I1 = Ry * Z_eff^2 / n^2
    double k;               // = n / (alpha * Z_eff)
    double z;               // = 1/k^2
    double zk2;             // should be 1.000
    double v_orbital;       // = c/k [m/s]
    double v_over_alpha_c;  // v / (α·c) — test for rational fractions
    double r_orbital;       // = n^2 * a0 / Z_eff [m]
    double screening;       // S = Z - Z_eff
    double eta;             // η = S/(Z-1) if Z>1
    
    // Nuclear
    double BE_per_A;
    double nuclear_spin;
    bool even_even;         // even Z, even N?
    
    // Harmonic analysis
    int n_240;              // nearest integer n where v/(αc) = n/240
    double n_240_deviation; // fractional difference from nearest n/240
    
    // Prime analysis
    int Z_eff_rounded;      // nearest integer
    bool Z_eff_near_prime;  // is rounded Z_eff prime?
    
    // Flags
    bool is_most_abundant;
};

static bool is_prime(int n) {
    if (n < 2) return false;
    if (n < 4) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; i * i <= n; i += 6)
        if (n % i == 0 || n % (i + 2) == 0) return false;
    return true;
}

static ZK2Result compute(const IsotopeData& iso) {
    using namespace constants;
    
    ZK2Result r{};
    r.Z = iso.Z;
    r.A = iso.A;
    r.symbol = iso.symbol;
    r.I1_eV = iso.I1_eV;
    r.is_most_abundant = iso.is_most_abundant;
    r.BE_per_A = iso.BE_per_A_MeV;
    r.nuclear_spin = iso.nuclear_spin;
    
    int N = iso.A - iso.Z;
    r.even_even = (iso.Z % 2 == 0) && (N % 2 == 0);
    
    // Get valence shell quantum number
    int idx = iso.Z - 1;  // 0-indexed
    if (idx >= 0 && idx < 20) {
        r.n_valence = shell_info[static_cast<size_t>(idx)].n;
    } else {
        r.n_valence = 1; // fallback
    }
    
    // ── Z_eff from measured ionisation energy ──
    // E = Ry * Z_eff^2 / n^2
    // Z_eff = n * sqrt(I1 / Ry)
    double n = static_cast<double>(r.n_valence);
    r.Z_eff = n * std::sqrt(iso.I1_eV / Ry_eV);
    
    // ── k from z·k²=1 ──
    // k = n / (alpha * Z_eff)
    r.k = n / (alpha * r.Z_eff);
    
    // ── z from z·k²=1 ──
    r.z = 1.0 / (r.k * r.k);
    
    // ── verification ──
    r.zk2 = r.z * r.k * r.k;   // must be 1.000
    
    // ── orbital velocity ──
    r.v_orbital = c / r.k;
    r.v_over_alpha_c = r.v_orbital / (alpha * c);
    
    // ── orbital radius ──
    r.r_orbital = n * n * a0 / r.Z_eff;
    
    // ── screening ──
    r.screening = static_cast<double>(iso.Z) - r.Z_eff;
    r.eta = (iso.Z > 1) ? r.screening / (static_cast<double>(iso.Z) - 1.0) : 0.0;
    
    // ── N=240 harmonic ──
    double v_ratio = r.v_over_alpha_c;
    int nearest_n = static_cast<int>(std::round(v_ratio * 240.0));
    r.n_240 = nearest_n;
    double expected_ratio = static_cast<double>(nearest_n) / 240.0;
    r.n_240_deviation = (v_ratio - expected_ratio) / expected_ratio;
    
    // ── prime analysis ──
    r.Z_eff_rounded = static_cast<int>(std::round(r.Z_eff));
    r.Z_eff_near_prime = is_prime(r.Z_eff_rounded);
    
    return r;
}

// ═══════════════════════════════════════════════════════════════════
// SECTION 4: Output — EVERYTHING, honestly
// ═══════════════════════════════════════════════════════════════════

static void print_separator(const char* title) {
    std::printf("\n");
    for (int i = 0; i < 100; ++i) std::printf("=");
    std::printf("\n  %s\n", title);
    for (int i = 0; i < 100; ++i) std::printf("=");
    std::printf("\n\n");
}

static void print_subsep(const char* title) {
    std::printf("\n--- %s ---\n\n", title);
}

int main() {
    std::printf("z·k² = 1 SYSTEMATIC ANALYSIS — FIRST 40 STABLE ISOTOPES\n");
    std::printf("NO cherry-picking. Every element treated identically.\n");
    std::printf("Failures shown honestly alongside successes.\n");
    std::printf("──────────────────────────────────────────────────────\n\n");
    
    // Compute all results
    std::vector<ZK2Result> results;
    results.reserve(40);
    for (auto& iso : isotopes) {
        results.push_back(compute(iso));
    }
    
    // ═══════════════════════════════════════════════════════════
    // TABLE 1: Core z·k²=1 parameters
    // ═══════════════════════════════════════════════════════════
    print_separator("TABLE 1: z·k²=1 Core Parameters");
    
    std::printf("%-5s %-4s %2s %2s  %9s  %8s  %10s  %12s  %6s\n",
        "Iso", "Sym", "Z", "n", "I1(eV)", "Z_eff", "k", "z", "z·k²");
    for (int i = 0; i < 80; ++i) std::printf("-");
    std::printf("\n");
    
    for (auto& r : results) {
        const char* mark = r.is_most_abundant ? "*" : " ";
        std::printf("%-3d%s %-4s %2d %2d  %9.4f  %8.6f  %10.3f  %12.6e  %6.4f\n",
            r.A, mark, r.symbol, r.Z, r.n_valence,
            r.I1_eV, r.Z_eff, r.k, r.z, r.zk2);
    }
    std::printf("\n* = most abundant isotope\n");
    
    // z·k² verification summary
    double max_dev = 0.0;
    for (auto& r : results) {
        double dev = std::abs(r.zk2 - 1.0);
        if (dev > max_dev) max_dev = dev;
    }
    std::printf("\nz·k² = 1 verification: max deviation = %.2e (should be ~machine epsilon)\n", max_dev);
    
    // ═══════════════════════════════════════════════════════════
    // TABLE 2: Velocities and radii
    // ═══════════════════════════════════════════════════════════
    print_separator("TABLE 2: Orbital Velocities and Radii");
    
    std::printf("%-5s %2s  %10s  %8s  %8s  %10s\n",
        "Sym", "Z", "v(km/s)", "v/c", "v/(αc)", "r(pm)");
    for (int i = 0; i < 60; ++i) std::printf("-");
    std::printf("\n");
    
    for (auto& r : results) {
        if (!r.is_most_abundant) continue;  // show most abundant only for clarity
        std::printf("%-5s %2d  %10.2f  %8.6f  %8.6f  %10.3f\n",
            r.symbol, r.Z,
            r.v_orbital / 1000.0,
            r.v_orbital / constants::c,
            r.v_over_alpha_c,
            r.r_orbital * 1e12);
    }
    
    // ═══════════════════════════════════════════════════════════
    // TABLE 3: Screening analysis
    // ═══════════════════════════════════════════════════════════
    print_separator("TABLE 3: Screening — Z_eff, S, η = S/(Z-1)");
    
    std::printf("%-5s %2s  %8s  %8s  %4s  %8s  %8s\n",
        "Sym", "Z", "Z_eff", "S", "Z-1", "η", "Δη");
    for (int i = 0; i < 60; ++i) std::printf("-");
    std::printf("\n");
    
    for (auto& r : results) {
        if (!r.is_most_abundant) continue;
        double delta_eta = (r.Z > 1) ? (r.eta - 1.0) : 0.0;
        std::printf("%-5s %2d  %8.6f  %8.4f  %4d  %8.6f  %+8.4f\n",
            r.symbol, r.Z, r.Z_eff, r.screening,
            r.Z - 1, r.eta, delta_eta);
    }
    
    // Find where η is closest to 1.000
    double best_eta_dev = 1e10;
    const char* best_eta_sym = "";
    int best_eta_Z = 0;
    for (auto& r : results) {
        if (!r.is_most_abundant || r.Z <= 1) continue;
        double dev = std::abs(r.eta - 1.0);
        if (dev < best_eta_dev) {
            best_eta_dev = dev;
            best_eta_sym = r.symbol;
            best_eta_Z = r.Z;
        }
    }
    std::printf("\nBest screening efficiency: %s (Z=%d), η = 1 ± %.6f\n",
        best_eta_sym, best_eta_Z, best_eta_dev);
    
    // ═══════════════════════════════════════════════════════════
    // TABLE 4: N=240 Harmonic test — ALL elements, not just the good ones
    // ═══════════════════════════════════════════════════════════
    print_separator("TABLE 4: N=240 Harmonic — v/(αc) = n/240?");
    
    std::printf("%-5s %2s  %10s  %5s  %10s  %10s  %6s\n",
        "Sym", "Z", "v/(αc)", "n240", "n/240", "deviation", "PASS?");
    for (int i = 0; i < 70; ++i) std::printf("-");
    std::printf("\n");
    
    int n240_pass = 0, n240_fail = 0;
    double threshold_240 = 0.02;  // 2% tolerance
    
    for (auto& r : results) {
        if (!r.is_most_abundant) continue;
        bool pass = std::abs(r.n_240_deviation) < threshold_240;
        if (pass) n240_pass++; else n240_fail++;
        
        std::printf("%-5s %2d  %10.6f  %5d  %10.6f  %+10.4f%%  %s\n",
            r.symbol, r.Z, r.v_over_alpha_c,
            r.n_240, static_cast<double>(r.n_240) / 240.0,
            r.n_240_deviation * 100.0,
            pass ? "PASS" : "FAIL");
    }
    std::printf("\nN=240 harmonic (2%% tolerance): %d PASS, %d FAIL out of %d\n",
        n240_pass, n240_fail, n240_pass + n240_fail);
    
    // ═══════════════════════════════════════════════════════════
    // TABLE 5: Rational fraction test — v/(αc) near p/q?
    // ═══════════════════════════════════════════════════════════
    print_separator("TABLE 5: Rational Fraction Test — v/(αc) ≈ p/q?");
    
    std::printf("%-5s %2s  %10s  %6s  %10s  %10s\n",
        "Sym", "Z", "v/(αc)", "p/q", "value", "error%");
    for (int i = 0; i < 60; ++i) std::printf("-");
    std::printf("\n");
    
    // Test all fractions p/q with q ≤ 12
    for (auto& r : results) {
        if (!r.is_most_abundant) continue;
        
        double val = r.v_over_alpha_c;
        double best_err = 1e10;
        int best_p = 0, best_q = 1;
        
        for (int q = 1; q <= 12; ++q) {
            for (int p = 1; p <= 12 * q; ++p) {
                double frac = static_cast<double>(p) / static_cast<double>(q);
                double err = std::abs(val - frac) / val;
                if (err < best_err) {
                    best_err = err;
                    best_p = p;
                    best_q = q;
                }
            }
        }
        
        // Simplify fraction
        int g = std::gcd(best_p, best_q);
        best_p /= g;
        best_q /= g;
        
        char frac_str[16];
        std::snprintf(frac_str, sizeof(frac_str), "%d/%d", best_p, best_q);
        
        std::printf("%-5s %2d  %10.6f  %6s  %10.6f  %+10.4f%%\n",
            r.symbol, r.Z, val, frac_str,
            static_cast<double>(best_p) / static_cast<double>(best_q),
            best_err * 100.0);
    }
    
    // ═══════════════════════════════════════════════════════════
    // TABLE 6: Nuclear pairing — BE/A by parity class
    // ═══════════════════════════════════════════════════════════
    print_separator("TABLE 6: Nuclear Pairing — BE/A by (Z,N) parity");
    
    double sum_ee = 0, cnt_ee = 0;
    double sum_eo = 0, cnt_eo = 0;
    double sum_oe = 0, cnt_oe = 0;
    double sum_oo = 0, cnt_oo = 0;
    
    for (auto& iso : isotopes) {
        if (iso.BE_per_A_MeV < 0.01) continue;  // skip H-1 (no binding)
        int N = iso.A - iso.Z;
        bool Z_even = (iso.Z % 2 == 0);
        bool N_even = (N % 2 == 0);
        
        if (Z_even && N_even)       { sum_ee += iso.BE_per_A_MeV; cnt_ee++; }
        else if (Z_even && !N_even) { sum_eo += iso.BE_per_A_MeV; cnt_eo++; }
        else if (!Z_even && N_even) { sum_oe += iso.BE_per_A_MeV; cnt_oe++; }
        else                        { sum_oo += iso.BE_per_A_MeV; cnt_oo++; }
    }
    
    std::printf("Parity  Count  <BE/A>(MeV)  Ratio to OO\n");
    for (int i = 0; i < 50; ++i) std::printf("-");
    std::printf("\n");
    
    double avg_oo = (cnt_oo > 0) ? sum_oo / cnt_oo : 0;
    auto print_parity = [&](const char* label, double sum, double cnt) {
        double avg = (cnt > 0) ? sum / cnt : 0;
        double ratio = (avg_oo > 0) ? avg / avg_oo : 0;
        std::printf("%-7s  %4.0f     %8.3f      %6.3f\n", label, cnt, avg, ratio);
    };
    
    print_parity("EE", sum_ee, cnt_ee);
    print_parity("EO", sum_eo, cnt_eo);
    print_parity("OE", sum_oe, cnt_oe);
    print_parity("OO", sum_oo, cnt_oo);
    
    double ratio_ee_oo = (cnt_oo > 0 && cnt_ee > 0) ?
        (sum_ee / cnt_ee) / (sum_oo / cnt_oo) : 0;
    std::printf("\nEE/OO ratio: %.4f  (claim: 3/2 = 1.5000, deviation: %+.2f%%)\n",
        ratio_ee_oo, (ratio_ee_oo - 1.5) / 1.5 * 100.0);
    
    // ═══════════════════════════════════════════════════════════
    // TABLE 7: Z_eff prime avoidance
    // ═══════════════════════════════════════════════════════════
    print_separator("TABLE 7: Z_eff vs Prime Numbers");
    
    std::printf("%-5s %2s  %8s  %4s  %6s\n",
        "Sym", "Z", "Z_eff", "⌊Z⌉", "Prime?");
    for (int i = 0; i < 40; ++i) std::printf("-");
    std::printf("\n");
    
    int prime_count = 0, total_count = 0;
    for (auto& r : results) {
        if (!r.is_most_abundant) continue;
        total_count++;
        if (r.Z_eff_near_prime) prime_count++;
        
        std::printf("%-5s %2d  %8.4f  %4d  %s\n",
            r.symbol, r.Z, r.Z_eff, r.Z_eff_rounded,
            r.Z_eff_near_prime ? "YES !" : "no");
    }
    
    // Expected primes below max Z_eff
    double max_zeff = 0;
    for (auto& r : results) if (r.is_most_abundant && r.Z_eff > max_zeff) max_zeff = r.Z_eff;
    int primes_below = 0;
    for (int i = 2; i <= static_cast<int>(max_zeff) + 1; ++i) if (is_prime(i)) primes_below++;
    double expected_frac = static_cast<double>(primes_below) / (static_cast<double>(static_cast<int>(max_zeff)) + 1);
    
    std::printf("\nZ_eff rounds to prime: %d out of %d (%.1f%%)\n",
        prime_count, total_count, 100.0 * prime_count / total_count);
    std::printf("Expected from prime density: %.1f%%\n", expected_frac * 100.0);
    
    // ═══════════════════════════════════════════════════════════
    // TABLE 8: Ionisation energy progression (I1 vs Z)
    // ═══════════════════════════════════════════════════════════
    print_separator("TABLE 8: Ionisation Energy Structure");
    
    std::printf("%-5s %2s  %8s  %8s  %8s  %8s  %6s\n",
        "Sym", "Z", "I1(eV)", "I1/Ry", "Z_eff²/n²", "Ry*Z²/n²", "SDT/QM");
    for (int i = 0; i < 70; ++i) std::printf("-");
    std::printf("\n");
    
    for (auto& r : results) {
        if (!r.is_most_abundant) continue;
        double n = static_cast<double>(r.n_valence);
        double I1_ratio = r.I1_eV / constants::Ry_eV;  // I1/Ry
        double zeff2_n2 = (r.Z_eff * r.Z_eff) / (n * n);
        double bare_pred = constants::Ry_eV * static_cast<double>(r.Z * r.Z) / (n * n);
        double sdt_qm = r.I1_eV / bare_pred;
        
        std::printf("%-5s %2d  %8.4f  %8.6f  %8.6f  %8.2f  %6.4f\n",
            r.symbol, r.Z, r.I1_eV, I1_ratio, zeff2_n2, bare_pred, sdt_qm);
    }
    
    // ═══════════════════════════════════════════════════════════
    // TABLE 9: Isotope shift — same Z, different A
    // ═══════════════════════════════════════════════════════════
    print_separator("TABLE 9: Isotope Shifts (same Z, different A)");
    
    std::printf("%-6s %-6s  %5s  %5s  %10s  %10s  %10s\n",
        "Iso1", "Iso2", "A1", "A2", "I1_1(eV)", "I1_2(eV)", "ΔI1/I1");
    for (int i = 0; i < 70; ++i) std::printf("-");
    std::printf("\n");
    
    for (size_t i = 0; i < results.size(); ++i) {
        for (size_t j = i + 1; j < results.size(); ++j) {
            if (results[i].Z == results[j].Z && results[i].A != results[j].A) {
                double dI = results[j].I1_eV - results[i].I1_eV;
                double ratio = dI / results[i].I1_eV;
                std::printf("%-6s %-6s  %5d  %5d  %10.4f  %10.4f  %+10.6f\n",
                    results[i].symbol, results[j].symbol,
                    results[i].A, results[j].A,
                    results[i].I1_eV, results[j].I1_eV, ratio);
                break;  // just first pair per element
            }
        }
    }
    
    // ═══════════════════════════════════════════════════════════
    // TABLE 10: Composite structure analysis
    // ═══════════════════════════════════════════════════════════
    print_separator("TABLE 10: Nuclear Composite Decomposition");
    
    std::printf("%-5s %2s %2s %2s  %4s  %7s  %7s  %7s  %7s\n",
        "Sym", "Z", "N", "A", "EE?", "α(max)", "α-tri", "tri", "deu");
    for (int i = 0; i < 65; ++i) std::printf("-");
    std::printf("\n");
    
    for (auto& iso : isotopes) {
        if (!iso.is_most_abundant) continue;
        int N = iso.A - iso.Z;
        bool ee = (iso.Z % 2 == 0) && (N % 2 == 0);
        
        // Greedy decomposition: max alphas first, then alpha-tris, triterons, deuterons
        int z_rem = iso.Z;
        int n_rem = N;
        int n_alpha = 0, n_alphatri = 0, n_tri = 0, n_deu = 0;
        
        // Alpha: 2p + 2n
        n_alpha = std::min(z_rem / 2, n_rem / 2);
        z_rem -= n_alpha * 2;
        n_rem -= n_alpha * 2;
        
        // Triteron: 1p + 2n
        if (n_rem >= 2 && z_rem >= 1) {
            n_tri = std::min(z_rem, n_rem / 2);
            z_rem -= n_tri;
            n_rem -= n_tri * 2;
        }
        
        // Deuteron: 1p + 1n
        if (n_rem >= 1 && z_rem >= 1) {
            n_deu = std::min(z_rem, n_rem);
            z_rem -= n_deu;
            n_rem -= n_deu;
        }
        
        // Alpha-tri count (estimate from original alphas broken)
        // Actually let's try the alpha-tri path too
        int z2 = iso.Z, n2 = N;
        int a_alphatri = 0;
        while (z2 >= 2 && n2 >= 3) { a_alphatri++; z2 -= 2; n2 -= 3; }
        
        std::printf("%-5s %2d %2d %2d  %4s  %3dα     %3dαt    %3dt    %3dd",
            iso.symbol, iso.Z, N, iso.A,
            ee ? "EE" : (iso.Z % 2 == 0 ? "EO" : (N % 2 == 0 ? "OE" : "OO")),
            n_alpha, a_alphatri, n_tri, n_deu);
        
        if (z_rem > 0 || n_rem > 0)
            std::printf("  +%dp+%dn RESIDUAL", z_rem, n_rem);
        std::printf("\n");
    }
    
    // ═══════════════════════════════════════════════════════════
    // SUMMARY: Honest Assessment
    // ═══════════════════════════════════════════════════════════
    print_separator("HONEST SUMMARY");
    
    // Count various metrics
    int n_tested = 0;
    int zk2_exact = 0;
    int velocity_rational_1pct = 0;
    int velocity_rational_5pct = 0;
    int eta_within_10pct = 0;
    int eta_within_5pct = 0;
    
    for (auto& r : results) {
        if (!r.is_most_abundant) continue;
        n_tested++;
        
        if (std::abs(r.zk2 - 1.0) < 1e-10) zk2_exact++;
        
        // Check if v/(αc) is within 1% of any p/q with q≤6
        bool found_1pct = false, found_5pct = false;
        for (int q = 1; q <= 6 && !found_1pct; ++q) {
            for (int p = 1; p <= 6 * q; ++p) {
                double frac = static_cast<double>(p) / static_cast<double>(q);
                double err = std::abs(r.v_over_alpha_c - frac) / r.v_over_alpha_c;
                if (err < 0.01) found_1pct = true;
                if (err < 0.05) found_5pct = true;
            }
        }
        if (found_1pct) velocity_rational_1pct++;
        if (found_5pct) velocity_rational_5pct++;
        
        if (r.Z > 1 && std::abs(r.eta - 1.0) < 0.10) eta_within_10pct++;
        if (r.Z > 1 && std::abs(r.eta - 1.0) < 0.05) eta_within_5pct++;
    }
    
    std::printf("Elements tested (most abundant isotopes): %d\n\n", n_tested);
    
    std::printf("CLAIM 1: z·k² = 1 (exact)\n");
    std::printf("  Result: %d/%d = %.1f%% exact (to machine precision)\n",
        zk2_exact, n_tested, 100.0 * zk2_exact / n_tested);
    std::printf("  VERDICT: %s\n\n",
        zk2_exact == n_tested ? "CONFIRMED — tautological (z = 1/k² by definition from I1)" :
        "PARTIAL");
    
    std::printf("CLAIM 2: v/(αc) quantises as rational fractions (p/q, q≤6)\n");
    std::printf("  Within 1%%: %d/%d = %.1f%%\n",
        velocity_rational_1pct, n_tested, 100.0 * velocity_rational_1pct / n_tested);
    std::printf("  Within 5%%: %d/%d = %.1f%%\n",
        velocity_rational_5pct, n_tested, 100.0 * velocity_rational_5pct / n_tested);
    std::printf("  VERDICT: %s\n\n",
        velocity_rational_1pct > n_tested * 0.8 ? "STRONG SUPPORT" :
        velocity_rational_1pct > n_tested * 0.5 ? "MODERATE SUPPORT" : "WEAK — may be numerology");
    
    std::printf("CLAIM 3: Screening efficiency η → 1 at Z=8 (oxygen)\n");
    std::printf("  Within 10%% of η=1: %d/%d elements\n", eta_within_10pct, n_tested - 1);
    std::printf("  Within  5%% of η=1: %d/%d elements\n", eta_within_5pct, n_tested - 1);
    std::printf("  Best: %s (Z=%d)\n", best_eta_sym, best_eta_Z);
    std::printf("  VERDICT: η trends toward 1 but NOT unique to oxygen — check Si, S, Cl, Ar\n\n");
    
    std::printf("CLAIM 4: Nuclear pairing BE ratio = 3/2\n");
    std::printf("  EE/OO = %.4f  (3/2 = 1.5000)\n", ratio_ee_oo);
    std::printf("  Deviation: %+.2f%%\n", (ratio_ee_oo - 1.5) / 1.5 * 100.0);
    std::printf("  VERDICT: %s\n\n",
        std::abs(ratio_ee_oo - 1.5) < 0.1 ? "CLOSE but includes high-A bias" :
        "NOT exact 3/2 — depends on sample range");
    
    std::printf("CLAIM 5: Z_eff avoids primes\n");
    std::printf("  Primes hit: %d/%d = %.1f%%\n",
        prime_count, total_count, 100.0 * prime_count / total_count);
    std::printf("  Expected: %.1f%%\n", expected_frac * 100.0);
    std::printf("  VERDICT: %s\n\n",
        prime_count < total_count * expected_frac * 0.5 ? "SIGNIFICANT avoidance" :
        "INCONCLUSIVE — small sample + Z_eff clusters near 1");
    
    std::printf("CRITICAL NOTE: z·k² = 1 is a TAUTOLOGY when Z_eff is DEFINED as\n");
    std::printf("  Z_eff = n·√(I1/Ry), and k = n/(α·Z_eff), and z = 1/k².\n");
    std::printf("  The constraint holds by construction, not by discovery.\n");
    std::printf("  The REAL test is whether the Z_eff values, velocities, and radii\n");
    std::printf("  derived this way match INDEPENDENT measurements.\n");
    
    return 0;
}
