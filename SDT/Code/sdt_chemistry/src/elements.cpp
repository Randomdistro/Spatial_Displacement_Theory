#include "sdt/chemistry/elements.hpp"
#include "sdt/chemistry/constants.hpp"
#include <stdexcept>
#include <cmath>
#include <cctype>
#include <limits>
#include <map>
#include <utility>

namespace sdt::chemistry {

    namespace {
        struct Subshell {
            int n;
            int l;
            int capacity;
        };

        const std::vector<Subshell> kAufbauOrder = {
            {1, 0, 2},  // 1s
            {2, 0, 2},  // 2s
            {2, 1, 6},  // 2p
            {3, 0, 2},  // 3s
            {3, 1, 6},  // 3p
            {4, 0, 2},  // 4s
            {3, 2, 10}, // 3d
            {4, 1, 6},  // 4p
            {5, 0, 2},  // 5s
            {4, 2, 10}, // 4d
            {5, 1, 6},  // 5p
            {6, 0, 2},  // 6s
            {4, 3, 14}, // 4f
            {5, 2, 10}, // 5d
            {6, 1, 6},  // 6p
            {7, 0, 2},  // 7s
            {5, 3, 14}, // 5f
            {6, 2, 10}, // 6d
            {7, 1, 6}   // 7p
        };

        std::map<std::pair<int, int>, int> build_configuration(int Z) {
            std::map<std::pair<int, int>, int> config;
            int remaining = Z;
            for (const auto& shell : kAufbauOrder) {
                if (remaining <= 0) {
                    break;
                }
                int fill = std::min(shell.capacity, remaining);
                config[{shell.n, shell.l}] = fill;
                remaining -= fill;
            }
            return config;
        }

        int count_shell_electrons(const std::map<std::pair<int, int>, int>& config, int n) {
            int count = 0;
            for (const auto& entry : config) {
                if (entry.first.first == n) {
                    count += entry.second;
                }
            }
            return count;
        }

        int count_shells_leq(const std::map<std::pair<int, int>, int>& config, int n_max) {
            int count = 0;
            for (const auto& entry : config) {
                if (entry.first.first <= n_max) {
                    count += entry.second;
                }
            }
            return count;
        }

        int count_same_n_sp(const std::map<std::pair<int, int>, int>& config, int n) {
            int count = 0;
            for (const auto& entry : config) {
                if (entry.first.first == n && entry.first.second <= 1) {
                    count += entry.second;
                }
            }
            return count;
        }

        std::vector<int> build_config_vector(int Z) {
            const auto config = build_configuration(Z);
            std::vector<int> flat_config;
            flat_config.reserve(static_cast<size_t>(Z) * 2);
            for (const auto& shell : kAufbauOrder) {
                const auto key = std::make_pair(shell.n, shell.l);
                auto it = config.find(key);
                if (it == config.end()) {
                    continue;
                }
                for (int i = 0; i < it->second; ++i) {
                    flat_config.push_back(shell.n);
                    flat_config.push_back(shell.l);
                }
            }
            return flat_config;
        }

        int infer_valence_electrons(int Z) {
            const auto config = build_configuration(Z);
            int max_n = 0;
            for (const auto& entry : config) {
                max_n = std::max(max_n, entry.first.first);
            }
            return count_shell_electrons(config, max_n);
        }

        ElementData make_unknown_element(int Z, const std::string& symbol, const std::string& name) {
            const double kUnknown = std::numeric_limits<double>::quiet_NaN();
            ElementData elem{};
            elem.Z = Z;
            elem.symbol = symbol;
            elem.name = name;
            elem.atomic_mass = kUnknown;  // NIST pending
            elem.atomic_radius_pm = kUnknown;  // NIST pending
            elem.covalent_radius_pm = kUnknown;  // NIST pending
            elem.ionic_radius_pm = kUnknown;  // NIST pending
            elem.ionization_energy_eV = kUnknown;  // NIST pending
            elem.electron_affinity_eV = kUnknown;  // NIST pending
            elem.electronegativity = kUnknown;  // NIST pending
            elem.valence_electrons = infer_valence_electrons(Z);
            elem.electron_config = build_config_vector(Z);  // [(n, l), ...] flattened
            elem.nuclear_radius_fm = kUnknown;  // NIST pending
            elem.effective_occlusion_radius_m = kUnknown;  // SDT pending
            elem.effective_nuclear_charge = kUnknown;  // SDT pending
            return elem;
        }
    } // namespace

