"""
Process stellar spectral data and calculate orbital parameters using SDT.
Based on Phase 22: Exoplanetary Systems from Stellar Compactness and Luminosity.
"""

import csv
import math

# Constants
c = 2.998e8  # m/s
sigma = 5.670374419e-8  # Stefan-Boltzmann constant, W·m⁻²·K⁻⁴
AU = 1.495978707e11  # m
R_sun = 6.957e8  # m
L_sun = 3.828e26  # W
T_sun = 5772  # K
z_0 = 2.125e-6  # Solar compactness

def calculate_stellar_radius(L, T_eff):
    """Calculate stellar radius from luminosity and effective temperature."""
    return math.sqrt(L / (4 * math.pi * sigma * T_eff**4))

def calculate_z_compactness(T_eff, metallicity=0.0):
    """Calculate z_compactness from T_eff using empirical relation."""
    # z = z_0 * (T_sun / T_eff)^2 * [1 + alpha_Fe * [Fe/H]]
    alpha_Fe = 0.1  # metallicity coefficient
    z = z_0 * (T_sun / T_eff)**2 * (1 + alpha_Fe * metallicity)
    return z

def calculate_k_factor(z):
    """Calculate k_factor from z_compactness using universal relation z·k² = 1."""
    return 1.0 / math.sqrt(z)

def calculate_orbital_velocity(k, R_star, a):
    """Calculate orbital velocity at semi-major axis a."""
    return (c / k) * math.sqrt(R_star / a)

def calculate_orbital_period(k, R_star, a):
    """Calculate orbital period from semi-major axis."""
    return (2 * math.pi * k / c) * math.sqrt(a**3 / R_star)

def calculate_semi_major_axis_from_period(k, R_star, P):
    """Calculate semi-major axis from orbital period."""
    # P = (2πk/c) * sqrt(a³/R)
    # a³ = (P² c² R) / (4π² k²)
    a_cubed = (P**2 * c**2 * R_star) / (4 * math.pi**2 * k**2)
    return a_cubed**(1/3)

def estimate_radius_from_observables(T_eff, V_mag, distance_pc, spectral_type):
    """Estimate stellar radius using SDT-native quantities only.
    
    Method: Use V_mag and distance to estimate absolute magnitude,
    then use bolometric correction and Stefan-Boltzmann to get radius.
    
    OR: Use spectral type + T_eff with main sequence radius relations
    (empirical, but no G or M involved).
    
    Pure SDT approach: Use Stefan-Boltzmann L = 4πR²σT_eff⁴
    We need L, which we estimate from absolute magnitude.
    """
    # Method 1: From absolute magnitude and bolometric correction
    # Distance modulus: m - M = 5*log10(d/10)
    # Absolute magnitude: M_V = V_mag - 5*log10(distance_pc) + 5
    
    M_V = V_mag - 5 * math.log10(distance_pc) + 5
    
    # Bolometric correction (BC) depends on spectral type and T_eff
    # Rough approximation: BC ≈ -0.1 for G stars, more negative for hotter
    # For main sequence: BC_V ≈ -0.3 * (T_eff/5772 - 1) (rough)
    BC_V = -0.3 * (T_eff / T_sun - 1)
    
    # Bolometric magnitude
    M_bol = M_V + BC_V
    
    # Luminosity from absolute bolometric magnitude
    # M_bol = M_bol,sun - 2.5*log10(L/L_sun)
    # L/L_sun = 10^((M_bol,sun - M_bol)/2.5)
    M_bol_sun = 4.74  # Solar bolometric magnitude
    L_ratio = 10**((M_bol_sun - M_bol) / 2.5)
    L_estimated = L_ratio * L_sun
    
    # Calculate radius from Stefan-Boltzmann (SDT-native, no G or M)
    R_est = math.sqrt(L_estimated / (4 * math.pi * sigma * T_eff**4))
    
    return R_est

def calculate_luminosity_from_radius(R, T_eff):
    """Calculate luminosity from radius and temperature using Stefan-Boltzmann."""
    return 4 * math.pi * R**2 * sigma * T_eff**4

