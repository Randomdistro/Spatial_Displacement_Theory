#include "sdt_navier/io.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <iomanip>

void print_usage(const char* prog_name) {
    std::cout << "Usage: " << prog_name << " <results.json>\n";
    std::cout << "Analyzes simulation results and compares to experimental values.\n";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    std::string filename = argv[1];
    std::ifstream file(filename);
    
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << filename << "\n";
        return 1;
    }

    std::cout << "============================================================\n";
    std::cout << "SDT-Navier Results Analysis\n";
    std::cout << "============================================================\n\n";
    std::cout << "File: " << filename << "\n\n";

    // Simple JSON parsing (for demonstration - in production, use a proper JSON library)
    std::string line;
    double binding_computed = 0.0, binding_exp = 0.0, binding_error = 0.0, binding_rel_error = 0.0;
    double mu_computed = 0.0, mu_exp = 0.0, mu_error = 0.0, mu_rel_error = 0.0;

    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::string key, value;
        
        // Simple extraction (this is a simplified parser)
        if (line.find("\"computed\"") != std::string::npos && 
            line.find("binding_energy") != std::string::npos) {
            size_t pos = line.find(":");
            if (pos != std::string::npos) {
                binding_computed = std::stod(line.substr(pos + 1));
            }
        }
        if (line.find("\"experimental\"") != std::string::npos && 
            line.find("binding_energy") != std::string::npos) {
            size_t pos = line.find(":");
            if (pos != std::string::npos) {
                binding_exp = std::stod(line.substr(pos + 1));
            }
        }
        if (line.find("\"computed\"") != std::string::npos && 
            line.find("magnetic_moment") != std::string::npos) {
            size_t pos = line.find(":");
            if (pos != std::string::npos) {
                mu_computed = std::stod(line.substr(pos + 1));
            }
        }
        if (line.find("\"experimental\"") != std::string::npos && 
            line.find("magnetic_moment") != std::string::npos) {
            size_t pos = line.find(":");
            if (pos != std::string::npos) {
                mu_exp = std::stod(line.substr(pos + 1));
            }
        }
    }

    binding_error = binding_computed - binding_exp;
    binding_rel_error = (binding_exp != 0.0) ? (binding_error / binding_exp * 100.0) : 0.0;
    mu_error = mu_computed - mu_exp;
    mu_rel_error = (mu_exp != 0.0) ? (mu_error / mu_exp * 100.0) : 0.0;

    std::cout << std::fixed << std::setprecision(4);
    std::cout << "Binding Energy:\n";
    std::cout << "  Computed:    " << binding_computed << " MeV\n";
    std::cout << "  Experimental: " << binding_exp << " MeV\n";
    std::cout << "  Error:       " << binding_error << " MeV\n";
    std::cout << "  Relative:    " << binding_rel_error << "%\n\n";

    std::cout << "Magnetic Moment:\n";
    std::cout << "  Computed:    " << mu_computed << " μ_N\n";
    std::cout << "  Experimental: " << mu_exp << " μ_N\n";
    std::cout << "  Error:       " << mu_error << " μ_N\n";
    std::cout << "  Relative:    " << mu_rel_error << "%\n\n";

    std::cout << "============================================================\n";
    std::cout << "Summary\n";
    std::cout << "============================================================\n";
    
    bool binding_ok = std::abs(binding_rel_error) < 50.0;
    bool mu_ok = std::abs(mu_rel_error) < 50.0;
    
    std::cout << "Binding energy: " << (binding_ok ? "✓ PASS" : "✗ FAIL") 
              << " (tolerance: 50%)\n";
    std::cout << "Magnetic moment: " << (mu_ok ? "✓ PASS" : "✗ FAIL") 
              << " (tolerance: 50%)\n";
    
    if (binding_ok && mu_ok) {
        std::cout << "\nAll checks passed!\n";
        return 0;
    } else {
        std::cout << "\nSome checks failed. Consider tuning force functional parameters.\n";
        return 1;
    }
}

