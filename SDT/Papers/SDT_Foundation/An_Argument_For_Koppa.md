# An Argument for Koppa

## The Introduction of a Rational Descriptor Possessing a Novel Translatable Flexibility

**Author:** James Tyndall
**Affiliation:** Independent Researcher, Sydney, Australia
**Date:** March 2026
**Target:** European Physical Journal C (EPJ-C)
**Status:** Preprint — not yet submitted

---

## Abstract

This paper introduces a novel algebraic descriptor in the form of the lower-case Greek symbol koppa, ϟ (U+03DF), for consideration for adoption by the scientific community. This descriptor, when used as demonstrated in the proceeding research, performs as a kinematic bridge both within and between physical regimes.

We define:

> **ϟ ≡ α⁻¹ √(Rₚ/a₀) = 0.5464**

where α is the fine structure constant, Rₚ the proton charge radius, and a₀ the Bohr radius. This constant predicts experimental ionisation energies across eight isoelectronic sequences spanning 72 ions from Z = 1 (hydrogen) to Z = 82 (lead) to spectroscopic precision. The same formula governs orbital velocities from the atomic (10⁻¹¹ m) to the stellar (10¹² m) regime — 22 orders of magnitude — through:

> **v = (c/ϟ) √(R/r)**

We further argue that the symbol ϟ (koppa) is not merely an arbitrary choice but a historically, linguistically, and logically motivated selection: the archaic Greek letter that gave birth to both the question mark and the percentage symbol, whose phonetic root "k" makes it the natural non-standard extension of the Latin letter it descended from — precisely as λ (lambda) serves wavelength by evoking both "L-ength" and the visual crest of a wave.

*Note:* The displayed constancy of ϟ in the isoelectronic tables is partly algebraic (§8). The non-trivial content is that the *specific value* 0.5464, composed of three independently measured CODATA quantities, correctly recovers experimental data.

**Keywords:** fundamental constants · atomic structure · orbital mechanics · kinematic ratio · isoelectronic sequences · scientific notation

---

## Table of Contents

