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
