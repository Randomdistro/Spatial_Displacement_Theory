"""
Dodecahedral/RRPT Lattice Discretization

Implements a 12-axis dodecahedral neighbor structure on a regular grid.
Each cell has 12 neighbors corresponding to the 12 faces of a dodecahedron.

The 12 directions are defined by the vertices of an icosahedron (dual of dodecahedron),
which gives uniform angular distribution.
"""

import numpy as np
from typing import Tuple, List, Optional
from .fields import FieldSystem


class DodecahedralLattice:
    """
    12-axis dodecahedral lattice for SDT-Navier discretization.
    
    Each cell has 12 neighbors defined by icosahedral directions.
    """
    
    # 12 directions from icosahedron vertices (normalized)
    # These are the directions to the 12 neighbors
    DIRECTIONS = np.array([
        [0.0, 0.525731, 0.850651],      # 0
        [0.0, -0.525731, 0.850651],     # 1
        [0.0, 0.525731, -0.850651],     # 2
        [0.0, -0.525731, -0.850651],    # 3
        [0.850651, 0.0, 0.525731],      # 4
        [-0.850651, 0.0, 0.525731],     # 5
        [0.850651, 0.0, -0.525731],     # 6
        [-0.850651, 0.0, -0.525731],   # 7
        [0.525731, 0.850651, 0.0],      # 8
        [-0.525731, 0.850651, 0.0],     # 9
        [0.525731, -0.850651, 0.0],     # 10
        [-0.525731, -0.850651, 0.0],    # 11
    ], dtype=np.float64)
    
    def __init__(self, nx: int, ny: int, nz: int, dx: float, dy: Optional[float] = None, dz: Optional[float] = None):
        """
        Initialize dodecahedral lattice.
        
        Parameters
        ----------
        nx, ny, nz : int
            Grid dimensions
        dx, dy, dz : float
            Grid spacing (m). If dy or dz are None, use dx.
        """
        self.nx = nx
        self.ny = ny
        self.nz = nz
        
        if dy is None:
            dy = dx
        if dz is None:
            dz = dx
        
        self.dx = dx
        self.dy = dy
        self.dz = dz
        
        # Normalize directions
        norms = np.linalg.norm(self.DIRECTIONS, axis=1)
        self.DIRECTIONS = self.DIRECTIONS / norms[:, np.newaxis]
        
        # Precompute neighbor offsets in grid coordinates
        # For each direction, find the nearest grid neighbor
        self.neighbor_offsets = []
        for direction in self.DIRECTIONS:
            # Convert direction to grid offsets (rounded to nearest integer)
            di = int(np.round(direction[0] * dx / dx))
            dj = int(np.round(direction[1] * dy / dy))
            dk = int(np.round(direction[2] * dz / dz))
            self.neighbor_offsets.append((di, dj, dk))
    
    def get_neighbor_indices(self, i: int, j: int, k: int) -> List[Tuple[int, int, int]]:
        """
        Get indices of 12 neighbors for cell (i, j, k).
        
        Parameters
        ----------
        i, j, k : int
            Grid indices
        
        Returns
        -------
        neighbors : list
            List of (i', j', k') tuples for 12 neighbors
        """
        neighbors = []
        for di, dj, dk in self.neighbor_offsets:
            ni = i + di
            nj = j + dj
            nk = k + dk
            
            # Check bounds
            if 0 <= ni < self.nx and 0 <= nj < self.ny and 0 <= nk < self.nz:
                neighbors.append((ni, nj, nk))
        
        return neighbors
    
    def get_neighbor_directions(self) -> np.ndarray:
        """
        Get the 12 neighbor direction vectors.
        
        Returns
        -------
        directions : array
            Shape (12, 3) - unit direction vectors
        """
        return self.DIRECTIONS.copy()


