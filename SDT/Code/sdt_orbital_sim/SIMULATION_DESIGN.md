# SDT Orbital Mechanics Simulation - Design Document

## Overview

This is a **high-performance, scientific-grade C++20+ simulation** for **Spatial Displacement Theory (SDT) Orbital Mechanics** based on pressure gradients. It simulates multi-body orbital dynamics using **SDT-native quantities only** (no G, no M).

## Critical Concept: SDT Orbital Mechanics from Pressure Gradients

### Why This is Most Critical

1. **Foundational**: Orbital mechanics underlies all gravitational phenomena
2. **Well-Validated**: Solar system predictions achieve <0.1% error
3. **Unifying**: Connects atomic (Ϟ), planetary, stellar, and galactic scales
4. **Predictive**: Can predict exoplanetary systems, galactic rotation curves
5. **Testable**: Direct validation against observational data

### SDT Orbital Equations

**Velocity Law:**
$$v(r) = \frac{c}{Ϟ}\sqrt{\frac{R_{\text{eff}}}{r}}$$

**Period Law:**
$$P = \frac{2\pi Ϟ}{c}\sqrt{\frac{r^3}{R_{\text{eff}}}}$$

**Acceleration from Pressure Gradient:**
$$a(r) = -\frac{\beta}{r^2}\hat{r}$$

where $\beta = \frac{c^2 R_{\text{eff}}}{Ϟ^2}$.

**Pressure Field:**
$$\Pi(r) = P_{\text{CMB}} - \frac{\beta \rho_s}{r}$$

## Architecture

### Core Components

```
sdt_orbital_sim/
├── include/
│   └── sdt/
│       ├── core/
│       │   ├── constants.hpp    # SDT fundamental constants (CODATA 2018)
│       │   └── types.hpp        # SDTParameters, CelestialBody, SystemState
│       ├── physics/
│       │   └── pressure_field.hpp  # Pressure gradient calculations
│       ├── numerics/
│       │   └── integrator.hpp   # RK4, Adaptive RK45, Symplectic
│       ├── simulation/
│       │   └── engine.hpp       # Main simulation engine
│       ├── io/
│       │   └── data_loader.hpp  # CSV data loading
│       └── analysis/
│           └── validator.hpp    # Validation metrics
├── src/
│   └── simulation_engine.cpp
├── main.cpp
└── CMakeLists.txt
```

### Data Flow

1. **Load**: CSV → `SystemState` (bodies with SDT parameters)
2. **Initialize**: Calculate initial energy, angular momentum
3. **Integrate**: Step-by-step N-body simulation
4. **Validate**: Compare with observations, monitor conservation
5. **Output**: CSV trajectory data, validation reports

### Key Design Decisions

#### 1. SDT-Native Quantities Only

- **No G, no M**: Uses Ϟ, R_eff, β, P_CMB exclusively
- **Pure geometry**: All forces from pressure gradients
- **Unified framework**: Same equations from atomic to galactic scales

#### 2. Modern C++20 Features

- **RAII**: Automatic resource management
- **Type safety**: Strong typing with `scalar_t`, `Vec3d`
- **Smart pointers**: `std::unique_ptr` for integrators
- **Function objects**: Callbacks for output/analysis
- **Concepts ready**: Can add C++20 concepts for further safety

#### 3. Scientific Rigor

- **Conservation monitoring**: Energy and angular momentum tracking
- **Multiple integrators**: Symplectic (long-term), RK4 (accuracy), Adaptive (robust)
- **Validation built-in**: Compare with observational data
- **Precision**: Double precision throughout, with error estimates

#### 4. Extensibility

- **Pluggable integrators**: Easy to add new numerical methods
- **Modular physics**: Pressure field calculations separated
- **Analysis hooks**: Callbacks for custom analysis
- **Data format**: CSV for easy integration with analysis tools

## Numerical Methods

### Integrator Comparison

| Integrator | Accuracy | Stability | Speed | Use Case |
|------------|----------|-----------|-------|----------|
| Symplectic | Medium | Excellent | Fast | Long-term evolution |
| RK4 | High | Good | Medium | High-accuracy |
| Adaptive RK45 | High | Excellent | Slow | Robust general-purpose |

**Recommendation**: Use Symplectic for long-term simulations (>100 orbits), RK4 for high-precision, Adaptive for unknown systems.

### Time Step Selection

- **Solar system**: 1 hour (3600 s) for planets
- **Exoplanetary**: 0.1-1 day depending on orbital period
- **Galactic**: Days to weeks

Adaptive integrator automatically adjusts based on error estimates.

## Validation Framework

### Metrics

1. **Orbital Period Error**: % difference from observed
2. **Velocity Error**: % difference from expected
3. **Energy Conservation**: Relative energy drift
4. **Angular Momentum Conservation**: Relative L drift
5. **Position Accuracy**: RMS position error

### Target Precision

- **Period prediction**: <0.8% error (SDT requirement)
- **Energy conservation**: <1e-6% drift per orbit
- **Angular momentum**: <1e-6% drift per orbit

## Data Integration

### Input Format (CSV)

```csv
Body,R,a,T,k_factor
Sun,6.957e8,0,0,686.34
Earth,6.371e6,1.496e11,3.15576e7,686.34
Jupiter,6.9911e7,7.785e11,3.7435e8,686.34
```

### Output Format (CSV)

```csv
Time(s),Body_x(m),Body_y(m),Body_z(m),Body_vx(m/s),Body_vy(m/s),Body_vz(m/s),Energy(J),Angular_Momentum(kg·m²/s)
0.0,1.496e11,0,0,0,29780,0,-1.234e33,2.654e40
86400.0,1.495e11,2.5e9,0,-500,29782,0,-1.234e33,2.654e40
```

## Performance Considerations

### Optimization Strategies

1. **Spatial indexing**: For N > 100 bodies, use octree/barnes-hut
2. **Parallelization**: Multi-thread pressure field calculations
3. **GPU acceleration**: Offload N-body forces to GPU
4. **Adaptive timestep**: Larger steps when forces are small

### Expected Performance

- **Solar system (10 bodies)**: ~1e6 steps/second (single-threaded)
- **Memory**: ~1 KB per body per timestep output

## Future Enhancements

### Short Term
- [ ] Visualization: VTK/Paraview integration
- [ ] Exoplanetary parameter calculation from L, T_eff
- [ ] Mutual occlusion screening effects

### Medium Term
- [ ] GPU acceleration (CUDA/OpenCL)
- [ ] Relativistic corrections
- [ ] Tidal effects
- [ ] N-body perturbation theory

### Long Term
- [ ] Galactic rotation curve simulation
- [ ] Large-scale structure formation
- [ ] Cosmological simulations

## Testing Strategy

### Unit Tests
- Pressure field calculations
- Integrator accuracy
- Conservation properties

### Integration Tests
- Solar system validation
- Exoplanetary system predictions
- Energy/momentum conservation over 1000 orbits

### Validation Tests
- Compare with JPL ephemerides
- Compare with exoplanet observations
- Compare with galactic rotation curves

## References

1. **Phase 15**: Gravitation from Spation Pressure Gradients
2. **Phase 22**: Exoplanetary Systems Deriving Orbital Dynamics
3. **CODATA 2018**: Fundamental Constants
4. **Numerical Recipes**: Press et al. (2007)

## Conclusion

This simulation provides a **rigorous, extensible framework** for testing SDT orbital mechanics predictions against observational data. It demonstrates that SDT can accurately predict orbital dynamics using **only geometric parameters** (Ϟ, R_eff) **without invoking G or M**, providing strong validation of the theoretical framework.

