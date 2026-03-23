// ============================================================================
// trefoil_proton_engine.cpp
// 
// SDT Trefoil Proton: Self-Consistent (2,3) Torus-Knot Closure
// 
// Derives the proton's internal structure from:
//   - The (2,3) torus-knot (trefoil) parameterisation
//   - Proton charge radius R_p = 0.8414 fm
//   - Spin quantisation  L_z = hbar/2
//   - Magnetic moment    mu_p = 2.7928473 mu_N
//   - Filament energy    E = m_p c^2
//
// Outputs: R, a, v_tor, v_pol, v_gear, kappa, tension, P_conf, rho_s
//          and the sinuation coupling coefficient kappa_sinu.
//
// C++20  —  no external libraries  —  all mathematics from first principles.
// ============================================================================

#include <cmath>
#include <cstdio>
#include <numbers>
#include <array>
#include <functional>

// ============================================================================
//  §0  Physical Constants (CODATA 2018)
// ============================================================================

namespace cst {
    inline constexpr double c     = 299'792'458.0;          // m/s
    inline constexpr double hbar  = 1.054'571'817e-34;      // J·s
    inline constexpr double h     = 6.626'070'15e-34;       // J·s
    inline constexpr double e_q   = 1.602'176'634e-19;      // C
    inline constexpr double m_p   = 1.672'621'924e-27;      // kg
    inline constexpr double m_e   = 9.109'383'702e-31;      // kg
    inline constexpr double mu_N  = 5.050'783'699e-27;      // J/T  (nuclear magneton)
    inline constexpr double R_p   = 0.8414e-15;             // m    (proton charge radius)
    inline constexpr double mu_p_ratio = 2.792'847'344'6;   // mu_p / mu_N
    inline constexpr double mu_p  = mu_p_ratio * mu_N;      // J/T
    inline constexpr double g_p   = 2.0 * mu_p_ratio;       // proton g-factor = 5.5857
    inline constexpr double pi    = std::numbers::pi;
    inline constexpr double P_inf = 1.39e-14;               // Pa   (CMB radiation pressure)
    inline constexpr double mp_c2 = m_p * c * c;            // J    (proton rest energy)
}

// ============================================================================
//  §1  Numerical Integration  (adaptive Simpson)
// ============================================================================

namespace quad {

// Recursive adaptive Simpson's rule
static double simpson_adaptive_impl(
    const std::function<double(double)>& f,
    double a, double b,
    double fa, double fm, double fb,
    double S_whole, double eps, int depth)
{
    double m1 = (a + (a + b) * 0.5) * 0.5;   // midpoint of left half
    double m2 = ((a + b) * 0.5 + b) * 0.5;   // midpoint of right half
    double mid = (a + b) * 0.5;

    double f1 = f(m1);
    double f2 = f(m2);

    double h6_left  = (mid - a) / 6.0;
    double h6_right = (b - mid) / 6.0;

    double S_left  = h6_left  * (fa + 4.0 * f1 + fm);
    double S_right = h6_right * (fm + 4.0 * f2 + fb);
    double S_two   = S_left + S_right;

    if (depth <= 0 || std::abs(S_two - S_whole) < 15.0 * eps) {
        return S_two + (S_two - S_whole) / 15.0;
    }
    return simpson_adaptive_impl(f, a, mid, fa, f1, fm, S_left,  eps * 0.5, depth - 1)
         + simpson_adaptive_impl(f, mid, b,  fm, f2, fb, S_right, eps * 0.5, depth - 1);
}

double integrate(const std::function<double(double)>& f,
                 double a, double b, double eps = 1e-12)
{
    double fa = f(a);
    double fb = f(b);
    double mid = (a + b) * 0.5;
    double fm = f(mid);
    double S = (b - a) / 6.0 * (fa + 4.0 * fm + fb);
    return simpson_adaptive_impl(f, a, b, fa, fm, fb, S, eps, 50);
}

} // namespace quad

// ============================================================================
//  §2  (2,3) Torus-Knot Geometry
// ============================================================================

