#include <iostream>
#include <string>
#include "sdt/physics/electron_orbitals.hpp"
#include "sdt/physics/spectral_transitions.hpp"
#include "sdt/visualization/orbital_viewer.hpp"
#include "sdt/io/atomic_data_loader.hpp"
#include <fmt/core.h>

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
            fmt::print("=== SDT Atomic Orbital 3D Viewer ===\n");
            fmt::print("Visualizing orbital: n={}, l={}, m={}\n", n, l, m);
            
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
            
            fmt::print("Controls:\n");
            fmt::print("  Mouse drag: Rotate\n");
            fmt::print("  Mouse wheel: Zoom\n");
            fmt::print("  'q' or close: Quit\n");
            fmt::print("\nStarting viewer...\n");
            
            viewer.render();
            viewer.start_interactor();
            
        } else if (mode == "spectrum") {
            fmt::print("=== SDT Atomic Spectrum Viewer ===\n");
            
            // Generate spectrum
            sdt::physics::atomic::AtomicSpectrum spectrum;
            spectrum.generate_hydrogen_spectrum(10);
            
            // Load experimental data if provided
            if (!spectral_file.empty()) {
                fmt::print("Loading experimental data from: {}\n", spectral_file);
                auto nist_data = sdt::io::atomic::NISTLoader::load_csv(spectral_file);
                fmt::print("Loaded {} experimental lines\n", nist_data.size());
            }
            
            // Show spectrum
            fmt::print("\nHydrogen Spectrum:\n");
            for (const auto& line : spectrum.lines) {
                if (line.wavelength > 0) {
                    fmt::print("  {}: λ = {:.2f} nm, E = {:.4f} eV\n",
                              line.name, line.wavelength * 1e9, line.energy);
                }
            }
            
        } else if (mode == "atom") {
            fmt::print("=== SDT Atomic System Viewer ===\n");
            
            sdt::physics::atomic::AtomicSystem atom;
            atom.Z = 1;
            atom.add_electron({1, 0, 0, 0.5});
            
            sdt::visualization::atomic::OrbitalViewer3D viewer;
            viewer.initialize(1920, 1080);
            viewer.visualize_atom(atom);
            
            viewer.render();
            viewer.start_interactor();
            
        } else {
            fmt::print("Usage: {} <mode> [options]\n", argv[0]);
            fmt::print("Modes:\n");
            fmt::print("  orbital [n] [l] [m]  - Visualize specific orbital\n");
            fmt::print("  spectrum [file.csv]  - Show spectrum\n");
            fmt::print("  atom                 - Visualize atom\n");
            return 1;
        }
        
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}

