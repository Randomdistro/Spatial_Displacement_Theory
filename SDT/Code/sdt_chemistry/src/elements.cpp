#include "sdt/chemistry/elements.hpp"
#include "sdt/chemistry/constants.hpp"
#include <stdexcept>
#include <cmath>
#include <cctype>

namespace sdt::chemistry {

    std::unordered_map<std::string, ElementData> Elements::element_map_;
    std::unordered_map<int, ElementData*> Elements::element_by_Z_;
    bool Elements::initialized_ = false;

    void Elements::initialize_database() {
        if (initialized_) {
            return;
        }
        
        // Initialize first 20 elements with key properties
        // Data from experimental values and SDT calculations
        
        auto add_element = [](const ElementData& elem) {
            element_map_[elem.symbol] = elem;
            element_by_Z_[elem.Z] = const_cast<ElementData*>(&element_map_[elem.symbol]);
        };
        
        // H
        add_element({
            1, "H", "Hydrogen", 1.007825,
            53.0, 31.0, 154.0,  // atomic, covalent, ionic radii (pm)
            13.59843, 0.754, 2.20,  // ionization, affinity, electronegativity
            1, {1, 0},  // valence, electron config
            0.84,  // nuclear radius (fm) for 1H
            1.0e-21,  // effective occlusion radius (m) from Phase 1
            1.0  // Z_eff
        });
        
        // He
        add_element({
            2, "He", "Helium", 4.002602,
            31.0, 28.0, 93.0,
            24.58741, -0.5, 0.0,
            2, {1, 0, 1, 0},
            1.7,
            1.5e-21,
            1.7
        });
        
        // Li
        add_element({
            3, "Li", "Lithium", 7.016004,
            152.0, 128.0, 76.0,
            5.39172, 0.618, 0.98,
            1, {1, 0, 1, 0, 2, 0},
            2.3,
            8.0e-11,
            1.3
        });
        
        // Be
        add_element({
            4, "Be", "Beryllium", 9.012182,
            112.0, 96.0, 45.0,
            9.32270, -0.5, 1.57,
            2, {1, 0, 1, 0, 2, 0, 2, 0},
            2.4,
            7.0e-11,
            1.9
        });
        
        // B
        add_element({
            5, "B", "Boron", 11.009305,
            85.0, 84.0, 27.0,
            8.29803, 0.277, 2.04,
            3, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1},
            2.5,
            6.5e-11,
            2.4
        });
        
