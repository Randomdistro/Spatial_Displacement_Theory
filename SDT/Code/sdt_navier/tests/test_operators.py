"""
Unit tests for discrete operators (gradient, divergence, advection).
"""

import numpy as np
import pytest
from sdt_navier.fields import initialize_fields
from sdt_navier.lattice import compute_gradient, compute_divergence, compute_advection, DodecahedralLattice


def test_gradient_linear():
    """Test gradient on linear field."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    
    # Linear field: f(x) = x
    x = np.arange(nx) * dx
    field = x[:, np.newaxis, np.newaxis]
    
    grad = compute_gradient(field, fields, boundary="extrapolate")
    
    # Gradient should be [1, 0, 0] everywhere (except boundaries)
    assert np.allclose(grad[1:-1, :, :, 0], 1.0, rtol=1e-10)
    assert np.allclose(grad[1:-1, :, :, 1], 0.0, rtol=1e-10)
    assert np.allclose(grad[1:-1, :, :, 2], 0.0, rtol=1e-10)


def test_divergence_constant():
    """Test divergence of constant vector field."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    
    # Constant velocity
    fields.v[:, :, :, :] = [1.0e6, 2.0e6, 3.0e6]
    
    div = compute_divergence(fields.v, fields, boundary="zero")
    
    # Divergence of constant field should be zero (except at boundaries)
    assert np.allclose(div[1:-1, 1:-1, 1:-1], 0.0, atol=1e-10)


def test_divergence_linear():
    """Test divergence of linear velocity field."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    
    # Linear velocity: v_x = x
    x = np.arange(nx) * dx
    fields.v[:, :, :, 0] = x[:, np.newaxis, np.newaxis]
    fields.v[:, :, :, 1] = 0.0
    fields.v[:, :, :, 2] = 0.0
    
    div = compute_divergence(fields.v, fields, boundary="extrapolate")
    
    # Divergence should be 1.0 (∂v_x/∂x = 1)
    assert np.allclose(div[1:-1, :, :], 1.0, rtol=1e-10)


def test_advection_constant():
    """Test advection of constant field."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    
    # Constant field
    field = np.ones((nx, ny, nz))
    
    # Constant velocity
    fields.v[:, :, :, :] = [1.0e6, 0.0, 0.0]
    
    adv = compute_advection(field, fields.v, fields, method="upwind")
    
    # Advection of constant field should be zero
    assert np.allclose(adv, 0.0, atol=1e-10)


def test_dodecahedral_lattice():
    """Test dodecahedral lattice structure."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    lattice = DodecahedralLattice(nx, ny, nz, dx)
    
    # Check that we have 12 directions
    assert len(lattice.DIRECTIONS) == 12
    assert len(lattice.neighbor_offsets) == 12
    
    # Check that directions are normalized
    for direction in lattice.DIRECTIONS:
        norm = np.linalg.norm(direction)
        assert np.isclose(norm, 1.0, rtol=1e-10)
    
    # Check neighbor lookup
    neighbors = lattice.get_neighbor_indices(5, 5, 5)
    assert len(neighbors) <= 12  # May be fewer at boundaries


def test_gradient_quadratic():
    """Test gradient on quadratic field."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    
    # Quadratic field: f(x) = x²
    x = np.arange(nx) * dx
    field = (x**2)[:, np.newaxis, np.newaxis]
    
    grad = compute_gradient(field, fields, boundary="extrapolate")
    
    # Gradient should be approximately 2x (except at boundaries)
    x_interior = x[1:-1]
    expected_grad = 2 * x_interior
    assert np.allclose(grad[1:-1, 0, 0, 0], expected_grad, rtol=0.1)  # Allow some error for finite difference

