import sys
import os
import numpy as np

# Add current directory to path
sys.path.append(os.getcwd())

print("Testing SDT Core Imports...")
try:
    from sdt_core.constants import CELESTIAL_BODIES, RHO_S
    from sdt_core.physics import compute_acceleration_particle, compute_navier_forces
    print("SUCCESS: sdt_core imported.")
except Exception as e:
    print(f"FAILURE: sdt_core import failed: {e}")
    sys.exit(1)

print("\nTesting Core Physics Logic...")
# Test Particle Acceleration (Phase 15)
# a = c^2 * R_eff / (Kappa^2 * r^2)
c = 299792458.0
r_eff = 1.0
kappa = 1.0
r_vec = np.array([1.0, 0.0, 0.0])
dist = 1.0

# Expected: a = c^2 * 1 / (1^2 * 1^2) = c^2
# Direction: [1, 0, 0]
expected_accel = np.array([c**2, 0.0, 0.0])

accel = compute_acceleration_particle(r_eff, kappa, r_vec, dist)

if np.allclose(accel, expected_accel):
    print("SUCCESS: compute_acceleration_particle correct.")
else:
    print(f"FAILURE: compute_acceleration_particle incorrect. Got {accel}, expected {expected_accel}")

# Test Navier Forces
grad_P = np.zeros((1,1,1,3))
F_curv = np.zeros((1,1,1,3))
F_slip = np.zeros((1,1,1,3))
v_advect = np.zeros((1,1,1,3))
rho_s = 1.0
dv_dt = compute_navier_forces(grad_P, F_curv, F_slip, v_advect, rho_s)
if np.allclose(dv_dt, np.zeros((1,1,1,3))):
    print("SUCCESS: compute_navier_forces correct (trivial case).")
else:
    print(f"FAILURE: compute_navier_forces incorrect.")

print("\nTesting Refactored Modules Imports...")
try:
    import sdt_navier.equations
    print("SUCCESS: sdt_navier.equations imported.")
except Exception as e:
    print(f"FAILURE: sdt_navier.equations import failed: {e}")

try:
    with open('pressure kernel.py', 'r') as f:
        content = f.read()
        if 'from sdt_core.constants import CELESTIAL_BODIES' in content:
            print("SUCCESS: pressure kernel.py has correct imports.")
        else:
            print("FAILURE: pressure kernel.py missing imports.")
except Exception as e:
    print(f"FAILURE: checking pressure kernel.py failed: {e}")

print("\nVerification Complete.")
