import math

# Constants
c = 2.99792458e8
e = 1.60217663e-19
epsilon_0 = 8.85418781e-12
h = 6.62607015e-34
hbar = h / (2 * math.pi)
m_e = 9.10938356e-31
m_p = 1.6726219e-27
alpha = 7.29735256e-3
a_0 = 5.291772109e-11
R_p = 0.8414e-15 # CODATA 2018

print(f"Target Gamma: 0.546")

# Hypothesis 1: v proportional to 1/sqrt(r) (Keplerian/Virial) from Bohr orbit
# v_bohr = alpha * c
v_bohr = alpha * c
v_at_Rp_kepler = v_bohr * math.sqrt(a_0 / R_p)
gamma_kepler = v_at_Rp_kepler / c
print(f"Hypothesis 1 (Keplerian scaling from a0): Gamma = {gamma_kepler:.4f} (v = {v_at_Rp_kepler:.2e})")

# Hypothesis 2: v proportional to 1/r (Angular momentum conservation)
v_at_Rp_angmom = v_bohr * (a_0 / R_p)
gamma_angmom = v_at_Rp_angmom / c
print(f"Hypothesis 2 (L conservation from a0): Gamma = {gamma_angmom:.4f} (v = {v_at_Rp_angmom:.2e})")

# Hypothesis 3: Escape velocity at Rp (Classical)
# v_esc = sqrt(2 * k_e * e^2 / (m * r)) ? No, potential is Coulomb.
# PE = e^2 / (4 * pi * eps * r)
# KE = PE (Virial) -> mv^2 = e^2 / (4 * pi * eps * r) -> v = sqrt(e^2 / (4 * pi * eps * m * r))
# For electron at Rp
v_virial_e = math.sqrt(e**2 / (4 * math.pi * epsilon_0 * m_e * R_p))
gamma_virial_e = v_virial_e / c
print(f"Hypothesis 3 (Virial v for electron at Rp): Gamma = {gamma_virial_e:.4f}")

# Hypothesis 4: Virial v for PROTON at Rp (self-energy?)
v_virial_p = math.sqrt(e**2 / (4 * math.pi * epsilon_0 * m_p * R_p))
gamma_virial_p = v_virial_p / c
print(f"Hypothesis 4 (Virial v for proton at Rp): Gamma = {gamma_virial_p:.4f}")

# Hypothesis 5: Geometric ratio involving Compton wavelength
lambda_c_p = h / (m_p * c)
ratio_lambda = R_p / lambda_c_p
print(f"Hypothesis 5 (Rp / Lambda_C_proton): {ratio_lambda:.4f}")

# Hypothesis 6: User said "decimal fraction of the orbital v at R_proton"
# Maybe they mean v/c IS the fraction?
# 0.546 is close to 1/2? Or sqrt(1/3)?
print(f"sqrt(1/3) = {math.sqrt(1/3):.4f}")
print(f"1/1.83 = {1/1.83:.4f}")

# Hypothesis 7: Fine structure constant relation?
# 0.546 / alpha = 74.8
# 0.546 * alpha = 0.0039

# Hypothesis 8: Proton magnetic moment related?
# mu_p = 2.79 * mu_N
# mu = e * v * r / 2
# 2.79 * (e hbar / 2 mp) = e * v * R_p / 2
# v = 2.79 * hbar / (m_p * R_p)
v_mag = 2.7928 * hbar / (m_p * R_p)
gamma_mag = v_mag / c
print(f"Hypothesis 8 (From Proton Magnetic Moment): Gamma = {gamma_mag:.4f}")
