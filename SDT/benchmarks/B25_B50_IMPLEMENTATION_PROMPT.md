# Benchmarks B25-B50: Excessively Detailed Validation Prompt (C++ Only)

**Purpose:** Define and complete 50 SDT benchmarks (B25-B74) with full, reproducible validation flows, combining the original B25–B50 set plus the additional validation-list benchmarks.  
**Constraint:** C++ only. Do not use Python.  
**Status:** Implementation-ready specification (aligned to SDT nuclear packing + spation field pipeline).  
**Total Benchmarks:** 50  
**Last Updated:** January 2026

---

## Global Rules (Apply to All Benchmarks)

1. **C++ Only:** All calculators and report generators must be implemented in C++.
2. **Data Provenance:** Experimental values must cite NIST/ENSDF/other sources, used **only** for validation.
3. **No Status Changes Without Math:** Do not change benchmark status unless backed by explicit calculations.
4. **Output Artifacts:** Each benchmark produces:
   - `SDT/benchmarks/B##_validation_report.json`
   - `SDT/benchmarks/B##_validation_results.json` (optional detailed data)
   - Data CSV in `SDT/benchmarks/data/B##_*.csv`
5. **Use SDT Core:** Prefer existing SDT math utilities in `SDT/Code/sdt_navier_cpp`.

### Validation Report Schema (Required)
```json
{
  "benchmark_id": "B##",
  "title": "Name",
  "status": "CERTIFIED | UNDER_INVESTIGATION | DRAFT",
  "inputs": {
    "data_sources": ["NIST ASD", "ENSDF", "..."],
    "data_files": ["SDT/benchmarks/data/B##_data.csv"],
    "constants": ["sdt::P_CMB_ATOMIC", "..."]
  },
  "methods": {
    "equations": ["..."],
    "pipeline": ["step 1", "step 2", "step 3"]
  },
  "results": {
    "total_tested": 0,
    "within_tolerance": 0,
    "max_error_percent": 0.0,
    "mean_error_percent": 0.0,
    "r_squared": 0.0
  },
  "comparison": {
    "metric": "MAPE | RMS | correlation",
    "tolerance": "..."
  },
  "conclusion": "..."
}
```

---

## B25: Alpha-Cluster Geometry Fidelity

**Objective:** Validate SDT alpha-cluster placements (triangle/tetrahedron/octahedron) for symmetry and distance invariants.  
**Inputs:** `AlphaClusterBuilder` outputs, inter-alpha spacing `dist_inter_alpha_fm`.  
**Method:**
1. Build C-12 (triangle), O-16 (tetrahedron), Mg-24 (octahedron).
2. Compute all pairwise distances; compare against expected edge length.
3. Validate centroid at origin and planar constraint for triangle.
4. Validate bond graph: triangle=3 edges, tetra=6, octa=12.
**Metric:** Max deviation in edge length; centroid norm.  
**Pass:** edge error ≤ 1e-9 * d, centroid ≤ 1e-12 * d.  
**Artifacts:** `B25_validation_report.json`, `B25_validation_results.json`.  
**Implementation Steps (C++):**
- Data: none (synthetic geometry).  
- Compute: use `AlphaClusterBuilder` in `sdt_navier_cpp`; generate coordinates; compute pairwise distances; centroid via double precision; bond graph via adjacency from builder.  
- Checks: enforce tolerance on distance variance and centroid magnitude; assert planar constraint for triangle via normal dot test ≤ 1e-12.  
- Output: write full distance matrix to `B25_validation_results.json`; summary metrics to report; log tolerance decisions.  
- Edge cases: guard against floating tolerance drift by using long double for centroid and variance; run with deterministic seed.

---

## B26: Inter-Alpha Occlusion Overlap Correction

