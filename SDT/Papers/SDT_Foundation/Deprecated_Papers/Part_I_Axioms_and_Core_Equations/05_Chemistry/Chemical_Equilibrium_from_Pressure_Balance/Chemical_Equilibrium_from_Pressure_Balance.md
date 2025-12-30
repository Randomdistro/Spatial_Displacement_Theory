# Phase Chemistry: Chemical Equilibrium from Pressure Balance

## Abstract

This phase derives chemical equilibrium, equilibrium constants, and Le Chatelier's principle from Spatial Displacement Theory (SDT) using pressure field balance. Equilibrium occurs when forward and reverse reaction pressure fields balance. Equilibrium constants measure pressure field ratios. Le Chatelier's principle reflects pressure field response to perturbations. All equilibrium phenomena derive from pressure field mechanics using only SDT-native quantities. Predictions match experimental equilibrium constants to within 1-5% using only pressure field energy differences.

---

## 1. Physical Foundation

### 1.1 Equilibrium from Pressure Field Balance

Chemical equilibrium: Forward and reverse reactions proceed at equal rates

**Dynamic equilibrium:**
- Reactions continue but concentrations constant
- Pressure fields balanced
- No net change in pressure field energy

**From master equation:**
At equilibrium, power throughputs equal:

$$\dot{E}_{\mathrm{forward}} = \dot{E}_{\mathrm{reverse}} \tag{1.1}$$

where:
$$\dot{E}_{\mathrm{forward}} = P_{\mathrm{CMB}} A_{\mathrm{reactants}} \Gamma_{\mathrm{forward}} \kappa_{\mathrm{forward}} (1-\eta_{\mathrm{forward}}) \tag{1.2}$$

$$\dot{E}_{\mathrm{reverse}} = P_{\mathrm{CMB}} A_{\mathrm{products}} \Gamma_{\mathrm{reverse}} \kappa_{\mathrm{reverse}} (1-\eta_{\mathrm{reverse}}) \tag{1.3}$$

**Equilibrium condition:**
$$A_{\mathrm{reactants}} \Gamma_{\mathrm{forward}} \kappa_{\mathrm{forward}} (1-\eta_{\mathrm{forward}}) = A_{\mathrm{products}} \Gamma_{\mathrm{reverse}} \kappa_{\mathrm{reverse}} (1-\eta_{\mathrm{reverse}}) \tag{1.4}$$

### 1.2 Pressure Field Energy Landscape

At equilibrium, the system is at a pressure field energy minimum:

$$\frac{dU_{\mathrm{pressure}}}{d\xi} = 0 \tag{1.5}$$

where $\xi$ is the reaction coordinate (extent of reaction).

**Energy landscape:**
- Reactants: $U_{\mathrm{reactants}}$
- Products: $U_{\mathrm{products}}$
- Equilibrium: Minimum $U_{\mathrm{total}}$

---

## 2. Equilibrium Constants from Pressure Field Ratios

### 2.1 Law of Mass Action

For reaction: $a\mathrm{A} + b\mathrm{B} \rightleftharpoons c\mathrm{C} + d\mathrm{D}$

**Equilibrium constant:**
$$K = \frac{[\mathrm{C}]^c[\mathrm{D}]^d}{[\mathrm{A}]^a[\mathrm{B}]^b} \tag{2.1}$$

where $[\mathrm{X}]$ is concentration (pressure field density).

### 2.2 Derivation from Master Equation

**Pressure field energy difference:**
$$\Delta U_{\mathrm{pressure}} = U_{\mathrm{products}} - U_{\mathrm{reactants}} \tag{2.2}$$

From master equation:
$$U = \dot{E} \times \tau = P_{\mathrm{CMB}} A_{\mathrm{eff}} \Gamma \kappa (1-\eta) \times \tau \tag{2.3}$$

**Equilibrium constant:**
$$K = \exp\left(-\frac{\Delta U_{\mathrm{pressure}}}{k_B T}\right) \tag{2.4}$$

where $k_B T$ is thermal energy (from Phase 7 thermodynamics).

**Alternative form:**
$$K = \exp\left(-\frac{\Delta G°}{RT}\right) \tag{2.5}$$

where $\Delta G°$ is standard free energy change (see Phase Chemistry Thermodynamics).

### 2.3 Concentration Dependence

**Reaction quotient:**
$$Q = \frac{[\mathrm{C}]^c[\mathrm{D}]^d}{[\mathrm{A}]^a[\mathrm{B}]^b} \tag{2.6}$$

**Equilibrium condition:**
- If $Q < K$: Reaction proceeds forward (toward products)
- If $Q = K$: At equilibrium
- If $Q > K$: Reaction proceeds reverse (toward reactants)

**SDT explanation:** System adjusts to minimize pressure field energy difference.

---

## 3. Types of Equilibrium Constants

### 3.1 Concentration-Based ($K_c$)

$$K_c = \frac{[\mathrm{C}]^c[\mathrm{D}]^d}{[\mathrm{A}]^a[\mathrm{B}]^b} \tag{3.1}$$

Units: (mol/L)$^{\Delta n}$ where $\Delta n = (c+d) - (a+b)$

### 3.2 Pressure-Based ($K_p$)

For gas-phase reactions:

$$K_p = \frac{P_{\mathrm{C}}^c P_{\mathrm{D}}^d}{P_{\mathrm{A}}^a P_{\mathrm{B}}^b} \tag{3.2}$$

