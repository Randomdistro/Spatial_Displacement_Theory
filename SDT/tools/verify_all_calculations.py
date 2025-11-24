"""
Verify all planetary calculations and identify errors.
Tests each calculation individually and reports discrepancies.
"""

import math
import csv

c = 2.998e8  # m/s

def calculate_orbital_period_from_k_factor(k_factor, R_primary, a_orbit):
    """Calculate orbital period from k_factor."""
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

# Read the CSV file
errors_found = []
warnings = []

with open('../data/planetary_parameters.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
    # Skip header and comments
    data_lines = [l.strip() for l in lines if l.strip() and not l.strip().startswith('#')]
    header = data_lines[0]
    
    for line in data_lines[1:]:
        if not line:
            continue
            
        parts = line.split(',')
        if len(parts) < 8:
            continue
            
        name = parts[0]
        try:
            R = float(parts[1])
            a = float(parts[2])
            T_obs = float(parts[3])
            v_obs = float(parts[4])
            k_factor = float(parts[5])
            T_pred = float(parts[6])
            error_reported = float(parts[7])
        except (ValueError, IndexError):
            warnings.append(f"{name}: Could not parse data")
            continue
        
        # Verify orbital velocity calculation
        v_calc = calculate_orbital_velocity(a, T_obs) if T_obs > 0 else 0
        if T_obs > 0 and abs(v_calc - v_obs) > 0.01:
            errors_found.append({
                'body': name,
                'type': 'v_orbital_mismatch',
                'calculated': v_calc,
                'reported': v_obs,
                'difference': abs(v_calc - v_obs)
            })
        
        # Verify period prediction
        if name == 'Sun':
            continue  # Skip Sun
            
        # Determine primary
        if name in ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']:
            primary_R = 6.957e8  # Sun
            primary_k = 686.42
        elif name in ['Moon', 'ISS', 'Hubble', 'GPS_Satellite', 'Geostationary', 'Galileo_Satellite', 'GOES_16', 'Iridium_33', 'Tiangong', 'Starlink']:
            primary_R = 6.371e6  # Earth
            primary_k = 37902.41
        elif name in ['Phobos', 'Deimos']:
            primary_R = 3.390e6  # Mars
            primary_k = 84346.21
        elif name in ['Io', 'Europa', 'Ganymede', 'Callisto']:
            primary_R = 6.991e7  # Jupiter
            primary_k = 7042.64
        elif name in ['Titan', 'Enceladus', 'Mimas', 'Tethys', 'Dione', 'Rhea', 'Iapetus']:
            primary_R = 5.823e7  # Saturn
            primary_k = 11746.64
        elif name in ['Miranda', 'Ariel', 'Umbriel', 'Titania', 'Oberon']:
            primary_R = 2.536e7  # Uranus
            primary_k = 19834.31
        elif name == 'Triton':
            primary_R = 2.462e7  # Neptune
            primary_k = 17991.80
        else:  # Planetoids and comets
            primary_R = 6.957e8  # Sun
            primary_k = 686.42
        
        # Verify k_factor matches primary
        if abs(k_factor - primary_k) > 0.01:
            errors_found.append({
                'body': name,
                'type': 'k_factor_mismatch',
                'reported': k_factor,
                'expected': primary_k,
                'difference': abs(k_factor - primary_k)
            })
        
        # Recalculate period
        T_recalc = calculate_orbital_period_from_k_factor(primary_k, primary_R, a)
        error_recalc = calculate_error(T_obs, T_recalc)
        
        # Check if reported prediction matches recalculation
        if T_obs > 0 and abs(T_pred - T_recalc) / T_obs > 0.001:  # 0.1% tolerance
            errors_found.append({
                'body': name,
                'type': 'T_prediction_mismatch',
                'reported': T_pred,
                'recalculated': T_recalc,
                'difference_pct': abs(T_pred - T_recalc) / T_obs * 100
            })
        
        # Check if reported error matches actual error
        if T_obs > 0 and abs(error_reported - error_recalc) > 0.01:
            errors_found.append({
                'body': name,
                'type': 'error_mismatch',
                'reported_error': error_reported,
                'actual_error': error_recalc,
                'difference': abs(error_reported - error_recalc)
            })

# Report results
print("=" * 80)
print("VERIFICATION RESULTS")
print("=" * 80)

if errors_found:
    print(f"\nFound {len(errors_found)} errors:")
    for err in errors_found:
        print(f"\n{err['body']} - {err['type']}:")
        for key, val in err.items():
            if key != 'body' and key != 'type':
                print(f"  {key}: {val}")
else:
    print("\n✓ No calculation errors found!")

if warnings:
    print(f"\nWarnings ({len(warnings)}):")
    for w in warnings:
        print(f"  {w}")

print("\n" + "=" * 80)

