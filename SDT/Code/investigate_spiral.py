import math

# Constants
c = 299792458.0
alpha_inv = 137.035999084
alpha = 1.0 / alpha_inv

# User Values
v_spin_e = 1.81 * c
v_spin_p = 1.8412 * c # Using the precise 1.8412 from previous turn
v_orb = c * alpha

print(f"Electron Spin: {v_spin_e:.4e} m/s (1.81c)")
print(f"Proton Spin: {v_spin_p:.4e} m/s (1.84c)")
print(f"Orbital Velocity: {v_orb:.4e} m/s (alpha * c)")

# 1. Geometric Interpretation (Spiral)
# If v_spiral = 1.81 * c and v_linear = c
# Then Path Ratio = 1.81
# Pitch Angle theta: cos(theta) = v_linear / v_spiral = 1 / 1.81
theta_e = math.acos(1.0 / 1.81)
theta_p = math.acos(1.0 / 1.8412)

print(f"Electron Spiral Angle: {math.degrees(theta_e):.4f} degrees")
print(f"Proton Spiral Angle: {math.degrees(theta_p):.4f} degrees")

# 2. Movement Budget (Total Energy)
# If Energy ~ v^2
# E_total = E_linear + E_spin?
# Or is E_total fixed at c^2?
# Maybe the "1.81c" is the Phase Velocity?
# v_phase * v_group = c^2?
# If v_phase = 1.81c, then v_group = c / 1.81
v_group_e = c / 1.81
v_group_p = c / 1.8412

print(f"Electron Group Velocity (if Phase=1.81c): {v_group_e:.4e} m/s ({1/1.81:.4f} c)")
print(f"Proton Group Velocity (if Phase=1.84c): {v_group_p:.4e} m/s ({1/1.8412:.4f} c)")

# 3. Rod Appearance
# To Itself: Stationary Rod.
# To Us (at 1.81c?):
# If it's a spiral, it looks like a Toroid or Shell.
# The "Combined Total"
# Maybe vector sum?
# v_total = sqrt(v_spin^2 + v_orb^2)
v_total_e = math.sqrt(v_spin_e**2 + v_orb**2)
print(f"Combined Total Velocity (Electron): {v_total_e:.4e} m/s ({v_total_e/c:.4f} c)")

# 4. Check 1.8412 vs 1.81
# Ratio
print(f"Ratio Proton/Electron Spin: {1.8412 / 1.81:.4f}") # ~1.017
