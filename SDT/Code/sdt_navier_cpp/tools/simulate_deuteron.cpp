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
#include <functional>

int main(int argc, char* argv[]) {
    std::cout << "============================================================\n";
    std::cout << "SDT-Navier Deuteron Simulation\n";
    std::cout << "============================================================\n\n";

    // Simulation parameters
    std::size_t nx = 50, ny = 50, nz = 50;
    double dx = 0.2e-15;  // 0.2 fm
    std::array<std::size_t, 3> center = {nx/2, ny/2, nz/2};
    double separation_cells = 10.0;  // 2 fm / 0.2 fm

    std::cout << "Grid: " << nx << " × " << ny << " × " << nz << "\n";
    std::cout << "Grid spacing: " << dx*1e15 << " fm\n";
    std::cout << "Separation: " << separation_cells * dx * 1e15 << " fm\n\n";

    // Initialize fields
    std::cout << "Initializing fields...\n";
    FieldSystem fields(nx, ny, nz, dx, dx, dx, sdt::P_INFINITY_NUCLEAR);
    initialize_fields(fields);

    // Create deuteron system
    std::cout << "Creating deuteron system...\n";
    DeuteronSystem deuteron(fields, center, separation_cells);

    std::cout << "Proton position: (" << deuteron.proton().position[0] << ", "
              << deuteron.proton().position[1] << ", " << deuteron.proton().position[2] << ")\n";
    std::cout << "Neutron position: (" << deuteron.neutron().position[0] << ", "
              << deuteron.neutron().position[1] << ", " << deuteron.neutron().position[2] << ")\n\n";

    // Compute initial binding energy
    std::cout << "Computing binding energy...\n";
    double B_mev = deuteron.compute_binding_energy_mev();
    double B_exp = sdt::B_DEUTERON;

    std::cout << "Computed binding energy: " << B_mev << " MeV\n";
    std::cout << "Experimental binding energy: " << B_exp << " MeV\n";
    std::cout << "Error: " << (B_mev - B_exp) << " MeV\n";
    std::cout << "Relative error: " << ((B_mev - B_exp) / B_exp * 100.0) << "%\n\n";

    // Compute magnetic moment
    std::cout << "Computing magnetic moment...\n";
    double mu_d = compute_nuclear_magnetic_moment(deuteron);
    double mu_exp = sdt::MU_D;

    std::cout << "Computed magnetic moment: " << mu_d << " μ_N\n";
    std::cout << "Experimental magnetic moment: " << mu_exp << " μ_N\n";
    std::cout << "Error: " << (mu_d - mu_exp) << " μ_N\n";
    std::cout << "Relative error: " << ((mu_d - mu_exp) / mu_exp * 100.0) << "%\n\n";

    // Run simulation
    std::cout << "Running simulation...\n";
    SDTNavierEquations equations;
    SDTNavierSolver solver(fields, equations, 1.0e-24, 0.5, "rk4", true);

    double t_end = 1.0e-23;  // 10 steps
    std::vector<double> times;
    std::vector<double> div_errors;
    int step_count = 0;

    solver.run_until(t_end, [&](SDTNavierSolver& s) {
        step_count++;
        if (step_count % 5 == 0) {
            double div_error = s.get_divergence_error();
            times.push_back(s.t());
            div_errors.push_back(div_error);
            std::cout << "  Step " << step_count << ": t = " << s.t()*1e24 << " × 10⁻²⁴ s, "
                     << "max|∇·v| = " << div_error << "\n";
        }
    });

    std::cout << "\nFinal divergence error: " << solver.get_divergence_error() << "\n\n";

    // Save results
    std::cout << "Saving results...\n";
    save_results_json("deuteron_results.json", B_mev, mu_d, B_exp, mu_exp);
    save_timeseries_csv("divergence_timeseries.csv", times, div_errors, "time,divergence_error");
    std::cout << "Results saved to deuteron_results.json and divergence_timeseries.csv\n\n";

    // Summary
    std::cout << "============================================================\n";
    std::cout << "Summary\n";
    std::cout << "============================================================\n";
    std::cout << "Binding energy error: " << ((B_mev - B_exp) / B_exp * 100.0) << "%\n";
    std::cout << "Magnetic moment error: " << ((mu_d - mu_exp) / mu_exp * 100.0) << "%\n";
    std::cout << "\nSimulation completed successfully.\n";

    return 0;
}

