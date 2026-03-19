# sdt_atomic_sim — Overview

🔴 **QUARANTINE CANDIDATE** — C++20 atomic orbital simulation. Currently implements textbook quantum mechanical wave functions, probability densities, and Laguerre polynomials. This is fundamentally incompatible with SDT, which models electrons as toroidal vortices at pressure-node minima of the nuclear displacement field.

## Subfolders

- **include/** — Header tree: core types/constants, physics (electron orbitals, spectral transitions), simulation engine, visualisation (orbital viewer), I/O (data loader)
- **src/** — Implementations: electron orbital wave functions (QM), spectral transitions, atomic engine, orbital viewer, data loader
- **tools/** — Atomic viewer CLI tool

## Files

- **CMakeLists.txt** — Build configuration
- **README.md** — Module documentation
- **BUILD.md** — Build instructions (requires Eigen)
- **SIMULATION_DESIGN.md** — Simulation architecture design document
- **VISUALIZATION_GUIDE.md** — Guide for orbital visualisation modes
- **main.cpp** — 🔴 Entry point: calls `probability_density()` on QM orbital objects