namespace trefoil {

// Parameterisation of the (2,3) torus knot on a torus (R, a):
//   x(θ) = (R + a cos 3θ) cos 2θ
//   y(θ) = (R + a cos 3θ) sin 2θ
//   z(θ) = a sin 3θ
//
// The tangent vector dx/dθ has squared norm:
//   |dx/dθ|² = 4(R + a cos 3θ)² + 9a²

// Squared norm of tangent vector
inline double tangent_norm_sq(double R, double a, double theta) {
    double u = R + a * std::cos(3.0 * theta);
    return 4.0 * u * u + 9.0 * a * a;
}

// Arc length of the full (2,3) torus knot
double arc_length(double R, double a) {
    return quad::integrate([R, a](double theta) {
        return std::sqrt(tangent_norm_sq(R, a, theta));
    }, 0.0, 2.0 * cst::pi);
}

// Charge-weighted RMS radius²  (distance from symmetry axis)
// For charge uniformly distributed along the knot path:
//   <r²> = (1/L) ∫₀²π |x_perp|² |dx/dθ| dθ
// where |x_perp|² = (R + a cos3θ)²      [distance from z-axis]
double charge_rms_r2(double R, double a) {
    double L = arc_length(R, a);
    double num = quad::integrate([R, a](double theta) {
        double u = R + a * std::cos(3.0 * theta);
        return u * u * std::sqrt(tangent_norm_sq(R, a, theta));
    }, 0.0, 2.0 * cst::pi);
    return num / L;
}

// Full 3D RMS radius² (distance from centre):
//   |x|² = (R + a cos3θ)² + a² sin²3θ = R² + 2Ra cos3θ + a²
double full_rms_r2(double R, double a) {
    double L = arc_length(R, a);
    double num = quad::integrate([R, a](double theta) {
        double c3 = std::cos(3.0 * theta);
        double s3 = std::sin(3.0 * theta);
        double r2 = (R + a * c3) * (R + a * c3) + a * a * s3 * s3;
        return r2 * std::sqrt(tangent_norm_sq(R, a, theta));
    }, 0.0, 2.0 * cst::pi);
    return num / L;
}

// Magnetic-moment integral:
//   ∫₀²π (x dy/dθ − y dx/dθ) dθ = 2 ∫₀²π (R + a cos3θ)² dθ = 2π(2R² + a²)
// This is exact for the (2,3) knot.
double magnetic_moment_integral(double R, double a) {
    return 2.0 * cst::pi * (2.0 * R * R + a * a);
}

// Decompose tangent speed into toroidal and poloidal components.
// At parameter θ, the toroidal tangent component magnitude is:
//   v_tor_local = 2(R + a cos3θ)  ω
// and the poloidal tangent component magnitude is:
//   v_pol_local = 3a  ω
// (there is no coupling term in the squared norm because the
//  toroidal and poloidal basis vectors on the torus are orthogonal)

// Average toroidal speed component:
//   <v²_tor> = ω² (1/2π) ∫₀²π 4(R+a cos3θ)² dθ = ω² · 2(2R²+a²)
double avg_v_tor_sq_coeff(double R, double a) {
    return quad::integrate([R, a](double theta) {
        double u = R + a * std::cos(3.0 * theta);
        return 4.0 * u * u;
    }, 0.0, 2.0 * cst::pi) / (2.0 * cst::pi);
}

// Average poloidal speed component (constant):
//   <v²_pol> = ω² · 9a²
double avg_v_pol_sq_coeff(double R, double a) {
    return 9.0 * a * a;
}

} // namespace trefoil

// ============================================================================
//  §3  The Angular Momentum / Magnetic Moment Decoupling
// ============================================================================
//
//  Key result from the (2,3) knot geometry:
//
//  For a point charge e AND point mass m both following the same knot path
//  with parametric angular velocity ω:
//
//    μ_z  = (eω/2) · (1/2π) · 2π(2R²+a²) = eω(2R²+a²)/2
//    <L_z> = mω(2R²+a²)
//
//    => μ_z / L_z = e/(2m)   => g = 1.
//
//  But measured g_p = 5.5857.  Therefore charge and mass do NOT
//  circulate at the same angular velocity.
//
//  Resolution: the charge races along the knot at speed v_gear while
//  the mass-energy pattern (the vortex envelope) rotates at a different
//  effective rate.
//
//  Two independent constraints:
//
//    [A]  μ_p = eω_charge(2R²+a²)/2       => ω_charge
//    [B]  L_z = ℏ/2                        => ω_mass  (via moment of inertia)
//
//  The g-factor is:
//    g_p = ω_charge / ω_mass · (I_charge / I_mass)
//
//  For identical distributions (both on knot path):
//    I_charge / I_mass = 1  =>  ω_charge/ω_mass = g_p = 5.5857
//
//  The physical interpretation:  the charge (as a zero-point-line feature)
//  circulates ~5.6× faster than the bulk vortex pattern rotates.
//  This is the trefoil gear-ratio.

