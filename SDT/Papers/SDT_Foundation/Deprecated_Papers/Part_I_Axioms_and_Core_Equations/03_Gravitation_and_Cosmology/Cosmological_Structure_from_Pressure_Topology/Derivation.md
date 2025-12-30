# Section 6.1: Universal c-Boundary Geometry

**Source:** Phase 16  
**Scale:** Stellar to universal  
**Phenomena:** Orbital velocity scaling, c-boundary radius, Schwarzschild ladder

---

## 1. Definitions: Ϟ as Velocity Ratio, ϟ as c-Boundary Position

### 1.1 Ϟ (Velocity Factor)

**Ϟ** is a dimensionless ratio encoding orbital speed as a fraction of $c$.

At a reference radius $R$ (usually the effective surface or mass shell of the parent body), define the orbital velocity:
$$v(R) = \frac{c}{\vartheta}$$

so that:
$$\frac{v(R)}{c} = \frac{1}{\vartheta} \quad \Rightarrow \quad \vartheta = \frac{c}{v(R)} \tag{1.1}$$

**Physical meaning:** $\vartheta$ measures how fast a given orbit is, as a ratio fraction of $c$.

### 1.2 ϟ (c-Boundary Position)

**ϟ** is the geometric locus (radius) where the local tangential speed reaches $c$.

By definition, at radius $r = \vartheta$:
$$v(\vartheta) = c \tag{1.2}$$

**Physical meaning:** $\vartheta$ is where the $c$-speed boundary sits in the gravity well.

### 1.3 Relationship

In SDT, $\vartheta$ and $\vartheta$ always appear together:
- $\vartheta$ is **how fast** a given orbit is, as a ratio fraction of $c$
- $\vartheta$ is **where** the $c$-speed boundary sits in the same gravity well

Both are purely geometric: independent of units and tied only to the spatial displacement structure.

---

## 2. Orbital Law with Ϟ and the c-Boundary ϟ

### 2.1 SDT Orbital Law

From Section 5.1, the SDT orbital law in a spherically symmetric well is:
$$v(r) = \frac{c}{\vartheta} \sqrt{\frac{R}{r}} \tag{2.1}$$

for orbits referenced to radius $R$ with surface speed $v(R) = c/\vartheta$.

### 2.2 c-Boundary Condition

Imposing the c-boundary condition $v(\vartheta) = c$:
$$c = \frac{c}{\vartheta} \sqrt{\frac{R}{\vartheta}} \quad \Rightarrow \quad 1 = \frac{1}{\vartheta} \sqrt{\frac{R}{\vartheta}}$$

Solving for $\vartheta$:
$$\sqrt{\frac{R}{\vartheta}} = \vartheta \quad \Rightarrow \quad \frac{R}{\vartheta} = \vartheta^2 \quad \Rightarrow \quad \vartheta = \frac{R}{\vartheta^2} \tag{2.2}$$

**Key invariant:**
> For any parent body with surface orbital speed $v(R) = c/\vartheta$, the c-boundary radius is fixed by
> $$\boxed{\vartheta = \frac{R}{\vartheta^2}} \tag{2.3}$$

This relation is **universal**: it holds for the Sun, planets, compact objects, and any spherically scaled mass distribution within SDT.

---

## 3. Internal Extension and Schwarzschild Ladder

### 3.1 Internal Gradient

The same orbital law can be extended formally to radii $r < R$ (internal gradient), keeping the same square-root structure:
$$v(r) = \frac{c}{\vartheta} \sqrt{\frac{R}{r}}, \quad 0 < r \le R \tag{3.1}$$

### 3.2 Schwarzschild Radius

For strongly curved wells, introduce the Schwarzschild radius $r_S$ from Section 5.1. Then SDT adopts the standard ladder:

**At $r = r_S$:**
$$v_{\text{orb}}(r_S) = \frac{c}{\sqrt{2}} \approx 0.707c$$

and the escape velocity there is $v_{\text{esc}}(r_S) = c$.

**At $r = \tfrac{1}{2} r_S$:**
$$v_{\text{orb}}(\tfrac{1}{2} r_S) = c$$

so no further stable circular orbits exist inward of $r_S/2$.

