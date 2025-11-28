import math

# Constants
c = 2.99792458e8
h = 6.62607015e-34
hbar = h / (2 * math.pi)
e = 1.60217663e-19
mu_N = 5.050783699e-27 # Nuclear magneton
m_p_exp = 1.6726219e-27
E_p_exp_J = m_p_exp * c**2
E_p_exp_MeV = E_p_exp_J / e / 1e6
mu_p_exp = 2.79284735 * mu_N

# SDT Parameters
R_p = 0.8414e-15 # Standard
Gamma_p = 0.546 # Derived from 1/1.8412
P_infinity = 1.65e31 # Scaled
eta_p = 1 - 0.9997 # Traction = 0.9997

# Derived Geometric Parameters
A_p = math.pi * R_p**2
kappa_p = 1 / R_p
tau_p = R_p / c

print(f"--- Proton Consistency Check ---")
print(f"Inputs:")
print(f"  R_p = {R_p} m")
print(f"  Gamma_p = {Gamma_p}")
print(f"  P_infinity = {P_infinity} Pa")
print(f"  Traction (1-eta) = {1-eta_p}")

# 1. Mass Calculation
# E_dot = P * A * Gamma * kappa * (1-eta)
# E = E_dot * tau
E_dot_calc = P_infinity * A_p * Gamma_p * kappa_p * (1-eta_p)
E_calc_J = E_dot_calc * tau_p
E_calc_MeV = E_calc_J / e / 1e6

print(f"\nMass Calculation:")
print(f"  Calc E_p = {E_calc_MeV:.2f} MeV")
print(f"  Exp E_p  = {E_p_exp_MeV:.2f} MeV")
ratio_mass = E_calc_MeV / E_p_exp_MeV
print(f"  Ratio (Calc/Exp) = {ratio_mass:.4f}")

# Note: The document mentions a "Geometric Correction Factor" of ~2.26.
# "Discrepancy factor: 938.272/415.0 = 2.261 (geometric correction for toroidal vs spherical)"
# Let's see if we get 415 MeV.

# 2. Magnetic Moment Calculation
# mu = q * v * r / 2
# v = Gamma * c ? Or v_surface?
# Document says: mu propto A^1/2 * Gamma * (1-eta)
# Formula 6.1: mu = q * v * r / 2
# Formula 6.3: mu_p = g_p * mu_N
# Formula 6.4: g_p = (Gamma_p * (1-eta_p) / (Gamma_Dirac * (1-eta_Dirac))) * 2
# Gamma_Dirac = ? Document says 0.195?
# Let's check the document's claim: g_p = 5.60

Gamma_Dirac = 0.195 # From document
eta_Dirac = 0 # From document (1-eta = 1.0)

g_p_calc = (Gamma_p * (1-eta_p) / (Gamma_Dirac * (1.0))) * 2
print(f"\nMagnetic Moment Calculation:")
print(f"  Calc g_p = {g_p_calc:.4f}")
print(f"  Exp g_p  = 5.586")
ratio_moment = g_p_calc / 5.586
print(f"  Ratio (Calc/Exp) = {ratio_moment:.4f}")

# 3. Consistency Verdict
if 0.9 < ratio_mass < 1.1 and 0.9 < ratio_moment < 1.1:
    print(f"\nVerdict: CONSISTENT (within 10%)")
elif abs(ratio_mass - 1) > 0.5:
    print(f"\nVerdict: INCONSISTENT (Mass off by factor {ratio_mass:.2f})")
else:
    print(f"\nVerdict: MIXED")
