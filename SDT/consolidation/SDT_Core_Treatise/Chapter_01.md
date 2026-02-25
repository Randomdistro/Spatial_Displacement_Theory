# Chapter 1: Introduction, Primitives, and Notation

## Context and scope

This document is the **Spatial Displacement Theory (SDT) Core Treatise**: a structured exposition of the core axioms, benchmarks, and formulas that define the SDT physics engine. The treatise does not introduce new physics beyond what is already certified in the primary dataset (*SDT Core Axioms & Mathematical Dataset*, Parts I–III). Its purpose is to organise that content into a single, readable reference with consistent notation, clear derivation steps, and explicit cross-references to benchmarks and formulas. Each chapter is self-contained enough to support study and implementation, while the whole forms a continuous narrative from geometric foundations through atomic and stellar validation to nuclear structure and cosmology.

This first chapter does three things. It states the **system instruction** that defines how the framework is to be implemented; it introduces the **four irreducible primitives** (matter, space, movement, now) and the **Euclidean lattice** of discrete units (spations) that constitute the medium; and it fixes **notation** (Ϟ, ϟ, k, κ) and the **scope** of the treatise. It then gives the **calculation order** (the sequence of steps for applying the framework to any scale) and the **falsification vectors** (where empirical or theoretical checks could contradict the model). A reader who finishes this chapter will know what SDT assumes, how to read the rest of the document, and how to use it for calculation and validation.

**Working title of the treatise:** *Spatial Displacement Theory: Core Axioms, Benchmarks, and Formulas.*

---

## System instruction

The following instruction is to be treated as the foundational specification for the SDT model:

*Implement the following mathematical framework as the foundational physics engine for the Spatial Displacement Theory (SDT) model. This dataset supersedes standard General Relativity and Quantum Chromodynamics formulations within this context. The universe is defined as a Euclidean lattice of discrete units (spations) under hydrostatic pressure from a cosmic boundary.*

In practice this means:

1. **Physics engine.** All dynamical predictions—orbital velocities, redshifts, accelerations, escape speeds, classical tests, nuclear binding, CMB interpretation—are to be derived from the axioms and formulas in the dataset, not from Newton’s law of gravitation, Einstein’s field equations, or QCD Lagrangians when operating within the SDT context.

2. **Supersession in context.** Where SDT and standard GR or QCD give different interpretations or formulas, the SDT formulation is the one to use for this framework. For example, “gravity” is not curvature of spacetime but the dynamical effect of a pressure gradient in the spation medium; “strong” nuclear effects are not a separate force but the same pressure and velocity field (Ϟ and ϟ at nucleon scale; nucleon surface Ϟ = √2).

3. **Universe definition.** The universe is not an expanding spacetime manifold with a Big Bang singularity. It is a **Euclidean** space (flat, infinite or very large) populated by a **lattice of discrete units** called spations, and the whole is under **hydrostatic pressure** from a **cosmic boundary** (identified with the CMB shell at redshift z ≈ 1090). That pressure, and the pressure differentials caused by matter displacing spations, drive all the phenomena that SDT models.

The rest of this chapter unpacks the primitives and the medium implied by this instruction, then fixes notation and implementation logic.

---

## Four irreducible primitives

SDT is built from four primitives. They are not derived from prior physics; they are the minimum set needed to construct the theory. Each is **irreducible** (it cannot be defined in terms of the others) and **unique** (no alternative serves the same role).

**Space (S).** Space is a discrete medium of identical units called **spations**. Each spation is a sphere of diameter 1.616×10⁻³⁵ m—the fundamental length. The spation has no internal structure; it is the smallest unit of spatial extension. Space is the collection of all spations: incompressible and contiguous. Thus “empty” space is not nothing; it is a packed lattice of spations. When we speak of the “spation medium,” we mean this lattice and the pressure it sustains.

**Matter (M).** Matter is substance under continuous compression from the moment of its formation to the present. Matter **displaces** spations: it excludes them from its volume. The cumulative pressure history of the universe acts on every material object. This exclusion creates pressure differentials between the interior of a body and the surrounding medium, and between different regions of the medium. In SDT, “mass” and “gravitational” effects are not primitive; they emerge from how matter displaces the medium and how the medium responds with a pressure gradient.

