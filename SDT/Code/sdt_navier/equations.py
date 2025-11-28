"""
SDT-Navier Field Equations

Implements the SDT-Navier field equations:
1. Incompressibility: ∇·v = 0
2. Flow equation: ρ_s (∂v/∂t + (v·∇)v) = -∇P + F_curv + F_slip
3. Curvature evolution: ∂κ/∂t + (v·∇)κ = C(κ,v) - D(κ,η)
4. Slip evolution: ∂η/∂t + (v·∇)η = S_strain(κ,v) - S_healing(κ)
5. Energy balance: ∂e/∂t + ∇·(ev) = P·σ - ė_radiation - ė_ν

Also implements force functionals with minimal but physically interpretable forms.
"""

import numpy as np
from typing import Tuple, Optional
from .fields import FieldSystem, compute_diversion_density
from sdt_core.constants import (
    RHO_S, ALPHA_CURV, BETA_SLIP, GAMMA_CREATE, 
    DELTA_DESTROY, EPSILON_STRAIN, ZETA_HEAL
)
from sdt_core.physics import compute_navier_forces


class SDTNavierEquations:
    """
    SDT-Navier field equations with configurable force functional parameters.
    """
    
    def __init__(
        self,
        rho_s: float = RHO_S,
        alpha_curv: float = ALPHA_CURV,
        beta_slip: float = BETA_SLIP,
        gamma_create: float = GAMMA_CREATE,
        delta_destroy: float = DELTA_DESTROY,
        epsilon_strain: float = EPSILON_STRAIN,
        zeta_heal: float = ZETA_HEAL,
    ):
        """
        Initialize SDT-Navier equations with force functional parameters.
        
        Parameters
        ----------
        rho_s : float
            Effective spation density (kg/m³)
        alpha_curv : float
            Curvature gradient force coefficient
        beta_slip : float
            Slip damping coefficient
        gamma_create : float
            Curvature creation coefficient
        delta_destroy : float
            Curvature destruction coefficient
        epsilon_strain : float
            Slip strain coefficient
        zeta_heal : float
            Slip healing coefficient
        """
        self.rho_s = rho_s
        self.alpha_curv = alpha_curv
        self.beta_slip = beta_slip
        self.gamma_create = gamma_create
        self.delta_destroy = delta_destroy
        self.epsilon_strain = epsilon_strain
        self.zeta_heal = zeta_heal
    
    def compute_incompressibility_residual(
        self,
        fields: FieldSystem,
        grad_v: np.ndarray,  # Shape (nx, ny, nz, 3, 3) - gradient tensor
    ) -> np.ndarray:
        """
        Compute incompressibility residual: ∇·v.
        
        Parameters
        ----------
        fields : FieldSystem
            Current field state
        grad_v : array
            Velocity gradient tensor, shape (nx, ny, nz, 3, 3)
            grad_v[i,j,k,a,b] = ∂v_a/∂x_b
        
        Returns
        -------
        div_v : array
            Divergence of velocity, shape (nx, ny, nz)
        """
        # Trace of gradient tensor = divergence
        return grad_v[:, :, :, 0, 0] + grad_v[:, :, :, 1, 1] + grad_v[:, :, :, 2, 2]
    
    def compute_flow_rhs(
        self,
        fields: FieldSystem,
        grad_P: np.ndarray,  # Shape (nx, ny, nz, 3)
        grad_v: np.ndarray,  # Shape (nx, ny, nz, 3, 3)
        F_curv: np.ndarray,  # Shape (nx, ny, nz, 3)
        F_slip: np.ndarray,  # Shape (nx, ny, nz, 3)
    ) -> np.ndarray:
        """
        Compute right-hand side of flow equation.
        
        ρ_s (∂v/∂t + (v·∇)v) = -∇P + F_curv + F_slip
        
        Returns
        -------
        dv_dt : array
            Time derivative of velocity, shape (nx, ny, nz, 3)
        """
        # Advection term: (v·∇)v
        # For each component a: (v·∇)v_a = v_b · ∂v_a/∂x_b
        v_advect = np.zeros_like(fields.v)
        for a in range(3):
            for b in range(3):
                v_advect[:, :, :, a] += fields.v[:, :, :, b] * grad_v[:, :, :, a, b]
        
        # Total acceleration using unified physics core
        dv_dt = compute_navier_forces(
            grad_P, F_curv, F_slip, v_advect, self.rho_s
        )
        
        return dv_dt
    
    def compute_curvature_rhs(
        self,
        fields: FieldSystem,
        grad_kappa: np.ndarray,  # Shape (nx, ny, nz, 3)
        grad_v: np.ndarray,  # Shape (nx, ny, nz, 3, 3)
        C: np.ndarray,  # Shape (nx, ny, nz)
        D: np.ndarray,  # Shape (nx, ny, nz)
    ) -> np.ndarray:
        """
        Compute right-hand side of curvature evolution equation.
        
        ∂κ/∂t + (v·∇)κ = C(κ,v) - D(κ,η)
        
        Returns
        -------
        dkappa_dt : array
            Time derivative of curvature, shape (nx, ny, nz)
        """
        # Advection term: (v·∇)κ = v · ∇κ
        v_dot_grad_kappa = (
            fields.v[:, :, :, 0] * grad_kappa[:, :, :, 0] +
            fields.v[:, :, :, 1] * grad_kappa[:, :, :, 1] +
            fields.v[:, :, :, 2] * grad_kappa[:, :, :, 2]
        )
        
        dkappa_dt = C - D - v_dot_grad_kappa
        
        return dkappa_dt
    
    def compute_slip_rhs(
        self,
        fields: FieldSystem,
        grad_eta: np.ndarray,  # Shape (nx, ny, nz, 3)
        grad_v: np.ndarray,  # Shape (nx, ny, nz, 3, 3)
        S_strain: np.ndarray,  # Shape (nx, ny, nz)
        S_healing: np.ndarray,  # Shape (nx, ny, nz)
    ) -> np.ndarray:
        """
        Compute right-hand side of slip evolution equation.
        
        ∂η/∂t + (v·∇)η = S_strain(κ,v) - S_healing(κ)
        
        Returns
        -------
        deta_dt : array
            Time derivative of slip, shape (nx, ny, nz)
        """
        # Advection term: (v·∇)η = v · ∇η
        v_dot_grad_eta = (
            fields.v[:, :, :, 0] * grad_eta[:, :, :, 0] +
            fields.v[:, :, :, 1] * grad_eta[:, :, :, 1] +
            fields.v[:, :, :, 2] * grad_eta[:, :, :, 2]
        )
        
        deta_dt = S_strain - S_healing - v_dot_grad_eta
        
        return deta_dt
    
    def compute_energy_rhs(
        self,
        fields: FieldSystem,
        grad_e: np.ndarray,  # Shape (nx, ny, nz, 3)
        sigma: np.ndarray,  # Shape (nx, ny, nz)
        e_radiation: Optional[np.ndarray] = None,  # Shape (nx, ny, nz)
        e_nu: Optional[np.ndarray] = None,  # Shape (nx, ny, nz)
    ) -> np.ndarray:
        """
        Compute right-hand side of energy balance equation.
        
        ∂e/∂t + ∇·(ev) = P·σ - ė_radiation - ė_ν
        
        Returns
        -------
        de_dt : array
            Time derivative of energy density, shape (nx, ny, nz)
        """
        # Advection term: ∇·(ev) = e(∇·v) + v·∇e
        # For incompressible flow, ∇·v = 0, so: ∇·(ev) = v·∇e
        v_dot_grad_e = (
            fields.v[:, :, :, 0] * grad_e[:, :, :, 0] +
            fields.v[:, :, :, 1] * grad_e[:, :, :, 1] +
            fields.v[:, :, :, 2] * grad_e[:, :, :, 2]
        )
        
        # Source term: P·σ
        source = fields.P * sigma
        
        # Sink terms
        sink = 0.0
        if e_radiation is not None:
            sink += e_radiation
        if e_nu is not None:
            sink += e_nu
        
        de_dt = source - sink - v_dot_grad_e
        
        return de_dt


