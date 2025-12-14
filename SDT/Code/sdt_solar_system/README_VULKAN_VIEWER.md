# Vulkan 3D SDT Solar System Viewer

## Overview

A high-performance 3D solar system simulator using Vulkan graphics API, integrating:

- **JPL DE421 Ephemeris Loader**: Loads initial conditions from earliest verified historical data (1800 AD)
- **SDT Physics Engine**: Uses symplectic integrator with SDT acceleration formula `a = c² * R_eff / (κ² * r²)`
- **Camera Controller**: 3D navigation with orbit, pan, and zoom controls
- **ImGui UI**: Interactive controls for timestep, time speed, body focus, and visualization toggles
- **Point Particle System**: White visualization markers at specific orbital distances

## Features

### Physics Simulation
- Symplectic leapfrog integrator for long-term stability
- Energy and angular momentum conservation tracking
- Adjustable timestep (100s to 86400s)
- Time speed multiplier (0x to 1000x)
- Pause/play controls

### Visualization
- 3D rendering of all major planets and moons
- Orbital trails
- Toggleable visualization markers at:
  - 50% Mercury orbital radius
  - Mercury orbit (20% offset from planet)
  - Halfway to Venus
  - Venus orbit (20% offset)
  - Halfway Venus→Earth
  - Earth orbit
  - 1/3 and 2/3 to Mars
  - Mars orbit
  - Continue pattern for outer planets
- Coordinate grid (toggleable)
- Focus on any celestial body

### Data Validation
- Compares simulation results against modern JPL ephemeris
- Tracks deviation from historical to modern positions
- Energy and angular momentum error display

## Building

### Prerequisites

- CMake 3.20+
- C++20 compatible compiler
- Vulkan SDK
- GLFW3
- ImGui
- Eigen3
- fmt

### Build Steps

```bash
cd SDT/Code/sdt_solar_system
mkdir build && cd build
cmake ..
make vulkan_solar_system_viewer
```

### Dependencies

The CMakeLists.txt will attempt to find:
- `Vulkan` (via `find_package(Vulkan REQUIRED)`)
- `glfw3` (via `find_package(glfw3 REQUIRED)`)
- `imgui` (via `find_package(imgui REQUIRED)`)
- `Eigen3` (already required)
- `fmt` (already required)

If packages are not found via CMake, you may need to:
1. Install Vulkan SDK from https://vulkan.lunarg.com/
2. Install GLFW3: `sudo apt-get install libglfw3-dev` (Linux) or use vcpkg
3. Install ImGui: Clone from https://github.com/ocornut/imgui and add to CMakeLists.txt

## Usage

```bash
./vulkan_solar_system_viewer
```

### Controls

**Mouse:**
- Left drag: Orbit camera around focus
- Right drag: Pan camera
- Scroll: Zoom in/out

**UI Controls:**
- **Time Step**: Adjust simulation timestep (affects accuracy, not speed)
- **Time Speed**: Multiplier for simulation speed
- **Pause/Play**: Toggle simulation
- **Focus Body**: Select celestial body to focus camera on
- **Show Markers**: Toggle visualization markers
- **Show Trails**: Toggle orbital trails
- **Show Grid**: Toggle coordinate grid

### Data Files

The viewer expects `planetary_parameters.csv` in one of these locations:
- `SDT/data/planetary_parameters.csv`
- `../../data/planetary_parameters.csv`
- `data/planetary_parameters.csv`

## Architecture

### Components

1. **JPLDE421Loader** (`jpl_de421_loader.hpp/cpp`)
   - Loads initial conditions from JPL DE421 ephemeris
   - Supports earliest verified date (1800-01-01, JD 2378495.0)
   - Uses orbital elements approximation (full DE421 binary support can be added)

2. **CameraController** (`camera_controller.hpp/cpp`)
   - Spherical coordinate camera system
   - Orbit, pan, zoom controls
   - View matrix calculation

3. **PointParticleSystem** (`point_particle_system.hpp/cpp`)
   - Calculates marker positions at specified orbital distances
   - Ensures 20% minimum distance from planets
   - Generates markers for all inter-planetary regions

4. **VulkanSolarSystemViewer** (`vulkan_solar_system_viewer.cpp`)
   - Main application class
   - Vulkan initialization and rendering
   - ImGui integration
   - Simulation loop

### SDT Physics Integration

The viewer uses the existing `SymplecticIntegrator` from `integrator.hpp`, which implements:
- Kick-drift-kick leapfrog algorithm
- SDT acceleration calculation via `PressureField::net_acceleration()`
- Energy and angular momentum conservation

## Future Enhancements

- Full JPL DE421 binary file support (currently uses orbital elements approximation)
- Vulkan rendering pipeline for bodies and markers (currently placeholder)
- Trajectory export functionality
- Comparison view (historical vs modern ephemeris side-by-side)
- Performance optimizations for large timesteps
- Multi-body focus (e.g., Earth-Moon barycenter)

## Notes

- The Vulkan rendering code is currently a skeleton - full implementation requires:
  - Vertex buffer creation for celestial bodies
  - Pipeline setup for 3D rendering
  - Shader compilation
  - Proper synchronization

- For a complete implementation, consider using a Vulkan wrapper library like:
  - Vulkan-HPP (C++ bindings)
  - VMA (Vulkan Memory Allocator)
  - Or a higher-level framework