# Read input file
input_file = '../data/Stellar_spectral_data_uncalculated.csv'
output_file = '../data/stellar_orbital_parameters_calculated.csv'

results = []

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
    # Find header line
    header_line = None
    for i, line in enumerate(lines):
        if line.startswith('Star_Name,RA_deg'):
            header_line = i
            break
    
    if header_line is None:
        print("Error: Could not find header line")
        exit(1)
    
    # Read data
    reader = csv.DictReader(lines[header_line:])
    
    for row in reader:
        star_name = row['Star_Name']
        T_eff = float(row['T_eff_K'])
        V_mag = float(row['V_mag'])
        distance_pc = float(row['Distance_pc'])
        spectral_type = row['Spectral_type']
        metallicity = float(row['Metallicity_Fe_H'])
        planet_count = int(row['Planet_count'])
        
        # Estimate radius from observables (no log_g, no G, no M)
        R_star = estimate_radius_from_observables(T_eff, V_mag, distance_pc, spectral_type)
        
        # Calculate luminosity from radius and temperature
        L_estimated = calculate_luminosity_from_radius(R_star, T_eff)
        z = calculate_z_compactness(T_eff, metallicity)
        k = calculate_k_factor(z)
        
        # For each planet, calculate orbital parameters at typical distances
        # Use habitable zone boundaries and typical spacing
        for planet_num in range(1, planet_count + 1):
            # Estimate semi-major axis based on planet number
            # Inner planets closer, outer planets further
            # Use rough scaling: a_n = a_0 * 1.5^(n-1) where a_0 is inner HZ
            # Inner HZ: r_inner ≈ sqrt(L/(4πσ*373^4*1.4)) for Earth-like
            # Outer HZ: r_outer ≈ sqrt(L/(4πσ*273^4*1.4))
            A = 0.3  # Bond albedo
            f_GH = 0.4  # Greenhouse factor
            
            r_inner = math.sqrt(L_estimated * (1 - A) / (4 * math.pi * sigma * 373**4 * (1 + f_GH)))
            r_outer = math.sqrt(L_estimated * (1 - A) / (4 * math.pi * sigma * 273**4 * (1 + f_GH)))
            
            # Distribute planets across HZ and beyond
            if planet_count == 1:
                a = (r_inner + r_outer) / 2  # Middle of HZ
            else:
                # Space planets from inner HZ outward
                spacing = (r_outer - r_inner) / (planet_count - 1) if planet_count > 1 else 0
                a = r_inner + spacing * (planet_num - 1)
            
            # Calculate orbital parameters
            v_orbital = calculate_orbital_velocity(k, R_star, a)
            P = calculate_orbital_period(k, R_star, a)
            P_days = P / 86400
            
            # Eccentricity, inclination, longitude, latitude - not calculable from stellar properties alone
            # These require observational data (RV curves, transits)
            e = 0.0  # Assume circular for now
            i = 90.0  # Assume edge-on (most likely to transit)
            longitude = 0.0  # Arbitrary reference
            latitude = 0.0  # Arbitrary reference
            
            results.append({
                'Star_Name': star_name,
                'Planet_Number': planet_num,
                'R_star_m': R_star,
                'R_star_Rsun': R_star / R_sun,
                'L_estimated_W': L_estimated,
                'L_estimated_Lsun': L_estimated / L_sun,
                'T_eff_K': T_eff,
                'z_compactness': z,
                'k_factor': k,
                'a_m': a,
                'a_AU': a / AU,
                'v_orbital_m_s': v_orbital,
                'v_orbital_km_s': v_orbital / 1000,
                'P_s': P,
                'P_days': P_days,
                'eccentricity': e,
                'inclination_deg': i,
                'longitude_deg': longitude,
                'latitude_deg': latitude
            })

# Write output
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    if results:
        fieldnames = results[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

print(f"Processed {len(results)} planetary systems")
print(f"Output written to: {output_file}")