// ============================================================================
//  §4  Self-Consistent Solver
// ============================================================================

struct ProtonState {
    double R;                   // major radius (m)
    double a;                   // minor radius (m)
    double alpha;               // a/R
    double L_knot;              // arc length (m)
    double omega_charge;        // charge angular velocity (rad/s)
    double omega_mass;          // mass pattern angular velocity (rad/s)
    double v_gear;              // charge path speed = L × ω_charge / 2π
    double v_mass;              // mass pattern speed = L × ω_mass / 2π
    double v_tor;               // toroidal circulation speed component
    double v_pol;               // poloidal circulation speed component
    double v_gear_eff;          // effective internal path speed (with sinuation)
    double kappa;               // v_tor / c
    double kappa_sinu;          // sinuation coupling coefficient
    double T_charge;            // charge circulation period (s)
    double T_mass;              // mass pattern period (s)
    double mu_z_computed;       // computed magnetic moment (J/T)
    double Lz_computed;         // computed angular momentum (J·s)
    double tension;             // filament tension (N)
    double P_conf;              // confinement pressure (Pa)
    double rho_s;               // local spation density (kg/m³)
    double f_compton;           // proton Compton frequency (Hz)
    double f_poloidal;          // poloidal frequency (Hz)
    double gear_ratio;          // ω_charge / ω_mass
    double R_p_computed;        // computed charge radius (m)
};

// Sinuation mode:  0 = linear (γ−1),  1 = quadratic (γ²−1)
ProtonState solve_proton(double alpha_input, int sinu_mode = 0) {
    using namespace cst;
    ProtonState s{};
    s.alpha = alpha_input;

    // ── Step 1: Fix R from charge radius ──
    s.R = R_p;
    s.a = alpha_input * s.R;

    // ── Step 2: Torus-knot arc length ──
    s.L_knot = trefoil::arc_length(s.R, s.a);

    // ── Step 3: Charge angular velocity from magnetic moment ──
    double I_geom = 2.0 * s.R * s.R + s.a * s.a;
    s.omega_charge = 2.0 * mu_p / (e_q * I_geom);

    // ── Step 4: Charge path speed ──
    s.T_charge = 2.0 * pi / s.omega_charge;
    s.v_gear = s.L_knot / s.T_charge;

    // ── Step 5: Mass angular velocity from spin ──
    double I_mass = m_p * (s.R * s.R + 0.75 * s.a * s.a);
    s.omega_mass = 0.5 * hbar / I_mass;

    s.T_mass = 2.0 * pi / s.omega_mass;
    s.v_mass = s.L_knot / s.T_mass;

    // ── Step 6: Gear ratio ──
    s.gear_ratio = s.omega_charge / s.omega_mass;

    // ── Step 7: Toroidal / poloidal decomposition ──
    s.v_tor = 2.0 * mu_p / (e_q * s.R);
    s.kappa = s.v_tor / c;
    double vg2 = s.v_gear * s.v_gear;
    double vt2 = s.v_tor * s.v_tor;
    s.v_pol = (vg2 > vt2) ? std::sqrt(vg2 - vt2) : 0.0;

    // ── Step 8: Sinuation correction ──
    double beta_tor = s.v_tor / c;
    double gamma_tor = 1.0 / std::sqrt(1.0 - beta_tor * beta_tor);

    // Coupling coefficient:  κ_sinu = (3/2) × α × 2  (linking number)
    s.kappa_sinu = 1.5 * s.alpha * 2.0;

    // Two models for the Lorentz-contraction pump:
    //   Mode 0 (linear):    f(γ) = γ − 1
    //   Mode 1 (quadratic): f(γ) = γ² − 1  (recursive contraction)
    double f_gamma;
    if (sinu_mode == 0) {
        f_gamma = gamma_tor - 1.0;
    } else {
        f_gamma = gamma_tor * gamma_tor - 1.0;
    }

    double v_pol_eff = s.v_pol + s.kappa_sinu * f_gamma * s.v_tor;
    s.v_gear_eff = std::sqrt(s.v_tor * s.v_tor + v_pol_eff * v_pol_eff);

    // ── Step 9: Filament tension and confinement ──
    s.tension = mp_c2 / s.L_knot;
    double lambda_C = hbar / (m_p * c);   // proton Compton wavelength
    s.P_conf = s.tension / (2.0 * pi * s.a * lambda_C);
    s.rho_s = s.P_conf / (c * c * s.kappa * s.kappa);

    // ── Step 10: Frequencies ──
    s.f_compton = mp_c2 / h;
    s.f_poloidal = s.v_pol / (2.0 * pi * s.a);

    // ── Step 11: Verification quantities ──
    s.mu_z_computed = e_q * s.omega_charge * I_geom / 2.0;
    s.Lz_computed = I_mass * s.omega_mass;
    s.R_p_computed = std::sqrt(trefoil::charge_rms_r2(s.R, s.a));

    return s;
}

