"""
Geometric Atomic Model - Physical Framework
===========================================

Physical scales:
- Protons: 20kg GP cement
- Neutrons: 20kg off-white  
- Electrons: 11 grams
- Electrons at exact perihelion

Geometric arrangement:
- Alpha particle holds the poles
- 1s1 and 1s2 are paired, pushed opposites
- 1p1, 1p2 unpaired, forming tetrahedral offset below poles
- Concentric rings per shell
- Rings rotate according to neighbor arrangements

Uses CODATA 2018 for all physical constants.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict
import json
from pathlib import Path

# ==============================================================================
# CODATA 2018 PHYSICAL CONSTANTS
# ==============================================================================

# Speed of light
C = 2.99792458e8  # m/s

# Planck constant
H = 6.62607015e-34  # J·s
HBAR = 1.054571817e-34  # J·s = h/(2π)

# Elementary charge
E_CHARGE = 1.602176634e-19  # C

# Vacuum permittivity
EPSILON_0 = 8.8541878128e-12  # F/m

# Particle masses (kg)
M_E = 9.1093837015e-31  # Electron mass
M_P = 1.67262192369e-27  # Proton mass
M_N = 1.67492749804e-27  # Neutron mass

# Fine structure constant
ALPHA = 7.2973525693e-3
ALPHA_INV = 137.035999084

# Derived constants
K_E = 1.0 / (4.0 * np.pi * EPSILON_0)  # Coulomb constant
A_0 = 5.29177210903e-11  # Bohr radius (m)
RYDBERG_EV = 13.605693122994  # Rydberg energy (eV)
RYDBERG_J = RYDBERG_EV * E_CHARGE  # J

# Gravitational constant
G = 6.67430e-11  # m³/kg/s²

# ==============================================================================
# PHYSICAL SCALES (User Specification)
# ==============================================================================

M_PROTON_PHYSICAL = 20.0  # kg (GP cement)
M_NEUTRON_PHYSICAL = 20.0  # kg (off-white)
M_ELECTRON_PHYSICAL = 0.011  # kg (11 grams)

# Mass ratios (physical to actual)
RATIO_PROTON = M_PROTON_PHYSICAL / M_P
RATIO_NEUTRON = M_NEUTRON_PHYSICAL / M_N
RATIO_ELECTRON = M_ELECTRON_PHYSICAL / M_E

# ==============================================================================
# GEOMETRIC STRUCTURES
# ==============================================================================

@dataclass
class Nucleon:
    """Nucleon (proton or neutron) with physical position."""
    type: str  # 'p' or 'n'
    position: np.ndarray  # 3D position (m)
    mass: float  # kg (physical scale)
    
@dataclass
class Electron:
    """Electron at exact perihelion."""
    n: int  # Principal quantum number
    l: int  # Angular momentum
    m: int  # Magnetic quantum number
    position: np.ndarray  # 3D position at perihelion (m)
    velocity: np.ndarray  # 3D velocity (m/s)
    mass: float  # kg (physical scale)
    energy: float  # J
    angular_momentum: np.ndarray  # kg·m²/s

@dataclass
class AlphaCluster:
    """Alpha particle (2p + 2n) holding the poles."""
    protons: List[Nucleon]
    neutrons: List[Nucleon]
    center: np.ndarray  # Center position
    pole_axis: np.ndarray  # Pole direction (normalized)
    
@dataclass
class ElectronShell:
    """Concentric ring of electrons in a shell."""
    n: int  # Principal quantum number
    electrons: List[Electron]
    ring_radius: float  # m
    rotation_axis: np.ndarray  # Rotation axis from neighbor arrangement
    angular_velocity: float  # rad/s

@dataclass
class Atom:
    """Complete atomic structure."""
    Z: int  # Atomic number
    A: int  # Mass number
    symbol: str
    name: str
    alpha_clusters: List[AlphaCluster]
    nucleons: List[Nucleon]
    electron_shells: List[ElectronShell]
    electrons: List[Electron]
    total_energy: float  # J
    compactness: float  # Dimensionless measure

# ==============================================================================
# GEOMETRIC ARRANGEMENT FUNCTIONS
# ==============================================================================

def create_alpha_cluster(center: np.ndarray, pole_axis: np.ndarray) -> AlphaCluster:
    """
    Create alpha particle (2p + 2n) holding the poles.
    
    Geometry:
    - Two protons at poles
    - Two neutrons offset tetrahedrally
    - Forms stable alpha cluster
    """
    # Pole distance (from alpha particle structure)
    # Typical alpha particle radius ~1.7 fm
    ALPHA_RADIUS = 1.7e-15  # m
    
    # Protons at poles
    p1_pos = center + pole_axis * ALPHA_RADIUS
    p2_pos = center - pole_axis * ALPHA_RADIUS
    
    protons = [
        Nucleon('p', p1_pos, M_PROTON_PHYSICAL),
        Nucleon('p', p2_pos, M_PROTON_PHYSICAL)
    ]
    
    # Neutrons in tetrahedral positions (perpendicular to pole axis)
    # Find perpendicular vectors
    if abs(pole_axis[2]) < 0.9:
        perp1 = np.array([pole_axis[1], -pole_axis[0], 0])
    else:
        perp1 = np.array([0, pole_axis[2], -pole_axis[1]])
    perp1 = perp1 / np.linalg.norm(perp1)
    perp2 = np.cross(pole_axis, perp1)
    perp2 = perp2 / np.linalg.norm(perp2)
    
    # Tetrahedral angle
    TETRA_ANGLE = np.arccos(-1/3)  # ~109.47°
    offset = ALPHA_RADIUS * np.sin(TETRA_ANGLE / 2)
    
    n1_pos = center + perp1 * offset
    n2_pos = center + perp2 * offset
    
    neutrons = [
        Nucleon('n', n1_pos, M_NEUTRON_PHYSICAL),
        Nucleon('n', n2_pos, M_NEUTRON_PHYSICAL)
    ]
    
    return AlphaCluster(protons, neutrons, center, pole_axis)

def create_1s_electrons(Z: int, nucleus_center: np.ndarray) -> List[Electron]:
    """
    Create 1s electrons: 1s1 and 1s2 are paired, pushed opposites.
    
    Geometry:
    - 1s1 and 1s2 at opposite positions
    - At perihelion distance (closest approach)
    - Circular orbit in plane perpendicular to pairing axis
    """
    # 1s orbital radius from CODATA/Bohr model
    # For hydrogen: r_1s = a_0
    # For Z > 1: r_1s ≈ a_0 / Z_eff
    Z_EFF_1S = Z  # Core electrons see full Z
    
    r_1s = A_0 / Z_EFF_1S
    
    # Pairing axis (arbitrary, but consistent)
    pair_axis = np.array([1.0, 0.0, 0.0])
    
    electrons = []
    
    if Z >= 1:
        # 1s1: at +pair_axis
        pos_1s1 = nucleus_center + pair_axis * r_1s
        # Velocity perpendicular to position (circular orbit)
        # For circular orbit: mv²/r = kZe²/r², so v = sqrt(kZe²/(mr))
        # Use actual M_E for physics, not scaled mass
        v_mag_1s = np.sqrt(K_E * E_CHARGE * E_CHARGE * Z_EFF_1S / (M_E * r_1s))
        vel_1s1 = np.cross(pair_axis, np.array([0, 1, 0])) * v_mag_1s
        vel_1s1 = vel_1s1 / np.linalg.norm(vel_1s1) * v_mag_1s
        
        # Energy: For circular orbit, E = T + V = -(1/2) kZe²/r
        # T = (1/2)mv² = (1/2)kZe²/r, V = -kZe²/r, so E = -(1/2)kZe²/r
        energy_1s1 = -0.5 * K_E * E_CHARGE * E_CHARGE * Z_EFF_1S / r_1s
        # Angular momentum (use actual M_E)
        L_1s1 = M_E * np.cross(pos_1s1 - nucleus_center, vel_1s1)
        
        electrons.append(Electron(
            n=1, l=0, m=0,
            position=pos_1s1,
            velocity=vel_1s1,
            mass=M_ELECTRON_PHYSICAL,
            energy=energy_1s1,
            angular_momentum=L_1s1
        ))
    
    if Z >= 2:
        # 1s2: at -pair_axis (opposite)
        pos_1s2 = nucleus_center - pair_axis * r_1s
        vel_1s2 = -vel_1s1  # Opposite velocity
        energy_1s2 = energy_1s1  # Same energy
        L_1s2 = M_E * np.cross(pos_1s2 - nucleus_center, vel_1s2)  # Use actual M_E
        
        electrons.append(Electron(
            n=1, l=0, m=0,
            position=pos_1s2,
            velocity=vel_1s2,
            mass=M_ELECTRON_PHYSICAL,
            energy=energy_1s2,
            angular_momentum=L_1s2
        ))
    
    return electrons

def create_2p_electrons(Z: int, nucleus_center: np.ndarray, 
                        pole_axis: np.ndarray) -> List[Electron]:
    """
    Create 2p electrons: 1p1, 1p2 unpaired, forming tetrahedral offset below poles.
    
    Geometry:
    - 2p electrons in tetrahedral positions
    - Offset below the alpha particle poles
    - Unpaired (different m values)
    """
    if Z < 3:
        return []
    
    # 2p orbital radius
    # For Z=3 (Li): r_2p ≈ 4a_0 (n=2)
    # With screening: Z_eff ≈ Z - 2 (core screening)
    Z_EFF_2P = max(1.0, Z - 2)
    r_2p = 4 * A_0 / Z_EFF_2P
    
    # Tetrahedral positions below poles
    # Find perpendicular to pole axis
    if abs(pole_axis[2]) < 0.9:
        perp1 = np.array([pole_axis[1], -pole_axis[0], 0])
    else:
        perp1 = np.array([0, pole_axis[2], -pole_axis[1]])
    perp1 = perp1 / np.linalg.norm(perp1)
    perp2 = np.cross(pole_axis, perp1)
    perp2 = perp2 / np.linalg.norm(perp2)
    
    # Tetrahedral angles
    TETRA_ANGLE = np.arccos(-1/3)
    offset_angle = TETRA_ANGLE / 2
    
    electrons = []
    
    # 2p1: m = -1
    if Z >= 5:  # B and above
        dir_2p1 = -pole_axis * np.cos(offset_angle) + perp1 * np.sin(offset_angle)
        dir_2p1 = dir_2p1 / np.linalg.norm(dir_2p1)
        pos_2p1 = nucleus_center + dir_2p1 * r_2p
        
        v_mag_2p = np.sqrt(K_E * E_CHARGE * E_CHARGE * Z_EFF_2P / (M_E * r_2p))  # Use actual M_E
        vel_2p1 = np.cross(dir_2p1, perp2) * v_mag_2p
        vel_2p1 = vel_2p1 / np.linalg.norm(vel_2p1) * v_mag_2p
        
        energy_2p1 = -0.5 * K_E * E_CHARGE * E_CHARGE * Z_EFF_2P / r_2p  # Circular orbit: E = -(1/2)kZe²/r
        L_2p1 = M_E * np.cross(pos_2p1 - nucleus_center, vel_2p1)  # Use actual M_E
        
        electrons.append(Electron(
            n=2, l=1, m=-1,
            position=pos_2p1,
            velocity=vel_2p1,
            mass=M_ELECTRON_PHYSICAL,
            energy=energy_2p1,
            angular_momentum=L_2p1
        ))
    
    # 2p2: m = +1
    if Z >= 6:  # C and above
        dir_2p2 = -pole_axis * np.cos(offset_angle) - perp1 * np.sin(offset_angle)
        dir_2p2 = dir_2p2 / np.linalg.norm(dir_2p2)
        pos_2p2 = nucleus_center + dir_2p2 * r_2p
        
        v_mag_2p = np.sqrt(K_E * E_CHARGE * E_CHARGE * Z_EFF_2P / (M_E * r_2p))  # Use actual M_E
        vel_2p2 = np.cross(dir_2p2, -perp2) * v_mag_2p
        vel_2p2 = vel_2p2 / np.linalg.norm(vel_2p2) * v_mag_2p
        
        energy_2p2 = -0.5 * K_E * E_CHARGE * E_CHARGE * Z_EFF_2P / r_2p  # Circular orbit: E = -(1/2)kZe²/r
        L_2p2 = M_E * np.cross(pos_2p2 - nucleus_center, vel_2p2)  # Use actual M_E
        
        electrons.append(Electron(
            n=2, l=1, m=+1,
            position=pos_2p2,
            velocity=vel_2p2,
            mass=M_ELECTRON_PHYSICAL,
            energy=energy_2p2,
            angular_momentum=L_2p2
        ))
    
    return electrons

def create_concentric_ring(n: int, l: int, Z: int, nucleus_center: np.ndarray,
                           neighbor_electrons: List[Electron]) -> ElectronShell:
    """
    Create concentric ring of electrons for shell (n, l).
    
    Geometry:
    - Electrons arranged in ring
    - Ring radius from CODATA/Bohr model
    - Rotation axis determined by neighbor arrangements
    - Angular velocity from neighbor interactions
    """
    # Ring radius: r_n = n² a_0 / Z_eff
    Z_EFF = max(1.0, Z - 2 * (n - 1))  # Approximate screening
    r_n = n**2 * A_0 / Z_EFF
    
    # Number of electrons in this shell
    max_electrons = 2 * (2 * l + 1)  # 2s: 2, 2p: 6, 3d: 10, etc.
    num_electrons = min(max_electrons, Z - sum(2 * (2 * ll + 1) for ll in range(l)))
    
    # Determine rotation axis from neighbors
    if neighbor_electrons:
        # Average angular momentum direction
        total_L = sum(e.angular_momentum for e in neighbor_electrons)
        rotation_axis = total_L / np.linalg.norm(total_L) if np.linalg.norm(total_L) > 1e-30 else np.array([0, 0, 1])
    else:
        rotation_axis = np.array([0, 0, 1])
    
    # Angular velocity from neighbor interactions
    if neighbor_electrons:
        # Estimate from orbital periods
        avg_r = np.mean([np.linalg.norm(e.position - nucleus_center) for e in neighbor_electrons])
        avg_v = np.mean([np.linalg.norm(e.velocity) for e in neighbor_electrons])
        angular_velocity = avg_v / avg_r if avg_r > 0 else 0
    else:
        # Default from orbital mechanics
        v_orbital = np.sqrt(K_E * E_CHARGE * E_CHARGE * Z_EFF / (M_E * r_n))
        angular_velocity = v_orbital / r_n if r_n > 0 else 0
    
    # Create electrons in ring
    electrons = []
    for m in range(-l, l + 1):
        if len(electrons) >= num_electrons:
            break
        
        # Position on ring
        angle = 2 * np.pi * len(electrons) / num_electrons
        # Perpendicular to rotation axis
        if abs(rotation_axis[2]) < 0.9:
            perp1 = np.array([rotation_axis[1], -rotation_axis[0], 0])
        else:
            perp1 = np.array([0, rotation_axis[2], -rotation_axis[1]])
        perp1 = perp1 / np.linalg.norm(perp1)
        perp2 = np.cross(rotation_axis, perp1)
        perp2 = perp2 / np.linalg.norm(perp2)
        
        direction = perp1 * np.cos(angle) + perp2 * np.sin(angle)
        position = nucleus_center + direction * r_n
        
        # Velocity (tangential to ring)
        velocity = np.cross(rotation_axis, direction) * r_n * angular_velocity
        
        # Energy: For circular orbit, E = -(1/2)kZe²/r
        energy = -0.5 * K_E * E_CHARGE * E_CHARGE * Z_EFF / r_n
        
        # Angular momentum (use actual M_E)
        L = M_E * np.cross(position - nucleus_center, velocity)
        
        electrons.append(Electron(
            n=n, l=l, m=m,
            position=position,
            velocity=velocity,
            mass=M_ELECTRON_PHYSICAL,
            energy=energy,
            angular_momentum=L
        ))
    
    return ElectronShell(n, electrons, r_n, rotation_axis, angular_velocity)

def build_atom(Z: int, A: int, symbol: str, name: str) -> Atom:
    """
    Build complete atomic structure from geometric rules.
    """
    nucleus_center = np.array([0.0, 0.0, 0.0])
    
    # Create alpha clusters
    # For Z <= 2: single alpha (He)
    # For Z > 2: multiple alphas
    num_alphas = (A + 3) // 4  # Approximate
    alpha_clusters = []
    nucleons = []
    
    pole_axis = np.array([0.0, 0.0, 1.0])
    
    for i in range(num_alphas):
        if i == 0:
            center = nucleus_center
        else:
            # Offset subsequent alphas
            offset = 2.0e-15 * i  # ~2 fm spacing
            center = nucleus_center + pole_axis * offset
        
        alpha = create_alpha_cluster(center, pole_axis)
        alpha_clusters.append(alpha)
        nucleons.extend(alpha.protons)
        nucleons.extend(alpha.neutrons)
    
    # Create electrons
    all_electrons = []
    electron_shells = []
    
    # 1s electrons (paired, opposites)
    electrons_1s = create_1s_electrons(Z, nucleus_center)
    all_electrons.extend(electrons_1s)
    
    # 2s electrons (if any)
    if Z >= 3:
        shell_2s = create_concentric_ring(2, 0, Z, nucleus_center, electrons_1s)
        electron_shells.append(shell_2s)
        all_electrons.extend(shell_2s.electrons)
    
    # 2p electrons (tetrahedral, unpaired) - only if not already created
    if Z >= 5:  # B and above have 2p
        electrons_2p = create_2p_electrons(Z, nucleus_center, pole_axis)
        all_electrons.extend(electrons_2p)
        # Create 2p shell for remaining 2p electrons
        if len(all_electrons) < Z:
            remaining_2p = Z - len(all_electrons)
            if remaining_2p > 0:
                shell_2p = create_concentric_ring(2, 1, Z, nucleus_center, all_electrons)
                # Only add electrons up to Z
                for e in shell_2p.electrons[:remaining_2p]:
                    all_electrons.append(e)
                electron_shells.append(shell_2p)
    
    # Higher shells (3s, 3p, 3d, 4s, etc.)
    for n in range(3, 8):
        for l in range(min(n, 4)):  # s, p, d, f
            if len(all_electrons) >= Z:
                break
            shell = create_concentric_ring(n, l, Z, nucleus_center, all_electrons)
            # Only add electrons up to Z
            remaining = Z - len(all_electrons)
            if remaining > 0:
                for e in shell.electrons[:remaining]:
                    all_electrons.append(e)
                electron_shells.append(shell)
            if len(all_electrons) >= Z:
                break
    
    # Total energy
    total_energy = sum(e.energy for e in all_electrons)
    
    # Compactness: ratio of occupied volume to total volume
    if all_electrons:
        max_r = max(np.linalg.norm(e.position - nucleus_center) for e in all_electrons)
        min_r = min(np.linalg.norm(e.position - nucleus_center) for e in all_electrons)
        compactness = min_r / max_r if max_r > 0 else 1.0
    else:
        compactness = 1.0
    
    return Atom(
        Z=Z, A=A, symbol=symbol, name=name,
        alpha_clusters=alpha_clusters,
        nucleons=nucleons,
        electron_shells=electron_shells,
        electrons=all_electrons,
        total_energy=total_energy,
        compactness=compactness
    )

# ==============================================================================
# ANALYSIS AND OUTPUT
# ==============================================================================

def analyze_atom(atom: Atom) -> Dict:
    """Analyze atom and return detailed results."""
    results = {
        'Z': atom.Z,
        'symbol': atom.symbol,
        'name': atom.name,
        'A': atom.A,
        'num_alpha_clusters': len(atom.alpha_clusters),
        'num_nucleons': len(atom.nucleons),
        'num_electrons': len(atom.electrons),
        'total_energy_J': atom.total_energy,
        'total_energy_eV': atom.total_energy / E_CHARGE,
        'compactness': atom.compactness,
        'electron_details': []
    }
    
    for e in atom.electrons:
        r = np.linalg.norm(e.position - np.array([0, 0, 0]))
        v = np.linalg.norm(e.velocity)
        L_mag = np.linalg.norm(e.angular_momentum)
        
        results['electron_details'].append({
            'shell': f"{e.n}{'spdfg'[e.l] if e.l < 5 else '?'}",
            'n': e.n,
            'l': e.l,
            'm': e.m,
            'r_m': float(r),
            'r_A': float(r * 1e10),
            'v_m_s': float(v),
            'v_c': float(v / C),
            'energy_eV': float(e.energy / E_CHARGE),
            'L_mag': float(L_mag),
            'position': e.position.tolist(),
            'velocity': e.velocity.tolist()
        })
    
    return results

def main():
    """Build and analyze first 48 elements."""
    elements = [
        (1, 1, 'H', 'Hydrogen'), (2, 4, 'He', 'Helium'),
        (3, 7, 'Li', 'Lithium'), (4, 9, 'Be', 'Beryllium'),
        (5, 11, 'B', 'Boron'), (6, 12, 'C', 'Carbon'),
        (7, 14, 'N', 'Nitrogen'), (8, 16, 'O', 'Oxygen'),
        (9, 19, 'F', 'Fluorine'), (10, 20, 'Ne', 'Neon'),
        (11, 23, 'Na', 'Sodium'), (12, 24, 'Mg', 'Magnesium'),
        (13, 27, 'Al', 'Aluminum'), (14, 28, 'Si', 'Silicon'),
        (15, 31, 'P', 'Phosphorus'), (16, 32, 'S', 'Sulfur'),
        (17, 35, 'Cl', 'Chlorine'), (18, 40, 'Ar', 'Argon'),
        (19, 39, 'K', 'Potassium'), (20, 40, 'Ca', 'Calcium'),
        (21, 45, 'Sc', 'Scandium'), (22, 48, 'Ti', 'Titanium'),
        (23, 51, 'V', 'Vanadium'), (24, 52, 'Cr', 'Chromium'),
        (25, 55, 'Mn', 'Manganese'), (26, 56, 'Fe', 'Iron'),
        (27, 59, 'Co', 'Cobalt'), (28, 59, 'Ni', 'Nickel'),
        (29, 64, 'Cu', 'Copper'), (30, 65, 'Zn', 'Zinc'),
        (31, 70, 'Ga', 'Gallium'), (32, 73, 'Ge', 'Germanium'),
        (33, 75, 'As', 'Arsenic'), (34, 79, 'Se', 'Selenium'),
        (35, 80, 'Br', 'Bromine'), (36, 84, 'Kr', 'Krypton'),
        (37, 85, 'Rb', 'Rubidium'), (38, 88, 'Sr', 'Strontium'),
        (39, 89, 'Y', 'Yttrium'), (40, 91, 'Zr', 'Zirconium'),
        (41, 93, 'Nb', 'Niobium'), (42, 96, 'Mo', 'Molybdenum'),
        (43, 98, 'Tc', 'Technetium'), (44, 101, 'Ru', 'Ruthenium'),
        (45, 103, 'Rh', 'Rhodium'), (46, 106, 'Pd', 'Palladium'),
        (47, 108, 'Ag', 'Silver'), (48, 112, 'Cd', 'Cadmium'),
    ]
    
    all_results = {}
    
    for Z, A, symbol, name in elements:
        print(f"Building {symbol} (Z={Z})...")
        atom = build_atom(Z, A, symbol, name)
        results = analyze_atom(atom)
        all_results[symbol] = results
        
        print(f"  {len(atom.electrons)} electrons")
        print(f"  Total energy: {results['total_energy_eV']:.4f} eV")
        print(f"  Compactness: {results['compactness']:.4f}")
    
    # Save results
    output_file = Path(__file__).parent / "geometric_atomic_model_results.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()
