"""
Unit tests for field definitions and initialization.
"""

import numpy as np
import pytest
from sdt_navier.fields import FieldSystem, initialize_fields, add_turbine_source, compute_diversion_density


def test_field_initialization():
    """Test field system initialization."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15  # 1 fm
    
    fields = initialize_fields(nx, ny, nz, dx)
    
    assert fields.nx == nx
    assert fields.ny == ny
    assert fields.nz == nz
    assert fields.dx == dx
    assert fields.dy == dx
    assert fields.dz == dx
    
    # Check field shapes
    assert fields.P.shape == (nx, ny, nz)
    assert fields.kappa.shape == (nx, ny, nz)
    assert fields.eta.shape == (nx, ny, nz)
    assert fields.e.shape == (nx, ny, nz)
    assert fields.Gamma.shape == (nx, ny, nz)
    assert fields.v.shape == (nx, ny, nz, 3)
    
    # Check initial values
    assert np.all(fields.P > 0)  # Pressure should be positive
    assert np.all(fields.eta >= 0) and np.all(fields.eta <= 1)  # Slip in [0, 1]
    assert np.all(fields.Gamma > 0)  # Circulation should be positive


def test_field_validation():
    """Test field validation (slip bounds)."""
    nx, ny, nz = 5, 5, 5
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    
    # Should pass validation
    assert fields.eta.min() >= 0
    assert fields.eta.max() <= 1
    
    # Try to create invalid field (should raise error)
    fields.eta[0, 0, 0] = 1.5
    with pytest.raises(ValueError, match="Slip field"):
        fields.__post_init__()


def test_turbine_source():
    """Test adding turbine source to fields."""
    nx, ny, nz = 20, 20, 20
    dx = 0.5e-15  # 0.5 fm
    
    fields = initialize_fields(nx, ny, nz, dx)
    
    # Add proton turbine at center
    center = (nx // 2, ny // 2, nz // 2)
    radius_cells = 2.0
    kappa_value = 1.19e15  # m⁻¹
    Gamma_value = 0.546
    eta_value = 0.0003
    
    add_turbine_source(
        fields,
        center,
        radius_cells,
        kappa_value,
        Gamma_value,
        eta_value,
        profile="gaussian",
    )
    
    # Check that curvature is increased at center
    i, j, k = center
    assert fields.kappa[i, j, k] > 0
    
    # Check that slip is decreased at center
    assert fields.eta[i, j, k] < 0.01  # Should be small


def test_diversion_density():
    """Test diversion density calculation."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    
    # Set test values
    fields.Gamma[:, :, :] = 0.5
    fields.kappa[:, :, :] = 1.0e15
    fields.eta[:, :, :] = 0.1
    
    sigma = compute_diversion_density(fields)
    
    # σ = Γ κ (1-η) = 0.5 * 1e15 * 0.9 = 4.5e14
    expected = 0.5 * 1.0e15 * 0.9
    assert np.allclose(sigma, expected, rtol=1e-10)


def test_custom_initial_conditions():
    """Test initialization with custom initial conditions."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    # Custom initial velocity
    v0 = np.zeros((nx, ny, nz, 3))
    v0[:, :, :, 0] = 1.0e6  # 1e6 m/s in x-direction
    
    # Custom initial curvature
    kappa0 = np.ones((nx, ny, nz)) * 1.0e15
    
    fields = initialize_fields(
        nx, ny, nz, dx,
        initial_velocity=v0,
        initial_kappa=kappa0,
    )
    
    assert np.allclose(fields.v[:, :, :, 0], 1.0e6)
    assert np.allclose(fields.kappa, 1.0e15)

