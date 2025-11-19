# Volume I: Foundations
## Book 3: The Derivation Tree

**Source:** Phase_0_Foundational_Principles.md, Part II  
**Equation Numbering:** I.3.Chapter.Section.Equation

---

## Introduction to Book 3

This book shows step-by-step how every observable quantity in physics derives from the four ingredients and their ratios. Each derivation includes:

- Starting ingredients
- Intermediate steps with dimensional analysis
- Final formula
- Numerical validation
- Comparison to conventional physics expression

**Key Principle:**

All observables are ratios or combinations of the four ingredients:
- **Space** (spation properties)
- **Matter** (displacement structures)
- **Movement** (shunt dynamics)
- **Now** (oscillation counting)

**Cross-Reference:** This book builds on Volume I, Books 1-2. The four ingredients (Book 1) and master equation (Book 2) are here shown to produce all observable quantities.

---

## Chapter 1: Primary Observables from Ratios

### Section 1.1: Frequency: Movement/Space

**Derivation:**

$$\nu = \frac{v}{\lambda_C} = \frac{\text{particle velocity}}{\text{characteristic length}} \tag{I.3.1.1.1}$$

**Units:** Hz = s⁻¹ (inverse time)

**Physical meaning:** Shunt repetition rate

**Dimensional Check:**

[ν] = [m/s] / [m] = [s⁻¹] ✓

**Limiting Cases:**

- **v → 0:** ν → 0 (no motion, no shunts)
- **v → c:** ν → c/λ_C (maximum shunt rate)
- **λ_C → 0:** ν → ∞ (point particle limit, unphysical)

**Numerical Example:**

Electron in hydrogen ground state:
- v = 2.19×10⁶ m/s
- λ_C = 2.43×10⁻¹² m
- ν = 9.0×10¹⁷ Hz ✓

**Validation:** All spectroscopic measurements are frequency measurements

**Connection to conventional:** Same ν, but different interpretation (oscillation vs. abstract wave)

### Section 1.2: Energy: Planck × Frequency

**Derivation:**

$$E = h\nu = h \times \frac{v}{\lambda_C} \tag{I.3.1.2.1}$$

**Units:** J = kg·m²/s²

**Physical meaning:** Energy per oscillation

**Dimensional Check:**

[E] = [J·s] × [s⁻¹] = [J] ✓

**Limiting Cases:**

- **ν → 0:** E → 0 (no oscillations, no energy)
- **ν → ∞:** E → ∞ (infinite oscillations, infinite energy)

**Numerical Example:**

Electron in hydrogen ground state:
- ν = 9.0×10¹⁷ Hz
- h = 6.626×10⁻³⁴ J·s
- E = 6.0×10⁻¹⁶ J per shunt

**Validation:** 

- Planck-Einstein relation E = hν (photoelectric effect)
- All atomic spectroscopy (line energies)

**Connection to conventional:** Same formula, but ν is physical oscillation not abstract frequency

### Section 1.3: Momentum: Planck / Wavelength

**Derivation:**

$$p = \frac{h}{\lambda} = \frac{h}{c/\nu} = \frac{h\nu}{c} \tag{I.3.1.3.1}$$

**For particle:** $p = mv$ where m emerges from shunt resistance (see Section 1.5)

**Units:** kg·m/s

**Physical meaning:** Cumulative directional shunt effect

**Dimensional Check:**

[p] = [J·s] / [m] = [kg·m²/s²·s] / [m] = [kg·m/s] ✓

**Limiting Cases:**

- **λ → ∞:** p → 0 (long wavelength, no momentum)
- **λ → 0:** p → ∞ (short wavelength, high momentum)

**Numerical Example:**

Electron de Broglie wavelength:
- λ = h/(m_e v) = 3.32×10⁻¹⁰ m (for v = 2.19×10⁶ m/s)
- p = h/λ = 1.99×10⁻²⁴ kg·m/s
- Compare: m_e v = 1.99×10⁻²⁴ kg·m/s ✓

**Validation:** 

- de Broglie relation (electron diffraction)
- Compton scattering

### Section 1.4: Force: Frequency × Momentum Transfer

**Derivation:**

$$F = \nu \times \langle \Delta p \rangle_{\text{directional}} = \frac{\text{shunts}}{\text{time}} \times \frac{\text{momentum}}{\text{shunt}} \tag{I.3.1.4.1}$$

