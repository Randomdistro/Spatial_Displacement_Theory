#pragma once

#include "sdt/visualization/orbit_viewer.hpp"
#include "sdt/core/types.hpp"
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <regex>
#include <stdexcept>

namespace sdt::io {

    // Spectral data file formats
    enum class SpectralFormat {
        CSV_RADIAL_VELOCITY,    // CSV with time, radial_velocity columns
        CSV_FITS_EXPORT,        // FITS exported to CSV
        NIST_SPECTRAL_LINES,    // NIST atomic spectra database format
        CUSTOM
    };
    
    // Load spectral data from various formats
    class SpectralDataLoader {
    public:
        // Load radial velocity data from CSV
        static std::vector<visualization::SpectralDataPoint> load_radial_velocity_csv(
            const std::string& filename
        ) {
            std::vector<visualization::SpectralDataPoint> data;
            std::ifstream file(filename);
            
            if (!file.is_open()) {
                throw std::runtime_error("Cannot open spectral data file: " + filename);
            }
            
            std::string line;
            bool header_found = false;
            std::map<std::string, size_t> column_map;
            
            while (std::getline(file, line)) {
                // Skip comments and empty lines
                if (line.empty() || line[0] == '#') {
                    continue;
                }
                
                // Parse header
                if (!header_found) {
                    std::stringstream ss(line);
                    std::string column;
                    size_t idx = 0;
                    
                    while (std::getline(ss, column, ',')) {
                        // Trim whitespace
                        column.erase(0, column.find_first_not_of(" \t"));
                        column.erase(column.find_last_not_of(" \t") + 1);
                        column_map[column] = idx++;
                    }
                    
                    header_found = true;
                    continue;
                }
                
                // Parse data row
                visualization::SpectralDataPoint point;
                std::stringstream ss(line);
                std::string field;
                std::vector<std::string> fields;
                
                while (std::getline(ss, field, ',')) {
                    fields.push_back(field);
                }
                
                // Extract time
                if (auto it = column_map.find("time"); it != column_map.end()) {
                    point.time = parse_double(fields[it->second]);
                } else if (auto it = column_map.find("jd"); it != column_map.end()) {
                    // Julian day - convert to seconds from some reference
                    const double jd = parse_double(fields[it->second]);
                    point.time = (jd - 2451545.0) * 86400.0;  // Reference: J2000.0
                }
                
                // Extract radial velocity
                if (auto it = column_map.find("radial_velocity"); it != column_map.end()) {
                    point.radial_velocity = parse_double(fields[it->second]);
                } else if (auto it = column_map.find("rv"); it != column_map.end()) {
                    point.radial_velocity = parse_double(fields[it->second]);
                } else if (auto it = column_map.find("vr"); it != column_map.end()) {
                    point.radial_velocity = parse_double(fields[it->second]);
                }
                
                // Extract wavelength shift (optional)
                if (auto it = column_map.find("wavelength_shift"); it != column_map.end()) {
                    point.wavelength_shift = parse_double(fields[it->second]);
                } else if (auto it = column_map.find("delta_lambda"); it != column_map.end()) {
                    point.wavelength_shift = parse_double(fields[it->second]);
                }
                
                // Extract flux (optional)
                if (auto it = column_map.find("flux"); it != column_map.end()) {
                    point.flux = parse_double(fields[it->second]);
                }
                
                // Extract uncertainties (optional)
                if (auto it = column_map.find("rv_error"); it != column_map.end()) {
                    point.position_uncertainty[0] = parse_double(fields[it->second]);
                }
                
                data.push_back(point);
            }
            
            return data;
        }
        
        // Load from NIST spectral lines format
        static std::vector<visualization::SpectralDataPoint> load_nist_format(
            const std::string& filename
        ) {
            // NIST format parsing - implement based on actual NIST file structure
            std::vector<visualization::SpectralDataPoint> data;
            // Placeholder - full implementation would parse NIST spectral database format
            return data;
        }
        
        // Detect file format and load
        static std::vector<visualization::SpectralDataPoint> load(
            const std::string& filename,
            SpectralFormat format = SpectralFormat::CUSTOM
        ) {
            // Auto-detect format if CUSTOM
            if (format == SpectralFormat::CUSTOM) {
                format = detect_format(filename);
            }
            
            switch (format) {
                case SpectralFormat::CSV_RADIAL_VELOCITY:
                case SpectralFormat::CSV_FITS_EXPORT:
                    return load_radial_velocity_csv(filename);
                case SpectralFormat::NIST_SPECTRAL_LINES:
                    return load_nist_format(filename);
                default:
                    throw std::runtime_error("Unsupported spectral data format");
            }
        }
        
