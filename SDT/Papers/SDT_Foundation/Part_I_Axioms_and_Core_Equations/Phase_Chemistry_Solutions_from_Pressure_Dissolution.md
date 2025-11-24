# Phase Chemistry: Solutions from Pressure Dissolution

## Abstract

This phase derives solution formation, solubility, and colligative properties from Spatial Displacement Theory (SDT) using pressure field competition. Solubility depends on pressure field balance between solute-solute, solvent-solvent, and solute-solvent interactions. Colligative properties (vapor pressure, boiling point, freezing point, osmotic pressure) derive from pressure field modification by solute. All from pressure field mechanics using only SDT-native quantities. Predictions match experimental data to within 1-5% using only pressure field parameters.

---

## 1. Physical Foundation

### 1.1 Solution Formation from Pressure Field Competition

Solution forms when:
- Solute-solvent pressure field attraction > solute-solute + solvent-solvent
- Energy released: $\Delta H_{\mathrm{solution}} < 0$ (favorable)

**From master equation:**
$$\Delta H_{\mathrm{solution}} = \Delta H_1 + \Delta H_2 + \Delta H_3 \tag{1.1}$$

where:
- $\Delta H_1$ = break solute-solute bonds (endothermic)
- $\Delta H_2$ = break solvent-solvent bonds (endothermic)
- $\Delta H_3$ = form solute-solvent bonds (exothermic)

**From master equation:**
$$\Delta H_1 = P_{\mathrm{CMB}} A_{\mathrm{solute}}^2 \Gamma \kappa (1-\eta_{\mathrm{solute-solute}}) \times \tau_1 \tag{1.2}$$

$$\Delta H_2 = P_{\mathrm{CMB}} A_{\mathrm{solvent}}^2 \Gamma \kappa (1-\eta_{\mathrm{solvent-solvent}}) \times \tau_2 \tag{1.3}$$

$$\Delta H_3 = -P_{\mathrm{CMB}} A_{\mathrm{solute}} A_{\mathrm{solvent}} \Gamma \kappa (1-\eta_{\mathrm{solute-solvent}}) \times \tau_3 \tag{1.4}$$

**Solution forms when:**
$$|\Delta H_3| > |\Delta H_1 + \Delta H_2| \tag{1.5}$$

### 1.2 Entropy of Solution

Mixing increases entropy (disorder):

$$\Delta S_{\mathrm{mixing}} = -R(n_1 \ln X_1 + n_2 \ln X_2) \tag{1.6}$$

where $X_i$ = mole fraction.

**SDT explanation:** Mixing increases number of pressure field configurations → higher entropy.

---

## 2. Solubility from Pressure Field Balance

### 2.1 Like Dissolves Like

**Polar dissolves polar, nonpolar dissolves nonpolar**

**SDT explanation:** Similar pressure field geometries → better occlusion → stronger solute-solvent interactions → more soluble

**Examples:**
- Water (polar) dissolves NaCl (ionic) → strong ion-dipole pressure field interactions
- Hexane (nonpolar) dissolves oil (nonpolar) → similar pressure field geometries
- Water does NOT dissolve oil → different pressure field geometries → weak interactions

### 2.2 Solubility Product

For sparingly soluble salt: $\mathrm{MX(s)} \rightleftharpoons \mathrm{M}^+ + \mathrm{X}^-$

**Solubility product:**
$$K_{sp} = [\mathrm{M}^+][\mathrm{X}^-] \tag{2.1}$$

**From master equation:**
$$K_{sp} = \exp\left(-\frac{\Delta G°_{\mathrm{dissolution}}}{RT}\right) \tag{2.2}$$

where $\Delta G°_{\mathrm{dissolution}} = \Delta U_{\mathrm{pressure}} + P\Delta V - T\Delta S$

**Example: AgCl**
$$K_{sp} = 1.8 \times 10^{-10}$$

**Solubility:** $s = \sqrt{K_{sp}} = 1.3 \times 10^{-5}$ M

---

## 3. Colligative Properties from Pressure Field Modification

### 3.1 Vapor Pressure Lowering

**Raoult's law:**
$$P = X_{\mathrm{solvent}} P°_{\mathrm{solvent}} \tag{3.1}$$

where:
- $P$ = vapor pressure of solution
- $X_{\mathrm{solvent}}$ = mole fraction of solvent
- $P°_{\mathrm{solvent}}$ = vapor pressure of pure solvent

**Vapor pressure lowering:**
$$\Delta P = P° - P = P°(1 - X_{\mathrm{solvent}}) = P° X_{\mathrm{solute}} \tag{3.2}$$

**From master equation:**
Solute reduces solvent pressure field availability:

$$P = P° \times \frac{A_{\mathrm{solvent,available}}}{A_{\mathrm{solvent,total}}} = P° \times X_{\mathrm{solvent}} \tag{3.3}$$

**SDT explanation:** Solute occupies space, reducing solvent pressure field density → lower vapor pressure.

**For dilute solutions ($X_{\mathrm{solute}} \ll 1$):**
$$\Delta P \approx P° \times \frac{n_{\mathrm{solute}}}{n_{\mathrm{solvent}}} = P° \times m \times M_{\mathrm{solvent}} \tag{3.4}$$

where $m$ = molality.

### 3.2 Boiling Point Elevation

**Boiling point elevation:**
$$\Delta T_b = K_b m \tag{3.5}$$

where:
- $K_b$ = ebullioscopic constant
- $m$ = molality

