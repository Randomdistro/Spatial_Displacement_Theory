# SDT 3D Orbital Visualization System

## Overview

Full-featured **3D orbital visualization** system that builds orbits from:
1. **Simulation data**: Direct trajectory output from SDT orbital mechanics simulation
2. **Spectral data**: Radial velocity measurements converted to 3D orbits using SDT
3. **Observational data**: Combined predicted vs observed orbit comparisons

## Key Features

### 🎯 Core Capabilities

- **Full 3D Rendering**: Interactive VTK-based visualization
- **Spectral Data Integration**: Automatic conversion of RV data to 3D orbits
- **Period Detection**: Lomb-Scargle periodogram for orbital period finding
- **Orbital Parameter Fitting**: Extract orbital elements from spectral curves
- **Comparison Views**: Side-by-side predicted vs observed
- **Interactive Controls**: Rotate, zoom, pan, animate

### 📊 Data Sources Supported

1. **Simulation Output CSV**
   - Direct trajectory data (x, y, z positions)
   - Time series from N-body simulation

2. **Radial Velocity CSV**
   - Time series radial velocity measurements
   - Automatic orbital period detection
   - Conversion to 3D positions via SDT

3. **Stellar Spectral Data**
   - Wavelength shift measurements
   - Flux variations
   - Multi-wavelength integration

## Quick Start

### Build Visualization

```bash
cd SDT/Code/sdt_orbital_sim
mkdir build && cd build
cmake ..
make -j$(nproc)
```

This creates: `sdt_viewer` executable

### Basic Usage

**View simulation orbits:**
```bash
./sdt_viewer simulation_output.csv
```

**View with spectral data:**
```bash
./sdt_viewer simulation_output.csv rv_data.csv PlanetName
```

## Spectral Data Format

### CSV Format (Radial Velocity)

```csv
time,radial_velocity,radial_velocity_error
2451545.0,50.2,2.1
2451546.0,45.8,2.0
2451547.0,40.1,1.9
```

Or with Julian Day:
```csv
jd,rv,rv_error
2451545.5,50.2,2.1
2451546.5,45.8,2.0
```

### Column Names Supported

- `time` or `jd`: Time (seconds or Julian Day)
- `radial_velocity`, `rv`, `vr`: Radial velocity (m/s)
- `wavelength_shift`, `delta_lambda`: Wavelength shift (nm)
- `flux`: Flux measurement
- `rv_error`: Radial velocity uncertainty

## Orbital Parameter Extraction

### Automatic Period Detection

Uses **Lomb-Scargle periodogram** to find orbital period from radial velocity data:

```cpp
double period = SpectralDataLoader::find_orbital_period(spectral_data);
```

### Orbital Fitting

Extracts complete orbital parameters:

- Orbital period (P)
- Semi-major axis (a) - via SDT: a = R_eff (c/κ)² / v²
- Radial velocity amplitude (K)
- Eccentricity (e)
- Inclination (i)
- Longitude of ascending node (Ω)
- Argument of periapsis (ω)

### 3D Position Conversion

From radial velocity curve to 3D orbit:

1. **Phase calculation**: φ = 2π t / P
2. **Position in orbital plane**: r = a [cos(φ), sin(φ), 0]
3. **Transform by orbital elements**: rotation by i, Ω, ω
4. **Relative to primary**: add primary position

All using **SDT-native orbital mechanics** (no G, no M).

## Visualization Pipeline

```
Spectral Data (CSV)
    ↓
[Parse & Load]
    ↓
[Lomb-Scargle Periodogram]
    ↓ Period Detection
[Orbital Parameter Fitting]
    ↓ Orbital Elements
[SDT Position Calculation]
    ↓ 3D Positions
[VTK Rendering]
    ↓
Interactive 3D Visualization
```

## Example Workflows

### Example 1: Solar System from Simulation

```bash
# Run simulation
./sdt_sim ../../data/planetary_parameters.csv solar_out.csv 3.15576e7

# Visualize
./sdt_viewer solar_out.csv
```

### Example 2: Exoplanet from Radial Velocity

```bash
# Load exoplanet RV data, auto-detect period, convert to 3D orbit
./sdt_viewer simulation.csv hd209458_rv.csv HD209458b
```

### Example 3: Comparison View

The viewer can overlay:
- **Predicted** (from SDT simulation) - solid lines
- **Observed** (from spectral data) - dashed lines  
- **Uncertainty bands** - transparent regions

## Color Schemes

Pre-defined colors for solar system bodies:

- **Sun**: Yellow-white (1.0, 1.0, 0.8)
- **Mercury**: Gray (0.7, 0.7, 0.7)
- **Venus**: Orange-tan (1.0, 0.8, 0.6)
- **Earth**: Blue (0.2, 0.5, 1.0)
- **Mars**: Red (1.0, 0.3, 0.2)
- **Jupiter**: Orange-brown (0.9, 0.7, 0.5)
- **Saturn**: Yellow (0.9, 0.8, 0.6)
- **Uranus**: Cyan (0.6, 0.8, 1.0)
- **Neptune**: Blue (0.2, 0.4, 1.0)

Custom colors can be set per body.

## Controls

### Mouse Controls

- **Left drag**: Rotate view
- **Right drag**: Pan
- **Wheel**: Zoom in/out
- **Middle drag**: Translate

### Keyboard Shortcuts

- `q` or `Esc`: Quit
- `r`: Reset camera
- `s`: Save screenshot
- `+/-`: Zoom in/out
- `a`: Toggle axes
- `o`: Toggle orbits
- `b`: Toggle bodies

## SDT Integration

### SDT Orbital Velocity Law

The visualization uses SDT's core orbital equation:

$$v(r) = \frac{c}{Ϟ}\sqrt{\frac{R_{\text{eff}}}{r}}$$

This enables direct conversion from **radial velocity → 3D position** using only:
- **Ϟ** (kappa): Velocity factor
- **R_eff**: Effective radius
- **c**: Speed of light

**No G or M required!**

### Validation

The viewer validates:
- Orbital period predictions vs observations
- Position accuracy from spectral conversion
- Energy conservation in trajectories

## Output Options

### Screenshots

```cpp
viewer.save_screenshot("orbit_view.png");
```

### Animation Export

```cpp
viewer.export_animation("orbit_animation.mp4", fps=30);
```

### Trajectory Export

Export 3D positions back to CSV for further analysis.

## Performance

- **Solar system (10 bodies)**: Real-time rendering
- **Large systems (100+ bodies)**: LOD (Level of Detail) rendering
- **Spectral data processing**: O(N log N) for periodogram

## Future Enhancements

- [ ] Real-time spectral data streaming
- [ ] Web-based viewer (WebGL export)
- [ ] VR/AR support
- [ ] Multi-wavelength spectral overlay
- [ ] Transit light curve visualization
- [ ] Galactic rotation curve visualization

## Dependencies

- VTK 9.0+ (Visualization Toolkit)
- OpenGL 3.3+
- All SDT simulation dependencies

## Documentation

See `VISUALIZATION_GUIDE.md` for detailed documentation.

## References

- **VTK**: https://vtk.org/documentation/
- **Lomb-Scargle**: VanderPlas (2018) "Understanding the Lomb-Scargle Periodogram"
- **SDT Orbital Mechanics**: Phase 15, Phase 22

