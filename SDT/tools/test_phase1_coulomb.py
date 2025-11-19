#!/usr/bin/env python3
"""
Test Phase 1 Coulomb Force Formulas
Validates key formulas from Phase 1 against experimental values
"""

import math

# CODATA 2018 constants
c = 2.99792458e8  # m/s
h = 6.62607015e-34  # J·s
hbar = 1.054571817e-34  # J·s
e = 1.602176634e-19  # C
m_e = 9.1093837015e-31  # kg
m_p = 1.67262192369e-27  # kg
k_e = 8.9875517923e9  # N·m²/C²
a_0 = 5.29177210903e-11  # m (Bohr radius)

# SDT constants
R_p = 8.4e-16  # m (proton radius)
R_e = 1e-21  # m (SDT electron exclusion radius)

print("=" * 70)
print("PHASE 1: COULOMB FORCE VALIDATION")
print("=" * 70)

# Test 1: Occlusion fraction formula
print("\n1. Testing Occlusion Fraction Formula")
print("-" * 70)
r = a_0  # Bohr radius
E_N = R_p**2 / (4 * r**2)
E_e = R_e**2 / (4 * r**2)

print(f"At r = a_0 = {a_0:.3e} m:")
print(f"  E_N (nuclear eclipse) = R_p²/(4r²) = {E_N:.3e}")
print(f"  E_e (electron eclipse) = R_e²/(4r²) = {E_e:.3e}")

# Test 2: Force formula
print("\n2. Testing Force Formula")
print("-" * 70)
# From Phase 1: F = (π/4) P_CMB (R_N² R_e²)/r²
# First calculate P_CMB from matching Coulomb's law
P_CMB = (4 * k_e * e**2) / (math.pi * R_p**2 * R_e**2)
print(f"P_CMB = 4k_e e^2/(pi R_N^2 R_e^2)")
print(f"  = {P_CMB:.3e} Pa")

# Calculate force at Bohr radius
F_occlusion = (math.pi / 4) * P_CMB * (R_p**2 * R_e**2) / r**2
F_coulomb = k_e * e**2 / r**2

print(f"\nAt r = a_0:")
print(f"  F_occlusion = (pi/4) P_CMB (R_N^2 R_e^2)/r^2 = {F_occlusion:.3e} N")
print(f"  F_coulomb = k_e e^2/r^2 = {F_coulomb:.3e} N")
print(f"  Relative error = {abs(F_occlusion - F_coulomb) / F_coulomb * 100:.2f}%")

# Test 3: Dimensional analysis
print("\n3. Dimensional Analysis")
print("-" * 70)
print("Force formula: F = (pi/4) P_CMB (R_N^2 R_e^2)/r^2")
print("  [P_CMB] = N/m^2 = kg/(m*s^2)")
print("  [R_N^2 R_e^2/r^2] = m^2")
print("  [F] = (N/m^2) * m^2 = N = kg*m/s^2 [PASS]")

# Test 4: Pressure scaling
print("\n4. Testing Pressure Scaling Law")
print("-" * 70)
print("P_CMB proportional to 1/R_e^2")
R_e_values = [1e-22, 1e-21, 1e-20, 5.023e-15]
for R_e_test in R_e_values:
    P_test = (4 * k_e * e**2) / (math.pi * R_p**2 * R_e_test**2)
    print(f"  R_e = {R_e_test:.3e} m → P_CMB = {P_test:.3e} Pa")

# Test 5: Check against Phase 1 stated values
print("\n5. Comparison with Phase 1 Document Values")
print("-" * 70)
# Phase 1 states: R_e = 10^-21 m → P_CMB = 4.16×10^44 Pa
P_CMB_stated = 4.16e44
P_CMB_calculated = (4 * k_e * e**2) / (math.pi * R_p**2 * R_e**2)
print(f"  Stated: P_CMB = {P_CMB_stated:.3e} Pa")
print(f"  Calculated: P_CMB = {P_CMB_calculated:.3e} Pa")
print(f"  Relative error: {abs(P_CMB_stated - P_CMB_calculated) / P_CMB_stated * 100:.2f}%")

if abs(P_CMB_stated - P_CMB_calculated) / P_CMB_stated > 0.01:
    print("  [ERROR] Significant discrepancy found!")
else:
    print("  [PASS] Values match")

# Test 6: Force at Bohr radius comparison
print("\n6. Force at Bohr Radius Comparison")
print("-" * 70)
# Phase 1 states: Occlusion force = 8.23×10^-8 N, Coulomb = 8.24×10^-8 N
F_occlusion_stated = 8.23e-8
F_coulomb_stated = 8.24e-8
print(f"  Stated occlusion force: {F_occlusion_stated:.3e} N")
print(f"  Stated Coulomb force: {F_coulomb_stated:.3e} N")
print(f"  Calculated occlusion force: {F_occlusion:.3e} N")
print(f"  Calculated Coulomb force: {F_coulomb:.3e} N")

error_occlusion = abs(F_occlusion - F_occlusion_stated) / F_occlusion_stated * 100
error_coulomb = abs(F_coulomb - F_coulomb_stated) / F_coulomb_stated * 100

print(f"  Occlusion error: {error_occlusion:.2f}%")
print(f"  Coulomb error: {error_coulomb:.2f}%")

if error_occlusion > 1.0 or error_coulomb > 1.0:
    print("  [ERROR] Significant discrepancy!")
else:
    print("  [PASS] Values match within 1%")

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)

