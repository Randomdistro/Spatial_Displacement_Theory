import math

# Constants
c = 299792458.0
alpha_inv = 137.035999084
alpha = 1.0 / alpha_inv
R_H = 5.29177210903e-11 # Bohr Radius
R_inf = 10973731.568160 # Rydberg Constant

# Ground State (n=1)
v_1 = c * alpha
R_1 = R_H
freq_1 = (v_1 / R_1) / (2.0 * math.pi)

print(f"Ground State (n=1):")
print(f"  Radius: {R_1:.4e} m")
print(f"  Velocity: {v_1:.4e} m/s")
print(f"  Frequency: {freq_1:.4e} Hz")

# First Excitation (n=2)
n = 2
R_2 = R_1 * n**2
v_2 = v_1 / n
freq_2 = (v_2 / R_2) / (2.0 * math.pi)

print(f"\nFirst Excitation (n=2):")
print(f"  Radius: {R_2:.4e} m (4 * R_H)")
print(f"  Velocity: {v_2:.4e} m/s (v_1 / 2)")
print(f"  Frequency: {freq_2:.4e} Hz")

# Scaling Factor
ratio = freq_1 / freq_2
print(f"\nRatio f_1 / f_2: {ratio:.4f}") # Expect 8.0 (n^3)

# Relation to Rydberg
freq_Rydberg = R_inf * c
print(f"Ratio f_2 / Rydberg: {freq_2 / freq_Rydberg:.4f}") # Expect 0.25 (1/4)
