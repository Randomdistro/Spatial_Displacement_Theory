#!/usr/bin/env python3
"""
SDT Star Calculator - Stellar Parameter Calculations from Phase 22

Calculates β-parameter, k-parameter, and validates z·k²=1 relationship
for stellar/planetary systems.
"""

import argparse
import math
import sys

# Constants
C = 299792458  # m/s

def calculate_beta(M_star_kg, R_star_m):
    """Calculate β = GM/c² compactness parameter (SDT: β = c²R_c/k²)"""
    G = 6.67430e-11  # m³/kg/s²
    return G * M_star_kg / (C * C)

def calculate_k_from_orbit(a_m, v_obs_ms, R_c_m):
    """Calculate k-parameter from observed orbital velocity: k = c√(R_c/r) / v"""
    if v_obs_ms == 0:
        return None
    r_ratio = math.sqrt(R_c_m / a_m)
    return C * r_ratio / v_obs_ms

def predict_velocity(a_m, beta, k):
    """Predict orbital velocity: v = (c/k)√(β/a)"""
    return (C / k) * math.sqrt(beta / a_m)

def verify_zk2(z, k):
    """Verify z·k² = 1 for continuous mass distributions"""
    product = z * k * k
    deviation = abs(product - 1.0)
    return product, deviation

def main():
    parser = argparse.ArgumentParser(description='SDT Stellar Parameter Calculator')
    parser.add_argument('--star', type=str, help='Star name')
    parser.add_argument('--mass', type=float, help='Star mass (solar masses)')
    parser.add_argument('--radius', type=float, help='Star radius (solar radii)')
    parser.add_argument('--planet-a', type=float, help='Planet semi-major axis (AU)')
    parser.add_argument('--planet-v', type=float, help='Planet velocity (km/s)')
    
    args = parser.parse_args()
    
    if not all([args.mass, args.radius]):
        print("Error: --mass and --radius required")
        sys.exit(1)
    
    # Convert to SI
    M_sun = 1.989e30  # kg
    R_sun = 6.96e8    # m
    AU = 1.496e11     # m
    
    M_star = args.mass * M_sun
    R_star = args.radius * R_sun
    
    # Calculate β
    beta = calculate_beta(M_star, R_star)
    
    print(f"\n{'='*60}")
    print(f"SDT Stellar Analysis: {args.star or 'Unknown Star'}")
    print(f"{'='*60}")
    print(f"Mass: {args.mass:.3f} M☉ ({M_star:.3e} kg)")
    print(f"Radius: {args.radius:.3f} R☉ ({R_star:.3e} m)")
    print(f"β-parameter: {beta:.3e} m")
    print(f"Compactness: {beta/R_star:.3e}")
    
    if args.planet_a and args.planet_v:
        a = args.planet_a * AU
        v_obs = args.planet_v * 1000  # km/s to m/s
        
        # Calculate k from observation
        k = calculate_k_from_orbit(a, v_obs, R_star)
        
        # Predict velocity
        v_pred = predict_velocity(a, beta, k)
        error = abs(v_pred - v_obs) / v_obs * 100
        
        # z·k² check
        z = 2 * R_star / (2 * a)  # Compactness ratio
        zk2, dev = verify_zk2(z, k)
        
        print(f"\n{'='*60}")
        print(f"Planetary Orbit Analysis")
        print(f"{'='*60}")
        print(f"Semi-major axis: {args.planet_a:.3f} AU ({a:.3e} m)")
        print(f"Observed velocity: {args.planet_v:.2f} km/s")
        print(f"k-parameter: {k:.2f}")
        print(f"Predicted velocity: {v_pred/1000:.2f} km/s")
        print(f"Error: {error:.2f}%")
        print(f"\nz·k² validation:")
        print(f"  z = {z:.4f}")
        print(f"  k = {k:.2f}")
        print(f"  z·k² = {zk2:.4f} (expect 1.0)")
        print(f"  Deviation: {dev:.4f}")
        print(f"{'='*60}\n")
    
if __name__ == '__main__':
    main()
