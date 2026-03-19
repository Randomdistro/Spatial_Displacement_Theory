// SDT Stellar Calculator - Command Line Tool
// Pure zk²=1 methodology — no G, no mass required
//
// z = Δλ/λ (spectroscopic observable)
// k = c/v  (kinematic observable)
// z·k² = 1 (master constraint)

#include "stellar_calculator.hpp"
#include <iostream>
#include <iomanip>
#include <string_view>
#include <map>

using namespace sdt;

namespace {

void print_header(std::string_view star_name) {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "SDT Stellar Analysis (zk²=1): " << star_name << "\n";
    std::cout << std::string(70, '=') << "\n\n";
}

void print_stellar_parameters(const StellarParameters& params) {
    std::cout << std::fixed << std::setprecision(4);
    std::cout << "Stellar Parameters (from observables only):\n";
    std::cout << "  Radius:          " << params.radius_solar() << " R☉ ("
              << std::scientific << params.radius_m << " m)\n";
    std::cout << "  v_surface:       " << std::fixed << params.v_surface_ms / 1000.0 << " km/s\n";
    std::cout << "  k = c/v:         " << params.k << "\n";
    std::cout << "  z = 1/k²:        " << std::scientific << params.z << "\n";
    std::cout << "  r_c = R/k²:      " << params.r_c_m << " m\n";
    std::cout << "  Circ@r_c:        " << params.circumference_c_boundary_m << " m\n";
    std::cout << "  z_velocity:      " << std::fixed << params.z_velocity_ms() << " m/s\n\n";
}

void print_orbital_analysis(const OrbitalAnalysis& analysis) {
    std::cout << std::string(70, '-') << "\n";
    std::cout << "Orbital Analysis Results\n";
    std::cout << std::string(70, '-') << "\n\n";

    std::cout << std::fixed << std::setprecision(4);
    std::cout << "Orbital Parameters:\n";
    std::cout << "  Semi-major axis: " << analysis.semi_major_axis_au() << " AU ("
              << std::scientific << std::setprecision(3) << analysis.semi_major_axis_m << " m)\n";

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "  Observed velocity:  " << analysis.observed_velocity_kms() << " km/s\n";
    std::cout << "  k-parameter:        " << analysis.k_parameter << "\n";
    std::cout << "  Predicted velocity: " << analysis.predicted_velocity_kms() << " km/s\n";
    std::cout << "  Prediction error:   " << std::setprecision(4) << analysis.error_percent << "%\n\n";

    std::cout << "zk² Validation:\n";
    std::cout << "  z (spectroscopic):  " << std::scientific << analysis.z_spectroscopic << "\n";
    std::cout << "  k:                  " << std::fixed << analysis.k_parameter << "\n";
    std::cout << "  z·k²:              " << analysis.zk2_product << " (expect = 1.0)\n";
    std::cout << "  Deviation:         " << analysis.zk2_deviation;

    if (analysis.is_zk2_valid()) {
        std::cout << " ✓ VALID\n";
    } else {
        std::cout << " ✗ OUTSIDE TOLERANCE\n";
    }

    std::cout << "\n" << std::string(70, '=') << "\n\n";
}

void print_balmer_shifts(const BalmerShifts& shifts) {
    std::cout << "Predicted Balmer Line Shifts (z = " << std::scientific << shifts.z << "):\n";
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "  Hα (656.281 nm): Δλ = " << shifts.delta_H_alpha_nm << " nm\n";
    std::cout << "  Hβ (486.135 nm): Δλ = " << shifts.delta_H_beta_nm << " nm\n";
    std::cout << "  Hγ (434.047 nm): Δλ = " << shifts.delta_H_gamma_nm << " nm\n";
    std::cout << "  Hδ (410.175 nm): Δλ = " << shifts.delta_H_delta_nm << " nm\n\n";
}

void print_usage(const char* program_name) {
    std::cout << "Usage: " << program_name << " [OPTIONS]\n\n";
    std::cout << "SDT Stellar Calculator — pure zk²=1 methodology, no G\n\n";
    std::cout << "Options:\n";
    std::cout << "  --star NAME         Star system name\n";
    std::cout << "  --radius FLOAT      Stellar radius in solar radii\n";
    std::cout << "  --v-surface FLOAT   Surface orbital velocity in km/s\n";
    std::cout << "  --k FLOAT           System k-parameter (alternative to --v-surface)\n";
    std::cout << "  --planet-a FLOAT    Planet semi-major axis in AU\n";
    std::cout << "  --planet-v FLOAT    Planet orbital velocity in km/s\n";
    std::cout << "  --balmer            Show predicted Balmer line shifts\n";
    std::cout << "  --excitation N      Show k for excitation level N (k = N/α)\n";
    std::cout << "  --example           Run with TRAPPIST-1 example\n";
    std::cout << "  --help              Show this help message\n\n";
    std::cout << "Example:\n";
    std::cout << "  " << program_name << " --star \"Sun\" --radius 1.0 --k 685.6\n";
    std::cout << "  " << program_name << " --star \"Sun\" --radius 1.0 --v-surface 437.2 "
              << "--planet-a 1.0 --planet-v 29.78 --balmer\n";
    std::cout << "  " << program_name << " --excitation 5      (solar band: k = 5/α ≈ 685)\n";
    std::cout << "  " << program_name << " --excitation 6      (k = 6/α ≈ 822)\n\n";
}

void run_trappist1_example() {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "TRAPPIST-1 System Analysis — zk²=1 (no G, no mass)\n";
    std::cout << std::string(70, '=') << "\n";

    // TRAPPIST-1: R = 0.121 R☉, surface velocity derived from orbital data
    // k is computed from TRAPPIST-1b orbit: a=0.01111 AU, v=53.1 km/s
    const double R_trappist = 0.121 * stellar_constants::R_SUN;
    const double a_trappist1b_m = 0.01111 * stellar_constants::AU;
    const double v_trappist1b_ms = 53.1e3;

    auto k_opt = StellarCalculator::calculate_k_parameter(
        a_trappist1b_m, v_trappist1b_ms, R_trappist);

    if (!k_opt) {
        std::cerr << "Error: Failed to compute k\n";
        return;
    }

    // Surface velocity from k: v_surface = c/k
    const double v_surface = stellar_constants::C / (*k_opt);
    auto stellar = StellarCalculator::from_radius_and_velocity(R_trappist, v_surface);
    print_stellar_parameters(stellar);

    // Analyze TRAPPIST-1b orbit
    std::cout << "Analyzing TRAPPIST-1b orbital dynamics:\n\n";
    auto analysis = StellarCalculator::analyze_orbit(
        R_trappist, 0.01111, 53.1);

    if (analysis) {
        print_orbital_analysis(*analysis);
        print_balmer_shifts(StellarCalculator::predict_balmer_shifts(*k_opt));
    } else {
        std::cerr << "Error: Failed to analyze orbit\n";
    }
}

} // anonymous namespace