**Objective:** Compare analytic occlusion sums vs overlap-corrected occlusion.  
**Inputs:** Alpha clusters + `occlusion_solid_angle_sampled`.  
**Method:**
1. Compute analytic bond occlusion sum.
2. Compute overlap-corrected occlusion via Fibonacci sampling (2k–10k rays).
3. Record relative difference and variance across sample counts.
**Metric:** Relative difference.  
**Pass:** ≤ 10% at 2k samples; ≤ 5% at 10k samples.  
**Implementation Steps (C++):**
- Data: geometry from B25; sampling rays generated procedurally.  
- Compute: use `occlusion_solid_angle_sampled` with ray counts {2k, 5k, 10k}; compute analytic closed-form occlusion; compute overlap-corrected totals.  
- Evaluate: relative diff = |sampled-analytic|/analytic; variance across ray batches.  
- Output: CSV of ray_count, analytic, sampled, rel_diff, variance; JSON summary.  
- Edge cases: ensure deterministic Fibonacci sampler; cap runtime by limiting ray count to 10k; assert analytic ≠ 0.

---

## B27: Nuclear Radius Scaling (Packing → Radius)

**Objective:** Verify packing-based radius scaling vs nuclear radii data.  
**Inputs:** ENSDF radii; SDT packing radius model.  
**Method:**
1. Compute SDT radii for isotopic chains (He, C, O, Ca, Sn).
2. Compare RMS error vs measured values.
3. Fit A^(1/3) scaling and verify correlation.
**Metric:** RMS error, correlation coefficient.  
**Pass:** RMS ≤ 8%, correlation ≥ 0.9.  
**Implementation Steps (C++):**
- Data: ingest radii CSV (add to `SDT/benchmarks/data/B27_radii.csv` with Z,N,R_exp).  
- Compute: `r_sdt = r0 * A^(1/3) * packing_factor(A,Z)` from SDT model; fit r0 via least squares; compute RMS and Pearson r.  
- Output: CSV with A,Z,N,r_exp,r_sdt,residual; JSON with RMS, r, r0.  
- Edge cases: exclude isotopes with missing radii; log any outliers >3σ.

---

## B28: Z_eff (Valence) from Occlusion Geometry

**Objective:** Derive valence Z_eff from occlusion geometry.  
**Inputs:** Occlusion transmission factor Xi_val, Slater trend data.  
**Method:**
1. Compute Xi_val for Z=1–36.
2. Map to Z_eff_val (define formula explicitly).
3. Compare trend to Slater/NIST values (correlation + rank).
**Metric:** Pearson correlation + Kendall rank.  
**Pass:** Pearson ≥ 0.85; Kendall ≥ 0.80.  
**Implementation Steps (C++):**
- Data: Slater/NIST reference in `B28_Zeff_reference.csv`.  
- Compute: Xi_val via occlusion geometry per shell; map to Z_eff_val with explicit formula `Z_eff = Z * Xi_val`; compute Pearson/Kendall.  
- Output: CSV per element with Xi_val, Z_eff_sdt, Z_eff_ref, residuals; JSON summary with correlations.  
- Edge cases: handle noble gas anomalies; ensure monotonic Xi_val in each period.

---

## B29: First Ionization Energy from SDT Pressure

**Objective:** Predict I1 using SDT pressure + occlusion.  
**Inputs:** NIST I1; `P_infinity` formulas; occlusion factors.  
**Method:**
1. Compute r_atom from SDT rules.
2. Compute Z_eff_ion from occlusion.
3. Apply I1 formula from SDT papers.
4. Compare to NIST for Z=1–36.
**Metric:** MAPE (median preferred).  
**Pass:** Median ≤ 15%, max ≤ 40%.  
**Implementation Steps (C++):**
- Data: `B29_I1_reference.csv` (Z, I1_exp).  
- Compute: r_atom via SDT packing; Z_eff_ion from occlusion; I1 = f(P_infinity, r_atom, Z_eff_ion); calculate median and max APE.  
- Output: CSV with I1_exp, I1_sdt, APE; JSON with median, max, N.  
- Edge cases: hydrogen/helium edge cases; ensure units (eV) consistent.

---

## B30: Electron Affinity Trend Consistency

**Objective:** Validate EA trend signs without electron-centric rules.  
**Inputs:** NIST EA.  
**Method:**
1. Use SDT occlusion/shell closure to predict trend sign per period.
2. Compare sign vs NIST orderings.
**Metric:** Trend-sign accuracy.  
**Pass:** ≥ 80% sign match.  
**Implementation Steps (C++):**
- Data: `B30_EA_reference.csv` (Z, EA_exp sign).  
- Compute: derive EA_sign_sdt from occlusion/shell closure energetics; compare to experimental sign; compute accuracy.  
- Output: CSV with signs and match flag; JSON accuracy.  
- Edge cases: noble gases (EA≈0) treat as zero-sign; halogen high EA.

