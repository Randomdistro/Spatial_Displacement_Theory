"""
Minimal Poisson solver for SDT electricity investigations
--------------------------------------------------------

Purpose:
  Provide a concrete numerical backbone for prompt Part 10:
    ∇²Φ = -ρ_q/ε0,  E = -∇Φ,  u = (1/2) ε0 |E|²

Notes:
  - This is intentionally minimal and deterministic (no external deps beyond numpy).
  - It is not intended to be "fast"; it's intended to be correct enough for
    small-grid sanity checks and for building intuition.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


EPS0 = 8.854_187_812_8e-12  # F/m

# NOTE: Keep output ASCII-only (Windows console compatibility).


@dataclass
class PoissonResult:
    phi: np.ndarray
    E: np.ndarray
    iterations: int
    max_delta: float


def solve_poisson_dirichlet(
    rho_q: np.ndarray,
    *,
    dx: float,
    epsilon0: float = EPS0,
    max_iter: int = 50_000,
    tol: float = 1e-7,
    omega: float = 1.8,
) -> PoissonResult:
    """
    Solve ∇²φ = -ρ_q/ε0 on a cubic grid with Dirichlet boundary φ=0 on all faces.

    Uses successive over-relaxation (SOR) Gauss-Seidel.
    """
    if rho_q.ndim != 3:
        raise ValueError("rho_q must be a 3D array (nx, ny, nz).")
    if dx <= 0:
        raise ValueError("dx must be positive.")
    if epsilon0 <= 0:
        raise ValueError("epsilon0 must be positive.")
    if not (0.0 < omega < 2.0):
        raise ValueError("omega must be in (0, 2) for SOR stability.")

    nx, ny, nz = rho_q.shape
    phi = np.zeros_like(rho_q, dtype=float)
    rhs = -rho_q / epsilon0

    inv6 = 1.0 / 6.0
    dx2 = dx * dx

    max_delta = float("inf")
    it = 0
    for it in range(1, max_iter + 1):
        max_delta = 0.0
        # Interior points only; boundaries are fixed at 0
        for i in range(1, nx - 1):
            for j in range(1, ny - 1):
                for k in range(1, nz - 1):
                    phi_new = inv6 * (
                        phi[i + 1, j, k]
                        + phi[i - 1, j, k]
                        + phi[i, j + 1, k]
                        + phi[i, j - 1, k]
                        + phi[i, j, k + 1]
                        + phi[i, j, k - 1]
                        - dx2 * rhs[i, j, k]
                    )
                    # SOR update
                    updated = (1.0 - omega) * phi[i, j, k] + omega * phi_new
                    delta = abs(updated - phi[i, j, k])
                    if delta > max_delta:
                        max_delta = delta
                    phi[i, j, k] = updated

        if max_delta < tol:
            break

    # Electric field E = -∇φ (central differences)
    E = np.zeros((nx, ny, nz, 3), dtype=float)
    E[1:-1, :, :, 0] = -(phi[2:, :, :] - phi[:-2, :, :]) / (2.0 * dx)
    E[:, 1:-1, :, 1] = -(phi[:, 2:, :] - phi[:, :-2, :]) / (2.0 * dx)
    E[:, :, 1:-1, 2] = -(phi[:, :, 2:] - phi[:, :, :-2]) / (2.0 * dx)

    return PoissonResult(phi=phi, E=E, iterations=it, max_delta=float(max_delta))


def point_charge_density(
    *,
    nx: int,
    dx: float,
    q_coulomb: float,
) -> np.ndarray:
    """
    Place a single point charge at the center cell as a discrete delta:
      ρ_q(center) = q / dx^3
    """
    if nx < 5:
        raise ValueError("nx must be >= 5.")
    rho = np.zeros((nx, nx, nx), dtype=float)
    c = nx // 2
    rho[c, c, c] = q_coulomb / (dx**3)
    return rho


def radial_profile_along_x(phi: np.ndarray, dx: float) -> list[tuple[float, float]]:
    """
    Sample φ along +x axis from the center and return (r, φ).
    """
    nx = phi.shape[0]
    c = nx // 2
    out: list[tuple[float, float]] = []
    for i in range(c + 1, nx - 1):
        r = (i - c) * dx
        out.append((r, float(phi[i, c, c])))
    return out


def main() -> None:
    print("START: running Poisson solver example")
    # A small sanity check: φ(r) should be ~ 1/r away from boundaries.
    # Keep this small so it runs quickly in lightweight environments.
    nx = 21
    dx = 0.05  # meters (arbitrary for shape checks)
    q = 1e-9  # C (arbitrary)

    rho = point_charge_density(nx=nx, dx=dx, q_coulomb=q)
    result = solve_poisson_dirichlet(rho, dx=dx, max_iter=4_000, tol=1e-6, omega=1.7)

    prof = radial_profile_along_x(result.phi, dx)
    # Compare φ(r)*r to a constant (should be roughly flat in the interior).
    values = [(r, phi * r) for (r, phi) in prof if r > 0]
    mid = values[len(values) // 2 : len(values) // 2 + 5]

    print("Poisson solver sanity check (Dirichlet box):")
    print(f"  iterations={result.iterations}, max_delta={result.max_delta:.3e}")
    print("  sample of r and (phi*r) (should be ~constant away from boundaries):")
    for r, phr in mid:
        print(f"    r={r:.3e} m, phi*r={phr:.6e} V*m (up to scaling)")

    # Energy density sanity check at a point away from center
    i = nx // 2 + 5
    c = nx // 2
    E_mag = float(np.linalg.norm(result.E[i, c, c, :]))
    u = 0.5 * EPS0 * E_mag**2
    print(f"  |E|(r~{(i-c)*dx:.3e} m) = {E_mag:.3e} V/m -> u~{u:.3e} J/m^3")


def visualize_atmospheric_field(
    antenna_height: float = 10.0,
    field_strength: float = 130.0,
    grid_size: int = 51,
    domain_size: float = 20.0
) -> None:
    """
    Visualize atmospheric electric field around vertical antenna.
    
    Creates 2D slice visualization of potential and field lines.
    """
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
    except ImportError:
        print("Matplotlib not available - skipping visualization")
        return
    
    dx = domain_size / (grid_size - 1)
    
    # Create charge distribution (vertical line charge representing antenna)
    rho = np.zeros((grid_size, grid_size, grid_size), dtype=float)
    center_x, center_y = grid_size // 2, grid_size // 2
    
    # Vertical line charge (simplified - point charges along z-axis)
    for k in range(grid_size // 4, 3 * grid_size // 4):
        # Approximate line charge density
        q_per_cell = field_strength * dx / (EPS0 * antenna_height)
        rho[center_x, center_y, k] = q_per_cell / (dx**3)
    
    # Solve Poisson equation
    print(f"Solving Poisson equation for atmospheric field (grid: {grid_size}^3)...")
    result = solve_poisson_dirichlet(rho, dx=dx, max_iter=5000, tol=1e-5)
    
    # Extract 2D slice (x-z plane at y=center)
    slice_idx = grid_size // 2
    phi_slice = result.phi[:, slice_idx, :]
    E_slice = result.E[:, slice_idx, :, [0, 2]]  # Ex and Ez components
    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Potential
    x = np.linspace(-domain_size/2, domain_size/2, grid_size)
    z = np.linspace(0, domain_size, grid_size)
    X, Z = np.meshgrid(x, z, indexing='ij')
    
    im1 = ax1.contourf(X, Z, phi_slice, levels=20, cmap='viridis')
    ax1.contour(X, Z, phi_slice, levels=20, colors='black', alpha=0.3, linewidths=0.5)
    ax1.set_xlabel('X (m)', fontsize=12)
    ax1.set_ylabel('Z (m)', fontsize=12)
    ax1.set_title('Electric Potential (Atmospheric Field)', fontsize=14)
    ax1.set_aspect('equal')
    plt.colorbar(im1, ax=ax1, label='Potential (V)')
    
    # Plot 2: Electric Field
    # Sample field vectors (every 3rd point for clarity)
    step = 3
    X_sample = X[::step, ::step]
    Z_sample = Z[::step, ::step]
    Ex_sample = E_slice[::step, ::step, 0]
    Ez_sample = E_slice[::step, ::step, 1]
    
    im2 = ax2.contourf(X, Z, np.sqrt(E_slice[:, :, 0]**2 + E_slice[:, :, 1]**2), 
                       levels=20, cmap='plasma')
    ax2.quiver(X_sample, Z_sample, Ex_sample, Ez_sample, 
              scale=1e3, width=0.003, color='white', alpha=0.7)
    ax2.set_xlabel('X (m)', fontsize=12)
    ax2.set_ylabel('Z (m)', fontsize=12)
    ax2.set_title('Electric Field (Atmospheric Field)', fontsize=14)
    ax2.set_aspect('equal')
    plt.colorbar(im2, ax=ax2, label='|E| (V/m)')
    
    plt.tight_layout()
    plt.savefig('SDT/investigations/atmospheric_field_visualization.png', dpi=150)
    print("Atmospheric field visualization saved to SDT/investigations/atmospheric_field_visualization.png")
    plt.close()


def visualize_telluric_field(
    electrode_separation: float = 10.0,
    voltage_gradient: float = 1e-5,
    grid_size: int = 51,
    domain_size: float = 20.0
) -> None:
    """
    Visualize telluric electric field between two electrodes.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib not available - skipping visualization")
        return
    
    dx = domain_size / (grid_size - 1)
    
    # Create charge distribution (two point charges representing electrodes)
    rho = np.zeros((grid_size, grid_size, grid_size), dtype=float)
    center_x, center_y, center_z = grid_size // 2, grid_size // 2, grid_size // 2
    
    # Two electrodes separated along x-axis
    sep_cells = int(electrode_separation / dx)
    electrode1_x = center_x - sep_cells // 2
    electrode2_x = center_x + sep_cells // 2
    
    # Approximate charge densities to create voltage gradient
    q1 = voltage_gradient * electrode_separation * EPS0 * dx**2
    q2 = -q1
    
    rho[electrode1_x, center_y, center_z] = q1 / (dx**3)
    rho[electrode2_x, center_y, center_z] = q2 / (dx**3)
    
    # Solve Poisson equation
    print(f"Solving Poisson equation for telluric field (grid: {grid_size}^3)...")
    result = solve_poisson_dirichlet(rho, dx=dx, max_iter=5000, tol=1e-5)
    
    # Extract 2D slice (x-y plane at z=center)
    slice_idx = grid_size // 2
    phi_slice = result.phi[:, :, slice_idx]
    E_slice = result.E[:, :, slice_idx, [0, 1]]  # Ex and Ey components
    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    x = np.linspace(-domain_size/2, domain_size/2, grid_size)
    y = np.linspace(-domain_size/2, domain_size/2, grid_size)
    X, Y = np.meshgrid(x, y, indexing='ij')
    
    # Plot 1: Potential
    im1 = ax1.contourf(X, Y, phi_slice, levels=20, cmap='coolwarm')
    ax1.contour(X, Y, phi_slice, levels=20, colors='black', alpha=0.3, linewidths=0.5)
    ax1.set_xlabel('X (m)', fontsize=12)
    ax1.set_ylabel('Y (m)', fontsize=12)
    ax1.set_title('Electric Potential (Telluric Field)', fontsize=14)
    ax1.set_aspect('equal')
    plt.colorbar(im1, ax=ax1, label='Potential (V)')
    
    # Plot 2: Electric Field
    step = 3
    X_sample = X[::step, ::step]
    Y_sample = Y[::step, ::step]
    Ex_sample = E_slice[::step, ::step, 0]
    Ey_sample = E_slice[::step, ::step, 1]
    
    im2 = ax2.contourf(X, Y, np.sqrt(E_slice[:, :, 0]**2 + E_slice[:, :, 1]**2),
                       levels=20, cmap='plasma')
    ax2.quiver(X_sample, Y_sample, Ex_sample, Ey_sample,
              scale=1e2, width=0.003, color='white', alpha=0.7)
    ax2.set_xlabel('X (m)', fontsize=12)
    ax2.set_ylabel('Y (m)', fontsize=12)
    ax2.set_title('Electric Field (Telluric Field)', fontsize=14)
    ax2.set_aspect('equal')
    plt.colorbar(im2, ax=ax2, label='|E| (V/m)')
    
    plt.tight_layout()
    plt.savefig('SDT/investigations/telluric_field_visualization.png', dpi=150)
    print("Telluric field visualization saved to SDT/investigations/telluric_field_visualization.png")
    plt.close()


if __name__ == "__main__":
    main()
    
    # Generate visualizations if matplotlib is available
    print("\nGenerating field visualizations...")
    try:
        visualize_atmospheric_field()
        visualize_telluric_field()
    except Exception as e:
        print(f"Visualization skipped: {e}")


