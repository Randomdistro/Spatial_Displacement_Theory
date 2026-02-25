# Chapter 3: Master Orbital Equation and Velocity Field

## Context and scope

Chapter 2 established that inverse-square behaviour—occlusion O(r) = R²/(4r²) and the pressure deficit it implies—rests on Euclidean solid-angle geometry alone. No mass, no coupling constant G; only the radius R of the displacing body and the distance r. This chapter introduces the **single dynamical equation** that converts that geometry into orbital motion: the master orbital equation. It governs the velocity field v(r) around any displacement source, from nucleons to galaxies, and yields acceleration, escape speed, and the radius-dependent velocity ratio Ϟ(r). All of this follows from hydrostatic equilibrium in the spation medium and one boundary condition: at a certain radius (the c-boundary), the orbital velocity equals the speed of light c.

The chapter is organised as follows. First we state the master equation in its two equivalent forms and define every variable (Formula F1 / Axiom 1.1). We then derive it from hydrostatic equilibrium and the c-boundary condition, and clarify what the c-boundary is and is not. Next we derive the radial acceleration (Formula F10, Rule 2), escape velocity (Formula F16, Rule 6), and the radius-dependent koppa Ϟ(r) (Formula F17), and we tie these to Rules 4, 5, and 9. A section on scale invariance shows that the same equation, with the same structure, applies across nuclear, celestial, and galactic scales—with nuclear use of κ = 1/√2 as the only scale-specific tweak. The chapter closes with a concise recap of the calculation order, cross-references to benchmarks (B2, B5, B6, B7, B8, D-01), and falsification vectors, plus a short worked example to fix ideas.

**Notation.** In this treatise, Ϟ (koppa, U+03DE) denotes the variable velocity ratio c/v at a given location; at the c-boundary, Ϟ = 1. The symbol k is used interchangeably for the surface value (k = c/v_surface). R_c is the c-boundary radius (geometric mass); R_phys is the physical surface radius of the body. κ (kappa) is reserved for the nuclear virial factor 1/√2 unless topology specifies otherwise (e.g. trefoil κ ≈ 0.694).

---

## The master orbital equation (F1 / Axiom 1.1)

### Statement and equivalent forms

The velocity field in the spation medium around any compact displacement source is given by:

**Master orbital equation (F1):**
```
v² = c² (R_c / r)
```

Equivalently, in terms of physical radius and the surface velocity ratio k = c/v_surface:

**v(r) = (c/k) √(R_phys / r)**

with the c-boundary radius defined as **R_c = R_phys / k²**. Thus R_c is the radius at which the orbital speed would equal c; it is a geometric length scale, not a physical surface.

In koppa notation: at the surface, Ϟ = k = c/v_surface, so v_surface = c/Ϟ. Then v(r) = (c/Ϟ)√(R/r) with R = R_phys, and R_c = R/Ϟ². The form **v(r) = c √(R_c/r)** follows immediately: at r = R_c, v = c; at r > R_c, v < c.

### Variables

| Symbol | Meaning | Units | Notes |
|--------|--------|--------|--------|
| v | Orbital velocity at radius r | m/s | Tangential speed for circular orbit; same field describes radial free-fall scaling. |
| c | Speed of light (propagation speed of the medium) | m/s | 2.99792458×10⁸ m/s (exact). |
| R_c | c-boundary radius (geometric mass) | m | At r = R_c, v = c. R_c = R_phys/k². |
| r | Radial distance from the geometric centre | m | r ≥ R_phys for external orbits. |
| R_phys | Physical surface radius of the body | m | Surface where v = v_surface = c/k. |
| k (or Ϟ at surface) | Inverse velocity ratio at surface | dimensionless | k = c/v_surface; at c-boundary, Ϟ = 1. |

So the only body-specific inputs are R_phys and k (or, equivalently, R_c). No gravitational constant G and no mass M appear in the equation. The dynamics are fixed by geometry (R, r) and the saturation of the medium at the c-boundary.

### Derivation from hydrostatic equilibrium

The spation medium is in hydrostatic equilibrium. The pressure P decreases outward, and the radial pressure gradient supports the centripetal stress of the flow. For a steady, spherically symmetric velocity field v(r):

(1) **dP/dr = −ρ_s (v²/r)**

where ρ_s is the spation mass density. Pressure is sustained by the displacement flux; the flux scales with v, so the dynamic pressure scales as ρ_s v². Hence:

(2) **P ∝ ρ_s v²**

