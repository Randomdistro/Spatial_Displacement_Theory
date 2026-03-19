# sdt_navier/tests — Overview

Python unit tests for the SDT Navier field implementation.

## Files

- **__init__.py** — Test package initialisation
- **test_fields.py** — ✅ Tests for field construction, TurbineCell models, and pressure field values
- **test_integration.py** — ✅ Integration tests for full solver pipeline: lattice → initialisation → solve → validate
- **test_operators.py** — ✅ Tests for differential operators (gradient, divergence, curl) on lattice
- **test_solver.py** — ✅ Tests for solver convergence, stability, and conservation
