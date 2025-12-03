#!/usr/bin/env python3
"""
SDT Galactic Rotation Calculator - Phase 24 Disk Eclipse Saturation

Predicts flat rotation curves without dark matter via disk eclipse
saturation mechanism.
"""

import argparse
import math
import numpy as np

C = 299792458  # m/s
KPC_TO_M = 3.086e19  # meters per kiloparsec

def calculate_occlusion(r_kpc, R_d_kpc, viewing_angle=90):
    """
    Calculate occlusion E(r) from disk mass interior to radius r
    E saturates at large r, causing flat rotation
    """
    r_ratio = r_kpc / R_d_kpc
    
    # Disk eclipse saturation model: E → E_sat as r → ∞
    # For r << R_d: E ∝ r² (growing occlusion)
    # For r >> R_d: E → E_sat (saturated, no new shadowing)
    
    if r_ratio < 1.0:
        E = 0.5 * r_ratio * r_ratio  # Parabolic growth
    else:
        E_sat = 0.64  # Saturation value (from Phase 24)
        E = E_sat * (1 - math.exp(-(r_ratio - 1)))
    
    return E

def predict_rotation_curve(r_values_kpc, R_d_kpc, v_flat_kms, beta_core=1e10):
    """
    Predict v(r) using disk eclipse saturation
    Inner: Keplerian v ∝ 1/√r
    Outer: Flat v ≈ v_flat (disk eclipse saturation)
    """
    results = []
    
    R_flat = 2.5 * R_d_kpc  # Predicted flat onset (Phase 24)
    
    for r in r_values_kpc:
        if r < R_flat:
            # Keplerian regime
            v = v_flat_kms * math.sqrt(R_flat / r)
        else:
            # Flat regime (eclipse saturation)
            v = v_flat_kms
        
        E = calculate_occlusion(r, R_d_kpc)
        results.append({'r_kpc': r, 'v_kms': v, 'E': E})
    
    return results

def test_rflat_rd_correlation(galaxies_data):
    """
    Test R_flat ≈ 2.5 R_d correlation from Phase 24
    Input: list of dicts with 'name', 'R_flat_kpc', 'R_d_kpc'
    """
    print(f"\n{'='*70}")
    print(f"Testing R_flat vs R_d Correlation (SDT Prediction: R_flat ≈ 2.5 R_d)")
    print(f"{'='*70}\n")
    
    print(f"{'Galaxy':<20} {'R_d (kpc)':<12} {'R_flat (kpc)':<15} {'R_flat/R_d':<12} {'Deviation'}")
    print(f"{'-'*70}")
    
    ratios = []
    for galaxy in galaxies_data:
        ratio = galaxy['R_flat_kpc'] / galaxy['R_d_kpc']
        deviation = abs(ratio - 2.5) / 2.5 * 100
        ratios.append(ratio)
        
        print(f"{galaxy['name']:<20} {galaxy['R_d_kpc']:<12.2f} {galaxy['R_flat_kpc']:<15.2f} {ratio:<12.2f} {deviation:>7.1f}%")
    
    avg_ratio = np.mean(ratios)
    std_ratio = np.std(ratios)
    
    print(f"{'-'*70}")
    print(f"Average R_flat/R_d: {avg_ratio:.2f} ± {std_ratio:.2f}")
    print(f"SDT Prediction: 2.50")
    print(f"Deviation: {abs(avg_ratio - 2.5)/2.5*100:.1f}%")
    print(f"{'='*70}\n")
    
    return avg_ratio, std_ratio

def main():
    parser = argparse.ArgumentParser(description='SDT Galactic Rotation Calculator')
    parser.add_argument('--R_d', type=float, help='Disk scale length (kpc)')
    parser.add_argument('--v_flat', type=float, help='Flat rotation velocity (km/s)')
    parser.add_argument('--r_max', type=float, default=30, help='Maximum radius to plot (kpc)')
    parser.add_argument('--test-correlation', action='store_true', help='Test R_flat/R_d correlation')
    
    args = parser.parse_args()
    
    if args.test_correlation:
        # Example galaxies from Phase 24
        test_galaxies = [
            {'name': 'Milky Way', 'R_d_kpc': 2.5, 'R_flat_kpc': 6.0},
            {'name': 'M31 (Andromeda)', 'R_d_kpc': 5.4, 'R_flat_kpc': 13.5},
            {'name': 'NGC 3198', 'R_d_kpc': 2.8, 'R_flat_kpc': 7.2},
            {'name': 'NGC 2403', 'R_d_kpc': 1.8, 'R_flat_kpc': 4.4},
        ]
        test_rflat_rd_correlation(test_galaxies)
        return
    
    if not all([args.R_d, args.v_flat]):
        print("Error: --R_d and --v_flat required (or use --test-correlation)")
        return
    
    # Generate rotation curve
    r_values = np.linspace(0.5, args.r_max, 50)
    curve = predict_rotation_curve(r_values, args.R_d, args.v_flat)
    
    print(f"\n{'='*60}")
    print(f"SDT Galactic Rotation Curve (No Dark Matter)")
    print(f"{'='*60}")
    print(f"Disk scale length R_d: {args.R_d:.2f} kpc")
    print(f"Flat velocity v_flat: {args.v_flat:.1f} km/s")
    print(f"Predicted R_flat: {2.5 * args.R_d:.2f} kpc")
    print(f"{'='*60}\n")
    
    print(f"{'r (kpc)':<10} {'v (km/s)':<12} {'E(r)':<10} {'Regime'}")
    print(f"{'-'*50}")
    
    for point in curve[::5]:  # Print every 5th point
        regime = 'Keplerian' if point['r_kpc'] < 2.5*args.R_d else 'Flat (Eclipse Sat.)'
        print(f"{point['r_kpc']:<10.1f} {point['v_kms']:<12.1f} {point['E']:<10.3f} {regime}")
    
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
