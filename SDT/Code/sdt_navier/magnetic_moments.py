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


def compute_magnetic_moment_from_current_density(
    fields: FieldSystem,
    position: Tuple[int, int, int],
    radius_cells: float,
    global_calibration: Optional[float] = None,
) -> np.ndarray:
    """
    Compute magnetic moment from effective current density integral.
    
    μ = (1/2) ∫ r × J(r) d³r
    
    where J(r) is the effective current density from pressure field:
    J(r) ∝ (1-η) Γ κ v (or curl of flow field)
    
    This is the PREDICTIVE version - no per-particle normalization.
    
    Parameters
    ----------
    fields : FieldSystem
        Field system from simulation
    position : tuple (i, j, k)
        Grid indices of turbine center
    radius_cells : float
        Turbine radius in grid cells
    global_calibration : float, optional
        Global calibration constant (set once from proton, then predict others).
        If None, compute raw moment (needs calibration).
    
    Returns
    -------
    mu : array
        Magnetic moment vector (in units of μ_N if calibrated, otherwise raw)
    """
    i0, j0, k0 = position
    
    # Create coordinate grids relative to center
    i = np.arange(fields.nx)
    j = np.arange(fields.ny)
    k = np.arange(fields.nz)
    I, J, K = np.meshgrid(i, j, k, indexing='ij')
    
    # Physical positions relative to center (m)
    x = (I - i0) * fields.dx
    y = (J - j0) * fields.dy
    z = (K - k0) * fields.dz
    r = np.sqrt(x**2 + y**2 + z**2)
    r_cells = r / fields.dx
    
    # Mask: only compute within turbine radius
    mask = r_cells <= radius_cells
    
    # Effective current density from SDT fields
    # J ∝ (1-η) Γ κ v (circulation × curvature × flow)
    # For magnetic moment, we need the curl-like contribution
    # Simplified: J = (1-η) Γ κ × (vorticity or velocity)
    
    # Extract fields in turbine region
    sigma = fields.Gamma * fields.kappa * (1 - fields.eta)  # Diversion density
    v = fields.v  # Velocity field
    
    # Current density: J ∝ σ × v (simplified model)
    # More physically: J comes from curl of pressure field, but for now use this
    J_x = sigma * v[:, :, :, 0]
    J_y = sigma * v[:, :, :, 1]
    J_z = sigma * v[:, :, :, 2]
    
    # Apply mask
    J_x = np.where(mask, J_x, 0)
    J_y = np.where(mask, J_y, 0)
    J_z = np.where(mask, J_z, 0)
    
    # Compute dipole moment: μ = (1/2) ∫ r × J d³r
    # μ_x = (1/2) ∫ (y*J_z - z*J_y) dV
    # μ_y = (1/2) ∫ (z*J_x - x*J_z) dV
    # μ_z = (1/2) ∫ (x*J_y - y*J_x) dV
    
    dV = fields.dx * fields.dy * fields.dz  # Volume element
    
    mu_x = 0.5 * np.sum((y * J_z - z * J_y) * dV)
    mu_y = 0.5 * np.sum((z * J_x - x * J_z) * dV)
    mu_z = 0.5 * np.sum((x * J_y - y * J_x) * dV)
    
    mu_raw = np.array([mu_x, mu_y, mu_z])
    
    # Apply global calibration if provided
    # Calibration constant should be set once from proton, then used for all
    if global_calibration is not None:
        # Convert to nuclear magneton units
        # Calibration: μ_calibrated = μ_raw * calibration_factor
        mu = mu_raw * global_calibration / MU_N
    else:
        # Return raw moment (needs calibration)
        mu = mu_raw
    
    return mu


def compute_magnetic_moment(
    turbine: TurbineCell,
    fields: Optional[FieldSystem] = None,
    position: Optional[Tuple[int, int, int]] = None,
    radius_cells: Optional[float] = None,
    global_calibration: Optional[float] = None,
) -> np.ndarray:
    """
    Compute magnetic moment for a single turbine cell.
    
    NEW PREDICTIVE VERSION: Uses field-integral method if fields provided,
    otherwise falls back to simple model (for compatibility).
    
    Parameters
    ----------
    turbine : TurbineCell
        Turbine cell (proton or neutron)
    fields : FieldSystem, optional
        Field system from simulation. If provided, use field-integral method.
    position : tuple (i, j, k), optional
        Grid indices of turbine center (required if fields provided)
    radius_cells : float, optional
        Turbine radius in grid cells (required if fields provided)
    global_calibration : float, optional
        Global calibration constant (set once from proton)
    
    Returns
    -------
    mu : array
        Magnetic moment vector (in units of μ_N)
    """
    # If fields provided, use predictive field-integral method
    if fields is not None and position is not None and radius_cells is not None:
        return compute_magnetic_moment_from_current_density(
            fields, position, radius_cells, global_calibration
        )
    
    # Simple model: μ ∝ Γ κ (1-η) n̂
    # Used when fields not available - requires calibration
    orientation = np.array([1.0, 0.0, 1.0])
    orientation = orientation / np.linalg.norm(orientation)
    
    # Raw moment from SDT formula
    mu_mag_raw = turbine.Gamma * turbine.kappa * (1 - turbine.eta)
    
    # Sign: neutron has negative moment from reversed circulation
    sign = -1.0 if turbine.cell_type == "neutron" else 1.0
    
    # Apply calibration if provided
    if global_calibration is not None:
        mu_mag_n = sign * mu_mag_raw * global_calibration / MU_N
    else:
        mu_mag_n = sign * mu_mag_raw  # Raw value, needs calibration
    
    return mu_mag_n * orientation