so that dP/dr ∝ ρ_s (d/dr)(v²). Combining with (1) gives (d/dr)(v²) ∝ −v²/r, i.e. v² ∝ 1/r. The constant of proportionality is set by the boundary condition: at the c-boundary radius R_c, the orbital velocity equals c. Thus:

(3) **v²(R_c) = c²** ⇒ **v²(r) = c² (R_c / r)**

So **v² = c² R_c/r** and **v(r) = c √(R_c/r)**. In terms of surface quantities, v_surface = c/k at r = R_phys, so v²(R_phys) = c²/k² = c² R_c/R_phys, giving R_c = R_phys/k² and v(r) = (c/k)√(R_phys/r). The derivation uses only hydrostatics and the single boundary condition v = c at R_c; no additional free parameters.

**Physical meaning.** The pressure gradient balances the centrifugal stress of the flow; the ratio R_c/r determines how much slower than c the orbit is at radius r. Closer to the source (smaller r), v is larger; at r = R_c, v reaches c. The “geometric mass” R_c is the single length scale that sets the strength of the field: all orbits at a given r respond to the same R_c. That is why one equation suffices from nucleons to galaxies—only R_c (or R_phys and k) changes with the body.

### The c-boundary: meaning and constraint

The **c-boundary** is the radius R_c at which the orbital velocity in the medium equals c. It is the velocity saturation point of the medium: the locus where v = c. It is **not** a singularity. In particular:

- At r = R_c, v = c and Ϟ(r_c) = 1.
- For r > R_c, v < c and Ϟ(r) > 1.
- R_c is related to the physical surface by R_c = R_phys/k². For the Sun, R_phys ≈ 6.96×10⁸ m and k_⊙ ≈ 686.6, so R_c(☉) ≈ 1.48 km—far inside the visible surface.

The same functional form v² = c² R_c/r applies at nuclear, celestial, and galactic scales. At nuclear scale, the surface velocity is v_surface = cκ with κ = 1/√2, so effectively k = 1/κ and the same master equation holds with the κ factor absorbed into the effective R_c or into the surface scaling (see Scale invariance below).

---

## Acceleration (F10) and Rule 2

From the master equation, the centripetal acceleration required to hold a test body in circular motion at radius r is a = v²/r. Substituting v² = c² R_c/r:

**a(r) = c² R_c / r²**

Since R_c = R_phys/k² (or R_c = R_phys/Ϟ²), this is equivalently:

**Formula F10 (acceleration):** **a(r) = c² R_phys / (k² r²) = c² R_c / r²**

**Rule 2 (Pressure-Difference Acceleration):** The radial acceleration toward the source is a(r) = c²R/(Ϟ²r²).

So the “gravitational” acceleration in SDT is the centripetal acceleration of the velocity field. No separate force law is postulated; it follows from the same pressure gradient that gave v² ∝ 1/r. Dimensional check: [c² R_c / r²] = (m/s)² · m / m² = m/s². Again, no G and no M—only R_c (or R_phys and k) and r. In the appropriate limit, this matches the Newtonian form when the geometric parameters are identified with the conventional Schwarzschild or Newtonian scales (Benchmark B6; Chapter 7).

**Why F10 matters.** F10 is the direct link between the master equation and “Newtonian” gravity. Once v² = c² R_c/r is accepted, a = v²/r is unavoidable for circular motion. So the inverse-square acceleration is not a separate law; it is the kinematic consequence of the velocity field. Every benchmark that tests orbital dynamics (B3 centripetal force, B6 planetary orbits) is implicitly testing F10 as well. The same formula applies at nuclear scale when written with κ: the pressure gradient that confines nucleons scales with c² R/(κ² r²).

---

## Escape velocity (F16) and Rule 6

The work required to move a test mass from the surface (or from radius r) to infinity is the integral of the radial force (or a(r)) with respect to r. For a(r) = c² R_c/r², the potential difference from r to infinity scales as c² R_c/r. Equating kinetic energy at launch to this work gives (1/2)v_escape² = c² R_c/r. At the **physical surface** r = R_phys, v_surface = c/k, so the work from R_phys to infinity is (1/2)(c/k)² × (factor from integration). The escape velocity from the surface is:

**Formula F16 (escape velocity):** **v_escape = √2 × c/Ϟ**

Equivalently, **v_escape = √2 × v_surface**. So the escape speed is exactly √2 times the surface orbital speed. This is geometric: the factor √2 arises from the 1/r potential implied by a ∝ 1/r².

**Rule 6 (Escape Velocity Rule):** v_escape = √2 × c/Ϟ.

