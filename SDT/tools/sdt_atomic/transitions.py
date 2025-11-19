"""
Transition Calculator (ALL Excitations)

Calculate ALL possible transitions for atomic configurations.
From Phase 2 and Phase 27A.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional, Set
from . import energy_levels
from .constants import *


def calculate_transition_energy(n_i: int, l_i: int, j_i: float, n_f: int, l_f: int, j_f: float,
                                Z: int = 1, electron_config_i: Optional[List[Tuple[int, int]]] = None,
                                electron_config_f: Optional[List[Tuple[int, int]]] = None,
                                F_i: Optional[float] = None, F_f: Optional[float] = None,
                                isotope: Optional[str] = None) -> float:
    """
    Calculate transition energy between two states.
    
    Parameters:
    -----------
    n_i : int
        Initial principal quantum number
    l_i : int
        Initial angular momentum quantum number
    j_i : float
        Initial total angular momentum
    n_f : int
        Final principal quantum number
    l_f : int
        Final angular momentum quantum number
    j_f : float
        Final total angular momentum
    Z : int
        Atomic number
    electron_config_i : List[Tuple[int, int]], optional
        Initial electron configuration
    electron_config_f : List[Tuple[int, int]], optional
        Final electron configuration
    F_i : float, optional
        Initial total angular momentum (including nuclear spin)
    F_f : float, optional
        Final total angular momentum (including nuclear spin)
    isotope : str, optional
        Isotope identifier
    
    Returns:
    --------
    delta_E : float
        Transition energy (eV, positive for emission)
    """
    # Calculate energies
    E_i = energy_levels.calculate_total_energy(
        n_i, l_i, j_i, F_i, Z, electron_config_i, isotope
    )
    E_f = energy_levels.calculate_total_energy(
        n_f, l_f, j_f, F_f, Z, electron_config_f, isotope
    )
    
    # Transition energy (positive for emission: higher to lower)
    delta_E = abs(E_f - E_i)
    
    return delta_E


def calculate_wavelength(delta_E_eV: float) -> float:
    """
    Calculate wavelength from transition energy.
    
    Parameters:
    -----------
    delta_E_eV : float
        Transition energy (eV)
    
    Returns:
    --------
    wavelength : float
        Wavelength (nm)
    """
    if delta_E_eV <= 0:
        return np.nan
    
    return HC_EV_NM / delta_E_eV


def calculate_frequency(delta_E_eV: float) -> float:
    """
    Calculate frequency from transition energy.
    
    Parameters:
    -----------
    delta_E_eV : float
        Transition energy (eV)
    
    Returns:
    --------
    frequency : float
        Frequency (Hz)
    """
    if delta_E_eV <= 0:
        return np.nan
    
    # Convert eV to Joules and use E = hν
    delta_E_J = delta_E_eV * E_CHARGE
    frequency = delta_E_J / H
    
    return frequency


def is_allowed_transition(l_i: int, l_f: int, j_i: float, j_f: float) -> bool:
    """
    Check if transition is electric dipole allowed.
    
    Selection rules:
    - Δl = ±1
    - Δj = 0, ±1 (but not j=0 → j=0)
    
    Parameters:
    -----------
    l_i : int
        Initial angular momentum
    l_f : int
        Final angular momentum
    j_i : float
        Initial total angular momentum
    j_f : float
        Final total angular momentum
    
    Returns:
    --------
    allowed : bool
        True if transition is allowed
    """
    # Δl = ±1
    delta_l = abs(l_f - l_i)
    if delta_l != 1:
        return False
    
    # Δj = 0, ±1 (but not j=0 → j=0)
    delta_j = abs(j_f - j_i)
    if delta_j > 1:
        return False
    if j_i == 0 and j_f == 0:
        return False
    
    return True


def find_all_transitions(max_n: int = 10, Z: int = 1, 
                        electron_config: Optional[List[Tuple[int, int]]] = None,
                        allowed_only: bool = False) -> List[Dict]:
    """
    Find all possible transitions for given configuration.
    
    Parameters:
    -----------
    max_n : int
        Maximum principal quantum number to consider
    Z : int
        Atomic number
    electron_config : List[Tuple[int, int]], optional
        Electron configuration [(n, l), ...]
    allowed_only : bool
        If True, only return electric dipole allowed transitions
    
    Returns:
    --------
    transitions : List[Dict]
        List of transition dictionaries with:
        - 'initial': (n_i, l_i, j_i)
        - 'final': (n_f, l_f, j_f)
        - 'delta_E': transition energy (eV)
        - 'wavelength': wavelength (nm)
        - 'frequency': frequency (Hz)
        - 'allowed': whether transition is allowed
    """
    transitions = []
    
    # Generate all states up to max_n
    for n_i in range(1, max_n + 1):
        for l_i in range(n_i):
            for j_i in [l_i - 0.5, l_i + 0.5]:
                if j_i < 0:
                    continue
                
                for n_f in range(1, max_n + 1):
                    if n_f == n_i:
                        continue  # No self-transitions
                    
                    for l_f in range(n_f):
                        for j_f in [l_f - 0.5, l_f + 0.5]:
                            if j_f < 0:
                                continue
                            
                            # Check if allowed
                            allowed = is_allowed_transition(l_i, l_f, j_i, j_f)
                            
                            if allowed_only and not allowed:
                                continue
                            
                            # Calculate transition energy
                            try:
                                delta_E = calculate_transition_energy(
                                    n_i, l_i, j_i, n_f, l_f, j_f, Z, 
                                    electron_config, electron_config
                                )
                                
                                wavelength = calculate_wavelength(delta_E)
                                frequency = calculate_frequency(delta_E)
                                
                                transitions.append({
                                    'initial': (n_i, l_i, j_i),
                                    'final': (n_f, l_f, j_f),
                                    'delta_E': delta_E,
                                    'wavelength': wavelength,
                                    'frequency': frequency,
                                    'allowed': allowed
                                })
                            except (ValueError, ZeroDivisionError):
                                continue
    
    return transitions


def spectral_series(element: str, series_type: str = 'Lyman', max_n: int = 10,
                   ionization_state: int = 0) -> List[Dict]:
    """
    Generate spectral series transitions.
    
    Parameters:
    -----------
    element : str
        Element symbol (e.g., 'H', 'He')
    series_type : str
        Series type: 'Lyman', 'Balmer', 'Paschen', 'Brackett', 'Pfund'
    max_n : int
        Maximum principal quantum number
    ionization_state : int
        Ionization state (0 = neutral, 1 = singly ionized, etc.)
    
    Returns:
    --------
    transitions : List[Dict]
        List of transitions in the series
    """
    # Series definitions (initial n values)
    series_map = {
        'Lyman': 1,
        'Balmer': 2,
        'Paschen': 3,
        'Brackett': 4,
        'Pfund': 5
    }
    
    if series_type not in series_map:
        raise ValueError(f"Unknown series type: {series_type}")
    
    n_i = series_map[series_type]
    
    # Get Z from element (simplified - would use elements database)
    Z_map = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8}
    Z = Z_map.get(element, 1)
    Z_eff = Z - ionization_state
    
    transitions = []
    
    # Generate series transitions
    for n_f in range(n_i + 1, max_n + 1):
        # S → P transitions (most common)
        for j_i in [0.5]:  # S-state: j = 1/2
            for j_f in [0.5, 1.5]:  # P-state: j = 1/2, 3/2
                try:
                    delta_E = calculate_transition_energy(
                        n_i, 0, j_i, n_f, 1, j_f, Z_eff
                    )
                    
                    wavelength = calculate_wavelength(delta_E)
                    frequency = calculate_frequency(delta_E)
                    
                    transitions.append({
                        'initial': (n_i, 0, j_i),
                        'final': (n_f, 1, j_f),
                        'delta_E': delta_E,
                        'wavelength': wavelength,
                        'frequency': frequency,
                        'allowed': True
                    })
                except (ValueError, ZeroDivisionError):
                    continue
    
    return transitions