    std::unordered_map<std::string, ElementData> Elements::element_map_;
    std::unordered_map<int, ElementData*> Elements::element_by_Z_;
    bool Elements::initialized_ = false;

    void Elements::initialize_database() {
        if (initialized_) {
            return;
        }
        
        // Initialize element database (NIST values + SDT parameters where available)
        
        auto add_element = [](const ElementData& elem) {
            element_map_[elem.symbol] = elem;
            element_by_Z_[elem.Z] = const_cast<ElementData*>(&element_map_[elem.symbol]);
        };
        auto add_unknown_element = [&](int Z, const std::string& symbol, const std::string& name) {
            add_element(make_unknown_element(Z, symbol, name));
        };
        
        // H
        add_element({
            /* Z */ 1,
            /* symbol */ "H",
            /* name */ "Hydrogen",
            /* atomic_mass (u) */ 1.007825,
            /* atomic_radius_pm */ 53.0,
            /* covalent_radius_pm */ 31.0,
            /* ionic_radius_pm */ 154.0,
            /* ionization_energy_eV (IE1) */ 13.59843,
            /* electron_affinity_eV */ 0.754,
            /* electronegativity (Pauling) */ 2.20,
            /* valence_electrons */ 1,
            /* electron_config [(n,l) pairs] */ {1, 0},
            /* nuclear_radius_fm (1H) */ 0.84,
            /* effective_occlusion_radius_m */ 1.0e-21,
            /* effective_nuclear_charge */ 1.0
        });
        
        // He
        add_element({
            /* Z */ 2,
            /* symbol */ "He",
            /* name */ "Helium",
            /* atomic_mass (u) */ 4.002602,
            /* atomic_radius_pm */ 31.0,
            /* covalent_radius_pm */ 28.0,
            /* ionic_radius_pm */ 93.0,
            /* ionization_energy_eV (IE1) */ 24.58741,
            /* electron_affinity_eV */ -0.5,
            /* electronegativity (Pauling) */ 0.0,
            /* valence_electrons */ 2,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0},
            /* nuclear_radius_fm */ 1.7,
            /* effective_occlusion_radius_m */ 1.5e-21,
            /* effective_nuclear_charge */ 1.7
        });
        
