#!/usr/bin/env python3
"""
Phase 2.4: Alpha Cluster Nuclei

Analyzes nuclei built from alpha clusters:
- C-12: 3 alphas in triangle
- O-16: 4 alphas in tetrahedron
- Be-8: 2 alphas (unstable)

Key: Inter-alpha bonding geometry and effective radius calculations.
"""

import math
import importlib.util
from pathlib import Path
from typing import List, Tuple

# Import modules
_calc_path = Path(__file__).parent / "02_01_occlusion_binding_calculator.py"
spec = importlib.util.spec_from_file_location("calc", _calc_path)
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)

_alpha_path = Path(__file__).parent / "02_03_alpha_structure.py"
spec = importlib.util.spec_from_file_location("alpha_mod", _alpha_path)
alpha_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alpha_mod)

# ============================================================================
# CONSTANTS
# ============================================================================

R_NUCLEON_FM = 0.84  # fm
DIST_ALPHA_FM = 1.45  # fm (alpha internal separation)
DIST_INTER_ALPHA_FM = 2.9  # fm (inter-alpha spacing)

# Experimental binding energies
B_C12_EXP = 92.162  # MeV
B_O16_EXP = 127.619  # MeV
B_BE8_EXP = 56.5  # MeV (unstable, 2 alphas)

# Alpha effective radius (from Phase 1)
# For tetrahedron: r_center = d * sqrt(3/8) ≈ 0.6124 * d
ALPHA_CENTER_DIST = DIST_ALPHA_FM * 0.6124  # fm
ALPHA_EFFECTIVE_RADIUS = ALPHA_CENTER_DIST + R_NUCLEON_FM  # fm


# ============================================================================
# ALPHA CLUSTER ARRANGEMENTS
# ============================================================================

class AlphaClusterNucleus:
    """
    Base class for alpha cluster nuclei.
    
    Structure:
    - Multiple alpha particles
    - Inter-alpha bonds
    - Total binding = internal alpha binding + inter-alpha binding
    """
    
    def __init__(self, n_alphas: int, arrangement_type: str):
        self.n_alphas = n_alphas
        self.arrangement_type = arrangement_type
        self.inter_alpha_separation = DIST_INTER_ALPHA_FM
        self.alpha_effective_radius = ALPHA_EFFECTIVE_RADIUS
        
        # Internal alpha binding (from Phase 2.3)
        self.alpha_structure = alpha_mod.AlphaParticleStructure()
        self.alpha_structure.calculate_total_occlusion()
        self.alpha_total_occlusion = self.alpha_structure.total_occlusion
        
        # Inter-alpha bonds
        self.n_inter_alpha_bonds = self._calculate_inter_alpha_bonds()
        self.inter_alpha_occlusion = 0.0
        self.total_occlusion = 0.0
    
    def _calculate_inter_alpha_bonds(self) -> int:
        """Calculate number of inter-alpha bonds"""
        if self.arrangement_type == 'triangle':
            return 3  # 3 alphas: 3 bonds
        elif self.arrangement_type == 'tetrahedron':
            return 6  # 4 alphas: 6 bonds
        elif self.arrangement_type == 'dumbbell':
            return 1  # 2 alphas: 1 bond
        else:
            # General: n(n-1)/2 for complete graph
            return self.n_alphas * (self.n_alphas - 1) // 2
    
    def calculate_inter_alpha_occlusion(self) -> float:
        """
        Calculate occlusion from inter-alpha bonds.
        
        Treats alphas as large spheres with effective radius.
        
        Returns:
        --------
        float
            Inter-alpha occlusion (steradians)
        """
        single_bond_occlusion = calc.spherical_occlusion(
            self.alpha_effective_radius,
            self.inter_alpha_separation
        )
        self.inter_alpha_occlusion = self.n_inter_alpha_bonds * single_bond_occlusion
        return self.inter_alpha_occlusion
    
    def calculate_total_occlusion(self) -> float:
        """
        Calculate total occlusion.
        
        Total = n_alphas * alpha_internal + inter_alpha
        
        Returns:
        --------
        float
            Total occlusion (steradians)
        """
        if self.inter_alpha_occlusion == 0.0:
            self.calculate_inter_alpha_occlusion()
        
        internal_total = self.n_alphas * self.alpha_total_occlusion
        self.total_occlusion = internal_total + self.inter_alpha_occlusion
        return self.total_occlusion
    
    def predict_binding_energy(self, k: float) -> float:
        """
        Predict binding energy using constant k.
        
        Parameters:
        -----------
        k : float
            Binding constant (MeV/sr)
        
        Returns:
        --------
        float
            Predicted binding energy (MeV)
        """
        if self.total_occlusion == 0.0:
            self.calculate_total_occlusion()
        
        return k * self.total_occlusion


