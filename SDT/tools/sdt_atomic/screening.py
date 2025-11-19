"""
Multi-Electron Screening

Calculate effective nuclear charge Z_eff from occlusion geometry.
From Phase 6 and Phase 27B.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from .constants import *
from . import occlusion


def calculate_screening_factor(Z: int, n: int, l: int, electron_config: List[Tuple[int, int]]) -> float:
    """
    Calculate screening factor (Z_eff/Z) for electron in configuration.
    
    From Phase 6: Z_eff = Z[1 - Σ E_ij] where E_ij is occlusion from other electrons.
    
    Parameters:
    -----------
    Z : int
        Atomic number
    n : int
        Principal quantum number of electron of interest
    l : int
        Angular momentum quantum number (0=s, 1=p, 2=d, ...)
    electron_config : List[Tuple[int, int]]
        List of (n, l) tuples for all electrons in atom
    
    Returns:
    --------
    Z_eff : float
        Effective nuclear charge (dimensionless)
    """
    # Find index of electron of interest
    electron_index = None
    for i, (n_i, l_i) in enumerate(electron_config):
        if n_i == n and l_i == l:
            electron_index = i
            break
    
    if electron_index is None:
        raise ValueError(f"Electron (n={n}, l={l}) not found in configuration")
    
    # Calculate orbital radii for all electrons
    electron_positions = []
    for n_i, l_i in electron_config:
        # Approximate orbital radius (could be refined with Z_eff iteration)
        r_i = A_0 * n_i**2 / Z
        electron_positions.append(r_i)
    
    # Calculate Z_eff using occlusion geometry
    Z_eff = occlusion.calculate_Z_eff(electron_index, electron_positions, Z)
    
    return Z_eff


def slater_equivalent_screening(Z: int, n: int, l: int, config: List[Tuple[int, int]]) -> float:
    """
    Calculate Z_eff using SDT occlusion geometry (equivalent to Slater rules).
    
    This is a geometric derivation of Slater-like screening rules.
    
    Parameters:
    -----------
    Z : int
        Atomic number
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
    config : List[Tuple[int, int]]
        Electron configuration [(n, l), ...]
    
    Returns:
    --------
    Z_eff : float
        Effective nuclear charge
    """
    return calculate_screening_factor(Z, n, l, config)


def directional_occlusion_fraction(n: int, l: int, core_config: List[Tuple[int, int]]) -> float:
    """
    Calculate directional occlusion fraction Ξ_nℓ.
    
    From Phase 6: accounts for directional effects of orbitals.
    s-orbitals: polar directions, least occluded
    p-orbitals: equatorial, moderate occlusion
    d-orbitals: within cube occlusion, highly occluded
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
    core_config : List[Tuple[int, int]]
        Core electron configuration
    
    Returns:
    --------
    Xi : float
        Unoccluded fraction (dimensionless, 0-1)
    """
    # Get directions for orbital
    directions = occlusion.dodecardinal_frame_directions(n, l)
    
    # For each direction, calculate occlusion from core electrons
    occlusion_sum = 0.0
    n_directions = len(directions)
    
    for dir_vec in directions:
        dir_occlusion = 0.0
        
        # Calculate occlusion from each core electron
        for n_core, l_core in core_config:
            if n_core < n:  # Only inner electrons screen
                # Approximate radius for core electron
                r_core = A_0 * n_core**2 / Z
                r_outer = A_0 * n**2 / Z
                
                # Directional occlusion
                core_directions = occlusion.dodecardinal_frame_directions(n_core, l_core)
                
                # Average occlusion over core directions
                for core_dir in core_directions:
                    E_ij = occlusion.calculate_directional_occlusion(
                        r_outer, dir_vec, r_core, core_dir
                    )
                    dir_occlusion += E_ij
        
        occlusion_sum += dir_occlusion / n_directions
    
    # Unoccluded fraction
    Xi = 1.0 - occlusion_sum / n_directions
    
    # Ensure 0 <= Xi <= 1
    return max(0.0, min(1.0, Xi))


def calculate_multi_electron_energy(n: int, l: int, Z: int, 
                                   electron_config: List[Tuple[int, int]],
                                   Z_eff: float = None) -> float:
    """
    Calculate energy level for multi-electron atom.
    
    From Phase 27B: E_nℓ = E_H × (Z_eff²/n²) × Ξ_nℓ
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
    Z : int
        Atomic number
    electron_config : List[Tuple[int, int]]
        Electron configuration
    Z_eff : float, optional
        Effective nuclear charge. If None, calculates from occlusion.
    
    Returns:
    --------
    E : float
        Energy level (eV)
    """
    if Z_eff is None:
        Z_eff = calculate_screening_factor(Z, n, l, electron_config)
    
    # Base hydrogenic energy
    E_H = -RYDBERG_EV * Z_eff**2 / (n**2)
    
    # Directional occlusion factor
    core_config = [(n_i, l_i) for n_i, l_i in electron_config if n_i < n]
    Xi = directional_occlusion_fraction(n, l, core_config)
    
    # Total energy
    E = E_H * Xi
    
    return E