**Movement (Δ).** Movement is the shunting of spations around material boundaries. It propagates at velocity **c = 299,792,458 m/s**. This is not a speed limit imposed on matter; it is the propagation rate of the medium itself. Nothing in the medium can outrun the medium’s own response. So c is the characteristic speed of the spation field—the speed at which pressure changes and displacement patterns propagate. Light, in this picture, is a wave or disturbance in the medium; its speed is c.

**Now (τ).** Now is the ever-present moment—the instantaneous state that defines simultaneity across the medium. Now is not duration; it is the boundary between what has occurred and what has not. All interactions occur at Now. The medium has no memory; each moment is complete in itself. This primitive underlies the use of equilibrium and steady-state conditions in the derivations (e.g. hydrostatic equilibrium): we are always “at Now,” and the velocity and pressure fields are taken as time-independent unless otherwise specified.

**What is not primitive.** Energy, force, and acceleration are **not** primitive. They are geometric consequences of pressure differentials in the medium. The numerical relationships between them (e.g. F = m v²/r for centripetal force, or a = c² R/(Ϟ² r²) for radial acceleration) emerge from the geometry and the velocity field; they are not inserted as separate laws. So the treatise will often “derive” force or energy from the master orbital equation and occlusion; that is consistent with the primitives.

---

## Euclidean lattice and spation medium

The system instruction states that the universe is a **Euclidean lattice** of discrete units under **hydrostatic pressure** from a **cosmic boundary**. We unpack this here.

**Euclidean.** Geometry is flat. Distances and angles obey Euclidean geometry. There is no curvature of “spacetime”; there is a three-dimensional Euclidean space, and time is a separate parameter. Solid-angle formulas (e.g. the occlusion O(r) = R²/(4r²) in Chapter 2) are derived in this Euclidean space. Classical tests such as light deflection and Shapiro delay are interpreted in SDT as refractive effects in a medium with a radially varying index, not as geodesics in a curved manifold.

**Lattice of discrete units.** Space is not a continuous manifold; it is composed of spations. The lattice structure implies a natural length scale (the spation diameter) and the possibility that phenomena at very small scales are influenced by discreteness (e.g. decoherence or stability conditions). For most of the treatise, we work in the continuum limit where the relevant lengths (orbital radii, wavelengths, nuclear sizes) are large compared with the spation scale, so that the velocity and pressure fields can be treated as smooth.

**Spation medium.** The spations collectively form a medium that can sustain pressure and transmit disturbances at speed c. Matter displaces this medium; the displacement creates a pressure deficit (or gradient) that pulls other matter inward—the SDT analogue of attraction. The pressure at large scales is set by the cosmic boundary (the CMB shell); locally, the pressure is modified by every displacing body. Hydrostatic equilibrium in this medium yields the master orbital equation v² = c² R_c/r (Chapter 3).

**Cosmic boundary.** The boundary is the source of the omnidirectional pressure. It is identified with the surface of last scattering at redshift z ≈ 1090, at a radius R_uni ≈ 48 Gly. The CMB is interpreted as the radiation from that boundary, gravitationally redshifted as it climbs out of the potential well. So the “edge” of the observable universe in SDT is not an initial singularity but a radiating surface that supplies the pressure that fills the lattice.

---

## Notation: Ϟ, ϟ, k, κ

Consistent notation is used throughout the treatise and the dataset.

**Ϟ (koppa, U+03DE).** Ϟ denotes the **variable velocity ratio** at a given radius: Ϟ = c/v, where v is the orbital (or flow) velocity in the medium at that radius. So Ϟ is dimensionless. At the **c-boundary** (the radius where v = c), Ϟ = 1. At the physical surface of a body, Ϟ equals the surface value (often written k). So “Ϟ” can mean either the function Ϟ(r) or the surface value, depending on context.

