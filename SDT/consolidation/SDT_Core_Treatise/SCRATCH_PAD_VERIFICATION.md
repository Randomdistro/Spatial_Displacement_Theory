# Scratch pad: claim verification for SDT Core Treatise

Verification of key claims against *SDT Core Axioms & Mathematical Dataset* (Parts I–III) and supporting sources. Entries: **Claim** (from treatise or dataset) → **Source** → **Status**.

---

## System instruction and primitives

| Claim | Source | Status |
|-------|--------|--------|
| Universe = Euclidean lattice of discrete units (spations) under hydrostatic pressure from cosmic boundary | Dataset intro | ✓ Matches |
| Four primitives: Space, Matter, Movement, Now | Dataset; conversation.md §2 | ✓ Matches |
| c = 2.99792458×10⁸ m/s | Dataset Part I 1.1; Ch16 | ✓ Matches |
| Spation diameter 1.616×10⁻³⁵ m | Ch1 (conversation.md §2.1) | ✓ In source |
| Energy, force, acceleration not primitive | Dataset implied; conversation §2.5 | ✓ Matches |

---

## Notation (Ϟ, k, κ, z, R_c)

| Claim | Source | Status |
|-------|--------|--------|
| Ϟ = variable velocity ratio c/v; at c-boundary Ϟ = 1 | Dataset intro, Part I 1.1 | ✓ Matches |
| k = c/v_surface (drafting) | Dataset intro, F2, F3 | ✓ Matches |
| κ = 1/√2 at nuclear scale (dataset uses this value) | Part III F11, F12; 09_CANONICAL §9 | ✓ Matches |
| k = 1 is not forbidden (at c-boundary k = 1) | Operator correction; dataset: at r_c, Ϟ = 1 | ✓ Correct |
| z = R_c/R_phys; z·k² = 1 | Part I 1.2, F2 | ✓ Matches |
| R_c = R_phys/k² | Part I 1.1, Rule 9 | ✓ Matches |

---

## Master equation and velocity field

| Claim | Source | Status |
|-------|--------|--------|
| v² = c² R_c/r | Part I 1.1, F1 | ✓ Matches |
| v(r) = (c/k)√(R_phys/r) | Part I 1.1, F1 | ✓ Matches |
| Derivation from dP/dr = −ρ_s(v²/r), boundary v(R_c)=c | Part III F1 | ✓ Matches |
| a(r) = c² R_c/r² (F10, Rule 2) | Part III F10, 06_RAW Rule 2 | ✓ Matches |
| v_escape = √2 × c/Ϟ (F16, Rule 6) | Part III F16, Rule 6 | ✓ Matches |
| Ϟ(r) = √(r/r_c) (F17) | Part III F17 | ✓ Matches |

---

## Occlusion and geometry

| Claim | Source | Status |
|-------|--------|--------|
| Ω(r) = 2π(1 − √(1 − R²/r²)) | Part II B1, Part III F9 | ✓ Matches |
| Far field Ω(r) ≈ πR²/r² | Part II B1 | ✓ Matches |
| O(r) = R²/(4r²); [O] = 1 | Part II B1, F9 | ✓ Matches |

---

## Redshift and scaling

| Claim | Source | Status |
|-------|--------|--------|
| z·k² = 1 (F2) | Part I 1.2, F2 | ✓ Matches |
| k_solar = k_proton²; k_p ≈ 26.2, k_⊙ ≈ 686.6 | Part I 1.2, F3; B5 | ✓ Matches |
| k_p² = 5 α⁻¹ ≈ 685.18 (trefoil) | Part I 1.3, F4 | ✓ Matches |
| α⁻¹ = Ϟ_H ≈ 137.036 | Part II B2, F3 | ✓ Matches |

---

## Calculation order and falsification

| Claim | Source | Status |
|-------|--------|--------|
| Order: (1) scale R_phys, v_surface or z (2) k = c/v_surface or 1/√z (3) R_c = R_phys/k² (4) v(r) = (c/k)√(R_phys/r) (5) atomic/nuclear: trefoil, κ | Part I §4.1 | ✓ Matches |
| Falsification: atomic (Lamb; d_orbital ≈ 3.36 α⁻² d_nuclear); galactic (rotation curves; R_occ); nuclear (³He vs ³H) | Part I §4.2 | ✓ Matches |

---

## Benchmarks (B1–B12, D-01, S-01)

