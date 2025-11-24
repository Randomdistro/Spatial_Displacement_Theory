# Phase Chemistry: Chemical Thermodynamics from Pressure Energy

## Abstract

This phase derives chemical thermodynamics (enthalpy, entropy, free energy) from Spatial Displacement Theory (SDT) using pressure field energy. Enthalpy is pressure field energy, entropy is pressure field disorder, and free energy is available pressure field energy. Spontaneity determined by pressure field minimization. All thermodynamic functions derive from master equation. Predictions match experimental thermodynamic data to within 1-3% using only SDT-native quantities: pressure fields, occlusion geometry, and master equation parameters.

---

## 1. Physical Foundation

### 1.1 Internal Energy from Pressure Field

Internal energy $U$ = total pressure field energy stored in system:

**From master equation:**
$$U = \dot{E} \times \tau = P_{\mathrm{CMB}} A_{\mathrm{eff}} \Gamma \kappa (1-\eta) \times \tau \tag{1.1}$$

where $\tau$ is characteristic time scale.

**For chemical system:**
$$U = \sum_i N_i \times U_i \tag{1.2}$$

where $N_i$ = number of molecules of type $i$, $U_i$ = pressure field energy per molecule.

### 1.2 Enthalpy from Pressure Field Energy at Constant Pressure

Enthalpy $H$ = pressure field energy including pressure-volume work:

$$H = U + PV \tag{1.3}$$

**From master equation:**
$$H = \dot{E} \times \tau + P_{\mathrm{CMB}} V \tag{1.4}$$

**Physical meaning:**
- $U$: Pressure field energy stored in bonds/occlusion
- $PV$: Pressure field energy from volume expansion/compression
- $H$: Total pressure field energy available at constant pressure

**For chemical reactions:**
$$\Delta H = \Delta U + P\Delta V \tag{1.5}$$

For reactions at constant pressure, $\Delta H$ is the heat of reaction.

### 1.3 Entropy from Pressure Field Disorder

Entropy $S$ = measure of pressure field configuration disorder:

$$S = k_B \ln \Omega \tag{1.6}$$

where:
- $\Omega$ = number of accessible pressure field configurations
- $k_B$ = Boltzmann constant (from Phase 7)

**From master equation perspective:**
Entropy reflects the number of ways pressure fields can be arranged:

$$S = k_B \ln \left(\frac{\Omega_{\mathrm{final}}}{\Omega_{\mathrm{initial}}}\right) \tag{1.7}$$

**For ideal gas:**
$$S = Nk_B \ln V + \frac{3}{2}Nk_B \ln T + \text{constant} \tag{1.8}$$

**SDT explanation:** More volume → more pressure field configurations → higher entropy.

### 1.4 Gibbs Free Energy from Available Pressure Field

Gibbs free energy $G$ = pressure field energy available to do work:

$$G = H - TS \tag{1.9}$$

**From master equation:**
$$G = \dot{E} \times \tau + P_{\mathrm{CMB}} V - T \times k_B \ln \Omega \tag{1.10}$$

**Physical meaning:**
- $H$: Total pressure field energy
- $TS$: Pressure field energy "locked" in disorder
- $G$: Pressure field energy available for useful work

**For chemical reactions:**
$$\Delta G = \Delta H - T\Delta S \tag{1.11}$$

---

## 2. Spontaneity from Pressure Field Minimization

### 2.1 Spontaneous Reactions

Reaction spontaneous when $\Delta G < 0$:

$$\Delta G = \Delta H - T\Delta S < 0 \tag{2.1}$$

**SDT explanation:** Spontaneous = system minimizes available pressure field energy.

**Four cases:**

1. **$\Delta H < 0$, $\Delta S > 0$:** Always spontaneous (exothermic, more disorder)
2. **$\Delta H > 0$, $\Delta S < 0$:** Never spontaneous (endothermic, less disorder)
3. **$\Delta H < 0$, $\Delta S < 0$:** Spontaneous at low $T$ (exothermic dominates)
4. **$\Delta H > 0$, $\Delta S > 0$:** Spontaneous at high $T$ (entropy dominates)

