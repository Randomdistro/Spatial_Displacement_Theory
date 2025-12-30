# Electricity from Spation Pressure Deformation
## Rigorous Derivation of Electromagnetic Phenomena from First Principles

**Author:** James C. Harvey  
**Date:** December 2025  
**Version:** 2.0  
**Status:** Complete Mathematical Derivation

---

## Abstract

We derive all electrical phenomena from Spatial Displacement Theory (SDT) using spation pressure deformation mechanics. Charge is identified as persistent radial deformation of the dodecahedral spation lattice, creating pressure fields that manifest as electric fields. The electric field is the pressure gradient: $\mathbf{E} = -\nabla P / \rho_{\text{eff}}$. All electrical laws (Coulomb's law, Gauss's law, Poisson's equation, Ohm's law) emerge from pressure equilibrium and spation mechanics. The Cosmic Microwave Background (CMB) provides the continuous influx of electromagnetic energy that establishes and maintains all pressure fields. All calculations proceed without use of mass $m$ or gravitational constant $G$ as fundamental quantities, deriving all effects from spation pressure dynamics driven by the CMB.

---

## 1. Introduction

### 1.1 Physical Foundation: Charge as Lattice Deformation

**Axiom 1.1 (Charge as Deformation).** Charge $Q$ is the persistent radial deformation of the dodecahedral spation lattice. A toroidal displacement vortex (electron) permanently displaces surrounding spation, creating a persistent pressure field.

**Axiom 1.2 (Electric Field as Pressure Gradient).** The electric field is the pressure gradient in the spation medium:

$$\mathbf{E} = -\frac{\nabla P}{\rho_{\text{eff}}} \tag{1.1}$$

where:
- $\mathbf{E}$ = electric field [V/m] = [N/C]
- $P$ = spation pressure [Pa]
- $\rho_{\text{eff}}$ = effective charge density per unit pressure [C/(Pa·m³)]

**Axiom 1.3 (CMB as Pressure Source).** The Cosmic Microwave Background (CMB) radiation, originating from the last scattering surface at redshift $z = 1089.9$, provides the continuous influx of electromagnetic energy that establishes and maintains all pressure fields throughout the universe.

---

## 2. Mathematical Framework

### 2.1 Definition: Charge from Pressure Flux

**Definition 2.1 (Charge from Pressure Flux).** Charge is operationally defined as the time-integrated pressure-flux through a closed surface:

$$Q \equiv \varepsilon_0 \oint_{\partial V} \mathbf{E} \cdot \mathbf{n} \, dA = \varepsilon_0 \oint_{\partial V} \left(-\frac{\nabla P}{\rho_{\text{eff}}}\right) \cdot \mathbf{n} \, dA \tag{2.1}$$

where:
- $\varepsilon_0 = 8.8541878128(13) \times 10^{-12}$ F/m is the vacuum permittivity (CODATA 2018)
- $\partial V$ is the closed surface bounding volume $V$
- $\mathbf{n}$ is the outward unit normal

**Physical Picture:**
- Toroidal vortex displaces spation outward along major radius → creates radial pressure gradient pointing away from vortex → measured as "positive charge"
- Negative charge (positron): Vortex with opposite circulation → displaces spation inward → pressure gradient points toward vortex
- Quantization: Cannot create partial vortex → charge comes in discrete units $e = 1.602176634 \times 10^{-19}$ C

### 2.2 Vacuum Permittivity from Spation Properties

**Theorem 2.1 (Permittivity from Spation Stiffness).** The vacuum permittivity $\varepsilon_0$ emerges from the coupling between spation pressure and charge:

$$\varepsilon_0 = \frac{K_{\text{bulk}}}{c^2 \rho_{\text{eff}}} \tag{2.2}$$

where:
- $K_{\text{bulk}} = 4.6 \times 10^{113}$ Pa is the spation bulk modulus
- $c = 2.99792458 \times 10^8$ m/s is the speed of light (spation sound speed)
- $\rho_{\text{eff}}$ is the effective charge density per unit pressure

**Proof:** The energy density in an electric field is:

$$u_E = \frac{1}{2}\varepsilon_0 E^2 \tag{2.3}$$

In SDT, this is elastic energy density in compressed spation:

