# sdt_navier_cpp/tests — Overview

Unit tests for the SDT Navier computational engine. Uses custom assertion macros.

## Files

- **CMakeLists.txt** — Build configuration for test executables
- **test_calculators.cpp** — 🟡 Tests for stellar, atomic, and galactic calculators. Contains `m_earth` mass-as-input, Schwarzschild/2 assertions, dark matter halo velocity test — needs purification
- **test_fields.cpp** — ✅ Tests for SDT field construction and initialisation
- **test_navier_core.cpp** — ✅ Tests for core Navier lattice construction, solver convergence, and operator consistency
- **test_nuclear.cpp** — ✅ Tests for nuclear geometry, binding energy predictions, and validation
- **test_operators.cpp** — ✅ Tests for differential operator algebra (gradient, divergence, curl)
- **test_solver.cpp** — ✅ Tests for solver convergence and stability
