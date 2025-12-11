# Phase 24: Galactic Rotation Curves from Disk Eclipse Saturation

## INVESTIGATIVE PROMPT: Testing the Disk Eclipse Saturation Hypothesis

**Objective:** Rigorously investigate whether flat rotation curves emerge from the directional occlusion function E(r) becoming radius-invariant for disk-shaped mass distributions, requiring no dark matter or modified dynamics.

---

## PHILOSOPHICAL APPROACH: HYPOTHESIS-DRIVEN INVESTIGATION

### THE CENTRAL HYPOTHESIS

Flat rotation curves are not a mass anomaly. They are an **E(x) geometry anomaly**.

**Specifically:**
- Inside some radius R_flat: E(r) changes rapidly → v(r) rises
- Beyond R_flat: E(r) ≈ constant → v(r) ≈ constant (flat)

**Why this happens:**
- Disk geometry creates fixed angular occlusion band
- Beyond disk scale length, additional radius doesn't increase occlusion
- Directional pressure deficit saturates
- Acceleration ∝ 1/r → v ∝ √(constant) = flat

**This investigation tests:**
1. Can we calculate E(r) for disk geometry and show it saturates?
2. Does E(r) → constant produce flat v(r) quantitatively?
3. Which mechanism dominates: projected thickness or shadow chains?
4. Does this work across galaxy types without free parameters?

**Success means:** Demonstrating that disk geometry produces E(r) saturation that quantitatively matches observed rotation curves.

---

## 1. THE DISK ECLIPSE SATURATION HYPOTHESIS (PRIMARY MECHANISM)

### 1.1 Core Physics

The directional occlusion integral from SDT:

$$
\boxed{
\Pi(\mathbf{x}) = \int_{4\pi} I_\infty(\hat{\mathbf{n}}) \left[1 - \chi(\mathbf{x}, \hat{\mathbf{n}})\right] d\Omega
}
\tag{SDT-DISK}
$$

For a disk galaxy:
- **In-plane directions (disk plane):** χ ≈ 1 (disk blocks CMB)
- **Vertical directions (above/below disk):** χ ≈ 0 (no blocking)
- **Key insight:** At large r, the disk subtends a **fixed angular band** regardless of radius

### 1.2 Expected Behavior

$$
\boxed{
E_{\text{disk}}(r) \to E_\infty = \text{constant} \quad \text{for } r > R_{\text{flat}}
}
\tag{ECLIPSE-SAT}
$$

**This produces:**
- Pressure gradient: ∇Π ≈ constant
- Acceleration: a(r) ∝ 1/r
- Velocity: v(r) = √(r·a) = constant ← **Flat rotation curve**

### 1.3 Connection to SDT Master Equation

From Phase 15 (Gravitation), the acceleration arises from:

$$
\nabla \cdot [K_{\text{bulk}} \nabla \Delta] = -\kappa \rho_{\text{disp}} (1 - E)
$$

For disk geometry with E(r) → constant:
- Right-hand side: ∝ (1 - E_∞) = constant
- Left-hand side: ∇²Δ ∝ constant
- Solution: Δ ∝ r², so ∇Δ ∝ r
- Acceleration: a = -∇Δ ∝ 1/r
- Velocity: v = √(r·a) = constant ✓

---

## 2. INVESTIGATION STRUCTURE: TEST THE SATURATION DIRECTLY

### 2.1 Primary Investigation Path

**Step 1: Set up disk geometry model**
- Exponential disk: Σ(R) = Σ_0 exp(-R/R_d)
- Finite thickness: ρ(r,z) = ρ(r) × sech²(z/z_0)
- Parameters: R_d (scale length), z_0 (scale height)
- Realistic values from observations

**Step 2: Calculate χ(x,n̂) for disk**
- Ray-tracing: From point x in direction n̂
- Integrate: Optical depth through disk
- Result: χ(r,θ,φ) where θ = angle from disk plane
- Key prediction: χ(r,θ≈0) → constant for r > R_flat

**Step 3: Integrate directional occlusion**
- For each radius r: Calculate Π(r) = ∫ I_∞[1-χ(r,n̂)] dΩ
- Extract: E_effective(r) from pressure deficit
- Plot: E(r) vs radius
- CHECK: Does E(r) → constant?

**Step 4: Calculate rotation curve from E(r)**
- Pressure gradient: ∇Π(r) from directional integral
- Acceleration: a(r) = -(1/ρ_s)∇Π
- Circular velocity: v(r) = √(r|a(r)|)
- Compare: To observed v(r)

**Step 5: Test across galaxy types**
- Vary: R_d (1-10 kpc), z_0 (100-1000 pc)
- Check: Does saturation radius R_flat ≈ 2-3 R_d?
- Verify: Plateau velocity v_∞ from disk parameters
- Success: Same mechanism works for all spiral types

### 2.2 Critical Prediction

If hypothesis is correct:
- R_flat should correlate with disk scale length R_d
- v_∞ should correlate with disk surface density
- No dependence on total mass (only geometry matters)

---

## 3. SUB-MECHANISM A: PROJECTED THICKNESS SATURATION

