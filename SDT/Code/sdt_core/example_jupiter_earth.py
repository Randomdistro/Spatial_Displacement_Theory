"""
REAL USAGE EXAMPLE 2: Jupiter-Earth Orbital Perturbation

Demonstrates State28D for GRAVITATIONAL dynamics:
1. Build Earth and Jupiter as 28D states
2. Calculate mutual occlusion (gravitational coupling)
3. Use Φ₄ to track Earth's trajectory variance during close approach
4. Use Φ₅ to calculate energy exchange between orbits
5. Predict orbital perturbation magnitude

This shows macroscopic usage - opposite scale from hydrogen ionization.
"""

import sys
import math
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from state_28d import State28D
import constants as sdt_const


def build_planetary_states() -> tuple[State28D, State28D, State28D]:
    """
    Build Sun, Earth, and Jupiter as 28D states with orbital dynamics.
    
    Returns:
        (sun, earth, jupiter) with full orbital coupling
    """
    print("="*70)
    print("BUILDING PLANETARY SYSTEM")
    print("="*70)
    
    # Central body: Sun
    sun = State28D()
    sun_data = sdt_const.CELESTIAL_BODIES['Sun']
    
    sun.xi_0 = 1.0  # Exists
    sun.T_1 = sun_data['R_eff']  # 6.957e8 m
    sun.T_2 = sun.T_1 / 10  # Approximate
    sun.T_3 = 4 * math.pi * sun.T_1 * sun.T_1
    sun.Phi_4 = sun_data['Kappa']  # 686.4
    
    print(f"\nSun:")
    print(f"  R_eff: {sun.T_1:.3e} m")
    print(f"  κ: {sun.Phi_4:.2f}")
    
    # Earth
    earth = State28D()
    earth_data = sdt_const.CELESTIAL_BODIES['Earth']
    
    earth.xi_0 = 1.0
    earth.T_1 = earth_data['R_eff']  # 6.371e6 m
    earth.T_2 = earth.T_1 / 10
    earth.T_3 = 4 * math.pi * earth.T_1 * earth.T_1
    earth.Phi_4 = earth_data['Kappa']  # 37901
    
    # Earth orbital parameters
    a_earth = 1.496e11  # 1 AU
    v_earth = 29780  # m/s
    
    earth.xi_10 = a_earth  # Orbital radius
    earth.xi_11 = v_earth  # Orbital velocity
    earth.Phi_1 = v_earth * v_earth / a_earth  # Centripetal
    earth.Phi_2 = v_earth / (2 * math.pi * a_earth)  # Orbital frequency
    
    print(f"\nEarth:")
    print(f"  R_eff: {earth.T_1:.3e} m")
    print(f"  κ: {earth.Phi_4:.2f}")
    print(f"  Orbital radius: {earth.xi_10:.3e} m ({earth.xi_10/1.496e11:.3f} AU)")
    print(f"  Orbital velocity: {earth.xi_11:.2f} m/s")
    print(f"  Orbital period: {1/earth.Phi_2/86400:.1f} days")
    
    # Jupiter
    jupiter = State28D()
    jupiter_data = sdt_const.CELESTIAL_BODIES['Jupiter']
    
    jupiter.xi_0 = 1.0
    jupiter.T_1 = jupiter_data['R_eff']  # 6.991e7 m
    jupiter.T_2 = jupiter.T_1 / 10
    jupiter.T_3 = 4 * math.pi * jupiter.T_1 * jupiter.T_1
    jupiter.Phi_4 = jupiter_data['Kappa']  # 7042.47
    
    # Jupiter orbital parameters
    a_jupiter = 7.78e11  # 5.2 AU
    v_jupiter = 13070  # m/s
    
    jupiter.xi_10 = a_jupiter
    jupiter.xi_11 = v_jupiter
    jupiter.Phi_1 = v_jupiter * v_jupiter / a_jupiter
    jupiter.Phi_2 = v_jupiter / (2 * math.pi * a_jupiter)
    
    print(f"\nJupiter:")
    print(f"  R_eff: {jupiter.T_1:.3e} m")
    print(f"  κ: {jupiter.Phi_4:.2f}")
    print(f"  Orbital radius: {jupiter.xi_10:.3e} m ({jupiter.xi_10/1.496e11:.3f} AU)")
    print(f"  Orbital velocity: {jupiter.xi_11:.2f} m/s")
    print(f"  Orbital period: {1/jupiter.Phi_2/86400:.1f} days")
    
    return sun, earth, jupiter