def compute_gradient(
    field: np.ndarray,
    fields: FieldSystem,
    boundary: str = "zero",
) -> np.ndarray:
    """
    Compute gradient of a scalar field using central differences.
    
    Parameters
    ----------
    field : array
        Scalar field, shape (nx, ny, nz)
    fields : FieldSystem
        Field system (for grid parameters)
    boundary : str
        Boundary condition: "zero", "periodic", or "extrapolate"
    
    Returns
    -------
    grad : array
        Gradient, shape (nx, ny, nz, 3)
    """
    nx, ny, nz = field.shape
    grad = np.zeros((nx, ny, nz, 3), dtype=field.dtype)
    
    # x-component: ∂/∂x
    if nx > 1:
        # Interior points: central difference
        grad[1:-1, :, :, 0] = (field[2:, :, :] - field[:-2, :, :]) / (2 * fields.dx)
        
        # Boundaries
        if boundary == "zero":
            grad[0, :, :, 0] = 0.0
            grad[-1, :, :, 0] = 0.0
        elif boundary == "extrapolate":
            grad[0, :, :, 0] = (field[1, :, :] - field[0, :, :]) / fields.dx
            grad[-1, :, :, 0] = (field[-1, :, :] - field[-2, :, :]) / fields.dx
        elif boundary == "periodic":
            grad[0, :, :, 0] = (field[1, :, :] - field[-1, :, :]) / (2 * fields.dx)
            grad[-1, :, :, 0] = (field[0, :, :] - field[-2, :, :]) / (2 * fields.dx)
    
    # y-component: ∂/∂y
    if ny > 1:
        grad[:, 1:-1, :, 1] = (field[:, 2:, :] - field[:, :-2, :]) / (2 * fields.dy)
        
        if boundary == "zero":
            grad[:, 0, :, 1] = 0.0
            grad[:, -1, :, 1] = 0.0
        elif boundary == "extrapolate":
            grad[:, 0, :, 1] = (field[:, 1, :] - field[:, 0, :]) / fields.dy
            grad[:, -1, :, 1] = (field[:, -1, :] - field[:, -2, :]) / fields.dy
        elif boundary == "periodic":
            grad[:, 0, :, 1] = (field[:, 1, :] - field[:, -1, :]) / (2 * fields.dy)
            grad[:, -1, :, 1] = (field[:, 0, :] - field[:, -2, :]) / (2 * fields.dy)
    
    # z-component: ∂/∂z
    if nz > 1:
        grad[:, :, 1:-1, 2] = (field[:, :, 2:] - field[:, :, :-2]) / (2 * fields.dz)
        
        if boundary == "zero":
            grad[:, :, 0, 2] = 0.0
            grad[:, :, -1, 2] = 0.0
        elif boundary == "extrapolate":
            grad[:, :, 0, 2] = (field[:, :, 1] - field[:, :, 0]) / fields.dz
            grad[:, :, -1, 2] = (field[:, :, -1] - field[:, :, -2]) / fields.dz
        elif boundary == "periodic":
            grad[:, :, 0, 2] = (field[:, :, 1] - field[:, :, -1]) / (2 * fields.dz)
            grad[:, :, -1, 2] = (field[:, :, 0] - field[:, :, -2]) / (2 * fields.dz)
    
    return grad


def compute_divergence(
    v: np.ndarray,
    fields: FieldSystem,
    boundary: str = "zero",
) -> np.ndarray:
    """
    Compute divergence of a vector field: ∇·v.
    
    Parameters
    ----------
    v : array
        Vector field, shape (nx, ny, nz, 3)
    fields : FieldSystem
        Field system (for grid parameters)
    boundary : str
        Boundary condition: "zero", "periodic", or "extrapolate"
    
    Returns
    -------
    div : array
        Divergence, shape (nx, ny, nz)
    """
    nx, ny, nz = v.shape[:3]
    div = np.zeros((nx, ny, nz), dtype=v.dtype)
    
    # ∂v_x/∂x
    if nx > 1:
        div[1:-1, :, :] += (v[2:, :, :, 0] - v[:-2, :, :, 0]) / (2 * fields.dx)
        
        if boundary == "zero":
            pass  # Already zero
        elif boundary == "extrapolate":
            div[0, :, :] += (v[1, :, :, 0] - v[0, :, :, 0]) / fields.dx
            div[-1, :, :] += (v[-1, :, :, 0] - v[-2, :, :, 0]) / fields.dx
        elif boundary == "periodic":
            div[0, :, :] += (v[1, :, :, 0] - v[-1, :, :, 0]) / (2 * fields.dx)
            div[-1, :, :] += (v[0, :, :, 0] - v[-2, :, :, 0]) / (2 * fields.dx)
    
    # ∂v_y/∂y
    if ny > 1:
        div[:, 1:-1, :] += (v[:, 2:, :, 1] - v[:, :-2, :, 1]) / (2 * fields.dy)
        
        if boundary == "extrapolate":
            div[:, 0, :] += (v[:, 1, :, 1] - v[:, 0, :, 1]) / fields.dy
            div[:, -1, :] += (v[:, -1, :, 1] - v[:, -2, :, 1]) / fields.dy
        elif boundary == "periodic":
            div[:, 0, :] += (v[:, 1, :, 1] - v[:, -1, :, 1]) / (2 * fields.dy)
            div[:, -1, :] += (v[:, 0, :, 1] - v[:, -2, :, 1]) / (2 * fields.dy)
    
    # ∂v_z/∂z
    if nz > 1:
        div[:, :, 1:-1] += (v[:, :, 2:, 2] - v[:, :, :-2, 2]) / (2 * fields.dz)
        
        if boundary == "extrapolate":
            div[:, :, 0] += (v[:, :, 1, 2] - v[:, :, 0, 2]) / fields.dz
            div[:, :, -1] += (v[:, :, -1, 2] - v[:, :, -2, 2]) / fields.dz
        elif boundary == "periodic":
            div[:, :, 0] += (v[:, :, 1, 2] - v[:, :, -1, 2]) / (2 * fields.dz)
            div[:, :, -1] += (v[:, :, 0, 2] - v[:, :, -2, 2]) / (2 * fields.dz)
    
    return div


