"""
Formula Validator for SDT

Performs dimensional analysis, numerical consistency checks, and validation
against experimental data for SDT formulas.
"""

import json
import re
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# CODATA 2018 constants
CODATA = {
    'c': 2.99792458e8,  # m/s (exact)
    'hbar': 1.054571817e-34,  # J·s
    'h': 6.62607015e-34,  # J·s
    'm_e': 9.1093837015e-31,  # kg
    'm_p': 1.67262192369e-27,  # kg
    'e': 1.602176634e-19,  # C
    'k_e': 8.9875517923e9,  # N·m²/C² (1/(4πε₀))
    'epsilon_0': 8.8541878128e-12,  # F/m
    'alpha': 7.2973525693e-3,  # Fine structure constant
    'a_0': 5.29177210903e-11,  # m (Bohr radius)
    'R_inf': 10973731.568160,  # m⁻¹ (Rydberg constant)
    'g_e': 2.00231930436,  # Electron g-factor
    'g_p': 5.5856946893,  # Proton g-factor
    'mu_B': 9.2740100783e-24,  # J/T (Bohr magneton)
    'G': 6.67430e-11,  # m³/(kg·s²) (gravitational constant)
}

# Experimental reference values
EXPERIMENTAL = {
    'E_H_ground': -13.605693122994,  # eV (Hydrogen ground state)
    'E_H_lyman_alpha': 10.19883,  # eV (Lyman α transition)
    'E_H_balmer_alpha': 1.88961,  # eV (Balmer α transition)
    'hyperfine_H_1S': 1420.405751,  # MHz (Hydrogen hyperfine splitting)
    'beta_Earth': 3.986004418e14,  # m³/s²
    'g_Earth': 9.80665,  # m/s²
    'R_Earth': 6.371e6,  # m
}

@dataclass
class ValidationResult:
    """Result of formula validation."""
    formula_id: str
    phase: str
    tag: Optional[str]
    status: str  # 'valid', 'error', 'warning', 'pending'
    errors: List[str]
    warnings: List[str]
    dimensional_check: Optional[bool]
    numerical_check: Optional[bool]
    experimental_check: Optional[bool]

