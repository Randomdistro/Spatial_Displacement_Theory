import math

# Constants
c = 299792458.0

# Standard GM values (m^3/s^2) and Radii (m) for reference to calculate Kappa
# We are NOT using GM in the final code, only to derive Kappa for the missing planets.
BODIES = {
    'Sun':     {'GM': 1.32712440018e20, 'R': 6.957e8},
    'Mercury': {'GM': 2.2032e13,        'R': 2.4397e6},
    'Venus':   {'GM': 3.24859e14,       'R': 6.0518e6},
    'Earth':   {'GM': 3.986004418e14,   'R': 6.371e6},
    'Mars':    {'GM': 4.282837e13,      'R': 3.390e6},
    'Jupiter': {'GM': 1.26686534e17,    'R': 6.991e7},
    'Saturn':  {'GM': 3.7931187e16,     'R': 5.8232e7},
    'Uranus':  {'GM': 5.793939e15,      'R': 2.5362e7},
    'Neptune': {'GM': 6.836529e15,      'R': 2.4622e7}
}

print("Calculating SDT Parameters (Kappa) from Phase 15 relation:")
print("a = c^2 * R_eff / (Kappa^2 * r^2)")
print("Equivalent to GM = c^2 * R_eff / Kappa^2")
print("=> Kappa = c * sqrt(R_eff / GM)")
print("-" * 60)
print(f"{'Body':<10} | {'R_eff (m)':<12} | {'Kappa (Ϟ)':<15}")
print("-" * 60)

results = {}

for name, data in BODIES.items():
    R = data['R']
    GM = data['GM']
    Kappa = c * math.sqrt(R / GM)
    results[name] = {'R': R, 'Kappa': Kappa}
    print(f"{name:<10} | {R:<12.3e} | {Kappa:<15.5e}")

print("-" * 60)
with open('kappa_values.txt', 'w') as f:
    f.write("CELESTIAL_BODIES = {\n")
    for name, data in results.items():
        f.write(f"    '{name}': {{'R_eff': {data['R']}, 'Kappa': {data['Kappa']:.5e}}},\n")
    f.write("}\n")
print("Wrote values to kappa_values.txt")
