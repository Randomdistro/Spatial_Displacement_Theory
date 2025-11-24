"""
Recalculate all planetary and satellite parameters using k_factor directly.
Long-form calculations showing each step individually.
Outputs to detailed calculation file.
"""

import math

# Constants
c = 2.998e8  # m/s

def calculate_orbital_period_from_k_factor(k_factor, R_primary, a_orbit):
    """
    Calculate orbital period from k_factor.
    From: v = (c/Ϟ)√(R/r) and v = 2πr/T
    Solving: 2πa/T = (c/Ϟ)√(R/a)
    T = 2πa / [(c/Ϟ)√(R/a)] = 2πaϞ / [c√(R/a)] = 2πϞ√(a³/R)/c
    """
    return (2 * math.pi * k_factor * math.sqrt(a_orbit ** 3 / R_primary)) / c

def calculate_orbital_velocity(a, T):
    """Calculate orbital velocity from semi-major axis and period."""
    if T == 0:
        return 0
    return 2 * math.pi * a / T

def calculate_error(observed, predicted):
    """Calculate percentage error."""
    if observed == 0:
        return 0
    return abs((predicted - observed) / observed) * 100

# Data: [name, R (m), a (m), T (s), primary_name, primary_R, primary_k]
data = [
    # Primary bodies (orbit Sun)
    ['Sun', 6.957e8, 0, 0, None, None, 686.42],
    
    # Planets (orbit Sun)
    ['Mercury', 2.439e6, 5.791e10, 7.600e6, 'Sun', 6.957e8, 686.42],
    ['Venus', 6.052e6, 1.082e11, 1.941e7, 'Sun', 6.957e8, 686.42],
    ['Earth', 6.371e6, 1.496e11, 3.156e7, 'Sun', 6.957e8, 686.42],
    ['Mars', 3.390e6, 2.279e11, 5.935e7, 'Sun', 6.957e8, 686.42],
    ['Jupiter', 6.991e7, 7.785e11, 3.743e8, 'Sun', 6.957e8, 686.42],
    ['Saturn', 5.823e7, 1.433e12, 9.293e8, 'Sun', 6.957e8, 686.42],
    ['Uranus', 2.536e7, 2.867e12, 2.651e9, 'Sun', 6.957e8, 686.42],
    ['Neptune', 2.462e7, 4.515e12, 5.200e9, 'Sun', 6.957e8, 686.42],
    
    # Earth satellites
    ['Moon', 1.737e6, 3.844e8, 2.361e6, 'Earth', 6.371e6, 37902.41],
    ['ISS', 0, 6.780e6, 5540, 'Earth', 6.371e6, 37902.41],
    ['Hubble', 0, 6.918e6, 5724, 'Earth', 6.371e6, 37902.41],
    ['GPS_Satellite', 0, 2.656e7, 43200, 'Earth', 6.371e6, 37902.41],
    ['Geostationary', 0, 4.216e7, 86164, 'Earth', 6.371e6, 37902.41],
    ['Galileo_Satellite', 0, 2.322e7, 50460, 'Earth', 6.371e6, 37902.41],
    ['GOES_16', 0, 4.216e7, 86164, 'Earth', 6.371e6, 37902.41],
    ['Iridium_33', 0, 7.780e6, 6024, 'Earth', 6.371e6, 37902.41],
    ['Tiangong', 0, 6.750e6, 5400, 'Earth', 6.371e6, 37902.41],
    ['Starlink', 0, 6.900e6, 5700, 'Earth', 6.371e6, 37902.41],
    
    # Mars satellites
    ['Phobos', 1.12e4, 9.377e6, 27654, 'Mars', 3.390e6, 84346.21],
    ['Deimos', 6.2e3, 2.346e7, 108900, 'Mars', 3.390e6, 84346.21],
    
    # Jupiter satellites
    ['Io', 1.822e6, 4.217e8, 152900, 'Jupiter', 6.991e7, 7042.64],
    ['Europa', 1.561e6, 6.711e8, 306800, 'Jupiter', 6.991e7, 7042.64],
    ['Ganymede', 2.634e6, 1.070e9, 618000, 'Jupiter', 6.991e7, 7042.64],
    ['Callisto', 2.410e6, 1.883e9, 1442000, 'Jupiter', 6.991e7, 7042.64],
    
    # Saturn satellites
    ['Titan', 2.575e6, 1.222e9, 1378000, 'Saturn', 5.823e7, 11746.64],
    ['Enceladus', 2.525e5, 2.380e8, 118400, 'Saturn', 5.823e7, 11746.64],
    ['Mimas', 1.985e5, 1.855e8, 81220, 'Saturn', 5.823e7, 11746.64],
    ['Tethys', 5.310e5, 2.947e8, 188800, 'Saturn', 5.823e7, 11746.64],
    ['Dione', 5.610e5, 3.774e8, 273700, 'Saturn', 5.823e7, 11746.64],
    ['Rhea', 7.648e5, 5.271e8, 451800, 'Saturn', 5.823e7, 11746.64],
    ['Iapetus', 7.345e5, 3.561e9, 7933000, 'Saturn', 5.823e7, 11746.64],
    
    # Uranus satellites
    ['Miranda', 2.359e5, 1.299e8, 122400, 'Uranus', 2.536e7, 19834.31],
    ['Ariel', 5.789e5, 1.912e8, 217200, 'Uranus', 2.536e7, 19834.31],
    ['Umbriel', 5.849e5, 2.662e8, 358400, 'Uranus', 2.536e7, 19834.31],
    ['Titania', 7.886e5, 4.362e8, 752200, 'Uranus', 2.536e7, 19834.31],
    ['Oberon', 7.614e5, 5.836e8, 1194000, 'Uranus', 2.536e7, 19834.31],
    
    # Neptune satellite
    ['Triton', 1.353e6, 3.548e8, 507700, 'Neptune', 2.462e7, 17991.80],
    
    # Planetoids (orbit Sun)
    ['Ceres', 4.70e5, 4.139e11, 1.360e8, 'Sun', 6.957e8, 686.42],
    ['Vesta', 2.63e5, 3.534e11, 1.325e8, 'Sun', 6.957e8, 686.42],
    ['Pallas', 2.72e5, 4.145e11, 1.686e8, 'Sun', 6.957e8, 686.42],
    ['Hygiea', 2.07e5, 4.701e11, 2.030e8, 'Sun', 6.957e8, 686.42],
    ['Interamnia', 1.58e5, 4.750e11, 2.050e8, 'Sun', 6.957e8, 686.42],
    ['Europa_asteroid', 1.56e5, 4.630e11, 1.980e8, 'Sun', 6.957e8, 686.42],
    ['Davida', 1.63e5, 4.750e11, 2.050e8, 'Sun', 6.957e8, 686.42],
    ['Sylvia', 1.43e5, 5.150e11, 2.380e8, 'Sun', 6.957e8, 686.42],
    ['Cybele', 1.19e5, 5.290e11, 2.510e8, 'Sun', 6.957e8, 686.42],
    ['Eunomia', 1.27e5, 4.950e11, 2.200e8, 'Sun', 6.957e8, 686.42],
    ['Juno', 1.23e5, 3.999e11, 1.593e8, 'Sun', 6.957e8, 686.42],
    ['Psyche', 1.13e5, 4.370e11, 1.820e8, 'Sun', 6.957e8, 686.42],
    ['Themis', 1.08e5, 4.750e11, 2.050e8, 'Sun', 6.957e8, 686.42],
    ['Hebe', 9.7e4, 4.620e11, 1.970e8, 'Sun', 6.957e8, 686.42],
    ['Metis', 9.5e4, 4.680e11, 2.010e8, 'Sun', 6.957e8, 686.42],
    
    # Comets (orbit Sun)
    ['Halley_Comet', 5.5e3, 2.668e12, 2.376e9, 'Sun', 6.957e8, 686.42],
    ['Hale_Bopp', 6.0e3, 2.783e13, 7.993e10, 'Sun', 6.957e8, 686.42],
    ['67P_Churyumov', 1.85e3, 5.290e11, 2.040e8, 'Sun', 6.957e8, 686.42],
    ['Encke', 2.4e3, 3.210e11, 1.042e8, 'Sun', 6.957e8, 686.42],
    ['Hyakutake', 2.1e3, 2.540e12, 5.365e9, 'Sun', 6.957e8, 686.42],
    ['Borrelly', 4.0e3, 1.031e12, 2.180e9, 'Sun', 6.957e8, 686.42],
    ['Wild_2', 2.0e3, 3.380e11, 1.100e8, 'Sun', 6.957e8, 686.42],
    ['Tempel_1', 3.0e3, 3.120e11, 1.020e8, 'Sun', 6.957e8, 686.42],
    ['Hartley_2', 1.2e3, 3.460e11, 1.130e8, 'Sun', 6.957e8, 686.42],
]