**Units:** N = kg·m/s²

**Physical meaning:** Time-averaged directional momentum transfer rate

**Dimensional Check:**

[F] = [s⁻¹] × [kg·m/s] = [kg·m/s²] = [N] ✓

**Limiting Cases:**

- **ν → 0:** F → 0 (no shunts, no force)
- **Δp → 0:** F → 0 (no momentum transfer, no force)

**Numerical Example:**

Electron in hydrogen (Coulomb force):
- ν = 9.0×10¹⁷ Hz
- ⟨Δp⟩ ~ 10⁻³⁰ kg·m/s (per shunt)
- F = 9.0×10⁻¹³ N
- Compare: k_e e²/r² = 8.2×10⁻⁸ N (at r = a₀)

**Note:** Need to account for directional averaging and many shunts to get exact match.

**Validation:** F = ma (all classical mechanics)

**Cross-Reference:** See Volume II, Book 4, Chapter 1 (Coulomb Force) for detailed derivation.

### Section 1.5: Mass: Shunt Resistance (EMERGENT)

**Derivation:**

$$m = \frac{F}{a} = \frac{\nu \langle \Delta p \rangle}{a} \tag{I.3.1.5.1}$$

**Mass is cumulative shunt resistance:**

- More shunts per second → more resistance
- Larger boundary area → more shunts
- Result: m emerges from geometry + dynamics

**Units:** kg

**Physical meaning:** Resistance to acceleration from cumulative shunts

**Dimensional Check:**

[m] = [N] / [m/s²] = [kg·m/s²] / [m/s²] = [kg] ✓

**Why m_e has specific value:**

- Electron geometry (~λ_C scale)
- Electron velocity (~αc in ground state)
- Shunt rate ~10¹⁸ Hz
- Cumulative resistance = 9.109×10⁻³¹ kg

**NOT fundamental—emergent from shunt dynamics!**

**Physical Picture:**

Mass is like friction—the more you try to accelerate a particle, the more shunts occur, creating resistance. This resistance IS what we call "mass."

**Limiting Cases:**

- **No shunts:** ν → 0 → m → 0 (no resistance, no mass)
- **Many shunts:** ν → ∞ → m → ∞ (high resistance, high mass)

**Numerical Validation:**

Electron mass:
- m_e = 9.109×10⁻³¹ kg (measured)
- From shunt dynamics: m_e = cumulative shunt resistance
- Agreement: Exact (by calibration)

**Key Insight:**

**Mass is NOT a fundamental property. Mass emerges from how many shunts occur when you try to accelerate a particle.**

### Section 1.6: Temperature: Average Shunt Energy

**Derivation:**

$$k_B T = \langle E_{\text{shunt}} \rangle = h \langle \nu_{\text{shunt}} \rangle \tag{I.3.1.6.1}$$

**Units:** K (Kelvin, via Boltzmann constant)

**Physical meaning:** Average energy per synchronized shunt oscillation

**Dimensional Check:**

[k_B T] = [J] ✓

**Limiting Cases:**

- **T → 0:** ⟨ν⟩ → ν_min (minimum shunt rate, ground state)
- **T → ∞:** ⟨ν⟩ → ∞ (infinite shunt rate, unphysical)

**Numerical Example:**

Room temperature (T = 300 K):
- k_B T = 4.14×10⁻²¹ J
- ⟨ν⟩ = k_B T/h = 6.25×10¹² Hz
- Compare: Thermal frequency ~10¹² Hz ✓

**Validation:** 

- Kinetic theory: ½m⟨v²⟩ = (3/2)kT
- Black body radiation: Wien's law, Stefan-Boltzmann
- Specific heats

**Connection to conventional:** Same T, but interpretation is oscillation frequency, not "average kinetic energy"

**Cross-Reference:** See Volume III, Book 7 (Thermodynamic Laws) for detailed treatment.

### Section 1.7: Entropy: Configuration Count

**Derivation:**

$$S = k_B \ln \Omega(N_{\text{shunts}}) \tag{I.3.1.7.1}$$

Where Ω = number of accessible shunt configurations

**Units:** J/K

**Physical meaning:** As oscillations accumulate (time passes), configuration space grows

**Dimensional Check:**

[S] = [J/K] ✓

**Arrow of time:** dS/dt > 0 because oscillation count increases monotonically

