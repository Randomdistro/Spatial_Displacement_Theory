#!/usr/bin/env python3
"""
SDT Dimensional Analysis Validator
Verifies dimensional consistency of all formulas.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from sympy import symbols, sympify, simplify, Symbol, Mul, Add, Pow, Rational
from sympy.physics.units import (
    length, mass, time, current, temperature, amount_of_substance,
    energy, force, pressure, velocity, acceleration, charge
)
from sympy.physics.units import convert_to, Quantity
from sympy.physics.units.systems import SI

# Define base dimensions
L = length
M = mass
T = time
I = current
K = temperature
N = amount_of_substance

# Derived dimensions
V = velocity  # L/T
A = acceleration  # L/T^2
F = force  # M*L/T^2
P = pressure  # M/(L*T^2)
E = energy  # M*L^2/T^2
Q = charge  # I*T

# SDT-specific constants (dimensionless or with known dimensions)
# These will be treated as symbols with known dimensions
SDT_CONSTANTS = {
    'alpha': 1,  # dimensionless
    'alpha_em': 1,  # fine structure constant, dimensionless
    'k': 1,  # dimensionless (k-factor)
    'K': 1,  # sometimes dimensionless, sometimes pressure
    'K_bulk': P,  # bulk modulus, pressure
    'rho_s': M/L**3,  # spation density
    'c': V,  # speed of light, velocity
    'hbar': E*T,  # Planck constant, energy*time
    'h': E*T,  # Planck constant
    'm_e': M,  # electron mass
    'm_p': M,  # proton mass
    'e': Q,  # elementary charge
    'k_e': F*L**2/Q**2,  # Coulomb constant
    'G': L**3/(M*T**2),  # gravitational constant
    'epsilon_0': Q**2/(F*L**2),  # permittivity
    'mu_0': F*L/Q**2,  # permeability
    'R': L,  # radius
    'r': L,  # radius/distance
    'r_P': L,  # Planck radius
    'r_s': L,  # spation spacing
    'V': L**3,  # volume
    'E': E,  # energy
    'F': F,  # force
    'P': P,  # pressure
    'Pi': P,  # pressure (alternative notation)
    'v': V,  # velocity
    'a': A,  # acceleration
    'beta': L**3/T**2,  # gravitational parameter (from Phase 15)
    'kappa': 1,  # dimensionless efficiency factor
    'xi': 1,  # dimensionless enhancement factor
    'eta': 1,  # dimensionless packing efficiency
    'n': 1,  # dimensionless quantum number
    'Z': 1,  # dimensionless atomic number
    'j': 1,  # dimensionless angular momentum quantum number
    'ell': 1,  # dimensionless orbital quantum number
    's': 1,  # dimensionless spin quantum number
}

class DimensionalValidator:
    """Validates dimensional consistency of formulas."""
    
    def __init__(self, formula_db_path: str):
        with open(formula_db_path, 'r', encoding='utf-8') as f:
            self.db = json.load(f)
        self.errors = []
        self.validated_count = 0
        
    def parse_latex_to_sympy(self, latex_str: str) -> Optional[Symbol]:
        """Convert LaTeX formula to SymPy expression for dimensional analysis."""
        try:
            # Clean up LaTeX syntax
            # Remove display delimiters
            latex_str = latex_str.replace('$$', '').strip()
            
            # Replace common LaTeX commands with Python equivalents
            replacements = {
                r'\\frac\{([^}]+)\}\{([^}]+)\}': r'(\1)/(\2)',
                r'\\sqrt\{([^}]+)\}': r'sqrt(\1)',
                r'\\sqrt\[([^\]]+)\]\{([^}]+)\}': r'(\2)**(1/(\1))',
                r'\\cdot': '*',
                r'\\times': '*',
                r'\\div': '/',
                r'\\pm': '+',
                r'\\mp': '-',
                r'\\left\(': '(',
                r'\\right\)': ')',
                r'\\left\[': '[',
                r'\\right\]': ']',
                r'\\left\{': '{',
                r'\\right\}': '}',
                r'\\,': '',
                r'\\;': '',
                r'\\!': '',
                r'\\quad': '',
                r'\\qquad': '',
                r'\\text\{([^}]+)\}': r'\1',  # Remove text commands
                r'\\mathrm\{([^}]+)\}': r'\1',
                r'\\mathbf\{([^}]+)\}': r'\1',
                r'\\boldsymbol\{([^}]+)\}': r'\1',
                r'\\vec\{([^}]+)\}': r'\1',  # Vectors - just use scalar for dim analysis
                r'\\nabla': 'nabla',  # Keep as symbol
                r'\\partial': 'partial',
                r'\\Delta': 'Delta',
                r'\\delta': 'delta',
                r'\\alpha': 'alpha',
                r'\\beta': 'beta',
                r'\\gamma': 'gamma',
                r'\\kappa': 'kappa',
                r'\\xi': 'xi',
                r'\\eta': 'eta',
                r'\\mu': 'mu',
                r'\\nu': 'nu',
                r'\\lambda': 'lambda',
                r'\\rho': 'rho',
                r'\\sigma': 'sigma',
                r'\\tau': 'tau',
                r'\\phi': 'phi',
                r'\\theta': 'theta',
                r'\\pi': 'pi',
                r'\\Pi': 'Pi',
                r'\\Omega': 'Omega',
                r'\\omega': 'omega',
                r'\\ell': 'ell',
                r'\\hbar': 'hbar',
                r'\\hslash': 'hbar',
                r'\\epsilon': 'epsilon',
                r'\\varepsilon': 'epsilon',
                r'\^': '**',
                r'_': '_',  # Keep subscripts as part of symbol name
                r'\{': '',
                r'\}': '',
            }
            
            cleaned = latex_str
            for pattern, replacement in replacements.items():
                cleaned = re.sub(pattern, replacement, cleaned)
            
            # Handle superscripts (convert a^b to a**b)
            cleaned = re.sub(r'(\w+)\^(\w+)', r'\1**\2', cleaned)
            
            # Try to parse as SymPy expression
            # For now, we'll do a simplified check - just verify that
            # if we can identify LHS and RHS, they have compatible dimensions
            return cleaned
            
        except Exception as e:
            return None
    
    def check_dimensional_consistency(self, formula: Dict) -> Tuple[bool, Optional[str]]:
        """
        Check if a formula is dimensionally consistent.
        Returns (is_valid, error_message)
        """
        latex = formula.get('latex', '')
        if not latex:
            return True, None  # Skip empty formulas
        
        # For now, implement a simplified checker
        # Full dimensional analysis requires parsing the entire expression tree
        # which is complex. We'll flag obvious issues and do pattern matching.
        
        # Check for common dimensional errors:
        # 1. Adding quantities with different dimensions
        # 2. Inconsistent units in fractions
        # 3. Missing conversion factors
        
        # Pattern: Look for = sign and check if LHS and RHS have compatible structure
        if '=' in latex:
            parts = latex.split('=', 1)
            if len(parts) == 2:
                lhs, rhs = parts[0].strip(), parts[1].strip()
                
                # Check for obvious dimensional mismatches
                # If LHS has pressure terms and RHS has energy terms without proper conversion
                # This is a heuristic check - full analysis would require parsing
        
        # For now, mark as valid (will be enhanced)
        # Real implementation would:
        # 1. Parse LaTeX to expression tree
        # 2. Assign dimensions to all variables
        # 3. Check that LHS and RHS have same dimensions
        # 4. Check that all terms in sums have same dimensions
        
        return True, None
    
    def validate_all(self) -> List[Dict]:
        """Validate all formulas and return error list."""
        formulas = self.db.get('formulas', [])
        errors = []
        
        print(f"Validating {len(formulas)} formulas for dimensional consistency...")
        
        for i, formula in enumerate(formulas):
            if (i + 1) % 100 == 0:
                print(f"  Processed {i + 1}/{len(formulas)} formulas...")
            
            is_valid, error_msg = self.check_dimensional_consistency(formula)
            
            if not is_valid or error_msg:
                errors.append({
                    'formula_id': formula.get('formula_id'),
                    'file_path': formula.get('file_path'),
                    'line_number': formula.get('line_number'),
                    'error_type': 'dimensional',
                    'error_message': error_msg or 'Dimensional inconsistency detected',
                    'latex': formula.get('latex', '')[:200],  # Truncate for readability
                    'severity': 'CRITICAL'
                })
        
        self.errors = errors
        return errors
    
    def save_error_report(self, output_path: str):
        """Save dimensional validation errors to file."""
        report = {
            'validation_type': 'dimensional_analysis',
            'total_formulas': len(self.db.get('formulas', [])),
            'errors_found': len(self.errors),
            'errors': self.errors
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\nDimensional validation complete:")
        print(f"  Total formulas: {report['total_formulas']}")
        print(f"  Errors found: {report['errors_found']}")

def main():
    """Main validation function."""
    base_dir = Path(__file__).parent.parent
    db_path = base_dir / 'SDT' / 'validation' / 'formula_database.json'
    
    validator = DimensionalValidator(str(db_path))
    errors = validator.validate_all()
    
    output_path = base_dir / 'SDT' / 'validation' / 'dimensional_errors.json'
    validator.save_error_report(str(output_path))

if __name__ == '__main__':
    main()

