// SDT Galactic Rotation Calculator - Command Line Tool
// Implements Phase 24: Disk Eclipse Saturation (No Dark Matter)
//
// World-class galactic dynamics calculator with visualization and validation

#include "galactic_rotation.hpp"
#include <iostream>
#include <iomanip>
#include <string_view>
#include <map>
#include <algorithm>

using namespace sdt;

namespace {

/// @brief Print formatted section header
void print_section_header(std::string_view title) {
    std::cout << "\n" << std::string(80, '=') << "\n";
    std::cout << title << "\n";
    std::cout << std::string(80, '=') << "\n\n";
}

/// @brief Print rotation curve table
void print_rotation_curve(const std::vector<RotationPoint>& curve, double R_d_kpc) {
    std::cout << std::setw(12) << "r (kpc)"
              << std::setw(15) << "v (km/s)"
              << std::setw(12) << "E(r)"
              << std::setw(25) << "Regime\n";
    std::cout << std::string(64, '-') << "\n";
    
    // Print every 5th point to keep output manageable
    for (size_t i = 0; i < curve.size(); i += std::max(size_t(1), curve.size() / 15)) {
        const auto& point = curve[i];
        std::string regime = point.is_flat_regime(R_d_kpc) ? 
                            "Flat (Eclipse Sat.)" : "Keplerian";
        
        std::cout << std::fixed << std::setprecision(2);
        std::cout << std::setw(12) << point.radius_kpc
                  << std::setw(15) << point.velocity_kms
                  << std::setprecision(4)
                  << std::setw(12) << point.occlusion_E
                  << std::setw(25) << regime << "\n";
    }
    std::cout << "\n";
}

/// @brief Print galaxy parameters
void print_galaxy_info(const GalaxyParameters& galaxy) {
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Galaxy: " << galaxy.name << "\n";
    std::cout << "  Disk scale length (R_d):     " << galaxy.R_d_kpc << " kpc\n";
    std::cout << "  Flat rotation velocity (v∞): " << galaxy.v_flat_kms << " km/s\n";
    std::cout << "  Predicted R_flat:            " << galaxy.R_flat_predicted_kpc() << " kpc\n";
    std::cout << "  Observed R_flat:             " << galaxy.R_flat_observed_kpc << " kpc\n";
    std::cout << "  R_flat / R_d ratio:          " << std::setprecision(3) << galaxy.R_flat_ratio() << "\n";
    std::cout << "  Prediction error:            " << std::setprecision(2) 
              << galaxy.R_flat_error_percent() << "%\n\n";
}

/// @brief Print validation statistics
void print_validation_stats(const ValidationStatistics& stats) {
    print_section_header("Statistical Validation Results");
    
    std::cout << std::fixed << std::setprecision(3);
    std::cout << "Sample Size:                " << stats.n_galaxies << " galaxies\n";
    std::cout << "Mean R_flat/R_d:           " << stats.mean_ratio << " ± " << stats.std_deviation << "\n";
    std::cout << "SDT Prediction:             2.500 (Phase 24)\n";
    std::cout << "Mean Prediction Error:      " << std::setprecision(2) << stats.mean_error_percent << "%\n";
    std::cout << "Maximum Error:              " << stats.max_error_percent << "%\n\n";
    
    std::cout << "Certification Status:       ";
    if (stats.passes_certification()) {
        std::cout << "✓ CERTIFIED (B14, <1% error)\n";
    } else {
        std::cout << "Under Investigation\n";
    }
    std::cout << "\n";
}

/// @brief Print comparison with dark matter prediction
void print_dark_matter_comparison(double r_kpc, double v_sdt, double v_dm) {
    const double diff_percent = std::abs(v_sdt - v_dm) / v_sdt * 100.0;
    
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "At r = " << r_kpc << " kpc:\n";
    std::cout << "  SDT (Eclipse Saturation): " << v_sdt << " km/s\n";
    std::cout << "  Dark Matter Halo Model:   " << v_dm << " km/s\n";
    std::cout << "  Difference:               " << diff_percent << "%\n\n";
}

/// @brief Print ASCII visualization of rotation curve
void print_ascii_curve_viz(const std::vector<RotationPoint>& curve, double R_d_kpc) {
    std::cout << "\nRotation Curve Visualization:\n\n";
    std::cout << "v (km/s)\n";
    
    const auto max_v = std::max_element(curve.begin(), curve.end(),
        [](const auto& a, const auto& b) { return a.velocity_kms < b.velocity_kms; });
    
    const int height = 15;
    const int width = 50;
    
    for (int row = height; row >= 0; --row) {
        const double v_level = (max_v->velocity_kms * row) / height;
        std::cout << std::setw(6) << std::fixed << std::setprecision(0) << v_level << " |";
        
        for (int col = 0; col < width; ++col) {
            const size_t idx = (col * curve.size()) / width;
            if (idx < curve.size()) {
                const double v = curve[idx].velocity_kms;
                if (std::abs(v - v_level) < (max_v->velocity_kms / height / 2)) {
                    std::cout << "█";
                } else {
                    std::cout << " ";
                }
            }
        }
        std::cout << "\n";
    }
    
    std::cout << "       +";
    std::cout << std::string(width, '-') << ">\n";
    std::cout << "       0";
    std::cout << std::string(width / 2 - 10, ' ') << "r (kpc)\n";
    std::cout << "\n       R_d = " << R_d_kpc << " kpc  |  R_flat ≈ " 
              << (galactic_constants::R_FLAT_FACTOR * R_d_kpc) << " kpc\n\n";
}

/// @brief Print usage information
void print_usage(const char* program_name) {
    std::cout << "Usage: " << program_name << " [OPTIONS]\n\n";
    std::cout << "Options:\n";
    std::cout << "  --R_d FLOAT           Disk scale length in kpc\n";
    std::cout << "  --v_flat FLOAT        Flat rotation velocity in km/s\n";
    std::cout << "  --r_max FLOAT         Maximum radius to calculate (default: 30 kpc)\n";
    std::cout << "  --validate            Validate R_flat/R_d = 2.5 correlation\n";
    std::cout << "  --viz                 Show ASCII visualization of rotation curve\n";
    std::cout << "  --compare-dm          Compare with dark matter halo model\n";
    std::cout << "  --galaxy NAME         Use predefined galaxy (MW, M31, NGC3198, etc.)\n";
    std::cout << "  --help                Show this help message\n\n";
    std::cout << "Examples:\n";
    std::cout << "  " << program_name << " --R_d 2.5 --v_flat 220 --viz\n";
    std::cout << "  " << program_name << " --galaxy MW --compare-dm\n";
    std::cout << "  " << program_name << " --validate\n\n";
}

/// @brief Run complete validation demonstration
void run_validation_demo() {
    print_section_header("R_flat vs R_d Correlation Validation (SDT Phase 24)");
    
    auto galaxies = GalacticRotationCalculator::get_standard_test_galaxies();
    
    std::cout << std::setw(20) << "Galaxy"
              << std::setw(12) << "R_d (kpc)"
              << std::setw(15) << "R_flat (kpc)"
              << std::setw(12) << "R_f/R_d"
              << std::setw(12) << "Error %\n";
    std::cout << std::string(71, '-') << "\n";
    
    for (const auto& galaxy : galaxies) {
        std::cout << std::setw(20) << galaxy.name
                  << std::fixed << std::setprecision(2)
                  << std::setw(12) << galaxy.R_d_kpc
                  << std::setw(15) << galaxy.R_flat_observed_kpc
                  << std::setprecision(3)
                  << std::setw(12) << galaxy.R_flat_ratio()
                  << std::setprecision(2)
                  << std::setw(12) << galaxy.R_flat_error_percent() << "\n";
    }
    
    auto stats = GalacticRotationCalculator::validate_rflat_correlation(galaxies);
    print_validation_stats(stats);
}

} // anonymous namespace

