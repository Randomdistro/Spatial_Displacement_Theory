
import math

# Constants from code
beta_geom = 0.951
g_I = 5.5856946893
g_e = 2.00231930436
m_e_over_m_p = 5.44617021487e-4
m_e_c2_eV = 510998.9502
alpha = 1.0 / 137.035999084
h = 6.62607015e-34
e_charge = 1.602176634e-19
n = 1

# Calculation from code
prefactor = (8.0/3.0) * beta_geom * g_I * g_e * m_e_over_m_p
energy_joule = prefactor * alpha**4 * (m_e_c2_eV * e_charge) / (n**3)
frequency = energy_joule / h

print(f"Frequency: {frequency/1e6} MHz")

# Standard Fermi contact formula check (roughly)
# E_F = (4/3) * g_I * g_e * (me/mp) * alpha^4 * me*c^2
prefactor_std = (4.0/3.0) * g_I * g_e * m_e_over_m_p
energy_joule_std = prefactor_std * alpha**4 * (m_e_c2_eV * e_charge)
freq_std = energy_joule_std / h
print(f"Standard Formula Frequency (approx): {freq_std/1e6} MHz")

