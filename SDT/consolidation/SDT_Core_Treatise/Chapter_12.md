# Chapter 12: Benchmark Suite and Certification

## Context and scope

The SDT framework is validated by a fixed set of benchmarks: geometric foundations, atomic and stellar dynamics, classical tests of gravitation, nuclear binding, cosmology, and the Ten Rules and paradox resolution. These benchmarks are not optional add-ons; they are the certification that the same primitives, occlusion, master equation, and \(z \cdot \varkappa^2 = 1\) yield correct or consistent results across scales. This chapter provides (1) a **master index** of all benchmarks (B1–B12, D-01, S-01) with one-line summary and chapter reference; (2) the **full certification text** for **Benchmark S-01** (screening factor ξ), which appears here in full as specified; (3) the **implementation logic**: calculation order (Part I §4.1) and falsification vectors (Part I §4.2); and (4) **how to use** the benchmarks for validation and falsification. The takeaway is that anyone implementing or testing SDT should use this chapter as the single reference for “what is certified” and “in what order to compute.”

---

## Master index of benchmarks

| ID | Short description | Key formula / relationship | Chapter | Status |
|----|-------------------|----------------------------|---------|--------|
| **B1** | Geometric foundation | \(O(r) = R^2/(4r^2)\); inverse-square from solid angle | 2 | CERTIFIED |
| **B2** | Koppa anchor | \(\varkappa_H = 137.036\); \(\varkappa = 1\) at c-boundary | 6 | CERTIFIED |
| **B3** | Centripetal force (hydrogen) | \(F = m_e v^2/a_0\); 4 sig. fig. vs CODATA | 6 | CERTIFIED |
| **B4** | Hydrogen spectrum | Lyman series; ionisation 13.606 eV; Ϟ framework | 6 | CERTIFIED |
| **B5** | Solar Ϟ (three routes) | Orbital, rotation, spectral → same \(k_\odot \approx 686.6\); \(z \cdot \varkappa^2 = 1\) | 7 | CERTIFIED |
| **B6** | Solar system orbits | \(v(r) = (c/k_\odot)\sqrt{R_\odot/r}\); max error &lt; 0.41% | 7 | CERTIFIED |
| **B7** | Jovian system | Galilean satellites; same \(v(r)\) with Jupiter’s \(k_J\), \(R_J\); max error 0.00% | 7 | CERTIFIED |
| **B8** | Exoplanetary validation | Stellar \(k\) from rotation/z/orbit; \(v_{\text{planet}}\); max error ≈ 2.02% | 7 | CERTIFIED |
| **B9** | Ten Rules codified | Rules 1–10; framework as constitution | 8 | CERTIFIED |
| **B10** | Paradox resolution | Six paradoxes (hierarchy, vacuum, duality, measurement, dark matter, dark energy) | 8 | CERTIFIED |
| **B11** | Classical tests of GR | Light deflection, Shapiro, perihelion; refractive interpretation; within error bars | 9 | CERTIFIED |
| **B12** | CMB interpretation | \(z \approx 1090\), \(T_{\text{obs}} = 2.73\) K; boundary radiator; static Euclidean | 11 | CERTIFIED |
| **D-01** | Deuteron binding | Magnetic ~2.15 MeV or p-p-e ~2.28 MeV; measured 2.224 MeV; κ = 1/√2 | 10 | CERTIFIED |
| **S-01** | Screening factor | ξ ≈ 6.3×10⁻⁹; nuclear stability ~94% | 12 (below) | CERTIFIED |

---

## Calculation order (implementation logic §4.1)

The dataset specifies a fixed sequence for computing the velocity field and related quantities. Use this order when implementing the physics engine or when checking a benchmark.

1. **Define scale.** Choose the body and its physical radius \(R_{\text{phys}}\). Obtain either the surface (or orbital) velocity \(v_{\text{surface}}\) at \(R_{\text{phys}}\), or the gravitational redshift \(z\) for that body.

2. **Compute Ϟ (or k).**  
   \(\varkappa = c/v_{\text{surface}}\) **or** \(\varkappa = 1/\sqrt{z}\).  
   Rule 7: Ϟ can also be obtained from orbital parameter (\(\varkappa = c/\sqrt{\beta/R}\)) or from rotation (\(\varkappa = \sqrt{\pi c/v_{\text{rot}}}\)). All routes must agree for the same body.

