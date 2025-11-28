import math

# Constants
c = 299792458.0
h = 6.62607015e-34
m_e = 9.10938356e-31
R_p = 0.841235667e-15 # Proton Radius
lambda_C = h / (m_e * c) # Compton Wavelength
alpha_inv = 137.035999084
alpha = 1.0 / alpha_inv
R_H = 5.29177210903e-11

print(f"Compton Wavelength (Rest Length?): {lambda_C:.4e} m")
print(f"Proton Radius (Contracted Length?): {R_p:.4e} m")

# 1. Gamma at Proton Surface
# If L_contracted = R_p
gamma_p = lambda_C / R_p
print(f"Gamma required for Sphere at R_p: {gamma_p:.4f}")

# 2. Length at Bohr Radius (n=1)
v_1 = c * alpha
gamma_1 = 1.0 / math.sqrt(1.0 - (v_1/c)**2)
L_1 = lambda_C / gamma_1
print(f"Length at R_H (n=1): {L_1:.4e} m")
print(f"  Contraction Factor: {gamma_1:.8f}")

# 3. Length at Excitation States
print(f"\n| n | Velocity (c) | Gamma | Length (m) | Ratio to R_p |")
print(f"|---|---|---|---|---|")

for n in range(1, 10):
    v_n = (c * alpha) / n
    beta = v_n / c
    gamma_n = 1.0 / math.sqrt(1.0 - beta**2)
    L_n = lambda_C / gamma_n
    ratio = L_n / R_p
    print(f"| {n} | {beta:.2e} | {gamma_n:.8f} | {L_n:.4e} | {ratio:.1f} |")

# 4. De Broglie Wavelength Comparison
lambda_dB_1 = h / (m_e * v_1)
print(f"\nDe Broglie Wavelength at n=1: {lambda_dB_1:.4e} m")
print(f"Ratio De Broglie / Compton: {lambda_dB_1 / lambda_C:.4f}") # Should be 137
