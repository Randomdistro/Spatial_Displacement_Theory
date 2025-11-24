#pragma once

/**
 * @file equations.hpp
 * @brief SDT-Navier field equations and force functionals
 */

#include "sdt_navier/fields.hpp"
#include "sdt_navier/operators.hpp"
#include <vector>
#include <array>

namespace sdt_navier {

/**
 * @brief SDT-Navier equations with force functional parameters
 */
class SDTNavierEquations {
public:
    /**
     * @brief Construct equations with default parameters
     */
    SDTNavierEquations(
        double rho_s = sdt::RHO_S,
        double alpha_curv = 1.0e-10,
        double beta_slip = 1.0e15,
        double gamma_create = 1.0e-24,
        double delta_destroy = 1.0e-9,
        double epsilon_strain = 1.0e-24,
        double zeta_heal = 1.0e-9
    );

    // Force functionals
    std::vector<FieldSystem::Vector3d> compute_force_curvature(
        const FieldSystem& fields,
        const std::vector<std::array<double, 3>>& grad_kappa
    ) const;

    std::vector<FieldSystem::Vector3d> compute_force_slip(
        const FieldSystem& fields
    ) const;

    std::vector<double> compute_curvature_creation(
        const FieldSystem& fields,
        const std::vector<std::array<std::array<double, 3>, 3>>& grad_v
    ) const;

    std::vector<double> compute_curvature_destruction(
        const FieldSystem& fields
    ) const;

    std::vector<double> compute_slip_strain(
        const FieldSystem& fields,
        const std::vector<std::array<std::array<double, 3>, 3>>& grad_v
    ) const;

    std::vector<double> compute_slip_healing(
        const FieldSystem& fields
    ) const;

    // RHS computation
    std::vector<FieldSystem::Vector3d> compute_flow_rhs(
        const FieldSystem& fields,
        const std::vector<std::array<double, 3>>& grad_P,
        const std::vector<std::array<std::array<double, 3>, 3>>& grad_v,
        const std::vector<FieldSystem::Vector3d>& F_curv,
        const std::vector<FieldSystem::Vector3d>& F_slip
    ) const;

    std::vector<double> compute_curvature_rhs(
        const FieldSystem& fields,
        const std::vector<std::array<double, 3>>& grad_kappa,
        const std::vector<std::array<std::array<double, 3>, 3>>& grad_v,
        const std::vector<double>& C,
        const std::vector<double>& D
    ) const;

    std::vector<double> compute_slip_rhs(
        const FieldSystem& fields,
        const std::vector<std::array<double, 3>>& grad_eta,
        const std::vector<std::array<std::array<double, 3>, 3>>& grad_v,
        const std::vector<double>& S_strain,
        const std::vector<double>& S_healing
    ) const;

    std::vector<double> compute_energy_rhs(
        const FieldSystem& fields,
        const std::vector<std::array<double, 3>>& grad_e,
        const std::vector<double>& sigma
    ) const;

    // Parameters
    double rho_s() const { return rho_s_; }
    double alpha_curv() const { return alpha_curv_; }
    double beta_slip() const { return beta_slip_; }

private:
    double rho_s_;
    double alpha_curv_;
    double beta_slip_;
    double gamma_create_;
    double delta_destroy_;
    double epsilon_strain_;
    double zeta_heal_;
};

}  // namespace sdt_navier