3. **Compute c-boundary radius.**  
   \(r_c = R_{\text{phys}}/\varkappa^2\).  
   At \(r = r_c\), orbital velocity equals \(c\) (Rule 9).

4. **Compute velocity field.**  
   \(v(r) = (c/\varkappa)\sqrt{R_{\text{phys}}/r} = c\sqrt{r_c/r}\).  
   This is the master equation (Rule 4, F1).

5. **If atomic or nuclear:** Apply scale-specific rules (e.g. trefoil \(n=3\), \(m=2\) for proton; κ = 1/√2 for nuclear first-principles). See Chapters 5 and 10.

No step introduces an empirical constant (e.g. \(G\) or \(M\)) beyond the inputs \(R_{\text{phys}}\) and \(v_{\text{surface}}\) (or \(z\)). The only “constants” that appear are \(c\) and the geometric outcomes (e.g. Ϟ_H = 137.036 from hydrogen, \(k_\odot = k_p^2\) from the proton–solar bridge).

---

## Falsification vectors (§4.2)

The dataset identifies three areas where the framework is most exposed to falsification. These are not the only possible tests but are the ones explicitly designated for monitoring.

- **Atomic.** **Lamb shift.** The orbital scale in hydrogen is much larger than the nuclear scale (\(d_{\text{orbital}} \approx 3.36\,\alpha^{-2}\,d_{\text{nuclear}}\)). Any SDT treatment of fine structure or Lamb shift must be consistent with this separation. A persistent discrepancy that cannot be explained by geometry or screening would count against the framework.

- **Galactic.** **Rotation curves.** SDT predicts \(v(r) = c\sqrt{R_{\text{occ}}/r}\) with an effective occlusion radius \(R_{\text{occ}}\) that may depend on the mass distribution and screening. Flat or rising rotation curves must be explained by this geometry (and ξ where relevant) without ad hoc dark matter. A systematic mismatch between observed \(v(r)\) and the occlusion-based form for a given mass profile would be a falsification vector.

- **Nuclear.** **³He vs ³H binding.** The binding energy difference between helium-3 and tritium depends on the geometry of the third nucleon and electron-mediated (or magnetic) bonding. SDT’s node geometry and κ = 1/√2 must reproduce the correct trend. A discrepancy that cannot be resolved by improved geometry or screening would count against the framework.

When validating SDT, run the calculation order for the relevant scale and compare with the corresponding benchmark (e.g. B2–B4 for atomic, B6–B8 for stellar, D-01 for deuteron). When considering falsification, prioritise these three vectors and the benchmarks that address them (Chapters 6, 7, 10, 12).

---

## Benchmark S-01: Screening factor — full certification

**What is certified:** The screening factor ξ (ratio of gravitational effect to “bare” displacement volume) is derived from Earth’s measured field and used to predict nuclear stability patterns. **ξ ≈ 6.3×10⁻⁹**; **~94% of stable nuclides** correctly predicted.

**Formulas and logic:** ξ is defined as the ratio that connects the “bare” displacement geometry (e.g. from \(R_{\text{phys}}\) and Ϟ) to the measured gravitational effect at laboratory scale (e.g. Earth’s surface field). From Earth’s measured \(g\) and radius, and the SDT relation between acceleration and \(R_c\) (or \(R/\varkappa^2\)), one infers the effective screening: only a fraction of the naive displacement volume is “active” for the net field. That fraction is ξ. Once ξ is fixed at one scale (Earth), it is used with nuclear geometry (and a semi-empirical mass formula calibrated to ³He, ⁴He) to predict which nuclides are stable. The result is that approximately 94% of known stable nuclides are correctly predicted.

**Commentary:** S-01 ties gravity at laboratory scale to the same displacement picture. It certifies that a single geometric screening factor, combined with nuclear geometry (and SEMF calibrated to ³He, ⁴He), reproduces the stability chart without dark parameters. The SEMF includes the **nuclear pairing term** (δ = ±12/√A MeV; even-even, odd-A, odd-odd) as set out in Chapter 10 (Nuclear pairing structure); pairing is interpreted in SDT as toroidal vortex pairing (magnetic alignment, constructive pressure). So “screening” is not an arbitrary fudge; it is the ratio of observed gravitational effect to the geometric displacement prediction, and it is consistent from laboratory to nuclear scale.

