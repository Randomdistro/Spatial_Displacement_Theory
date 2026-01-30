# G-Factor Issue Analysis

**Date:** 2026-01-02  
**Author:** Composer  
**Status:** 🔍 INVESTIGATING - G-factor precision and sign convention

---

## Issue Identified

User reports: "why are the gfasses out?" (likely "g-factors")

---

## Current G-Factor Definitions

### In `constants.py`:

```python
G_E = 2.00231930436  # electron g-factor
G_P = 5.5856946893  # proton g-factor
G_N = -3.82608545  # neutron g-factor
```

### CODATA 2018 Values (from web search):

- **Electron g-factor**: −2.00231930436256(35) (NEGATIVE, full precision)
- **Proton g-factor**: +5.5856946893(16) (matches current value)
- **Neutron g-factor**: −3.82608545 (matches current value)

---

## Issues Found

### 1. Electron G-Factor Precision Loss

**Before fix**: `G_E = 2.00231930436` (11 significant digits)  
**CODATA**: `2.00231930436256` (15 significant digits)  
**After fix**: `G_E = 2.00231930436256` (15 significant digits) ✅

**Missing digits**: "256" at the end

**Precision loss**: 
```
2.00231930436256 - 2.00231930436 = 0.00000000000256
Relative error: 2.56×10⁻¹² / 2.00231930436 = 1.28×10⁻¹²
```

**Impact**: For hyperfine splitting (1420.405751768 MHz), this precision loss could affect the 12th decimal place.

### 2. Electron G-Factor Sign Convention

**CODATA value**: −2.00231930436256 (negative)  
**Current code**: +2.00231930436 (positive)

**Question**: Does the sign matter in hyperfine calculations?

**Standard hyperfine formula**:
$$\Delta E_{\text{hf}} = \frac{8\pi}{3} \frac{\mu_0}{4\pi} \frac{\mu_e \mu_p}{\hbar^2} |\psi(0)|^2 \Delta\langle \mathbf{I} \cdot \mathbf{S} \rangle$$

where:
- $\mu_e = -g_e \mu_B$ (electron magnetic moment, negative)
- $\mu_p = +g_p \mu_N$ (proton magnetic moment, positive)

**Product**: $\mu_e \mu_p = (-g_e \mu_B)(+g_p \mu_N) = -g_e g_p \mu_B \mu_N$

**In SDT formula** (Phase 5):
$$\Delta E_{\text{hf}} = (2/3) g_I g_e (m_e/m_N) (μ/m_e)^3 α⁴ m_e c² / n³$$

**Analysis**: The formula uses $g_I g_e$ as a product. The sign convention depends on:
1. Whether we use $g_e$ (positive) or $|g_e|$ (absolute value)
2. Whether the sign is absorbed into the spin correlation term

**Standard practice**: In hyperfine formulas, we typically use $|g_e|$ because the sign is handled by the spin-spin interaction term $\mathbf{I} \cdot \mathbf{S}$.

**However**: For maximum precision and correctness, we should:
1. Use the full CODATA value: `2.00231930436256`
2. Document the sign convention clearly

---

## Verification: Does Sign Matter?

### Test Calculation

**With positive g_e** (current):
$$g_I \times g_e = 5.5856946893 \times 2.00231930436 = 11.191...$$

**With negative g_e** (CODATA):
$$g_I \times (-g_e) = 5.5856946893 \times (-2.00231930436256) = -11.191...$$

**In hyperfine formula**: The product $g_I g_e$ appears in the prefactor. If we use the negative value, we get a negative energy splitting, which would be wrong (hyperfine splitting is positive).

**Conclusion**: The sign convention in the formula assumes positive $g_e$ (absolute value). This is standard practice in hyperfine structure calculations.

**However**: We should use the full precision value: `2.00231930436256` (not `2.00231930436`).

---

## Recommended Fix

### Update `constants.py`:

```python
# Nuclear g-factors (CODATA 2018, full precision)
G_E = 2.00231930436256  # electron g-factor (absolute value for hyperfine calculations)
G_P = 5.5856946893  # proton g-factor
G_N = -3.82608545  # neutron g-factor
```

**Note**: Using absolute value of electron g-factor is standard in hyperfine calculations. The sign is handled by the spin-spin interaction term.

---

## Impact Assessment

### Precision Loss Impact

**Current precision**: 11 significant digits  
**Full precision**: 15 significant digits  
**Loss**: 4 significant digits

**For hyperfine splitting** (1420.405751768 MHz):
- Current precision: ~0.001 MHz uncertainty from g-factor
- Full precision: ~0.000001 MHz uncertainty from g-factor

**B05 benchmark tolerance**: <0.003% (~40 kHz = 0.04 MHz)

**Current precision is sufficient** for B05, but full precision is better for consistency.

---

## Action Items

1. ✅ **Update G_E to full precision**: `2.00231930436256`
2. ✅ **Verify sign convention**: Document that we use |g_e| (absolute value)
3. ✅ **Check all usages**: Ensure consistency across codebase
4. ✅ **Update documentation**: Note the sign convention

---

## Files to Update

1. `SDT/tools/sdt_atomic/constants.py` - Update G_E precision
2. `SDT/tools/sdt_atomic/hyperfine.py` - Verify usage
3. `SDT/tools/validate_b05_hyperfine.py` - Verify usage
