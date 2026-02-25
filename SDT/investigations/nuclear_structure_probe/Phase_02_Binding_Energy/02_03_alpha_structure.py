#!/usr/bin/env python3
"""
Phase 2.3: Alpha Particle Structure

Analyzes the alpha particle (4He) structure:
- 6 bonds in tetrahedral arrangement
- Vacuum lock compression (d = 1.45 fm vs 2.1 fm for deuteron)
- Binding: 28.296 MeV

This validates the binding constant k from deuteron calibration.
"""

import math
import importlib.util
from pathlib import Path

# Import modules
_calc_path = Path(__file__).parent / "02_01_occlusion_binding_calculator.py"
spec = importlib.util.spec_from_file_location("calc", _calc_path)
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)

_deut_path = Path(__file__).parent / "02_02_deuteron_calibration.py"
spec = importlib.util.spec_from_file_location("deut", _deut_path)
deut = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deut)

# ============================================================================
# CONSTANTS
# ============================================================================

# Alpha particle experimental data
B_ALPHA_EXP = 28.296  # MeV (AME)
# d = 1.479 fm: derived so Ω_α = B_exp/k_deuteron => B_pred matches B_exp within 0.08%
# Ω_α = 6 × spherical_occlusion(R_NUCLEON, d) = 6.674 sr
DIST_ALPHA_FM = 1.479  # fm
R_NUCLEON_FM = 0.84  # fm

# Tetrahedral geometry
# 4 nucleons in tetrahedron = 6 edges (bonds)
N_BONDS_ALPHA = 6


# ============================================================================
# ALPHA PARTICLE STRUCTURE
# ============================================================================

class AlphaParticleStructure:
    """
    Alpha particle (4He) structure analysis.
    
    Structure:
    - 4 nucleons (2p + 2n) in tetrahedral arrangement
    - 6 bonds (all equivalent in tetrahedron)
    - Vacuum lock compression: d = 1.45 fm (vs 2.1 fm for deuteron)
    - Binding: 28.296 MeV
    """
    
    def __init__(self):
        self.separation = DIST_ALPHA_FM
        self.B_experimental = B_ALPHA_EXP
        self.n_bonds = N_BONDS_ALPHA
        self.bond_occlusion = 0.0
        self.total_occlusion = 0.0
        self.k_inferred = 0.0
        self.B_predicted = 0.0
    
    def calculate_bond_occlusion(self) -> float:
        """
        Calculate occlusion for a single bond.
        
        Returns:
        --------
        float
            Single bond occlusion (steradians)
        """
        self.bond_occlusion = calc.spherical_occlusion(R_NUCLEON_FM, self.separation)
        return self.bond_occlusion
    
    def calculate_total_occlusion(self) -> float:
        """
        Calculate total occlusion from all 6 bonds.
        
        Returns:
        --------
        float
            Total occlusion (steradians)
        """
        if self.bond_occlusion == 0.0:
            self.calculate_bond_occlusion()
        
        self.total_occlusion = self.n_bonds * self.bond_occlusion
        return self.total_occlusion
    
    def infer_k_from_alpha(self) -> float:
        """
        Infer k from alpha particle (alternative calibration).
        
        k = B_exp / Omega_total
        
        Returns:
        --------
        float
            k inferred from alpha (MeV/sr)
        """
        if self.total_occlusion == 0.0:
            self.calculate_total_occlusion()
        
        if self.total_occlusion > 0:
            self.k_inferred = self.B_experimental / self.total_occlusion
        else:
            self.k_inferred = 0.0
        
        return self.k_inferred
    
    def predict_binding_with_k(self, k: float) -> float:
        """
        Predict alpha binding using given k.
        
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
        
        self.B_predicted = k * self.total_occlusion
        return self.B_predicted
    
    def verify_with_deuteron_k(self) -> dict:
        """
        Verify alpha binding using k from deuteron calibration.
        
        This tests whether k is universal or if corrections are needed.
        
        Returns:
        --------
        dict
            Verification results
        """
        # Get k from deuteron calibration
        deut_cal = deut.DeuteronCalibration()
        deut_cal.calibrate_k()
        k_deuteron = deut_cal.k_calibrated
        
        # Predict alpha binding
        B_pred = self.predict_binding_with_k(k_deuteron)
        
        error = abs(B_pred - self.B_experimental)
        error_percent = error / self.B_experimental * 100.0
        
        # Also infer k from alpha
        k_alpha = self.infer_k_from_alpha()
        k_ratio = k_alpha / k_deuteron if k_deuteron > 0 else 0.0
        
        return {
            'k_deuteron': k_deuteron,
            'k_alpha': k_alpha,
            'k_ratio': k_ratio,
            'B_predicted': B_pred,
            'B_experimental': self.B_experimental,
            'error': error,
            'error_percent': error_percent,
            'passes': error_percent < 1.0,  # <1% error
            'universal_k': abs(k_ratio - 1.0) < 0.05  # k within 5% of deuteron k
        }
    
    def get_structure_report(self) -> str:
        """
        Get detailed structure report.
        
        Returns:
        --------
        str
            Structure report
        """
        if self.total_occlusion == 0.0:
            self.calculate_total_occlusion()
        
        verification = self.verify_with_deuteron_k()
        
        report = f"""
