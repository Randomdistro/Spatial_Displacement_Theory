"""
Hydrogenic Calculations

Single-electron (hydrogenic) atom calculations using SDT formulations.
From Phase 2 and Phase 27A.
"""

import numpy as np
from . import constants as const


def calculate_K_factor(n: int, Z: int = 1, use_reduced_mass: bool = True) -> float:
    """
    Calculate K-factor (Ϟ) for hydrogenic atom.
    
    From Phase 2: Ϟ_n = n/(Zα)
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    Z : int
        Atomic number (default: 1 for hydrogen)
    use_reduced_mass : bool
        Whether to use reduced mass correction (only for hydrogen, default: True)
    
    Returns:
    --------
    K : float
        K-factor (Ϟ), dimensionless
    """
    # Note: Reduced mass correction affects energy but not K-factor directly
    # K-factor is determined by orbital quantization condition
    return n / (Z * const.ALPHA)


def calculate_orbital_radius(n: int, Z: int = 1, use_reduced_mass: bool = True) -> float:
    """
    Calculate orbital radius for hydrogenic atom.
    
    From Phase 27A: r_n = n²a₀/Z
    With reduced mass correction: r_n(H) = a₀n²(1 + m_e/m_p)
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    Z : int
        Atomic number (default: 1 for hydrogen)
    use_reduced_mass : bool
        Whether to apply reduced mass correction (only for hydrogen, default: True)
    
    Returns:
    --------
    r : float
        Orbital radius (m)
    """
    radius = n**2 * const.A_0 / Z
    
    # Reduced mass correction for hydrogen only
    if use_reduced_mass and Z == 1:
        radius *= (1.0 + const.M_E / const.M_P)
    
    return radius


def calculate_energy_level(n: int, Z: int = 1, use_reduced_mass: bool = True) -> float:
    """
    Calculate energy level for hydrogenic atom.
    
    From Phase 27A: E_n = -½μc²/Ϟ_n² = -13.6 Z²/n² eV
    With reduced mass: E_n = -13.6 Z²/n² × (μ/m_e) eV
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    Z : int
        Atomic number (default: 1 for hydrogen)
    use_reduced_mass : bool
        Whether to apply reduced mass correction (only for hydrogen, default: True)
    
    Returns:
    --------
    E : float
        Energy level (eV)
    """
    if n <= 0:
        raise ValueError("Principal quantum number must be positive")
    
    # Base energy
    energy = -const.RYDBERG_EV * Z**2 / (n**2)
    
    # Reduced mass correction for hydrogen only
    if use_reduced_mass and Z == 1:
        energy *= const.REDUCED_MASS_FACTOR_H
    
    return energy


def calculate_orbital_velocity(n: int, Z: int = 1, r: float = None, use_reduced_mass: bool = True) -> float:
    """
    Calculate orbital velocity using SDT orbital law.
    
    From Phase 16: v(r) = (c/K) * sqrt(R/r)
    For atomic systems: R = a₀, K = Ϟ_n = n/(Zα)
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    Z : int
        Atomic number (default: 1 for hydrogen)
    r : float, optional
        Orbital radius (m). If None, calculates from n and Z.
    use_reduced_mass : bool
        Whether to use reduced mass correction for radius (only for hydrogen)
    
    Returns:
    --------
    v : float
        Orbital velocity (m/s)
    """
    if r is None:
        r = calculate_orbital_radius(n, Z, use_reduced_mass)
    
    K = calculate_K_factor(n, Z, use_reduced_mass)
    
    # Reference radius (Bohr radius for atomic systems)
    R_ref = const.A_0
    
    # Orbital velocity law
    v = (const.C / K) * np.sqrt(R_ref / r)
    
    return v


def calculate_velocity_at_proton_surface(n: int, Z: int = 1, use_reduced_mass: bool = True) -> float:
    """
    Calculate orbital velocity at proton surface.
    
    Uses SDT orbital law: v(R_p) = (c/K) * sqrt(a₀/R_p)
    For hydrogen ground state, this gives v ≈ 1.84c
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    Z : int
        Atomic number (default: 1 for hydrogen)
    use_reduced_mass : bool
        Whether to use reduced mass correction (only for hydrogen)
    
    Returns:
    --------
    v_surf : float
        Orbital velocity at proton surface (m/s)
    """
    K = calculate_K_factor(n, Z, use_reduced_mass)
    R_ref = const.A_0
    
    # Velocity at proton surface
    v_surf = (const.C / K) * np.sqrt(R_ref / const.R_P)
    
    return v_surf


def calculate_c_boundary_radius(n: int, Z: int = 1, use_reduced_mass: bool = True) -> float:
    """
    Calculate c-boundary radius (ϟ) where orbital velocity equals c.
    
    From Phase 16: ϟ = R/K²
    For hydrogen ground state, ϟ = a₀/(1/α)² = α²a₀ ≈ r_e (classical electron radius)
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    Z : int
        Atomic number (default: 1 for hydrogen)
    use_reduced_mass : bool
        Whether to use reduced mass correction (only for hydrogen)
    
    Returns:
    --------
    c_boundary : float
        c-boundary radius (m) where v(ϟ) = c
    """
    K = calculate_K_factor(n, Z, use_reduced_mass)
    R_ref = const.A_0
    
    # c-boundary radius
    c_boundary = R_ref / (K ** 2)
    
    return c_boundary

