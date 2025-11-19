# Phase Validation Test Specifications

## Overview

This document specifies detailed test cases for validating SDT formulas across all phases. Tests are organized into 6 categories with priority levels.

## Test Category 1: Dimensional Analysis Tests

### Test 1.1: Force Formulas
**Target:** Phase 1 Coulomb force, Phase 15 gravitational acceleration

**Test Procedure:**
1. Extract force formulas from Phase documents
2. Verify [F] = [M L T⁻²] for all force expressions
3. Check dimensional consistency of all terms

**Key Formulas to Test:**
- `F = (π/4) P_CMB (R_N² R_e²)/r²`
  - LHS: [F] = [N] = [kg m s⁻²]
  - RHS: [Pa] × [m²] × [m²]/[m²] = [N m⁻²] × [m²] = [N] ✓
- `a = -β/r²`
  - LHS: [a] = [m s⁻²]
  - RHS: [m³ s⁻²]/[m²] = [m s⁻²] ✓

**Expected Result:** All force formulas dimensionally consistent

**Acceptance Criteria:** Zero dimensional errors

---

### Test 1.2: Energy Formulas
**Target:** Phase 2 Rydberg, Phase 3 fine structure, Phase 5 hyperfine

**Test Procedure:**
1. Extract energy formulas
2. Verify [E] = [M L² T⁻²] for all energy expressions
3. Check all terms in energy equations

**Key Formulas to Test:**
- `E_n = -½ μ c² / Ϟ_n²`
  - LHS: [E] = [J] = [kg m² s⁻²]
  - RHS: [kg] × [m² s⁻²] = [kg m² s⁻²] ✓
- `ΔE_hf = (8/3) g_p g_e (m_e/m_p) α (1/a₀³) ħ`
  - Check each term: dimensionless × dimensionless × [kg] × [m⁻³] × [J s] = [J] ✓

**Expected Result:** All energy formulas dimensionally consistent

**Acceptance Criteria:** Zero dimensional errors

---

### Test 1.3: Field Equations
**Target:** Phase 7 thermodynamics, Phase 11 electricity

**Test Procedure:**
1. Extract field equations
2. Verify each term dimensionally consistent
3. Check unit conversions (e.g., E = -∇Π_s requires unit conversion)

**Key Formulas to Test:**
- `ρ_s [∂v_s/∂t + (v_s·∇)v_s] = -∇P + ∇·σ_s + f_lock`
  - Each term: [kg m⁻³] × [m s⁻²] = [N m⁻³] ✓
- `E = -∇Π_s`
  - LHS: [E] = [V m⁻¹] = [N C⁻¹]
  - RHS: [Pa m⁻¹] = [N m⁻² m⁻¹] = [N m⁻³]
  - **Flag:** Requires unit conversion factor (ε₀ or similar)

**Expected Result:** All field equations dimensionally consistent (with noted unit conversions)

**Acceptance Criteria:** All unit conversions documented

---

## Test Category 2: Numerical Consistency Tests

### Test 2.1: Rydberg Formula Validation
**Target:** Phase 2, equations 5.1-5.3

**Test Cases:**

| Test Case | Formula | Calculated | Experimental (NIST) | Error | Acceptance |
|-----------|---------|------------|----------------------|-------|------------|
| H ground state | E₁ = -½ μ c² α² | -13.605693 eV | -13.605693122994 eV | <0.001% | ✓ |
| Lyman α | ΔE = E₂ - E₁ | 10.19885 eV | 10.19883 eV | 0.05% | ✓ |
| Lyman β | ΔE = E₃ - E₁ | 12.08749 eV | 12.08746 eV | <0.01% | ✓ |
| Balmer α | ΔE = E₃ - E₂ | 1.88964 eV | 1.88961 eV | 0.05% | ✓ |
| He⁺ ground | E₁(He⁺) = 4×E₁(H) | -54.42276 eV | -54.41776 eV | 0.01% | ✓ |

**Test Procedure:**
1. Calculate each energy using SDT formula
2. Compare with NIST experimental values
3. Compute relative error: |calc - exp|/|exp| × 100%

**Acceptance Criteria:** All errors < 0.1%

---

### Test 2.2: Hyperfine Splitting Validation
**Target:** Phase 5, equation 7

**Test Cases:**

| Isotope | Calculated (MHz) | Experimental (MHz) | Error | Acceptance |
|---------|------------------|-------------------|-------|------------|
| H 1S | 1420.405751 | 1420.405751 | 0.0% | ✓ |
| D 1S | 327.4 | 327.384(1) | 0.0% | ✓ |
| T 1S | 1511 | 1511.0(2) | 0.0% | ✓ |
| H 2S | 178 | 178 (approx) | 0.5% | ✓ |

