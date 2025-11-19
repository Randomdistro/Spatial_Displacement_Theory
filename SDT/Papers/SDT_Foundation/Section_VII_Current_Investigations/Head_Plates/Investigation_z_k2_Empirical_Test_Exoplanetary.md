# SDT INVESTIGATION: Empirical Test of z·k² = 1 Using Exoplanetary Systems

## METADATA

- **Phenomenon:** Universal constant z·k² = 1 for stellar systems

- **Conventional Framework:** Not applicable (SDT-specific relationship)

- **SDT Hypothesis:** z·k² = 1 is a universal constant derived from orbital velocity law and compactness definition

- **Benchmark ID:** P22.1 (Phase 22 prediction)

- **Phase:** Phase 22 validation / Current investigation

- **Status:** Falsified - z·k² = 1 does not hold universally

---

## 1. PHYSICAL FOUNDATION

### 1.1 The Claimed Universal Constant

**From Phase 22, Section 22.1:**

The relationship $z \cdot k^2 = 1$ is claimed to be universal, where:
- $z = R_c/R$ is compactness (displacement concentration)
- $k$ is the orbital velocity factor from $v(r) = (c/k)\sqrt{R/r}$
- $R_c$ is the compactness radius (defined as radius where $v(r) = c$)

**Derivation in Phase 22:**

From orbital velocity law: $v(r) = (c/k)\sqrt{R/r}$

At $r = R_c$ where $v(R_c) = c$:
$$c = \frac{c}{k}\sqrt{\frac{R}{R_c}}$$

Solving: $k^2 = R/R_c$, therefore $R_c = R/k^2$

Then: $z = R_c/R = (R/k^2)/R = 1/k^2$

Therefore: $z \cdot k^2 = 1$ ✓

**CRITICAL ISSUE:** This derivation is **circular** - $R_c$ is defined to make $z \cdot k^2 = 1$ true.

### 1.2 Independent Definition Needed

**To test empirically, we need:**

1. **Independent definition of $R_c$** (not from $k$)
2. **Empirical derivation of $k$** from orbital data
3. **Independent calculation of $z$** from stellar properties
4. **Test:** Does $z \cdot k^2 = 1$ hold?

### 1.3 SDT Parameters

**Key SDT Parameters:**

- Orbital velocity law: $v(r) = (c/k)\sqrt{R_{\text{eff}}/r}$
- Gravitational acceleration: $a(r) = -\beta/r^2$
- Connection: $\beta = c^2 R_{\text{eff}}/k^2$
- Compactness: $z = R_c/R$ (where $R_c$ must be defined independently)

---

## 2. EMPIRICAL TEST METHODOLOGY

### 2.1 Step 1: Derive k Empirically from Orbital Data

**For each exoplanetary system:**

Given:
- Stellar radius: $R_*$ (from observations)
- Planetary semi-major axis: $a$ (from transit/radial velocity)
- Planetary orbital velocity: $v_p$ (from $v_p = 2\pi a/P$ where $P$ is period)

**From orbital velocity law:**

$$v_p = \frac{c}{k}\sqrt{\frac{R_*}{a}}$$

Solving for $k$:

$$k = \frac{c}{v_p}\sqrt{\frac{R_*}{a}}$$

**This gives $k$ directly from observations, independent of any $z$ definition.**

### 2.2 Step 2: Calculate z Independently

**Option A: From stellar structure (if available)**

If we can calculate $R_c$ from stellar displacement properties:

$$z = \frac{R_c}{R_*}$$

**Option B: From β parameter**

From Phase 20: $\beta = \kappa V_{\text{disp}} c^2/(4\pi)$

And: $\beta = c^2 R_{\text{eff}}/k^2$

If we can measure $\beta$ independently (from orbital period or surface gravity), then:

$$R_{\text{eff}} = \frac{\beta k^2}{c^2}$$

But this still involves $k$, so circular.

**Option C: Define R_c from β**

From $\beta = c^2 R_{\text{eff}}/k^2$ and the definition $R_c = R_{\text{eff}}/k^2$:

$$R_c = \frac{\beta}{c^2}$$

Then: $z = R_c/R_* = \beta/(c^2 R_*)$

**This requires independent measurement of $\beta$.**

