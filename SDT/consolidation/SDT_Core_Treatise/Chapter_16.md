# Chapter 16: References, Constants, and Symbol Index

## Scope of this chapter

This chapter is **Book 16** of the SDT Core Treatise: an extended reference section. It does not introduce new physics or new benchmarks. It provides (1) **primary and supporting sources** for the treatise; (2) a **constants table** of numerical values used or derived in SDT (c, fine structure, Ϟ_H, k_p, k_⊙, solar and nuclear scales, pressure hierarchy, screening factor, CMB); (3) a **symbol index** (R, r, Ϟ, k, κ, z, β, r_c, Ω, O, and related notation) with brief definitions and cross-references to chapters; and (4) a **short reference table** of key solar-system and atomic values for quick lookup. Use this chapter when you need a precise symbol meaning, a constant value, or a source citation without re-reading the full exposition.

**How to use this chapter.** For **symbols**, search the Symbol index for the character (e.g. Ϟ, κ, z); the entry gives a one-line definition and the chapter(s) where it is defined or used. For **numbers**, use the Constants table and the Short reference tables; all values are consistent with the dataset and certified benchmarks. For **sources**, cite the primary dataset and, when relevant, the supporting document (e.g. 09_CANONICAL for formula variants). For **implementation**, combine this chapter with the calculation order and benchmark list in Chapter 12.

---

## Primary and supporting sources

**Primary source (authoritative):**  
*SDT Core Axioms & Mathematical Dataset* — `SDT/consolidation/SDT_CORE_AXIOMS_AND_DATASET.md`.  
Parts I (Core Axioms), II (Benchmark Tests), and III (Standout Formulas) are the single source of truth for the SDT physics engine and for certification. All chapters of the treatise draw from this document.

**Supporting sources:**  
- *09_CANONICAL_SDT_FORMULAS.md* — Canonical formula set; only formulations consistent with the dataset (e.g. κ = 1/√2 at nuclear scale) are included.  
- *05_STRUCTURE_MAP.md* — Structure map of treatise/conversation sections with line ranges.  
- *08_CONSISTENCY_REPORT.md* — Consistency notes (e.g. z×Ϟ² = 1, Rule 7, β vs κ/Ϟ).  
- *06_RAW_FORMULA_LIST.md* — Ten Rules and key equations with section references.  
- Treatise sections in *conversation.md* (see structure map for section numbers and approximate lines).

**Treatise structure:**  
- *00_TREATISE_TITLE_AND_TOC.md* — Working title, table of contents (Chapters 1–13), and word-count checklist.  
- *HANDOFF_FOR_AGENTS_2_3_4.md* — Specification, chapter list and scope, calculation order, falsification vectors, and book-to-agent assignment.

**Note on authority.** In case of conflict between the primary dataset and a supporting source (or between chapters), the dataset takes precedence. The treatise chapters expand and structure the dataset; they do not introduce new axioms or new certified benchmarks beyond what is in Part I–III.

---

## Constants table

Values below are either defined (e.g. c) or derived within SDT from certified benchmarks. They are not “input” coupling constants but outcomes of the geometry and the implementation logic.

| Symbol | Name / meaning | Value (or order) | Source / note |
|--------|----------------|------------------|----------------|
| **c** | Speed of light (propagation speed of medium) | 2.99792458×10⁸ m/s | Defined; CODATA. |
| **α⁻¹** | Fine-structure inverse | 137.035999… ≈ 137.036 | B2: Ϟ_H = c/v_electron. |
| **Ϟ_H** | Hydrogen koppa | 137.036 | B2; same as α⁻¹. |
| **k_p** | Proton displacement parameter | ≈ 26.2 | Trefoil: k_p² = 5 α⁻¹ ≈ 685.18. |
| **k_⊙** | Solar displacement parameter | ≈ 686.6 | B5; k_⊙ = k_p². |
| **R_⊙** | Solar physical radius | 6.957×10⁸ m | Standard value. |
| **r_c(☉)** | Solar c-boundary radius | ≈ 1.48 km (1,476 m) | R_⊙/k_⊙². |
| **z_solar** | Solar gravitational redshift (geometric) | ≈ 2.12×10⁻⁶ | 1/k_⊙²; B5. |
| **P_∞** | Ambient spation pressure (CMB scale) | ≈ 1.39×10⁻¹⁴ Pa | Part I 2.3; from CMB. |
| **P_conf** | Confinement pressure (nuclear) | ≈ 10³⁴ Pa | Part I 2.3; QCD bag scale. |
| **ρ_s** | Spation density (nuclear saturation) | ≈ 2.3×10¹⁷ kg/m³ | 2 P_conf/c². |
| **ξ** | Screening factor | ≈ 6.3×10⁻⁹ | S-01; Earth → nuclear stability. |
| **T_CMB** | CMB temperature (observed) | 2.725 K | B12. |
| **z_boundary** | CMB / boundary redshift | ≈ 1090 | B12; (R_uni/R_boundary) − 1. |
| **R_uni** | Universe radius (static model) | ≈ 48 Gly | Part I 3.1; B12. |
| **κ (nuclear)** | Nuclear virial factor | 1/√2 ≈ 0.7071 | Dataset; Part III F11. |
| **Δ_topo** | Trefoil invariant | 5 | n² − m²; n=3, m=2. |

