"""
Beryllium: Next Element in 2s Shell
===================================

After Lithium (1s² 2s¹), Beryllium (1s² 2s²) completes the 2s shell.

Key question: Where does the 4th electron go, and how does it pair with the 3rd?

Structure:
- 1s²: Two electrons diametrically opposite (from He core)
- 2s²: Two electrons diametrically opposite (new pairing)

Nuclear structure: Be-9 = [α] + [α] + n (two alphas + bridge neutron)
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, List
import json
from pathlib import Path

# ==============================================================================
# CODATA 2018 CONSTANTS
# ==============================================================================

A_0 = 5.29177210903e-11  # m (Bohr radius)
K_E = 8.9875517923e9  # N·m²/C²
E_CHARGE = 1.602176634e-19  # C
M_E = 9.1093837015e-31  # kg

# ==============================================================================
# SCALE CONVERSION (same as Lithium model)
# ==============================================================================

SCALE_FACTOR = 1e14  # 1 fm = 10 cm

def nuclear_to_macro(nuclear_value_fm: float) -> float:
    """Convert nuclear scale (fm) to macro scale (cm)."""
    return nuclear_value_fm * 10.0

# ==============================================================================
# BERYLLIUM STRUCTURE
# ==============================================================================

@dataclass
class BerylliumStructure:
    """Beryllium atomic and nuclear structure."""
    Z: int = 4
    A: int = 9
    symbol: str = "Be"
    name: str = "Beryllium"
    
    # Nuclear: Be-9 = [α] + [α] + n (two alphas + bridge neutron)
    nuclear_structure: str = "[α] + [α] + n"
    
    # Electronic: 1s² 2s²
    electron_config: str = "1s² 2s²"

def calculate_2s_orbital_radius(Z: int, n: int) -> float:
    """
    Calculate 2s orbital radius with screening.
    
    For Be (Z=4):
    - 1s² core screens by ~2
    - Z_eff for 2s ≈ Z - 2 = 2
    - r_2s = n² a_0 / Z_eff = 4 a_0 / 2 = 2 a_0
    """
    Z_eff = max(1.0, Z - 2)  # Core screening
    r = n**2 * A_0 / Z_eff
    return r

def calculate_2s_pairing_geometry() -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """
    Calculate positions for 2s² paired electrons.
    
    Rules:
    - Two electrons diametrically opposite
    - Their linked protons also diametrically opposite
    - Perpendicular to 1s² pairing axis
    
    Returns:
    - (pos_2s1, pos_2s2) in meters
    """
    # 2s orbital radius
    r_2s = calculate_2s_orbital_radius(4, 2)  # Be, n=2
    
    # 1s electrons are along Z-axis (above/below)
    # 2s electrons should be perpendicular (along X or Y axis)
    # Choose X-axis for 2s pairing
    
    pos_2s1 = np.array([r_2s, 0.0, 0.0])  # +X
    pos_2s2 = np.array([-r_2s, 0.0, 0.0])  # -X (diametrically opposite)
    
    return (pos_2s1, pos_2s2)

def calculate_2s_velocities(pos_2s1: np.ndarray, pos_2s2: np.ndarray,
                           nucleus_center: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate velocities for 2s electrons at perihelion.
    
    Circular orbit: v = sqrt(kZe²/(mr))
    """
    r_2s = np.linalg.norm(pos_2s1 - nucleus_center)
    Z_eff = 2.0  # Screened
    
    v_mag = np.sqrt(K_E * E_CHARGE * E_CHARGE * Z_eff / (M_E * r_2s))
    
    # Velocities perpendicular to positions
    # 2s1 at +X: velocity in +Y direction
    vel_2s1 = np.array([0.0, v_mag, 0.0])
    # 2s2 at -X: velocity in -Y direction (opposite)
    vel_2s2 = np.array([0.0, -v_mag, 0.0])
    
    return (vel_2s1, vel_2s2)