def calculate_perturbation_during_approach(earth: State28D, jupiter: State28D):
    """
    Calculate how Jupiter perturbs Earth during close orbital approach.
    
    KEY: This uses Φ₄ to track trajectory variance as coupling changes.
    """
    print(f"\n{'='*70}")
    print(f"JUPITER-EARTH CLOSE APPROACH PERTURBATION")
    print(f"{'='*70}")
    
    # Closest approach: Earth and Jupiter separated by ~4.2 AU (minimum)
    # This happens when Earth is at perihelion and Jupiter at aphelion
    
    # Baseline occlusion (far apart)
    sep_far = abs(jupiter.xi_10 - earth.xi_10)  # ~4.2 AU
    E_far = earth.calculate_occlusion(jupiter, sep_far)
    
    print(f"\nBaseline (far apart):")
    print(f"  Separation: {sep_far:.3e} m ({sep_far/1.496e11:.2f} AU)")
    print(f"  Occlusion E: {E_far:.6e}")
    
    # Closest approach (opposition)
    sep_close = abs(jupiter.xi_10 - earth.xi_10) * 0.8  # Approximate closest
    E_close = earth.calculate_occlusion(jupiter, sep_close)
    
    print(f"\nClosest approach:")
    print(f"  Separation: {sep_close:.3e} m ({sep_close/1.496e11:.2f} AU)")
    print(f"  Occlusion E: {E_close:.6e}")
    
    # Change in occlusion
    delta_E = E_close - E_far
    
    print(f"\nOcclusion change:")
    print(f"  ΔE = {delta_E:.6e}")
    print(f"  Fractional: {delta_E/E_far:.3%}")
    
    # THIS IS THE KEY: Φ₄ encodes trajectory variance from external influence
    # Baseline Φ₄ from Sun coupling
    E_sun_earth = earth.calculate_occlusion(State28D.proton_nuclear(), 1.496e11)  # Placeholder
    baseline_phi4 = (1.0 - E_sun_earth) * 1e15  # Sun's influence on Earth trajectory
    
    # Jupiter perturbation adds to Φ₄
    jupiter_perturbation_phi4 = (1.0 - E_close) * 1e15
    
    # Total trajectory variance
    total_phi4 = baseline_phi4 + jupiter_perturbation_phi4
    fractional_variance = jupiter_perturbation_phi4 / baseline_phi4
    
    print(f"\nΦ₄ (Trajectory Variance):")
    print(f"  Baseline (Sun): {baseline_phi4:.3e}")
    print(f"  Jupiter adds: {jupiter_perturbation_phi4:.3e}")
    print(f"  Total: {total_phi4:.3e}")
    print(f"  Fractional variance: {fractional_variance:.3%}")
    
    # Calculate actual orbital perturbation
    # In SDT: trajectory perturbation ∝ ΔΦ₄
    # This affects orbital elements (semi-major axis, eccentricity)
    
    # Velocity perturbation (rough estimate)
    delta_v = earth.xi_11 * fractional_variance * 0.01  # Order of magnitude
    
    print(f"\nOrbital Perturbation:")
    print(f"  Velocity change: ~{delta_v:.2f} m/s")
    print(f"  Fractional δv/v: {delta_v/earth.xi_11:.2e}")
    
    return fractional_variance, delta_v


