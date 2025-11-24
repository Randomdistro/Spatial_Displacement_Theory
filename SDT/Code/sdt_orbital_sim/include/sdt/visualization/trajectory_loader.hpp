#pragma once

#include "sdt/visualization/orbit_viewer.hpp"
#include <string>
#include <vector>

namespace sdt::visualization {

    // Utility: Load trajectory from simulation CSV
    std::vector<TrajectoryData> load_trajectories_from_csv(const std::string& filename);
    
    // Utility: Load spectral data from file
    std::vector<SpectralDataPoint> load_spectral_data(const std::string& filename);

} // namespace sdt::visualization

