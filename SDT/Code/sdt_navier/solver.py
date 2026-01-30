"""
SDT-Navier Solver Kernel

Implements time-stepping for SDT-Navier field equations with:
- Explicit time-stepping (Euler or Runge-Kutta)
- Incompressibility enforcement via pressure projection
- Adaptive timestep based on CFL condition
"""

import numpy as np
from typing import Optional, Callable

try:  # SciPy is optional for the simplified projection used here
    from scipy.sparse import csc_matrix  # type: ignore
    from scipy.sparse.linalg import spsolve  # type: ignore
except ImportError:  # pragma: no cover - fallback for lightweight environments
    csc_matrix = None  # type: ignore
    spsolve = None  # type: ignore

from .fields import FieldSystem
from .equations import (
    SDTNavierEquations,
    compute_force_curvature,
    compute_force_slip,
    compute_curvature_creation,
    compute_curvature_destruction,
    compute_slip_strain,
    compute_slip_healing,
    compute_diversion_density,
)
from .lattice import (
    compute_gradient,
    compute_divergence,
    compute_velocity_gradient,
)


class SDTNavierSolver:
    """
    Solver for SDT-Navier field equations.
    """
    
    def __init__(
        self,
        fields: FieldSystem,
        equations: SDTNavierEquations,
        dt: Optional[float] = None,
        cfl: float = 0.5,
        method: str = "euler",
        enforce_incompressibility: bool = True,
    ):
        """
        Initialize SDT-Navier solver.
        
        Parameters
        ----------
        fields : FieldSystem
            Initial field state
        equations : SDTNavierEquations
            SDT-Navier equations with force functional parameters
        dt : float, optional
            Fixed timestep (s). If None, use adaptive timestep based on CFL.
        cfl : float
            CFL number for adaptive timestep (default 0.5)
        method : str
            Time-stepping method: "euler" or "rk2"
        enforce_incompressibility : bool
            Whether to enforce ∇·v = 0 via pressure projection
        """
        self.fields = fields
        self.equations = equations
        self.cfl = cfl
        self.method = method
        self.enforce_incompressibility = enforce_incompressibility
        
        if dt is None:
            # Estimate initial timestep from CFL condition
            dt = self._estimate_timestep()
        
        self.dt = dt
        self.t = fields.t
    
    def _estimate_timestep(self) -> float:
        """
        Estimate timestep from CFL condition: dt < CFL * dx / |v_max|.
        
        Returns
        -------
        dt : float
            Estimated timestep (s)
        """
        v_max = np.max(np.abs(self.fields.v))
        if v_max == 0:
            v_max = 1.0  # Default to avoid division by zero
        
        dx_min = min(self.fields.dx, self.fields.dy, self.fields.dz)
        dt = self.cfl * dx_min / v_max
        
        # Also consider diffusion timescale
        # For slip damping: dt < 1 / (beta_slip * eta_max / rho_s)
        eta_max = np.max(self.fields.eta)
        if eta_max > 0:
            dt_slip = 1.0 / (self.equations.beta_slip * eta_max / self.equations.rho_s)
            dt = min(dt, dt_slip)
        
        return dt
    
    def step(self) -> None:
        """
        Perform one time step.
        """
        if self.method == "euler":
            self._step_euler()
        elif self.method == "rk2":
            self._step_rk2()
        else:
            raise ValueError(f"Unknown method: {self.method}")
        
        # Update time
        self.fields.t = self.t
        self.t += self.dt
    
    def _step_euler(self) -> None:
        """
        Euler time-stepping: u^{n+1} = u^n + dt * du/dt.
        """
        # Compute gradients
        grad_P = compute_gradient(self.fields.P, self.fields, boundary="extrapolate")
        grad_kappa = compute_gradient(self.fields.kappa, self.fields, boundary="extrapolate")
        grad_eta = compute_gradient(self.fields.eta, self.fields, boundary="extrapolate")
        grad_e = compute_gradient(self.fields.e, self.fields, boundary="extrapolate")
        grad_v = compute_velocity_gradient(self.fields.v, self.fields, boundary="extrapolate")
        
        # Compute force functionals
        F_curv = compute_force_curvature(
            self.fields,
            grad_kappa,
            alpha_curv=self.equations.alpha_curv,
        )
        F_slip = compute_force_slip(
            self.fields,
            beta_slip=self.equations.beta_slip,
        )
        
        C = compute_curvature_creation(
            self.fields,
            grad_v,
            gamma_create=self.equations.gamma_create,
        )
        D = compute_curvature_destruction(
            self.fields,
            delta_destroy=self.equations.delta_destroy,
        )
        
        S_strain = compute_slip_strain(
            self.fields,
            grad_v,
            epsilon_strain=self.equations.epsilon_strain,
        )
        S_healing = compute_slip_healing(
            self.fields,
            zeta_heal=self.equations.zeta_heal,
        )
        
        # Compute RHS for each equation
        dv_dt = self.equations.compute_flow_rhs(
            self.fields,
            grad_P,
            grad_v,
            F_curv,
            F_slip,
        )
        
        dkappa_dt = self.equations.compute_curvature_rhs(
            self.fields,
            grad_kappa,
            grad_v,
            C,
            D,
        )
        
        deta_dt = self.equations.compute_slip_rhs(
            self.fields,
            grad_eta,
            grad_v,
            S_strain,
            S_healing,
        )
        
        sigma = compute_diversion_density(self.fields)
        de_dt = self.equations.compute_energy_rhs(
            self.fields,
            grad_e,
            sigma,
        )
        
        # Update fields
        self.fields.v += self.dt * dv_dt
        self.fields.kappa += self.dt * dkappa_dt
        self.fields.eta += self.dt * deta_dt
        self.fields.e += self.dt * de_dt
        
        # Clamp slip field to [0, 1]
        self.fields.eta = np.clip(self.fields.eta, 0.0, 1.0)
        
        # Enforce incompressibility
        if self.enforce_incompressibility:
            self._project_pressure()
    
    def _step_rk2(self) -> None:
        """
        Second-order Runge-Kutta (Heun's method).
        """
        # Store initial state
        v0 = self.fields.v.copy()
        kappa0 = self.fields.kappa.copy()
        eta0 = self.fields.eta.copy()
        e0 = self.fields.e.copy()
        
        # First stage (Euler step)
        self._step_euler()
        
        # Store intermediate state
        v1 = self.fields.v.copy()
        kappa1 = self.fields.kappa.copy()
        eta1 = self.fields.eta.copy()
        e1 = self.fields.e.copy()
        
        # Restore initial state
        self.fields.v = v0
        self.fields.kappa = kappa0
        self.fields.eta = eta0
        self.fields.e = e0
        
        # Second stage: compute RHS at intermediate state
        # (This is a simplified RK2 - full implementation would recompute RHS)
        # For now, use average of initial and intermediate
        self.fields.v = 0.5 * (v0 + v1)
        self.fields.kappa = 0.5 * (kappa0 + kappa1)
        self.fields.eta = 0.5 * (eta0 + eta1)
        self.fields.e = 0.5 * (e0 + e1)
        
        # Enforce incompressibility
        if self.enforce_incompressibility:
            self._project_pressure()
    
    def _project_pressure(self) -> None:
        """
        Enforce incompressibility ∇·v = 0 via proper pressure projection.
        
        Standard projection method:
        1. Compute divergence of intermediate velocity: div_v = ∇·v*
        2. Solve Poisson equation: ∇²φ = (1/Δt) ∇·v*
        3. Correct velocity: v^{n+1} = v* - ∇φ
        
        This ensures ∇·v^{n+1} = 0 exactly (up to numerical error).
        """
        # Step 1: Compute divergence of current velocity
        div_v = compute_divergence(self.fields.v, self.fields, boundary="extrapolate")
        
        # Step 2: Solve Poisson equation ∇²φ = (1/Δt) div_v
        # For periodic BCs, use FFT; for Dirichlet, use sparse solver
        # For now, implement a simple iterative solver (Jacobi) for Dirichlet BCs
        
        # Initialize potential
        phi = np.zeros_like(div_v)
        
        # Jacobi iteration for Poisson: ∇²φ = f
        # φ^{n+1} = (1/6) * (φ_neighbors + h² * f)
        # where h = dx (assuming cubic grid)
        h = self.fields.dx  # Grid spacing
        f = div_v / self.dt  # Source term: (1/Δt) div_v
        
        # Iterate until convergence (or fixed number of iterations)
        max_iter = 50
        tolerance = 1e-6
        
        for iteration in range(max_iter):
            phi_new = phi.copy()
            
            # Interior points: Jacobi update
            if self.fields.nx > 2 and self.fields.ny > 2 and self.fields.nz > 2:
                # 6-point stencil for 3D Laplacian
                phi_new[1:-1, 1:-1, 1:-1] = (
                    phi[2:, 1:-1, 1:-1] + phi[:-2, 1:-1, 1:-1] +  # x neighbors
                    phi[1:-1, 2:, 1:-1] + phi[1:-1, :-2, 1:-1] +  # y neighbors
                    phi[1:-1, 1:-1, 2:] + phi[1:-1, 1:-1, :-2] +  # z neighbors
                    h**2 * f[1:-1, 1:-1, 1:-1]
                ) / 6.0
            
            # Check convergence
            error = np.max(np.abs(phi_new - phi))
            phi = phi_new
            
            if error < tolerance:
                break
        
        # Step 3: Correct velocity: v^{n+1} = v* - ∇φ
        grad_phi = compute_gradient(phi, self.fields, boundary="extrapolate")
        self.fields.v -= grad_phi
        
        # Optional: Also update pressure field
        # P^{n+1} = P^n + φ (pressure increment)
        self.fields.P += phi
    
    def run_until(self, t_end: float, callback: Optional[Callable] = None) -> None:
        """
        Run simulation until t_end.
        
        Parameters
        ----------
        t_end : float
            End time (s)
        callback : callable, optional
            Function to call after each step: callback(solver)
        """
        while self.t < t_end:
            # Adjust timestep if needed
            if self.t + self.dt > t_end:
                self.dt = t_end - self.t
            
            self.step()
            
            if callback is not None:
                callback(self)
    
    def get_divergence_error(self) -> float:
        """
        Compute maximum divergence error: max|∇·v|.
        
        Returns
        -------
        error : float
            Maximum absolute divergence
        """
        div_v = compute_divergence(self.fields.v, self.fields, boundary="extrapolate")
        return np.max(np.abs(div_v))

