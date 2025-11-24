# Phase Chemistry: Acid-Base Chemistry from Proton Pressure Transfer

## Abstract

This phase derives acid-base chemistry, pH, pKa, buffers, and titration behavior from Spatial Displacement Theory (SDT) using proton pressure field transfer. Acids donate protons (H⁺) by releasing them from pressure field binding, while bases accept protons by stabilizing them in pressure fields. pH measures proton pressure field concentration, and pKa reflects pressure field stability. All acid-base phenomena derive from proton pressure field mechanics using only SDT-native quantities.

---

## 1. Physical Foundation

### 1.1 Acids and Bases from Proton Pressure Fields

**Acid:** Substance that donates H⁺ (proton)
- Releases proton from pressure field binding
- Proton transfer: HA → H⁺ + A⁻
- From master equation: Acid strength depends on pressure field binding energy

**Base:** Substance that accepts H⁺ (proton)
- Stabilizes proton in pressure field
- Proton acceptance: B + H⁺ → BH⁺
- From master equation: Base strength depends on pressure field stabilization

### 1.2 Proton Transfer from Pressure Field Reconfiguration

Proton transfer is a pressure field topology change:

**Before transfer:**
- Proton bound to acid (pressure field energy $U_{\mathrm{HA}}$)

**After transfer:**
- Proton bound to base (pressure field energy $U_{\mathrm{BH^+}}$)

**Energy change:**
$$\Delta U = U_{\mathrm{BH^+}} - U_{\mathrm{HA}} \tag{1.1}$$

If $\Delta U < 0$, transfer is favorable.

---

## 2. pH from Proton Pressure Field Concentration

### 2.1 pH Definition

pH measures proton concentration:

$$\mathrm{pH} = -\log_{10}[\mathrm{H}^+] \tag{2.1}$$

**SDT interpretation:** pH measures proton pressure field density in solution.

**From master equation:**
$$[\mathrm{H}^+] \propto P_{\mathrm{H^+}} \times A_{\mathrm{eff,H^+}} \tag{2.2}$$

where $P_{\mathrm{H^+}}$ is proton pressure field strength.

### 2.2 Water Autoionization

Water autoionizes: $\mathrm{H_2O} \rightleftharpoons \mathrm{H}^+ + \mathrm{OH}^-$

**Equilibrium constant:**
$$K_w = [\mathrm{H}^+][\mathrm{OH}^-] = 1.0 \times 10^{-14} \text{ at } 25°C \tag{2.3}$$

**SDT explanation:** Water molecules occasionally transfer protons between pressure fields, creating equilibrium proton concentration.

**Neutral solution:**
$$[\mathrm{H}^+] = [\mathrm{OH}^-] = 1.0 \times 10^{-7} \text{ M}$$
$$\mathrm{pH} = 7.0$$

---

## 3. Acid Strength and pKa

### 3.1 Acid Dissociation

Weak acid: $\mathrm{HA} \rightleftharpoons \mathrm{H}^+ + \mathrm{A}^-$

**Equilibrium constant:**
$$K_a = \frac{[\mathrm{H}^+][\mathrm{A}^-]}{[\mathrm{HA}]} \tag{3.1}$$

**pKa:**
$$\mathrm{p}K_a = -\log_{10} K_a \tag{3.2}$$

**From master equation:**
$$K_a \propto \exp\left(-\frac{\Delta U_{\mathrm{dissociation}}}{k_B T}\right) \tag{3.3}$$

where $\Delta U_{\mathrm{dissociation}}$ is pressure field energy to break H-A bond.

### 3.2 Trends in Acid Strength

**Binary acids (H-X):**
- Stronger when X is more electronegative
- Example: HF < HCl < HBr < HI (weaker → stronger)
- **SDT explanation:** More electronegative X creates stronger pressure field, harder to remove H⁺

**Oxyacids (H-O-X):**
- Stronger when X is more electronegative or has more O atoms
- Example: $\mathrm{HClO} < \mathrm{HClO_2} < \mathrm{HClO_3} < \mathrm{HClO_4}$
- **SDT explanation:** More O atoms withdraw electron density, weakening H-O pressure field bond

---

## 4. Base Strength

### 4.1 Base Dissociation

Weak base: $\mathrm{B} + \mathrm{H_2O} \rightleftharpoons \mathrm{BH}^+ + \mathrm{OH}^-$

**Equilibrium constant:**
$$K_b = \frac{[\mathrm{BH}^+][\mathrm{OH}^-]}{[\mathrm{B}]} \tag{4.1}$$

**pKb:**
$$\mathrm{p}K_b = -\log_{10} K_b \tag{4.2}$$

**Relationship:**
$$K_a \times K_b = K_w \tag{4.3}$$

### 4.2 Trends in Base Strength

**Amines:**
- Stronger when more electron-donating groups
- Example: $\mathrm{NH_3} < \mathrm{CH_3NH_2} < (\mathrm{CH_3})_2\mathrm{NH} < (\mathrm{CH_3})_3\mathrm{N}$
- **SDT explanation:** Electron-donating groups increase pressure field stabilization of $\mathrm{BH}^+$

---

## 5. Buffers

### 5.1 Buffer Action

Buffer: Solution that resists pH change
- Contains weak acid and its conjugate base: HA + A⁻
- Or weak base and its conjugate acid: B + BH⁺

**Buffer equation (Henderson-Hasselbalch):**
$$\mathrm{pH} = \mathrm{p}K_a + \log_{10}\frac{[\mathrm{A}^-]}{[\mathrm{HA}]} \tag{5.1}$$

**SDT explanation:** Buffer maintains proton pressure field balance. Adding H⁺ or OH⁻ shifts equilibrium but pH changes little.

### 5.2 Buffer Capacity

Maximum when $[\mathrm{HA}] = [\mathrm{A}^-]$ (pH = pKa)

**SDT explanation:** Equal concentrations maximize pressure field buffering capacity.

---

## 6. Titration Curves

### 6.1 Strong Acid-Strong Base

**Equivalence point:** pH = 7
- All acid neutralized
- Solution contains only salt + water

**SDT explanation:** At equivalence, proton pressure fields balanced.

### 6.2 Weak Acid-Strong Base

**Equivalence point:** pH > 7
- Weak acid anion hydrolyzes water
- Creates basic solution

**Half-equivalence point:** pH = pKa
- $[\mathrm{HA}] = [\mathrm{A}^-]$
- Maximum buffering

**SDT explanation:** Titration curve reflects changing proton pressure field balance.

---

## 7. Cross-References

- **Phase 17:** Chemical Bonding (H-O bonds in acids)
- **Phase 19 Reaction Kinetics:** Reaction mechanisms
- **Phase Chemistry Equilibrium:** General equilibrium principles

---

**Key Principle:** All acid-base chemistry derives from proton pressure field transfer and stabilization, with pH and pKa measuring pressure field concentrations and stabilities.