def calculate_2s_energies(r_2s: float) -> Tuple[float, float]:
    """
    Calculate energies for 2s electrons.
    
    Circular orbit: E = -(1/2) kZe²/r
    """
    Z_eff = 2.0
    energy = -0.5 * K_E * E_CHARGE * E_CHARGE * Z_eff / r_2s
    return (energy, energy)  # Same for both

def calculate_nuclear_structure_be9() -> dict:
    """
    Calculate nuclear structure for Be-9.
    
    Structure: [α] + [α] + n
    - Two alpha particles
    - Bridge neutron connecting them
    """
    # Alpha 1 at center
    alpha1_center = np.array([0.0, 0.0, 0.0])
    R_alpha_fm = 2.3
    
    # Alpha 2 attached
    d_alpha_alpha_fm = 2.9  # Inter-alpha spacing (from C-12/O-16)
    alpha2_center = np.array([d_alpha_alpha_fm, 0.0, 0.0])  # Along X-axis
    
    # Bridge neutron between alphas
    bridge_neutron_pos_fm = (alpha1_center + alpha2_center) / 2
    bridge_neutron_pos_fm[1] = 1.5  # Perpendicular offset (creates structure)
    
    # Convert to macro scale
    alpha1_macro_cm = (0.0, 0.0, 0.0)
    alpha2_macro_cm = (nuclear_to_macro(d_alpha_alpha_fm), 0.0, 0.0)
    bridge_macro_cm = (
        nuclear_to_macro(bridge_neutron_pos_fm[0]),
        nuclear_to_macro(bridge_neutron_pos_fm[1]),
        0.0
    )
    
    return {
        'alpha1_center_cm': alpha1_macro_cm,
        'alpha2_center_cm': alpha2_macro_cm,
        'bridge_neutron_cm': bridge_macro_cm,
        'structure': '[α] + [α] + n'
    }

def calculate_proton_electron_pairing() -> dict:
    """
    Calculate 1:1 proton-electron pairing for Be.
    
    Be has 4 protons, 4 electrons:
    - 1s²: 2 electrons paired, linked to 2 protons in alpha1
    - 2s²: 2 electrons paired, linked to 2 protons in alpha2
    """
    # 1s electrons: along Z-axis (from He core)
    r_1s = A_0 / 4.0  # Z_eff = 4 for 1s (no screening)
    pos_1s1 = np.array([0.0, 0.0, r_1s])  # +Z
    pos_1s2 = np.array([0.0, 0.0, -r_1s])  # -Z
    
    # 2s electrons: along X-axis (perpendicular to 1s)
    pos_2s1, pos_2s2 = calculate_2s_pairing_geometry()
    
    # Nuclear structure
    nuclear = calculate_nuclear_structure_be9()
    
    # Pairing:
    # - 1s1 and 1s2: linked to protons in alpha1 (diametrically opposite)
    # - 2s1 and 2s2: linked to protons in alpha2 (diametrically opposite)
    
    return {
        '1s_electrons': {
            'electron1': {
                'position_m': pos_1s1.tolist(),
                'position_A': (pos_1s1 * 1e10).tolist(),
                'linked_to': 'alpha1_proton1',
                'paired_with': '1s_electron2'
            },
            'electron2': {
                'position_m': pos_1s2.tolist(),
                'position_A': (pos_1s2 * 1e10).tolist(),
                'linked_to': 'alpha1_proton2',
                'paired_with': '1s_electron1'
            }
        },
        '2s_electrons': {
            'electron3': {
                'position_m': pos_2s1.tolist(),
                'position_A': (pos_2s1 * 1e10).tolist(),
                'linked_to': 'alpha2_proton1',
                'paired_with': '2s_electron4'
            },
            'electron4': {
                'position_m': pos_2s2.tolist(),
                'position_A': (pos_2s2 * 1e10).tolist(),
                'linked_to': 'alpha2_proton2',
                'paired_with': '2s_electron3'
            }
        },
        'nuclear_structure': nuclear,
        'pairing_geometry': {
            '1s_axis': 'Z-axis (vertical)',
            '2s_axis': 'X-axis (horizontal, perpendicular to 1s)',
            'angle_between_pairs': '90° (perpendicular)'
        }
    }

