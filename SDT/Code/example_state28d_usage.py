"""
Example: Using State28D in Investigation Scripts

Demonstrates how to integrate the 28-dimensional state vector
into existing SDT investigation workflows.
"""

import sys
sys.path.insert(0, '.')

from sdt_core import State28D, validate_force_hierarchy

# Quick validation
print("=== Quick Force Hierarchy Validation ===")
validate_force_hierarchy()
print()

# Detailed usage example
print("=== Detailed Example: Atomic Calculations ===")

# Create electron and proton states
electron = State28D.electron_atomic()
proton = State28D.proton_nuclear()

print(f"Electron T₃ (surface): {electron.T_3:.3e} m²")
print(f"Proton T₃ (surface):   {proton.T_3:.3e} m²")
print()

# Calculate occlusion at different scales
bohr_radius = 5.29e-11  # Bohr radius [m]
E_atomic = electron.calculate_occlusion(proton, bohr_radius)

print(f"Occlusion E at Bohr radius: {E_atomic:.3e}")
print(f"This gives Coulomb regime (E ≈ 0)")
print()

# Phase space calculation (Φ₄)
electron.Phi_4 = 2.2  # Excited state with log(9) substates
phase_space = electron.accessible_phase_space_volume()
print(f"Accessible phase space Φ₄: {phase_space:.2f}")
print()

# Export to numpy for numerical integration
state_vector = electron.to_array()
print(f"28D state vector shape: {state_vector.shape}")
print(f"First 5 components: {state_vector[:5]}")
