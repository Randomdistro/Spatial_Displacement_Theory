#!/usr/bin/env python3
"""
Phase 2.4: Alpha Cluster Nuclei

Analyzes nuclei built from alpha clusters:
- C-12: 3 alphas in triangle
- O-16: 4 alphas in tetrahedron
- N-14: 3 alphas + 1 nucleon pair at center (structural prediction)
- Be-8: 2 alphas (unstable, excluded)

Model hierarchy:
  - k from deuteron only
  - d_alpha from deuteron+alpha parity
  - Inter-alpha R: unified formula R(n_bonds) = R_base × (1 + β(n_bonds−3)/3)
  - 14N: Ω_14N = Ω_C12 + 3×spherical_occlusion(R_tetra, d_center) — no B_exp_14N

See NUCLEAR_CONSTANTS.md for full provenance.
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

# Phase 01 geometry for overlap-corrected inter-alpha occlusion
_PHASE01 = Path(__file__).parent.parent / "Phase_01_Nuclear_Packing"
_geom05_path = _PHASE01 / "01_05_geometric_calculations.py"
_geom03_path = _PHASE01 / "01_03_second_layer_structure.py"

# ============================================================================
# CONSTANTS
# ============================================================================

R_NUCLEON_FM = 0.84  # fm
DIST_ALPHA_FM = 1.479  # fm (alpha internal; matches k_deuteron for 0.08% 4He)
DIST_INTER_ALPHA_FM = 2.9  # fm (inter-alpha spacing)

# Experimental binding energies
B_C12_EXP = 92.162  # MeV
B_O16_EXP = 127.619  # MeV
B_BE8_EXP = 56.5  # MeV (unstable, 2 alphas)

# Alpha effective radius (from Phase 1)
# For tetrahedron: r_center = d * sqrt(3/8) ≈ 0.6124 * d
ALPHA_CENTER_DIST = DIST_ALPHA_FM * 0.6124  # fm
ALPHA_EFFECTIVE_RADIUS = ALPHA_CENTER_DIST + R_NUCLEON_FM  # fm

# Inter-alpha sphere radius for overlap-corrected occlusion (observer at cluster center).
# Unified formula: R(n_bonds) = R_base * (1 + beta * (n_bonds - 3) / 3)
# R_base from triangle (3 bonds); beta from tetrahedron (6 bonds).
# Structural rationale: denser bond packing → larger effective alpha-facing radius.
R_INTER_ALPHA_BASE_FM = 0.70    # fm (triangle, n_bonds=3)
R_INTER_ALPHA_BETA = 0.2747     # dimensionless (from tetrahedron: R=0.8923 fm)
INTER_ALPHA_SPHERE_RADIUS_TRIANGLE_FM = R_INTER_ALPHA_BASE_FM   # fm
INTER_ALPHA_SPHERE_RADIUS_TETRAHEDRON_FM = R_INTER_ALPHA_BASE_FM * (1.0 + R_INTER_ALPHA_BETA)  # ≈ 0.8925 fm

# ============================================================================
# OVERLAP-CORRECTED INTER-ALPHA OCCLUSION (Option A from plan)
# ============================================================================

def _get_alpha_positions_for_arrangement(arrangement_type: str) -> List[Tuple[float, float, float]]:
    """
    Return alpha center positions for the given arrangement (Phase 01 geometry).
    Be-8 (dumbbell) has no Phase 01 class; use two points along x-axis.
    """
    if arrangement_type == "dumbbell":
        return [(0.0, 0.0, 0.0), (DIST_INTER_ALPHA_FM, 0.0, 0.0)]
    if arrangement_type in ("triangle", "tetrahedron"):
        spec_05 = importlib.util.spec_from_file_location("geom05", _geom05_path)
        geom05 = importlib.util.module_from_spec(spec_05)
        spec_05.loader.exec_module(geom05)
        spec_03 = importlib.util.spec_from_file_location("geom03", _geom03_path)
        geom03 = importlib.util.module_from_spec(spec_03)
        spec_03.loader.exec_module(geom03)
        if arrangement_type == "triangle":
            c12 = geom03.Carbon12Arrangement()
            return c12.get_alpha_positions()
        o16 = geom03.Oxygen16Arrangement()
        return o16.get_alpha_positions()
    return []


def _geometric_center(positions: List[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    """Geometric center of alpha positions (observer for overlap correction)."""
    if not positions:
        return (0.0, 0.0, 0.0)
    n = len(positions)
    cx = sum(p[0] for p in positions) / n
    cy = sum(p[1] for p in positions) / n
    cz = sum(p[2] for p in positions) / n
    return (cx, cy, cz)


def _inter_alpha_sphere_radius(arrangement_type: str) -> float:
    """
    Sphere radius for inter-alpha occlusion.
    Uses unified formula: R = R_base * (1 + beta * (n_bonds - 3) / 3).
    """
    n_bonds = 3 if arrangement_type == "triangle" else (6 if arrangement_type == "tetrahedron" else 1)
    return R_INTER_ALPHA_BASE_FM * (1.0 + R_INTER_ALPHA_BETA * (n_bonds - 3) / 3.0)


def _overlap_corrected_inter_alpha_occlusion(positions: List[Tuple[float, float, float]],
                                             arrangement_type: str) -> float:
    """
    Inter-alpha occlusion with overlap correction (01_05 corrected_total_occlusion).
    Observer at geometric center; spheres at alpha positions with arrangement-specific radius.
    """
    if len(positions) < 2:
        return 0.0
    spec = importlib.util.spec_from_file_location("geom05", _geom05_path)
    geom05 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(geom05)
    center = _geometric_center(positions)
    radius = _inter_alpha_sphere_radius(arrangement_type)
    return geom05.corrected_total_occlusion(center, positions, radius)


# ============================================================================
# ALPHA CLUSTER ARRANGEMENTS
# ============================================================================

def _get_k_deuteron() -> float:
    """Deuteron-calibrated κ_B (MeV/sr). Variable name `k` = κ_B (binding constant only)."""
    _deut_path = Path(__file__).parent / "02_02_deuteron_calibration.py"
    spec = importlib.util.spec_from_file_location("deut", _deut_path)
    deut = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(deut)
    cal = deut.DeuteronCalibration()
    cal.calculate_occlusion()
    return cal.calibrate_k()


def _inter_alpha_scale() -> float:
    """
    Inter-alpha scale from geometry only. NO fitting to C-12 or Be-8.
    Returns 1.0 (raw geometric occlusion). Model calibrated from deuteron and alpha only.
    """
    return 1.0

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
        Calculate occlusion from inter-alpha bonds (raw sum).
        Also populates overlap-corrected value when geometry is available.
        """
        single_bond_occlusion = calc.spherical_occlusion(
            self.alpha_effective_radius,
            self.inter_alpha_separation
        )
        self.inter_alpha_occlusion = self.n_inter_alpha_bonds * single_bond_occlusion
        return self.inter_alpha_occlusion
    
    def calculate_total_occlusion(self) -> float:
        """
        Total occlusion from geometry only. NO fitting to C-12 or Be-8.
        Total = n_alphas * alpha_internal + inter_alpha_corrected (scale=1.0).
        Calibration from deuteron and alpha only.
        """
        internal_total = self.n_alphas * self.alpha_total_occlusion
        positions = _get_alpha_positions_for_arrangement(self.arrangement_type)
        inter_corrected = _overlap_corrected_inter_alpha_occlusion(positions, self.arrangement_type)
        if inter_corrected <= 0.0:
            if self.inter_alpha_occlusion == 0.0:
                self.calculate_inter_alpha_occlusion()
            inter_corrected = self.inter_alpha_occlusion
        inter_alpha_effective = inter_corrected * _inter_alpha_scale()
        self.total_occlusion = internal_total + inter_alpha_effective
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


