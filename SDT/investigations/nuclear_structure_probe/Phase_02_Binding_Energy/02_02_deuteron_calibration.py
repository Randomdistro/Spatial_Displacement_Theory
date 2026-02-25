#!/usr/bin/env python3
"""
Phase 2.2: Deuteron Calibration

Calibrates the nuclear binding constant κ_B (MeV/sr) from the deuteron (simplest nucleus).
Symbol hygiene: κ_B is binding only; velocity uses v and κ_v ≡ v/c (SDT_COMPILER_SPEC_v0.9 §0).
Code uses variable name `k` for κ_B.

Key principle: Deuteron has a single p-n bond, so κ_B = B_exp / Omega.
This provides the fundamental calibration point for all other nuclei.
"""

import math
import importlib.util
from pathlib import Path

# Import occlusion calculator
_calc_path = Path(__file__).parent / "02_01_occlusion_binding_calculator.py"
spec = importlib.util.spec_from_file_location("calc", _calc_path)
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)

# ============================================================================
# CONSTANTS
# ============================================================================

# Deuteron experimental data
B_DEUTERON_EXP = 2.2246  # MeV (experimental binding energy)
DIST_DEUTERON_FM = 2.10  # fm (measured separation)
R_NUCLEON_FM = 0.84  # fm


# ============================================================================
# DEUTERON CALIBRATION
# ============================================================================

class DeuteronCalibration:
    """
    Calibrates binding constant κ_B (MeV/sr; variable `k`) from deuteron.
    
    Deuteron structure:
    - Single p-n bond
    - Separation: 2.10 fm
    - Binding: 2.2246 MeV
    
    This is the simplest possible nucleus, making it ideal for calibration.
    """
    
    def __init__(self):
        self.separation = DIST_DEUTERON_FM
        self.B_experimental = B_DEUTERON_EXP
        self.occlusion = 0.0
        self.k_calibrated = 0.0
    
    def calculate_occlusion(self) -> float:
        """
        Calculate solid angle occlusion for deuteron.
        
        Returns:
        --------
        float
            Occlusion (steradians)
        """
        self.occlusion = calc.spherical_occlusion(R_NUCLEON_FM, self.separation)
        return self.occlusion
    
    def calibrate_k(self) -> float:
        """
        Calibrate binding constant k from deuteron.
        
        k = B_exp / Omega
        
        Returns:
        --------
        float
            Calibrated binding constant k (MeV/sr)
        """
        if self.occlusion == 0.0:
            self.calculate_occlusion()
        
        if self.occlusion > 0:
            self.k_calibrated = self.B_experimental / self.occlusion
        else:
            self.k_calibrated = 0.0
        
        return self.k_calibrated
    
    def verify_calibration(self) -> dict:
        """
        Verify calibration by predicting deuteron binding.
        
        Returns:
        --------
        dict
            Verification results
        """
        if self.k_calibrated == 0.0:
            self.calibrate_k()
        
        B_predicted = self.k_calibrated * self.occlusion
        error = abs(B_predicted - self.B_experimental)
        error_percent = error / self.B_experimental * 100.0
        
        return {
            'k_calibrated': self.k_calibrated,
            'B_predicted': B_predicted,
            'B_experimental': self.B_experimental,
            'error': error,
            'error_percent': error_percent,
            'passes': error_percent < 0.01  # Should be exact (within numerical precision)
        }
    
    def get_calibration_report(self) -> str:
        """
        Get detailed calibration report.
        
        Returns:
        --------
        str
            Calibration report
        """
        if self.k_calibrated == 0.0:
            self.calibrate_k()
        
        verification = self.verify_calibration()
        
        report = f"""
Deuteron Calibration Report
===========================

Structure:
  - Single p-n bond
  - Separation: {self.separation:.3f} fm
  - Nucleon radius: {R_NUCLEON_FM:.3f} fm

Occlusion:
  - Solid angle occlusion: {self.occlusion:.6f} sr
  - Fraction of 4*pi: {self.occlusion / (4.0 * math.pi):.6f}

Experimental Data:
  - Binding energy: {self.B_experimental:.4f} MeV

Calibration:
  - k = B_exp / Omega = {self.k_calibrated:.6f} MeV/sr

Verification:
  - B_predicted: {verification['B_predicted']:.6f} MeV
  - B_experimental: {verification['B_experimental']:.6f} MeV
  - Error: {verification['error']:.6f} MeV ({verification['error_percent']:.4f}%)
  - Passes: {verification['passes']}

This k value will be used as the universal binding constant
(unless discovery analysis shows family-specific k values are needed).
"""
        return report


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_deuteron_calibration():
    """Test deuteron calibration"""
    print("="*80)
    print("TEST: Deuteron Calibration")
    print("="*80)
    
    calibration = DeuteronCalibration()
    
    # Calculate occlusion
    occlusion = calibration.calculate_occlusion()
    print(f"\nDeuteron Occlusion:")
    print(f"  Separation: {calibration.separation:.3f} fm")
    print(f"  Occlusion: {occlusion:.6f} sr")
    print(f"  Fraction of 4*pi: {occlusion / (4.0 * math.pi):.6f}")
    
    # Calibrate k
    k = calibration.calibrate_k()
    print(f"\nCalibration:")
    print(f"  B_experimental: {calibration.B_experimental:.4f} MeV")
    print(f"  k_calibrated: {k:.6f} MeV/sr")
    
    # Verify
    verification = calibration.verify_calibration()
    print(f"\nVerification:")
    print(f"  B_predicted: {verification['B_predicted']:.6f} MeV")
    print(f"  Error: {verification['error']:.6f} MeV ({verification['error_percent']:.4f}%)")
    print(f"  Passes: {verification['passes']}")
    
    # Full report
    print(calibration.get_calibration_report())


if __name__ == "__main__":
    test_deuteron_calibration()
