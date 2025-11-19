"""
Validation and Comparison

Compare SDT predictions against NIST data.
"""

import numpy as np
from typing import Dict, List, Optional
from . import calculator
from . import elements
from .constants import *


def compare_energy_levels(element: str, n: int, l: int = 0, j: float = 0.5,
                         experimental: Optional[float] = None) -> Dict:
    """
    Compare SDT energy level with experimental value.
    
    Parameters:
    -----------
    element : str
        Element symbol
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
    j : float
        Total angular momentum
    experimental : float, optional
        Experimental energy level (eV). If None, attempts to look up.
    
    Returns:
    --------
    comparison : dict
        Dictionary with:
        - 'SDT': SDT prediction (eV)
        - 'experimental': experimental value (eV)
        - 'error': absolute error (eV)
        - 'error_pct': relative error (%)
        - 'within_tolerance': bool
    """
    calc = calculator.AtomicCalculator(element)
    
    # Calculate SDT prediction
    E_sdt = calc.energy_level(n, l, j)
    
    # Get experimental value if not provided
    if experimental is None:
        # Attempt to look up from known values
        if element == 'H' and n == 1:
            experimental = -13.59843449  # eV, CODATA 2018
        elif element == 'H' and n == 2:
            experimental = -3.399699  # eV
        else:
            experimental = None
    
    if experimental is None:
        return {
            'SDT': E_sdt,
            'experimental': None,
            'error': None,
            'error_pct': None,
            'within_tolerance': None
        }
    
    # Calculate error
    error = abs(E_sdt - experimental)
    error_pct = abs(error / experimental) * 100
    
    # Check tolerance (0.8% for hydrogen, 5% for others)
    if element == 'H':
        tolerance = 0.8
    else:
        tolerance = 5.0
    
    within_tolerance = error_pct < tolerance
    
    return {
        'SDT': E_sdt,
        'experimental': experimental,
        'error': error,
        'error_pct': error_pct,
        'within_tolerance': within_tolerance,
        'tolerance': tolerance
    }


def compare_ionization_energies(element: str, ionization_state: int = 1) -> Dict:
    """
    Compare SDT ionization energy with experimental value.
    
    Parameters:
    -----------
    element : str
        Element symbol
    ionization_state : int
        Ionization state (1 = first ionization, etc.)
    
    Returns:
    --------
    comparison : dict
        Dictionary with comparison results
    """
    calc = calculator.AtomicCalculator(element)
    
    # Calculate SDT prediction
    IE_sdt = calc.ionization(ionization_state)
    
    # Get experimental value
    try:
        IEs_exp = elements.get_ionization_energies(element)
        if ionization_state <= len(IEs_exp):
            IE_exp = IEs_exp[ionization_state - 1]
        else:
            IE_exp = None
    except (ValueError, IndexError):
        IE_exp = None
    
    if IE_exp is None:
        return {
            'SDT': IE_sdt,
            'experimental': None,
            'error': None,
            'error_pct': None,
            'within_tolerance': None
        }
    
    # Calculate error
    error = abs(IE_sdt - IE_exp)
    error_pct = abs(error / IE_exp) * 100
    
    # Check tolerance (0.8% for hydrogen, 5% for others)
    if element == 'H':
        tolerance = 0.8
    else:
        tolerance = 5.0
    
    within_tolerance = error_pct < tolerance
    
    return {
        'SDT': IE_sdt,
        'experimental': IE_exp,
        'error': error,
        'error_pct': error_pct,
        'within_tolerance': within_tolerance,
        'tolerance': tolerance
    }


