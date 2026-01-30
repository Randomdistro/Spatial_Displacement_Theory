#!/usr/bin/env python3
"""
Phase 2.6: Binding Energy Discovery

Implements the discovery-first methodology:
1. Measure k_i = B_exp / Omega_i for each nucleus
2. Analyze patterns: mean, stddev, CV, family splits
3. Test universality: CV < 5%?
4. Test family-specific: Different k per family?
5. Test corrections: Overlap, compression, pairing

This is the core discovery engine - we DISCOVER k, we don't assume it.
"""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
import importlib.util
from pathlib import Path

# Import modules
_calc_path = Path(__file__).parent / "02_01_occlusion_binding_calculator.py"
spec = importlib.util.spec_from_file_location("calc", _calc_path)
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)

# ============================================================================
# DISCOVERY DATA STRUCTURES
# ============================================================================

@dataclass
class NucleusDiscovery:
    """
    Discovery data for a single nucleus.
    
    Contains:
    - Geometric structure (occlusion)
    - Experimental binding energy
    - Inferred k_i = B_exp / Omega
    - Family classification
    """
    Z: int
    N: int
    A: int
    name: str
    family: str  # 'deuteron', 'alpha', 'alpha_cluster', 'odd_A', etc.
    
    total_occlusion: float  # steradians
    B_experimental: float  # MeV
    k_inferred: float  # MeV/sr
    
    def __init__(self, Z: int, N: int, name: str, family: str):
        self.Z = Z
        self.N = N
        self.A = Z + N
        self.name = name
        self.family = family
        self.total_occlusion = 0.0
        self.B_experimental = 0.0
        self.k_inferred = 0.0
    
    def infer_k(self) -> float:
        """Infer k from experimental data"""
        if self.total_occlusion > 0 and self.B_experimental > 0:
            self.k_inferred = self.B_experimental / self.total_occlusion
        else:
            self.k_inferred = 0.0
        return self.k_inferred


