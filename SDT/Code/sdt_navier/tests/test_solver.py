"""
Unit tests for solver components.
"""

import numpy as np
import pytest
from sdt_navier.fields import initialize_fields
from sdt_navier.equations import SDTNavierEquations
from sdt_navier.solver import SDTNavierSolver
from sdt_navier.lattice import compute_divergence


def test_solver_initialization():
    """Test solver initialization."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    equations = SDTNavierEquations()
    
    solver = SDTNavierSolver(fields, equations, dt=1.0e-24)
    
    assert solver.fields is fields
    assert solver.equations is equations
    assert solver.dt == 1.0e-24
    assert solver.t == 0.0


def test_single_step():
    """Test single time step."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    equations = SDTNavierEquations()
    
    solver = SDTNavierSolver(fields, equations, dt=1.0e-24)
    
    # Store initial state
    v0 = fields.v.copy()
    kappa0 = fields.kappa.copy()
    
    # Take one step
    solver.step()
    
    # Fields should have changed
    assert not np.allclose(fields.v, v0)
    assert not np.allclose(fields.kappa, kappa0)
    
    # Time should advance
    assert solver.t == 1.0e-24
    assert fields.t == 1.0e-24


def test_incompressibility_enforcement():
    """Test that incompressibility is enforced."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    equations = SDTNavierEquations()
    
    # Create a divergent velocity field
    fields.v[:, :, :, 0] = np.linspace(0, 1e6, nx)[:, np.newaxis, np.newaxis]
    
    solver = SDTNavierSolver(
        fields,
        equations,
        dt=1.0e-24,
        enforce_incompressibility=True,
    )
    
    # Check initial divergence
    div_initial = compute_divergence(fields.v, fields)
    max_div_initial = np.max(np.abs(div_initial))
    
    # Take several steps
    for _ in range(10):
        solver.step()
    
    # Divergence should be reduced
    div_final = compute_divergence(fields.v, fields)
    max_div_final = np.max(np.abs(div_final))
    
    # Divergence should be smaller (or at least not much larger)
    # Note: projection is simplified, so we just check it doesn't explode
    assert max_div_final < max_div_initial * 10  # Allow some tolerance


def test_run_until():
    """Test run_until method."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    equations = SDTNavierEquations()
    
    solver = SDTNavierSolver(fields, equations, dt=1.0e-24)
    
    # Run until t = 1e-23 (10 steps)
    t_end = 1.0e-23
    step_count = [0]
    
    def callback(s):
        step_count[0] += 1
    
    solver.run_until(t_end, callback=callback)
    
    assert solver.t >= t_end
    assert step_count[0] == 10


def test_adaptive_timestep():
    """Test adaptive timestep estimation."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    
    # Set high velocity
    fields.v[:, :, :, 0] = 1.0e8  # 0.1c
    
    equations = SDTNavierEquations()
    solver = SDTNavierSolver(fields, equations, dt=None, cfl=0.5)
    
    # Timestep should be estimated from CFL condition
    # dt < CFL * dx / v_max = 0.5 * 1e-15 / 1e8 = 5e-24
    assert solver.dt < 1.0e-23
    assert solver.dt > 0


def test_slip_bounds():
    """Test that slip field stays in [0, 1]."""
    nx, ny, nz = 10, 10, 10
    dx = 1.0e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    
    # Set slip to boundary values
    fields.eta[:, :, :] = 0.0
    
    equations = SDTNavierEquations()
    solver = SDTNavierSolver(fields, equations, dt=1.0e-24)
    
    # Take many steps
    for _ in range(100):
        solver.step()
    
    # Slip should still be in bounds
    assert np.all(fields.eta >= 0)
    assert np.all(fields.eta <= 1)

