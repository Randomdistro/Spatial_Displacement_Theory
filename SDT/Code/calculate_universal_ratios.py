import math

# Constants
c = 299792458.0
h = 6.62607015e-34
m_e = 9.10938356e-31
e_charge = 1.60217663e-19
epsilon_0 = 8.85418781e-12
alpha_inv = 137.035999084
alpha = 1.0 / alpha_inv

# Base Units (The "Unitary" System?)
# User wants "ratio scale whereby this can all be expressed as a constant".
# Maybe Base Length = Compton Wavelength? Or Planck Length?
# Or Base Length = Classical Electron Radius?
# Let's try normalizing to the c-boundary (r_e) and c.

L_base = 2.8179403227e-15 # r_e
T_base = L_base / c
M_base = m_e

print(f"Base Units (c-Boundary Normalization):")
print(f"L_0 = {L_base:.4e} m (r_e)")
print(f"T_0 = {T_base:.4e} s")
print(f"V_0 = c")

print(f"\n| System | Radius (L/L_0) | Velocity (v/c) | Rotation (f * T_0) | Energy (E / m c^2) |")
print(f"|---|---|---|---|---|")

# Proton Surface
R_p = 0.8412e-15
v_p = c * math.sqrt(L_base / R_p)
f_p = v_p / R_p
E_p_rot = 0.5 * m_e * v_p**2 # Classical approx

print(f"| Proton | {R_p/L_base:.4f} | {v_p/c:.4f} | {f_p * T_base:.4f} | {E_p_rot / (m_e*c**2):.4f} |")

# c-Boundary
print(f"| c-Bound | 1.0000 | 1.0000 | {1.0 / (2*math.pi):.4f} | 0.5000 |")

# Hydrogen Ground (n=1)
R_H = 5.2918e-11
v_1 = c * alpha
f_1 = v_1 / R_H
E_1 = -13.6 * 1.6e-19

print(f"| H (n=1) | {R_H/L_base:.4e} | {alpha:.4e} | {f_1 * T_base:.4e} | {E_1 / (m_e*c**2):.4e} |")

# Solar System (Earth)
R_earth = 1.496e11
v_earth = 29780
print(f"| Earth | {R_earth/L_base:.4e} | {v_earth/c:.4e} | {(v_earth/R_earth) * T_base:.4e} | - |")