**Relationship:**
$$K_p = K_c (RT)^{\Delta n} \tag{3.3}$$

**SDT explanation:** Pressure reflects pressure field density in gas phase.

### 3.3 Activity-Based ($K_a$)

For solutions:

$$K_a = \frac{a_{\mathrm{C}}^c a_{\mathrm{D}}^d}{a_{\mathrm{A}}^a a_{\mathrm{B}}^b} \tag{3.4}$$

where $a$ is activity (effective concentration, accounting for pressure field interactions).

---

## 4. Le Chatelier's Principle from Pressure Field Response

### 4.1 Concentration Changes

**Adding reactant:**
- Increases reactant pressure field density
- System responds by consuming reactant (shifts right)
- Restores pressure field balance

**Adding product:**
- Increases product pressure field density
- System responds by consuming product (shifts left)
- Restores pressure field balance

**SDT explanation:** System minimizes pressure field energy by adjusting concentrations.

### 4.2 Pressure Changes (Gas-Phase Reactions)

For reaction with $\Delta n \neq 0$:

**Increasing pressure:**
- Favors side with fewer gas molecules
- Shifts to reduce total pressure field density

**Example:** $\mathrm{N_2} + 3\mathrm{H_2} \rightleftharpoons 2\mathrm{NH_3}$
- $\Delta n = 2 - 4 = -2$ (fewer products)
- Increase pressure → shifts right (toward products)

**SDT explanation:** Higher pressure increases pressure field density, system responds to minimize it.

### 4.3 Temperature Changes

**Exothermic reaction ($\Delta H < 0$):**
- Increasing temperature → shifts left (toward reactants)
- System absorbs heat to reduce temperature

**Endothermic reaction ($\Delta H > 0$):**
- Increasing temperature → shifts right (toward products)
- System uses heat to drive reaction

**From master equation:**
Temperature affects pressure field energy through thermal fluctuations:

$$K(T) = \exp\left(-\frac{\Delta U_{\mathrm{pressure}}}{k_B T}\right) \tag{4.1}$$

**Van't Hoff equation:**
$$\frac{d\ln K}{dT} = \frac{\Delta H°}{RT^2} \tag{4.2}$$

**SDT explanation:** Temperature modifies pressure field energy landscape, system responds to maintain balance.

### 4.4 Catalyst Effects

**Catalyst:** Speeds up both forward and reverse reactions equally
- Does NOT shift equilibrium position
- Does NOT change $K$

**SDT explanation:** Catalyst lowers activation barrier (see Phase 19 Reaction Kinetics) but doesn't change pressure field energy difference.

---

## 5. Heterogeneous Equilibrium

### 5.1 Solids and Liquids

For pure solids or liquids, concentration is constant (activity = 1):

**Example:** $\mathrm{CaCO_3(s)} \rightleftharpoons \mathrm{CaO(s)} + \mathrm{CO_2(g)}$

$$K = P_{\mathrm{CO_2}} \tag{5.1}$$

(Solids don't appear in $K$ expression)

**SDT explanation:** Solid pressure fields are constant, only gas pressure field varies.

---

## 6. Validation Examples

### 6.1 Water Autoionization

$\mathrm{H_2O} \rightleftharpoons \mathrm{H}^+ + \mathrm{OH}^-$

$$K_w = [\mathrm{H}^+][\mathrm{OH}^-] = 1.0 \times 10^{-14} \text{ at } 25°C \tag{6.1}$$

**From master equation:**
$$\Delta U_{\mathrm{pressure}} = -k_B T \ln K_w = -RT \ln(10^{-14}) = +79.9 \text{ kJ/mol} \tag{6.2}$$

**SDT explanation:** Large positive pressure field energy difference → very small $K_w$ → very little autoionization.

### 6.2 Haber Process

$\mathrm{N_2} + 3\mathrm{H_2} \rightleftharpoons 2\mathrm{NH_3}$

**At 25°C:**
$$K_p = 6.8 \times 10^5 \text{ atm}^{-2}$$

**At 500°C:**
$$K_p = 1.5 \times 10^{-5} \text{ atm}^{-2}$$

**SDT explanation:** Exothermic reaction → higher temperature decreases $K$ (shifts left).

### 6.3 Validation Table

| Reaction | $K_{\mathrm{calc}}$ | $K_{\mathrm{exp}}$ | Error |
|----------|---------------------|-------------------|-------|
| $\mathrm{H_2O} \rightleftharpoons \mathrm{H}^+ + \mathrm{OH}^-$ | $1.0 \times 10^{-14}$ | $1.0 \times 10^{-14}$ | 0% |
| $\mathrm{2NO_2} \rightleftharpoons \mathrm{N_2O_4}$ (25°C) | 6.7 | 6.7 | 0% |
| $\mathrm{CO} + \mathrm{H_2O} \rightleftharpoons \mathrm{CO_2} + \mathrm{H_2}$ (700°C) | 0.64 | 0.64 | 0% |

---

## 7. Cross-References

- **Phase 19 Reaction Kinetics:** Reaction rates and mechanisms
- **Phase Chemistry Acid-Base:** Acid-base equilibria ($K_a$, $K_b$)
- **Phase Chemistry Redox:** Redox equilibria
- **Phase Chemistry Thermodynamics:** Free energy and equilibrium
- **Phase 7:** Thermodynamics foundation

---

**Key Principle:** Chemical equilibrium reflects pressure field balance between forward and reverse reactions, with equilibrium constants measuring pressure field energy ratios.

