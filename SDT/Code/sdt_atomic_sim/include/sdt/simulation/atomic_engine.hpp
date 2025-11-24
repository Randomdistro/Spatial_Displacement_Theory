#pragma once

#include "sdt/physics/electron_orbitals.hpp"
#include "sdt/physics/spectral_transitions.hpp"
#include "sdt/core/types.hpp"
#include <vector>
#include <memory>
#include <functional>

namespace sdt::simulation::atomic {

    // Atomic simulation engine
    class AtomicSimulationEngine {
    public:
        AtomicSimulationEngine(int Z = 1);
        
        // Setup atomic system
        void set_nuclear_charge(int Z);
        void add_electron(const QuantumNumbers& qn);
        void configure_ground_state();
        
        // Calculate properties
        double calculate_total_energy() const;
        std::vector<SpectralLine> calculate_spectrum(int max_n = 10);
        std::vector<SpectralTransition> calculate_all_transitions(int max_n = 10);
        
        // Fine structure calculation
        std::vector<FineStructureLevel> calculate_fine_structure_levels(int max_n = 5);
        
        // Hyperfine structure
        HyperfineSplitting calculate_hyperfine_structure(int n = 1, int l = 0);
        
        // Time evolution (for transition dynamics)
        void evolve(double dt);
        
        // Get current state
        AtomicSystem get_atomic_system() const { return atom_; }
        
        // Set output callback
        void set_output_callback(std::function<void(const AtomicSystem&)> callback);
        
    private:
        AtomicSystem atom_;
        double current_time_ = 0.0;
        std::function<void(const AtomicSystem&)> output_callback_;
    };
    
    // Multi-electron atom simulation
    class MultiElectronSimulator {
    public:
        MultiElectronSimulator(int Z);
        
        // Calculate electron configuration
        std::vector<OrbitalState> calculate_electron_configuration();
        
        // Calculate screening effects
        double calculate_screening_factor(int n, int l) const;
        
        // Calculate effective nuclear charge
        double calculate_effective_Z(int n, int l) const;
        
        // Calculate total energy with electron-electron interactions
        double calculate_total_energy_with_interactions() const;
        
        // Calculate ionization energies
        std::vector<double> calculate_ionization_energies() const;
        
    private:
        int Z_;
        std::vector<OrbitalState> occupied_orbitals_;
    };

} // namespace sdt::simulation::atomic