---

## B31: Atomic Radius Canonical Definition

**Objective:** Define SDT canonical radius type and validate trends.  
**Inputs:** NIST radius data (single consistent type).  
**Method:**
1. Define which radius SDT reports (covalent/metallic/vdW).
2. Compute SDT radii and compare only to that type.
3. Validate slope changes at shell closures.
**Metric:** Trend correlation + slope-change position.  
**Pass:** Correlation ≥ 0.85, closure offset ≤ 1 group.  
**Implementation Steps (C++):**
- Data: choose one radius dataset (e.g., covalent) `B31_radii_reference.csv`.  
- Compute: r_sdt via SDT canonical definition; compute Pearson correlation; detect slope-change via finite differences and compare group positions.  
- Output: CSV with r_exp, r_sdt, delta, slope_change flags; JSON with correlation and closure offsets.  
- Edge cases: transition metals (multiple radii definitions); keep dataset consistent.

---

## B32: Shell Closure Prediction from Packing

**Objective:** Predict shell closures via packing transitions.  
**Inputs:** Packing layer capacities; known closures (He, Ne, Ar, Kr, Xe, Rn).  
**Method:**
1. Compute closure points from packing geometry.
2. Compare to known closures.
**Metric:** Correct closure count.  
**Pass:** ≥ 5/6 correct.  
**Implementation Steps (C++):**
- Data: hardcoded closure targets; no external file required.  
- Compute: run packing model; identify closure Z where new layer starts; compare list vs targets.  
- Output: JSON with predicted closures and count of matches; CSV optional.  
- Edge cases: if multiple closures near same Z, choose nearest integer; document tie-break.

---

## B33: Isotope Shift from Neutron Overload (T = N−Z)

**Objective:** Predict isotope shifts in radius/I1 from neutron overload.  
**Inputs:** ENSDF isotope series data.  
**Method:**
1. Compute SDT shift vs N for series (e.g., Ca, Sn, Pb).
2. Compare direction and magnitude.
**Metric:** Direction accuracy + magnitude error.  
**Pass:** Direction 100%; magnitude ≤ 20%.  
**Implementation Steps (C++):**
- Data: `B33_isotope_series.csv` with Z,N,radius_exp,I1_exp.  
- Compute: delta_r_sdt vs N using neutron overload term; delta_I1_sdt similarly; compare sign and magnitude.  
- Output: CSV per isotope with predicted/exp shifts; JSON with direction accuracy and MAPE.  
- Edge cases: skip isotopes with missing data; ensure baseline isotope defined (lowest N).

---

## B34: Binding Energy from Occlusion Constant

**Objective:** Use deuteron-derived k to predict light nuclei binding.  
**Inputs:** Deuteron binding, He-4, C-12, O-16 energies.  
**Method:**
1. Infer k from deuteron occlusion.
2. Apply to alpha clusters for He-4, C-12, O-16.
3. Compare to experimental binding energy.
**Metric:** Percent error.  
**Pass:** He-4 ≤ 10%; C-12/O-16 ≤ 15%.  
**Implementation Steps (C++):**
- Data: `B34_binding_reference.csv` (nuclide, BE_exp MeV).  
- Compute: derive k from deuteron geometry/occlusion; apply to cluster energies; compute percent errors.  
- Output: CSV with BE_exp, BE_sdt, error%; JSON summary.  
- Edge cases: ensure consistent MeV units; document if k is reused elsewhere.

---

## B35: Spin/Parity Proxy via Packing Symmetry

**Objective:** Correlate packing symmetry to spin/parity trends.  
**Inputs:** Ground state spin/parity tables.  
**Method:**
1. Assign symmetry class to nucleus (packing).
2. Predict parity sign and compare.
**Metric:** Parity accuracy.  
**Pass:** ≥ 70%.  
**Implementation Steps (C++):**
- Data: `B35_spin_parity.csv` (Z,N,spin,parity_exp).  
- Compute: symmetry classification from packing; map to predicted parity; compare to exp; compute accuracy.  
- Output: CSV with predictions; JSON accuracy and confusion counts.  
- Edge cases: treat unknown spins as skip; parity only (ignore exact J).

---