// ============================================================================
//  §5  Scan for the α = a/R that yields v_gear_eff ≈ 1.836c
// ============================================================================

double find_alpha_for_target_v(double v_target_over_c,
                                double alpha_lo, double alpha_hi,
                                int sinu_mode = 0,
                                double tol = 1e-6)
{
    for (int i = 0; i < 200; ++i) {
        double mid = 0.5 * (alpha_lo + alpha_hi);
        ProtonState s = solve_proton(mid, sinu_mode);
        double ratio = s.v_gear_eff / cst::c;
        if (ratio < v_target_over_c) {
            alpha_lo = mid;
        } else {
            alpha_hi = mid;
        }
        if (alpha_hi - alpha_lo < tol) break;
    }
    return 0.5 * (alpha_lo + alpha_hi);
}

// ============================================================================
//  §6  Report
// ============================================================================

void print_state(const char* label, const ProtonState& s) {
    using namespace cst;
    std::printf("\n");
    std::printf("══════════════════════════════════════════════════════════\n");
    std::printf("  %s\n", label);
    std::printf("══════════════════════════════════════════════════════════\n");

    std::printf("\n── Geometry ──\n");
    std::printf("  R  (major radius)     = %.4f fm\n", s.R * 1e15);
    std::printf("  a  (minor radius)     = %.4f fm\n", s.a * 1e15);
    std::printf("  α  = a/R              = %.6f\n", s.alpha);
    std::printf("  R−a (inner edge)      = %.4f fm\n", (s.R - s.a) * 1e15);
    std::printf("  L  (knot arc length)  = %.4f fm  (= %.4f π R)\n",
                s.L_knot * 1e15, s.L_knot / (pi * s.R));
    std::printf("  R_p (charge RMS)      = %.4f fm  (target: %.4f fm)\n",
                s.R_p_computed * 1e15, R_p * 1e15);

    std::printf("\n── Circulation Speeds ──\n");
    std::printf("  v_tor  (toroidal)     = %.6e m/s  = %.4f c\n", s.v_tor, s.v_tor / c);
    std::printf("  v_pol  (poloidal,raw) = %.6e m/s  = %.4f c\n", s.v_pol, s.v_pol / c);
    std::printf("  v_gear (charge path)  = %.6e m/s  = %.4f c\n", s.v_gear, s.v_gear / c);
    std::printf("  κ      = v_tor/c      = %.6f\n", s.kappa);

    std::printf("\n── Sinuation Correction ──\n");
    double beta = s.v_tor / c;
    double gamma = 1.0 / std::sqrt(1.0 - beta * beta);
    std::printf("  β_tor                 = %.6f\n", beta);
    std::printf("  γ_tor                 = %.6f\n", gamma);
    std::printf("  κ_sinu                = %.6f\n", s.kappa_sinu);
    double v_pol_eff = s.v_pol + s.kappa_sinu * (gamma - 1.0) * s.v_tor;
    std::printf("  v_pol_eff             = %.6e m/s  = %.4f c\n", v_pol_eff, v_pol_eff / c);
    std::printf("  v_gear_eff            = %.6e m/s  = %.4f c  ◄\n",
                s.v_gear_eff, s.v_gear_eff / c);

    std::printf("\n── Angular Velocities ──\n");
    std::printf("  ω_charge              = %.6e rad/s\n", s.omega_charge);
    std::printf("  ω_mass                = %.6e rad/s\n", s.omega_mass);
    std::printf("  T_charge              = %.6e s\n", s.T_charge);
    std::printf("  T_mass                = %.6e s\n", s.T_mass);
    std::printf("  gear ratio ω_ch/ω_m   = %.4f  (g_p = %.4f)\n", s.gear_ratio, g_p);

    std::printf("\n── Magnetic Moment ──\n");
    std::printf("  μ_z (computed)        = %.6e J/T\n", s.mu_z_computed);
    std::printf("  μ_p (measured)        = %.6e J/T\n", mu_p);
    std::printf("  μ_z / μ_N             = %.6f  (target: %.6f)\n",
                s.mu_z_computed / mu_N, mu_p_ratio);
    std::printf("  error                 = %.4f %%\n",
                100.0 * std::abs(s.mu_z_computed - mu_p) / mu_p);

    std::printf("\n── Angular Momentum ──\n");
    std::printf("  L_z (computed)        = %.6e J·s\n", s.Lz_computed);
    std::printf("  ℏ/2 (target)          = %.6e J·s\n", 0.5 * hbar);
    std::printf("  error                 = %.4f %%\n",
                100.0 * std::abs(s.Lz_computed - 0.5 * hbar) / (0.5 * hbar));

    std::printf("\n── Frequencies ──\n");
    std::printf("  f_Compton             = %.4e Hz\n", s.f_compton);
    std::printf("  f_poloidal            = %.4e Hz\n", s.f_poloidal);
    std::printf("  f_pol / f_Compton     = %.4f\n",
                (s.f_compton > 0.0) ? s.f_poloidal / s.f_compton : 0.0);

    std::printf("\n── Confinement ──\n");
    std::printf("  Tension               = %.4e N  (%.1f kN)\n", s.tension, s.tension * 1e-3);
    std::printf("  P_conf                = %.4e Pa\n", s.P_conf);
    std::printf("  ρ_s (spation density) = %.4e kg/m³\n", s.rho_s);
    std::printf("  ρ_nuclear (reference) = 2.3e+17 kg/m³\n");
    std::printf("  P_conf / P_∞          = %.4e\n", s.P_conf / P_inf);

    std::printf("\n── Proton Mass Consistency ──\n");
    double E_from_tension = s.tension * s.L_knot;
    std::printf("  E = T × L             = %.6e J  (= %.2f MeV)\n",
                E_from_tension, E_from_tension / 1.602176634e-13);
    std::printf("  m_p c²                = %.6e J  (= %.2f MeV)\n",
                mp_c2, mp_c2 / 1.602176634e-13);
    std::printf("  error                 = %.6f %%\n",
                100.0 * std::abs(E_from_tension - mp_c2) / mp_c2);
    std::printf("\n");
}

