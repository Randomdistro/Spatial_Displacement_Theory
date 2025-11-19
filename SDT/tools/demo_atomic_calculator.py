"""
SDT Atomic Calculator Demo

Demonstrates the calculator's capabilities with detailed outputs.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sdt_atomic import calculator
from sdt_atomic import geometry
import numpy as np


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*80)
    print(title)
    print("="*80)


def demo_hydrogen():
    """Demonstrate hydrogen calculations."""
    print_section("HYDROGEN ATOMIC CALCULATOR")
    
    calc = calculator.AtomicCalculator('H')
    print(f"Element: {calc.element}, Z={calc.Z}, Ionization State={calc.ionization_state}")
    
    # Energy Levels
    print("\n--- Energy Levels ---")
    print("n   l   j    E_SDT (eV)       E_exp (eV)      Error (%)")
    print("-" * 65)
    known_levels = {
        1: -13.59843449,
        2: -3.399699,
        3: -1.510934,
        4: -0.850302,
    }
    for n in [1, 2, 3, 4]:
        E_sdt = calc.energy_level(n, 0, 0.5)
        if n in known_levels:
            E_exp = known_levels[n]
            error_pct = abs(E_sdt - E_exp) / abs(E_exp) * 100
            print(f"{n}   0   0.5  {E_sdt:12.6f}   {E_exp:12.6f}   {error_pct:8.4f}")
        else:
            print(f"{n}   0   0.5  {E_sdt:12.6f}")
    
    # Geometric Structure for n=1
    print("\n--- Geometric Structure (n=1, Ground State) ---")
    geom = calc.geometric_structure(1)
    
    distances = geom.get_distance_summary()
    print("\nDistances:")
    print(f"  Proton radius:                {distances['proton_radius']:15.6e} m")
    print(f"  Orbital radius (Bohr):        {distances['orbital_radius']:15.6e} m")
    print(f"  Classical electron radius:    {distances['classical_electron_radius']:15.6e} m")
    print(f"  c-boundary radius:            {distances['c_boundary_radius']:15.6e} m")
    print(f"  Lightspeed boundary:          {distances['lightspeed_boundary_radius']:15.6e} m")
    
    velocities = geom.get_velocity_summary()
    ratios = geom.get_velocity_ratios()
    print("\nVelocities:")
    print(f"  Orbital velocity:             {velocities['orbital_velocity']:15.6e} m/s ({ratios['orbital_velocity_over_c']:8.6f}c)")
    print(f"  Velocity at proton surface:   {velocities['velocity_at_proton_surface']:15.6e} m/s ({ratios['velocity_at_proton_surface_over_c']:8.6f}c)")
    print(f"  Velocity at c-boundary:       {velocities['velocity_at_c_boundary']:15.6e} m/s ({ratios['velocity_at_c_boundary_over_c']:8.6f}c)")
    print(f"  Speed of light:               {velocities['speed_of_light']:15.6e} m/s")
    
    print("\nKey Parameters:")
    print(f"  K-factor:                     {ratios['K_factor']:15.6f}")
    print(f"  Ratio (c-boundary / r_e):     {distances['c_boundary_radius'] / distances['classical_electron_radius']:15.6f}")
    
    # Transitions
    print("\n--- Spectral Transitions ---")
    known_lines = {
        ('Lyman a', (1, 0, 0.5), (2, 0, 0.5)): 121.567,
        ('Lyman b', (1, 0, 0.5), (3, 0, 0.5)): 102.572,
        ('Balmer a', (2, 0, 0.5), (3, 1, 1.5)): 656.279,
        ('Balmer b', (2, 0, 0.5), (4, 1, 1.5)): 486.135,
    }
    print("Transition            Initial      Final        lambda_SDT (nm)    lambda_exp (nm)    Error (%)")
    print("-" * 90)
    for name, initial, final in known_lines:
        trans = calc.transition(initial, final)
        lambda_exp = known_lines[(name, initial, final)]
        error_pct = abs(trans['wavelength'] - lambda_exp) / lambda_exp * 100
        print(f"{name:20s} {str(initial):12s} {str(final):12s} {trans['wavelength']:12.3f}   {lambda_exp:12.3f}   {error_pct:8.4f}")


def demo_geometric_structures():
    """Demonstrate geometric structures for different states."""
    print_section("GEOMETRIC STRUCTURES FOR DIFFERENT STATES")
    
    calc = calculator.AtomicCalculator('H')
    
    print("n   Orbital Radius (m)    c-boundary (m)      v_orbital (c)    v_proton_surf (c)    K-factor")
    print("-" * 100)
    
    for n in [1, 2, 3, 4, 5]:
        geom = calc.geometric_structure(n)
        distances = geom.get_distance_summary()
        ratios = geom.get_velocity_ratios()
        
        print(f"{n}   {distances['orbital_radius']:15.6e}   {distances['c_boundary_radius']:15.6e}   "
              f"{ratios['orbital_velocity_over_c']:12.8f}   {ratios['velocity_at_proton_surface_over_c']:17.8f}   "
              f"{ratios['K_factor']:10.4f}")


def demo_ionization():
    """Demonstrate ionization energy calculations."""
    print_section("IONIZATION ENERGIES")
    
    elements = ['H', 'He', 'Li']
    
    for element in elements:
        calc = calculator.AtomicCalculator(element)
        print(f"\n{element} (Z={calc.Z}):")
        print("  Ionization State    IE_SDT (eV)    IE_exp (eV)    Error (%)")
        print("  " + "-" * 55)
        
        IEs = calc.all_ionizations()
        known_IEs = {
            'H': [13.59843],
            'He': [24.58741, 54.41778],
            'Li': [5.39172, 75.6400, 122.454],
        }
        
        for i, ie_data in enumerate(IEs[:min(5, len(IEs))], 1):
            IE_sdt = ie_data['IE']
            if element in known_IEs and i <= len(known_IEs[element]):
                IE_exp = known_IEs[element][i-1]
                error_pct = abs(IE_sdt - IE_exp) / IE_exp * 100
                print(f"  {i:2d}                  {IE_sdt:12.4f}   {IE_exp:12.4f}   {error_pct:8.4f}")
            else:
                print(f"  {i:2d}                  {IE_sdt:12.4f}")


def demo_spectrum():
    """Demonstrate spectrum generation."""
    print_section("HYDROGEN SPECTRUM (Selected Lines)")
    
    calc = calculator.AtomicCalculator('H')
    
    # Generate some transitions
    transitions = [
        ((1, 0, 0.5), (2, 0, 0.5), "1S -> 2S (Lyman a)"),
        ((1, 0, 0.5), (3, 0, 0.5), "1S -> 3S (Lyman b)"),
        ((2, 0, 0.5), (3, 1, 1.5), "2S -> 3P (Balmer a)"),
        ((2, 0, 0.5), (4, 1, 1.5), "2S -> 4P (Balmer b)"),
        ((2, 0, 0.5), (5, 1, 1.5), "2S -> 5P (Balmer g)"),
        ((3, 0, 0.5), (4, 1, 1.5), "3S -> 4P (Paschen a)"),
    ]
    
    print("Transition               Initial      Final        Delta_E (eV)        lambda (nm)         nu (GHz)     Allowed")
    print("-" * 100)
    
    for initial, final, name in transitions:
        trans = calc.transition(initial, final)
        frequency_GHz = trans['frequency'] / 1e9
        allowed = "Yes" if trans['allowed'] else "No"
        print(f"{name:24s} {str(initial):12s} {str(final):12s} {trans['delta_E']:12.6f}   "
              f"{trans['wavelength']:12.3f}   {frequency_GHz:12.3f}   {allowed}")


def main():
    """Run all demos."""
    print("\n" + "="*80)
    print("SDT ATOMIC CALCULATOR - COMPREHENSIVE DEMONSTRATION")
    print("="*80)
    print("\nThis calculator uses ONLY SDT formulations and geometric rules.")
    print("No quantum mechanical postulates - only pressure fields, occlusion,")
    print("and helical wake quantization.")
    
    demo_hydrogen()
    demo_geometric_structures()
    demo_ionization()
    demo_spectrum()
    
    print_section("DEMONSTRATION COMPLETE")
    print("\nAll calculations use pure SDT formulations:")
    print("  - Orbital equation: v = (c/K) * sqrt(R/r)")
    print("  - c-boundary: s = R/K^2")
    print("  - K-factor: K = n/(Z*alpha)")
    print("  - Occlusion geometry for multi-electron screening")
    print("  - Helical wake quantization for energy levels")


if __name__ == '__main__':
    main()

