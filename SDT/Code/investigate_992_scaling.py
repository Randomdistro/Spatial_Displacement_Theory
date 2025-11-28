import math

# Constants
c = 299792458.0
h = 6.62607015e-34
e_charge = 1.60217663e-19
epsilon_0 = 8.85418781e-12
m_e = 9.10938356e-31
m_p = 1.6726219e-27
m_n = 1.674927471e-27
alpha_inv = 137.035999

# User Values
factor_7_6 = 7.6
factor_992_4 = 992.4

print(f"Investigating Scaling Factor: {factor_992_4}")
print(f"EM Factor: {factor_7_6}")
print("-" * 30)

# 1. Check Mass Ratios
ratio_p_e = m_p / m_e
print(f"Proton/Electron Mass Ratio: {ratio_p_e:.4f}")
print(f"  Ratio / 992.4: {ratio_p_e / factor_992_4:.4f}")
print(f"  Ratio / 7.6: {ratio_p_e / factor_7_6:.4f}")

# 2. Check Alpha
print(f"Alpha Inverse: {alpha_inv:.4f}")
print(f"  992.4 / Alpha Inv: {factor_992_4 / alpha_inv:.4f}")
print(f"  Alpha Inv * 7.6: {alpha_inv * factor_7_6:.4f}") # ~1041

# 3. Check 7.6 relation to 992.4
print(f"992.4 / 7.6: {factor_992_4 / factor_7_6:.4f}") # ~130.5
# Is 130.5 significant? Close to 137?

# 4. Check Powers of c
# Unitary Length L_u = 1/c^4
L_u = 1.0 / c**4
print(f"Unitary Length (1/c^4): {L_u:.4e}")

# Maybe the "Neutrino" mass relates to m_e via 992.4?
# m_e / 992.4
m_scaled = m_e / factor_992_4
print(f"Electron Mass / 992.4: {m_scaled:.4e} kg")
# Convert to eV
E_scaled_eV = (m_scaled * c**2) / e_charge
print(f"  Energy (eV): {E_scaled_eV:.4f} eV")
# Neutrino mass is < 0.12 eV. This is ~515 eV. Too high for neutrino?
# Maybe m_e / (992.4^2)?
E_scaled_2 = E_scaled_eV / factor_992_4
print(f"  Energy / 992.4 (eV): {E_scaled_2:.4f} eV") # ~0.5 eV. CLOSE to Neutrino limit!

# 5. Check "Proton" scaling
m_p_scaled = m_p / factor_992_4
E_p_scaled = (m_p_scaled * c**2) / e_charge
print(f"Proton Mass / 992.4 (eV): {E_p_scaled:.4e} eV") # ~1 MeV?
print(f"  Value: {E_p_scaled / 1e6:.4f} MeV") # ~945 MeV / 1000 = 0.94 MeV.
# Neutron - Proton mass diff is 1.29 MeV.
# Electron mass is 0.511 MeV.
# 938 MeV / 992.4 = 0.945 MeV.
# This is almost exactly 2 * m_e (1.02 MeV)? Or close to Neutron-Proton diff?

# 6. Check 992.4 vs 1000 (Metric?)
# No, user said "oh no way", implies physics match.

# 7. Check 31.5^2
print(f"Sqrt(992.4): {math.sqrt(factor_992_4):.4f}") # 31.50

# 8. Check 7.6^3?
print(f"7.6^3: {factor_7_6**3:.4f}") # 438
print(f"7.6^3.3: {factor_7_6**3.3:.4f}")

# 9. Check c scaling
# c / 992.4?
print(f"c / 992.4: {c / factor_992_4:.4f}") # ~300,000

