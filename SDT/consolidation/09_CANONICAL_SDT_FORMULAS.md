# Canonical SDT Formulas (from conversation.md)

**Source:** SDT/conversation.md only.  
**Rule:** Only formulations that are (1) internally consistent, (2) not superseded by an explicit correction, and (3) either in the Ten Rules / CERTIFIED benchmarks or in the CRITICAL CORRECTION block are included. Erroneous variants are listed in 10_DELETION_LOG.md.

---

## Definitions (symbols)

- **R:** surface radius of body (m). **r:** radial distance from centre (m).
- **Ϟ (koppa):** Ϟ ≡ c/v_surface; dimensionless; at c-boundary Ϟ = 1.
- **κ (kappa):** in nuclear context κ = 1/√2; v_surface = cκ.
- **β:** orbital parameter (m³/s²); optional; β = R c²/Ϟ² when v_surface = c/Ϟ.
- **r_c:** c-boundary radius (where orbital v = c). **z:** gravitational redshift.
- **c:** 299,792,458 m/s (propagation speed of the medium).

---

## 1. Geometry and occlusion

- **Solid angle:** Ω(r) = 2π(1 − √(1 − R²/r²)). Source: §4.1, Rule 1.
- **Far field:** Ω(r) ≈ πR²/r². Source: §4.2.
- **Occlusion:** O(r) = R²/(4r²). Source: §4.2, Rule 1, B1.

**Sub-steps:** (a) Definitions: R, r, Ω, O. (b) B1 certifies inverse-square and dimensions.

---

## 2. Orbital mechanics

- **Orbital velocity:** v(r) = (c/Ϟ)√(R/r). Source: Rule 4, §10.4, §11.
- **Surface velocity:** v_surface = c/Ϟ. Source: Rule 5.
- **Escape velocity:** v_escape = √2 × c/Ϟ. Source: Rule 6.
- **c-boundary:** r_c = R/Ϟ²; at r_c, Ϟ = 1. Source: Rule 9, §10.1.
- **Equivalent:** v(r) = c√(r_c/r); r = r_c × Ϟ². Source: §6.3, §10.4.

**Nuclear (first-principles):** v² = c²κ²(R/r); κ = 1/√2; v_surface = cκ = c/2. Source: CRITICAL CORRECTION §10430, §10444.

**Sub-steps:** (a) Definitions: Ϟ, κ, R, r_c. (b) B5, B6, B7, B8 certify orbital use; CRITICAL CORRECTION certifies nuclear κ form.

---

## 3. Parameter definitions

- **Ϟ:** Ϟ ≡ c/v_surface. At c-boundary: Ϟ = 1. Source: Rule 3, §6.1, Rule 9.
- **Ϟ(r):** Ϟ(r) = √(r/r_c). Source: §6.3.
- **Ϟ routes:** Ϟ = c/√(β/R); Ϟ = 1/√z; Ϟ = √(πc/v_rot). Source: Rule 7, §9.
- **κ (nuclear):** κ = 1/2; v_surface = cκ; κ=1 forbidden. Source: §10432, §10434.

**Sub-steps:** (a) Ϟ and κ defined. (b) Relation: at nucleon surface Ϟ = 1/κ = 2 when κ=1/2.

---

## 4. Force and acceleration

- **Acceleration:** a(r) = c²R/(Ϟ²r²). Source: Rule 2.
- **Centripetal (hydrogen):** F = m_e v²/a₀. Source: §7.1, B3.

**Sub-steps:** (a) a(r) from pressure differential. (b) B3 certifies F.

---

## 5. Redshift and spectral

- **Redshift:** z × Ϟ² = 1. Source: §10.2, Appendix C, B5.
- **Spectral Ϟ:** Ϟ = 1/√z. Source: Rule 7.

**Sub-steps:** (a) z defined. (b) B5 verifies z×Ϟ² = 1.

---

## 6. Hydrogen and atomic

- **Ϟ_H:** Ϟ_H = c/v_electron = 137.036. Source: §6.4, B2.
- **Force:** F = m_e v²/a₀. Source: §7.1.
- **Spectrum:** E_n, λ from Ϟ framework; ionisation 13.606 eV. Source: §8, Appendix F, B4.

**Sub-steps:** (a) Definitions: a₀, v_e, Ϟ_H. (b) B2, B4 certify.

---

## 7. Solar and stellar

- **Solar c-boundary:** r_c(☉) = R_☉/Ϟ². Source: §10.1.
- **Planetary v:** v(r) = c√(r_c/r) with Ϟ_☉, r_c. Source: §11.
- **Stellar Ϟ:** from orbital / rotation / spectral (Rule 7). Source: §9, §11–13.

**Sub-steps:** (a) Ϟ_☉, r_c(☉). (b) B5–B8 certify.

---

## 8. Classical tests

- **Shapiro:** Δt = (4R/Ϟ²c) ln(4r₁r₂/b²). Source: §17.2, Appendix C.
- **Perihelion:** Δω = 6πR/(Ϟ²a(1−e²)). Source: §17.3, Appendix C.
- **Light deflection:** δφ (formula in Appendix I). Source: §17.1.

**Sub-steps:** (a) Formulas. (b) B11 certifies.

---

## 9. Nuclear

- **Master (nuclear):** v² = c²κ²(R/r); κ = 1/√2. Source: §10434.
- **Surface:** v_surface = cκ = c/2. Source: §10444.
- **Kinetic/nucleon:** (1/2)m_N c²κ² = m_N c²/4. Source: §10448.
- **Confinement:** P_N κ² = P_N/2. Source: §10450.
- **Mutual velocity:** v²_mutual = c²κ² R_N/d. Source: §10460.
- **Overlap pressure:** P_overlap = κ² P_N. Source: §10476.
- **Deuteron:** E_mag = 2.15 MeV (magnetic); revised p-p-e 2.28 MeV. Source: §10496, §10656.
- **Magnetic moment:** μ_p = e c R/(2√2); already used correct κ. Source: §10488.

**Sub-steps:** (a) All use κ=1/2 explicitly. (b) D-01 certifies deuteron.

---

## 10. CMB and cosmology

- **Redshift:** z = (R_universe/R_boundary) − 1 = 1089. Source: §21296.
- **Temperature:** T_emit = 2971 K; T_obs = 2.73 K (gravitational redshift). Source: §21268.
- **Spation pressure:** P_spation(r) = ρ_s c² R_universe/r. Source: §21240.
- **Decoupling:** Spation pressure vs plasma/radiation (two systems). Source: §21236.

**Sub-steps:** (a) Definitions: R_boundary, R_universe. (b) B12 certifies CMB interpretation.

---

## 11. Constants that emerged

- **137.036:** Ϟ_H = c/v_electron. Source: §6.4, §15.1.
- **Centripetal coefficient:** from geometry. Source: §15.2.
- CODATA/NASA values as outputs. Source: §15.

**Sub-steps:** (a) Listed. (b) Not input to framework.

---

*End of Canonical SDT Formulas. Erroneous variants removed per 10_DELETION_LOG.md.*
