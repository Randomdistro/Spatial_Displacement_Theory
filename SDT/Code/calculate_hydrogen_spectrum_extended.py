import math

# Constants
c = 299792458.0
h = 6.62607015e-34
e_charge = 1.60217663e-19
m_e = 9.10938356e-31
lambda_C = h / (m_e * c)
alpha_inv = 137.035999084
alpha = 1.0 / alpha_inv
R_H = 5.29177210903e-11
E_Rydberg_eV = 13.605693
epsilon_0 = 8.85418781e-12
k_c = 1.0 / (4.0 * math.pi * epsilon_0)

print(f"| n | Radius (m) | Rotation (Hz) | Energy (eV) | Force (N) | Lyman (nm) | Balmer (nm) | Delta L (m) |")
print(f"|---|---|---|---|---|---|---|---|")

# Range: 1-9, then 10, 20, 50, 100, 137
levels = list(range(1, 10)) + [10, 20, 50, 100, 137]

for n in levels:
    # 1. Radius and Velocity
    R_n = R_H * n**2
    v_n = (c * alpha) / n
    
    # 2. Rotation Frequency (Tidal Lock)
    omega = v_n / R_n
    f_rot = omega / (2.0 * math.pi)
    
    # 3. Energy
    E_n = -E_Rydberg_eV / n**2
    
    # 4. Forces
    F_coulomb = (k_c * e_charge**2) / R_n**2
    
    # 5. Length Deficit
    beta = v_n / c
    gamma = 1.0 / math.sqrt(1.0 - beta**2)
    L_n = lambda_C / gamma
    delta_L = lambda_C - L_n
    
    # 6. Wavelengths
    if n > 1:
        dE_Lyman = (E_Rydberg_eV * (1.0 - 1.0/n**2)) * e_charge
        lambda_Lyman = (h * c) / dE_Lyman
        lyman_str = f"{lambda_Lyman*1e9:.1f}"
    else:
        lyman_str = "-"
        
    if n > 2:
        dE_Balmer = (E_Rydberg_eV * (1.0/4.0 - 1.0/n**2)) * e_charge
        lambda_Balmer = (h * c) / dE_Balmer
        balmer_str = f"{lambda_Balmer*1e9:.1f}"
    else:
        balmer_str = "-"
        
    print(f"| {n} | {R_n:.2e} | {f_rot:.2e} | {E_n:.4f} | {F_coulomb:.2e} | {lyman_str} | {balmer_str} | {delta_L:.2e} |")
