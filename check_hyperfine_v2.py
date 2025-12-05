
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
beta_geom = 0.951

# Standard Fermi Contact (Textbook)
# nu = (4/3) * g_I * g_e * (me/mp) * alpha^4 * (me*c^2 / h) * (correction?)
# g_I here is 5.58 (proton g-factor)
# g_e is 2.002
# Spin of proton I = 1/2.
# Factor is 4/3 for Hydrogen 1S.
# Let's check this exact calculation.

c = 299792458
R_inf = 10973731.568160 # m^-1
# Ry = R_inf * c
Ry_Hz = R_inf * c

# Frequency from formula:
# nu = (4/3) * g_I * g_e * (m_e/m_p) * alpha^2 * Ry * c ... wait
# Let's use the energy formula:
# E = (4/3) * g_I * g_e * (m_e/m_p) * alpha^4 * m_e * c^2
prefactor_std = (4.0/3.0) * g_I * g_e * m_e_over_m_p
energy_joule_std = prefactor_std * alpha**4 * (m_e_c2_eV * e_charge)
freq_std = energy_joule_std / h

print(f"Standard Formula (4/3, no beta): {freq_std/1e6} MHz")

# Code uses 8/3 and beta_geom = 0.951
prefactor_code = (8.0/3.0) * beta_geom * g_I * g_e * m_e_over_m_p
freq_code = (prefactor_code * alpha**4 * (m_e_c2_eV * e_charge)) / h
print(f"Code Formula (8/3, beta=0.951): {freq_code/1e6} MHz")

# Hypothesis: beta should be 1/0.951 and factor 4/3?
# Or maybe the code's beta_geom is applied incorrectly?
# If we want 1420.4:
factor_needed = 1420.40575 / (freq_std/1e6)
print(f"Factor needed relative to Standard: {factor_needed}")

# 1420.4 is approx half of 2845.
# Is it possible g_I should be 2.79?
# g_p = 5.58. mu_p = 2.79 mu_N.
# In the formula, is it g_I or mu_I/mu_N?
# Usually written as g_p.

# If we use 2.79 instead of 5.58 in Standard:
freq_half_g = freq_std * (2.79284735 / 5.5856946893)
print(f"Standard with g_I=2.79: {freq_half_g/1e6} MHz")


