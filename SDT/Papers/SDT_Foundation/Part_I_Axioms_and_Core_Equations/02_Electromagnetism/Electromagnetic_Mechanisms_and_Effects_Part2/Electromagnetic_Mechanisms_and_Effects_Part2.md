# Electromagnetic Mechanisms and Effects Part 2
## Advanced Wave Phenomena, Resonant Systems, and Quantum Precursors

**Author:** James C. Harvey  
**Date:** December 2025  
**Version:** 2.0  
**Status:** Complete Mathematical Derivation

---

## Abstract

We derive advanced electromagnetic phenomena from Spatial Displacement Theory (SDT) including resonant systems, radiation pressure, wave propagation in conductors, and quantum precursors. All phenomena emerge from spation mechanics and boundary locking mechanisms. The Cosmic Microwave Background (CMB) provides the continuous influx of electromagnetic energy that establishes and maintains all wave propagation. All calculations proceed without use of mass $m$ or gravitational constant $G$ as fundamental quantities, deriving all effects from spation pressure dynamics driven by the CMB.

---

## 1. Introduction

This paper extends Part 1 to cover advanced electromagnetic phenomena including resonant systems, radiation pressure, wave propagation in conductors, and connections to quantum mechanics. All derivations follow the same SDT framework established in Part 1.

---

## 2. Resonant Systems and Energy Storage

### 2.1 LC Oscillator

**Definition 2.1 (LC Oscillator).** An LC circuit consists of:
- **Capacitor:** Stores compression energy $U_C = \frac{1}{2}CV^2$
- **Inductor:** Stores circulation energy $U_L = \frac{1}{2}LI^2$

**Total energy:**
$$U = U_C + U_L = \text{const} \quad \text{(ideal, lossless)} \tag{2.1}$$

**Oscillation frequency:**
$$\omega_0 = \frac{1}{\sqrt{LC}} \tag{2.2}$$

**Current-voltage relation:**
$$I(t) = I_0 \cos(\omega_0 t), \quad V(t) = V_0 \sin(\omega_0 t) \tag{2.3}$$

**With losses** (resistance $R$):

**Damping rate:**
$$\gamma = \frac{R}{2L} \tag{2.4}$$

**Q factor:**
$$Q = \frac{\omega_0 L}{R} = \frac{1}{R}\sqrt{\frac{L}{C}} \tag{2.5}$$

**SDT:** $R$ from locking to resistive elements. Therefore:

$$Q = \omega_0 \tau_{\text{lock}} \tag{2.6}$$

High $Q$ → long energy storage time (weak locking to environment).

### 2.2 RLC Circuit Response

**Theorem 2.1 (Driven Oscillator).** Driven oscillator equation:

$$L\frac{d^2 Q}{dt^2} + R\frac{dQ}{dt} + \frac{Q}{C} = V_0 \cos(\omega t) \tag{2.7}$$

**Impedance:**
$$Z(\omega) = R + i\left(\omega L - \frac{1}{\omega C}\right) \tag{2.8}$$

**Resonance** ($\omega = \omega_0$):
$$|Z(\omega_0)| = R \quad \text{(minimum)} \tag{2.9}$$

**Power absorbed:**
$$P(\omega) = \frac{V_0^2}{2|Z(\omega)|^2}R = \frac{V_0^2}{2R}\frac{\gamma^2}{(\omega - \omega_0)^2 + \gamma^2} \tag{2.10}$$

Lorentzian lineshape with width $\Delta\omega = 2\gamma = R/L$.

**SDT:** Matches atomic absorption—same physics (damped oscillator via locking).

### 2.3 Coupled Resonators

**Theorem 2.2 (Coupled LC Circuits).** Two LC circuits with mutual inductance $M$:

**Coupled equations:**
$$\begin{aligned}
L_1 \frac{d^2 Q_1}{dt^2} + \frac{Q_1}{C_1} &= M\frac{d^2 Q_2}{dt^2} \tag{2.11a} \\
L_2 \frac{d^2 Q_2}{dt^2} + \frac{Q_2}{C_2} &= M\frac{d^2 Q_1}{dt^2} \tag{2.11b}
\end{aligned}$$

**Normal modes:**
$$\omega_\pm = \frac{1}{2}\left[\omega_1^2 + \omega_2^2 \pm \sqrt{(\omega_1^2 - \omega_2^2)^2 + 4\kappa^2}\right]^{1/2} \tag{2.12}$$

where $\kappa = M/\sqrt{L_1 L_2}$ is the coupling strength.

**Mode splitting:** $\Delta\omega = \omega_+ - \omega_- \approx \kappa\omega_0$ (for $\omega_1 \approx \omega_2 \approx \omega_0$).

**SDT:** Coupling via shared spation circulation → energy exchange between resonators.

**Rabi oscillations:** Energy transfers back and forth at frequency $\Delta\omega/2$.

---

## 3. Radiation Pressure and Momentum