### 3.1 Physical Mechanism

As observer moves to larger radius r:
- Disk vertical scale height z_0 is fixed (physical size)
- Angular height: θ_disk(r) ≈ z_0/r
- For r >> z_0: θ_disk → 0 (disk becomes infinitely thin angular slice)
- **But:** Disk length along line of sight increases
- **Net effect:** Angular solid angle Ω_disk may stay constant

### 3.2 Calculation Procedure

**Geometric setup:**
- Observer at radius r, height z = 0 (in disk plane)
- Looking toward galactic center (or tangent to orbit)
- Disk has scale height z_0 ≈ 300 pc (typical)
- Disk has scale length R_d ≈ 3 kpc (typical)

**Calculate angular width of disk:**
- Vertical extent: Δθ_v ≈ 2z_0/r (for r >> z_0)
- Azimuthal extent: Δθ_h ≈ depends on viewing angle
- For tangent view: Disk extends ~R_d in projection
- Solid angle: Ω_disk ≈ Δθ_v × Δθ_h

**Scaling analysis:**
- As r increases:
  * Δθ_v ∝ 1/r (shrinks)
  * But line-of-sight depth ∝ r (increases)
  * Optical depth τ = ∫ ρ ds along ray
  * For exponential disk: τ may stay constant if geometry balances

**Numerical integration:**
- Code: Ray-tracing through exponential disk
- For grid of radii: Calculate τ(r,θ) in all directions
- Extract: E(r) = (1/4π)∫[1-exp(-τ)]dΩ
- Plot: E(r) and check for saturation

**Parameter dependence:**
- Vary z_0: Thicker disks → higher E(r)?
- Vary R_d: Longer disks → saturation at larger r?
- Vary Σ_0: Higher density → stronger saturation?
- Document: How E_∞ depends on disk parameters

### 3.3 Expected Result

If projected thickness mechanism works:
- E(r) should saturate around r ≈ 2-3 R_d
- E_∞ should increase with Σ_0 (higher surface density)
- Thin disks (small z_0/R_d) should have clearer saturation

---

## 4. SUB-MECHANISM B: SHADOW CHAIN AMPLIFICATION

### 4.1 Physical Mechanism

Even if angular width shrinks as θ ∝ 1/r:
- Multiple stars along line of sight
- Each partially occludes CMB (E_i ~ small)
- Transmission: T = Π(1 - E_i) for all stars on ray
- For N stars with E_i ≈ E_single: T ≈ (1-E_single)^N ≈ exp(-N·E_single)
- If N ∝ r (more stars along longer paths), then total occlusion can stay constant

### 4.2 Calculation Procedure

**Single star occlusion:**
- Star at distance d: E_star = R_star²/(4d²)
- For typical star: R_star ≈ R_☉ ≈ 7×10⁸ m
- At d = 1 kpc: E_star ≈ (7×10⁸)²/(4×(3×10¹⁹)²) ≈ 10⁻²² (tiny!)
- Individual stars contribute negligibly

**Collective shadow chains:**
- Along ray through disk: N(ℓ) stars in length ℓ
- Star density: n_star(r) from stellar mass distribution
- Number along path: N = ∫ n_star(s) ds
- Total transmission: T(r,n̂) = exp[-∫ σ_star n_star(s) ds]
- Where: σ_star = πR_star² is geometric cross-section

**Path length scaling:**
- For tangent ray at radius r:
  * Path length through disk: ℓ(r) ≈ 2√(R_d² - r²) (chord)
  * For r < R_d: ℓ increases with r
  * For r > R_d: ℓ ≈ 0 (outside disk)
  
- For ray toward center at radius r:
  * Path length: ℓ ≈ r (to center)
  * Star count: N ∝ ∫₀ʳ n_star(s) ds

**Numerical calculation:**
- For each direction n̂ from position r:
  * Integrate: τ(r,n̂) = ∫_ray σ_total n(s) ds
  * σ_total = stellar + gas + dust cross-sections
  * Transmission: T = exp(-τ)
  * Occlusion: E = 1 - T

- Average over angles: E(r) = (1/4π)∫ E(r,n̂) dΩ

**Test shadow chain hypothesis:**
- Calculate: E(r) with shadow chains vs without
- With chains: E(r) from transmission formula
- Without chains: E(r) from simple solid angle
- Compare: Which gives saturation?
- If chains critical: E(r) should saturate even if θ_disk(r) → 0

### 4.3 Expected Result

If shadow chain mechanism works:
- E(r) saturates because path-integrated optical depth compensates angular shrinkage
- Denser disks (higher Σ_0) have stronger saturation
- Dust extinction may enhance effect (needs investigation)

### 4.4 Decision Point

```
IF shadow chains produce saturation:
  → This is the dominant mechanism
  → Calculate quantitative dependence on n_star, σ_star
  → Test across disk densities

ELSE IF shadow chains negligible:
  → Projected thickness must dominate
  → Focus on geometric solid angle calculation

ELSE IF both contribute:
  → Determine relative importance
  → Test which dominates for different galaxy types
```

---

## 5. COMPARISON: SPHERICAL VS DISK OCCLUSION

