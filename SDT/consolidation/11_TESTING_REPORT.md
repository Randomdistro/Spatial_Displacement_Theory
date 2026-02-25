# SDT conversation.md — Testing Report (Phase 6)

**Source:** SDT/conversation.md only.  
**Purpose:** Per-category consistency, cross-category consistency, sub-steps verification.

---

## 6.1 Per-category consistency

### Geometry and occlusion (Category 3.1)

- **Check:** No two formulas in 09_CANONICAL for this category contradict. Ω(r) exact; O(r)=R²/(4r²) far-field; O = Ω/(4π). All consistent.
- **Symbols:** R, r, Ω, O defined in category; no undefined symbols.
- **Result:** PASS.

### Orbital mechanics (Category 3.2)

- **Check:** v(r)=(c/Ϟ)√(R/r) and v_surface=c/Ϟ imply at r=R, v(R)=c/Ϟ (consistent). r_c=R/Ϟ² and v(r)=c√(r_c/r) imply v²=c²r_c/r=c²R/(Ϟ²r) ⇒ v=(c/Ϟ)√(R/r). Nuclear v²=c²κ²(R/r) with κ=1/2 and Ϟ=1/κ gives (c/Ϟ)²=c²κ² ⇒ consistent.
- **Symbols:** Ϟ, κ, R, r, r_c, c defined in Definitions or Parameter definitions.
- **Result:** PASS.

### Parameter definitions (Category 3.3)

- **Check:** Ϟ≡c/v_surface and v_surface=c/Ϟ are equivalent. κ=1/2 and “κ=1 forbidden” are consistent. No two definitions of Ϟ or κ conflict.
- **Result:** PASS.

### Force and acceleration (Category 3.4)

- **Check:** a(r)=c²R/(Ϟ²r²). From v²=c²R/(Ϟ²r), a=v²/r gives a=c²R/(Ϟ²r²). Single formulation; F=m_e v²/a₀ is hydrogen-specific. No conflict.
- **Result:** PASS.

### Redshift and spectral (Category 3.5)

- **Check:** z×Ϟ²=1 and Ϟ=1/√z are equivalent. Single relation.
- **Result:** PASS.

### Hydrogen and atomic (Category 3.6)

- **Check:** Ϟ_H=137.036 and F=m_e v²/a₀; spectrum from Ϟ. No internal contradiction.
- **Result:** PASS.

### Solar and stellar (Category 3.7)

- **Check:** r_c(☉)=R_☉/Ϟ²; v(r)=c√(r_c/r); stellar Ϟ from Rule 7. All use same Ϟ, R, r_c. PASS.
- **Result:** PASS.

### Classical tests (Category 3.8)

- **Check:** Shapiro and perihelion use R, Ϟ, c; no second formulation for same observable. PASS.
- **Result:** PASS.

### Nuclear (Category 3.9)

- **Check:** All use κ=1/2; v²=c²κ²(R/r); v_surface=cκ; P_N κ²; v²_mutual=c²κ² R_N/d. No κ=1 or v=c at surface. PASS.
- **Result:** PASS.

### CMB and cosmology (Category 3.10)

- **Check:** z=1089; T_emit, T_obs; P_spation(r); decoupling. Single set of relations. PASS.
- **Result:** PASS.

### Constants that emerged (Category 3.11)

- **Check:** 137.036=Ϟ_H; centripetal; CODATA as output. No formula conflict. PASS.
- **Result:** PASS.

---

## 6.2 Cross-category consistency

### Orbital vs force/acceleration

- **Check:** v(r)=(c/Ϟ)√(R/r) ⇒ v²=c²R/(Ϟ²r). Then a=v²/r=c²R/(Ϟ²r²), which matches Rule 2 a(r)=c²R/(Ϟ²r²). PASS.
- **Mismatch list:** None.

### Redshift vs parameter definition

- **Check:** z×Ϟ²=1 ⇒ Ϟ=1/√z. Rule 7 “Spectral: Ϟ=1/√z” matches. PASS.
- **Mismatch list:** None.

### Nuclear κ vs treatise Ϟ

- **Check:** At nucleon surface v_surface=c/2=cκ (κ=1/2). So Ϟ_nucleon=c/v_surface=2=1/κ. Treatise Rule 5 v_surface=c/Ϟ gives same. No conflict. PASS.

---

## 6.3 Sub-steps verification

**Requirement:** Every list item in 09_CANONICAL has at least two sub-steps (e.g. Definitions + Equations, or Formulas + Benchmark).

| Category | Sub-step (a) | Sub-step (b) | Met |
|----------|---------------|--------------|-----|
| 1. Geometry | Definitions R, r, Ω, O | B1 certifies | Yes |
| 2. Orbital | Definitions Ϟ, κ, R, r_c | B5–B8, CRITICAL CORRECTION | Yes |
| 3. Parameters | Ϟ, κ defined | Ϟ=1/κ at nucleon | Yes |
| 4. Force | a(r), F | B3 | Yes |
| 5. Redshift | z defined | B5 | Yes |
| 6. Hydrogen | Definitions a₀, v_e, Ϟ_H | B2, B4 | Yes |
| 7. Solar | Ϟ_☉, r_c(☉) | B5–B8 | Yes |
| 8. Classical | Formulas | B11 | Yes |
| 9. Nuclear | κ=1/2 in all | D-01 | Yes |
| 10. CMB | R_boundary, R_universe | B12 | Yes |
| 11. Constants | Listed | Not input | Yes |

**Result:** All categories have ≥2 sub-steps. PASS.

---

## 6.4 Deletion log sub-steps

**Requirement:** Every deleted formula has (a) What was deleted, (b) Why.

| # | (a) What was deleted | (b) Why | Met |
|---|------------------------|--------|-----|
| 1 | v_surface=c, κ=1 in nuclear | §10432, §10444, §10446 | Yes |
| 2 | E_k=(1/2)m_N c² (no κ²) | §10446–10448 | Yes |
| 3 | P_conf=P_N (no κ²) | §10446, §10450 | Yes |
| 4 | v(r)=c√(R/r) in nuclear first-principles | §10434 | Yes |

**Result:** PASS.

---

## 6.5 Final pass (09_CANONICAL)

- **Symbol check:** Every formula in 09_CANONICAL uses only R, r, Ϟ, κ, β (optional), r_c, z, c, and body-specific subscripts (☉, H, N). All defined in Definitions or in the same category.
- **Body-specific:** Solar (Ϟ_☉, R_☉, r_c(☉)), hydrogen (Ϟ_H, a₀), nuclear (κ, R_N, P_N) are clearly indicated. Generic “any body” formulas use R, Ϟ or κ without subscript where appropriate.
- **Result:** PASS.

---

## Summary

| Test | Result |
|------|--------|
| Per-category consistency (11 categories) | All PASS |
| Cross-category (orbital–force; redshift–Ϟ; nuclear–treatise) | All PASS |
| Sub-steps in 09_CANONICAL (11 categories) | All have ≥2 sub-steps |
| Deletion log sub-steps (4 entries) | All have (a)+(b) |
| Final symbol and body-specific pass | PASS |

**Overall:** Ruthless testing completed. No inconsistencies remain within the canonical set. Erroneous variants are only those listed in 10_DELETION_LOG.md with a correct counterpart in the document.

---

*End of Testing Report. Fact-finding prompt execution complete. Deliverables: 05–11.*