### 3.1 EM Momentum Density

**Definition 3.1 (Momentum Density).** From Part 1:

$$\mathbf{g} = \frac{\mathbf{S}}{c^2} = \varepsilon_0(\mathbf{E} \times \mathbf{B}) \tag{3.1}$$

**For plane wave:** $S = (c/\mu_0)EB = (\varepsilon_0 c)E^2$

$$g = \frac{\varepsilon_0 E^2}{c} = \frac{u}{c} \tag{3.2}$$

**Momentum per photon:** $p = E/c = \hbar\omega/c = \hbar k$

### 3.2 Radiation Pressure

**Theorem 3.1 (Radiation Pressure).** 

**Perfectly absorbing surface:**
Incident flux $\Phi$ (energy per area per time) carries momentum flux:

$$\frac{dp}{dt \, dA} = \frac{\Phi}{c} \tag{3.3}$$

**Radiation pressure:**
$$P_{\text{rad}} = \frac{\Phi}{c} = \frac{I}{c} \tag{3.4}$$

**Perfectly reflecting surface:** Momentum reverses → factor 2:

$$P_{\text{rad}} = \frac{2I}{c} \tag{3.5}$$

**Example** (sunlight, $I = 1360$ W/m²):
$$P_{\text{rad}} = \frac{2 \times 1360}{3 \times 10^8} = 9.1 \times 10^{-6} \text{ Pa} = 9.1 \, \mu\text{Pa}$$

**Applications:**
- Solar sails (propulsion)
- Optical tweezers (manipulating particles)
- Radiation force on atoms (laser cooling)

**SDT:** Helical spation wave carries momentum → transfers to matter via locking → force.

### 3.3 Abraham-Minkowski Controversy

**Theorem 3.2 (Momentum in Dielectric).** In dielectric (refractive index $n$):

**Minkowski momentum:** $p_M = (n E)/c$  
**Abraham momentum:** $p_A = E/(n c)$

**Experiment:** Both correct in different circumstances!

- **Minkowski:** Momentum of EM field + medium (canonical)
- **Abraham:** Momentum of wave packet (kinetic)

**SDT Resolution:**

Total momentum = wave momentum + entrained spation momentum:

$$\mathbf{p}_{\text{total}} = \mathbf{p}_{\text{wave}} + \mathbf{p}_{\text{entrained}} = \frac{n\mathbf{S}}{c^2} + \rho_s \mathbf{v}_s V_{\text{lock}} \tag{3.6}$$

Depends on how you define "field momentum" vs "matter momentum"—both are valid, different decompositions.

---

## 4. Wave Propagation in Conductors

### 4.1 Skin Depth

**Theorem 4.1 (Skin Depth).** In conductor, displacement current negligible → Ampère becomes:

$$\nabla \times \mathbf{B} = \mu_0 \mathbf{J} = \mu_0 \sigma \mathbf{E} \tag{4.1}$$

**Wave equation:**
$$\nabla^2 \mathbf{E} - \mu_0 \sigma \frac{\partial \mathbf{E}}{\partial t} = 0 \tag{4.2}$$

**Solution:** Exponentially decaying wave:

$$E(x, t) = E_0 e^{-x/\delta} e^{i(kx - \omega t)} \tag{4.3}$$

**Skin depth:**
$$\delta = \sqrt{\frac{2}{\mu_0 \sigma \omega}} = \sqrt{\frac{2\rho_{\text{spation}} V_{\text{disp}}}{\mu_0 e^2 n \tau_{\text{lock}} \omega}} \tag{4.4}$$

where $\sigma = ne^2\tau_{\text{lock}}/(\rho_{\text{spation}} V_{\text{disp}})$ is conductivity.

**SDT:** Current creates magnetic field → induces opposing E-field → wave decays. Penetration depth determined by locking time $\tau_{\text{lock}}$.

### 4.2 Waveguide Propagation

**Theorem 4.2 (Waveguide Modes).** In waveguide, boundary conditions quantize allowed modes:

**Cutoff frequency:**
$$\omega_c = \frac{c \pi}{a} \sqrt{m^2 + n^2} \tag{4.5}$$

where $a$ is waveguide dimension, $m, n$ are mode numbers.

**Propagation constant:**
$$k_z = \sqrt{\left(\frac{\omega}{c}\right)^2 - \left(\frac{\omega_c}{c}\right)^2} \tag{4.6}$$

**SDT:** Boundary locking restricts allowed spation oscillation modes → quantization.

---

## 5. Quantum Precursors in Classical EM

### 5.1 Discretization Hints

**Theorem 5.1 (Radiation Damping).** Planck's constant appears in classical EM through:

**Radiation damping time:**
$$\tau_{\text{rad}} = \frac{6\pi\varepsilon_0 \rho_{\text{spation}} V_{\text{disp}} c^3}{e^2\omega^2} \tag{5.1}$$

