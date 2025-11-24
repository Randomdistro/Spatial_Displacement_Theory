# Changelog

All notable changes to the SDT-Navier C++ simulator will be documented in this file.

## [0.1.0] - 2025-01-XX

### Added
- Initial implementation of SDT-Navier field theory simulator
- Field system with 3D storage (P, v, κ, η, e, Γ)
- Dodecahedral lattice structure with 12-axis connectivity
- Discrete operators (gradient, divergence, advection)
- SDT-Navier equations with force functionals
- Time-stepping solver with RK4 and pressure projection
- Nuclear system models (deuteron, triton, helion, alpha)
- Binding energy and magnetic moment calculations
- CSV and JSON I/O for results
- Python bindings via pybind11
- Unit tests with Catch2
- Executable tools (simulate_deuteron, simulate_nuclear, analyze_results)
- Comprehensive documentation

### Features
- High-performance C++20 implementation
- Incompressibility enforcement via pressure projection
- Adaptive timestep based on CFL condition
- Integration with existing Python validation infrastructure
- Validation against experimental nuclear data

### Known Limitations
- Simplified pressure projection (full Poisson solver can be added)
- RK4 implementation uses simplified approach (can be enhanced)
- HDF5 I/O not yet fully implemented (CSV/JSON available)
- GPU acceleration not yet implemented

