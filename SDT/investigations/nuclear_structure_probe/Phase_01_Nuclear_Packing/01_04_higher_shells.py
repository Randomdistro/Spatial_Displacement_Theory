#!/usr/bin/env python3
"""
Phase 1.4: Higher Shell Structures

Establishes higher shell structures (third layer and beyond):
- Shell condensation effects
- Packing density evolution
- Geometric closure conditions
- Shell progression rules

This enables construction of heavy nuclei.
"""

import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass
import math

# ============================================================================
# CONSTANTS
# ============================================================================

R_NUCLEON_FM = 0.84  # fm

# ============================================================================
# SHELL STRUCTURE
# ============================================================================

@dataclass
class NuclearShell:
    """
    Represents a nuclear shell.
    
    Shell structure:
    - Shell 0 (Center): r₀ = 0 (single central sphere)
    - Shell 1: r₁ = 2Rₛ = D (where Rₛ is sphere radius, D is diameter)
    - Shell k: r_k = k*D = 2*k*R_s
    """
    shell_number: int
    radius: float  # Distance from center to shell (fm)
    n_positions: int  # Number of positions in this shell
    positions: List[Tuple[float, float, float]]  # Positions of nucleons in shell
    is_complete: bool  # Whether shell is completely filled
    
    def calculate_packing_density(self) -> float:
        """
        Calculate packing density of this shell.
        
        Returns:
        --------
        float
            Packing density (dimensionless)
        """
        if self.n_positions == 0:
            return 0.0
        
        # Surface area of shell
        surface_area = 4.0 * math.pi * self.radius * self.radius
        
        # Area occupied by nucleons
        nucleon_area = self.n_positions * math.pi * R_NUCLEON_FM * R_NUCLEON_FM
        
        # Packing density = occupied area / total area
        return nucleon_area / surface_area if surface_area > 0 else 0.0


class ShellProgression:
    """
    Manages shell progression and condensation.
    
    Key Principle: All packings come from this order:
    1. Icosahedral base (12 spheres around center)
    2. Octahedral spaces fill (creating pairs)
    3. Next layer forms in icosahedral/dodecahedral interstitial spacings
    4. Each layer offsets the previous, condensing as shells are engaged
    """
    
    def __init__(self, nucleon_radius: float = R_NUCLEON_FM):
        """
        Initialize shell progression.
        
        Parameters:
        -----------
        nucleon_radius : float
            Nucleon radius (fm)
        """
        self.nucleon_radius = nucleon_radius
        self.diameter = 2.0 * nucleon_radius
        self.shells: List[NuclearShell] = []
    
    def add_shell(self, shell_number: int, positions: List[Tuple[float, float, float]]) -> NuclearShell:
        """
        Add a new shell.
        
        Parameters:
        -----------
        shell_number : int
            Shell number (0 = center, 1 = first, etc.)
        positions : List[Tuple[float, float, float]]
            Positions of nucleons in this shell
        
        Returns:
        --------
        NuclearShell
            Created shell
        """
        # Shell radius: r_k = k*D = 2*k*R_s
        radius = shell_number * self.diameter
        
        shell = NuclearShell(
            shell_number=shell_number,
            radius=radius,
            n_positions=len(positions),
            positions=positions,
            is_complete=False  # Will be determined by geometry
        )
        
        self.shells.append(shell)
        return shell
    
    def calculate_total_nucleons(self) -> int:
        """Calculate total number of nucleons across all shells"""
        return sum(shell.n_positions for shell in self.shells)
    
    def calculate_total_radius(self) -> float:
        """Calculate total radius (outermost shell + nucleon radius)"""
        if not self.shells:
            return self.nucleon_radius
        
        max_shell_radius = max(shell.radius for shell in self.shells)
        return max_shell_radius + self.nucleon_radius
    
    def analyze_condensation(self) -> Dict:
        """
        Analyze shell condensation effects.
        
        As each shell is engaged, the structure condenses, affecting:
        - Solid angle occlusion
        - Binding energy
        - Packing density
        
        Returns:
        --------
        dict
            Condensation analysis
        """
        analysis = {
            'shells': [],
            'total_packing_density': 0.0,
            'condensation_trend': []
        }
        
        cumulative_density = 0.0
        for shell in self.shells:
            density = shell.calculate_packing_density()
            cumulative_density += density
            
            shell_info = {
                'shell_number': shell.shell_number,
                'radius_fm': shell.radius,
                'n_positions': shell.n_positions,
                'packing_density': density,
                'cumulative_density': cumulative_density
            }
            analysis['shells'].append(shell_info)
            analysis['condensation_trend'].append(cumulative_density)
        
        analysis['total_packing_density'] = cumulative_density
        
        return analysis
    
    def check_geometric_closure(self) -> Dict:
        """
        Check for geometric closure conditions.
        
        Geometric closure occurs when:
        - Shell is completely filled
        - Next shell cannot form without overlap
        - Structure reaches maximum packing density
        
        Returns:
        --------
        dict
            Closure analysis
        """
        closure_info = {
            'is_closed': False,
            'closed_shells': [],
            'next_shell_possible': True
        }
        
        for shell in self.shells:
            # Check if shell is complete (all positions filled)
            # This is geometry-dependent
            if shell.n_positions > 0:
                # For now, assume shell is complete if it has expected number of positions
                # (This would be determined by icosahedral/dodecahedral geometry)
                closure_info['closed_shells'].append(shell.shell_number)
        
        # Check if next shell is possible
        if self.shells:
            last_shell = self.shells[-1]
            next_radius = (last_shell.shell_number + 1) * self.diameter
            
            # If next shell would overlap with current, closure reached
            if next_radius <= last_shell.radius + 2.0 * self.nucleon_radius:
                closure_info['next_shell_possible'] = False
                closure_info['is_closed'] = True
        
        return closure_info


