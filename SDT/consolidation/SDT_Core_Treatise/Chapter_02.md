# Chapter 2: Geometry and the Occlusion Foundation

## Context and scope

Spatial Displacement Theory (SDT) does not introduce gravity or radiation dilution as separate laws. Instead, it derives both from a single geometric fact: a sphere of radius \(R\) at distance \(r\) blocks a definite fraction of the sky. That fraction—the *occlusion*—is a pure consequence of Euclidean solid-angle geometry. No empirical constants, no mass \(M\), no gravitational constant \(G\) appear in its derivation. This chapter establishes that foundation in full.

Here we (1) define the exact solid angle \(\Omega(r)\) subtended by a sphere of radius \(R\) as seen from a point at distance \(r\), (2) derive the far-field occlusion \(O(r) = R^2/(4r^2)\) and confirm its dimensions, (3) state and certify **Benchmark B1** (Geometric Foundation), and (4) present **Formula F9** (Occlusion) with derivation and commentary. The takeaway is that inverse-square behaviour—in acceleration, flux dilution, and the pressure deficit that SDT identifies with “gravity”—is *geometric only*. It is the same at nuclear, celestial, and galactic scales because it depends only on \(R\) and \(r\), not on scale-specific physics. The rest of the treatise (master orbital equation, redshift identity, hydrogen, solar system, classical tests, cosmology) builds on this one result.

---

## Solid angle: exact formula

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

## Far-field approximation and occlusion

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

## Dimensional analysis

Solid angle is dimensionless in the sense that it is a ratio of areas (sphere cap to radius-squared); the SI derived unit is the steradian (sr), with dimension 1. So \([\Omega] = 1\). The full sky is \(4\pi\) sr, so \(O = \Omega/(4\pi)\) is a pure number: \([O] = 1\). Checking the right-hand side: \(R^2\) and \(r^2\) both have dimension \(\mathsf{L}^2\), so \(R^2/r^2\) is dimensionless. Thus \([O] = 1\) is satisfied. Benchmark B1 explicitly certifies this dimensional consistency: the inverse-square law and occlusion are derived from Euclidean geometry with no empirical parameters, and \([O] = 1\) is verified.

---

## Benchmark B1: Geometric Foundation — full certification

**What is certified:** The inverse-square law and occlusion \(O(r) = R^2/(4r^2)\) are derived from Euclidean solid-angle geometry with no empirical parameters. Dimensional analysis \([O] = 1\) is verified.

**Formulas (certified):**
- Exact solid angle: \(\Omega(r) = 2\pi\left(1 - \sqrt{1 - R^2/r^2}\right)\).
- Far field (\(r \gg R\)): \(\Omega(r) \approx \pi R^2/r^2\).
- Occlusion (fraction of sky blocked): \(O(r) = \Omega/(4\pi) = R^2/(4r^2)\).

**Commentary:** B1 is the foundation of all SDT dynamics. Gravity and radiation dilution both emerge from the same geometric fact: a sphere of radius \(R\) at distance \(r\) blocks a fraction \(R^2/(4r^2)\) of the sky. The pressure deficit in the spation medium scales with this occlusion, giving inverse-square acceleration. No \(G\), no \(M\)—only \(R\) and \(r\). This is why SDT can treat nuclear, celestial, and galactic scales with one velocity law and the identity \(z \cdot k^2 = 1\): the underlying dependence on “size and distance” is the same occlusion.

**Experimental / theoretical check:** Dimensional consistency is confirmed; agreement with the Newtonian limit is obtained when \(k\) and \(R_c\) are identified with \(GM/c^2\) and \(R\) in the appropriate limit. No free parameters are introduced. **Status: CERTIFIED.**

**Commentary (B1).** B1 is the first of the certified benchmarks. It does not depend on any measured constant (other than the geometric use of \(R\) and \(r\)). So “certification” here means: the derivation is logically complete, dimensionally consistent, and sufficient to support all later SDT formulas that depend on inverse-square behaviour. If B1 were false (e.g. if solid angle did not scale as \(R^2/r^2\) in the far field), the entire SDT dynamical structure would need to be rederived. No such failure is known; the Euclidean solid angle is standard geometry.

---

## Formula F9: Occlusion — statement, derivation, and why it matters

**Statement:** Far-field occlusion (fraction of sky blocked by a sphere of radius \(R\) at distance \(r\)) is \(O(r) = R^2/(4r^2)\). The exact solid angle is \(\Omega(r) = 2\pi\left(1 - \sqrt{1 - R^2/r^2}\right)\), and \(O = \Omega/(4\pi)\).

**Derivation (concise):**
1. Solid angle of the spherical cap from \(P\): \(\Omega(r) = 2\pi(1 - \sqrt{1 - R^2/r^2})\).
2. For \(r \gg R\), Taylor expansion gives \(\Omega \approx \pi R^2/r^2\).
3. Occlusion is the fraction of the full sky: \(O = \Omega/(4\pi) = R^2/(4r^2)\).
4. \([O] = 1\) (dimensionless).

**Why it matters:** All inverse-square behaviour in SDT—radial acceleration \(a(r) \propto 1/r^2\), flux dilution, and the pressure gradient that replaces “gravitational” force—stems from this relation. B1 certifies that no physics beyond Euclidean geometry is needed for the foundation. Every later benchmark (B2–B12) and formula (F1–F17) that uses the same \(R\), \(r\), and \(k\) (or Ϟ) structure rests on occlusion. Without B1 and F9, the master orbital equation and the redshift identity would lack their geometric anchor.

