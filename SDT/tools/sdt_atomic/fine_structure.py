"""
Fine Structure Corrections

Three corrections at order α⁴ from Phase 3:
1. Relativistic kinetic: -p⁴/(8m_e³c²)
2. Spin-orbit coupling: helical wake interaction
3. Darwin term: vortex zitterbewegung smearing
"""

import numpy as np
from .constants import *


def calculate_fine_structure(n: int, l: int, j: float, Z: int = 1) -> float:
    """
    Calculate fine structure energy correction.
    
    From Phase 3: ΔE_fs = (α² Z⁴)/(n⁴) × [n/(j+½) - 3/4] × m_e c² / 2
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number (0=s, 1=p, 2=d, ...)
    j : float
        Total angular momentum (j = l ± 1/2 for one electron)
    Z : int
        Atomic number (default: 1 for hydrogen)
    
    Returns:
    --------
    delta_E_fs : float
        Fine structure correction (eV)
    """
    if l < 0 or l >= n:
        raise ValueError(f"Invalid l={l} for n={n}")
    
    if j != l + 0.5 and j != l - 0.5:
        if l == 0:
            if j != 0.5:
                raise ValueError(f"Invalid j={j} for l=0 (must be 0.5)")
        else:
            raise ValueError(f"Invalid j={j} for l={l} (must be {l}±0.5)")
    
    # Base fine structure formula
    # ΔE_fs = (m_e c² α⁴ Z⁴)/(2n⁴) × [n/(j+½) - 3/4]
    m_e_c2_eV = M_E * C**2 / E_CHARGE  # Electron rest energy in eV
    alpha4 = ALPHA**4
    
    delta_E_fs = (m_e_c2_eV * alpha4 * Z**4) / (2.0 * n**4) * (n / (j + 0.5) - 3.0/4.0)
    
    return delta_E_fs


def relativistic_correction(n: int, l: int, Z: int = 1) -> float:
    """
    Calculate relativistic kinetic energy correction H₁.
    
    From Phase 3: H₁ = -p⁴/(8m_e³c²)
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
    Z : int
        Atomic number
    
    Returns:
    --------
    delta_E_rel : float
        Relativistic correction (eV)
    """
    m_e_c2_eV = M_E * C**2 / E_CHARGE
    alpha4 = ALPHA**4
    
    if l >= 1:
        # For ℓ ≥ 1: ⟨H₁⟩ = -(m_e c² α⁴ Z⁴)/(8n⁴) × [4 - n/(ℓ+1/2)]
        delta_E_rel = -(m_e_c2_eV * alpha4 * Z**4) / (8.0 * n**4) * (4.0 - n / (l + 0.5))
    else:
        # For ℓ = 0: ⟨H₁⟩ = -(m_e c² α⁴ Z⁴)/(8n⁴) × [4 - 4n]
        delta_E_rel = -(m_e_c2_eV * alpha4 * Z**4) / (8.0 * n**4) * (4.0 - 4.0 * n)
    
    return delta_E_rel


def spin_orbit_coupling(n: int, l: int, j: float, Z: int = 1) -> float:
    """
    Calculate spin-orbit coupling H_SO.
    
    From Phase 3: H_SO ∝ S · L / r³
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number (must be ≥ 1)
    j : float
        Total angular momentum
    Z : int
        Atomic number
    
    Returns:
    --------
    delta_E_SO : float
        Spin-orbit coupling correction (eV)
    """
    if l < 1:
        return 0.0  # Spin-orbit coupling only for ℓ ≥ 1
    
    if j != l + 0.5 and j != l - 0.5:
        raise ValueError(f"Invalid j={j} for l={l} (must be {l}±0.5)")
    
    m_e_c2_eV = M_E * C**2 / E_CHARGE
    alpha4 = ALPHA**4
    
    # S · L expectation value
    # S · L = (ℏ²/2)[j(j+1) - ℓ(ℓ+1) - 3/4]
    S_dot_L = 0.5 * (j * (j + 1) - l * (l + 1) - 0.75)
    
    # ⟨H_SO⟩ = (Z⁴α⁴ m_e c²)/(2n³ ℓ(ℓ+1/2)(ℓ+1)) × [j(j+1) - ℓ(ℓ+1) - 3/4]
    delta_E_SO = (Z**4 * alpha4 * m_e_c2_eV) / (2.0 * n**3 * l * (l + 0.5) * (l + 1)) * S_dot_L
    
    return delta_E_SO


def darwin_term(n: int, Z: int = 1) -> float:
    """
    Calculate Darwin term H_D (zitterbewegung smearing).
    
    From Phase 3: H_D affects only ℓ = 0 (S-states)
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    Z : int
        Atomic number
    
    Returns:
    --------
    delta_E_D : float
        Darwin term correction (eV)
    """
    m_e_c2_eV = M_E * C**2 / E_CHARGE
    alpha4 = ALPHA**4
    
    # Darwin term: ⟨H_D⟩ = (Z⁴α⁴ m_e c²)/(2n³) for ℓ = 0
    delta_E_D = (Z**4 * alpha4 * m_e_c2_eV) / (2.0 * n**3)
    
    return delta_E_D


def fine_structure_splitting(n: int, l: int, Z: int = 1) -> float:
    """
    Calculate fine structure splitting between j = ℓ+1/2 and j = ℓ-1/2.
    
    From Phase 3: |ΔE_split| = (m_e c² α⁴ Z⁴)/(2n³ℓ(ℓ+1))
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number (must be ≥ 1)
    Z : int
        Atomic number
    
    Returns:
    --------
    delta_E_split : float
        Fine structure splitting (eV)
    """
    if l < 1:
        return 0.0  # No splitting for S-states
    
    m_e_c2_eV = M_E * C**2 / E_CHARGE
    alpha4 = ALPHA**4
    
    # Splitting: |ΔE_split| = (m_e c² α⁴ Z⁴)/(2n³ℓ(ℓ+1))
    delta_E_split = (m_e_c2_eV * alpha4 * Z**4) / (2.0 * n**3 * l * (l + 1))
    
    return delta_E_split

