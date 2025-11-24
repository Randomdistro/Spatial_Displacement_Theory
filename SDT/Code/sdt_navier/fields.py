"""
SDT-Navier Field Definitions

Defines continuous fields over space:
- P(x,t): spation pressure
- v(x,t): spation flow velocity (3D vector field)
- κ(x,t): curvature density
- η(x,t): slip field (0 ≤ η ≤ 1)
- e(x,t): energy density

Also defines:
- σ(x,t): diversion density = Γ(x,t) · κ(x,t) · (1-η(x,t))
- Γ(x,t): circulation factor (poloidal velocity / c)
"""

import numpy as np
from typing import Tuple, Optional, Dict
from dataclasses import dataclass


@dataclass
class FieldSystem:
    """
    Container for all SDT-Navier fields on a discrete grid.
    
    All fields are stored as numpy arrays with shape (nx, ny, nz) for scalar fields
    or (nx, ny, nz, 3) for vector fields.
    """
    # Scalar fields
    P: np.ndarray  # Pressure field (Pa)
    kappa: np.ndarray  # Curvature density (m⁻¹)
    eta: np.ndarray  # Slip field (dimensionless, 0 ≤ η ≤ 1)
    e: np.ndarray  # Energy density (J/m³)
    Gamma: np.ndarray  # Circulation factor (dimensionless)
    
    # Vector field
    v: np.ndarray  # Flow velocity (m/s), shape (nx, ny, nz, 3)
    
    # Grid parameters
    nx: int
    ny: int
    nz: int
    dx: float  # Grid spacing (m)
    dy: float
    dz: float
    
    # Time
    t: float = 0.0  # Current time (s)
    
    def __post_init__(self):
        """Validate field shapes and values."""
        # Check scalar field shapes
        expected_shape = (self.nx, self.ny, self.nz)
        for field_name, field in [("P", self.P), ("kappa", self.kappa), 
                                   ("eta", self.eta), ("e", self.e), ("Gamma", self.Gamma)]:
            if field.shape != expected_shape:
                raise ValueError(f"Field {field_name} has shape {field.shape}, expected {expected_shape}")
        
        # Check vector field shape
        expected_v_shape = (self.nx, self.ny, self.nz, 3)
        if self.v.shape != expected_v_shape:
            raise ValueError(f"Velocity field v has shape {self.v.shape}, expected {expected_v_shape}")
        
        # Validate slip field bounds
        if np.any(self.eta < 0) or np.any(self.eta > 1):
            raise ValueError("Slip field η must satisfy 0 ≤ η ≤ 1")
        
        # Validate circulation factor
        if np.any(self.Gamma < 0):
            raise ValueError("Circulation factor Γ must be non-negative")


def initialize_fields(
    nx: int,
    ny: int,
    nz: int,
    dx: float,
    dy: Optional[float] = None,
    dz: Optional[float] = None,
    P_infinity: float = 1.65e31,  # Nuclear scale pressure (Pa) from Phase 19
    initial_velocity: Optional[np.ndarray] = None,
    initial_kappa: Optional[np.ndarray] = None,
    initial_eta: Optional[np.ndarray] = None,
    initial_Gamma: Optional[np.ndarray] = None,
) -> FieldSystem:
    """
    Initialize SDT-Navier field system.
    
    Parameters
    ----------
    nx, ny, nz : int
        Grid dimensions
    dx, dy, dz : float
        Grid spacing (m). If dy or dz are None, use dx.
    P_infinity : float
        Background spation pressure (Pa). Default is nuclear scale from Phase 19.
    initial_velocity : array, optional
        Initial velocity field, shape (nx, ny, nz, 3). If None, initialize to zero.
    initial_kappa : array, optional
        Initial curvature density, shape (nx, ny, nz). If None, initialize to zero.
    initial_eta : array, optional
        Initial slip field, shape (nx, ny, nz). If None, initialize to small value (0.01).
    initial_Gamma : array, optional
        Initial circulation factor, shape (nx, ny, nz). If None, initialize to 0.546 (proton value).
    
    Returns
    -------
    FieldSystem
        Initialized field system
    """
    if dy is None:
        dy = dx
    if dz is None:
        dz = dx
    
    # Initialize scalar fields
    P = np.full((nx, ny, nz), P_infinity, dtype=np.float64)
    
    if initial_kappa is None:
        kappa = np.zeros((nx, ny, nz), dtype=np.float64)
    else:
        kappa = np.array(initial_kappa, dtype=np.float64)
        if kappa.shape != (nx, ny, nz):
            raise ValueError(f"initial_kappa shape {kappa.shape} doesn't match grid ({nx}, {ny}, {nz})")
    
    if initial_eta is None:
        eta = np.full((nx, ny, nz), 0.01, dtype=np.float64)  # Small initial slip
    else:
        eta = np.array(initial_eta, dtype=np.float64)
        if eta.shape != (nx, ny, nz):
            raise ValueError(f"initial_eta shape {eta.shape} doesn't match grid ({nx}, {ny}, {nz})")
    
    if initial_Gamma is None:
        Gamma = np.full((nx, ny, nz), 0.546, dtype=np.float64)  # Proton circulation factor
    else:
        Gamma = np.array(initial_Gamma, dtype=np.float64)
        if Gamma.shape != (nx, ny, nz):
            raise ValueError(f"initial_Gamma shape {Gamma.shape} doesn't match grid ({nx}, {ny}, {nz})")
    
    # Initialize vector field
    if initial_velocity is None:
        v = np.zeros((nx, ny, nz, 3), dtype=np.float64)
    else:
        v = np.array(initial_velocity, dtype=np.float64)
        if v.shape != (nx, ny, nz, 3):
            raise ValueError(f"initial_velocity shape {v.shape} doesn't match grid ({nx}, {ny}, {nz}, 3)")
    
    # Initialize energy density from master equation
    # e = P · σ = P · Γ · κ · (1-η) per unit volume
    sigma = Gamma * kappa * (1 - eta)
    e = P * sigma  # Energy density (W/m³, which is J/(m³·s))
    # Convert to energy density by multiplying by characteristic time
    # For nuclear scale, use τ ~ R_p / c
    tau_char = 8.4e-16 / 2.998e8  # ~2.8e-24 s (proton response time)
    e = e * tau_char  # Now in J/m³
    
    return FieldSystem(
        P=P,
        kappa=kappa,
        eta=eta,
        e=e,
        Gamma=Gamma,
        v=v,
        nx=nx,
        ny=ny,
        nz=nz,
        dx=dx,
        dy=dy,
        dz=dz,
        t=0.0,
    )