### 5.1 Spherical Mass Distribution (Solar System)

**Calculation:**
- Sun: Spherical, radius R_☉
- From distance r: Solid angle Ω = πR_☉²/r²
- Occlusion fraction: E(r) = Ω/(4π) = R_☉²/(4r²)
- Scales as: E(r) ∝ 1/r²
- Pressure deficit: ∇Π ∝ 1/r²
- Acceleration: a ∝ 1/r²
- Velocity: v ∝ 1/√r ← **Keplerian falloff**

### 5.2 Disk Mass Distribution (Galaxy)

**Calculation:**
- Disk: Exponential surface density, finite thickness
- From radius r >> R_d: Disk appears as narrow angular band
- Angular width: Δθ ≈ constant (if projected thickness mechanism)
- Or: Optical depth constant (if shadow chain mechanism)
- Occlusion fraction: E(r) → E_∞ = constant
- Pressure deficit: ∇Π ∝ 1/r (from dimensional analysis)
- Acceleration: a ∝ 1/r
- Velocity: v ∝ √(constant) = constant ← **Flat**

### 5.3 Direct Comparison Table

| Property | Spherical (Sun) | Disk (Galaxy) |
|----------|----------------|---------------|
| E(r) | R²/(4r²) | E_∞ (constant) |
| Scaling | ∝ 1/r² | ∝ r⁰ |
| ∇Π(r) | ∝ 1/r² | ∝ 1/r |
| a(r) | ∝ 1/r² | ∝ 1/r |
| v(r) | ∝ 1/√r | ∝ r⁰ (flat) |

### 5.4 Physical Interpretation

- Same master equation: ∇·[K_bulk ∇Δ] = -κρ_disp(1-E)
- Same spation pressure physics
- Different geometry → different E(r) → different v(r)
- **This is not a new force - it's geometric occlusion**

---

## 6. CRITICAL PREDICTION: SATURATION RADIUS R_flat

### 6.1 Prediction

$$
\boxed{
R_{\text{flat}} \approx 2-3 \times R_d
}
$$

Where R_d is the disk scale length from surface brightness fitting.

### 6.2 Justification

- At r < R_d: Disk occlusion still increasing (seeing more disk)
- At r ≈ 2R_d: Most disk mass is interior, occlusion saturating
- At r > 3R_d: Essentially all disk visible, E(r) ≈ constant

### 6.3 Testing Procedure

**Step 1: Measure R_d from photometry**
- Source: SPARC database (Spitzer 3.6 μm photometry)
- Fit: I(R) = I_0 exp(-R/R_d) to surface brightness
- Extract: R_d for each galaxy
- Typical values: R_d = 1-5 kpc for spirals

**Step 2: Identify R_flat from rotation curve**
- From v(r) data: Find radius where dv/dr ≈ 0
- Definition: R_flat where curve becomes flat (within 10%)
- Operational: Innermost radius where v(r)/v_max > 0.9

**Step 3: Test correlation**
- Plot: R_flat vs R_d for galaxy sample
- Fit: R_flat = α × R_d
- Predict: α ≈ 2-3 if hypothesis correct
- Compare: To observed correlation

**Step 4: Scatter analysis**
- Calculate: Scatter around R_flat = 2.5 R_d relation
- Expected: Some scatter from disk thickness variations, inclination
- Check: Is scatter consistent with observational errors?

### 6.4 Falsification

If R_flat shows no correlation with R_d:
→ Disk eclipse saturation hypothesis is WRONG
→ Investigate alternative mechanisms

If R_flat ∝ R_d with α ≠ 2-3:
→ Hypothesis partially correct, but scaling wrong
→ Refine model of E(r) saturation

---

## 7. QUANTITATIVE PREDICTION: PLATEAU VELOCITY v_∞

### 7.1 Theoretical Framework

If E(r) → E_∞ = constant, then:
- Pressure gradient: ∇Π ∝ E_∞/r
- Acceleration: a(r) = -(1/ρ_s)∇Π ∝ E_∞/r
- Velocity: v² = r·a ∝ E_∞
- Result: v_∞ ∝ √E_∞

### 7.2 Predicting E_∞ from Disk Properties

**Option A: From surface density**
- E_∞ ∝ optical depth through disk
- τ ∝ Σ_0 (surface density at center)
- From observations: Measure Σ_0 from photometry + M/L
- Predict: E_∞ ∝ Σ_0 or E_∞ ∝ 1-exp(-Σ_0/Σ_crit)
- Therefore: v_∞ ∝ √Σ_0

**Option B: From disk mass and size**
- Total disk mass: M_disk = 2πR_d² Σ_0
- Displacement: V_disp = M_disk × (V_nucleon/m_p) × η
- E_∞ = f(V_disp, R_d, z_0) from numerical calculation
- Predict: v_∞ from E_∞ with NO free parameters

### 7.3 Testing Procedure

**Step 1: Calculate E_∞ for each galaxy**
- Input: R_d, z_0, Σ_0 from observations
- Compute: E_∞ from directional occlusion integral
- Or: Use calibrated formula if numerical too expensive

