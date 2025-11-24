#!/usr/bin/env python3
"""
Example Python script using SDT-Navier C++ bindings

This demonstrates how to use the pybind11 bindings to run simulations
from Python.
"""

import sys
import os

# Add the build directory to path (adjust as needed)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'build'))

try:
    import sdt_navier_cpp
except ImportError:
    print("Error: Could not import sdt_navier_cpp")
    print("Make sure the Python bindings are built and in your Python path.")
    sys.exit(1)

def main():
    print("=" * 70)
    print("SDT-Navier Python Example")
    print("=" * 70)
    print()

    # Create field system
    print("Creating field system...")
    nx, ny, nz = 50, 50, 50
    dx = 0.2e-15  # 0.2 fm
    
    fields = sdt_navier_cpp.FieldSystem(nx, ny, nz, dx, dx, dx)
    print(f"Grid: {nx} × {ny} × {nz}")
    print(f"Grid spacing: {dx*1e15:.2f} fm")
    print()

    # Create equations and solver
    print("Creating equations and solver...")
    equations = sdt_navier_cpp.SDTNavierEquations()
    solver = sdt_navier_cpp.SDTNavierSolver(
        fields, equations, dt=1.0e-24, cfl=0.5, method="rk4", 
        enforce_incompressibility=True
    )
    print(f"Initial timestep: {solver.dt():.2e} s")
    print()

    # Run simulation
    print("Running simulation...")
    t_end = 1.0e-23  # 10 steps
    step_count = 0
    
    def callback(s):
        nonlocal step_count
        step_count += 1
        if step_count % 5 == 0:
            div_error = s.get_divergence_error()
            print(f"  Step {step_count}: t = {s.t()*1e24:.2f} × 10⁻²⁴ s, "
                  f"max|∇·v| = {div_error:.2e}")
    
    solver.run_until(t_end, callback)
    print()

    # Final statistics
    print("=" * 70)
    print("Simulation Complete")
    print("=" * 70)
    print(f"Total steps: {step_count}")
    print(f"Final time: {solver.t()*1e24:.2f} × 10⁻²⁴ s")
    print(f"Final divergence error: {solver.get_divergence_error():.2e}")
    print()

    # Access constants
    print("Constants:")
    print(f"  Speed of light: {sdt_navier_cpp.constants.C:.2e} m/s")
    print(f"  Deuteron binding energy (exp): {sdt_navier_cpp.constants.B_DEUTERON} MeV")
    print(f"  Deuteron magnetic moment (exp): {sdt_navier_cpp.constants.MU_D} μ_N")
    print()

if __name__ == "__main__":
    main()