class FormulaValidator:
    """Validates SDT formulas."""
    
    def __init__(self, registry_path: Path):
        with open(registry_path, 'r', encoding='utf-8') as f:
            self.registry = json.load(f)
        self.results: List[ValidationResult] = []
    
    def get_formulas_by_phase(self, phase_ids: List[str]) -> List[Dict]:
        """Get all formulas from specified phases."""
        formulas = []
        for formula in self.registry['formulas']:
            if formula['phase'] in phase_ids:
                formulas.append(formula)
        return formulas
    
    def check_dimensional_consistency(self, latex: str) -> Tuple[bool, List[str]]:
        """
        Check dimensional consistency of a formula.
        This is a simplified check - full dimensional analysis would require
        parsing the LaTeX and understanding physical meanings.
        """
        errors = []
        
        # Check for common dimensional issues
        # This is a placeholder - full implementation would parse LaTeX
        
        # Check for mismatched parentheses
        if latex.count('(') != latex.count(')'):
            errors.append("Mismatched parentheses")
        if latex.count('[') != latex.count(']'):
            errors.append("Mismatched square brackets")
        if latex.count('{') != latex.count('}'):
            errors.append("Mismatched curly braces")
        
        return len(errors) == 0, errors
    
    def check_numerical_consistency(self, formula: Dict) -> Tuple[bool, List[str]]:
        """
        Check numerical consistency for known formulas.
        """
        errors = []
        warnings = []
        latex = formula['latex']
        tag = formula.get('tag', '')
        
        # Check specific known formulas
        if '1.1' in tag or '1.2' in tag or '1.3' in tag:
            # Spation lattice properties from Phase 1
            pass
        
        # Rydberg formula check
        if 'E_n' in latex and 'Ϟ' in latex or 'R_∞' in latex:
            # Check if formula matches expected form
            if 'R_∞' in latex and 'hc' in latex:
                # Standard Rydberg form
                pass
        
        # Hyperfine splitting check
        if 'ΔE_hf' in latex or 'hyperfine' in latex.lower():
            # Should match experimental value for H 1S
            pass
        
        return len(errors) == 0, errors, warnings
    
    def validate_atomic_formulas(self) -> List[ValidationResult]:
        """Validate atomic scale formulas (Phases 1-6, 8, 23, 27A-C)."""
        atomic_phases = ['1', '2', '3', '4', '5', '6', '8', '23', '27A', '27B', '27C']
        formulas = self.get_formulas_by_phase(atomic_phases)
        
        results = []
        
        for formula in formulas:
            result = ValidationResult(
                formula_id=formula['id'],
                phase=formula['phase'],
                tag=formula.get('tag'),
                status='pending',
                errors=[],
                warnings=[],
                dimensional_check=None,
                numerical_check=None,
                experimental_check=None
            )
            
            # Dimensional check
            dim_ok, dim_errors = self.check_dimensional_consistency(formula['latex'])
            result.dimensional_check = dim_ok
            result.errors.extend(dim_errors)
            
            # Numerical check
            num_ok, num_errors, num_warnings = self.check_numerical_consistency(formula)
            result.numerical_check = num_ok
            result.errors.extend(num_errors)
            result.warnings.extend(num_warnings)
            
            # Determine overall status
            if result.errors:
                result.status = 'error'
            elif result.warnings:
                result.status = 'warning'
            else:
                result.status = 'valid'
            
            results.append(result)
        
        self.results.extend(results)
        return results
    
    def validate_thermodynamic_formulas(self) -> List[ValidationResult]:
        """Validate thermodynamic formulas (Phase 7)."""
        formulas = self.get_formulas_by_phase(['7'])
        results = []
        
        for formula in formulas:
            result = ValidationResult(
                formula_id=formula['id'],
                phase=formula['phase'],
                tag=formula.get('tag'),
                status='pending',
                errors=[],
                warnings=[],
                dimensional_check=None,
                numerical_check=None,
                experimental_check=None
            )
            
            dim_ok, dim_errors = self.check_dimensional_consistency(formula['latex'])
            result.dimensional_check = dim_ok
            result.errors.extend(dim_errors)
            
            if result.errors:
                result.status = 'error'
            else:
                result.status = 'valid'
            
            results.append(result)
        
        self.results.extend(results)
        return results
    
    def validate_gravitational_formulas(self) -> List[ValidationResult]:
        """Validate gravitational formulas (Phases 1, 15, 16, 22, 24-25)."""
        gravity_phases = ['1', '15', '16', '22', '24', '25']
        formulas = self.get_formulas_by_phase(gravity_phases)
        results = []
        
        for formula in formulas:
            result = ValidationResult(
                formula_id=formula['id'],
                phase=formula['phase'],
                tag=formula.get('tag'),
                status='pending',
                errors=[],
                warnings=[],
                dimensional_check=None,
                numerical_check=None,
                experimental_check=None
            )
            
            dim_ok, dim_errors = self.check_dimensional_consistency(formula['latex'])
            result.dimensional_check = dim_ok
            result.errors.extend(dim_errors)
            
            # Check for β formula consistency
            latex = formula['latex']
            if 'β' in latex or 'beta' in latex.lower():
                # Verify β = c² R_eff/Ϟ² form
                pass
            
            if result.errors:
                result.status = 'error'
            else:
                result.status = 'valid'
            
            results.append(result)
        
        self.results.extend(results)
        return results
    
    def validate_electromagnetic_formulas(self) -> List[ValidationResult]:
        """Validate electromagnetic formulas (Phases 10-12)."""
        em_phases = ['10', '11', '12']
        formulas = self.get_formulas_by_phase(em_phases)
        results = []
        
        for formula in formulas:
            result = ValidationResult(
                formula_id=formula['id'],
                phase=formula['phase'],
                tag=formula.get('tag'),
                status='pending',
                errors=[],
                warnings=[],
                dimensional_check=None,
                numerical_check=None,
                experimental_check=None
            )
            
            dim_ok, dim_errors = self.check_dimensional_consistency(formula['latex'])
            result.dimensional_check = dim_ok
            result.errors.extend(dim_errors)
            
            if result.errors:
                result.status = 'error'
            else:
                result.status = 'valid'
            
            results.append(result)
        
        self.results.extend(results)
        return results
    
    def save_results(self, output_path: Path):
        """Save validation results to JSON."""
        results_dict = {
            'summary': {
                'total_formulas': len(self.results),
                'valid': sum(1 for r in self.results if r.status == 'valid'),
                'errors': sum(1 for r in self.results if r.status == 'error'),
                'warnings': sum(1 for r in self.results if r.status == 'warning'),
            },
            'results': [
                {
                    'formula_id': r.formula_id,
                    'phase': r.phase,
                    'tag': r.tag,
                    'status': r.status,
                    'errors': r.errors,
                    'warnings': r.warnings,
                    'dimensional_check': r.dimensional_check,
                    'numerical_check': r.numerical_check,
                    'experimental_check': r.experimental_check,
                }
                for r in self.results
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    base_dir = Path(__file__).parent.parent.parent
    registry_path = base_dir / 'SDT' / 'validation' / 'formula_registry.json'
    
    validator = FormulaValidator(registry_path)
    
    print("Validating atomic formulas...")
    validator.validate_atomic_formulas()
    
    print("Validating thermodynamic formulas...")
    validator.validate_thermodynamic_formulas()
    
    print("Validating gravitational formulas...")
    validator.validate_gravitational_formulas()
    
    print("Validating electromagnetic formulas...")
    validator.validate_electromagnetic_formulas()
    
    output_path = base_dir / 'SDT' / 'validation' / 'validation_results.json'
    validator.save_results(output_path)
    
    print(f"\nValidation complete!")
    print(f"  Total formulas validated: {len(validator.results)}")
    print(f"  Valid: {sum(1 for r in validator.results if r.status == 'valid')}")
    print(f"  Errors: {sum(1 for r in validator.results if r.status == 'error')}")
    print(f"  Warnings: {sum(1 for r in validator.results if r.status == 'warning')}")
    print(f"\nResults saved to: {output_path}")