At nuclear scale, the virial stability limit is κ = v_orb/v_esc = 1/√2 (Chapter 5). So the same √2 relation appears in the orbital-to-escape ratio; the nuclear κ is the inverse of that ratio at the nucleon surface. **Why it matters:** Escape velocity is not a separate postulate; it is the integrated effect of the same a(r). The factor √2 is geometric (from the 1/r potential), and it ties directly to nuclear stability (κ = 1/√2) 
---

## Radius-dependent koppa Ϟ(r) (F17) and Rules 4, 5, 9

The velocity ratio Ϟ is defined at every radius as Ϟ(r) = c/v(r). From v(r) = c√(R_c/r) we have v(r)/c = √(R_c/r), so:

**Formula F17 (radius-dependent koppa):** **Ϟ(r) = √(r / r_c)**

Here r_c = R_c (c-boundary radius). So Ϟ increases with r: at r = r_c, Ϟ = 1; at the physical surface r = R_phys, Ϟ = k = c/v_surface; and at larger r, Ϟ grows as the square root of r/r_c. The “koppa at surface” (k or Ϟ_surface) is the anchor; Ϟ(r) extends the same geometry to all radii.

**Rule 4 (Master Orbital Equation):** v(r) = (c/Ϟ)√(R/r). With Ϟ(r) = √(r/r_c) and R_c = R/Ϟ², this is v(r) = c√(R_c/r), as above.

**Rule 5 (Surface Velocity Rule):** v_surface = c/Ϟ. At r = R_phys, Ϟ = k, so v_surface = c/k.

**Rule 9 (c-Boundary Rule):** r_c = R/Ϟ²; at r = r_c, Ϟ(r_c) = 1 (orbital velocity = c). So the c-boundary is the unique radius where the local koppa equals 1.

Together, Rules 4, 5, and 9 tie the velocity field, surface velocity, and c-boundary into one consistent picture: one parameter (e.g. k or R_c) fixes v(r) everywhere.

**Why F17 matters.** Ϟ(r) is the local “slowness” of the orbit relative to c: at large r, Ϟ is large and v is small. It is the running coupling that connects the surface (where we measure k) to the c-boundary (where Ϟ = 1). In hydrogen, Ϟ_H = 137.036 at the Bohr radius; in the Sun, k_⊙ ≈ 686.6 at the photosphere. F17 says that at any intermediate r, the local ratio is Ϟ(r) = √(r/r_c). So the entire radial profile is fixed by one number (r_c or k). This is why “three routes to solar Ϟ” (B5) all converge: they are three ways to fix the same r_c.

---

## Scale invariance: nuclear, celestial, galactic

The same master equation and the same koppa structure apply across some 53 orders of magnitude in length scale.

**Celestial (planets, moons, exoplanets).** For the Sun, k_⊙ ≈ 686.6 and R_c(☉) ≈ 1.48 km. Planetary orbital velocities satisfy v(r) = (c/k_⊙)√(R_☉/r) = c√(R_c/r) (Benchmarks B5, B6). Jupiter’s satellites obey the same form with Jupiter’s k_J and R_J (B7); exoplanets use the stellar k and R (B8). No G, no M; only R_c (or R and k) and r.

**Nuclear.** At nucleon scale, the surface velocity is not c but cκ with κ = 1/√2 (Chapter 5). So v_surface = c/√2 and the effective “koppa” at the nucleon surface is 1/κ = √2. The velocity field is **v² = c² κ² (R/r)** with the same 1/r dependence. Same equation, with κ² scaling the effective R_c. Kinetic energy per nucleon is (1/2)m_N v² = m_N c²κ²/2 = m_N c²/4; confinement and overlap pressures scale with κ² (Formula F11; Chapter 10). So nuclear dynamics use the same geometric law with κ = 1/√2 at the nucleon surface.

**Galactic.** Flat rotation curves are interpreted in SDT as v = c√(R_occ/r) where R_occ is an occlusion radius (screening or effective displacement radius). The same inverse-square-root form holds; the “flat” curve arises from how R_occ scales with r in the disk (Chapter 8; Benchmark B10). So again: same equation, different scale.

**Rule 10 (Scale Invariance):** Same equations, same Ϟ structure, across nuclear, celestial, and galactic scales. The master equation v² = c² R_c/r (and its nuclear form v² = c²κ²(R/r)) is the single dynamical engine; only the numerical values of R, r_c, and (at nuclear scale) κ change.

