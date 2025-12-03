
import math

# Constants from code
g_I = 5.5856946893
g_e = 2.00231930436
m_e_over_m_p = 5.44617021487e-4
m_e_c2_eV = 510998.9502
alpha = 1.0 / 137.035999084
h = 6.62607015e-34
e_charge = 1.602176634e-19
n = 1

# New Code Logic
reduced_mass_corr = 1.0 / ((1.0 + m_e_over_m_p)**3)
prefactor = (2.0/3.0) * g_I * g_e * m_e_over_m_p * reduced_mass_corr
energy_joule = prefactor * alpha**4 * (m_e_c2_eV * e_charge) / (n**3)
frequency = energy_joule / h

print(f"New Code Logic Frequency: {frequency/1e6} MHz")
print(f"Target: 1420.40575 MHz")
print(f"Error: {(frequency/1e6 - 1420.40575) / 1420.40575 * 100:.4f}%")