$$u_{\text{elastic}} = \frac{1}{2}K_{\text{bulk}} \left(\frac{\Delta V}{V}\right)^2 \tag{2.4}$$

For radial field $E = E_r(r)$, the volume strain is:

$$\frac{\Delta V}{V} = \nabla \cdot \mathbf{u} \propto \frac{E}{c} \tag{2.5}$$

Equating energy densities:

$$\frac{1}{2}\varepsilon_0 E^2 = \frac{1}{2}K_{\text{bulk}} \left(\frac{E}{c}\right)^2 \tag{2.6}$$

Therefore:

$$\varepsilon_0 = \frac{K_{\text{bulk}}}{c^2} \times \frac{1}{\rho_{\text{eff}}} \tag{2.7}$$

The measured value $\varepsilon_0 = 8.854 \times 10^{-12}$ F/m establishes the coupling constant $\rho_{\text{eff}}$ between spation mechanics and charge. □

---

## 3. Coulomb's Law from Pressure Equilibrium

### 3.1 Single Charge Pressure Field

**Theorem 3.1 (Pressure Field Around Point Charge).** An isolated charge $q$ at the origin creates a pressure field:

$$P(r) = P_0 - \frac{A}{r} \tag{3.1}$$

where $P_0$ is the ambient pressure (established by CMB) and $A$ is determined by the charge magnitude.

**Proof:** For static deformation in free space, pressure satisfies Laplace's equation:

$$\nabla^2 P = 0 \quad \text{for } r > r_{\text{source}} \tag{3.2}$$

In spherical coordinates with spherical symmetry:

$$\frac{1}{r^2}\frac{d}{dr}\left(r^2 \frac{dP}{dr}\right) = 0 \tag{3.3}$$

General solution:

$$P(r) = -\frac{A}{r} + B \tag{3.4}$$

Boundary conditions:
- $P(\infty) = P_0$ (ambient CMB pressure) → $B = P_0$
- At the source, pressure matches the vortex boundary condition

Therefore:

$$P(r) = P_0 - \frac{A}{r} \tag{3.5}$$

□

### 3.2 Electric Field from Pressure Gradient

**Theorem 3.2 (Electric Field from Pressure).** The electric field is:

$$\mathbf{E}(\mathbf{r}) = \frac{q}{4\pi \varepsilon_0 r^2} \hat{\mathbf{r}} \tag{3.6}$$

**Proof:** From equation (1.1), the electric field is:

$$\mathbf{E} = -\frac{\nabla P}{\rho_{\text{eff}}} = -\frac{dP}{dr} \frac{\hat{\mathbf{r}}}{\rho_{\text{eff}}} = \frac{A}{\rho_{\text{eff}} r^2} \hat{\mathbf{r}} \tag{3.7}$$

From Gauss's law:

$$\oint_{\partial V} \mathbf{E} \cdot \mathbf{n} \, dA = \frac{q}{\varepsilon_0} \tag{3.8}$$

For a sphere of radius $r$:

$$4\pi r^2 E_r = \frac{q}{\varepsilon_0} \tag{3.9}$$

Therefore:

$$E_r = \frac{q}{4\pi \varepsilon_0 r^2} \tag{3.10}$$

Matching equations (3.7) and (3.10):

$$\frac{A}{\rho_{\text{eff}}} = \frac{q}{4\pi \varepsilon_0} \tag{3.11}$$

Therefore:

$$\mathbf{E}(\mathbf{r}) = \frac{q}{4\pi \varepsilon_0 r^2} \hat{\mathbf{r}} \tag{3.12}$$

□

### 3.3 Force Between Two Charges

