#!/usr/bin/env python3
"""
B24: Multi-Electron Occlusion for Z > 20

Extends existing Z≤20 implementation to heavy elements (Z=21-118).
Implements advanced many-body occlusion calculations for:
- Transition metals (Z=21-30)
- Lanthanides (Z=57-71)
- Heavy elements (Z>71)

Validates against NIST ionization energies and atomic radii.
"""

import numpy as np
import json
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from datetime import datetime

# Import existing SDT atomic tools
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
from sdt_atomic import occlusion, screening, constants

# NIST reference data (first ionization energies in eV)
# Source: NIST Atomic Spectra Database
NIST_IONIZATION_ENERGIES = {
    21: 6.561,   # Sc
    22: 6.828,   # Ti
    23: 6.746,   # V
    24: 6.767,   # Cr
    25: 7.434,   # Mn
    26: 7.902,   # Fe
    27: 7.881,   # Co
    28: 7.640,   # Ni
    29: 7.726,   # Cu
    30: 9.394,   # Zn
    31: 5.999,   # Ga
    32: 7.899,   # Ge
    33: 9.789,   # As
    34: 9.752,   # Se
    35: 11.814,  # Br
    36: 13.999,  # Kr
    37: 4.177,   # Rb
    38: 5.695,   # Sr
    39: 6.217,   # Y
    40: 6.634,   # Zr
    41: 6.759,   # Nb
    42: 7.092,   # Mo
    43: 7.280,   # Tc
    44: 7.361,   # Ru
    45: 7.459,   # Rh
    46: 8.337,   # Pd
    47: 7.576,   # Ag
    48: 8.993,   # Cd
    49: 5.786,   # In
    50: 7.344,   # Sn
    51: 8.608,   # Sb
    52: 9.009,   # Te
    53: 10.451,  # I
    54: 12.130,  # Xe
    55: 3.894,   # Cs
    56: 5.212,   # Ba
    57: 5.577,   # La
    58: 5.539,   # Ce
    59: 5.464,   # Pr
    60: 5.525,   # Nd
    61: 5.582,   # Pm
    62: 5.670,   # Sm
    63: 5.864,   # Eu
    64: 6.150,   # Gd
    65: 5.939,   # Tb
    66: 5.984,   # Dy
    67: 6.022,   # Ho
    68: 6.108,   # Er
    69: 6.184,   # Tm
    70: 6.254,   # Yb
    71: 6.825,   # Lu
    72: 7.000,   # Hf
    73: 7.550,   # Ta
    74: 7.980,   # W
    75: 7.880,   # Re
    76: 8.438,   # Os
    77: 8.967,   # Ir
    78: 8.959,   # Pt
    79: 9.226,   # Au
    80: 10.437,  # Hg
    81: 6.108,   # Tl
    82: 7.417,   # Pb
    83: 7.289,   # Bi
    84: 8.414,   # Po
    85: 9.318,   # At
    86: 10.748,  # Rn
}

# Atomic radii (in Angstroms, from experimental data)
# Source: Various experimental measurements
ATOMIC_RADII = {
    21: 1.62,   # Sc
    22: 1.47,   # Ti
    23: 1.34,   # V
    24: 1.28,   # Cr
    25: 1.27,   # Mn
    26: 1.26,   # Fe
    27: 1.25,   # Co
    28: 1.24,   # Ni
    29: 1.28,   # Cu
    30: 1.39,   # Zn
    31: 1.87,   # Ga
    32: 1.39,   # Ge
    33: 1.19,   # As
    34: 1.20,   # Se
    35: 1.20,   # Br
    36: 1.16,   # Kr
    37: 2.50,   # Rb
    38: 2.15,   # Sr
    39: 1.80,   # Y
    40: 1.60,   # Zr
    41: 1.46,   # Nb
    42: 1.39,   # Mo
    43: 1.36,   # Tc
    44: 1.34,   # Ru
    45: 1.34,   # Rh
    46: 1.37,   # Pd
    47: 1.44,   # Ag
    48: 1.52,   # Cd
    49: 1.67,   # In
    50: 1.40,   # Sn
    51: 1.40,   # Sb
    52: 1.40,   # Te
    53: 1.40,   # I
    54: 1.40,   # Xe
    55: 2.60,   # Cs
    56: 2.15,   # Ba
    57: 1.87,   # La
    58: 1.82,   # Ce
    59: 1.82,   # Pr
    60: 1.81,   # Nd
    61: 1.80,   # Pm
    62: 1.79,   # Sm
    63: 2.04,   # Eu
    64: 1.79,   # Gd
    65: 1.77,   # Tb
    66: 1.75,   # Dy
    67: 1.73,   # Ho
    68: 1.72,   # Er
    69: 1.70,   # Tm
    70: 1.94,   # Yb
    71: 1.75,   # Lu
}