def main():
    """Calculate Beryllium 2s pairing structure."""
    print("="*80)
    print("BERYLLIUM: NEXT ELEMENT IN 2s SHELL")
    print("2s² Pairing Geometry")
    print("="*80)
    
    be = BerylliumStructure()
    pairing = calculate_proton_electron_pairing()
    
    print(f"\nElement: {be.symbol} - {be.name} (Z={be.Z})")
    print(f"Configuration: {be.electron_config}")
    print(f"Nuclear Structure: {be.nuclear_structure}")
    
    print(f"\n1s² Electrons (He core):")
    e1s = pairing['1s_electrons']
    print(f"  Electron 1: r = {np.linalg.norm(e1s['electron1']['position_m']) * 1e10:.3f} Å, axis = Z")
    print(f"  Electron 2: r = {np.linalg.norm(e1s['electron2']['position_m']) * 1e10:.3f} Å, axis = -Z")
    print(f"  Paired: Diametrically opposite along Z-axis")
    
    print(f"\n2s² Electrons (new pairing):")
    e2s = pairing['2s_electrons']
    print(f"  Electron 3: r = {np.linalg.norm(np.array(e2s['electron3']['position_m'])) * 1e10:.3f} Å, axis = X")
    print(f"  Electron 4: r = {np.linalg.norm(np.array(e2s['electron4']['position_m'])) * 1e10:.3f} Å, axis = -X")
    print(f"  Paired: Diametrically opposite along X-axis")
    
    print(f"\nPairing Geometry:")
    geom = pairing['pairing_geometry']
    print(f"  1s axis: {geom['1s_axis']}")
    print(f"  2s axis: {geom['2s_axis']}")
    print(f"  Angle between pairs: {geom['angle_between_pairs']}")
    
    print(f"\nNuclear Structure (Macro Scale):")
    nuc = pairing['nuclear_structure']
    print(f"  Alpha 1 center: {nuc['alpha1_center_cm']} cm")
    print(f"  Alpha 2 center: {nuc['alpha2_center_cm']} cm")
    print(f"  Bridge neutron: {nuc['bridge_neutron_cm']} cm")
    
    # Calculate 2s orbital properties
    pos_2s1, pos_2s2 = calculate_2s_pairing_geometry()
    vel_2s1, vel_2s2 = calculate_2s_velocities(pos_2s1, pos_2s2, np.array([0, 0, 0]))
    en_2s1, en_2s2 = calculate_2s_energies(np.linalg.norm(pos_2s1))
    
    print(f"\n2s Electron Properties:")
    print(f"  Orbital radius: {np.linalg.norm(pos_2s1) * 1e10:.3f} Å")
    print(f"  Velocity: {np.linalg.norm(vel_2s1) / 2.99792458e8:.6f} c")
    print(f"  Energy: {en_2s1 / E_CHARGE:.4f} eV")
    
    # Save results
    results = {
        'element': {
            'Z': be.Z,
            'symbol': be.symbol,
            'name': be.name,
            'A': be.A,
            'config': be.electron_config,
            'nuclear_structure': be.nuclear_structure
        },
        'electron_pairing': pairing,
        '2s_properties': {
            'r_2s_A': float(np.linalg.norm(pos_2s1) * 1e10),
            'v_c': float(np.linalg.norm(vel_2s1) / 2.99792458e8),
            'energy_eV': float(en_2s1 / E_CHARGE),
            'Z_eff': 2.0
        }
    }
    
    output_file = Path(__file__).parent / "beryllium_2s_pairing_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()
