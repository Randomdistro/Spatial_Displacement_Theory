"""
Energy Level Calculator

Combines base energy with all corrections:
- Base hydrogenic energy
- Fine structure
- Hyperfine structure
- Lamb shift
From Phase 2, 3, 4, 5, 8, 27A.
"""

import numpy as np
from typing import Optional, List, Tuple
from . import hydrogenic
from . import fine_structure
from . import hyperfine
from . import lamb_shift
from . import screening
from .constants import *


def calculate_total_energy(n: int, l: int, j: float, F: Optional[float] = None,
                          Z: int = 1, electron_config: Optional[List[Tuple[int, int]]] = None,
                          isotope: Optional[str] = None,
                          include_fine: bool = True,
                          include_hf: bool = True,
                          include_lamb: bool = True,
                          use_reduced_mass: bool = True) -> float:
    """
    Calculate total energy level with all corrections.
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
    j : float
        Total angular momentum (j = l ± 1/2)
    F : float, optional
        Total angular momentum including nuclear spin (for hyperfine)
    Z : int
        Atomic number (default: 1 for hydrogen)
    electron_config : List[Tuple[int, int]], optional
        Electron configuration [(n, l), ...] for multi-electron atoms
    isotope : str, optional
        Isotope identifier (for hyperfine)
    include_fine : bool
        Include fine structure correction (default: True)
    include_hf : bool
        Include hyperfine structure correction (default: True)
    include_lamb : bool
        Include Lamb shift correction (default: True, only for S-states)
    use_reduced_mass : bool
        Use reduced mass correction (default: True, only for hydrogen)
    
    Returns:
    --------
    E_total : float
        Total energy level (eV)
    """
    # Base hydrogenic energy
    if electron_config is None or len(electron_config) == 1:
        # Single-electron (hydrogenic) atom
        E_base = hydrogenic.calculate_energy_level(n, Z, use_reduced_mass)
    else:
        # Multi-electron atom: use screening
        try:
            Z_eff = screening.calculate_screening_factor(Z, n, l, electron_config)
            E_base = hydrogenic.calculate_energy_level(n, int(Z_eff), use_reduced_mass)
        except ValueError:
            # If electron not in config, use hydrogenic approximation
            E_base = hydrogenic.calculate_energy_level(n, Z, use_reduced_mass)
        # Note: This is an approximation - full calculation would iterate
    
    E_total = E_base
    
    # Fine structure correction
    if include_fine:
        delta_E_fs = fine_structure.calculate_fine_structure(n, l, j, Z)
        E_total += delta_E_fs
    
    # Lamb shift (only for S-states)
    if include_lamb and l == 0:
        state_type = f"{n}S"
        delta_E_Lamb = lamb_shift.calculate_lamb_shift(n, Z, state_type)
        E_total += delta_E_Lamb
    
    # Hyperfine structure (requires F)
    if include_hf and F is not None:
        delta_E_hf = hyperfine.calculate_hyperfine_splitting(n, Z, isotope)
        # Hyperfine splitting depends on F - this is simplified
        # Full calculation would give energy levels for each F value
        # For now, add half the splitting as approximation
        E_total += delta_E_hf / 2.0
    
    return E_total


def calculate_energy_with_corrections(n: int, l: int, j: float, Z: int = 1,
                                     corrections: Optional[dict] = None) -> dict:
    """
    Calculate energy level with breakdown of all corrections.
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
    j : float
        Total angular momentum
    Z : int
        Atomic number
    corrections : dict, optional
        Dictionary of correction flags. If None, uses defaults.
    
    Returns:
    --------
    energy_breakdown : dict
        Dictionary with:
        - 'base': Base hydrogenic energy
        - 'fine_structure': Fine structure correction
        - 'lamb_shift': Lamb shift (if S-state)
        - 'total': Total energy
    """
    if corrections is None:
        corrections = {
            'fine': True,
            'lamb': True,
            'hf': False  # Hyperfine requires F
        }
    
    # Base energy
    E_base = hydrogenic.calculate_energy_level(n, Z)
    
    result = {
        'base': E_base,
        'fine_structure': 0.0,
        'lamb_shift': 0.0,
        'hyperfine': 0.0,
        'total': E_base
    }
    
    # Fine structure
    if corrections.get('fine', True):
        delta_E_fs = fine_structure.calculate_fine_structure(n, l, j, Z)
        result['fine_structure'] = delta_E_fs
        result['total'] += delta_E_fs
    
    # Lamb shift (only for S-states)
    if corrections.get('lamb', True) and l == 0:
        state_type = f"{n}S"
        delta_E_Lamb = lamb_shift.calculate_lamb_shift(n, Z, state_type)
        result['lamb_shift'] = delta_E_Lamb
        result['total'] += delta_E_Lamb
    
    # Hyperfine (simplified)
    if corrections.get('hf', False):
        delta_E_hf = hyperfine.calculate_hyperfine_splitting(n, Z)
        result['hyperfine'] = delta_E_hf / 2.0  # Approximation
        result['total'] += result['hyperfine']
    
    return result

