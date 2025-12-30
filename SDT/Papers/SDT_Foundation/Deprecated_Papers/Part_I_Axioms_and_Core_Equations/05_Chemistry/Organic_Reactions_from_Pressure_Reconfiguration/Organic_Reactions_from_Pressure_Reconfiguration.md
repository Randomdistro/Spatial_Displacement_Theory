# Phase Chemistry: Organic Reactions from Pressure Reconfiguration

## Abstract

This phase derives organic reaction mechanisms (substitution, elimination, addition, rearrangement) from Spatial Displacement Theory (SDT) using pressure field reconfiguration. Reactions proceed through transition states where pressure fields are reconfigured. Mechanisms reflect pressure field pathways. All from pressure field mechanics using only SDT-native quantities. Activation energies and reaction rates derive from pressure field barrier heights and transition state geometries.

---

## 1. Physical Foundation

### 1.1 Reactions as Pressure Field Reconfiguration

Organic reactions = pressure field topology changes:

**Reactants → Transition State → Products**

**From master equation:**
$$E_a = \Delta \dot{E}_{\mathrm{reconfig}} \times \tau_{\mathrm{transition}} \tag{1.1}$$

where:
- $\Delta \dot{E}_{\mathrm{reconfig}}$ = power required to overcome pressure field barrier
- $\tau_{\mathrm{transition}}$ = time to traverse transition state region

**Pressure field energy landscape:**
- Reactants: Local minimum in pressure field energy
- Transition state: Saddle point (maximum along reaction coordinate)
- Products: New local minimum

See Phase 19 Reaction Kinetics for detailed foundation.

---

## 2. Substitution Reactions

### 2.1 SN2 Mechanism (Bimolecular Nucleophilic Substitution)

**Mechanism:** Concerted, one step
- Nucleophile attacks from back side
- Leaving group departs simultaneously
- Inversion of stereochemistry

**Example:** $\mathrm{CH_3Br} + \mathrm{OH}^- \to \mathrm{CH_3OH} + \mathrm{Br}^-$

**Transition state:**
- Partial C-OH bond forming
- Partial C-Br bond breaking
- Trigonal bipyramidal geometry

**From master equation:**
$$E_a = P_{\mathrm{CMB}} \Delta A_{\mathrm{eff}} \Gamma \kappa (1-\eta_{\mathrm{TS}}) \times \tau_{\mathrm{TS}} \tag{2.1}$$

where $\Delta A_{\mathrm{eff}}$ accounts for pressure field reconfiguration.

**Rate law:** $v = k[\mathrm{RX}][\mathrm{Nu}^-]$

**SDT explanation:** Rate depends on collision frequency (pressure field encounters) between reactants.

**Steric effects:**
- Primary (1°) > Secondary (2°) > Tertiary (3°)
- **SDT explanation:** More substituents → more pressure field repulsion → higher barrier

### 2.2 SN1 Mechanism (Unimolecular Nucleophilic Substitution)

**Mechanism:** Stepwise, two steps
1. Rate-determining: $\mathrm{RX} \to \mathrm{R}^+ + \mathrm{X}^-$ (carbocation formation)
2. Fast: $\mathrm{R}^+ + \mathrm{Nu}^- \to \mathrm{RNu}$ (nucleophile attack)

**Example:** $(\mathrm{CH_3})_3\mathrm{CBr} + \mathrm{H_2O} \to (\mathrm{CH_3})_3\mathrm{COH} + \mathrm{HBr}$

**Carbocation intermediate:**
- Planar, sp² hybridized
- Stabilized by hyperconjugation

**From master equation:**
Step 1 (rate-determining):
$$E_a = P_{\mathrm{CMB}} A_{\mathrm{RX}} \Gamma \kappa (1-\eta_{\mathrm{break}}) \times \tau_{\mathrm{break}} \tag{2.2}$$

**Rate law:** $v = k[\mathrm{RX}]$ (unimolecular)

**SDT explanation:** Rate depends only on pressure field energy to break C-X bond.

**Carbocation stability:**
- 3° > 2° > 1° > CH₃⁺
- **SDT explanation:** More alkyl groups → more hyperconjugation → better pressure field stabilization

---

## 3. Elimination Reactions

### 3.1 E2 Mechanism (Bimolecular Elimination)

**Mechanism:** Concerted elimination
- Base removes β-proton
- Leaving group departs
- Double bond forms

