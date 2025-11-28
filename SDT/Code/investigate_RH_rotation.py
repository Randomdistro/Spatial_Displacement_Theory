import math

# Constants
c = 299792458.0
alpha_inv = 137.035999084
alpha = 1.0 / alpha_inv
R_H = 5.29177210903e-11 # Bohr Radius
R_inf = 10973731.568160 # Rydberg Constant

print(f"Bohr Radius (R_H): {R_H:.4e} m")

# 1. Orbital Velocity at R_H
v_orb = c * alpha
print(f"Orbital Velocity (alpha * c): {v_orb:.4e} m/s")

# 2. Rotation Frequency (Tidally Locked)
# omega = v / r
omega_H = v_orb / R_H
freq_H = omega_H / (2.0 * math.pi)

print(f"Angular Velocity (omega): {omega_H:.4e} rad/s")
print(f"Frequency (Hz): {freq_H:.4e} Hz")
print(f"Period (s): {1.0/freq_H:.4e} s")

# 3. Compare to Rydberg Frequency
freq_Rydberg = R_inf * c
print(f"Rydberg Frequency (R_inf * c): {freq_Rydberg:.4e} Hz")
print(f"Ratio freq_H / freq_Rydberg: {freq_H / freq_Rydberg:.4f}") # Expect 2.0

# 4. Compare to Proton Surface Rotation
freq_p = 1.04e23
print(f"Ratio freq_p / freq_H: {freq_p / freq_H:.4e}")