**Experimental / theoretical check:** Earth’s surface field; nuclear stability data. **Status: CERTIFIED.**

---

## How to use the benchmarks for validation

**Implementing the physics engine:**  
Use the calculation order above. For each body (e.g. Sun, Jupiter, a star with exoplanets), obtain \(R_{\text{phys}}\) and \(v_{\text{surface}}\) (or \(z\) or \(\beta\)); compute Ϟ, \(r_c\), and \(v(r)\). Compare planetary or satellite velocities with B6, B7, B8; compare solar Ϟ with B5. For hydrogen, use B2–B4; for deuteron, use D-01; for CMB, use B12.

**Validating against data:**  
For each benchmark, the “What is certified” and “Experimental check” lines state what is being tested. Use the cited data sources (JPL, CODATA, NASA Exoplanet Archive, etc.) and the formulas in the relevant chapters. Fill in “Actual count” or “Result” as needed; confirm that results fall within the certified tolerances (e.g. B6 max error &lt; 0.41%, B5 σ ≈ 0.03%).

**Falsification:**  
If a benchmark fails repeatedly after careful recalculation and updated data, the framework is under pressure. The designated falsification vectors (Lamb shift, rotation curves, ³He vs ³H) are the first to monitor. Document the discrepancy and whether it can be resolved by refining geometry, screening, or calibration (e.g. SEMF) without abandoning the Ten Rules.

**Cross-references:**  
Each benchmark points to specific chapters (see master index). For formulas, use Chapter 13 (formula compendium). For the Ten Rules, use Chapter 8. For paradox resolution, use Chapter 8 (B10).

---

## Compact benchmark summary (by category)

**Geometry and foundation:** B1 (occlusion \(O(r) = R^2/(4r^2)\)).

**Atomic:** B2 (Ϟ_H = 137.036), B3 (centripetal force), B4 (hydrogen spectrum).

**Stellar and planetary:** B5 (solar Ϟ, three routes), B6 (planets), B7 (Jovian moons), B8 (exoplanets).

**Framework and paradoxes:** B9 (Ten Rules), B10 (six paradoxes).

**Classical tests:** B11 (light deflection, Shapiro, perihelion).

**Cosmology:** B12 (CMB, z ≈ 1090, 48 Gyr boundary).

**Nuclear:** D-01 (deuteron binding), S-01 (screening ξ, stability); nuclear pairing structure (δ, SEMF) in Chapter 10.

---

## Checks and cross-references

- **Chapters 2–11:** Each benchmark is treated in detail in the chapter listed in the master index.
- **Chapter 1:** Calculation order and falsification vectors are introduced; this chapter repeats them in full for the benchmark suite.
- **Chapter 8:** B9 (Ten Rules) and B10 (paradox resolution) as the constitution.
- **Chapter 13:** Formula compendium F1–F17 with cross-links to benchmarks.
- **Primary source:** Part II (all benchmarks) and Part I §4.1–4.2 (SDT_CORE_AXIOMS_AND_DATASET).

---

## Summary

- **Master index:** B1–B12, D-01, S-01 with one-line description, key formula, chapter, and status (all CERTIFIED).
- **Calculation order:** (1) Define scale; (2) Ϟ = c/v_surface or 1/√z; (3) r_c = R/Ϟ²; (4) v(r) = (c/Ϟ)√(R/r); (5) atomic/nuclear tweaks as needed.
- **Falsification vectors:** Atomic (Lamb shift), galactic (rotation curves), nuclear (³He vs ³H).
- **S-01 in full:** Screening factor ξ ≈ 6.3×10⁻⁹; ~94% stable nuclides; certification text given above.
- **How to use:** Implement with the calculation order; validate against each benchmark’s “What is certified” and experimental check; monitor falsification vectors.

---

*Sources: Part II (all benchmarks), Part I §4.1–4.2 (SDT_CORE_AXIOMS_AND_DATASET).*