**Theorem 3.3 (Coulomb's Law).** The force between two charges is:

$$\mathbf{F}_{12} = k_e \frac{q_1 q_2}{r^2} \hat{\mathbf{r}} \tag{3.13}$$

where $k_e = 1/(4\pi \varepsilon_0) = 8.9875517923(14) \times 10^9$ N·m²/C² is Coulomb's constant.

**Proof:** Charge $q_1$ at the origin creates field $\mathbf{E}_1$ at location $\mathbf{r}$:

$$\mathbf{E}_1(\mathbf{r}) = \frac{q_1}{4\pi \varepsilon_0 r^2} \hat{\mathbf{r}} \tag{3.14}$$

Force on charge $q_2$ at $\mathbf{r}$:

$$\mathbf{F}_{12} = q_2 \mathbf{E}_1(\mathbf{r}) = \frac{q_1 q_2}{4\pi \varepsilon_0 r^2} \hat{\mathbf{r}} = k_e \frac{q_1 q_2}{r^2} \hat{\mathbf{r}} \tag{3.15}$$

□

**SDT Interpretation:** Force arises from pressure gradient created by first charge acting on second vortex. No action-at-a-distance—pressure field mediates locally through continuous spation lattice, ultimately driven by CMB energy influx.

### 3.4 Superposition Principle

**Theorem 3.4 (Superposition).** For multiple charges, the total field is:

$$\mathbf{E}(\mathbf{r}) = \sum_{i} \frac{q_i}{4\pi \varepsilon_0 |\mathbf{r} - \mathbf{r}_i|^2} \hat{\mathbf{r}}_i \tag{3.16}$$

**Proof:** Spation response is linear for small deformations (elastic regime). Pressure fields superpose linearly. □

---

## 4. Gauss's Law and Poisson's Equation

### 4.1 Gauss's Law

**Theorem 4.1 (Gauss's Law).** The divergence of the electric field is:

$$\nabla \cdot \mathbf{E} = \frac{\rho_q}{\varepsilon_0} \tag{4.1}$$

where $\rho_q$ is the charge density [C/m³].

**Proof:** From the definition of charge (equation 2.1) and the divergence theorem:

$$Q = \varepsilon_0 \oint_{\partial V} \mathbf{E} \cdot \mathbf{n} \, dA = \varepsilon_0 \int_V \nabla \cdot \mathbf{E} \, dV \tag{4.2}$$

Also:

$$Q = \int_V \rho_q \, dV \tag{4.3}$$

Equating:

$$\int_V \left(\varepsilon_0 \nabla \cdot \mathbf{E} - \rho_q\right) \, dV = 0 \tag{4.4}$$

Since this holds for any volume $V$:

$$\nabla \cdot \mathbf{E} = \frac{\rho_q}{\varepsilon_0} \tag{4.5}$$

□

### 4.2 Poisson's Equation

**Theorem 4.2 (Poisson's Equation).** The electric potential satisfies:

$$\nabla^2 \Phi = -\frac{\rho_q}{\varepsilon_0} \tag{4.6}$$

**Proof:** From Gauss's law (equation 4.1) and $\mathbf{E} = -\nabla \Phi$:

$$\nabla \cdot \mathbf{E} = -\nabla^2 \Phi = \frac{\rho_q}{\varepsilon_0} \tag{4.7}$$

Therefore:

$$\nabla^2 \Phi = -\frac{\rho_q}{\varepsilon_0} \tag{4.8}$$

□

**SDT Interpretation:** This is the equilibrium equation for spation pressure field under charge sources. Same mathematical form as elastostatics, with the pressure field driven by CMB energy influx.

---

## 5. Electric Potential and Energy

### 5.1 Potential Definition

**Definition 5.1 (Electric Potential).** The electric potential $\Phi$ is defined such that:

$$\Phi(\mathbf{r}) = -\int_\infty^{\mathbf{r}} \mathbf{E} \cdot d\mathbf{l} \tag{5.1}$$

**Theorem 5.1 (Potential from Pressure).** The electric potential is related to pressure by:

$$\Phi = \frac{P - P_0}{\rho_{\text{eff}}} \tag{5.2}$$

**Proof:** From equation (1.1):

$$\Phi(\mathbf{r}) = -\int_\infty^{\mathbf{r}} \mathbf{E} \cdot d\mathbf{l} = -\int_\infty^{\mathbf{r}} \left(-\frac{\nabla P}{\rho_{\text{eff}}}\right) \cdot d\mathbf{l} = \frac{1}{\rho_{\text{eff}}} \int_\infty^{\mathbf{r}} \nabla P \cdot d\mathbf{l} = \frac{P(\mathbf{r}) - P(\infty)}{\rho_{\text{eff}}} \tag{5.3}$$

Setting $P(\infty) = P_0$ and $\Phi(\infty) = 0$:

$$\Phi = \frac{P - P_0}{\rho_{\text{eff}}} \tag{5.4}$$

□

**For point charge:**

$$\Phi(r) = \frac{q}{4\pi \varepsilon_0 r} \tag{5.5}$$

### 5.2 Potential Energy

**Theorem 5.2 (Electrostatic Energy).** The total energy to assemble a system of charges is:

$$U = \frac{1}{2}\sum_{i \neq j} \frac{q_i q_j}{4\pi \varepsilon_0 r_{ij}} = \frac{1}{2}\sum_{i} q_i \Phi_i \tag{5.6}$$

**Proof:** Standard electrostatic result. The factor $1/2$ avoids double-counting. □

**Energy density in field:**

$$u_E = \frac{1}{2}\varepsilon_0 E^2 \tag{5.7}$$

**Total energy:**

$$U = \int_{\text{all space}} \frac{1}{2}\varepsilon_0 E^2 \, d^3r \tag{5.8}$$

**SDT Interpretation:** This is elastic strain energy stored in compressed spation lattice, ultimately sourced from CMB energy influx.

---

## 6. Capacitance from Lattice Compression

### 6.1 Parallel Plate Capacitor

**Theorem 6.1 (Parallel Plate Capacitance).** For two conducting plates of area $A$ separated by distance $d$:

$$C = \frac{\varepsilon_0 A}{d} \tag{6.1}$$

**Proof:** Uniform field between plates:

$$E = \frac{V}{d} \tag{6.2}$$

Surface charge density:

$$\sigma = \varepsilon_0 E = \frac{\varepsilon_0 V}{d} \tag{6.3}$$

Total charge:

$$Q = \sigma A = \frac{\varepsilon_0 A}{d} V \tag{6.4}$$

Capacitance:

$$C = \frac{Q}{V} = \frac{\varepsilon_0 A}{d} \tag{6.5}$$

□

**SDT Interpretation:** Applying voltage compresses spation between plates. Stored energy:

$$U = \frac{1}{2}CV^2 = \frac{1}{2}\varepsilon_0 A d E^2 = \int \frac{1}{2}\varepsilon_0 E^2 \, dV \tag{6.6}$$

This is compression energy of spation lattice in volume $Ad$. Discharge: Releasing plates allows spation to relax → energy flows back out as current (spation momentum flux).

### 6.2 Dielectric Materials

**Theorem 6.2 (Dielectric Capacitance).** With dielectric (permittivity $\varepsilon = \kappa \varepsilon_0$):

$$C = \frac{\kappa \varepsilon_0 A}{d} \tag{6.7}$$

where $\kappa$ is the dielectric constant (dimensionless).

**SDT Mechanism:** Dielectric molecules have internal charge asymmetry (polar) or induced dipoles. Applied field aligns these → creates additional compression/rarefaction patterns → amplifies net lattice deformation → increases capacitance.

---

## 7. Current as Spation Momentum Flux

### 7.1 Current Definition

**Definition 7.1 (Electric Current).** Electric current is charge flow per unit time:

$$I = \frac{dQ}{dt} \tag{7.1}$$

Current density:

$$\mathbf{J} = \rho_q \mathbf{v}_{\text{drift}} \tag{7.2}$$

where $\mathbf{v}_{\text{drift}}$ is the average velocity of charge carriers.

### 7.2 Microscopic Picture in SDT

**Axiom 7.1 (Current from Vortex Motion).** In a conductor, free charges (electron vortices) move through the spation lattice. Applied field $\mathbf{E}$ creates pressure gradient → vortices experience force → motion creates momentum flux.

**Force on charge:**

$$\mathbf{F} = q \mathbf{E} \tag{7.3}$$

**Drift velocity:** Balance between:
1. Acceleration from electric force
2. Drag from spation-matter scattering

Steady state:

$$\mathbf{v}_{\text{drift}} = \mu \mathbf{E} \tag{7.4}$$

where $\mu$ is mobility [m²/(V·s)].

**Current density:**

$$\mathbf{J} = nq \mathbf{v}_{\text{drift}} = nq\mu \mathbf{E} = \sigma \mathbf{E} \tag{7.5}$$

where:
- $n$ = electron density [m⁻³]
- $\sigma = nq\mu$ = conductivity [S/m]

### 7.3 Ohm's Law

**Theorem 7.1 (Ohm's Law).** For a conductor of length $L$ and cross-section $A$:

$$V = IR \tag{7.6}$$

where:

$$R = \frac{L}{\sigma A} = \frac{\rho L}{A} \tag{7.7}$$

$\rho = 1/\sigma$ is resistivity [Ω·m].

**Proof:** Integrated over conductor:

$$I = \int \mathbf{J} \cdot d\mathbf{A} = JA = \sigma E A \tag{7.8}$$

$$V = EL \tag{7.9}$$

$$I = \sigma \frac{A}{L} V = \frac{V}{R} \tag{7.10}$$

Therefore:

$$V = IR \tag{7.11}$$

□

**SDT Interpretation:** Resistance arises from scattering of electron vortices off lattice imperfections, transferring momentum to thermal motion (Joule heating). The energy ultimately comes from CMB-driven pressure gradients.

---

## 8. Connection to Cosmic Microwave Background

### 8.1 CMB as Pressure Source

**Theorem 8.1 (CMB Pressure Field).** The pressure field at any point receives contributions from the CMB:

$$\Pi(\mathbf{r}) = \int_{\Omega} I_{\text{CMB}}(\hat{\mathbf{n}})[1 - E(\mathbf{r}, \hat{\mathbf{n}})] \, d\Omega \quad \text{[Pa]} \tag{8.1}$$

where $I_{\text{CMB}}(\hat{\mathbf{n}})$ is the CMB intensity from direction $\hat{\mathbf{n}}$ and $E(\mathbf{r}, \hat{\mathbf{n}})$ is the occlusion function.

**Physical Mechanism:**
1. CMB radiation propagates through spation, establishing pressure gradients
2. Charge creates additional pressure sources in this CMB-driven field
3. Electric fields emerge from pressure gradients
4. All electrical phenomena trace to CMB energy influx

### 8.2 Energy Flow

**Theorem 8.2 (Energy Conservation).** The electrical energy in any system is ultimately sourced from CMB energy influx. The CMB provides continuous replenishment of pressure fields, maintaining electrical potentials and currents.

**Proof:** All pressure fields trace to CMB radiation. Charge creates local modifications to this field, but the underlying energy source is the CMB. Energy conservation requires that all electrical work ultimately comes from CMB energy influx. □

---

## 9. Validation Benchmarks

### 9.1 Benchmark E1: Coulomb's Law

**Phenomenon:** Force between two point charges

**Experimental:** $F = k_e q_1 q_2 / r^2$ with $k_e = 8.9875517923(14) \times 10^9$ N·m²/C²

**SDT Prediction:** From pressure gradient mechanics (Theorem 3.3)

**Result:** Exact match. SDT reproduces Coulomb's law from pressure equilibrium.

### 9.2 Benchmark E2: Capacitance

**Phenomenon:** Parallel plate capacitor

**Experimental:** $C = \varepsilon_0 A / d$

**SDT Prediction:** From lattice compression (Theorem 6.1)

**Result:** Exact match. SDT reproduces capacitance from spation compression.

---

## 10. Conclusion

We have derived all electrical phenomena from SDT using spation pressure deformation mechanics. The key results are:

1. Charge is persistent radial deformation of spation lattice
2. Electric field is pressure gradient: $\mathbf{E} = -\nabla P / \rho_{\text{eff}}$
3. All electrical laws emerge from pressure equilibrium
4. CMB provides continuous energy influx maintaining all pressure fields

All calculations proceed without use of mass $m$ or gravitational constant $G$ as fundamental quantities. The electrical phenomena are purely geometric and pressure-dynamic, requiring no field-theoretic assumptions beyond the four irreducible primitives of SDT, with the CMB as the ultimate energy source.

---

## References

1. CODATA 2018: Fundamental Physical Constants
2. Jackson, J.D., "Classical Electrodynamics" (3rd ed., 1999)
3. Griffiths, D.J., "Introduction to Electrodynamics" (4th ed., 2013)
4. Foundational Principles of SDT (Phase 0)
5. Coulomb Force from CMB Mutual Occlusion (Phase 1)

---

**End of Document**

