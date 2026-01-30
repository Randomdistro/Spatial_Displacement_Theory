#!/usr/bin/env python3
"""
Phase 2.7: Fit Quality Analysis

Comprehensive analysis of fit quality:
- Error metrics (RMS, mean error, max error)
- Correlation (R²)
- Chi-squared
- Outlier identification
- Systematic trends

This validates the binding energy model.
"""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
import math

# ============================================================================
# FIT QUALITY METRICS
# ============================================================================

@dataclass
class FitQualityMetrics:
    """
    Comprehensive fit quality metrics.
    """
    n_points: int
    
    # Error metrics
    mean_error: float  # Mean absolute error
    rms_error: float  # Root mean square error
    max_error: float  # Maximum absolute error
    mean_error_percent: float  # Mean percentage error
    
    # Correlation
    r_squared: float  # R² correlation coefficient
    
    # Chi-squared
    chi_squared: float
    reduced_chi_squared: float  # chi² / (n - dof)
    
    # Outliers
    n_outliers: int  # Number of outliers (|z-score| > 2.0)
    
    def __init__(self):
        self.n_points = 0
        self.mean_error = 0.0
        self.rms_error = 0.0
        self.max_error = 0.0
        self.mean_error_percent = 0.0
        self.r_squared = 0.0
        self.chi_squared = 0.0
        self.reduced_chi_squared = 0.0
        self.n_outliers = 0


@dataclass
class BindingEnergyFit:
    """
    Represents a binding energy fit result.
    """
    nucleus_name: str
    Z: int
    N: int
    B_predicted: float  # MeV
    B_experimental: float  # MeV
    error: float  # |B_pred - B_exp|
    error_percent: float  # error / B_exp * 100
    z_score: float  # Standardized error


