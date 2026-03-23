#include "sdt/io/atomic_data_loader.hpp"
#include "sdt/core/constants.hpp"
#include <fstream>
#include <sstream>
#include <algorithm>

namespace sdt::io::atomic {

    std::vector<NISTSpectralLine> NISTLoader::load_csv(const std::string& filename) {
        std::vector<NISTSpectralLine> lines;
        std::ifstream file(filename);
        
        if (!file.is_open()) {
            return lines;
        }
        
        std::string line_str;
        bool header_found = false;
        std::map<std::string, size_t> column_map;
        
        while (std::getline(file, line_str)) {
            if (line_str.empty() || line_str[0] == '#') {
                continue;
            }
            
            if (!header_found) {
                std::stringstream ss(line_str);
                std::string column;
                size_t idx = 0;
                
                while (std::getline(ss, column, ',')) {
                    column.erase(0, column.find_first_not_of(" \t"));
                    column.erase(column.find_last_not_of(" \t") + 1);
                    column_map[column] = idx++;
                }
                
                header_found = true;
                continue;
            }
            
            NISTSpectralLine nist_line;
            std::stringstream ss(line_str);
            std::string field;
            std::vector<std::string> fields;
            
            while (std::getline(ss, field, ',')) {
                fields.push_back(field);
            }
            
            // Parse fields based on column map
            if (auto it = column_map.find("Element"); it != column_map.end()) {
                nist_line.element = fields[it->second];
            }
            if (auto it = column_map.find("Wavelength"); it != column_map.end()) {
                nist_line.wavelength = std::stod(fields[it->second]) * 1e-9;  // Convert nm to m
            }
            if (auto it = column_map.find("Intensity"); it != column_map.end()) {
                nist_line.intensity = std::stod(fields[it->second]);
            }
            if (auto it = column_map.find("Transition"); it != column_map.end()) {
                nist_line.transition = fields[it->second];
            }
            
            lines.push_back(nist_line);
        }
        
        return lines;
    }
    
    std::vector<SpectralLine> NISTLoader::convert_to_sdt(
        const std::vector<NISTSpectralLine>& nist_data,
        int Z
    ) {
        std::vector<SpectralLine> sdt_lines;
        
        for (const auto& nist : nist_data) {
            SpectralLine line;
            line.wavelength = nist.wavelength;
            line.frequency = sdt::constants::c / line.wavelength;
            line.energy = sdt::constants::h * line.frequency / 1.602176634e-19;  // eV
            line.intensity = nist.intensity;
            line.series = SpectralSeries::LYMAN;  // Default, should parse from transition
            line.name = nist.transition;
            
            sdt_lines.push_back(line);
        }
        
        return sdt_lines;
    }
    
    AtomicConstants CODATALoader::load_codata_2018() {
        AtomicConstants constants;
        
        constants.bohr_radius = 5.29177210903e-11;  // m
        constants.rydberg_constant = 10973731.568160;  // m⁻¹
        constants.fine_structure_constant = 7.2973525693e-3;
        constants.electron_mass = 9.1093837015e-31;  // kg
        constants.proton_mass = 1.67262192369e-27;  // kg
        
        return constants;
    }

} // namespace sdt::io::atomic

