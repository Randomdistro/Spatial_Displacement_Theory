import math

# Constants
c = 299792458
v_percent = 99.999997
v = (v_percent / 100.0) * c
beta = v / c

# Lorentz Factor
gamma = 1.0 / math.sqrt(1.0 - beta**2)
print(f"Velocity: {v_percent}% c")
print(f"Beta: {beta:.8f}")
print(f"Gamma: {gamma:.4f}")

# Target: Spherical Entity (Proton?)
# Diameter of Proton ~ 1.68 fm (2 * 0.84 fm)
L_contracted = 1.68e-15 # m

# L_contracted = L_rest / gamma
# L_rest = L_contracted * gamma
L_rest = L_contracted * gamma

print(f"\nTarget Contracted Length (Proton Diameter): {L_contracted:.4e} m")
print(f"Required Rest Length (L_rest): {L_rest:.4e} m")

# User mentioned "10^-31 scale for a rod cross section".
# Maybe the "rod" has radius 10^-31?
# Or maybe the length is related to the Universe scale?
R_univ = 4.4e26 # m
print(f"Universe Radius: {R_univ:.4e} m")
print(f"Ratio (L_rest / R_univ): {L_rest / R_univ:.4e}")

# Check if L_rest matches any known scale.
# Maybe the "rod" is the size of the universe?
# If L_rest = R_univ, what gamma is needed?
gamma_needed = R_univ / L_contracted
print(f"\nGamma needed for Universe -> Proton: {gamma_needed:.4e}")
# Calculate v for this gamma.
# gamma = 1 / sqrt(1 - beta^2)
# 1 - beta^2 = 1/gamma^2
# beta = sqrt(1 - 1/gamma^2)
beta_needed = math.sqrt(1.0 - 1.0/gamma_needed**2)
print(f"Beta needed: {beta_needed:.20f}")
