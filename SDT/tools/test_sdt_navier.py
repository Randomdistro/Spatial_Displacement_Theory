"""
Benchmark script for SDT-Navier field theory.

Runs deuteron simulation and extracts binding energy and magnetic moment,
comparing to experimental values.
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Code'))

from sdt_navier.fields import initialize_fields
from sdt_navier.equations import SDTNavierEquations
from sdt_navier.solver import SDTNavierSolver
from sdt_navier.nuclear import DeuteronSystem
from sdt_navier.magnetic_moments import (
    compute_nuclear_magnetic_moment,
    compare_magnetic_moment,
    MU_D_EXP,
)


def run_deuteron_benchmark():
    """
    Run deuteron benchmark simulation.
    
    Returns
    -------
    results : dict
        Dictionary with simulation results and comparisons
    """
    print("=" * 70)
    print("SDT-Navier Deuteron Benchmark")
    print("=" * 70)
    print()
    
    # Simulation parameters
    nx, ny, nz = 50, 50, 50
    dx = 0.2e-15  # 0.2 fm grid spacing
    center = (nx // 2, ny // 2, nz // 2)
    separation_cells = 10.0  # 2 fm separation
    
    print(f"Grid: {nx} × {ny} × {nz}")
    print(f"Grid spacing: {dx*1e15:.2f} fm")
    print(f"Separation: {separation_cells * dx * 1e15:.2f} fm")
    print()
    
    # Initialize fields
    print("Initializing fields...")
    fields = initialize_fields(nx, ny, nz, dx, P_infinity=1.65e31)
    
    # Create deuteron system
    print("Creating deuteron system...")
    equations = SDTNavierEquations()
    deuteron = DeuteronSystem(fields, center, separation_cells, equations)
    
    print(f"Proton position: {deuteron.proton.position}")
    print(f"Neutron position: {deuteron.neutron.position}")
    print()
    
    # Compute initial binding energy
    print("Computing binding energy...")
    B_mev = deuteron.compute_binding_energy_mev()
    B_exp = 2.224  # MeV
    
    print(f"Computed binding energy: {B_mev:.4f} MeV")
    print(f"Experimental binding energy: {B_exp:.4f} MeV")
    print(f"Error: {B_mev - B_exp:.4f} MeV")
    print(f"Relative error: {(B_mev - B_exp) / B_exp * 100:.2f}%")
    print()
    
    # Compute magnetic moment
    print("Computing magnetic moment...")
    mu_d = compute_nuclear_magnetic_moment(deuteron)
    mu_exp = MU_D_EXP
    
    print(f"Computed magnetic moment: {mu_d:.4f} μ_N")
    print(f"Experimental magnetic moment: {mu_exp:.4f} μ_N")
    print(f"Error: {mu_d - mu_exp:.4f} μ_N")
    print(f"Relative error: {(mu_d - mu_exp) / mu_exp * 100:.2f}%")
    print()
    
    # Run short simulation
    print("Running simulation...")
    solver = SDTNavierSolver(
        fields,
        equations,
        dt=1.0e-24,
        enforce_incompressibility=True,
    )
    
    t_end = 1.0e-23  # 10 steps
    step_count = [0]
    
    def callback(s):
        step_count[0] += 1
        if step_count[0] % 5 == 0:
            div_error = s.get_divergence_error()
            print(f"  Step {step_count[0]}: t = {s.t*1e24:.2f} × 10⁻²⁴ s, max|∇·v| = {div_error:.2e}")
    
    solver.run_until(t_end, callback=callback)
    print()
    
    # Final divergence error
    div_error = solver.get_divergence_error()
    print(f"Final divergence error: {div_error:.2e}")
    print()
    
    # Compile results
    results = {
        "binding_energy": {
            "computed": B_mev,
            "experimental": B_exp,
            "error": B_mev - B_exp,
            "relative_error_percent": (B_mev - B_exp) / B_exp * 100,
        },
        "magnetic_moment": {
            "computed": mu_d,
            "experimental": mu_exp,
            "error": mu_d - mu_exp,
            "relative_error_percent": (mu_d - mu_exp) / mu_exp * 100,
        },
        "simulation": {
            "final_time": solver.t,
            "steps": step_count[0],
            "divergence_error": div_error,
        },
    }
    
    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Binding energy error: {results['binding_energy']['relative_error_percent']:.2f}%")
    print(f"Magnetic moment error: {results['magnetic_moment']['relative_error_percent']:.2f}%")
    print()
    
    return results


if __name__ == "__main__":
    results = run_deuteron_benchmark()
    
    # Exit with error code if results are poor
    if abs(results["binding_energy"]["relative_error_percent"]) > 50:
        print("WARNING: Binding energy error > 50%")
        sys.exit(1)
    
    if abs(results["magnetic_moment"]["relative_error_percent"]) > 50:
        print("WARNING: Magnetic moment error > 50%")
        sys.exit(1)
    
    print("Benchmark completed successfully.")
    sys.exit(0)

