# sdt_orbital_sim/include — Overview

Header tree for the orbital simulation module. Organised under the `sdt::` namespace.

## Subfolders

- **sdt/core/** — 🔴 Core types (`Vec3d` = Eigen Cartesian, `SDTParameters` with `beta` field, `CelestialBody` with `mass_conv`), constants (`G_conv`, `solar_mass_conv`)
- **sdt/physics/** — 🟡 Pressure field calculator (correct SDT physics but uses `beta` and Cartesian types)
- **sdt/simulation/** — Simulation engine interface (integrator-based stepping)
- **sdt/numerics/** — Numerical integrators (RK4, leapfrog)