@dataclass
class DiscoveryAnalysis:
    """
    Analysis of k values across all nuclei.
    
    Tests:
    1. Universality: Is k constant across all nuclei?
    2. Family-specific: Are there different k per family?
    3. Corrections: Do we need corrections?
    """
    nuclei: List[NucleusDiscovery]
    
    # Universal k analysis
    k_mean: float
    k_std: float
    k_cv: float  # Coefficient of variation
    k_min: float
    k_max: float
    
    # Family-specific analysis
    family_stats: Dict[str, Dict[str, float]]  # {family: {mean, std, cv, n}}
    
    # Outliers
    outliers: List[NucleusDiscovery]  # Nuclei with |z-score| > 2.0
    
    def __init__(self, nuclei: List[NucleusDiscovery]):
        self.nuclei = nuclei
        self.k_mean = 0.0
        self.k_std = 0.0
        self.k_cv = 0.0
        self.k_min = 0.0
        self.k_max = 0.0
        self.family_stats = {}
        self.outliers = []
    
    def analyze_universality(self) -> Dict:
        """
        Analyze whether k is universal.
        
        Returns:
        --------
        dict
            Universality analysis results
        """
        # Get all k values
        k_values = [n.k_inferred for n in self.nuclei if n.k_inferred > 0]
        
        if len(k_values) == 0:
            return {'universal': False, 'reason': 'No k values'}
        
        self.k_mean = np.mean(k_values)
        self.k_std = np.std(k_values)
        self.k_cv = (self.k_std / self.k_mean * 100.0) if self.k_mean > 0 else 0.0
        self.k_min = np.min(k_values)
        self.k_max = np.max(k_values)
        
        # Test universality: CV < 5%?
        is_universal = self.k_cv < 5.0
        
        return {
            'universal': is_universal,
            'k_mean': self.k_mean,
            'k_std': self.k_std,
            'k_cv': self.k_cv,
            'k_min': self.k_min,
            'k_max': self.k_max,
            'n_nuclei': len(k_values),
            'criterion': 'CV < 5%',
            'passes': is_universal
        }
    
    def analyze_families(self) -> Dict:
        """
        Analyze k values by nuclear family.
        
        Returns:
        --------
        dict
            Family-specific analysis
        """
        # Group by family
        families = {}
        for nucleus in self.nuclei:
            if nucleus.k_inferred > 0:
                if nucleus.family not in families:
                    families[nucleus.family] = []
                families[nucleus.family].append(nucleus.k_inferred)
        
        # Calculate stats per family
        self.family_stats = {}
        for family, k_vals in families.items():
            if len(k_vals) > 0:
                mean = np.mean(k_vals)
                std = np.std(k_vals)
                cv = (std / mean * 100.0) if mean > 0 else 0.0
                
                self.family_stats[family] = {
                    'mean': mean,
                    'std': std,
                    'cv': cv,
                    'n': len(k_vals),
                    'min': np.min(k_vals),
                    'max': np.max(k_vals)
                }
        
        # Test if families have different k
        family_means = [stats['mean'] for stats in self.family_stats.values()]
        if len(family_means) > 1:
            family_std = np.std(family_means)
            family_cv = (family_std / np.mean(family_means) * 100.0) if np.mean(family_means) > 0 else 0.0
            families_different = family_cv > 5.0
        else:
            families_different = False
        
        return {
            'families_different': families_different,
            'family_stats': self.family_stats,
            'n_families': len(self.family_stats)
        }
    
    def identify_outliers(self) -> List[NucleusDiscovery]:
        """
        Identify outliers (|z-score| > 2.0).
        
        Returns:
        --------
        List[NucleusDiscovery]
            List of outliers
        """
        if self.k_mean == 0.0:
            self.analyze_universality()
        
        self.outliers = []
        for nucleus in self.nuclei:
            if nucleus.k_inferred > 0 and self.k_std > 0:
                z_score = abs((nucleus.k_inferred - self.k_mean) / self.k_std)
                if z_score > 2.0:
                    self.outliers.append(nucleus)
        
        return self.outliers
    
    def get_discovery_report(self) -> str:
        """
        Get comprehensive discovery report.
        
        Returns:
        --------
        str
            Discovery report
        """
        universality = self.analyze_universality()
        families = self.analyze_families()
        outliers = self.identify_outliers()
        
        report = f"""
Binding Energy Discovery Report
================================

Total Nuclei Analyzed: {len(self.nuclei)}
Nuclei with k values: {universality['n_nuclei']}

UNIVERSALITY TEST
----------------
  k_mean: {universality['k_mean']:.6f} MeV/sr
  k_std: {universality['k_std']:.6f} MeV/sr
  k_cv: {universality['k_cv']:.2f}%
  k_range: [{universality['k_min']:.6f}, {universality['k_max']:.6f}] MeV/sr
  
  Criterion: CV < 5%
  Result: {'UNIVERSAL' if universality['universal'] else 'NOT UNIVERSAL'}
  
  {'✓ k appears to be universal - can use single k for all nuclei' if universality['universal'] else '✗ k varies significantly - may need family-specific k or corrections'}

FAMILY-SPECIFIC ANALYSIS
-------------------------
  Number of families: {families['n_families']}
  Families have different k: {families['families_different']}
  
"""
        
        for family, stats in self.family_stats.items():
            report += f"  {family}:\n"
            report += f"    n = {stats['n']}\n"
            report += f"    k_mean = {stats['mean']:.6f} MeV/sr\n"
            report += f"    k_std = {stats['std']:.6f} MeV/sr\n"
            report += f"    k_cv = {stats['cv']:.2f}%\n"
            report += f"    k_range = [{stats['min']:.6f}, {stats['max']:.6f}] MeV/sr\n\n"
        
        report += f"""
OUTLIERS (|z-score| > 2.0)
---------------------------
  Number of outliers: {len(outliers)}
"""
        
        if outliers:
            for nucleus in outliers:
                z_score = abs((nucleus.k_inferred - self.k_mean) / self.k_std)
                report += f"  {nucleus.name} (Z={nucleus.Z}, N={nucleus.N}): "
                report += f"k={nucleus.k_inferred:.6f}, z={z_score:.2f}\n"
        else:
            report += "  No outliers found.\n"
        
        report += f"""
RECOMMENDATIONS
---------------
"""
        
        if universality['universal']:
            report += "  ✓ Use universal k = {:.6f} MeV/sr for all nuclei\n".format(universality['k_mean'])
        else:
            if families['families_different']:
                report += "  → Consider family-specific k values\n"
            if outliers:
                report += "  → Investigate outliers for corrections (overlap, compression, pairing)\n"
            report += "  → May need correction model: B = k*Omega_eff - corrections\n"
        
        return report


