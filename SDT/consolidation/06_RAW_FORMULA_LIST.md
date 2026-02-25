# SDT conversation.md — Raw Formula List (Phase 2)

**Source:** SDT/conversation.md only.  
**Purpose:** Every explicit Rule and key equation with section reference.

---

## 1. The Ten Rules (§14, approx. lines 1213–1314)

| Rule | Title | Exact statement / formula | Section |
|------|--------|----------------------------|---------|
| 1 | The Occlusion Principle | Ω(r) = 2π(1 - √(1 - R²/r²)); O(r) = R²/(4r²) (far field) | §14 |
| 2 | Pressure-Difference Acceleration | a(r) = c²R/(Ϟ²r²) | §14 |
| 3 | Ϟ-Parameter Definition | Ϟ ≡ c/v_surface (v_surface = orbital velocity at body surface) | §14 |
| 4 | Master Orbital Equation | v(r) = (c/Ϟ)√(R/r) | §14 |
| 5 | Surface Velocity Rule | v_surface = c/Ϟ | §14 |
| 6 | Escape Velocity Rule | v_escape = √2 × c/Ϟ | §14 |
| 7 | Ϟ-Value Calculation | Orbital: Ϟ = c/√(β/R); Spectral: Ϟ = 1/√z; Rotation: Ϟ = √(πc/v_rot) | §14 |
| 8 | Multi-Body Superposition | Accelerations superpose vectorially; each body contributes geometric occlusion share | §14 |
| 9 | c-Boundary Rule | r_c = R/Ϟ²; at r_c, Ϟ(r_c) = 1 (orbital velocity = c) | §14 |
| 10 | Scale Invariance | Same equations, same Ϟ structure, 53 orders of magnitude | §14 |

---

## 2. Other formulas (by section)

### Geometry and occlusion
- Ω(r) = 2π(1 - √(1 - R²/r²)) — §4.1
- Ω(r) ≈ πR²/r² (far field) — §4.2
- O(r) = Ω/(4π) = R²/(4r²) — §4.2, §4.3

### c-boundary and orbital (early, β-based)
- r_c = β/c² — §5.4
- r_s = 2β/c² (Schwarzschild, escape v=c) — §5.4
- v(r_p) = √(β/r_p) — §5.5

### Koppa (Ϟ) and orbital (treatise)
- Ϟ ≡ c/v_orbital; Ϟ = 1 at r = r_c — §6.1
- v(r) = c × √(r_c/r) = c/√(r/r_c) — §6.3
- Ϟ(r) = √(r/r_c) — §6.3
- Ϟ_H = c/v_electron = 137.036 — §6.4
- r_c = R/Ϟ² (solar); r_c(☉) = R_☉/Ϟ² — §10.1, Rule 9
- v(r) = c/Ϟ = c × √(r_c/r); r = r_c × Ϟ² — §10.4
- z × Ϟ² = 1 — §10.2
- v_surface = √(β/R); Ϟ_J = c/v_surface — §11 (Jupiter), §13 (exoplanets)

### Force and centripetal
- F = m_e v²/a₀ — §7.1

### Classical tests (Appendix C / §17)
- z × Ϟ² = 1 — §10.2, Appendix C
- Shapiro: Δt = (4R/Ϟ²c) ln(4r₁r₂/b²) — §17.2
- Perihelion: Δω = 6πR/(Ϟ²a(1−e²)) — §17.3

### Nuclear (κ-based, corrected)
- v² = c²κ²(R/r); κ = 1/2 = 0.7071 — CRITICAL CORRECTION §10430
- v_surface = cκ = c/2 (nucleon) — §10444
- Kinetic energy/nucleon: (1/2)m_N c²κ² = m_N c²/4 — §10448
- Confinement pressure: P_N κ² = P_N/2 — §10450
- v²_mutual = c²κ² R_N/d — §10460
- P_overlap = κ² P_N = P_N/2 — §10476
- μ_p = e c R/2√2 (magnetic moment; already had κ correct) — §10488

### Nuclear (alternative κ from topology)
- κ = π^(1/4) / (√n · (1+(a/R)²)^(1/4)); n=3, a/R=1/2 → κ≈0.694 — §6294, §8835
- κ = v_orb/c = 1/√2 (orbital/escape ratio) — §6416, §6328

### CMB / cosmology
- P_spation(r) = ρ_s c² R_universe / r — §21240
- z = (R_universe/R_boundary) − 1 = 1089 — §21296
- T_emit = 2971 K; T_obs = 2.73 K (gravitationally redshifted) — §21268

---

## 3. Benchmark-certified formulas (Appendix D + in-text)

| ID | Certified formula / relationship | Key metric |
|----|-----------------------------------|------------|
| B1 | O(r) = R²/(4r²); inverse-square from geometry | Geometric foundation |
| B2 | Ϟ = 1 at c-boundary; Ϟ_H = 137.036 | Koppa anchor |
| B3 | F = m_e v²/a₀ (centripetal) | 4 sig. fig. |
| B4 | Hydrogen spectrum from Ϟ framework | Lyman series |
| B5 | z×Ϟ² = 1; three routes to solar Ϟ | σ = 0.03% |
| B6 | v(r) from Ϟ_☉, r_c | Max error 0.41% |
| B7 | Jovian system same Ϟ framework | Max 0.00% |
| B8 | Exoplanetary v from stellar Ϟ | Max 2.02% |
| B9 | Rules 1–10 codified | Framework |
| B10 | Paradox resolutions | 6 paradoxes |
| B11 | Light deflection, Shapiro, perihelion | Within error bars |
| B12 | CMB z from pressure mechanism | Pressure |
| D-01 | Deuteron binding (magnetic 2.15 MeV; later p-p-e 2.28 MeV) | 3.1% / 2.5% |
| S-01 | Screening factor ξ | CERTIFIED |

---

## 4. Constant and parameter definitions

- **β:** body's orbital parameter (m³/s²); v² = β/r; r_c = β/c². (§5, §7 Rule 7, §11–13)
- **Ϟ (koppa):** Ϟ ≡ c/v_surface; dimensionless. At c-boundary Ϟ = 1. (§6, Rule 3, 9)
- **κ (kappa):** nuclear/proton context: κ = 1/√2; v_surface = cκ; v² = c²κ²(R/r). (CRITICAL CORRECTION §10430)
- **R:** body surface radius (m).
- **R_eff:** effective radius (used in “pure SDT” phrasing elsewhere; in conversation.md same role as R in v(r), r_c).
- **r_c:** c-boundary radius; v = c; r_c = β/c² or r_c = R/Ϟ².
- **z:** gravitational redshift; z × Ϟ² = 1.

---

*End of Raw Formula List. See 07_CATEGORIZED_FORMULAS.md for categories and 08_CONSISTENCY_REPORT.md for conflicts.*