**Commentary.** Scale invariance is a falsifiable claim: if orbital velocities at some scale required a different functional form (e.g. v ∝ r rather than v ∝ 1/√r), the framework would fail. Benchmarks B6–B8 (planets, moons, exoplanets) and nuclear first-principles (D-01, F11) are the empirical anchors. The only scale-specific ingredient is κ = 1/√2 at the nucleon surface; elsewhere the surface koppa k is fixed by observation (or by the proton–solar bridge k_⊙ = k_p²).

---

## Calculation order, benchmarks, and falsification

**Calculation order (from Chapter 1 / Part I §4.1).** (1) Define scale: choose R_phys and v_surface (or redshift z). (2) k = c/v_surface or k = 1/√z. (3) R_c = R_phys/k². (4) v(r) = (c/k)√(R_phys/r) = c√(R_c/r). (5) For atomic/nuclear applications, apply trefoil (n=3, m=2) and κ = 1/√2 where appropriate.

**Benchmarks that rest on the master equation.** B2 (Koppa anchor): Ϟ_H = 137.036 from hydrogen; Ϟ = 1 at r_c. B5 (solar Ϟ): three routes to k_⊙ ≈ 686.6; z×k² = 1. B6 (solar system orbits): planetary v(r) from r_c(☉) ≈ 1.48 km; max error < 0.41%. B7 (Jovian system): same v(r) for Galilean moons. B8 (exoplanets): stellar k then v_planet; typical error ~1%. D-01 (deuteron): binding from geometry and κ = 1/√2. All of these use F1, F10, F16, F17 and Rules 2, 4, 5, 6, 9 without introducing new constants.

**Falsification vectors (Part I §4.2).** Atomic: Lamb shift; orbital vs nuclear length scales (d_orbital ≈ 3.36 α⁻² d_nuclear). Galactic: rotation curves; predictions of v = c√(R_occ/r) and R_occ scaling. Nuclear: ³He vs ³H binding from electron-mediated node geometry. A confirmed deviation in these areas would challenge the single-field picture. The master equation F1 is thus the central dynamical statement of SDT; all of B2, B5, B6, B7, B8, and D-01 rely on it without introducing additional empirical constants.

### Worked example: Earth’s orbital velocity

Solar physical radius R_☉ ≈ 6.96×10⁸ m; k_⊙ ≈ 686.6; so R_c(☉) = R_☉/k_⊙² ≈ 1.476×10³ m (about 1.48 km). Earth’s orbital radius r ≈ 1.496×10¹¹ m. Then:

v(r) = c √(R_c/r) ≈ 2.998×10⁸ × √(1476 / 1.496×10¹¹) m/s ≈ 2.998×10⁸ × 9.93×10⁻⁵ ≈ 29.76 km/s.

Observed value ≈ 29.78 km/s; agreement to within 0.1%. No G, no M_☉—only R_c and r (Benchmark B6).

**Second example: Io (Jupiter).** Jupiter’s physical radius R_J ≈ 6.99×10⁷ m; from B7, Jupiter’s k_J is determined by its surface dynamics (rotation or satellite orbits). Io’s orbital radius r ≈ 4.22×10⁸ m. Using the same formula v(r) = c√(R_c/r) with Jupiter’s R_c gives Io’s orbital velocity. B7 certifies max error 0.00% for the Galilean satellites—the same master equation and calculation order apply to planet–moon systems (Rule 10).

---

## Summary

- **F1:** v² = c² R_c/r; v(r) = (c/k)√(R_phys/r); R_c = R_phys/k². Derived from hydrostatic equilibrium and v = c at R_c.
- **F10:** a(r) = c² R_c/r² (Rule 2). Centripetal acceleration of the velocity field; no G, no M.
- **F16:** v_escape = √2 × c/Ϟ (Rule 6). Geometric √2 from 1/r potential.
- **F17:** Ϟ(r) = √(r/r_c). Radius-dependent koppa; Rules 4, 5, 9 tie v(r), v_surface, and c-boundary.
- **Scale invariance:** Same equation at nuclear (κ = 1/√2), celestial, and galactic scales; Rule 10.

The master orbital equation and velocity field are the core dynamics of SDT. Chapters 4 and 5 add the redshift–displacement identity and trefoil proton structure; Chapters 6–9 apply and certify this dynamics from hydrogen to classical tests and paradox resolution.

---

*Word count: ~2,720 (target 2,680–6,064).*

*Sources: SDT_CORE_AXIOMS_AND_DATASET.md Part I §1.1, Part III F1, F10, F16, F17; 09_CANONICAL_SDT_FORMULAS.md §2; 06_RAW_FORMULA_LIST Rules 2, 4, 5, 6, 9.*