        // Extract orbital parameters from spectral data using phase folding
        struct OrbitalParameters {
            double period = 0.0;
            double semi_major_axis = 0.0;
            double eccentricity = 0.0;
            double inclination = 0.0;
            double longitude_of_ascending_node = 0.0;
            double argument_of_periapsis = 0.0;
            double time_of_periapsis = 0.0;
            double radial_velocity_semi_amplitude = 0.0;
            double center_of_mass_velocity = 0.0;
        };
        
        // Perform periodogram analysis to find orbital period
        static double find_orbital_period(
            const std::vector<visualization::SpectralDataPoint>& spectral_data,
            double min_period = 1.0 * constants::day_to_sec,
            double max_period = 1000.0 * constants::day_to_sec,
            size_t num_samples = 10000
        ) {
            if (spectral_data.size() < 3) {
                return 0.0;  // Need at least 3 points
            }
            
            // Lomb-Scargle periodogram
            double best_period = 0.0;
            double max_power = 0.0;
            
            const double log_min = std::log10(min_period);
            const double log_max = std::log10(max_period);
            
            for (size_t i = 0; i < num_samples; ++i) {
                const double log_period = log_min + (log_max - log_min) * i / (num_samples - 1);
                const double period = std::pow(10.0, log_period);
                
                // Calculate Lomb-Scargle power
                double power = lomb_scargle_power(spectral_data, period);
                
                if (power > max_power) {
                    max_power = power;
                    best_period = period;
                }
            }
            
            return best_period;
        }
        
        // Fit orbital parameters from radial velocity curve
        static OrbitalParameters fit_orbital_parameters(
            const std::vector<visualization::SpectralDataPoint>& spectral_data,
            double period_hint = 0.0
        ) {
            OrbitalParameters params;
            
            // Find period if not provided
            if (period_hint <= 0.0) {
                params.period = find_orbital_period(spectral_data);
            } else {
                params.period = period_hint;
            }
            
            if (params.period <= 0.0) {
                return params;  // Cannot fit without period
            }
            
            // Calculate radial velocity amplitude (K)
            double max_rv = 0.0;
            double min_rv = 0.0;
            double sum_rv = 0.0;
            
            for (const auto& point : spectral_data) {
                max_rv = std::max(max_rv, point.radial_velocity);
                min_rv = std::min(min_rv, point.radial_velocity);
                sum_rv += point.radial_velocity;
            }
            
            params.radial_velocity_semi_amplitude = (max_rv - min_rv) / 2.0;
            params.center_of_mass_velocity = sum_rv / spectral_data.size();
            
            // Simplified: assume circular orbit for now
            // Full implementation would fit eccentricity, etc.
            params.eccentricity = 0.0;
            params.inclination = 90.0;  // Edge-on (typical for RV detections)
            
            return params;
        }
        
    private:
        static double parse_double(const std::string& str) {
            if (str.empty()) {
                return 0.0;
            }
            try {
                return std::stod(str);
            } catch (const std::exception&) {
                return 0.0;
            }
        }
        
        static SpectralFormat detect_format(const std::string& filename) {
            // Simple heuristic - check file extension and content
            if (filename.ends_with(".csv")) {
                return SpectralFormat::CSV_RADIAL_VELOCITY;
            } else if (filename.ends_with(".fits") || filename.ends_with(".fit")) {
                return SpectralFormat::CSV_FITS_EXPORT;  // Assume exported
            } else {
                return SpectralFormat::CUSTOM;
            }
        }
        
        static double lomb_scargle_power(
            const std::vector<visualization::SpectralDataPoint>& data,
            double period
        ) {
            // Simplified Lomb-Scargle periodogram
            // Full implementation would use proper algorithm
            double sum_cos = 0.0, sum_sin = 0.0;
            double sum_cos2 = 0.0, sum_sin2 = 0.0;
            
            for (const auto& point : data) {
                const double phase = 2.0 * std::numbers::pi * point.time / period;
                const double cos_phase = std::cos(phase);
                const double sin_phase = std::sin(phase);
                
                sum_cos += point.radial_velocity * cos_phase;
                sum_sin += point.radial_velocity * sin_phase;
                sum_cos2 += cos_phase * cos_phase;
                sum_sin2 += sin_phase * sin_phase;
            }
            
            const double power = (sum_cos * sum_cos / sum_cos2 + 
                                 sum_sin * sum_sin / sum_sin2) / data.size();
            return power;
        }
    };

} // namespace sdt::io