## B36: Quadrupole Moments from Packing Geometry

**Objective:** Estimate quadrupole sign/magnitude from cluster anisotropy.  
**Inputs:** Experimental quadrupole moments.  
**Method:**
1. Compute quadrupole tensor from cluster positions.
2. Compare sign and scaled magnitude.
**Metric:** Sign accuracy + normalized error.  
**Pass:** Sign ≥ 80%; magnitude ≤ 30%.  
**Implementation Steps (C++):**
- Data: `B36_quadrupole_reference.csv` (Z,N,Q_exp barns).  
- Compute: positions from packing; quadrupole tensor; principal component sign; scale factor fit; compare.  
- Output: CSV with Q_exp, Q_sdt, sign_match, rel_error; JSON summary.  
- Edge cases: handle spherical cases (Q≈0) by excluding from sign metric.

---

## B37: Screening Factor Geometry (B21 Extension)

**Objective:** Extend screening factors to heavy elements with overlap correction.  
**Inputs:** Occlusion geometry; second-layer packing.  
**Method:**
1. Compute Xi for Z>20 with overlap-corrected occlusion.
2. Compare to Slater/NIST screening trends.
**Metric:** MAPE.  
**Pass:** ≤ 15%.  
**Implementation Steps (C++):**
- Data: `B37_screening_reference.csv` (Z, Xi_ref).  
- Compute: overlap-corrected occlusion via ray tracing; derive Xi_sdt; compute MAPE vs ref.  
- Output: CSV with Xi_ref, Xi_sdt, ape; JSON summary.  
- Edge cases: ensure ray count sufficient (≥5k) to reduce noise; deterministic seeds.

---

## B38: Multi-Electron Occlusion (B24 Extension)

**Objective:** Validate multi-electron occlusion for heavy atoms.  
**Inputs:** NIST ionization energies for Z=21–54.  
**Method:**
1. Compute Z_eff using multi-electron occlusion.
2. Predict I1 and compare to NIST.
**Metric:** Median absolute percent error.  
**Pass:** ≤ 20%.  
**Implementation Steps (C++):**
- Data: `B38_I1_reference.csv` (Z, I1_exp).  
- Compute: multi-electron occlusion per shell; compute Z_eff; predict I1; compute median APE.  
- Output: CSV of predictions; JSON with median and max APE.  
- Edge cases: handle semi-core shielding in transition metals; document any outliers.

---

## B39: Nuclear Charge Radius vs Packing Saturation

**Objective:** Verify saturation behavior when interstitial spaces fill.  
**Inputs:** Charge radii data, packing occupancy models.  
**Method:**
1. Track predicted radius slope changes at saturation.
2. Compare to observed slope shifts.
**Metric:** Slope-change proximity.  
**Pass:** Within ±1 shell.  
**Implementation Steps (C++):**
- Data: `B39_radii_series.csv` (A,Z,R_exp).  
- Compute: detect slope change in R_sdt(A); compare to slope change in R_exp via derivative sign change; compute offset in shell index.  
- Output: JSON with detected change positions; CSV with derivatives.  
- Edge cases: smooth noisy data via small moving average before derivative.

---

## B40: Nuclear Surface Pressure Coupling

**Objective:** Validate SDT coupling between P_infinity and nuclear surface.  
**Inputs:** P_infinity formula; nuclear radii.  
**Method:**
1. Compute surface pressure for multiple nuclei.
2. Validate scaling exponent with radius.
**Metric:** Exponent error.  
**Pass:** ≤ 0.1.  
**Implementation Steps (C++):**
- Data: radii set from B27/B39; no new file required.  
- Compute: P_surface ∝ P_infinity * f(R); fit exponent n in P∝R^n; compare to SDT expected n.  
- Output: JSON with fitted n and error; CSV with R, P_surface.  
- Edge cases: exclude extreme light nuclei where model breaks.

---

## B41: Spation Field Initialization Consistency

**Objective:** Validate P_infinity scaling and monotonicity.  
**Inputs:** compute_p_infinity, hydrogen reference.  
**Method:**
1. Compute P_infinity for hydrogen and scaled densities.
2. Verify monotonic changes with n_e, rho_n, r_n.
**Metric:** Monotonic ordering + sign.  
**Pass:** All monotonic tests pass; no negative values.  
**Implementation Steps (C++):**
- Data: synthetic parameter grid.  
- Compute: sweep n_e, rho_n, r_n; compute P_infinity; assert monotonic trends; assert positivity.  
- Output: CSV grid; JSON pass/fail with violations list.  
- Edge cases: guard against floating underflow; clamp inputs to physical ranges.