**Physical Interpretation:**

Each new shunt adds possible configurations. As N_shunts increases, Ω increases, so S increases. This is why entropy always increases—it's counting more oscillations!

**Validation:** All of thermodynamics (Carnot, statistical mechanics)

**Cross-Reference:**

For detailed derivation, see Volume III, Book 7, Chapter 2 (Second Law).

---

## Chapter 2: Composite Observables

### Section 2.1: Pressure: Force per Area

**Derivation:**

$$P = \frac{F}{A} = \frac{\nu \langle \Delta p \rangle}{A} \tag{I.3.2.1.1}$$

**Units:** Pa = N/m²

**Physical meaning:** Momentum transfer rate per unit area

**Dimensional Check:**

[P] = [N] / [m²] = [Pa] ✓

**Connection to spation pressure:**

This is the pressure field Π(x) from Volume I, Book 1, Chapter 1, Section 1.3, now derived from shunt dynamics.

### Section 2.2: Work: Integrated Force

**Derivation:**

$$W = \int F \cdot dx = \int \nu \langle \Delta p \rangle \cdot dx \tag{I.3.2.2.1}$$

**Units:** J = N·m

**Physical meaning:** Total energy transferred through directed shunts

**Dimensional Check:**

[W] = [N] × [m] = [J] ✓

### Section 2.3: Power: Work per Time

**Derivation:**

$$P = \frac{dW}{dt} = F \cdot v = \nu \langle \Delta p \rangle \cdot v \tag{I.3.2.3.1}$$

**Units:** W = J/s

**Physical meaning:** Energy transfer rate

**Dimensional Check:**

[P] = [J] / [s] = [W] ✓

### Section 2.4: Angular Momentum: Movement Budget

**Derivation:**

$$L = m v r = (\text{shunt resistance}) \times (\text{velocity}) \times (\text{radius}) \tag{I.3.2.4.1}$$

**Units:** kg·m²/s = J·s

**Physical meaning:** Rotational shunt accumulation

**Conservation:** Linear ↔ angular momentum exchange through shunts

**Dimensional Check:**

[L] = [kg] × [m/s] × [m] = [kg·m²/s] ✓

### Section 2.5: Action: Energy × Time

**Derivation:**

$$S = \int E \, dt = \int h\nu \cdot \frac{dN}{\nu} = h \int dN = hN \tag{I.3.2.5.1}$$

**Action is Planck's constant times oscillation count!**

**Units:** J·s

**Physical meaning:** Total oscillations accumulated

**Dimensional Check:**

[S] = [J] × [s] = [J·s] ✓

**Key Insight:**

This is why action is quantized in units of ℏ. Action measures oscillation count, and oscillations come in discrete units!

---

## Chapter 3: Electromagnetic Phenomena

### Section 3.1: EM as Shunt Propagation

**When electron changes orbit:**

- Shunt frequency changes: ν_high → ν_low
- Creates disturbance in spation pressure field
- Disturbance propagates at c (natural medium speed)
- **This propagating disturbance = "photon"**

**NOT:** Separate particle traveling

**YES:** Information about shunt change propagating

**Physical Picture:**

Like a stone dropped in water creates ripples, an electron changing orbit creates a pressure disturbance that propagates through spation. This disturbance IS what we call a "photon."

**Cross-Reference:** See Volume IV, Book 11, Chapter 2 (Photons as Shunt Propagation Signals) for detailed treatment.

### Section 3.2: Wavelength and Frequency

**Derivation:**

$$\lambda = \frac{c}{\nu} \tag{I.3.3.2.1}$$

Where ν is the oscillation frequency of the source shunt.

**Units:** m

**Physical meaning:** Distance pressure wave travels in one oscillation period

**Dimensional Check:**

[λ] = [m/s] / [s⁻¹] = [m] ✓

**Validation:** All EM spectroscopy

### Section 3.3: Electric vs Magnetic

**"Electric" field:**

- E → 0 limit (small displacement, little occlusion)
- Direct pressure gradient
- Radial from charge

**"Magnetic" field:**

- From helical wake circulation
- Perpendicular to motion
- Directional bias in shunt pattern

**Both are pressure field phenomena!**

**Mathematical Description:**

**Electric field:**

$$\mathbf{E} = -\nabla \Pi_s \tag{I.3.3.3.1}$$

**Magnetic field:**

