# Volume II: Atomic Physics
## Book 6: Nuclear Structure

**Source:** Phase_17, Phase_18, atomica sentis.md Section 0.9  
**Equation Numbering:** II.6.Chapter.Section.Equation  
**Status:** B18, B19 Under Investigation

---

## Introduction to Book 6

This book extends SDT to nuclear structure, showing how toroidal vortices at the femtoscale create nuclear binding, decay processes, and the strong force.

**Cross-Reference:** This book builds on Volume I, Book 1, Chapter 2 (displacement structures) and Volume I, Book 2, Chapter 2 (master equation).

---

## Chapter 1: Toroidal Structures at Femtoscale

**Source:** Phase_17_Toroidal_Structures_and_Pressure_Differentials_at_Femtoscale.md  
**Benchmark:** B18 (Under Investigation)  
**Status:** 🔬 Under Investigation

### Section 1.1: The Toroidal Vortex Model of Nucleons

**Physical Structure of the Proton:**

In SDT, the proton is not a point charge but a stable, toroidal vortex structure in the spation medium.

**Geometric Parameters:**

- Proton radius: R_p = 0.8414(19) fm (CODATA 2018)
- Toroidal structure: Donut-shaped (torus) displacement region
- Major radius: R_torus ≈ R_p ≈ 0.84 fm
- Minor radius: r_torus ≈ R_p/3 ≈ 0.28 fm (estimated from vortex stability)

**Physical Interpretation:**

The toroidal structure is the lowest-energy configuration for a stable, rotating displacement vortex. The rotation creates a helical wake (magnetic field), while the toroidal geometry minimizes the surface area-to-volume ratio.

### Section 1.2: Physical Structure of the Neutron

**The neutron is a composite structure:**

A proton and an electron brought into such close proximity (under immense nuclear pressure) that their displacement fields merge.

**Geometric Parameters:**

- Neutron radius: R_n ≈ 0.8 fm
- Structure: Bound p⁺-e⁻ system in toroidal configuration
- The electron is trapped in the proton's pressure well

**Stability Mechanism:**

The neutron is stable within a nucleus because the external pressure from surrounding nucleons maintains the geometric lock. When free, the neutron decays (mean lifetime ≈ 880 s).

### Section 1.3: Pressure Differentials at Femtoscale

**Toroidal Pressure Field:**

For a toroidal vortex of major radius R_t and minor radius r_t:

$$P(d) = P_0 \left[1 - \frac{R_t^2 r_t^2}{4d^4}\right] \quad \text{for } d \gg R_t \tag{II.6.1.3.1}$$

**The 1/d⁴ falloff** (rather than 1/d²) reflects the more complex geometry of the torus.

**Pressure Gradient:**

The pressure gradient ∇P creates the confining force:

$$F_{\text{confine}} = -\nabla P \cdot A_{\text{cross-section}} \tag{II.6.1.3.2}$$

**For the proton, this yields the Strong Nuclear Force strength** (~1.77 × 10⁵ N).

### Section 1.4: Nuclear Packing and Pressure Interactions

**Nucleon-Nucleon Interactions:**

When two nucleons approach within nuclear distances (d < 3 fm), their toroidal pressure fields overlap.

**Attractive Region:**

At intermediate distances (1-2 fm), overlapping pressure fields create a region of reduced pressure between nucleons → attractive force.

**Repulsive Core:**

At very short distances (d < 0.5 fm), toroidal structures overlap → increased pressure → repulsive core.

**The Nuclear Potential:**

The resulting potential has characteristic shape: attractive at intermediate distances, repulsive at short distances.

### Section 1.5: Nuclear Binding Energies

**Current Status:**

The complete nuclear binding energy model is under development. Current work focuses on:
- Toroidal packing geometry
- Pressure field overlap calculations
- Binding energy predictions for light nuclei

**Cross-Reference:** See Volume VIII, Book 20, Chapter 1 for investigation status.

---

## Chapter 2: Alpha Particles and Beta Decay

**Source:** Phase_18_Alpha_Particles_and_Beta_Decay.md  
**Benchmark:** B19 (Under Investigation)  
**Status:** 🔬 Under Investigation

### Section 2.1: The Alpha Particle as a Geometric Unit

**Tetrahedral Geometry:**

The alpha particle (⁴He nucleus) is a stable, geometrically perfect tetrahedral cluster:
- Four nucleons (2p, 2n) at vertices of perfect tetrahedron
- Edge length: a ≈ 2.4 fm
- Binding energy: E_binding ≈ 28.3 MeV
- Most stable nuclear configuration possible