def compute_force_curvature(
    fields: FieldSystem,
    grad_kappa: np.ndarray,  # Shape (nx, ny, nz, 3)
    alpha_curv: float = 1.0e-10,
) -> np.ndarray:
    """
    Compute curvature gradient force: F_curv = -α_curv ∇κ
    
    This force drives flow from regions of high curvature to low curvature.
    
    Parameters
    ----------
    fields : FieldSystem
        Current field state
    grad_kappa : array
        Gradient of curvature, shape (nx, ny, nz, 3)
    alpha_curv : float
        Curvature force coefficient (N·m²)
    
    Returns
    -------
    F_curv : array
        Curvature force, shape (nx, ny, nz, 3)
    """
    return -alpha_curv * grad_kappa


def compute_force_slip(
    fields: FieldSystem,
    beta_slip: float = 1.0e15,
) -> np.ndarray:
    """
    Compute slip damping force: F_slip = -β_slip η v
    
    This force represents energy loss to slip (becomes heat, radiation, neutrinos).
    
    Parameters
    ----------
    fields : FieldSystem
        Current field state
    beta_slip : float
        Slip damping coefficient (kg/(m³·s))
    
    Returns
    -------
    F_slip : array
        Slip force, shape (nx, ny, nz, 3)
    """
    # Expand eta to match velocity shape
    eta_expanded = fields.eta[:, :, :, np.newaxis]  # Shape (nx, ny, nz, 1)
    return -beta_slip * eta_expanded * fields.v