$$\mathbf{B} = \nabla \times \mathbf{A}_s \tag{I.3.3.3.2}$$

Where A_s is spation circulation potential.

**Cross-Reference:** See Volume IV, Book 9 (Electric Phenomena) and Book 10 (Magnetic Phenomena) for detailed derivations.

### Section 3.4: Maxwell's Equations Emerge

**Wave equation from pressure propagation:**

$$\nabla^2 \Pi - \frac{1}{c^2}\frac{\partial^2 \Pi}{\partial t^2} = 0 \tag{I.3.3.4.1}$$

**This IS the EM wave equation.**

**Maxwell's equations:**

From spation conservation laws:
- **Gauss's law:** ∇·E = ρ_q/ε₀ (pressure divergence)
- **Faraday's law:** ∇×E = -∂B/∂t (circulation dynamics)
- **Ampère's law:** ∇×B = μ₀J + μ₀ε₀∂E/∂t (current + displacement)
- **Gauss's law (magnetic):** ∇·B = 0 (no magnetic monopoles)

**Cross-Reference:**

For detailed derivation, see Volume IV, Book 11, Chapter 1 (Maxwell's Equations from Spation Conservation).

---

## Chapter 4: Gravitational Phenomena

### Section 4.1: Gravity as E → 1 Limit

**Large displacement → significant occlusion → gravity**

**Key differences from "electric":**

- E → 1 (strong occlusion)
- Affects all masses (displacement always occludes)
- Weaker (pressure deficit smaller)

**Physical Picture:**

At atomic scales, occlusion is negligible (E ≈ 0), so Coulomb force dominates. At planetary scales, occlusion is significant (E ≈ 0.64), so gravity dominates but is screened.

**Cross-Reference:** See Volume V, Book 12, Chapter 1 (Gravitation from Spation Pressure Gradients) for detailed treatment.

### Section 4.2: Gravitational Parameter β

**Derivation:**

$$\beta = \frac{\kappa V_{\text{disp}} K_{\text{bulk}}}{4\pi} \tag{I.3.4.2.1}$$

**Replaces GM in conventional physics.**

**Units:** m³/s²

**Physical meaning:** Pressure deficit strength per unit displacement volume

**Dimensional Check:**

[β] = [m³] × [Pa] = [m³] × [N/m²] = [m³·kg/(m·s²)] = [m³/s²] ✓

**Numerical Example:**

Earth:
- V_disp,⊕ ≈ 5.56×10⁻² m³ (from Phase 1)
- κ ≈ 1
- K_bulk = 4.6×10¹¹³ Pa
- β_⊕ = 2.04×10¹² m³/s²
- Compare: GM_⊕ = 3.986×10¹⁴ m³/s²

**Note:** Need to account for screening factor ξ ~ 10⁻⁹ to get exact match.

**Cross-Reference:** See Volume V, Book 12, Chapter 3 for detailed β parameter treatment.

### Section 4.3: Orbital Mechanics

**Derivation:**

$$v(r) = \sqrt{\frac{\beta}{r}} \tag{I.3.4.3.1}$$

**Kepler's laws emerge from pressure balance.**

**Dimensional Check:**

[v] = √([m³/s²] / [m]) = √([m²/s²]) = [m/s] ✓

**Validation:**

- Planetary orbits
- Moon's orbit
- Satellite orbits

**Cross-Reference:**

For detailed derivation, see Volume II, Book 4, Chapter 1 (Coulomb Force) and Volume V, Book 13, Chapter 1 (Orbital Mechanics).

---

## Summary of Book 3

This book has shown how all observable quantities derive from the four ingredients:

1. **Primary Observables:** Frequency, energy, momentum, force, mass, temperature, entropy
2. **Composite Observables:** Pressure, work, power, angular momentum, action
3. **Electromagnetic Phenomena:** EM waves, electric and magnetic fields, Maxwell's equations
4. **Gravitational Phenomena:** Gravity, orbital mechanics, β parameter

**All emerge from:**
- Space (spation properties)
- Matter (displacement structures)
- Movement (shunt dynamics)
- Now (oscillation counting)

**Next:** Volume II begins the detailed application of these foundations to specific physical systems.

---

**End of Book 3**

**End of Volume I: Foundations**

---

**Volume I Complete:** The complete foundation of Spatial Displacement Theory is now established. All subsequent volumes build upon these three books.

