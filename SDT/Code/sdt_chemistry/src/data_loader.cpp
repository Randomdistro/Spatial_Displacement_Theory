#include "sdt/chemistry/data_loader.hpp"
#include <fstream>
#include <sstream>
#if __has_include(<filesystem>)
#include <filesystem>
namespace fs = std::filesystem;
#else
#include <experimental/filesystem>
namespace fs = std::experimental::filesystem;
#endif

namespace sdt::chemistry {

    std::string DataLoader::data_dir_ = "";

    std::vector<std::unordered_map<std::string, std::string>> DataLoader::load_atomic_spectra(
        const std::string& filepath
    ) {
        std::vector<std::unordered_map<std::string, std::string>> data;
        
        std::ifstream file(filepath);
        if (!file.is_open()) {
            return data;
        }
        
        std::string line;
        bool first_line = true;
        std::vector<std::string> headers;
        
        while (std::getline(file, line)) {
            if (line.empty() || line[0] == '#') {
                continue;
            }
            
            std::vector<std::string> values = parse_csv_line(line);
            
            if (first_line) {
                headers = values;
                first_line = false;
                continue;
            }
            
            if (values.size() != headers.size()) {
                continue;
            }
            
            std::unordered_map<std::string, std::string> row;
            for (size_t i = 0; i < headers.size(); ++i) {
                row[headers[i]] = values[i];
            }
            data.push_back(row);
        }
        
        return data;
    }

    std::vector<std::unordered_map<std::string, std::string>> DataLoader::load_validation_data(
        const std::string& filepath
    ) {
        return load_atomic_spectra(filepath);  // Same format
    }

    bool DataLoader::load_element_data(const std::string& filepath) {
        // Load element data from CSV and update Elements database
        // TODO: Implement full element data loading
        return true;
    }

    std::vector<std::unordered_map<std::string, std::string>> DataLoader::load_bond_parameters(
        const std::string& filepath
    ) {
        return load_atomic_spectra(filepath);  // Same format
    }

    std::vector<std::string> DataLoader::parse_csv_line(const std::string& line) {
        std::vector<std::string> result;
        std::stringstream ss(line);
        std::string item;
        
        while (std::getline(ss, item, ',')) {
            // Remove quotes if present
            if (item.front() == '"' && item.back() == '"') {
                item = item.substr(1, item.length() - 2);
            }
            result.push_back(item);
        }
        
        return result;
    }

    std::string DataLoader::get_data_directory() {
        if (data_dir_.empty()) {
            // Try to find data directory relative to executable
            fs::path current_path = fs::current_path();
            fs::path data_path = current_path / "data";
            
            if (fs::exists(data_path)) {
                data_dir_ = data_path.string();
            } else {
                // Try parent directory
                data_path = current_path.parent_path() / "data";
                if (fs::exists(data_path)) {
                    data_dir_ = data_path.string();
                } else {
                    data_dir_ = current_path.string();
                }
            }
        }
        return data_dir_;
    }

} // namespace sdt::chemistry

