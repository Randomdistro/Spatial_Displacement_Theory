# Benchmarks B25-B74: Validation Prompt (C++ Only)

**Purpose:** Validation-focused guide for B25-B74. This mirrors the implementation prompt and enforces C++ only execution.  
**Status:** Active validation plan  
**Created:** January 2026  
**Total Benchmarks:** 50

---

## Global Validation Protocol

1. **C++ only:** No Python scripts. Use C++ executables and CSV input.
2. **Data provenance:** Cite NIST/ENSDF/Planck/SDSS or other sources, but never use their values inside SDT calculations.
3. **Metrics:** Always include tolerance, error stats, and a decision rule.
4. **Artifacts:** Produce JSON reports for each benchmark (schema below).
5. **Status change rule:** Update status only if computations and comparisons are performed.

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

## B25-B74 Validation Checklist (Detailed)

### B25 - Alpha-Cluster Geometry Fidelity
- Validate: edge equality, centroid at origin, planarity for triangle, bond counts.
- Metric: max edge deviation, centroid norm.
- Pass: edge error <= 1e-9 * d, centroid <= 1e-12 * d.

### B26 - Inter-Alpha Occlusion Overlap Correction
- Validate: analytic vs sampled occlusion.
- Metric: relative difference at 2k/10k samples.
- Pass: <= 10% at 2k, <= 5% at 10k.

### B27 - Nuclear Radius Scaling (Packing -> Radius)
- Validate: RMS error vs ENSDF radii; A^(1/3) correlation.
- Pass: RMS <= 8%, correlation >= 0.9.

### B28 - Z_eff (Valence) from Occlusion Geometry
- Validate: trend correlation and rank vs Slater/NIST.
- Pass: Pearson >= 0.85, Kendall >= 0.80.

### B29 - First Ionization Energy from SDT Pressure
- Validate: I1 vs NIST for Z=1-36.
- Pass: median <= 15%, max <= 40%.

### B30 - Electron Affinity Trend Consistency
- Validate: period trend sign matches NIST.
- Pass: >= 80% sign agreement.

### B31 - Atomic Radius Canonical Definition
- Validate: single radius type, trend correlation, shell closure slope shifts.
- Pass: correlation >= 0.85, closure offset <= 1 group.

### B32 - Shell Closure Prediction from Packing
- Validate: closures match He, Ne, Ar, Kr, Xe, Rn.
- Pass: >= 5/6 correct.

### B33 - Isotope Shift from Neutron Overload
- Validate: direction + magnitude of isotope shifts.
- Pass: direction 100%, magnitude <= 20%.

### B34 - Binding Energy from Occlusion Constant
- Validate: He-4, C-12, O-16 binding predictions.
- Pass: He-4 <= 10%, C-12/O-16 <= 15%.

### B35 - Spin/Parity Proxy via Packing Symmetry
- Validate: parity sign accuracy.
- Pass: >= 70%.

### B36 - Quadrupole Moments from Packing Geometry
- Validate: sign + normalized magnitude.
- Pass: sign >= 80%, magnitude <= 30%.

### B37 - Screening Factor Geometry (B21 Extension)
- Validate: Xi trends for Z>20 vs Slater/NIST.
- Pass: MAPE <= 15%.

### B38 - Multi-Electron Occlusion (B24 Extension)
- Validate: I1 for Z=21-54 using multi-electron occlusion.
- Pass: median <= 20%.

### B39 - Nuclear Charge Radius vs Packing Saturation
- Validate: slope-change proximity at saturation.
- Pass: within +/- 1 shell.

### B40 - Nuclear Surface Pressure Coupling
- Validate: scaling exponent vs nuclear radius.
- Pass: exponent error <= 0.1.

### B41 - Spation Field Initialization Consistency
- Validate: monotonic P_infinity scaling.
- Pass: all monotonic checks pass; no negative values.

### B42 - Turbine Cell Consistency Test
- Validate: eta in [0,1], Gamma >= 0 after source injection.
- Pass: 0 violations.

### B43 - Occlusion Transmission vs Ionization
- Validate: Xi_ion correlation to I1.
- Pass: Pearson >= 0.8.

### B44 - Periodic Table Emergence from Packing
- Validate: group/period assignment accuracy.
- Pass: >= 80% correct.

### B45 - CMB Pressure Scaling Across Elements
- Validate: P_infinity scaling correlation across Z.
- Pass: correlation >= 0.9.