def get_electron_configuration(Z: int) -> List[Tuple[int, int]]:
    """
    Get electron configuration for element Z.
    
    Uses standard Aufbau principle with exceptions for transition metals.
    
    Parameters:
    -----------
    Z : int
        Atomic number
    
    Returns:
    --------
    config : List[Tuple[int, int]]
        List of (n, l) tuples for all electrons
    """
    config = []
    
    # Shell capacities: (n, l): max_electrons
    shell_capacity = {
        (1, 0): 2,   # 1s
        (2, 0): 2,   # 2s
        (2, 1): 6,   # 2p
        (3, 0): 2,   # 3s
        (3, 1): 6,   # 3p
        (3, 2): 10,  # 3d
        (4, 0): 2,   # 4s
        (4, 1): 6,   # 4p
        (4, 2): 10,  # 4d
        (4, 3): 14,  # 4f
        (5, 0): 2,   # 5s
        (5, 1): 6,   # 5p
        (5, 2): 10,  # 5d
        (5, 3): 14,  # 5f
        (6, 0): 2,   # 6s
        (6, 1): 6,   # 6p
        (6, 2): 10,  # 6d
        (7, 0): 2,   # 7s
    }
    
    # Aufbau order
    aufbau_order = [
        (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (3, 2), (4, 1),
        (5, 0), (4, 2), (5, 1), (6, 0), (4, 3), (5, 2), (6, 1), (7, 0),
        (5, 3), (6, 2), (7, 1)
    ]
    
    # Special cases (transition metal exceptions)
    exceptions = {
        24: [(1,0), (1,0), (2,0), (2,0), (2,1), (2,1), (2,1), (2,1), (2,1), (2,1),
             (3,0), (3,0), (3,1), (3,1), (3,1), (3,1), (3,1), (3,1), (3,2), (3,2),
             (3,2), (3,2), (3,2), (4,0), (4,0)],  # Cr: [Ar] 3d5 4s1
        29: [(1,0), (1,0), (2,0), (2,0), (2,1), (2,1), (2,1), (2,1), (2,1), (2,1),
             (3,0), (3,0), (3,1), (3,1), (3,1), (3,1), (3,1), (3,1), (3,2), (3,2),
             (3,2), (3,2), (3,2), (3,2), (3,2), (3,2), (3,2), (3,2), (4,0)],  # Cu: [Ar] 3d10 4s1
    }
    
    if Z in exceptions:
        return exceptions[Z][:Z]
    
    # Standard Aufbau filling
    electrons_placed = 0
    for n, l in aufbau_order:
        if electrons_placed >= Z:
            break
        max_in_shell = shell_capacity.get((n, l), 2 * (2 * l + 1))
        for _ in range(min(max_in_shell, Z - electrons_placed)):
            config.append((n, l))
            electrons_placed += 1
    
    return config[:Z]


def calculate_advanced_occlusion_Z_gt_20(Z: int, n: int, l: int, 
                                        electron_config: List[Tuple[int, int]],
                                        use_shell_averaging: bool = True) -> float:
    """
    Calculate Z_eff for Z > 20 using 4π steradian occlusion.
    
    Single mechanism:
    - Occlusion is the blocked solid angle on a sphere (4π steradians).
    - Use diameters for occlusion geometry.
    - Spation diameter is Planck length (d_p = 2 * R_PLANCK).
    
    Occlusion fraction for a source of diameter D at distance r:
    E = D^2 / (16 r^2)
    
    Parameters:
    -----------
    Z : int
        Atomic number
    n : int
        Principal quantum number of electron of interest
    l : int
        Angular momentum quantum number
    electron_config : List[Tuple[int, int]]
        Full electron configuration
    use_shell_averaging : bool
        Unused (kept for compatibility)
    
    Returns:
    --------
    Z_eff : float
        Effective nuclear charge
    """
    if Z <= 20:
        return screening.calculate_screening_factor(Z, n, l, electron_config)
    
    # Spation diameter at Planck length
    d_planck = 2.0 * constants.R_PLANCK
    
    # Approximate nuclear diameter (placeholder until nuclear geometry database)
    A_approx = 2 * Z
    R_N = 1.2e-15 * (A_approx**(1.0 / 3.0))
    D_N = 2.0 * R_N
    
    # Initial positions (hydrogenic)
    electron_positions = [constants.A_0 * n_i**2 / Z for n_i, l_i in electron_config]
    
    # Iterative refinement using 4π occlusion
    for _ in range(20):
        new_positions = []
        Z_eff_values = {}
        
        for i, (n_i, l_i) in enumerate(electron_config):
            r_i = electron_positions[i]
            r_i_eff = max(r_i, d_planck)
            
            # Nuclear occlusion
            E_nucleus = (D_N**2) / (16.0 * r_i_eff**2)
            
            # Electron occlusion (all other electrons)
            E_electrons = 0.0
            for j, (n_j, l_j) in enumerate(electron_config):
                if j == i:
                    continue
                r_j = electron_positions[j]
                r_ij = abs(r_i - r_j)
                r_ij_eff = max(r_ij, d_planck)
                E_ij = (constants.D_E**2) / (16.0 * r_ij_eff**2)
                E_electrons += E_ij
            
            E_total = min(1.0, E_nucleus + E_electrons)
            Z_eff_i = Z * (1.0 - E_total)
            Z_eff_i = max(1.0, min(Z_eff_i, Z))
            Z_eff_values[(n_i, l_i)] = Z_eff_i
            
            r_i_new = constants.A_0 * n_i**2 / Z_eff_i
            new_positions.append(r_i_new)
        
        electron_positions = new_positions
    
    Z_eff = Z_eff_values.get((n, l), Z * 0.7)
    return max(1.0, min(Z_eff, Z))


def calculate_ionization_energy_Z_gt_20(Z: int) -> float:
    """
    Calculate first ionization energy for Z > 20.
    
    Uses advanced occlusion calculations.
    
    Parameters:
    -----------
    Z : int
        Atomic number
    
    Returns:
    --------
    IP1 : float
        First ionization energy (eV)
    """
    # Get electron configuration
    config = get_electron_configuration(Z)
    
    # Find outermost electron
    max_n = max(n for n, l in config)
    outer_electrons = [(n, l) for n, l in config if n == max_n]
    if not outer_electrons:
        return 0.0
    
    # Use the highest l value for outermost shell
    n_outer, l_outer = max(outer_electrons, key=lambda x: x[1])
    
    # Calculate Z_eff for outermost electron
    Z_eff = calculate_advanced_occlusion_Z_gt_20(Z, n_outer, l_outer, config)
    
    # Calculate ionization energy
    # IP1 = Rydberg * Z_eff^2 / n^2 (energy to remove electron from bound state)
    IP1 = constants.RYDBERG_EV * Z_eff**2 / (n_outer**2)
    
    # Apply directional occlusion factor (reduces binding)
    core_config = [(n, l) for n, l in config if n < n_outer]
    Xi = screening.directional_occlusion_fraction(n_outer, l_outer, core_config, Z)
    
    # Xi reduces the effective binding (0 < Xi <= 1)
    IP1 *= Xi
    
    return IP1


def calculate_atomic_radius_Z_gt_20(Z: int) -> float:
    """
    Calculate atomic radius for Z > 20.
    
    Uses Z_eff to determine radius.
    
    Parameters:
    -----------
    Z : int
        Atomic number
    
    Returns:
    --------
    radius : float
        Atomic radius (Angstroms)
    """
    config = get_electron_configuration(Z)
    
    # Find outermost electron
    max_n = max(n for n, l in config)
    outer_electrons = [(n, l) for n, l in config if n == max_n]
    if not outer_electrons:
        return 0.0
    
    n_outer, l_outer = max(outer_electrons, key=lambda x: x[1])
    
    # Calculate Z_eff
    Z_eff = calculate_advanced_occlusion_Z_gt_20(Z, n_outer, l_outer, config)
    
    # Atomic radius scales as n^2 / Z_eff
    radius_bohr = constants.A_0 * n_outer**2 / Z_eff
    
    # Convert to Angstroms
    radius_angstrom = radius_bohr * 1e10
    
    return radius_angstrom


def validate_B24_Z_gt_20() -> Dict:
    """
    Validate B24 for Z > 20 elements.
    
    Returns:
    --------
    results : dict
        Validation results
    """
    print("="*80)
    print("B24 VALIDATION: Multi-Electron Occlusion for Z > 20")
    print("="*80)
    
    results = {
        "benchmark": "B24",
        "name": "Multi-Electron Occlusion",
        "validation_date": datetime.now().isoformat(),
        "Z_range": "21-86",
        "ionization_energies": {},
        "atomic_radii": {},
        "statistics": {}
    }
    
    # Validate ionization energies
    ionization_errors = []
    ionization_results = []
    
    print("\nValidating Ionization Energies (Z=21-86):")
    print("-" * 80)
    
    for Z in range(21, 87):
        if Z not in NIST_IONIZATION_ENERGIES:
            continue
        
        IP1_SDT = calculate_ionization_energy_Z_gt_20(Z)
        IP1_exp = NIST_IONIZATION_ENERGIES[Z]
        
        error = abs(IP1_SDT - IP1_exp) / IP1_exp * 100
        
        ionization_errors.append(error)
        ionization_results.append({
            "Z": Z,
            "IP1_SDT": IP1_SDT,
            "IP1_exp": IP1_exp,
            "error_percent": error
        })
        
        if Z <= 30 or Z in [57, 58, 71, 72]:  # Print sample
            print(f"Z={Z:2d}: IP1_SDT={IP1_SDT:7.3f} eV, IP1_exp={IP1_exp:7.3f} eV, Error={error:5.2f}%")
    
    results["ionization_energies"] = ionization_results
    
    # Validate atomic radii
    radius_errors = []
    radius_results = []
    
    print("\n\nValidating Atomic Radii (Z=21-71):")
    print("-" * 80)
    
    for Z in range(21, 72):
        if Z not in ATOMIC_RADII:
            continue
        
        radius_SDT = calculate_atomic_radius_Z_gt_20(Z)
        radius_exp = ATOMIC_RADII[Z]
        
        error = abs(radius_SDT - radius_exp) / radius_exp * 100
        
        radius_errors.append(error)
        radius_results.append({
            "Z": Z,
            "radius_SDT": radius_SDT,
            "radius_exp": radius_exp,
            "error_percent": error
        })
        
        if Z <= 30 or Z in [57, 58, 71]:  # Print sample
            print(f"Z={Z:2d}: r_SDT={radius_SDT:5.2f} Å, r_exp={radius_exp:5.2f} Å, Error={error:5.2f}%")
    
    results["atomic_radii"] = radius_results
    
    # Calculate statistics
    if ionization_errors:
        results["statistics"]["ionization"] = {
            "n_tested": len(ionization_errors),
            "mean_error": np.mean(ionization_errors),
            "max_error": np.max(ionization_errors),
            "within_5pct": sum(1 for e in ionization_errors if e < 5.0),
            "within_10pct": sum(1 for e in ionization_errors if e < 10.0),
            "within_5pct_pct": sum(1 for e in ionization_errors if e < 5.0) / len(ionization_errors) * 100
        }
    
    if radius_errors:
        results["statistics"]["atomic_radius"] = {
            "n_tested": len(radius_errors),
            "mean_error": np.mean(radius_errors),
            "max_error": np.max(radius_errors),
            "within_5pct": sum(1 for e in radius_errors if e < 5.0),
            "within_10pct": sum(1 for e in radius_errors if e < 10.0)
        }
    
    # Determine overall status
    if ionization_errors:
        mean_error = np.mean(ionization_errors)
        within_5pct = results["statistics"]["ionization"]["within_5pct_pct"]
        
        if mean_error < 10.0 and within_5pct >= 50:
            results["overall_status"] = "CERTIFIED"
        else:
            results["overall_status"] = "UNDER_INVESTIGATION"
        
        results["max_error_percent"] = np.max(ionization_errors)
    else:
        results["overall_status"] = "UNDER_INVESTIGATION"
        results["max_error_percent"] = None
    
    # Print summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    if ionization_errors:
        print(f"Ionization Energies:")
        print(f"  Tested: {len(ionization_errors)} elements")
        print(f"  Mean Error: {np.mean(ionization_errors):.2f}%")
        print(f"  Max Error: {np.max(ionization_errors):.2f}%")
        print(f"  Within 5%: {results['statistics']['ionization']['within_5pct']}/{len(ionization_errors)} ({results['statistics']['ionization']['within_5pct_pct']:.1f}%)")
        print(f"  Within 10%: {results['statistics']['ionization']['within_10pct']}/{len(ionization_errors)}")
    
    if radius_errors:
        print(f"\nAtomic Radii:")
        print(f"  Tested: {len(radius_errors)} elements")
        print(f"  Mean Error: {np.mean(radius_errors):.2f}%")
        print(f"  Max Error: {np.max(radius_errors):.2f}%")
    
    print(f"\nOverall Status: {results['overall_status']}")
    
    return results


if __name__ == "__main__":
    # Run validation
    results = validate_B24_Z_gt_20()
    
    # Save results
    output_file = Path(__file__).parent / "B24_validation_results_Z_gt_20.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