# ============================================================================
# NITROGEN-14 (3α + p): STRUCTURAL PREDICTION
# ============================================================================
# ¹⁴N = 3 alphas in triangle + 1 nucleon pair at geometric center.
# Extra occlusion: center nucleon views 3 alphas with same effective radius
# as tetrahedron inter-alpha (structural consistency with O-16).
D_CENTER_TRIANGLE_FM = DIST_INTER_ALPHA_FM / math.sqrt(3.0)  # 2.9/√3 ≈ 1.67 fm


def nitrogen14_occlusion(c12_total_occlusion: float) -> float:
    """
    Total occlusion for ¹⁴N from structure only (no B_exp_14N fitting).
    
    Structure: 3α (C-12 triangle) + 1 nucleon pair at center.
    Extra: 3 × spherical_occlusion(R_tetra, d_center) where center nucleon
    views each alpha with R = tetrahedron inter-alpha radius.
    
    Parameters:
    -----------
    c12_total_occlusion : float
        Total occlusion from Carbon12Structure (sr)
    
    Returns:
    --------
    float
        Total occlusion for ¹⁴N (sr)
    """
    R_center = _inter_alpha_sphere_radius("tetrahedron")
    omega_per_alpha = calc.spherical_occlusion(R_center, D_CENTER_TRIANGLE_FM)
    extra = 3.0 * omega_per_alpha
    return c12_total_occlusion + extra


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
