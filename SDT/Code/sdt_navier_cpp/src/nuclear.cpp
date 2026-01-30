#include "sdt_navier/nuclear.hpp"
#include "sdt_navier/fields.hpp"
#include "sdt_navier/constants.hpp"
#include <cmath>
#include <algorithm>
#include <numbers>

namespace sdt_navier {

ProtonTurbine::ProtonTurbine(
    const std::array<std::size_t, 3>& position,
    double radius_cells,
    bool bound
) {
    this->position = position;
    this->radius_cells = radius_cells;
    this->kappa = sdt::KAPPA_P;
    this->Gamma = sdt::GAMMA_P;
    this->eta = bound ? sdt::ETA_P_BOUND : sdt::ETA_P_BOUND;  // Same for now
    this->cell_type = "proton";
}

NeutronTurbine::NeutronTurbine(
    const std::array<std::size_t, 3>& position,
    double radius_cells,
    bool bound
) {
    this->position = position;
    this->radius_cells = radius_cells;
    this->kappa = sdt::KAPPA_N;
    this->Gamma = sdt::GAMMA_E_N;
    this->eta = bound ? sdt::ETA_N_BOUND : sdt::ETA_N_FREE;
    this->cell_type = "neutron";
}

DeuteronSystem::DeuteronSystem(
    FieldSystem& fields,
    const std::array<std::size_t, 3>& center,
    double separation_cells
) : fields_(fields),
    proton_([&]() {
        std::size_t i0 = center[0];
        std::size_t j0 = center[1];
        std::size_t k0 = center[2];
        std::size_t i_p = static_cast<std::size_t>(i0 - separation_cells / 2.0);
        double radius_cells = std::max(1.0, sdt::R_P / fields.dx());
        return ProtonTurbine({i_p, j0, k0}, radius_cells, true);
    }()),
    neutron_([&]() {
        std::size_t i0 = center[0];
        std::size_t j0 = center[1];
        std::size_t k0 = center[2];
        std::size_t i_n = static_cast<std::size_t>(i0 + separation_cells / 2.0);
        double radius_cells = std::max(1.0, sdt::R_P / fields.dx());
        return NeutronTurbine({i_n, j0, k0}, radius_cells, true);
    }())
{
    std::size_t i0 = center[0];
    std::size_t j0 = center[1];
    std::size_t k0 = center[2];

    // Place proton and neutron along x-axis
    std::size_t i_p = static_cast<std::size_t>(i0 - separation_cells / 2.0);
    std::size_t i_n = static_cast<std::size_t>(i0 + separation_cells / 2.0);

    // Add turbines to fields
    add_turbine_source(fields_, proton_.position, proton_.radius_cells,
                      proton_.kappa, proton_.Gamma, proton_.eta, "gaussian");
    add_turbine_source(fields_, neutron_.position, neutron_.radius_cells,
                      neutron_.kappa, neutron_.Gamma, neutron_.eta, "gaussian");
}

double DeuteronSystem::compute_binding_energy() const {
    // Energy per unit volume from master equation
    double sigma_bound = proton_.Gamma * proton_.kappa * (1.0 - proton_.eta) +
                        neutron_.Gamma * neutron_.kappa * (1.0 - neutron_.eta);

    // Free state
    ProtonTurbine proton_free(proton_.position, proton_.radius_cells, false);
    NeutronTurbine neutron_free(neutron_.position, neutron_.radius_cells, false);
    double sigma_free = proton_free.Gamma * proton_free.kappa * (1.0 - proton_free.eta) +
                       neutron_free.Gamma * neutron_free.kappa * (1.0 - neutron_free.eta);

    double delta_sigma = sigma_bound - sigma_free;
    double P_infinity = sdt::P_INFINITY_NUCLEAR;

    // Approximate volume
    constexpr double SEPARATION = 2.0e-15;  // m
    double volume_per_turbine = (4.0 * std::numbers::pi / 3.0) * std::pow(SEPARATION / 2.0, 3);
    double total_volume = 2.0 * volume_per_turbine;

    double B = P_infinity * delta_sigma * total_volume;
    double tau_char = sdt::R_P / constants::C;
    B *= tau_char;

    return B;
}

double DeuteronSystem::compute_binding_energy_mev() const {
    double B_j = compute_binding_energy();
    return B_j / (1.602e-13);  // Convert J to MeV
}

TritonSystem::TritonSystem(
    FieldSystem& fields,
    const std::array<std::size_t, 3>& center,
    double separation_cells
) : fields_(fields),
    neutron1_([&]() {
        std::size_t i0 = center[0];
        std::size_t j0 = center[1];
        std::size_t k0 = center[2];
        double radius_cells = std::max(1.0, sdt::R_P / fields.dx());
        return NeutronTurbine({i0 - static_cast<std::size_t>(separation_cells), j0, k0}, radius_cells, true);
    }()),
    proton_([&]() {
        std::size_t i0 = center[0];
        std::size_t j0 = center[1];
        std::size_t k0 = center[2];
        double radius_cells = std::max(1.0, sdt::R_P / fields.dx());
        return ProtonTurbine({i0, j0, k0}, radius_cells, true);
    }()),
    neutron2_([&]() {
        std::size_t i0 = center[0];
        std::size_t j0 = center[1];
        std::size_t k0 = center[2];
        double radius_cells = std::max(1.0, sdt::R_P / fields.dx());
        return NeutronTurbine({i0 + static_cast<std::size_t>(separation_cells), j0, k0}, radius_cells, true);
    }())
{
    std::size_t i0 = center[0];
    std::size_t j0 = center[1];
    std::size_t k0 = center[2];

    add_turbine_source(fields_, neutron1_.position, neutron1_.radius_cells,
                      neutron1_.kappa, neutron1_.Gamma, neutron1_.eta, "gaussian");
    add_turbine_source(fields_, proton_.position, proton_.radius_cells,
                      proton_.kappa, proton_.Gamma, proton_.eta, "gaussian");
    add_turbine_source(fields_, neutron2_.position, neutron2_.radius_cells,
                      neutron2_.kappa, neutron2_.Gamma, neutron2_.eta, "gaussian");
}

HelionSystem::HelionSystem(
    FieldSystem& fields,
    const std::array<std::size_t, 3>& center,
    double separation_cells
) : fields_(fields),
    proton1_([&]() {
        std::size_t i0 = center[0];
        std::size_t j0 = center[1];
        std::size_t k0 = center[2];
        double radius_cells = std::max(1.0, sdt::R_P / fields.dx());
        return ProtonTurbine({i0 - static_cast<std::size_t>(separation_cells), j0, k0}, radius_cells, true);
    }()),
    neutron_([&]() {
        std::size_t i0 = center[0];
        std::size_t j0 = center[1];
        std::size_t k0 = center[2];
        double radius_cells = std::max(1.0, sdt::R_P / fields.dx());
        return NeutronTurbine({i0, j0, k0}, radius_cells, true);
    }()),
    proton2_([&]() {
        std::size_t i0 = center[0];
        std::size_t j0 = center[1];
        std::size_t k0 = center[2];
        double radius_cells = std::max(1.0, sdt::R_P / fields.dx());
        return ProtonTurbine({i0 + static_cast<std::size_t>(separation_cells), j0, k0}, radius_cells, true);
    }())
{
    std::size_t i0 = center[0];
    std::size_t j0 = center[1];
    std::size_t k0 = center[2];

    add_turbine_source(fields_, proton1_.position, proton1_.radius_cells,
                      proton1_.kappa, proton1_.Gamma, proton1_.eta, "gaussian");
    add_turbine_source(fields_, neutron_.position, neutron_.radius_cells,
                      neutron_.kappa, neutron_.Gamma, neutron_.eta, "gaussian");
    add_turbine_source(fields_, proton2_.position, proton2_.radius_cells,
                      proton2_.kappa, proton2_.Gamma, proton2_.eta, "gaussian");
}

AlphaSystem::AlphaSystem(
    FieldSystem& fields,
    const std::array<std::size_t, 3>& center,
    double separation_cells
) : fields_(fields),
    proton1_([&]() {
        std::size_t i0 = center[0];
        std::size_t j0 = center[1];
        std::size_t k0 = center[2];
        double radius_cells = std::max(1.0, sdt::R_P / fields.dx());
        return ProtonTurbine({i0 - static_cast<std::size_t>(separation_cells), j0, k0}, radius_cells, true);
    }()),
    proton2_([&]() {
        std::size_t i0 = center[0];
        std::size_t j0 = center[1];
        std::size_t k0 = center[2];
        double radius_cells = std::max(1.0, sdt::R_P / fields.dx());
        return ProtonTurbine({i0 + static_cast<std::size_t>(separation_cells), j0, k0}, radius_cells, true);
    }()),
    neutron1_([&]() {
        std::size_t i0 = center[0];
        std::size_t j0 = center[1];
        std::size_t k0 = center[2];
        double radius_cells = std::max(1.0, sdt::R_P / fields.dx());
        return NeutronTurbine({i0, j0 - static_cast<std::size_t>(separation_cells), k0}, radius_cells, true);
    }()),
    neutron2_([&]() {
        std::size_t i0 = center[0];
        std::size_t j0 = center[1];
        std::size_t k0 = center[2];
        double radius_cells = std::max(1.0, sdt::R_P / fields.dx());
        return NeutronTurbine({i0, j0 + static_cast<std::size_t>(separation_cells), k0}, radius_cells, true);
    }())
{
    std::size_t i0 = center[0];
    std::size_t j0 = center[1];
    std::size_t k0 = center[2];

    add_turbine_source(fields_, proton1_.position, proton1_.radius_cells,
                      proton1_.kappa, proton1_.Gamma, proton1_.eta, "gaussian");
    add_turbine_source(fields_, proton2_.position, proton2_.radius_cells,
                      proton2_.kappa, proton2_.Gamma, proton2_.eta, "gaussian");
    add_turbine_source(fields_, neutron1_.position, neutron1_.radius_cells,
                      neutron1_.kappa, neutron1_.Gamma, neutron1_.eta, "gaussian");
    add_turbine_source(fields_, neutron2_.position, neutron2_.radius_cells,
                      neutron2_.kappa, neutron2_.Gamma, neutron2_.eta, "gaussian");
}

}  // namespace sdt_navier

