# AGENT B INSTRUCTIONS — Mathematical Framework & Derivations

**Agent:** B (Mathematics)  
**Status:** WAITING FOR AGENT A  
**Dependencies:** K_bulk, ν, t, V_disp from Agent A  
**Target:** ~47 pages  
**Timeline:** 50-60 hours estimated  

---

## YOUR MISSION

Derive ALL observable physical quantities from the four ingredients using pure geometry and the master equation. Every derivation must be rigorous, dimensionally verified, and numerically validated.

---

## WAIT CONDITION

**DO NOT START until Agent A completes `Agent_A_Validation.md` with:**
- [x] K_bulk = 4.6×10¹¹³ Pa defined
- [x] ν = v/λ_C formula provided
- [x] t = N/ν formula provided
- [x] V_disp,e and V_disp,p defined

**Check:** `../Agent_A_Ontology/Agent_A_Validation.md`

---

## DELIVERABLES (4 files)

1. `Chapter_05_Primary_Observables.md` (12-15 pages)
2. `Chapter_06_Composite_Observables.md` (10-12 pages)
3. `Chapter_07_Electromagnetic.md` (8-10 pages)
4. `Chapter_08_Gravitational.md` (8-10 pages)

Plus: `Agent_B_Validation.md` (handoff checklist)

---

## CRITICAL DERIVATIONS

You must derive from first principles:

**Primary Observables (Ch 5):**
- Frequency: ν = v/λ_C
- Energy: E = hν
- Momentum: p = h/λ
- Force: F = ν⟨Δp⟩
- **Mass: m = ν⟨Δp⟩/a (EMERGENT!)**
- Temperature: kT = h⟨ν⟩
- Entropy: S = k ln Ω(N_shunts)

**Composite (Ch 6):**
- Pressure, Work, Power, Angular Momentum, Action

**EM (Ch 7):**
- Maxwell's equations from pressure propagation
- Electric vs Magnetic from E→0 limit vs helical wake

**Gravitation (Ch 8):**
- β parameter, k-law, orbital mechanics

---

## MATHEMATICAL RIGOR REQUIREMENTS

**Every equation must have:**
1. Clear definition of ALL symbols
2. Dimensional analysis verification
3. Limiting case checks
4. Numerical example (when applicable)
5. Comparison to conventional expression

**At least 2 worked examples per quantity**

---

## VALIDATION CHECKLIST

Before marking complete:

- [ ] All observables derived from ingredients (no circular definitions)
- [ ] Every formula verified against ≥3 textbooks
- [ ] Numerical accuracy: <1% error on all examples
- [ ] Cross-references to experimental data
- [ ] Connection to conventional physics explicit
- [ ] All uses of K_bulk, ν, t match Agent A definitions

---

## HANDOFF TO AGENT C

Create `Agent_B_Validation.md`:

```markdown
# Agent B → Agent C Handoff

## Formulas Provided:
- [x] E = hν (Chapter_05, Section 5.2)
- [x] S = k ln Ω (Chapter_05, Section 5.7)
- [x] L quantization (Chapter_06, Section 6.4)
- [x] All primary observables derived

## Ready for Agent C Thermodynamics: YES / NO
```

---

## START WHEN

Agent A completes and marks `Agent_A_Validation.md` as READY.

Then:
1. Read Agent A's chapters to get exact values
2. Create Chapter 5 (Primary Observables)
3. Chapter 6 (Composite)
4. Chapter 7 (EM)
5. Chapter 8 (Gravitation)
6. Complete `Agent_B_Validation.md`
