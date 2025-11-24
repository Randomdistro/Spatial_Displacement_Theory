#pragma once

#include "elements.hpp"
#include "bonds.hpp"
#include "pressure_field.hpp"
#include <Eigen/Dense>
#include <vector>
#include <string>
#include <unordered_map>
#include <optional>

namespace sdt::chemistry {

    using Vec3d = Eigen::Vector3d;

    /**
     * Atom in a molecule
     */
    struct Atom {
        int element_Z;  // Atomic number
        Vec3d position;  // Position (m)
        int charge;  // Formal charge
        int spin_multiplicity;  // Spin multiplicity (2S+1)
        
        // SDT-specific
        double effective_radius_m;  // Effective occlusion radius (m)
        
        const ElementData& element_data() const {
            return Elements::get_element(element_Z);
        }
    };
    
    /**
     * Molecular structure (graph-based)
     */
    class Molecule {
    public:
        Molecule();
        explicit Molecule(const std::string& name);
        
        // Accessors
        const std::string& name() const { return name_; }
        size_t num_atoms() const { return atoms_.size(); }
        size_t num_bonds() const { return bonds_.size(); }
        
        const Atom& atom(size_t index) const { return atoms_[index]; }
        Atom& atom(size_t index) { return atoms_[index]; }
        
        const Bond& bond(size_t index) const { return bonds_[index]; }
        Bond& bond(size_t index) { return bonds_[index]; }
        
        // Atom manipulation
        size_t add_atom(int element_Z, const Vec3d& position = Vec3d::Zero());
        void remove_atom(size_t index);
        void set_atom_position(size_t index, const Vec3d& position);
        
        // Bond manipulation
        size_t add_bond(size_t atom1_index, size_t atom2_index, BondType type, int bond_order = 1);
        void remove_bond(size_t index);
        void update_bond_length(size_t bond_index, double length_pm);
        
        // Geometry
        Vec3d center_of_mass() const;
        double total_energy() const;  // Total pressure field energy
        double bond_energy() const;  // Sum of all bond energies
        
        // Connectivity
        std::vector<size_t> neighbors(size_t atom_index) const;
        bool are_bonded(size_t atom1_index, size_t atom2_index) const;
        std::optional<size_t> find_bond(size_t atom1_index, size_t atom2_index) const;
        
        // Validation
        bool is_valid() const;
        std::vector<std::string> validate() const;
        
        // I/O
        std::string to_smiles() const;  // Convert to SMILES notation (simplified)
        void from_smiles(const std::string& smiles);  // Parse SMILES (simplified)
        std::string to_json() const;
        
    private:
        std::string name_;
        std::vector<Atom> atoms_;
        std::vector<Bond> bonds_;
        
        // Connectivity map: atom_index -> list of bond indices
        std::unordered_map<size_t, std::vector<size_t>> connectivity_;
        
        void update_connectivity();
        double calculate_pressure_field_energy() const;
    };

} // namespace sdt::chemistry

