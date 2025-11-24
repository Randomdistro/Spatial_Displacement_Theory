#pragma once

#include "sdt/physics/spectral_transitions.hpp"
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <map>

namespace sdt::io::atomic {

    // NIST spectral line data structure
    struct NISTSpectralLine {
        std::string element;
        int charge_state = 0;  // 0=neutral, 1=ionized, etc.
        double wavelength = 0.0;  // nm (vacuum)
        double wavelength_air = 0.0;  // nm (air)
        double intensity = 0.0;  // relative
        std::string transition;  // e.g., "3s-2p"
        double uncertainty = 0.0;  // nm
    };
    
    // Load NIST atomic spectra database
    class NISTLoader {
    public:
        // Load from NIST format file
        static std::vector<NISTSpectralLine> load_nist_file(const std::string& filename);
        
        // Load from CSV export
        static std::vector<NISTSpectralLine> load_csv(const std::string& filename);
        
        // Convert to SDT SpectralLine format
        static std::vector<SpectralLine> convert_to_sdt(
            const std::vector<NISTSpectralLine>& nist_data,
            int Z
        );
        
        // Match calculated lines with NIST data
        static std::vector<std::pair<SpectralLine, NISTSpectralLine>> match_lines(
            const std::vector<SpectralLine>& calculated,
            const std::vector<NISTSpectralLine>& experimental,
            double tolerance_nm = 0.1
        );
    };
    
    // Load atomic constants from CODATA
    class CODATALoader {
    public:
        struct AtomicConstants {
            double bohr_radius = 0.0;  // m
            double rydberg_constant = 0.0;  // m⁻¹
            double fine_structure_constant = 0.0;
            double electron_mass = 0.0;  // kg
            double proton_mass = 0.0;  // kg
        };
        
        static AtomicConstants load_codata_2018();
    };
    
    // Load transition data from codebase CSV
    class TransitionDataLoader {
    public:
        // Load from SDT data files
        static std::vector<SpectralLine> load_from_csv(const std::string& filename);
        
        // Save calculated transitions to CSV
        static void save_to_csv(
            const std::vector<SpectralLine>& lines,
            const std::string& filename
        );
    };

} // namespace sdt::io::atomic