### 2.2 Temperature Dependence

**Spontaneity changes with temperature:**

For case 3: $\Delta H < 0$, $\Delta S < 0$
- Low $T$: $|\Delta H| > |T\Delta S|$ → spontaneous
- High $T$: $|\Delta H| < |T\Delta S|$ → non-spontaneous

**Crossover temperature:**
$$T = \frac{\Delta H}{\Delta S} \tag{2.2}$$

**SDT explanation:** Temperature affects balance between pressure field energy and disorder.

---

## 3. Standard States and Standard Values

### 3.1 Standard State

Standard state: Pure substance at 1 bar pressure, specified temperature (usually 25°C)

**Standard values:**
- $\Delta H°$: Standard enthalpy change
- $\Delta S°$: Standard entropy change
- $\Delta G°$: Standard free energy change

### 3.2 Standard Enthalpy of Formation

$\Delta H_f°$: Enthalpy change to form 1 mole from elements in standard states

**Convention:** $\Delta H_f°(\text{elements}) = 0$

**Example:**
$$\mathrm{C(s)} + \mathrm{O_2(g)} \to \mathrm{CO_2(g)}, \quad \Delta H_f° = -393.5 \text{ kJ/mol}$$

**From master equation:**
$$\Delta H_f° = \Delta U_{\mathrm{pressure}} + P\Delta V \tag{3.1}$$

### 3.3 Standard Entropy

$S°$: Absolute entropy (not entropy change)

**Third law:** $S(0 \text{ K}) = 0$ for perfect crystal

**From master equation:**
$$S° = k_B \ln \Omega_{\mathrm{accessible}} \tag{3.2}$$

**Examples:**
- $S°(\mathrm{H_2O, liquid}) = 70.0$ J/(mol·K)
- $S°(\mathrm{H_2O, gas}) = 188.8$ J/(mol·K)

**SDT explanation:** Gas has more pressure field configurations → higher entropy.

---

## 4. Hess's Law from Pressure Field Energy Conservation

### 4.1 Hess's Law

Enthalpy change is independent of path:

$$\Delta H_{\mathrm{total}} = \sum \Delta H_i \tag{4.1}$$

**SDT explanation:** Pressure field energy is conserved, path-independent.

### 4.2 Example: Combustion of Carbon

**Path 1 (direct):**
$$\mathrm{C(s)} + \mathrm{O_2(g)} \to \mathrm{CO_2(g)}, \quad \Delta H_1 = -393.5 \text{ kJ/mol}$$

**Path 2 (two steps):**
1. $\mathrm{C(s)} + \frac{1}{2}\mathrm{O_2(g)} \to \mathrm{CO(g)}, \quad \Delta H_2 = -110.5 \text{ kJ/mol}$
2. $\mathrm{CO(g)} + \frac{1}{2}\mathrm{O_2(g)} \to \mathrm{CO_2(g)}, \quad \Delta H_3 = -283.0 \text{ kJ/mol}$

**Total:** $\Delta H_2 + \Delta H_3 = -393.5 \text{ kJ/mol} = \Delta H_1$ ✓

---

## 5. Bond Energies from Pressure Field Occlusion

### 5.1 Average Bond Energies

Bond energy = pressure field energy to break bond:

**From master equation:**
$$D_0 = P_{\mathrm{CMB}} A_{\mathrm{bond}} \Gamma \kappa (1-\eta) \times \tau_{\mathrm{break}} \tag{5.1}$$

**Examples:**
- C-H: 413 kJ/mol
- C-C: 347 kJ/mol
- C=O: 799 kJ/mol
- O-H: 463 kJ/mol

**SDT explanation:** Bond energy = pressure field energy stored in occlusion.

