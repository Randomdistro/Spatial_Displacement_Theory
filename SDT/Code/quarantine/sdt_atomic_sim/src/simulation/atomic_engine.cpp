#include "sdt/simulation/atomic_engine.hpp"
#include <algorithm>

namespace sdt::simulation::atomic {

    AtomicSimulationEngine::AtomicSimulationEngine(int Z) {
        atom_.Z = Z;
    }
    
    void AtomicSimulationEngine::set_nuclear_charge(int Z) {
        atom_.Z = Z;
    }
    
    void AtomicSimulationEngine::add_electron(const QuantumNumbers& qn) {
        atom_.add_electron(qn);
    }
    
    void AtomicSimulationEngine::configure_ground_state() {
        atom_.occupied_orbitals.clear();
        
        // Add electrons following Aufbau principle
        // Simplified: just add to lowest energy states
        for (int shell = 1; shell <= atom_.Z && shell <= 7; ++shell) {
            QuantumNumbers qn{shell, 0, 0, 0.5};
            atom_.add_electron(qn);
        }
    }
    
    double AtomicSimulationEngine::calculate_total_energy() const {
        return atom_.total_energy();
    }
    
    std::vector<SpectralLine> AtomicSimulationEngine::calculate_spectrum(int max_n) {
        AtomicSpectrum spectrum;
        spectrum.Z = atom_.Z;
        spectrum.generate_hydrogen_spectrum(max_n);
        return spectrum.lines;
    }
    
    std::vector<FineStructureLevel> AtomicSimulationEngine::calculate_fine_structure_levels(int max_n) {
        std::vector<FineStructureLevel> levels;
        
        for (int n = 1; n <= max_n; ++n) {
            for (int l = 0; l < n; ++l) {
                FineStructureLevel level;
                level.n = n;
                level.l = l;
                level.calculate(atom_.Z);
                levels.push_back(level);
            }
        }
        
        return levels;
    }
    
    HyperfineSplitting AtomicSimulationEngine::calculate_hyperfine_structure(int n, int l) {
        SpectralAnalyzer analyzer;
        return analyzer.calculate_hyperfine(n, l, 1);  // Assume spin-1/2 nucleus
    }

} // namespace sdt::simulation::atomic