# ============================================================================
# DISCOVERY ENGINE
# ============================================================================

class BindingEnergyDiscovery:
    """
    Main discovery engine.
    
    Collects data from all nuclei and performs discovery analysis.
    """
    
    def __init__(self):
        self.nuclei_discoveries: List[NucleusDiscovery] = []
        self.analysis: Optional[DiscoveryAnalysis] = None
    
    def add_nucleus(self, nucleus: NucleusDiscovery):
        """Add a nucleus to discovery set"""
        nucleus.infer_k()
        self.nuclei_discoveries.append(nucleus)
    
    def analyze(self) -> DiscoveryAnalysis:
        """
        Perform discovery analysis.
        
        Returns:
        --------
        DiscoveryAnalysis
            Analysis results
        """
        self.analysis = DiscoveryAnalysis(self.nuclei_discoveries)
        return self.analysis
    
    def get_best_k(self) -> float:
        """
        Get best k value (universal or family-specific).
        
        Returns:
        --------
        float
            Best k value (MeV/sr)
        """
        if self.analysis is None:
            self.analyze()
        
        universality = self.analysis.analyze_universality()
        
        if universality['universal']:
            return universality['k_mean']
        else:
            # Use mean of all nuclei as fallback
            return universality['k_mean']


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_binding_energy_discovery():
    """Test binding energy discovery"""
    print("="*80)
    print("TEST: Binding Energy Discovery")
    print("="*80)
    
    discovery = BindingEnergyDiscovery()
    
    # Add some test nuclei
    # Deuteron
    deut = NucleusDiscovery(Z=1, N=1, name="H2", family="deuteron")
    deut.total_occlusion = 0.1692  # Approximate from test
    deut.B_experimental = 2.2246
    deut.infer_k()
    discovery.add_nucleus(deut)
    
    # Alpha
    alpha = NucleusDiscovery(Z=2, N=2, name="He4", family="alpha")
    alpha.total_occlusion = 1.0152  # Approximate from test
    alpha.B_experimental = 28.296
    alpha.infer_k()
    discovery.add_nucleus(alpha)
    
    # C-12
    c12 = NucleusDiscovery(Z=6, N=6, name="C12", family="alpha_cluster")
    c12.total_occlusion = 3.0456  # Approximate
    c12.B_experimental = 92.162
    c12.infer_k()
    discovery.add_nucleus(c12)
    
    # O-16
    o16 = NucleusDiscovery(Z=8, N=8, name="O16", family="alpha_cluster")
    o16.total_occlusion = 4.0608  # Approximate
    o16.B_experimental = 127.619
    o16.infer_k()
    discovery.add_nucleus(o16)
    
    # Analyze
    analysis = discovery.analyze()
    
    # Print report
    print(analysis.get_discovery_report())
    
    # Get best k
    best_k = discovery.get_best_k()
    print(f"\nBest k value: {best_k:.6f} MeV/sr")


if __name__ == "__main__":
    test_binding_energy_discovery()