**Why Tetrahedral?**

The tetrahedron maximizes the attractive pressure deficit from overlapping toroidal fields while minimizing repulsive core overlap.

### Section 2.2: Alpha Decay Mechanism

**Pressure-Driven Ejection:**

Alpha decay occurs when a heavy nucleus contains an alpha particle cluster that is under sufficient pressure to overcome the confining barrier.

**The Barrier:**

$$V_{\text{barrier}} = \frac{Z_\alpha Z_{\text{daughter}} e^2}{4\pi\varepsilon_0 r_{\text{contact}}} \tag{II.6.2.2.1}$$

where r_contact ≈ 8 fm.

**Ejection Process:**

1. Alpha cluster forms within parent nucleus
2. Pressure gradient builds up
3. Cluster accelerates toward nuclear surface
4. Cluster tunnels through pressure barrier (pressure-driven, not quantum)
5. Cluster emerges with characteristic energy E_alpha

### Section 2.3: Beta Decay Mechanism

**Neutron Structure:**

The neutron is a bound p⁺-e⁻ system. Beta decay occurs when this bound system reconfigures.

**Decay Process:**

1. Neutron in nucleus: Stable due to external pressure
2. Neutron free: System seeks lower-energy state
3. Reconfiguration: p⁺-e⁻ → p⁺ + e⁻ + ν̄ (neutrino from pressure release)
4. Energy release: Q-value from geometric reconfiguration

**Current Status:**

The complete beta decay mechanism is under development.

**Cross-Reference:** See Volume VIII, Book 20, Chapter 1 for investigation status.

### Section 2.4: Decay Rate Calculations

**Geometric Formation Factor:**

For a nucleus with A nucleons, the probability of forming an alpha cluster scales with geometric stability.

**Pressure Gradient Factor:**

$$\nabla P \propto \frac{Z^2}{A^{1/3}} \tag{II.6.2.4.1}$$

Larger nuclei have stronger pressure gradients → faster decay.

**Current Status:**

Complete decay rate calculations are under development.

---

## Chapter 3: Strong Force as Confinement Pressure

### Section 3.1: Baryonic Confinement

**From atomica sentis.md:**

The proton confinement force:

$$F_{\text{confine}} \approx 1.77 \times 10^5 \text{ N} \tag{II.6.3.1.1}$$

**This is the mechanical origin of the Strong Nuclear Force.**

**Derivation:**

From pressure gradient and displacement volume:

$$F = P_0 \times V_{\text{disp}} \times \text{(geometric factor)} \tag{II.6.3.1.2}$$

**Cross-Reference:** See atomica sentis.md, Section 2 for detailed derivation.

### Section 3.2: Nuclear Binding Mechanism

**Pressure Balance:**

Nuclear binding emerges from pressure balance between:
- Confining pressure (from P₀ and K_bulk)
- Repulsive pressure (from toroidal overlap)

**Binding Energy:**

$$E_{\text{binding}} = \text{(pressure work)} - \text{(repulsive energy)} \tag{II.6.3.2.1}$$

**Current Status:**

Complete binding energy model under development.

---

## Chapter 4: Nuclear Binding Energies

### Section 4.1: Light Nuclei

**Current Status:**

Binding energy calculations for light nuclei (A ≤ 20) are under active development.

**Approach:**

- Toroidal packing geometry
- Pressure field overlap
- Geometric stability factors

**Cross-Reference:** See Volume VIII, Book 20, Chapter 1 for investigation status.

### Section 4.2: Magic Numbers

**Geometric Interpretation:**

Magic numbers (2, 8, 20, 28, 50, 82, 126) correspond to geometric packing stability, not shell closure.

**Current Status:**

Complete geometric derivation of magic numbers is under development.

---

## Summary of Book 6

This book has established the foundation for nuclear structure in SDT:

1. **Toroidal Structures:** Nucleons as toroidal vortices (B18 under investigation)
2. **Alpha and Beta Decay:** Mechanical decay processes (B19 under investigation)
3. **Strong Force:** Confinement pressure mechanism
4. **Nuclear Binding:** Under active development

**Key Achievement:** Strong force identified as confinement pressure (~1.77×10⁵ N).

**Outstanding Work:**
- Complete nuclear binding energy model
- Magic number derivation
- Complete decay rate calculations

**Next:** Volume III: Thermodynamics

---

**End of Book 6**

**End of Volume II: Atomic Physics**

---

**Volume II Complete:** Atomic physics from single-electron to nuclear structure, with 6 certified benchmarks and 2 under investigation.