        // Li
        add_element({
            /* Z */ 3,
            /* symbol */ "Li",
            /* name */ "Lithium",
            /* atomic_mass (u) */ 7.016004,
            /* atomic_radius_pm */ 152.0,
            /* covalent_radius_pm */ 128.0,
            /* ionic_radius_pm */ 76.0,
            /* ionization_energy_eV (IE1) */ 5.39172,
            /* electron_affinity_eV */ 0.618,
            /* electronegativity (Pauling) */ 0.98,
            /* valence_electrons */ 1,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0},
            /* nuclear_radius_fm */ 2.3,
            /* effective_occlusion_radius_m */ 8.0e-11,
            /* effective_nuclear_charge */ 1.3
        });
        
        // Be
        add_element({
            /* Z */ 4,
            /* symbol */ "Be",
            /* name */ "Beryllium",
            /* atomic_mass (u) */ 9.012182,
            /* atomic_radius_pm */ 112.0,
            /* covalent_radius_pm */ 96.0,
            /* ionic_radius_pm */ 45.0,
            /* ionization_energy_eV (IE1) */ 9.32270,
            /* electron_affinity_eV */ -0.5,
            /* electronegativity (Pauling) */ 1.57,
            /* valence_electrons */ 2,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0},
            /* nuclear_radius_fm */ 2.4,
            /* effective_occlusion_radius_m */ 7.0e-11,
            /* effective_nuclear_charge */ 1.9
        });
        
        // B
        add_element({
            /* Z */ 5,
            /* symbol */ "B",
            /* name */ "Boron",
            /* atomic_mass (u) */ 11.009305,
            /* atomic_radius_pm */ 85.0,
            /* covalent_radius_pm */ 84.0,
            /* ionic_radius_pm */ 27.0,
            /* ionization_energy_eV (IE1) */ 8.29803,
            /* electron_affinity_eV */ 0.277,
            /* electronegativity (Pauling) */ 2.04,
            /* valence_electrons */ 3,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1},
            /* nuclear_radius_fm */ 2.5,
            /* effective_occlusion_radius_m */ 6.5e-11,
            /* effective_nuclear_charge */ 2.4
        });
        
        // C
        add_element({
            /* Z */ 6,
            /* symbol */ "C",
            /* name */ "Carbon",
            /* atomic_mass (u) */ 12.0,
            /* atomic_radius_pm */ 77.0,
            /* covalent_radius_pm */ 76.0,
            /* ionic_radius_pm */ 16.0,
            /* ionization_energy_eV (IE1) */ 11.26030,
            /* electron_affinity_eV */ 1.262,
            /* electronegativity (Pauling) */ 2.55,
            /* valence_electrons */ 4,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1},
            /* nuclear_radius_fm */ 2.6,
            /* effective_occlusion_radius_m */ 6.0e-11,
            /* effective_nuclear_charge */ 3.1
        });
        
        // N
        add_element({
            /* Z */ 7,
            /* symbol */ "N",
            /* name */ "Nitrogen",
            /* atomic_mass (u) */ 14.003074,
            /* atomic_radius_pm */ 75.0,
            /* covalent_radius_pm */ 71.0,
            /* ionic_radius_pm */ 146.0,
            /* ionization_energy_eV (IE1) */ 14.53414,
            /* electron_affinity_eV */ -0.07,
            /* electronegativity (Pauling) */ 3.04,
            /* valence_electrons */ 5,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1},
            /* nuclear_radius_fm */ 2.7,
            /* effective_occlusion_radius_m */ 5.8e-11,
            /* effective_nuclear_charge */ 3.8
        });
        
        // O
        add_element({
            /* Z */ 8,
            /* symbol */ "O",
            /* name */ "Oxygen",
            /* atomic_mass (u) */ 15.994915,
            /* atomic_radius_pm */ 73.0,
            /* covalent_radius_pm */ 66.0,
            /* ionic_radius_pm */ 140.0,
            /* ionization_energy_eV (IE1) */ 13.61806,
            /* electron_affinity_eV */ 1.461,
            /* electronegativity (Pauling) */ 3.44,
            /* valence_electrons */ 6,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1},
            /* nuclear_radius_fm */ 2.8,
            /* effective_occlusion_radius_m */ 5.6e-11,
            /* effective_nuclear_charge */ 4.5
        });
        
        // F
        add_element({
            /* Z */ 9,
            /* symbol */ "F",
            /* name */ "Fluorine",
            /* atomic_mass (u) */ 18.998403,
            /* atomic_radius_pm */ 72.0,
            /* covalent_radius_pm */ 57.0,
            /* ionic_radius_pm */ 133.0,
            /* ionization_energy_eV (IE1) */ 17.42282,
            /* electron_affinity_eV */ 3.401,
            /* electronegativity (Pauling) */ 3.98,
            /* valence_electrons */ 7,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1},
            /* nuclear_radius_fm */ 2.9,
            /* effective_occlusion_radius_m */ 5.4e-11,
            /* effective_nuclear_charge */ 5.2
        });
        
        // Ne
        add_element({
            /* Z */ 10,
            /* symbol */ "Ne",
            /* name */ "Neon",
            /* atomic_mass (u) */ 20.1797,
            /* atomic_radius_pm */ 71.0,
            /* covalent_radius_pm */ 58.0,
            /* ionic_radius_pm */ 112.0,
            /* ionization_energy_eV (IE1) */ 21.56454,
            /* electron_affinity_eV */ -0.5,
            /* electronegativity (Pauling) */ 0.0,
            /* valence_electrons */ 8,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1},
            /* nuclear_radius_fm */ 3.0,
            /* effective_occlusion_radius_m */ 5.2e-11,
            /* effective_nuclear_charge */ 6.0
        });
        
        // Na
        add_element({
            /* Z */ 11,
            /* symbol */ "Na",
            /* name */ "Sodium",
            /* atomic_mass (u) */ 22.989769,
            /* atomic_radius_pm */ 186.0,
            /* covalent_radius_pm */ 166.0,
            /* ionic_radius_pm */ 102.0,
            /* ionization_energy_eV (IE1) */ 5.13908,
            /* electron_affinity_eV */ 0.548,
            /* electronegativity (Pauling) */ 0.93,
            /* valence_electrons */ 1,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0},
            /* nuclear_radius_fm */ 3.1,
            /* effective_occlusion_radius_m */ 1.2e-10,
            /* effective_nuclear_charge */ 1.0
        });
        
        // Mg
        add_element({
            /* Z */ 12,
            /* symbol */ "Mg",
            /* name */ "Magnesium",
            /* atomic_mass (u) */ 24.305,
            /* atomic_radius_pm */ 160.0,
            /* covalent_radius_pm */ 141.0,
            /* ionic_radius_pm */ 72.0,
            /* ionization_energy_eV (IE1) */ 7.64624,
            /* electron_affinity_eV */ -0.4,
            /* electronegativity (Pauling) */ 1.31,
            /* valence_electrons */ 2,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0},
            /* nuclear_radius_fm */ 3.2,
            /* effective_occlusion_radius_m */ 1.1e-10,
            /* effective_nuclear_charge */ 1.3
        });
        
        // Al
        add_element({
            /* Z */ 13,
            /* symbol */ "Al",
            /* name */ "Aluminum",
            /* atomic_mass (u) */ 26.981538,
            /* atomic_radius_pm */ 143.0,
            /* covalent_radius_pm */ 121.0,
            /* ionic_radius_pm */ 53.5,
            /* ionization_energy_eV (IE1) */ 5.98577,
            /* electron_affinity_eV */ 0.441,
            /* electronegativity (Pauling) */ 1.61,
            /* valence_electrons */ 3,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1},
            /* nuclear_radius_fm */ 3.3,
            /* effective_occlusion_radius_m */ 1.0e-10,
            /* effective_nuclear_charge */ 2.6
        });
        
        // Si
        add_element({
            /* Z */ 14,
            /* symbol */ "Si",
            /* name */ "Silicon",
            /* atomic_mass (u) */ 28.085,
            /* atomic_radius_pm */ 118.0,
            /* covalent_radius_pm */ 111.0,
            /* ionic_radius_pm */ 40.0,
            /* ionization_energy_eV (IE1) */ 8.15169,
            /* electron_affinity_eV */ 1.385,
            /* electronegativity (Pauling) */ 1.90,
            /* valence_electrons */ 4,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1},
            /* nuclear_radius_fm */ 3.4,
            /* effective_occlusion_radius_m */ 9.5e-11,
            /* effective_nuclear_charge */ 3.3
        });
        
        // P
        add_element({
            /* Z */ 15,
            /* symbol */ "P",
            /* name */ "Phosphorus",
            /* atomic_mass (u) */ 30.973762,
            /* atomic_radius_pm */ 110.0,
            /* covalent_radius_pm */ 107.0,
            /* ionic_radius_pm */ 44.0,
            /* ionization_energy_eV (IE1) */ 10.48669,
            /* electron_affinity_eV */ 0.746,
            /* electronegativity (Pauling) */ 2.19,
            /* valence_electrons */ 5,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1},
            /* nuclear_radius_fm */ 3.5,
            /* effective_occlusion_radius_m */ 9.0e-11,
            /* effective_nuclear_charge */ 4.1
        });
        
        // S
        add_element({
            /* Z */ 16,
            /* symbol */ "S",
            /* name */ "Sulfur",
            /* atomic_mass (u) */ 32.065,
            /* atomic_radius_pm */ 103.0,
            /* covalent_radius_pm */ 105.0,
            /* ionic_radius_pm */ 184.0,
            /* ionization_energy_eV (IE1) */ 10.36001,
            /* electron_affinity_eV */ 2.077,
            /* electronegativity (Pauling) */ 2.58,
            /* valence_electrons */ 6,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1, 3, 1},
            /* nuclear_radius_fm */ 3.6,
            /* effective_occlusion_radius_m */ 8.5e-11,
            /* effective_nuclear_charge */ 4.9
        });
        
        // Cl
        add_element({
            /* Z */ 17,
            /* symbol */ "Cl",
            /* name */ "Chlorine",
            /* atomic_mass (u) */ 35.453,
            /* atomic_radius_pm */ 99.0,
            /* covalent_radius_pm */ 102.0,
            /* ionic_radius_pm */ 181.0,
            /* ionization_energy_eV (IE1) */ 12.96764,
            /* electron_affinity_eV */ 3.617,
            /* electronegativity (Pauling) */ 3.16,
            /* valence_electrons */ 7,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1},
            /* nuclear_radius_fm */ 3.7,
            /* effective_occlusion_radius_m */ 8.0e-11,
            /* effective_nuclear_charge */ 5.7
        });
        
        // Ar
        add_element({
            /* Z */ 18,
            /* symbol */ "Ar",
            /* name */ "Argon",
            /* atomic_mass (u) */ 39.948,
            /* atomic_radius_pm */ 97.0,
            /* covalent_radius_pm */ 106.0,
            /* ionic_radius_pm */ 154.0,
            /* ionization_energy_eV (IE1) */ 15.75962,
            /* electron_affinity_eV */ -0.5,
            /* electronegativity (Pauling) */ 0.0,
            /* valence_electrons */ 8,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1},
            /* nuclear_radius_fm */ 3.8,
            /* effective_occlusion_radius_m */ 7.5e-11,
            /* effective_nuclear_charge */ 6.6
        });
        
        // K
        add_element({
            /* Z */ 19,
            /* symbol */ "K",
            /* name */ "Potassium",
            /* atomic_mass (u) */ 39.0983,
            /* atomic_radius_pm */ 227.0,
            /* covalent_radius_pm */ 203.0,
            /* ionic_radius_pm */ 138.0,
            /* ionization_energy_eV (IE1) */ 4.34066,
            /* electron_affinity_eV */ 0.501,
            /* electronegativity (Pauling) */ 0.82,
            /* valence_electrons */ 1,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 4, 0},
            /* nuclear_radius_fm */ 3.9,
            /* effective_occlusion_radius_m */ 1.5e-10,
            /* effective_nuclear_charge */ 1.0
        });
        
        // Ca
        add_element({
            /* Z */ 20,
            /* symbol */ "Ca",
            /* name */ "Calcium",
            /* atomic_mass (u) */ 40.078,
            /* atomic_radius_pm */ 197.0,
            /* covalent_radius_pm */ 176.0,
            /* ionic_radius_pm */ 100.0,
            /* ionization_energy_eV (IE1) */ 6.11316,
            /* electron_affinity_eV */ 0.024,
            /* electronegativity (Pauling) */ 1.00,
            /* valence_electrons */ 2,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 4, 0, 4, 0},
            /* nuclear_radius_fm */ 4.0,
            /* effective_occlusion_radius_m */ 1.4e-10,
            /* effective_nuclear_charge */ 1.3
        });

        // Sc
        add_element({
            /* Z */ 21,
            /* symbol */ "Sc",
            /* name */ "Scandium",
            /* atomic_mass (u) */ 44.955908,
            /* atomic_radius_pm */ 162.0,
            /* covalent_radius_pm */ 144.0,
            /* ionic_radius_pm */ 75.0,
            /* ionization_energy_eV (IE1) */ 6.5615,
            /* electron_affinity_eV */ 0.188,
            /* electronegativity (Pauling) */ 1.36,
            /* valence_electrons */ 3,
            /* electron_config [(n,l) pairs] */ {1, 0, 1, 0, 2, 0, 2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 0, 3, 0, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 4, 0, 4, 0, 3, 2},
            /* nuclear_radius_fm */ 3.5,
            /* effective_occlusion_radius_m */ 1.3e-10,
            /* effective_nuclear_charge */ 3.0
        });

        // Ti through Og (NIST values pending)
        add_unknown_element(22, "Ti", "Titanium");
        add_unknown_element(23, "V", "Vanadium");
        add_unknown_element(24, "Cr", "Chromium");
        add_unknown_element(25, "Mn", "Manganese");
        add_unknown_element(26, "Fe", "Iron");
        add_unknown_element(27, "Co", "Cobalt");
        add_unknown_element(28, "Ni", "Nickel");
        add_unknown_element(29, "Cu", "Copper");
        add_unknown_element(30, "Zn", "Zinc");
        add_unknown_element(31, "Ga", "Gallium");
        add_unknown_element(32, "Ge", "Germanium");
        add_unknown_element(33, "As", "Arsenic");
        add_unknown_element(34, "Se", "Selenium");
        add_unknown_element(35, "Br", "Bromine");
        add_unknown_element(36, "Kr", "Krypton");
        add_unknown_element(37, "Rb", "Rubidium");
        add_unknown_element(38, "Sr", "Strontium");
        add_unknown_element(39, "Y", "Yttrium");
        add_unknown_element(40, "Zr", "Zirconium");
        add_unknown_element(41, "Nb", "Niobium");
        add_unknown_element(42, "Mo", "Molybdenum");
        add_unknown_element(43, "Tc", "Technetium");
        add_unknown_element(44, "Ru", "Ruthenium");
        add_unknown_element(45, "Rh", "Rhodium");
        add_unknown_element(46, "Pd", "Palladium");
        add_unknown_element(47, "Ag", "Silver");
        add_unknown_element(48, "Cd", "Cadmium");
        add_unknown_element(49, "In", "Indium");
        add_unknown_element(50, "Sn", "Tin");
        add_unknown_element(51, "Sb", "Antimony");
        add_unknown_element(52, "Te", "Tellurium");
        add_unknown_element(53, "I", "Iodine");
        add_unknown_element(54, "Xe", "Xenon");
        add_unknown_element(55, "Cs", "Cesium");
        add_unknown_element(56, "Ba", "Barium");
        add_unknown_element(57, "La", "Lanthanum");
        add_unknown_element(58, "Ce", "Cerium");
        add_unknown_element(59, "Pr", "Praseodymium");
        add_unknown_element(60, "Nd", "Neodymium");
        add_unknown_element(61, "Pm", "Promethium");
        add_unknown_element(62, "Sm", "Samarium");
        add_unknown_element(63, "Eu", "Europium");
        add_unknown_element(64, "Gd", "Gadolinium");
        add_unknown_element(65, "Tb", "Terbium");
        add_unknown_element(66, "Dy", "Dysprosium");
        add_unknown_element(67, "Ho", "Holmium");
        add_unknown_element(68, "Er", "Erbium");
        add_unknown_element(69, "Tm", "Thulium");
        add_unknown_element(70, "Yb", "Ytterbium");
        add_unknown_element(71, "Lu", "Lutetium");
        add_unknown_element(72, "Hf", "Hafnium");
        add_unknown_element(73, "Ta", "Tantalum");
        add_unknown_element(74, "W", "Tungsten");
        add_unknown_element(75, "Re", "Rhenium");
        add_unknown_element(76, "Os", "Osmium");
        add_unknown_element(77, "Ir", "Iridium");
        add_unknown_element(78, "Pt", "Platinum");
        add_unknown_element(79, "Au", "Gold");
        add_unknown_element(80, "Hg", "Mercury");
        add_unknown_element(81, "Tl", "Thallium");
        add_unknown_element(82, "Pb", "Lead");
        add_unknown_element(83, "Bi", "Bismuth");
        add_unknown_element(84, "Po", "Polonium");
        add_unknown_element(85, "At", "Astatine");
        add_unknown_element(86, "Rn", "Radon");
        add_unknown_element(87, "Fr", "Francium");
        add_unknown_element(88, "Ra", "Radium");
        add_unknown_element(89, "Ac", "Actinium");
        add_unknown_element(90, "Th", "Thorium");
        add_unknown_element(91, "Pa", "Protactinium");
        add_unknown_element(92, "U", "Uranium");
        add_unknown_element(93, "Np", "Neptunium");
        add_unknown_element(94, "Pu", "Plutonium");
        add_unknown_element(95, "Am", "Americium");
        add_unknown_element(96, "Cm", "Curium");
        add_unknown_element(97, "Bk", "Berkelium");
        add_unknown_element(98, "Cf", "Californium");
        add_unknown_element(99, "Es", "Einsteinium");
        add_unknown_element(100, "Fm", "Fermium");
        add_unknown_element(101, "Md", "Mendelevium");
        add_unknown_element(102, "No", "Nobelium");
        add_unknown_element(103, "Lr", "Lawrencium");
        add_unknown_element(104, "Rf", "Rutherfordium");
        add_unknown_element(105, "Db", "Dubnium");
        add_unknown_element(106, "Sg", "Seaborgium");
        add_unknown_element(107, "Bh", "Bohrium");
        add_unknown_element(108, "Hs", "Hassium");
        add_unknown_element(109, "Mt", "Meitnerium");
        add_unknown_element(110, "Ds", "Darmstadtium");
        add_unknown_element(111, "Rg", "Roentgenium");
        add_unknown_element(112, "Cn", "Copernicium");
        add_unknown_element(113, "Nh", "Nihonium");
        add_unknown_element(114, "Fl", "Flerovium");
        add_unknown_element(115, "Mc", "Moscovium");
        add_unknown_element(116, "Lv", "Livermorium");
        add_unknown_element(117, "Ts", "Tennessine");
        add_unknown_element(118, "Og", "Oganesson");
        
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
        // Slater's rules with d/f corrections for Z > 20
        const auto config = build_configuration(Z);
        const auto key = std::make_pair(n, l);
        auto it = config.find(key);
        if (it == config.end()) {
            return static_cast<double>(Z);
        }

        const int valence_count = it->second;
        if (valence_count <= 0) {
            return static_cast<double>(Z);
        }

        double sigma = 0.0;
        if (l <= 1) {
            // ns/np electrons
            const int same_shell_total = count_same_n_sp(config, n);
            const int same_shell_other = std::max(0, same_shell_total - 1);
            sigma += (n == 1 ? 0.30 : 0.35) * same_shell_other;

            const int n_minus_1 = count_shell_electrons(config, n - 1);
            sigma += 0.85 * n_minus_1;

            const int n_minus_2_or_less = count_shells_leq(config, n - 2);
            sigma += 1.00 * n_minus_2_or_less;
        } else {
            // nd/nf electrons
            sigma += 0.35 * (valence_count - 1);

            const int lower_shells = count_shells_leq(config, n - 1);
            sigma += 1.00 * lower_shells;

            const int same_n_sp = count_same_n_sp(config, n);
            sigma += 1.00 * same_n_sp;
        }

        return std::max(0.0, static_cast<double>(Z) - sigma);
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

