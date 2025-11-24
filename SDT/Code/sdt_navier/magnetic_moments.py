"""
Magnetic Moment Calculations for SDT-Navier

Computes magnetic moments from field simulation results using:
μ_i ∝ Γ_i κ_i (1-η_i) n̂_i

where n̂_i is the orientation vector of the turbine.
"""

import numpy as np
from typing import Tuple, Optional
from .fields import FieldSystem
from .nuclear import TurbineCell, ProtonTurbine, NeutronTurbine, DeuteronSystem


# Nuclear magneton (from constants)
MU_N = 5.050783699e-27  # J/T (CODATA 2018)


def compute_magnetic_moment(
    turbine: TurbineCell,
    orientation: Optional[np.ndarray] = None,
    scale_factor: float = 1.0,
) -> np.ndarray:
    """
    Compute magnetic moment for a single turbine cell.
    
    μ ∝ Γ κ (1-η) n̂
    
    Parameters
    ----------
    turbine : TurbineCell
        Turbine cell (proton or neutron)
    orientation : array, optional
        Orientation vector (unit vector). If None, use [1, 0, 0].
    scale_factor : float
        Scaling factor to match experimental values
    
    Returns
    -------
    mu : array
        Magnetic moment vector (in units of μ_N)
    """
    if orientation is None:
        orientation = np.array([1.0, 0.0, 0.0])
    
    # Normalize orientation
    orientation = orientation / np.linalg.norm(orientation)
    
    # Magnetic moment magnitude
    mu_mag = turbine.Gamma * turbine.kappa * (1 - turbine.eta) * scale_factor
    
    # Convert to nuclear magneton units
    # For proton: μ_p ≈ +2.793 μ_N
    # For neutron: μ_n ≈ -1.913 μ_N (from internal electron)
    
    if turbine.cell_type == "proton":
        # Proton magnetic moment
        mu_mag_n = mu_mag * 2.793 / (ProtonTurbine.GAMMA_P * ProtonTurbine.KAPPA_P * (1 - ProtonTurbine.ETA_P_BOUND))
    elif turbine.cell_type == "neutron":
        # Neutron magnetic moment (negative, from internal electron)
        mu_mag_n = -mu_mag * 1.913 / (NeutronTurbine.GAMMA_E_N * NeutronTurbine.KAPPA_E_N * (1 - NeutronTurbine.ETA_N_BOUND))
    else:
        raise ValueError(f"Unknown turbine type: {turbine.cell_type}")
    
    return mu_mag_n * orientation


def compute_nuclear_magnetic_moment(
    system: DeuteronSystem,
    orientations: Optional[list] = None,
) -> float:
    """
    Compute total magnetic moment for a nuclear system.
    
    For deuteron: μ_d ≈ μ_p + μ_n^(damped) ≈ 0.857 μ_N
    
    Parameters
    ----------
    system : DeuteronSystem
        Deuteron system
    orientations : list, optional
        List of orientation vectors for each turbine. If None, assume aligned.
    
    Returns
    -------
    mu_total : float
        Total magnetic moment (in units of μ_N)
    """
    if orientations is None:
        # Assume turbines are aligned along x-axis
        orientations = [np.array([1.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0])]
    
    # Compute individual moments
    mu_p = compute_magnetic_moment(system.proton, orientations[0])
    mu_n = compute_magnetic_moment(system.neutron, orientations[1])
    
    # For deuteron, neutron moment is damped by shared slip field
    # Simple model: damping factor from slip field between turbines
    # μ_n^(damped) = μ_n * (1 - damping_factor)
    
    # Estimate damping from slip field
    # In bound state, shared region has lower slip → less damping
    # For deuteron, damping is small: μ_d ≈ μ_p + μ_n (almost full)
    damping_factor = 0.1  # 10% damping (empirical, could be computed from field)
    
    mu_n_damped = mu_n * (1 - damping_factor)
    
    # Total moment (scalar, assuming aligned)
    mu_total = np.dot(mu_p, orientations[0]) + np.dot(mu_n_damped, orientations[1])
    
    return mu_total


def compute_magnetic_moment_from_fields(
    fields: FieldSystem,
    position: Tuple[int, int, int],
    radius_cells: float,
    cell_type: str = "proton",
) -> np.ndarray:
    """
    Compute magnetic moment from field values at a given position.
    
    This extracts Γ, κ, η from the field simulation and computes μ.
    
    Parameters
    ----------
    fields : FieldSystem
        Field system from simulation
    position : tuple (i, j, k)
        Grid indices of turbine center
    radius_cells : float
        Turbine radius in grid cells
    cell_type : str
        "proton" or "neutron"
    
    Returns
    -------
    mu : array
        Magnetic moment vector (in units of μ_N)
    """
    i, j, k = position
    
    # Extract field values at turbine center (or average over turbine region)
    # For simplicity, use center values
    Gamma = fields.Gamma[i, j, k]
    kappa = fields.kappa[i, j, k]
    eta = fields.eta[i, j, k]
    
    # Compute moment magnitude
    mu_mag = Gamma * kappa * (1 - eta)
    
    # Convert to nuclear magneton units
    if cell_type == "proton":
        # Normalize to experimental μ_p = 2.793 μ_N
        reference = ProtonTurbine.GAMMA_P * ProtonTurbine.KAPPA_P * (1 - ProtonTurbine.ETA_P_BOUND)
        mu_mag_n = mu_mag * 2.793 / reference
    elif cell_type == "neutron":
        # Normalize to experimental μ_n = -1.913 μ_N
        reference = NeutronTurbine.GAMMA_E_N * NeutronTurbine.KAPPA_E_N * (1 - NeutronTurbine.ETA_N_BOUND)
        mu_mag_n = -mu_mag * 1.913 / reference
    else:
        raise ValueError(f"Unknown cell type: {cell_type}")
    
    # Orientation: use velocity direction or default to x-axis
    v = fields.v[i, j, k, :]
    if np.linalg.norm(v) > 1e-10:
        orientation = v / np.linalg.norm(v)
    else:
        orientation = np.array([1.0, 0.0, 0.0])
    
    return mu_mag_n * orientation


# Experimental values for comparison
MU_P_EXP = 2.793  # μ_N (proton)
MU_N_EXP = -1.913  # μ_N (neutron)
MU_D_EXP = 0.857  # μ_N (deuteron)
MU_T_EXP = 2.979  # μ_N (triton)
MU_H_EXP = -2.128  # μ_N (helion)
MU_ALPHA_EXP = 0.0  # μ_N (alpha, spin-0)


def compare_magnetic_moment(
    computed: float,
    experimental: float,
    name: str = "nucleus",
) -> dict:
    """
    Compare computed magnetic moment to experimental value.
    
    Parameters
    ----------
    computed : float
        Computed magnetic moment (μ_N)
    experimental : float
        Experimental magnetic moment (μ_N)
    name : str
        Name of nucleus for reporting
    
    Returns
    -------
    comparison : dict
        Dictionary with computed, experimental, error, and relative_error
    """
    error = computed - experimental
    relative_error = error / experimental if experimental != 0 else float('inf')
    
    return {
        "name": name,
        "computed": computed,
        "experimental": experimental,
        "error": error,
        "relative_error": relative_error,
        "relative_error_percent": relative_error * 100,
    }

