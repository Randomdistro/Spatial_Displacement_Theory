# sdt_atomic_sim/include — Overview

C++ header tree for the atomic simulation module. Organised under the `sdt::` namespace hierarchy.

## Subfolders

- **sdt/core/** — Core types (`Vec3d` = Eigen Vector3d) and physical constants (`M_E`, `M_P`, `M_N`, Bohr radius, fine structure constant)
- **sdt/physics/** — 🔴 Electron orbital wave functions (QM model), spectral transition calculations
- **sdt/simulation/** — Atomic engine interface (`add_electron()` with quantum numbers)
- **sdt/io/** — Atomic data loader for reference datasets
- **sdt/visualization/** — Orbital viewer for 3D probability density rendering
