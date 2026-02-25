# SDT conversation.md — Consistency Report (Phase 4)

**Source:** SDT/conversation.md only.  
**Purpose:** Same-quantity formulations, notation conflicts, explicit corrections, benchmark vs formulas, dimensional notes.

---

## 4.1 Same quantity, multiple formulations

### (a) r_c (c-boundary radius)

| Formulation | Location | Notes |
|-------------|----------|--------|
| r_c = β/c² | §5.4 | Uses β; dimensionally correct. |
| r_c = R/Ϟ² | Rule 9, §10.1 | Uses Ϟ, R. Equivalent to β/c² when β = R c²/Ϟ². |

**Consistency:** Mathematically equivalent. Treatise uses both; later “pure SDT” prefers R and Ϟ (no β). No internal contradiction.

---

### (b) v(r) (orbital velocity)

| Formulation | Location | Notes |
|-------------|----------|--------|
| v(r) = (c/Ϟ)√(R/r) | Rule 4, §10.4, §11 | Canonical in treatise. |
| v(r) = c√(r_c/r) = c/√(r/r_c) | §6.3, §10.4 | Same, since Ϟ(r)=√(r/r_c) and at surface Ϟ = c/v_surface. |
| v(r_p) = √(β/r_p) | §5.5 | β form; equivalent when β = R c²/Ϟ² ⇒ v² = c²R/(Ϟ²r). |
| v² = c²κ²(R/r) | §10430 (CRITICAL CORRECTION) | Nuclear; κ = 1/√2. With Ϟ = 1/κ at surface: (c/Ϟ)² = c²κ², so same form. |
| v(r) = c√(R/r) (no Ϟ) | §8493, §9108 (later) | **Contradiction:** implies v(R)=c. Document states v(R)=c/2 in nuclear context. Treat as erroneous in nuclear first-principles context when correct counterpart (κ explicit) exists. |

**Consistency:** Rules 4 and CRITICAL CORRECTION agree when Ϟ = 1/κ (nucleon: κ=1/2 ⇒ Ϟ=2). Any v(r)=c√(R/r) without κ/Ϟ in nuclear section contradicts §10430.

---

### (c) v at surface of a body

| Formulation | Location | Notes |
|-------------|----------|--------|
| v_surface = c/Ϟ | Rule 5 | Body-dependent Ϟ. |
| v_surface = √(β/R) | §11, §13 | β form; c/Ϟ = √(β/R) when Ϟ = c/√(β/R). |
| v_surface = c (κ=1) | Implied where κ=1 used | **Explicitly WRONG:** §10432, §10444 say κ=1 forbidden; correct is c/2. |
| v_surface = cκ = c/2 | §10444 (Corrected table) | For nucleon; κ = 1/2. |

**Consistency:** Canonical: v_surface = c/Ϟ (treatise) or v_surface = cκ with κ=1/2 (nuclear). Any “v_surface = c” or “κ=1” in nuclear first-principles derivation is erroneous per document.

---

### (d) a(r) (acceleration)

| Formulation | Location | Notes |
|-------------|----------|--------|
| a(r) = c²R/(Ϟ²r²) | Rule 2 | Only explicit form in Rules. |

**Consistency:** Single formulation; no conflict. With v² = c²R/(Ϟ²r), a = v²/r gives same. ✓

---

### (e) Redshift relation (z and Ϟ or k)

| Formulation | Location | Notes |
|-------------|----------|--------|
| z × Ϟ² = 1 | §10.2, Rule 7 (Ϟ = 1/√z) | Canonical. |
| z · k² = 1 | (User preference elsewhere; k≡Ϟ) | Same relation, different symbol. |

**Consistency:** No contradiction; k and Ϟ same role.

---

## 4.2 Notation conflicts

- **β vs κ/Ϟ:** Early treatise uses β (m³/s²) for orbits; Rule 7 gives Ϟ = c/√(β/R). Later “CRITICAL CORRECTION” uses only κ and R (no β) for nuclear first-principles. Document does not remove β from treatise; it adds that κ=1/2 must be retained and κ=1 is forbidden. **Resolution:** For canonical set, keep both: (1) treatise/stellar: Ϟ and R (and β only where needed for JPL-style input); (2) nuclear: κ and R, κ=1/2.
- **Ϟ vs κ:** Ϟ = c/v_surface (dimensionless); in nuclear section v_surface = c/2 ⇒ Ϟ_nucleon = 2, so Ϟ = 1/κ for that case. Same physics; different name. No deletion of one; record equivalence where applicable.

---

## 4.3 Explicit corrections (wrong → correct)

| Wrong (document-stated) | Correct (document-stated) | Location |
|-------------------------|---------------------------|----------|
| κ = 1 | κ = 1/2; v² = c²κ²(R/r) with κ explicit | §10430, §10432 |
| Surface velocity = c | Surface velocity = c/2 = 0.707c | §10446 table |
| Kinetic/nucleon = (1/2)m_N c² | Kinetic/nucleon = (1/2)m_N c²κ² = m_N c²/4 | §10448 |
| Confinement pressure P_N | P_N κ² = P_N/2 | §10450 |
| v(r) = c√(R/r) (no κ) in nuclear first-principles | v² = c²κ²(R/r), κ=1/2 | §10434 |

**Deletion rule:** Any formulation that *explicitly* states or implies κ=1 or v_surface=c in a nuclear first-principles context is marked erroneous when the corrected formulation exists in §10430–10450.

---

## 4.4 Benchmark vs formulas

- **B1–B12:** Certified formulas (occlusion, Ϟ, v(r), z×Ϟ², classical tests, CMB) match Rules and §4–19. No formula in treatise contradicts these.
- **D-01:** Deuteron 2.15 MeV (magnetic) or 2.28 MeV (p-p-e); both certified; different models, not a contradiction.
- **Later v(r)=c√(R/r)** (e.g. §8493, §9108): Used in some proton/Earth examples. If interpreted as v(R)=c, contradicts CRITICAL CORRECTION. **Resolution:** In nuclear/proton first-principles, only v²=c²κ²(R/r) is correct; elsewhere v(r)=(c/Ϟ)√(R/r) with body-specific Ϟ is correct. The bare v(r)=c√(R/r) is ambiguous (Ϟ=1 assumed); treat as superseded by κ-explicit form where nuclear.

---

## 4.5 Dimensional and numerical consistency

- **O(r) = R²/(4r²):** [R²/r²] = 1. ✓
- **a(r) = c²R/(Ϟ²r²):** [c²][R]/[r²] = (m/s)²·m/m² = m/s². ✓
- **v(r) = (c/Ϟ)√(R/r):** [c]√[R/r] = m/s. ✓
- **r_c = R/Ϟ²:** [R] = m. ✓
- **z × Ϟ² = 1:** z and Ϟ² dimensionless. ✓
- **Ϟ_H = 137.036:** From c/v_e; dimensionless. ✓

No dimensional inconsistencies in canonical forms.

---

*End of Consistency Report. See 09_CANONICAL_SDT_FORMULAS.md and 10_DELETION_LOG.md.*