class Carbon12Structure(AlphaClusterNucleus):
    """
    Carbon-12: 3 alphas in triangular arrangement.
    """
    
    def __init__(self):
        super().__init__(n_alphas=3, arrangement_type='triangle')
        self.B_experimental = B_C12_EXP
        self.name = "C-12"
    
    def get_structure_report(self, k: float) -> str:
        """Get structure report"""
        if self.total_occlusion == 0.0:
            self.calculate_total_occlusion()
        
        B_pred = self.predict_binding_energy(k)
        error = abs(B_pred - self.B_experimental)
        error_percent = error / self.B_experimental * 100.0
        
        return f"""
Carbon-12 Structure Report
==========================

Structure:
  - 3 alpha particles in triangular arrangement
  - 3 inter-alpha bonds
  - Inter-alpha separation: {self.inter_alpha_separation:.3f} fm
  - Alpha effective radius: {self.alpha_effective_radius:.3f} fm

Occlusion:
  - Internal alpha occlusion (per alpha): {self.alpha_total_occlusion:.6f} sr
  - Total internal (3 alphas): {self.n_alphas * self.alpha_total_occlusion:.6f} sr
  - Inter-alpha occlusion: {self.inter_alpha_occlusion:.6f} sr
  - Total occlusion: {self.total_occlusion:.6f} sr

Binding Energy:
  - B_predicted (k={k:.6f}): {B_pred:.4f} MeV
  - B_experimental: {self.B_experimental:.4f} MeV
  - Error: {error:.4f} MeV ({error_percent:.2f}%)
"""


class Oxygen16Structure(AlphaClusterNucleus):
    """
    Oxygen-16: 4 alphas in tetrahedral arrangement.
    """
    
    def __init__(self):
        super().__init__(n_alphas=4, arrangement_type='tetrahedron')
        self.B_experimental = B_O16_EXP
        self.name = "O-16"
    
    def get_structure_report(self, k: float) -> str:
        """Get structure report"""
        if self.total_occlusion == 0.0:
            self.calculate_total_occlusion()
        
        B_pred = self.predict_binding_energy(k)
        error = abs(B_pred - self.B_experimental)
        error_percent = error / self.B_experimental * 100.0
        
        return f"""
Oxygen-16 Structure Report
==========================

Structure:
  - 4 alpha particles in tetrahedral arrangement
  - 6 inter-alpha bonds
  - Inter-alpha separation: {self.inter_alpha_separation:.3f} fm
  - Alpha effective radius: {self.alpha_effective_radius:.3f} fm

Occlusion:
  - Internal alpha occlusion (per alpha): {self.alpha_total_occlusion:.6f} sr
  - Total internal (4 alphas): {self.n_alphas * self.alpha_total_occlusion:.6f} sr
  - Inter-alpha occlusion: {self.inter_alpha_occlusion:.6f} sr
  - Total occlusion: {self.total_occlusion:.6f} sr

Binding Energy:
  - B_predicted (k={k:.6f}): {B_pred:.4f} MeV
  - B_experimental: {self.B_experimental:.4f} MeV
  - Error: {error:.4f} MeV ({error_percent:.2f}%)
"""


class Beryllium8Structure(AlphaClusterNucleus):
    """
    Beryllium-8: 2 alphas in dumbbell arrangement (unstable).
    """
    
    def __init__(self):
        super().__init__(n_alphas=2, arrangement_type='dumbbell')
        self.B_experimental = B_BE8_EXP
        self.name = "Be-8"
        self.is_stable = False
    
    def get_structure_report(self, k: float) -> str:
        """Get structure report"""
        if self.total_occlusion == 0.0:
            self.calculate_total_occlusion()
        
        B_pred = self.predict_binding_energy(k)
        error = abs(B_pred - self.B_experimental)
        error_percent = error / self.B_experimental * 100.0
        
        return f"""
Beryllium-8 Structure Report
=============================

Structure:
  - 2 alpha particles in dumbbell arrangement
  - 1 inter-alpha bond
  - Inter-alpha separation: {self.inter_alpha_separation:.3f} fm
  - Alpha effective radius: {self.alpha_effective_radius:.3f} fm
  - Status: UNSTABLE (decays to 2 alphas)

Occlusion:
  - Internal alpha occlusion (per alpha): {self.alpha_total_occlusion:.6f} sr
  - Total internal (2 alphas): {self.n_alphas * self.alpha_total_occlusion:.6f} sr
  - Inter-alpha occlusion: {self.inter_alpha_occlusion:.6f} sr
  - Total occlusion: {self.total_occlusion:.6f} sr

Binding Energy:
  - B_predicted (k={k:.6f}): {B_pred:.4f} MeV
  - B_experimental: {self.B_experimental:.4f} MeV
  - Error: {error:.4f} MeV ({error_percent:.2f}%)
"""


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_alpha_clusters():
    """Test alpha cluster nuclei"""
    print("="*80)
    print("TEST: Alpha Cluster Nuclei")
    print("="*80)
    
    # Get k from deuteron
    _deut_path = Path(__file__).parent / "02_02_deuteron_calibration.py"
    spec = importlib.util.spec_from_file_location("deut", _deut_path)
    deut = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(deut)
    
    deut_cal = deut.DeuteronCalibration()
    k = deut_cal.calibrate_k()
    
    print(f"\nUsing k from deuteron: {k:.6f} MeV/sr\n")
    
    # Test C-12
    print("="*80)
    c12 = Carbon12Structure()
    c12.calculate_total_occlusion()
    B_pred_c12 = c12.predict_binding_energy(k)
    print(c12.get_structure_report(k))
    
    # Test O-16
    print("="*80)
    o16 = Oxygen16Structure()
    o16.calculate_total_occlusion()
    B_pred_o16 = o16.predict_binding_energy(k)
    print(o16.get_structure_report(k))
    
    # Test Be-8
    print("="*80)
    be8 = Beryllium8Structure()
    be8.calculate_total_occlusion()
    B_pred_be8 = be8.predict_binding_energy(k)
    print(be8.get_structure_report(k))


if __name__ == "__main__":
    test_alpha_clusters()