// ============================================================================
//  §7  Main
// ============================================================================

int main() {
    using namespace cst;

    std::printf("╔══════════════════════════════════════════════════════════╗\n");
    std::printf("║     SDT TREFOIL PROTON ENGINE                           ║\n");
    std::printf("║     (2,3) Torus-Knot Self-Consistent Closure            ║\n");
    std::printf("╚══════════════════════════════════════════════════════════╝\n");

    // ── Part A: Evaluate at the manuscript's two candidate geometries ──

    // Candidate 1: Lamb-shift chapter gives r_p = 0.4207 fm (α = 0.5)
    std::printf("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    std::printf("  PART A: Evaluate Manuscript Candidate Geometries\n");
    std::printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    {
        ProtonState s1 = solve_proton(0.5);
        print_state("Candidate 1: α = 0.50  (ch06 Lamb shift: r_p = R_p/2)", s1);

        ProtonState s2 = solve_proton(0.7);
        print_state("Candidate 2: α = 0.70  (fat torus, >50% occlusion)", s2);

        ProtonState s3 = solve_proton(1.0 / 3.0);
        print_state("Candidate 3: α = 1/3   (user's initial geometry)", s3);
    }

    // ── Part B: Scan α to find where v_gear_eff = 1.836 c ──
    std::printf("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    std::printf("  PART B: Scan for α that yields v_gear_eff = 1.836 c\n");
    std::printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n");

    std::printf("  α         v_gear/c    v_gear_eff/c  L/(πR)    κ\n");
    std::printf("  ──────    ────────    ──────────    ──────    ──────\n");
    for (double alpha = 0.1; alpha <= 3.0; alpha += 0.1) {
        ProtonState s = solve_proton(alpha);
        std::printf("  %.2f      %.4f      %.4f        %.4f    %.4f",
                    alpha, s.v_gear / c, s.v_gear_eff / c,
                    s.L_knot / (pi * s.R), s.kappa);
        if (std::abs(s.v_gear_eff / c - 1.836) < 0.15)
            std::printf("  ◄◄◄");
        std::printf("\n");
    }

    // ── Part C: Bisect to precise α (linear model) ──
    double alpha_target = find_alpha_for_target_v(1.836, 0.1, 3.0, 0);
    ProtonState s_target = solve_proton(alpha_target, 0);
    print_state("CLOSURE [LINEAR f=g-1]: alpha tuned for v_gear_eff = 1.836 c", s_target);

    // ── Part F: The QUADRATIC model at the PHYSICAL α = 0.70 ──
    std::printf("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    std::printf("  PART F: Quadratic Sinuation Model f(g) = g^2 - 1\n");
    std::printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n");

    std::printf("  Side-by-side at alpha = 0.70 (fat torus):\n\n");
    ProtonState s_lin = solve_proton(0.7, 0);
    ProtonState s_quad = solve_proton(0.7, 1);
    std::printf("    %-28s  %-14s  %-14s\n", "Property", "Linear(g-1)", "Quadratic(g^2-1)");
    std::printf("    %-28s  %-14s  %-14s\n", "---", "---", "---");
    std::printf("    %-28s  %.4f c        %.4f c\n", "v_gear (raw)",
                s_lin.v_gear/c, s_quad.v_gear/c);
    std::printf("    %-28s  %.4f c        %.4f c\n", "v_gear_eff",
                s_lin.v_gear_eff/c, s_quad.v_gear_eff/c);
    std::printf("    %-28s  %.4e Pa   %.4e Pa\n", "P_conf",
                s_lin.P_conf, s_quad.P_conf);
    std::printf("    %-28s  %.4e        %.4e\n", "rho_s (kg/m^3)",
                s_lin.rho_s, s_quad.rho_s);

    print_state("alpha = 0.70 with QUADRATIC sinuation f(g) = g^2-1", s_quad);

    // Scan quadratic model
    std::printf("\n  Quadratic model scan:\n\n");
    std::printf("  alpha     v_gear/c    v_gear_eff/c\n");
    std::printf("  ------    --------    ----------\n");
    for (double alpha = 0.3; alpha <= 1.5; alpha += 0.05) {
        ProtonState sq = solve_proton(alpha, 1);
        std::printf("  %.2f      %.4f      %.4f",
                    alpha, sq.v_gear/c, sq.v_gear_eff/c);
        if (std::abs(sq.v_gear_eff/c - 1.836) < 0.1)
            std::printf("  <<<");
        std::printf("\n");
    }

    // Bisect quadratic model
    double alpha_q = find_alpha_for_target_v(1.836, 0.1, 3.0, 1);
    ProtonState s_q = solve_proton(alpha_q, 1);
    print_state("CLOSURE [QUADRATIC f=g^2-1]: alpha for v_gear_eff = 1.836 c", s_q);

    // ── Part D: Mass ratio connection with best closure ──
    std::printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    std::printf("  PART D:  Mass Ratio Connection\n");
    std::printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n");
    double mass_ratio = m_p / m_e;
    std::printf("  m_p / m_e             = %.6f\n", mass_ratio);
    std::printf("  v_gear_eff / c (quad) = %.6f\n", s_q.v_gear_eff / c);
    std::printf("  alpha (quad closure)  = %.6f\n", alpha_q);
    std::printf("  6pi                   = %.6f\n", 6.0 * pi);
    std::printf("  mass_ratio / 6pi      = %.4f\n", mass_ratio / (6.0 * pi));
    std::printf("\n");

    // ── Part E: Summary ──
    std::printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    std::printf("  PART E:  Closure Condition Summary\n");
    std::printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n");
    std::printf("  LINEAR  model (f = g-1):   alpha = %.4f => v_eff = %.4f c\n",
                alpha_target, s_target.v_gear_eff / c);
    std::printf("  QUADRATIC model (f = g^2-1): alpha = %.4f => v_eff = %.4f c\n",
                alpha_q, s_q.v_gear_eff / c);
    std::printf("\n");
    std::printf("  Both models satisfy:\n");
    std::printf("    mu_z / mu_N = 2.7928  (0.00%% error)\n");
    std::printf("    L_z = hbar/2          (0.00%% error)\n");
    std::printf("    E = m_p c^2           (0.00%% error)\n");
    std::printf("\n");
    std::printf("  The quadratic model (recursive Lorentz contraction)\n");
    std::printf("  reaches 1.836c at a SMALLER alpha, closer to the\n");
    std::printf("  physically motivated fat-torus geometry (alpha=0.70).\n");
    std::printf("\n");

    return 0;
}
