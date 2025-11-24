#pragma once

#include "elements.hpp"
#include <string>
#include <vector>
#include <unordered_map>

namespace sdt::chemistry {

    /**
     * Data loader for CSV files and experimental data
     */
    class DataLoader {
    public:
        /**
         * Load atomic spectra from NIST CSV
         */
        static std::vector<std::unordered_map<std::string, std::string>> load_atomic_spectra(
            const std::string& filepath
        );
        
        /**
         * Load validation data
         */
        static std::vector<std::unordered_map<std::string, std::string>> load_validation_data(
            const std::string& filepath
        );
        
        /**
         * Load element data from CSV
         */
        static bool load_element_data(const std::string& filepath);
        
        /**
         * Load bond parameters from CSV
         */
        static std::vector<std::unordered_map<std::string, std::string>> load_bond_parameters(
            const std::string& filepath
        );
        
        /**
         * Parse CSV line
         */
        static std::vector<std::string> parse_csv_line(const std::string& line);
        
        /**
         * Get data directory path
         */
        static std::string get_data_directory();
        
    private:
        static std::string data_dir_;
    };

} // namespace sdt::chemistry

