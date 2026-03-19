# sdt_navier_cpp/include/sdt_navier — Overview

Internal headers for the core SDT Navier field engine. These define the lattice, field types, equation implementations, solver interface, and nuclear turbine models.

## Files

- **constants.hpp** — 🟡 Physical constants: speed of light, Planck constant, fine structure constant, spation density/pressure, proton/neutron geometry parameters, experimental binding energies, magnetic moments. Contains `M_E`, `M_P`, `M_N` as standalone constants — should be in `derived_reference` sub-namespace
- **equations.hpp** — ✅ SDT Navier field equation declarations: pressure gradient, vorticity evolution, continuity
- **fields.hpp** — ✅ Field type definitions: TurbineCell (proton/neutron/electron vortex models), circulation parameters, SDT field state
- **lattice.hpp** — ✅ Lattice construction for numerical Navier simulations
- **solver.hpp** — ✅ Solver interface for iterating field equations to convergence
- **operators.hpp** — ✅ Differential operator algebra (gradient, divergence, curl) on the lattice
- **nuclear.hpp** — ✅ Nuclear system types: DeuteronSystem, AlphaParticleSystem, and related binding structures
- **io.hpp** — ✅ I/O utilities for reading/writing simulation results
- **analysis.hpp** — ✅ Magnetic moment computation and comparison utilities