def compute_diversion_density(fields: FieldSystem) -> np.ndarray:
    """
    Compute diversion density σ(x,t) = Γ(x,t) · κ(x,t) · (1-η(x,t)).
    
    This represents how strongly local curvature diverts the background flow.
    
    Parameters
    ----------
    fields : FieldSystem
        Current field state
    
    Returns
    -------
    sigma : array
        Diversion density, shape (nx, ny, nz)
    """
    return fields.Gamma * fields.kappa * (1 - fields.eta)


def add_turbine_source(
    fields: FieldSystem,
    position: Tuple[int, int, int],
    radius_cells: float,
    kappa_value: float,
    Gamma_value: float,
    eta_value: float,
    profile: str = "gaussian",
) -> None:
    """
    Add a turbine cell source to the fields.
    
    This sets up a localized region with high curvature, circulation, and low slip
    to represent a nucleon turbine.
    
    Parameters
    ----------
    fields : FieldSystem
        Field system to modify (in-place)
    position : tuple (i, j, k)
        Grid indices of turbine center
    radius_cells : float
        Turbine radius in grid cells
    kappa_value : float
        Peak curvature density (m⁻¹)
    Gamma_value : float
        Circulation factor
    eta_value : float
        Slip value (should be small for stable turbines, e.g., 0.0003)
    profile : str
        Profile type: "gaussian" or "step"
    """
    i0, j0, k0 = position
    
    # Create coordinate grids
    i = np.arange(fields.nx)
    j = np.arange(fields.ny)
    k = np.arange(fields.nz)
    I, J, K = np.meshgrid(i, j, k, indexing='ij')
    
    # Distance from center in grid cells
    di = (I - i0) * fields.dx
    dj = (J - j0) * fields.dy
    dk = (K - k0) * fields.dz
    r = np.sqrt(di**2 + dj**2 + dk**2)
    r_cells = r / fields.dx  # Convert to grid cells
    
    if profile == "gaussian":
        # Gaussian profile with width = radius_cells
        weight = np.exp(-0.5 * (r_cells / radius_cells)**2)
    elif profile == "step":
        # Step function: 1 inside radius, 0 outside
        weight = (r_cells < radius_cells).astype(float)
    else:
        raise ValueError(f"Unknown profile type: {profile}")
    
    # Add turbine source (blend with existing values)
    fields.kappa = np.maximum(fields.kappa, kappa_value * weight)
    fields.Gamma = np.maximum(fields.Gamma, Gamma_value * weight)
    fields.eta = np.minimum(fields.eta, eta_value * weight)
    
    # Update energy density
    sigma = compute_diversion_density(fields)
    tau_char = 8.4e-16 / 2.998e8
    fields.e = fields.P * sigma * tau_char

