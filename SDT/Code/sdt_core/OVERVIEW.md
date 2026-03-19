# sdt_core — Overview

Python core SDT library. Defines fundamental constants, physics equations, the 28-dimensional state vector, and orbital mechanics examples. Contains validation tests for the zk²=1 invariant.

## Subfolders

- (none)

## Files

- **__init__.py** — Package initialisation and public API exports
- **constants.py** — ✅ SDT physical constants (c, ħ, α, P_CMB, spation properties, unit conversions)
- **physics.py** — ✅ Core SDT physics functions: pressure field, orbital velocity, c-boundary radius, effective temperature
- **state_28d.py** — ✅ Python implementation of the 28-dimensional state vector on spherical basis (r, θ, φ)
- **example_jupiter_earth.py** — ✅ Jupiter-Earth orbital comparison using SDT k-factor methodology
- **example_real_usage.py** — ✅ Real-world usage examples with measured data
- **solve_three_body.py** — ✅ Three-body problem solver using SDT pressure-field dynamics
- **test_28d_proper.py** — ✅ Tests for 28D state vector construction and invariants
- **test_zk2_invariant.py** — ✅ Tests confirming zk²=1 universal relation
- **test_stress_regime.py** — ✅ Tests for stress regime transitions in pressure field
- **sdt_three_body_solution.png** — Three-body solution visualisation output
- **three_body_solution.png** — Alternative three-body solution visualisation
