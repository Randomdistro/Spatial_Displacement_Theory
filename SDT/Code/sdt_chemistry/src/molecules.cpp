#include "sdt/chemistry/molecules.hpp"
#include <stdexcept>
#include <sstream>
#include <algorithm>
#include <cmath>

namespace sdt::chemistry {

    Molecule::Molecule() : name_("Unnamed") {
    }

    Molecule::Molecule(const std::string& name) : name_(name) {
    }

    size_t Molecule::add_atom(int element_Z, const Vec3d& position) {
        if (!Elements::exists(element_Z)) {
            throw std::runtime_error("Invalid element Z: " + std::to_string(element_Z));
        }
        
        const ElementData& elem = Elements::get_element(element_Z);
        
        Atom atom;
        atom.element_Z = element_Z;
        atom.position = position;
        atom.charge = 0;
        atom.spin_multiplicity = 1;
        atom.effective_radius_m = elem.effective_occlusion_radius_m;
        
        atoms_.push_back(atom);
        return atoms_.size() - 1;
    }

    void Molecule::remove_atom(size_t index) {
        if (index >= atoms_.size()) {
            throw std::runtime_error("Atom index out of range");
        }
        
        // Remove all bonds involving this atom
        bonds_.erase(
            std::remove_if(bonds_.begin(), bonds_.end(),
                [index](const Bond& b) {
                    return b.atom1_index == index || b.atom2_index == index;
                }),
            bonds_.end()
        );
        
        // Remove atom
        atoms_.erase(atoms_.begin() + index);
        
        // Update bond indices
        for (auto& bond : bonds_) {
            if (bond.atom1_index > index) {
                bond.atom1_index--;
            }
            if (bond.atom2_index > index) {
                bond.atom2_index--;
            }
        }
        
        update_connectivity();
    }

    void Molecule::set_atom_position(size_t index, const Vec3d& position) {
        if (index >= atoms_.size()) {
            throw std::runtime_error("Atom index out of range");
        }
        atoms_[index].position = position;
    }

    size_t Molecule::add_bond(size_t atom1_index, size_t atom2_index, BondType type, int bond_order) {
        if (atom1_index >= atoms_.size() || atom2_index >= atoms_.size()) {
            throw std::runtime_error("Atom index out of range");
        }
        if (atom1_index == atom2_index) {
            throw std::runtime_error("Cannot bond atom to itself");
        }
        
        // Check if bond already exists
        if (are_bonded(atom1_index, atom2_index)) {
            throw std::runtime_error("Bond already exists");
        }
        
        Bond bond;
        bond.atom1_index = atom1_index;
        bond.atom2_index = atom2_index;
        bond.type = type;
        bond.bond_order = bond_order;
        
        // Calculate bond length and energy
        const ElementData& elem1 = atoms_[atom1_index].element_data();
        const ElementData& elem2 = atoms_[atom2_index].element_data();
        
        Vec3d r_vec = atoms_[atom2_index].position - atoms_[atom1_index].position;
        double r_m = r_vec.norm();
        bond.length_pm = r_m * constants::m_to_pm;
        
        // Calculate bond energy based on type
        switch (type) {
            case BondType::COVALENT:
                bond.length_pm = Bonds::covalent_bond_length(elem1, elem2, bond_order);
                bond.energy_kJ_per_mol = Bonds::covalent_bond_energy(elem1, elem2, bond.length_pm, bond_order);
                break;
            case BondType::IONIC:
                bond.length_pm = Bonds::ionic_bond_length(elem1, elem2);
                bond.energy_kJ_per_mol = Bonds::lattice_energy(elem1, elem2, bond.length_pm);
                break;
            case BondType::HYDROGEN:
                bond.length_pm = Bonds::hydrogen_bond_length(elem1, elem2);
                bond.energy_kJ_per_mol = Bonds::hydrogen_bond_energy(elem1, elem2, bond.length_pm);
                break;
            default:
                bond.energy_kJ_per_mol = 0.0;
                break;
        }
        
        bond.occlusion_radius1_m = atoms_[atom1_index].effective_radius_m;
        bond.occlusion_radius2_m = atoms_[atom2_index].effective_radius_m;
        
        bonds_.push_back(bond);
        update_connectivity();
        
        return bonds_.size() - 1;
    }

    void Molecule::remove_bond(size_t index) {
        if (index >= bonds_.size()) {
            throw std::runtime_error("Bond index out of range");
        }
        bonds_.erase(bonds_.begin() + index);
        update_connectivity();
    }

    void Molecule::update_bond_length(size_t bond_index, double length_pm) {
        if (bond_index >= bonds_.size()) {
            throw std::runtime_error("Bond index out of range");
        }
        
        Bond& bond = bonds_[bond_index];
        bond.length_pm = length_pm;
        
        // Update atom positions to match bond length
        Vec3d r_vec = atoms_[bond.atom2_index].position - atoms_[bond.atom1_index].position;
        double r_current = r_vec.norm();
        if (r_current > 0.0) {
            double r_new = length_pm * constants::pm_to_m;
            Vec3d direction = r_vec.normalized();
            atoms_[bond.atom2_index].position = atoms_[bond.atom1_index].position + direction * r_new;
        }
        
        // Recalculate bond energy
        const ElementData& elem1 = atoms_[bond.atom1_index].element_data();
        const ElementData& elem2 = atoms_[bond.atom2_index].element_data();
        
        switch (bond.type) {
            case BondType::COVALENT:
                bond.energy_kJ_per_mol = Bonds::covalent_bond_energy(elem1, elem2, length_pm, bond.bond_order);
                break;
            case BondType::IONIC:
                bond.energy_kJ_per_mol = Bonds::lattice_energy(elem1, elem2, length_pm);
                break;
            case BondType::HYDROGEN:
                bond.energy_kJ_per_mol = Bonds::hydrogen_bond_energy(elem1, elem2, length_pm);
                break;
            default:
                break;
        }
    }

