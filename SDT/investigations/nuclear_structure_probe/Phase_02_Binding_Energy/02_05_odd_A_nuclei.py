#!/usr/bin/env python3
"""
Phase 2.5: Odd-A and Mixed Nuclei

Analyzes odd-A and mixed nuclei:
- Triton (³H): n-p-n linear
- Helion (³He): p-n-p linear
- Li-6: Alpha + Deuteron attachment
- Pairing effects and corrections

These nuclei don't fit the simple alpha cluster model and may require corrections.
"""

import math
import importlib.util
from pathlib import Path

# Import modules
_calc_path = Path(__file__).parent / "02_01_occlusion_binding_calculator.py"
spec = importlib.util.spec_from_file_location("calc", _calc_path)
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)

# ============================================================================
# CONSTANTS
# ============================================================================

R_NUCLEON_FM = 0.84  # fm
DIST_DEUTERON_FM = 2.10  # fm
DIST_ALPHA_FM = 1.45  # fm

# Experimental binding energies
B_TRITON_EXP = 8.482  # MeV (³H)
B_HELION_EXP = 7.718  # MeV (³He)
B_LI6_EXP = 31.995  # MeV


# ============================================================================
# ODD-A NUCLEI STRUCTURES
# ============================================================================

class TritonStructure:
    """
    Triton (³H): n-p-n linear arrangement.
    
    Structure: 3 nucleons in linear chain
    - n-p bond: 2.10 fm (deuteron-like)
    - p-n bond: 2.10 fm (deuteron-like)
    - n-n separation: ~4.2 fm (through proton)
    """
    
    def __init__(self):
        self.B_experimental = B_TRITON_EXP
        self.name = "Triton (³H)"
        self.n_bonds = 2  # Two p-n bonds
        self.bond_separation = DIST_DEUTERON_FM
        self.total_occlusion = 0.0
    
    def calculate_total_occlusion(self) -> float:
        """Calculate total occlusion from 2 p-n bonds"""
        single_bond_occlusion = calc.spherical_occlusion(R_NUCLEON_FM, self.bond_separation)
        self.total_occlusion = self.n_bonds * single_bond_occlusion
        return self.total_occlusion
    
    def predict_binding_energy(self, k: float) -> float:
        """Predict binding energy"""
        if self.total_occlusion == 0.0:
            self.calculate_total_occlusion()
        return k * self.total_occlusion


class HelionStructure:
    """
    Helion (³He): p-n-p linear arrangement.
    
    Structure: 3 nucleons in linear chain
    - p-n bond: 2.10 fm (deuteron-like)
    - n-p bond: 2.10 fm (deuteron-like)
    - p-p separation: ~4.2 fm (through neutron)
    """
    
    def __init__(self):
        self.B_experimental = B_HELION_EXP
        self.name = "Helion (³He)"
        self.n_bonds = 2  # Two p-n bonds
        self.bond_separation = DIST_DEUTERON_FM
        self.total_occlusion = 0.0
    
    def calculate_total_occlusion(self) -> float:
        """Calculate total occlusion from 2 p-n bonds"""
        single_bond_occlusion = calc.spherical_occlusion(R_NUCLEON_FM, self.bond_separation)
        self.total_occlusion = self.n_bonds * single_bond_occlusion
        return self.total_occlusion
    
    def predict_binding_energy(self, k: float) -> float:
        """Predict binding energy"""
        if self.total_occlusion == 0.0:
            self.calculate_total_occlusion()
        return k * self.total_occlusion


class Lithium6Structure:
    """
    Lithium-6: Alpha + Deuteron attachment.
    
    Structure:
    - One alpha particle (4 nucleons)
    - One deuteron attached
    - Attachment bond between alpha and deuteron
    """
    
    def __init__(self):
        self.B_experimental = B_LI6_EXP
        self.name = "Lithium-6"
        
        # Alpha internal occlusion (from Phase 2.3)
        _alpha_path = Path(__file__).parent / "02_03_alpha_structure.py"
        spec = importlib.util.spec_from_file_location("alpha_mod", _alpha_path)
        alpha_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(alpha_mod)
        
        alpha = alpha_mod.AlphaParticleStructure()
        alpha.calculate_total_occlusion()
        self.alpha_occlusion = alpha.total_occlusion
        
        # Deuteron occlusion
        self.deuteron_occlusion = calc.spherical_occlusion(R_NUCLEON_FM, DIST_DEUTERON_FM)
        
        # Attachment bond (alpha-deuteron)
        # Effective radius of alpha
        ALPHA_CENTER_DIST = DIST_ALPHA_FM * 0.6124
        ALPHA_EFFECTIVE_RADIUS = ALPHA_CENTER_DIST + R_NUCLEON_FM
        ATTACHMENT_SEPARATION = 2.5  # fm (estimated)
        
        self.attachment_occlusion = calc.spherical_occlusion(
            ALPHA_EFFECTIVE_RADIUS,
            ATTACHMENT_SEPARATION
        )
        
        self.total_occlusion = 0.0
    
    def calculate_total_occlusion(self) -> float:
        """Calculate total occlusion"""
        self.total_occlusion = (
            self.alpha_occlusion +
            self.deuteron_occlusion +
            self.attachment_occlusion
        )
        return self.total_occlusion
    
    def predict_binding_energy(self, k: float) -> float:
        """Predict binding energy"""
        if self.total_occlusion == 0.0:
            self.calculate_total_occlusion()
        return k * self.total_occlusion


