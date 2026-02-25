#!/usr/bin/env python3
"""
Phase 2.1: Occlusion-Based Binding Calculator

Core calculator for binding energy from solid angle occlusion.
Implements the fundamental relationship: B = k * Omega_total

Key principle: DISCOVER k from data, don't assume it.
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass
import math

# Import Phase 1 geometric utilities
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "Phase_01_Nuclear_Packing"))

# ============================================================================
# CONSTANTS
# ============================================================================

R_NUCLEON_FM = 0.84  # fm (nucleon radius)

# Experimental binding energies (MeV) - reference values
B_EXP = {
    'H1': 0.0,
    'H2': 2.2246,      # Deuteron
    'H3': 8.482,       # Triton
    'He3': 7.718,      # Helion
    'He4': 28.296,     # Alpha
    'Li6': 31.995,
    'Li7': 39.245,
    'Be8': 56.5,       # Unstable, 2 alphas
    'Be9': 58.165,
    'B10': 64.751,
    'B11': 76.205,
    'C12': 92.162,
    'C13': 97.108,
    'C14': 105.285,
    'N14': 104.659,
    'N15': 115.492,
    'O16': 127.619,
    'O17': 131.763,
    'O18': 139.808,
    'F19': 147.801,
    'Ne20': 160.645,
    'Fe56': 492.275,
}


# ============================================================================
# OCCLUSION CALCULATIONS
# ============================================================================

def spherical_occlusion(radius: float, distance: float) -> float:
    """
    Calculate solid angle occlusion of a sphere at a given distance.
    
    Formula: Omega = 2*pi*(1 - cos theta) where sin theta = R/d
    Geometric interpretation: observer at distance d from sphere center;
    sphere of radius R subtends solid angle Omega.
    
    Edge cases (physically correct):
    - d < R: observer inside sphere → full sky subtended → 4π sr
    - d = R: observer on sphere surface → hemisphere → 2π sr
    - d > R: standard formula
    
    Parameters:
    -----------
    radius : float
        Radius of occluding sphere (fm)
    distance : float
        Distance from observer to sphere center (fm)
    
    Returns:
    --------
    float
        Solid angle occlusion (steradians)
    """
    if distance <= 0.0:
        return 0.0
    if distance < radius:
        return 4.0 * math.pi  # Observer inside sphere: full sky
    if distance == radius:
        return 2.0 * math.pi  # Observer on surface: hemisphere
    
    sin_theta = radius / distance
    if sin_theta >= 1.0:
        return 2.0 * math.pi
    
    cos_theta = math.sqrt(1.0 - sin_theta * sin_theta)
    return 2.0 * math.pi * (1.0 - cos_theta)


def distance_between_points(p1: Tuple[float, float, float],
                           p2: Tuple[float, float, float]) -> float:
    """Calculate Euclidean distance between two points"""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)


# ============================================================================
# BOND CLASSIFICATION
# ============================================================================

@dataclass
class Bond:
    """Represents a single bond between two nucleons"""
    nucleon1_index: int
    nucleon2_index: int
    separation: float  # Distance between nucleons (fm)
    occlusion: float  # Solid angle occlusion (steradians)
    bond_type: str  # 'p-n', 'p-p', 'n-n'
    
    def calculate_occlusion(self, nucleon_radius: float = R_NUCLEON_FM) -> float:
        """Calculate occlusion for this bond"""
        self.occlusion = spherical_occlusion(nucleon_radius, self.separation)
        return self.occlusion


@dataclass
class NucleusBinding:
    """
    Represents binding energy calculation for a nucleus.
    
    Discovery-first approach:
    1. Calculate total occlusion Omega_total
    2. Measure k_i = B_exp / Omega_total for each nucleus
    3. Analyze patterns to discover universal k or family-specific k
    """
    Z: int  # Atomic number
    N: int  # Neutron number
    A: int  # Mass number
    name: str  # Element name
    
    # Geometric structure
    bonds: List[Bond]  # All bonds in nucleus
    total_occlusion: float  # Total solid angle occlusion (steradians)
    
    # Experimental data
    B_experimental: float  # Experimental binding energy (MeV)
    
    # Discovery results
    k_inferred: float  # k = B_exp / Omega (MeV/sr)
    B_predicted: float  # B = k * Omega (MeV)
    error_percent: float  # |B_pred - B_exp| / B_exp * 100
    
    # Overlap corrections
    overlap_correction: float  # Correction for overlapping occlusions (steradians)
    corrected_occlusion: float  # Omega - overlap_correction
    
    def __init__(self, Z: int, N: int, name: str = ""):
        self.Z = Z
        self.N = N
        self.A = Z + N
        self.name = name or f"Z{Z}N{N}"
        self.bonds = []
        self.total_occlusion = 0.0
        self.B_experimental = 0.0
        self.k_inferred = 0.0
        self.B_predicted = 0.0
        self.error_percent = 0.0
        self.overlap_correction = 0.0
        self.corrected_occlusion = 0.0
    
    def add_bond(self, bond: Bond):
        """Add a bond to the nucleus"""
        self.bonds.append(bond)
    
    def calculate_total_occlusion(self) -> float:
        """
        Calculate total occlusion from all bonds.
        
        Returns:
        --------
        float
            Total occlusion (steradians)
        """
        self.total_occlusion = sum(bond.occlusion for bond in self.bonds)
        return self.total_occlusion
    
    def calculate_overlap_correction(self) -> float:
        """
        Calculate overlap correction when bonds are close together.
        
        When bonds share nucleons or are very close, their occlusions overlap.
        This estimates the correction.
        
        Returns:
        --------
        float
            Overlap correction (steradians)
        """
        correction = 0.0
        n = len(self.bonds)
        
        # For each pair of bonds, check if they overlap
        for i in range(n):
            for j in range(i+1, n):
                bond1 = self.bonds[i]
                bond2 = self.bonds[j]
                
                # Check if bonds share a nucleon
                if (bond1.nucleon1_index == bond2.nucleon1_index or
                    bond1.nucleon1_index == bond2.nucleon2_index or
                    bond1.nucleon2_index == bond2.nucleon1_index or
                    bond1.nucleon2_index == bond2.nucleon2_index):
                    # Bonds share a nucleon - significant overlap
                    # Estimate: average occlusion times overlap factor
                    avg_occlusion = (bond1.occlusion + bond2.occlusion) / 2.0
                    correction += avg_occlusion * 0.1  # 10% overlap estimate
                
                # Check if bonds are very close (within 2 nucleon radii)
                elif bond1.separation < 2.0 * R_NUCLEON_FM and bond2.separation < 2.0 * R_NUCLEON_FM:
                    # Both bonds are short - potential overlap
                    avg_occlusion = (bond1.occlusion + bond2.occlusion) / 2.0
                    correction += avg_occlusion * 0.05  # 5% overlap estimate
        
        self.overlap_correction = correction
        self.corrected_occlusion = max(0.0, self.total_occlusion - correction)
        return correction
    
    def infer_binding_constant(self) -> float:
        """
        Infer binding constant k from experimental binding energy.
        
        k = B_exp / Omega_total
        
        This is the DISCOVERY step - we measure k from data.
        
        Returns:
        --------
        float
            Binding constant k (MeV/sr)
        """
        if self.total_occlusion > 0 and self.B_experimental > 0:
            self.k_inferred = self.B_experimental / self.total_occlusion
        else:
            self.k_inferred = 0.0
        
        return self.k_inferred
    
    def predict_binding_energy(self, k: float) -> float:
        """
        Predict binding energy using constant k.
        
        B = k * Omega_total
        
        Parameters:
        -----------
        k : float
            Binding constant (MeV/sr)
        
        Returns:
        --------
        float
            Predicted binding energy (MeV)
        """
        self.B_predicted = k * self.total_occlusion
        
        if self.B_experimental > 0:
            self.error_percent = abs(self.B_predicted - self.B_experimental) / self.B_experimental * 100.0
        
        return self.B_predicted
    
    def get_experimental_binding(self) -> Optional[float]:
        """
        Get experimental binding energy from database.
        
        Returns:
        --------
        Optional[float]
            Experimental binding energy (MeV) or None if not found
        """
        # Try to find in database
        key = f"{self.name}{self.A}"
        if key in B_EXP:
            self.B_experimental = B_EXP[key]
            return self.B_experimental
        
        # Try alternative naming
        if self.A == 1:
            self.B_experimental = B_EXP.get('H1', 0.0)
        elif self.A == 2 and self.Z == 1:
            self.B_experimental = B_EXP.get('H2', 0.0)
        elif self.A == 3 and self.Z == 1:
            self.B_experimental = B_EXP.get('H3', 0.0)
        elif self.A == 3 and self.Z == 2:
            self.B_experimental = B_EXP.get('He3', 0.0)
        elif self.A == 4 and self.Z == 2:
            self.B_experimental = B_EXP.get('He4', 0.0)
        
        return self.B_experimental if self.B_experimental > 0 else None


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_occlusion_binding_calculator():
    """Test occlusion binding calculator"""
    print("="*80)
    print("TEST: Occlusion-Based Binding Calculator")
    print("="*80)
    
    # Test spherical occlusion
    print("\nSpherical Occlusion Test:")
    R = 0.84  # fm
    d = 2.10  # fm (deuteron separation)
    occlusion = spherical_occlusion(R, d)
    print(f"  Radius: {R:.3f} fm")
    print(f"  Distance: {d:.3f} fm")
    print(f"  Occlusion: {occlusion:.3f} sr")
    print(f"  Fraction of 4*pi: {occlusion / (4.0 * math.pi):.3f}")
    
    # Test deuteron
    print("\nDeuteron Binding Test:")
    deuteron = NucleusBinding(Z=1, N=1, name="H")
    deuteron.A = 2
    
    # Single p-n bond
    bond = Bond(
        nucleon1_index=0,
        nucleon2_index=1,
        separation=2.10,  # fm
        occlusion=0.0,
        bond_type='p-n'
    )
    bond.calculate_occlusion()
    deuteron.add_bond(bond)
    
    deuteron.calculate_total_occlusion()
    deuteron.get_experimental_binding()
    k = deuteron.infer_binding_constant()
    
    print(f"  Total occlusion: {deuteron.total_occlusion:.3f} sr")
    print(f"  B_experimental: {deuteron.B_experimental:.3f} MeV")
    print(f"  k_inferred: {k:.3f} MeV/sr")
    
    # Predict with inferred k
    B_pred = deuteron.predict_binding_energy(k)
    print(f"  B_predicted: {B_pred:.3f} MeV")
    print(f"  Error: {deuteron.error_percent:.2f}%")


if __name__ == "__main__":
    test_occlusion_binding_calculator()