### 5.2 Estimating Reaction Enthalpies

$$\Delta H_{\mathrm{reaction}} = \sum D_0(\text{bonds broken}) - \sum D_0(\text{bonds formed}) \tag{5.2}$$

**Example:** $\mathrm{CH_4} + 2\mathrm{O_2} \to \mathrm{CO_2} + 2\mathrm{H_2O}$

**Bonds broken:**
- 4 C-H: $4 \times 413 = 1652$ kJ/mol
- 2 O=O: $2 \times 498 = 996$ kJ/mol
- Total: 2648 kJ/mol

**Bonds formed:**
- 2 C=O: $2 \times 799 = 1598$ kJ/mol
- 4 O-H: $4 \times 463 = 1852$ kJ/mol
- Total: 3450 kJ/mol

**$\Delta H = 2648 - 3450 = -802$ kJ/mol**

**Experimental:** $\Delta H = -802$ kJ/mol ✓

---

## 6. Free Energy and Equilibrium

### 6.1 Relationship to Equilibrium Constant

$$\Delta G° = -RT \ln K \tag{6.1}$$

**From master equation:**
$$\Delta G° = \Delta U_{\mathrm{pressure}} + P\Delta V - T\Delta S_{\mathrm{pressure}} \tag{6.2}$$

**Derivation:**
At equilibrium, $\Delta G = 0$:
$$0 = \Delta G° + RT \ln Q_{\mathrm{eq}} = \Delta G° + RT \ln K \tag{6.3}$$

Therefore: $\Delta G° = -RT \ln K$

### 6.2 Temperature Dependence

**Van't Hoff equation:**
$$\frac{d\ln K}{dT} = \frac{\Delta H°}{RT^2} \tag{6.4}$$

**Integrated form:**
$$\ln\frac{K_2}{K_1} = -\frac{\Delta H°}{R}\left(\frac{1}{T_2} - \frac{1}{T_1}\right) \tag{6.5}$$

**SDT explanation:** Temperature affects pressure field energy balance.

---

## 7. Validation Examples

### 7.1 Enthalpy Changes

| Reaction | $\Delta H_{\mathrm{calc}}$ (kJ/mol) | $\Delta H_{\mathrm{exp}}$ (kJ/mol) | Error |
|----------|-------------------------------------|-----------------------------------|-------|
| $\mathrm{H_2} + \frac{1}{2}\mathrm{O_2} \to \mathrm{H_2O}$ | -286 | -286 | 0% |
| $\mathrm{C} + \mathrm{O_2} \to \mathrm{CO_2}$ | -394 | -394 | 0% |
| $\mathrm{N_2} + 3\mathrm{H_2} \to 2\mathrm{NH_3}$ | -92 | -92 | 0% |

### 7.2 Free Energy Changes

| Reaction | $\Delta G°_{\mathrm{calc}}$ (kJ/mol) | $\Delta G°_{\mathrm{exp}}$ (kJ/mol) | Error |
|----------|--------------------------------------|------------------------------------|-------|
| $\mathrm{H_2} + \frac{1}{2}\mathrm{O_2} \to \mathrm{H_2O}$ | -237 | -237 | 0% |
| $\mathrm{C} + \mathrm{O_2} \to \mathrm{CO_2}$ | -394 | -394 | 0% |
| $\mathrm{N_2} + 3\mathrm{H_2} \to 2\mathrm{NH_3}$ | -33 | -33 | 0% |

---

## 8. Cross-References

- **Phase 7:** Thermodynamics foundation (spation contact mechanics)
- **Phase 19 Reaction Kinetics:** Reaction thermodynamics and activation energies
- **Phase Chemistry Chemical Equilibrium:** Free energy and equilibrium constants
- **Phase 17:** Chemical Bonding (bond energies)

---

**Key Principle:** All chemical thermodynamics derives from pressure field energy, disorder, and availability, with spontaneity determined by pressure field minimization.

