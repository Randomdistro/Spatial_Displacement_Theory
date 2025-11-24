#include "sdt_navier/fields.hpp"
#include "sdt_navier/equations.hpp"
#include "sdt_navier/solver.hpp"
#include "sdt_navier/nuclear.hpp"
#include "sdt_navier/analysis.hpp"
#include "sdt_navier/io.hpp"
#include "sdt_navier/constants.hpp"
#include <iostream>
#include <iomanip>
#include <vector>
#include <array>
#include <string>
#include <map>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "Usage: " << argv[0] << " <nucleus> [options]\n";
        std::cout << "Nuclei: deuteron, triton, helion, alpha\n";
        std::cout << "Options:\n";
        std::cout << "  --nx <n>     Grid size in x (default: 50)\n";
        std::cout << "  --ny <n>     Grid size in y (default: 50)\n";
        std::cout << "  --nz <n>     Grid size in z (default: 50)\n";
        std::cout << "  --dx <d>     Grid spacing in fm (default: 0.2)\n";
        std::cout << "  --t_end <t>  End time in 10^-24 s (default: 10.0)\n";
        return 1;
    }

    std::string nucleus_type = argv[1];
    std::map<std::string, std::string> options;

    // Parse options
    for (int i = 2; i < argc; i += 2) {
        if (i + 1 < argc) {
            options[argv[i]] = argv[i + 1];
        }
    }

    // Default parameters
    std::size_t nx = 50, ny = 50, nz = 50;
    double dx_fm = 0.2;
    double t_end_units = 10.0;

    if (options.find("--nx") != options.end()) {
        nx = std::stoul(options["--nx"]);
    }
    if (options.find("--ny") != options.end()) {
        ny = std::stoul(options["--ny"]);
    }
    if (options.find("--nz") != options.end()) {
        nz = std::stoul(options["--nz"]);
    }
    if (options.find("--dx") != options.end()) {
        dx_fm = std::stod(options["--dx"]);
    }
    if (options.find("--t_end") != options.end()) {
        t_end_units = std::stod(options["--t_end"]);
    }

    double dx = dx_fm * 1e-15;  // Convert fm to m
    double t_end = t_end_units * 1e-24;  // Convert to seconds

    std::cout << "============================================================\n";
    std::cout << "SDT-Navier " << nucleus_type << " Simulation\n";
    std::cout << "============================================================\n\n";

    std::cout << "Grid: " << nx << " × " << ny << " × " << nz << "\n";
    std::cout << "Grid spacing: " << dx_fm << " fm\n";
    std::cout << "End time: " << t_end_units << " × 10⁻²⁴ s\n\n";

    // Initialize fields
    std::cout << "Initializing fields...\n";
    FieldSystem fields(nx, ny, nz, dx, dx, dx, sdt::P_INFINITY_NUCLEAR);
    initialize_fields(fields);

    std::array<std::size_t, 3> center = {nx/2, ny/2, nz/2};
    double separation_cells = 10.0;

    // Create nuclear system
    std::cout << "Creating " << nucleus_type << " system...\n";
    
    if (nucleus_type == "deuteron") {
        DeuteronSystem system(fields, center, separation_cells);
        
        double B_mev = system.compute_binding_energy_mev();
        double mu = compute_nuclear_magnetic_moment(system);
        
        std::cout << "Binding energy: " << B_mev << " MeV (exp: " << sdt::B_DEUTERON << " MeV)\n";
        std::cout << "Magnetic moment: " << mu << " μ_N (exp: " << sdt::MU_D << " μ_N)\n\n";
        
        // Run simulation
        SDTNavierEquations equations;
        SDTNavierSolver solver(fields, equations, 1.0e-24, 0.5, "rk4", true);
        
        std::cout << "Running simulation...\n";
        int step_count = 0;
        solver.run_until(t_end, [&](SDTNavierSolver& s) {
            step_count++;
            if (step_count % 10 == 0) {
                std::cout << "  Step " << step_count << ": t = " << s.t()*1e24 
                         << " × 10⁻²⁴ s\n";
            }
        });
        
        save_results_json("deuteron_results.json", B_mev, mu, sdt::B_DEUTERON, sdt::MU_D);
        
    } else if (nucleus_type == "triton") {
        TritonSystem system(fields, center, separation_cells);
        std::cout << "Triton system created.\n";
        std::cout << "Binding energy (exp): " << sdt::B_TRITON << " MeV\n";
        std::cout << "Magnetic moment (exp): " << sdt::MU_T << " μ_N\n\n";
        
        SDTNavierEquations equations;
        SDTNavierSolver solver(fields, equations, 1.0e-24, 0.5, "rk4", true);
        solver.run_until(t_end);
        
    } else if (nucleus_type == "helion") {
        HelionSystem system(fields, center, separation_cells);
        std::cout << "Helion system created.\n";
        std::cout << "Binding energy (exp): " << sdt::B_HELION << " MeV\n";
        std::cout << "Magnetic moment (exp): " << sdt::MU_H << " μ_N\n\n";
        
        SDTNavierEquations equations;
        SDTNavierSolver solver(fields, equations, 1.0e-24, 0.5, "rk4", true);
        solver.run_until(t_end);
        
    } else if (nucleus_type == "alpha") {
        AlphaSystem system(fields, center, separation_cells);
        std::cout << "Alpha system created.\n";
        std::cout << "Binding energy (exp): " << sdt::B_ALPHA << " MeV\n";
        std::cout << "Magnetic moment (exp): " << sdt::MU_ALPHA << " μ_N\n\n";
        
        SDTNavierEquations equations;
        SDTNavierSolver solver(fields, equations, 1.0e-24, 0.5, "rk4", true);
        solver.run_until(t_end);
        
    } else {
        std::cerr << "Unknown nucleus type: " << nucleus_type << "\n";
        return 1;
    }

    std::cout << "\nSimulation completed.\n";
    return 0;
}

