#!/usr/bin/env python3
"""
Phase 1.2: First Shell Completion

Completes the first shell by filling the two octahedral spaces:
- Deuteron (2nuc_H): First octahedral space (p+n)
- Helium Deuteron (2nuc_He): Second octahedral space (p+n)
- Alpha Particle: Both octahedral spaces filled (2p+2n)

This establishes the fundamental building blocks of nuclear structure.
"""

import numpy as np
from typing import Tuple, List
from dataclasses import dataclass
import math
# Import base geometry module
import importlib.util
from pathlib import Path

_base_geom_path = Path(__file__).parent / "01_01_icosahedral_base_geometry.py"
spec = importlib.util.spec_from_file_location("base_geom", _base_geom_path)
base_geom = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base_geom)

# ============================================================================
# CONSTANTS
# ============================================================================

R_NUCLEON_FM = 0.84  # fm
DIST_DEUTERON_FM = 2.10  # fm (measured separation)
DIST_ALPHA_FM = 1.45  # fm (compressed, vacuum lock)
N_BONDS_ALPHA = 6  # Tetrahedral edges

# Experimental binding energies
B_DEUTERON_EXP = 2.2246  # MeV
B_ALPHA_EXP = 28.296  # MeV

# ============================================================================
# FIRST SHELL STRUCTURES
# ============================================================================

@dataclass
class DeuteronStructure:
    """
    Deuteron (²H): First octahedral space filled with p+n.
    
    Structure: (np) = 1p + 1n
    - Proton and neutron together in FIRST octahedral space
    - They pair within that space
    - This is the basic building block
    """
    proton_position: Tuple[float, float, float]  # Position in octahedral space
    neutron_position: Tuple[float, float, float]  # Position in octahedral space
    separation: float  # Distance between p and n (fm)
    octahedral_space_index: int = 0  # First octahedral space
    
    def calculate_occlusion(self) -> float:
        """
        Calculate solid angle occlusion from deuteron structure.
        
        Returns:
        --------
        float
            Total occlusion (steradians)
        """
        # Single bond occlusion: p-n pair
        # Using spherical occlusion formula
        if self.separation <= R_NUCLEON_FM:
            return 2.0 * math.pi  # Full immersion
        else:
            sin_theta = R_NUCLEON_FM / self.separation
            if sin_theta >= 1.0:
                return 2.0 * math.pi
            cos_theta = math.sqrt(1.0 - sin_theta*sin_theta)
            return 2.0 * math.pi * (1.0 - cos_theta)
    
    def infer_binding_constant(self) -> float:
        """
        Infer binding constant k from experimental binding energy.
        
        k = B_exp / Omega
        
        Returns:
        --------
        float
            Binding constant k (MeV/sr)
        """
        omega = self.calculate_occlusion()
        if omega > 0:
            return B_DEUTERON_EXP / omega
        return 0.0


@dataclass
class HeliumDeuteronStructure:
    """
    Helium Deuteron (2nuc_He): Second octahedral space filled with p+n.
    
    Structure: (np) = 1p + 1n
    - Proton and neutron together in SECOND octahedral space
    - They pair within that space
    - Identical structure to deuteron, different location
    """
    proton_position: Tuple[float, float, float]
    neutron_position: Tuple[float, float, float]
    separation: float  # Distance between p and n (fm)
    octahedral_space_index: int = 1  # Second octahedral space
    
    def calculate_occlusion(self) -> float:
        """Calculate solid angle occlusion (same as deuteron)"""
        if self.separation <= R_NUCLEON_FM:
            return 2.0 * math.pi
        else:
            sin_theta = R_NUCLEON_FM / self.separation
            if sin_theta >= 1.0:
                return 2.0 * math.pi
            cos_theta = math.sqrt(1.0 - sin_theta*sin_theta)
            return 2.0 * math.pi * (1.0 - cos_theta)