---

## B42: Turbine Cell Consistency Test

**Objective:** Validate gamma/kappa/eta bounds and stability.  
**Inputs:** FieldSystem init + add_turbine_source.  
**Method:**
1. Initialize fields.
2. Inject sources with gaussian and step profiles.
3. Validate eta in [0,1], Gamma >= 0.
**Metric:** Constraint violations.  
**Pass:** 0 violations.  
**Implementation Steps (C++):**
- Data: synthetic field setup.  
- Compute: init FieldSystem; add turbine sources; step solver a few ticks; track eta, Gamma, kappa bounds.  
- Output: JSON listing any violations (index, value); CSV time series optional.  
- Edge cases: ensure boundary conditions consistent; run with deterministic seed.

---

## B43: Occlusion Transmission vs Ionization

**Objective:** Correlate Xi_ion with I1 across period.  
**Inputs:** Xi_ion and NIST I1.  
**Method:**
1. Compute Xi_ion for Z=1–36.
2. Compare correlation to I1 trend.
**Metric:** Pearson correlation.  
**Pass:** ≥ 0.8.  
**Implementation Steps (C++):**
- Data: `B43_I1_reference.csv` (Z, I1_exp).  
- Compute: Xi_ion via occlusion; correlate with I1_exp; compute Pearson r.  
- Output: CSV with Xi_ion, I1_exp; JSON with r and p-value.  
- Edge cases: handle low-I1 anomalies (alkali metals).

---

## B44: Periodic Table Emergence from Packing

**Objective:** Show group/period structure emerging from packing.  
**Inputs:** Packing layer model; known group assignments.  
**Method:**
1. Assign groups from packing closure positions.
2. Compare to actual periodic groups.
**Metric:** Group assignment accuracy.  
**Pass:** ≥ 80%.  
**Implementation Steps (C++):**
- Data: `B44_groups_reference.csv` (Z, group_actual).  
- Compute: derive group_sdt from packing closure positions; compare; compute accuracy.  
- Output: CSV with group_sdt, group_actual, match flag; JSON accuracy.  
- Edge cases: handle d/f block offsets; document mapping rules.

---

## B45: CMB Pressure Scaling Across Elements

**Objective:** Validate pressure scaling across Z.  
**Inputs:** P_infinity per element; SDT constants.  
**Method:**
1. Compute P_infinity across Z=1–36.
2. Validate correlation with expected scaling.
**Metric:** Correlation.  
**Pass:** ≥ 0.9.  
**Implementation Steps (C++):**
- Data: none (computed).  
- Compute: P_infinity(Z); compare to expected scaling law; compute correlation.  
- Output: CSV with Z, P_inf; JSON with r.  
- Edge cases: ensure constants consistent with core SDT; check monotonicity.

---

## B46: Metallic vs Non-Metallic Boundary Prediction

**Objective:** Predict metal/non-metal boundary using occlusion + packing.  
**Inputs:** Periodic table classifications.  
**Method:**
1. Define threshold in Z_eff or occlusion.
2. Classify elements and compare.
**Metric:** Classification accuracy.  
**Pass:** ≥ 80%.  
**Implementation Steps (C++):**
- Data: `B46_metallicity_reference.csv` (Z, class_actual).  
- Compute: pick occlusion/Z_eff threshold; classify; compute accuracy/precision/recall.  
- Output: CSV with predicted class; JSON metrics (accuracy, confusion matrix).  
- Edge cases: treat metalloids explicitly; threshold sweep optional.

---

## B47: Phase-Velocity Constraint Consistency

**Objective:** Ensure phase-velocity assumptions remain non-contradictory.  
**Inputs:** Trefoil/phase velocity constraints from SDT docs.  
**Method:**
1. Log phase velocity vs bulk velocity constraints.
2. Confirm consistency with SDT spation flow rules.
**Metric:** Constraint checks.  
**Pass:** All checks true.  
**Implementation Steps (C++):**
- Data: synthetic parameter sweep.  
- Compute: evaluate constraint expressions over ranges; assert inequalities; log any failures.  
- Output: JSON with pass/fail and violating points; CSV optional.  
- Edge cases: guard division by zero; ensure ranges cover expected physical domain.