# ============================================================================
# PACKING DENSITY EVOLUTION
# ============================================================================

def calculate_packing_density_evolution(max_shells: int = 5) -> Dict:
    """
    Calculate how packing density evolves with shell number.
    
    Parameters:
    -----------
    max_shells : int
        Maximum number of shells to calculate
    
    Returns:
    --------
    dict
        Packing density evolution
    """
    progression = ShellProgression()
    
    # Shell 0: Center (1 nucleon)
    progression.add_shell(0, [(0.0, 0.0, 0.0)])
    
    # Shell 1: Icosahedral (12 nucleons)
    # Would be populated from icosahedral base
    # For now, use placeholder
    shell1_positions = [(2.0*R_NUCLEON_FM, 0.0, 0.0)] * 12  # Simplified
    progression.add_shell(1, shell1_positions)
    
    # Higher shells would be populated from interstices
    # For demonstration, add placeholder shells
    for k in range(2, max_shells + 1):
        # Placeholder: would be calculated from actual geometry
        n_positions = 20 * (k - 1)  # Rough estimate
        positions = [(k * 2.0 * R_NUCLEON_FM, 0.0, 0.0)] * n_positions
        progression.add_shell(k, positions)
    
    return progression.analyze_condensation()


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_higher_shells():
    """Test higher shell structures"""
    print("="*80)
    print("TEST: Higher Shell Structures")
    print("="*80)
    
    progression = ShellProgression()
    
    # Add shells
    progression.add_shell(0, [(0.0, 0.0, 0.0)])  # Center
    progression.add_shell(1, [(2.0*R_NUCLEON_FM, 0.0, 0.0)] * 12)  # Icosahedral
    
    print(f"\nShell Structure:")
    print(f"  Total nucleons: {progression.calculate_total_nucleons()}")
    print(f"  Total radius: {progression.calculate_total_radius():.3f} fm")
    
    for shell in progression.shells:
        print(f"\n  Shell {shell.shell_number}:")
        print(f"    Radius: {shell.radius:.3f} fm")
        print(f"    Positions: {shell.n_positions}")
        print(f"    Packing density: {shell.calculate_packing_density():.4f}")
    
    # Condensation analysis
    condensation = progression.analyze_condensation()
    print(f"\nCondensation Analysis:")
    print(f"  Total packing density: {condensation['total_packing_density']:.4f}")
    print(f"  Condensation trend: {condensation['condensation_trend']}")
    
    # Closure check
    closure = progression.check_geometric_closure()
    print(f"\nGeometric Closure:")
    print(f"  Is closed: {closure['is_closed']}")
    print(f"  Closed shells: {closure['closed_shells']}")
    print(f"  Next shell possible: {closure['next_shell_possible']}")


if __name__ == "__main__":
    test_higher_shells()
