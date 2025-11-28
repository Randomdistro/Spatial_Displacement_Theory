
import sys
import os
import numpy as np
import json
import time

print("Starting Poincaré Experiment Script...", flush=True)

# Add SDT/Code to path to import sdt_navier
# File is in SDT/investigations/millennium_problems/poincare_conjecture/experiments/
# We need to go up 5 levels to get to SDT, then add Code
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
code_path = os.path.join(root_path, "Code")
print(f"Adding to path: {code_path}", flush=True)
sys.path.append(code_path)

try:
    from sdt_navier.fields import initialize_fields, add_turbine_source, compute_diversion_density
    from sdt_navier.equations import SDTNavierEquations
    from sdt_navier.solver import SDTNavierSolver
    print("Successfully imported sdt_navier", flush=True)
except ImportError as e:
    print(f"Failed to import sdt_navier: {e}", flush=True)
    sys.exit(1)

def run_simply_connected_scenario(output_dir):
    """
    Scenario A: Simply Connected Region
    Initialize with random pressure perturbations but no matter (no turbine cells).
    Expectation: Pressure gradients smooth out, returning to uniform P_CMB (3-sphere).
    """
    print("Running Scenario A: Simply Connected Region...")
    
    nx, ny, nz = 32, 32, 32
    dx = 1.0e-15  # Femtometer scale
    
    # Initialize with constant background
    fields = initialize_fields(nx, ny, nz, dx)
    
    # Add random pressure perturbations (noise)
    # This represents a "deformed" but simply connected region
    # Reduce noise to avoid numerical explosion
    noise_level = 1.0e-5 * fields.P[0,0,0]
    np.random.seed(42)
    fields.P += np.random.normal(0, noise_level, fields.P.shape)
    
    # No turbine sources added -> Simply Connected
    
    # Setup solver
    equations = SDTNavierEquations()
    # Use smaller CFL for stability
    solver = SDTNavierSolver(fields, equations, cfl=0.1)
    
    # Track pressure variance
    history = []
    
    t_end = 1.0e-24  # Very short time scale for relaxation
    steps = 20
    dt_step = t_end / steps
    
    initial_variance = np.var(fields.P)
    print(f"Initial Pressure Variance: {initial_variance:.4e}")
    
    for i in range(steps):
        try:
            solver.run_until(solver.t + dt_step)
        except Exception as e:
            print(f"Simulation failed at step {i}: {e}")
            break
        
        variance = np.var(fields.P)
        max_v = np.max(np.abs(fields.v))
        
        # Check for NaN
        if np.isnan(variance) or np.isnan(max_v):
            print("NaN detected! Stopping simulation.")
            break

        history.append({
            "step": i,
            "time": solver.t,
            "pressure_variance": float(variance),
            "max_velocity": float(max_v)
        })
        
        if i % 5 == 0:
            print(f"Step {i}: Var(P)={variance:.4e}, Max(v)={max_v:.4e}")

    final_variance = np.var(fields.P)
    print(f"Final Pressure Variance: {final_variance:.4e}")
    
    # Result: Did it relax?
    # Handle NaN case
    if np.isnan(final_variance):
        relaxed = False
    else:
        relaxed = final_variance < 0.9 * initial_variance # Just check if it decreased
    
    result = {
        "scenario": "A_simply_connected",
        "relaxed": bool(relaxed),
        "initial_variance": float(initial_variance),
        "final_variance": float(final_variance) if not np.isnan(final_variance) else None,
        "history": history
    }
    
    with open(os.path.join(output_dir, "scenario_a_results.json"), "w") as f:
        json.dump(result, f, indent=2)
        
    return result

