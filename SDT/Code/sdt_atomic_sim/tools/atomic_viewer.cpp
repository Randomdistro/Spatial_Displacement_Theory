#include <iostream>
#include <iomanip>
#include <string>
#include "sdt/physics/electron_orbitals.hpp"
#include "sdt/physics/spectral_transitions.hpp"
#include "sdt/visualization/orbital_viewer.hpp"
#include "sdt/io/atomic_data_loader.hpp"

int main(int argc, char* argv[]) {
    try {
        std::string mode = "orbital";
        int n = 1, l = 0, m = 0;
        std::string spectral_file;
        
        if (argc > 1) {
            mode = argv[1];
        }
        if (argc > 2 && mode == "orbital") {
            n = std::stoi(argv[2]);
            if (argc > 3) l = std::stoi(argv[3]);
            if (argc > 4) m = std::stoi(argv[4]);
        }
        if (argc > 2 && mode == "spectrum") {
            spectral_file = argv[2];
        }
        
        if (mode == "orbital") {
            std::cout << "=== SDT Atomic Orbital 3D Viewer ===\n";
            std::cout << "Visualizing orbital: n=" << n << ", l=" << l << ", m=" << m << "\n";
            
            // Create orbital
            sdt::physics::atomic::HydrogenAtom hydrogen;
            auto state = hydrogen.get_state(n, l, m);
            
            sdt::physics::atomic::ElectronOrbital orbital;
            orbital.state = state;
            orbital.Z = 1;
            
            // Create viewer
            sdt::visualization::atomic::OrbitalViewer3D viewer;
            viewer.initialize(1920, 1080);
            viewer.set_isosurface_value(0.01);
            
            // Visualize
            viewer.visualize_orbital(orbital);
            
            std::cout << "Controls:\n";
            std::cout << "  Mouse drag: Rotate\n";
            std::cout << "  Mouse wheel: Zoom\n";
            std::cout << "  'q' or close: Quit\n";
            std::cout << "\nStarting viewer...\n";
            
            viewer.render();
            viewer.start_interactor();
            
        } else if (mode == "spectrum") {
            std::cout << "=== SDT Atomic Spectrum Viewer ===\n";
            
            // Generate spectrum
            sdt::physics::atomic::AtomicSpectrum spectrum;
            spectrum.generate_hydrogen_spectrum(10);
            
            // Load experimental data if provided
            if (!spectral_file.empty()) {
                std::cout << "Loading experimental data from: " << spectral_file << "\n";
                auto nist_data = sdt::io::atomic::NISTLoader::load_csv(spectral_file);
                std::cout << "Loaded " << nist_data.size() << " experimental lines\n";
            }
            
            // Show spectrum
            std::cout << "\nHydrogen Spectrum:\n";
            for (const auto& line : spectrum.lines) {
                if (line.wavelength > 0) {
                    std::cout << "  " << line.name << ": λ = "
                              << std::fixed << std::setprecision(2) << line.wavelength * 1e9
                              << " nm, E = " << std::setprecision(4) << line.energy << " eV\n";
                }
            }
            
        } else if (mode == "atom") {
            std::cout << "=== SDT Atomic System Viewer ===\n";
            
            sdt::physics::atomic::AtomicSystem atom;
            atom.Z = 1;
            atom.add_electron({1, 0, 0, 0.5});
            
            sdt::visualization::atomic::OrbitalViewer3D viewer;
            viewer.initialize(1920, 1080);
            viewer.visualize_atom(atom);
            
            viewer.render();
            viewer.start_interactor();
            
        } else {
            std::cout << "Usage: " << argv[0] << " <mode> [options]\n";
            std::cout << "Modes:\n";
            std::cout << "  orbital [n] [l] [m]  - Visualize specific orbital\n";
            std::cout << "  spectrum [file.csv]  - Show spectrum\n";
            std::cout << "  atom                 - Visualize atom\n";
            return 1;
        }
        
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