int main(int argc, char* argv[]) {
    std::map<std::string_view, std::string_view> args;

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

    // Excitation level mode: just print k = n/α
    if (args.contains("--excitation")) {
        try {
            int n = std::stoi(std::string(args["--excitation"]));
            double k = StellarCalculator::k_from_excitation(n);
            double z = 1.0 / (k * k);
            double v_grav = stellar_constants::C * z;

            std::cout << "\nExcitation level n=" << n << ":\n";
            std::cout << "  k = n/α = " << std::fixed << std::setprecision(3) << k << "\n";
            std::cout << "  z = 1/k² = " << std::scientific << z << "\n";
            std::cout << "  v_grav = " << std::fixed << std::setprecision(1) << v_grav << " m/s\n\n";

            print_balmer_shifts(StellarCalculator::predict_balmer_shifts(k));
            return 0;
        } catch (...) {
            std::cerr << "Error: invalid excitation level\n";
            return 1;
        }
    }

    // Require radius
    if (!args.contains("--radius")) {
        std::cerr << "Error: --radius is required\n\n";
        print_usage(argv[0]);
        return 1;
    }

    // Need either --k or --v-surface
    if (!args.contains("--k") && !args.contains("--v-surface")) {
        std::cerr << "Error: either --k or --v-surface is required\n\n";
        print_usage(argv[0]);
        return 1;
    }

    try {
        auto star_name = args.contains("--star") ? args["--star"] : "Unknown Star";
        const double radius_solar = std::stod(std::string(args["--radius"]));
        const double radius_m = radius_solar * stellar_constants::R_SUN;

        StellarParameters stellar{};
        if (args.contains("--k")) {
            double k = std::stod(std::string(args["--k"]));
            double v_surface = stellar_constants::C / k;
            stellar = StellarCalculator::from_radius_and_velocity(radius_m, v_surface);
        } else {
            double v_surface_kms = std::stod(std::string(args["--v-surface"]));
            stellar = StellarCalculator::from_radius_and_velocity(radius_m, v_surface_kms * 1000.0);
        }

        print_header(star_name);
        print_stellar_parameters(stellar);

        if (args.contains("--balmer") || args.contains("--planet-a")) {
            print_balmer_shifts(StellarCalculator::predict_balmer_shifts(stellar.k));
        }

        // Orbital analysis if planetary data provided
        if (args.contains("--planet-a") && args.contains("--planet-v")) {
            const double a_au = std::stod(std::string(args["--planet-a"]));
            const double v_kms = std::stod(std::string(args["--planet-v"]));

            auto analysis = StellarCalculator::analyze_orbit(radius_m, a_au, v_kms);

            if (analysis) {
                print_orbital_analysis(*analysis);
            } else {
                std::cerr << "Error: Failed to analyze orbit\n";
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
