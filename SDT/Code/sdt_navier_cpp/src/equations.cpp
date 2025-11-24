#include "sdt_navier/equations.hpp"
#include "sdt_navier/constants.hpp"
#include "sdt_navier/fields.hpp"
#include <cmath>
#include <algorithm>

namespace sdt_navier {

SDTNavierEquations::SDTNavierEquations(
    double rho_s,
    double alpha_curv,
    double beta_slip,
    double gamma_create,
    double delta_destroy,
    double epsilon_strain,
    double zeta_heal
) : rho_s_(rho_s), alpha_curv_(alpha_curv), beta_slip_(beta_slip),
    gamma_create_(gamma_create), delta_destroy_(delta_destroy),
    epsilon_strain_(epsilon_strain), zeta_heal_(zeta_heal)
{}

std::vector<FieldSystem::Vector3d> SDTNavierEquations::compute_force_curvature(
    const FieldSystem& fields,
    const std::vector<std::array<double, 3>>& grad_kappa
) const {
    std::vector<FieldSystem::Vector3d> F_curv(fields.size());
    for (std::size_t i = 0; i < fields.size(); ++i) {
        F_curv[i] = -alpha_curv_ * FieldSystem::Vector3d(
            grad_kappa[i][0],
            grad_kappa[i][1],
            grad_kappa[i][2]
        );
    }
    return F_curv;
}

std::vector<FieldSystem::Vector3d> SDTNavierEquations::compute_force_slip(
    const FieldSystem& fields
) const {
    std::vector<FieldSystem::Vector3d> F_slip(fields.size());
    auto eta = fields.eta();
    const auto& v = fields.v();

    for (std::size_t i = 0; i < fields.size(); ++i) {
        F_slip[i] = -beta_slip_ * eta[i] * v[i];
    }
    return F_slip;
}

std::vector<double> SDTNavierEquations::compute_curvature_creation(
    const FieldSystem& fields,
    const std::vector<std::array<std::array<double, 3>, 3>>& grad_v
) const {
    std::vector<double> C(fields.size());
    auto kappa = fields.kappa();

    for (std::size_t i = 0; i < fields.size(); ++i) {
        // Compute divergence
        double div_v = grad_v[i][0][0] + grad_v[i][1][1] + grad_v[i][2][2];
        C[i] = gamma_create_ * kappa[i] * std::abs(div_v);
    }
    return C;
}

std::vector<double> SDTNavierEquations::compute_curvature_destruction(
    const FieldSystem& fields
) const {
    std::vector<double> D(fields.size());
    auto kappa = fields.kappa();
    auto eta = fields.eta();

    for (std::size_t i = 0; i < fields.size(); ++i) {
        D[i] = delta_destroy_ * kappa[i] * eta[i];
    }
    return D;
}

std::vector<double> SDTNavierEquations::compute_slip_strain(
    const FieldSystem& fields,
    const std::vector<std::array<std::array<double, 3>, 3>>& grad_v
) const {
    std::vector<double> S_strain(fields.size());
    auto kappa = fields.kappa();

    for (std::size_t i = 0; i < fields.size(); ++i) {
        // Compute |∇v| as Frobenius norm
        double norm = 0.0;
        for (std::size_t a = 0; a < 3; ++a) {
            for (std::size_t b = 0; b < 3; ++b) {
                norm += grad_v[i][a][b] * grad_v[i][a][b];
            }
        }
        norm = std::sqrt(norm);
        S_strain[i] = epsilon_strain_ * kappa[i] * norm;
    }
    return S_strain;
}

std::vector<double> SDTNavierEquations::compute_slip_healing(
    const FieldSystem& fields
) const {
    std::vector<double> S_healing(fields.size());
    auto kappa = fields.kappa();

    for (std::size_t i = 0; i < fields.size(); ++i) {
        S_healing[i] = zeta_heal_ * kappa[i] * kappa[i];
    }
    return S_healing;
}

std::vector<FieldSystem::Vector3d> SDTNavierEquations::compute_flow_rhs(
    const FieldSystem& fields,
    const std::vector<std::array<double, 3>>& grad_P,
    const std::vector<std::array<std::array<double, 3>, 3>>& grad_v,
    const std::vector<FieldSystem::Vector3d>& F_curv,
    const std::vector<FieldSystem::Vector3d>& F_slip
) const {
    std::vector<FieldSystem::Vector3d> dv_dt(fields.size());
    const auto& v = fields.v();

    for (std::size_t i = 0; i < fields.size(); ++i) {
        // Advection term: (v·∇)v
        FieldSystem::Vector3d v_advect(0.0, 0.0, 0.0);
        for (std::size_t a = 0; a < 3; ++a) {
            for (std::size_t b = 0; b < 3; ++b) {
                v_advect[a] += v[i][b] * grad_v[i][a][b];
            }
        }

        // Total acceleration
        FieldSystem::Vector3d grad_P_vec(grad_P[i][0], grad_P[i][1], grad_P[i][2]);
        dv_dt[i] = (-grad_P_vec + F_curv[i] + F_slip[i] - rho_s_ * v_advect) / rho_s_;
    }
    return dv_dt;
}

std::vector<double> SDTNavierEquations::compute_curvature_rhs(
    const FieldSystem& fields,
    const std::vector<std::array<double, 3>>& grad_kappa,
    const std::vector<std::array<std::array<double, 3>, 3>>& grad_v,
    const std::vector<double>& C,
    const std::vector<double>& D
) const {
    std::vector<double> dkappa_dt(fields.size());
    const auto& v = fields.v();

    for (std::size_t i = 0; i < fields.size(); ++i) {
        // Advection: (v·∇)κ
        double v_dot_grad_kappa = v[i][0] * grad_kappa[i][0] +
                                  v[i][1] * grad_kappa[i][1] +
                                  v[i][2] * grad_kappa[i][2];
        dkappa_dt[i] = C[i] - D[i] - v_dot_grad_kappa;
    }
    return dkappa_dt;
}

std::vector<double> SDTNavierEquations::compute_slip_rhs(
    const FieldSystem& fields,
    const std::vector<std::array<double, 3>>& grad_eta,
    const std::vector<std::array<std::array<double, 3>, 3>>& grad_v,
    const std::vector<double>& S_strain,
    const std::vector<double>& S_healing
) const {
    std::vector<double> deta_dt(fields.size());
    const auto& v = fields.v();

    for (std::size_t i = 0; i < fields.size(); ++i) {
        // Advection: (v·∇)η
        double v_dot_grad_eta = v[i][0] * grad_eta[i][0] +
                                v[i][1] * grad_eta[i][1] +
                                v[i][2] * grad_eta[i][2];
        deta_dt[i] = S_strain[i] - S_healing[i] - v_dot_grad_eta;
    }
    return deta_dt;
}

std::vector<double> SDTNavierEquations::compute_energy_rhs(
    const FieldSystem& fields,
    const std::vector<std::array<double, 3>>& grad_e,
    const std::vector<double>& sigma
) const {
    std::vector<double> de_dt(fields.size());
    const auto& v = fields.v();
    auto P = fields.P();

    for (std::size_t i = 0; i < fields.size(); ++i) {
        // Advection: (v·∇)e
        double v_dot_grad_e = v[i][0] * grad_e[i][0] +
                              v[i][1] * grad_e[i][1] +
                              v[i][2] * grad_e[i][2];
        // Source: P·σ
        de_dt[i] = P[i] * sigma[i] - v_dot_grad_e;
    }
    return de_dt;
}

}  // namespace sdt_navier