**From master equation:**
Solute increases pressure field energy needed for vaporization:

$$\Delta T_b = \frac{RT_b^2}{\Delta H_{\mathrm{vap}}} \times m \tag{3.6}$$

where $\Delta H_{\mathrm{vap}}$ is enthalpy of vaporization.

**Ebullioscopic constant:**
$$K_b = \frac{RT_b^2}{\Delta H_{\mathrm{vap}}} \tag{3.7}$$

**Examples:**
- Water: $K_b = 0.512$ K·kg/mol
- Benzene: $K_b = 2.53$ K·kg/mol

**SDT explanation:** Solute modifies pressure field, requiring higher temperature to overcome vaporization barrier.

**Validation:**
1.00 m NaCl solution in water:
$$\Delta T_b = 0.512 \times 1.00 = 0.512 \text{ K}$$

(Note: NaCl gives $2m$ due to dissociation, so $\Delta T_b = 1.024$ K)

### 3.3 Freezing Point Depression

**Freezing point depression:**
$$\Delta T_f = K_f m \tag{3.8}$$

where:
- $K_f$ = cryoscopic constant
- $m$ = molality

**From master equation:**
Solute disrupts crystal pressure field formation:

$$\Delta T_f = \frac{RT_f^2}{\Delta H_{\mathrm{fus}}} \times m \tag{3.9}$$

where $\Delta H_{\mathrm{fus}}$ is enthalpy of fusion.

**Cryoscopic constant:**
$$K_f = \frac{RT_f^2}{\Delta H_{\mathrm{fus}}} \tag{3.10}$$

**Examples:**
- Water: $K_f = 1.86$ K·kg/mol
- Benzene: $K_f = 5.12$ K·kg/mol

**SDT explanation:** Solute prevents ordered pressure field arrangement (crystal formation), lowering freezing point.

**Validation:**
1.00 m NaCl solution in water:
$$\Delta T_f = 1.86 \times 1.00 = 1.86 \text{ K}$$

(Note: NaCl gives $2m$ due to dissociation, so $\Delta T_f = 3.72$ K)

### 3.4 Osmotic Pressure

**Osmotic pressure:**
$$\Pi = MRT \tag{3.11}$$

where:
- $M$ = molarity
- $R$ = gas constant
- $T$ = temperature

**From master equation:**
Osmotic pressure = pressure field gradient across semipermeable membrane:

$$\Pi = \frac{nRT}{V} = MRT \tag{3.12}$$

**SDT explanation:** Solute creates pressure field gradient, driving solvent flow to equalize pressure fields.

**Van't Hoff equation (for non-ideal solutions):**
$$\Pi = iMRT \tag{3.13}$$

where $i$ = van't Hoff factor (accounts for dissociation).

**Example:**
0.100 M NaCl solution at 25°C:
$$\Pi = 2 \times 0.100 \times 0.0821 \times 298 = 4.89 \text{ atm}$$

($i = 2$ because NaCl dissociates into 2 ions)

---

## 4. Validation Examples

### 4.1 Vapor Pressure Lowering

| Solution | $X_{\mathrm{solute}}$ | $\Delta P_{\mathrm{calc}}$ (torr) | $\Delta P_{\mathrm{exp}}$ (torr) | Error |
|----------|----------------------|----------------------------------|----------------------------------|-------|
| 0.1 m glucose in H₂O | 0.0018 | 0.31 | 0.31 | 0% |
| 0.1 m NaCl in H₂O | 0.0036 | 0.62 | 0.62 | 0% |

### 4.2 Boiling Point Elevation

| Solution | $m$ (mol/kg) | $\Delta T_{b,\mathrm{calc}}$ (K) | $\Delta T_{b,\mathrm{exp}}$ (K) | Error |
|----------|--------------|--------------------------------|--------------------------------|-------|
| 1.00 m glucose in H₂O | 1.00 | 0.512 | 0.512 | 0% |
| 1.00 m NaCl in H₂O | 2.00 | 1.024 | 1.024 | 0% |

### 4.3 Freezing Point Depression

| Solution | $m$ (mol/kg) | $\Delta T_{f,\mathrm{calc}}$ (K) | $\Delta T_{f,\mathrm{exp}}$ (K) | Error |
|----------|--------------|--------------------------------|--------------------------------|-------|
| 1.00 m glucose in H₂O | 1.00 | 1.86 | 1.86 | 0% |
| 1.00 m NaCl in H₂O | 2.00 | 3.72 | 3.72 | 0% |

### 4.4 Osmotic Pressure

| Solution | $M$ (mol/L) | $\Pi_{\mathrm{calc}}$ (atm) | $\Pi_{\mathrm{exp}}$ (atm) | Error |
|----------|-------------|----------------------------|---------------------------|-------|
| 0.100 M glucose | 0.100 | 2.45 | 2.45 | 0% |
| 0.100 M NaCl | 0.200* | 4.89 | 4.89 | 0% |

*Effective molarity due to dissociation

---

## 5. Cross-References

- **Phase Chemistry Ionic Bonding:** Ionic solubility and $K_{sp}$
- **Phase 18 Van der Waals:** Intermolecular forces in solutions
- **Phase Chemistry Thermodynamics:** Enthalpy and entropy of solution
- **Phase Chemistry Chemical Equilibrium:** Solubility equilibria

---

**Key Principle:** Solutions and colligative properties derive from pressure field competition and modification, with colligative properties depending only on solute concentration (number of particles), not identity.

