"""
SDT-Navier Field Theory Module

Implements the SDT-Navier field theory: a local field formulation of the SDT master
equation discretized on a dodecahedral/RRPT lattice for simulating spation flow
and nuclear systems.

The master equation: Ẻ = P_∞ A_eff Γ κ (1-η)

is converted to local field form:
- Pressure field P(x,t)
- Flow velocity v(x,t)
- Curvature density κ(x,t)
- Slip field η(x,t)
- Energy density e(x,t)
"""

__version__ = "0.1.0"

from .fields import FieldSystem, initialize_fields
from .equations import (
    SDTNavierEquations,
    compute_diversion_density,
    compute_force_curvature,
    compute_force_slip,
    compute_curvature_creation,
    compute_curvature_destruction,
    compute_slip_strain,
    compute_slip_healing,
)
from .lattice import DodecahedralLattice, compute_gradient, compute_divergence, compute_advection
from .solver import SDTNavierSolver
from .nuclear import (
    TurbineCell,
    ProtonTurbine,
    NeutronTurbine,
    DeuteronSystem,
    TritonSystem,
    HelionSystem,
    AlphaSystem,
)
from .magnetic_moments import compute_magnetic_moment, compute_nuclear_magnetic_moment

__all__ = [
    "FieldSystem",
    "initialize_fields",
    "SDTNavierEquations",
    "compute_diversion_density",
    "compute_force_curvature",
    "compute_force_slip",
    "compute_curvature_creation",
    "compute_curvature_destruction",
    "compute_slip_strain",
    "compute_slip_healing",
    "DodecahedralLattice",
    "compute_gradient",
    "compute_divergence",
    "compute_advection",
    "SDTNavierSolver",
    "TurbineCell",
    "ProtonTurbine",
    "NeutronTurbine",
    "DeuteronSystem",
    "TritonSystem",
    "HelionSystem",
    "AlphaSystem",
    "compute_magnetic_moment",
    "compute_nuclear_magnetic_moment",
]