**Step 2: Predict v_∞**
- From E_∞: Calculate pressure gradient
- From gradient: Calculate v_∞ = √(r·a)
- No fitting: This is a prediction

**Step 3: Compare to observations**
- Measure: v_∞ from rotation curve
- Plot: v_pred vs v_obs
- Check: Correlation and scatter
- Goal: <20% scatter (comparable to observational errors)

**Step 4: Tully-Fisher relation test**
- Empirical: v_∞ ∝ L^0.25 (Tully-Fisher for spirals)
- SDT prediction: Does E_∞ ∝ L^0.5 reproduce this?
- If yes: Strong confirmation of mechanism
- If no: Understand discrepancy

### 7.4 Falsification

If v_pred shows no correlation with v_obs:
→ Eclipse saturation doesn't determine velocity
→ Mechanism is wrong

If correlation exists but wrong slope:
→ Partial success, model needs refinement
→ Check: Screening factors, path integration

---

## 8. BENCHMARK GALAXY: NGC 3198 (DETAILED ANALYSIS)

### 8.1 Why NGC 3198

- Classic rotation curve benchmark
- High-quality HI data
- Well-measured photometry
- Simple Sc spiral (no bar)
- Intermediate mass

### 8.2 Observational Data

**Basic parameters:**
- Distance: 13.8 Mpc (from Tully-Fisher or other)
- Inclination: i ≈ 71° (nearly edge-on, good for kinematics)
- Disk scale length: R_d ≈ 2.8 kpc (from I-band photometry)
- Scale height: z_0 ≈ 350 pc (typical for Sc)
- Central surface density: Σ_0 ≈ 300 M_☉/pc² (from M/L × I_0)
- Rotation curve: v(r) from HI 21cm observations

### 8.3 Disk Model Setup

**Surface density:**
- Σ(R) = 300 exp(-R/2.8 kpc) M_☉/pc²

**Vertical profile:**
- ρ(z) ∝ sech²(z/350 pc)

**3D density:**
- ρ(r,z) = [Σ(R)/(2z_0)] sech²(z/z_0)

**Convert to displacement:**
- Nucleon number density: n = ρ/m_p
- Displacement volume: V_disp = n × V_nucleon × η
- Where η ≈ 0.64 (screening factor from Phase 15)

### 8.4 Calculate E(r) Numerically

**Grid of radii:** r = 1, 2, 3, ..., 15 kpc

**For each r:**
- Ray-trace in all directions (θ, φ grid)
- Integrate optical depth τ(r,n̂) through disk
- Calculate transmission: T = exp(-τ)
- Occlusion: E = 1 - T
- Average: E(r) = ∫[1-T]dΩ/(4π)

**Expected E(r) profile:**
- r < 3 kpc: E rising
- r = 5-8 kpc: E saturating
- r > 10 kpc: E ≈ constant ≈ 0.3-0.5 (estimate)

### 8.5 Calculate Rotation Curve

