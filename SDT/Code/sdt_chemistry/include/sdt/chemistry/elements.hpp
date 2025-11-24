#pragma once

#include "constants.hpp"
#include <string>
#include <vector>
#include <unordered_map>
#include <optional>

namespace sdt::chemistry {

    /**
     * Element data structure
     */
    struct ElementData {
        int Z;  // Atomic number
        std::string symbol;
        std::string name;
        double atomic_mass;  // u (atomic mass units)
        double atomic_radius_pm;  // pm (picometers)
        double covalent_radius_pm;  // pm
        double ionic_radius_pm;  // pm (for common ion)
        double ionization_energy_eV;  // First ionization energy (eV)
        double electron_affinity_eV;  // Electron affinity (eV)
        double electronegativity;  // Pauling scale
        int valence_electrons;  // Number of valence electrons
        std::vector<int> electron_config;  // Electron configuration [n, l, ...]
        double nuclear_radius_fm;  // fm (femtometers) = r_0 * A^(1/3)
        
        // SDT-specific parameters
        double effective_occlusion_radius_m;  // m (effective radius for pressure field)
        double effective_nuclear_charge;  // Z_eff (accounting for shielding)
    };
    
    /**
     * Element database and accessor
     */
    class Elements {
    public:
        /**
         * Get element data by symbol
         */
        static const ElementData& get_element(const std::string& symbol);
        
        /**
         * Get element data by atomic number
         */
        static const ElementData& get_element(int Z);
        
        /**
         * Check if element exists
         */
        static bool exists(const std::string& symbol);
        static bool exists(int Z);
        
        /**
         * Get all element symbols
         */
        static std::vector<std::string> all_symbols();
        
        /**
         * Calculate effective nuclear charge
         * Z_eff = Z - σ (shielding constant)
         */
        static double effective_nuclear_charge(int Z, int n, int l);
        
        /**
         * Calculate atomic radius from SDT
         * r_atom ∝ n² / Z_eff * a_0
         */
        static double atomic_radius_sdt(int Z, int n);
        
        /**
         * Calculate ionization energy from SDT
         * I_1 ∝ Z_eff² / n²
         */
        static double ionization_energy_sdt(int Z, int n);
        
        /**
         * Calculate nuclear radius
         * R_nuc = r_0 * A^(1/3) where r_0 = 1.2 fm
         */
        static double nuclear_radius(int A);
        
    private:
        static void initialize_database();
        static std::unordered_map<std::string, ElementData> element_map_;
        static std::unordered_map<int, ElementData*> element_by_Z_;
        static bool initialized_;
    };

} // namespace sdt::chemistry