def run_proton_scenario(output_dir, velocity_factor=1.0):
    """
    Scenario B: Proton (Toroidal Vortex)
    Initialize with a stable turbine cell (proton).
    Expectation: Structure persists (topology prevented from relaxing to 3-sphere).
    
    velocity_factor: Scale factor for circulation to test 1.84c condition.
    """
    print(f"Running Scenario B: Proton (Turbine Cell) with factor {velocity_factor}...")
    
    nx, ny, nz = 32, 32, 32
    dx = 1.0e-16  # Finer scale for proton
    
    fields = initialize_fields(nx, ny, nz, dx)
    
    # Add Proton Turbine
    # Radius ~ 0.84 fm = 8.4e-16 m
    # dx = 1e-16 -> Radius ~ 8.4 cells
    proton_radius_cells = 8.4
    
    # Standard parameters
    kappa_val = 1.0e15 # 1/m approx
    gamma_val = 0.546 * velocity_factor # Standard circulation * factor
    eta_val = 0.0003 # Low slip for stability
    
    center = (nx//2, ny//2, nz//2)
    add_turbine_source(
        fields, 
        center, 
        proton_radius_cells, 
        kappa_val, 
        gamma_val, 
        eta_val,
        profile="gaussian"
    )
    
    # Setup solver
    equations = SDTNavierEquations()
    solver = SDTNavierSolver(fields, equations, cfl=0.5)
    
    # Track stability
    history = []
    
    # Run for characteristic time
    # tau = R/c ~ 1e-23 s
    t_end = 2.0e-24  # Shorter simulation window to capture dynamics before instability
    steps = 100      # More steps for finer resolution
    dt_step = t_end / steps
    
    # Measure "structure" via energy density or curvature integral
    initial_energy = np.sum(fields.e)
    print(f"Initial Energy: {initial_energy:.4e}")
    
    # Use extremely conservative CFL for stability with high curvature
    solver.cfl = 0.01 
    
    for i in range(steps):
        try:
            solver.run_until(solver.t + dt_step)
        except Exception as e:
            print(f"Simulation failed at step {i}: {e}")
            break
            
        energy = np.sum(fields.e)
        max_v = np.max(np.abs(fields.v))
        max_kappa = np.max(fields.kappa)
        
        if np.isnan(energy) or np.isnan(max_v):
            print("NaN detected! Stopping simulation.")
            break
        
        history.append({
            "step": i,
            "time": solver.t,
            "total_energy": float(energy),
            "max_velocity": float(max_v),
            "max_kappa": float(max_kappa)
        })
        
        if i % 10 == 0:
            print(f"Step {i}: E={energy:.4e}, Max(v)={max_v:.4e}, Max(k)={max_kappa:.4e}")

    final_energy = np.sum(fields.e)
    print(f"Final Energy: {final_energy:.4e}")
    
    # Result: Did it persist?
    if np.isnan(final_energy):
        persisted = False
    else:
        persisted = final_energy > 0.5 * initial_energy
    
    result = {
        "scenario": f"B_proton_factor_{velocity_factor}",
        "velocity_factor": velocity_factor,
        "persisted": bool(persisted),
        "initial_energy": float(initial_energy),
        "final_energy": float(final_energy),
        "history": history
    }
    
    filename = f"scenario_b_results_{velocity_factor}.json"
    with open(os.path.join(output_dir, filename), "w") as f:
        json.dump(result, f, indent=2)
        
    return result

def main():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 1. Run Simply Connected Case
    res_a = run_simply_connected_scenario(output_dir)
    
    # 2. Run Proton Case (Standard)
    res_b_std = run_proton_scenario(output_dir, velocity_factor=1.0)
    
    # 3. Run Proton Case (1.84c Condition)
    # Testing the user's specific query about 1.84c
    # We interpret this as a velocity/circulation factor or related condition
    res_b_184 = run_proton_scenario(output_dir, velocity_factor=1.84) # 1.84 * c or relative scaling
    
    print("\nSummary:")
    print(f"Scenario A (Simply Connected): Relaxed? {res_a['relaxed']}")
    print(f"Scenario B (Proton 1.0c): Persisted? {res_b_std['persisted']}")
    print(f"Scenario B (Proton 1.84c): Persisted? {res_b_184['persisted']}")

if __name__ == "__main__":
    main()