**Remarks.** The speed of light c is the propagation speed of the spation medium and is taken as defined (CODATA). The fine-structure inverse α⁻¹ and the hydrogen koppa Ϟ_H are identical in value (137.036) but differ in origin: α⁻¹ is usually cited as a coupling constant, whereas in SDT Ϟ_H is the ratio c/v_electron from the Bohr orbit (B2). The solar and proton k values are linked by k_⊙ = k_p² (proton–solar bridge); k_p follows from trefoil topology (k_p² = 5 α⁻¹). The pressure hierarchy (P_∞, P_conf, ρ_s) connects CMB-scale pressure to nuclear confinement. The screening factor ξ is derived from Earth’s field and used in S-01 for nuclear stability. All constants in this table are either universal (c), emergent from benchmarks (Ϟ_H, k_p, k_⊙), or set by the dataset (e.g. κ = 1/√2 at nuclear scale).

---

## Symbol index

**Geometry and occlusion**  
- **R** — Physical surface radius of the body (m). Used in Ω(r), O(r), v(r), r_c = R/Ϟ².  
- **r** — Radial distance from the centre of the body (m).  
- **Ω(r)** — Solid angle subtended by a sphere of radius R at distance r (steradians). Ω(r) = 2π(1 − √(1 − R²/r²)).  
- **O(r)** — Occlusion: fraction of sky blocked. O(r) = Ω(r)/(4π) = R²/(4r²) in far field. Dimensionless.  
- **B1, F9** — Chapter 2.

**Velocity ratio and c-boundary**  
- **Ϟ (koppa)** — Variable velocity ratio: Ϟ ≡ c/v at a given location. At the body surface, Ϟ = k = c/v_surface. At the c-boundary, Ϟ = 1. Dimensionless.  
- **k** — Same as Ϟ at the surface; k = c/v_surface. Used interchangeably in drafting.  
- **κ (kappa)** — In nuclear context, κ = 1/√2; v_surface = cκ. Trefoil topology gives κ ≈ 0.694 ≈ 1/√2.  
- **r_c** — c-boundary radius (m). At r = r_c, orbital velocity = c. r_c = R/Ϟ² = R_phys/k².  
- **R_c** — Same as r_c; “geometric mass” in some phrasing.  
- **Chapters 3, 4, 5.**

**Redshift and scaling**  
- **z** — Gravitational redshift (geometric depth of well). z = R_c/R_phys = 1/k². Identity: z · k² = 1.  
- **α** — Fine-structure constant; α⁻¹ = 137.036 = Ϟ_H.  
- **Chapters 4, 6.**

**Orbital mechanics**  
- **v(r)** — Orbital velocity at radius r. v(r) = (c/Ϟ)√(R/r) = c√(r_c/r).  
- **v_surface** — Orbital velocity at r = R_phys; v_surface = c/Ϟ.  
- **v_escape** — Escape velocity; v_escape = √2 × c/Ϟ.  
- **β** — Orbital parameter (m³/s²); v² = β/r, r_c = β/c². Optional; β = R c²/Ϟ² when v_surface = c/Ϟ.  
- **Rules 4, 5, 6, 7, 9; F1, F10, F16, F17.** Chapter 3.

**Force and acceleration**  
- **a(r)** — Radial acceleration toward the body. a(r) = c² R/(Ϟ² r²) = c² R_c/r².  
- **F** — Force (e.g. centripetal F = m_e v²/a₀ in hydrogen).  
- **Rules 2; B3.** Chapters 3, 6.

