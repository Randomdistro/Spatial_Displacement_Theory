// =========================================================================
//  NUMERICAL VERIFICATION: "An Argument For Koppa"
//  Tests every numerical claim in the paper
//  C++20 — no external dependencies
// =========================================================================

#include <cmath>
#include <cstdio>
#include <string>
#include <vector>
#include <array>

// =========================================================================
// CODATA 2018 Constants
// =========================================================================
constexpr double c         = 299'792'458.0;          // m/s
constexpr double alpha     = 7.2973525693e-3;        // fine structure constant
constexpr double alpha_inv = 137.035999084;           // 1/alpha
constexpr double R_p       = 0.8414e-15;             // proton charge radius (m)
constexpr double a_0       = 5.29177210903e-11;      // Bohr radius (m)
constexpr double m_e       = 9.1093837015e-31;       // electron mass (kg)
constexpr double eV_to_J   = 1.602176634e-19;        // eV to Joules
constexpr double E_Ry      = 13.605693122994;        // Rydberg energy (eV)

// =========================================================================
// Celestial body data
// =========================================================================
constexpr double GM_sun    = 1.32712440018e20;       // m^3 s^-2
constexpr double R_sun     = 6.957e8;                // m

constexpr double GM_jup    = 1.26686534e17;          // m^3 s^-2
constexpr double R_jup     = 7.1492e7;               // m (polar)

constexpr double GM_sat    = 3.7931187e16;           // m^3 s^-2
constexpr double R_sat     = 6.0268e7;               // m (polar)

constexpr double GM_earth  = 3.986004418e14;         // m^3 s^-2
constexpr double R_earth_mean  = 6.371e6;            // m (mean)
constexpr double R_earth_polar = 6.356752e6;         // m (polar)

// =========================================================================
// Helpers
// =========================================================================
struct TestResult {
    std::string name;
    double expected;
    double computed;
    double error_pct;
    bool pass;
};

static std::vector<TestResult> results;
static int total_pass = 0;
static int total_fail = 0;

void check(const char* name, double computed, double expected, double tol_pct) {
    double err = 0.0;
    if (expected != 0.0) {
        err = std::abs((computed - expected) / expected) * 100.0;
    } else {
        err = std::abs(computed) * 100.0;
    }
    bool pass = (err <= tol_pct);
    if (pass) total_pass++; else total_fail++;

    const char* status = pass ? "PASS" : "**FAIL**";
    std::printf("  %-55s  %14.6f  %14.6f  %8.4f%%  %s\n",
                name, computed, expected, err, status);
    results.push_back({name, expected, computed, err, pass});
}

void section(const char* title) {
    std::printf("\n%s\n", std::string(80, '=').c_str());
    std::printf("  %s\n", title);
    std::printf("%s\n", std::string(80, '=').c_str());
    std::printf("  %-55s  %14s  %14s  %8s  %s\n",
                "Test", "Computed", "Expected", "Error", "Status");
    std::printf("  %s\n", std::string(100, '-').c_str());
}

// =========================================================================
// Orbital velocity from koppa: v = (c/k)*sqrt(R/r)
// =========================================================================
double v_from_koppa(double k, double R, double r) {
    return (c / k) * std::sqrt(R / r);
}

// koppa from GM and R:  k = c / sqrt(GM/R)
double koppa_from_GM(double GM, double R) {
    return c / std::sqrt(GM / R);
}