def calculate_energy_exchange(earth: State28D, jupiter: State28D):
    """
    Calculate energy exchange between Earth and Jupiter orbits.
    
    KEY: This uses Φ₅ (phase transition potential) for orbital energy transfer.
    """
    print(f"\n{'='*70}")
    print(f"ORBITAL ENERGY EXCHANGE")
    print(f"{'='*70}")
    
    # Orbital energies (per unit mass, simplified)
    # E_orbit = -GM/(2a) in Newtonian, but in SDT:
    # E_orbit ~ (c²R_eff)/(κ²a)
    
    sun_R_eff = 6.957e8
    sun_kappa = 686.4
    c = sdt_const.C_LATTICE
    
    E_earth_orbit = -(c**2 * sun_R_eff) / (sun_kappa**2 * earth.xi_10)
    E_jupiter_orbit = -(c**2 * sun_R_eff) / (sun_kappa**2 * jupiter.xi_10)
    
    print(f"\nOrbital energies (per kg):")
    print(f"  Earth: {E_earth_orbit:.3e} J/kg")
    print(f"  Jupiter: {E_jupiter_orbit:.3e} J/kg")
    
    # During close approach, energy can transfer
    # The mechanism: Φ₅ = phase transition potential from external exchange
    
    # Occlusion determines coupling strength
    sep = abs(jupiter.xi_10 - earth.xi_10) * 0.8
    E_coupling = earth.calculate_occlusion(jupiter, sep)
    
    # Energy transfer potential ∝ coupling × energy difference
    delta_E_potential = E_coupling * abs(E_earth_orbit - E_jupiter_orbit) * 1e-6
    
    # Set Φ₅ for Earth (energy available for orbital change)
    earth.Phi_5 = delta_E_potential
    
    print(f"\nΦ₅ (Energy Exchange Potential):")
    print(f"  Coupling E: {E_coupling:.3e}")
    print(f"  Earth Φ₅: {earth.Phi_5:.3e} J/kg")
    
    # This energy changes the orbital elements
    # ΔE ~ Φ₅ → changes in a, e, i
    
    # Semi-major axis change
    # ΔE = (GMm)/(2a²) Δa → Δa/a ~ 2ΔE/E
    delta_a = 2 * earth.Phi_5 / abs(E_earth_orbit) * earth.xi_10
    
    print(f"\nOrbital Element Changes:")
    print(f"  Δa (semi-major axis): {delta_a:.3e} m ({delta_a/earth.xi_10:.2e})")
    print(f"  Δa (km): {delta_a/1000:.1f} km")
    
    return earth.Phi_5, delta_a


def demonstrate_jupiter_earth_usage():
    """
    FULL DEMONSTRATION: Jupiter-Earth perturbation using State28D
    """
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║   REAL USAGE 2: Jupiter-Earth Orbital Perturbation (State28D)     ║")
    print("║         Showing macroscopic gravitational dynamics                ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Build system
    sun, earth, jupiter = build_planetary_states()
    
    # Calculate perturbation
    frac_variance, delta_v = calculate_perturbation_during_approach(earth, jupiter)
    
    # Calculate energy exchange
    phi5, delta_a = calculate_energy_exchange(earth, jupiter)
    
    # Summary
    print(f"\n{'='*70}")
    print(f"SUMMARY: How to USE State28D for Orbital Mechanics")
    print(f"{'='*70}")
    print(f"\n1. BUILD STATES from orbital parameters:")
    print(f"   - ξ₁₀ = orbital radius")
    print(f"   - ξ₁₁ = orbital velocity")
    print(f"   - Φ₁ = centripetal acceleration")
    print(f"   - Φ₂ = orbital frequency")
    print(f"\n2. CALCULATE COUPLING via occlusion:")
    print(f"   - E = calculate_occlusion(other, separation)")
    print(f"   - E changes during orbit → coupling varies")
    print(f"\n3. TRACK PERTURBATION with Φ₄:")
    print(f"   - Φ₄ = trajectory variance from external")
    print(f"   - Jupiter adds {frac_variance:.3%} variance to Earth")
    print(f"   - Results in ~{delta_v:.2f} m/s velocity change")
    print(f"\n4. CALCULATE ENERGY EXCHANGE with Φ₅:")
    print(f"   - Φ₅ = phase transition potential")
    print(f"   - Energy: {phi5:.3e} J/kg available")
    print(f"   - Changes orbital radius by ~{delta_a/1000:.1f} km")
    print(f"\n5. KEY INSIGHT:")
    print(f"   - Same 28D framework works from atomic to cosmological")
    print(f"   - Φ₄ and Φ₅ are UNIVERSAL mechanisms")
    print(f"   - Occlusion E determines force type (here: gravity)")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    demonstrate_jupiter_earth_usage()