class FitQualityAnalyzer:
    """
    Analyzes fit quality for binding energy predictions.
    """
    
    def __init__(self):
        self.fits: List[BindingEnergyFit] = []
        self.metrics: FitQualityMetrics = FitQualityMetrics()
    
    def add_fit(self, name: str, Z: int, N: int, B_pred: float, B_exp: float):
        """Add a fit result"""
        error = abs(B_pred - B_exp)
        error_pct = (error / B_exp * 100.0) if B_exp > 0 else 0.0
        
        fit = BindingEnergyFit(
            nucleus_name=name,
            Z=Z,
            N=N,
            B_predicted=B_pred,
            B_experimental=B_exp,
            error=error,
            error_percent=error_pct,
            z_score=0.0
        )
        self.fits.append(fit)
    
    def calculate_metrics(self) -> FitQualityMetrics:
        """
        Calculate all fit quality metrics.
        
        Returns:
        --------
        FitQualityMetrics
            Calculated metrics
        """
        if len(self.fits) == 0:
            return self.metrics
        
        self.metrics.n_points = len(self.fits)
        
        # Error metrics
        errors = [fit.error for fit in self.fits]
        errors_pct = [fit.error_percent for fit in self.fits]
        
        self.metrics.mean_error = np.mean(errors)
        self.metrics.rms_error = np.sqrt(np.mean([e*e for e in errors]))
        self.metrics.max_error = np.max(errors)
        self.metrics.mean_error_percent = np.mean(errors_pct)
        
        # Correlation (R²)
        B_pred = np.array([fit.B_predicted for fit in self.fits])
        B_exp = np.array([fit.B_experimental for fit in self.fits])
        
        ss_res = np.sum((B_exp - B_pred)**2)
        ss_tot = np.sum((B_exp - np.mean(B_exp))**2)
        
        if ss_tot > 0:
            self.metrics.r_squared = 1.0 - (ss_res / ss_tot)
        else:
            self.metrics.r_squared = 0.0
        
        # Chi-squared
        # Assuming experimental uncertainty ~1% of value
        uncertainties = B_exp * 0.01
        chi_sq = np.sum(((B_exp - B_pred) / uncertainties)**2)
        self.metrics.chi_squared = chi_sq
        self.metrics.reduced_chi_squared = chi_sq / max(1, len(self.fits) - 1)
        
        # Calculate z-scores and identify outliers
        if self.metrics.rms_error > 0:
            for fit in self.fits:
                fit.z_score = fit.error / self.metrics.rms_error
                if abs(fit.z_score) > 2.0:
                    self.metrics.n_outliers += 1
        
        return self.metrics
    
    def get_quality_report(self) -> str:
        """
        Get comprehensive quality report.
        
        Returns:
        --------
        str
            Quality report
        """
        if self.metrics.n_points == 0:
            self.calculate_metrics()
        
        report = f"""
Fit Quality Analysis Report
============================

Number of Nuclei: {self.metrics.n_points}

ERROR METRICS
-------------
  Mean absolute error: {self.metrics.mean_error:.4f} MeV
  RMS error: {self.metrics.rms_error:.4f} MeV
  Maximum error: {self.metrics.max_error:.4f} MeV
  Mean percentage error: {self.metrics.mean_error_percent:.2f}%

CORRELATION
-----------
  R² (coefficient of determination): {self.metrics.r_squared:.6f}
  
  Interpretation:
    R² = 1.0: Perfect fit
    R² > 0.99: Excellent fit
    R² > 0.95: Good fit
    R² > 0.90: Acceptable fit
    R² < 0.90: Poor fit

CHI-SQUARED
-----------
  Chi-squared: {self.metrics.chi_squared:.2f}
  Reduced chi-squared: {self.metrics.reduced_chi_squared:.4f}
  
  Interpretation:
    Reduced chi² ≈ 1.0: Good fit
    Reduced chi² < 1.0: Over-fitting or overestimated uncertainties
    Reduced chi² > 1.0: Under-fitting or underestimated uncertainties

OUTLIERS
--------
  Number of outliers (|z-score| > 2.0): {self.metrics.n_outliers}
  Outlier percentage: {self.metrics.n_outliers / self.metrics.n_points * 100.0:.1f}%

OVERALL ASSESSMENT
------------------
"""
        
        # Overall assessment
        if self.metrics.r_squared > 0.99 and self.metrics.mean_error_percent < 1.0:
            assessment = "EXCELLENT - Model fits data very well"
        elif self.metrics.r_squared > 0.95 and self.metrics.mean_error_percent < 5.0:
            assessment = "GOOD - Model fits data well"
        elif self.metrics.r_squared > 0.90 and self.metrics.mean_error_percent < 10.0:
            assessment = "ACCEPTABLE - Model fits data reasonably well"
        else:
            assessment = "POOR - Model needs improvement"
        
        report += f"  {assessment}\n"
        
        if self.metrics.n_outliers > 0:
            report += f"\n  Note: {self.metrics.n_outliers} outliers identified - investigate for corrections\n"
        
        return report
    
    def get_outliers(self) -> List[BindingEnergyFit]:
        """Get list of outliers"""
        return [fit for fit in self.fits if abs(fit.z_score) > 2.0]
    
    def get_worst_fits(self, n: int = 5) -> List[BindingEnergyFit]:
        """Get n worst fits (by error percentage)"""
        sorted_fits = sorted(self.fits, key=lambda f: f.error_percent, reverse=True)
        return sorted_fits[:n]


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_fit_quality_analysis():
    """Test fit quality analysis"""
    print("="*80)
    print("TEST: Fit Quality Analysis")
    print("="*80)
    
    analyzer = FitQualityAnalyzer()
    
    # Add some test fits (with realistic errors)
    analyzer.add_fit("H2", 1, 1, 2.2246, 2.2246)  # Perfect
    analyzer.add_fit("He4", 2, 2, 28.5, 28.296)  # Small error
    analyzer.add_fit("C12", 6, 6, 92.0, 92.162)  # Small error
    analyzer.add_fit("O16", 8, 8, 128.0, 127.619)  # Small error
    analyzer.add_fit("Test1", 10, 10, 150.0, 160.0)  # Larger error
    analyzer.add_fit("Test2", 20, 20, 300.0, 350.0)  # Outlier
    
    # Calculate metrics
    metrics = analyzer.calculate_metrics()
    
    # Print report
    print(analyzer.get_quality_report())
    
    # Show outliers
    outliers = analyzer.get_outliers()
    if outliers:
        print("\nOutliers:")
        for fit in outliers:
            print(f"  {fit.nucleus_name}: error={fit.error:.4f} MeV ({fit.error_percent:.2f}%), z={fit.z_score:.2f}")
    
    # Show worst fits
    worst = analyzer.get_worst_fits(3)
    print("\nWorst Fits:")
    for fit in worst:
        print(f"  {fit.nucleus_name}: error={fit.error:.4f} MeV ({fit.error_percent:.2f}%)")


if __name__ == "__main__":
    test_fit_quality_analysis()
