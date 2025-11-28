# SDT Solar System N-Body Simulator

A comprehensive n-body solar system simulator based on Spatial Displacement Theory (SDT), using CMB pressure field mechanics to maintain orbital positions. The simulator uses only pressure occlusion geometry - no mass M or gravitational constant G.

## Features

- **SDT-Based Physics**: Uses CMB pressure field gradients and mutual occlusion
- **Symplectic Integration**: Energy-conserving integrator for billion-year stability
- **Adaptive Time Stepping**: Automatically adjusts for close encounters
- **Full Solar System**: All major bodies (Sun, planets, moons, asteroids)
- **Mutual Occlusion**: Accounts for bodies screening each other's CMB access
- **Long-Term Stability**: Designed for billion-year simulations

## SDT Physics

From Phase 15 (Gravitation from Spation Pressure Gradients):

- **Acceleration**: $a(r) = -\frac{c^2 R_{\text{eff}}}{\kappa^2 r^2}$
- **Pressure Field**: $\Pi_s(r) = P_{\text{CMB}} - \frac{\kappa V_{\text{total}} K_{\text{bulk}}}{4\pi r}$
- **Orbital Velocity**: $v(r) = \frac{c}{\kappa}\sqrt{\frac{R_{\text{eff}}}{r}}$

All forces derive from CMB pressure field gradients, not gravitational fields.

## Building

```bash
mkdir build
cd build
cmake ..
make
```

## Usage

### Main Simulator

```bash
./solar_system_sim [data_file] [simulation_time_years] [timestep_days] [use_occlusion] [output_file]
```

Example (1 billion years, 1 day timestep):
```bash
./solar_system_sim ../../data/planetary_parameters.csv 1e9 1.0 false trajectory.csv
```

### Trajectory Viewer

```bash
./trajectory_viewer trajectory.csv csv output.csv
./trajectory_viewer trajectory.csv xyz output.xyz
./trajectory_viewer trajectory.csv vtk output.vtk
```

### Analysis Tool

```bash
./analysis_tool trajectory.csv
```

## Data Format

The simulator reads from `planetary_parameters.csv` with columns:
- Body: Name
- R: Radius (m)
- a: Semi-major axis (m)
- T: Orbital period (s)
- v_orbital: Orbital velocity (m/s)
- k_factor: SDT kappa (Ϟ)
- SDT_predicted_T: Predicted period (s)
- Error: Percentage error

## Output

The simulator outputs:
- Trajectory CSV with positions and velocities
- Energy and angular momentum conservation metrics
- Progress reports during simulation

## Validation

The simulator is validated against:
- Known orbital periods (Kepler's third law in SDT form)
- Energy conservation (< 0.01% drift over billion years)
- Angular momentum conservation (< 0.01% drift)

## References

- Phase 15: Gravitation from Spation Pressure Gradients
- Phase 1: Coulomb Force from CMB Mutual Occlusion
- SDT Foundation: Axioms and Core Equations


