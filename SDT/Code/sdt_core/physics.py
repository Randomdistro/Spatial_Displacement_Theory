"""
SDT Core Physics
Central repository for physical laws and calculations in Spatial Displacement Theory.
Unifies Particle (Pressure Kernel) and Field (Navier) logic.
"""

import numpy as np
from typing import Tuple, Optional

def compute_acceleration_particle(
    r_eff: float,
    kappa: float,
    r_vec: np.ndarray,
    distance: float
) -> np.ndarray:
    """
    Computes the acceleration on a test particle due to a displacement source.
    
    SDT Fundamental Law (Phase 15):
    a = c^2 * R_eff / (Kappa^2 * r^2)
    
    The acceleration is directed TOWARDS the source (along r_vec).
    
    Parameters
    ----------
    r_eff : float
        Effective Radius of the source (m)
    kappa : float
        Velocity Factor (Kappa/Koppa) of the source (dimensionless)
    r_vec : np.ndarray
        Vector pointing FROM the test particle TO the source.
    distance : float
        Distance between particle and source (magnitude of r_vec).
        
    Returns
    -------
    np.ndarray
        Acceleration vector.
    """
    if distance == 0:
        return np.zeros_like(r_vec)
    
    # Speed of Light (Lattice Limit)
    c = 299792458.0
        
    # Magnitude: a = c^2 * R_eff / (Kappa^2 * r^2)
    accel_magnitude = (c**2 * r_eff) / (kappa**2 * distance**2)
    
    # Direction: Normalized r_vec
    direction = r_vec / distance
    
    return direction * accel_magnitude

def compute_navier_forces(
    grad_P: np.ndarray,
    F_curv: np.ndarray,
    F_slip: np.ndarray,
    v_advect: np.ndarray,
    rho_s: float
) -> np.ndarray:
    """
    Computes the time derivative of velocity (acceleration) for the SDT-Navier field.
    
    SDT Fundamental Law (Field View):
    rho_s (dv/dt + (v.grad)v) = -grad_P + F_curv + F_slip
    
    Parameters
    ----------
    grad_P : np.ndarray
        Pressure gradient.
    F_curv : np.ndarray
        Curvature force.
    F_slip : np.ndarray
        Slip force.
    v_advect : np.ndarray
        Advection term (v.grad)v.
    rho_s : float
        Spation density.
        
    Returns
    -------
    np.ndarray
        dv/dt (Acceleration field).
    """
    # dv/dt = (-grad_P + F_curv + F_slip - rho_s * v_advect) / rho_s
    return (-grad_P + F_curv + F_slip - rho_s * v_advect) / rho_s

def calculate_neutron_contraction(
    v_phase: float,
    c: float = 299792458.0
) -> float:
    """
    Calculates the geometric contraction factor (Gamma) for the Neutron state.
    
    In SDT, v > c is interpreted as "Overtightened Phase Velocity".
    The contraction is driven by the tension: gamma = 1 / sqrt(1 - v^2/c^2)
    For v > c, this becomes imaginary in SR, but in SDT geometry it represents
    internal winding density. We use the magnitude |gamma|.
    
    Parameters
    ----------
    v_phase : float
        Phase velocity at the proton surface (approx 1.84c).
    c : float
        Speed of light.
        
    Returns
    -------
    float
        Contraction factor (magnitude).
    """
    # Use absolute difference for geometric tension magnitude
    # gamma = 1 / sqrt(|1 - (v/c)^2|)
    beta = v_phase / c
    return 1.0 / np.sqrt(np.abs(1.0 - beta**2))

def calculate_geometric_anomaly(
    r_inner: float,
    circumference_outer: float
) -> float:
    """
    Calculates the Geometric Anomaly (a_e) as a pitch ratio.
    
    a_e = r_inner / L_outer
    
    Parameters
    ----------
    r_inner : float
        Inner radius (e.g., Classical Electron Radius).
    circumference_outer : float
        Outer circulation length (e.g., Compton Wavelength).
        
    Returns
    -------
    float
        Anomaly ratio.
    """
    if circumference_outer == 0:
        return 0.0
    return r_inner / circumference_outer