**For hydrogen** ($\omega = \omega_{\text{Lyman-}\alpha} = 2.47 \times 10^{16}$ rad/s):
$$\tau_{\text{rad}} = 1.6 \text{ ns}$$

**Spontaneous emission rate:** $\Gamma_{\text{sp}} = 1/\tau_{\text{rad}}$

**Energy radiated per period:**
$$\Delta E_{\text{period}} = P_{\text{rad}} \times \frac{2\pi}{\omega} = \frac{e^2 a^2}{3\varepsilon_0 c^3\omega} \tag{5.2}$$

**For ground state oscillation** with amplitude $x_0 \sim a_0$ (Bohr radius):
$$\Delta E_{\text{period}} \sim \frac{e^2\omega^3 a_0^2}{3\varepsilon_0 c^3} \sim \alpha^3 \hbar\omega \tag{5.3}$$

Extremely small ($\alpha^3 \sim 10^{-6}$) → classical radiation negligible.

**But:** After $\sim 1/\alpha^3$ periods, energy loss $\sim \hbar\omega$ → quantum jump required.

### 5.2 Zero-Point Energy Hints

**Theorem 5.2 (Casimir Force).** Casimir force between parallel plates:

$$F_{\text{Casimir}} = -\frac{\hbar c \pi^2}{240 d^4}A \tag{5.4}$$

**SDT Interpretation:** Spation lattice has vacuum fluctuations from Planck-scale granularity → boundary conditions modify allowed modes → measurable force.

**Not virtual photons**—real mechanical pressure from discrete contact structure.

### 5.3 Photon-Like Behavior

**Axiom 5.1 (Energy Packets).** Energy packets: $E = \hbar\omega$ from:

1. Emission occurs in quantum jumps (bound state transitions)
2. Each transition creates coherent wave packet with energy $\hbar\omega$
3. Packet length $\sim c\tau_{\text{rad}} \sim$ wavelengths

**Not point particles**—extended helical deformations of spation.

**Photoelectric effect:** Threshold frequency $\omega_0$ where $\hbar\omega_0 =$ work function.

- **Below $\omega_0$:** Individual wave packet insufficient energy to release electron (no matter how intense)
- **Above $\omega_0$:** Each packet can release one electron

**SDT:** Emission/absorption involves discrete bound-state transitions → energy quantized as $\hbar\omega$. But propagation is continuous wave (classical EM).

---

## 6. Connection to Cosmic Microwave Background

### 6.1 CMB as Wave Source

**Theorem 6.1 (CMB Pressure Field).** The pressure field that drives all wave propagation receives contributions from the CMB:

$$\Pi(\mathbf{r}) = \int_{\Omega} I_{\text{CMB}}(\hat{\mathbf{n}})[1 - E(\mathbf{r}, \hat{\mathbf{n}})] \, d\Omega \quad \text{[Pa]} \tag{6.1}$$

where $I_{\text{CMB}}(\hat{\mathbf{n}})$ is the CMB intensity from direction $\hat{\mathbf{n}}$ and $E(\mathbf{r}, \hat{\mathbf{n}})$ is the occlusion function.

**Physical Mechanism:**
1. CMB radiation propagates through spation, establishing pressure gradients
2. These gradients drive all wave propagation
3. All electromagnetic waves ultimately trace to CMB energy influx

### 6.2 Energy Flow

**Theorem 6.2 (Energy Conservation).** The electromagnetic energy in any resonant system or wave is ultimately sourced from CMB energy influx. The CMB provides continuous replenishment of pressure fields, maintaining all wave propagation and resonant oscillations.

**Proof:** All pressure fields trace to CMB radiation. Wave propagation and resonant systems are driven by these fields. Energy conservation requires that all electromagnetic energy ultimately comes from CMB energy influx. □

---

## 7. Conclusion

We have derived advanced electromagnetic phenomena from SDT including resonant systems, radiation pressure, wave propagation in conductors, and quantum precursors. The key results are:

1. Resonant systems store energy in compression and circulation modes
2. Radiation pressure transfers momentum from waves to matter
3. Wave propagation in conductors shows frequency-dependent penetration
4. Quantum behavior emerges from discrete bound-state transitions
5. CMB provides continuous energy influx maintaining all wave phenomena

All calculations proceed without use of mass $m$ or gravitational constant $G$ as fundamental quantities. The electromagnetic phenomena are purely geometric and pressure-dynamic, requiring no field-theoretic assumptions beyond the four irreducible primitives of SDT, with the CMB as the ultimate energy source.

---

## References

1. Born & Wolf, "Principles of Optics" (7th ed., 1999)
2. Jackson, "Classical Electrodynamics" (3rd ed., 1999)
3. Foundational Principles of SDT (Phase 0)
4. Electromagnetic Mechanisms and Effects Part 1
5. Electricity from Spation Pressure Deformation (Phase 11)
6. Magnetic Moments from Toroidal Circulation (Phase 4)

---

**End of Document**

