# SDT 3D Orbital Visualization Guide

## Overview

The SDT visualization system provides **full 3D orbital visualization** built from:
- **Simulation data**: Direct trajectories from SDT orbital mechanics simulation
- **Spectral data**: Radial velocity measurements converted to 3D orbits
- **Observational data**: Combined predicted vs observed comparisons

## Features

### Core Capabilities

1. **3D Orbit Rendering**
   - Full 3D trajectories with customizable colors
   - Multiple bodies with proper scaling
   - Smooth trajectory curves

2. **Spectral Data Integration**
   - Load radial velocity measurements from CSV
   - Automatic period detection (Lomb-Scargle periodogram)
   - Convert spectral data to 3D orbital positions
   - Phase folding for periodic signals

3. **Comparison Views**
   - Predicted orbits (from simulation)
   - Observed orbits (from spectral/observational data)
   - Side-by-side or overlaid comparison

4. **Interactive Controls**
   - Rotate, zoom, pan with mouse
   - Toggle visibility of orbits/bodies
   - Adjust time animation
   - Save screenshots

## Building

### Requirements

- VTK (Visualization Toolkit) 9.0+
- OpenGL support
- All dependencies from main simulation

### Build Steps

```bash
cd SDT/Code/sdt_orbital_sim
mkdir build && cd build
cmake ..
make -j$(nproc)
```

This creates two executables:
- `sdt_sim`: The orbital simulation
- `sdt_viewer`: The 3D visualization tool

## Usage

### Basic Usage

**View simulation results:**
```bash
./sdt_viewer simulation_output.csv
```

**View with spectral data:**
```bash
./sdt_viewer simulation_output.csv radial_velocity_data.csv PlanetName
```

### Spectral Data Format

CSV file with columns:
```csv
time,radial_velocity,radial_velocity_error
2451545.0,50.2,2.1
2451546.0,45.8,2.0
2451547.0,40.1,1.9
...
```

Or with Julian Day:
```csv
jd,rv,rv_error
2451545.5,50.2,2.1
2451546.5,45.8,2.0
...
```

Or with wavelength shift:
```csv
time,wavelength_shift,flux
0.0,0.001234,1.0
1.0,0.001156,0.99
...
```

### Converting Spectral Data to Orbits

The viewer automatically:
1. **Detects orbital period** using Lomb-Scargle periodogram
2. **Fits orbital parameters** (semi-major axis, eccentricity, etc.)
3. **Converts to 3D positions** using SDT orbital mechanics
4. **Renders orbit** in 3D space

## Visualization Pipeline

### Data Flow

```
Spectral Data (CSV)
    ↓
[Period Detection]
    ↓
[Orbital Parameter Fitting]
    ↓
[3D Position Calculation]
    ↓
[VTK Rendering]
    ↓
3D Visualization
```

### Orbital Parameter Extraction

From radial velocity curve, the system extracts:

1. **Orbital Period (P)**
   - Lomb-Scargle periodogram analysis
   - Searches frequency space for peak power
   - Validates with phase folding

2. **Radial Velocity Amplitude (K)**
   - Maximum velocity range from data
   - Corrected for inclination

3. **Semi-Major Axis (a)**
   - From SDT: v(r) = (c/κ)√(R_eff/r)
   - Inverted to get: a = R_eff (c/κ)² / v²

4. **Orbital Elements**
   - Phase = 2π t / P
   - Position = a [cos(phase), sin(phase), 0]
   - Transformed by inclination, longitude, etc.

## Example Workflows

### Example 1: Solar System Visualization

```bash
# Run simulation
./sdt_sim ../../data/planetary_parameters.csv solar_system.csv 3.15576e7

# Visualize results
./sdt_viewer solar_system.csv
```

### Example 2: Exoplanet from Radial Velocity

```bash
# Load exoplanet RV data
./sdt_viewer simulation.csv hd209458_rv.csv HD209458b
```

### Example 3: Comparison View

The viewer can overlay:
- **Predicted orbit** (from SDT simulation)
- **Observed orbit** (from spectral data)
- **Uncertainty bands** (from measurement errors)

## Color Schemes

### Default Colors

- **Stars**: Yellow-white (1.0, 1.0, 0.8)
- **Planets**: Light blue (0.5, 0.7, 1.0)
- **Moons**: Gray (0.7, 0.7, 0.7)

### Custom Colors

Colors can be set per body via `BodyColor` structure:
```cpp
BodyColor color;
color.color = {r, g, b};  // RGB 0-1
color.opacity = 1.0;
color.size = 1.0;  // Relative size scaling
```

## Advanced Features

### Animation

- Play/pause orbital motion
- Adjust speed multiplier
- Step through time
- Loop animations

### Export Options

- **Screenshots**: PNG format
- **Animation**: Sequence of frames
- **Trajectory data**: Export 3D positions to CSV

### Multi-System View

View multiple exoplanetary systems simultaneously:
- Different star systems side-by-side
- Compare orbital architectures
- Highlight similarities/differences

## Integration with SDT Theory

### SDT Orbital Velocity Law

The visualization uses SDT's native orbital mechanics:

$$v(r) = \frac{c}{Ϟ}\sqrt{\frac{R_{\text{eff}}}{r}}$$

This allows direct conversion from radial velocity measurements to 3D orbital positions **without using G or M**.

### Validation

The viewer validates:
- Orbital period predictions vs observations
- Position accuracy from spectral data
- Energy conservation in trajectories

## Troubleshooting

### VTK Not Found

Install VTK:
```bash
# Ubuntu/Debian
sudo apt-get install libvtk9-dev

# macOS
brew install vtk

# Windows
# Use vcpkg or download from VTK website
```

### OpenGL Issues

Ensure OpenGL support:
- Update graphics drivers
- Check OpenGL version: `glxinfo | grep "OpenGL version"`

### Large Files

For large trajectory files:
- Use data sampling (every Nth point)
- Limit time range
- Use LOD (Level of Detail) rendering

## Future Enhancements

- [ ] Real-time spectral data streaming
- [ ] Web-based viewer (WebGL)
- [ ] VR/AR support
- [ ] Automatic orbit classification
- [ ] Machine learning period detection
- [ ] Multi-wavelength spectral integration

## References

- VTK Documentation: https://vtk.org/documentation/
- Lomb-Scargle Periodogram: VanderPlas (2018)
- SDT Orbital Mechanics: Phase 15, Phase 22

