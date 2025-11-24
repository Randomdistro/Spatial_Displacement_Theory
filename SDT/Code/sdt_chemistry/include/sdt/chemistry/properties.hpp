#pragma once

#include "molecules.hpp"
#include "master_equation.hpp"
#include <optional>
#include <vector>

namespace sdt::chemistry {

    /**
     * Molecular property calculator
     */
    class Properties {
    public:
        /**
         * Calculate binding energy (kJ/mol)
         */
        static double binding_energy(const Molecule& molecule);
        
        /**
         * Calculate formation enthalpy (kJ/mol)
         */
        static double formation_enthalpy(const Molecule& molecule);
        
        /**
         * Calculate stability (relative to separated atoms)
         */
        static double stability(const Molecule& molecule);
        
        /**
         * Calculate reactivity index (lower = more reactive)
         */
        static double reactivity_index(const Molecule& molecule);
        
        /**
         * Calculate HOMO-LUMO gap (eV) - simplified
         */
        static double homo_lumo_gap(const Molecule& molecule);
        
        /**
         * Calculate dipole moment (Debye)
         */
        static double dipole_moment(const Molecule& molecule);
        
        /**
         * Calculate molecular volume (Å³)
         */
        static double molecular_volume(const Molecule& molecule);
        
        /**
         * Calculate surface area (Å²)
         */
        static double surface_area(const Molecule& molecule);
        
        /**
         * Predict melting point (K) - empirical
         */
        static double melting_point(const Molecule& molecule);
        
        /**
         * Predict boiling point (K) - empirical
         */
        static double boiling_point(const Molecule& molecule);
        
        /**
         * Predict solubility in water (g/L) - empirical
         */
        static double solubility_water(const Molecule& molecule);
        
        /**
         * Calculate total pressure field energy (kJ/mol)
         */
        static double total_energy(const Molecule& molecule);
        
        /**
         * Calculate bond dissociation energy for a specific bond (kJ/mol)
         */
        static double bond_dissociation_energy(
            const Molecule& molecule,
            size_t bond_index
        );
        
        /**
         * Calculate activation energy for a reaction (kJ/mol)
         * Simplified model based on bond energies
         */
        static double activation_energy(
            const Molecule& reactant,
            const Molecule& product
        );
        
        /**
         * Calculate thermodynamic stability
         * Returns free energy change (kJ/mol)
         */
        static double free_energy_change(
            const Molecule& molecule,
            double temperature_K = 298.15
        );
        
        /**
         * Calculate entropy (J/(mol·K))
         */
        static double entropy(const Molecule& molecule);
        
    private:
        static double calculate_volume_from_atoms(const Molecule& molecule);
        static double calculate_surface_from_atoms(const Molecule& molecule);
    };

} // namespace sdt::chemistry

