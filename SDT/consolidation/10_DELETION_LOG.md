# SDT conversation.md — Deletion Log (Phase 5)

**Rule:** A formulation is listed as **deleted** only when (1) it expresses the same physical quantity as another formulation in the document, and (2) the document explicitly states it is wrong/superseded, or it is mathematically inconsistent with a formulation marked correct/CERTIFIED. No deletion based on external physics.

---

## Deleted formulations

### 1. Surface velocity = c (nuclear first-principles)

- **What was deleted:** Any statement that at the nucleon (or proton) surface the orbital velocity equals c, or that κ = 1 in the master equation v² = c²κ²(R/r).
- **Where it appeared:** Implicit in earlier nuclear derivations that “normalized” κ=1; explicitly contradicted in §10432 (“I incorrectly ‘normalized’ κ=1. This is **forbidden**”) and §10446 table (“Previous (WRONG): c”).
- **Why deleted:** Document states correct form is v_surface = c/2 = cκ with κ=1/2 (§10444, §10446). Same quantity (surface velocity) has a correct counterpart.
- **Sub-steps:** (a) Deleted: “v_surface = c” or “κ=1” in nuclear context. (b) Reason: CRITICAL CORRECTION table and text.

---

### 2. Kinetic energy per nucleon = (1/2)m_N c² (nuclear)

- **What was deleted:** Single-nucleon kinetic energy written as (1/2)m_N c² without κ².
- **Where it appeared:** §10446 “Previous (WRONG)” column: “(1/2)m_N c²”.
- **Why deleted:** Corrected form given: (1/2)m_N c²κ² = m_N c²/4 (§10448). Same quantity.
- **Sub-steps:** (a) Deleted: E_k = (1/2)m_N c² for nucleon. (b) Reason: Corrected table §10446–10448.

---

### 3. Confinement pressure P_N without κ² (nuclear)

- **What was deleted:** Confinement pressure at nucleon surface written as P_N only (i.e. as if κ=1).
- **Where it appeared:** §10446 “Previous (WRONG)”: “P_N”.
- **Why deleted:** Corrected: P_N κ² = P_N/2 (§10450). Same quantity.
- **Sub-steps:** (a) Deleted: P_conf = P_N (no κ²). (b) Reason: Corrected table §10446, §10450.

---

### 4. v(r) = c√(R/r) with no Ϟ or κ (nuclear/proton first-principles)

- **What was deleted:** Use of v(r) = c√(R/r) (or v² = c²R/r) in nuclear or proton first-principles derivations, which implies v(R)=c and Ϟ=1 or κ=1.
- **Where it appeared:** e.g. §8493 “v(r)=c√(R/r)”, §9108 “v(r)=c√(R/r)” in examples; any nuclear derivation using this without κ.
- **Why deleted:** CRITICAL CORRECTION states master equation is v² = c²κ²(R/r) with κ=1/2 (§10434). Same quantity (orbital velocity); correct counterpart exists. In non-nuclear stellar/planetary context, v(r)=(c/Ϟ)√(R/r) with body-specific Ϟ remains canonical; the bare c√(R/r) is ambiguous (Ϟ=1) and is superseded by the κ-explicit form in nuclear context.
- **Sub-steps:** (a) Deleted: v(r) = c√(R/r) in nuclear first-principles. (b) Reason: §10430–10434; benchmark-style formulas use Ϟ or κ.

---

## Not deleted (no correct counterpart in document)

- **β-based formulas (r_c = β/c², v = √(β/r), Ϟ = c/√(β/R)):** Kept. Document does not state β is “wrong”; later “pure SDT” prefers Ϟ and R but β is still used in §11–13. Relation β = R c²/Ϟ² is consistent. So no deletion; both β and Ϟ forms retained with equivalence noted.
- **κ = 0.694 from topology (π^(1/4)/(√n·(1+(a/R)²)^(1/4))):** Kept. Alternative derivation for κ; document reconciles 0.694 vs 1/√2 as relativistic/topology correction. Not marked wrong; no deletion.
- **Diproton / dineutron unbound:** Explanatory text; no formula contradicted. Not deleted.
- **48 Gyr vs 13.8 Gyr:** Different models; no single “correct” formula deleted from the other.

---

## Summary

| # | Deleted formulation | Reason |
|---|---------------------|--------|
| 1 | v_surface = c (κ=1) in nuclear context | §10432, §10444, §10446 correct form: c/2, κ=1/2 |
| 2 | E_k = (1/2)m_N c² (no κ²) for nucleon | §10446–10448 correct form: (1/2)m_N c²κ² |
| 3 | P_conf = P_N (no κ²) at nucleon | §10446, §10450 correct form: P_N κ² |
| 4 | v(r) = c√(R/r) in nuclear first-principles | §10434 correct form: v² = c²κ²(R/r) |

**Narrative text:** No narrative or explanatory sentences were deleted; only the above equation-level formulations are treated as superseded where they appear in a nuclear first-principles context with an explicit correct counterpart.

---

*End of Deletion Log. See 11_TESTING_REPORT.md for cross-checks.*
