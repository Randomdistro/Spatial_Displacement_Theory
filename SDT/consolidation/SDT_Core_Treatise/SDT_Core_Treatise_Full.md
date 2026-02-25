# Spatial Displacement Theory: Core Axioms, Benchmarks, and Formulas

**Primary source:** *SDT Core Axioms & Mathematical Dataset* (Parts I–III).  
**Supporting sources:** *09_CANONICAL_SDT_FORMULAS.md*, *05_STRUCTURE_MAP.md*, *08_CONSISTENCY_REPORT.md*, treatise sections in *conversation.md*.

---
## Table of contents

- [**Chapter 1:** Introduction, Primitives, and Notation](#introduction-primitives-and-notation)
- [**Chapter 2:** Geometry and the Occlusion Foundation](#geometry-and-the-occlusion-foundation)
- [**Chapter 3:** Master Orbital Equation and Velocity Field](#master-orbital-equation-and-velocity-field)
- [**Chapter 4:** Redshift–Displacement Identity and Scaling](#redshiftdisplacement-identity-and-scaling)
- [**Chapter 5:** Trefoil Topology and Proton Structure](#trefoil-topology-and-proton-structure)
- [**Chapter 6:** Hydrogen System and Atomic Benchmarks](#hydrogen-system-and-atomic-benchmarks)
- [**Chapter 7:** Solar and Stellar Systems](#solar-and-stellar-systems)
- [**Chapter 8:** Ten Rules and Paradox Resolution](#ten-rules-and-paradox-resolution)
- [**Chapter 9:** Classical Tests of Gravitation](#classical-tests-of-gravitation)
- [**Chapter 10:** Nuclear Structure and Binding](#nuclear-structure-and-binding)
- [**Chapter 11:** Cosmology and CMB](#cosmology-and-cmb)
- [**Chapter 12:** Benchmark Suite and Certification](#benchmark-suite-and-certification)
- [**Chapter 13:** Standout Formulas Compendium](#standout-formulas-compendium)
- [**Chapter 15:** Galactic Systems and Flat Rotation Curves](#galactic-systems-and-flat-rotation-curves)
- [**Chapter 16:** References, Constants, and Symbol Index](#references-constants-and-symbol-index)

---



## Chapter 1: Introduction, Primitives, and Notation

### Context and scope

This document is the **Spatial Displacement Theory (SDT) Core Treatise**: a structured exposition of the core axioms, benchmarks, and formulas that define the SDT physics engine. The treatise does not introduce new physics beyond what is already certified in the primary dataset (*SDT Core Axioms & Mathematical Dataset*, Parts I–III). Its purpose is to organise that content into a single, readable reference with consistent notation, clear derivation steps, and explicit cross-references to benchmarks and formulas. Each chapter is self-contained enough to support study and implementation, while the whole forms a continuous narrative from geometric foundations through atomic and stellar validation to nuclear structure and cosmology.

This first chapter does three things. It states the **system instruction** that defines how the framework is to be implemented; it introduces the **four irreducible primitives** (matter, space, movement, now) and the **Euclidean lattice** of discrete units (spations) that constitute the medium; and it fixes **notation** (Ϟ, ϟ, k, κ) and the **scope** of the treatise. It then gives the **calculation order** (the sequence of steps for applying the framework to any scale) and the **falsification vectors** (where empirical or theoretical checks could contradict the model). A reader who finishes this chapter will know what SDT assumes, how to read the rest of the document, and how to use it for calculation and validation.

**Working title of the treatise:** *Spatial Displacement Theory: Core Axioms, Benchmarks, and Formulas.*

---

### System instruction

The following instruction is to be treated as the foundational specification for the SDT model:

*Implement the following mathematical framework as the foundational physics engine for the Spatial Displacement Theory (SDT) model. This dataset supersedes standard General Relativity and Quantum Chromodynamics formulations within this context. The universe is defined as a Euclidean lattice of discrete units (spations) under hydrostatic pressure from a cosmic boundary.*

In practice this means:

1. **Physics engine.** All dynamical predictions—orbital velocities, redshifts, accelerations, escape speeds, classical tests, nuclear binding, CMB interpretation—are to be derived from the axioms and formulas in the dataset, not from Newton’s law of gravitation, Einstein’s field equations, or QCD Lagrangians when operating within the SDT context.

2. **Supersession in context.** Where SDT and standard GR or QCD give different interpretations or formulas, the SDT formulation is the one to use for this framework. For example, “gravity” is not curvature of spacetime but the dynamical effect of a pressure gradient in the spation medium; “strong” nuclear effects are not a separate force but the same pressure and velocity field (Ϟ and ϟ at nucleon scale; nucleon surface Ϟ = √2).

3. **Universe definition.** The universe is not an expanding spacetime manifold with a Big Bang singularity. It is a **Euclidean** space (flat, infinite or very large) populated by a **lattice of discrete units** called spations, and the whole is under **hydrostatic pressure** from a **cosmic boundary** (identified with the CMB shell at redshift z ≈ 1090). That pressure, and the pressure differentials caused by matter displacing spations, drive all the phenomena that SDT models.

The rest of this chapter unpacks the primitives and the medium implied by this instruction, then fixes notation and implementation logic.

---

### Four irreducible primitives

SDT is built from four primitives. They are not derived from prior physics; they are the minimum set needed to construct the theory. Each is **irreducible** (it cannot be defined in terms of the others) and **unique** (no alternative serves the same role).

**Space (S).** Space is a discrete medium of identical units called **spations**. Each spation is a sphere of diameter 1.616×10⁻³⁵ m—the fundamental length. The spation has no internal structure; it is the smallest unit of spatial extension. Space is the collection of all spations: incompressible and contiguous. Thus “empty” space is not nothing; it is a packed lattice of spations. When we speak of the “spation medium,” we mean this lattice and the pressure it sustains.

**Matter (M).** Matter is substance under continuous compression from the moment of its formation to the present. Matter **displaces** spations: it excludes them from its volume. The cumulative pressure history of the universe acts on every material object. This exclusion creates pressure differentials between the interior of a body and the surrounding medium, and between different regions of the medium. In SDT, “mass” and “gravitational” effects are not primitive; they emerge from how matter displaces the medium and how the medium responds with a pressure gradient.

**Movement (Δ).** Movement is the shunting of spations around material boundaries. It propagates at velocity **c = 299,792,458 m/s**. This is not a speed limit imposed on matter; it is the propagation rate of the medium itself. Nothing in the medium can outrun the medium’s own response. So c is the characteristic speed of the spation field—the speed at which pressure changes and displacement patterns propagate. Light, in this picture, is a wave or disturbance in the medium; its speed is c.

**Now (τ).** Now is the ever-present moment—the instantaneous state that defines simultaneity across the medium. Now is not duration; it is the boundary between what has occurred and what has not. All interactions occur at Now. The medium has no memory; each moment is complete in itself. This primitive underlies the use of equilibrium and steady-state conditions in the derivations (e.g. hydrostatic equilibrium): we are always “at Now,” and the velocity and pressure fields are taken as time-independent unless otherwise specified.

**What is not primitive.** Energy, force, and acceleration are **not** primitive. They are geometric consequences of pressure differentials in the medium. The numerical relationships between them (e.g. F = m v²/r for centripetal force, or a = c² R/(Ϟ² r²) for radial acceleration) emerge from the geometry and the velocity field; they are not inserted as separate laws. So the treatise will often “derive” force or energy from the master orbital equation and occlusion; that is consistent with the primitives.

---

### Euclidean lattice and spation medium

The system instruction states that the universe is a **Euclidean lattice** of discrete units under **hydrostatic pressure** from a **cosmic boundary**. We unpack this here.

**Euclidean.** Geometry is flat. Distances and angles obey Euclidean geometry. There is no curvature of “spacetime”; there is a three-dimensional Euclidean space, and time is a separate parameter. Solid-angle formulas (e.g. the occlusion O(r) = R²/(4r²) in Chapter 2) are derived in this Euclidean space. Classical tests such as light deflection and Shapiro delay are interpreted in SDT as refractive effects in a medium with a radially varying index, not as geodesics in a curved manifold.

**Lattice of discrete units.** Space is not a continuous manifold; it is composed of spations. The lattice structure implies a natural length scale (the spation diameter) and the possibility that phenomena at very small scales are influenced by discreteness (e.g. decoherence or stability conditions). For most of the treatise, we work in the continuum limit where the relevant lengths (orbital radii, wavelengths, nuclear sizes) are large compared with the spation scale, so that the velocity and pressure fields can be treated as smooth.

**Spation medium.** The spations collectively form a medium that can sustain pressure and transmit disturbances at speed c. Matter displaces this medium; the displacement creates a pressure deficit (or gradient) that pulls other matter inward—the SDT analogue of attraction. The pressure at large scales is set by the cosmic boundary (the CMB shell); locally, the pressure is modified by every displacing body. Hydrostatic equilibrium in this medium yields the master orbital equation v² = c² R_c/r (Chapter 3).

**Cosmic boundary.** The boundary is the source of the omnidirectional pressure. It is identified with the surface of last scattering at redshift z ≈ 1090, at a radius R_uni ≈ 48 Gly. The CMB is interpreted as the radiation from that boundary, gravitationally redshifted as it climbs out of the potential well. So the “edge” of the observable universe in SDT is not an initial singularity but a radiating surface that supplies the pressure that fills the lattice.

---

### Notation: Ϟ, ϟ, k, κ

Consistent notation is used throughout the treatise and the dataset.

**Ϟ (koppa, U+03DE).** Ϟ denotes the **variable velocity ratio** at a given radius: Ϟ = c/v, where v is the orbital (or flow) velocity in the medium at that radius. So Ϟ is dimensionless. At the **c-boundary** (the radius where v = c), Ϟ = 1. At the physical surface of a body, Ϟ equals the surface value (often written k). So “Ϟ” can mean either the function Ϟ(r) or the surface value, depending on context.

**ϟ (stigma, U+03DF).** ϟ is the **fixed value at the c-boundary**: ϟ = 1. It is used when one wants to emphasise the normalisation “at the velocity saturation point.” **Even in nuclear** the convention is Ϟ and ϟ (U+03DE, U+03DF); at the c-boundary we always have ϟ = 1.

**k.** In drafting and in many formulas, **k** is used interchangeably with the surface value of Ϟ: **k = c/v_surface**. So k is the inverse of the velocity ratio at the body’s physical surface. For the Sun, k_⊙ ≈ 686.6; for hydrogen (electron at Bohr radius), Ϟ_H = k_H ≈ 137.036. The identity z·k² = 1 (redshift times surface-k squared equals one) uses this k.

**κ (kappa).** In some legacy or dataset phrasing, κ appears for a numerical factor (e.g. 1/√2 at nucleon, or trefoil ≈ 0.694). The **convention** for the velocity ratio and c-boundary is nevertheless **Ϟ and ϟ (U+03DE, U+03DF) at all scales, including nuclear.** At the nucleon surface, if v_surface = c/√2, then the surface value is **Ϟ = c/v_surface = √2**; the symbol is still Ϟ, and at the c-boundary ϟ = 1. So: v_surface = c/Ϟ; v = (c/Ϟ)√(R/r); z·k² = 1; rotation Ϟ = √(πc/v_rot). Even in nuclear it is Ϟ and ϟ.

**Summary.** Ϟ (or k at the surface) = c/v_surface; at the c-boundary, Ϟ = ϟ = 1 (ϟ = U+03DF). Same convention everywhere, including nuclear. R_phys (or R) = physical radius; R_c = c-boundary radius = R_phys/Ϟ²; r = radial distance from the centre.

---

### Scope of the document

The treatise is organised in **three books** and **13 chapters**.

**Book I: Foundations and core mechanics (Chapters 1–5).** Chapter 1 (this chapter) sets primitives, notation, and implementation logic. Chapter 2 establishes the occlusion foundation (solid angle, O(r) = R²/(4r²), Benchmark B1, Formula F9). Chapter 3 presents the master orbital equation (F1), velocity field, acceleration (F10), escape velocity (F16), Ϟ(r) (F17), and scale invariance. Chapter 4 covers the redshift–displacement identity (z·k² = 1), scaling (k_solar = k_proton²), and Rule 7 (three routes to Ϟ). Chapter 5 treats trefoil topology and proton structure (F4, F12, Δ_topo = 5).

**Book II: Atomic to stellar validation (Chapters 6–9).** Chapter 6: hydrogen system and atomic benchmarks (B2, B3, B4); Ϟ_H = 137.036; centripetal force and spectrum. Chapter 7: solar and stellar systems (B5–B8); F8 (rotation coupling); worked examples. Chapter 8: Ten Rules (B9) and paradox resolution (B10). Chapter 9: classical tests of gravitation (B11; F13, F14; light deflection, Shapiro, perihelion).

**Book III: Nuclear, cosmology, and reference (Chapters 10–13).** Chapter 10: nuclear structure and binding (Part I 2.1–2.3; B D-01; F5, F11; nucleon Ϟ = √2, Ϟ and ϟ convention). Chapter 11: cosmology and CMB (48 Gyr radiator, B12, F7, F15). Chapter 12: benchmark suite and certification (B1–B12, D-01, S-01; calculation order and falsification). Chapter 13: standout formulas compendium (F1–F17: statement, derivation, “why it matters,” cross-links).

**Sources.** Primary: *SDT Core Axioms & Mathematical Dataset* (Parts I–III). Supporting: *09_CANONICAL_SDT_FORMULAS.md*, *05_STRUCTURE_MAP.md*, *08_CONSISTENCY_REPORT.md*, and treatise sections in *conversation.md* (structure map line ranges). No new physics is introduced; the treatise only structures and expands existing content.

---

### Calculation order (implementation logic 4.1)

To apply the SDT framework to any given system, follow this **calculation order**:

1. **Define the scale.** Identify the physical surface radius R_phys and either the surface velocity v_surface or the gravitational redshift z (or equivalent observable).

2. **Obtain k.** Compute **k = c/v_surface** if v_surface is known, or **k = 1/√z** if z is known. So k is fixed by dynamics or spectroscopy.

3. **Obtain the c-boundary radius.** **R_c = R_phys / k².** This is the radius at which the orbital velocity in the medium would equal c.

4. **Velocity field.** **v(r) = (c/k) √(R_phys/r)** or equivalently **v(r) = c √(R_c/r).** Use this for orbital speeds at any radius r ≥ R_phys (or r ≥ R_c as appropriate).

5. **If atomic or nuclear:** apply scale-specific rules. For atomic (hydrogen), use Ϟ_H = 137.036 and the Bohr radius/spectrum. For nuclear, the convention is still **Ϟ and ϟ (U+03DE, U+03DF)**; at the nucleon surface Ϟ = √2 (v_surface = c/√2) and trefoil (n = 3, m = 2) where relevant.

This order ensures that body-specific quantities (R_phys, k or z) are taken from observation or from a known scale (e.g. solar k from B5), and that all derived quantities (R_c, v(r), acceleration, escape speed) follow from the same formulas. The calculation order is the same whether the system is a nucleus, a star, or a galaxy; only the numerical values of R and k change.

---

### Falsification vectors (implementation logic 4.2)

The dataset specifies **falsification vectors**—places where experiment or theory could contradict SDT. They are not predictions of failure; they are the agreed checks.

**Atomic.** **Lamb shift.** SDT predicts orbital and spectral structure from the Ϟ framework; the Lamb shift is a subtle effect that may require the discrete structure of the spation medium (e.g. decoherence or finite size) to be fully reproduced. **Orbital scale:** the hydrogen orbital scale is d_orbital ≈ 3.36 α⁻² d_nuclear; consistency of this ratio with observed radii and with nuclear scale (trefoil node) is a check.

**Galactic.** **Rotation curves.** SDT predicts v = c √(R_occ/r) with R_occ (occlusion radius) scaling set by geometry. Flat or rising rotation curves must be explained by the distribution of displacing mass (screening, R_occ) without ad hoc dark matter. A hard-line geometric prediction that could falsify would be a systematic mismatch between observed v(r) and the occlusion-based form for a given mass profile.

**Nuclear.** **³He vs ³H binding.** The difference in binding energy between helium-3 and tritium depends on the geometry of the third nucleon and the electron-mediated (or magnetic) bonding. SDT’s node geometry and the same Ϟ/ϟ framework (nucleon surface Ϟ = √2) must yield the correct trend. A persistent discrepancy that cannot be resolved by improved geometry or screening would count against the framework.

Implementers and reviewers should use these vectors when validating code or comparing SDT to data: success at these points supports the model; clear, repeatable failure would require revision of the axioms or scope.

---

### How to use this treatise

- **By role.** If you are **implementing** the physics engine, start with this chapter (primitives, notation, calculation order), then Chapter 2 (occlusion), Chapter 3 (master equation), and Chapter 12 (benchmark suite and certification). Use Chapter 13 as the formula index. If you are **validating** against benchmarks, use the certification sections in each chapter (e.g. B1 in Chapter 2, B2–B4 in Chapter 6) and the full benchmark list in Chapter 12. If you are **studying** the theory, read Books I–III in order; each chapter opens with context and closes with cross-references and a short summary.

- **Word-count band.** Each chapter is written to fall between 2,680 and 6,064 words (inclusive), with a target of about 3,500–4,500 words where possible. This keeps chapters long enough for full derivations and commentary but bounded for readability. A word-count checklist is provided at the end of the treatise.

- **Cross-references.** Chapters refer to benchmarks (B1–B12, D-01, S-01), formulas (F1–F17), and Rules (1–10) by their standard identifiers. “Part I,” “Part II,” “Part III” refer to the three parts of the primary dataset.

Chapter 2 establishes the geometric foundation: solid angle Ω(r), far-field occlusion O(r) = R²/(4r²), and Benchmark B1, so that the inverse-square behaviour used everywhere else is seen to be geometric only.

---

*Sources: Dataset intro + 4.1–4.2; 05_STRUCTURE_MAP §1–2.*



## Chapter 2: Geometry and the Occlusion Foundation

### Context and scope

Spatial Displacement Theory (SDT) does not introduce gravity or radiation dilution as separate laws. Instead, it derives both from a single geometric fact: a sphere of radius \(R\) at distance \(r\) blocks a definite fraction of the sky. That fraction—the *occlusion*—is a pure consequence of Euclidean solid-angle geometry. No empirical constants, no mass \(M\), no gravitational constant \(G\) appear in its derivation. This chapter establishes that foundation in full.

Here we (1) define the exact solid angle \(\Omega(r)\) subtended by a sphere of radius \(R\) as seen from a point at distance \(r\), (2) derive the far-field occlusion \(O(r) = R^2/(4r^2)\) and confirm its dimensions, (3) state and certify **Benchmark B1** (Geometric Foundation), and (4) present **Formula F9** (Occlusion) with derivation and commentary. The takeaway is that inverse-square behaviour—in acceleration, flux dilution, and the pressure deficit that SDT identifies with “gravity”—is *geometric only*. It is the same at nuclear, celestial, and galactic scales because it depends only on \(R\) and \(r\), not on scale-specific physics. The rest of the treatise (master orbital equation, redshift identity, hydrogen, solar system, classical tests, cosmology) builds on this one result.

---

### Solid angle: exact formula

Consider a sphere of radius \(R\) and a point \(P\) at distance \(r\) from its centre, with \(r \geq R\). The sphere subtends a solid angle \(\Omega(r)\) at \(P\). Standard Euclidean geometry gives the solid angle of a spherical cap of half-angle \(\theta\) as \(2\pi(1 - \cos\theta)\). For a sphere of radius \(R\) with centre \(O\), the cap as seen from \(P\) is the set of directions from \(P\) that hit the sphere. The half-angle \(\theta\) satisfies \(\sin\theta = R/r\) (right triangle from \(P\) to the centre and to the tangent from \(P\) to the sphere). Thus \(\cos\theta = \sqrt{1 - R^2/r^2}\), and

\[
\Omega(r) = 2\pi\left(1 - \sqrt{1 - R^2/r^2}\right).
\]

**Step-by-step derivation.** (1) Draw the line from \(P\) to the centre \(O\) of the sphere; length \(r\). (2) From \(P\), draw a tangent to the sphere; the tangent touches the sphere at a point \(T\). The line \(OT\) is perpendicular to the tangent and has length \(R\). So the triangle \(POT\) is right-angled at \(T\), with \(PO = r\) and \(OT = R\). Hence the half-angle at \(P\) satisfies \(\sin\theta = R/r\). (3) The solid angle of a cone of half-angle \(\theta\) (the set of directions from \(P\) that hit the sphere) is the area on the unit sphere cut off by that cone. For a sphere, the area of a cap of half-angle \(\theta\) is \(2\pi(1 - \cos\theta)\) steradians. (4) Substitute \(\cos\theta = \sqrt{1 - \sin^2\theta} = \sqrt{1 - R^2/r^2}\) to obtain \(\Omega(r) = 2\pi(1 - \sqrt{1 - R^2/r^2})\). No physics beyond Euclidean geometry is used.

**Variables:**
- \(R\): physical radius of the sphere (metres).
- \(r\): radial distance from the centre of the sphere to the observer (metres).
- \(\Omega(r)\): solid angle subtended by the sphere at distance \(r\) (steradians, sr).

This expression is exact for all \(r \geq R\). At \(r = R\) (observer on the surface), \(\sqrt{1 - R^2/r^2} = 0\), so \(\Omega = 2\pi\) sr (half the sky). As \(r \to \infty\), \(\Omega \to 0\). In words: the solid angle is \(2\pi\) times one minus the cosine of the half-angle, where the half-angle is determined solely by the ratio \(R/r\).

---

### Far-field approximation and occlusion

When \(r \gg R\), we expand \(\sqrt{1 - R^2/r^2} \approx 1 - R^2/(2r^2)\). Then

\[
1 - \sqrt{1 - R^2/r^2} \approx \frac{R^2}{2r^2},
\]

so

\[
\Omega(r) \approx 2\pi \cdot \frac{R^2}{2r^2} = \frac{\pi R^2}{r^2}.
\]

The *occlusion* \(O(r)\) is the fraction of the full sky (\(4\pi\) sr) blocked by the sphere:

\[
O(r) = \frac{\Omega(r)}{4\pi}.
\]

In the far field, with \(\Omega(r) \approx \pi R^2/r^2\),

\[
\boxed{O(r) = \frac{R^2}{4r^2}.}
\]

This is **Formula F9** (Occlusion). In words: the fraction of the sky blocked by a sphere of radius \(R\) at distance \(r\) is \(R^2/(4r^2)\). No constants, no mass, no coupling—only geometry. Verbal form: *Occlusion equals the square of the sphere’s radius divided by four times the square of the distance.*

**Commentary.** F9 is the single geometric input from which SDT derives inverse-square behaviour. The pressure deficit in the spation medium at distance \(r\) is taken to scale with the fraction of the sky that is “blocked” by the displacing body—i.e. the solid angle it subtends divided by the full sky. So the deficit scales as \(\Omega/(4\pi) = O(r)\). In the far field that is \(R^2/(4r^2)\). Any force or acceleration that is proportional to this deficit will then scale as \(1/r^2\). Thus the inverse-square law is not an independent assumption; it is the direct consequence of spherical geometry and the identification of “force” with pressure gradient.

---

### Dimensional analysis

Solid angle is dimensionless in the sense that it is a ratio of areas (sphere cap to radius-squared); the SI derived unit is the steradian (sr), with dimension 1. So \([\Omega] = 1\). The full sky is \(4\pi\) sr, so \(O = \Omega/(4\pi)\) is a pure number: \([O] = 1\). Checking the right-hand side: \(R^2\) and \(r^2\) both have dimension \(\mathsf{L}^2\), so \(R^2/r^2\) is dimensionless. Thus \([O] = 1\) is satisfied. Benchmark B1 explicitly certifies this dimensional consistency: the inverse-square law and occlusion are derived from Euclidean geometry with no empirical parameters, and \([O] = 1\) is verified.

---

### Benchmark B1: Geometric Foundation — full certification

**What is certified:** The inverse-square law and occlusion \(O(r) = R^2/(4r^2)\) are derived from Euclidean solid-angle geometry with no empirical parameters. Dimensional analysis \([O] = 1\) is verified.

**Formulas (certified):**
- Exact solid angle: \(\Omega(r) = 2\pi\left(1 - \sqrt{1 - R^2/r^2}\right)\).
- Far field (\(r \gg R\)): \(\Omega(r) \approx \pi R^2/r^2\).
- Occlusion (fraction of sky blocked): \(O(r) = \Omega/(4\pi) = R^2/(4r^2)\).

**Commentary:** B1 is the foundation of all SDT dynamics. Gravity and radiation dilution both emerge from the same geometric fact: a sphere of radius \(R\) at distance \(r\) blocks a fraction \(R^2/(4r^2)\) of the sky. The pressure deficit in the spation medium scales with this occlusion, giving inverse-square acceleration. No \(G\), no \(M\)—only \(R\) and \(r\). This is why SDT can treat nuclear, celestial, and galactic scales with one velocity law and the identity \(z \cdot k^2 = 1\): the underlying dependence on “size and distance” is the same occlusion.

**Experimental / theoretical check:** Dimensional consistency is confirmed; agreement with the Newtonian limit is obtained when \(k\) and \(R_c\) are identified with \(GM/c^2\) and \(R\) in the appropriate limit. No free parameters are introduced. **Status: CERTIFIED.**

**Commentary (B1).** B1 is the first of the certified benchmarks. It does not depend on any measured constant (other than the geometric use of \(R\) and \(r\)). So “certification” here means: the derivation is logically complete, dimensionally consistent, and sufficient to support all later SDT formulas that depend on inverse-square behaviour. If B1 were false (e.g. if solid angle did not scale as \(R^2/r^2\) in the far field), the entire SDT dynamical structure would need to be rederived. No such failure is known; the Euclidean solid angle is standard geometry.

---

### Formula F9: Occlusion — statement, derivation, and why it matters

**Statement:** Far-field occlusion (fraction of sky blocked by a sphere of radius \(R\) at distance \(r\)) is \(O(r) = R^2/(4r^2)\). The exact solid angle is \(\Omega(r) = 2\pi\left(1 - \sqrt{1 - R^2/r^2}\right)\), and \(O = \Omega/(4\pi)\).

**Derivation (concise):**
1. Solid angle of the spherical cap from \(P\): \(\Omega(r) = 2\pi(1 - \sqrt{1 - R^2/r^2})\).
2. For \(r \gg R\), Taylor expansion gives \(\Omega \approx \pi R^2/r^2\).
3. Occlusion is the fraction of the full sky: \(O = \Omega/(4\pi) = R^2/(4r^2)\).
4. \([O] = 1\) (dimensionless).

**Why it matters:** All inverse-square behaviour in SDT—radial acceleration \(a(r) \propto 1/r^2\), flux dilution, and the pressure gradient that replaces “gravitational” force—stems from this relation. B1 certifies that no physics beyond Euclidean geometry is needed for the foundation. Every later benchmark (B2–B12) and formula (F1–F17) that uses the same \(R\), \(r\), and \(k\) (or Ϟ) structure rests on occlusion. Without B1 and F9, the master orbital equation and the redshift identity would lack their geometric anchor.

**Second commentary (F9).** F9 has no free parameters. Once you choose \(R\) (the radius of the displacing body) and \(r\) (the distance of the test point), \(O(r)\) is fixed. So at 1 AU from the Sun, with \(R_\odot \approx 6.96\times10^8\) m and \(r \approx 1.496\times10^{11}\) m, the occlusion is \(R^2/(4r^2) \approx 2.16\times10^{-6}\). That small number is the fraction of the sky blocked by the Sun; the pressure deficit at Earth’s orbit scales with it, and hence the “gravitational” acceleration toward the Sun also scales with it. The same formula applies to a nucleus occluding the medium at a distance of a few fm: only the numerical values of \(R\) and \(r\) change.

---

### Why inverse-square is geometric only

In SDT, “gravity” is not a separate force mediated by mass. It is the dynamical response of the spation medium to a pressure deficit. That deficit is proportional to the fraction of the sky occluded by the displacing body: the more sky blocked, the larger the local pressure drop and the resulting inward acceleration. Because occlusion is \(O(r) = R^2/(4r^2)\), the deficit, and hence the acceleration, scale as \(1/r^2\). So the inverse-square law is not postulated; it is derived from the geometry of a sphere in Euclidean space.

Consequences:
- **No \(G\) or \(M\) in the foundation.** Body-specific quantities enter later via the c-boundary radius \(R_c = R_{\text{phys}}/k^2\) and the velocity field \(v^2 = c^2 R_c/r\), which themselves tie back to occlusion and the single medium.
- **Scale invariance.** The same \(O(r)\) applies to a nucleus, a star, or a galaxy. Only \(R\) and \(r\) (and the body’s \(k\)) change; the \(1/r^2\) form does not.
- **Radiation and “gravity” unified.** Flux from a compact source also dilutes as \(1/r^2\) because the same solid-angle argument applies to the fraction of the sphere’s surface (or emitting shell) visible at distance \(r\). One geometry underlies both.

This is why the document can speak of a single framework from hydrogen to exoplanets to the CMB: the inverse-square behaviour is geometric only, and the rest is consistent application of the master equation and \(z \cdot k^2 = 1\).

**Worked limits.** At the surface of a body, \(r = R\), the exact formula gives \(\Omega = 2\pi\) and \(O = 1/2\): half the sky is blocked. So the pressure deficit at the surface is maximal (in the sense that the body blocks half of the incoming pressure field from that hemisphere). In the far field, \(O(r) = R^2/(4r^2)\) is the working approximation. For the Sun at 1 AU, \(O \approx 2.16\times10^{-6}\); for a proton of radius \(\sim 0.84\) fm at 1 fm, \(O \sim R^2/(4r^2)\) is of order 0.1–0.2 depending on the exact \(R\) used. So nuclear and stellar systems both obey the same \(O(r)\); only the length scales differ.

---

### Checks and cross-references

- **B1** certifies the geometric foundation and \([O] = 1\); F9 is the occlusion formula.
- **Rule 1** (Ten Rules): occlusion as the basis for the pressure deficit and inverse-square.
- **Rule 2:** acceleration \(a(r) = c^2 R/(\varkappa^2 r^2)\) follows from the pressure gradient that scales with occlusion; F10 gives the same in terms of \(R_c\).
- **F1 (Master orbital equation):** \(v^2 = c^2 R_c/r\) is derived from hydrostatic equilibrium in the same medium whose pressure gradient is set by occlusion; see Chapter 3.
- **F10 (Acceleration):** \(a(r) = c^2 R_c/r^2\) is centripetal \(v^2/r\) with F1; the \(1/r^2\) factor is the same as in \(O(r)\).
- **B2–B12:** All use the same \(R\), \(r\), and \(k\) (or Ϟ) structure that ultimately traces back to B1 and F9.

**Falsification / limits:** B1 is purely geometric; it does not by itself fix \(k\) or \(R_c\) for a given body. Those come from dynamics and spectroscopy (e.g. B2, B5). Disagreement of observed orbits or redshift with the master equation and \(z \cdot k^2 = 1\) would challenge the *use* of occlusion in dynamics, not the correctness of \(O(r) = R^2/(4r^2)\) as solid-angle geometry.

---

### Summary

- **Exact solid angle:** \(\Omega(r) = 2\pi\left(1 - \sqrt{1 - R^2/r^2}\right)\); far field: \(\Omega(r) \approx \pi R^2/r^2\).
- **Occlusion (F9):** \(O(r) = R^2/(4r^2)\); \([O] = 1\).
- **B1** certifies that inverse-square and occlusion come from Euclidean geometry with no empirical parameters.
- Inverse-square in SDT is **geometric only**: same at all scales; no \(G\) or \(M\) in the foundation; radiation dilution and “gravitational” acceleration share the same geometric origin.

Chapter 3 will introduce the master orbital equation and velocity field that use this occlusion-based pressure gradient to give \(v^2 = c^2 R_c/r\) and the full set of orbital and redshift relations.

---

*Sources: Part I §1 (precursor to 1.1), Part II B1, Part III F9; 05_STRUCTURE_MAP §1–2; 09_CANONICAL_SDT_FORMULAS §1.*



## Chapter 3: Master Orbital Equation and Velocity Field

### Context and scope

Chapter 2 established that inverse-square behaviour—occlusion O(r) = R²/(4r²) and the pressure deficit it implies—rests on Euclidean solid-angle geometry alone. No mass, no coupling constant G; only the radius R of the displacing body and the distance r. This chapter introduces the **single dynamical equation** that converts that geometry into orbital motion: the master orbital equation. It governs the velocity field v(r) around any displacement source, from nucleons to galaxies, and yields acceleration, escape speed, and the radius-dependent velocity ratio Ϟ(r). All of this follows from hydrostatic equilibrium in the spation medium and one boundary condition: at a certain radius (the c-boundary), the orbital velocity equals the speed of light c.

The chapter is organised as follows. First we state the master equation in its two equivalent forms and define every variable (Formula F1 / Axiom 1.1). We then derive it from hydrostatic equilibrium and the c-boundary condition, and clarify what the c-boundary is and is not. Next we derive the radial acceleration (Formula F10, Rule 2), escape velocity (Formula F16, Rule 6), and the radius-dependent koppa Ϟ(r) (Formula F17), and we tie these to Rules 4, 5, and 9. A section on scale invariance shows that the same equation, with the same structure, applies across nuclear, celestial, and galactic scales—with nuclear use of κ = 1/√2 as the only scale-specific tweak. The chapter closes with a concise recap of the calculation order, cross-references to benchmarks (B2, B5, B6, B7, B8, D-01), and falsification vectors, plus a short worked example to fix ideas.

**Notation.** In this treatise, Ϟ (koppa, U+03DE) denotes the variable velocity ratio c/v at a given location; at the c-boundary, Ϟ = 1. The symbol k is used interchangeably for the surface value (k = c/v_surface). R_c is the c-boundary radius (geometric mass); R_phys is the physical surface radius of the body. κ (kappa) is reserved for the nuclear virial factor 1/√2 unless topology specifies otherwise (e.g. trefoil κ ≈ 0.694).

---

### The master orbital equation (F1 / Axiom 1.1)

#### Statement and equivalent forms

The velocity field in the spation medium around any compact displacement source is given by:

**Master orbital equation (F1):**
```
v² = c² (R_c / r)
```

Equivalently, in terms of physical radius and the surface velocity ratio k = c/v_surface:

**v(r) = (c/k) √(R_phys / r)**

with the c-boundary radius defined as **R_c = R_phys / k²**. Thus R_c is the radius at which the orbital speed would equal c; it is a geometric length scale, not a physical surface.

In koppa notation: at the surface, Ϟ = k = c/v_surface, so v_surface = c/Ϟ. Then v(r) = (c/Ϟ)√(R/r) with R = R_phys, and R_c = R/Ϟ². The form **v(r) = c √(R_c/r)** follows immediately: at r = R_c, v = c; at r > R_c, v < c.

#### Variables

| Symbol | Meaning | Units | Notes |
|--------|--------|--------|--------|
| v | Orbital velocity at radius r | m/s | Tangential speed for circular orbit; same field describes radial free-fall scaling. |
| c | Speed of light (propagation speed of the medium) | m/s | 2.99792458×10⁸ m/s (exact). |
| R_c | c-boundary radius (geometric mass) | m | At r = R_c, v = c. R_c = R_phys/k². |
| r | Radial distance from the geometric centre | m | r ≥ R_phys for external orbits. |
| R_phys | Physical surface radius of the body | m | Surface where v = v_surface = c/k. |
| k (or Ϟ at surface) | Inverse velocity ratio at surface | dimensionless | k = c/v_surface; at c-boundary, Ϟ = 1. |

So the only body-specific inputs are R_phys and k (or, equivalently, R_c). No gravitational constant G and no mass M appear in the equation. The dynamics are fixed by geometry (R, r) and the saturation of the medium at the c-boundary.

#### Derivation from hydrostatic equilibrium

The spation medium is in hydrostatic equilibrium. The pressure P decreases outward, and the radial pressure gradient supports the centripetal stress of the flow. For a steady, spherically symmetric velocity field v(r):

(1) **dP/dr = −ρ_s (v²/r)**

where ρ_s is the spation mass density. Pressure is sustained by the displacement flux; the flux scales with v, so the dynamic pressure scales as ρ_s v². Hence:

(2) **P ∝ ρ_s v²**

so that dP/dr ∝ ρ_s (d/dr)(v²). Combining with (1) gives (d/dr)(v²) ∝ −v²/r, i.e. v² ∝ 1/r. The constant of proportionality is set by the boundary condition: at the c-boundary radius R_c, the orbital velocity equals c. Thus:

(3) **v²(R_c) = c²** ⇒ **v²(r) = c² (R_c / r)**

So **v² = c² R_c/r** and **v(r) = c √(R_c/r)**. In terms of surface quantities, v_surface = c/k at r = R_phys, so v²(R_phys) = c²/k² = c² R_c/R_phys, giving R_c = R_phys/k² and v(r) = (c/k)√(R_phys/r). The derivation uses only hydrostatics and the single boundary condition v = c at R_c; no additional free parameters.

**Physical meaning.** The pressure gradient balances the centrifugal stress of the flow; the ratio R_c/r determines how much slower than c the orbit is at radius r. Closer to the source (smaller r), v is larger; at r = R_c, v reaches c. The “geometric mass” R_c is the single length scale that sets the strength of the field: all orbits at a given r respond to the same R_c. That is why one equation suffices from nucleons to galaxies—only R_c (or R_phys and k) changes with the body.

#### The c-boundary: meaning and constraint

The **c-boundary** is the radius R_c at which the orbital velocity in the medium equals c. It is the velocity saturation point of the medium: the locus where v = c. It is **not** a singularity. In particular:

- At r = R_c, v = c and Ϟ(r_c) = 1.
- For r > R_c, v < c and Ϟ(r) > 1.
- R_c is related to the physical surface by R_c = R_phys/k². For the Sun, R_phys ≈ 6.96×10⁸ m and k_⊙ ≈ 686.6, so R_c(☉) ≈ 1.48 km—far inside the visible surface.

The same functional form v² = c² R_c/r applies at nuclear, celestial, and galactic scales. At nuclear scale, the surface velocity is v_surface = cκ with κ = 1/√2, so effectively k = 1/κ and the same master equation holds with the κ factor absorbed into the effective R_c or into the surface scaling (see Scale invariance below).

---

### Acceleration (F10) and Rule 2

From the master equation, the centripetal acceleration required to hold a test body in circular motion at radius r is a = v²/r. Substituting v² = c² R_c/r:

**a(r) = c² R_c / r²**

Since R_c = R_phys/k² (or R_c = R_phys/Ϟ²), this is equivalently:

**Formula F10 (acceleration):** **a(r) = c² R_phys / (k² r²) = c² R_c / r²**

**Rule 2 (Pressure-Difference Acceleration):** The radial acceleration toward the source is a(r) = c²R/(Ϟ²r²).

So the “gravitational” acceleration in SDT is the centripetal acceleration of the velocity field. No separate force law is postulated; it follows from the same pressure gradient that gave v² ∝ 1/r. Dimensional check: [c² R_c / r²] = (m/s)² · m / m² = m/s². Again, no G and no M—only R_c (or R_phys and k) and r. In the appropriate limit, this matches the Newtonian form when the geometric parameters are identified with the conventional Schwarzschild or Newtonian scales (Benchmark B6; Chapter 7).

**Why F10 matters.** F10 is the direct link between the master equation and “Newtonian” gravity. Once v² = c² R_c/r is accepted, a = v²/r is unavoidable for circular motion. So the inverse-square acceleration is not a separate law; it is the kinematic consequence of the velocity field. Every benchmark that tests orbital dynamics (B3 centripetal force, B6 planetary orbits) is implicitly testing F10 as well. The same formula applies at nuclear scale when written with κ: the pressure gradient that confines nucleons scales with c² R/(κ² r²).

---

### Escape velocity (F16) and Rule 6

The work required to move a test mass from the surface (or from radius r) to infinity is the integral of the radial force (or a(r)) with respect to r. For a(r) = c² R_c/r², the potential difference from r to infinity scales as c² R_c/r. Equating kinetic energy at launch to this work gives (1/2)v_escape² = c² R_c/r. At the **physical surface** r = R_phys, v_surface = c/k, so the work from R_phys to infinity is (1/2)(c/k)² × (factor from integration). The escape velocity from the surface is:

**Formula F16 (escape velocity):** **v_escape = √2 × c/Ϟ**

Equivalently, **v_escape = √2 × v_surface**. So the escape speed is exactly √2 times the surface orbital speed. This is geometric: the factor √2 arises from the 1/r potential implied by a ∝ 1/r².

**Rule 6 (Escape Velocity Rule):** v_escape = √2 × c/Ϟ.

At nuclear scale, the virial stability limit is κ = v_orb/v_esc = 1/√2 (Chapter 5). So the same √2 relation appears in the orbital-to-escape ratio; the nuclear κ is the inverse of that ratio at the nucleon surface. **Why it matters:** Escape velocity is not a separate postulate; it is the integrated effect of the same a(r). The factor √2 is geometric (from the 1/r potential), and it ties directly to nuclear stability (κ = 1/√2) 
---

### Radius-dependent koppa Ϟ(r) (F17) and Rules 4, 5, 9

The velocity ratio Ϟ is defined at every radius as Ϟ(r) = c/v(r). From v(r) = c√(R_c/r) we have v(r)/c = √(R_c/r), so:

**Formula F17 (radius-dependent koppa):** **Ϟ(r) = √(r / r_c)**

Here r_c = R_c (c-boundary radius). So Ϟ increases with r: at r = r_c, Ϟ = 1; at the physical surface r = R_phys, Ϟ = k = c/v_surface; and at larger r, Ϟ grows as the square root of r/r_c. The “koppa at surface” (k or Ϟ_surface) is the anchor; Ϟ(r) extends the same geometry to all radii.

**Rule 4 (Master Orbital Equation):** v(r) = (c/Ϟ)√(R/r). With Ϟ(r) = √(r/r_c) and R_c = R/Ϟ², this is v(r) = c√(R_c/r), as above.

**Rule 5 (Surface Velocity Rule):** v_surface = c/Ϟ. At r = R_phys, Ϟ = k, so v_surface = c/k.

**Rule 9 (c-Boundary Rule):** r_c = R/Ϟ²; at r = r_c, Ϟ(r_c) = 1 (orbital velocity = c). So the c-boundary is the unique radius where the local koppa equals 1.

Together, Rules 4, 5, and 9 tie the velocity field, surface velocity, and c-boundary into one consistent picture: one parameter (e.g. k or R_c) fixes v(r) everywhere.

**Why F17 matters.** Ϟ(r) is the local “slowness” of the orbit relative to c: at large r, Ϟ is large and v is small. It is the running coupling that connects the surface (where we measure k) to the c-boundary (where Ϟ = 1). In hydrogen, Ϟ_H = 137.036 at the Bohr radius; in the Sun, k_⊙ ≈ 686.6 at the photosphere. F17 says that at any intermediate r, the local ratio is Ϟ(r) = √(r/r_c). So the entire radial profile is fixed by one number (r_c or k). This is why “three routes to solar Ϟ” (B5) all converge: they are three ways to fix the same r_c.

---

### Scale invariance: nuclear, celestial, galactic

The same master equation and the same koppa structure apply across some 53 orders of magnitude in length scale.

**Celestial (planets, moons, exoplanets).** For the Sun, k_⊙ ≈ 686.6 and R_c(☉) ≈ 1.48 km. Planetary orbital velocities satisfy v(r) = (c/k_⊙)√(R_☉/r) = c√(R_c/r) (Benchmarks B5, B6). Jupiter’s satellites obey the same form with Jupiter’s k_J and R_J (B7); exoplanets use the stellar k and R (B8). No G, no M; only R_c (or R and k) and r.

**Nuclear.** At nucleon scale, the surface velocity is not c but cκ with κ = 1/√2 (Chapter 5). So v_surface = c/√2 and the effective “koppa” at the nucleon surface is 1/κ = √2. The velocity field is **v² = c² κ² (R/r)** with the same 1/r dependence. Same equation, with κ² scaling the effective R_c. Kinetic energy per nucleon is (1/2)m_N v² = m_N c²κ²/2 = m_N c²/4; confinement and overlap pressures scale with κ² (Formula F11; Chapter 10). So nuclear dynamics use the same geometric law with κ = 1/√2 at the nucleon surface.

**Galactic.** Flat rotation curves are interpreted in SDT as v = c√(R_occ/r) where R_occ is an occlusion radius (screening or effective displacement radius). The same inverse-square-root form holds; the “flat” curve arises from how R_occ scales with r in the disk (Chapter 8; Benchmark B10). So again: same equation, different scale.

**Rule 10 (Scale Invariance):** Same equations, same Ϟ structure, across nuclear, celestial, and galactic scales. The master equation v² = c² R_c/r (and its nuclear form v² = c²κ²(R/r)) is the single dynamical engine; only the numerical values of R, r_c, and (at nuclear scale) κ change.

**Commentary.** Scale invariance is a falsifiable claim: if orbital velocities at some scale required a different functional form (e.g. v ∝ r rather than v ∝ 1/√r), the framework would fail. Benchmarks B6–B8 (planets, moons, exoplanets) and nuclear first-principles (D-01, F11) are the empirical anchors. The only scale-specific ingredient is κ = 1/√2 at the nucleon surface; elsewhere the surface koppa k is fixed by observation (or by the proton–solar bridge k_⊙ = k_p²).

---

### Calculation order, benchmarks, and falsification

**Calculation order (from Chapter 1 / Part I §4.1).** (1) Define scale: choose R_phys and v_surface (or redshift z). (2) k = c/v_surface or k = 1/√z. (3) R_c = R_phys/k². (4) v(r) = (c/k)√(R_phys/r) = c√(R_c/r). (5) For atomic/nuclear applications, apply trefoil (n=3, m=2) and κ = 1/√2 where appropriate.

**Benchmarks that rest on the master equation.** B2 (Koppa anchor): Ϟ_H = 137.036 from hydrogen; Ϟ = 1 at r_c. B5 (solar Ϟ): three routes to k_⊙ ≈ 686.6; z×k² = 1. B6 (solar system orbits): planetary v(r) from r_c(☉) ≈ 1.48 km; max error < 0.41%. B7 (Jovian system): same v(r) for Galilean moons. B8 (exoplanets): stellar k then v_planet; typical error ~1%. D-01 (deuteron): binding from geometry and κ = 1/√2. All of these use F1, F10, F16, F17 and Rules 2, 4, 5, 6, 9 without introducing new constants.

**Falsification vectors (Part I §4.2).** Atomic: Lamb shift; orbital vs nuclear length scales (d_orbital ≈ 3.36 α⁻² d_nuclear). Galactic: rotation curves; predictions of v = c√(R_occ/r) and R_occ scaling. Nuclear: ³He vs ³H binding from electron-mediated node geometry. A confirmed deviation in these areas would challenge the single-field picture. The master equation F1 is thus the central dynamical statement of SDT; all of B2, B5, B6, B7, B8, and D-01 rely on it without introducing additional empirical constants.

#### Worked example: Earth’s orbital velocity

Solar physical radius R_☉ ≈ 6.96×10⁸ m; k_⊙ ≈ 686.6; so R_c(☉) = R_☉/k_⊙² ≈ 1.476×10³ m (about 1.48 km). Earth’s orbital radius r ≈ 1.496×10¹¹ m. Then:

v(r) = c √(R_c/r) ≈ 2.998×10⁸ × √(1476 / 1.496×10¹¹) m/s ≈ 2.998×10⁸ × 9.93×10⁻⁵ ≈ 29.76 km/s.

Observed value ≈ 29.78 km/s; agreement to within 0.1%. No G, no M_☉—only R_c and r (Benchmark B6).

**Second example: Io (Jupiter).** Jupiter’s physical radius R_J ≈ 6.99×10⁷ m; from B7, Jupiter’s k_J is determined by its surface dynamics (rotation or satellite orbits). Io’s orbital radius r ≈ 4.22×10⁸ m. Using the same formula v(r) = c√(R_c/r) with Jupiter’s R_c gives Io’s orbital velocity. B7 certifies max error 0.00% for the Galilean satellites—the same master equation and calculation order apply to planet–moon systems (Rule 10).

---

### Summary

- **F1:** v² = c² R_c/r; v(r) = (c/k)√(R_phys/r); R_c = R_phys/k². Derived from hydrostatic equilibrium and v = c at R_c.
- **F10:** a(r) = c² R_c/r² (Rule 2). Centripetal acceleration of the velocity field; no G, no M.
- **F16:** v_escape = √2 × c/Ϟ (Rule 6). Geometric √2 from 1/r potential.
- **F17:** Ϟ(r) = √(r/r_c). Radius-dependent koppa; Rules 4, 5, 9 tie v(r), v_surface, and c-boundary.
- **Scale invariance:** Same equation at nuclear (κ = 1/√2), celestial, and galactic scales; Rule 10.

The master orbital equation and velocity field are the core dynamics of SDT. Chapters 4 and 5 add the redshift–displacement identity and trefoil proton structure; Chapters 6–9 apply and certify this dynamics from hydrogen to classical tests and paradox resolution.

---

*Word count: ~2,720 (target 2,680–6,064).*

*Sources: SDT_CORE_AXIOMS_AND_DATASET.md Part I §1.1, Part III F1, F10, F16, F17; 09_CANONICAL_SDT_FORMULAS.md §2; 06_RAW_FORMULA_LIST Rules 2, 4, 5, 6, 9.*



## Chapter 4: Redshift–Displacement Identity and Scaling

### Context and scope

Chapters 2 and 3 established the geometric foundation (occlusion O(r) = R²/(4r²)) and the master orbital equation (v² = c² R_c/r). The velocity field and acceleration follow from hydrostatic equilibrium and the c-boundary condition, with no gravitational constant G or mass M. This chapter adds the **universal identity** that locks gravitational redshift to the displacement parameter: **z · k² = 1**. It defines z and k precisely, states **Formula F2** (the identity) and **Formula F3** (k definition and scaling), and presents the **proton–solar bridge** (k_solar = k_proton²) and the role of the fine-structure constant and trefoil factor 5. **Rule 7** (three routes to Ϟ) is given in full, with short derivation and commentary. The takeaway is that one measurement—either spectral (redshift z) or dynamical (surface velocity, hence k)—fixes the other; no free parameter separates “gravitational redshift” from the same geometric lock that gives hydrogen (137), solar (686), and CMB (z ≈ 1090).

**Source mapping:** Part I §1.2; Part III F2, F3.

---

### Definitions: z and k

**k (displacement parameter).** The dimensionless ratio **k = c / v_surface** is the inverse of the velocity ratio at the physical surface of a body. So k is “how many times slower than c” the surface orbital (or flow) velocity is. For the Sun, v_surface (or the equivalent orbital speed at the photosphere) gives k_⊙ ≈ 686.6. For the hydrogen electron in the ground state, v_electron ≈ 2.188×10⁶ m/s, so **Ϟ_H = k_H = c/v_electron ≈ 137.036**—the inverse of the fine-structure constant α. At the c-boundary, by definition v = c, so the “surface” there has k = 1 (or Ϟ = 1).

**z (gravitational redshift).** The **geometric depth** of the potential well is defined as **z = R_c / R_phys**. So z is the ratio of the c-boundary radius to the physical radius. It is the “redshift” in the sense that light climbing out of the well is redshifted by a factor (1+z) in wavelength (or 1/(1+z) in frequency). For the Sun, z_solar ≈ 2.12×10⁻⁶; for the CMB boundary, z ≈ 1090. Both z and k are dimensionless.

**Relation.** From the master equation at the surface: v_surface² = c² R_c/R_phys = c² z. So v_surface = c√z, hence **k = c/v_surface = 1/√z**. Thus **z = 1/k²** and therefore **z · k² = 1**. This is the **universal redshift–displacement identity**.

---

### Formula F2: Universal identity z · k² = 1

**Statement:** **z · k² = 1**, with k = c/v_surface and z = R_c/R_phys (so z = 1/k²).

**Derivation.** (1) k = c/v_surface by definition. (2) At r = R_phys, v = v_surface = c/k. (3) From the master equation, v² = c² R_c/r; at r = R_phys, v_surface² = c² R_c/R_phys = c² z. So (c/k)² = c² z, hence 1/k² = z, i.e. z · k² = 1. (4) Equivalently, the c-boundary is at R_c = R_phys/k², so z = R_c/R_phys = 1/k².

**Why it matters.** One measurement (either spectral z or dynamical k) fixes the other. There is no separate “gravitational redshift formula” with a free constant; the lock is geometric and holds at nuclear, stellar, and galactic scales. Fine structure (137), solar (686), and CMB (z ≈ 1090) all satisfy the same identity. Benchmark B5 certifies z×k² = 1 for the Sun; B2 gives Ϟ_H = 137.036 from hydrogen; B12 ties CMB z to the boundary. So F2 is the single equation that connects spectroscopy and dynamics across scales.

**Verification (Sun).** z_solar ≈ 2.12×10⁻⁶; k_⊙ ≈ 686.6; k² ≈ 471,556; z × k² ≈ 1.00. B5 certifies this to high precision (σ ≈ 0.03%).

---

### Formula F3: k definition and scaling k_solar = k_proton²

**Statement:** k = c/v_surface. For the proton (trefoil): k_p ≈ 26.2; for the Sun: k_⊙ = k_p² ≈ 686.

**Derivation.** (1) k = c/v_surface from definition. (2) Trefoil topology (Chapter 5): k_p² = 5 α⁻¹ ≈ 685.18, so k_p ≈ 26.2. (3) Solar–proton bridge: the scaling law is **k_⊙ = k_p²**. So the Sun’s displacement parameter is the square of the proton’s. No independent “solar constant”; the proton and the Sun are linked by topology (the factor 5 = n²−m² from the trefoil) and the fine-structure constant.

**Why it matters.** The questions “why is the fine-structure constant what it is?” and “why is the solar k ≈ 686?” become one geometric story. The proton is a trefoil vortex with Δ_topo = 5; the hydrogen electron sees α⁻¹ = 137.036; and k_p² = 5 α⁻¹ gives 685.18, which is k_⊙. So the atomic scale (137) and the stellar scale (686) are not independent; they are related by the trefoil factor 5.

**Checks.** B2 (Ϟ_H = 137.036); B5 (k_⊙ ≈ 686.6 from three routes); trefoil Δ_topo = 5 (Chapter 5).

---

### Proton–solar bridge and fine structure

The **proton–solar bridge** is the relation **k_solar = k_proton²**. In numbers:

- **α⁻¹ = Ϟ_H ≈ 137.036** (hydrogen electron at Bohr radius; fine-structure inverse).
- **k_p² = 5 α⁻¹ ≈ 685.18** (trefoil topology: n=3, m=2, n²−m² = 5).
- **k_⊙ ≈ 686.6** (from orbital, rotation, and spectral routes; B5).

So k_⊙ is not 5 α⁻¹ by accident; it is k_p², and k_p² is 5 α⁻¹ by the topology of the proton (trefoil 3₁). The small difference between 685.18 and 686.6 is within the precision of the trefoil and solar determinations. The bridge certifies that one body (the proton) and one orbit (Bohr) fix the scale for all larger systems via z·k² = 1 and the master equation.

**Fine structure.** The fine-structure constant α ≈ 1/137.036 emerges in SDT as the ratio v_electron/c at the Bohr radius—i.e. 1/Ϟ_H. It is not a coupling constant inserted by hand; it is the measured velocity ratio of the ground-state electron. So “why α ≈ 1/137?” is “why is the electron’s speed at a₀ what it is?”—answered by the same velocity field and c-boundary that give the rest of the spectrum (B4).

**Trefoil factor 5.** The number 5 comes from the winding numbers of the trefoil knot: n = 3, m = 2, so Δ_topo = n² − m² = 9 − 4 = 5. So k_p² = 5 α⁻¹ ties the proton’s internal topology to the hydrogen scale. Chapter 5 develops this in full (F4, F12).

---

### Rule 7: Three routes to Ϟ (or k)

**Rule 7 (Ϟ-Value Calculation):** The displacement parameter Ϟ (or k) can be determined by three independent methods:

1. **Orbital:** Ϟ = c/√(β/R), where β is the orbital parameter (v²r) at a known orbit. Equivalently, from v_orb at radius r and R_phys: v_orb² = c² R_c/r and R_c = R_phys/k², so k = c/√(v_orb² r / R_phys) = c/√(β/R) with β = v_orb² r.
2. **Spectral:** Ϟ = 1/√z. From the gravitational redshift z (or the depth of the well), k = 1/√z. So a measurement of z (e.g. solar spectral lines) gives k directly.
3. **Rotation:** Ϟ = √(π c / v_rot). The surface rotation velocity v_rot is tied to the orbital velocity at a reference radius by v_rot = π v_orb²/c (Formula F8; Chapter 7). So from the observed rotation period and radius, v_rot is known, and k_⊙ = √(πc/v_rot) ≈ 686.6.

**Commentary.** B5 certifies that all three routes give the same k_⊙ to within about 0.03%. So the Sun’s displacement parameter is overdetermined: dynamics (orbit at 1 AU), spectrum (redshift), and rotation (sidereal period) all agree. No free solar constant is needed. The same three routes can be used for other stars (B8) and, in principle, for any body with measurable orbit, redshift, or rotation.

**Why “three routes” matter.** If only one route were available, k could be fitted. The convergence of three independent methods is a strong consistency check. It also shows that “gravitational redshift” and “orbital dynamics” are not separate phenomena in SDT; they are two expressions of the same geometric lock z·k² = 1 and the same velocity field.

**Worked example (solar k from each route).** (1) Orbital: Earth’s v_orb ≈ 29.78 km/s at r ≈ 1.496×10¹¹ m; R_☉ ≈ 6.96×10⁸ m. Then v_orb² r = β ≈ 1.33×10²⁰ m³/s²; k_⊙ = c/√(β/R_☉) ≈ 686.5. (2) Spectral: z_solar ≈ 2.12×10⁻⁶ ⇒ k_⊙ = 1/√z ≈ 686.9. (3) Rotation: v_rot from T_rot ≈ 25.4 days and R_☉ gives v_rot ≈ 2.0 km/s; k_⊙ = √(πc/v_rot) ≈ 686.6. All three cluster around 686.6; B5 reports σ ≈ 0.03%.

---

### Summary of formulas and rules

- **F2:** z · k² = 1; z = R_c/R_phys, k = c/v_surface. One measurement (z or k) fixes the other.
- **F3:** k = c/v_surface; k_solar = k_proton²; k_p² = 5 α⁻¹ ≈ 685.18; k_⊙ ≈ 686.6.
- **Rule 7:** Three routes to Ϟ: orbital (Ϟ = c/√(β/R)), spectral (Ϟ = 1/√z), rotation (Ϟ = √(πc/v_rot)).

**Cross-references.** B2 (Koppa anchor, Ϟ_H = 137.036); B5 (solar Ϟ, three routes, z×k² = 1); B12 (CMB z ≈ 1090). Chapter 5 gives the trefoil topology (F4) and the proton structure that yields k_p² = 5 α⁻¹. Chapter 6 fills in the hydrogen system (B2–B4); Chapter 7 the solar and stellar systems (B5–B8) and F8 (rotation coupling).

---

### Checks and physical meaning

**Physical meaning of z·k² = 1.** The identity says that the “depth” of the well (z) and the “slowness” of the surface (k) are reciprocally related: deeper well ⇒ slower surface ⇒ larger k, and z = 1/k². So a body with a large k (e.g. Sun, k ≈ 686) has a very small z (2.12×10⁻⁶); its c-boundary is very close to its surface in relative terms (R_c = R_phys/k²). A body with k = 1 (the c-boundary itself) has z = 1. The CMB boundary has z ≈ 1090, so the effective k at that “surface” would be 1/√1090 ≈ 0.03—but the CMB is usually described by z and R_uni/R_boundary rather than a single body k.

**Numerical check (proton–solar).** k_p ≈ 26.2 ⇒ k_p² ≈ 686.4; k_⊙ ≈ 686.6. Agreement to better than 0.1%. The trefoil prediction 5 α⁻¹ ≈ 685.18 is slightly lower; the difference is consistent with the precision of α, the trefoil geometry (κ ≈ 0.694), and the solar determinations.

Chapter 5 develops the trefoil topology (n=3, m=2, Δ_topo = 5), the minor-to-major radius ratio a/R = 1/√2, and the internal κ ≈ 0.694, and ties them to F4 and F12 (proton magnetic moment).

---

*Sources: Part I §1.2; Part III F2, F3; 09_CANONICAL §5; 06_RAW_FORMULA_LIST Rule 7.*



## Chapter 5: Trefoil Topology and Proton Structure

### Context and scope

Chapters 2–4 established the occlusion foundation, the master orbital equation, and the universal identity z·k² = 1. The proton–solar bridge (k_⊙ = k_p²) and the trefoil factor 5 were introduced in Chapter 4 but not derived. This chapter develops the **trefoil–torus topology** of the proton: the winding numbers n = 3, m = 2; the invariant Δ_topo = 5; the relation **k_p² = 5 α⁻¹ ≈ 685.18**; the minor-to-major radius ratio a/R = 1/√2; and the internal geometric parameter κ ≈ 0.694 ≈ 1/√2. It presents **Formula F4** (trefoil topology) and **Formula F12** (proton magnetic moment μ_p = e c R/(2√2)) with derivations and commentary. The takeaway is that the proton is not a point particle but a self-sustaining vortex knot (Trefoil 3₁) on a fat torus; that structure fixes both the hydrogen scale (137) and the solar scale (686), and links to the nuclear κ = 1/√2 used in deuteron and confinement (Chapter 10).

**Source mapping:** Part I §1.3; Part III F4, F12; 09_CANONICAL §5.

---

### The trefoil–torus model

The proton is modelled as a self-sustaining vortex knot on a fat torus. In knot theory, the Trefoil 3₁ is the simplest nontrivial knot: a closed loop with three crossings. When wrapped on a torus (a doughnut-shaped surface), the knot has two winding numbers: the **poloidal winding** n (times around the tube) and the **toroidal winding** m (times around the hole). For the Trefoil 3₁: n = 3, m = 2. The combination n² − m² = 9 − 4 = 5 is the key invariant that links the proton to the hydrogen scale and the Sun.

---

### Topology constants and Formula F4

**Δ_topo = n² − m² = 5.** The invariant appears in the proton's displacement parameter: **k_p² = (n² − m²) α⁻¹ = 5 × 137.035999 ≈ 685.18**, so **k_p ≈ 26.2**. The solar koppa is k_⊙ = k_p² ≈ 686 (Chapter 4, B5), so the proton and the Sun are locked: k_⊙ = k_p² = 5 α⁻¹.

**Formula F4:** Proton velocity factor from knot: n = 3, m = 2; Δ_topo = 5; k_p² = 5 × 137.036 ≈ 685.18. Internal κ from torus geometry: a/R = 1/√2; κ ≈ 0.694 ≈ 1/√2. **Derivation:** Trefoil 3₁ has n²−m² = 5; α⁻¹ from hydrogen (B2); k_⊙ = k_p² requires k_p² = 5 α⁻¹; κ from fat-torus stability (virial). **Why it matters:** The proton is a structured vortex; that structure fixes hydrogen (137), solar (686), and nuclear κ = 1/√2 (Chapter 10, CRITICAL CORRECTION).

---

### Occlusion and stability: a/R and κ

**a/R = 1/√2.** On a fat torus, a/R ≈ 0.7071 sets the virial limit v_orb/v_esc = 1/√2 (κ ≈ 1/√2). **κ ≈ 0.694.** The formula κ = π^(1/4) / (n (1+(a/R)²)^(1/4)) with n = 3 and a/R = 1/√2 gives κ ≈ 0.694 ≈ 1/√2. In nuclear first-principles, κ = 1/√2 is used consistently (F11, F12, D-01).

---

### Formula F12: Proton magnetic moment

**Statement:** μ_p = e c R/(2√2); uses κ = 1/√2 (not κ = 1). **Derivation:** Magnetic moment from circulating current at R with v = cκ; μ ∝ e v R; κ = 1/√2 gives 2√2 in denominator. **Why it matters:** Proton magnetic moment is geometric prediction from trefoil radius and κ. **CRITICAL:** The formula uses κ = 1/√2, not κ = 1. **Checks:** CODATA μ_p; 09_CANONICAL §9; B2, B5.

---

### Physical meaning and summary

**Why a vortex knot?** In SDT, matter displaces the spation medium. The trefoil is the simplest nontrivial knot; winding numbers n = 3, m = 2 are fixed by topology. **Link to hydrogen and solar:** k_p² = 5 α⁻¹ ties proton to hydrogen (137); k_⊙ = k_p² ties proton to Sun (686). **Summary:** n = 3, m = 2; Δ_topo = 5; k_p² = 5 α⁻¹ ≈ 685.18; κ ≈ 0.694 ≈ 1/√2; F4, F12. **Cross-references:** Ch 4, 6, 7, 10. Sources: Part I §1.3; Part III F4, F12; 09_CANONICAL §5.

---

## Chapter 6: Hydrogen System and Atomic Benchmarks

### Context and scope

Book I established the geometric foundation (occlusion, master orbital equation, redshift–displacement identity, trefoil topology). The hydrogen atom is the first system where SDT can be tested quantitatively: one proton, one electron, and the same velocity field and c-boundary that apply at stellar and cosmological scales. This chapter presents the **hydrogen system** in full and certifies three atomic benchmarks: **B2** (Koppa anchor: Ϟ_H = 137.036, no empirical fitting), **B3** (centripetal force F = m_e v²/a₀ matches the measured electromagnetic force to four significant figures), and **B4** (hydrogen spectrum—energy levels, Lyman series, ionisation—from the Ϟ framework). A brief note on the neutron as a composite (p⁺ + e⁻) (Part I §2.1) is included to connect atomic and nuclear scales. The takeaway is that the “magic number” 137.036 and the hydrogen spectrum are not separate quantum rules but consequences of the same geometric engine (Chapters 2–5).

**Source mapping:** Part II B2, B3, B4; Part I §2.1 (neutron as p+e) brief; 09_CANONICAL §4, §6.

---

### The hydrogen setup: one proton, one electron

In SDT the hydrogen atom is a two-body system in the spation medium. The proton is the displacement source (trefoil vortex; Chapter 5); the electron orbits in the resulting velocity field. The master equation **v² = c² R_c/r** holds, with R_c the c-boundary for the proton–electron system. The orbital radius at which v = c defines r_c; the physical “surface” for the electron is the Bohr radius a₀, where the ground-state orbital velocity is v_e. So **Ϟ_H = c/v_e** is the displacement parameter for hydrogen. No separate “Coulomb law” is postulated; the force that holds the electron in orbit is the pressure-gradient force from occlusion (Chapter 2), and its magnitude is exactly that required for circular motion: **F = m_e v²/a₀** (Benchmark B3).

**Variables (hydrogen):**
- **a₀:** Bohr radius ≈ 5.292×10⁻¹¹ m (CODATA).
- **v_e (or v_1):** Ground-state electron orbital speed ≈ 2.188×10⁶ m/s.
- **r_c:** c-boundary radius for the electron orbit; at r = r_c, v = c.
- **Ϟ_H (or k_H):** Ϟ_H = c/v_e ≈ 137.036; dimensionless.
- **E_n:** Energy of level n (eV or J); E_n ∝ −1/n² in the Ϟ framework.

The c-boundary rule gives r_c = R_phys/Ϟ². For hydrogen the “surface” of the orbit is at a₀, so effectively r_c = a₀/Ϟ_H² in the sense that the orbit at a₀ has velocity v_e = c/Ϟ_H, and the radius at which v = c is r_c = a₀ Ϟ_H² (counting from the same scaling). The exact relation used in the treatise is: at r = a₀, v = v_e; Ϟ_H = c/v_e; and the same master equation and Ϟ(r) = √(r/r_c) give the higher levels (B4).

---

### Benchmark B2: Koppa Anchor — full certification

**What is certified:** The unit anchor Ϟ = 1 (or k = 1) at the c-boundary; hydrogen Ϟ_H = c/v_electron = 137.036 from observed velocity; no empirical fitting; the fine-structure constant emerges as a geometric ratio.

**Formulas (certified):**
- **Ϟ ≡ c/v_surface** (or k = c/v_surface). At r = r_c: **Ϟ = 1.**
- **Ϟ_H = c/v_electron = 2.99792458×10⁸ / 2.188×10⁶ ≈ 137.036.**

**Derivation / reasoning.** (1) By definition, Ϟ is the ratio of c to the orbital (or surface) velocity. (2) The ground-state electron speed v_e is measured from spectroscopy (Rydberg constant, a₀, and v_e = ℏ/(m_e a₀) or equivalently from energy and radius). (3) So Ϟ_H = c/v_e is a direct calculation from CODATA values; no free parameter is fitted. (4) The result 137.036 matches the inverse fine-structure constant α⁻¹ to within experimental precision. (5) Therefore the fine-structure “constant” is not a coupling constant inserted by hand; it is the geometric ratio of c to the measured ground-state electron speed.

**Commentary.** B2 is the anchor for all larger systems. The c-boundary is the radius at which orbital velocity equals c. Counting outward in units of that radius gives the hydrogen “magic number” 137.036—the fine-structure inverse. One body (the proton) and one orbit (Bohr) fix the scale for all larger systems via k_solar = k_p² (Chapter 4) and z·k² = 1. If B2 were false (e.g. if Ϟ_H differed from α⁻¹ after using the same v_e and c), the link between atomic and stellar scales would break. No such discrepancy is observed.

**Experimental check:** v_e and a₀ from spectroscopy; Ϟ_H matches α⁻¹ to CODATA. **Status: CERTIFIED.**

---

### Benchmark B3: Centripetal Force — full certification

**What is certified:** The centripetal force required to hold the electron in the Bohr orbit, F = m_e v²/a₀, matches the tabulated electromagnetic force to four significant figures. No separate “force law” is assumed; force emerges from the orbital geometry.

**Formula:** **F = m_e v²/a₀.**

**Step-by-step calculation.** With m_e = 9.109×10⁻³¹ kg, v = 2.188×10⁶ m/s, a₀ = 5.292×10⁻¹¹ m:
- Centripetal force F_c = m_e v²/a₀ = (9.109×10⁻³¹)(2.188×10⁶)²/(5.292×10⁻¹¹) N ≈ 8.238×10⁻⁸ N.
- CODATA / standard electromagnetic force between proton and electron at separation a₀: F_em ≈ 8.239×10⁻⁸ N.
- Agreement to four significant figures.

**Verbal form:** The force required by circular motion at the observed speed and radius equals the measured electromagnetic force between the proton and the electron at the Bohr radius.

**Commentary.** In SDT, the force that holds the electron in orbit is the pressure-gradient force from occlusion (Chapter 2). B3 shows that the magnitude required by circular motion at the observed v and a₀ is exactly the magnitude measured between proton and electron. So “electromagnetism” at the Bohr scale is geometrically consistent with a single velocity field and occlusion. No second force law or coupling constant is needed to match the number. The centripetal formula is the same as in classical mechanics; the physical interpretation is that the pressure gradient supplies that force.

**Experimental check:** Agreement to 4 sig. fig. **Status: CERTIFIED.**

---

### Benchmark B4: Hydrogen Spectrum — full certification

**What is certified:** All hydrogen energy levels and Lyman wavelengths derive from the Ϟ framework (Ϟ_n ∝ n, r_n ∝ n², v_n ∝ 1/n, E_n ∝ −1/n²). Ionisation 13.606 eV; series limit 91.2 nm.

**Formulas and scaling.** In the Ϟ picture, the nth orbit has:
- **Ϟ_n ∝ n** (velocity ratio scales with principal quantum number in the same geometric scheme).
- **r_n ∝ n²** (radius scales as n²).
- **v_n ∝ 1/n** (orbital velocity v_n = c/Ϟ_n ∝ 1/n).
- **E_n ∝ −1/n²** (energy scales as −1/n², as in the Rydberg formula).

**Ionisation energy.** Ground state to continuum: E_ion = 13.606 eV (CODATA). In SDT this is the work required to move the electron from a₀ to infinity in the same pressure field; it matches the Rydberg-derived value.

**Lyman series (n → 1).** Wavelengths λ(n→1) for transitions to the ground state. Series limit (n → ∞) ≈ 91.2 nm. The Lyman α (2→1), β (3→1), γ (4→1), etc., lines match observed hydrogen spectroscopy. The formula E_n (eV) and λ(n→1) (nm) follow from the same Ϟ_n, r_n, v_n relations and the identity Ϟ = 1 at r_c.

**Commentary.** The spectrum is not a separate “quantum” rule; it is the set of allowed orbits under the same master equation and Ϟ = 1 at r_c. B4 certifies that the same geometric engine that gives 137.036 (B2) and centripetal force (B3) also gives the full Rydberg progression. So hydrogen is a single consistent system: one velocity field, one c-boundary, one Ϟ definition, and the observed spectrum.

**Experimental check:** Lyman α, β, γ, etc.; ionisation energy; series limit. **Status: CERTIFIED.**

---

### Neutron as composite (p⁺ + e⁻): brief note

Part I §2.1 states the neutron as a composite: **n = p⁺ + e⁻_internal.** An electron is bound at a trefoil node; r_node = R − a ≈ 0.25 fm. Binding arises from magnetic compression and external spation pressure P_∞. This is not an atomic benchmark but a bridge to nuclear structure (Chapter 10). It shows that the same “electron in a potential” picture that gives hydrogen can be extended to the nucleon scale: the neutron is a proton with an internal electron at the node, and the deuteron (two protons sharing one electron) is the next step (D-01, Chapter 10). No separate “strong force” is required for this picture; geometry and pressure suffice for the binding narrative.

---

### Summary of formulas and checks

- **B2:** Ϟ_H = c/v_e ≈ 137.036; Ϟ = 1 at r_c. Fine structure emerges as geometric ratio; no empirical fitting. **CERTIFIED.**
- **B3:** F = m_e v²/a₀ ≈ 8.238×10⁻⁸ N; matches electromagnetic force to 4 sig. fig. **CERTIFIED.**
- **B4:** E_n ∝ −1/n²; Lyman series and ionisation 13.606 eV from Ϟ framework. **CERTIFIED.**

**Why the hydrogen system matters.** Hydrogen is the only atom for which the “orbital” picture can be compared directly to spectroscopy and force without many-body complications. B2, B3, and B4 together show that one number (Ϟ_H = 137.036), one force formula (F = m_e v²/a₀), and one scaling (E_n ∝ −1/n²) suffice. That same Ϟ and the trefoil (Chapter 5) give k_p and hence k_⊙ = k_p² (Chapter 4). So the hydrogen benchmarks are not isolated checks; they are the anchor from which stellar and cosmological scales are fixed.

**Worked numbers (reference).** Lyman α (2→1): λ ≈ 121.57 nm; Lyman β (3→1): λ ≈ 102.57 nm; Lyman γ (4→1): λ ≈ 97.25 nm. Ionisation 13.606 eV corresponds to λ_limit ≈ 91.18 nm. These follow from E_n = −13.606/n² eV and ΔE = E_n − E_1 with λ = hc/ΔE. In the Ϟ framework, the same energies come from the orbital radii and velocities at each n.

**Cross-references.** B2 links to F2, F3 (z·k² = 1, k_solar = k_p²); B3 links to F10 (acceleration), Rule 2; B4 links to F1 (master equation), Ϟ(r) = √(r/r_c). Falsification vector (Part I §4.2): Lamb shift; orbital vs nuclear length scale d_orbital ≈ 3.36 α⁻² d_nuclear remains a test of the framework.

Chapter 7 extends the same velocity field and k to the solar and stellar systems (B5–B8).

---

*Sources: Part II B2, B3, B4; Part I §2.1; 09_CANONICAL §4, §6.*



## Chapter 7: Solar and Stellar Systems

### Context and scope

Chapters 3 and 4 established the master orbital equation v² = c² R_c/r, the redshift–displacement identity z·k² = 1, and the proton–solar bridge k_⊙ = k_p² ≈ 686. This chapter applies that framework to the Sun, the Solar System, Jupiter’s moons, and exoplanetary systems. Four benchmarks (B5–B8) certify that one number—the solar koppa k_⊙—is fixed by three independent routes (orbital dynamics, surface rotation, and gravitational redshift), and that every planetary and satellite orbit, and a wide sample of exoplanets, then follow from the same v(r) with no gravitational constant G and no mass M.

The chapter is organised as follows. We first state Benchmark B5 in full: the three routes to solar Ϟ (orbital, rotation, spectral) and the verification z×k² = 1. We then give the solar c-boundary and Formula F8 (rotation coupling v_rot = π v_orb²/c), with derivation and commentary. Next we present B6 (Solar System orbits) and B7 (Jovian system) with compact tables and maximum errors, then B8 (exoplanetary validation) with representative systems and typical versus max error. We close with a short summary of what “stellar k” means for other stars and how to use the same formulas there. All content is drawn from Part II B5–B8, Part III F8, and 09_CANONICAL §7; no new physics is introduced.

**Notation.** k_⊙ (or Ϟ_⊙) is the solar surface velocity ratio c/v_surface. R_☉ is the Sun’s physical radius; r_c(☉) = R_☉/k_⊙² is the solar c-boundary (~1.48 km). For other stars we use k_star, R_star, r_c(star).

---

### Benchmark B5: Solar Ϟ (Three Routes) — CERTIFIED ✓

**What is certified.** The solar k (or Ϟ) value is determined to high precision (σ ≈ 0.03%) by three independent methods: (1) orbital dynamics at 1 AU, (2) surface rotation, and (3) gravitational redshift z. The identity z×Ϟ² = 1 is verified for the Sun.

**Route 1 — Orbital.** At 1 AU the Earth’s orbital velocity is v_orb ≈ 29.78 km/s. From the master equation v(r) = (c/k_⊙)√(R_☉/r) we have k_⊙ = (c/v_orb)√(R_☉/r). With R_☉ ≈ 6.96×10⁸ m, r = 1.496×10¹¹ m, c = 2.998×10⁸ m/s, and v_orb = 2.978×10⁴ m/s, k_⊙ ≈ 686.5. So orbital dynamics at 1 AU fix k_⊙ to within the precision of the ephemerides.

**Route 2 — Rotation.** The Sun’s surface rotation velocity v_rot is linked to the orbital velocity at 1 AU by the geometric coupling (Formula F8):

**v_rot = π v_orb² / c**

With v_orb = 436.7 km/s (conventional 1 AU reference for this relation), v_rot ≈ π × (4.367×10⁵)² / (2.998×10⁸) m/s ≈ 2.00×10³ m/s. The rotation period is T_rot = 2π R_☉/v_rot ≈ 25.32 days (siderial). From Rule 7 (rotation route), k_⊙ = √(πc/v_rot) ≈ 686.6. Observed siderial period is ~25.4 days; agreement is within measurement uncertainty.

**Route 3 — Spectral.** Gravitational redshift at the solar surface gives z_solar ≈ 2.12×10⁻⁶. From z·k² = 1 we have k_⊙ = 1/√z ≈ 1/√(2.12×10⁻⁶) ≈ 686.9. So spectroscopy provides a third, independent determination of k_⊙.

**Verification of z×k² = 1.** Using the orbital/rotation value k_⊙ ≈ 686.6, k_⊙² ≈ 471,556. Then z_solar × k_⊙² ≈ 2.12×10⁻⁶ × 471,556 ≈ 1.00. The identity is satisfied to within the combined errors of z and k. B5 certifies that the Sun is not an exception: the same geometric lock between redshift and dynamics that holds for hydrogen (Ϟ_H = 137.036) holds for the star. No free parameter is introduced for the Sun; the only inputs are measured quantities (v_orb, v_rot, z, R_☉, r).

**Commentary.** B5 is the bridge from atomic to stellar scales. One number (k_⊙ ≈ 686.6) is fixed by dynamics, rotation, and redshift. That number equals 5×137 (trefoil factor Δ_topo = 5 times fine-structure inverse α⁻¹), so the proton and the Sun are locked by topology and z·k² = 1. There is no free “solar constant”; k_⊙ is predicted from k_p² = 5 α⁻¹ (Chapter 5).

---

### Solar c-boundary and Formula F8 (rotation coupling)

**Solar c-boundary.** The c-boundary radius for the Sun is r_c(☉) = R_☉/k_⊙². With R_☉ ≈ 6.96×10⁸ m and k_⊙ ≈ 686.6, r_c(☉) ≈ 1.476×10³ m ≈ 1.48 km. So the radius at which the orbital velocity would equal c is about 1.48 km—far inside the visible surface. Every planetary orbit responds to this single length scale: v(r) = c√(r_c(☉)/r).

**Formula F8: Solar rotation coupling.** The Sun’s surface rotation velocity is tied to the orbital velocity at 1 AU by:

**v_rot = π v_orb² / c**

**Derivation.** (1) Geometric flux coupling between the orbit (at 1 AU) and the spin of the star: the same displacement field that sets v_orb also couples to rotation. (2) Dimensionally, v_orb²/c has units of velocity; the factor π arises from the geometry of the coupling (circumference and flux integral). (3) Then T_rot = 2π R_☉/v_rot with R_☉ and v_rot from the formula. Inverting: v_rot = 2π R_☉/T_rot. The link v_rot = π v_orb²/c can be viewed as the condition that the stellar spin period is set by the same k that gives the 1 AU orbital speed—so k_⊙ = √(πc/v_rot) recovers the same value as k_⊙ = (c/v_orb)√(R_☉/r) when both are consistent.

**Why it matters.** Solar rotation is not an arbitrary initial condition; it is locked to the same k and orbital velocity that give B5 and B6. So F8 provides the third independent route to k_⊙ (Rule 7: Ϟ = √(πc/v_rot)). B5 certifies; observed siderial period ~25.4 days matches the predicted ~25.32 days within error. Any theory that treated rotation as independent would need an extra free parameter; in SDT, rotation and orbit share one geometric constant.

---

### Benchmark B6: Solar System Orbits — CERTIFIED ✓

**What is certified.** Every planetary orbital velocity in the Solar System is predicted by v(r) = (c/k_⊙)√(R_☉/r) with k_⊙ ≈ 686.7 and r_c(☉) = R_☉/k_⊙² ≈ 1.48 km. Maximum error is less than 0.41% (Saturn).

**Formula.** v(r) = c √(r_c/r) with r_c = 1,476 m. Equivalently, v(r) = (c/k_⊙)√(R_☉/r). No G, no M_☉; only the solar c-boundary and the distance r. Dimensional check: [c√(r_c/r)] = (m/s)·√(m/m) = m/s.

**Worked table (representative).** Using r_c(☉) ≈ 1.476×10³ m and c = 2.998×10⁸ m/s:

| Planet   | r (m) approx.   | v_pred (km/s) | v_obs (km/s) | Error (%) |
|----------|------------------|---------------|--------------|-----------|
| Mercury  | 5.79×10¹⁰        | 47.87         | 47.87        | 0.00      |
| Venus    | 1.08×10¹¹        | 35.02         | 35.02        | 0.00      |
| Earth    | 1.496×10¹¹       | 29.78         | 29.78        | 0.00      |
| Mars     | 2.28×10¹¹        | 24.13         | 24.08        | ~0.2      |
| Jupiter  | 7.78×10¹¹        | 13.07         | 13.06        | ~0.1      |
| Saturn   | 1.43×10¹²        | 9.64          | 9.68         | ~0.41     |
| Uranus   | 2.87×10¹²        | 6.80          | 6.80         | 0.00      |
| Neptune  | 4.52×10¹²        | 5.43          | 5.43         | 0.00      |

(Values rounded; JPL ephemerides are the reference. Max error cited in dataset: Saturn < 0.41%.)

**Commentary.** B6 shows that “Newtonian” planetary orbits are the low-velocity limit of the same displacement field that gives hydrogen and redshift. One length scale (1.48 km) and the master equation suffice for all eight planets. The small residual errors (e.g. Saturn ~0.41%) are within ephemeris and measurement uncertainty; they do not require dark matter or modified gravity. Falsification would be a systematic deviation (e.g. all outer planets too fast or too slow) that could not be explained by improved data or multi-body perturbations.

---

### Benchmark B7: Jovian System — CERTIFIED ✓

**What is certified.** The Galilean satellites (Io, Europa, Ganymede, Callisto) obey the same v(r) = (c/k)√(R/r) with Jupiter’s k_J and R_J. Maximum error 0.00%.

**Formula.** For each satellite at orbital radius r, v(r) = (c/k_J)√(R_J/r), where R_J is Jupiter’s physical radius and k_J = c/v_surface(Jupiter). Equivalently v(r) = c√(r_c(J)/r) with r_c(J) = R_J/k_J².

**Commentary.** Jupiter acts as a second “Sun” in the same framework. B7 extends scale invariance from star–planet to planet–moon: same equation, different R and k. JPL satellite orbits confirm; max error is 0.00% for the four Galilean moons. Physically, the displacement field of Jupiter is determined by its physical radius and surface velocity (hence k_J); the moons orbit in that field exactly as planets orbit in the solar field. No separate “moon law” is needed.

---

### Benchmark B8: Exoplanetary Validation — CERTIFIED ✓

**What is certified.** Stellar k is derived from stellar parameters (rotation, spectral z, or planetary orbit); then v_planet = (c/k)√(R_star/r). Validated across many systems. Maximum error ≈ 2.02%; typical error ≈ 1%.

**Procedure.** (1) Obtain stellar k from one of Rule 7’s three routes: orbital (if one planet’s v and r are known), rotation (k = √(πc/v_rot)), or spectral (k = 1/√z). (2) Compute predicted orbital velocity for other planets or for the same planet at different epochs: v_planet = (c/k)√(R_star/r). (3) Compare to radial-velocity or transit-derived values.

**Representative systems (from dataset).** 51 Pegasi, HD 209458, GJ 876, Tau Ceti, Kepler-186, HR 8799, Kepler-62. For each, stellar R_star and k (from rotation, spectral z, or primary planet) yield predicted v_planet; comparison with NASA Exoplanet Archive and radial velocity/transit data gives typical agreement ~1%, max ~2.02%.

**Commentary.** Exoplanets are not exceptions; they follow the same k and v(r). B8 generalises B5–B7 to arbitrary stars and confirms that z·k² = 1 and the master equation apply wherever a compact source and orbits are observed. The slightly larger typical error (~1%) and max (~2.02%) compared to the Solar System reflect uncertainties in stellar radius, rotation, and radial-velocity or transit-derived planet masses/semi-major axes—not a breakdown of the velocity law. As stellar and orbital data improve, SDT predicts that residuals will shrink toward the level of B6 and B7.

---

### Stellar k and other stars

For any star, the same logic applies. **Stellar Ϟ (or k)** can be obtained from:

- **Orbital:** If at least one planetary orbital velocity v_orb and semi-major axis r are known, k_star = (c/v_orb)√(R_star/r).
- **Rotation:** k_star = √(πc/v_rot) from the star’s surface rotation velocity (or period and radius).
- **Spectral:** k_star = 1/√z from the star’s gravitational redshift.

Then r_c(star) = R_star/k_star² and v(r) = c√(r_c/r) for any orbit around that star. 09_CANONICAL §7 summarises: solar c-boundary r_c(☉) = R_☉/Ϟ²; planetary v from Ϟ_☉ and r_c; stellar Ϟ from orbital/rotation/spectral (Rule 7); B5–B8 certify.

---

### Worked example: 51 Pegasi b

As a second worked example, consider the hot Jupiter 51 Pegasi b. The star 51 Pegasi has measured parameters (radius, rotation or spectral redshift, and the planet’s orbital period and semi-major axis from radial velocity). From the planet’s period P and semi-major axis a, the orbital velocity is v_planet ≈ 2πa/P. SDT predicts v_planet = (c/k_star)√(R_star/a), so k_star = (c/v_planet)√(R_star/a). Alternatively, if k_star is first determined from the star’s rotation or redshift, then v_planet is predicted and compared to 2πa/P. B8 reports validation across this and other systems (e.g. HD 209458, GJ 876, Tau Ceti, Kepler-186, HR 8799, Kepler-62) with typical error ~1% and max error ≈ 2.02%. The same formula v(r) = c√(r_c/r) applies; only the stellar c-boundary r_c(star) = R_star/k_star² changes from system to system.

---

### Summary and cross-references

- **B5:** Three routes to k_⊙ ≈ 686.6 (orbital, rotation, spectral); z×k² = 1 verified. Bridge from atomic to stellar.
- **F8:** v_rot = π v_orb²/c; third route to k_⊙; T_rot ≈ 25.32 days (obs. ~25.4 days).
- **B6:** All planetary orbital velocities from v(r) = c√(r_c/r), r_c(☉) ≈ 1.48 km; max error < 0.41%.
- **B7:** Galilean satellites obey same v(r) with Jupiter’s k_J, R_J; max error 0.00%.
- **B8:** Exoplanets: stellar k from rotation/spectral/orbital; v_planet = (c/k)√(R_star/r); typical error ~1%, max ≈ 2.02%.

**Cross-references.** Chapter 3 (master equation, F1); Chapter 4 (z·k² = 1, F2, F3); Chapter 5 (k_⊙ = k_p², trefoil); Chapter 6 (hydrogen, Ϟ_H); Chapter 12 (benchmark index). Sources: Part II B5–B8; Part III F8; 09_CANONICAL §7.

---

*Word count: ~2,750 (target 2,680–6,064).*



## Chapter 8: Ten Rules and Paradox Resolution

### Context and scope

Spatial Displacement Theory (SDT) is not a collection of ad hoc formulas. It is a single framework derived from four primitives (matter, space, movement, now), Euclidean geometry, and hydrostatic equilibrium in the spation medium. That framework is codified in **Ten Rules**—the “constitution” of SDT. Every benchmark (B1–B8, B10–B12), every formula (F1–F17), and the implementation logic (calculation order, falsification vectors) trace back to these rules. No empirical constants are introduced; the same Ϟ (or k) structure applies across some 53 orders of magnitude in scale.

This chapter (1) states **Benchmark B9**: the full Ten Rules with a short derivation or comment per rule; (2) states **Benchmark B10**: six Standard Model paradoxes and their SDT resolution without new postulates; (3) explains why the Ten Rules function as a single constitution and how they support validation and falsification. The takeaway is that B9 and B10 certify the framework as self-consistent and conceptually coherent: the same geometric picture that yields orbits, redshift, and hydrogen also addresses hierarchy, vacuum, dark matter, and dark energy in a unified way.

---

### Benchmark B9: Ten Rules codified — full certification

**What is certified:** The full SDT framework is summarised in Ten Rules (occlusion, acceleration, Ϟ definition, master equation, surface and escape velocity, Ϟ from orbital/spectral/rotation, superposition, c-boundary, scale invariance). All are derived from primitives; no empirical constants are introduced; the set is self-consistent and scale-invariant.

**Status:** CERTIFIED.

Below, each rule is given with its exact statement (or formula) and a short derivation or comment tying it to the preceding chapters.

---

#### Rule 1: The Occlusion Principle

**Statement:** Exact solid angle \(\Omega(r) = 2\pi\left(1 - \sqrt{1 - R^2/r^2}\right)\). Far field (\(r \gg R\)): \(O(r) = R^2/(4r^2)\).

**Comment:** The pressure deficit that SDT identifies with “gravity” is proportional to the fraction of the sky occluded by the displacing body. That fraction is pure Euclidean geometry—no G, no M. Rule 1 is the foundation; B1 certifies it. See Chapter 2.

---

#### Rule 2: Pressure-Difference Acceleration

**Statement:** \(a(r) = c^2 R/(\varkappa^2 r^2)\). Equivalently \(a(r) = c^2 R_c/r^2\) with \(R_c = R/\varkappa^2\).

**Derivation:** From the master equation \(v^2 = c^2 R_c/r\), centripetal acceleration is \(a = v^2/r = c^2 R_c/r^2\). The pressure gradient in the spation medium is \(dP/dr \propto -\rho_s v^2/r\), so the radial force on a test body scales as \(c^2 R_c/r^2\). Rule 2 is F10; see Chapter 3.

---

#### Rule 3: Ϟ-Parameter Definition

**Statement:** \(\varkappa \equiv c/v_{\text{surface}}\), where \(v_{\text{surface}}\) is the orbital velocity at the body’s physical surface.

**Comment:** Ϟ (or k) is dimensionless. At the c-boundary, by definition \(\varkappa = 1\). Rule 3 fixes the meaning of Ϟ used in Rules 2, 4, 5, 6, 7, 9. See Chapters 3 and 4.

---

#### Rule 4: Master Orbital Equation

**Statement:** \(v(r) = (c/\varkappa)\sqrt{R/r}\). Equivalently \(v(r) = c\sqrt{r_c/r}\) with \(r_c = R/\varkappa^2\).

**Derivation:** Hydrostatic equilibrium and the c-boundary condition \(v = c\) at \(r = r_c\) yield \(v^2 = c^2 R_c/r\). With \(R_c = R/\varkappa^2\) and \(\varkappa = c/v_{\text{surface}}\), this is F1. See Chapter 3.

---

#### Rule 5: Surface Velocity Rule

**Statement:** \(v_{\text{surface}} = c/\varkappa\).

**Comment:** This is the definition of Ϟ applied at \(r = R_{\text{phys}}\). So at the surface, the orbital speed is exactly \(c/\varkappa\). See Chapter 3.

---

#### Rule 6: Escape Velocity Rule

**Statement:** \(v_{\text{escape}} = \sqrt{2} \times c/\varkappa\).

**Derivation:** Work to escape from \(R_{\text{phys}}\) to infinity: \(\int_{R_{\text{phys}}}^\infty a(r)\,dr\) with \(a(r) = c^2 R_c/r^2\) gives \((1/2)v_{\text{escape}}^2 = c^2/\varkappa^2\), so \(v_{\text{escape}} = \sqrt{2}\,c/\varkappa\). Same as Newtonian \(v_{\text{esc}} = \sqrt{2GM/R}\) when \(GM = c^2 R/\varkappa^2\). F16; see Chapter 3.

---

#### Rule 7: Ϟ-Value Calculation (three routes)

**Statement:** Ϟ can be obtained by: (1) **Orbital:** \(\varkappa = c/\sqrt{\beta/R}\), where \(\beta\) is the orbital parameter (\(v^2 = \beta/r\), \(r_c = \beta/c^2\)). (2) **Spectral:** \(\varkappa = 1/\sqrt{z}\), where \(z\) is gravitational redshift. (3) **Rotation:** \(\varkappa = \sqrt{\pi c/v_{\text{rot}}}\).

**Comment:** All three must give the same Ϟ for a given body. The spectral route is the identity \(z \cdot \varkappa^2 = 1\) (F2). B5 certifies the three routes for the Sun. See Chapter 4.

---

#### Rule 8: Multi-Body Superposition

**Statement:** Accelerations superpose vectorially; each body contributes its geometric occlusion share.

**Comment:** In a multi-body system, the pressure deficit (and hence acceleration) at a point is the sum of the contributions from each displacing body. No new law; occlusion and the master equation apply per body, and the medium responds to the total deficit. See Chapters 2 and 3.

---

#### Rule 9: c-Boundary Rule

**Statement:** \(r_c = R/\varkappa^2\); at \(r = r_c\), \(\varkappa(r_c) = 1\) (orbital velocity = c).

**Comment:** The c-boundary is the radius at which the velocity field reaches c. It is a geometric length scale, not a physical surface. \(\varkappa(r) = \sqrt{r/r_c}\) (F17) so \(\varkappa = 1\) at \(r = r_c\). See Chapter 3.

---

#### Rule 10: Scale Invariance

**Statement:** The same equations and the same Ϟ structure apply across approximately 53 orders of magnitude (nuclear to cosmological).

**Comment:** Hydrogen (Ϟ_H = 137), proton (trefoil), Sun (Ϟ_⊙ ≈ 686), planets, exoplanets, and the CMB boundary all use the same master equation, \(z \cdot \varkappa^2 = 1\), and occlusion. Only R, r, and the body’s Ϟ (or κ at nuclear scale) change. B2–B8, B12, D-01 certify this. See Chapters 3, 4, 6, 7, 11.

---

### The Ten Rules as constitution

B9 certifies that the Ten Rules are the source of truth for implementation. The calculation order (Chapter 1) is: define scale; then \(\varkappa = c/v_{\text{surface}}\) or \(\varkappa = 1/\sqrt{z}\); then \(r_c = R/\varkappa^2\); then \(v(r) = (c/\varkappa)\sqrt{R/r}\). Each step is a direct application of Rules 3, 7, 9, and 4. Falsification vectors (atomic: Lamb shift; galactic: rotation curves; nuclear: ³He vs ³H) are chosen because they probe the same framework at different scales. So when validating or falsifying SDT, one should reference Rules 1–10 as the canonical statement of the theory; benchmarks and formulas are consequences of these rules.

---

### Benchmark B10: Paradox resolution — full certification

**What is certified:** Six Standard Model paradoxes (hierarchy problem, vacuum catastrophe, wave–particle duality, measurement problem, dark matter, dark energy) are addressed within SDT without new postulates: hierarchy from geometry, vacuum from contact pressure, dark matter from screening/rotation (e.g. flat curves from \(v = c\sqrt{R_{\text{occ}}/r}\)), and related resolutions.

**Commentary:** B10 is conceptual rather than a single formula. It certifies that the same geometric picture that gives B1–B9 and B11–B12 also provides a coherent story for why the universe does not require fine-tuned constants or undetected matter/energy in the way the Standard Model does.

**Status:** CERTIFIED.

Below, each paradox is stated briefly and the SDT resolution is summarised.

---

#### 1. Hierarchy problem

**Paradox:** The Standard Model requires extreme fine-tuning between the electroweak scale and the Planck scale (or the Higgs mass and quantum corrections). The ratio of scales is often cited as a “naturalness” problem.

**SDT resolution:** In SDT there is no separate hierarchy of “fundamental” coupling constants. Mass and force scales emerge from geometry: the c-boundary \(R_c = R/\varkappa^2\), the trefoil factor 5, and the fine-structure inverse 137. The proton and the Sun are linked by \(k_\odot = k_p^2\) (Chapter 4); no arbitrary large ratio is inserted by hand. So the apparent “hierarchy” is a consequence of displacement geometry and topology, not of fine-tuned constants.

---

#### 2. Vacuum catastrophe

**Paradox:** Quantum field theory predicts a vacuum energy density that is many orders of magnitude larger than the observed cosmological constant (or dark energy density). The discrepancy is often cited as the “worst prediction in physics.”

**SDT resolution:** In SDT, the vacuum is not a quantum field ground state with infinite zero-point energy. The large-scale pressure field is set by the cosmic boundary (CMB, 48 Gyr radiator) and the spation medium. The “vacuum” energy that matters for dynamics is the contact pressure \(P_\infty\) and the pressure gradient that gives orbits and redshift. There is no separate cosmological constant to fine-tune; the CMB temperature and redshift are tied to the same pressure field (B12, Chapter 11). So the “catastrophe” is sidestepped by not identifying vacuum energy with the QFT zero-point sum in the first place.

---

#### 3. Wave–particle duality

**Paradox:** In quantum mechanics, light and matter exhibit both wave-like and particle-like behaviour, and the transition between them is often presented as paradoxical or as requiring “complementarity” without a single underlying picture.

**SDT resolution:** SDT does not replace quantum mechanics but offers a consistent kinematic and geometric layer. Propagation in the spation medium (waves) and localised displacement (particles) are two aspects of the same medium: waves are disturbances in the medium; “particles” are stable displacement structures (e.g. trefoil proton). So duality is not two incompatible natures but two views of the same underlying displacement and pressure field. The framework does not add new postulates; it reframes the ontology (primitives: matter, space, movement, now) so that wave and particle descriptions refer to the same substrate.

---

#### 4. Measurement problem

**Paradox:** In standard quantum mechanics, the “collapse” of the wave function upon measurement has no clear dynamical mechanism and leads to debates about the role of the observer and the definition of measurement.

**SDT resolution:** SDT does not provide a full quantum measurement theory but constrains the ontology: the primitives are matter, space, movement, and now. “Measurement” is an interaction in the same spation medium; there is no separate “classical” realm. So the framework points toward a single, continuous medium in which both “system” and “apparatus” are displacement structures. Resolving the measurement problem in detail would require a fuller quantum formulation within SDT; B10 certifies that the geometric picture is consistent with seeking such a formulation without introducing observer-dependent collapse by fiat.

---

#### 5. Dark matter

**Paradox:** Galactic rotation curves and cluster dynamics suggest more “mass” than is visible. The Standard Model invokes dark matter as an unknown component.

**SDT resolution:** In SDT, orbital velocity is set by \(v(r) = c\sqrt{r_c/r}\) (or \(v = c\sqrt{R_{\text{occ}}/r}\) when an effective occlusion radius \(R_{\text{occ}}\) is used). Flat or rising rotation curves are explained by the distribution of displacing mass and by screening: the effective \(R_{\text{occ}}\) can scale with r in a disk or halo so that \(v(r)\) matches observations without invoking invisible matter. So “dark matter” is reframed as a question of geometry and occlusion (and, where relevant, the screening factor ξ; S-01). The same master equation and Rules 1–4 apply; no new particle is required. See Chapter 3 (scale invariance) and Chapter 12 (falsification: rotation curves).

---

#### 6. Dark energy

**Paradox:** The observed acceleration of the expansion of the universe is often attributed to dark energy or a cosmological constant.

**SDT resolution:** SDT uses a static Euclidean universe with a boundary at ~48 Gly (Chapter 11). The CMB is the boundary radiator; redshift is gravitational (climbing out of the pressure well), not Doppler from expansion. So there is no global expansion to accelerate; the “dark energy” phenomenon is not introduced as a separate component. If certain distance–redshift relations are reinterpreted within the static model (pressure field, z from boundary), the need for dark energy as an extra fluid or constant is removed. B12 certifies the CMB and redshift interpretation.

---

### Framework as single constitution

The Ten Rules (B9) and paradox resolutions (B10) together show that SDT is one constitution: one set of primitives, one geometry (occlusion), one dynamical equation (master equation), one identity (\(z \cdot \varkappa^2 = 1\)), and one scale-invariant structure. Implementation logic (calculation order, falsification vectors) references the rules; benchmarks certify consequences of the rules at different scales. Paradoxes are addressed by re-describing the same world in terms of displacement and pressure rather than by adding new particles or constants. So B9 and B10 are not optional “philosophy”—they are the certification that the framework is self-consistent and conceptually unified.

---

### Checks and cross-references

- **B1–B8, B11–B12:** Each benchmark is a consequence of the Ten Rules; see Chapters 2, 3, 4, 6, 7, 9, 11.
- **D-01, S-01:** Deuteron binding and screening factor also follow from the same framework (Chapters 10, 12).
- **Calculation order (4.1):** Rules 3, 7, 9, 4; see Chapter 1.
- **Falsification (4.2):** Lamb shift (atomic), rotation curves (galactic), ³He vs ³H (nuclear); see Chapter 1 and 12.
- **Formula index:** Rules 2, 4, 5, 6, 7, 9 correspond to F10, F1, F16, F2/F3/F8, F17; see Chapter 13.

---

### Summary

- **B9:** Ten Rules codified—occlusion (1), acceleration (2), Ϟ definition (3), master equation (4), surface velocity (5), escape velocity (6), three routes to Ϟ (7), superposition (8), c-boundary (9), scale invariance (10). All derived from primitives; no empirical constants; CERTIFIED.
- **B10:** Six paradoxes (hierarchy, vacuum catastrophe, wave–particle duality, measurement problem, dark matter, dark energy) addressed within SDT without new postulates; CERTIFIED.
- **Constitution:** Rules 1–10 are the source of truth; implementation and falsification reference them; B9 and B10 certify the framework as single and coherent.

---

*Sources: Part II B9, B10 (SDT_CORE_AXIOMS_AND_DATASET); 06_RAW_FORMULA_LIST Rules 1–10.*



## Chapter 9: Classical Tests of Gravitation

### Context and scope

SDT reproduces the same numerical predictions as GR for the four classical tests: light deflection, Shapiro delay, perihelion advance, and (where applicable) frame dragging. The interpretation is different: SDT attributes these effects to **refraction in the spation medium** (refractive index n(r) = 1 + 2R/(Ϟ²r)), not spacetime curvature. This chapter presents **Benchmark B11** (certification that light deflection, Shapiro, and perihelion are reproduced within error bars), **Formula F13** (Shapiro delay Δt = (4R/(Ϟ²c)) ln(4r₁r₂/b²)), and **Formula F14** (perihelion advance Δω = 6πR/(Ϟ²a(1−e²))).

**Source mapping:** Part II B11; Part III F13, F14; 09_CANONICAL §8.

---

### Refractive interpretation vs GR

In GR, light deflection, Shapiro delay, and perihelion advance arise from the Schwarzschild metric. In SDT, they arise from a radially varying refractive index n(r) = 1 + 2R/(Ϟ²r). The formulas have the same structure: Schwarzschild GM/c² is replaced by R/Ϟ². With R_☉ and Ϟ_⊙ ≈ 686, SDT and GR yield the same numbers. **B11 certifies:** all within error bars.

---

### Benchmark B11 and formulas

**B11:** Light deflection, Shapiro, perihelion (and frame dragging) reproduced from refractive gradient; no curved spacetime; CERTIFIED.

**F13 (Shapiro):** Δt = (4R/(Ϟ²c)) ln(4r₁r₂/b²). Refractive index n(r) = 1 + 2R/(Ϟ²r); integrated optical path gives extra time ∝ ∫ (n−1) dr; logarithm from 1/r. Same number as GR; B11 certifies; Cassini.

**F14 (Perihelion):** Δω = 6πR/(Ϟ²a(1−e²)). Non-Newtonian correction from pressure gradient; 6π from first-order perturbation. Mercury 43″/century; B11 certifies.

---

### Within error bars

Light deflection ~1.75″; Shapiro (Cassini) within ~0.002%; Mercury perihelion 43″/century. Both GR and SDT agree; B11 certifies. Refractive interpretation is consistent with classical tests.

**Cross-references:** Ch 2, 3, 7, 12. Sources: Part II B11; Part III F13, F14; 09_CANONICAL §8.

---

## Chapter 10: Nuclear Structure and Binding

### Context and scope

Chapters 5–6 linked the proton (trefoil) to hydrogen (Ϟ_H = 137.036) and the solar scale (k_⊙ = k_p²). At the nuclear scale the same displacement field operates with at the nucleon surface **v_surface = cκ** with **κ = 1/√2**; the nuclear form is v² = c²κ²(R/r) with κ = 1/√2. This chapter sets out **nuclear structure and binding** in SDT: the neutron as a composite (p⁺ + e⁻), the deuteron bond (two protons plus one shared electron or magnetic coupling), and the **pressure hierarchy** (P_∞, P_conf, ρ_s). It gives the full certification of **Benchmark D-01** (deuteron binding), **Formula F5** (p-p-e binding E_bind ≈ 3 k_e e²/D), and **Formula F11** (nuclear kinetic and confinement with κ = 1/√2). The takeaway is that nuclear “strong” effects are not a separate force but the same pressure and velocity field with κ = 1/√2 at the nucleon surface; deuteron binding is certified within ~2.5–3.1% from geometric/electromagnetic models.

**Source mapping:** Part I §2.1–2.3; Part II D-01; Part III F5, F11; 09_CANONICAL §9.

---

### Neutron composite and deuteron bond (Part I §2.1–2.2)

**Neutron composite (2.1).** The neutron is modelled as **n = p⁺ + e⁻_internal.** An electron is bound at a trefoil node; r_node = R − a ≈ 0.25 fm. Binding comes from magnetic compression and external spation pressure P_∞. So the neutron is not a fundamental particle but a proton with an internal electron at the node—consistent with the same “electron in a potential” picture used for hydrogen (Chapter 6) and for the deuteron.

**Deuteron bond (2.2).** The deuteron (²H) is the simplest bound nucleus. Two models are certified in D-01:
1. **Magnetic coupling:** μ_p, μ_N, separation give E_bind ≈ 2.15 MeV (error ~3.1%).
2. **Electron-mediated p–p–e (Coulomb geometry):** E_bind ≈ 3 k_e e²/D − V_pp; D ≈ 1.942 fm; result ~2.28 MeV (error ~2.5%). Measured value: 2.224 MeV.

**Geometric check.** Proton diameter d_p ≈ 1.68 fm; deuteron separation D ≈ 1.942 fm; gap D − d_p ≈ 0.26 fm, on the scale of the electron node (~0.25 fm). So the p-p-e picture is geometrically consistent: the shared electron sits in the gap between the two protons.

---

### Pressure hierarchy (Part I §2.3)

**P_∞ (cosmic pressure).** From the CMB: **P_∞ ≈ 1.39×10⁻¹⁴ Pa.** This is the ambient spation pressure at cosmological scale (radiation pressure of the boundary field).

**Stiffness ratio.** ρ_s c²/P_∞ ≈ 1.5×10⁴⁸. The medium is extremely stiff compared to the cosmic pressure; local displacement dominates.

**P_conf (confinement).** At the nuclear (QCD bag) scale: **P_conf ≈ 10³⁴ Pa.** This is the pressure that confines the nucleon in the same hydrostatic picture; it is not a separate “strong force” constant but the pressure at the nucleon scale when v_surface = cκ with κ = 1/√2.

**ρ_s (spation density).** **ρ_s = 2 P_conf/c² ≈ 2.3×10¹⁷ kg/m³.** Matches nuclear saturation density. So mass and “strong” pressure emerge from the same spation medium; no separate QCD bag constant is inserted by hand—it is the confinement pressure under κ = 1/√2 (Formula F6; see also F11).

---

### Nuclear κ = 1/√2

At the nucleon surface the velocity is **v_surface = cκ** with **κ = 1/√2** (so v_surface = c/√2 at the nucleon). The orbital form is **v² = c²κ²(R/r)** with **κ = 1/√2**.

**Why κ = 1/√2.** (1) Virial stability: v_orb/v_escape = 1/√2, so κ is the orbital-to-escape ratio at the nucleon. (2) Kinetic energy per nucleon becomes (1/2)m_N c²κ² = m_N c²/4; confinement and overlap pressures scale with κ² = 1/2. (3) The proton magnetic moment μ_p = e c R/(2√2) uses κ = 1/√2 (F12).

**Summary.** Surface velocity: c/√2 (κ = 1/√2). Orbital form: v² = c²κ²(R/r). Kinetic per nucleon: m_N c²/4. Confinement: P_N κ² = P_N/2. All certified formulas (F11, F12, D-01) use κ = 1/√2.

---

### Formula F5: Deuteron binding (p-p-e)

**Statement:** Two protons plus one shared internal electron. **E_bind ≈ 3 k_e e²/D − V_pp;** D = 1.942 fm; result ~2.28 MeV (measured 2.224 MeV).

**Derivation.** (1) Coulomb p–e–p attraction vs p–p repulsion. (2) Symmetric geometry: two p–e terms ~−k_e e²/(D/2) each, one p–p term ~+k_e e²/D. (3) Net ≈ 3 k_e e²/D with appropriate sign and geometry. (4) D is chosen so the gap D − d_p matches the electron node scale (~0.26 fm). (5) V_pp is a small correction for proton–proton repulsion; the dominant binding is from the shared electron.

**Why it matters.** The deuteron is the first bound nucleus. D-01 certifies that binding can be treated as electromagnetic/geometric (electron-mediated), not a separate “strong force” with free parameters. κ = 1/√2 is already embedded in the magnetic moment used in the alternative 2.15 MeV (magnetic) model. So both routes to E_bind are consistent with the same κ.

**Checks.** D-01; B2; nuclear SEMF (Chapter 12). Error ~2.5% for p-p-e; ~3.1% for magnetic.

---

### Formula F11: Nuclear kinetic and confinement (κ = 1/√2)

**Statement:** Kinetic energy per nucleon **(1/2)m_N c²κ² = m_N c²/4;** confinement pressure scaled by κ²: **P_N κ² = P_N/2;** overlap pressure **P_overlap = κ² P_N.**

**Derivation.** (1) v_surface = cκ with κ = 1/√2 ⇒ v² = c²/2. (2) E_kin = (1/2)m_N v² = m_N c²/4. (3) Pressure from hydrostatic equilibrium at nuclear scale; the κ² factor comes from velocity-squared scaling in the displacement field. (4) When two nucleons overlap, the overlap pressure is κ² P_N (same scaling).

**Why it matters.** Nuclear “strong” effects are not a separate force; they are the same pressure and velocity field with κ = 1/√2 at the nucleon surface. All nuclear first-principles (deuteron, magnetic moment, saturation) use κ = 1/√2.

**Checks.** D-01; nuclear saturation density; 09_CANONICAL §9.

---

### Benchmark D-01: Deuteron binding — full certification

**What is certified:** Deuteron binding energy is predicted from (a) magnetic coupling (μ_p, μ_N, separation) giving ~2.15 MeV, or (b) electron-mediated p–p–e Coulomb geometry giving ~2.28 MeV. Measured 2.224 MeV. Error ~3.1% (magnetic) or ~2.5% (p-p-e).

**Formula (p-p-e):** E_bind ≈ 3 k_e e²/D − V_pp; D ≈ 1.942 fm; geometric check gap ≈ 0.26 fm (electron node).

**Commentary.** The deuteron is the first nuclear “molecule.” D-01 certifies that nuclear binding can be treated geometrically (shared electron, magnetic coupling, pressure relief) without invoking meson exchange or ad hoc strong-force parameters. κ = 1/√2 is already embedded in the magnetic moment used in the magnetic model. Both routes give binding close to 2.224 MeV; the framework is overdetermined.

**Experimental check:** 2.224 MeV. **Status: CERTIFIED.**

---

### Scale consistency: nuclear vs atomic vs stellar

At the nucleon, v_surface = c/2 (κ = 1/√2); at the Bohr orbit, v_e = c/137 (Ϟ_H = 137); at the Sun, v_surface (effective) gives k_⊙ ≈ 686. The same master equation v² = c² R_c/r (or v² = c²κ²(R/r) with κ explicit at nuclear scale) applies; only R and the surface velocity ratio (κ or k) change. So nuclear structure and binding are not an exception to SDT; they are the same geometry with κ = 1/√2 and the pressure hierarchy P_∞, P_conf, ρ_s.

---

### Summary and cross-references

- **Neutron:** n = p⁺ + e⁻_internal; node ≈ 0.25 fm. **Deuteron:** p-p-e or magnetic; E_bind ≈ 2.15–2.28 MeV (measured 2.224 MeV). **Pressure:** P_∞ ≈ 1.39×10⁻¹⁴ Pa; P_conf ≈ 10³⁴ Pa; ρ_s ≈ 2.3×10¹⁷ kg/m³.
- **Nuclear κ:** κ = 1/√2; v² = c²κ²(R/r); v_surface = c/√2; E_kin/nucleon = m_N c²/4.
- **F5:** E_bind ≈ 3 k_e e²/D (p-p-e); **F11:** kinetic and confinement with κ² = 1/2. **D-01:** CERTIFIED.

**Worked numbers (deuteron).** With D = 1.942 fm = 1.942×10⁻¹⁵ m, e = 1.602×10⁻¹⁹ C, k_e ≈ 8.99×10⁹ N⋅m²/C²: 3 k_e e²/D ≈ 3 × 8.99×10⁹ × (1.602×10⁻¹⁹)² / (1.942×10⁻¹⁵) J ≈ 3.57×10⁻¹³ J ≈ 2.23 MeV. With a small V_pp correction the p-p-e model gives ~2.28 MeV; measured 2.224 MeV. The magnetic model (dipole–dipole, μ_p, separation) gives ~2.15 MeV. Both are within a few percent of the measured value.

**Cross-references.** F12 (μ_p = e c R/(2√2)); F6 (pressure hierarchy); Chapter 5 (trefoil, κ ≈ 0.694); Chapter 6 (hydrogen); Chapter 12 (benchmark suite, S-01). Falsification (Part I §4.2): ³He vs ³H binding from electron-mediated node geometry.

Chapter 11 treats cosmology and the CMB (B12, F7, F15) in the same static Euclidean picture.

---

*Sources: Part I §2.1–2.3; Part II D-01; Part III F5, F11; 09_CANONICAL §9.*



## Chapter 11: Cosmology and CMB

### Context and scope

Spatial Displacement Theory extends the same geometric framework—occlusion, master equation, and z·k² = 1—to cosmological scales. The universe is modelled as a **static Euclidean** volume with a boundary at roughly 48 Gly. The cosmic microwave background (CMB) is not interpreted as a relic of an expanding Big Bang but as the radiation field of a **48 Gyr spation radiator**: a boundary at which the pressure field is sustained and from which redshift arises by the same gravitational/climbing-out mechanism that applies at stellar and atomic scales. No expansion of space is required; redshift and the observed CMB temperature follow from the static pressure field and the identity z = (R_universe/R_boundary) − 1.

This chapter presents Part I §3 (cosmological boundary conditions), Benchmark B12 (CMB certification), and Formulas F7 and F15. We describe the 48 Gyr radiator and the solar–proton π bridge (k_⊙ = k_p²), then state B12 in full and derive F7 (z_boundary, 48 Gyr, temperature) and F15 (spation pressure P_spation(r)). We close with the static-Euclidean picture, the absence of expansion, and cross-references to the rest of the treatise. Sources: Part I §3.1–3.2; Part II B12; Part III F7, F15; 09_CANONICAL §10.

**Notation.** R_uni (or R_universe) ≈ 48 Gly is the effective radius of the static Euclidean volume; R_boundary is the boundary radius at which the CMB is emitted (or the effective “last scattering” surface). z_boundary ≈ 1090 is the redshift from that boundary to the observer. T_CMB = 2.725 K (observed); T_boundary ≈ 3000 K (emission); T_emit ≈ 2971 K at recombination.

---

### Part I §3.1: The 48 Gyr Spation Radiator

**Static Euclidean volume.** In SDT, the universe is not expanding. It is a static Euclidean volume with an effective radius R_uni ≈ 48 Gly (billion light-years). The CMB is the pressure-field source: the boundary of this volume acts as a radiator sustaining the spation pressure. Time in this picture is not “age since Big Bang” but the duration over which the boundary has been radiating—hence “48 Gyr” as both a distance scale (48 Gly) and a time scale (48 billion years) in natural units where c = 1.

**CMB temperature and redshift.** The observed CMB temperature is T_CMB = 2.725 K. The redshift from the boundary is z_boundary ≈ 1090. The temperature at the boundary (emission) is T_boundary = T_CMB(1 + z) ≈ 2.725 × 1091 ≈ 2970 K (often quoted as ~3000 K). So T_obs = T_emit/(1+z): the same gravitational-redshift relation that applies to stars applies to the cosmological boundary. Redshift is interpreted as climbing out of the pressure potential, not as Doppler shift from expansion. Approximate wavefront spreading gives z ∝ r² − 1 in some formulations; the exact relation is tied to the pressure profile (F15).

**Why “48 Gyr”.** The value R_uni ≈ 48 Gly is chosen so that the resulting z and T_obs match the observed CMB redshift (~1090) and temperature (2.73 K). It is the cosmological counterpart of the c-boundary radius: the scale at which the pressure field is defined. No separate “Hubble constant” or “dark energy” is introduced; the single geometric scale R_uni (with the boundary condition) sets the observable cosmology. In natural units (c = 1), 48 Gly corresponds to 48 Gyr, so the “age” of the universe in this picture is of order 48 billion years—the time for light to cross the static volume—rather than the ~13.8 Gyr of the standard model.

---

### Part I §3.2: Solar–Proton Scaling (π bridge)

**k_⊙ = k_p² ≈ 686.** The solar koppa is the square of the proton koppa: k_⊙ = k_p² (Chapter 4 and 5). So the proton (trefoil topology, k_p² = 5 α⁻¹) and the Sun are locked; the same topology that gives the fine-structure inverse at the Bohr scale gives the solar surface velocity ratio.

**Rotation coupling: v_rot = π v_orb²/c.** The Sun’s surface rotation is tied to the orbital velocity at 1 AU by v_rot = π v_orb²/c (Formula F8, Chapter 7). With v_orb = 436.7 km/s this gives T_rot ≈ 25.32 days (siderial). This “π bridge” links orbit and spin; it is the same geometric coupling that appears in Rule 7 (rotation route to Ϟ). So atomic (137), solar (686), and rotation (π v_orb²/c) are part of one scaling picture from proton to star.

---

### Benchmark B12: CMB Interpretation — CERTIFIED ✓

**What is certified.** CMB redshift z ≈ 1090 and temperature T_obs = 2.73 K are interpreted as gravitational redshift and cooling from a boundary at R_boundary, with z = (R_universe/R_boundary) − 1. The pressure mechanism (spation pressure, not expansion) drives the redshift. T_emit ≈ 2971 K at recombination; T_obs = T_emit/(1+z).

**Formulas.** (1) Redshift: z = (R_universe/R_boundary) − 1 ≈ 1089–1090. (2) Temperature: T_obs = T_emit/(1+z) with T_emit ≈ 2971 K. (3) Spation pressure (F15): P_spation(r) = ρ_s c² R_universe/r (see below).

**Commentary.** The CMB is not a “relic of the Big Bang” in SDT; it is the signature of a boundary at ~48 Gly and a static pressure field. B12 certifies that the same z·k² = 1 and master equation used at smaller scales extend to cosmology. The observed blackbody spectrum and temperature are reproduced by treating the boundary as a radiator at T_emit and the redshift as gravitational. Status: CERTIFIED.

---

### Formula F7: 48 Gyr Static Universe and z_boundary ≈ 1090

**Statement.** R_uni ≈ 48 Gly; z_boundary ≈ 1090; T_boundary ≈ 3000 K; T_obs = 2.73 K. Redshift is from gravitational/climbing-out, not expansion.

**Derivation.** (1) z = (R_universe/R_boundary) − 1. If R_uni/R_boundary ≈ 1090, then z ≈ 1089–1090. So one number (the ratio of universe radius to boundary radius) fixes the CMB redshift. (2) T_obs = T_emit/(1+z) with T_emit ≈ 2971 K at recombination (or at the boundary). This is the standard gravitational-redshift formula for temperature: the observed temperature is the emitted temperature divided by (1+z). (3) Wavefront spreading in the pressure field can be approximated as z ∝ r² − 1 in some treatments; the exact relation follows from the radial pressure profile (F15). (4) The value 48 Gly is the effective radius of the static volume that yields the observed z and T_obs when combined with the boundary condition and P_spation(r).

**Why it matters.** Cosmology is not “exceptional”; the same z·k² = 1 and pressure field apply at the boundary. The CMB is the boundary radiator, not a relic of an expanding singularity. B12 certifies this interpretation. Falsification would be a clear observational need for expansion (e.g. accelerating expansion that could not be rephrased in terms of a static pressure gradient) or a CMB spectrum that could not be fitted by a single redshifted blackbody from a boundary.

**Checks.** B12; CMB temperature and spectrum (COBE, WMAP, Planck).

---

### Formula F15: CMB Pressure Field P_spation(r) = ρ_s c² R_uni/r

**Statement.** Spation pressure at cosmological scale: P_spation(r) = ρ_s c² R_universe/r. Redshift from climbing out of this potential: z = (R_universe/R_boundary) − 1 ≈ 1089.

**Derivation.** (1) Hydrostatic equilibrium in a static Euclidean universe with boundary at R_uni: the pressure gradient dP/dr is set by the same physics as at stellar scale but integrated over the cosmological volume. (2) P ∝ 1/r from the integrated pressure gradient (same scaling as the potential that gives v² ∝ 1/r at smaller scales). (3) The constant of proportionality is ρ_s c² R_uni so that dimensions are correct ([P] = Pa). (4) The redshift z from boundary to observer is the gravitational redshift formula tied to the same R and boundary: z = (R_uni/R_boundary) − 1.

**Why it matters.** The CMB is the boundary radiator; temperature and z come from the same pressure field that gives orbits at smaller scales. B12 certifies; no expansion is required. The pressure P_spation(r) is the cosmological analogue of the pressure gradient that gives a(r) = c² R_c/r² in Chapter 3; here the “source” is the boundary at R_uni.

**Checks.** B12; 09_CANONICAL §10; T_obs = 2.73 K.

---

### Static Euclidean picture and no expansion

**Static Euclidean.** Space is not expanding. The metric is Euclidean; distances are defined in the usual way. Redshift is not Doppler shift from receding sources but the result of climbing out of the pressure potential: photons lose energy as they propagate from the boundary to the observer, yielding z = (R_uni/R_boundary) − 1 and T_obs = T_emit/(1+z). The “Hubble flow” and distance–redshift relation, if interpreted in SDT, would be rephrased in terms of the pressure field and boundary geometry, not comoving coordinates in an expanding metric.

**No expansion.** SDT does not introduce a scale factor a(t) or a Big Bang singularity. The 48 Gyr radiator is a boundary condition, not an initial moment. Age of the universe in the conventional sense is replaced by the time scale associated with the boundary (48 Gyr in natural units). Dark energy, as usually formulated (a cosmological constant driving acceleration), is not required; the static pressure field and boundary suffice to interpret CMB and redshift within the certified benchmarks.

**Decoupling.** The dataset (09_CANONICAL §10) notes that spation pressure and plasma/radiation can be treated as two systems at decoupling: the pressure field sets the geometry and redshift, while the plasma recombines and emits the blackbody at T_emit. The observed CMB spectrum is then the redshifted blackbody from that emission surface.

**CMB spectrum.** The CMB is observed to be a nearly perfect blackbody at T_obs = 2.725 K. In SDT, this is explained by emission at the boundary (or recombination surface) at T_emit ≈ 2971 K, followed by gravitational redshift (1+z) ≈ 1090, so T_obs = T_emit/(1+z) ≈ 2.73 K. The same thermodynamic and radiative physics that give a blackbody at T_emit apply; the only difference from standard cosmology is the interpretation of z (climbing out of potential vs expansion). Anisotropies (dipole, acoustic peaks) would be interpreted in terms of the static geometry and pressure fluctuations, not necessarily as Doppler or Sachs–Wolfe in an expanding universe; detailed comparison is beyond the scope of this chapter.

**Comparison to standard cosmology (one paragraph).** In the standard ΛCDM model, the CMB is the relic of the hot Big Bang; redshift is cosmological (expansion); and the universe has a finite age (~13.8 Gyr). In SDT, the CMB is the boundary radiator in a static Euclidean volume; redshift is gravitational/climbing-out; and the 48 Gyr scale is the boundary radius/time. Both frameworks can fit the observed CMB temperature and approximate redshift; they differ in mechanism (expansion vs pressure gradient) and in the need for dark energy and an initial singularity. B12 certifies that the SDT interpretation is consistent with the CMB data within the scope of this treatise.

**Falsification.** The static-Euclidean, no-expansion picture would be challenged by (a) evidence that redshift is demonstrably Doppler (e.g. time dilation in type Ia supernovae that could not be rephrased in a static model), or (b) CMB observables (e.g. acoustic peak structure, polarization) that could not be accommodated by a boundary radiator and pressure field. Until such evidence is established, B12 stands as CERTIFIED.

**Worked numerical check.** With z = 1090, T_emit = 2971 K gives T_obs = 2971/1091 ≈ 2.724 K, matching T_CMB = 2.725 K. With R_uni/R_boundary = 1090, z = 1089. So the numbers are internally consistent. The pressure hierarchy (Chapter 10, F6) connects P_∞ from the CMB to the same ρ_s and c: P_∞ ≈ 1.39×10⁻¹⁴ Pa from CMB energy density, and the stiffness ratio ρ_s c²/P_∞ ≈ 1.5×10⁴⁸ ties the nuclear spation density to the cosmological boundary. Thus atomic, stellar, and cosmological scales share one pressure field and one set of geometric relations.

---

### Summary and cross-references

- **Part I §3.1:** 48 Gyr spation radiator; R_uni ≈ 48 Gly; T_CMB = 2.725 K; z_boundary ≈ 1090; T_boundary ≈ 3000 K; static Euclidean; redshift from wavefront spreading / climbing out.
- **Part I §3.2:** k_⊙ = k_p²; v_rot = π v_orb²/c (π bridge); T_rot ≈ 25.32 days.
- **B12:** CMB redshift and temperature interpreted as gravitational redshift from boundary; z = (R_uni/R_boundary) − 1; T_obs = T_emit/(1+z); pressure mechanism; CERTIFIED.
- **F7:** R_uni ≈ 48 Gly; z_boundary ≈ 1090; T_boundary ≈ 3000 K; T_obs = 2.73 K; no expansion.
- **F15:** P_spation(r) = ρ_s c² R_universe/r; z from same potential; B12 certifies.

**Cross-references.** Chapter 3 (master equation, pressure gradient); Chapter 4 (z·k² = 1); Chapter 5 (k_p, trefoil); Chapter 7 (F8, solar rotation); Chapter 12 (B12 in benchmark index). Sources: Part I §3; Part II B12; Part III F7, F15; 09_CANONICAL §10.

---

*Word count: ~2,720 (target 2,680–6,064).*



## Chapter 12: Benchmark Suite and Certification

### Context and scope

The SDT framework is validated by a fixed set of benchmarks: geometric foundations, atomic and stellar dynamics, classical tests of gravitation, nuclear binding, cosmology, and the Ten Rules and paradox resolution. These benchmarks are not optional add-ons; they are the certification that the same primitives, occlusion, master equation, and \(z \cdot \varkappa^2 = 1\) yield correct or consistent results across scales. This chapter provides (1) a **master index** of all benchmarks (B1–B12, D-01, S-01) with one-line summary and chapter reference; (2) the **full certification text** for **Benchmark S-01** (screening factor ξ), which appears here in full as specified; (3) the **implementation logic**: calculation order (Part I §4.1) and falsification vectors (Part I §4.2); and (4) **how to use** the benchmarks for validation and falsification. The takeaway is that anyone implementing or testing SDT should use this chapter as the single reference for “what is certified” and “in what order to compute.”

---

### Master index of benchmarks

| ID | Short description | Key formula / relationship | Chapter | Status |
|----|-------------------|----------------------------|---------|--------|
| **B1** | Geometric foundation | \(O(r) = R^2/(4r^2)\); inverse-square from solid angle | 2 | CERTIFIED |
| **B2** | Koppa anchor | \(\varkappa_H = 137.036\); \(\varkappa = 1\) at c-boundary | 6 | CERTIFIED |
| **B3** | Centripetal force (hydrogen) | \(F = m_e v^2/a_0\); 4 sig. fig. vs CODATA | 6 | CERTIFIED |
| **B4** | Hydrogen spectrum | Lyman series; ionisation 13.606 eV; Ϟ framework | 6 | CERTIFIED |
| **B5** | Solar Ϟ (three routes) | Orbital, rotation, spectral → same \(k_\odot \approx 686.6\); \(z \cdot \varkappa^2 = 1\) | 7 | CERTIFIED |
| **B6** | Solar system orbits | \(v(r) = (c/k_\odot)\sqrt{R_\odot/r}\); max error &lt; 0.41% | 7 | CERTIFIED |
| **B7** | Jovian system | Galilean satellites; same \(v(r)\) with Jupiter’s \(k_J\), \(R_J\); max error 0.00% | 7 | CERTIFIED |
| **B8** | Exoplanetary validation | Stellar \(k\) from rotation/z/orbit; \(v_{\text{planet}}\); max error ≈ 2.02% | 7 | CERTIFIED |
| **B9** | Ten Rules codified | Rules 1–10; framework as constitution | 8 | CERTIFIED |
| **B10** | Paradox resolution | Six paradoxes (hierarchy, vacuum, duality, measurement, dark matter, dark energy) | 8 | CERTIFIED |
| **B11** | Classical tests of GR | Light deflection, Shapiro, perihelion; refractive interpretation; within error bars | 9 | CERTIFIED |
| **B12** | CMB interpretation | \(z \approx 1090\), \(T_{\text{obs}} = 2.73\) K; boundary radiator; static Euclidean | 11 | CERTIFIED |
| **D-01** | Deuteron binding | Magnetic ~2.15 MeV or p-p-e ~2.28 MeV; measured 2.224 MeV; κ = 1/√2 | 10 | CERTIFIED |
| **S-01** | Screening factor | ξ ≈ 6.3×10⁻⁹; nuclear stability ~94% | 12 (below) | CERTIFIED |

---

### Calculation order (implementation logic §4.1)

The dataset specifies a fixed sequence for computing the velocity field and related quantities. Use this order when implementing the physics engine or when checking a benchmark.

1. **Define scale.** Choose the body and its physical radius \(R_{\text{phys}}\). Obtain either the surface (or orbital) velocity \(v_{\text{surface}}\) at \(R_{\text{phys}}\), or the gravitational redshift \(z\) for that body.

2. **Compute Ϟ (or k).**  
   \(\varkappa = c/v_{\text{surface}}\) **or** \(\varkappa = 1/\sqrt{z}\).  
   Rule 7: Ϟ can also be obtained from orbital parameter (\(\varkappa = c/\sqrt{\beta/R}\)) or from rotation (\(\varkappa = \sqrt{\pi c/v_{\text{rot}}}\)). All routes must agree for the same body.

3. **Compute c-boundary radius.**  
   \(r_c = R_{\text{phys}}/\varkappa^2\).  
   At \(r = r_c\), orbital velocity equals \(c\) (Rule 9).

4. **Compute velocity field.**  
   \(v(r) = (c/\varkappa)\sqrt{R_{\text{phys}}/r} = c\sqrt{r_c/r}\).  
   This is the master equation (Rule 4, F1).

5. **If atomic or nuclear:** Apply scale-specific rules (e.g. trefoil \(n=3\), \(m=2\) for proton; κ = 1/√2 for nuclear first-principles). See Chapters 5 and 10.

No step introduces an empirical constant (e.g. \(G\) or \(M\)) beyond the inputs \(R_{\text{phys}}\) and \(v_{\text{surface}}\) (or \(z\)). The only “constants” that appear are \(c\) and the geometric outcomes (e.g. Ϟ_H = 137.036 from hydrogen, \(k_\odot = k_p^2\) from the proton–solar bridge).

---

### Falsification vectors (§4.2)

The dataset identifies three areas where the framework is most exposed to falsification. These are not the only possible tests but are the ones explicitly designated for monitoring.

- **Atomic.** **Lamb shift.** The orbital scale in hydrogen is much larger than the nuclear scale (\(d_{\text{orbital}} \approx 3.36\,\alpha^{-2}\,d_{\text{nuclear}}\)). Any SDT treatment of fine structure or Lamb shift must be consistent with this separation. A persistent discrepancy that cannot be explained by geometry or screening would count against the framework.

- **Galactic.** **Rotation curves.** SDT predicts \(v(r) = c\sqrt{R_{\text{occ}}/r}\) with an effective occlusion radius \(R_{\text{occ}}\) that may depend on the mass distribution and screening. Flat or rising rotation curves must be explained by this geometry (and ξ where relevant) without ad hoc dark matter. A systematic mismatch between observed \(v(r)\) and the occlusion-based form for a given mass profile would be a falsification vector.

- **Nuclear.** **³He vs ³H binding.** The binding energy difference between helium-3 and tritium depends on the geometry of the third nucleon and electron-mediated (or magnetic) bonding. SDT’s node geometry and κ = 1/√2 must reproduce the correct trend. A discrepancy that cannot be resolved by improved geometry or screening would count against the framework.

When validating SDT, run the calculation order for the relevant scale and compare with the corresponding benchmark (e.g. B2–B4 for atomic, B6–B8 for stellar, D-01 for deuteron). When considering falsification, prioritise these three vectors and the benchmarks that address them (Chapters 6, 7, 10, 12).

---

### Benchmark S-01: Screening factor — full certification

**What is certified:** The screening factor ξ (ratio of gravitational effect to “bare” displacement volume) is derived from Earth’s measured field and used to predict nuclear stability patterns. **ξ ≈ 6.3×10⁻⁹**; **~94% of stable nuclides** correctly predicted.

**Formulas and logic:** ξ is defined as the ratio that connects the “bare” displacement geometry (e.g. from \(R_{\text{phys}}\) and Ϟ) to the measured gravitational effect at laboratory scale (e.g. Earth’s surface field). From Earth’s measured \(g\) and radius, and the SDT relation between acceleration and \(R_c\) (or \(R/\varkappa^2\)), one infers the effective screening: only a fraction of the naive displacement volume is “active” for the net field. That fraction is ξ. Once ξ is fixed at one scale (Earth), it is used with nuclear geometry (and a semi-empirical mass formula calibrated to ³He, ⁴He) to predict which nuclides are stable. The result is that approximately 94% of known stable nuclides are correctly predicted.

**Commentary:** S-01 ties gravity at laboratory scale to the same displacement picture. It certifies that a single geometric screening factor, combined with nuclear geometry (and SEMF calibrated to ³He, ⁴He), reproduces the stability chart without dark parameters. So “screening” is not an arbitrary fudge; it is the ratio of observed gravitational effect to the geometric displacement prediction, and it is consistent from laboratory to nuclear scale.

**Experimental / theoretical check:** Earth’s surface field; nuclear stability data. **Status: CERTIFIED.**

---

### How to use the benchmarks for validation

**Implementing the physics engine:**  
Use the calculation order above. For each body (e.g. Sun, Jupiter, a star with exoplanets), obtain \(R_{\text{phys}}\) and \(v_{\text{surface}}\) (or \(z\) or \(\beta\)); compute Ϟ, \(r_c\), and \(v(r)\). Compare planetary or satellite velocities with B6, B7, B8; compare solar Ϟ with B5. For hydrogen, use B2–B4; for deuteron, use D-01; for CMB, use B12.

**Validating against data:**  
For each benchmark, the “What is certified” and “Experimental check” lines state what is being tested. Use the cited data sources (JPL, CODATA, NASA Exoplanet Archive, etc.) and the formulas in the relevant chapters. Fill in “Actual count” or “Result” as needed; confirm that results fall within the certified tolerances (e.g. B6 max error &lt; 0.41%, B5 σ ≈ 0.03%).

**Falsification:**  
If a benchmark fails repeatedly after careful recalculation and updated data, the framework is under pressure. The designated falsification vectors (Lamb shift, rotation curves, ³He vs ³H) are the first to monitor. Document the discrepancy and whether it can be resolved by refining geometry, screening, or calibration (e.g. SEMF) without abandoning the Ten Rules.

**Cross-references:**  
Each benchmark points to specific chapters (see master index). For formulas, use Chapter 13 (formula compendium). For the Ten Rules, use Chapter 8. For paradox resolution, use Chapter 8 (B10).

---

### Compact benchmark summary (by category)

**Geometry and foundation:** B1 (occlusion \(O(r) = R^2/(4r^2)\)).

**Atomic:** B2 (Ϟ_H = 137.036), B3 (centripetal force), B4 (hydrogen spectrum).

**Stellar and planetary:** B5 (solar Ϟ, three routes), B6 (planets), B7 (Jovian moons), B8 (exoplanets).

**Framework and paradoxes:** B9 (Ten Rules), B10 (six paradoxes).

**Classical tests:** B11 (light deflection, Shapiro, perihelion).

**Cosmology:** B12 (CMB, z ≈ 1090, 48 Gyr boundary).

**Nuclear:** D-01 (deuteron binding), S-01 (screening ξ, stability).

---

### Checks and cross-references

- **Chapters 2–11:** Each benchmark is treated in detail in the chapter listed in the master index.
- **Chapter 1:** Calculation order and falsification vectors are introduced; this chapter repeats them in full for the benchmark suite.
- **Chapter 8:** B9 (Ten Rules) and B10 (paradox resolution) as the constitution.
- **Chapter 13:** Formula compendium F1–F17 with cross-links to benchmarks.
- **Primary source:** Part II (all benchmarks) and Part I §4.1–4.2 (SDT_CORE_AXIOMS_AND_DATASET).

---

### Summary

- **Master index:** B1–B12, D-01, S-01 with one-line description, key formula, chapter, and status (all CERTIFIED).
- **Calculation order:** (1) Define scale; (2) Ϟ = c/v_surface or 1/√z; (3) r_c = R/Ϟ²; (4) v(r) = (c/Ϟ)√(R/r); (5) atomic/nuclear tweaks as needed.
- **Falsification vectors:** Atomic (Lamb shift), galactic (rotation curves), nuclear (³He vs ³H).
- **S-01 in full:** Screening factor ξ ≈ 6.3×10⁻⁹; ~94% stable nuclides; certification text given above.
- **How to use:** Implement with the calculation order; validate against each benchmark’s “What is certified” and experimental check; monitor falsification vectors.

---

*Sources: Part II (all benchmarks), Part I §4.1–4.2 (SDT_CORE_AXIOMS_AND_DATASET).*



## Chapter 13: Standout Formulas Compendium

### Context and scope

This chapter is the formula index for the SDT Core Treatise: a condensed reference for **F1–F17** with statement, one-line derivation, one-line "why it matters," and cross-links to chapters and benchmarks. Full derivations are in the referenced chapters. **Source:** Part III (SDT_CORE_AXIOMS_AND_DATASET); 09_CANONICAL_SDT_FORMULAS.md.

---

### Formula index (F1–F17)

**F1:** v² = c² R_c/r; v(r) = (c/k)√(R_phys/r). Hydrostatic equilibrium + v=c at R_c. Only dynamical equation for orbits; no G, M. Ch 3; B2, B5, B6, B7, B8, D-01.

**F2:** z·k² = 1; k = c/v_surface, z = R_c/R_phys. At R_phys, v=c/k; R_c = R_phys/k² ⇒ z = 1/k². One measurement (z or k) fixes the other. Ch 4; B2, B5, B12.

**F3:** k = c/v_surface; k_p ≈ 26.2; k_⊙ = k_p² ≈ 686. Trefoil k_p² = 5 α⁻¹; solar–proton bridge. Proton and Sun linked by factor 5. Ch 4, 5; B2, B5, B6.

**F4:** n=3, m=2; Δ_topo=5; k_p² = 5×137.036 ≈ 685.18; a/R = 1/√2; κ ≈ 0.694 ≈ 1/√2. Trefoil 3₁ invariant; κ from torus. Proton is structured vortex; fixes 137, 686, κ. Ch 5; B2, B5; F12.

**F5:** E_bind ≈ 3 k_e e²/D − V_pp; D ≈ 1.942 fm; ~2.28 MeV (measured 2.224 MeV). Coulomb p-e-p vs p-p; symmetric geometry. Deuteron first bound nucleus; D-01 certifies. Ch 10; D-01; B2.

**F6:** P_∞ ≈ 1.39×10⁻¹⁴ Pa; P_conf ≈ 10³⁴ Pa; ρ_s = 2 P_conf/c² ≈ 2.3×10¹⁷ kg/m³. CMB; hydrostatic at nuclear scale; equation of state. Mass and "strong" pressure from same medium. Ch 10; B4, D-01.

**F7:** R_uni ≈ 48 Gly; z_boundary ≈ 1090; T_obs = 2.73 K; redshift from gravitational, not expansion. z = (R_uni/R_boundary) − 1; T_obs = T_emit/(1+z). Cosmology not exceptional; B12 certifies. Ch 11; B12.

**F8:** v_rot = π v_orb²/c; T_rot ≈ 25.32 days. Geometric flux coupling; dimensionally correct. Third route to k_⊙. Ch 7; B5; Rule 7.

**F9:** O(r) = R²/(4r²); Ω(r) = 2π(1 − √(1 − R²/r²)); O = Ω/(4π). Solid angle; Taylor for r≫R. All inverse-square from this; B1 certifies. Ch 2; B1.

**F10:** a(r) = c² R_c/r² = c² R_phys/(k² r²). Centripetal a = v²/r; pressure gradient. Newtonian gravity = low-velocity limit. Ch 3; B3, B6; Rule 2.

**F11:** E_kin/nucleon = m_N c²/4; P_N κ² = P_N/2; κ = 1/√2. v_surface = cκ; hydrostatic equilibrium. Nuclear "strong" = same pressure field. **CRITICAL: κ=1 forbidden.** Ch 10; D-01; 09_CANONICAL §9.

**F12:** μ_p = e c R/(2√2); κ = 1/√2 (not κ=1). Magnetic moment from circulating current; κ gives 2√2. Geometric prediction; anomaly is κ. Ch 5, 10; CODATA μ_p.

**F13:** Δt = (4R/(Ϟ²c)) ln(4r₁r₂/b²). n(r) = 1 + 2R/(Ϟ²r); integrated optical path. Same as GR; B11 certifies. Ch 9; B11; Cassini.

**F14:** Δω = 6πR/(Ϟ²a(1−e²)). Pressure gradient; first-order perturbation. Mercury 43″/century; B11 certifies. Ch 9; B11; Mercury.

**F15:** P_spation(r) = ρ_s c² R_uni/r; z ≈ 1089. Hydrostatic at R_uni; P ∝ 1/r. CMB boundary radiator; B12 certifies. Ch 11; B12.

**F16:** v_escape = √2 × c/Ϟ = √2 v_surface. Work ∫ a dr; (1/2)v_esc² = c²/Ϟ². √2 geometric; ties to κ = 1/√2. Ch 3; B3; Rules 5–6.

**F17:** Ϟ(r) = √(r/r_c). v(r) = c√(r_c/r) ⇒ Ϟ = c/v = √(r/r_c). Ϟ grows with r; surface koppa is anchor. Ch 3; B2, B5, B6; Rules 4, 9.

---

### Cross-reference table

| Formula | Primary chapter | Benchmarks |
|---------|-----------------|------------|
| F1 | 3 | B2, B5, B6, B7, B8, D-01 |
| F2 | 4 | B2, B5, B12 |
| F3 | 4, 5 | B2, B5, B6 |
| F4 | 5 | B2, B5, F12 |
| F5 | 10 | D-01, B2 |
| F6 | 10 | B4, D-01 |
| F7 | 11 | B12 |
| F8 | 7 | B5 |
| F9 | 2 | B1 |
| F10 | 3 | B3, B6 |
| F11 | 10 | D-01, F12 |
| F12 | 5, 10 | μ_p, CRITICAL CORRECTION |
| F13 | 9 | B11, Cassini |
| F14 | 9 | B11, Mercury |
| F15 | 11 | B12 |
| F16 | 3 | B3, Rules 5–6 |
| F17 | 3 | B2, B5, B6 |

**Sources:** Part III (SDT_CORE_AXIOMS_AND_DATASET); 09_CANONICAL_SDT_FORMULAS.md.

---

## Chapter 15: Galactic Systems and Flat Rotation Curves

**Scope (Book 15).** This chapter is an extended application of the SDT framework at **galactic scale**. It expands the galactic content of Benchmark B10 (paradox resolution) and the falsification vectors in Part I §4.2: rotation curves, the velocity law v = c√(R_occ/r), and the interpretation of “dark matter” as geometry and occlusion rather than invisible mass. Book 15 is shared by Agents 2 and 3; it is not part of the original 13-chapter core list but is included to give a dedicated treatment of galactic scaling. Word-count target: 2,680–6,064 (same as other chapters).

---

### Context and scope

Chapters 3 and 7 showed that the master equation v² = c² R_c/r (equivalently v(r) = c√(r_c/r)) applies from hydrogen to exoplanets with a single body-specific length scale (the c-boundary r_c or the physical radius R and koppa k). At **galactic** scale, the same form is used: orbital velocity in the disk or halo is given by **v(r) = c√(R_occ/r)**, where **R_occ** is an effective **occlusion radius** that encodes how much of the sky is blocked by the displacing mass (stars, gas, and any structure that contributes to the pressure deficit). In the standard narrative, “flat” or rising rotation curves are taken as evidence for dark matter. In SDT, they are explained by the **geometry of occlusion and screening**: R_occ can scale with r in such a way that v(r) remains roughly constant or rises slightly without invoking unseen matter. This chapter states that picture in full, ties it to B10 and the Ten Rules, and discusses falsification and the role of the screening factor ξ (S-01) where relevant.

**Notation.** R_occ = effective occlusion radius at galactic scale (may depend on r and on the mass distribution). v(r) = c√(R_occ/r). For a single compact source, R_occ = r_c = R/k²; for a disk or extended distribution, R_occ is an effective scale that can vary with r. ξ = screening factor (Benchmark S-01); at laboratory/planetary scale it relates gravitational effect to “bare” displacement volume.

---

### The velocity law at galactic scale

**Same equation, different scale.** Rule 10 (scale invariance) states that the same equations and the same Ϟ structure apply across nuclear, celestial, and galactic scales. So the orbital velocity at radius r in a galaxy is still:

**v(r) = c √(R_occ / r)**

Here R_occ is the effective radius that plays the role of the c-boundary (or r_c) at galactic scale. For a point-like or spherically symmetric source, R_occ = r_c = R/k². For a disk or a distribution of displacing mass, R_occ is determined by how the occlusion (solid angle blocked by the mass) accumulates with r. So “flat” rotation curves (v roughly constant over a range of r) arise when R_occ scales approximately linearly with r: if R_occ ∝ r, then v ∝ √(r/r) = constant. In other words, the geometry of the disk (and any screening) can yield R_occ(r) such that v(r) matches the observed rotation curve without adding dark matter.

**Physical meaning.** The spation medium is displaced by all gravitating mass—stars, gas, dust. The pressure deficit at distance r depends on the solid angle subtended by that mass (occlusion). In a disk galaxy, the distribution of luminous matter and the way occlusion integrates with r set R_occ(r). So the rotation curve is a **geometric** prediction once the distribution of displacing mass (and screening) is specified. No G, no M, in the same sense as at solar scale: only the effective occlusion radius and r. The “hard-line” geometric claim is that for a given mass profile and screening, v(r) = c√(R_occ/r) with the appropriate R_occ(r) must match observation; a systematic mismatch would be a falsification vector (Part I §4.2; Chapter 1, 12). Dimensional check: [c√(R_occ/r)] = (m/s)·√(m/m) = m/s, so the formula is dimensionally consistent. The same occlusion foundation (B1, F9) that gives O(r) = R²/(4r²) at stellar scale gives the inverse-square acceleration and hence v² ∝ 1/r at every scale; at galactic scale the “R” is replaced by the effective R_occ.

---

### Benchmark B10 (galactic part) and dark matter resolution

**What B10 certifies (dark matter).** Six Standard Model paradoxes are addressed within SDT without new postulates. Among them: **dark matter.** Galactic rotation curves and cluster dynamics suggest more “mass” than is visible in the Standard Model; the usual response is to invoke dark matter. In SDT, orbital velocity is set by v(r) = c√(r_c/r) or v = c√(R_occ/r) with an effective occlusion radius. Flat or rising rotation curves are explained by the distribution of displacing mass and by screening: R_occ can scale with r so that v(r) matches observations without invisible matter. So “dark matter” is reframed as geometry and occlusion (and, where relevant, the screening factor ξ; S-01). The same master equation and Rules 1–4 apply; no new particle is required.

**Commentary.** B10 is conceptual: it certifies that the same geometric picture that gives B1–B9 and B11–B12 also provides a coherent story for the rotation curve. The detailed prediction depends on modelling R_occ(r) from the observed baryonic distribution and from screening. That modelling is beyond the scope of this treatise; the point here is that the **form** of the velocity law is unchanged (v = c√(R_occ/r)), and the framework does not introduce dark matter as a new substance. Falsification would require a rotation curve that could not be fitted by any reasonable R_occ(r) consistent with the same occlusion and screening physics.

---

### R_occ scaling and “flat” curves

**Why curves can be flat.** If v(r) = c√(R_occ/r), then v is constant when R_occ ∝ r. So an effective occlusion radius that grows linearly with distance (e.g. because the enclosed “blocking” mass or the geometry of the disk causes the integrated occlusion to scale that way) naturally gives a flat rotation curve. In the standard picture, this would be attributed to a dark halo whose enclosed mass M(r) ∝ r (so v² ∝ M(r)/r ∝ constant). In SDT, the same v(r) is attributed to R_occ(r) ∝ r—a geometric/occlusion effect, not an extra mass component. The difference is interpretive: one framework adds dark matter to make M(r) large; the other keeps the same velocity law and attributes the profile to how R_occ depends on r given the baryonic distribution and screening.

**Screening (ξ) and S-01.** Benchmark S-01 certifies a screening factor ξ (ratio of gravitational effect to “bare” displacement volume) derived from Earth’s measured field and used to predict nuclear stability (~94% of stable nuclides). At galactic scale, screening could in principle affect how the displacement of the medium translates into R_occ for a given mass distribution. The treatise does not develop a full galactic screening model here; the role of ξ in B10 and in falsification (Chapter 12) is to note that a single geometric screening factor, combined with occlusion, is part of the same framework. So when comparing v(r) = c√(R_occ/r) to data, R_occ may incorporate both the “bare” occlusion from the mass distribution and any screening correction consistent with S-01 and the Ten Rules. If a galaxy’s rotation curve were to be fitted in detail, one would first fix the baryonic distribution (from light and gas), then compute or fit R_occ(r) so that v(r) = c√(R_occ/r) matches the observed curve; any residual could be attributed to screening or to refinements of the occlusion integral, not to dark matter.

---

### Falsification at galactic scale

**Falsification vectors (Part I §4.2).** Galactic: rotation curves; SDT predicts v = c√(R_occ/r) with R_occ scaling set by geometry (and ξ where relevant). A **hard-line** falsification would be a systematic mismatch between observed v(r) and the occlusion-based form for a given mass profile: i.e. no choice of R_occ(r) consistent with the baryonic distribution and screening could reproduce the data. So long as such a mismatch is not established, B10 stands: flat curves are explained by R_occ scaling, not by dark matter.

**What would challenge SDT.** (1) A rotation curve that clearly required v(r) to have a different functional form (e.g. v ∝ r or v ∝ 1/r in regimes where occlusion would predict otherwise). (2) Cluster dynamics (e.g. Bullet Cluster) that could not be rephrased in terms of occlusion and screening of the displacing mass. (3) A proven need for a dark-matter particle (e.g. direct detection with properties incompatible with a geometric interpretation). Until then, the galactic application of the master equation remains a valid and certified part of the framework.

---

### Worked qualitative example and verbal formula

**Qualitative example.** Suppose in the outer disk of a spiral galaxy the effective occlusion radius scales as R_occ = λ r for some constant λ (e.g. because the enclosed displacing mass or the geometry yields that scaling). Then v(r) = c√(λ r/r) = c√λ, a constant. So the rotation curve is flat with v = c√λ. The value of λ would be set by the baryonic distribution and screening; no dark matter is required. Conversely, if observations give v(r) ≈ constant in the outer disk, SDT interprets this as R_occ(r) ∝ r in that regime.

**Verbal formula.** In words: at galactic scale, orbital speed equals the speed of light times the square root of (effective occlusion radius divided by distance). The “flat” curve is the case where that effective radius grows in proportion to distance, so the square root is constant. The same master equation that gives planetary orbits and hydrogen gives galaxy rotation; only the definition of the effective radius (R_occ) changes with the mass distribution.

---

### Clusters and z·k² = 1 at galactic scale

**Clusters.** Galaxy clusters show dynamics (velocity dispersions, lensing) that in the Standard Model are often attributed to dark matter halos. In SDT, the same principle applies: the velocity field is set by occlusion and the effective R_occ for the cluster. The cluster’s “depth” in the potential can be described by a redshift parameter z_cluster; the identity z·k² = 1 would then relate that depth to a cluster koppa k_cluster. So at galactic and cluster scale, the same z·k² = 1 and master equation extend without introducing new matter. Detailed modelling of R_occ for clusters (and of lensing in the refractive picture of Chapter 9) is left for future work; the treatise certifies that the framework is consistent with B10 and the Ten Rules.

---

### Relation to other approaches (one paragraph)

Modified Newtonian dynamics (MOND) and dark-matter halo models (e.g. NFW) aim to fit rotation curves with different functional forms or extra mass. SDT does not use MOND’s interpolation function or NFW’s density profile; it uses v = c√(R_occ/r) with R_occ determined by occlusion and screening. So the **form** of the velocity law is fixed (inverse-square-root in r for a given R_occ); the freedom is in how R_occ depends on r and on the baryonic distribution. That places SDT closer to a “geometry only” interpretation than to adding a new force law (MOND) or a new mass component (dark matter). Falsification would be a regime where no reasonable R_occ(r) could reproduce the data.

---

### Summary and cross-references

- **Velocity law at galactic scale:** v(r) = c√(R_occ/r). Same form as at stellar and atomic scale; R_occ is the effective occlusion radius (may depend on r and mass distribution).
- **Flat curves:** R_occ ∝ r gives v ≈ constant. Explained by geometry and occlusion, not by dark matter (B10).
- **Screening:** ξ (S-01) can play a role in how R_occ is determined; full galactic screening model is not developed here.
- **Falsification:** Systematic mismatch between observed v(r) and occlusion-based v = c√(R_occ/r) for a given mass profile would falsify the galactic application.

**Implementation note.** When using the calculation order (Chapter 1) at galactic scale, one defines the “body” as the galaxy (or the relevant mass distribution). The surface radius R and surface velocity (or redshift z) then refer to an effective galactic scale: e.g. the half-light radius and the rotation velocity at that radius, or a redshift measure of the potential depth. Then k = c/v_surface or k = 1/√z, R_occ = R/k² (or the appropriate R_occ(r) from the distribution), and v(r) = c√(R_occ/r). So the same four-step order applies; only the interpretation of R and k changes. Book 15 thus ties galactic dynamics explicitly to the rest of the treatise.

**Cross-references.** Chapter 3 (master equation, scale invariance, Rule 10); Chapter 8 (B10, paradox resolution, dark matter); Chapter 12 (falsification vectors, rotation curves); Part I §4.2 (galactic falsification); B10, S-01.

---

*Word count: ~2,720 (target 2,680–6,064).*



## Chapter 16: References, Constants, and Symbol Index

### Scope of this chapter

This chapter is **Book 16** of the SDT Core Treatise: an extended reference section. It does not introduce new physics or new benchmarks. It provides (1) **primary and supporting sources** for the treatise; (2) a **constants table** of numerical values used or derived in SDT (c, fine structure, Ϟ_H, k_p, k_⊙, solar and nuclear scales, pressure hierarchy, screening factor, CMB); (3) a **symbol index** (R, r, Ϟ, k, κ, z, β, r_c, Ω, O, and related notation) with brief definitions and cross-references to chapters; and (4) a **short reference table** of key solar-system and atomic values for quick lookup. Use this chapter when you need a precise symbol meaning, a constant value, or a source citation without re-reading the full exposition.

**How to use this chapter.** For **symbols**, search the Symbol index for the character (e.g. Ϟ, κ, z); the entry gives a one-line definition and the chapter(s) where it is defined or used. For **numbers**, use the Constants table and the Short reference tables; all values are consistent with the dataset and certified benchmarks. For **sources**, cite the primary dataset and, when relevant, the supporting document (e.g. 09_CANONICAL for formula variants). For **implementation**, combine this chapter with the calculation order and benchmark list in Chapter 12.

---

### Primary and supporting sources

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

### Constants table

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

### Symbol index

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

### Short reference table: solar system and atomic

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

### Word-count checklist (reference)

The treatise constraint is **2,680–6,064 words per chapter** (inclusive), with a target of ~3,500–4,500 where possible. The official word-count checklist table (target range, actual count, “In range?”) is maintained in **00_TREATISE_TITLE_AND_TOC.md**. After drafting or revising any chapter (including this one), update that table. For Book 16 (this chapter), the same range applies if it is counted as a treatise chapter; if it is treated as an appendix or extended reference only, the editor may choose to waive or adjust the count. See 00_TREATISE_TITLE_AND_TOC.md and HANDOFF_FOR_AGENTS_2_3_4.md for details.

---

### Summary

- **Primary source:** SDT_CORE_AXIOMS_AND_DATASET.md (Parts I–III).  
- **Supporting sources:** 09_CANONICAL, 05_STRUCTURE_MAP, 08_CONSISTENCY_REPORT, 06_RAW_FORMULA_LIST, conversation.md (structure map).  
- **Constants:** c, α⁻¹, Ϟ_H, k_p, k_⊙, R_⊙, r_c(☉), P_∞, P_conf, ρ_s, ξ, T_CMB, z_boundary, R_uni, κ, Δ_topo.  
- **Symbol index:** R, r, Ω, O, Ϟ, k, κ, r_c, z, v(r), β, a(r), and related notation with chapter references.  
- **Short tables:** Solar, hydrogen, proton/trefoil, nuclear, CMB.  
- **Word count:** See 00_TREATISE_TITLE_AND_TOC.md.

---

*Book 16 — Extended reference. No new physics; authority remains SDT_CORE_AXIOMS_AND_DATASET and the treatise chapters 1–13.*


---
## Index

### Formulas (F1–F17)
| ID | Statement | Chapter |
|----|--------|--------|
| F1 | v² = c² R_c/r; v(r) = (c/k)√(R_phys/r) | 3 |
| F2 | z · k² = 1 | 4 |
| F3 | k = c/v_surface; k_solar = k_proton² | 4 |
| F4 | Trefoil: k_p² = 5 α⁻¹; κ ≈ 0.694 | 5 |
| F5 | Deuteron E_bind ≈ 3 k_e e²/D (p-p-e) | 10 |
| F6 | Pressure hierarchy P_∞, P_conf, ρ_s | 10 |
| F7 | 48 Gyr; z_boundary ≈ 1090 | 11 |
| F8 | v_rot = π v_orb²/c | 7 |
| F9 | O(r) = R²/(4r²) | 2 |
| F10 | a(r) = c² R_c/r² | 3 |
| F11 | Nuclear kinetic/confinement κ = 1/√2 | 10 |
| F12 | μ_p = e c R/(2√2) | 5 |
| F13 | Shapiro Δt = (4R/(Ϟ²c)) ln(4r₁r₂/b²) | 9 |
| F14 | Perihelion Δω = 6πR/(Ϟ²a(1−e²)) | 9 |
| F15 | P_spation(r) = ρ_s c² R_uni/r | 11 |
| F16 | v_escape = √2 × c/Ϟ | 3 |
| F17 | Ϟ(r) = √(r/r_c) | 3 |

### Benchmarks
| ID | Short description | Chapter |
|----|-------------------|--------|
| B1 | Geometric foundation O(r)=R²/(4r²) | 2 |
| B2 | Koppa anchor Ϟ_H = 137.036 | 6 |
| B3 | Centripetal force F = m_e v²/a₀ | 6 |
| B4 | Hydrogen spectrum | 6 |
| B5 | Solar Ϟ three routes; z×k² = 1 | 7 |
| B6 | Solar system orbits | 7 |
| B7 | Jovian system | 7 |
| B8 | Exoplanetary validation | 7 |
| B9 | Ten Rules codified | 8 |
| B10 | Paradox resolution | 8 |
| B11 | Classical tests (light deflection, Shapiro, perihelion) | 9 |
| B12 | CMB interpretation | 11 |
| D-01 | Deuteron binding | 10 |
| S-01 | Screening factor ξ | 12 |

### Symbols (quick reference)
- **Ϟ, k** — velocity ratio c/v_surface; at c-boundary Ϟ = 1. **R, R_phys** — physical radius. **R_c, r_c** — c-boundary radius = R_phys/k². **r** — radial distance. **z** — gravitational redshift; z·k² = 1. **κ** — nuclear virial 1/√2 (nuclear first-principles). **Ω, O** — solid angle, occlusion. See Chapter 16 for full symbol index.

### Rules 1–10 (summary)
1. Occlusion O(r)=R²/(4r²). 2. a(r)=c²R/(Ϟ²r²). 3. Ϟ≡c/v_surface. 4. v(r)=(c/Ϟ)√(R/r). 5. v_surface=c/Ϟ. 6. v_escape=√2×c/Ϟ. 7. Three routes to Ϟ (orbital, spectral, rotation). 8. Superposition. 9. r_c=R/Ϟ²; at r_c Ϟ=1. 10. Scale invariance. See Chapter 8 for full list.

---
*Consolidated from SDT Core Treatise chapters. Verification scratch pad: SCRATCH_PAD_VERIFICATION.md.*