        // C
        add_element({
            6, "C", "Carbon", 12.0,
            77.0, 76.0, 16.0,
            11.26030, 1.262, 2.55,
            4, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1},
            2.6,
            6.0e-11,
            3.1
        });
        
        // N
        add_element({
            7, "N", "Nitrogen", 14.003074,
            75.0, 71.0, 146.0,
            14.53414, -0.07, 3.04,
            5, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1},
            2.7,
            5.8e-11,
            3.8
        });
        
        // O
        add_element({
            8, "O", "Oxygen", 15.994915,
            73.0, 66.0, 140.0,
            13.61806, 1.461, 3.44,
            6, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1},
            2.8,
            5.6e-11,
            4.5
        });
        
        // F
        add_element({
            9, "F", "Fluorine", 18.998403,
            72.0, 57.0, 133.0,
            17.42282, 3.401, 3.98,
            7, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1},
            2.9,
            5.4e-11,
            5.2
        });
        
        // Ne
        add_element({
            10, "Ne", "Neon", 20.1797,
            71.0, 58.0, 112.0,
            21.56454, -0.5, 0.0,
            8, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1},
            3.0,
            5.2e-11,
            6.0
        });
        
        // Na
        add_element({
            11, "Na", "Sodium", 22.989769,
            186.0, 166.0, 102.0,
            5.13908, 0.548, 0.93,
            1, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0},
            3.1,
            1.2e-10,
            1.0
        });
        
        // Mg
        add_element({
            12, "Mg", "Magnesium", 24.305,
            160.0, 141.0, 72.0,
            7.64624, -0.4, 1.31,
            2, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0},
            3.2,
            1.1e-10,
            1.3
        });
        
        // Al
        add_element({
            13, "Al", "Aluminum", 26.981538,
            143.0, 121.0, 53.5,
            5.98577, 0.441, 1.61,
            3, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1},
            3.3,
            1.0e-10,
            2.6
        });
        
        // Si
        add_element({
            14, "Si", "Silicon", 28.085,
            118.0, 111.0, 40.0,
            8.15169, 1.385, 1.90,
            4, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1},
            3.4,
            9.5e-11,
            3.3
        });
        
        // P
        add_element({
            15, "P", "Phosphorus", 30.973762,
            110.0, 107.0, 44.0,
            10.48669, 0.746, 2.19,
            5, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1},
            3.5,
            9.0e-11,
            4.1
        });
        
        // S
        add_element({
            16, "S", "Sulfur", 32.065,
            103.0, 105.0, 184.0,
            10.36001, 2.077, 2.58,
            6, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1, 3, 1},
            3.6,
            8.5e-11,
            4.9
        });
        
        // Cl
        add_element({
            17, "Cl", "Chlorine", 35.453,
            99.0, 102.0, 181.0,
            12.96764, 3.617, 3.16,
            7, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1},
            3.7,
            8.0e-11,
            5.7
        });
        
        // Ar
        add_element({
            18, "Ar", "Argon", 39.948,
            97.0, 106.0, 154.0,
            15.75962, -0.5, 0.0,
            8, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1},
            3.8,
            7.5e-11,
            6.6
        });
        
        // K
        add_element({
            19, "K", "Potassium", 39.0983,
            227.0, 203.0, 138.0,
            4.34066, 0.501, 0.82,
            1, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 4, 0},
            3.9,
            1.5e-10,
            1.0
        });
        
        // Ca
        add_element({
            20, "Ca", "Calcium", 40.078,
            197.0, 176.0, 100.0,
            6.11316, 0.024, 1.00,
            2, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 4, 0, 4, 0},
            4.0,
            1.4e-10,
            1.3
        });

        // Sc
        add_element({
            21, "Sc", "Scandium", 44.955908,
            162.0, 144.0, 75.0,
            6.5615, 0.188, 1.36,
            3, {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 4, 0, 4, 0, 3, 2},
            3.5,
            1.3e-10,
            3.0
        });
        
        initialized_ = true;
    }

    const ElementData& Elements::get_element(const std::string& symbol) {
        initialize_database();
        
        std::string sym = symbol;
        if (sym.length() > 0) {
            sym[0] = std::toupper(sym[0]);
            if (sym.length() > 1) {
                sym[1] = std::tolower(sym[1]);
            }
        }
        
        auto it = element_map_.find(sym);
        if (it == element_map_.end()) {
            throw std::runtime_error("Element not found: " + symbol);
        }
        return it->second;
    }

    const ElementData& Elements::get_element(int Z) {
        initialize_database();
        
        auto it = element_by_Z_.find(Z);
        if (it == element_by_Z_.end()) {
            throw std::runtime_error("Element not found: Z=" + std::to_string(Z));
        }
        return *(it->second);
    }

    bool Elements::exists(const std::string& symbol) {
        try {
            get_element(symbol);
            return true;
        } catch (...) {
            return false;
        }
    }

    bool Elements::exists(int Z) {
        try {
            get_element(Z);
            return true;
        } catch (...) {
            return false;
        }
    }

    std::vector<std::string> Elements::all_symbols() {
        initialize_database();
        
        std::vector<std::string> symbols;
        symbols.reserve(element_map_.size());
        for (const auto& pair : element_map_) {
            symbols.push_back(pair.first);
        }
        return symbols;
    }

    double Elements::effective_nuclear_charge(int Z, int n, int l) {
        // Slater's rules approximation
        double sigma = 0.0;
        
        // Core electrons: full shielding
        if (n > 1) {
            sigma += 2.0;  // 1s
        }
        if (n > 2) {
            sigma += 8.0;  // 2s2p
        }
        if (n > 3) {
            sigma += 8.0;  // 3s3p
        }
        
        // Same shell electrons: 0.35 per electron (except 1s: 0.30)
        // Simplified: use average shielding
        int valence_electrons = Z - static_cast<int>(sigma);
        if (n == 1) {
            sigma += 0.30 * (valence_electrons - 1);
        } else {
            sigma += 0.35 * (valence_electrons - 1);
        }
        
        return Z - sigma;
    }

    double Elements::atomic_radius_sdt(int Z, int n) {
        double Z_eff = effective_nuclear_charge(Z, n, 0);
        return (n * n / Z_eff) * constants::a_0;
    }

    double Elements::ionization_energy_sdt(int Z, int n) {
        double Z_eff = effective_nuclear_charge(Z, n, 0);
        // I_1 ∝ Z_eff² / n² in Rydberg units
        double rydberg_eV = 13.605693122994;  // Rydberg energy in eV
        return rydberg_eV * (Z_eff * Z_eff) / (n * n);
    }

    double Elements::nuclear_radius(int A) {
        constexpr double r_0 = 1.2e-15;  // fm
        return r_0 * std::pow(static_cast<double>(A), 1.0/3.0);
    }

} // namespace sdt::chemistry