def compute_velocity_gradient(
    v: np.ndarray,
    fields: FieldSystem,
    boundary: str = "zero",
) -> np.ndarray:
    """
    Compute velocity gradient tensor: ∇v (shape (nx, ny, nz, 3, 3)).
    
    grad_v[i,j,k,a,b] = ∂v_a/∂x_b
    
    Parameters
    ----------
    v : array
        Velocity field, shape (nx, ny, nz, 3)
    fields : FieldSystem
        Field system (for grid parameters)
    boundary : str
        Boundary condition
    
    Returns
    -------
    grad_v : array
        Velocity gradient tensor, shape (nx, ny, nz, 3, 3)
    """
    nx, ny, nz = v.shape[:3]
    grad_v = np.zeros((nx, ny, nz, 3, 3), dtype=v.dtype)
    
    # For each component of velocity
    for a in range(3):
        grad_scalar = compute_gradient(v[:, :, :, a], fields, boundary=boundary)
        grad_v[:, :, :, a, :] = grad_scalar
    
    return grad_v


def compute_advection(
    field: np.ndarray,
    v: np.ndarray,
    fields: FieldSystem,
    method: str = "upwind",
) -> np.ndarray:
    """
    Compute advection term: (v·∇)field
    
    Parameters
    ----------
    field : array
        Scalar field to advect, shape (nx, ny, nz)
    v : array
        Velocity field, shape (nx, ny, nz, 3)
    fields : FieldSystem
        Field system (for grid parameters)
    method : str
        Advection method: "upwind" or "central"
    
    Returns
    -------
    advection : array
        Advection term, shape (nx, ny, nz)
    """
    if method == "upwind":
        # Upwind differencing (first-order, stable)
        advection = np.zeros_like(field)
        
        # x-direction
        if fields.nx > 1:
            # Forward difference where v_x < 0, backward where v_x > 0
            vx_pos = v[:, :, :, 0] > 0
            vx_neg = v[:, :, :, 0] < 0
            
            # Interior
            backward = np.zeros_like(field)
            forward = np.zeros_like(field)
            backward[1:, :, :] = (field[1:, :, :] - field[:-1, :, :]) / fields.dx
            forward[:-1, :, :] = (field[1:, :, :] - field[:-1, :, :]) / fields.dx
            
            advection += np.where(vx_pos, backward, 0) * v[:, :, :, 0]
            advection += np.where(vx_neg, forward, 0) * v[:, :, :, 0]
        
        # y-direction
        if fields.ny > 1:
            vy_pos = v[:, :, :, 1] > 0
            vy_neg = v[:, :, :, 1] < 0
            
            backward = np.zeros_like(field)
            forward = np.zeros_like(field)
            backward[:, 1:, :] = (field[:, 1:, :] - field[:, :-1, :]) / fields.dy
            forward[:, :-1, :] = (field[:, 1:, :] - field[:, :-1, :]) / fields.dy
            
            advection += np.where(vy_pos, backward, 0) * v[:, :, :, 1]
            advection += np.where(vy_neg, forward, 0) * v[:, :, :, 1]
        
        # z-direction
        if fields.nz > 1:
            vz_pos = v[:, :, :, 2] > 0
            vz_neg = v[:, :, :, 2] < 0
            
            backward = np.zeros_like(field)
            forward = np.zeros_like(field)
            backward[:, :, 1:] = (field[:, :, 1:] - field[:, :, :-1]) / fields.dz
            forward[:, :, :-1] = (field[:, :, 1:] - field[:, :, :-1]) / fields.dz
            
            advection += np.where(vz_pos, backward, 0) * v[:, :, :, 2]
            advection += np.where(vz_neg, forward, 0) * v[:, :, :, 2]
        
        return advection
    
    elif method == "central":
        # Central differencing (second-order, but can be unstable)
        grad = compute_gradient(field, fields, boundary="extrapolate")
        return (
            v[:, :, :, 0] * grad[:, :, :, 0] +
            v[:, :, :, 1] * grad[:, :, :, 1] +
            v[:, :, :, 2] * grad[:, :, :, 2]
        )
    
    else:
        raise ValueError(f"Unknown advection method: {method}")