**ϟ (stigma, U+03DF).** ϟ is the **fixed value at the c-boundary**: ϟ = 1. It is used when one wants to emphasise the normalisation “at the velocity saturation point.” **Even in nuclear** the convention is Ϟ and ϟ (U+03DE, U+03DF); at the c-boundary we always have ϟ = 1.

**k.** In drafting and in many formulas, **k** is used interchangeably with the surface value of Ϟ: **k = c/v_surface**. So k is the inverse of the velocity ratio at the body’s physical surface. For the Sun, k_⊙ ≈ 686.6; for hydrogen (electron at Bohr radius), Ϟ_H = k_H ≈ 137.036. The identity z·k² = 1 (redshift times surface-k squared equals one) uses this k.

**κ (kappa).** In some legacy or dataset phrasing, κ appears for a numerical factor (e.g. 1/√2 at nucleon, or trefoil ≈ 0.694). The **convention** for the velocity ratio and c-boundary is nevertheless **Ϟ and ϟ (U+03DE, U+03DF) at all scales, including nuclear.** At the nucleon surface, if v_surface = c/√2, then the surface value is **Ϟ = c/v_surface = √2**; the symbol is still Ϟ, and at the c-boundary ϟ = 1. So: v_surface = c/Ϟ; v = (c/Ϟ)√(R/r); z·k² = 1; rotation Ϟ = √(πc/v_rot). Even in nuclear it is Ϟ and ϟ.

**Summary.** Ϟ (or k at the surface) = c/v_surface; at the c-boundary, Ϟ = ϟ = 1 (ϟ = U+03DF). Same convention everywhere, including nuclear. R_phys (or R) = physical radius; R_c = c-boundary radius = R_phys/Ϟ²; r = radial distance from the centre.

---

## Scope of the document

The treatise is organised in **three books** and **13 chapters**.

**Book I: Foundations and core mechanics (Chapters 1–5).** Chapter 1 (this chapter) sets primitives, notation, and implementation logic. Chapter 2 establishes the occlusion foundation (solid angle, O(r) = R²/(4r²), Benchmark B1, Formula F9). Chapter 3 presents the master orbital equation (F1), velocity field, acceleration (F10), escape velocity (F16), Ϟ(r) (F17), and scale invariance. Chapter 4 covers the redshift–displacement identity (z·k² = 1), scaling (k_solar = k_proton²), and Rule 7 (three routes to Ϟ). Chapter 5 treats trefoil topology and proton structure (F4, F12, Δ_topo = 5).

**Book II: Atomic to stellar validation (Chapters 6–9).** Chapter 6: hydrogen system and atomic benchmarks (B2, B3, B4); Ϟ_H = 137.036; centripetal force and spectrum. Chapter 7: solar and stellar systems (B5–B8); F8 (rotation coupling); worked examples. Chapter 8: Ten Rules (B9) and paradox resolution (B10). Chapter 9: classical tests of gravitation (B11; F13, F14; light deflection, Shapiro, perihelion).

**Book III: Nuclear, cosmology, and reference (Chapters 10–13).** Chapter 10: nuclear structure and binding (Part I 2.1–2.3; B D-01; F5, F11; nucleon Ϟ = √2, Ϟ and ϟ convention). Chapter 11: cosmology and CMB (48 Gyr radiator, B12, F7, F15). Chapter 12: benchmark suite and certification (B1–B12, D-01, S-01; calculation order and falsification). Chapter 13: standout formulas compendium (F1–F17: statement, derivation, “why it matters,” cross-links).

**Sources.** Primary: *SDT Core Axioms & Mathematical Dataset* (Parts I–III). Supporting: *09_CANONICAL_SDT_FORMULAS.md*, *05_STRUCTURE_MAP.md*, *08_CONSISTENCY_REPORT.md*, and treatise sections in *conversation.md* (structure map line ranges). No new physics is introduced; the treatise only structures and expands existing content.

---

## Calculation order (implementation logic 4.1)

To apply the SDT framework to any given system, follow this **calculation order**:

1. **Define the scale.** Identify the physical surface radius R_phys and either the surface velocity v_surface or the gravitational redshift z (or equivalent observable).

