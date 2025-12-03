# AGENT A INSTRUCTIONS — Ontology & Ingredient Foundations

**Agent:** A (Ontology)  
**Status:** READY TO START (No dependencies)  
**Target:** ~45 pages  
**Timeline:** 40-50 hours estimated  

---

## YOUR MISSION

Establish the four fundamental primitives (Space, Matter, Movement, Now) with rigorous definitions, properties, mathematical representations, and physical evidence. You are creating the **foundation** that all other agents will build upon.

---

## DELIVERABLES (5 files)

1. `Preface.md` (2-3 pages)
2. `Chapter_01_Space.md` (8-10 pages)
3. `Chapter_02_Matter.md` (8-10 pages)  
4. `Chapter_03_Movement.md` (10-12 pages)
5. `Chapter_04_Now.md` (8-10 pages)

Plus: `Agent_A_Validation.md` (handoff checklist)

---

## CRITICAL VALUES YOU MUST DEFINE

These values will be used by Agent B and C:

- **K_bulk** = 4.6×10¹¹³ Pa (bulk modulus of spation)
- **ν = v/λ_C** (shunt frequency formula)
- **t = N/ν** (time as oscillation count)
- **V_disp,e** (electron displacement volume)
- **V_disp,p** (proton displacement volume)

**Where to define:**
- K_bulk → `Chapter_01_Space.md`, Section 1.3
- ν formula → `Chapter_03_Movement.md`, Section 3.4
- t formula → `Chapter_04_Now.md`, Section 4.2
- V_disp → `Chapter_02_Matter.md`, Section 2.2

---

## DETAILED CONTENT REQUIREMENTS

See: `Phase_0_Master_Outline.md` → **AGENT A: ONTOLOGY & INGREDIENT FOUNDATIONS**

**Every equation must include:**
1. Symbol definitions
2. Dimensional analysis
3. Limiting case check
4. Numerical example
5. Comparison to conventional physics

**Example format:**
```markdown
**Shunt Frequency:**
$$\nu = \frac{v}{\lambda_C}$$

Where:
- ν: Shunt frequency [Hz = s⁻¹]
- v: Particle velocity [m/s]
- λ_C: Compton wavelength = 2.426×10⁻¹² m

**Dimensional check:**
[m/s] / [m] = [s⁻¹] ✓

**Limiting case:**
v → 0: ν → 0 (no motion, no shunts) ✓

**Numerical example:**
Electron in H ground state:
v = 2.19×10⁶ m/s
ν = 2.19×10⁶ / 2.426×10⁻¹² = 9.0×10¹⁷ Hz ✓
```

---

## VALIDATION CHECKLIST

Before marking complete, verify:

- [ ] All four ingredients precisely defined
- [ ] Properties listed with evidence for each
- [ ] Mathematical framework established
- [ ] What each replaces in conventional physics stated
- [ ] Physical examples for all concepts
- [ ] All constants from CODATA 2018
- [ ] No quantum postulates used
- [ ] Cross-references to Phase 20 verified
- [ ] Ready for Agent B to build derivations

---

## HANDOFF TO AGENT B

Create `Agent_A_Validation.md`:

```markdown
# Agent A → Agent B Handoff

## Critical Values Defined:
- [x] K_bulk = 4.6×10¹¹³ Pa (Chapter_01_Space.md, Section 1.3)
- [x] ν = v/λ_C (Chapter_03_Movement.md, Section 3.4)
- [x] t = N/ν (Chapter_04_Now.md, Section 4.2)
- [x] V_disp,e definition (Chapter_02_Matter.md, Section 2.2)
- [x] V_disp,p definition (Chapter_02_Matter.md, Section 2.2)

## All Ingredients Defined:
- [x] Space (spation) - Chapter 1
- [x] Matter (displacement) - Chapter 2
- [x] Movement (shunt dynamics) - Chapter 3
- [x] Now (time emergence) - Chapter 4

## Status: READY FOR AGENT B ✓
```

---

## START HERE

1. Read `Phase_0_Master_Outline.md` → Agent A section
2. Create `Preface.md` first
3. Then Chapters 1-4 in order
4. Complete `Agent_A_Validation.md`
5. Notify when ready for handoff

**You can begin immediately!**
