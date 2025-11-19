"""
Ionization Calculator (ALL Ionizations)

Calculate ALL ionization energies for all elements and states.
From Phase 27A and Phase 27B.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from . import hydrogenic
from . import screening
from . import energy_levels
from .constants import *


def calculate_ionization_energy(element: str, ionization_state: int,
                                electron_config: Optional[List[Tuple[int, int]]] = None,
                                removal_index: Optional[int] = None) -> float:
    """
    Calculate ionization energy for specific electron removal.
    
    Parameters:
    -----------
    element : str
        Element symbol (e.g., 'H', 'He', 'Li')
    ionization_state : int
        Current ionization state (0 = neutral, 1 = singly ionized, etc.)
    electron_config : List[Tuple[int, int]], optional
        Electron configuration [(n, l), ...]
    removal_index : int, optional
        Index of electron to remove. If None, removes outermost electron.
    
    Returns:
    --------
    IE : float
        Ionization energy (eV)
    """
    # Get Z from element (simplified - would use elements database)
    Z_map = {
        'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
        'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16,
        'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20
    }
    Z = Z_map.get(element, 1)
    
    if electron_config is None:
        # Get ground state configuration
        try:
            electron_config = elements.get_ground_state_config(element)
        except (ValueError, AttributeError):
            # Default: single electron in n=1 for hydrogen-like
            electron_config = [(1, 0)]
    
    if removal_index is None:
        removal_index = len(electron_config) - 1  # Remove outermost
    
    # Get electron to remove
    n_remove, l_remove = electron_config[removal_index]
    
    # For ionization, calculate Z_eff from current configuration
    # If configuration has multiple electrons, use screening
    if len(electron_config) > 1:
        try:
            Z_eff = screening.calculate_screening_factor(Z, n_remove, l_remove, electron_config)
        except ValueError:
            # If calculation fails, use simplified Z_eff = Z
            Z_eff = Z
    else:
        # Single electron: no screening
        Z_eff = Z
    
    # Ionization energy = binding energy = |E_n|
    IE = abs(hydrogenic.calculate_energy_level(n_remove, int(Z_eff)))
    
    return IE


def calculate_sequential_ionization(element: str, max_ionization: Optional[int] = None) -> List[float]:
    """
    Calculate sequential ionization energies.
    
    Parameters:
    -----------
    element : str
        Element symbol
    max_ionization : int, optional
        Maximum ionization state to calculate. If None, calculates all up to Z.
    
    Returns:
    --------
    ionization_energies : List[float]
        List of ionization energies (eV) for IE(1), IE(2), ..., IE(max)
    """
    # Get Z
    Z_map = {
        'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
        'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16,
        'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20
    }
    Z = Z_map.get(element, 1)
    
    if max_ionization is None:
        max_ionization = Z
    
    ionization_energies = []
    
    # Simple approximation: calculate ionization energy for each state
    # Full calculation would track electron configuration and recalculate Z_eff
    for ion_state in range(max_ionization):
        try:
            # Approximate: assume removing electron from n = ion_state + 1, l = 0
            n = ion_state + 1
            Z_eff = Z - ion_state  # Simplified: no screening for ionization calculation
            
            IE = abs(hydrogenic.calculate_energy_level(n, Z_eff))
            ionization_energies.append(IE)
        except (ValueError, ZeroDivisionError):
            break
    
    return ionization_energies


def find_all_ionization_states(element: str) -> List[Dict]:
    """
    Find all possible ionization energies for element.
    
    Parameters:
    -----------
    element : str
        Element symbol
    
    Returns:
    --------
    ionization_states : List[Dict]
        List of ionization state dictionaries with:
        - 'ionization_state': ionization state (1 = first ionization, etc.)
        - 'IE': ionization energy (eV)
        - 'element': element symbol
    """
    # Get Z
    Z_map = {
        'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
        'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16,
        'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20
    }
    Z = Z_map.get(element, 1)
    
    ionization_states = []
    
    # Calculate sequential ionizations
    IEs = calculate_sequential_ionization(element, Z)
    
    for i, IE in enumerate(IEs, 1):
        ionization_states.append({
            'ionization_state': i,
            'IE': IE,
            'element': element
        })
    
    return ionization_states


def calculate_ionization_potential(Z: int, n: int, l: int,
                                   config: List[Tuple[int, int]],
                                   removal_index: int) -> float:
    """
    Calculate ionization potential for specific electron removal.
    
    Parameters:
    -----------
    Z : int
        Atomic number
    n : int
        Principal quantum number of electron to remove
    l : int
        Angular momentum quantum number
    config : List[Tuple[int, int]]
        Electron configuration
    removal_index : int
        Index of electron to remove in config
    
    Returns:
    --------
    IE : float
        Ionization energy (eV)
    """
    # Calculate Z_eff for electron to be removed
    Z_eff = screening.calculate_screening_factor(Z, n, l, config)
    
    # Ionization energy = binding energy
    IE = abs(hydrogenic.calculate_energy_level(n, int(Z_eff)))
    
    return IE

