# SDT Atomic Physics Simulator - Visualization Guide

## Overview

The SDT Atomic Physics Simulator includes comprehensive 3D visualization capabilities for electron orbitals, atomic spectra, energy levels, and transitions. This guide explains how to use the visualization tools effectively.

## Quick Start

### Basic Orbital Visualization

```bash
# Visualize hydrogen 1s orbital
./sdt_atomic_viewer orbital 1 0 0

# Visualize 2p orbital
./sdt_atomic_viewer orbital 2 1 0

# Visualize 3d orbital
./sdt_atomic_viewer orbital 3 2 0
```

### Spectrum Visualization

```bash
# Generate and display hydrogen spectrum
./sdt_atomic_viewer spectrum

# Compare with experimental data
./sdt_atomic_viewer spectrum ../../data/atomic_spectra_nist.csv
```

### Complete Atom Visualization

```bash
# Visualize hydrogen atom with all occupied orbitals
./sdt_atomic_viewer atom
```

## Orbital Visualization

### 3D Orbital Shapes

The viewer renders electron orbitals as 3D probability density isosurfaces. The shape represents regions where the electron is most likely to be found.

**Orbital Types:**

- **s orbitals** (l=0): Spherical shapes (red color)
- **p orbitals** (l=1): Dumbbell shapes (green color)
  - pz: Along z-axis
  - px: Along x-axis
  - py: Along y-axis
- **d orbitals** (l=2): Complex shapes (blue color)
- **f orbitals** (l=3): Very complex shapes (yellow color)

### Interactive Controls

**Mouse Controls:**
- **Left-click + Drag:** Rotate orbital
- **Right-click + Drag:** Zoom in/out
- **Middle-click + Drag:** Pan view

**Keyboard Shortcuts:**
- `r`: Reset camera to default view
- `s`: Save screenshot
- `q` or `Esc`: Quit viewer
- `+` / `-`: Adjust isosurface threshold
- `c`: Cycle color scheme
- `a`: Toggle axes display

### View Angles

**Common Views:**
- **xy-plane:** View along z-axis
- **xz-plane:** View along y-axis
- **yz-plane:** View along x-axis
- **3D perspective:** Default oblique view

**Example:**
```cpp
viewer.set_view_angle("xy");  // View from above
viewer.set_view_angle("3d");  // Perspective view
```

### Isosurface Values

The isosurface value controls the probability threshold displayed:

- **High value (0.1):** Shows only highest probability regions (compact)
- **Medium value (0.01):** Standard view (default)
- **Low value (0.001):** Shows extended probability cloud

**Adjustment:**
```cpp
viewer.set_isosurface_value(0.05);  // More compact
viewer.set_isosurface_value(0.005);  // More extended
```

### Color Schemes

**Default Color Mapping:**
- s orbitals: Red (RGB: 1.0, 0.3, 0.3)
- p orbitals: Green (RGB: 0.3, 1.0, 0.3)
- d orbitals: Blue (RGB: 0.3, 0.3, 1.0)
- f orbitals: Yellow (RGB: 1.0, 1.0, 0.3)

**Custom Colors:**
```cpp
std::array<double, 3> custom_color = {0.8, 0.2, 0.9};  // Purple
viewer.visualize_orbital(orbital, 0.01, custom_color);
```

## Energy Level Diagrams

### Displaying Energy Levels

```cpp
EnergyLevelViewer viewer;
viewer.show_levels(atom, 10);  // Show levels up to n=10
viewer.render();
```

**Features:**
- Horizontal lines represent energy levels
- Vertical arrows show transitions
- Color-coded by principal quantum number
- Labels show quantum numbers

### Transition Visualization

**Display Transitions:**
```cpp
viewer.show_transitions(transitions);  // Show allowed transitions
```

**Transition Colors:**
- Red: Lyman series (n → 1)
- Green: Balmer series (n → 2)
- Blue: Paschen series (n → 3)
- Yellow: Higher series

## Spectral Line Visualization

### Displaying Spectra

```cpp
SpectralViewer viewer;
viewer.show_spectrum(spectrum);  // Display calculated spectrum
viewer.render();
```

**Spectral Plot Features:**
- Wavelength on x-axis (nm)
- Relative intensity on y-axis
- Color-coded by series
- Labels for major lines (Hα, Hβ, Lyman α, etc.)

### Comparing Spectra

**Calculated vs Experimental:**
```cpp
viewer.compare_spectra(calculated_spectrum, experimental_spectrum);
```

**Comparison Features:**
- Overlay calculated (blue) and experimental (red) lines
- Highlight matching lines (green)
- Error bars for experimental uncertainties
- Percentage error display

### Specific Series

**Show Only Specific Series:**
```cpp
viewer.show_series(spectrum, SpectralSeries::BALMER);  // Only Balmer
viewer.show_series(spectrum, SpectralSeries::LYMAN);   // Only Lyman
```

## Transition Animations

### Animating Transitions

```cpp
TransitionViewer viewer;
viewer.animate_transition(initial_state, final_state, 2.0);  // 2 second animation
viewer.start_interactor();
```

