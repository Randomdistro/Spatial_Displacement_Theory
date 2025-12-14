# SDT 3D Solar System Model

A high-precision, verifiable 3D solar system simulation using Spatial Displacement Theory (SDT) physics. This model demonstrates CMB pressure field propagation, accurate orbital mechanics, and sophisticated visualizations including dodecahedral wireframe shells.

## Features

- **SDT Physics**: All forces calculated from CMB pressure gradients (Phase 15)
- **Verifiable Calculations**: No fudged numbers - all formulas are exact SDT derivations
- **3D Visualization**: Beautiful Three.js-based rendering with smooth camera controls
- **Dodecahedral Shells**: Nested wireframe shells pairing celestial bodies
- **Orbital Markers**: White point markers at specified orbital radii
- **Lagrange Points**: Accurate L1-L5 calculations using SDT pressure field equations
- **Variable Timestep**: Physics timestep affects velocity, visual timestep keeps movement consistent
- **Conservation Monitoring**: Real-time energy and momentum drift tracking

## Usage

1. Open `index.html` in a modern web browser
2. Use mouse to orbit, pan, and zoom the camera
3. Click on bodies to focus camera
4. Hover over bodies or shells to see detailed information
5. Adjust timestep and speed controls to change simulation behavior

## Controls

- **Timestep Slider**: Changes physics timestep (affects velocity calculations)
- **Speed Slider**: Simulation speed multiplier
- **Play/Pause**: Toggle simulation
- **Reset**: Return to initial conditions
- **Focus**: Select body to focus camera on
- **Visualization Toggles**: Toggle particles, markers, shells, trails, grid

## Physics

All calculations use SDT formulas from Phase 15:

- **Pressure Field**: Π_s(r) = P_CMB - β ρ_s / r
- **Acceleration**: a(r) = -β / r² * r_hat
- **Beta Parameter**: β = c² R_eff / Ϟ²
- **Orbital Velocity**: v(r) = (c/Ϟ) √(R_eff/r)

## File Structure

```
SDT_3D_Solar_System/
├── index.html              # Main HTML file
├── css/
│   └── styles.css         # UI styling
├── js/
│   ├── main.js            # Application entry point
│   ├── data/
│   │   ├── constants.js   # SDT constants
│   │   ├── planetary_data.js
│   │   └── jpl_ephemeris.js
│   ├── physics/
│   │   ├── sdt_physics.js
│   │   ├── integrator.js
│   │   ├── conservation.js
│   │   └── lagrange_points.js
│   ├── visualization/
│   │   ├── scene_setup.js
│   │   ├── bodies.js
│   │   ├── dodecahedral_shells.js
│   │   ├── orbital_markers.js
│   │   ├── camera_controls.js
│   │   └── hover_info.js
│   └── ui/
│       └── controls.js
└── README.md
```

## Dependencies

- Three.js (r150+) - Loaded via CDN
- OrbitControls - Three.js addon (loaded via CDN)

## Browser Requirements

- Modern browser with WebGL support
- ES6 modules support
- Canvas API

## Notes

- Initial conditions use circular orbit approximation
- For precise JPL ephemeris data, implement DE file parser
- Performance optimized for 60 FPS with all visualizations enabled
- All formulas documented with Phase references

## Future Enhancements

- Real JPL DE file parsing for precise initial conditions
- Export trajectory data
- Comparison mode (SDT vs Newtonian)
- Multiple time scales
- Asteroid belt visualization
- Comet trajectories

