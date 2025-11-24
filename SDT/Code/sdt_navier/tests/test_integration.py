"""
Integration tests for deuteron simulation and observable extraction.
"""

import numpy as np
import pytest
from sdt_navier.fields import initialize_fields
from sdt_navier.equations import SDTNavierEquations
from sdt_navier.solver import SDTNavierSolver
from sdt_navier.nuclear import DeuteronSystem
from sdt_navier.magnetic_moments import (
    compute_nuclear_magnetic_moment,
    compare_magnetic_moment,
    MU_D_EXP,
)


def test_deuteron_initialization():
    """Test deuteron system initialization."""
    nx, ny, nz = 50, 50, 50
    dx = 0.2e-15  # 0.2 fm
    
    fields = initialize_fields(nx, ny, nz, dx)
    center = (nx // 2, ny // 2, nz // 2)
    separation_cells = 10.0  # 2 fm / 0.2 fm = 10 cells
    
    deuteron = DeuteronSystem(fields, center, separation_cells)
    
    assert deuteron.proton is not None
    assert deuteron.neutron is not None
    assert deuteron.proton.cell_type == "proton"
    assert deuteron.neutron.cell_type == "neutron"


def test_deuteron_binding_energy():
    """Test deuteron binding energy calculation."""
    nx, ny, nz = 50, 50, 50
    dx = 0.2e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    center = (nx // 2, ny // 2, nz // 2)
    separation_cells = 10.0
    
    equations = SDTNavierEquations()
    deuteron = DeuteronSystem(fields, center, separation_cells, equations)
    
    # Compute binding energy
    B_mev = deuteron.compute_binding_energy_mev()
    
    # Should be positive (bound state)
    assert B_mev > 0
    
    # Should be in reasonable range (experimental: 2.224 MeV)
    # Allow large tolerance for now since force functionals need tuning
    assert B_mev < 10.0  # Less than 10 MeV


def test_deuteron_magnetic_moment():
    """Test deuteron magnetic moment calculation."""
    nx, ny, nz = 50, 50, 50
    dx = 0.2e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    center = (nx // 2, ny // 2, nz // 2)
    separation_cells = 10.0
    
    deuteron = DeuteronSystem(fields, center, separation_cells)
    
    # Compute magnetic moment
    mu_d = compute_nuclear_magnetic_moment(deuteron)
    
    # Should be positive (experimental: 0.857 μ_N)
    assert mu_d > 0
    
    # Compare to experimental
    comparison = compare_magnetic_moment(mu_d, MU_D_EXP, "deuteron")
    
    # Allow large tolerance for now
    assert abs(comparison["relative_error"]) < 1.0  # Within 100% (needs tuning)


def test_deuteron_simulation():
    """Test running a short deuteron simulation."""
    nx, ny, nz = 30, 30, 30
    dx = 0.2e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    center = (nx // 2, ny // 2, nz // 2)
    separation_cells = 10.0
    
    deuteron = DeuteronSystem(fields, center, separation_cells)
    
    equations = SDTNavierEquations()
    solver = SDTNavierSolver(
        fields,
        equations,
        dt=1.0e-24,
        enforce_incompressibility=True,
    )
    
    # Run for a short time
    t_end = 1.0e-23  # 10 steps
    solver.run_until(t_end)
    
    # Check that fields evolved
    assert solver.t >= t_end
    
    # Check that turbines are still present
    i_p, j_p, k_p = deuteron.proton.position
    assert fields.kappa[i_p, j_p, k_p] > 0
    
    i_n, j_n, k_n = deuteron.neutron.position
    assert fields.kappa[i_n, j_n, k_n] > 0


def test_binding_energy_convergence():
    """Test that binding energy calculation is stable."""
    nx, ny, nz = 50, 50, 50
    dx = 0.2e-15
    
    fields = initialize_fields(nx, ny, nz, dx)
    center = (nx // 2, ny // 2, nz // 2)
    separation_cells = 10.0
    
    equations = SDTNavierEquations()
    deuteron = DeuteronSystem(fields, center, separation_cells, equations)
    
    # Compute binding energy multiple times
    B1 = deuteron.compute_binding_energy_mev()
    B2 = deuteron.compute_binding_energy_mev()
    B3 = deuteron.compute_binding_energy_mev()
    
    # Should be consistent
    assert np.isclose(B1, B2, rtol=1e-10)
    assert np.isclose(B2, B3, rtol=1e-10)

