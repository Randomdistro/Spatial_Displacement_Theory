#include "sdt/solar_system/visualizer.hpp"
#include "sdt/solar_system/data_loader.hpp"
#include <fmt/core.h>
#include <iostream>
#include <string>
#include <fstream>
#include <sstream>

using namespace sdt::solar_system;

int main(int argc, char* argv[]) {
    try {
        if (argc < 3) {
            fmt::print("Usage: {} <trajectory_file.csv> <output_format> [output_file]\n", argv[0]);
            fmt::print("Formats: csv, xyz, vtk\n");
            return 1;
        }
        
        std::string trajectory_file = argv[1];
        std::string format = argv[2];
        std::string output_file = (argc > 3) ? argv[3] : "output." + format;
        
        // Read trajectory CSV
        std::ifstream file(trajectory_file);
        if (!file.is_open()) {
            fmt::print(stderr, "Error: Cannot open file {}\n", trajectory_file);
            return 1;
        }
        
        // Parse CSV (simplified - assumes same format as exported)
        std::string line;
        std::getline(file, line);  // Skip header
        
        // For now, just convert the last state
        // Full implementation would parse all states
        SystemState state;
        state.current_time = 0.0;
        
        // This is a placeholder - full implementation would parse the CSV properly
        fmt::print("Reading trajectory from {}\n", trajectory_file);
        fmt::print("Converting to {} format...\n", format);
        
        // Export based on format
        if (format == "csv") {
            // Already CSV, just copy
            fmt::print("Output file: {}\n", output_file);
        } else if (format == "xyz") {
            // Would need to parse CSV first
            fmt::print("XYZ export not fully implemented yet\n");
        } else if (format == "vtk") {
            // Would need to parse CSV first
            fmt::print("VTK export not fully implemented yet\n");
        } else {
            fmt::print(stderr, "Error: Unknown format {}\n", format);
            return 1;
        }
        
        return 0;
    } catch (const std::exception& e) {
        fmt::print(stderr, "Error: {}\n", e.what());
        return 1;
    }
}