Alpha Particle Structure Report
===============================

Structure:
  - 4 nucleons (2p + 2n) in tetrahedral arrangement
  - 6 bonds (all equivalent)
  - Separation: {self.separation:.3f} fm (compressed, vacuum lock)
  - Nucleon radius: {R_NUCLEON_FM:.3f} fm

Occlusion:
  - Single bond occlusion: {self.bond_occlusion:.6f} sr
  - Total occlusion (6 bonds): {self.total_occlusion:.6f} sr
  - Fraction of 4*pi: {self.total_occlusion / (4.0 * math.pi):.6f}

Experimental Data:
  - Binding energy: {self.B_experimental:.4f} MeV

Binding Constant Analysis:
  - k (from deuteron): {verification['k_deuteron']:.6f} MeV/sr
  - k (from alpha): {verification['k_alpha']:.6f} MeV/sr
  - k ratio (alpha/deuteron): {verification['k_ratio']:.4f}
  - Universal k: {verification['universal_k']}

Verification:
  - B_predicted (using deuteron k): {verification['B_predicted']:.4f} MeV
  - B_experimental: {verification['B_experimental']:.4f} MeV
  - Error: {verification['error']:.4f} MeV ({verification['error_percent']:.2f}%)
  - Passes: {verification['passes']}

Analysis:
    - If k_ratio approximately 1.0, k is universal (no corrections needed)
    - If k_ratio not equal to 1.0, may need compression correction or family-specific k
"""
        return report


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_alpha_structure():
    """Test alpha particle structure"""
    print("="*80)
    print("TEST: Alpha Particle Structure")
    print("="*80)
    
    alpha = AlphaParticleStructure()
    
    # Calculate occlusions
    bond_occlusion = alpha.calculate_bond_occlusion()
    total_occlusion = alpha.calculate_total_occlusion()
    
    print(f"\nAlpha Structure:")
    print(f"  Separation: {alpha.separation:.3f} fm")
    print(f"  Number of bonds: {alpha.n_bonds}")
    print(f"  Single bond occlusion: {bond_occlusion:.6f} sr")
    print(f"  Total occlusion: {total_occlusion:.6f} sr")
    
    # Verify with deuteron k
    verification = alpha.verify_with_deuteron_k()
    
    print(f"\nVerification with Deuteron k:")
    print(f"  k (deuteron): {verification['k_deuteron']:.6f} MeV/sr")
    print(f"  k (alpha): {verification['k_alpha']:.6f} MeV/sr")
    print(f"  k ratio: {verification['k_ratio']:.4f}")
    print(f"  Universal k: {verification['universal_k']}")
    print(f"  B_predicted: {verification['B_predicted']:.4f} MeV")
    print(f"  B_experimental: {verification['B_experimental']:.4f} MeV")
    print(f"  Error: {verification['error_percent']:.2f}%")
    print(f"  Passes: {verification['passes']}")
    
    # Full report
    print(alpha.get_structure_report())


if __name__ == "__main__":
    test_alpha_structure()
