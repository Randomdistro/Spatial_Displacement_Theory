# sdt_chemistry/include/sdt/chemistry — Overview

Headers for the SDT molecular chemistry engine. All bond models use pressure-gradient minima rather than electron sharing.

## Files

- **bonds.hpp** — ✅ Chemical bond types and SDT pressure-field bond model
- **constants.hpp** — Chemical constants (needs audit for mass-as-input)
- **elements.hpp** — ✅ Element data structure: Z, name, orbital configuration, nuclear geometry
- **molecules.hpp** — ✅ Molecular structure: atom positions, bond graph, molecular properties
- **geometry.hpp** — ✅ Molecular geometry utilities: bond angles, dihedral angles, distance calculations
- **pressure_field.hpp** — ✅ SDT pressure-field model for chemical bonding: admittance, overlap, bond strength
- **master_equation.hpp** — ✅ Master equation for reaction kinetics from pressure-field dynamics
- **properties.hpp** — ✅ Molecular property calculations: dipole moment, polarisability
- **designer.hpp** — ✅ Molecular design tools: build molecules from component specification
- **data_loader.hpp** — ✅ Reference data loading for element and molecule databases
- **visualizer.hpp** — ✅ Molecular visualisation: ball-and-stick rendering, pressure field overlays