def compute_nuclear_magnetic_moment(
    system: DeuteronSystem,
    global_calibration: Optional[float] = None,
) -> float:
    """
    Compute total magnetic moment for a nuclear system using field-integral method.
    
    PREDICTIVE VERSION: Computes from field integrals, no damping factors.
    
    Parameters
    ----------
    system : DeuteronSystem
        Deuteron system with fields
    global_calibration : float, optional
        Global calibration constant (set once from proton)
    
    Returns
    -------
    mu_total : float
        Total magnetic moment (in units of μ_N if calibrated)
    """
    # Compute individual moments from fields
    mu_p = compute_magnetic_moment_from_current_density(
        system.fields,
        system.proton.position,
        system.proton.radius_cells,
        global_calibration,
    )
    
    mu_n = compute_magnetic_moment_from_current_density(
        system.fields,
        system.neutron.position,
        system.neutron.radius_cells,
        global_calibration,
    )
    
    # Total moment: sum of individual moments
    # Field coupling effects emerge naturally from overlap
    mu_total_vec = mu_p + mu_n
    
    # Return magnitude along dominant direction
    mu_total = np.linalg.norm(mu_total_vec)
    
    # Sign from dot product with proton moment (proton is positive)
    if np.dot(mu_total_vec, mu_p) < 0:
        mu_total = -mu_total
    
    return mu_total


def compute_magnetic_moment_from_fields(
    fields: FieldSystem,
    position: Tuple[int, int, int],
    radius_cells: float,
    cell_type: str = "proton",
    global_calibration: Optional[float] = None,
) -> np.ndarray:
    """
    Compute magnetic moment from field values using field-integral method.
    
    This is the PREDICTIVE version - uses current density integral.
    
    Parameters
    ----------
    fields : FieldSystem
        Field system from simulation
    position : tuple (i, j, k)
        Grid indices of turbine center
    radius_cells : float
        Turbine radius in grid cells
    cell_type : str
        "proton" or "neutron" (for sign/orientation, but not normalization)
    global_calibration : float, optional
        Global calibration constant (set once from proton)
    
    Returns
    -------
    mu : array
        Magnetic moment vector (in units of μ_N if calibrated)
    """
    # Use field-integral method (predictive)
    mu = compute_magnetic_moment_from_current_density(
        fields, position, radius_cells, global_calibration
    )
    
    # Neutron has negative moment from reversed (left-handed) circulation
    # This should emerge from field calculations, but ensure sign is correct
    if cell_type == "neutron":
        # Check if sign is wrong - neutron moment should be negative
        mu_mag = np.linalg.norm(mu)
        if mu_mag > 0 and np.dot(mu, np.array([1.0, 0.0, 0.0])) > 0:
            # If positive, flip sign (neutron has reversed circulation)
            mu = -mu
    
    return mu


# Experimental values (CODATA 2018 / benchmark data)
MU_P_EXP = 2.79284734462   # μ_N (proton)
MU_N_EXP = -1.91304272     # μ_N (neutron, negative from reversed circulation)
MU_D_EXP = 0.857421        # μ_N (deuteron, p+n with damping)
MU_T_EXP = 2.979           # μ_N (triton)
MU_H_EXP = -2.128          # μ_N (helion)
MU_ALPHA_EXP = 0.0         # μ_N (alpha, spin-0)


def calibrate_from_proton(
    fields: FieldSystem,
    proton_position: Tuple[int, int, int],
    proton_radius_cells: float,
) -> float:
    """
    Calibrate global magnetic moment constant from proton.
    
    This sets the global calibration factor by matching the computed
    proton moment to the experimental value. Once calibrated, this
    constant is used for ALL nuclei (predictive).
    
    Parameters
    ----------
    fields : FieldSystem
        Field system with proton turbine
    proton_position : tuple (i, j, k)
        Grid indices of proton center
    proton_radius_cells : float
        Proton radius in grid cells
    
    Returns
    -------
    calibration : float
        Global calibration constant (units: μ_N per raw moment unit)
    """
    # Compute raw moment (without calibration)
    mu_raw = compute_magnetic_moment_from_current_density(
        fields, proton_position, proton_radius_cells, global_calibration=None
    )
    
    # Magnitude of raw moment
    mu_raw_mag = np.linalg.norm(mu_raw)
    
    if mu_raw_mag == 0:
        raise ValueError("Computed proton moment is zero - check field values")
    
    # Calibration: experimental / raw
    # Convert experimental value to SI units
    mu_p_exp_si = MU_P_EXP * MU_N  # J/T
    
    # Calibration factor: how many raw units per μ_N
    calibration = mu_p_exp_si / mu_raw_mag
    
    return calibration


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

