import math

# Constants
c = 299792458.0
# Sun Parameters
M_sun = 1.989e30
G = 6.67430e-11
R_sun = 6.9634e8

# Planetary Data (Mean Distance in m, Mean Velocity in m/s)
planets = {
    'Mercury': {'r': 5.79e10, 'v': 47400},
    'Venus':   {'r': 1.082e11, 'v': 35020},
    'Earth':   {'r': 1.496e11, 'v': 29780},
    'Mars':    {'r': 2.279e11, 'v': 24070},
    'Jupiter': {'r': 7.786e11, 'v': 13070},
    'Saturn':  {'r': 1.433e12, 'v': 9680},
    'Uranus':  {'r': 2.872e12, 'v': 6800},
    'Neptune': {'r': 4.495e12, 'v': 5430}
}

print(f"| Body | Radius (m) | Velocity (m/s) | k (v/c) | z (R_s/r) | z * k^2 |")
print(f"|---|---|---|---|---|---|")

# Calculate Schwarzschild Radius for Sun (Gravitational Radius)
# In SDT, this is the "Compaction Parameter" reference?
# Or is it just GM/c^2?
R_s = 2 * G * M_sun / c**2
print(f"Sun Schwarzschild Radius (R_s): {R_s:.4e} m")

# For SDT, the "Universal Constant" is z * k^2 = 1?
# Where z = R_effective / r
# And k = c / v
# Wait. User said "k factor is a universally applicable, constant scaled variable".
# And "z * k^2 = 1" in previous chat.
# Let's check: (R_eff / r) * (c / v)^2 = 1
# => R_eff = r * (v/c)^2
# This R_eff should be constant for the Sun (approx GM/c^2).

for name, data in planets.items():
    r = data['r']
    v = data['v']
    
    # k factor (velocity ratio)
    # User might mean k = c/v or v/c.
    # Let's use k_inv = c/v.
    k_inv = c / v
    
    # z factor (geometric ratio)
    # z = R_eff / r
    # We want z * k_inv^2 = 1
    # => R_eff = r / k_inv^2 = r * (v/c)^2
    
    R_eff = r * (v / c)**2
    
    # Check consistency
    # R_eff should be half Schwarzschild radius? (GM/c^2)
    # GM/c^2 = 1476 m.
    
    print(f"| {name} | {r:.2e} | {v:.0f} | {c/v:.2f} | {R_eff:.2e} | {R_eff / 1476.0:.4f} |")

# Also check Electron
print(f"\nElectron Analysis:")
# Ground State
v_e = c / 137.036
r_e = 5.29e-11
R_eff_e = r_e * (v_e / c)**2
print(f"Electron R_eff: {R_eff_e:.4e} m")
print(f"Classical Radius: {2.82e-15} m")
print(f"Ratio: {R_eff_e / 2.82e-15:.4f}") # Should be 1.0?
