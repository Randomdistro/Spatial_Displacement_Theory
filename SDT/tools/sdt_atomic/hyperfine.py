"""
Hyperfine Structure

Hyperfine splitting from magnetic moment overlap.
From Phase 5 and Phase 8.
"""

import numpy as np
from typing import Optional
from .constants import *


def calculate_hyperfine_splitting(n: int, Z: int = 1, isotope: str = None) -> float:
    """
    Calculate hyperfine splitting.
    
    From Phase 8: ΔE_hf = (8/3) β_geom g_I g_e (m_e/m_p) Z³ α⁴ m_e c² / n³
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    Z : int
        Atomic number (default: 1 for hydrogen)
    isotope : str, optional
        Isotope identifier (e.g., '1H', '2H', '3He'). If None, uses hydrogen-1.
    
    Returns:
    --------
    delta_E_hf : float
        Hyperfine splitting (eV)
    """
    # Get nuclear g-factor
    g_I = get_nuclear_g_factor(isotope, Z)
    
    # Base hyperfine formula
    # ΔE_hf = (8/3) β_geom g_I g_e (m_e/m_p) Z³ α⁴ m_e c² / n³
    m_e_c2_eV = M_E * C**2 / E_CHARGE
    alpha4 = ALPHA**4
    
    delta_E_hf = (8.0/3.0) * BETA_GEOM * g_I * G_E * (M_E/M_P) * Z**3 * alpha4 * m_e_c2_eV / (n**3)
    
    return delta_E_hf


def get_nuclear_g_factor(isotope: Optional[str], Z: int) -> float:
    """
    Get nuclear g-factor for isotope.
    
    Parameters:
    -----------
    isotope : str, optional
        Isotope identifier (e.g., '1H', '2H', '3He')
    Z : int
        Atomic number
    
    Returns:
    --------
    g_I : float
        Nuclear g-factor (dimensionless)
    """
    # Nuclear g-factors from CODATA 2018
    if isotope is None:
        isotope = '1H'
    
    isotope = isotope.strip().upper()
    
    # Common isotopes
    g_factors = {
        '1H': G_P,        # Proton g-factor
        '2H': 0.8574382311,  # Deuteron g-factor
        '3HE': -4.255250615,  # Helium-3
        '4HE': 0.0,       # Helium-4 (spin-0, no hyperfine)
        '6LI': 0.822047,  # Lithium-6
        '7LI': 2.170951,  # Lithium-7
        '23NA': 1.478,    # Sodium-23
        '39K': 0.2609778, # Potassium-39
        '85RB': 0.54121,  # Rubidium-85
        '87RB': 1.83427,  # Rubidium-87
        '133CS': 0.73783, # Cesium-133
    }
    
    if isotope in g_factors:
        return g_factors[isotope]
    
    # Default: use proton g-factor for odd-Z, 0 for even-Z
    if Z % 2 == 0:
        return 0.0  # Even-Z nuclei often have spin-0
    else:
        return G_P  # Approximate with proton g-factor


def get_nuclear_moment(isotope: Optional[str], Z: int) -> float:
    """
    Get nuclear magnetic moment in units of nuclear magneton.
    
    Parameters:
    -----------
    isotope : str, optional
        Isotope identifier
    Z : int
        Atomic number
    
    Returns:
    --------
    mu_N : float
        Nuclear magnetic moment (in units of μ_N)
    """
    g_I = get_nuclear_g_factor(isotope, Z)
    
    # Nuclear magnetic moment: μ = g_I I μ_N
    # For hydrogen-1 (proton), I = 1/2
    # This is a simplified version - full calculation needs spin I
    return g_I * 0.5  # Approximate with I = 1/2


def hydrogen_hyperfine_splitting() -> float:
    """
    Calculate hydrogen 1S hyperfine splitting (21 cm line).
    
    This is the famous 21 cm line used in radio astronomy.
    
    Returns:
    --------
    delta_E_hf : float
        Hyperfine splitting (eV)
    """
    return calculate_hyperfine_splitting(n=1, Z=1, isotope='1H')

