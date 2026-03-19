# sdt_navier_cpp — Overview

C++20 implementation of SDT Navier field equations, nuclear geometry, and the complete benchmark validation suite (B01–B100). This is the largest and most comprehensive computational module in the SDT codebase.

## Subfolders

- **include/** — Public headers: stellar/atomic/galactic calculators, nuclear geometry models, state_28d manifold, and core Navier equation declarations
- **include/sdt_navier/** — Internal headers: field equation types, lattice structures, solver interfaces, operator algebra, physical constants, and nuclear turbine models
- **src/** — Implementation of core Navier field equations, lattice construction, solver, operator algebra, nuclear binding, and magnetic moment analysis
- **tools/** — Standalone executables: 100 certified benchmarks (B25–B100), calculator CLIs, galactic rotation curve generator, lk² validation, zk² systematic analysis
- **tests/** — Unit tests for all calculators, field equations, Navier core, nuclear geometry, operators, and solver convergence
- **examples/** — Example programs demonstrating force hierarchy calculations and Python bindings
- **python/** — Python bindings (CMakeLists.txt)
- **build/** — Build output directory (generated)

## Files

- **CMakeLists.txt** — Master CMake build configuration for the module
- **README.md** — Module documentation and usage guide
- **API.md** — Public API reference for all calculators and the Navier core
- **BUILD.md** — Build instructions and dependency information
- **CHANGELOG.md** — Version history and change log
- **CONTRIBUTING.md** — Contribution guidelines
- **LICENSE** — License file
- **LK2_IMPLEMENTATION.md** — Documentation of the L·k² = constant galactic relation implementation
- **NUCLEAR_CALCULATOR_README.md** — Nuclear binding energy calculator documentation (trefoil neutrino model)
- **QUICK_REFERENCE.md** — Quick reference card for SDT equations and constants
- **SDT_TEXTBOOK_INTEGRATION.md** — Integration notes with SDT textbook material