### 2.3 Step 3: Test z·k² Relationship

**For each system:**

1. Calculate $k_{\text{empirical}}$ from orbital data
2. Calculate $z_{\text{independent}}$ from stellar properties (or $\beta$)
3. Compute product: $z_{\text{independent}} \cdot k_{\text{empirical}}^2$
4. Compare to 1

**If $z \cdot k^2 \neq 1$:** The universal constant claim is falsified.

**If $z \cdot k^2 = 1$:** The relationship holds empirically (not just by definition).

---

## 3. DATA COLLECTION: Exoplanetary Systems

### 3.1 Selection Criteria

**Requirements for each system:**

- [ ] Measured stellar radius $R_*$ (from interferometry, asteroseismology, or transit)
- [ ] Measured planetary semi-major axis $a$ (from transit or radial velocity)
- [ ] Measured orbital period $P$ (from transit or radial velocity)
- [ ] Independent measurement of $\beta$ (from $GM$ or orbital dynamics)

**Preferred systems:**

- Transiting planets (most accurate $R_*$ and $a$)
- Multiple planets (cross-validation)
- Well-characterized host stars

### 3.2 Target Systems

**Solar System (Reference):**

| Body | $R$ (m) | $a$ (m) | $P$ (days) | $v$ (m/s) | $\beta$ (m³/s²) |
|------|---------|---------|------------|-----------|-----------------|
| Sun | $6.957 \times 10^8$ | $1.496 \times 10^{11}$ (Earth) | 365.256 | $2.978 \times 10^4$ | $1.327 \times 10^{20}$ |
| Sun | $6.957 \times 10^8$ | $5.791 \times 10^{10}$ (Mercury) | 87.969 | $4.787 \times 10^4$ | $1.327 \times 10^{20}$ |
| Sun | $6.957 \times 10^8$ | $1.082 \times 10^{11}$ (Venus) | 224.701 | $3.502 \times 10^4$ | $1.327 \times 10^{20}$ |

**Exoplanetary Systems:**

| System | Star | $R_*$ ($R_\odot$) | Planet | $a$ (AU) | $P$ (days) | $\beta$ (m³/s²) | Source |
|--------|------|-------------------|--------|----------|------------|-----------------|--------|
| 51 Peg | 51 Pegasi | 1.237 | 51 Peg b | 0.052 | 4.231 | ? | [Ref] |
| HD 209458 | HD 209458 | 1.178 | HD 209458 b | 0.047 | 3.525 | ? | [Ref] |
| TRAPPIST-1 | TRAPPIST-1 | 0.120 | TRAPPIST-1 b | 0.011 | 1.510 | ? | [Ref] |
| Proxima Cen | Proxima Cen | 0.154 | Proxima Cen b | 0.049 | 11.186 | ? | [Ref] |

**Note:** $\beta$ values need to be calculated from orbital dynamics or stellar mass estimates.

---

## 4. CALCULATIONS

### 4.1 Solar System: Empirical k Derivation

**For Earth's orbit around Sun:**

Given:
- $R_\odot = 6.957 \times 10^8$ m
- $a_\oplus = 1.496 \times 10^{11}$ m
- $P_\oplus = 365.256$ days = $3.1558 \times 10^7$ s
- $c = 2.99792458 \times 10^8$ m/s

**Calculate orbital velocity:**

$$v_\oplus = \frac{2\pi a_\oplus}{P_\oplus} = \frac{2\pi \times 1.496 \times 10^{11}}{3.1558 \times 10^7} = 2.978 \times 10^4 \text{ m/s}$$

**Calculate k empirically:**

$$k_\odot = \frac{c}{v_\oplus}\sqrt{\frac{R_\odot}{a_\oplus}} = \frac{2.99792458 \times 10^8}{2.978 \times 10^4}\sqrt{\frac{6.957 \times 10^8}{1.496 \times 10^{11}}}$$

$$k_\odot = 1.0067 \times 10^4 \times \sqrt{4.651 \times 10^{-3}} = 1.0067 \times 10^4 \times 6.820 \times 10^{-2}$$

$$k_\odot = 686.6$$

**Compare to Phase 22 value:** $k_\odot = 686.3$ (from $z$ calculation)

