#include "sdt_navier/solver.hpp"
#include "sdt_navier/constants.hpp"
#include "sdt_navier/operators.hpp"
#include "sdt_navier/fields.hpp"
#include <algorithm>
#include <cmath>
#include <functional>

namespace sdt_navier {

SDTNavierSolver::SDTNavierSolver(
    FieldSystem& fields,
    const SDTNavierEquations& equations,
    double dt,
    double cfl,
    const std::string& method,
    bool enforce_incompressibility
) : fields_(fields), equations_(equations), cfl_(cfl),
    method_(method), enforce_incompressibility_(enforce_incompressibility),
    t_(fields.t())
{
    if (dt == 0.0) {
        dt_ = estimate_timestep();
    } else {
        dt_ = dt;
    }
}

double SDTNavierSolver::estimate_timestep() const {
    // CFL condition: dt < CFL * dx / |v_max|
    double v_max = 0.0;
    for (const auto& vi : fields_.v()) {
        double v_mag = vi.norm();
        if (v_mag > v_max) v_max = v_mag;
    }
    if (v_max == 0.0) v_max = 1.0;

    double dx_min = std::min({fields_.dx(), fields_.dy(), fields_.dz()});
    double dt = cfl_ * dx_min / v_max;

    // Also consider slip damping timescale
    auto eta = fields_.eta();
    double eta_max = *std::max_element(eta.begin(), eta.end());
    if (eta_max > 0.0) {
        double dt_slip = 1.0 / (equations_.beta_slip() * eta_max / equations_.rho_s());
        dt = std::min(dt, dt_slip);
    }

    return dt;
}

void SDTNavierSolver::step() {
    if (method_ == "euler") {
        step_euler();
    } else if (method_ == "rk4") {
        step_rk4();
    }
    fields_.set_t(t_);
    t_ += dt_;
}

void SDTNavierSolver::step_euler() {
    // Compute gradients
    auto P_vec = fields_.P();
    std::vector<double> P(P_vec.data(), P_vec.data() + fields_.size());
    auto grad_P = compute_gradient(P, fields_, "extrapolate");

    auto kappa_vec = fields_.kappa();
    std::vector<double> kappa(kappa_vec.data(), kappa_vec.data() + fields_.size());
    auto grad_kappa = compute_gradient(kappa, fields_, "extrapolate");

    auto eta_vec = fields_.eta();
    std::vector<double> eta(eta_vec.data(), eta_vec.data() + fields_.size());
    auto grad_eta = compute_gradient(eta, fields_, "extrapolate");

    auto e_vec = fields_.e();
    std::vector<double> e(e_vec.data(), e_vec.data() + fields_.size());
    auto grad_e = compute_gradient(e, fields_, "extrapolate");

    auto grad_v = compute_velocity_gradient(fields_.v(), fields_, "extrapolate");

    // Compute force functionals
    auto F_curv = equations_.compute_force_curvature(fields_, grad_kappa);
    auto F_slip = equations_.compute_force_slip(fields_);
    auto C = equations_.compute_curvature_creation(fields_, grad_v);
    auto D = equations_.compute_curvature_destruction(fields_);
    auto S_strain = equations_.compute_slip_strain(fields_, grad_v);
    auto S_healing = equations_.compute_slip_healing(fields_);

    // Compute RHS
    auto dv_dt = equations_.compute_flow_rhs(fields_, grad_P, grad_v, F_curv, F_slip);
    auto dkappa_dt = equations_.compute_curvature_rhs(fields_, grad_kappa, grad_v, C, D);
    auto deta_dt = equations_.compute_slip_rhs(fields_, grad_eta, grad_v, S_strain, S_healing);

    auto sigma = compute_diversion_density(fields_);
    auto de_dt = equations_.compute_energy_rhs(fields_, grad_e, sigma);

    // Update fields
    auto& v = fields_.v();
    for (std::size_t i = 0; i < fields_.size(); ++i) {
        v[i] += dt_ * dv_dt[i];
    }

    auto kappa_map = fields_.kappa();
    for (std::size_t i = 0; i < fields_.size(); ++i) {
        kappa_map[i] += dt_ * dkappa_dt[i];
    }

    auto eta_map = fields_.eta();
    for (std::size_t i = 0; i < fields_.size(); ++i) {
        eta_map[i] += dt_ * deta_dt[i];
        eta_map[i] = std::clamp(eta_map[i], 0.0, 1.0);
    }

    auto e_map = fields_.e();
    for (std::size_t i = 0; i < fields_.size(); ++i) {
        e_map[i] += dt_ * de_dt[i];
    }

    if (enforce_incompressibility_) {
        project_pressure();
    }
}

void SDTNavierSolver::step_rk4() {
    // Simplified RK4: store intermediate states and average
    // Full implementation would recompute RHS at each stage
    step_euler();  // For now, use Euler (can be enhanced)
}

void SDTNavierSolver::project_pressure() {
    // Simplified pressure projection
    auto div_v = compute_divergence(fields_.v(), fields_, "extrapolate");

    // Adjust pressure
    auto P = fields_.P();
    double alpha_p = 1.0e10;
    for (std::size_t i = 0; i < fields_.size(); ++i) {
        P[i] += alpha_p * div_v[i] * dt_;
    }

    // Correct velocity
    auto grad_div = compute_gradient(div_v, fields_, "extrapolate");
    auto& v = fields_.v();
    double beta_v = 0.1 * dt_;
    for (std::size_t i = 0; i < fields_.size(); ++i) {
        v[i] -= beta_v * FieldSystem::Vector3d(grad_div[i][0], grad_div[i][1], grad_div[i][2]);
    }
}

void SDTNavierSolver::run_until(
    double t_end,
    std::function<void(SDTNavierSolver&)> callback
) {
    while (t_ < t_end) {
        if (t_ + dt_ > t_end) {
            dt_ = t_end - t_;
        }
        step();
        if (callback) {
            callback(*this);
        }
    }
}

double SDTNavierSolver::get_divergence_error() const {
    auto div_v = compute_divergence(fields_.v(), fields_, "extrapolate");
    double max_div = 0.0;
    for (double div : div_v) {
        max_div = std::max(max_div, std::abs(div));
    }
    return max_div;
}

}  // namespace sdt_navier

