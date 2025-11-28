import math

# Constants
c = 299792458.0
m_e = 9.10938356e-31
m_p = 1.6726219e-27
r_p = 0.84e-15 # Proton Radius
e_charge = 1.60217663e-19
epsilon_0 = 8.85418781e-12

# User Values
v_spin_p = 1.8412 * c
v_spin_e = 1.81 * c
v_spin_n = 1.825 * c # "1.82 or 1.83"

print(f"Proton Spin: {v_spin_p:.4e} m/s")
print(f"Electron Spin: {v_spin_e:.4e} m/s")
print(f"Neutron Spin (Est): {v_spin_n:.4e} m/s")

# 1. Binding Force Calculation
# User says > 2 Million Newtons.
# Let's check Centripetal Force of the Electron inside the Neutron.
# v = c (approx)
# r = r_p (0.84 fm)
# gamma = 4082 (from previous calc)

gamma = 4082.0
v_rel = c # Electron speed inside
F_centripetal = (gamma * m_e * v_rel**2) / r_p
print(f"Centripetal Force (Gamma=4082): {F_centripetal:.4e} N") # ~400,000 N

# What if gamma is higher?
# Or what if mass is higher (effective mass)?
# User mentioned "Self Occlusion".
# Maybe F = P_nuc * Area?
P_nuc = 1.65e31
Area_p = math.pi * r_p**2
F_pressure = P_nuc * Area_p
print(f"Pressure Force (P_nuc * Area): {F_pressure:.4e} N") # ~36 N.

# What if the "2 Million Newtons" is the Coulomb Force at a smaller scale?
# F = k * e^2 / r^2
k_c = 1.0 / (4.0 * math.pi * epsilon_0)
F_coulomb = (k_c * e_charge**2) / r_p**2
print(f"Coulomb Force at Proton Radius: {F_coulomb:.4e} N") # ~330 N.

# To get 2 Million Newtons from Coulomb:
# r_sq = k * e^2 / 2e6
r_target = math.sqrt((k_c * e_charge**2) / 2.0e6)
print(f"Radius for 2 MN Coulomb Force: {r_target:.4e} m") # ~10^-17 m.

# 2. Neutron Rotation (Weighted Average?)
# Does the Neutron spin match the weighted average of P and e?
# (m_p * v_p + m_e * v_e) / (m_p + m_e)?
v_weighted = (m_p * v_spin_p + m_e * v_spin_e) / (m_p + m_e)
print(f"Weighted Average Velocity: {v_weighted:.4e} m/s ({v_weighted/c:.4f} c)")
# This is dominated by Proton (1.84c).
# User says 1.82 or 1.83.
# This implies the Electron has a HUGE drag effect (effective mass?).
# If v_n = 1.825c, what is the effective electron mass?
# m_p * v_p + m_eff * v_e = (m_p + m_eff) * v_n
# m_p(v_p - v_n) = m_eff(v_n - v_e)
# m_eff = m_p * (v_p - v_n) / (v_n - v_e)

v_n_target = 1.825 * c
m_eff = m_p * (v_spin_p - v_n_target) / (v_n_target - v_spin_e)
print(f"Effective Electron Mass for 1.825c: {m_eff:.4e} kg")
print(f"  Ratio m_eff / m_p: {m_eff / m_p:.4f}") # ~1.0?
# This implies the Electron has the SAME effective mass as the Proton inside the Neutron?
