# Gas Constants Fix

**Date:** 2026-01-02  
**Author:** Composer  
**Status:** ✅ FIXED - Added missing gas constants to constants.py

---

## Issue Identified

User reported: "why are the gasses out?" (typo for "gases")

**Root cause**: Boltzmann constant (`k_B`) and ideal gas constant (`R`) were missing from `SDT/tools/sdt_atomic/constants.py`.

---

## Problem

### Missing Constants

The main constants file `SDT/tools/sdt_atomic/constants.py` was missing:
1. **Boltzmann constant** (`k_B`) - Used in thermodynamics, statistical mechanics
2. **Ideal gas constant** (`R`) - Used in ideal gas law, thermodynamics

### Impact

- Files like `nuclear_driven_chemistry_calculations.py` and `verify_all_benchmarks.py` had to define `k_B` locally
- No centralized definition for gas-related constants
- Inconsistent values across files

---

## Fix Applied

### Added to `SDT/tools/sdt_atomic/constants.py`:

```python
# Thermodynamic constants (CODATA 2018)
K_B = 1.380649e-23  # J/K (Boltzmann constant)
R_GAS = 8.314462618  # J/(mol·K) (Ideal gas constant, molar gas constant)
```

**CODATA 2018 values**:
- **Boltzmann constant**: `k_B = 1.380649 × 10⁻²³ J/K` (exact)
- **Ideal gas constant**: `R = 8.314462618 J/(mol·K)` (exact)

**Relationship**: `R = N_A × k_B` where `N_A` is Avogadro's number

---

## Usage

### Boltzmann Constant (`K_B`)

Used in:
- Statistical mechanics: `E = (3/2) k_B T` (kinetic energy per particle)
- Boltzmann distribution: `P(E) ∝ exp(-E / k_B T)`
- Entropy: `S = k_B ln(W)`
- Mean free path calculations
- Temperature-energy conversions

### Ideal Gas Constant (`R_GAS`)

Used in:
- Ideal gas law: `PV = nRT`
- Thermodynamic calculations per mole
- Chemical reaction thermodynamics
- Phase transition calculations

---

## Files That Can Now Import

All files can now import from `constants.py`:

```python
from sdt_atomic.constants import K_B, R_GAS

# Example: Ideal gas law
P = n * R_GAS * T / V

# Example: Kinetic energy
E_kinetic = (3/2) * K_B * T
```

---

## Files Previously Using Local Definitions

These files had local definitions that can now be removed (or kept for backward compatibility):

1. `SDT/investigations/nuclear_driven_chemistry_calculations.py`:
   ```python
   k_B = 1.380649e-23  # J/K
   ```
   → Can now use `from sdt_atomic.constants import K_B`

2. `SDT/benchmarks/Claude_Verification/verify_all_benchmarks.py`:
   ```python
   K_B = 1.380649e-23  # Boltzmann constant (J/K)
   ```
   → Can now use `from sdt_atomic.constants import K_B`

---

## Summary

**Issue**: Missing gas constants (k_B, R) in main constants file  
**Fix**: Added `K_B` and `R_GAS` to `constants.py` with CODATA 2018 values  
**Status**: ✅ FIXED - Gas constants now available for import  
**Impact**: Centralized constants, consistent values across codebase
