#include "sdt_navier/fields.hpp"
#include "sdt_navier/constants.hpp"
#include <algorithm>
#include <cmath>
#include <stdexcept>
#include <string>

namespace sdt_navier {

FieldSystem::FieldSystem(
    std::size_t nx, std::size_t ny, std::size_t nz,
    double dx, double dy, double dz,
    double P_infinity
) : nx_(nx), ny_(ny), nz_(nz), size_(nx * ny * nz),
    dx_(dx), dy_(dy), dz_(dz)
{
    // Allocate fields
    P_.resize(size_, P_infinity);
    kappa_.resize(size_, 0.0);
    eta_.resize(size_, 0.01);
    e_.resize(size_, 0.0);
    Gamma_.resize(size_, sdt::GAMMA_P);
    v_.resize(size_, Vector3d::Zero());

    // Initialize energy density
    for (std::size_t i = 0; i < size_; ++i) {
        double sigma = Gamma_[i] * kappa_[i] * (1.0 - eta_[i]);
        double tau_char = sdt::R_P / constants::C;  // ~2.8e-24 s
        e_[i] = P_[i] * sigma * tau_char;
    }
}

void FieldSystem::validate() const {
    // Check slip bounds
    for (std::size_t i = 0; i < size_; ++i) {
        if (eta_[i] < 0.0 || eta_[i] > 1.0) {
            throw std::runtime_error("Slip field η must satisfy 0 ≤ η ≤ 1");
        }
    }

    // Check circulation factor
    for (std::size_t i = 0; i < size_; ++i) {
        if (Gamma_[i] < 0.0) {
            throw std::runtime_error("Circulation factor Γ must be non-negative");
        }
    }
}

void initialize_fields(
    FieldSystem& fields,
    double P_infinity,
    double initial_kappa,
    double initial_eta,
    double initial_Gamma
) {
    auto P = fields.P();
    auto kappa = fields.kappa();
    auto eta = fields.eta();
    auto Gamma = fields.Gamma();

    P.setConstant(P_infinity);
    kappa.setConstant(initial_kappa);
    eta.setConstant(initial_eta);
    Gamma.setConstant(initial_Gamma);

    // Update energy density
    for (std::size_t i = 0; i < fields.size(); ++i) {
        double sigma = Gamma[i] * kappa[i] * (1.0 - eta[i]);
        double tau_char = sdt::R_P / constants::C;
        fields.e()[i] = P[i] * sigma * tau_char;
    }
}

double compute_p_infinity(
    double n_e,
    double rho_n,
    double r_n,
    double alpha
) {
    const double hbar = constants::HBAR;
    const double m_e = constants::M_E;
    const double numerator = hbar * hbar * n_e * rho_n;
    const double denominator = 2.0 * m_e * r_n * r_n * alpha * alpha;
    return numerator / denominator;
}

double compute_p_infinity_hydrogen() {
    return compute_p_infinity(
        sdt::N_E_HYDROGEN,
        sdt::RHO_N,
        sdt::R_P,
        sdt::ALPHA
    );
}

void add_turbine_source(
    FieldSystem& fields,
    const std::array<std::size_t, 3>& position,
    double radius_cells,
    double kappa_value,
    double Gamma_value,
    double eta_value,
    const std::string& profile
) {
    std::size_t i0 = position[0];
    std::size_t j0 = position[1];
    std::size_t k0 = position[2];

    auto kappa = fields.kappa();
    auto Gamma = fields.Gamma();
    auto eta = fields.eta();

    for (std::size_t k = 0; k < fields.nz(); ++k) {
        for (std::size_t j = 0; j < fields.ny(); ++j) {
            for (std::size_t i = 0; i < fields.nx(); ++i) {
                // Distance from center
                double di = static_cast<double>(i) - static_cast<double>(i0);
                double dj = static_cast<double>(j) - static_cast<double>(j0);
                double dk = static_cast<double>(k) - static_cast<double>(k0);
                double r_cells = std::sqrt(di*di + dj*dj + dk*dk);

                double weight = 0.0;
                if (profile == "gaussian") {
                    weight = std::exp(-0.5 * (r_cells / radius_cells) * (r_cells / radius_cells));
                } else if (profile == "step") {
                    weight = (r_cells < radius_cells) ? 1.0 : 0.0;
                } else {
                    throw std::runtime_error("Unknown profile type: " + profile);
                }

                std::size_t idx = fields.index(i, j, k);
                kappa[idx] = std::max(kappa[idx], kappa_value * weight);
                Gamma[idx] = std::max(Gamma[idx], Gamma_value * weight);
                eta[idx] = std::min(eta[idx], eta_value * weight);
            }
        }
    }

    // Update energy density
    auto P = fields.P();
    auto e = fields.e();
    for (std::size_t i = 0; i < fields.size(); ++i) {
        double sigma = Gamma[i] * kappa[i] * (1.0 - eta[i]);
        double tau_char = sdt::R_P / constants::C;
        e[i] = P[i] * sigma * tau_char;
    }
}

std::vector<double> compute_diversion_density(const FieldSystem& fields) {
    std::vector<double> sigma(fields.size());
    auto Gamma = fields.Gamma();
    auto kappa = fields.kappa();
    auto eta = fields.eta();

    for (std::size_t i = 0; i < fields.size(); ++i) {
        sigma[i] = Gamma[i] * kappa[i] * (1.0 - eta[i]);
    }

    return sigma;
}

}  // namespace sdt_navier

