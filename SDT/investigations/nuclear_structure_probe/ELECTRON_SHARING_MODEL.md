# Electron-Sharing Model for Nuclear Structure

**Status:** Specification  
**Version:** 1.0  
**Related:** 6π Trefoil Interleaved Nuclear Structure; D-01 (Deuteron); Alpha binding

---

## 1. Overview

Within the SDT framework, nuclei are built from **6π trefoil** nucleons (protons and neutrons) whose internal electrons mediate binding between adjacent protons. The neutron is a composite **n = p⁺ + e⁻_internal**; its nestled electron is available for **shared mediation** with neighboring protons. This document formalizes the electron-sharing rules and their geometric implications for deuteron, alpha, and heavier nuclei.

---

## 2. Deuteron: p–p–e Geometry

### 2.1 Structure

A deuteron is **two protons sharing one internal electron**. The neutron contributes its internal electron, which sits in the gap between both protons and mediates the bond.

- **Notation:** p–p–e (proton–proton–electron)
- **Electron locus:** Gap center; D − d_p ≈ 0.26 fm (proton diameter d_p ≈ 1.68 fm, separation D ≈ 1.94 fm)
- **Chirality:** L–R or R–L for the p–n pair

### 2.2 Binding Energy

**Formula:**
```
E_bind ≈ 3 k_e e² / D
```

- **D:** Deuteron separation ≈ 1.94 fm (1.942 fm in SDT core axioms)
- **k_e:** Coulomb constant
- **Measured:** 2.224 MeV  
- **SDT derivation:** Binding from the shared-electron pressure well; equilibrium between inter-proton repulsion and the binding force from the shared electron.

### 2.3 Physical Mechanism

The two protons would normally repel. The shared electron vortex creates a **localized low-pressure zone** between them. Stability arises from equilibrium between:

1. Inter-proton Coulomb repulsion
2. Binding force from the shared-electron pressure well

The internal electron "circles" between its host proton (inside the neutron) and the deuteron’s proton, acting as glue.

---

## 3. Alpha: Four-Way Electron Sharing

### 3.1 Structure

The alpha particle (⁴He) is **two deuterons that mesh**, not merely stick. Their internal electron vortices **synchronize**.

- **Nucleons:** 2 protons + 2 neutrons (each neutron = p + e_internal)
- **Internal electrons:** 2 (one per neutron)
- **Sharing:** Both electrons weave between **all four protons** → four-way sharing

### 3.2 Geometry

- **Arrangement:** Tetrahedral L–R–L–R chirality
- **Spine:** Two neutrons form a central stabilizing spine
- **Lock:** Two protons lock onto this spine in a perfect tetrahedral geometry

### 3.3 Binding

- **E_bind ≈ 28.3 MeV** (alpha particle)
- **Mechanism:** Four-way internal electron sharing creates a "super-stabilized" knot. The two internal electrons have four protons to weave between, producing maximal geometric closure.

---

## 4. T-Units and D-Units

### 4.1 T-Units (Trefoil Units)

- **Composition:** 1 proton + 2 neutrons → p + 2n
- **Internal electrons:** 1 per T-unit (from the two neutrons; one neutron contributes its electron for inter-unit mediation)
- **Role:** Bridge between alpha clusters; contribute to binding via shared-electron pressure wells

### 4.2 D-Units (Deuteron Units)

- **Composition:** 1 proton + 1 neutron → p + n
- **Internal electrons:** 1 shared between the two protons (standard deuteron)
- **Role:** Pair contribution; no extra electron beyond the deuteron bond

### 4.3 General Rule

- **Each T-unit:** Contributes 1 internal electron for mediation
- **Each D-unit:** Contributes a p–n pair; the neutron’s electron mediates between the two protons of that deuteron
- **Binding:** Arises from shared-electron mediation + occlusion

---

## 5. Binding Contribution from Shared-Electron Pressure Wells

The shared electron creates a **pressure well** in the spation medium:

- **Depth:** Proportional to 1/D (separation)
- **Extent:** Localized to the gap between protons
- **Compounding:** In multi-proton systems, effective occlusion grows nonlinearly with depth/packing (from SDT core axioms)

The binding energy is the energy required to overcome this shared-electron bond and separate the proton vortices.

---

## 6. Cross-References

| System        | Formula / Observation                          | Source                          |
|---------------|--------------------------------------------------|---------------------------------|
| Deuteron      | E_bind ≈ 3 k_e e²/D; D ≈ 1.94 fm; gap ≈ 0.26 fm | SDT_CORE_AXIOMS §2.2; D-01      |
| Neutron       | n = p⁺ + e⁻_internal; r_node ≈ 0.25 fm            | SDT_CORE_AXIOMS §2.1            |
| Alpha         | 2e⁻ shared among 4p; tetrahedral                | 002_Helium; atomica_sentis      |
| Interleaving  | Deuterons mesh; vortices synchronize            | 6PI_TREFOIL_INTERLEAVED_SPEC    |

---

## 7. Open Questions

1. **Quantification:** The plan notes that deuteron "actual binding stronger due to electron sharing mechanism" — mechanism not yet fully quantified beyond E_bind ≈ 3 k_e e²/D.
2. **Electron dynamics:** Treat electrons as static mediation points or add orbital/phase (e.g. 6π phase lock)?
3. **T-unit electron allocation:** Precise assignment of which neutron’s electron mediates in multi-T alpha clusters.

---

*(End of ELECTRON_SHARING_MODEL.md)*
