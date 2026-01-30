"""
Geometric Atomic Model - 1:1 Proton-Electron Pairing
====================================================

Key principles:
- Alpha particle at center (2p + 2n)
- Each electron is inextricably linked to a specific proton
- Paired electrons are diametrically opposite each other
- Their linked nucleons are also diametrically opposite
- Electrons do NOT change hands inside the atom
- Screening emerges from geometric arrangement, not "effective charge"

Physical scales:
- Protons: 20kg GP cement
- Neutrons: 20kg off-white
- Electrons: 11 grams
- Electrons at exact perihelion
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import json
from pathlib import Path

# ==============================================================================
# CODATA 2018 PHYSICAL CONSTANTS
# ==============================================================================

C = 2.99792458e8  # m/s
H = 6.62607015e-34  # J·s
HBAR = 1.054571817e-34  # J·s
E_CHARGE = 1.602176634e-19  # C
EPSILON_0 = 8.8541878128e-12  # F/m
M_E = 9.1093837015e-31  # kg
M_P = 1.67262192369e-27  # kg
M_N = 1.67492749804e-27  # kg
ALPHA = 7.2973525693e-3
K_E = 1.0 / (4.0 * np.pi * EPSILON_0)
A_0 = 5.29177210903e-11  # m
RYDBERG_EV = 13.605693122994  # eV

# Physical scales
M_PROTON_PHYSICAL = 20.0  # kg
M_NEUTRON_PHYSICAL = 20.0  # kg
M_ELECTRON_PHYSICAL = 0.011  # kg

# ==============================================================================
# GEOMETRIC STRUCTURES
# ==============================================================================

@dataclass
class Nucleon:
    """Nucleon with position and linked electron."""
    type: str  # 'p' or 'n'
    position: np.ndarray  # 3D position (m)
    mass: float  # kg
    linked_electron_id: Optional[int] = None  # ID of inextricably linked electron

@dataclass
class Electron:
    """Electron at exact perihelion, linked to specific proton."""
    id: int  # Unique identifier
    n: int  # Principal quantum number
    l: int  # Angular momentum
    m: int  # Magnetic quantum number
    position: np.ndarray  # 3D position at perihelion (m)
    velocity: np.ndarray  # 3D velocity (m/s)
    mass: float  # kg
    energy: float  # J
    angular_momentum: np.ndarray  # kg·m²/s
    linked_proton_id: int  # ID of inextricably linked proton
    paired_electron_id: Optional[int] = None  # ID of diametrically opposite paired electron

@dataclass
class AlphaCluster:
    """Alpha particle (2p + 2n) at center."""
    protons: List[Nucleon]
    neutrons: List[Nucleon]
    center: np.ndarray

@dataclass
class Atom:
    """Complete atomic structure with 1:1 proton-electron pairing."""
    Z: int  # Atomic number
    A: int  # Mass number
    symbol: str
    name: str
    alpha_clusters: List[AlphaCluster]
    nucleons: List[Nucleon]
    electrons: List[Electron]
    total_energy: float  # J
    screening_factors: Dict[int, float]  # Screening for each electron from geometry

# ==============================================================================
# GEOMETRIC ARRANGEMENT FUNCTIONS
# ==============================================================================

def create_alpha_at_center() -> AlphaCluster:
    """
    Create alpha particle (2p + 2n) at center.
    Protons will be linked to electrons, positioned diametrically opposite.
    """
    center = np.array([0.0, 0.0, 0.0])
    ALPHA_RADIUS = 1.7e-15  # m
    
    # Two protons at opposite positions (will be linked to electrons)
    pole_axis = np.array([0.0, 0.0, 1.0])
    p1_pos = center + pole_axis * ALPHA_RADIUS
    p2_pos = center - pole_axis * ALPHA_RADIUS
    
    protons = [
        Nucleon('p', p1_pos, M_PROTON_PHYSICAL),
        Nucleon('p', p2_pos, M_PROTON_PHYSICAL)
    ]
    
    # Two neutrons in perpendicular plane
    perp1 = np.array([1.0, 0.0, 0.0])
    perp2 = np.array([0.0, 1.0, 0.0])
    
    n1_pos = center + perp1 * ALPHA_RADIUS
    n2_pos = center + perp2 * ALPHA_RADIUS
    
    neutrons = [
        Nucleon('n', n1_pos, M_NEUTRON_PHYSICAL),
        Nucleon('n', n2_pos, M_NEUTRON_PHYSICAL)
    ]
    
    return AlphaCluster(protons, neutrons, center)

def create_paired_electrons(Z: int, nucleus_center: np.ndarray, 
                            nucleons: List[Nucleon]) -> List[Electron]:
    """
    Create electrons with 1:1 pairing to protons.
    
    Rules:
    - Alpha at center
    - Two electrons above and below (for H, He)
    - All paired electrons are diametrically opposite
    - Their linked nucleons are also diametrically opposite
    - Electrons are inextricably linked to specific protons
    """
    electrons = []
    electron_id = 0
    
    # Get protons (will be linked to electrons)
    protons = [n for n in nucleons if n.type == 'p']
    
    # For H (Z=1): One electron above, linked to one proton
    if Z >= 1:
        # First electron: above center
        pole_axis = np.array([0.0, 0.0, 1.0])
        r_1s = A_0  # For H, r = a_0
        pos_e1 = nucleus_center + pole_axis * r_1s
        
        # Velocity perpendicular (circular orbit)
        v_mag = np.sqrt(K_E * E_CHARGE * E_CHARGE / (M_E * r_1s))
        vel_e1 = np.cross(pole_axis, np.array([1.0, 0.0, 0.0])) * v_mag
        vel_e1 = vel_e1 / np.linalg.norm(vel_e1) * v_mag
        
        energy_e1 = -0.5 * K_E * E_CHARGE * E_CHARGE / r_1s
        L_e1 = M_E * np.cross(pos_e1 - nucleus_center, vel_e1)
        
        # Link to first proton
        linked_proton_id = 0
        
        e1 = Electron(
            id=electron_id,
            n=1, l=0, m=0,
            position=pos_e1,
            velocity=vel_e1,
            mass=M_ELECTRON_PHYSICAL,
            energy=energy_e1,
            angular_momentum=L_e1,
            linked_proton_id=linked_proton_id,
            paired_electron_id=None
        )
        electrons.append(e1)
        protons[linked_proton_id].linked_electron_id = electron_id
        electron_id += 1
    
    # For He (Z=2): Two electrons, diametrically opposite
    if Z >= 2:
        # Second electron: below center (diametrically opposite)
        pos_e2 = nucleus_center - pole_axis * r_1s
        vel_e2 = -vel_e1  # Opposite velocity
        
        energy_e2 = energy_e1
        L_e2 = M_E * np.cross(pos_e2 - nucleus_center, vel_e2)
        
        # Link to second proton
        linked_proton_id = 1
        
        e2 = Electron(
            id=electron_id,
            n=1, l=0, m=0,
            position=pos_e2,
            velocity=vel_e2,
            mass=M_ELECTRON_PHYSICAL,
            energy=energy_e2,
            angular_momentum=L_e2,
            linked_proton_id=linked_proton_id,
            paired_electron_id=0  # Paired with e1
        )
        electrons.append(e2)
        electrons[0].paired_electron_id = electron_id  # Link back
        protons[linked_proton_id].linked_electron_id = electron_id
        electron_id += 1
    
    # For Li and above: Add more electrons following same pattern
    # Each electron is linked to a specific proton
    # Paired electrons are diametrically opposite
    
    if Z >= 3:
        # Li: 3rd electron in 2s shell
        # Position: Above, but further out
        r_2s = 4 * A_0  # n=2, screened
        pos_e3 = nucleus_center + pole_axis * r_2s
        
        v_mag_2s = np.sqrt(K_E * E_CHARGE * E_CHARGE / (M_E * r_2s))
        vel_e3 = np.cross(pole_axis, np.array([1.0, 0.0, 0.0])) * v_mag_2s
        vel_e3 = vel_e3 / np.linalg.norm(vel_e3) * v_mag_2s
        
        energy_e3 = -0.5 * K_E * E_CHARGE * E_CHARGE / r_2s
        L_e3 = M_E * np.cross(pos_e3 - nucleus_center, vel_e3)
        
        # For Z > 2, need more protons (add them as needed)
        # For now, link to first proton (will need to expand nucleon structure)
        linked_proton_id = 0  # Placeholder - need to add more protons
        
        e3 = Electron(
            id=electron_id,
            n=2, l=0, m=0,
            position=pos_e3,
            velocity=vel_e3,
            mass=M_ELECTRON_PHYSICAL,
            energy=energy_e3,
            angular_momentum=L_e3,
            linked_proton_id=linked_proton_id,
            paired_electron_id=None
        )
        electrons.append(e3)
        electron_id += 1
    
    # Continue pattern for higher Z...
    # Each electron linked to specific proton
    # Paired electrons diametrically opposite
    
    return electrons

def calculate_screening_from_geometry(electrons: List[Electron], 
                                      nucleus_center: np.ndarray) -> Dict[int, float]:
    """
    Calculate screening factors from geometric arrangement.
    
    Screening = how much other electrons/nucleons block the field
    This comes from spatial geometry, not "effective charge"
    """
    screening = {}
    
    for e in electrons:
        # Distance from nucleus
        r_e = np.linalg.norm(e.position - nucleus_center)
        
        # Count how many other electrons are between this electron and nucleus
        # Or how much geometry blocks the field
        
        # Simple model: screening from electrons closer to nucleus
        num_screening = sum(1 for other in electrons 
                           if other.id != e.id and 
                           np.linalg.norm(other.position - nucleus_center) < r_e)
        
        # Screening factor: each closer electron reduces field by ~1/Z
        # But this is geometric, not "charge"
        screening_factor = 1.0 - (num_screening / max(1, len(electrons)))
        
        screening[e.id] = screening_factor
    
    return screening

def build_atom(Z: int, A: int, symbol: str, name: str) -> Atom:
    """
    Build complete atomic structure with 1:1 proton-electron pairing.
    """
    nucleus_center = np.array([0.0, 0.0, 0.0])
    
    # Create alpha at center
    alpha = create_alpha_at_center()
    
    # For Z > 2, need more nucleons
    # For now, use alpha structure
    all_nucleons = alpha.protons + alpha.neutrons
    
    # Create electrons with 1:1 pairing
    electrons = create_paired_electrons(Z, nucleus_center, all_nucleons)
    
    # Calculate screening from geometry
    screening = calculate_screening_from_geometry(electrons, nucleus_center)
    
    # Total energy
    total_energy = sum(e.energy for e in electrons)
    
    return Atom(
        Z=Z, A=A, symbol=symbol, name=name,
        alpha_clusters=[alpha],
        nucleons=all_nucleons,
        electrons=electrons,
        total_energy=total_energy,
        screening_factors=screening
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
        'num_nucleons': len(atom.nucleons),
        'num_electrons': len(atom.electrons),
        'total_energy_J': atom.total_energy,
        'total_energy_eV': atom.total_energy / E_CHARGE,
        'electron_details': [],
        'pairing_details': []
    }
    
    for e in atom.electrons:
        r = np.linalg.norm(e.position - np.array([0, 0, 0]))
        v = np.linalg.norm(e.velocity)
        L_mag = np.linalg.norm(e.angular_momentum)
        screening = atom.screening_factors.get(e.id, 1.0)
        
        # Find linked proton
        linked_proton = next((n for n in atom.nucleons 
                             if n.linked_electron_id == e.id), None)
        proton_pos = linked_proton.position if linked_proton else None
        
        results['electron_details'].append({
            'id': e.id,
            'shell': f"{e.n}{'spdfg'[e.l] if e.l < 5 else '?'}",
            'n': e.n,
            'l': e.l,
            'm': e.m,
            'r_A': float(r * 1e10),
            'v_c': float(v / C),
            'energy_eV': float(e.energy / E_CHARGE),
            'L_mag': float(L_mag),
            'linked_proton_id': e.linked_proton_id,
            'paired_electron_id': e.paired_electron_id,
            'screening_factor': float(screening),
            'position': e.position.tolist()
        })
        
        if e.paired_electron_id is not None:
            results['pairing_details'].append({
                'electron_1_id': e.id,
                'electron_2_id': e.paired_electron_id,
                'diametrically_opposite': True
            })
    
    return results

def main():
    """Build and analyze first 10 elements."""
    elements = [
        (1, 1, 'H', 'Hydrogen'),
        (2, 4, 'He', 'Helium'),
        (3, 7, 'Li', 'Lithium'),
        (4, 9, 'Be', 'Beryllium'),
        (5, 11, 'B', 'Boron'),
        (6, 12, 'C', 'Carbon'),
        (7, 14, 'N', 'Nitrogen'),
        (8, 16, 'O', 'Oxygen'),
        (9, 19, 'F', 'Fluorine'),
        (10, 20, 'Ne', 'Neon'),
    ]
    
    all_results = {}
    
    for Z, A, symbol, name in elements:
        print(f"Building {symbol} (Z={Z})...")
        atom = build_atom(Z, A, symbol, name)
        results = analyze_atom(atom)
        all_results[symbol] = results
        
        print(f"  {len(atom.electrons)} electrons")
        print(f"  Total energy: {results['total_energy_eV']:.4f} eV")
        print(f"  Pairings: {len(results['pairing_details'])}")
    
    # Save results
    output_file = Path(__file__).parent / "geometric_atomic_model_paired_results.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()
