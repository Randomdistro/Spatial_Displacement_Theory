# SDT-Navier Validator Fixes

## Summary

Fixed critical issues that made the code a "generator + renderer" instead of a true validator. The code now computes observables from field integrals without hard-coded normalization.

## Changes Made

### 1. Magnetic Moments: Field-Integral Method (PREDICTIVE)

**Problem:** Magnetic moments were hard-coded with per-particle normalization:
```python
mu_mag_n = mu_mag * 2.793 / (reference_value)  # Non-predictive!
```

**Fix:** Compute from current density integral:
```python
μ = (1/2) ∫ r × J(r) d³r
```
where `J(r) ∝ (1-η) Γ κ v` is the effective current density from SDT fields.

**Key Changes:**
- `compute_magnetic_moment_from_current_density()`: New function that computes dipole moment from field integral
- `calibrate_from_proton()`: Calibrate global constant ONCE from proton, then predict all others
- Removed per-particle normalization factors

**Usage:**
```python
# Step 1: Calibrate from proton (once)
calibration = calibrate_from_proton(fields, proton_pos, proton_radius)

# Step 2: Predict all other nuclei (no normalization!)
mu_n = compute_magnetic_moment_from_current_density(
    fields, neutron_pos, neutron_radius, calibration
)
mu_d = compute_nuclear_magnetic_moment(deuteron, calibration)
```

### 2. Dodecahedral Lattice: Proper Interpolation

**Problem:** Directions rounded to -1/0/+1, collapsing to 3D Moore stencil:
```python
di = int(np.round(direction[0] * dx / dx))  # Always -1, 0, or +1!
```

**Fix:** Use interpolation weights and remove duplicates:
- Store interpolation weights for each direction
- Remove duplicate offsets (keep highest weight)
- Enables proper 12-axis flux calculations

**Key Changes:**
- Added `interpolation_weights` and `direction_indices`
- Removed duplicate offsets that mapped to same grid point
- Preserves 12 distinct directions

### 3. Incompressibility: Proper Poisson Solve

**Problem:** Heuristic divergence damper:
```python
P += alpha_p * div_v * dt  # Not a proper projection!
v -= beta_v * grad(div_v)  # Doesn't enforce ∇·v = 0
```

**Fix:** Standard pressure projection:
1. Compute divergence: `div_v = ∇·v*`
2. Solve Poisson: `∇²φ = (1/Δt) div_v`
3. Correct velocity: `v^{n+1} = v* - ∇φ`

**Key Changes:**
- Implemented Jacobi iteration for Poisson solve
- Properly enforces `∇·v = 0` (up to numerical error)
- Updates pressure field: `P += φ`

### 4. Binding Energy: Field Energy Functional

**Problem:** Multiple free parameters:
```python
P_infinity = 1.65e31  # Free parameter
volume_per_turbine = (4π/3) * (separation/2)^3  # Guessed
tau_char = 8.4e-16 / c  # Another free parameter
B = P_infinity * delta_sigma * volume * tau_char
```

**Fix:** Compute from field energy density integral:
```python
E = ∫ e(r) d³r = ∫ P(r) · σ(r) d³r
B = E_bound - E_free
```

**Key Changes:**
- Energy computed as spatial integral of `e = P · σ`
- No free parameters - uses field values and grid spacing
- Volume comes from grid: `dV = dx * dy * dz`

## Validation Strategy

### Magnetic Moments

1. **Calibrate once:** Run proton simulation, compute raw moment, set calibration
2. **Predict all:** Use same calibration for neutron, deuteron, triton, helion, alpha
3. **Compare ratios:** Check if `μ_n/μ_p`, `μ_d/μ_p` match experiment (not just absolute values)

### Binding Energies

1. **Compute ratios first:** `B_d/B_t`, `B_α/B_d` (less sensitive to absolute calibration)
2. **Then absolute:** Compare `B_d`, `B_t`, `B_α` to experiment
3. **Energy functional:** All energies from same `E = ∫ e d³r` formula

## Testing

To test the fixes:

```python
from sdt_navier import *

# Initialize fields with proton
fields = initialize_fields(64, 64, 64, dx=0.1e-15)
proton = ProtonTurbine((32, 32, 32), radius_cells=2.0)
add_turbine_source(fields, ...)

# Run simulation to equilibrium
solver = SDTNavierSolver(fields, equations)
solver.run_until(t_end=1e-21)

# Calibrate from proton
calibration = calibrate_from_proton(fields, proton.position, proton.radius_cells)

# Predict neutron (should give ~-1.913 μ_N)
# Predict deuteron (should give ~0.857 μ_N)
# etc.
```

## Next Steps

1. **Test magnetic moments:** Run proton/neutron/deuteron simulations, compare to experiment
2. **Test binding energies:** Compute ratios first, then absolute values
3. **Refine current density model:** Current `J ∝ σ × v` is simplified - may need curl-based model
4. **Improve Poisson solver:** Consider FFT for periodic BCs, or sparse solver for Dirichlet
5. **Add energy conservation check:** Monitor `dE/dt` to ensure energy is conserved

## Files Modified

- `magnetic_moments.py`: Field-integral method, calibration function
- `lattice.py`: Proper 12-axis interpolation
- `solver.py`: Proper Poisson projection
- `nuclear.py`: Field energy functional for binding energy