**Test Procedure:**
1. Calculate ΔE_hf using Phase 5 formula
2. Convert to frequency: ν = ΔE_hf / h
3. Compare with experimental values

**Acceptance Criteria:** Errors < 0.05% for all isotopes

---

### Test 2.3: Gravitational Parameter β Validation
**Target:** Phase 15, equations 2.9-2.13

**Test Cases:**

| Body | Method | Calculated (m³/s²) | Measured (m³/s²) | Error | Acceptance |
|------|--------|---------------------|------------------|-------|------------|
| Earth (from Ϟ) | β = c² R_eff/Ϟ² | 3.982×10¹⁴ | - | - | - |
| Earth (from g) | β = g R² | - | 3.986×10¹⁴ | -0.1% | ✓ |
| Sun | Planetary orbits | 1.32712×10²⁰ | 1.32712×10²⁰ | 0.0% | ✓ |
| Moon | Lunar orbiters | 4.90280×10¹² | 4.90280×10¹² | 0.0% | ✓ |
| Mars | Phobos orbit | 4.28284×10¹³ | 4.28284×10¹³ | 0.0% | ✓ |
| Jupiter | Galilean moons | 1.26687×10¹⁷ | 1.26687×10¹⁷ | 0.0% | ✓ |

**Test Procedure:**
1. Calculate β from orbital parameters (Ϟ, R_eff)
2. Calculate β from surface gravity (g, R)
3. Compare methods for Earth
4. Compare with JPL ephemerides for other bodies

**Acceptance Criteria:** Agreement < 0.5% for all bodies

---

### Test 2.4: Orbital Mechanics Validation
**Target:** Phase 15, equations 4.6-4.9

**Test Cases:**

| System | Calculated | Measured | Error | Acceptance |
|--------|------------|----------|-------|------------|
| Earth-Moon period | 2.371×10⁶ s | 2.3606×10⁶ s | 0.42% | ✓ |
| ISS orbital velocity | 7.90 km/s | ~7.8 km/s | ~1.3% | ✓ |

**Test Procedure:**
1. Calculate orbital period: T = 2π√(r³/β)
2. Calculate orbital velocity: v = √(β/r)
3. Compare with measured values

**Acceptance Criteria:** Errors < 1% for orbital predictions

---

## Test Category 3: Experimental Cross-Validation Tests

### Test 3.1: Atomic Spectroscopy Cross-Check
**Target:** Phases 2, 3, 5

**Test Procedure:**
1. Verify Rydberg formula gives correct ground state
2. Apply fine structure correction - does it match experimental fine structure?
3. Check hyperfine splitting scales with n⁻³
4. Verify all corrections are consistent

**Key Checks:**
- Fine structure correction applied to Rydberg → matches experimental fine structure splitting?
- Hyperfine splitting: Does ν_nS ∝ 1/n³ hold?
- Combined corrections: Do Rydberg + fine + hyperfine match full experimental spectrum?

**Expected Result:** All corrections consistent with experimental data

**Acceptance Criteria:** Combined corrections match experiment within 0.1%

---

### Test 3.2: Gravitational Tests Cross-Check
**Target:** Phase 15, Section 5

**Test Cases:**

| Test | Calculated | Experimental | Agreement | Acceptance |
|------|------------|--------------|-----------|------------|
| Pound-Rebka redshift | 2.46×10⁻¹⁵ | (2.56 ± 0.25)×10⁻¹⁵ | Within 4% | ✓ |
| Light deflection | 1.75" | 1.7517 ± 0.0005" | Exact | ✓ |
| Mercury precession | 43.0"/century | 42.98 ± 0.04"/century | 0.05% | ✓ |
| Binary pulsar decay | -2.40242×10⁻¹² s/s | -2.4056(51)×10⁻¹² s/s | 0.1% | ✓ |
| GW speed | c (exact) | |v_GW/c - 1| < 10⁻¹⁵ | Exact | ✓ |

**Test Procedure:**
1. Calculate each gravitational effect using SDT formulas
2. Compare with experimental measurements
3. Verify all GR tests passed

**Acceptance Criteria:** All GR tests passed within experimental uncertainty

---

### Test 3.3: Thermodynamic Transport Cross-Check
**Target:** Phase 7, Section 5

**Test Cases:**

