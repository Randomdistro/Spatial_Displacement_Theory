#pragma once

/**
 * @file nuclear.hpp
 * @brief Nuclear system models (deuteron, triton, helion, alpha)
 */

#include "sdt_navier/fields.hpp"
#include "sdt_navier/constants.hpp"
#include <array>
#include <vector>

namespace sdt_navier {

/**
 * @brief Turbine cell (proton or neutron)
 */
struct TurbineCell {
    std::array<std::size_t, 3> position;  // Grid indices
    double radius_cells;  // Radius in grid cells
    double kappa;  // Curvature (m⁻¹)
    double Gamma;  // Circulation factor
    double eta;  // Slip
    std::string cell_type;  // "proton" or "neutron"
};

/**
 * @brief Proton turbine
 */
struct ProtonTurbine : TurbineCell {
    ProtonTurbine(
        const std::array<std::size_t, 3>& position,
        double radius_cells,
        bool bound = true
    );
};

/**
 * @brief Neutron turbine
 */
struct NeutronTurbine : TurbineCell {
    NeutronTurbine(
        const std::array<std::size_t, 3>& position,
        double radius_cells,
        bool bound = true
    );
};

/**
 * @brief Deuteron system (p-n)
 */
class DeuteronSystem {
public:
    DeuteronSystem(
        FieldSystem& fields,
        const std::array<std::size_t, 3>& center,
        double separation_cells
    );

    double compute_binding_energy() const;  // J
    double compute_binding_energy_mev() const;  // MeV

    const ProtonTurbine& proton() const { return proton_; }
    const NeutronTurbine& neutron() const { return neutron_; }

private:
    FieldSystem& fields_;
    ProtonTurbine proton_;
    NeutronTurbine neutron_;
};

/**
 * @brief Triton system (n-p-n)
 */
class TritonSystem {
public:
    TritonSystem(
        FieldSystem& fields,
        const std::array<std::size_t, 3>& center,
        double separation_cells
    );

private:
    FieldSystem& fields_;
    NeutronTurbine neutron1_;
    ProtonTurbine proton_;
    NeutronTurbine neutron2_;
};

/**
 * @brief Helion system (p-n-p)
 */
class HelionSystem {
public:
    HelionSystem(
        FieldSystem& fields,
        const std::array<std::size_t, 3>& center,
        double separation_cells
    );

private:
    FieldSystem& fields_;
    ProtonTurbine proton1_;
    NeutronTurbine neutron_;
    ProtonTurbine proton2_;
};

/**
 * @brief Alpha system (2p-2n tetrahedral)
 */
class AlphaSystem {
public:
    AlphaSystem(
        FieldSystem& fields,
        const std::array<std::size_t, 3>& center,
        double separation_cells
    );

private:
    FieldSystem& fields_;
    ProtonTurbine proton1_;
    ProtonTurbine proton2_;
    NeutronTurbine neutron1_;
    NeutronTurbine neutron2_;
};

}  // namespace sdt_navier

