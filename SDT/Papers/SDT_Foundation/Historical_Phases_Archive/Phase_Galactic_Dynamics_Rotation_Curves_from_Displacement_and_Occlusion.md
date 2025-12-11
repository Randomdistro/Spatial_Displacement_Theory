# PHASE Y — GALACTIC DYNAMICS: INVESTIGATING ROTATION CURVES FROM DISPLACEMENT AND OCCLUSION

*(Exploratory investigation of flat rotation curves without dark matter)*

---

## Y.0 Scope and Philosophical Approach

### Y.0.1 Investigation, Not Certification

**THIS PHASE IS DIFFERENT FROM OTHERS:**

Unlike atomic physics (where QM predictions are precise) or planetary orbits (where Kepler's laws are exact), galactic rotation is an **active mystery**. The conventional answer (dark matter) is a hypothesis, not a measurement. MOND is an empirical fit, not a theory.

**Therefore, this phase is structured as:**

- **Investigation:** What mechanisms could produce flat curves?
- **Hypothesis testing:** Which mechanisms dominate?
- **Adaptive strategy:** If approach A fails, try approach B
- **Data-driven:** Let observations guide theory development
- **Honest uncertainty:** State what we don't know

**Success criteria:**

- ✓ Identify plausible SDT mechanisms
- ✓ Test each mechanism against data
- ✓ Narrow down which effects matter
- ✓ Achieve comparable or better fit than MOND
- ✗ NOT required to match every galaxy perfectly (yet)

**Standards:**

- All constants from CODATA 2018 or astronomical catalogs
- All calculations verified numerically where possible
- All uncertainties propagated honestly
- All failures documented as openly as successes
- All predictions made falsifiable

---

## Y.1 The Galactic Rotation Problem

### Y.1.1 Part A: Expected Keplerian Falloff

**Conventional prediction:**

For visible matter only, with mass within radius r given by M(r):

$$v(r) = \sqrt{\frac{GM(r)}{r}}$$

**Beyond visible disk:**

- Stellar mass distribution: M_stars(r) typically drops exponentially
- Beyond ~3-5 scale lengths: M_stars(r) ≈ constant
- Expected velocity: $v(r) \propto r^{-1/2}$ (Keplerian falloff)

**Example calculation (Milky Way):**

- Stellar disk scale length: $R_d \approx 3$ kpc
- At $r = 10$ kpc: Most stars within this radius
- At $r = 20$ kpc: M_stars(r) ≈ constant
- Expected: $v(20 \text{ kpc}) \approx v(10 \text{ kpc}) / \sqrt{2} \approx 155$ km/s
- But observed: $v(20 \text{ kpc}) \approx 220$ km/s (flat!)

**The problem:** Velocity should drop as $v \propto 1/\sqrt{r}$ at large $r$, but it doesn't.

---

### Y.1.2 Part B: Observed Flat Rotation Curves

**Universal feature:**

Nearly all spiral galaxies show **flat rotation curves** extending far beyond the visible disk.

**Example galaxies:**

| Galaxy | Type | v_∞ (km/s) | Flat to (kpc) | v_obs/v_visible |
|--------|------|------------|---------------|-----------------|
| Milky Way | Sb | 220 | ~15 | ~2-3 |
| NGC 3198 | Sc | 150 | ~30 | ~3-4 |
| M33 | Sc | 120 | ~20 | ~2-3 |
| DDO 154 | Dwarf | 50 | ~5 | ~10 |

**Key observations:**

1. **Velocity stays constant** out to large radii (10-100 kpc)
2. **No Keplerian falloff** despite visible matter dropping
3. **Dwarf galaxies:** Even more "dark matter dominated" (v_obs/v_visible > 10)
4. **Universal:** Feature appears in nearly all spiral galaxies

**Data sources:**

- SPARC database: 175 galaxies with high-quality rotation curves
- THINGS survey: 34 nearby galaxies with resolved HI kinematics
- Individual studies: Milky Way, M31, M33, NGC 3198

---

### Y.1.3 Part C: Conventional Solution (Dark Matter Halo)

**Hypothesis:**

Invisible matter in spherical halo around galaxy.

**Distribution:**

- NFW profile: $\rho_{\text{DM}}(r) = \frac{\rho_0}{(r/r_s)(1 + r/r_s)^2}$
- Or cored profile: $\rho_{\text{DM}}(r) = \frac{\rho_0}{1 + (r/r_c)^2}$
- Total mass: $M_{\text{DM}} \sim 5-10 \times M_{\text{visible}}$

**Problems:**

1. **Never detected directly:** No particle physics evidence
2. **Requires new physics:** WIMPs, axions, or other candidates
3. **Fine-tuning:** Halo profiles must match rotation curves
4. **Core-cusp problem:** Dwarf galaxies prefer cores, simulations predict cusps
5. **Missing satellites:** Simulations predict more dwarf galaxies than observed

**Status:** Dark matter is a **hypothesis**, not a measurement.

---

### Y.1.4 Part D: MOND Alternative (Modified Newtonian Dynamics)

**Empirical fit:**

Modify gravity at low acceleration:

$$F = m \mu(a/a_0) a$$

where:
- $a_0 \approx 1.2 \times 10^{-10}$ m/s² (empirical threshold)
- $\mu(x \to \infty) = 1$ (Newtonian at high acceleration)
- $\mu(x \to 0) = x$ (modified at low acceleration)

**Success:**

- Fits many rotation curves well
- Single parameter ($a_0$) for all galaxies
- No dark matter needed

**Problems:**

1. **No theoretical foundation:** Purely empirical
2. **Fails for galaxy clusters:** Still needs dark matter
3. **Unclear cosmology:** How to extend to large scales?
4. **Acceleration scale unexplained:** Why $a_0$?

**Status:** MOND is a **fit**, not a theory.

---

### Y.1.5 Part E: SDT Approach (Displacement-Based)

**No dark matter particles, no modification of dynamics.**

**Mechanisms to investigate:**

1. **SMBH shadow chains:** Long-range pressure gradients from supermassive black hole
2. **Distributed stellar displacement:** Collective β effect from all stars
3. **Gas/dust contribution:** Often neglected in conventional analyses
4. **Modified k-law:** Does k vary with scale for diffuse distributions?
5. **Large-scale CMB occlusion:** Directional pressure patterns from galactic mass
6. **Scale-dependent screening:** Does screening change at galactic scales?

**Investigation strategy:**

- Test each mechanism independently
- Combine mechanisms that show promise
- Let data guide which effects matter
- Document failures as openly as successes

---

## Y.2 Investigative Strategy: Decision Tree Approach

### Y.2.1 The Investigation Framework

**Decision tree structure:**

```
START
├─ Mechanism 1: SMBH Shadow Chains
│  ├─ Calculate: β_SMBH, shadow chain transmission
│  ├─ Predict: v(r) from SMBH alone
│  ├─ Compare: To observed v(r)
│  ├─ IF good match (>70%):
│  │  └─ Document success, refine calculation
│  ├─ IF poor match (<30%):
│  │  └─ SMBH not dominant, try Mechanism 2
│  └─ IF partial match (30-70%):
│     └─ SMBH contributes, test combined with others
│
├─ Mechanism 2: Distributed Stellar Displacement
│  ├─ Calculate: β_total from all stars (integrate β_i)
│  ├─ Account for: Screening (stars occlude each other)
│  ├─ Predict: v(r) from stellar distribution
│  ├─ Compare: To observed v(r)
│  └─ [Same decision logic as Mechanism 1]
│
├─ Mechanism 3: Gas/Dust Contribution
│  ├─ Measure: HI/H₂ mass distribution from 21cm/CO
│  ├─ Calculate: β_gas(r) from gas displacement
│  ├─ Add to: Stellar contribution
│  ├─ Predict: v(r) from visible matter only
│  └─ [Decision logic]
│
├─ Mechanism 4: Modified k-Law for Diffuse Systems
│  ├─ Hypothesis: k varies with density or scale
│  ├─ Test: Fit k(r) to match rotation curve
│  ├─ Check: Physical plausibility of k(r) function
│  ├─ Compare: To atomic/stellar k values
│  └─ [Decision logic]
│
├─ Mechanism 5: Large-Scale CMB Occlusion
│  ├─ Calculate: E(r,n̂) from galactic mass distribution
│  ├─ Integrate: Pressure field Π(r) from directional occlusion
│  ├─ Predict: v(r) from pressure gradients
│  └─ [Decision logic]
│
└─ Combined Mechanisms
   ├─ IF no single mechanism works:
   │  └─ Test combinations (SMBH + stars + gas + ...)
   ├─ IF multiple mechanisms contribute:
   │  └─ Determine relative importance of each
   └─ Document: Which galaxies are dominated by which mechanisms
```

### Y.2.2 Adaptive Strategy

**Phase 1 (Quick Assessment):** Test each mechanism independently

**Phase 2 (Refinement):** Combine mechanisms that show promise

**Phase 3 (Hypothesis Narrowing):** Identify which mechanisms are necessary

**Phase 4 (Falsification):** Design observations that could disprove SDT predictions

**Phase 5 (Generalization):** Extend successful mechanisms to full galaxy sample

### Y.2.3 Honesty Requirements

- [ ] If a mechanism fails: Document the failure explicitly
- [ ] If predictions are poor: State the error magnitude honestly
- [ ] If fitting is required: Acknowledge it's a fit, not a prediction
- [ ] If uncertainties are large: Report confidence intervals
- [ ] If results are ambiguous: Present alternative interpretations

---

## Y.3 Mechanism 1: SMBH Shadow Chain Hypothesis

### Y.3.1 Physical Mechanism

From Phase 20, Section 20.1.6 (directional occlusion):

- SMBH has enormous displacement volume $V_{\text{disp,SMBH}}$
- Creates pressure deficit in narrow solid angle
- Shadow chains propagate through intervening matter
- Stars/gas sit in compound shadow → experience pressure imbalance

**Question:** Can SMBH-induced long-range pressure gradients explain flat curves?

### Y.3.2 Investigation Procedure

**Step 1: Estimate SMBH displacement**

For Milky Way:
- SMBH mass: $M_{\text{BH}} \approx 4 \times 10^6 M_\odot$ (from stellar dynamics)
- Convert to nucleon count: $N_{\text{BH}} = M_{\text{BH}}/m_p \approx 4.8 \times 10^{57}$ nucleons
- Displacement volume: $V_{\text{disp,SMBH}} = N_{\text{BH}} \times V_n \times \eta_{\text{SMBH}}$
- Where $V_n = 2.76 \times 10^{-45}$ m³ per nucleon (from Phase 15)
- Question: What is $\eta_{\text{SMBH}}$ for compact object? (Unknown, needs investigation)

**Step 2: Calculate pressure field from SMBH**

Using Phase 20, Eq. 20.13:

$$\Pi_s(r) = \Pi_0 - \frac{\kappa V_{\text{disp}} K_{\text{bulk}}}{4\pi r}$$

Gradient:

$$\frac{d\Pi_s}{dr} = +\frac{\kappa V_{\text{disp}} K_{\text{bulk}}}{4\pi r^2}$$

Acceleration:

$$a(r) = -\frac{1}{\rho_s}\frac{d\Pi_s}{dr} = -\frac{\kappa V_{\text{disp}} c^2}{4\pi r^2} = -\frac{\beta_{\text{SMBH}}}{r^2}$$

**Step 3: Predict velocity curve**

For circular orbit: $v^2 = r \times |a(r)| = r \times (\beta_{\text{SMBH}}/r^2) = \beta_{\text{SMBH}}/r$

Result: $v(r) = \sqrt{\beta_{\text{SMBH}}/r}$ ← **This is KEPLERIAN, not flat!**

At large $r$: $v \propto r^{-1/2}$ ← Falls off, doesn't stay flat

**PROBLEM:** SMBH alone cannot explain flat curves.

**Step 4: Check if shadow chains modify this**

Hypothesis: Intervening matter alters pressure transmission.

Calculate transmission function: $T(r,\hat{\mathbf{n}}) = \prod_i [1 - E_i(r,\hat{\mathbf{n}})]$ for stars along ray.

Question: Does this amplify or reduce the gradient?

**Preliminary assessment:** SMBH contribution likely **subdominant** at large radii due to $1/\sqrt{r}$ falloff.

### Y.3.3 Decision Point

```
IF v_SMBH(r) matches v_obs(r) within 20%:
  → SMBH dominant (unlikely based on v ∝ 1/√r)
  → Document success
  → Test on other galaxies

ELSE IF v_SMBH(r) < 0.5 × v_obs(r):
  → SMBH not dominant
  → Move to Mechanism 2 (distributed matter)
  → Keep SMBH as baseline contribution

ELSE IF 0.5 < v_SMBH/v_obs < 1.5:
  → SMBH contributes significantly
  → Test combined SMBH + distributed matter
```

**Current status:** SMBH likely contributes at small $r$ but cannot explain flat curves at large $r$. **Investigation continues with Mechanism 2.**

---

## Y.4 Mechanism 2: Distributed Stellar Displacement Hypothesis

### Y.4.1 Physical Mechanism

Each star contributes $\beta_i = (\kappa V_{\text{disp},i} c^2)/(4\pi)$, and effects add (with screening).

**Question:** Can collective displacement from all stars produce flat curves?

### Y.4.2 Investigation Procedure

**Step 1: Obtain stellar mass distribution**

Data sources:
- SPARC database: Near-IR photometry (traces stellar mass)
- 2MASS, WISE: Near-/mid-IR surface brightness
- Surface brightness profile: $I(R)$ where $R$ = projected radius

Convert to surface density: $\Sigma(R) = I(R) \times (M/L)$

Deproject to 3D density: $\rho_{\text{stars}}(r)$ (Abel transform or assume exponential disk model)

**Step 2: Calculate total displacement within radius r**

For each shell:

$$V_{\text{disp}}(r) = \int_0^r \rho_{\text{stars}}(r') \times \frac{V_{\text{star}}}{M_{\text{star}}} \times 4\pi r'^2 dr'$$

Where $V_{\text{star}}/M_{\text{star}}$: Volume displaced per unit mass

For solar-type stars:
- $N_\odot = M_\odot/m_p \approx 10^{57}$ nucleons
- $V_\odot/M_\odot \approx (N_\odot \times V_n \times \eta)/M_\odot$
- With $\eta \approx 0.64$ (screening factor from Phase 20)

**Step 3: Account for mutual screening**

Problem: Stars occlude each other (similar to atomic screening).

For dense bulge: High screening (most displacement mutually occluded)

For thin disk: Low screening (stars don't shadow each other much)

Hypothesis: Effective displacement

$$V_{\text{eff}}(r) = \int_0^r V_{\text{disp}}(r') \times [1 - E_{\text{internal}}(r')] dr'$$

Where $E_{\text{internal}}(r')$: Average occlusion factor within radius $r'$

**Question:** How to calculate $E_{\text{internal}}$ for galaxy? (Needs investigation)

**Step 4: Calculate β(r) and predict v(r)**

$$\beta(r) = \frac{\kappa V_{\text{eff}}(r) c^2}{4\pi}$$

Circular velocity: $v(r) = \sqrt{\beta(r)/r}$

Compare to observed $v(r)$.

**Step 5: Sensitivity analysis**

Test how $v(r)$ depends on:
- $\eta$ (screening factor): Vary from 0.5 to 0.8
- $\kappa$ (geometric efficiency): Vary from $8.84 \times 10^{-9}$ (calibrated) to $10^{-8}$
- $M/L$ ratio: Uncertainty typically ±30%
- $E_{\text{internal}}(r)$: Try different screening models

Document which parameters matter most.

### Y.4.3 Decision Point

```
IF v_stars(r) matches v_obs(r) within 20% using reasonable parameters:
  → Stellar displacement sufficient!
  → No dark matter needed
  → Test on multiple galaxies
  → Refine screening model

ELSE IF v_stars(r) < 0.7 × v_obs(r):
  → Stars alone insufficient
  → Add gas contribution (Mechanism 3)
  → Or test modified k-law (Mechanism 4)

ELSE IF v_stars(r) > 1.3 × v_obs(r):
  → Too much displacement predicted
  → Check: Is M/L ratio too high?
  → Check: Is screening underestimated?
  → Recalibrate parameters
```

**Current status:** **Investigation in progress.** Requires detailed calculation for benchmark galaxies.

---

## Y.5 Mechanism 3: Gas and Dust Contribution

### Y.5.1 Why This Matters

Conventional analyses often use stellar mass only, neglecting gas:

- **HI (atomic hydrogen):** Traced by 21 cm line
- **H₂ (molecular):** Traced by CO emission (J=1-0 line at 115 GHz)
- **Dust:** Inferred from IR emission
- **Total gas mass:** Can be 10-50% of stellar mass in spirals

**Often neglected but potentially important!**

### Y.5.2 Investigation Procedure

**Step 1: Obtain gas mass distribution**

Data sources:
- HI data: 21 cm maps (VLA, WSRT, ATCA, ASKAP)
- Convert: From brightness temperature to column density $N_{\text{HI}}$
- H₂ data: CO maps (IRAM, ALMA, NRAO)
- Convert: CO intensity → $N_{\text{H₂}}$ using $X_{\text{CO}}$ factor (uncertainty ×2-3)
- Dust: Far-IR/sub-mm (Herschel, Planck) → dust mass → total gas
- Sum: $M_{\text{gas}}(r) = M_{\text{HI}}(r) + M_{\text{H₂}}(r)$

**Step 2: Calculate gas displacement**

$$V_{\text{disp,gas}}(r) = M_{\text{gas}}(r) \times \frac{V_n}{m_p} \times \eta_{\text{gas}}$$

Question: Is $\eta_{\text{gas}}$ same as $\eta_{\text{stars}}$ (0.64) or different?

Hypothesis: Diffuse gas may have less self-screening → $\eta_{\text{gas}} > \eta_{\text{stars}}$?

Test: Use $\eta_{\text{gas}}$ as free parameter, constrain from rotation curves.

**Step 3: Add to stellar contribution**

$$\beta_{\text{total}}(r) = \beta_{\text{stars}}(r) + \beta_{\text{gas}}(r)$$

$$v_{\text{total}}(r) = \sqrt{\frac{\beta_{\text{total}}(r)}{r}}$$

Compare to observed $v(r)$.

**Step 4: Gas fraction analysis**

Define: $f_{\text{gas}}(r) = M_{\text{gas}}(r)/(M_{\text{stars}}(r) + M_{\text{gas}}(r))$

Plot: $f_{\text{gas}}(r)$ vs radius

Check: Where is gas most important?

Typically: $f_{\text{gas}}$ increases at large $r$ (stars drop off faster than gas)

Hypothesis: Gas contribution could flatten outer curve.

### Y.5.3 Decision Point

```
IF v_stars+gas(r) matches v_obs(r) within 15%:
  → Visible matter (stars + gas) sufficient!
  → No dark matter needed
  → Document success
  → Test on gas-rich and gas-poor galaxies

ELSE IF gas contribution is <20% of total:
  → Gas not dominant
  → Continue investigation of other mechanisms

ELSE IF large uncertainty in X_CO or η_gas:
  → Cannot conclude yet
  → Identify observations needed to reduce uncertainty
```

**Current status:** **Investigation in progress.** Gas contribution often neglected but may be crucial.

---

## Y.6 Mechanism 4: The k-Law Investigation

### Y.6.1 Hypothesis

The orbital velocity law $v(r) = (c/k)\sqrt{R_{\text{eff}}/r}$ has been validated for:

- Atoms: $k \approx 137$ (compact, quantum)
- Planets: $k \approx 10^4-10^5$ (well-defined central mass)
- Stars: $k \approx 10^2-10^4$ (stellar systems)

**Question:** Does $k$ require modification for diffuse galactic systems?

### Y.6.2 Investigation Procedure

**Step 1: Test standard k-law**

Assume: $v(r) = (c/k_{\text{gal}})\sqrt{R_{\text{eff}}/r}$

For each galaxy:
- Measure $R_{\text{eff}}$ (effective radius)
- Fit $k_{\text{gal}}$ to match observed $v(r)$
- Check: Is $k_{\text{gal}}$ consistent across galaxies?
- Check: Is $k_{\text{gal}}$ related to galactic properties ($M_{\text{total}}$, size, morphology)?

**Step 2: Compare k_gal to stellar/planetary values**

- Stellar: $k \approx 10^4$ (Sun)
- Fitted: $k_{\text{gal}} \approx ?$ (from rotation curves)

If $k_{\text{gal}} \sim 10^4$: Consistent with stellar systems

If $k_{\text{gal}} \gg 10^5$: Suggests different physics at galactic scales

If $k_{\text{gal}}$ varies widely: May not be a universal constant

**Step 3: Test scale-dependent k(r)**

Hypothesis: $k$ varies with radius (density? local properties?)

Functional forms to test:
- Power law: $k(r) = k_0 \times (r/R_0)^\alpha$
- Broken: $k(r) = k_{\text{inner}}$ for $r < R_{\text{break}}$, $k_{\text{outer}}$ for $r > R_{\text{break}}$
- Smooth transition: $k(r) = k_\infty \times [1 + (r/r_s)^\beta]^\gamma$

For each form: Fit parameters to rotation curve

Check: Physical plausibility of $k(r)$ function

Compare: To theoretical expectations from SDT

**Step 4: Explore z·k² relationship**

From stellar systems: $z \cdot k^2 = 1$ (continuous mass)

From atoms: $z \cdot k^2 = 1/\alpha^2$ (quantized)

Calculate: $z_{\text{gal}}$ for galaxy (if definable)

Test: Does $z_{\text{gal}} \cdot k_{\text{gal}}^2$ equal 1 or some other universal constant?

If yes: Galactic systems follow same law as stellar

If no: Need to understand why galaxies are different

**Step 5: Connection to β parameter**

From Phase 20: $\beta = c^2 R_{\text{eff}}/k^2$

Calculate: $\beta_{\text{gal}}$ from fitted $k_{\text{gal}}$

Compare: To $\beta$ calculated from visible matter displacement

If consistent: k-law works, $\beta$ from displacement works

If inconsistent: Missing displacement, or k-law breaks down

### Y.6.3 Decision Point

```
IF constant k_gal fits all galaxies within 20%:
  → k-law works at galactic scales
  → Determine: k_gal value and uncertainty
  → Check: Does this predict correct β from displacement?

ELSE IF k(r) function provides better fit:
  → Scale-dependent k required
  → Determine: Functional form and physical origin
  → Test: Across galaxy types (spirals, ellipticals, dwarfs)

ELSE IF no k-law formulation works:
  → k-law may not apply to diffuse systems
  → Return to: Direct pressure gradient calculations
  → Or: Fundamentally different mechanism at galactic scales
```

**Current status:** **Investigation in progress.** Requires fitting to rotation curve data.

---

## Y.7 Mechanism 5: Large-Scale CMB Occlusion Patterns

### Y.7.1 Physical Mechanism

From Phase 20, Section 20.1.6:

- Each point in galaxy has filtered local sky: $\Pi(\mathbf{x}) = \int I_\infty(\hat{\mathbf{n}})[1-\chi(\mathbf{x},\hat{\mathbf{n}})] d\Omega$
- Galactic mass distribution creates complex $\chi(\mathbf{x},\hat{\mathbf{n}})$
- Shadow chains through disk/bulge/halo
- Resulting pressure gradients may not follow simple $1/r^2$ law

**Question:** Does directional occlusion significantly alter rotation curves?

### Y.7.2 Investigation Procedure

**Step 1: Set up directional occlusion calculation**

- 3D mass distribution: $\rho(r,\theta,\phi)$ for galaxy
- For each point $\mathbf{x}$: Calculate $\chi(\mathbf{x},\hat{\mathbf{n}})$ for all directions $\hat{\mathbf{n}}$
- Integrate: $\Pi(\mathbf{x}) = \int_{4\pi} I_\infty(\hat{\mathbf{n}})[1-\chi(\mathbf{x},\hat{\mathbf{n}})] d\Omega$
- Gradient: $\nabla\Pi(\mathbf{x})$ gives local acceleration
- For rotation curve: Sample points along galactic plane at various $r$

**Step 2: Simplifications for tractability**

- Full 3D integration is computationally expensive
- Symmetry: Assume axial symmetry (reasonable for disk galaxies)
- Reduces: $\chi(\mathbf{x},\hat{\mathbf{n}}) \to \chi(r,z,\theta)$ where $\theta$ is angle from disk
- Numerical: Use ray-tracing or Monte Carlo integration

**Step 3: Test limiting cases**

**Case A: Thin disk only**
- $\chi(\mathbf{x},\hat{\mathbf{n}})$: Primarily blocked in disk plane directions
- Expected: Pressure deficit in vertical direction
- Effect on $v(r)$: Unclear, calculate numerically

**Case B: Spherical bulge + thin disk**
- $\chi(\mathbf{x},\hat{\mathbf{n}})$: Complex angular dependence
- Bulge: Creates radial pressure gradient (like SMBH but extended)
- Disk: Creates planar structure

**Case C: Include SMBH + distributed matter**
- Combined: Shadow chains from SMBH through disk stars
- Possible: Amplification or screening effects

**Step 4: Numerical calculation**

- Code: Ray tracing through density field
- For grid of $(r,z)$ points: Calculate $a(r,z)$
- Extract: $a_r(r,z=0)$ for rotation curve
- Compare: To simple $\beta/r^2$ expectation
- Check: Does directional occlusion modify the profile?

**Step 5: Scale analysis**

- Estimate: $P_{\text{CMB}}$ required for galactic forces
- From Phase 20: $P_{\text{CMB}}$ depends on $R_e$ (electron exclusion radius)
- For atomic $R_e \sim 10^{-21}$ m: $P_{\text{CMB}} \sim 10^{44}$ Pa
- For galactic separations: Occlusion factors $E \ll 1$
- Question: Is $E$ small enough that simple $\beta/r^2$ works, or do directional effects matter?

### Y.7.3 Decision Point

```
IF directional calculation gives v(r) significantly different from β/r²:
  → Directional effects important
  → Document: How occlusion pattern modifies rotation curve
  → Test: On multiple galaxies

ELSE IF directional ≈ spherical to within 10%:
  → Simplified β/r² approach sufficient
  → Directional complexity not needed
  → Use faster calculations

ELSE IF calculation too expensive/complex:
  → Defer: To future computational work
  → Use: Simplified models with caveat
```

**Current status:** **Computational complexity assessment needed.** May defer to future work.

---

## Y.8 Benchmark Galaxies for Investigation

### Y.8.1 Tier 1: High-Priority Benchmarks

**Milky Way**
- Why: Best data, our home
- Data: Gaia (stellar kinematics), HI surveys, SMBH mass
- Challenge: Inside-out view, uncertainty in Galactic constants
- Test: SMBH + stars + gas mechanisms
- Success metric: $v(R_\odot) = 220$ km/s within 10%

**NGC 3198**
- Why: Classic rotation curve, well-studied
- Data: High-quality HI, optical photometry
- Morphology: Sc spiral, moderate mass
- Test: All mechanisms
- Success metric: Flat curve to 30 kpc within 15%

**M33 (Triangulum)**
- Why: Nearby, resolved, low-mass spiral
- Data: HI, Hα, stellar photometry
- Challenge: Lower surface brightness than Milky Way
- Test: Gas contribution important
- Success metric: Match flat $v \approx 120$ km/s

**DDO 154**
- Why: Dark-matter dominated dwarf (conventionally)
- Data: HI kinematics
- Challenge: Very low surface brightness, gas dominated
- Test: Critical test - can SDT explain without dark matter?
- Success metric: $v_{\text{obs}}/v_{\text{visible}} \sim 10$, explain this ratio

### Y.8.2 Tier 2: Secondary Tests

- M31 (massive spiral)
- NGC 6503 (intermediate mass)
- IC 2574 (dwarf irregular)
- NGC 2403 (late-type spiral)

### Y.8.3 Tier 3: Extended Sample

- SPARC sample: Test on 50-100 galaxies
- Check: Success rate across morphologies
- Identify: Which galaxy types SDT works best for
- Document: Failure modes and outliers

---

## Y.9 Data Sources and Observables

### Y.9.1 Primary Data: Rotation Curves

**High-quality samples:**

**SPARC (Spitzer Photometry & Accurate Rotation Curves)**
- 175 galaxies
- Near-IR photometry (traces stars)
- HI and Hα rotation curves
- Quality flags for each galaxy

**THINGS (The HI Nearby Galaxy Survey)**
- 34 nearby galaxies
- High-resolution HI kinematics
- Resolved rotation curves

**Little THINGS**
- 41 dwarf irregular galaxies
- HI kinematics
- Low-mass systems (dark matter dominated?)

**Individual well-studied galaxies:**
- Milky Way
- M31 (Andromeda)
- M33 (Triangulum)
- NGC 3198 (rotation curve benchmark)
- NGC 6503
- DDO 154 (dark matter dominated dwarf)

### Y.9.2 Secondary Data: Mass Distributions

- Stellar mass: Near-IR photometry (2MASS, WISE, Spitzer)
- Gas mass: HI (21cm) and CO observations
- Bulge/disk decomposition: SDSS, Hubble
- SMBH mass: Stellar dynamics, maser measurements

### Y.9.3 Data Quality Issues

- Inclination: Edge-on ($i \approx 90°$) best, face-on uncertain
- Distance: Affects $M/L$ ratio calibration
- Non-circular motions: Bars, spiral arms cause deviations
- Beam smearing: Low resolution → underestimate $v_{\text{max}}$
- Asymmetric drift: Gas velocity ≠ circular velocity (needs correction)

### Y.9.4 Uncertainty Propagation

- Photometry: ±0.1-0.2 mag → ±20-40% in $M/L$
- Distance: ±10-20% typical
- Inclination: $\sin(i)$ uncertainty → large $v$ uncertainty near face-on
- Gas mass: $X_{\text{CO}}$ factor ±factor of 2-3
- Total: Rotation curves typically ±10-20% uncertainty

---

## Y.10 Comparative Analysis: SDT vs Dark Matter vs MOND

### Y.10.1 Metrics for Comparison

**Accuracy:**
- RMS deviation: $\sqrt{\Sigma(v_{\text{pred}} - v_{\text{obs}})^2/N}$
- Fractional error: Average $|v_{\text{pred}} - v_{\text{obs}}|/v_{\text{obs}}$
- Success rate: Fraction of galaxies fit within 20%

**Predictive power:**
- Dark matter: Requires fitting halo profile (2-5 parameters)
- MOND: Requires fitting $a_0$ (1 parameter, but universal)
- SDT: No free parameters IF mechanisms work (or $\eta$, $\kappa$ if uncertain)

**Physical plausibility:**
- Dark matter: Requires new particle, but simple
- MOND: Empirical fit, no theoretical foundation
- SDT: Geometric mechanism, testable via displacement

**Falsifiability:**
- Dark matter: Could be detected directly
- MOND: Fails for galaxy clusters (requires extra matter anyway)
- SDT: Specific predictions for displacement, screening, k-law

### Y.10.2 Comparison Table Template

| Galaxy | $v_{\text{obs}}$ | $v_{\text{DM}}$ | $v_{\text{MOND}}$ | $v_{\text{SDT}}$ | Error_DM | Error_MOND | Error_SDT |
|--------|-----------------|-----------------|-------------------|-----------------|----------|------------|-----------|
| MW     | 220             | ...             | ...               | ...             | ...      | ...        | ...       |
| NGC3198| 150             | ...             | ...               | ...             | ...      | ...        | ...       |
| ...    | ...             | ...             | ...               | ...             | ...      | ...        | ...       |

### Y.10.3 Honesty Requirement

- [ ] If SDT fails for some galaxies: Report it
- [ ] If dark matter fits better: Acknowledge it
- [ ] If MOND is superior: State why
- [ ] If results are ambiguous: Present all interpretations

---

## Y.11 Adaptive Strategy: Learning from Failures

### Y.11.1 Failure Mode 1: Predicted Velocity Too Low

**Possible causes:**
- Underestimated displacement: Check $M/L$ ratio, gas mass
- Underestimated screening efficiency: Try higher $\eta$
- Missing component: Stellar halo? Extended gas?
- k-law breaks down: Try modified $k(r)$

**Action:**
```
→ Recalibrate: M/L using independent constraints
→ Test: Higher η values (0.7, 0.8 instead of 0.64)
→ Search: For extended components in data
→ If still fails: Document as outlier, investigate further
```

### Y.11.2 Failure Mode 2: Predicted Velocity Too High

**Possible causes:**
- Overestimated displacement: $M/L$ too high
- Underestimated screening: More mutual occlusion than assumed
- Double-counting: SMBH + stars counted twice somehow
- Observational issue: Asymmetric drift not corrected

**Action:**
```
→ Recheck: Mass estimates independently
→ Test: Lower η values (0.5, 0.4)
→ Verify: No double-counting in calculation
→ Check: Observational corrections applied
```

### Y.11.3 Failure Mode 3: Wrong Shape

**Possible causes:**
- Gas contribution important at large $r$
- k-law requires scale-dependence $k(r)$
- Screening changes with radius
- Disk warping or non-circular motions

**Action:**
```
→ Add: Gas contribution (often missing)
→ Test: k(r) functions (power law, broken)
→ Model: Radius-dependent screening
→ Check: Observational data quality at large r
```

### Y.11.4 Failure Mode 4: Dwarf Galaxies Systematically Fail

**Implication:**
- If all dwarfs fail: SDT may require modification at low mass
- If some dwarfs work: Identify what's different
- Question: Is there a critical mass scale?

**Action:**
```
→ Separate: Dwarf analysis from spiral analysis
→ Test: Different mechanisms for different scales?
→ Consider: Whether dwarfs are fundamentally different
→ If cannot explain: Acknowledge limitation
```

### Y.11.5 Learning Protocol

After each galaxy:
- [ ] Document: Which mechanisms were tested
- [ ] Record: Parameter values used
- [ ] Note: What worked and what didn't
- [ ] Update: Prior expectations for next galaxy
- [ ] Refine: Strategy based on accumulating evidence

---

## Y.12 Falsifiable Predictions

### Y.12.1 Prediction 1: Displacement-Velocity Correlation

- Predict: Galaxies with more visible matter should have higher $v_\infty$
- Quantify: $v_\infty \propto (M_{\text{visible}})^\alpha$ where $\alpha \approx 0.5$ if $\beta \propto M_{\text{visible}}$
- Test: Across galaxy sample
- Falsification: If no correlation, SDT fails

### Y.12.2 Prediction 2: Gas-Rich vs Gas-Poor Galaxies

- Predict: Gas-rich galaxies should have less "dark matter" (i.e., less discrepancy)
- Quantify: $\Delta v = v_{\text{obs}} - v_{\text{visible}}$ should be smaller when gas is included
- Test: Compare gas-rich spirals to gas-poor ellipticals
- Falsification: If gas doesn't help, gas displacement is wrong

### Y.12.3 Prediction 3: SMBH Mass Correlation

- Predict: If SMBH contributes, rotation curves should correlate with $M_{\text{BH}}$
- Test: Galaxies with massive SMBHs should have higher $v$ at small $r$
- Falsification: If no correlation, SMBH shadow chains don't work

### Y.12.4 Prediction 4: Scale-Free Nature

- Predict: SDT mechanisms should work across all scales (dwarf to giant)
- No magic scale: Unlike MOND's $a_0$
- Test: Same mechanisms on $10^6 M_\odot$ dwarfs and $10^{12} M_\odot$ giants
- Falsification: If mechanism works for spirals but fails for dwarfs, something's wrong

### Y.12.5 Prediction 5: No Dark Matter in Galaxy Clusters

- Predict: If SDT works for galaxies, should extend to clusters
- Test: Velocity dispersion of galaxies in clusters from visible matter
- Falsification: If clusters require dark matter but galaxies don't, SDT incomplete

**Timeline:**
- Predictions 1-2: Testable now with existing data
- Prediction 3: Testable with SMBH sample
- Prediction 4: Ongoing (test on diverse sample)
- Prediction 5: Phase [Z+1] future work

---

## Y.13 Limitations and Open Questions

### Y.13.1 Current Limitations

**1. Screening model uncertain**
- $\eta = 0.64$ from Phase 20, but for spherical bodies
- Disk galaxies: Non-spherical, how does screening work?
- State: "Screening in disk geometry requires future work"

**2. k-law applicability unknown**
- Works for atoms, planets, stars
- Galaxies: Diffuse, no single central mass
- State: "k-law for extended mass distributions under investigation"

**3. Computational complexity**
- Full directional occlusion: Expensive to compute
- Approximations: May miss important effects
- State: "Full 3D calculations deferred, simplified models used"

**4. Observational uncertainties large**
- $M/L$ ratio: Factor of 2 uncertainty
- Gas mass: Factor of 2-3 uncertainty
- Combined: Predictions uncertain to 50%
- State: "Uncertainties limit precision of SDT tests"

### Y.13.2 Open Questions

**Q1:** Does the k-law require modification for diffuse systems?

**Q2:** What is the correct screening factor $\eta$ for disk galaxies?

**Q3:** Do SMBH shadow chains extend to 10+ kpc scales?

**Q4:** Can dwarf galaxies be explained without dark matter in SDT?

**Q5:** Does directional occlusion significantly alter rotation curves?

---

## Y.14 Numerical Consistency (Relaxed for Investigation)

### Y.14.1 Required Constants (CODATA 2018)

- $c = 299792458$ m/s (exact)
- $K_{\text{bulk}} = 4.6 \times 10^{113}$ Pa (from Phase 20)
- $\rho_s = 5.12 \times 10^{96}$ kg/m³ (from Phase 20)

### Y.14.2 Galaxy-Specific Parameters (With Uncertainties)

- Distance: ±10-20% typical
- $M/L$ ratio: ±30-50% (depends on stellar population models)
- Gas mass: ±factor of 2-3 ($X_{\text{CO}}$ uncertainty)
- SMBH mass: ±20-50% (except Milky Way)

### Y.14.3 Acceptable Error Ranges

Unlike atomic physics (parts per billion), galactic dynamics:

- Excellent agreement: <10% RMS error
- Good agreement: 10-20% RMS error
- Acceptable: 20-30% RMS error (comparable to MOND)
- Poor: >30% RMS error (needs investigation)

### Y.14.4 Honesty in Reporting

- Always report: Mean error, RMS error, and scatter
- Never claim: "Perfect agreement" (observational uncertainties too large)
- Always state: Which parameters were fitted vs predicted
- Always show: Error bars on predictions

---

## Y.15 Dimensional Consistency

**Verification checklist:**

All formulas dimensionally consistent:

- $[\beta] = \text{m}^3/\text{s}^2$ ✓
- $[v] = [c/k]\sqrt{[R/r]} = (\text{m/s})/(\text{dimensionless}) \times \sqrt{(\text{m/m})} = \text{m/s}$ ✓
- $[a] = [\beta/r^2] = (\text{m}^3/\text{s}^2)/\text{m}^2 = \text{m/s}^2$ ✓
- $[V_{\text{disp}}] = \text{m}^3$ ✓
- $[\kappa] = \text{dimensionless}$ ✓
- $[\eta] = \text{dimensionless}$ ✓

---

## Y.16 Summary and Status

### Y.16.1 Investigation Status

**Phase Y is an ongoing investigation, not a completed derivation.**

**Current status:**
- Framework established ✓
- Mechanisms identified ✓
- Decision trees defined ✓
- Benchmark galaxies selected ✓
- Data sources identified ✓
- **Detailed calculations: IN PROGRESS**

**Next steps:**
1. Calculate stellar displacement for benchmark galaxies
2. Test gas contribution
3. Investigate k-law modifications
4. Compare to observations
5. Refine mechanisms based on results

### Y.16.2 Success Criteria (Different from Other Phases)

Phase Y is successful if:

1. **Comprehensive investigation:** All mechanisms tested systematically
2. **Competitive performance:** SDT comparable to MOND (within 20-30% RMS)
3. **Physical insight:** Understand which mechanisms matter and why
4. **Falsifiable:** Clear predictions that could disprove SDT
5. **Honest assessment:** Failures documented as openly as successes

Phase Y is **NOT** required to:

- Match every galaxy perfectly
- Outperform dark matter fits (those have free parameters)
- Explain every anomaly
- Have zero adjustable parameters

**The goal is understanding, not certification.**

---

## Y.17 References

- Phase 15: Gravitation from Spation Pressure Gradients
- Phase 20: Spation Planck Scales, Global Stiffness, and Force Hierarchy
- Phase 21: Screening Factors and the 10⁻⁹ vs 10⁻¹²³ Hierarchy
- Phase 22: Exoplanetary Systems (k-law validation)
- SPARC database: Spitzer Photometry & Accurate Rotation Curves
- THINGS survey: The HI Nearby Galaxy Survey

---

**END OF PHASE Y (INVESTIGATION IN PROGRESS)**

**This phase represents an exploratory investigation of galactic rotation curves using SDT mechanisms. Detailed calculations and comparisons to observations are ongoing. Results will be updated as the investigation progresses.**