### B46 - Metallic vs Non-Metallic Boundary Prediction
- Validate: classification accuracy.
- Pass: >= 80%.

### B47 - Phase-Velocity Constraint Consistency
- Validate: internal phase velocity consistency with SDT constraints.
- Pass: all checks true.

### B48 - Nuclear Packing Pathway Enumeration
- Validate: stable isotope alignment with allowed pathways.
- Pass: >= 80% alignment.

### B49 - Energetic Stability Map
- Validate: stability map accuracy for Z=1-30.
- Pass: >= 70%.

### B50 - End-to-End SDT Prediction Pass
- Validate: overall median error for Z=1-36 properties.
- Pass: median <= 20%.

### B51 - Nuclear Fusion Cross-Sections
- Validate: stellar rates and lab cross-sections vs reference datasets.
- Pass: stellar rates within 10%; cross-sections within order-of-magnitude.

### B52 - Nuclear Magnetic Moments (Complete)
- Validate: magnetic moments and quadrupoles across stable isotopes.
- Pass: <= 1% (moments), <= 5% (quadrupoles) on validation set.

### B53 - Beta Decay Spectra
- Validate: endpoints and spectra shapes.
- Pass: endpoint <= 2%; shape within experimental bands.

### B54 - Nuclear Isomerism
- Validate: excitation energy and lifetime.
- Pass: energy <= 10%; lifetime within order-of-magnitude.

### B55 - Quark Confinement
- Validate: confinement scale and potential shape.
- Pass: scale within +/- 10%; qualitative agreement on shape.

### B56 - Hadron Mass Spectrum
- Validate: hadron masses vs PDG.
- Pass: <= 10% for light hadrons; order-of-magnitude for heavy.

### B57 - Strong Force Coupling
- Validate: running coupling vs reference curve.
- Pass: within 20% over tested Q range.

### B58 - Weak Force Unification
- Validate: derived coupling vs G_F scale.
- Pass: within 10%.

### B59 - Neutrino Oscillations
- Validate: oscillation lengths and phase trends.
- Pass: lengths within 15%; trends consistent.

### B60 - Gravitational Wave Polarization
- Validate: polarization ratios vs event posteriors.
- Pass: majority within reported bands.

### B61 - Black Hole Thermodynamics
- Validate: pressure-based T and S vs reference values.
- Pass: within 20% where estimable.

### B62 - Neutron Star Structure
- Validate: mass-radius curve vs NICER constraints.
- Pass: curve overlaps credible regions.

### B63 - Gravitational Lensing (Extended)
- Validate: Einstein radius and enclosed mass.
- Pass: within 10% on test set.

### B64 - Frame-Dragging Effects
- Validate: precession rates vs GR measurements.
- Pass: within 10-20% band.

### B65 - X-Ray Spectra
- Validate: key lines vs experimental energies.
- Pass: <= 1% on validation lines.

### B66 - Molecular Bond Energies
- Validate: D0 values for small molecules.
- Pass: <= 5% for validation set.

### B67 - Molecular Vibrational Spectra
- Validate: fundamental frequencies for key modes.
- Pass: <= 2% error.

### B68 - Chemical Reaction Rates
- Validate: barriers and rate constants for exemplar reactions.
- Pass: barriers <= 10%; rates within order-of-magnitude.

### B69 - Crystal Structure Prediction
- Validate: structure/topology and lattice parameters.
- Pass: correct structure for majority; lattice params within a few percent.

### B70 - Superconductivity
- Validate: Tc trends across families.
- Pass: Tc within order-of-magnitude and trend correct.

### B71 - Phase Transitions
- Validate: Tc and critical exponents.
- Pass: Tc within 10%; exponents within accepted ranges.

### B72 - Stellar Evolution
- Validate: HR tracks and lifetimes.
- Pass: tracks within observational bands; lifetimes within factor ~2.

### B73 - Supernova Dynamics
- Validate: explosion energy and nickel yield trends.
- Pass: energy within factor ~2; yields capture trend.

### B74 - Large-Scale Structure Formation
- Validate: power spectrum shape vs observations.
- Pass: matches observational envelope across k range.

---

**Note:** For computation steps, formulas, and file layouts, follow  
`SDT/benchmarks/B25_B50_IMPLEMENTATION_PROMPT.md`.