**Animation Features:**
- Smooth morphing between orbital shapes
- Photon emission visualization
- Energy level change display
- Time-progress indicator

### Photon Visualization

**Photon Emission:**
```cpp
viewer.show_photon_emission(
    source_position,      // Where photon is emitted
    wavelength,           // Wavelength in meters
    emission_direction    // Direction vector
);
```

**Photon Rendering:**
- Wavy line representing electromagnetic wave
- Color based on wavelength (visible spectrum)
- Propagation animation

## Advanced Visualization

### Multi-Orbital Display

**Overlaying Multiple Orbitals:**
```cpp
std::vector<ElectronOrbital> orbitals;
orbitals.push_back(orbital_1s);
orbitals.push_back(orbital_2p);
orbitals.push_back(orbital_3d);

viewer.visualize_orbitals(orbitals);
```

**Use Cases:**
- Hybrid orbitals (sp, sp², sp³)
- Multi-electron atom visualization
- Orbital interactions

### Electron Density Visualization

**Full Electron Density:**
```cpp
AtomicSystem atom;
// ... configure atom ...
viewer.visualize_atom(atom);
```

**Features:**
- Total electron density as volume rendering
- Isosurfaces at multiple thresholds
- Color mapping by density value
- Nucleus visualization (optional)

### Fine Structure Visualization

**Display Fine Structure Splitting:**
```cpp
EnergyLevelViewer viewer;
FineStructureLevel level = analyzer.calculate_fine_structure(1, 2, 1);  // 2p
viewer.show_fine_structure(level);
```

**Visualization:**
- Split levels shown as closely spaced lines
- Splitting magnitude indicated
- Components labeled (j = l ± 1/2)

## Exporting Results

### Screenshots

**Save Screenshot:**
```cpp
viewer.save_screenshot("orbital_1s.png");
```

**Supported Formats:**
- PNG (recommended)
- JPEG
- TIFF

### Export Data

**Probability Density Grid:**
```cpp
auto grid = orbital.generate_probability_grid(center, extent, 100);
// Save to HDF5 or binary format
```

**Spectral Data:**
```cpp
// Save to CSV
TransitionDataLoader::save_to_csv(spectrum.lines, "spectrum.csv");
```

## Troubleshooting

### Display Issues

**Black Screen:**
- Check OpenGL drivers are installed
- Verify VTK is properly configured
- Try software rendering: `export LIBGL_ALWAYS_SOFTWARE=1`

**No Window Appears:**
- Check X11/Wayland display is available
- Verify DISPLAY environment variable (Linux)
- Try running with `DISPLAY=:0 ./sdt_atomic_viewer ...`

### Performance Issues

**Slow Rendering:**
- Reduce grid resolution
- Lower isosurface threshold (fewer polygons)
- Disable anti-aliasing

**High Memory Usage:**
- Reduce grid resolution
- Don't load too many orbitals simultaneously
- Close unused viewers

### Missing Features

**Orbital Not Displayed:**
- Check quantum numbers are valid (l < n, |m| ≤ l)
- Verify orbital state is properly calculated
- Check isosurface value is appropriate

**No Spectral Lines:**
- Verify spectrum generation completed
- Check wavelength range is visible
- Ensure transitions are allowed (selection rules)

## Examples

### Example 1: Hydrogen Atom Visualization

```cpp
#include "sdt/physics/electron_orbitals.hpp"
#include "sdt/visualization/orbital_viewer.hpp"

// Create hydrogen atom
physics::atomic::HydrogenAtom hydrogen;

// Get 1s orbital
auto state = hydrogen.get_state(1, 0, 0);
physics::atomic::ElectronOrbital orbital;
orbital.state = state;
orbital.Z = 1;

// Visualize
visualization::atomic::OrbitalViewer3D viewer;
viewer.initialize();
viewer.visualize_orbital(orbital);
viewer.start_interactor();
```

### Example 2: Complete Spectrum Analysis

```cpp
// Generate spectrum
physics::atomic::AtomicSpectrum spectrum;
spectrum.generate_hydrogen_spectrum(10);

// Display
visualization::atomic::SpectralViewer viewer;
viewer.show_spectrum(spectrum);
viewer.render();
```

### Example 3: Transition Animation

```cpp
// Get initial and final states
auto initial = hydrogen.get_state(2, 1, 0);  // 2p
auto final = hydrogen.get_state(1, 0, 0);    // 1s

// Animate transition
visualization::atomic::TransitionViewer viewer;
viewer.animate_transition(initial, final, 2.0);
viewer.start_interactor();
```

## Further Reading

- [VTK Documentation](https://vtk.org/documentation/)
- [SDT Phase 2: Rydberg Spectrum](Phase_2_Rydberg_Spectrum_from_Helical_Standing_Waves.md)
- [SDT Phase 3: Fine Structure](Phase_3_Fine_Structure.md)
- [Orbital Visualization Theory](SIMULATION_DESIGN.md)

