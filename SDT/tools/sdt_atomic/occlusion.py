"""
Occlusion Geometry Engine

Multi-electron occlusion calculations from Phase 6 and Phase 27B.
"""

import numpy as np
from typing import List, Tuple, Optional
from .constants import *


def calculate_occlusion_fraction(r_i: float, r_j: float, d_e: float = None) -> float:
    """
    Calculate occlusion fraction E_ij between two electrons.
    
    From Phase 6: E_ij = d_e²/(16r_ij²) for r_ij >> d_e
    
    Parameters:
    -----------
    r_i : float
        Position of electron i (m)
    r_j : float
        Position of electron j (m)
    d_e : float, optional
        Effective hard-sphere diameter (m). If None, uses default from constants.
    
    Returns:
    --------
    E_ij : float
        Occlusion fraction (dimensionless, 0-1)
    """
    if d_e is None:
        d_e = D_E
    
    # Distance between electrons
    r_ij = abs(r_i - r_j)
    
    # Avoid division by zero
    if r_ij < d_e:
        return 1.0  # Complete occlusion when electrons overlap
    
    # Occlusion fraction (far-field approximation)
    E_ij = d_e**2 / (16.0 * r_ij**2)
    
    # Ensure 0 <= E_ij <= 1
    return min(1.0, max(0.0, E_ij))


def ray_trace_occlusion(r_i: float, r_j: float, d_e: float = None, n_rays: int = 10000) -> float:
    """
    Calculate directional occlusion fraction using ray-tracing.
    
    For near-field or directional effects, use ray-tracing to determine
    actual occlusion fraction accounting for geometry.
    
    Parameters:
    -----------
    r_i : float
        Position of electron i (m)
    r_j : float
        Position of electron j (m)
    d_e : float, optional
        Effective hard-sphere diameter (m). If None, uses default from constants.
    n_rays : int
        Number of rays to trace (default: 10000)
    
    Returns:
    --------
    E_ij : float
        Occlusion fraction from ray-tracing (dimensionless, 0-1)
    """
    if d_e is None:
        d_e = D_E
    
    r_ij = abs(r_i - r_j)
    
    # For far-field, use analytical formula
    if r_ij > 10.0 * d_e:
        return calculate_occlusion_fraction(r_i, r_j, d_e)
    
    # For near-field, use ray-tracing
    # This is a simplified version - full implementation would trace rays
    # from electron i to nucleus, checking if electron j occludes
    
    # Simplified: use analytical formula with correction for near-field
    E_base = calculate_occlusion_fraction(r_i, r_j, d_e)
    
    # Near-field correction (when electrons are close)
    if r_ij < 5.0 * d_e:
        correction = 1.0 - np.exp(-(r_ij / d_e)**2)
        E_ij = E_base * (1.0 + correction)
        return min(1.0, E_ij)
    
    return E_base


def calculate_Z_eff(electron_index: int, electron_positions: List[float], 
                    Z: int, d_e: float = None) -> float:
    """
    Calculate effective nuclear charge Z_eff for electron i.
    
    From Phase 6: Z_eff,i = Z[1 - Σ_j≠i E_ij]
    
    Parameters:
    -----------
    electron_index : int
        Index of electron for which to calculate Z_eff
    electron_positions : List[float]
        List of electron orbital radii (m)
    Z : int
        Atomic number
    d_e : float, optional
        Effective hard-sphere diameter (m). If None, uses default from constants.
    
    Returns:
    --------
    Z_eff : float
        Effective nuclear charge (dimensionless)
    """
    if d_e is None:
        d_e = D_E
    
    if electron_index >= len(electron_positions):
        raise ValueError(f"electron_index {electron_index} out of range")
    
    r_i = electron_positions[electron_index]
    
    # Sum occlusion from all other electrons
    occlusion_sum = 0.0
    for j, r_j in enumerate(electron_positions):
        if j != electron_index:
            E_ij = calculate_occlusion_fraction(r_i, r_j, d_e)
            occlusion_sum += E_ij
    
    # Effective nuclear charge
    Z_eff = Z * (1.0 - occlusion_sum)
    
    # Ensure Z_eff >= 1 (at least one proton charge visible)
    return max(1.0, Z_eff)


def dodecardinal_frame_directions(n: int, l: int) -> np.ndarray:
    """
    Generate geometric directions for orbital using dodecardinal frame.
    
    From Phase 6: s-orbitals use polar directions, p-orbitals use equatorial,
    d-orbitals use cube vertices, etc.
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number (0=s, 1=p, 2=d, ...)
    
    Returns:
    --------
    directions : np.ndarray
        Array of direction vectors (shape: (n_directions, 3))
    """
    if l == 0:  # s-orbital: polar directions
        # Two polar directions (up and down)
        directions = np.array([
            [0.0, 0.0, 1.0],
            [0.0, 0.0, -1.0]
        ])
    elif l == 1:  # p-orbital: equatorial directions
        # Three equatorial directions (x, y, z axes)
        directions = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ])
    elif l == 2:  # d-orbital: cube vertices
        # Five directions from cube vertices
        directions = np.array([
            [1.0, 1.0, 0.0],
            [1.0, -1.0, 0.0],
            [-1.0, 1.0, 0.0],
            [-1.0, -1.0, 0.0],
            [0.0, 0.0, 1.0]
        ]) / np.sqrt(2.0)
    else:  # Higher l: use more directions
        # Generate uniform directions on sphere
        n_directions = 2 * (l + 1)**2
        theta = np.linspace(0, np.pi, n_directions // 2)
        phi = np.linspace(0, 2*np.pi, n_directions)
        
        directions = []
        for t in theta:
            for p in phi:
                directions.append([
                    np.sin(t) * np.cos(p),
                    np.sin(t) * np.sin(p),
                    np.cos(t)
                ])
        
        directions = np.array(directions[:n_directions])
    
    # Normalize directions
    norms = np.linalg.norm(directions, axis=1, keepdims=True)
    directions = directions / norms
    
    return directions


def calculate_directional_occlusion(electron_i_pos: float, electron_i_direction: np.ndarray,
                                   electron_j_pos: float, electron_j_direction: np.ndarray,
                                   d_e: float = None) -> float:
    """
    Calculate directional occlusion between two electrons.
    
    Accounts for directional effects (e.g., p-electrons have different
    occlusion depending on orientation relative to other electrons).
    
    Parameters:
    -----------
    electron_i_pos : float
        Orbital radius of electron i (m)
    electron_i_direction : np.ndarray
        Direction vector for electron i (shape: (3,))
    electron_j_pos : float
        Orbital radius of electron j (m)
    electron_j_direction : np.ndarray
        Direction vector for electron j (shape: (3,))
    d_e : float, optional
        Effective hard-sphere diameter (m). If None, uses default from constants.
    
    Returns:
    --------
    E_ij : float
        Directional occlusion fraction (dimensionless, 0-1)
    """
    if d_e is None:
        d_e = D_E
    
    # Average distance between orbital positions
    r_ij = abs(electron_i_pos - electron_j_pos)
    
    # Dot product of direction vectors (angle between orbitals)
    cos_angle = np.dot(electron_i_direction, electron_j_direction)
    
    # Directional correction: parallel orbitals occlude less than perpendicular
    # This is a simplified model - full implementation would use ray-tracing
    directional_factor = 1.0 - 0.5 * (1.0 + cos_angle)
    
    # Base occlusion
    E_base = calculate_occlusion_fraction(electron_i_pos, electron_j_pos, d_e)
    
    # Apply directional correction
    E_ij = E_base * directional_factor
    
    return min(1.0, max(0.0, E_ij))

