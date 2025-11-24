#pragma once

#include "pressure_field.hpp"
#include "elements.hpp"
#include <string>
#include <optional>

namespace sdt::chemistry {

    /**
     * Bond type enumeration
     */
    enum class BondType {
        IONIC,      // Ionic bond (electron transfer)
        COVALENT,   // Covalent bond (shared electrons)
        METALLIC,   // Metallic bond (delocalized electrons)
        COORDINATION, // Coordination bond (ligand-metal)
        HYDROGEN,   // Hydrogen bond
        VAN_DER_WAALS, // Van der Waals interaction
        DIPOLE_DIPOLE, // Dipole-dipole interaction
        ION_DIPOLE   // Ion-dipole interaction
    };
    
    /**
     * Bond data structure
     */
    struct Bond {
        int atom1_index;  // Index of first atom
        int atom2_index;  // Index of second atom
        BondType type;    // Bond type
        int bond_order;    // Bond order (1=single, 2=double, 3=triple)
        double length_pm;  // Bond length (pm)
        double energy_kJ_per_mol;  // Bond energy (kJ/mol)
        std::optional<double> angle_deg;  // Bond angle (degrees) if part of angle
        
        // SDT-specific
        double occlusion_radius1_m;  // Effective occlusion radius of atom 1 (m)
        double occlusion_radius2_m;  // Effective occlusion radius of atom 2 (m)
    };
    
    /**
     * Bond calculator using SDT pressure field mechanics
     */
    class Bonds {
    public:
        /**
         * Calculate covalent bond length from pressure field balance
         * 
         * From Phase Chemistry Covalent: r_bond determined by pressure equilibrium
         */
        static double covalent_bond_length(
            const ElementData& elem1,
            const ElementData& elem2,
            int bond_order = 1
        );
        
        /**
         * Calculate covalent bond energy
         */
        static double covalent_bond_energy(
            const ElementData& elem1,
            const ElementData& elem2,
            double bond_length_pm,
            int bond_order = 1
        );
        
        /**
         * Calculate ionic bond length
         * 
         * From Phase Chemistry Ionic: r_ionic = r_cation + r_anion
         */
        static double ionic_bond_length(
            const ElementData& cation,
            const ElementData& anion,
            int cation_charge = 1,
            int anion_charge = -1
        );
        
        /**
         * Calculate lattice energy for ionic compound
         * 
         * From Phase Chemistry Ionic: E_lattice from Born-Haber cycle
         */
        static double lattice_energy(
            const ElementData& cation,
            const ElementData& anion,
            double bond_length_pm,
            int cation_charge = 1,
            int anion_charge = -1
        );
        
        /**
         * Calculate hydrogen bond length
         * 
         * From Phase Chemistry Intermolecular: r_HB from extended occlusion
         */
        static double hydrogen_bond_length(
            const ElementData& donor,
            const ElementData& acceptor
        );
        
        /**
         * Calculate hydrogen bond energy
         */
        static double hydrogen_bond_energy(
            const ElementData& donor,
            const ElementData& acceptor,
            double bond_length_pm
        );
        
        /**
         * Calculate bond order from bond length
         * 
         * Shorter bonds typically have higher bond order
         */
        static int estimate_bond_order(
            const ElementData& elem1,
            const ElementData& elem2,
            double bond_length_pm
        );
        
        /**
         * Calculate bond length correction for multiple bonds
         * 
         * Multiple bonds are shorter due to increased occlusion
         */
        static double bond_length_correction(int bond_order);
        
    private:
        // Bond length parameters (from experimental data)
        static double get_covalent_radius_sum(const ElementData& elem1, const ElementData& elem2);
        static double get_ionic_radius_sum(const ElementData& cation, const ElementData& anion);
    };

} // namespace sdt::chemistry