def validate_hydrogen_spectrum(max_n: int = 10) -> Dict:
    """
    Validate hydrogen spectrum against NIST data.
    
    Parameters:
    -----------
    max_n : int
        Maximum principal quantum number
    
    Returns:
    --------
    results : dict
        Dictionary with validation results
    """
    calc = calculator.AtomicCalculator('H')
    
    # Known hydrogen spectral lines (wavelengths in nm, from NIST)
    known_lines = {
        (1, 0, 0.5, 2, 0, 0.5): 121.567,  # Lyman α
        (1, 0, 0.5, 3, 0, 0.5): 102.572,  # Lyman β
        (1, 0, 0.5, 4, 0, 0.5): 97.254,   # Lyman γ
        (2, 0, 0.5, 3, 1, 1.5): 656.279,  # Balmer α
        (2, 0, 0.5, 4, 1, 1.5): 486.135,  # Balmer β
        (2, 0, 0.5, 5, 1, 1.5): 434.047,  # Balmer γ
    }
    
    results = []
    errors = []
    
    for (n_i, l_i, j_i, n_f, l_f, j_f), lambda_exp in known_lines.items():
        trans = calc.transition((n_i, l_i, j_i), (n_f, l_f, j_f))
        lambda_sdt = trans['wavelength']
        
        error_nm = abs(lambda_sdt - lambda_exp)
        error_pct = abs(error_nm / lambda_exp) * 100
        
        results.append({
            'transition': f"{n_i}{_l_to_letter(l_i)} → {n_f}{_l_to_letter(l_f)}",
            'lambda_SDT': lambda_sdt,
            'lambda_exp': lambda_exp,
            'error_nm': error_nm,
            'error_pct': error_pct,
            'within_tolerance': error_pct < 0.8
        })
        
        errors.append(error_pct)
    
    avg_error = np.mean(errors)
    max_error = np.max(errors)
    
    return {
        'results': results,
        'avg_error_pct': avg_error,
        'max_error_pct': max_error,
        'all_within_tolerance': all(r['within_tolerance'] for r in results)
    }


def _l_to_letter(l: int) -> str:
    """Convert angular momentum quantum number to letter."""
    letters = ['s', 'p', 'd', 'f', 'g', 'h', 'i', 'k']
    if l < len(letters):
        return letters[l]
    return chr(ord('l') + l - 4)


def generate_validation_report(elements: List[str] = ['H', 'He', 'Li']) -> str:
    """
    Generate validation report comparing SDT predictions with experimental data.
    
    Parameters:
    -----------
    elements : List[str]
        List of elements to validate
    
    Returns:
    --------
    report : str
        Validation report as formatted string
    """
    report = "=" * 80 + "\n"
    report += "SDT ATOMIC CALCULATOR VALIDATION REPORT\n"
    report += "=" * 80 + "\n\n"
    
    for element in elements:
        report += f"\nElement: {element}\n"
        report += "-" * 80 + "\n"
        
        # Energy levels
        calc = calculator.AtomicCalculator(element)
        for n in [1, 2, 3, 4]:
            try:
                E_sdt = calc.energy_level(n, 0, 0.5)
                comp = compare_energy_levels(element, n, 0, 0.5)
                
                if comp['experimental'] is not None:
                    report += f"  n={n}: E_SDT={E_sdt:.6f} eV, "
                    report += f"E_exp={comp['experimental']:.6f} eV, "
                    report += f"error={comp['error_pct']:.4f}%\n"
            except Exception as e:
                report += f"  n={n}: Error - {e}\n"
        
        # Ionization energies
        try:
            all_IEs = calc.all_ionizations()
            IEs_exp = elements.get_ionization_energies(element) if hasattr(elements, 'get_ionization_energies') else None
            
            report += "\n  Ionization Energies:\n"
            for i, ie_data in enumerate(all_IEs[:min(5, len(all_IEs))], 1):
                IE_sdt = ie_data['IE']
                if IEs_exp and i <= len(IEs_exp):
                    IE_exp = IEs_exp[i-1]
                    error_pct = abs(IE_sdt - IE_exp) / IE_exp * 100
                    report += f"    IE({i}): {IE_sdt:.4f} eV (exp: {IE_exp:.4f} eV, error: {error_pct:.4f}%)\n"
                else:
                    report += f"    IE({i}): {IE_sdt:.4f} eV\n"
        except Exception as e:
            report += f"  Ionization energies: Error - {e}\n"
    
    report += "\n" + "=" * 80 + "\n"
    
    return report

