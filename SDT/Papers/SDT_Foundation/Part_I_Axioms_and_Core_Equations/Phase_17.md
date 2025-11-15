# Phase 16 — Universal c-Boundary Geometry (Ϟ and ϟ)

## 1. Definitions: Ϟ as Velocity Ratio, ϟ as c-Boundary Position

- **Ϟ (velocity factor):** Dimensionless ratio encoding orbital speed as a fraction of $c$.

  At a reference radius $R$ (usually the effective surface or mass shell of the parent body), define the orbital velocity
  $$v(R) = \frac{c}{\,Ϟ\,}$$
  so that
  $$\frac{v(R)}{c} = \frac{1}{Ϟ} \quad \Rightarrow \quad Ϟ = \frac{c}{v(R)}.$$

- **ϟ (c-boundary position):** Geometric locus (radius) where the local tangential speed reaches $c$.

  By definition, at radius $r = ϟ$,
  $$v(ϟ) = c.$$

In SDT, Ϟ and ϟ always appear together:

- Ϟ is **how fast** a given orbit is, as a ratio fraction of $c$.
- ϟ is **where** the $c$-speed boundary sits in the same gravity well.

Both are purely geometric: independent of units and tied only to the spatial displacement structure.

---

## 2. Orbital Law with Ϟ and the c-Boundary ϟ

From Phase 15, the SDT orbital law in a spherically symmetric well is
$$v(r) = \frac{c}{Ϟ} \sqrt{\frac{R}{r}}$$
for orbits referenced to radius $R$ with surface speed $v(R) = c/Ϟ$.

Imposing the c-boundary condition $v(ϟ) = c$ gives
$$c = \frac{c}{Ϟ} \sqrt{\frac{R}{ϟ}} \quad \Rightarrow \quad 1 = \frac{1}{Ϟ} \sqrt{\frac{R}{ϟ}}.$$
Solving for ϟ:
$$\sqrt{\frac{R}{ϟ}} = Ϟ \quad \Rightarrow \quad \frac{R}{ϟ} = Ϟ^2 \quad \Rightarrow \quad ϟ = \frac{R}{Ϟ^2}.$$

**Key invariant:**
> For any parent body with surface orbital speed $v(R) = c/Ϟ$, the c-boundary radius is fixed by
> $$ϟ = \dfrac{R}{Ϟ^2}.$$

This relation is universal: it holds for the Sun, planets, compact objects, and any spherically scaled mass distribution within SDT.

---

## 3. Internal Extension and Schwarzschild Ladder

The same orbital law can be extended formally to radii $r < R$ (internal gradient), keeping the same square-root structure:
$$v(r) = \frac{c}{Ϟ} \sqrt{\frac{R}{r}}, \quad 0 < r \le R.$$

For strongly curved wells, introduce the Schwarzschild radius $r_S$ from Phase 15. Then SDT adopts the standard ladder:

- At $r = r_S$:
  $$v_{\text{orb}}(r_S) = \frac{c}{\sqrt{2}} \approx 0.707c,$$
  and the escape velocity there is $v_{\text{esc}}(r_S) = c$.

- At $r = \tfrac{1}{2} r_S$:
  $$v_{\text{orb}}(\tfrac{1}{2} r_S) = c,$$
  so no further stable circular orbits exist inward of $r_S/2$.

More generally, SDT encodes the **orbital/escape ladder**:

- The orbital speed at radius $r$ is the escape speed at $2r$.
- The orbital speed at $r_S$ is the escape speed at $2 r_S$.
- The orbital speed at $2 r_S$ is the escape speed at $4 r_S$, and so on.

This ladder is purely geometric and is preserved under spherical rescalings of the mass distribution. It explains why accretion disks and stable orbits exist around black holes: the well is steep but not singular, and the ϟ boundary marks where circular motion would demand $v = c$.

---

## 4. Solar Example: Ϟ_⊙ and the Sun’s c-Boundary

For the Sun, define $R_\odot$ as the effective solar radius and choose Ϟ_⊙ from the observed surface orbital speed. Using
$$Ϟ_\odot = 686.34,$$
we obtain
$$v_{\text{surf},\odot} = \frac{c}{Ϟ_\odot} = \frac{2.998\times10^8\ \text{m/s}}{686.34} \approx 4.368\times10^5\ \text{m/s} = 436.8\ \text{km/s}.$$

The corresponding c-boundary radius for the solar well is
$$ϟ_\odot = \frac{R_\odot}{Ϟ_\odot^2}.$$

In numerical terms, this evaluates to a radius of order
$$ϟ_\odot \sim 10^3\ \text{m}$$
from the center (the precise value depends on the chosen $R_\odot$ and movement budget partition).

At $r = ϟ_\odot$ the tangential speed required for a circular orbit reaches $c$; inward of ϟ_⊙, strictly circular orbits are no longer physically possible in SDT.

The same Ϟ/ϟ pair can be defined for any star, planet, or compact object by measuring (or assigning) its surface orbital speed and applying
$$v(R) = \frac{c}{Ϟ}, \qquad ϟ = \frac{R}{Ϟ^2}.$$

---

## 5. Venus, Tidal Locking, and Non-Singular Wells

Because SDT treats gravity as a pressure gradient in a finite, compressible spation lattice rather than an infinite singular field, several qualitative consequences follow:

- **Accretion disks exist** because the well is steep but not divergent at the center; material can orbit, shear, and dissipate without falling radially inward in one step.

- **Tidal locking (e.g., Venus)** arises from the long-term exchange of angular momentum in a finite well. In the absence of a moon, the planetary rotation state is determined almost entirely by solar coupling and internal dissipation; no additional exotic mechanism is required.

In all cases, the Ϟ of the body (its surface speed as a fraction of $c$) and the associated ϟ (its c-boundary radius) fix the geometric scaffolding on which these dynamical processes play out.

---

## 6. Role of Phase 16 in the SDT Program

Phase 16 is the last **concrete geometric** phase before SDT moves into higher abstraction (field mappings, spectral operators, and cosmological scaling). Its role is to:

1. **Pin down notation:** Ϟ as the velocity factor $c/v$, ϟ as the c-boundary locus $v=c$.
2. **Establish the universal relation:** $ϟ = R / Ϟ^2$ for any spherically scaled mass distribution.
3. **Provide a bridge:** Connect the orbital law of Phase 15 with later abstraction, where Ϟ and ϟ appear as parameters in spectral, thermodynamic, and cosmological operators.

All subsequent phases may treat Ϟ and ϟ as given primitives, already grounded in this concrete geometric phase