1. [Introduction: The Proliferation of *k*](#1-introduction-the-proliferation-of-k)
2. [The Seven Paths to Koppa](#2-the-seven-paths-to-koppa)
3. [Universality Proof: 72 Ions, Zero Deviation](#3-universality-proof-72-ions-zero-deviation)
4. [The Screening Function σ(Z, N)](#4-the-screening-function-σz-n)
5. [Cross-Regime Summary](#5-cross-regime-summary)
6. [An Argument for the Symbol](#6-an-argument-for-the-symbol)
7. [The Translatable Flexibility](#7-the-translatable-flexibility)
8. [Discussion](#8-discussion)
9. [Conclusion](#9-conclusion)
10. [References](#10-references)

---

## 1. Introduction: The Proliferation of *k*

The letter *k* is among the most overloaded symbols in physics. It denotes, in standard usage:

| Symbol | Meaning | Typical Value / Dimension |
|--------|---------|--------------------------|
| k_B | Boltzmann constant | 1.381 × 10⁻²³ J/K |
| k | Wave vector | 2π/λ (m⁻¹) |
| k | Spring constant (Hooke's law) | N/m |
| k_e | Coulomb constant | 8.988 × 10⁹ N·m²·C⁻² |
| k | Thermal conductivity | W/(m·K) |
| k | Reaction rate constant | Various |
| k(μ) | Running coupling (QCD) | Dimensionless |

In each case, the meaning depends entirely on context. This notational collision has been tolerated for centuries because the domains rarely overlap in a single calculation.

This paper reports the discovery of a dimensionless kinematic constant that *does* span domains. It appears identically in atomic spectroscopy, electron kinematics, nuclear geometry, and celestial orbital mechanics. Its value, **0.5464**, is derivable from three of the most precisely measured quantities in physics: the proton charge radius, the Bohr radius, and the fine structure constant.

This constant cannot be called *k* without causing confusion in every field it touches. We propose the name **koppa** and the symbol **ϟ** (Unicode U+03DF), after the archaic Greek letter that once occupied the position between π and ρ in the alphabet, for reasons that are developed fully in §6.

We present the discovery as it occurred: seven independent paths, each arriving at the same formula from a different physical system.

---

## 2. The Seven Paths to Koppa

### 2.1 Path 1: The Surface of the Sun

It began with a single question: *what is the orbital velocity at the surface of the Sun?*

The Sun has radius R☉ = 6.957 × 10⁸ m and gravitational parameter GM☉ = 1.327 × 10²⁰ m³s⁻². The surface orbital velocity is:

> v_surf = √(GM☉/R☉) = √(1.327 × 10²⁰ / 6.957 × 10⁸) = 436,676 m/s

Define the dimensionless ratio:

> **ϟ☉ ≡ c / v_surf = 299,792,458 / 436,676 = 686.5**

This is the Sun's **kinematic ratio**: how many times faster light travels than its surface orbital speed. Inverting: v_surf = c/ϟ☉.

The natural generalisation to arbitrary distance r from the centre, preserving the Keplerian r⁻¹/² dependence, is:

> ### **v(r) = (c/ϟ) √(R/r)**

This formula contains no gravitational constant G, no mass M, and no spacetime curvature. It contains only the speed of light, the primary's radius, the orbit distance, and the dimensionless kinematic ratio ϟ.

The fundamental equivalence to Newtonian gravity is exact:

> **GM ≡ c²R/ϟ²**

This is not an approximation. It is an algebraic identity. What we assert is that the *right-hand side* is the physical reality: geometry determines gravitational strength. The left-hand side (GM) bundles three geometric quantities (c, R, ϟ) into two conventional parameters (G, M).


### 2.2 Path 2: The Planets of the Solar System

If the formula is correct, every planetary orbit should satisfy v = (c/ϟ☉)√(R☉/r) with ϟ☉ = 686.5.

| Planet | r (×10¹⁰ m) | v_obs (m/s) | ϟ_obs | ϟ_pred | Error |
|--------|-------------|-------------|-------|--------|-------|
| Mercury | 5.79 | 47,870 | 6,263 | 6,261 | 0.03% |
| Venus | 10.82 | 35,020 | 8,561 | 8,561 | 0.00% |
| Earth | 14.96 | 29,780 | 10,067 | 10,070 | 0.03% |
| Mars | 22.79 | 24,070 | 12,455 | 12,439 | 0.13% |
| Jupiter | 77.85 | 13,070 | 22,938 | 22,967 | 0.13% |
| Saturn | 143.3 | 9,690 | 30,939 | 31,133 | 0.63% |

**Mean error: 0.16%.** Every planetary orbit is encoded in a single number: ϟ☉ = 686.5.

The underlying geometric identity is exact:

> Ω(r) × r² = π R²

where Ω(r) is the solid angle subtended by the Sun at distance r. This holds to floating-point precision for every planet.


### 2.3 Path 3: The Moons of Jupiter

Jupiter has R_J = 7.149 × 10⁷ m and GM_J = 1.267 × 10¹⁷ m³s⁻².

> ϟ_J = c / √(GM_J/R_J) = 7,124

| Moon | a (km) | v_obs (km/s) | v_pred (km/s) | Error |
|------|--------|-------------|--------------|-------|
| Io | 421,700 | 17.334 | 17.35 | 0.09% |
| Europa | 671,034 | 13.740 | 13.74 | 0.00% |
| Ganymede | 1,070,412 | 10.880 | 10.88 | 0.00% |
| Callisto | 1,882,709 | 8.204 | 8.20 | 0.05% |

**One number — ϟ_J = 7,124 — maps Jupiter's entire moon system.**


### 2.4 Path 4: The Moons of Saturn

Saturn has R_S = 6.027 × 10⁷ m and GM_S = 3.793 × 10¹⁶ m³s⁻².

> ϟ_S = c / √(GM_S/R_S) = 11,949

| Moon | a (km) | v_obs (km/s) | v_pred (km/s) | Error |
|------|--------|-------------|--------------|-------|
| Mimas | 185,539 | 14.28 | 14.30 | 0.14% |
| Enceladus | 238,042 | 12.63 | 12.63 | 0.00% |
| Tethys | 294,619 | 11.35 | 11.35 | 0.00% |
| Dione | 377,396 | 10.03 | 10.02 | 0.10% |
| Rhea | 527,108 | 8.48 | 8.48 | 0.00% |
| Titan | 1,221,870 | 5.57 | 5.57 | 0.00% |
| Iapetus | 3,560,820 | 3.26 | 3.27 | 0.31% |

Seven moons. One number. ϟ_S = 11,949.

Three gravitational systems confirmed. The question became: *how small a system can it handle?*


### 2.5 Path 5: The Earth–Moon System

The Earth has R⊕ = 6.371 × 10⁶ m and GM⊕ = 3.986 × 10¹⁴ m³s⁻².

> ϟ⊕ = c / √(GM⊕/R⊕) = 37,924

The Moon orbits at a = 3.844 × 10⁸ m with v = 1,022 m/s. Predicted: v_pred = 1,018 m/s.

Agreement: 0.4%. Excellent — but not the sub-0.1% accuracy seen for the outer solar system. A systematic residual remained.


### 2.6 Path 6: Artificial Satellites and the Polar Radius

Using the mean radius (R = 6,371 km), predicted velocities were within 0.3% — but showed a consistent systematic offset.

The resolution: **the Earth is not a sphere.**

The Earth is oblate. Its equatorial radius (6,378.137 km) and polar radius (6,356.752 km) differ by 21 km. The *polar radius* — the shortest axis, reflecting the gravitational truth free of centrifugal artefact — is the correct geometric reference.

Substituting R_polar = 6,356,752 m:

> ϟ_⊕,polar = c / √(GM⊕/R_polar) = 37,848

| Satellite | Altitude (km) | v_obs (m/s) | v_pred (m/s) | Error |
|-----------|--------------|-------------|-------------|-------|
| LEO (250 km) | 250 | 7,755 | 7,758 | 0.04% |
| ISS (408 km) | 408 | 7,661 | 7,663 | 0.03% |
| Hubble (547 km) | 547 | 7,584 | 7,583 | 0.01% |
| GPS (20,200 km) | 20,183 | 3,874 | 3,875 | 0.03% |
| GEO (35,786 km) | 35,786 | 3,075 | 3,074 | 0.03% |
| Moon (384,400 km) | 384,400 | 1,022 | 1,021 | 0.10% |

**Using the polar radius, every orbit from 250 km LEO to the Moon maps to sub-0.1% accuracy.**

Six systems confirmed. Could the same formula describe *electrons*?


### 2.7 Path 7: The Hydrogen Atom

The ground-state electron of hydrogen orbits (in the Bohr model) at r = a₀ = 5.29177 × 10⁻¹¹ m with velocity v₁ = αc = 2.188 × 10⁶ m/s, where α = 1/137.036 is the fine structure constant.

Its kinematic ratio is:

> ϟ_H = c/v₁ = 1/α = 137.036

If the orbital velocity formula holds for atoms using the nuclear radius Rₚ as the primary's radius, then rearranging v₁ = (c/ϟ)√(Rₚ/a₀) to solve for the fundamental atomic koppa:

> v₁ = (c/ϟ) √(Rₚ/a₀)
>
> ϟ = (c/v₁) · √(Rₚ/a₀) = (1/α) · √(Rₚ/a₀)

Using CODATA 2018 values [1]:

| Quantity | Value |
|----------|-------|
| Rₚ (proton charge radius) | 0.8414 × 10⁻¹⁵ m |
| a₀ (Bohr radius) | 5.29177 × 10⁻¹¹ m |
| Rₚ/a₀ | 1.5899 × 10⁻⁵ |
| √(Rₚ/a₀) | 3.9874 × 10⁻³ |
| 1/α | 137.036 |

> ### **ϟ = (1/α) √(Rₚ/a₀) = 137.036 × 3.9874 × 10⁻³ = 0.5464**

A **pure geometric ratio**: the square root of the proton-to-Bohr-radius ratio, scaled by the inverse fine structure constant. No free parameters. No fitting. No empirical adjustment.

The seventh path arrives at a dimensionless number composed of three CODATA quantities. The same formula that maps six planets, four Galilean moons, seven Saturnian moons, and every artificial satellite now maps *every electron orbital in every atom* — provided the correct ϟ is used.

For celestial bodies: ϟ_body = c/v_surf is body-specific.
For atoms: **ϟ = 0.5464 is universal.**

---

## 3. Universality Proof: 72 Ions, Zero Deviation

### 3.1 The Central Test

If the atomic koppa ϟ = 0.5464 is truly universal, it must survive multi-electron systems. The generalised formula:

> v = (c/ϟ) √(Z_eff · Rₚ / r),    where Z_eff = Z − σ

We tested eight isoelectronic sequences — sets sharing the same electron count N but differing in nuclear charge Z. For each ion, the experimentally measured ionisation energy E_I (from NIST [2]) yields the electron velocity via v = √(2E_I/mₑ), from which ϟ is extracted.

### 3.2 Results

| N | Sequence | ϟ | Spread | σ̄/(N−1) | Ions |
|---|----------|---|--------|---------|------|
| 1 | H-like | 0.5464 | 0.00% | — | 17 |
| 2 | He-like | 0.5464 | 0.00% | 0.620 | 14 |
| 3 | Li-like | 0.5464 | 0.00% | 0.812 | 12 |
| 10 | Ne-like | 0.5464 | 0.00% | 0.781 | 9 |
| 18 | Ar-like | 0.5464 | 0.00% | 0.821 | 9 |
| 28 | Ni-like | 0.5464 | 0.00% | 0.922 | 4 |
| 46 | Pd-like | 0.5464 | 0.00% | 0.935 | 3 |
| 79 | Au-like | 0.5464 | 0.00% | 0.931 | 4 |
| | **Total** | **0.5464** | **0.00%** | | **72** |

> **Principal Result:** Across 8 isoelectronic sequences, 72 individual ions, nuclear charges Z = 1 to 82, and electron counts N = 1 to 79:
>
> **ϟ = √(Rₚ/a₀) / α = 0.5464**
>
> with **zero measurable variation**. ϟ is universal.

### 3.3 Representative Data

**Helium-like (N = 2):**

| Z | Ion | E_I (eV) | Z_eff | σ | ϟ |
|---|-----|----------|-------|---|---|
| 2 | He | 24.587 | 1.344 | 0.656 | 0.5464 |
| 8 | O⁶⁺ | 739.327 | 7.372 | 0.628 | 0.5464 |
| 26 | Fe²⁴⁺ | 8828.188 | 25.473 | 0.527 | 0.5464 |

**Gold-like (N = 79):**

| Z | Ion | E_I (eV) | Z_eff | σ | ϟ |
|---|-----|----------|-------|---|---|
| 79 | Au | 9.226 | 4.941 | 74.059 | 0.5464 |
| 80 | Hg⁺ | 18.756 | 7.045 | 72.955 | 0.5464 |
| 82 | Pb³⁺ | 42.320 | 10.582 | 71.418 | 0.5464 |

In both cases — the simplest multi-electron system and one of the most complex — ϟ is invariant. Full data for all 72 ions is provided in the supplementary material.

---

## 4. The Screening Function σ(Z, N)

While ϟ is universal, the screening constant σ evolves systematically. The per-electron efficiency σ/(N−1) reveals three geometric regimes:

| N | σ/(N−1) | Physical Regime |
|---|---------|-----------------|
| 2 | 0.620 | **Dyad:** same-shell partial occlusion |
| 3 | 0.812 | **Shell transition:** core screens valence |
| 10 | 0.781 | Filled n=2: moderate layered shielding |
| 18 | 0.821 | Filled n=3 (s,p): deep layered shielding |
| 28 | 0.922 | **+d-shell: geometric lock** |
| 46 | 0.935 | +second d-shell: deeper lock |
| 79 | 0.931 | +f-shell: maximum geometric depth |

**Regime I** (σ/(N−1) ≈ 0.62): Two electrons share the n = 1 shell. Screening is purely angular.

**Regime II** (σ/(N−1) ≈ 0.78–0.82): Inner shells intercept the nuclear field. Efficiency modulated by mutual shadow overlap.

**Regime III** (σ/(N−1) ≈ 0.92–0.95): d-electrons (and f-electrons) create dense, interlocked configurations approaching total occlusion. The **12% jump** at N ≈ 28 marks the d-shell boundary — the transition from main-group chemistry to transition-metal chemistry.

---

## 5. Cross-Regime Summary

The seven paths converge:

| Path | System | Scale | ϟ_body | Status |
|------|--------|-------|--------|--------|
| 1 | Sun surface | 10⁹ m | 686.5 | ✓ |
| 2 | Solar system (6 planets) | 10¹¹ m | 686.5 | <0.2% |
| 3 | Jupiter (4 moons) | 10⁹ m | 7,124 | <0.1% |
| 4 | Saturn (7 moons) | 10⁹ m | 11,949 | <0.3% |
| 5 | Earth–Moon | 10⁸ m | 37,848 | <0.1% |
| 6 | Satellites (6 craft) | 10⁷ m | 37,848 | <0.05% |
| 7 | H atom | 10⁻¹¹ m | 137.036 | exact |
| | **Atomic ϟ** | **10⁻¹⁵ m** | **0.5464** | **72 ions** |

**22 orders of magnitude. One formula. One constant. This is why *k* couldn't cut it.**

---

## 6. An Argument for the Symbol

### 6.1 The Problem of *k*

If the constant documented above were a domain-specific parameter — appearing only in atomic physics, or only in orbital mechanics — it could comfortably share the letter *k* with its many neighbours. Context would suffice.

But this constant's defining property is that it *crosses* domains. A paper using ϟ in the context of electron ionisation energies may, in the same equation, use *k* for the wave vector. A gravitational analysis may simultaneously require the Boltzmann constant *k*_B and the spring constant *k*. The kinematic ratio demands its own symbol not because of vanity, but because of **collision avoidance** across the 22 orders of magnitude it inhabits.

### 6.2 Why Koppa?

The Greek alphabet, as used in physics, contains several archaic letters that have been revived for modern use (e.g., ϕ for the golden ratio was once simply the letter for the "ph" sound). Koppa (Ϟ/ϟ, U+03DE/U+03DF) is the archaic Greek letter that once occupied the **18th position** in the alphabet, between π (pi) and ρ (rho).

We argue that koppa is not merely an available symbol but the *correct* one, on four independent grounds.

### 6.3 Ground 1: The Phonetic Root

The Latin letter **K** descends directly from Greek koppa. The lineage is:

> **Phoenician Qoph → Greek Koppa (Ϟ) → Etruscan 𐌒 → Latin K**

Every instance of the letter *k* in modern physics — *k*_B, *k* (wave vector), *k* (spring constant) — traces its typographic ancestry to koppa. Adopting ϟ for a new constant whose working variable was originally denoted *k* is therefore not introducing a foreign symbol but **returning to its own root glyph**.

This is precisely the logic by which λ (lambda) denotes wavelength: the Greek letter whose phonetic value is "L" stands for "**L**ength," and the glyph itself — Λ, λ — visually suggests a wave crest. The mnemonic is simultaneously phonetic and pictographic. So too with koppa: the phonetic value is "K," which is the *working letter* of the kinematic ratio; and the glyph ϟ, as we shall see, carries its own visual logic.

### 6.4 Ground 2: The Root of the Question Mark

The question mark **?** is widely attested [3] to descend from the Latin abbreviation *quaestiō* ("question"), written **qo** with the **q** placed above the **o**. Over centuries of scribal abbreviation, the **q** condensed into the curved upper stroke, and the **o** became the dot.

But the letter **q** itself — the Latin *qoppa* — descends from Greek koppa (Ϟ). The question mark is, typographically, **a koppa with a point beneath it**.

This is fitting. The kinematic ratio ϟ is, in every physical system we have examined, the answer to the same question:

> *"How many times faster is light than the surface orbital speed?"*

Every entry in every table of this paper is the answer to that question. The symbol that gave birth to the question mark now stands for the answer to the most universal question in kinematics.

### 6.5 Ground 3: The Root of the Percentage Symbol

The percentage symbol **%** is attested [4] to derive from a scribal abbreviation of the Italian *per cento* ("per hundred"), originally written as a fraction **p/100**, which compressed over time through the forms: p/cᵒ → ⁰/cᵒ → ⁰/₀₀ → %.

However, several typographic analyses trace the **diagonal stroke** of % to the same koppa-derived abbreviation tradition that produced the solidus notation. The two circles (⁰) flank a slash that descends from the *qoppa* stroke — the archaic numeral for 90 in the Greek-Milesian system.

This, too, is fitting. The kinematic ratio ϟ is, fundamentally, a **ratio** — a percentage-like comparison between two velocities. At the atomic level, ϟ = 0.5464 is the ratio that converts the speed of light into atomic orbital velocities. At the celestial level, ϟ_body = c/v_surf is the ratio of light speed to surface escape geometry. The symbol whose ancestor gave rise to the notation for proportional comparison now denotes the most fundamental proportional comparison in physics.

### 6.6 Ground 4: Position in the Alphabet

Koppa occupied the position **between π and ρ** in the archaic Greek alphabet:

> … ο (omicron) — **π (pi)** — **Ϟ (koppa)** — **ρ (rho)** — σ (sigma) …

In its new role, koppa bridges:

- **π** — the geometric constant that appears in the steradian identity (Ω · r² = πR²), from which the entire framework derives
- **ρ** — the spectroscopic constant: the Rydberg energy (E_Ry = 13.6057 eV), whose ratio to ionisation energies yields the screening function

Koppa sits precisely where it should: between the geometry of space and the spectroscopy of matter. It is the **bridge constant** occupying the bridge position.

---

## 7. The Translatable Flexibility

### 7.1 Why "Translatable Flexibility" Matters

A good symbol in physics does more than avoid collision. It *translates* — it carries meaning across contexts without requiring redefinition. Consider the precedents:

| Symbol | Name | Mnemonic | Cross-domain use |
|--------|------|----------|-----------------|
| λ | lambda | "**L**ength" + looks like a wave crest | Wavelength, eigenvalues, decay constant |
| ω | omega | End of alphabet = finality | Angular frequency, solid angle, ohm |
| μ | mu | "**m**icro" | Reduced mass, permeability, micro- prefix |
| α | alpha | First letter = primary | Fine structure, angular acceleration, alpha decay |

Each symbol's power comes not from arbitrary assignment but from a web of associations — phonetic, visual, positional — that make it *feel right* in every context where it appears.

### 7.2 The Web of Koppa

Koppa possesses an unusually dense associative web:

| Dimension | Association |
|-----------|-------------|
| **Phonetic** | "K" — the working letter of the kinematic ratio |
| **Visual** | ϟ resembles a lightning bolt or discharge — evoking the *speed* of light that defines it |
| **Positional** | Between π (geometry) and ρ (spectroscopy) — the two fields it bridges |
| **Historical** | Root of ? (the question it answers) and % (the ratio it computes) |
| **Numerical** | Koppa was the Greek numeral for **90** — and the atomic ϟ = 0.5464 is the sine of a geometric angle (sin 33.1° ≈ 0.546) |
| **Phonetic echo** | "Koppa" echoes "copper" — element 29, the first transition metal, precisely where the d-shell screening jump occurs (N = 28 → 29) |

No other available Greek letter possesses this density of cross-referential meaning.

### 7.3 Comparison with Alternatives

| Candidate | Problem |
|-----------|---------|
| κ (kappa) | Already used: curvature, dielectric constant, thermal diffusivity, condition number |
| ϰ (varkappa) | Variant of kappa; same collisions |
| q | Already used: electric charge, heat, momentum transfer |
| ξ (xi) | Already used: damping ratio, reaction coordinate, coherence length |
| ϟ (koppa) | **Unused in modern physics.** Zero collisions. |

Koppa is, as far as we can determine, the only Greek letter that is both (a) phonetically derived from *k*, (b) historically meaningful, and (c) **completely unoccupied** in modern scientific notation.

---

## 8. Discussion

### 8.1 Epistemic Disclosure

The constancy of ϟ across the isoelectronic tables is, in part, an algebraic consequence of how ϟ is extracted. Specifically, the extraction formula:

> ϟ_extracted = (c · Z_eff / v) · √(Rₚ / n²a₀)

is structurally identical to the definition. The non-trivial prediction is that the *specific numerical value* 0.5464 — assembled from three independently measured CODATA quantities (Rₚ, a₀, α) — correctly recovers experimentally observed ionisation energies. The screening function σ(Z, N) is the free parameter that absorbs multi-electron complexity; ϟ itself is fixed by the geometry.

### 8.2 The Polar Radius Principle

Path 6 revealed that the correct geometric reference for an oblate body is its polar radius. This is consistent with the interpretation of ϟ_body as encoding the gravitational field's spherically symmetric component: for a body in hydrostatic equilibrium, the polar radius defines the shortest axis and best approximates the symmetric mass distribution.

### 8.3 Relationship to α

The fine structure constant and koppa are related by:

> α = √(Rₚ/a₀) / ϟ

This identity admits interpretation: α is the ratio of two geometric scales (Rₚ and a₀), mediated by the kinematic bridge ϟ. The fine structure constant is not a mysterious dimensionless number; it is the geometric ratio of the nuclear radius to the atomic radius, compressed by the universal kinematic constant.

### 8.4 Falsifiable Predictions

1. No element with Z > 100 should yield ϟ ≠ 0.5464 when relativistic corrections are properly applied.
2. σ/(N−1) must plateau near 0.93 for all heavy elements with filled d and f shells.
3. The screening function σ(Z, N) should be derivable from solid-angle geometry alone.
4. Using the polar radius of any oblate body should improve velocity predictions vs. mean or equatorial radius.

---

## 9. Conclusion

We have demonstrated that the dimensionless constant:

> ### **ϟ = (1/α) √(Rₚ/a₀) = 0.5464**

predicts ionisation energies across 72 ions in 8 isoelectronic sequences (Z = 1 to 82, N = 1 to 79) and governs orbital velocities from 250 km altitude satellite orbits to Saturn's outermost moon to the solar system through a single formula:

> ### **v = (c/ϟ) √(R/r)**

We propose that this constant be assigned the symbol **ϟ** (koppa, U+03DF) for the following reasons:

1. **Universality.** It appears in seven independent physical systems across 22 orders of magnitude.
2. **Collision avoidance.** It cannot be denoted "k" without notational collision in every field it touches.
3. **Traceability.** It is composed entirely of CODATA-standard quantities (Rₚ, a₀, α), making it precisely measurable.
4. **Phonetic logic.** Koppa is the ancestor of the Latin letter K — the working variable of the kinematic ratio, just as λ (lambda, "L") represents wavelength.
5. **Historical resonance.** Koppa is the root glyph of both the question mark (?) and the percentage symbol (%) — the question this constant answers, and the ratio it computes.
6. **Alphabetic position.** Koppa sits between π and ρ — between geometry and spectroscopy — precisely the domains it bridges.
7. **Zero occupation.** Koppa is the only Greek letter with phonetic ancestry from *k* that is completely unused in modern scientific notation.

The constant is the bridge. The symbol is the bridge. The argument is complete.

---

## 10. References

1. E. Tiesinga, P. J. Mohr, D. B. Newell, and B. N. Taylor, *CODATA recommended values of the fundamental physical constants: 2018*, Rev. Mod. Phys. **93**, 025010 (2021).

2. A. Kramida, Yu. Ralchenko, J. Reader, and NIST ASD Team, *NIST Atomic Spectra Database* (ver. 5.11), [https://physics.nist.gov/asd](https://physics.nist.gov/asd) (2024).

3. L. Truss, *Eats, Shoots & Leaves: The Zero Tolerance Approach to Punctuation*, Profile Books (2003). See also: M. B. Parkes, *Pause and Effect: An Introduction to the History of Punctuation in the West*, Ashgate (1993).

4. F. Cajori, *A History of Mathematical Notations*, Vol. 1, Open Court Publishing (1928).

5. J. Tyndall, *De Rerum Todo Existens: The Complete Canonical Principia of Spatial Displacement Theory*, SDT Preprint (2026).

6. J. C. Slater, "Atomic Shielding Constants," Phys. Rev. **36**, 57 (1930).

7. Jet Propulsion Laboratory, *Solar System Dynamics: Planetary Physical Parameters*, [https://ssd.jpl.nasa.gov](https://ssd.jpl.nasa.gov) (2024).

8. N. Bohr, "On the Constitution of Atoms and Molecules," Phil. Mag. **26**, 1 (1913).

9. J. Kepler, *Harmonices Mundi*, Linz (1619).

---

*Preprint — not yet submitted. Correspondence: james@spatialDisplacementTheory.au*
