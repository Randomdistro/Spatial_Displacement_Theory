# SDT conversation.md — Categorized Formulas (Phase 3)

**Source:** SDT/conversation.md only.  
**Purpose:** Assign every rule and formula to one category; each category has ≥2 sub-steps.

---

## 3.1 Geometry and occlusion

**Definitions**
- R: radius of screening sphere (m). r: distance from centre of sphere to observer (m).
- Ω: solid angle (steradians). O: occlusion = fraction of full sky blocked (dimensionless).

**Equations**
- Ω(r) = 2π(1 − √(1 − R²/r²)). Exact. §4.1, Rule 1.
- Ω(r) ≈ πR²/r² (far field r≫R). §4.2.
- O(r) = Ω/(4π) = R²/(4r²). §4.2, Rule 1.

**Benchmark**
- B1 certifies inverse-square from geometry; dimensional check [O]=1. §4.3.

---

## 3.2 Orbital mechanics

**Definitions**
- v(r): orbital speed at radius r. v_surface: at r=R. v_escape: escape speed from surface.
- r_c: c-boundary radius (where v=c). R: surface radius of body.

**Equations (Ϟ form — treatise / Rules)**
- v(r) = (c/Ϟ)√(R/r). Rule 4, §10.4, §11.
- v_surface = c/Ϟ. Rule 5.
- v_escape = √2 × c/Ϟ. Rule 6.
- r_c = R/Ϟ²; Ϟ(r_c) = 1. Rule 9, §10.1.
- Equivalently: v(r) = c√(r_c/r); r = r_c × Ϟ². §6.3, §10.4.

**Equations (β form — early treatise)**
- v(r_p) = √(β/r_p). §5.5.
- v_surface = √(β/R). §11, §13.
- r_c = β/c². §5.4.

**Equations (κ form — nuclear, corrected)**
- v² = c²κ²(R/r); κ = 1/√2. CRITICAL CORRECTION §10430.
- v_surface = cκ = c/2 (nucleon). §10444.

---

## 3.3 Parameter definitions (Ϟ, κ, β, R_eff)

**Ϟ (koppa)**
- Ϟ ≡ c/v_surface. Rule 3, §6.1.
- At c-boundary: Ϟ = 1. §6.1, Rule 9.
- Ϟ(r) = √(r/r_c). §6.3.
- Routes: Ϟ = c/√(β/R); Ϟ = 1/√z; Ϟ = √(πc/v_rot). Rule 7, §9.

**κ (kappa)**
- In nuclear context: κ = 1/2 (geometric orbital/escape ratio). §6328, §10434.
- v_surface = cκ; κ=1 forbidden. §10432, §10444.
- Alternative (topology): κ = π^(1/4)/(√n·(1+(a/R)²)^(1/4)). §6294.

**β**
- Orbital parameter (m³/s²); v² = β/r; r_c = β/c². §5, Rule 7.
- Relation: β = R c²/Ϟ² when v_surface = c/Ϟ. (Derived.)
- Document later prefers “pure SDT” without β (use Ϟ and R). (Stated in conversation context.)

**R_eff**
- In conversation.md used in “pure SDT” phrasing; same role as R in v(r) and r_c.

---

## 3.4 Force and acceleration

**Definitions**
- a(r): radial acceleration toward body. F: force (e.g. centripetal).

**Equations**
- a(r) = c²R/(Ϟ²r²). Rule 2.
- F = m_e v²/a₀ (hydrogen centripetal). §7.1.

**Benchmark**
- B3 certifies F to 4 sig. fig. against CODATA. §7.

---

## 3.5 Redshift and spectral

**Definitions**
- z: gravitational redshift (dimensionless).

**Equations**
- z × Ϟ² = 1. §10.2, Appendix C.
- Ϟ = 1/√z (spectral route). Rule 7.

**Benchmark**
- B5 verifies z×Ϟ² = 1 for Sun. §10.2.

---

## 3.6 Hydrogen and atomic

**Definitions**
- a₀: Bohr radius. v_e: electron orbital speed. Ϟ_H: hydrogen Ϟ. E_n: energy level. λ: wavelength.

**Equations**
- Ϟ_H = c/v_electron = 137.036. §6.4.
- F = m_e v²/a₀. §7.1.
- E_n, λ from Ϟ framework. §8, Appendix F.
- Ionisation E ≥ 13.606 eV; Ϟ→∞ at r→∞. §8.4.

**Benchmarks**
- B2: Ϟ anchor. B4: spectrum. §6.5, §8.

---

## 3.7 Solar and stellar

**Definitions**
- Ϟ_☉: solar Ϟ. Ϟ_J: Jupiter. r_c(☉): solar c-boundary.

**Equations**
- r_c(☉) = R_☉/Ϟ². §10.1.
- v(r) = c√(r_c/r) for planets. §11.
- Ϟ from orbital / rotation / spectral; β used in derivation. §9, §11–13.

**Benchmarks**
- B5: solar Ϟ. B6: Solar System. B7: Jovian. B8: exoplanets. §10–13.

---

## 3.8 Classical tests (GR)

**Equations**
- Light deflection: δφ (formula in Appendix I). §17.1.
- Shapiro delay: Δt = (4R/Ϟ²c) ln(4r₁r₂/b²). §17.2, Appendix C.
- Perihelion advance: Δω = 6πR/(Ϟ²a(1−e²)). §17.3, Appendix C.

**Benchmark**
- B11: all within error bars. §17.

---

## 3.9 Nuclear

**Definitions**
- κ = 1/√2 for nucleon. R_N: nucleon radius (~0.84 fm). P_N: confinement pressure. d: separation.

**Equations (corrected)**
- v² = c²κ²(R/r); v_surface = cκ = c/2. §10430, §10444.
- Kinetic/nucleon: (1/2)m_N c²κ² = m_N c²/4. §10448.
- P_conf: P_N κ² = P_N/2. §10450.
- v²_mutual = c²κ² R_N/d. §10460.
- P_overlap = κ² P_N. §10476.
- Deuteron: magnetic E_mag = 2.15 MeV; revised p-p-e model 2.28 MeV. §10496, §10656.
- SEMF (phenomenological); neutron = p+e. §10566, §10630.

**Benchmarks**
- D-01: deuteron. §10498, §10821.

---

## 3.10 CMB and cosmology

**Definitions**
- R_boundary, R_universe: radii. z: CMB redshift. T_emit, T_obs: temperatures.

**Equations**
- z = (R_universe/R_boundary) − 1 = 1089. §21296.
- T_emit = 2971 K; T_obs = 2.73 K (gravitational redshift). §21268.
- P_spation(r) = ρ_s c² R_universe/r. §21240.
- Pressure decoupling: spation pressure vs plasma/radiation. §21236.

**Benchmark**
- B12: CMB interpretation. §19.

---

## 3.11 Constants that emerged

**Items**
- 137.036 = Ϟ_H from c/v_electron. §6.4, §15.1.
- Centripetal coefficient from geometry. §15.2.
- CODATA/NASA values matched as outputs, not inputs. §15.

---

*End of Categorized Formulas. See 08_CONSISTENCY_REPORT.md and 09_CANONICAL_SDT_FORMULAS.md.*
