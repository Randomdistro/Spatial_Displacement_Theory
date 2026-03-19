# sdt_solar_system — Overview

C++20 solar system simulation using SDT pressure-field orbital mechanics. Includes JPL DE421 ephemeris loading, point-particle N-body integration, and both terminal and Vulkan visualisation.

## Subfolders

- **include/sdt/** — Headers: solar system types, constants, and structure definitions
- **src/** — Implementations: camera controller, JPL DE421 loader, point particle system
- **tools/** — Executables: solar system simulator, analysis tool, trajectory viewer, Vulkan viewer (full and simple versions)
- **tests/** — Unit tests
- **data/** — Ephemeris and reference data
- **build/** — Build output directory (generated)

## Files

- **CMakeLists.txt** — Build configuration (standard)
- **CMakeLists_vulkan.txt** — Alternative build configuration with Vulkan rendering support
- **README.md** — Module documentation
- **README_VULKAN_VIEWER.md** — Vulkan viewer setup and usage guide
- **IMPLEMENTATION_SUMMARY.md** — Summary of implemented features