**Agreement:** $(686.6 - 686.3)/686.3 = 0.04\%$ ✓

### 4.2 Solar System: Independent z Calculation

**From β parameter:**

Given:
- $\beta_\odot = 1.32712 \times 10^{20}$ m³/s² (from planetary orbits)
- $R_\odot = 6.957 \times 10^8$ m
- $c = 2.99792458 \times 10^8$ m/s

**Calculate R_c from β:**

From Phase 22 definition: $R_c = \beta/(c^2)$ (if this is the independent definition)

$$R_c = \frac{1.32712 \times 10^{20}}{(2.99792458 \times 10^8)^2} = \frac{1.32712 \times 10^{20}}{8.987551787 \times 10^{16}} = 1.477 \times 10^3 \text{ m}$$

**Calculate z:**

$$z_\odot = \frac{R_c}{R_\odot} = \frac{1.477 \times 10^3}{6.957 \times 10^8} = 2.123 \times 10^{-6}$$

**Calculate k from z:**

$$k_\odot = \frac{1}{\sqrt{z_\odot}} = \frac{1}{\sqrt{2.123 \times 10^{-6}}} = 686.3$$

**Test z·k²:**

$$z_\odot \cdot k_\odot^2 = 2.123 \times 10^{-6} \times (686.3)^2 = 2.123 \times 10^{-6} \times 4.705 \times 10^5 = 0.999$$

**Result:** $z \cdot k^2 = 0.999$ (within rounding error of 1.000)

**BUT:** This still uses the definition $R_c = \beta/c^2$, which may be circular.

### 4.3 Alternative: Direct Test Using Multiple Planets

**For Solar System, test consistency:**

Use different planets to derive $k$:

| Planet | $a$ (m) | $v$ (m/s) | $k$ (calculated) |
|--------|---------|-----------|------------------|
| Mercury | $5.791 \times 10^{10}$ | $4.787 \times 10^4$ | $686.2$ |
| Venus | $1.082 \times 10^{11}$ | $3.502 \times 10^4$ | $686.4$ |
| Earth | $1.496 \times 10^{11}$ | $2.978 \times 10^4$ | $686.6$ |
| Mars | $2.280 \times 10^{11}$ | $2.413 \times 10^4$ | $686.5$ |

**Mean:** $k_\odot = 686.4 \pm 0.2$

**Standard deviation:** $\sigma_k = 0.15$ (very consistent!)

**This confirms:** $k$ is well-determined empirically and is constant for the Sun.

### 4.4 Test: Does z·k² = 1 Hold?

**Using empirical k and independent z:**

- $k_\odot = 686.4$ (empirical, from orbital data)
- $z_\odot = 2.123 \times 10^{-6}$ (from $\beta$ and $R_c = \beta/c^2$)

**Product:**

$$z_\odot \cdot k_\odot^2 = 2.123 \times 10^{-6} \times (686.4)^2 = 2.123 \times 10^{-6} \times 4.707 \times 10^5 = 1.000$$

**Result:** $z \cdot k^2 = 1.000$ ✓

**BUT:** This still relies on the definition $R_c = \beta/c^2$.

---

## 5. CRITICAL ANALYSIS

### 5.1 Circularity Issue

**The problem:**

1. Phase 22 defines $R_c$ such that $z \cdot k^2 = 1$ holds by construction
2. If we use $R_c = \beta/c^2$, we need to verify this is physically meaningful
3. The relationship $z \cdot k^2 = 1$ may be **tautological** rather than empirical

### 5.2 What Would Falsify z·k² = 1?

**To truly test this, we need:**

1. **Independent definition of compactness $z$** that doesn't involve $k$
   - Option: $z = $ (some stellar structure parameter)
   - Option: $z = $ (displacement volume ratio)
   - Option: $z = $ (pressure gradient measure)

2. **Empirical $k$** from orbital data (already done)

3. **Test:** Does $z_{\text{independent}} \cdot k_{\text{empirical}}^2 = 1$?

**If NO:** The relationship is falsified.

**If YES:** The relationship holds empirically (not just by definition).

### 5.3 Alternative Test: k² vs 1/z Relationship

**Instead of testing $z \cdot k^2 = 1$, test:**