---

## B48: Nuclear Packing Pathway Enumeration

**Objective:** Enumerate allowed vs forbidden packing transitions.  
**Inputs:** Packing rule set; stable isotope list.  
**Method:**
1. Generate allowed transitions between shells.
2. Compare stability of known isotopes.
**Metric:** Stability alignment.  
**Pass:** ≥ 80% of stable isotopes fall in allowed pathways.  
**Implementation Steps (C++):**
- Data: `B48_stable_isotopes.csv` (Z,N,stable_flag).  
- Compute: generate packing transitions; mark allowed; compare stable isotopes membership; compute coverage %.  
- Output: CSV with allowed flag per isotope; JSON with coverage.  
- Edge cases: treat ambiguous stability as stable if half-life > 1e6 y; document rule set.

---

## B49: Energetic Stability Map

**Objective:** Build stability map from occlusion-based binding energies.  
**Inputs:** Binding energy dataset for Z=1–30.  
**Method:**
1. Compute binding energies via occlusion constant.
2. Mark stable/unstable regions and compare to known stability.
**Metric:** Stability accuracy.  
**Pass:** ≥ 70%.  
**Implementation Steps (C++):**
- Data: `B49_binding_map_reference.csv` (Z,N,stable_flag,BE_exp).  
- Compute: BE_sdt from occlusion; classify stability vs threshold; compare to stable_flag; compute accuracy.  
- Output: CSV with BE_sdt, stability_pred; JSON metrics.  
- Edge cases: define threshold clearly; handle odd-odd nuclei separately if needed.

---

## B50: End-to-End SDT Prediction Pass

**Objective:** End-to-end SDT predictions for Z=1–36 without using NIST in computation.  
**Inputs:** SDT packing, occlusion, spation field, Z_eff.  
**Method:**
1. Compute r_atom, Z_eff, I1, and radius.
2. Compare to NIST only for evaluation.
**Metric:** Median error.  
**Pass:** Median ≤ 20%.  
**Implementation Steps (C++):**
- Data: NIST evaluation set `B50_reference.csv` (r_exp, I1_exp).  
- Compute: fully SDT-derived predictions with no fitted experimental inputs; compute median APE across metrics; report.  
- Output: CSV per element with predictions; JSON summary with median, max, count.  
- Edge cases: ensure pipeline uses only SDT constants; log any fallbacks; treat missing experimental values as skipped.

---

## B51: Nuclear Fusion Cross-Sections

**Objective:** Predict stellar fusion rates (pp, CNO) and lab fusion cross-sections (D-T, D-D, ³He-³He) via pressure-field tunneling.  
**Inputs:** Masses/Q-values (from SDT), Coulomb barrier, fusion datasets (NACRE II/EXFOR for validation only).  
**Method:** Gamow factor with SDT pressure enhancement; integrate ⟨σv⟩ over MB distribution; compute D-T/D-D cross-sections vs E.  
**Metric:** Stellar rates within 10%; cross-sections within order-of-magnitude.  
**Pass:** Solar luminosity reproduced; σ(D-T, 100 keV) ~ 5 b within 10×.  
**Implementation Steps (C++):** implement Gamow+pressure factor; integrate numerically; output CSV of σ(E), ⟨σv⟩(T); JSON summary.

---

## B52: Nuclear Magnetic Moments (Complete)

**Objective:** Extend nuclear moments and quadrupoles across stable isotopes using pressure-field circulation.  
**Inputs:** Nuclear constants; reference moments for validation.  
**Metric:** Magnetic moments ≤1% error (simple cases), quadrupoles ≤5% where applicable.  
**Pass:** Achieve target errors on validation set; document outliers.  
**Implementation Steps (C++):** Schmidt-line baseline + pressure corrections; compute μ and Q; compare to reference CSV; JSON metrics.

---

## B53: Beta Decay Spectra

