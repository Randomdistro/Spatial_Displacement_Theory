#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate Trefoil Nuclear Structure Mathematics

Checks:
1. Three-velocity constraint: v₁·v₃ = c²
2. Rotation frequency calculations
3. Position geometry consistency
4. Relative velocity calculations
5. Chirality patterns
"""

import json
import math
from pathlib import Path

DATA_FILE = Path("SDT/data/trefoil_mappings.json")

# Constants
C = 299792458.0  # m/s
R_P_FM = 0.84  # fm
V1_C = 2.23
V2_C = 1.84
V3_C = 0.395
OMEGA_P_EXPECTED = 6.57e23  # rad/s

def validate_three_velocity_constraint():
    """Check v₁·v₃ = c² constraint"""
    print("=" * 60)
    print("1. THREE-VELOCITY CONSTRAINT VALIDATION")
    print("=" * 60)
    
    v1_v3_product = V1_C * V3_C
    expected = 1.0  # c² in units of c
    error = abs(v1_v3_product - expected) / expected * 100
    
    print(f"v1 = {V1_C}c")
    print(f"v3 = {V3_C}c")
    print(f"v1*v3 = {v1_v3_product:.6f}")
    print(f"Expected: 1.0 (c²)")
    print(f"Error: {error:.2f}%")
    
    if error < 15:
        print("[OK] Constraint satisfied (within 15% tolerance)")
    else:
        print("[X] Constraint NOT satisfied - needs adjustment")
    
    print()

def validate_rotation_frequency():
    """Check rotation frequency calculation"""
    print("=" * 60)
    print("2. ROTATION FREQUENCY VALIDATION")
    print("=" * 60)
    
    # Calculate from v_rim and R_p
    v_rim = V2_C * C  # m/s
    R_p = R_P_FM * 1e-15  # m
    omega_calculated = v_rim / R_p
    
    print(f"v_rim = {V2_C}c = {v_rim:.2e} m/s")
    print(f"R_p = {R_P_FM} fm = {R_p:.2e} m")
    print(f"omega = v_rim / R_p = {omega_calculated:.2e} rad/s")
    print(f"Expected: {OMEGA_P_EXPECTED:.2e} rad/s")
    
    error = abs(omega_calculated - OMEGA_P_EXPECTED) / OMEGA_P_EXPECTED * 100
    print(f"Error: {error:.2f}%")
    
    if error < 5:
        print("[OK] Rotation frequency calculation correct")
    else:
        print("[X] Rotation frequency mismatch")
    
    print()

def validate_alpha_geometry():
    """Check alpha particle geometry"""
    print("=" * 60)
    print("3. ALPHA PARTICLE GEOMETRY VALIDATION")
    print("=" * 60)
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        structures = json.load(f)
    
    # Find Helium (alpha particle)
    he = next(s for s in structures if s['element_symbol'] == 'He')
    nucleons = he['nucleons']
    
    if len(nucleons) != 4:
        print(f"[X] Expected 4 nucleons, got {len(nucleons)}")
        return
    
    print(f"Helium-4 (Alpha Particle): {len(nucleons)} nucleons")
    
    # Calculate distances
    def dist(n1, n2):
        dx = n1['x'] - n2['x']
        dy = n1['y'] - n2['y']
        dz = n1['z'] - n2['z']
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    distances = []
    for i in range(4):
        for j in range(i+1, 4):
            d = dist(nucleons[i], nucleons[j])
            distances.append(d)
            print(f"  Distance {i+1}-{j+1}: {d:.3f} fm")
    
    avg_dist = sum(distances) / len(distances)
    expected_alpha_dist = 1.45  # fm (compressed)
    
    print(f"\nAverage distance: {avg_dist:.3f} fm")
    print(f"Expected (compressed alpha): ~{expected_alpha_dist} fm")
    
    error = abs(avg_dist - expected_alpha_dist) / expected_alpha_dist * 100
    print(f"Error: {error:.2f}%")
    
    if error < 30:
        print("[OK] Alpha geometry reasonable")
    else:
        print("[X] Alpha geometry needs refinement")
    
    print()

def validate_relative_velocities():
    """Check relative velocity calculations"""
    print("=" * 60)
    print("4. RELATIVE VELOCITY VALIDATION")
    print("=" * 60)
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        structures = json.load(f)
    
    # Check deuteron
    deuterium = next((s for s in structures if s['element_symbol'] == 'D'), None)
    if not deuterium:
        print("Deuterium not found, checking Hydrogen...")
        deuterium = structures[0]  # Fallback
    
    if len(deuterium['nucleons']) >= 2:
        n1 = deuterium['nucleons'][0]
        n2 = deuterium['nucleons'][1]
        
        v1 = n1['velocity_v2']  # Use average velocity
        v2 = n2['velocity_v2']
        rel_v = abs(v1 - v2)
        
        print(f"Deuteron relative velocity:")
        print(f"  Proton v₂: {v1:.6f}c")
        print(f"  Neutron v₂: {v2:.6f}c")
        print(f"  Relative: {rel_v:.6f}c")
        print(f"  Expected: ~0.015c (from documentation)")
        
        if 0.01 < rel_v < 0.02:
            print("[OK] Relative velocity reasonable")
        else:
            print("[X] Relative velocity outside expected range")
    else:
        print("[X] Not enough nucleons for deuteron check")
    
    print()

def validate_chirality_patterns():
    """Check chirality patterns"""
    print("=" * 60)
    print("5. CHIRALITY PATTERN VALIDATION")
    print("=" * 60)
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        structures = json.load(f)
    
    # Check alpha particle (should have L-R-L-R pattern)
    he = next(s for s in structures if s['element_symbol'] == 'He')
    nucleons = he['nucleons']
    
    if len(nucleons) == 4:
        pattern = [n['chirality'] for n in nucleons]
        print(f"Helium-4 chirality pattern: {''.join(pattern)}")
        print(f"Expected: L-R-L-R (alternating)")
        
        if pattern == ['L', 'R', 'L', 'R'] or pattern == ['R', 'L', 'R', 'L']:
            print("[OK] Chirality pattern correct (alternating)")
        else:
            print("[X] Chirality pattern not alternating")
    else:
        print(f"[X] Expected 4 nucleons, got {len(nucleons)}")
    
    print()

def validate_nuclear_rotation():
    """Check nuclear rotation vs individual spin"""
    print("=" * 60)
    print("6. NUCLEAR ROTATION VALIDATION")
    print("=" * 60)
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        structures = json.load(f)
    
    # Check first few elements
    for struct in structures[:5]:
        if struct['nucleons']:
            individual = struct['nucleons'][0]['rotation_frequency']
            nuclear = struct['nuclear_rotation_frequency']
            ratio = individual / nuclear if nuclear > 0 else 0
            
            print(f"{struct['element_symbol']}:")
            print(f"  Individual spin: {individual:.2e} rad/s")
            print(f"  Nuclear rotation: {nuclear:.2e} rad/s")
            print(f"  Ratio: {ratio:.2e}")
            print(f"  Expected ratio: ~10^10 (nuclear much slower)")
            
            if 1e9 < ratio < 1e11:
                print("  [OK] Ratio reasonable")
            else:
                print("  [X] Ratio outside expected range")
            print()

def main():
    """Run all validations"""
    print("\n" + "=" * 60)
    print("TREFOIL NUCLEAR STRUCTURE MATHEMATICAL VALIDATION")
    print("=" * 60 + "\n")
    
    validate_three_velocity_constraint()
    validate_rotation_frequency()
    validate_alpha_geometry()
    validate_relative_velocities()
    validate_chirality_patterns()
    validate_nuclear_rotation()
    
    print("=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
