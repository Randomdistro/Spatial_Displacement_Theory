#include <iostream>
#include <iomanip>
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
        std::cout << "=== SDT Atomic Physics Simulator ===\n\n";
        
        // Example 1: Hydrogen atom ground state
        std::cout << "Example 1: Hydrogen Atom Ground State\n";
        std::cout << "=====================================\n";
        
        HydrogenAtom hydrogen;
        auto ground_state = hydrogen.get_state(1, 0, 0);
        
        std::cout << "Ground State (1s):\n";
        std::cout << std::fixed << std::setprecision(6);
        std::cout << "  Energy: " << ground_state.energy << " eV\n";
        std::cout << std::scientific << std::setprecision(2);
        std::cout << "  Radius: " << ground_state.radius << " m (Bohr radius: " << constants::A_0 << " m)\n";
        std::cout << std::fixed << std::setprecision(2);
        std::cout << "  Ϟ: " << ground_state.kappa << "\n";
        std::cout << "\n";
        
        // Example 2: Lyman Alpha transition
        std::cout << "Example 2: Lyman Alpha Transition\n";
        std::cout << "==================================\n";
        
        const double lyman_alpha_energy = hydrogen.transition_energy(2, 1);
        const double lyman_alpha_wavelength = hydrogen.transition_wavelength(2, 1);
        
        std::cout << "2p → 1s Transition:\n";
        std::cout << std::fixed << std::setprecision(6);
        std::cout << "  Energy: " << lyman_alpha_energy << " eV\n";
        std::cout << std::scientific << std::setprecision(2);
        std::cout << "  Wavelength: " << lyman_alpha_wavelength << " m ("
                  << std::fixed << std::setprecision(2) << lyman_alpha_wavelength * 1e9 << " nm)\n";
        std::cout << std::scientific << std::setprecision(2);
        std::cout << "  Frequency: " << constants::C / lyman_alpha_wavelength << " Hz\n";
        std::cout << "\n";
        
        // Example 3: Generate hydrogen spectrum
        std::cout << "Example 3: Hydrogen Spectral Series\n";
        std::cout << "====================================\n";
        
        AtomicSpectrum spectrum;
        spectrum.generate_hydrogen_spectrum(10);
        
        // Show Lyman series
        auto lyman_lines = spectrum.get_lines_in_series(SpectralSeries::LYMAN);
        std::cout << "Lyman Series (n → 1):\n";
        for (size_t i = 0; i < std::min(static_cast<size_t>(5), lyman_lines.size()); ++i) {
            const auto& line = lyman_lines[i];
            std::cout << "  " << line.name << ": λ = " << std::fixed << std::setprecision(2)
                      << line.wavelength * 1e9 << " nm, E = " << std::setprecision(4)
                      << line.energy << " eV\n";
        }
        std::cout << "\n";
        
        // Show Balmer series
        auto balmer_lines = spectrum.get_lines_in_series(SpectralSeries::BALMER);
        std::cout << "Balmer Series (n → 2):\n";
        for (size_t i = 0; i < std::min(static_cast<size_t>(5), balmer_lines.size()); ++i) {
            const auto& line = balmer_lines[i];
            std::cout << "  " << line.name << ": λ = " << std::fixed << std::setprecision(2)
                      << line.wavelength * 1e9 << " nm, E = " << std::setprecision(4)
                      << line.energy << " eV\n";
        }
        std::cout << "\n";
        
        // Example 4: Fine structure
        std::cout << "Example 4: Fine Structure (n=2, l=1)\n";
        std::cout << "=====================================\n";
        
        using namespace sdt::simulation::atomic;
        AtomicSimulationEngine engine(1);
        auto fine_structure = engine.calculate_fine_structure_levels(3);
        
        for (const auto& level : fine_structure) {
            if (level.n == 2 && level.l == 1) {
                std::cout << "2p Level Fine Structure:\n";
                for (const auto& comp : level.components) {
                    std::cout << std::fixed;
                    std::cout << "  j = " << std::setprecision(1) << comp.j * 0.5
                              << ": Energy = " << std::setprecision(8) << comp.energy
                              << " eV, Splitting = " << comp.splitting << " eV\n";
                }
                break;
            }
        }
        std::cout << "\n";
        
        // Example 5: Hyperfine structure
        std::cout << "Example 5: Hyperfine Structure (1s)\n";
        std::cout << "====================================\n";
        
        auto hyperfine = engine.calculate_hyperfine_structure(1, 0);
        std::cout << "1s Hyperfine Splitting:\n";
        std::cout << std::fixed << std::setprecision(6);
        std::cout << "  Frequency: " << hyperfine.frequency / 1e6 << " MHz\n";
        std::cout << std::scientific << std::setprecision(8);
        std::cout << "  Energy: " << hyperfine.energy << " eV\n";
        std::cout << std::fixed << std::setprecision(2);
        std::cout << "  Wavelength: " << constants::C / hyperfine.frequency * 100.0 << " cm (21 cm line)\n";
        std::cout << "\n";
        
        // Example 6: Orbital visualization data
        std::cout << "Example 6: Generating Orbital Data\n";
        std::cout << "===================================\n";
        
        ElectronOrbital orbital;
        orbital.state = ground_state;
        orbital.Z = 1;
        
        const double expected_r = orbital.expected_radius();
        std::cout << "1s Orbital:\n";
        std::cout << std::scientific << std::setprecision(2);
        std::cout << "  Expected radius: " << expected_r << " m\n";
        std::cout << "  Probability density at origin: "
                  << orbital.probability_density(Vec3d::Zero()) << "\n";
        
        std::cout << "\nSimulation complete!\n";
        
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