    Vec3d Molecule::center_of_mass() const {
        Vec3d com = Vec3d::Zero();
        double total_mass = 0.0;
        
        for (const auto& atom : atoms_) {
            const ElementData& elem = atom.element_data();
            double mass = elem.atomic_mass;
            com += mass * atom.position;
            total_mass += mass;
        }
        
        if (total_mass > 0.0) {
            com /= total_mass;
        }
        return com;
    }

    double Molecule::total_energy() const {
        return calculate_pressure_field_energy();
    }

    double Molecule::bond_energy() const {
        double E_total = 0.0;
        for (const auto& bond : bonds_) {
            E_total += bond.energy_kJ_per_mol;
        }
        return E_total;
    }

    std::vector<size_t> Molecule::neighbors(size_t atom_index) const {
        std::vector<size_t> neighbors;
        
        auto it = connectivity_.find(atom_index);
        if (it != connectivity_.end()) {
            for (size_t bond_idx : it->second) {
                const Bond& bond = bonds_[bond_idx];
                if (bond.atom1_index == atom_index) {
                    neighbors.push_back(bond.atom2_index);
                } else {
                    neighbors.push_back(bond.atom1_index);
                }
            }
        }
        
        return neighbors;
    }

    bool Molecule::are_bonded(size_t atom1_index, size_t atom2_index) const {
        return find_bond(atom1_index, atom2_index).has_value();
    }

    std::optional<size_t> Molecule::find_bond(size_t atom1_index, size_t atom2_index) const {
        for (size_t i = 0; i < bonds_.size(); ++i) {
            const Bond& bond = bonds_[i];
            if ((bond.atom1_index == atom1_index && bond.atom2_index == atom2_index) ||
                (bond.atom1_index == atom2_index && bond.atom2_index == atom1_index)) {
                return i;
            }
        }
        return std::nullopt;
    }

    bool Molecule::is_valid() const {
        return validate().empty();
    }

    std::vector<std::string> Molecule::validate() const {
        std::vector<std::string> errors;
        
        // Check atom indices in bonds
        for (size_t i = 0; i < bonds_.size(); ++i) {
            const Bond& bond = bonds_[i];
            if (bond.atom1_index >= atoms_.size()) {
                errors.push_back("Bond " + std::to_string(i) + ": atom1_index out of range");
            }
            if (bond.atom2_index >= atoms_.size()) {
                errors.push_back("Bond " + std::to_string(i) + ": atom2_index out of range");
            }
            if (bond.atom1_index == bond.atom2_index) {
                errors.push_back("Bond " + std::to_string(i) + ": atom bonded to itself");
            }
        }
        
        return errors;
    }

    std::string Molecule::to_smiles() const {
        // Simplified SMILES conversion (basic implementation)
        std::ostringstream oss;
        // TODO: Implement full SMILES conversion
        oss << "C";  // Placeholder
        return oss.str();
    }

    void Molecule::from_smiles(const std::string& smiles) {
        // Simplified SMILES parsing (basic implementation)
        // TODO: Implement full SMILES parsing
        throw std::runtime_error("SMILES parsing not yet implemented");
    }

    std::string Molecule::to_json() const {
        std::ostringstream oss;
        oss << "{\n";
        oss << "  \"name\": \"" << name_ << "\",\n";
        oss << "  \"atoms\": [\n";
        for (size_t i = 0; i < atoms_.size(); ++i) {
            const Atom& atom = atoms_[i];
            oss << "    {\"index\": " << i << ", \"Z\": " << atom.element_Z
                << ", \"position\": [" << atom.position.x() << ", " 
                << atom.position.y() << ", " << atom.position.z() << "]},\n";
        }
        oss << "  ],\n";
        oss << "  \"bonds\": [\n";
        for (size_t i = 0; i < bonds_.size(); ++i) {
            const Bond& bond = bonds_[i];
            oss << "    {\"index\": " << i << ", \"atom1\": " << bond.atom1_index
                << ", \"atom2\": " << bond.atom2_index 
                << ", \"length_pm\": " << bond.length_pm << "},\n";
        }
        oss << "  ]\n";
        oss << "}";
        return oss.str();
    }

    void Molecule::update_connectivity() {
        connectivity_.clear();
        for (size_t i = 0; i < bonds_.size(); ++i) {
            const Bond& bond = bonds_[i];
            connectivity_[bond.atom1_index].push_back(i);
            connectivity_[bond.atom2_index].push_back(i);
        }
    }

    double Molecule::calculate_pressure_field_energy() const {
        double E_total = 0.0;
        
        // Bond energies
        E_total += bond_energy();
        
        // Non-bonded interactions (simplified)
        for (size_t i = 0; i < atoms_.size(); ++i) {
            for (size_t j = i + 1; j < atoms_.size(); ++j) {
                if (!are_bonded(i, j)) {
                    // Van der Waals interaction
                    Vec3d r_vec = atoms_[j].position - atoms_[i].position;
                    double r = r_vec.norm();
                    if (r > 0.0) {
                        double R1 = atoms_[i].effective_radius_m;
                        double R2 = atoms_[j].effective_radius_m;
                        // Simplified van der Waals energy
                        double E_vdw = PressureField::bond_energy_kJ_per_mol(R1, R2, r) * 0.1;  // Much weaker
                        E_total += E_vdw;
                    }
                }
            }
        }
        
        return E_total;
    }

} // namespace sdt::chemistry