**Atomic**  
- **a₀** — Bohr radius.  
- **E_n** — Hydrogen energy level (eV).  
- **λ** — Wavelength (e.g. Lyman series).  
- **Chapters 6.**

**Nuclear**  
- **D** — Deuteron separation (e.g. 1.942 fm in p-p-e model).  
- **E_bind** — Binding energy (e.g. deuteron 2.224 MeV).  
- **μ_p** — Proton magnetic moment; μ_p = e c R/(2√2) with κ = 1/√2.  
- **Chapters 5, 10.**

**Cosmology**  
- **T_CMB, T_obs, T_emit, T_boundary** — CMB and boundary temperatures.  
- **P_spation(r)** — Spation pressure; P_spation(r) = ρ_s c² R_uni/r at cosmological scale.  
- **Chapter 11.**

**Benchmarks and formulas**  
- **B1–B12** — Benchmark tests (geometry, atomic, stellar, rules, paradoxes, classical tests, CMB).  
- **D-01** — Deuteron binding benchmark.  
- **S-01** — Screening factor benchmark.  
- **F1–F17** — Standout formulas (see Chapter 13).  
- **Rules 1–10** — Ten Rules (see Chapter 8).

---

## Short reference table: solar system and atomic

**Solar (B5, B6)**  
| Quantity | Value |
|----------|--------|
| k_⊙ | 686.6 |
| R_⊙ | 6.957×10⁸ m |
| r_c(☉) | 1.48 km |
| z_solar | 2.12×10⁻⁶ |
| v(Earth, 1 AU) | 29.78 km/s |

**Hydrogen (B2, B3, B4)**  
| Quantity | Value |
|----------|--------|
| Ϟ_H | 137.036 |
| v_electron (ground) | 2.188×10⁶ m/s |
| a₀ | 5.292×10⁻¹¹ m |
| Ionisation | 13.606 eV |
| Lyman limit | 91.2 nm |

**Proton / trefoil (Ch 5)**  
| Quantity | Value |
|----------|--------|
| k_p | ≈ 26.2 |
| k_p² | 5 α⁻¹ ≈ 685.18 |
| Δ_topo | 5 (n=3, m=2) |
| a/R | 1/√2 |
| κ | ≈ 0.694 ≈ 1/√2 |

**Nuclear (Ch 10, D-01, S-01)**  
| Quantity | Value |
|----------|--------|
| κ (nuclear) | 1/√2 |
| Deuteron E_bind | 2.224 MeV |
| ξ | 6.3×10⁻⁹ |
| Stable nuclides (S-01) | ~94% predicted |

**CMB (B12)**  
| Quantity | Value |
|----------|--------|
| z_boundary | ≈ 1090 |
| T_obs | 2.725 K |
| R_uni | ≈ 48 Gly |
| T_emit (recombination) | ≈ 2971 K |

---

## Word-count checklist (reference)

The treatise constraint is **2,680–6,064 words per chapter** (inclusive), with a target of ~3,500–4,500 where possible. The official word-count checklist table (target range, actual count, “In range?”) is maintained in **00_TREATISE_TITLE_AND_TOC.md**. After drafting or revising any chapter (including this one), update that table. For Book 16 (this chapter), the same range applies if it is counted as a treatise chapter; if it is treated as an appendix or extended reference only, the editor may choose to waive or adjust the count. See 00_TREATISE_TITLE_AND_TOC.md and HANDOFF_FOR_AGENTS_2_3_4.md for details.

---

## Summary

- **Primary source:** SDT_CORE_AXIOMS_AND_DATASET.md (Parts I–III).  
- **Supporting sources:** 09_CANONICAL, 05_STRUCTURE_MAP, 08_CONSISTENCY_REPORT, 06_RAW_FORMULA_LIST, conversation.md (structure map).  
- **Constants:** c, α⁻¹, Ϟ_H, k_p, k_⊙, R_⊙, r_c(☉), P_∞, P_conf, ρ_s, ξ, T_CMB, z_boundary, R_uni, κ, Δ_topo.  
- **Symbol index:** R, r, Ω, O, Ϟ, k, κ, r_c, z, v(r), β, a(r), and related notation with chapter references.  
- **Short tables:** Solar, hydrogen, proton/trefoil, nuclear, CMB.  
- **Word count:** See 00_TREATISE_TITLE_AND_TOC.md.

---

*Book 16 — Extended reference. No new physics; authority remains SDT_CORE_AXIOMS_AND_DATASET and the treatise chapters 1–13.*