# ============================================================================
# PAIRING CORRECTIONS
# ============================================================================

def calculate_pairing_correction(Z: int, N: int) -> float:
    """
    Calculate pairing correction factor.
    
    Even-even nuclei: f = 1.0 (perfect pairing)
    Odd-odd nuclei: f < 1.0 (geometric stress)
    Odd-even: f ≈ 0.95 (moderate pairing)
    
    Parameters:
    -----------
    Z : int
        Atomic number
    N : int
        Neutron number
    
    Returns:
    --------
    float
        Pairing correction factor
    """
    if Z % 2 == 0 and N % 2 == 0:
        return 1.0  # Even-even: perfect pairing
    elif Z % 2 == 1 and N % 2 == 1:
        return 0.9  # Odd-odd: geometric stress
    else:
        return 0.95  # Odd-even: moderate pairing


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_odd_A_nuclei():
    """Test odd-A nuclei"""
    print("="*80)
    print("TEST: Odd-A and Mixed Nuclei")
    print("="*80)
    
    # Get k from deuteron
    _deut_path = Path(__file__).parent / "02_02_deuteron_calibration.py"
    spec = importlib.util.spec_from_file_location("deut", _deut_path)
    deut = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(deut)
    
    deut_cal = deut.DeuteronCalibration()
    k = deut_cal.calibrate_k()
    
    print(f"\nUsing k from deuteron: {k:.6f} MeV/sr\n")
    
    # Test Triton
    print("="*80)
    triton = TritonStructure()
    triton.calculate_total_occlusion()
    B_pred = triton.predict_binding_energy(k)
    error = abs(B_pred - triton.B_experimental)
    error_pct = error / triton.B_experimental * 100.0
    
    print(f"{triton.name}:")
    print(f"  Total occlusion: {triton.total_occlusion:.6f} sr")
    print(f"  B_predicted: {B_pred:.4f} MeV")
    print(f"  B_experimental: {triton.B_experimental:.4f} MeV")
    print(f"  Error: {error:.4f} MeV ({error_pct:.2f}%)")
    
    # Test Helion
    print("\n" + "="*80)
    helion = HelionStructure()
    helion.calculate_total_occlusion()
    B_pred = helion.predict_binding_energy(k)
    error = abs(B_pred - helion.B_experimental)
    error_pct = error / helion.B_experimental * 100.0
    
    print(f"{helion.name}:")
    print(f"  Total occlusion: {helion.total_occlusion:.6f} sr")
    print(f"  B_predicted: {B_pred:.4f} MeV")
    print(f"  B_experimental: {helion.B_experimental:.4f} MeV")
    print(f"  Error: {error:.4f} MeV ({error_pct:.2f}%)")
    
    # Test Li-6
    print("\n" + "="*80)
    li6 = Lithium6Structure()
    li6.calculate_total_occlusion()
    B_pred = li6.predict_binding_energy(k)
    error = abs(B_pred - li6.B_experimental)
    error_pct = error / li6.B_experimental * 100.0
    
    print(f"{li6.name}:")
    print(f"  Alpha occlusion: {li6.alpha_occlusion:.6f} sr")
    print(f"  Deuteron occlusion: {li6.deuteron_occlusion:.6f} sr")
    print(f"  Attachment occlusion: {li6.attachment_occlusion:.6f} sr")
    print(f"  Total occlusion: {li6.total_occlusion:.6f} sr")
    print(f"  B_predicted: {B_pred:.4f} MeV")
    print(f"  B_experimental: {li6.B_experimental:.4f} MeV")
    print(f"  Error: {error:.4f} MeV ({error_pct:.2f}%)")


if __name__ == "__main__":
    test_odd_A_nuclei()