# Calculate k_factor for primary bodies first
# For planets: calculate from their own orbital data around Sun
# For satellites: use primary's k_factor

results = []
output_lines = []

output_lines.append("=" * 80)
output_lines.append("PLANETARY PARAMETERS - k_factor DIRECT CALCULATIONS")
output_lines.append("=" * 80)
output_lines.append("")
output_lines.append("Formula: T = 2*pi*k_factor*sqrt(a^3/R_primary)/c")
output_lines.append("From orbital velocity law: v = (c/k_factor)*sqrt(R_primary/r)")
output_lines.append("")

for entry in data:
    name, R, a, T_obs, primary_name, primary_R, primary_k = entry
    
    if name == 'Sun':
        v_orbital = 0
        k_factor = primary_k
        T_pred = 0
        error = 0
        output_lines.append(f"\n{name}:")
        output_lines.append(f"  R = {R:.3E} m")
        output_lines.append(f"  k_factor = {k_factor:.2f} (from Phase 16)")
        output_lines.append(f"  v_surface = c/k = {c/k_factor:.2f} m/s = {c/k_factor/1000:.2f} km/s")
    else:
        v_orbital = calculate_orbital_velocity(a, T_obs)
        k_factor = primary_k  # Use primary's k_factor
        T_pred = calculate_orbital_period_from_k_factor(k_factor, primary_R, a)
        error = calculate_error(T_obs, T_pred)
        
        output_lines.append(f"\n{name} (orbits {primary_name}):")
        output_lines.append(f"  R = {R:.3E} m")
        output_lines.append(f"  a = {a:.3E} m")
        output_lines.append(f"  T_observed = {T_obs:.3E} s")
        output_lines.append(f"  v_orbital = 2*pi*a/T = {v_orbital:.2f} m/s")
        output_lines.append(f"  Using {primary_name}'s k_factor = {k_factor:.2f}")
        output_lines.append(f"  R_primary = {primary_R:.3E} m")
        output_lines.append(f"  Calculation:")
        output_lines.append(f"    sqrt(a^3/R_primary) = sqrt(({a:.3E})^3 / {primary_R:.3E})")
        sqrt_val = math.sqrt(a ** 3 / primary_R)
        output_lines.append(f"    = sqrt({a**3:.3E} / {primary_R:.3E})")
        output_lines.append(f"    = sqrt({a**3/primary_R:.3E})")
        output_lines.append(f"    = {sqrt_val:.3E}")
        output_lines.append(f"    T = 2*pi*{k_factor:.2f}*{sqrt_val:.3E} / {c:.3E}")
        output_lines.append(f"    T = {2*math.pi*k_factor*sqrt_val:.3E} / {c:.3E}")
        output_lines.append(f"    T = {T_pred:.3E} s")
        output_lines.append(f"  Error = {error:.2f}%")
    
    results.append([name, R, a, T_obs, v_orbital, k_factor, T_pred, error])

# Write detailed calculations
with open('planetary_calculations_detailed.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

# Write CSV output
csv_lines = ["Body,R,a,T,v_orbital,k_factor,SDT_predicted_T,Error"]
for r in results:
    csv_lines.append(f"{r[0]},{r[1]:.3E},{r[2]:.3E},{r[3]:.3E},{r[4]:.2f},{r[5]:.2f},{r[6]:.3E},{r[7]:.2f}")

with open('planetary_parameters_recalculated.csv', 'w', encoding='utf-8') as f:
    f.write('\n'.join(csv_lines))

print("Calculations complete!")
print(f"Detailed calculations written to: planetary_calculations_detailed.txt")
print(f"CSV output written to: planetary_parameters_recalculated.csv")
