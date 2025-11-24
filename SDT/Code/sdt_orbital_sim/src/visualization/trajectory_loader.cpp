#include "sdt/visualization/orbit_viewer.hpp"
#include "sdt/core/constants.hpp"
#include <fstream>
#include <sstream>
#include <map>
#include <algorithm>

namespace sdt::visualization {

    std::vector<TrajectoryData> load_trajectories_from_csv(const std::string& filename) {
        std::vector<TrajectoryData> trajectories;
        std::ifstream file(filename);
        
        if (!file.is_open()) {
            std::cerr << "Cannot open trajectory file: " << filename << std::endl;
            return trajectories;
        }
        
        std::string line;
        bool header_found = false;
        std::map<std::string, size_t> column_map;
        std::vector<std::string> body_names;
        
        // Parse header
        while (std::getline(file, line)) {
            if (line.empty() || line[0] == '#') {
                continue;
            }
            
            if (!header_found) {
                std::stringstream ss(line);
                std::string column;
                size_t idx = 0;
                
                while (std::getline(ss, column, ',')) {
                    // Trim whitespace
                    column.erase(0, column.find_first_not_of(" \t"));
                    column.erase(column.find_last_not_of(" \t") + 1);
                    column_map[column] = idx++;
                    
                    // Extract body names from position columns (Body_x, Body_y, Body_z)
                    if (column.ends_with("_x")) {
                        std::string body_name = column.substr(0, column.length() - 2);
                        body_names.push_back(body_name);
                    }
                }
                
                header_found = true;
                
                // Initialize trajectory data structures
                for (const auto& name : body_names) {
                    TrajectoryData traj;
                    traj.body_name = name;
                    traj.color = BodyColor{{1.0, 1.0, 1.0}, 1.0, 1.0};
                    traj.show_orbit = true;
                    trajectories.push_back(traj);
                }
                
                continue;
            }
            
            // Parse data row
            std::stringstream ss(line);
            std::string field;
            std::vector<std::string> fields;
            
            while (std::getline(ss, field, ',')) {
                fields.push_back(field);
            }
            
            // Extract time
            double time = 0.0;
            if (auto it = column_map.find("Time(s)"); it != column_map.end()) {
                time = std::stod(fields[it->second]);
            }
            
            // Extract positions for each body
            for (size_t i = 0; i < body_names.size() && i < trajectories.size(); ++i) {
                const std::string& body_name = body_names[i];
                
                std::string x_col = body_name + "_x(m)";
                std::string y_col = body_name + "_y(m)";
                std::string z_col = body_name + "_z(m)";
                
                if (column_map.count(x_col) && column_map.count(y_col) && column_map.count(z_col)) {
                    double x = std::stod(fields[column_map[x_col]]);
                    double y = std::stod(fields[column_map[y_col]]);
                    double z = std::stod(fields[column_map[z_col]]);
                    
                    trajectories[i].positions.push_back(Vec3d(x, y, z));
                    trajectories[i].times.push_back(time);
                }
            }
        }
        
        return trajectories;
    }
    
    std::vector<SpectralDataPoint> load_spectral_data(const std::string& filename) {
        // Delegate to SpectralDataLoader
        return io::SpectralDataLoader::load(filename);
    }

} // namespace sdt::visualization

