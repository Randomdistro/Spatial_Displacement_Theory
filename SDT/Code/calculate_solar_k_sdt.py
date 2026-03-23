"""
SDT Solar κ Calculator — Pure SDT derivation
=============================================
Derives the solar κ (velocity factor) from observed planetary orbital velocities.
SDT relation: κ = c/v, z = 1/κ², R_eff = r·v²/c² (derived, not input)
No G, no M — geometry and observables only.
"""

c = 299792458.0  # Speed of light [m/s]
R_sun = 6.9634e8  # Solar radius [m] (directly measured)

# Planetary orbital data (mean distance in m, mean velocity in m/s)
planets = {
    'Mercury': {'r': 5.79e10,  'v': 47400},
    'Venus':   {'r': 1.082e11, 'v': 35020},
    'Earth':   {'r': 1.496e11, 'v': 29780},
    'Mars':    {'r': 2.279e11, 'v': 24070},
    'Jupiter': {'r': 7.786e11, 'v': 13070},
    'Saturn':  {'r': 1.433e12, 'v': 9680},
    'Uranus':  {'r': 2.872e12, 'v': 6800},
    'Neptune': {'r': 4.495e12, 'v': 5430},
}

print("SDT Solar κ Derivation — No G, No M")
print("=" * 60)
print(f"{'Body':<10} {'r (m)':<12} {'v (m/s)':<10} {'κ=c/v':<10} {'R_eff (m)':<12} {'z·κ²':<8}")
print("-" * 60)

r_eff_values = []

for name, data in planets.items():
    r = data['r']
    v = data['v']

    # SDT: κ = c/v (velocity factor, dimensionless)
    kappa = c / v

    # SDT: z = R_eff/r = v²/c² = 1/κ² (universal relation)
    z = (v / c) ** 2

    # Derived effective radius: R_eff = r · v² / c²
    # This should be constant for all planets orbiting the same body
    R_eff = r * z

    # Verify z·κ² = 1 (fundamental SDT identity)
    identity = z * kappa ** 2

    r_eff_values.append(R_eff)

    print(f"{name:<10} {r:<12.3e} {v:<10.0f} {kappa:<10.2f} {R_eff:<12.4e} {identity:<8.6f}")

print("-" * 60)

# R_eff should be constant — this is the SDT equivalent of GM/c²
import statistics
mean_R_eff = statistics.mean(r_eff_values)
std_R_eff = statistics.stdev(r_eff_values)
cv = std_R_eff / mean_R_eff * 100

print(f"\nR_eff consistency check:")
print(f"  Mean R_eff  = {mean_R_eff:.4e} m")
print(f"  Std dev     = {std_R_eff:.4e} m")
print(f"  CV          = {cv:.2f}%")
print(f"  R_eff/R_sun = {mean_R_eff/R_sun:.6e}")

# SDT c-boundary radius: R_c = R_eff (where v → c)
print(f"\nSDT c-boundary radius R_c = {mean_R_eff:.4e} m")
print(f"  (This is where the pressure field predicts v → c)")

# Electron analysis (ground state hydrogen)
print(f"\nElectron Analysis (Hydrogen ground state):")
v_e = c / 137.036  # First Bohr orbit velocity
r_e = 5.29177e-11  # Bohr radius
R_eff_e = r_e * (v_e / c) ** 2
kappa_e = c / v_e
print(f"  v_e       = {v_e:.4e} m/s")
print(f"  κ_e       = {kappa_e:.4f} (= 1/α)")
print(f"  R_eff_e   = {R_eff_e:.4e} m")
print(f"  z·κ² = 1  ✓ (by construction)")
