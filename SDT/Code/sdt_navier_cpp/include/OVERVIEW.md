# sdt_navier_cpp/include — Overview

Public C++ headers for the SDT Navier computational engine. Contains the high-level calculator interfaces and domain-specific geometry models.

## Subfolders

- **sdt_navier/** — Internal headers for the core Navier field engine (constants, equations, fields, lattice, solver, operators, nuclear turbine models, I/O, analysis)

## Files

- **stellar_calculator.hpp** — 🟡 Stellar structure calculator using zk²=1 methodology: c-boundary radius, effective temperature, luminosity-radius relation. Contains `M_SUN` constant (unused in calc) and `force_at_c_boundary(mass_kg)` taking mass as input — both need purification
- **galactic_rotation.hpp** — 🟡 Galactic rotation curve calculator: disk eclipse saturation model, L·k² diagnostic. Contains `M_SUN` constant, `M_disk_solar` as input, and `dark_matter_halo_velocity()` NFW function — needs purification
- **atomic_calculator.hpp** — 🟡 Atomic structure calculator: Rydberg transitions, fine/hyperfine structure, geometric occlusion screening (Z_eff). Uses `M_E`/`M_P` as input primitives in reduced mass — needs Compton wavelength rewrite
- **state_28d.hpp** — ✅ Pure SDT 28-dimensional state vector manifold on spherical basis (r, θ, φ). Coordinates: position, velocity, acceleration, jerk, pressure, density, vorticity, expansion, shear
- **nuclear_geometry.hpp** — ✅ Pure SDT nuclear binding via trefoil vortex model: neutrino counting per channel, deuteron/alpha/carbon-12/oxygen-16 geometries
- **nuclear_geometry_occlusion.hpp** — ✅ Pure SDT solid-angle occlusion binding model: CMB pressure shadow gives binding energy per steradian
- **nuclear_packing.hpp** — 🟡 Icosahedral nuclear packing geometry: 12-vertex base, second layer, alpha cluster arrangements. Uses Cartesian `.x .y .z` coordinates — needs spherical refactor
