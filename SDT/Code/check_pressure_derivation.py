import math

# Constants
c = 2.99792458e8
e = 1.60217663e-19
epsilon_0 = 8.85418781e-12
h = 6.62607015e-34
hbar = h / (2 * math.pi)
m_p = 1.6726219e-27
E_p_J = m_p * c**2
R_p = 0.8414e-15
alpha = 7.29735256e-3

Target_P = 1.65e31

print(f"Target Pressure: {Target_P:.2e} Pa")

# 1. Proton Mass Energy Density (Spherical)
V_sphere = (4/3) * math.pi * R_p**3
rho_E_sphere = E_p_J / V_sphere
print(f"1. Mass Energy Density (Sphere): {rho_E_sphere:.2e} Pa")
print(f"   Ratio (Target/Density): {Target_P/rho_E_sphere:.4e}")
print(f"   Alpha factor? {rho_E_sphere * alpha:.2e} (Ratio: {Target_P/(rho_E_sphere*alpha):.2f})")
print(f"   Alpha/4 factor? {rho_E_sphere * alpha / 4:.2e} (Ratio: {Target_P/(rho_E_sphere*alpha/4):.2f})")

# 2. Proton Mass Energy Density (Toroidal)
# Assume R_major = R_p, r_minor = R_p/3? Or R_p?
# If tube radius = R_p (horn torus): V = 2 * pi^2 * R_p^3
V_torus = 2 * math.pi**2 * R_p**3
rho_E_torus = E_p_J / V_torus
print(f"2. Mass Energy Density (Torus, r=R): {rho_E_torus:.2e} Pa")
print(f"   Ratio (Target/Density): {Target_P/rho_E_torus:.4e}")

# 3. Coulomb Energy Density at Surface
# u = epsilon_0 * E^2 / 2
E_field = e / (4 * math.pi * epsilon_0 * R_p**2)
u_coulomb = 0.5 * epsilon_0 * E_field**2
print(f"3. Coulomb Energy Density (Surface): {u_coulomb:.2e} Pa")
print(f"   Ratio (Target/Coulomb): {Target_P/u_coulomb:.4f}")

# 4. Spation Yield Stress?
# P_planck = c^7 / (hbar * G^2) ... no G in SDT.
# K_bulk = 4.6e113
# P = K_bulk * (R_planck / R_p)^4 ?
R_planck = 1.616e-35
P_scaled = 4.6e113 * (R_planck / R_p)**4
print(f"4. Planck Scaling (r^-4): {P_scaled:.2e} Pa")

# 5. User's "Charge Value" hint
# Maybe P_infinity is related to the "Charge Pressure"?
# P = Q / Area? No, units.
# P = Force / Area.
# F_coulomb at R_p?
F_c = e**2 / (4 * math.pi * epsilon_0 * R_p**2)
P_force = F_c / (math.pi * R_p**2) # Pressure on cross section?
print(f"5. Coulomb Pressure (F/A): {P_force:.2e} Pa")
print(f"   Ratio (Target/P_force): {Target_P/P_force:.4f}")

# 6. Check specific ratio 1.65e31 / u_coulomb
# u_coulomb was 1.96e32
# Ratio is ~0.084
# 0.084 is close to 1/12? (0.0833)
print(f"   Is it u_coulomb / 12? {u_coulomb/12:.2e}")