### 3.3 Orbital/Escape Ladder

More generally, SDT encodes the **orbital/escape ladder**:

- The orbital speed at radius $r$ is the escape speed at $2r$
- The orbital speed at $r_S$ is the escape speed at $2 r_S$
- The orbital speed at $2 r_S$ is the escape speed at $4 r_S$, and so on

This ladder is purely geometric and is preserved under spherical rescalings of the mass distribution. It explains why accretion disks and stable orbits exist around black holes: the well is steep but not singular, and the $\vartheta$ boundary marks where circular motion would demand $v = c$.

---

## 4. Solar Example: Ϟ_⊙ and the Sun's c-Boundary

### 4.1 Solar Parameters

For the Sun, define $R_\odot$ as the effective solar radius and choose $\vartheta_\odot$ from the observed surface orbital speed.

Using:
$$\vartheta_\odot = 686.34$$

we obtain:
$$v_{\text{surf},\odot} = \frac{c}{\vartheta_\odot} = \frac{2.998 \times 10^8 \text{ m/s}}{686.34} \approx 4.368 \times 10^5 \text{ m/s} = 436.8 \text{ km/s}$$

### 4.2 Solar c-Boundary

The corresponding c-boundary radius for the solar well is:
$$\vartheta_\odot = \frac{R_\odot}{\vartheta_\odot^2}$$

In numerical terms, this evaluates to a radius of order:
$$\vartheta_\odot \sim 10^3 \text{ m}$$

from the center (the precise value depends on the chosen $R_\odot$ and movement budget partition).

**Physical meaning:** At $r = \vartheta_\odot$ the tangential speed required for a circular orbit reaches $c$; inward of $\vartheta_\odot$, strictly circular orbits are no longer physically possible in SDT.

### 4.3 Universal Application

The same $\vartheta$/$\vartheta$ pair can be defined for any star, planet, or compact object by measuring (or assigning) its surface orbital speed and applying:
$$v(R) = \frac{c}{\vartheta}, \qquad \vartheta = \frac{R}{\vartheta^2} \tag{4.1}$$

---

## 5. Physical Consequences

### 5.1 Accretion Disks

Because SDT treats gravity as a pressure gradient in a finite, compressible spation lattice rather than an infinite singular field, **accretion disks exist** because:
- The well is steep but not divergent at the center
- Material can orbit, shear, and dissipate without falling radially inward in one step

### 5.2 Tidal Locking

**Tidal locking** (e.g., Venus) arises from the long-term exchange of angular momentum in a finite well. In the absence of a moon, the planetary rotation state is determined almost entirely by solar coupling and internal dissipation; no additional exotic mechanism is required.

### 5.3 Non-Singular Wells

In all cases, the $\vartheta$ of the body (its surface speed as a fraction of $c$) and the associated $\vartheta$ (its c-boundary radius) fix the geometric scaffolding on which these dynamical processes play out.

---

## 6. Summary

### 6.1 Core Results

**Velocity factor:**
$$\boxed{\vartheta = \frac{c}{v(R)}}$$

**c-Boundary radius:**
$$\boxed{\vartheta = \frac{R}{\vartheta^2}}$$

**Orbital velocity law:**
$$\boxed{v(r) = \frac{c}{\vartheta} \sqrt{\frac{R}{r}}}$$

### 6.2 Key Achievements

✓ **Universal relation** — $\vartheta = R/\vartheta^2$ for any spherically scaled mass  
✓ **Geometric foundation** — purely spatial displacement structure  
✓ **Schwarzschild ladder** — orbital/escape speed relationship  
✓ **Non-singular wells** — explains accretion disks and stable orbits

### 6.3 Physical Interpretation

- $\vartheta$ measures orbital speed as fraction of $c$
- $\vartheta$ marks where $v = c$ boundary sits
- Universal relation connects geometry to dynamics
- Non-singular wells allow stable internal orbits

---

## 7. Connection to Other Sections

- **Section 5.1:** Builds on gravitational pressure gradients
- **Section 6.2:** Extends to exoplanetary systems
- **Section 1.2:** Uses similar quantization (Rydberg)

---

**Status:** CERTIFIED ✓  
**Cross-reference:** Part I, Phase 16