def compute_curvature_creation(
    fields: FieldSystem,
    grad_v: np.ndarray,  # Shape (nx, ny, nz, 3, 3)
    gamma_create: float = 1.0e-24,
) -> np.ndarray:
    """
    Compute curvature creation: C(κ,v) = γ_create κ |∇·v|
    
    Curvature is created by converging flow (how vortices/tori form).
    
    Parameters
    ----------
    fields : FieldSystem
        Current field state
    grad_v : array
        Velocity gradient tensor, shape (nx, ny, nz, 3, 3)
    gamma_create : float
        Curvature creation coefficient (m²/s)
    
    Returns
    -------
    C : array
        Curvature creation rate, shape (nx, ny, nz)
    """
    # Compute divergence
    div_v = grad_v[:, :, :, 0, 0] + grad_v[:, :, :, 1, 1] + grad_v[:, :, :, 2, 2]
    
    # For incompressible flow, ∇·v should be ~0, but we use absolute value
    # to capture convergence/divergence effects
    return gamma_create * fields.kappa * np.abs(div_v)


def compute_curvature_destruction(
    fields: FieldSystem,
    delta_destroy: float = 1.0e-9,
) -> np.ndarray:
    """
    Compute curvature destruction: D(κ,η) = δ_destroy κ η
    
    Curvature is destroyed via slip (how vortices unwind → decay, radiation, neutrinos).
    
    Parameters
    ----------
    fields : FieldSystem
        Current field state
    delta_destroy : float
        Curvature destruction coefficient (1/s)
    
    Returns
    -------
    D : array
        Curvature destruction rate, shape (nx, ny, nz)
    """
    return delta_destroy * fields.kappa * fields.eta


def compute_slip_strain(
    fields: FieldSystem,
    grad_v: np.ndarray,  # Shape (nx, ny, nz, 3, 3)
    epsilon_strain: float = 1.0e-24,
) -> np.ndarray:
    """
    Compute slip increase from strain: S_strain(κ,v) = ε_strain κ |∇v|
    
    High curvature + misaligned flow → increased slip (less traction).
    
    Parameters
    ----------
    fields : FieldSystem
        Current field state
    grad_v : array
        Velocity gradient tensor, shape (nx, ny, nz, 3, 3)
    epsilon_strain : float
        Slip strain coefficient (m²/s)
    
    Returns
    -------
    S_strain : array
        Slip strain rate, shape (nx, ny, nz)
    """
    # Compute |∇v| as Frobenius norm of gradient tensor
    grad_v_norm = np.sqrt(
        np.sum(grad_v**2, axis=(3, 4))
    )
    
    return epsilon_strain * fields.kappa * grad_v_norm


def compute_slip_healing(
    fields: FieldSystem,
    zeta_heal: float = 1.0e-9,
) -> np.ndarray:
    """
    Compute slip decrease from stable curvature: S_healing(κ) = ζ_heal κ²
    
    Well-structured toroids (protons, alpha) → decreased slip (more traction).
    
    Parameters
    ----------
    fields : FieldSystem
        Current field state
    zeta_heal : float
        Slip healing coefficient (m/s)
    
    Returns
    -------
    S_healing : array
        Slip healing rate, shape (nx, ny, nz)
    """
    return zeta_heal * fields.kappa**2