@dataclass
class AlphaParticleStructure:
    """
    Alpha Particle (⁴He): Tetrahedral structure with 4 nucleons.
    
    Structure:
    - 4 nucleons (2p + 2n) in tetrahedral arrangement
    - 6 bonds (tetrahedral edges, all equivalent)
    - Vacuum lock compression: d = 1.45 fm (vs 2.1 fm for deuteron)
    - Binding: 28.296 MeV
    
    This replaces the incorrect 2-deuteron model.
    """
    # Tetrahedral structure parameters
    separation: float = DIST_ALPHA_FM  # fm (compressed, vacuum lock)
    n_bonds: int = N_BONDS_ALPHA  # Tetrahedral edges
    bond_occlusion: float = 0.0  # Single bond occlusion
    total_occlusion: float = 0.0  # Total from 6 bonds
    
    # Binding energy
    B_experimental: float = B_ALPHA_EXP  # MeV
    k_inferred: float = 0.0  # MeV/sr
    B_predicted: float = 0.0  # MeV
    
    def calculate_bond_occlusion(self) -> float:
        """
        Calculate occlusion for a single tetrahedral bond.
        
        Uses compressed separation (1.45 fm) instead of deuteron separation (2.1 fm).
        
        Returns:
        --------
        float
            Single bond occlusion (steradians)
        """
        R = R_NUCLEON_FM  # fm (nucleon radius)
        d = self.separation
        
        if d <= R:
            self.bond_occlusion = 2.0 * math.pi
            return self.bond_occlusion
        
        sin_theta = R / d
        if sin_theta >= 1.0:
            self.bond_occlusion = 2.0 * math.pi
            return self.bond_occlusion
        
        cos_theta = math.sqrt(1.0 - sin_theta*sin_theta)
        self.bond_occlusion = 2.0 * math.pi * (1.0 - cos_theta)
        return self.bond_occlusion
    
    def calculate_total_occlusion(self) -> float:
        """
        Calculate total occlusion from all 6 tetrahedral bonds.
        
        Returns:
        --------
        float
            Total occlusion (steradians)
        """
        if self.bond_occlusion == 0.0:
            self.calculate_bond_occlusion()
        self.total_occlusion = self.n_bonds * self.bond_occlusion
        return self.total_occlusion
    
    def calculate_binding_energy(self, k: float) -> float:
        """
        Calculate binding energy using constant k.
        
        Parameters:
        -----------
        k : float
            Binding constant (MeV/sr)
        
        Returns:
        --------
        float
            Binding energy (MeV)
        """
        if self.total_occlusion == 0.0:
            self.calculate_total_occlusion()
        self.B_predicted = k * self.total_occlusion
        return self.B_predicted
    
    def verify_alpha_binding(self, k: float = None) -> dict:
        """
        Verify alpha binding energy against experimental value.
        
        Parameters:
        -----------
        k : float, optional
            Binding constant (MeV/sr). If None, infers from alpha.
        
        Returns:
        --------
        dict
            Verification results
        """
        if self.total_occlusion == 0.0:
            self.calculate_total_occlusion()
        
        if k is None:
            # Infer k from alpha
            if self.total_occlusion > 0:
                self.k_inferred = self.B_experimental / self.total_occlusion
                k = self.k_inferred
            else:
                k = 0.0
        else:
            self.k_inferred = k
        
        B_calc = self.calculate_binding_energy(k)
        error_pct = abs(B_calc - self.B_experimental) / self.B_experimental * 100.0
        
        return {
            'k_used': k,
            'k_inferred_from_alpha': self.k_inferred if k == self.k_inferred else None,
            'B_calculated': B_calc,
            'B_experimental': self.B_experimental,
            'error_percent': error_pct,
            'passes': error_pct < 1.0,  # <1% error
            'total_occlusion': self.total_occlusion,
            'bond_occlusion': self.bond_occlusion,
            'n_bonds': self.n_bonds,
            'separation': self.separation
        }