int main(int argc, char* argv[]) {
    if (argc == 1) {
        print_usage(argv[0]);
        return 0;
    }
    
    std::map<std::string_view, std::string_view> args;
    std::vector<std::string_view> flags;
    
    // Parse arguments
    for (int i = 1; i < argc; ++i) {
        std::string_view arg = argv[i];
        
        if (arg == "--help") {
            print_usage(argv[0]);
            return 0;
        }
        
        if (arg == "--validate") {
            run_validation_demo();
            return 0;
        }
        
        if (arg.starts_with("--")) {
            if (i + 1 < argc && !std::string_view(argv[i + 1]).starts_with("--")) {
                args[arg] = argv[++i];
            } else {
                flags.push_back(arg);
            }
        }
    }
    
    try {
        double R_d_kpc = 2.5;
        double v_flat_kms = 220.0;
        double r_max_kpc = 30.0;
        std::string galaxy_name = "Custom Galaxy";
        
        // Handle predefined galaxies
        if (args.contains("--galaxy")) {
            std::string gal_str(args["--galaxy"]);
            auto galaxies = GalacticRotationCalculator::get_standard_test_galaxies();
            
            for (const auto& gal : galaxies) {
                if (gal.name.find(gal_str) != std::string::npos) {
                    R_d_kpc = gal.R_d_kpc;
                    v_flat_kms = gal.v_flat_kms;
                    galaxy_name = gal.name;
                    break;
                }
            }
        }
        
        // Override with explicit parameters
        if (args.contains("--R_d")) {
            R_d_kpc = std::stod(std::string(args["--R_d"]));
        }
        if (args.contains("--v_flat")) {
            v_flat_kms = std::stod(std::string(args["--v_flat"]));
        }
        if (args.contains("--r_max")) {
            r_max_kpc = std::stod(std::string(args["--r_max"]));
        }
        
        // Generate rotation curve
        auto curve = GalacticRotationCalculator::generate_rotation_curve(
            R_d_kpc, v_flat_kms, r_max_kpc, 50
        );
        
        print_section_header("SDT Galactic Rotation Curve (No Dark Matter Required)");
        
        std::cout << "Galaxy: " << galaxy_name << "\n";
        std::cout << std::fixed << std::setprecision(2);
        std::cout << "Disk scale length (R_d):    " << R_d_kpc << " kpc\n";
        std::cout << "Flat velocity (v∞):          " << v_flat_kms << " km/s\n";
        std::cout << "Predicted R_flat:            " << (galactic_constants::R_FLAT_FACTOR * R_d_kpc) << " kpc\n";
        std::cout << "Mechanism:                   Disk Eclipse Saturation\n\n";
        
        print_rotation_curve(curve, R_d_kpc);
        
        // ASCII visualization
        if (std::find(flags.begin(), flags.end(), "--viz") != flags.end()) {
            print_ascii_curve_viz(curve, R_d_kpc);
        }
        
#ifdef SDT_ALLOW_LEGACY_COMPARISON
        // Dark matter comparison (quarantined — NOT SDT)
        if (std::find(flags.begin(), flags.end(), "--compare-dm") != flags.end()) {
            print_section_header("Comparison with Dark Matter Halo Model");
            
            const double test_r = 15.0; // kpc
            const double v_sdt = GalacticRotationCalculator::predict_velocity(test_r, R_d_kpc, v_flat_kms);
            const double v_dm = GalacticRotationCalculator::dark_matter_halo_velocity(test_r, v_flat_kms, R_d_kpc * 2);
            
            print_dark_matter_comparison(test_r, v_sdt, v_dm);
            
            std::cout << "Note: SDT explains flat rotation via disk eclipse saturation.\n";
            std::cout << "      No dark matter halo required. (Phase 24)\n\n";
        }
#endif
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }
    
    return 0;
}