**Objective:** Full beta spectra (shapes, endpoints, Kurie plots) including allowed/forbidden transitions.  
**Inputs:** Q-values from SDT masses; reference spectra endpoints.  
**Metric:** Endpoint ≤2% error; shape match within experimental bands.  
**Pass:** All tested decays meet endpoint and shape tolerance.  
**Implementation Steps (C++):** implement spectrum generator with Fermi function and SDT pressure corrections; output spectra CSV; JSON stats.

---

## B54: Nuclear Isomerism

**Objective:** Predict isomer excitation energies and lifetimes from SDT packing/pressure barriers.  
**Inputs:** Isomer dataset for validation.  
**Metric:** Excitation energy ≤10%; lifetime order-of-magnitude.  
**Pass:** Majority of set meets both criteria.  
**Implementation Steps (C++):** model barrier heights from packing deformation; compute transition rates; compare.

---

## B55: Quark Confinement

**Objective:** Map SDT pressure confinement to hadronization scale.  
**Inputs:** Hadron size/energy scales for validation.  
**Metric:** Confinement scale within ±10%; qualitative agreement on potential shape.  
**Pass:** Scale and potential shape validated.  
**Implementation Steps (C++):** derive confinement potential; compute characteristic length/energy; compare to reference.

---

## B56: Hadron Mass Spectrum

**Objective:** Estimate hadron masses from SDT confinement energy.  
**Inputs:** PDG hadron masses for validation.  
**Metric:** ≤10% for light hadrons; order-of-magnitude for heavy.  
**Pass:** Targets met on validation subset.  
**Implementation Steps (C++):** apply confinement energy model to hadron states; compare to PDG CSV.

---

## B57: Strong Force Coupling

**Objective:** Derive running coupling analogue from SDT at nuclear scales.  
**Inputs:** Reference α_s(Q) curve for validation.  
**Metric:** Curve shape and magnitude within 20% over tested Q range.  
**Pass:** Meets tolerance across sampled Q.  
**Implementation Steps (C++):** compute SDT coupling vs Q; correlate to reference; output CSV/JSON.

---

## B58: Weak Force Unification

**Objective:** Map SDT pressure-mediated weak coupling to observed G_F scale.  
**Inputs:** Fermi constant for validation.  
**Metric:** Derived coupling within 10% of G_F.  
**Pass:** Within tolerance.  
**Implementation Steps (C++):** compute weak coupling from SDT parameters; compare.

---

## B59: Neutrino Oscillations

**Objective:** Derive oscillation lengths/phases from SDT neutrino wake mechanics.  
**Inputs:** Δm², mixing data for validation.  
**Metric:** Oscillation length within 15%; phase trends correct.  
**Pass:** Meets thresholds on key baselines.  
**Implementation Steps (C++):** compute SDT oscillation parameters; compare to dataset.

---

## B60: Gravitational Wave Polarization

**Objective:** Predict polarization ratios vs LIGO/Virgo reconstructions.  
**Inputs:** GW event polarization posteriors (validation only).  
**Metric:** Polarization ratio within reported uncertainty bands.  
**Pass:** Majority events within bands.  
**Implementation Steps (C++):** compute SDT polarization model; evaluate per event; JSON summary.

---

## B61: Black Hole Thermodynamics

**Objective:** SDT analogue of BH temperature/entropy.  
**Inputs:** Observational/GR reference values.  
**Metric:** Temperature/entropy within 20% where estimable.  
**Pass:** Meets tolerance or documented deviation.  
**Implementation Steps (C++):** derive pressure-based horizon analog; compute T,S; compare.

---

## B62: Neutron Star Structure

**Objective:** Mass-radius curves vs NICER constraints.  
**Inputs:** NS observation bands.  
**Metric:** Curve within NICER credible region.  
**Pass:** Overlaps credible intervals.  
**Implementation Steps (C++):** SDT EOS → TOV-like integration; output M-R CSV; compare.

---

## B63: Gravitational Lensing (Extended)

**Objective:** Extended lensing profiles without dark matter.  
**Inputs:** Strong-lensing reconstructions.  
**Metric:** Einstein radius/enclosed mass within 10%; slope consistent.  
**Pass:** Meets on test set.  
**Implementation Steps (C++):** compute SDT eclipse/pressure lens model; compare profiles.

---

## B64: Frame-Dragging Effects