2. **Obtain k.** Compute **k = c/v_surface** if v_surface is known, or **k = 1/√z** if z is known. So k is fixed by dynamics or spectroscopy.

3. **Obtain the c-boundary radius.** **R_c = R_phys / k².** This is the radius at which the orbital velocity in the medium would equal c.

4. **Velocity field.** **v(r) = (c/k) √(R_phys/r)** or equivalently **v(r) = c √(R_c/r).** Use this for orbital speeds at any radius r ≥ R_phys (or r ≥ R_c as appropriate).

5. **If atomic or nuclear:** apply scale-specific rules. For atomic (hydrogen), use Ϟ_H = 137.036 and the Bohr radius/spectrum. For nuclear, the convention is still **Ϟ and ϟ (U+03DE, U+03DF)**; at the nucleon surface Ϟ = √2 (v_surface = c/√2) and trefoil (n = 3, m = 2) where relevant.

This order ensures that body-specific quantities (R_phys, k or z) are taken from observation or from a known scale (e.g. solar k from B5), and that all derived quantities (R_c, v(r), acceleration, escape speed) follow from the same formulas. The calculation order is the same whether the system is a nucleus, a star, or a galaxy; only the numerical values of R and k change.

---

## Falsification vectors (implementation logic 4.2)

The dataset specifies **falsification vectors**—places where experiment or theory could contradict SDT. They are not predictions of failure; they are the agreed checks.

**Atomic.** **Lamb shift.** SDT predicts orbital and spectral structure from the Ϟ framework; the Lamb shift is a subtle effect that may require the discrete structure of the spation medium (e.g. decoherence or finite size) to be fully reproduced. **Orbital scale:** the hydrogen orbital scale is d_orbital ≈ 3.36 α⁻² d_nuclear; consistency of this ratio with observed radii and with nuclear scale (trefoil node) is a check.

**Galactic.** **Rotation curves.** SDT predicts v = c √(R_occ/r) with R_occ (occlusion radius) scaling set by geometry. Flat or rising rotation curves must be explained by the distribution of displacing mass (screening, R_occ) without ad hoc dark matter. A hard-line geometric prediction that could falsify would be a systematic mismatch between observed v(r) and the occlusion-based form for a given mass profile.

**Nuclear.** **³He vs ³H binding.** The difference in binding energy between helium-3 and tritium depends on the geometry of the third nucleon and the electron-mediated (or magnetic) bonding. SDT’s node geometry and the same Ϟ/ϟ framework (nucleon surface Ϟ = √2) must yield the correct trend. A persistent discrepancy that cannot be resolved by improved geometry or screening would count against the framework.

Implementers and reviewers should use these vectors when validating code or comparing SDT to data: success at these points supports the model; clear, repeatable failure would require revision of the axioms or scope.

---

## How to use this treatise

- **By role.** If you are **implementing** the physics engine, start with this chapter (primitives, notation, calculation order), then Chapter 2 (occlusion), Chapter 3 (master equation), and Chapter 12 (benchmark suite and certification). Use Chapter 13 as the formula index. If you are **validating** against benchmarks, use the certification sections in each chapter (e.g. B1 in Chapter 2, B2–B4 in Chapter 6) and the full benchmark list in Chapter 12. If you are **studying** the theory, read Books I–III in order; each chapter opens with context and closes with cross-references and a short summary.

- **Word-count band.** Each chapter is written to fall between 2,680 and 6,064 words (inclusive), with a target of about 3,500–4,500 words where possible. This keeps chapters long enough for full derivations and commentary but bounded for readability. A word-count checklist is provided at the end of the treatise.

- **Cross-references.** Chapters refer to benchmarks (B1–B12, D-01, S-01), formulas (F1–F17), and Rules (1–10) by their standard identifiers. “Part I,” “Part II,” “Part III” refer to the three parts of the primary dataset.

Chapter 2 establishes the geometric foundation: solid angle Ω(r), far-field occlusion O(r) = R²/(4r²), and Benchmark B1, so that the inverse-square behaviour used everywhere else is seen to be geometric only.

---

*Sources: Dataset intro + 4.1–4.2; 05_STRUCTURE_MAP §1–2.*
