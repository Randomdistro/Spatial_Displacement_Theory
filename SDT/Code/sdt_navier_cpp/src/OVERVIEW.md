# sdt_navier_cpp/src — Overview

Implementation of the core SDT Navier field equations, lattice construction, solver, operator algebra, nuclear binding calculations, and magnetic moment analysis.

## Files

- **equations.cpp** — ✅ SDT Navier field equation implementations: pressure gradient computation, vorticity evolution, continuity enforcement
- **fields.cpp** — ✅ Field initialisation and TurbineCell construction for proton, neutron, and electron vortex models
- **lattice.cpp** — ✅ Lattice construction and adjacency for numerical simulations
- **solver.cpp** — ✅ Iterative solver for converging field equations to steady state
- **operators.cpp** — ✅ Differential operator implementations (gradient, divergence, curl) applied to lattice fields
- **nuclear.cpp** — ✅ Nuclear system construction: deuteron pairing, alpha particle assembly, binding energy from vortex channels
- **analysis.cpp** — ✅ Magnetic moment computation from turbine circulation parameters, comparison against NIST values
- **io.cpp** — ✅ I/O utilities for serialising simulation state
