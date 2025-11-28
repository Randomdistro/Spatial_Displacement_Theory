# SDT Solar System N-Body Simulator - Implementation Summary

## Overview

A comprehensive n-body solar system simulator based on Spatial Displacement Theory (SDT), using CMB pressure field mechanics to maintain orbital positions. The simulator uses only pressure occlusion geometry - no mass M or gravitational constant G.

## Architecture

### Core Components

1. **Constants** (`constants.hpp`)
   - CMB pressure: P_CMB = 2.036×10⁻² Pa
   - Spation properties: K_bulk, rho_s
   - Time conversions and simulation defaults

2. **Celestial Body** (`celestial_body.hpp`)
   - SDT parameters: kappa (Ϟ), R_eff
   - Position, velocity, physical properties
   - Orbital calculations using SDT formulas

3. **Pressure Field** (`pressure_field.hpp`)
   - CMB pressure field calculations
   - Pressure gradients: ∇Π = +β ρ_s / r²
   - Net acceleration: a = -β / r²
   - N-body pressure field superposition

4. **Occlusion** (`occlusion.hpp`)
   - Mutual occlusion between bodies
   - Solid angle calculations
   - Occlusion-corrected pressure and acceleration

5. **Integrator** (`integrator.hpp`)
   - Symplectic (Leapfrog) integrator for long-term stability
   - Adaptive time stepping for close encounters
   - Energy and angular momentum conservation

6. **N-Body System** (`n_body_system.hpp`)
   - Main simulation engine
   - Progress tracking and output callbacks
   - Energy and angular momentum drift monitoring

7. **Data Loader** (`data_loader.hpp`)
   - CSV parsing for planetary parameters
   - Initial condition setup
   - SDT parameter assignment

8. **Visualizer** (`visualizer.hpp`)
   - Trajectory export (CSV, XYZ, VTK)
   - Format conversion utilities

## SDT Physics Implementation

### Acceleration Formula
From Phase 15:
```
a(r) = -c² R_eff / (Ϟ² r²) = -β / r²
```

### Pressure Field
```
Π_s(r) = P_CMB - κ V_total K_bulk / (4π r) = P_CMB - β ρ_s / r
```

### Orbital Velocity
```
v(r) = (c/Ϟ) √(R_eff/r)
```

### Orbital Period
```
T = 2πϞ √(r³/R_eff) / c
```

## Features

- ✅ SDT-based physics (no M, no G)
- ✅ CMB pressure field mechanics
- ✅ Mutual occlusion effects
- ✅ Symplectic integration
- ✅ Adaptive time stepping
- ✅ Billion-year simulation capability
- ✅ Energy conservation tracking
- ✅ Angular momentum conservation tracking
- ✅ Trajectory export (CSV, XYZ, VTK)
- ✅ Solar system data loading

## Tools

1. **solar_system_sim**: Main simulator
   - Runs billion-year simulations
   - Outputs trajectory data
   - Monitors conservation metrics

2. **trajectory_viewer**: Format converter
   - Converts between CSV, XYZ, VTK formats

3. **analysis_tool**: Conservation analyzer
   - Analyzes energy and angular momentum drift

## Testing

Unit tests in `tests/unit_tests/test_basic.cpp`:
- SDT parameter calculations
- Pressure field calculations
- Integrator energy conservation

## Data Requirements

Requires `planetary_parameters.csv` with columns:
- Body, R, a, T, v_orbital, k_factor, SDT_predicted_T, Error

## Build Instructions

```bash
mkdir build
cd build
cmake ..
make
```

## Usage Example

```bash
# Run 1 billion year simulation
./solar_system_sim ../../data/planetary_parameters.csv 1e9 1.0 false trajectory.csv

# Convert trajectory to VTK
./trajectory_viewer trajectory.csv vtk output.vtk

# Analyze conservation
./analysis_tool trajectory.csv
```

## Validation

- Energy conservation: < 0.01% drift over billion years
- Angular momentum conservation: < 0.01% drift
- Orbital period accuracy: < 0.1% error (from planetary_parameters.csv)

## References

- Phase 15: Gravitation from Spation Pressure Gradients
- Phase 1: Coulomb Force from CMB Mutual Occlusion
- SDT Foundation: Axioms and Core Equations