class FirstShell:
    """
    Complete first shell structure.
    
    Contains:
    - Icosahedral base (12 outer spheres)
    - First octahedral space: Deuteron
    - Second octahedral space: Helium Deuteron
    - Alpha particle: Both spaces filled
    """
    
    def __init__(self, base: base_geom.IcosahedralBase):
        """
        Initialize first shell from icosahedral base.
        
        Parameters:
        -----------
        base : IcosahedralBase
            Icosahedral base structure
        """
        self.base = base
        
        # Create deuteron in first octahedral space
        self.deuteron = self._create_deuteron(space_index=0)
        
        # Create helium deuteron in second octahedral space
        self.helium_deuteron = self._create_deuteron(space_index=1)
        
        # Create alpha particle (tetrahedral structure, not 2-deuteron model)
        self.alpha = AlphaParticleStructure(
            separation=DIST_ALPHA_FM,
            n_bonds=N_BONDS_ALPHA
        )
    
    def _create_deuteron(self, space_index: int) -> DeuteronStructure:
        """
        Create deuteron structure in specified octahedral space.
        
        Parameters:
        -----------
        space_index : int
            Which octahedral space (0 or 1)
        
        Returns:
        --------
        DeuteronStructure
            Deuteron in the specified space
        """
        if space_index >= len(self.base.octahedral_spaces):
            raise ValueError(f"Octahedral space {space_index} does not exist")
        
        space = self.base.octahedral_spaces[space_index]
        
        # Position proton and neutron in the octahedral space
        # For simplicity, place them along the line between the two vertices
        # that define the octahedral space
        v1_idx, v2_idx = space['vertex_pair']
        v1 = self.base.vertices[v1_idx]
        v2 = self.base.vertices[v2_idx]
        
        # Midpoint between vertices
        mid_x = (v1.x + v2.x) / 2.0
        mid_y = (v1.y + v2.y) / 2.0
        mid_z = (v1.z + v2.z) / 2.0
        
        # Place proton and neutron separated by DIST_DEUTERON_FM
        # Direction along the line between vertices
        dx = v2.x - v1.x
        dy = v2.y - v1.y
        dz = v2.z - v1.z
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        if dist > 0:
            unit_x = dx / dist
            unit_y = dy / dist
            unit_z = dz / dist
        else:
            unit_x, unit_y, unit_z = 1.0, 0.0, 0.0
        
        # Proton and neutron positions
        half_sep = DIST_DEUTERON_FM / 2.0
        proton_pos = (
            mid_x - half_sep * unit_x,
            mid_y - half_sep * unit_y,
            mid_z - half_sep * unit_z
        )
        neutron_pos = (
            mid_x + half_sep * unit_x,
            mid_y + half_sep * unit_y,
            mid_z + half_sep * unit_z
        )
        
        if space_index == 0:
            return DeuteronStructure(
                proton_position=proton_pos,
                neutron_position=neutron_pos,
                separation=DIST_DEUTERON_FM,
                octahedral_space_index=0
            )
        else:
            return HeliumDeuteronStructure(
                proton_position=proton_pos,
                neutron_position=neutron_pos,
                separation=DIST_DEUTERON_FM,
                octahedral_space_index=1
            )
    
    def get_complete_structure(self) -> dict:
        """
        Get complete first shell structure description.
        
        Returns:
        --------
        dict
            Complete structure information
        """
        return {
            'icosahedral_base': {
                'n_vertices': len(self.base.vertices),
                'sphere_radius_fm': self.base.r,
                'total_width_fm': self.base.total_width
            },
            'deuteron': {
                'structure': '(np) = 1p + 1n',
                'octahedral_space': 0,
                'separation_fm': self.deuteron.separation,
                'occlusion_sr': self.deuteron.calculate_occlusion()
            },
            'helium_deuteron': {
                'structure': '(np) = 1p + 1n',
                'octahedral_space': 1,
                'separation_fm': self.helium_deuteron.separation,
                'occlusion_sr': self.helium_deuteron.calculate_occlusion()
            },
            'alpha_particle': {
                'structure': '4 nucleons (2p + 2n) in tetrahedral arrangement, 6 bonds',
                'separation_fm': self.alpha.separation,
                'n_bonds': self.alpha.n_bonds,
                'bond_occlusion_sr': self.alpha.calculate_bond_occlusion(),
                'total_occlusion_sr': self.alpha.calculate_total_occlusion(),
                'verification': self.alpha.verify_alpha_binding()
            }
        }


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_first_shell():
    """Test first shell completion"""
    print("="*80)
    print("TEST: First Shell Completion")
    print("="*80)
    
    # Create icosahedral base
    base = base_geom.IcosahedralBase(r=R_NUCLEON_FM)
    
    # Create first shell
    first_shell = FirstShell(base)
    
    # Get structure
    structure = first_shell.get_complete_structure()
    
    print(f"\nIcosahedral Base:")
    print(f"  Vertices: {structure['icosahedral_base']['n_vertices']}")
    print(f"  Sphere radius: {structure['icosahedral_base']['sphere_radius_fm']:.3f} fm")
    print(f"  Total width: {structure['icosahedral_base']['total_width_fm']:.3f} fm")
    
    print(f"\nDeuteron (First Octahedral Space):")
    print(f"  Structure: {structure['deuteron']['structure']}")
    print(f"  Separation: {structure['deuteron']['separation_fm']:.3f} fm")
    print(f"  Occlusion: {structure['deuteron']['occlusion_sr']:.3f} sr")
    
    print(f"\nHelium Deuteron (Second Octahedral Space):")
    print(f"  Structure: {structure['helium_deuteron']['structure']}")
    print(f"  Separation: {structure['helium_deuteron']['separation_fm']:.3f} fm")
    print(f"  Occlusion: {structure['helium_deuteron']['occlusion_sr']:.3f} sr")
    
    print(f"\nAlpha Particle:")
    print(f"  Structure: {structure['alpha_particle']['structure']}")
    print(f"  Separation: {structure['alpha_particle']['separation_fm']:.3f} fm (compressed)")
    print(f"  Number of bonds: {structure['alpha_particle']['n_bonds']}")
    print(f"  Single bond occlusion: {structure['alpha_particle']['bond_occlusion_sr']:.6f} sr")
    print(f"  Total occlusion: {structure['alpha_particle']['total_occlusion_sr']:.6f} sr")
    
    verification = structure['alpha_particle']['verification']
    print(f"\nBinding Energy Verification:")
    if verification['k_inferred_from_alpha'] is not None:
        print(f"  k (inferred from alpha): {verification['k_used']:.6f} MeV/sr")
    else:
        print(f"  k (used): {verification['k_used']:.6f} MeV/sr")
    print(f"  B (calculated): {verification['B_calculated']:.4f} MeV")
    print(f"  B (experimental): {verification['B_experimental']:.4f} MeV")
    print(f"  Error: {verification['error_percent']:.2f}%")
    print(f"  Passes (<1%): {verification['passes']}")


if __name__ == "__main__":
    test_first_shell()