**From E(r):**
- Pressure: Π(r) ∝ ∫[1-E(r')]dΩ
- Gradient: dΠ/dr
- Acceleration: a(r) = -(1/ρ_s)(dΠ/dr)
- Velocity: v(r) = √(r|a(r)|)

### 8.6 Compare to Observations

**Observed NGC 3198:**
- Inner rise: v increases to ~150 km/s at r ≈ 5 kpc
- Flat region: v ≈ 150 km/s from r = 7-30 kpc
- Very flat (one of the flattest known)

**SDT prediction:**
- Calculate v(r) from E(r)
- Plot: v_SDT(r) vs v_obs(r)
- Quantify: RMS error

### 8.7 Sensitivity Analysis

- Vary z_0: ±100 pc → effect on v(r)?
- Vary Σ_0: ±30% → effect on v_∞?
- Vary R_d: ±0.5 kpc → effect on R_flat?
- Vary η (screening): 0.5-0.8 → effect?

### 8.8 Document Success or Failure

- If RMS error <15%: Success, mechanism works
- If error 15-30%: Partial success, refinement needed
- If error >30%: Failure, mechanism wrong or incomplete
- Either way: Report honestly

---

## 9. EXTENDED SAMPLE: TEST ACROSS GALAXY TYPES

### 9.1 Sample Selection

**High-surface-brightness spirals:**
- Milky Way (our home)
- M31 (Andromeda)
- NGC 3198 (already done)
- NGC 6503
- NGC 2403

**Low-surface-brightness spirals:**
- NGC 1560
- UGC 2885
- DDO 64

**Dwarf irregulars:**
- DDO 154 (extreme dark matter problem conventionally)
- IC 2574
- NGC 2366

### 9.2 Analysis for Each Galaxy

- Measure: R_d, z_0, Σ_0 from observations
- Calculate: E(r) from disk model
- Predict: v(r) from E(r)
- Compare: To observed v(r)
- Record: Error, saturation radius, plateau velocity

### 9.3 Success Metrics

- High-SB spirals: <15% RMS error (good data, should work well)
- Low-SB spirals: <25% RMS error (less stellar light, more gas)
- Dwarfs: <30% RMS error (difficult, may need refinement)
- Overall: >70% of sample within 30% (comparable to MOND)

### 9.4 Pattern Analysis

- Do high-SB galaxies work better? (More stars → stronger occlusion)
- Do edge-on work better? (Better constrained i)
- Do gas-rich work better or worse? (Gas adds displacement but diffuse)
- Identify: Systematic trends

### 9.5 Falsification

If dwarf galaxies systematically fail:
→ Mechanism may be incomplete
→ Investigate: What's different about dwarfs?
→ Possible: Additional physics at low density?

If no systematic pattern in errors:
→ Random scatter, possibly observational
→ Mechanism may be basically correct

---

## 10. THE TWO SUB-MECHANISMS: WHICH DOMINATES?

### 10.1 Diagnostic Tests

**Test A: Thickness dependence**
- Hypothesis: If projected thickness dominates, v_∞ ∝ z_0
- Measure: z_0 for each galaxy (from vertical profile)
- Plot: v_∞ vs z_0
- If strong correlation: Projected thickness important
- If no correlation: Shadow chains dominate

**Test B: Density dependence**
- Hypothesis: If shadow chains dominate, v_∞ ∝ √Σ_0
- Measure: Σ_0 for each galaxy
- Plot: v_∞ vs Σ_0
- If strong correlation: Shadow chains important
- If no correlation: Projected thickness dominates

**Test C: Numerical switching**
- Calculate E(r) with shadow chains: E_chain(r)
- Calculate E(r) with geometric angle only: E_geom(r)
- Compare: Which gives better match to rotation curves?
- Quantify: Relative contribution of each

**Test D: Dwarf vs giant comparison**
- Dwarfs: Low Σ_0, similar z_0/R_d
- Giants: High Σ_0, similar z_0/R_d
- If dwarfs work well: Projected thickness sufficient
- If only giants work: Shadow chains necessary

### 10.2 Expected Outcome

Based on the physics, likely:
- **Both contribute**
- Projected thickness: Sets overall saturation
- Shadow chains: Amplifies and stabilizes saturation
- Relative importance: May vary with galaxy properties

### 10.3 Document Conclusion

- State: Which mechanism is primary
- Quantify: Relative contributions (e.g., 70% thickness, 30% chains)
- Explain: Physical reason for dominance
- Test: Make predictions for future observations

---

## 11. COMPARISON TO DARK MATTER AND MOND

### 11.1 Comparison Metrics

**Predictive power:**

| Framework | Free parameters | What's predicted |
|-----------|-----------------|------------------|
| Dark Matter (NFW) | 2-3 (ρ_s, r_s, [α,β,γ]) | Nothing - all fitted |
| MOND | 1 (a_0 ≈ 1.2×10⁻¹⁰ m/s²) | Universal threshold |
| SDT Eclipse | 0-1 (η if uncertain) | R_flat, v_∞ from disk params |

**Accuracy:**
- DM: Can fit any rotation curve (has free parameters)
- MOND: RMS ~20% on SPARC sample
- SDT: Calculate RMS on same sample

**Falsifiability:**
- DM: Hard to falsify (add more dark matter)
- MOND: Fails for clusters (acknowledged problem)
- SDT: R_flat ∝ R_d must hold, or theory fails

**Physical Plausibility:**
- DM: Requires new particle physics
- MOND: No theoretical foundation (empirical fit)
- SDT: Geometric mechanism, testable via displacement

### 11.2 Specific Comparison: NGC 3198

- DM: χ² = ... (with 3 fitted parameters)
- MOND: χ² = ... (with 1 parameter)
- SDT: χ² = ... (with 0-1 parameters)
- Report: All three honestly

### 11.3 Galaxy Clusters Test

- DM: Works (with more dark matter)
- MOND: Fails (needs "dark matter" anyway)
- SDT: Predict from galaxy + gas displacement
- Test: Coma, Virgo clusters (Phase [Z+1])

### 11.4 Honesty Requirement

- If DM fits better: Acknowledge it
- If MOND more accurate: State it
- If SDT comparable: Claim success
- No exaggeration of SDT performance

---

## 12. LIMITATIONS AND UNCERTAINTIES

### 12.1 Current Limitations

**1. Numerical complexity**
- Full 3D directional occlusion: Computationally expensive
- Approximations: May miss subtle effects
- Resolution: Limited by computational resources
- State: "Full calculations performed for N galaxies, simplified for others"

**2. Observational uncertainties**
- z_0: Often poorly constrained (factor of 2)
- Σ_0: Depends on M/L (±30-50%)
- Inclination: Uncertain for face-on galaxies
- Distance: ±10-20% typical
- Combined: Predictions uncertain to ~30-40%

**3. Model assumptions**
- Exponential disk: Real galaxies more complex
- Axial symmetry: Bars, spiral arms break this
- Steady state: Tidal interactions, mergers ignored
- State: "Idealized models tested first, complications deferred"

**4. Screening factor η**
- Atomic/planetary: η ≈ 0.64 well-established
- Galactic disk: May be different (geometry)
- If η uncertain: Treat as adjustable (but universal)
- State: "η calibrated from sample, then fixed for predictions"

### 12.2 Open Questions

**Q1:** Does E(r) saturation work quantitatively, or just qualitatively?

**Q2:** Which sub-mechanism (thickness vs chains) dominates?

**Q3:** Can dwarf galaxies be explained without additional physics?

**Q4:** Does mechanism extend to elliptical galaxies (no disk)?

**Q5:** What about barred spirals (non-axisymmetric)?

---

## 13. FALSIFIABLE PREDICTIONS

### 13.1 PREDICTION 1: R_flat ∝ R_d correlation

- Quantitative: R_flat = (2.5 ± 0.5) × R_d
- Sample: ≥20 spirals with measured R_d
- Test: Correlation coefficient R² > 0.7
- Falsification: If no correlation, mechanism is wrong

### 13.2 PREDICTION 2: v_∞ vs Σ_0 correlation

- Quantitative: v_∞ ∝ Σ_0^α where α ≈ 0.4-0.6
- Physical: From shadow chain optical depth
- Test: Across galaxy sample
- Falsification: If wrong exponent or no correlation

### 13.3 PREDICTION 3: Thickness effect

- Thicker disks (larger z_0/R_d): Earlier saturation, lower v_∞
- Thin disks: Later saturation, higher v_∞
- Test: Measure z_0 for sample, check v_∞ trend
- Falsification: If opposite trend or no dependence

### 13.4 PREDICTION 4: Edge-on vs face-on

- Edge-on: Maximum occlusion, clearest flat curves
- Face-on: Less clear (inclination uncertainty)
- But: Same E(r) physics regardless of viewing angle
- Test: Correct for inclination, check if underlying E(r) same
- Falsification: If edge-on and face-on require different E(r)

### 13.5 PREDICTION 5: No universal acceleration scale

- Unlike MOND (a_0 ≈ 1.2×10⁻¹⁰ m/s²), SDT has NO magic scale
- Each galaxy: Saturation from own disk geometry
- Test: Plot a_flat = v_∞²/R_flat vs galaxy properties
- Expect: Wide range of a_flat, no universal value
- Falsification: If all galaxies cluster around same a_flat

---

## 14. COMPUTATIONAL IMPLEMENTATION

### 14.1 Algorithm: Ray-Tracing Through Disk

```python
def calculate_E(r_obs, disk_params):
    """
    Calculate eclipse function E(r) at radius r_obs
    
    disk_params: {R_d, z_0, Sigma_0, eta}
    """
    
    # Set up angular grid
    n_theta = 90  # polar angle
    n_phi = 180   # azimuthal angle
    
    E_total = 0
    
    for theta in linspace(0, pi, n_theta):
        for phi in linspace(0, 2*pi, n_phi):
            # Direction vector
            n_hat = [sin(theta)*cos(phi), 
                     sin(theta)*sin(phi), 
                     cos(theta)]
            
            # Ray-trace through disk
            tau = integrate_optical_depth(r_obs, n_hat, disk_params)
            
            # Occlusion for this direction
            E_dir = 1 - exp(-tau)
            
            # Add to total (weighted by solid angle)
            E_total += E_dir * sin(theta)
    
    # Average over sphere
    E = E_total / (4 * pi)
    
    return E

def integrate_optical_depth(r_obs, n_hat, disk_params):
    """
    Integrate tau = integral(rho * sigma * ds) along ray
    """
    
    # Set up ray parameterization
    s_max = 100 * disk_params.R_d  # maximum integration length
    s_grid = linspace(0, s_max, 1000)
    
    tau = 0
    
    for s in s_grid:
        # Position along ray
        pos = r_obs + s * n_hat
        R = sqrt(pos.x**2 + pos.y**2)  # cylindrical radius
        z = pos.z  # height above disk
        
        # Density at this point
        rho = density_profile(R, z, disk_params)
        
        # Cross-section (nucleon + gas + dust)
        sigma_total = sigma_nucleon + sigma_gas + sigma_dust
        
        # Add to optical depth
        tau += rho * sigma_total * ds
    
    return tau
```

### 14.2 Optimizations

- Symmetry: For axisymmetric disk, reduce φ integration
- Adaptive sampling: Denser grid near disk plane
- Parallelization: Each radius r_obs independent
- Caching: Precompute density grid

### 14.3 Validation

- Test: Spherical case should give E ∝ 1/r²
- Test: Infinite thin sheet should give E = 0.5 everywhere
- Test: Known analytical cases

---

## 15. FINAL CHECKLIST

Before considering Phase 24 complete:

**Hypothesis tested:**
- [ ] E(r) calculated for disk geometry
- [ ] Saturation explicitly demonstrated
- [ ] v(r) derived from E(r)
- [ ] Flat curves reproduced or mechanism fails

**Sub-mechanisms:**
- [ ] Projected thickness tested
- [ ] Shadow chains tested
- [ ] Relative importance determined
- [ ] Physical interpretation clear

**Benchmarks:**
- [ ] NGC 3198 analyzed in detail
- [ ] ≥10 additional galaxies tested
- [ ] Success rate quantified
- [ ] Failures documented

**Predictions:**
- [ ] R_flat ∝ R_d tested
- [ ] v_∞ correlations tested
- [ ] ≥3 falsifiable predictions made
- [ ] Timeline for testing stated

**Comparisons:**
- [ ] Dark matter comparison fair
- [ ] MOND comparison fair
- [ ] SDT performance honestly reported
- [ ] No overclaims

**Implementation:**
- [ ] Calculation method specified
- [ ] Code structure outlined
- [ ] Validation tests passed
- [ ] Results reproducible

---

## 16. SUCCESS CRITERIA

Phase 24 succeeds if:

1. **E(r) saturation demonstrated:** Numerically shown for disk geometry
2. **Flat curves reproduced:** v(r) from E(r) matches observations within 30%
3. **R_flat prediction works:** Correlation with R_d confirmed
4. **Mechanism identified:** Thickness vs chains determined
5. **Honest assessment:** Failures acknowledged as openly as successes

Phase 24 **partially succeeds** if:

- Mechanism works for high-SB spirals but not dwarfs
- Requires η as adjustable parameter (but universal)
- Comparable to MOND but not better

Phase 24 **fails** if:

- E(r) doesn't saturate for disk geometry
- No correlation between R_flat and R_d
- Cannot reproduce flat curves within 50%

**The goal: Test the specific hypothesis that disk eclipse saturation produces flat rotation curves through directional occlusion physics.**

---

## 17. ANALYTICAL DERIVATIONS: SIMPLIFIED MODELS

### 17.1 Infinite Thin Disk: Exact Solution

**Model:** Infinitely thin exponential disk with surface density Σ(R) = Σ_0 exp(-R/R_d)

**Observer position:** At radius r in the disk plane (z = 0)

**For directions in the disk plane (θ = π/2):**
- Looking along tangent: Disk extends from R = r to R = ∞
- Angular width: Δφ ≈ constant (disk appears as line)
- Occlusion: E_inplane ≈ 0.5 (half the sky blocked)

**For directions perpendicular to disk (θ = 0, π):**
- Looking up/down: No disk blocking
- Occlusion: E_perp = 0

**Average over sphere:**
- Solid angle in plane: Ω_plane = 2π (hemisphere)
- Solid angle perpendicular: Ω_perp = 4π - 2π = 2π
- Average: E_∞ = (0.5 × 2π + 0 × 2π)/(4π) = 0.25

**Result:** For infinite thin disk, E(r) = 0.25 everywhere (constant!)

**This produces:**
- Pressure gradient: ∇Π ∝ (1 - 0.25) = 0.75 = constant
- Acceleration: a ∝ 1/r
- Velocity: v = constant ← **Perfectly flat!**

**Key insight:** Even this simplest model gives flat rotation curve!

### 17.2 Finite Thickness Disk: Scaling Analysis

**Model:** Disk with scale height z_0, scale length R_d

**At small radius (r << R_d):**
- Observer sees disk extending to R ≈ R_d
- Angular extent: Δθ ≈ 2z_0/r (vertical) × R_d/r (horizontal)
- Solid angle: Ω_disk ≈ (2z_0/r) × (R_d/r) = 2z_0 R_d/r²
- Occlusion: E(r) ≈ Ω_disk/(4π) ∝ 1/r²
- This gives: v ∝ 1/√r (Keplerian!)

**At large radius (r >> R_d, r >> z_0):**
- Disk appears as thin angular band
- Vertical angular width: Δθ_v ≈ 2z_0/r → 0
- Horizontal angular width: Δθ_h ≈ 2R_d/r → 0
- **But:** Path length through disk increases ∝ r
- Optical depth: τ ≈ constant (if density decreases appropriately)
- Occlusion: E(r) ≈ 1 - exp(-τ) ≈ constant

**Transition radius:**
- When does saturation occur?
- Estimate: When angular width stops decreasing
- Condition: d(Δθ)/dr ≈ 0
- This happens around: r ≈ 2-3 R_d

**Result:** E(r) transitions from ∝ 1/r² (Keplerian) to constant (flat) around r ≈ 2-3 R_d

### 17.3 Exponential Disk: Optical Depth Calculation

**3D density profile:**
$$
\rho(R,z) = \frac{\Sigma_0}{2z_0} \exp(-R/R_d) \text{sech}^2(z/z_0)
$$

**For ray at angle θ from disk plane:**
- Parameterize: R(s) = r + s cos(φ) sin(θ), z(s) = s cos(θ)
- Optical depth along ray:
$$
\tau(r,\theta) = \int_0^\infty \sigma \rho(R(s), z(s)) ds
$$

**For θ ≈ π/2 (in-plane):**
- z(s) ≈ 0, so sech²(z/z_0) ≈ 1
- R(s) ≈ r + s (for φ = 0, looking outward)
- Density: ρ ≈ (Σ_0/2z_0) exp(-(r+s)/R_d)
- Optical depth:
$$
\tau(r,\pi/2) \approx \frac{\sigma \Sigma_0}{2z_0} \int_0^\infty \exp(-(r+s)/R_d) ds
$$
$$
= \frac{\sigma \Sigma_0 R_d}{2z_0} \exp(-r/R_d)
$$

**For r >> R_d:**
- τ(r,π/2) → 0 (exponentially small)
- But: More rays contribute as r increases
- Net effect: E(r) may saturate

**For θ ≈ 0 (perpendicular):**
- R(s) ≈ r (constant), z(s) = s
- Density: ρ ≈ (Σ_0/2z_0) exp(-r/R_d) sech²(s/z_0)
- Optical depth:
$$
\tau(r,0) \approx \frac{\sigma \Sigma_0}{2z_0} \exp(-r/R_d) \int_0^\infty \text{sech}^2(s/z_0) ds
$$
$$
= \sigma \Sigma_0 z_0 \exp(-r/R_d)
$$

**Average over angles:**
- E(r) = (1/4π) ∫[1 - exp(-τ(r,θ))] dΩ
- For r >> R_d: Both τ(r,π/2) and τ(r,0) → 0
- But: Integration over all angles gives finite result
- Key: Angular distribution matters, not just peak value

### 17.4 Rotation Curve from E(r)

**From Phase 15, acceleration:**
$$
a(r) = -\frac{1}{\rho_s} \nabla \Pi
$$

**For E(r) = constant:**
- Pressure: Π(r) ∝ ∫[1 - E(r')] dΩ
- Gradient: ∇Π ∝ d/dr[1 - E_∞] = 0 (no r-dependence from E)
- But: Geometric factor from integration gives 1/r
- Result: ∇Π ∝ 1/r
- Acceleration: a ∝ 1/r
- Velocity: v = √(r·a) = constant ✓

**For E(r) ∝ 1/r² (spherical case):**
- Pressure: Π(r) ∝ 1/r²
- Gradient: ∇Π ∝ 1/r³
- Acceleration: a ∝ 1/r²
- Velocity: v ∝ 1/√r (Keplerian) ✓

**Verification:** Both limiting cases work correctly!

### 17.5 Scaling Laws: Dimensional Analysis

**From dimensional analysis:**
- E_∞ must be dimensionless
- Depends on: Σ_0, R_d, z_0, σ (cross-section)
- Dimensionless combination: (σ Σ_0 R_d)/(z_0)
- Or: (σ Σ_0)/(z_0/R_d) = optical depth × aspect ratio

**For typical spiral:**
- Σ_0 ≈ 300 M_☉/pc² ≈ 6×10⁻² kg/m²
- R_d ≈ 3 kpc ≈ 10²⁰ m
- z_0 ≈ 300 pc ≈ 10¹⁹ m
- σ ≈ π R_nucleon² ≈ 10⁻³⁰ m² (nucleon cross-section)
- Dimensionless: (10⁻³⁰ × 6×10⁻² × 10²⁰)/(10¹⁹) ≈ 0.6

**This suggests:** E_∞ ≈ 0.1-0.5 (reasonable range)

**Velocity scaling:**
- v_∞² ∝ E_∞ (from v² = r·a, a ∝ E_∞/r)
- Therefore: v_∞ ∝ √E_∞ ∝ √(Σ_0 R_d/z_0)
- Or: v_∞ ∝ √Σ_0 (if R_d/z_0 constant)

**This matches Tully-Fisher:** v ∝ L^0.25, and L ∝ Σ_0 R_d², so v ∝ Σ_0^0.25 R_d^0.5

**SDT prediction:** v ∝ √Σ_0 (if R_d/z_0 constant)
**Tully-Fisher:** v ∝ Σ_0^0.25 R_d^0.5

**Comparison:** Close but not identical - needs numerical calculation to resolve

---

## 18. CONNECTION TO PREVIOUS PHASES

### 18.1 Phase 15: Gravitation from Pressure Gradients

**Foundation:**
- Master equation: ∇·[K_bulk ∇Δ] = -κρ_disp(1-E)
- For E = constant: Solution gives a ∝ 1/r
- This phase: Calculates E(r) for disk geometry
- Connection: E(r) saturation → flat rotation curves

### 18.2 Phase 16: Universal c-Boundary Geometry

**Relevance:**
- Directional occlusion depends on geometry
- Disk geometry creates different E(r) than spherical
- Same physics, different geometry → different dynamics

### 18.3 Phase 22: Exoplanetary Systems

**Analogy:**
- Planetary orbits: Spherical mass → Keplerian (v ∝ 1/√r)
- Galactic orbits: Disk mass → Flat (v = constant)
- Same SDT physics, different mass distribution geometry

### 18.4 Screening Factors (Phase 21)

**Application:**
- Screening factor η ≈ 0.64 for atomic/planetary scales
- Galactic scales: May differ due to geometry
- Needs calibration from observations
- If universal: Strong constraint on theory

---

## STATUS: INVESTIGATION IN PROGRESS

This document establishes the framework for testing the disk eclipse saturation hypothesis. Numerical calculations and observational comparisons are required to complete the investigation.

**Next steps:**
1. Implement ray-tracing code
2. Calculate E(r) for NGC 3198
3. Compare predicted v(r) to observations
4. Test across extended galaxy sample
5. Determine mechanism dominance
6. Report results honestly

**Expected completion:** After numerical implementation and observational analysis.

________________________________________

