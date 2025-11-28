import math

# Constants
c = 299792458.0
h = 6.62607015e-34
e_charge = 1.60217663e-19
m_e = 9.10938356e-31
epsilon_0 = 8.85418781e-12
k_c = 1.0 / (4.0 * math.pi * epsilon_0)

# Derived Constants
alpha = e_charge**2 / (4.0 * math.pi * epsilon_0 * h * c / (2*math.pi)) # Fine Structure
# Or just 1/137.035999
alpha_inv = 137.035999084
alpha = 1.0 / alpha_inv

R_H = 5.29177210903e-11 # Bohr Radius
E_Rydberg_J = 2.179872e-18 # 13.6 eV
E_Rydberg_eV = 13.605693

print(f"| n | Radius (m) | Rotation (Hz) | Energy (eV) | Coulomb Force (N) | Centripetal (N) | Lyman (nm) | Balmer (nm) |")
print(f"|---|---|---|---|---|---|---|---|")

for n in range(1, 10):
    # 1. Radius and Velocity
    R_n = R_H * n**2
    v_n = (c * alpha) / n
    
    # 2. Rotation Frequency (Tidal Lock)
    omega = v_n / R_n
    f_rot = omega / (2.0 * math.pi)
    
    # 3. Energy (Standard)
    E_n = -E_Rydberg_eV / n**2
    
    # 4. Forces
    F_coulomb = (k_c * e_charge**2) / R_n**2
    F_centripetal = (m_e * v_n**2) / R_n
    
    # 5. Wavelengths
    # Lyman (n -> 1)
    if n > 1:
        dE_Lyman = E_Rydberg_J * (1.0 - 1.0/n**2)
        lambda_Lyman = (h * c) / dE_Lyman
        lyman_str = f"{lambda_Lyman*1e9:.1f}"
    else:
        lyman_str = "-"
        
    # Balmer (n -> 2)
    if n > 2:
        dE_Balmer = E_Rydberg_J * (1.0/4.0 - 1.0/n**2)
        lambda_Balmer = (h * c) / dE_Balmer
        balmer_str = f"{lambda_Balmer*1e9:.1f}"
    else:
        balmer_str = "-"
        
    print(f"| {n} | {R_n:.2e} | {f_rot:.2e} | {E_n:.2f} | {F_coulomb:.2e} | {F_centripetal:.2e} | {lyman_str} | {balmer_str} |")