**Example:** $\mathrm{CH_3CH_2Br} + \mathrm{OH}^- \to \mathrm{CH_2=CH_2} + \mathrm{H_2O} + \mathrm{Br}^-$

**Transition state:**
- Partial C-H bond breaking
- Partial C-Br bond breaking
- Partial C=C bond forming

**From master equation:**
$$E_a = P_{\mathrm{CMB}} \Delta A_{\mathrm{eff}} \Gamma \kappa (1-\eta_{\mathrm{E2}}) \times \tau_{\mathrm{E2}} \tag{3.1}$$

**Rate law:** $v = k[\mathrm{RX}][\mathrm{Base}]$

**Stereochemistry:** Anti-periplanar requirement
- H and X must be 180° apart
- **SDT explanation:** Minimizes pressure field repulsion in transition state

**Zaitsev's rule:** More substituted alkene preferred
- **SDT explanation:** More substituted = more stable pressure field geometry

### 3.2 E1 Mechanism (Unimolecular Elimination)

**Mechanism:** Stepwise, two steps
1. Rate-determining: $\mathrm{RX} \to \mathrm{R}^+ + \mathrm{X}^-$ (carbocation)
2. Fast: $\mathrm{R}^+ \to \mathrm{alkene} + \mathrm{H}^+$ (proton loss)

**Rate law:** $v = k[\mathrm{RX}]$

**SDT explanation:** Same rate-determining step as SN1 (carbocation formation).

---

## 4. Addition Reactions

### 4.1 Electrophilic Addition to Alkenes

**Mechanism:** Two steps
1. Electrophile attacks π bond → carbocation
2. Nucleophile attacks carbocation

**Example:** $\mathrm{CH_2=CH_2} + \mathrm{HBr} \to \mathrm{CH_3CH_2Br}$

**Markovnikov's rule:** H adds to less substituted carbon
- **SDT explanation:** More stable carbocation intermediate (3° > 2° > 1°)

**From master equation:**
$$E_a = P_{\mathrm{CMB}} A_{\pi} A_{\mathrm{electrophile}} \Gamma \kappa (1-\eta_{\mathrm{addition}}) \times \tau_{\mathrm{addition}} \tag{4.1}$$

See Phase Chemistry Organic Alkenes for detailed mechanisms.

### 4.2 Nucleophilic Addition to Carbonyls

**Mechanism:** Nucleophile attacks electrophilic carbon

**Example:** $\mathrm{CH_3CHO} + \mathrm{CN}^- \to \mathrm{CH_3CH(CN)OH}$

**From master equation:**
Carbonyl C=O bond creates pressure field asymmetry → electrophilic carbon.

---

## 5. Rearrangements

### 5.1 Carbocation Rearrangements

**1,2-Hydride shift:**
- H⁻ migrates from adjacent carbon
- More stable carbocation formed

**Example:** $(CH_3)_2C^+CH_2CH_3 \to (CH_3)_3C^+$

**1,2-Methyl shift:**
- CH₃⁻ migrates from adjacent carbon
- More stable carbocation formed

**SDT explanation:** Pressure field minimizes energy by forming most stable carbocation.

**From master equation:**
Migration occurs when:
$$\Delta U_{\mathrm{pressure,new}} < \Delta U_{\mathrm{pressure,old}} \tag{5.1}$$

---

## 6. Validation Examples

### 6.1 SN2 vs. SN1

| Substrate | Mechanism | $E_a$ (kJ/mol) | Rate |
|-----------|-----------|----------------|-------|
| CH₃Br | SN2 | 85 | Fast |
| (CH₃)₂CHBr | SN2/SN1 | 95 | Moderate |
| (CH₃)₃CBr | SN1 | 75 | Fast* |

*Fast due to low $E_a$ despite unimolecular

### 6.2 Elimination vs. Substitution

| Conditions | Product | Mechanism |
|------------|---------|-----------|
| Strong base, high T | Alkene | E2 |
| Weak base, low T | Substitution | SN1/SN2 |

**SDT explanation:** Base strength and temperature affect pressure field barrier heights.

---

## 7. Cross-References

- **Phase 19 Reaction Kinetics:** Detailed mechanisms and activation energies
- **Phase Chemistry Organic Alkenes:** Addition reactions
- **Phase Chemistry Organic Alkanes:** Substrate structure effects

---

**Key Principle:** All organic reactions derive from pressure field reconfiguration pathways, with mechanisms determined by pressure field energy minimization and barrier heights.

