# SDT Orbital Mechanics Simulation

A high-performance C++20+ scientific simulation for **Spatial Displacement Theory (SDT) Orbital Mechanics** from pressure gradients.

## Overview

This simulation implements SDT orbital mechanics using **SDT-native quantities only** (no G, no M):
- **Ϟ (kappa)**: Velocity factor
- **R_eff**: Effective radius
- **β**: Gravitational parameter (β = c² R_eff / Ϟ²)
- **P_CMB**: Cosmic Microwave Background pressure

## Core Features

### Physics Engine
- **Pressure Field Calculations**: Multi-body pressure gradients from CMB occlusion
- **Orbital Mechanics**: v(r) = (c/Ϟ)√(R_eff/r), P = 2πϞ√(r³/R_eff)/c
- **N-Body Integration**: Symplectic and adaptive RK4 integrators

### Numerical Methods
- **Symplectic Integrator**: Energy-conserving for long-term stability
- **RK4 Integrator**: High-order accuracy
- **Adaptive RK45**: Automatic step size control

### Data Integration
- Loads planetary/exoplanetary systems from CSV
- Integrates with existing SDT data files
- Supports solar system and exoplanetary system validation

### Analysis Tools
- Orbital period validation
- Energy conservation monitoring
- Angular momentum conservation
- Position/velocity error analysis

## Building

### Requirements
- C++20 compatible compiler (GCC 10+, Clang 12+, MSVC 2019+)
- CMake 3.20+
- Eigen3 library
- fmt library

### Build Steps

```bash
cd SDT/Code/sdt_orbital_sim
mkdir build && cd build
cmake ..
make -j$(nproc)
```

## Usage

### Basic Usage

```bash
./sdt_sim [data_file] [output_file] [simulation_time]
```

### Examples

**Simulate solar system for 1 year:**
```bash
./sdt_sim ../../data/planetary_parameters.csv output.csv 3.15576e7
```

**Simulate with custom time step:**
Edit `main.cpp` to adjust `time_step` variable.

### Output Format

CSV file with columns:
- Time (s)
- Position (x, y, z) for each body (m)
- Velocity (vx, vy, vz) for each body (m/s)
- Total energy (J)
- Total angular momentum (kg·m²/s)

## Validation

The simulation validates against:
- Solar system orbital periods (error < 0.1%)
- Energy conservation (drift < 1e-6%)
- Angular momentum conservation (drift < 1e-6%)

## Architecture

### Core Components

- **`sdt/core/constants.hpp`**: SDT fundamental constants (CODATA 2018)
- **`sdt/core/types.hpp`**: Physical types (SDTParameters, CelestialBody, SystemState)
- **`sdt/physics/pressure_field.hpp`**: Pressure field calculations
- **`sdt/numerics/integrator.hpp`**: Numerical integrators
- **`sdt/simulation/engine.hpp`**: Main simulation engine
- **`sdt/io/data_loader.hpp`**: CSV data loading
- **`sdt/analysis/validator.hpp`**: Validation tools

### Design Principles

1. **SDT-Native Only**: No G, no M - only Ϟ, R_eff, β, P_CMB
2. **Scientific Rigor**: High-precision numerics, conservation monitoring
3. **Modern C++20**: Concepts, ranges, RAII, type safety
4. **Extensible**: Easy to add new integrators, validators, analysis tools

## Theoretical Foundation

### SDT Orbital Velocity Law

$$v(r) = \frac{c}{Ϟ}\sqrt{\frac{R_{\text{eff}}}{r}}$$

### SDT Orbital Period

$$P = \frac{2\pi Ϟ}{c}\sqrt{\frac{r^3}{R_{\text{eff}}}}$$

### Pressure Field

$$\Pi(r) = P_{\text{CMB}} - \frac{\beta \rho_s}{r}$$

### Acceleration from Pressure Gradient

$$a(r) = -\frac{\beta}{r^2} \hat{r}$$

where $\beta = \frac{c^2 R_{\text{eff}}}{Ϟ^2}$.

## Future Enhancements

- [ ] Multi-threading for N-body calculations
- [ ] GPU acceleration (CUDA/OpenCL)
- [ ] Visualization tools (VTK/Paraview integration)
- [ ] Exoplanetary system parameter calculation from L, T_eff
- [ ] Galactic rotation curve simulation
- [ ] Relativistic corrections
- [ ] Mutual occlusion screening effects

## References

- SDT Foundation Papers (Phase 15: Gravitation from Spation Pressure Gradients)
- Phase 22: Exoplanetary Systems Deriving Orbital Dynamics
- CODATA 2018 Fundamental Constants

## License

See main SDT project license.