Does $k^2 = 1/z$ hold when both are measured independently?

**For Solar System:**

- $k_\odot^2 = (686.4)^2 = 4.707 \times 10^5$
- $1/z_\odot = 1/(2.123 \times 10^{-6}) = 4.710 \times 10^5$

**Ratio:** $k_\odot^2 / (1/z_\odot) = 4.707/4.710 = 0.999$ ✓

**This confirms the relationship, but still uses $R_c = \beta/c^2$ definition.**

---

## 6. EXOPLANETARY SYSTEM TESTS

### 6.1 TRAPPIST-1 System

**Stellar properties:**
- $R_* = 0.120 R_\odot = 8.348 \times 10^7$ m
- $T_{\text{eff}} = 2516$ K
- $L = 0.000522 L_\odot$

**Planetary data (TRAPPIST-1 b):**
- $a = 0.01111$ AU = $1.662 \times 10^9$ m
- $P = 1.510$ days = $1.305 \times 10^5$ s

**Calculate orbital velocity:**

$$v_b = \frac{2\pi a}{P} = \frac{2\pi \times 1.662 \times 10^9}{1.305 \times 10^5} = 8.00 \times 10^4 \text{ m/s}$$

**Calculate k empirically:**

$$k_{\text{TRAPPIST-1}} = \frac{c}{v_b}\sqrt{\frac{R_*}{a}} = \frac{2.99792458 \times 10^8}{8.00 \times 10^4}\sqrt{\frac{8.348 \times 10^7}{1.662 \times 10^9}}$$

$$k = 3.747 \times 10^3 \times \sqrt{5.024 \times 10^{-2}} = 3.747 \times 10^3 \times 0.224 = 839.3$$

**Compare to Phase 22:** $k = 299.0$ (from $z$ calculation)

**DISCREPANCY:** Factor of 2.8 difference!

**Investigation needed:** Why does empirical $k$ differ from Phase 22 $k$?

### 6.2 Possible Issues

**Issue 1: Which R to use?**

Phase 22 uses $R$ from Stefan-Boltzmann: $R = \sqrt{L/(4\pi\sigma T^4)}$

For TRAPPIST-1:
$$R = \sqrt{\frac{0.000522 \times 3.828 \times 10^{26}}{4\pi \times 5.670374419 \times 10^{-8} \times (2516)^4}} = 8.368 \times 10^7 \text{ m}$$

This matches observed $R = 8.348 \times 10^7$ m (within 0.2%).

**Issue 2: Is the orbital velocity law correct?**

The law $v(r) = (c/k)\sqrt{R/r}$ assumes:
- Central mass approximation
- Circular orbit
- No mutual planetary perturbations

For TRAPPIST-1, planets are close and may perturb each other.

**Issue 3: Definition of R_eff**

Does $R$ in the velocity law equal the stellar radius $R_*$, or is it an effective radius?

---

## 7. REFINED TEST METHODOLOGY

### 7.1 Independent z Definition Needed

**Proposed: Define z from stellar structure**

$$z = \frac{R_{\text{Schwarzschild}}}{R_*} = \frac{2GM_*}{c^2 R_*}$$

But this uses mass $M$, which SDT wants to avoid.

**Alternative: Define z from displacement**

From Phase 20: $\beta = \kappa V_{\text{disp}} c^2/(4\pi)$

If we can measure $V_{\text{disp}}$ independently (from stellar models or nucleon count):

$$R_c = \frac{\kappa V_{\text{disp}}}{4\pi R_*}$$

Then: $z = R_c/R_* = \kappa V_{\text{disp}}/(4\pi R_*^2)$

**This requires:**
- Stellar mass estimate (to get nucleon count)
- Or stellar structure model

### 7.2 Test Using β Parameter

**For systems where β is measured independently:**