| ID | Claim (certified) | Source | Status |
|----|-------------------|--------|--------|
| B1 | Occlusion O(r)=R²/(4r²); inverse-square from geometry; [O]=1 | Part II B1 | ✓ |
| B2 | Ϟ = 1 at c-boundary; Ϟ_H = 137.036 | Part II B2 | ✓ |
| B3 | F = m_e v²/a₀ matches EM to 4 sig fig | Part II B3 | ✓ |
| B4 | Hydrogen spectrum from Ϟ framework; ionisation 13.606 eV | Part II B4 | ✓ |
| B5 | Solar k from three routes; z×Ϟ² = 1 | Part II B5 | ✓ |
| B6 | Planetary v(r) from r_c(☉); max error < 0.41% | Part II B6 | ✓ |
| B7 | Jovian satellites same v(r); max error 0.00% | Part II B7 | ✓ |
| B8 | Exoplanets; stellar k then v_planet; max ≈ 2.02% | Part II B8 | ✓ |
| B9 | Ten Rules codified | Part II B9 | ✓ |
| B10 | Six paradoxes resolved | Part II B10 | ✓ |
| B11 | Light deflection, Shapiro, perihelion within error bars | Part II B11 | ✓ |
| B12 | CMB z ≈ 1090; pressure mechanism; T_obs = 2.73 K | Part II B12 | ✓ |
| D-01 | Deuteron 2.224 MeV; p-p-e ~2.28 MeV or magnetic ~2.15 MeV | Part II D-01 | ✓ |
| S-01 | Screening ξ ≈ 6.3×10⁻⁹; ~94% stable nuclides | Part II S-01 | ✓ |

---

## Nuclear (κ, trefoil, deuteron)

| Claim | Source | Status |
|-------|--------|--------|
| n = 3, m = 2; Δ_topo = 5; a/R = 1/√2; κ ≈ 0.694 from topology | Part I 1.3, F4 | ✓ Matches |
| v² = c² κ² (R/r); κ = 1/√2 at nuclear scale | Part III F11 | ✓ Matches |
| μ_p = e c R/(2√2) (F12) | Part III F12 | ✓ Matches |
| E_bind ≈ 3 k_e e²/D; D = 1.942 fm | Part I 2.2, F5, D-01 | ✓ Matches |

---

## Cosmology and CMB

| Claim | Source | Status |
|-------|--------|--------|
| R_uni ≈ 48 Gly; z_boundary ≈ 1090; static Euclidean | Part I 3.1, B12, F7 | ✓ Matches |
| T_CMB = 2.725 K; T_boundary ≈ 3000 K | Part I 3.1, B12 | ✓ Matches |
| v_rot = π v_orb²/c (F8) | Part I 3.2, F8 | ✓ Matches |
| P_spation(r) = ρ_s c² R_uni/r (F15) | Part III F15 | ✓ Matches |

---

## Constants (Ch16 / dataset)

| Symbol | Claimed value | Source | Status |
|--------|----------------|--------|--------|
| c | 2.99792458×10⁸ m/s | Dataset, CODATA | ✓ |
| α⁻¹, Ϟ_H | 137.036 | B2 | ✓ |
| k_p | ≈ 26.2 | k_p² = 5 α⁻¹ | ✓ |
| k_⊙ | ≈ 686.6 | B5 | ✓ |
| r_c(☉) | ≈ 1.48 km | R_⊙/k_⊙² | ✓ |
| P_∞ | ≈ 1.39×10⁻¹⁴ Pa | Part I 2.3 | ✓ |
| P_conf | ≈ 10³⁴ Pa | Part I 2.3 | ✓ |
| ρ_s | ≈ 2.3×10¹⁷ kg/m³ | Part I 2.3 | ✓ |
| ξ | ≈ 6.3×10⁻⁹ | S-01 | ✓ |
| κ (nuclear) | 1/√2 | Dataset / Part III F11 | ✓ |

---

## Cross-reference checks (treatise internal)

- Chapter 2 cites B1, F9 → correct.
- Chapter 3 cites F1, F10, F16, F17, Rules 2,4,5,6,9 → correct.
- Chapter 4 cites F2, F3, Rule 7 → correct.
- Chapters 6–12 cite benchmarks and formulas per scope → consistent with dataset.
- Ch16 symbol index and constants table → aligned with Parts I–III.

---

*Scratch pad complete. All sampled claims verified against SDT_CORE_AXIOMS_AND_DATASET.md and supporting sources. No contradictions found; k=1 at c-boundary confirmed not forbidden.*