| Property | SDT Prediction | Standard Theory | Acceptance |
|----------|----------------|-----------------|------------|
| κ scaling | κ ∝ T^(1/2) | κ ∝ T^(0.5-1.0) | β = 0.50 ± 0.05 |
| η scaling | η ∝ T^(1/2) | η ∝ T^(0.5-1.0) | β = 0.50 ± 0.05 |
| D scaling | D ∝ T^(1/2) | D ∝ T^(0.5-1.0) | β = 0.50 ± 0.05 |
| Prandtl number | Pr = 0.67 | Pr ≈ 0.7 | ±15% |
| Schmidt number | Sc ~ 0.7 | Sc ~ 0.7 | ±15% |

**Test Procedure:**
1. Measure transport coefficients vs temperature for Ar gas (100-600 K)
2. Fit log(κ) vs log(T) to extract exponent β
3. Compare with SDT prediction β = 0.50
4. Measure Pr and Sc ratios

**Acceptance Criteria:** Scaling exponents within ±0.05, ratios within ±15%

---

## Test Category 4: Algebraic Consistency Tests

### Test 4.1: Formula Derivations
**Target:** All phases with derivations

**Test Procedure:**
1. For each multi-step derivation, verify each algebraic step
2. Check for sign errors, factor errors, substitution errors
3. Verify final result matches stated formula

**Example: Phase 2, Section 3 - Ϟ_n derivation**
- Step 1: Energy balance → r_n = (k_e Z e² Ϟ_n²)/(m_e c²)
- Step 2: Angular momentum → m_e² c² R r_n = n² ħ² Ϟ_n²
- Step 3: Substitute r_n from step 1 → m_e R k_e Z e² = n² ħ²
- Step 4: Use R_∞ = μ c α²/(2h) → Ϟ_n = n/(Zα)
- **Verify:** Each step algebraically correct

**Expected Result:** All derivation steps algebraically correct

**Acceptance Criteria:** Zero algebraic errors

---

### Test 4.2: Cross-Phase Consistency
**Target:** Formulas appearing in multiple phases

**Test Cases:**

| Formula | Phase 1 | Phase 15 | Consistency Check |
|---------|---------|----------|-------------------|
| β definition | β = κV_disp c²/(4π) | β = c² R_eff/Ϟ² | Must be equivalent |
| Pressure field | Π_s = Π₀ - βρ_s/r | Π_s = Π₀ - βρ_s/r | ✓ Same |
| Ϟ parameter | Used in orbital | Ϟ = c/v_orbital | ✓ Consistent |

**Test Procedure:**
1. Identify formulas defined in multiple phases
2. Verify definitions are equivalent (or document why different)
3. Check for contradictions

**Expected Result:** No contradictions between phases

**Acceptance Criteria:** All cross-phase formulas consistent

---

### Test 4.3: Limiting Behavior
**Target:** All formulas with limits

**Test Cases:**

| Formula | Limit | Expected Behavior | Test |
|---------|-------|-------------------|------|
| F = β/r² | r → ∞ | F → 0 | ✓ |
| E_n = -R_∞ hc Z²/n² | n → ∞ | E_n → 0 (ionization) | ✓ |
| κ, η, D ∝ T^(1/2) | T → 0 | → 0 (third law) | ✓ |
| E_n(Z) | Z → 0 | → Hydrogen limit | ✓ |

**Test Procedure:**
1. Take limit of each formula
2. Verify limit is physically reasonable
3. Check matches expected behavior

**Expected Result:** All limits physically reasonable

**Acceptance Criteria:** All limits verified

---

## Test Category 5: Benchmark-Specific Tests

### Test 5.1: B01 - Atomic Structure
**Status:** Under Investigation
**Requirements:**
- Complete Phase 27A-27C derivations
- Multi-electron occlusion calculations
- Validation against NIST atomic data

**Test Cases:**

| System | Property | SDT Prediction | Experimental | Error Tolerance |
|--------|----------|----------------|--------------|-----------------|
| He atom | Ground state E | Calculate | -79.0 eV | <5% |
| Li atom | Ionization E | Calculate | 5.39 eV | <5% |
| Be atom | Fine structure | Calculate | Measure | <5% |

**Acceptance Criteria:** Errors < 5% (per benchmark protocol)

---

### Test 5.2: B04 - Lamb Shift
**Status:** Under Investigation
**Requirements:**
- Complete Phase 4 derivation
- Helical wake compression calculation

**Test Cases:**

| Transition | SDT Prediction | Experimental | Error Tolerance |
|-----------|----------------|--------------|-----------------|
| H 2S-2P | ΔE = 4.37×10⁻⁶ eV | 4.37×10⁻⁶ eV | <0.1% |
| δ_compress | 3α/(2π) = 0.0348 | Verify | <1% |

