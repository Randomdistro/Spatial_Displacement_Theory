#include <iostream>
#include <fmt/core.h>
#include "sdt/physics/electron_orbitals.hpp"
#include "sdt/physics/spectral_transitions.hpp"
#include "sdt/simulation/atomic_engine.hpp"
#include "sdt/io/atomic_data_loader.hpp"
#include "sdt/core/constants.hpp"
#include "sdt/core/types.hpp"

using namespace sdt;
using namespace sdt::physics::atomic;

int main(int argc, char* argv[]) {
    try {
        fmt::print("=== SDT Atomic Physics Simulator ===\n\n");
        
        // Example 1: Hydrogen atom ground state
        fmt::print("Example 1: Hydrogen Atom Ground State\n");
        fmt::print("=====================================\n");
        
        HydrogenAtom hydrogen;
        auto ground_state = hydrogen.get_state(1, 0, 0);
        
        fmt::print("Ground State (1s):\n");
        fmt::print("  Energy: {:.6f} eV\n", ground_state.energy);
        fmt::print("  Radius: {:.2e} m (Bohr radius: {:.2e} m)\n", 
                  ground_state.radius, constants::A_0);
        fmt::print("  Ϟ: {:.2f}\n", ground_state.kappa);
        fmt::print("\n");
        
        // Example 2: Lyman Alpha transition
        fmt::print("Example 2: Lyman Alpha Transition\n");
        fmt::print("==================================\n");
        
        const double lyman_alpha_energy = hydrogen.transition_energy(2, 1);
        const double lyman_alpha_wavelength = hydrogen.transition_wavelength(2, 1);
        
        fmt::print("2p → 1s Transition:\n");
        fmt::print("  Energy: {:.6f} eV\n", lyman_alpha_energy);
        fmt::print("  Wavelength: {:.2e} m ({:.2f} nm)\n", 
                  lyman_alpha_wavelength, lyman_alpha_wavelength * 1e9);
        fmt::print("  Frequency: {:.2e} Hz\n", constants::C / lyman_alpha_wavelength);
        fmt::print("\n");
        
        // Example 3: Generate hydrogen spectrum
        fmt::print("Example 3: Hydrogen Spectral Series\n");
        fmt::print("====================================\n");
        
        AtomicSpectrum spectrum;
        spectrum.generate_hydrogen_spectrum(10);
        
        // Show Lyman series
        auto lyman_lines = spectrum.get_lines_in_series(SpectralSeries::LYMAN);
        fmt::print("Lyman Series (n → 1):\n");
        for (size_t i = 0; i < std::min(static_cast<size_t>(5), lyman_lines.size()); ++i) {
            const auto& line = lyman_lines[i];
            fmt::print("  {}: λ = {:.2f} nm, E = {:.4f} eV\n",
                      line.name, line.wavelength * 1e9, line.energy);
        }
        fmt::print("\n");
        
        // Show Balmer series
        auto balmer_lines = spectrum.get_lines_in_series(SpectralSeries::BALMER);
        fmt::print("Balmer Series (n → 2):\n");
        for (size_t i = 0; i < std::min(static_cast<size_t>(5), balmer_lines.size()); ++i) {
            const auto& line = balmer_lines[i];
            fmt::print("  {}: λ = {:.2f} nm, E = {:.4f} eV\n",
                      line.name, line.wavelength * 1e9, line.energy);
        }
        fmt::print("\n");
        
        // Example 4: Fine structure
        fmt::print("Example 4: Fine Structure (n=2, l=1)\n");
        fmt::print("=====================================\n");
        
        using namespace sdt::simulation::atomic;
        AtomicSimulationEngine engine(1);
        auto fine_structure = engine.calculate_fine_structure_levels(3);
        
        for (const auto& level : fine_structure) {
            if (level.n == 2 && level.l == 1) {
                fmt::print("2p Level Fine Structure:\n");
                for (const auto& comp : level.components) {
                    fmt::print("  j = {:.1f}: Energy = {:.8f} eV, Splitting = {:.8f} eV\n",
                              comp.j * 0.5, comp.energy, comp.splitting);
                }
                break;
            }
        }
        fmt::print("\n");
        
        // Example 5: Hyperfine structure
        fmt::print("Example 5: Hyperfine Structure (1s)\n");
        fmt::print("====================================\n");
        
        auto hyperfine = engine.calculate_hyperfine_structure(1, 0);
        fmt::print("1s Hyperfine Splitting:\n");
        fmt::print("  Frequency: {:.6f} MHz\n", hyperfine.frequency / 1e6);
        fmt::print("  Energy: {:.8e} eV\n", hyperfine.energy);
        fmt::print("  Wavelength: {:.2f} cm (21 cm line)\n", 
                  constants::C / hyperfine.frequency * 100.0);
        fmt::print("\n");
        
        // Example 6: Orbital visualization data
        fmt::print("Example 6: Generating Orbital Data\n");
        fmt::print("===================================\n");
        
        ElectronOrbital orbital;
        orbital.state = ground_state;
        orbital.Z = 1;
        
        const double expected_r = orbital.expected_radius();
        fmt::print("1s Orbital:\n");
        fmt::print("  Expected radius: {:.2e} m\n", expected_r);
        fmt::print("  Probability density at origin: {:.2e}\n",
                  orbital.probability_density(Vec3d::Zero()));
        
        fmt::print("\nSimulation complete!\n");
        
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}