**Second commentary (F9).** F9 has no free parameters. Once you choose \(R\) (the radius of the displacing body) and \(r\) (the distance of the test point), \(O(r)\) is fixed. So at 1 AU from the Sun, with \(R_\odot \approx 6.96\times10^8\) m and \(r \approx 1.496\times10^{11}\) m, the occlusion is \(R^2/(4r^2) \approx 2.16\times10^{-6}\). That small number is the fraction of the sky blocked by the Sun; the pressure deficit at Earth’s orbit scales with it, and hence the “gravitational” acceleration toward the Sun also scales with it. The same formula applies to a nucleus occluding the medium at a distance of a few fm: only the numerical values of \(R\) and \(r\) change.

---

## Why inverse-square is geometric only

In SDT, “gravity” is not a separate force mediated by mass. It is the dynamical response of the spation medium to a pressure deficit. That deficit is proportional to the fraction of the sky occluded by the displacing body: the more sky blocked, the larger the local pressure drop and the resulting inward acceleration. Because occlusion is \(O(r) = R^2/(4r^2)\), the deficit, and hence the acceleration, scale as \(1/r^2\). So the inverse-square law is not postulated; it is derived from the geometry of a sphere in Euclidean space.

Consequences:
- **No \(G\) or \(M\) in the foundation.** Body-specific quantities enter later via the c-boundary radius \(R_c = R_{\text{phys}}/k^2\) and the velocity field \(v^2 = c^2 R_c/r\), which themselves tie back to occlusion and the single medium.
- **Scale invariance.** The same \(O(r)\) applies to a nucleus, a star, or a galaxy. Only \(R\) and \(r\) (and the body’s \(k\)) change; the \(1/r^2\) form does not.
- **Radiation and “gravity” unified.** Flux from a compact source also dilutes as \(1/r^2\) because the same solid-angle argument applies to the fraction of the sphere’s surface (or emitting shell) visible at distance \(r\). One geometry underlies both.

This is why the document can speak of a single framework from hydrogen to exoplanets to the CMB: the inverse-square behaviour is geometric only, and the rest is consistent application of the master equation and \(z \cdot k^2 = 1\).

**Worked limits.** At the surface of a body, \(r = R\), the exact formula gives \(\Omega = 2\pi\) and \(O = 1/2\): half the sky is blocked. So the pressure deficit at the surface is maximal (in the sense that the body blocks half of the incoming pressure field from that hemisphere). In the far field, \(O(r) = R^2/(4r^2)\) is the working approximation. For the Sun at 1 AU, \(O \approx 2.16\times10^{-6}\); for a proton of radius \(\sim 0.84\) fm at 1 fm, \(O \sim R^2/(4r^2)\) is of order 0.1–0.2 depending on the exact \(R\) used. So nuclear and stellar systems both obey the same \(O(r)\); only the length scales differ.

---

## Checks and cross-references

- **B1** certifies the geometric foundation and \([O] = 1\); F9 is the occlusion formula.
- **Rule 1** (Ten Rules): occlusion as the basis for the pressure deficit and inverse-square.
- **Rule 2:** acceleration \(a(r) = c^2 R/(\varkappa^2 r^2)\) follows from the pressure gradient that scales with occlusion; F10 gives the same in terms of \(R_c\).
- **F1 (Master orbital equation):** \(v^2 = c^2 R_c/r\) is derived from hydrostatic equilibrium in the same medium whose pressure gradient is set by occlusion; see Chapter 3.
- **F10 (Acceleration):** \(a(r) = c^2 R_c/r^2\) is centripetal \(v^2/r\) with F1; the \(1/r^2\) factor is the same as in \(O(r)\).
- **B2–B12:** All use the same \(R\), \(r\), and \(k\) (or Ϟ) structure that ultimately traces back to B1 and F9.

**Falsification / limits:** B1 is purely geometric; it does not by itself fix \(k\) or \(R_c\) for a given body. Those come from dynamics and spectroscopy (e.g. B2, B5). Disagreement of observed orbits or redshift with the master equation and \(z \cdot k^2 = 1\) would challenge the *use* of occlusion in dynamics, not the correctness of \(O(r) = R^2/(4r^2)\) as solid-angle geometry.

---

## Summary

- **Exact solid angle:** \(\Omega(r) = 2\pi\left(1 - \sqrt{1 - R^2/r^2}\right)\); far field: \(\Omega(r) \approx \pi R^2/r^2\).
- **Occlusion (F9):** \(O(r) = R^2/(4r^2)\); \([O] = 1\).
- **B1** certifies that inverse-square and occlusion come from Euclidean geometry with no empirical parameters.
- Inverse-square in SDT is **geometric only**: same at all scales; no \(G\) or \(M\) in the foundation; radiation dilution and “gravitational” acceleration share the same geometric origin.

Chapter 3 will introduce the master orbital equation and velocity field that use this occlusion-based pressure gradient to give \(v^2 = c^2 R_c/r\) and the full set of orbital and redshift relations.

---

*Sources: Part I §1 (precursor to 1.1), Part II B1, Part III F9; 05_STRUCTURE_MAP §1–2; 09_CANONICAL_SDT_FORMULAS §1.*