**Objective:** Predict Lense–Thirring-like effects from SDT flow.  
**Inputs:** GR reference measurements (e.g., Gravity Probe B).  
**Metric:** Precession rate within 10–20%.  
**Pass:** Within stated band.  
**Implementation Steps (C++):** derive frame-drag analogue; compute rates; compare.

---

## B65: X-Ray Spectra

**Objective:** Model high-energy atomic X-ray lines under SDT.  
**Inputs:** Experimental X-ray transition energies.  
**Metric:** ≤1% on key lines.  
**Pass:** Meets tolerance on validation lines.  
**Implementation Steps (C++):** extend atomic solver to X-ray transitions; compare to data.

---

## B66: Molecular Bond Energies

**Objective:** Predict bond dissociation energies for small molecules.  
**Inputs:** Reference bond energies.  
**Metric:** ≤5% on validation set.  
**Pass:** Majority within tolerance.  
**Implementation Steps (C++):** SDT bond occlusion model; compute D0; compare.

---

## B67: Molecular Vibrational Spectra

**Objective:** Vibrational frequencies for key modes.  
**Inputs:** IR/Raman lines for validation.  
**Metric:** ≤2% error on fundamentals.  
**Pass:** Meets threshold for test molecules.  
**Implementation Steps (C++):** compute force constants via SDT; normal modes; compare.

---

## B68: Chemical Reaction Rates

**Objective:** Reaction barriers/rates for exemplar reactions.  
**Inputs:** Kinetics datasets.  
**Metric:** Barriers within 10%; rate constants within order-of-magnitude.  
**Pass:** Meets barriers; rates acceptable.  
**Implementation Steps (C++):** SDT barrier model; Arrhenius-like rates; compare.

---

## B69: Crystal Structure Prediction

**Objective:** Predict stable crystal structures from SDT packing/pressure.  
**Inputs:** Known structures for validation.  
**Metric:** Correct structure/topology for test set; lattice params within few %.  
**Pass:** Majority structures correct.  
**Implementation Steps (C++):** search packing minima; output predicted lattices; compare.

---

## B70: Superconductivity

**Objective:** SDT mechanism for superconducting transition Tc.  
**Inputs:** Tc dataset.  
**Metric:** Tc within order-of-magnitude; trend across families.  
**Pass:** Meets trend; Tc magnitude acceptable.  
**Implementation Steps (C++):** pressure/occlusion pairing model; compute Tc; compare.

---

## B71: Phase Transitions

**Objective:** Model first/second-order transitions and critical exponents.  
**Inputs:** Experimental Tc/critical exponents.  
**Metric:** Tc within 10%; exponents within accepted ranges.  
**Pass:** Meets thresholds on test cases.  
**Implementation Steps (C++):** SDT free-energy analogue; compute exponents; compare.

---

## B72: Stellar Evolution

**Objective:** Stellar tracks (HR diagram) under SDT β-compactness.  
**Inputs:** Stellar catalog tracks for validation.  
**Metric:** Tracks within observational bands; lifetimes within factor ~2.  
**Pass:** Meets track/lifetime targets.  
**Implementation Steps (C++):** integrate stellar structure/evolution with SDT EOS; compare.

---

## B73: Supernova Dynamics

**Objective:** Core-collapse energetics and ejecta profiles.  
**Inputs:** SN observational constraints.  
**Metric:** Explosion energy within factor ~2; nickel yield trend captured.  
**Pass:** Meets energy/yield bounds.  
**Implementation Steps (C++):** SDT pressure-wave model for collapse/bounce; compare.

---

## B74: Large-Scale Structure Formation

**Objective:** Matter power spectrum/growth under SDT (no dark matter).  
**Inputs:** CMB/LSS observational spectra.  
**Metric:** Power spectrum shape within observational envelope.  
**Pass:** Matches envelope across k-range.  
**Implementation Steps (C++):** evolve perturbations with SDT pressure; compare to observed P(k).

---

## Implementation Methodology (C++ Only)

1. **Data Ingest:** Parse CSV with a minimal C++ parser (no external libs required).
2. **Compute:** Use `sdt_navier_cpp` utilities for constants, occlusion, geometry.
3. **Report:** Emit JSON reports matching the schema above.
4. **Track:** Update `SDT/benchmarks/B01_B24_TrackingSheet.csv` (or a B25+ sheet if available).

---

**End of Prompt**