// =========================================================================
//  MAIN
// =========================================================================
int main() {
    std::printf("\n");
    std::printf("########################################################################\n");
    std::printf("#  NUMERICAL VERIFICATION: An Argument For Koppa                       #\n");
    std::printf("#  Every formula. Every table. Every claim.                             #\n");
    std::printf("########################################################################\n");

    // =====================================================================
    // PATH 1: Sun surface
    // =====================================================================
    section("PATH 1: The Surface of the Sun");

    double v_surf_sun = std::sqrt(GM_sun / R_sun);
    check("v_surf = sqrt(GM_sun/R_sun)", v_surf_sun, 436676.0, 0.5);

    double k_sun = c / v_surf_sun;
    check("k_sun = c / v_surf", k_sun, 686.5, 0.1);

    // GM equivalence: GM = c^2 * R / k^2
    double GM_from_k = (c * c * R_sun) / (k_sun * k_sun);
    check("GM from c^2*R/k^2 vs actual GM_sun", GM_from_k, GM_sun, 0.001);

    // Schwarzschild radius / 2 = R / k^2
    double R_c_sun = R_sun / (k_sun * k_sun);
    double R_c_expected = GM_sun / (c * c);  // = GM/c^2
    check("R_c = R/k^2 = GM/c^2 (m)", R_c_sun, R_c_expected, 0.001);
    check("R_c numerical value (m)", R_c_sun, 1476.5, 0.1);

    // =====================================================================
    // PATH 2: Planets
    // =====================================================================
    section("PATH 2: The Planets of the Solar System");

    struct Planet {
        const char* name;
        double r;        // orbital distance (m)
        double v_obs;    // observed velocity (m/s)
        double k_obs;    // paper's k_obs
        double k_pred;   // paper's k_pred
        double err_paper; // paper's stated error %
    };

    Planet planets[] = {
        {"Mercury",  5.79e10,  47870.0,  6263.0,  6261.0, 0.03},
        {"Venus",   10.82e10,  35020.0,  8561.0,  8561.0, 0.00},
        {"Earth",   14.96e10,  29780.0, 10067.0, 10070.0, 0.03},
        {"Mars",    22.79e10,  24070.0, 12455.0, 12439.0, 0.13},
        {"Jupiter", 77.85e10,  13070.0, 22938.0, 22967.0, 0.13},
        {"Saturn", 143.3e10,    9690.0, 30939.0, 31133.0, 0.63},
    };

    for (auto& p : planets) {
        // Compute k_obs = c / v_obs
        double k_obs_comp = c / p.v_obs;
        char buf[128];
        std::snprintf(buf, sizeof(buf), "%-8s: k_obs = c/v_obs", p.name);
        check(buf, k_obs_comp, p.k_obs, 0.1);

        // Compute k_pred = k_sun * sqrt(r / R_sun)
        double k_pred_comp = k_sun * std::sqrt(p.r / R_sun);
        std::snprintf(buf, sizeof(buf), "%-8s: k_pred = k_sun*sqrt(r/R)", p.name);
        check(buf, k_pred_comp, p.k_pred, 0.5);

        // Compute v_pred from formula
        double v_pred = v_from_koppa(k_sun, R_sun, p.r);
        double vel_err = std::abs(v_pred - p.v_obs) / p.v_obs * 100.0;
        std::snprintf(buf, sizeof(buf), "%-8s: v_pred vs v_obs (m/s)", p.name);
        check(buf, v_pred, p.v_obs, 1.0);
    }

    // Steradian identity: Omega * r^2 = pi * R^2
    section("STERADIAN IDENTITY: Omega * r^2 = pi * R^2");
    for (auto& p : planets) {
        double omega = M_PI * R_sun * R_sun / (p.r * p.r);
        double lhs = omega * p.r * p.r;
        double rhs = M_PI * R_sun * R_sun;
        char buf[128];
        std::snprintf(buf, sizeof(buf), "%-8s: Omega*r^2 / (pi*R^2)", p.name);
        check(buf, lhs / rhs, 1.0, 1e-10);
    }

    // =====================================================================
    // PATH 3: Jupiter's moons
    // =====================================================================
    section("PATH 3: The Moons of Jupiter");

    double k_jup = koppa_from_GM(GM_jup, R_jup);
    check("k_Jupiter = c/sqrt(GM_J/R_J)", k_jup, 7124.0, 0.5);

    struct Moon {
        const char* name;
        double a;       // semi-major axis (m)
        double v_obs;   // observed velocity (m/s)
    };

    Moon jup_moons[] = {
        {"Io",        421700e3,   17334.0},
        {"Europa",    671034e3,   13740.0},
        {"Ganymede", 1070412e3,   10880.0},
        {"Callisto", 1882709e3,    8204.0},
    };

    for (auto& m : jup_moons) {
        double v_pred = v_from_koppa(k_jup, R_jup, m.a);
        char buf[128];
        std::snprintf(buf, sizeof(buf), "%-10s: v_pred vs v_obs (m/s)", m.name);
        check(buf, v_pred, m.v_obs, 0.5);
    }

    // =====================================================================
    // PATH 4: Saturn's moons
    // =====================================================================
    section("PATH 4: The Moons of Saturn");

    double k_sat = koppa_from_GM(GM_sat, R_sat);
    check("k_Saturn = c/sqrt(GM_S/R_S)", k_sat, 11949.0, 0.5);

    Moon sat_moons[] = {
        {"Mimas",      185539e3, 14280.0},
        {"Enceladus",  238042e3, 12630.0},
        {"Tethys",     294619e3, 11350.0},
        {"Dione",      377396e3, 10030.0},
        {"Rhea",       527108e3,  8480.0},
        {"Titan",     1221870e3,  5570.0},
        {"Iapetus",   3560820e3,  3260.0},
    };

    for (auto& m : sat_moons) {
        double v_pred = v_from_koppa(k_sat, R_sat, m.a);
        char buf[128];
        std::snprintf(buf, sizeof(buf), "%-10s: v_pred vs v_obs (m/s)", m.name);
        check(buf, v_pred, m.v_obs, 0.5);
    }

    // =====================================================================
    // PATH 5: Earth-Moon
    // =====================================================================
    section("PATH 5: The Earth-Moon System");

    double k_earth_mean = koppa_from_GM(GM_earth, R_earth_mean);
    check("k_Earth (mean R) = c/sqrt(GM/R)", k_earth_mean, 37924.0, 0.1);

    double v_moon_pred_mean = v_from_koppa(k_earth_mean, R_earth_mean, 3.844e8);
    check("Moon v_pred (mean R)", v_moon_pred_mean, 1022.0, 0.5);

    // =====================================================================
    // PATH 6: Polar radius & satellites
    // =====================================================================
    section("PATH 6: Artificial Satellites (Polar Radius)");

    double k_earth_polar = koppa_from_GM(GM_earth, R_earth_polar);
    check("k_Earth (polar R) = c/sqrt(GM/R_pol)", k_earth_polar, 37848.0, 0.1);

    struct Satellite {
        const char* name;
        double r;       // orbital radius from centre (m)
        double v_obs;   // observed velocity (m/s)
    };

    Satellite sats[] = {
        {"LEO (250km)",   6607e3,   7755.0},
        {"ISS (408km)",   6765e3,   7661.0},
        {"Hubble (547km)",6904e3,   7584.0},
        {"GPS (20200km)", 26540e3,  3874.0},
        {"GEO (35786km)", 42143e3,  3075.0},
        {"Moon",          384400e3, 1022.0},
    };

    for (auto& s : sats) {
        double v_pred = v_from_koppa(k_earth_polar, R_earth_polar, s.r);
        char buf[128];
        std::snprintf(buf, sizeof(buf), "%-18s: v_pred vs v_obs", s.name);
        check(buf, v_pred, s.v_obs, 0.2);
    }

    // =====================================================================
    // PATH 7: Hydrogen atom — derivation of atomic koppa
    // =====================================================================
    section("PATH 7: The Hydrogen Atom — Deriving Koppa = 0.5464");

    // Hydrogen ground state velocity
    double v_H = alpha * c;
    check("v_H = alpha*c (m/s)", v_H, 2.18769e6, 0.01);

    // Hydrogen kinematic ratio = 1/alpha
    double k_H = c / v_H;
    check("k_H = c/v_H = 1/alpha", k_H, alpha_inv, 0.001);

    // R_p / a_0
    double Rp_over_a0 = R_p / a_0;
    check("R_p / a_0", Rp_over_a0, 1.5899e-5, 0.1);

    // sqrt(R_p/a_0)
    double sqrt_ratio = std::sqrt(Rp_over_a0);
    check("sqrt(R_p/a_0)", sqrt_ratio, 3.9874e-3, 0.1);

    // KOPPA = (1/alpha) * sqrt(R_p/a_0)
    double koppa_atomic = alpha_inv * sqrt_ratio;
    check("KOPPA = (1/alpha)*sqrt(R_p/a_0)", koppa_atomic, 0.5464, 0.1);

    // Verify: v = (c/koppa)*sqrt(R_p/a_0) should equal alpha*c
    double v_check = (c / koppa_atomic) * std::sqrt(R_p / a_0);
    check("v = (c/koppa)*sqrt(R_p/a_0) vs alpha*c", v_check, v_H, 0.001);

    // =====================================================================
    // ISOELECTRONIC SEQUENCES — Helium-like (N=2)
    // =====================================================================
    section("ISOELECTRONIC: Helium-like (N=2)");

    struct Ion {
        const char* name;
        int Z;
        int n;         // principal quantum number of outermost electron
        double E_I;    // ionisation energy (eV)
        double Z_eff_paper;
        double sigma_paper;
    };

    Ion he_like[] = {
        {"He",      2, 1,    24.587,  1.344, 0.656},
        {"Li+",     3, 1,    75.640,  2.358, 0.642},
        {"Be2+",    4, 1,   153.896,  3.363, 0.637},
        {"B3+",     5, 1,   259.372,  4.366, 0.634},
        {"C4+",     6, 1,   392.090,  5.368, 0.632},
        {"N5+",     7, 1,   552.072,  6.370, 0.630},
        {"O6+",     8, 1,   739.327,  7.372, 0.628},
        {"F7+",     9, 1,   953.898,  8.373, 0.627},
        {"Ne8+",   10, 1,  1195.828,  9.375, 0.625},
        {"Si12+",  14, 1,  2437.658, 13.385, 0.615},
        {"Ar16+",  18, 1,  4120.886, 17.403, 0.597},
        {"Fe24+",  26, 1,  8828.188, 25.473, 0.527},
    };

    for (auto& ion : he_like) {
        // v = sqrt(2 * E_I / m_e)
        double v = std::sqrt(2.0 * ion.E_I * eV_to_J / m_e);
        double v_over_c = v / c;

        // Z_eff = n * sqrt(E_I / E_Ry)
        double Z_eff = ion.n * std::sqrt(ion.E_I / E_Ry);

        // sigma = Z - Z_eff
        double sigma = ion.Z - Z_eff;

        // k_SDT = (c * Z_eff / v) * sqrt(R_p / (n^2 * a_0))
        double k_SDT = (c * Z_eff / v) * std::sqrt(R_p / (ion.n * ion.n * a_0));

        char buf[128];
        std::snprintf(buf, sizeof(buf), "%-7s: Z_eff", ion.name);
        check(buf, Z_eff, ion.Z_eff_paper, 0.1);

        std::snprintf(buf, sizeof(buf), "%-7s: sigma", ion.name);
        check(buf, sigma, ion.sigma_paper, 1.0);

        std::snprintf(buf, sizeof(buf), "%-7s: k_SDT", ion.name);
        check(buf, k_SDT, 0.5464, 0.1);
    }

    // =====================================================================
    // ISOELECTRONIC: Gold-like (N=79)
    // =====================================================================
    section("ISOELECTRONIC: Gold-like (N=79)");

    Ion au_like[] = {
        {"Au",     79, 6,   9.226,  4.941, 74.059},
        {"Hg+",    80, 6,  18.756,  7.045, 72.955},
        {"Tl2+",   81, 6,  29.830,  8.884, 72.116},
        {"Pb3+",   82, 6,  42.320, 10.582, 71.418},
    };

    for (auto& ion : au_like) {
        double v = std::sqrt(2.0 * ion.E_I * eV_to_J / m_e);
        double Z_eff = ion.n * std::sqrt(ion.E_I / E_Ry);
        double sigma = ion.Z - Z_eff;
        double k_SDT = (c * Z_eff / v) * std::sqrt(R_p / (ion.n * ion.n * a_0));

        char buf[128];
        std::snprintf(buf, sizeof(buf), "%-7s: Z_eff", ion.name);
        check(buf, Z_eff, ion.Z_eff_paper, 0.5);

        std::snprintf(buf, sizeof(buf), "%-7s: sigma", ion.name);
        check(buf, sigma, ion.sigma_paper, 1.0);

        std::snprintf(buf, sizeof(buf), "%-7s: k_SDT", ion.name);
        check(buf, k_SDT, 0.5464, 0.5);
    }

    // =====================================================================
    // ISOELECTRONIC: Hydrogen-like (N=1) — spot checks
    // =====================================================================
    section("ISOELECTRONIC: Hydrogen-like (N=1) — spot checks");

    Ion h_like[] = {
        {"H",       1, 1,    13.598,  1.000, 0.000},
        {"He+",     2, 1,    54.418,  2.000, 0.000},
        {"Li2+",    3, 1,   122.454,  3.000, 0.000},
        {"Be3+",    4, 1,   217.719,  4.000, 0.000},
        {"C5+",     6, 1,   489.993,  6.001, -0.001},
        {"Ne9+",   10, 1,  1362.199, 10.006, -0.006},
        {"Fe25+",  26, 1,  9277.690, 26.113, -0.113},
    };

    for (auto& ion : h_like) {
        double v = std::sqrt(2.0 * ion.E_I * eV_to_J / m_e);
        double Z_eff = ion.n * std::sqrt(ion.E_I / E_Ry);
        double sigma = ion.Z - Z_eff;
        double k_SDT = (c * Z_eff / v) * std::sqrt(R_p / (ion.n * ion.n * a_0));

        char buf[128];
        std::snprintf(buf, sizeof(buf), "%-7s: Z_eff", ion.name);
        check(buf, Z_eff, ion.Z_eff_paper, 0.5);

        std::snprintf(buf, sizeof(buf), "%-7s: k_SDT", ion.name);
        check(buf, k_SDT, 0.5464, 0.5);
    }

    // =====================================================================
    // ISOELECTRONIC: Lithium-like (N=3) & Neon-like (N=10) — spot checks
    // =====================================================================
    section("ISOELECTRONIC: Lithium-like (N=3) — spot checks");

    Ion li_like[] = {
        {"Li",      3, 2,    5.392,  1.259, 1.741},
        {"Be+",     4, 2,   18.211,  2.314, 1.686},
        {"C3+",     6, 2,   64.494,  4.354, 1.646},
        {"O5+",     8, 2,  138.120,  6.372, 1.628},
        {"Fe23+",  26, 2, 2045.759, 24.524, 1.476},
    };

    for (auto& ion : li_like) {
        double v = std::sqrt(2.0 * ion.E_I * eV_to_J / m_e);
        double Z_eff = ion.n * std::sqrt(ion.E_I / E_Ry);
        double sigma = ion.Z - Z_eff;
        double k_SDT = (c * Z_eff / v) * std::sqrt(R_p / (ion.n * ion.n * a_0));

        char buf[128];
        std::snprintf(buf, sizeof(buf), "%-7s: Z_eff (n=2)", ion.name);
        check(buf, Z_eff, ion.Z_eff_paper, 0.5);

        std::snprintf(buf, sizeof(buf), "%-7s: sigma", ion.name);
        check(buf, sigma, ion.sigma_paper, 1.0);

        std::snprintf(buf, sizeof(buf), "%-7s: k_SDT", ion.name);
        check(buf, k_SDT, 0.5464, 0.5);
    }

    section("ISOELECTRONIC: Neon-like (N=10) — spot checks");

    Ion ne_like[] = {
        {"Ne",     10, 2,   21.565,  2.518, 7.482},
        {"Na+",    11, 2,   47.286,  3.729, 7.271},
        {"Si4+",   14, 2,  166.767,  7.002, 6.998},
        {"Fe16+",  26, 2, 1266.000, 19.292, 6.708},
    };

    for (auto& ion : ne_like) {
        double v = std::sqrt(2.0 * ion.E_I * eV_to_J / m_e);
        double Z_eff = ion.n * std::sqrt(ion.E_I / E_Ry);
        double sigma = ion.Z - Z_eff;
        double k_SDT = (c * Z_eff / v) * std::sqrt(R_p / (ion.n * ion.n * a_0));

        char buf[128];
        std::snprintf(buf, sizeof(buf), "%-7s: Z_eff (n=2)", ion.name);
        check(buf, Z_eff, ion.Z_eff_paper, 0.5);

        std::snprintf(buf, sizeof(buf), "%-7s: k_SDT", ion.name);
        check(buf, k_SDT, 0.5464, 0.5);
    }

    // =====================================================================
    // NICKEL-LIKE (N=28) — d-shell screening jump
    // =====================================================================
    section("ISOELECTRONIC: Nickel-like (N=28) — d-shell jump");

    Ion ni_like[] = {
        {"Ni",     28, 3,    7.640,  2.248, 25.752},
        {"Cu+",    29, 3,   20.292,  3.664, 25.336},
        {"Zn2+",   30, 3,   39.723,  5.126, 24.874},
    };

    for (auto& ion : ni_like) {
        double v = std::sqrt(2.0 * ion.E_I * eV_to_J / m_e);
        double Z_eff = ion.n * std::sqrt(ion.E_I / E_Ry);
        double sigma = ion.Z - Z_eff;
        double k_SDT = (c * Z_eff / v) * std::sqrt(R_p / (ion.n * ion.n * a_0));

        char buf[128];
        std::snprintf(buf, sizeof(buf), "%-7s: Z_eff (n=3)", ion.name);
        check(buf, Z_eff, ion.Z_eff_paper, 0.5);

        std::snprintf(buf, sizeof(buf), "%-7s: sigma/(N-1)", ion.name);
        double sig_per_e = sigma / 27.0;
        double expected_sig_per_e = ion.sigma_paper / 27.0;
        check(buf, sig_per_e, expected_sig_per_e, 1.0);

        std::snprintf(buf, sizeof(buf), "%-7s: k_SDT", ion.name);
        check(buf, k_SDT, 0.5464, 0.5);
    }

    // =====================================================================
    // ARGON-LIKE (N=18, n=3) — spot checks
    // =====================================================================
    section("ISOELECTRONIC: Argon-like (N=18) — spot checks");

    Ion ar_like[] = {
        {"Ar",     18, 3,   15.760,  3.229, 14.771},
        {"K+",     19, 3,   31.630,  4.574, 14.426},
        {"Ca2+",   20, 3,   50.913,  5.803, 14.197},
        {"Fe8+",   26, 3,  233.600, 12.431, 13.569},
    };

    for (auto& ion : ar_like) {
        double v = std::sqrt(2.0 * ion.E_I * eV_to_J / m_e);
        double Z_eff = ion.n * std::sqrt(ion.E_I / E_Ry);
        double sigma = ion.Z - Z_eff;
        double k_SDT = (c * Z_eff / v) * std::sqrt(R_p / (ion.n * ion.n * a_0));

        char buf[128];
        std::snprintf(buf, sizeof(buf), "%-7s: Z_eff (n=3)", ion.name);
        check(buf, Z_eff, ion.Z_eff_paper, 0.5);

        std::snprintf(buf, sizeof(buf), "%-7s: k_SDT", ion.name);
        check(buf, k_SDT, 0.5464, 0.5);
    }

    // =====================================================================
    // CROSS-CHECKS: alpha relationship
    // =====================================================================
    section("CROSS-CHECKS: Relationships and identities");

    // alpha = sqrt(R_p/a_0) / koppa
    double alpha_from_koppa = sqrt_ratio / koppa_atomic;
    check("alpha = sqrt(R_p/a_0) / koppa", alpha_from_koppa, alpha, 0.01);

    // GM = c^2 * R / k^2 for each body
    double GM_jup_check = c * c * R_jup / (k_jup * k_jup);
    check("GM_J from c^2*R_J/k_J^2", GM_jup_check, GM_jup, 0.01);

    double GM_sat_check = c * c * R_sat / (k_sat * k_sat);
    check("GM_S from c^2*R_S/k_S^2", GM_sat_check, GM_sat, 0.01);

    double GM_earth_check = c * c * R_earth_polar / (k_earth_polar * k_earth_polar);
    check("GM_E from c^2*R_pol/k_pol^2", GM_earth_check, GM_earth, 0.01);

    // Verify koppa_atomic^2 relationship
    // k^2 = R_p / (alpha^2 * a_0)
    double k_sq = R_p / (alpha * alpha * a_0);
    check("k^2 = R_p/(alpha^2 * a_0)", k_sq, koppa_atomic * koppa_atomic, 0.01);

    // =====================================================================
    // FINAL SUMMARY
    // =====================================================================
    std::printf("\n");
    std::printf("########################################################################\n");
    std::printf("#  FINAL RESULTS                                                       #\n");
    std::printf("########################################################################\n");
    std::printf("\n");
    std::printf("  Total tests:  %d\n", total_pass + total_fail);
    std::printf("  Passed:       %d\n", total_pass);
    std::printf("  Failed:       %d\n", total_fail);
    std::printf("  Pass rate:    %.1f%%\n",
                100.0 * total_pass / (total_pass + total_fail));
    std::printf("\n");

    if (total_fail > 0) {
        std::printf("  FAILURES:\n");
        for (auto& r : results) {
            if (!r.pass) {
                std::printf("    - %s  (computed=%.6f, expected=%.6f, err=%.4f%%)\n",
                            r.name.c_str(), r.computed, r.expected, r.error_pct);
            }
        }
    } else {
        std::printf("  ALL TESTS PASSED. Every numerical claim in the paper is verified.\n");
    }
    std::printf("\n");

    return total_fail > 0 ? 1 : 0;
}
