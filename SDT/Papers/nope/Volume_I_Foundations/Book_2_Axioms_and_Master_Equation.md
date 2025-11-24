# Volume I: Foundations
## Book 2: Axioms and Master Equation

**Source:** atomica sentis.md, Phase 1 (Axioms), Phase 20 (Master Equation)  
**Equation Numbering:** I.2.Chapter.Section.Equation

---

## Introduction to Book 2

This book establishes the formal mathematical framework of Spatial Displacement Theory. The four ingredients described in Book 1 are here unified into four axioms and a single master equation that governs all physical phenomena.

**Cross-Reference:** This book builds directly on Book 1. The four ingredients (Space, Matter, Movement, Now) are formalized as Axioms 1-4, and their interaction is captured in the Master Displacement Equation.

---

## Chapter 1: SDT Axioms 1-4

### Section 1.1: Axiom 1 — Space Is a Pressurised Spation Lattice

**Formal Statement:**

Space is a pressurized spation lattice. The boundary of last scattering (CMB horizon) represents the densest region and produces inward isotropic pressure:

$$P_{\text{CMB}} = \text{constant at local scale} \tag{I.2.1.1.1}$$

**Physical Meaning:**

- Spation fills all space
- Pressure is isotropic (same from all directions)
- Pressure originates from the CMB boundary
- At local scales, pressure is effectively constant

**Mathematical Representation:**

The pressure field at any point x is:

$$\Pi(\mathbf{x}) = \int_{4\pi} I_\infty(\hat{\mathbf{n}}) [1 - E(\mathbf{x}, \hat{\mathbf{n}})] d\Omega \tag{I.2.1.1.2}$$

Where I_∞(n̂) is the incoming pressure from direction n̂, and E(x,n̂) is the occlusion function.

**Connection to Book 1:**

This axiom formalizes the "Space" ingredient from Book 1, Chapter 1. The spation medium with bulk modulus K_bulk = 4.6×10¹¹³ Pa is the foundation.

**Cross-Reference:** See Volume I, Book 1, Chapter 1, Section 1.3 for the pressure field formulation.

### Section 1.2: Axiom 2 — Matter Excludes Spations

**Formal Statement:**

Every particle has a physical radius and forms an exclusion shell. Matter displaces spation, creating regions where spation cannot occupy.

**Mathematical Representation:**

For a particle with exclusion radius R:

$$V_{\text{disp}} = \frac{4\pi}{3} R^3 \tag{I.2.1.2.1}$$

**Physical Meaning:**

- Particles are not points but extended structures
- Each particle excludes a volume V_disp of spation
- This exclusion creates boundaries
- Boundaries are where interactions occur

**Examples:**

- **Electron:** R_e ≈ 10⁻²¹ m, V_disp,e ≈ 4.19×10⁻⁶³ m³
- **Proton:** R_p = 8.4×10⁻¹⁶ m, V_disp,p ≈ 1836 × V_disp,e

**Connection to Book 1:**

This axiom formalizes the "Matter" ingredient from Book 1, Chapter 2. Displacement structures (toroidal vortices) exclude spation volume.

**Cross-Reference:** See Volume I, Book 1, Chapter 2, Section 2.2 for displacement volume calculations.

### Section 1.3: Axiom 3 — Occlusion Creates Pressure Imbalance

**Formal Statement:**

Any object blocks a solid angle of incoming pressure. This creates a pressure imbalance that manifests as force.

**Mathematical Representation:**

For a sphere of radius R viewed from distance r, the occlusion function is:

$$E(\mathbf{x}, \hat{\mathbf{n}}) = \frac{R^2}{4r^2} \quad \text{(for small angles)} \tag{I.2.1.3.1}$$

**Physical Meaning:**

- Matter blocks incoming pressure from some directions
- Pressure from blocked directions is reduced
- This creates pressure gradients
- Pressure gradients create forces

**Limiting Cases:**

- **E → 0:** Negligible occlusion (atomic scales) → Coulomb force
- **E → 1:** Strong occlusion (planetary scales) → Gravitational force

