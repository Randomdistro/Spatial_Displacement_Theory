#pragma once

/**
 * @file fields.hpp
 * @brief Field system definitions for SDT-Navier
 */

#include "sdt_navier/constants.hpp"
#include <Eigen/Dense>
#include <array>
#include <cstddef>
#include <vector>
#include <string>

namespace sdt_navier {

/**
 * @brief Field system containing all SDT-Navier fields
 * 
 * Stores 3D fields: P (pressure), v (velocity), κ (curvature),
 * η (slip), e (energy density), Γ (circulation factor)
 */
class FieldSystem {
public:
    using Vector3d = Eigen::Vector3d;
    using Array3d = Eigen::Array3d;

    /**
     * @brief Construct field system
     * @param nx, ny, nz Grid dimensions
     * @param dx, dy, dz Grid spacing (m)
     * @param P_infinity Background pressure (Pa)
     */
    FieldSystem(
        std::size_t nx, std::size_t ny, std::size_t nz,
        double dx, double dy, double dz,
        double P_infinity = sdt::P_INFINITY_NUCLEAR
    );

    // Field accessors
    Eigen::Map<Eigen::ArrayXd> P() { return Eigen::Map<Eigen::ArrayXd>(P_.data(), size_); }
    Eigen::Map<Eigen::ArrayXd> kappa() { return Eigen::Map<Eigen::ArrayXd>(kappa_.data(), size_); }
    Eigen::Map<Eigen::ArrayXd> eta() { return Eigen::Map<Eigen::ArrayXd>(eta_.data(), size_); }
    Eigen::Map<Eigen::ArrayXd> e() { return Eigen::Map<Eigen::ArrayXd>(e_.data(), size_); }
    Eigen::Map<Eigen::ArrayXd> Gamma() { return Eigen::Map<Eigen::ArrayXd>(Gamma_.data(), size_); }
    
    // Velocity field (3D vector at each point)
    std::vector<Vector3d>& v() { return v_; }
    const std::vector<Vector3d>& v() const { return v_; }

    // Const accessors
    const Eigen::Map<const Eigen::ArrayXd> P() const { return Eigen::Map<const Eigen::ArrayXd>(P_.data(), size_); }
    const Eigen::Map<const Eigen::ArrayXd> kappa() const { return Eigen::Map<const Eigen::ArrayXd>(kappa_.data(), size_); }
    const Eigen::Map<const Eigen::ArrayXd> eta() const { return Eigen::Map<const Eigen::ArrayXd>(eta_.data(), size_); }
    const Eigen::Map<const Eigen::ArrayXd> e() const { return Eigen::Map<const Eigen::ArrayXd>(e_.data(), size_); }
    const Eigen::Map<const Eigen::ArrayXd> Gamma() const { return Eigen::Map<const Eigen::ArrayXd>(Gamma_.data(), size_); }

    // Grid properties
    std::size_t nx() const { return nx_; }
    std::size_t ny() const { return ny_; }
    std::size_t nz() const { return nz_; }
    std::size_t size() const { return size_; }
    double dx() const { return dx_; }
    double dy() const { return dy_; }
    double dz() const { return dz_; }
    double dt() const { return dt_; }
    void set_dt(double dt) { dt_ = dt; }
    double t() const { return t_; }
    void set_t(double t) { t_ = t; }

    // Index conversion
    std::size_t index(std::size_t i, std::size_t j, std::size_t k) const {
        return i + nx_ * (j + ny_ * k);
    }
    std::array<std::size_t, 3> coords(std::size_t idx) const {
        std::size_t i = idx % nx_;
        std::size_t j = (idx / nx_) % ny_;
        std::size_t k = idx / (nx_ * ny_);
        return {i, j, k};
    }

    // Validation
    void validate() const;

private:
    std::size_t nx_, ny_, nz_, size_;
    double dx_, dy_, dz_;
    double dt_ = 0.0;
    double t_ = 0.0;

    // Scalar fields
    std::vector<double> P_;
    std::vector<double> kappa_;
    std::vector<double> eta_;
    std::vector<double> e_;
    std::vector<double> Gamma_;

    // Vector field (velocity)
    std::vector<Vector3d> v_;
};

/**
 * @brief Initialize field system with default values
 */
void initialize_fields(
    FieldSystem& fields,
    double P_infinity = sdt::P_INFINITY_NUCLEAR,
    double initial_kappa = 0.0,
    double initial_eta = 0.01,
    double initial_Gamma = sdt::GAMMA_P
);

/**
 * @brief Compute asymptotic pressure P_infinity from SDT formula
 * P_infinity = (ħ^2 * n_e * rho_n) / (2 * m_e * r_n^2 * alpha^2)
 */
double compute_p_infinity(
    double n_e,
    double rho_n,
    double r_n,
    double alpha = sdt::ALPHA
);

/**
 * @brief Hydrogen reference P_infinity (using SDT compendium constants)
 */
double compute_p_infinity_hydrogen();

/**
 * @brief Add turbine source to fields
 * @param fields Field system to modify
 * @param position Grid indices (i, j, k)
 * @param radius_cells Turbine radius in grid cells
 * @param kappa_value Peak curvature (m⁻¹)
 * @param Gamma_value Circulation factor
 * @param eta_value Slip value
 * @param profile "gaussian" or "step"
 */
void add_turbine_source(
    FieldSystem& fields,
    const std::array<std::size_t, 3>& position,
    double radius_cells,
    double kappa_value,
    double Gamma_value,
    double eta_value,
    const std::string& profile = "gaussian"
);

/**
 * @brief Compute diversion density σ = Γ κ (1-η)
 */
std::vector<double> compute_diversion_density(const FieldSystem& fields);

}  // namespace sdt_navier