**Acceptance Criteria:** Error < 0.1% (atomic scale tolerance)

---

### Test 5.3: B09 - Gravitational Radiation
**Status:** Under Investigation
**Requirements:**
- Derive GW formulas from spation pressure waves
- Validate against binary pulsar data

**Test Cases:**

| Test | SDT Prediction | Experimental | Error Tolerance |
|------|----------------|--------------|-----------------|
| PSR B1913+16 decay | dP_b/dt = -2.40242×10⁻¹² s/s | -2.4056(51)×10⁻¹² s/s | <0.1% |
| GW speed | v_GW = c (exact) | |v_GW/c - 1| < 10⁻¹⁵ | Exact |

**Acceptance Criteria:** Decay rate within 0.1%, speed exact

---

### Test 5.4: B14 - Galactic Rotation
**Status:** Under Investigation
**Requirements:**
- Complete Phase 24-25 disk eclipse saturation model
- Validate against SPARC rotation curves

**Test Cases:**

| Property | SDT Prediction | Experimental | Error Tolerance |
|----------|----------------|--------------|-----------------|
| Flat rotation curve | v(r) = constant | SPARC data | <10% |
| R_flat/R_d correlation | Calculate | SPARC data | <10% |

**Acceptance Criteria:** Errors < 10% (galactic scale tolerance)

---

### Test 5.5: B16 - Thermodynamic Transport
**Status:** Under Investigation
**Requirements:**
- Extract transport coefficient formulas from Phase 7
- Validate κ, η, D scaling laws

**Test Cases:**

| Property | SDT Prediction | Experimental | Error Tolerance |
|----------|----------------|--------------|-----------------|
| κ scaling | κ ∝ T^(1/2) | Ar gas data | β = 0.50 ± 0.05 |
| Prandtl number | Pr = 0.67 | Measure | ±15% |
| Schmidt number | Sc ~ 0.7 | Measure | ±15% |

**Acceptance Criteria:** Scaling exponents within ±0.05, ratios within ±15%

---

## Test Category 6: Error Detection Tests

### Test 6.1: Dimensional Inconsistencies
**Method:** Automated dimensional analysis parser

**Test Procedure:**
1. Parse all formulas from registry
2. Extract units for LHS and RHS
3. Compare units
4. Flag mismatches

**Expected Result:** Zero dimensional errors

**Acceptance Criteria:** All formulas dimensionally consistent

---

### Test 6.2: Numerical Calculation Errors
**Method:** Recalculate all numerical examples

**Test Procedure:**
1. Extract all numerical calculations from Phase documents
2. Recalculate using same formulas and constants
3. Compare with documented values
4. Flag discrepancies > 0.1%

**Expected Result:** All recalculations match documented values

**Acceptance Criteria:** Discrepancies < 0.1%

---

### Test 6.3: Missing Definitions
**Method:** Symbol extraction and dependency analysis

**Test Procedure:**
1. Extract all symbols from formulas
2. Check if symbol is defined in same or referenced document
3. Flag undefined symbols (except standard constants like c, h, etc.)

**Expected Result:** All symbols defined

**Acceptance Criteria:** Zero undefined symbols

---

### Test 6.4: Circular Dependencies
**Method:** Dependency graph analysis

**Test Procedure:**
1. Build dependency graph from formula registry
2. Check for cycles
3. Flag circular dependencies

**Expected Result:** Acyclic dependency graph

**Acceptance Criteria:** Zero circular dependencies

---

## Test Implementation Priority

### Priority 1 (Critical - Implement First)
- Test 2.1: Rydberg formula (foundational)
- Test 2.3: β parameter (gravitational foundation)
- Test 3.2: Gravitational tests (GR validation)
- Test 4.2: Cross-phase consistency (theory coherence)

### Priority 2 (Important - Implement Second)
- Test 2.2: Hyperfine splitting
- Test 2.4: Orbital mechanics
- Test 3.1: Atomic spectroscopy cross-check
- Test 5.1-5.5: Benchmark-specific tests

### Priority 3 (Comprehensive - Implement Third)
- Test 1.1-1.3: Dimensional analysis (automated)
- Test 4.1: Formula derivations (manual review)
- Test 4.3: Limiting behavior
- Test 6.1-6.4: Error detection (automated)

---

## Test Execution Plan

1. **Week 1:** Implement Priority 1 tests, run on all formulas
2. **Week 2:** Implement Priority 2 tests, validate benchmark requirements
3. **Week 3:** Implement Priority 3 tests, comprehensive error detection
4. **Week 4:** Fix all detected errors, re-run tests, generate final report

---

*Last Updated: November 2025*

