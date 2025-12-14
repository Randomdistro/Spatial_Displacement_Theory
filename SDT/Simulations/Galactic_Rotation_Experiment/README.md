# SDT Galactic Rotation Experiment

A comprehensive simulation and validation framework for testing SDT's disk eclipse saturation hypothesis for flat galactic rotation curves.

## Objective

Validate SDT prediction that flat galactic rotation curves arise from disk eclipse saturation of the CMB pressure field, **without requiring dark matter**.

## Key Prediction

For disk geometry, the directional occlusion function E(r) becomes radius-invariant at large r, producing constant acceleration:

**a(r) ∝ 1/r** → **v(r) = constant**

**Test:** R_flat should correlate with disk scale length R_d as:

**R_flat ≈ 2.5 R_d**

## Features

- **Directional Occlusion Calculation**: E(r) for exponential disk geometry
- **Rotation Curve Prediction**: v(r) from SDT pressure gradients
- **SPARC Database Analysis**: Compare predictions to 175+ galaxies
- **R_flat/R_d Correlation Test**: Validate the 2.5 prediction
- **Visualization**: Rotation curves, occlusion functions, correlation plots
- **Dark Matter Comparison**: SDT vs NFW halo models

## Physics

From Phase 24: Disk Eclipse Saturation

- **Occlusion Function**: E(r) = 1 - exp(-τ(r))
- **Optical Depth**: τ(r) = σ n₀ R_d (1 - exp(-r/R_d))
- **Saturation**: E(r) → E_∞ = constant for r >> R_d
- **Rotation Velocity**: v(r) = √(β (1-E(r)) / r)

## Usage

```bash
# Calculate rotation curve for a galaxy
python galactic_rotation_sim.py --galaxy NGC3198

# Test R_flat/R_d correlation
python galactic_rotation_sim.py --test-correlation

# Analyze SPARC database
python galactic_rotation_sim.py --analyze-sparc

# Generate visualizations
python galactic_rotation_sim.py --visualize --galaxy NGC3198
```

## Files

- `galactic_rotation_sim.py` - Main simulation engine
- `disk_occlusion.py` - Directional occlusion calculations
- `sparc_analyzer.py` - SPARC database analysis
- `visualization.py` - Plotting and visualization
- `data/` - SPARC data and results

## Status

Under active development - validating against SPARC database.