**Connection to Book 1:**

This axiom formalizes how "Movement" (shunt dynamics) creates pressure imbalances. The occlusion function E(x,n̂) quantifies directional shadowing.

**Cross-Reference:** See Volume I, Book 1, Chapter 1, Section 1.3 for the occlusion function in the pressure field equation.

### Section 1.4: Axiom 4 — Force = Pressure Imbalance × Cross-section

**Formal Statement:**

Force equals pressure imbalance times cross-section. This is deterministic—no fields, no potentials, no probabilities.

**Mathematical Representation:**

$$\mathbf{F} = -V_{\text{disp}} \nabla \Pi(\mathbf{x}) \tag{I.2.1.4.1}$$

Where:
- **F:** Force [N]
- **V_disp:** Displacement volume [m³]
- **∇Π:** Pressure gradient [Pa/m]

**Physical Meaning:**

- Force is geometric, not fundamental
- Force emerges from pressure gradients
- Larger displacement volume → larger force
- Stronger pressure gradient → larger force

**Dimensional Check:**

[F] = [m³] × [Pa/m] = [m³] × [N/m³] = [N] ✓

**Connection to Book 1:**

This axiom formalizes how "Movement" (shunt dynamics) creates forces. The cumulative effect of shunts creates pressure gradients, which create forces.

**Cross-Reference:** See Volume I, Book 1, Chapter 3 for shunt dynamics and Volume I, Book 3 for force derivation.

### Section 1.5: Sufficiency of the Four Axioms

**These four axioms are sufficient:**

- No additional postulates needed
- No probabilistic assumptions
- No field-theoretic assumptions
- No relativistic assumptions (relativity emerges)

**What these axioms replace:**

| Conventional Framework | SDT Axioms |
|----------------------|------------|
| Quantum postulates | Axioms 1-4 + geometry |
| Field equations | Master equation (Chapter 2) |
| Spacetime curvature | Pressure field topology |
| Virtual particles | Pressure disturbances |

**All of physics emerges from these four axioms plus geometry.**

---

## Chapter 2: Master Displacement Equation

### Section 2.1: The Master Equation

**The Master Displacement Equation:**

$$\boxed{\nabla \cdot \left[ K_{\text{bulk}} \nabla \Delta(\mathbf{x}) \right] = -\kappa \rho_{\text{disp}}(\mathbf{x}) \left(1 - E(\mathbf{x})\right)} \tag{I.2.2.1.1}$$

Where:
- **K_bulk:** Bulk modulus of spation [Pa] = 4.6×10¹¹³ Pa
- **Δ(x):** Displacement potential [m]
- **κ:** Geometric efficiency factor [dimensionless] ≈ 1
- **ρ_disp(x):** Displacement density [m⁻³ or dimensionless]
- **E(x):** Occlusion function [dimensionless]

**Physical Interpretation:**

This equation states that the divergence of the pressure gradient (left side) equals the displacement density reduced by occlusion (right side).

**What This Equation Replaces:**

- ❌ Newton's law of gravitation
- ❌ Coulomb's law
- ❌ Schrödinger equation
- ❌ Einstein field equations
- ❌ Quantum field theory Lagrangians

**With pure geometry.**

### Section 2.2: Derivation from Axioms

**From Axiom 1 (Pressurized Spation):**

Pressure field exists: Π(x) = K_bulk ∇Δ(x)

**From Axiom 2 (Matter Excludes Spations):**

Displacement density: ρ_disp(x) quantifies excluded volume

**From Axiom 3 (Occlusion Creates Imbalance):**

Occlusion function: E(x) reduces effective displacement

**From Axiom 4 (Force from Pressure Gradient):**

Force: F = -V_disp ∇Π creates dynamics

**Combining:**

The master equation unifies all four axioms into a single mathematical framework.

**Cross-Reference:** See Volume I, Book 1 for the physical foundation of each axiom.

### Section 2.3: Limiting Cases

**Case 1: E → 0 (Atomic Scales)**

For atomic systems, occlusion is negligible:

$$E(\mathbf{x}) \approx 0 \tag{I.2.2.3.1}$$

The master equation becomes:

$$\nabla \cdot \left[ K_{\text{bulk}} \nabla \Delta(\mathbf{x}) \right] = -\kappa \rho_{\text{disp}}(\mathbf{x}) \tag{I.2.2.3.2}$$

**Solution:** Coulomb potential form

$$\Delta(r) \propto -\frac{1}{r} \tag{I.2.2.3.3}$$

**Result:** Coulomb force emerges

$$F = -\nabla \Pi \propto \frac{1}{r^2} \tag{I.2.2.3.4}$$

**Cross-Reference:** See Volume II, Book 4, Chapter 1 (Coulomb Force) for detailed derivation.

**Case 2: E → 1 (Planetary Scales)**

For massive objects, occlusion is significant:

$$E(\mathbf{x}) \approx 0.64 \quad \text{(for Earth)} \tag{I.2.2.3.5}$$

The master equation becomes:

$$\nabla \cdot \left[ K_{\text{bulk}} \nabla \Delta(\mathbf{x}) \right] = -\kappa \rho_{\text{disp}}(\mathbf{x}) (1 - 0.64) = -0.36 \kappa \rho_{\text{disp}}(\mathbf{x}) \tag{I.2.2.3.6}$$

**Result:** Gravitational force emerges (screened by factor ~0.36)

**Cross-Reference:** See Volume V, Book 12, Chapter 1 (Gravitation from Spation Pressure Gradients) for detailed derivation.

**Case 3: Intermediate E (Multi-Electron Atoms)**

For many-electron atoms, partial occlusion occurs:

$$0 < E(\mathbf{x}) < 1 \tag{I.2.2.3.7}$$

**Result:** Screening effects emerge

$$Z_{\text{eff}}(r) = Z[1 - E_{\text{inner}}(r)] \tag{I.2.2.3.8}$$

**Cross-Reference:** See Volume II, Book 5, Chapter 1 (Many-Electron Atoms) for detailed treatment.

### Section 2.4: Solutions and Applications

**General Solution:**

For spherical symmetry:

$$\Delta(r) = -\frac{\kappa}{4\pi K_{\text{bulk}}} \int \frac{\rho_{\text{disp}}(\mathbf{r}') (1 - E(\mathbf{r}'))}{|\mathbf{r} - \mathbf{r}'|} dV' \tag{I.2.2.4.1}$$

**Pressure Field:**

$$\Pi(\mathbf{r}) = -K_{\text{bulk}} \nabla \Delta(\mathbf{r}) \tag{I.2.2.4.2}$$

**Force:**

$$\mathbf{F}(\mathbf{r}) = -V_{\text{disp}} \nabla \Pi(\mathbf{r}) \tag{I.2.2.4.3}$$

**Applications Across All Scales:**

- **Atomic:** E→0 → Coulomb force (Volume II)
- **Nuclear:** E→0.64 → Strong force (Volume II, Book 6)
- **Planetary:** E→0.64 → Gravity (Volume V)
- **Stellar:** E→0.64 → Stellar structure (Volume V, Book 13)
- **Galactic:** E→constant → Flat rotation curves (Volume VI, Book 15)
- **Cosmological:** E→1 → CMB horizon (Volume VI, Book 15)

**Cross-Reference:** See Volume VII, Book 18 (Master Equation Applications) for complete treatment across all scales.

---

## Chapter 3: Calibration Procedures

### Section 3.1: Calibration of K_bulk

**Method:**

Require pressure gradients to reproduce Bohr radius a₀.

**Procedure:**

1. Calculate pressure deficit from electron-proton displacement
2. Set pressure gradient to match observed Coulomb force
3. Back-calculate K_bulk from force balance

**Result:**

$$K_{\text{bulk}} = 4.6 \times 10^{113} \text{ Pa} \tag{I.2.3.1.1}$$

**Validation:**

Once calibrated, K_bulk is used universally at all scales:
- ✓ Atomic structure (B02, B03, B05, B06)
- ✓ Planetary orbits (B08)
- ✓ Stellar structure (B12)
- ✓ Gravitational phenomena (B09, B10, B11)

**Cross-Reference:** See Volume VIII, Book 19 for benchmark validations.

### Section 3.2: Calibration of V_disp

**Electron Displacement Volume:**

Calibrated from atomic ground state:

$$V_{\text{disp,e}} = \frac{4\pi}{3} R_e^3 \tag{I.2.3.2.1}$$

Where R_e ≈ 10⁻²¹ m (effective exclusion radius).

**Proton Displacement Volume:**

Calibrated from nuclear structure:

$$V_{\text{disp,p}} \approx 1836 \times V_{\text{disp,e}} \tag{I.2.3.2.2}$$

**Validation:**

Displacement volumes reproduce:
- ✓ Coulomb attraction (B08)
- ✓ Hyperfine structure (B05)
- ✓ Nuclear binding (B18 - under investigation)

**Cross-Reference:** See atomica sentis.md, Section 0.9 for detailed calibration procedures.

### Section 3.3: Calibration of Geometric Factors

**κ (Geometric Efficiency):**

Typically κ ≈ 1 for spherical particles.

**β (Gravitational Parameter):**

$$\beta = \frac{\kappa V_{\text{disp}} K_{\text{bulk}}}{4\pi} \tag{I.2.3.3.1}$$

Replaces GM in conventional physics.

**ξ (Screening Factor):**

$$\xi \sim 10^{-9} \tag{I.2.3.3.2}$$

Explains gravity's weakness relative to electromagnetism.

**Cross-Reference:** See Volume V, Book 12, Chapter 3 for β parameter and Volume VII, Book 17, Chapter 2 for screening factors.

---

## Chapter 4: Dimensional Analysis Framework

### Section 4.1: Fundamental Dimensions

**Base Units (SI):**

- **Length:** meter [m]
- **Mass:** kilogram [kg]
- **Time:** second [s]
- **Current:** ampere [A]
- **Temperature:** kelvin [K]

**SDT Fundamental Quantities:**

- **K_bulk:** [Pa] = [kg/(m·s²)]
- **V_disp:** [m³]
- **ρ_disp:** [m⁻³] or [dimensionless]
- **E:** [dimensionless]
- **Π:** [Pa] = [kg/(m·s²)]

### Section 4.2: Derived Quantities

**Force:**

$$[F] = [V_{\text{disp}}] \times [\nabla \Pi] = [m^3] \times [Pa/m] = [N] = [kg·m/s^2] \tag{I.2.4.2.1}$$

**Energy:**

$$[E] = [h] \times [\nu] = [J·s] \times [s^{-1}] = [J] = [kg·m^2/s^2] \tag{I.2.4.2.2}$$

**Pressure:**

$$[\Pi] = [K_{\text{bulk}}] \times [\nabla \Delta] = [Pa] \times [m/m] = [Pa] = [kg/(m·s^2)] \tag{I.2.4.2.3}$$

### Section 4.3: Dimensionless Parameters

**Fine Structure Constant:**

$$\alpha = \frac{e^2}{4\pi \varepsilon_0 \hbar c} = 7.2973525693 \times 10^{-3} \tag{I.2.4.3.1}$$

**Emerges from:** Vortex geometry (not fundamental)

**Screening Factor:**

$$\xi \sim 10^{-9} \tag{I.2.4.3.2}$$

**Emerges from:** Occlusion geometry

**Geometric Efficiency:**

$$\kappa \approx 1 \tag{I.2.4.3.3}$$

**Emerges from:** Particle shape

**Cross-Reference:** See Volume X, Book 25 (Constants and Units) for complete dimensional analysis tables.

---

## Summary of Book 2

This book has established:

1. **Four Axioms:** Formal statements of the four ingredients
2. **Master Equation:** Single equation governing all physics
3. **Calibration:** Procedures for determining constants
4. **Dimensional Framework:** Complete dimensional analysis

**Next:** Volume I, Book 3: The Derivation Tree — showing how all observables emerge from the four ingredients and master equation.

---

**End of Book 2**

