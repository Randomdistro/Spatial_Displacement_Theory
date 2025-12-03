// SDT Stellar Calculator - Command Line Tool
// Implements Phase 22: Exoplanetary Systems & z·k² Validation
//
// World-class implementation with comprehensive error handling,
// formatted output, and SPARC in automated validation.

#include "stellar_calculator.hpp"
#include <iostream>
#include <iomanip>
#include <string_view>
#include <map>

using namespace sdt;

namespace {

/// @brief Print formatted stellar analysis header
void print_header(std::string_view star_name) {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "SDT Stellar Analysis: " << star_name << "\n";
    std::cout << std::string(70, '=') << "\n\n";
}

/// @brief Print stellar parameters with formatted output
void print_stellar_parameters(const StellarParameters& params) {
    std::cout << std::fixed << std::setprecision(3);
    std::cout << "Stellar Physical Parameters:\n";
    std::cout << "  Mass:        " << params.mass_solar() << " M☉ ("
              << std::scientific << params.mass_kg << " kg)\n";
    std::cout << "  Radius:      " << std::fixed << params.radius_solar() << " R☉ ("
              << std::scientific << params.radius_m << " m)\n";
    std::cout << "  β-parameter: " << params.beta << " m\n";
    std::cout << "  Compactness: " << params.compactness << "\n\n";
}

/// @brief Print orbital analysis results
void print_orbital_analysis(const OrbitalAnalysis& analysis) {
    std::cout << std::string(70, '=') << "\n";
    std::cout << "Orbital Analysis Results\n";
    std::cout << std::string(70, '=') << "\n\n";
    
    std::cout << std::fixed << std::setprecision(4);
    std::cout << "Orbital Parameters:\n";
    std::cout << "  Semi-major axis: " << analysis.semi_major_axis_au() << " AU ("
              << std::scientific << std::setprecision(3) << analysis.semi_major_axis_m << " m)\n";
    
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "  Observed velocity:  " << analysis.observed_velocity_kms() << " km/s\n";
    std::cout << "  k-parameter:        " << analysis.k_parameter << "\n";
    std::cout << "  Predicted velocity: " << analysis.predicted_velocity_kms() << " km/s\n";
    std::cout << "  Prediction error:   " << std::setprecision(4) << analysis.error_percent << "%\n\n";
    
    std::cout << "z·k² Validation (Continuous Mass Distribution Test):\n";
    std::cout << "  z (compactness):   " << analysis.z_compactness << "\n";
    std::cout << "  k:                 " << analysis.k_parameter << "\n";
    std::cout << "  z·k²:              " << analysis.zk2_product << " (expect ≈ 1.0)\n";
    std::cout << "  Deviation:         " << analysis.zk2_deviation;
    
    if (analysis.is_zk2_valid()) {
        std::cout << " ✓ VALID\n";
    } else {
        std::cout << " ✗ OUTSIDE TOLERANCE\n";
    }
    
    std::cout << "\n" << std::string(70, '=') << "\n\n";
}

/// @brief Print usage information
void print_usage(const char* program_name) {
    std::cout << "Usage: " << program_name << " [OPTIONS]\n\n";
    std::cout << "Options:\n";
    std::cout << "  --star NAME         Star system name\n";
    std::cout << "  --mass FLOAT        Stellar mass in solar masses\n";
    std::cout << "  --radius FLOAT      Stellar radius in solar radii\n";
    std::cout << "  --planet-a FLOAT    Planet semi-major axis in AU\n";
    std::cout << "  --planet-v FLOAT    Planet orbital velocity in km/s\n";
    std::cout << "  --example           Run with TRAPPIST-1 example\n";
    std::cout << "  --help              Show this help message\n\n";
    std::cout << "Example:\n";
    std::cout << "  " << program_name << " --star \"TRAPPIST-1\" --mass 0.089 --radius 0.121 "
              << "--planet-a 0.01111 --planet-v 53.1\n\n";
}

/// @brief Run TRAPPIST-1 system analysis as example
void run_trappist1_example() {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "Running TRAPPIST-1 System Analysis (Example)\n";
    std::cout << std::string(70, '=') << "\n";
    
    auto stellar = StellarCalculator::calculate_stellar_parameters(0.089, 0.121);
    print_stellar_parameters(stellar);
    
    // TRAPPIST-1b planet data
    std::cout << "Analyzing TRAPPIST-1b orbital dynamics:\n\n";
    auto analysis = StellarCalculator::analyze_orbit(stellar, 0.01111, 53.1);
    
    if (analysis) {
        print_orbital_analysis(*analysis);
    } else {
        std::cerr << "Error: Failed to analyze orbit\n";
    }
}

} // anonymous namespace

int main(int argc, char* argv[]) {
    std::map<std::string_view, std::string_view> args;
    
    // Parse command line arguments
    for (int i = 1; i < argc; ++i) {
        std::string_view arg = argv[i];
        
        if (arg == "--help") {
            print_usage(argv[0]);
            return 0;
        }
        
        if (arg == "--example") {
            run_trappist1_example();
            return 0;
        }
        
        if (arg.starts_with("--") && i + 1 < argc) {
            args[arg] = argv[++i];
        }
    }
    
    // Extract parameters
    auto star_name = args.contains("--star") ? args["--star"] : "Unknown Star";
    
    if (!args.contains("--mass") || !args.contains("--radius")) {
        std::cerr << "Error: --mass and --radius are required\n\n";
        print_usage(argv[0]);
        return 1;
    }
    
    try {
        const double mass_solar = std::stod(std::string(args["--mass"]));
        const double radius_solar = std::stod(std::string(args["--radius"]));
        
        // Calculate stellar parameters
        auto stellar = StellarCalculator::calculate_stellar_parameters(mass_solar, radius_solar);
        
        print_header(star_name);
        print_stellar_parameters(stellar);
        
        // If planetary data provided, analyze orbit
        if (args.contains("--planet-a") && args.contains("--planet-v")) {
            const double a_au = std::stod(std::string(args["--planet-a"]));
            const double v_kms = std::stod(std::string(args["--planet-v"]));
            
            auto analysis = StellarCalculator::analyze_orbit(stellar, a_au, v_kms);
            
            if (analysis) {
                print_orbital_analysis(*analysis);
            } else {
                std::cerr << "Error: Failed to analyze orbit (check input values)\n";
                return 1;
            }
        } else {
            std::cout << "Note: Provide --planet-a and --planet-v for orbital analysis\n\n";
        }
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }
    
    return 0;
}