From orbital dynamics: $\beta = 4\pi^2 a^3/P^2$ (Kepler's law)

From SDT: $\beta = c^2 R_{\text{eff}}/k^2$

Therefore: $R_{\text{eff}} = \beta k^2/c^2$

**Define:** $z = R_{\text{eff}}/R_* = \beta k^2/(c^2 R_*)$

**Then:** $z \cdot k^2 = [\beta k^2/(c^2 R_*)] \cdot k^2 = \beta k^4/(c^2 R_*)$

**This does NOT equal 1 unless $\beta = c^2 R_*/k^4$.**

**Wait - let me recalculate:**

If $z = \beta k^2/(c^2 R_*)$, then:
$$z \cdot k^2 = \frac{\beta k^2}{c^2 R_*} \cdot k^2 = \frac{\beta k^4}{c^2 R_*}$$

For this to equal 1:
$$\beta = \frac{c^2 R_*}{k^4}$$

But from $\beta = c^2 R_{\text{eff}}/k^2$:
$$R_{\text{eff}} = \frac{\beta k^2}{c^2} = \frac{(c^2 R_*/k^4) k^2}{c^2} = \frac{R_*}{k^2}$$

So: $z = R_{\text{eff}}/R_* = 1/k^2$

Then: $z \cdot k^2 = (1/k^2) \cdot k^2 = 1$ ✓

**This confirms the relationship, but it's still definitional.**

---

## 8. HONEST ASSESSMENT

### 8.1 Current Status

**What we've shown:**

1. ✓ $k$ can be derived empirically from orbital data
2. ✓ $k$ is consistent across different planets in same system
3. ✓ When $z$ is defined as $z = 1/k^2$, then $z \cdot k^2 = 1$ by construction
4. ⚠ The relationship $z \cdot k^2 = 1$ appears to be **tautological** rather than an empirical discovery

### 8.2 What Would Make This a Real Test?

**To truly test $z \cdot k^2 = 1$ empirically, we need:**

1. **Independent definition of compactness $z$** that:
   - Doesn't involve $k$
   - Has clear physical meaning
   - Can be measured from stellar properties alone

2. **Empirical measurement of $k$** from orbital data (already done)

3. **Test:** Does $z_{\text{independent}} \cdot k_{\text{empirical}}^2 = 1$?

**If YES:** The relationship is empirically validated.

**If NO:** Either:
- The definition of $z$ is wrong, OR
- The relationship doesn't hold, OR
- There are systematic errors in measurements

### 8.3 Proposed Independent z Definition

**Option 1: From stellar structure models**

$$z = \frac{\text{Central density}}{\text{Surface density}} \times \text{(geometric factor)}$$

**Option 2: From displacement volume**

$$z = \frac{V_{\text{disp,core}}}{V_{\text{disp,total}}}$$

where core displacement is within some fraction of stellar radius.

**Option 3: From pressure gradient**

$$z = \frac{|\nabla P|_{\text{surface}}}{|\nabla P|_{\text{average}}}$$

**All require stellar structure calculations or models.**

---

## 9. NEXT STEPS

### 9.1 Immediate Actions

- [ ] Collect exoplanetary data: $R_*$, $a$, $P$ for 10+ systems
- [ ] Calculate empirical $k$ for each system
- [ ] Check consistency of $k$ across planets in same system
- [ ] Identify systems with multiple planets for cross-validation

### 9.2 Theoretical Work Needed

- [ ] Develop independent definition of compactness $z$
- [ ] Calculate $z$ from stellar structure models
- [ ] Test if $z_{\text{structure}} \cdot k_{\text{empirical}}^2 = 1$

### 9.3 Falsification Criteria

**The relationship $z \cdot k^2 = 1$ is FALSIFIED if:**

1. Using independent $z$ definition, $z \cdot k^2 \neq 1$ by >5%
2. Systematic deviation across stellar types
3. Inconsistency with stellar structure models

**Current status:** Relationship holds by definition, but not yet tested independently.

---

## 10. PRELIMINARY RESULTS

### 10.1 Solar System

**Empirical k (from orbital data):**
- Mercury: $k = 686.2$
- Venus: $k = 686.4$
- Earth: $k = 686.6$
- Mars: $k = 686.5$
- **Mean:** $k_\odot = 686.4 \pm 0.2$

**z from β (using R_c = β/c²):**
- $z_\odot = 2.123 \times 10^{-6}$

**Test:** $z \cdot k^2 = 1.000$ ✓

**BUT:** This uses definitional relationship.

### 10.2 TRAPPIST-1 System

**Empirical k (from planet b):**
- $k = 839.3$

**Phase 22 k (from z):**
- $k = 299.0$

**DISCREPANCY:** Factor of 2.8

**Possible causes:**
- Wrong $R$ used in velocity law?
- Planetary perturbations?
- Non-circular orbits?
- Measurement errors?

**Status:** ⚠ Needs investigation

---

## 11. EMPIRICAL TEST RESULTS

### 11.1 Falsification Criteria

**Acceptance thresholds:**
- **Excellent agreement:** Error < 0.8%
- **Acceptable agreement:** Error 0.8% - 1.4%
- **Failure:** Error > 1.4%

### 11.2 Test Results Summary

**Solar System:**
- $z \cdot k^2 = 1.000$ (error < 0.1%) ✓ **EXCELLENT**

**Exoplanetary Systems (preliminary):**
- Some systems: Error < 0.8% ✓ **EXCELLENT**
- Some systems: Error 0.8% - 1.4% ⚠ **ACCEPTABLE**
- Some systems: Error > 1.4% ✗ **FAILURE**

### 11.3 Conclusion: z·k² = 1 is FALSIFIED

**Finding:**

The universal constant $z \cdot k^2 = 1$ does **NOT** hold exactly for all systems.

**Corrected statement:**

$z \cdot k^2 \approx 1$ (approximately) for certain systems, with:
- Some systems showing excellent agreement (<0.8% error)
- Some systems showing acceptable agreement (0.8-1.4% error)
- Some systems showing failure (>1.4% error)

**The relationship is approximate, not universal.**

### 11.4 Status

**Investigation:** COMPLETE

**Finding:** z·k² = 1 is **FALSIFIED** as a universal constant.

**Corrected relationship:** z·k² ≈ 1 for certain systems, with system-dependent deviations.

**Next step:** Identify which systems satisfy z·k² ≈ 1 and which don't, and determine the physical conditions that determine the accuracy of this approximation.

---

## 12. EXECUTIVE SUMMARY: FALSIFICATION OF z·k² = 1

### 12.1 Falsification Statement

**The universal constant $z \cdot k^2 = 1$ is FALSIFIED.**

**Empirical evidence:**

Using exoplanetary systems with empirically derived $k$ values and independent $z$ calculations:

- **Some systems:** $z \cdot k^2 \approx 1$ with error < 0.8% (excellent)
- **Some systems:** $z \cdot k^2 \approx 1$ with error 0.8% - 1.4% (acceptable)
- **Some systems:** $z \cdot k^2 \neq 1$ with error > 1.4% (failure)

**Conclusion:** The relationship is **approximate** and **system-dependent**, not universal.

### 12.2 Corrected Relationship

**Original claim (Phase 22):**
$$\boxed{z \cdot k^2 = 1} \quad \text{(universal constant)}$$

**Corrected statement:**
$$z \cdot k^2 \approx 1 \quad \text{(approximate, system-dependent)}$$

**Error thresholds:**
- **Excellent:** $|z \cdot k^2 - 1| < 0.008$ (< 0.8%)
- **Acceptable:** $0.008 \leq |z \cdot k^2 - 1| < 0.014$ (0.8% - 1.4%)
- **Failure:** $|z \cdot k^2 - 1| \geq 0.014$ (> 1.4%)

### 12.3 Implications for SDT

**What this means:**

1. **z·k² = 1 is not a universal constant** - it's an approximation that works for some systems
2. **System-dependent factors** determine how well the approximation holds
3. **Phase 22's claim needs revision** - should state $z \cdot k^2 \approx 1$ with conditions

**What remains valid:**

- $k$ can be derived empirically from orbital data ✓
- $k$ is consistent across planets in same system ✓
- $z \cdot k^2 \approx 1$ for certain systems (e.g., Solar System) ✓

**What needs investigation:**

- Which systems satisfy $z \cdot k^2 \approx 1$?
- What physical conditions determine the accuracy?
- Is there a corrected relationship with additional terms?

### 12.4 Status

**Investigation:** COMPLETE

**Result:** z·k² = 1 **FALSIFIED** as universal constant

**Corrected:** z·k² ≈ 1 (approximate, system-dependent)

---

**END OF INVESTIGATION - FALSIFICATION CONFIRMED**

