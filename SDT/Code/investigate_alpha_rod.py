import math

# Constants
c = 299792458.0
alpha_inv = 137.035999084
alpha = 1.0 / alpha_inv
v = c * alpha

# 1. Lorentz Factor
beta = v / c
gamma = 1.0 / math.sqrt(1.0 - beta**2)

print(f"Velocity: {v:.4e} m/s (c/137)")
print(f"Beta: {beta:.8f}")
print(f"Gamma: {gamma:.8f}")

# 2. Target Scale: 10^-21 to 10^-22 m
L_observed = 1.0e-21

# Standard Contraction: L_obs = L_rest / gamma
L_rest_std = L_observed * gamma
print(f"Standard Rest Length (if L_obs = 10^-21): {L_rest_std:.4e} m")
# Since gamma ~ 1, L_rest ~ L_obs. This is boring.

# 3. Alternative Scaling?
# Maybe the user implies L_obs = L_rest * alpha? (Or alpha^2?)
L_rest_alpha = L_observed / alpha
L_rest_alpha2 = L_observed / alpha**2
L_rest_alpha3 = L_observed / alpha**3
L_rest_alpha4 = L_observed / alpha**4

print(f"L_rest if scaled by Alpha (L/a): {L_rest_alpha:.4e} m")
print(f"L_rest if scaled by Alpha^2 (L/a^2): {L_rest_alpha2:.4e} m") # ~10^-17
print(f"L_rest if scaled by Alpha^3 (L/a^3): {L_rest_alpha3:.4e} m") # ~10^-15 (Proton?)
print(f"L_rest if scaled by Alpha^4 (L/a^4): {L_rest_alpha4:.4e} m") # ~10^-13
print(f"L_rest if scaled by Alpha^5 (L/a^5): {L_rest_alpha4 / alpha:.4e} m") # ~10^-11 (Compton?)

# Check Compton Wavelength
L_Compton = 2.426e-12
print(f"Electron Compton Wavelength: {L_Compton:.4e} m")

# Ratio Compton / 10^-21
ratio = L_Compton / L_observed
print(f"Ratio Compton / 10^-21: {ratio:.4e}")
# Log base alpha of ratio
log_alpha = math.log(ratio) / math.log(alpha)
print(f"Power of Alpha (Compton -> 10^-21): {log_alpha:.4f}") # Expect ~4 or 5?

# 4. Check 1.8412 Factor
factor_1_8412 = 1.8412
print(f"Factor 1.8412: {factor_1_8412}")
# Is it Proton/Electron / 1000?
m_p_m_e = 1836.15
print(f"Proton/Electron / 1000: {m_p_m_e / 1000.0:.4f}")
