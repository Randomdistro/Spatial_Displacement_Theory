#include "sdt/chemistry/properties.hpp"
#include <cmath>
#include <algorithm>

namespace sdt::chemistry {

    double Properties::binding_energy(const Molecule& molecule) {
        return molecule.bond_energy();
    }

    double Properties::formation_enthalpy(const Molecule& molecule) {
        // Formation enthalpy = total energy - sum of atomic energies
        double E_total = molecule.total_energy();
        
        double E_atoms = 0.0;
        for (size_t i = 0; i < molecule.num_atoms(); ++i) {
            const ElementData& elem = molecule.atom(i).element_data();
            // Simplified: use ionization energy as reference
            E_atoms += elem.ionization_energy_eV * constants::eV_to_J * constants::N_A / 1000.0;  // kJ/mol
        }
        
        return E_total - E_atoms;
    }

    double Properties::stability(const Molecule& molecule) {
        // Stability = negative of formation enthalpy (more negative = more stable)
        return -formation_enthalpy(molecule);
    }

    double Properties::reactivity_index(const Molecule& molecule) {
        // Lower HOMO-LUMO gap = more reactive
        double gap = homo_lumo_gap(molecule);
        return 1.0 / (gap + 0.1);  // Avoid division by zero
    }

    double Properties::homo_lumo_gap(const Molecule& molecule) {
        // Simplified: estimate from bond energies
        // Stronger bonds = larger gap
        double avg_bond_energy = 0.0;
        if (molecule.num_bonds() > 0) {
            avg_bond_energy = molecule.bond_energy() / molecule.num_bonds();
        }
        
        // Convert to eV (rough estimate)
        double gap_eV = avg_bond_energy / (constants::N_A * constants::eV_to_J * 1000.0);
        return std::max(0.1, gap_eV);  // Minimum gap
    }

    double Properties::dipole_moment(const Molecule& molecule) {
        // Calculate from charge distribution
        Vec3d dipole = Vec3d::Zero();
        Vec3d com = molecule.center_of_mass();
        
        for (size_t i = 0; i < molecule.num_atoms(); ++i) {
            const Atom& atom = molecule.atom(i);
            const ElementData& elem = atom.element_data();
            
            // Simplified: use formal charge
            double charge = static_cast<double>(atom.charge) * constants::e_charge;
            Vec3d r = atom.position - com;
            dipole += charge * r;
        }
        
        // Convert to Debye (1 D = 3.336e-30 C·m)
        double dipole_moment_D = dipole.norm() / 3.336e-30;
        return dipole_moment_D;
    }

    double Properties::molecular_volume(const Molecule& molecule) {
        double volume_m3 = calculate_volume_from_atoms(molecule);
        double volume_A3 = volume_m3 * 1e30;  // Convert to Å³
        return volume_A3;
    }

    double Properties::surface_area(const Molecule& molecule) {
        double area_m2 = calculate_surface_from_atoms(molecule);
        double area_A2 = area_m2 * 1e20;  // Convert to Å²
        return area_A2;
    }

    double Properties::melting_point(const Molecule& molecule) {
        // Empirical: higher molecular weight and stronger bonds = higher melting point
        double total_mass = 0.0;
        for (size_t i = 0; i < molecule.num_atoms(); ++i) {
            total_mass += molecule.atom(i).element_data().atomic_mass;
        }
        
        double avg_bond_energy = molecule.bond_energy() / std::max(1.0, static_cast<double>(molecule.num_bonds()));
        
        // Empirical formula (simplified)
        double T_melt = 100.0 + total_mass * 10.0 + avg_bond_energy * 0.1;
        return std::max(50.0, std::min(2000.0, T_melt));  // Reasonable range
    }

    double Properties::boiling_point(const Molecule& molecule) {
        // Boiling point typically 1.2-1.5x melting point
        double T_melt = melting_point(molecule);
        return T_melt * 1.3;
    }

    double Properties::solubility_water(const Molecule& molecule) {
        // Simplified: based on polarity and size
        double dipole = dipole_moment(molecule);
        double volume = molecular_volume(molecule);
        
        // More polar and smaller = more soluble
        double solubility = dipole * 10.0 / (volume + 1.0);
        return std::max(0.0, std::min(1000.0, solubility));  // g/L
    }

    double Properties::total_energy(const Molecule& molecule) {
        return molecule.total_energy();
    }

    double Properties::bond_dissociation_energy(
        const Molecule& molecule,
        size_t bond_index
    ) {
        if (bond_index >= molecule.num_bonds()) {
            return 0.0;
        }
        
        const Bond& bond = molecule.bond(bond_index);
        return bond.energy_kJ_per_mol;
    }

    double Properties::activation_energy(
        const Molecule& reactant,
        const Molecule& product
    ) {
        // Simplified: activation energy ≈ 10% of bond energy difference
        double E_reactant = reactant.total_energy();
        double E_product = product.total_energy();
        double delta_E = std::abs(E_product - E_reactant);
        
        return delta_E * 0.1;
    }

    double Properties::free_energy_change(
        const Molecule& molecule,
        double temperature_K
    ) {
        double H = formation_enthalpy(molecule);
        double S = entropy(molecule);
        double T = temperature_K;
        
        // G = H - T*S
        double G = H - (T * S / 1000.0);  // Convert S to kJ/(mol·K)
        return G;
    }

    double Properties::entropy(const Molecule& molecule) {
        // Simplified: entropy based on molecular complexity
        // More atoms and bonds = higher entropy
        double S = 50.0;  // Base entropy (J/(mol·K))
        S += molecule.num_atoms() * 10.0;
        S += molecule.num_bonds() * 5.0;
        
        return S;
    }

    double Properties::calculate_volume_from_atoms(const Molecule& molecule) {
        // Approximate volume as sum of atomic volumes
        double volume = 0.0;
        
        for (size_t i = 0; i < molecule.num_atoms(); ++i) {
            const Atom& atom = molecule.atom(i);
            double r = atom.effective_radius_m;
            // Volume of sphere
            volume += (4.0 / 3.0) * constants::pi * r * r * r;
        }
        
        return volume;
    }

    double Properties::calculate_surface_from_atoms(const Molecule& molecule) {
        // Approximate surface as sum of atomic surfaces
        double surface = 0.0;
        
        for (size_t i = 0; i < molecule.num_atoms(); ++i) {
            const Atom& atom = molecule.atom(i);
            double r = atom.effective_radius_m;
            // Surface area of sphere
            surface += 4.0 * constants::pi * r * r;
        }
        
        return surface;
    }

} // namespace sdt::chemistry

