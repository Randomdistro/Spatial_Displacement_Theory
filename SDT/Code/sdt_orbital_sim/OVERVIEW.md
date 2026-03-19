# sdt_orbital_sim — Overview

🔴 **NEEDS PURIFICATION** — C++20 orbital simulation engine using SDT pressure-field dynamics. Core physics approach is sound (pressure gradients, occlusion) but implementation is contaminated with `β` gravitational parameter, `mass_conv` inputs, `G_conv`/`solar_mass_conv` constants, and Eigen Cartesian `Vec3d` types.

## Subfolders

- **include/** — Header tree: core (types, constants, galactic_structure), physics (pressure_field), simulation (engine), numerics (integrator)
- **src/** — Implementations: galaxy_sim, simulation_engine, I/O, visualisation
- **build/** — Build output directory (generated)

## Files

- **CMakeLists.txt** — Build configuration (requires Eigen)
- **README.md** — Module documentation
- **README_VISUALIZATION.md** — Visualisation guide
- **SIMULATION_DESIGN.md** — Simulation architecture design
- **VISUALIZATION_GUIDE.md** — Plotting and output guide
- **build.sh** — Unix build script
- **main.cpp** — 🟡 Entry point for N-body orbital simulation
- **.gitignore** — Build artifact exclusions
