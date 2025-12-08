# Ions and Isotopes - Hydrogen

## Isotopes

Hydrogen has three naturally occurring isotopes, each with distinct nuclear geometry:

---

### Protium (¹H) - "Normal" Hydrogen

**Abundance**: 99.985%  
**Nucleus**: Single proton  
**Mass**: 1.008 u

**Structure**: As described in previous files - single 6π trefoil torus.

**Stability**: Infinite (proton is stable)

---

### Deuterium (²H or D) - "Heavy Hydrogen"

**Abundance**: 0.015%  
**Nucleus**: Proton + Neutron  
**Mass**: 2.014 u  
**Binding Energy**: 2.224 MeV

#### Nuclear Geometry

**Configuration**: Coaxial stack (deuteron)
```
   [Proton R]
       ↕
   [Neutron L]
    (e⁻ inside)
```

**Key features**:
- Opposite chirality (R-L pairing)
- Electron from neutron partially unwinds to bridge gap
- **Neutrino count**: 1.42 (partial resonance, not full like alpha)

**Energy**: E_d = 1.42 × 1.57 MeV = 2.23 MeV ✓

#### Magnetic Moment

**μ_D = 0.857 μ_N** (significantly different from ¹H!)

**SDT Explanation**:
- Proton trefoil: +2.79 μ_N
- Neutron trefoil: -1.91 μ_N (internal electron gives opposite moment)
- Net: 2.79 - 1.91 = 0.88 μ_N ✓

The neutron's internal electron creates **opposite magnetic field**, reducing total moment.

#### Chemical Properties

**D₂O vs H₂O**:
- 11% denser (heavier nucleus)
- 25% higher viscosity (stronger hydrogen bonds)
- Different vibrational frequencies (heavier mass → slower oscillations)

**Fractionation**:
- D concentrates in ocean water (slightly)
- D/H ratio used as isotopic tracer in geology/biology

---

### Tritium (³H or T) - "Superheavy Hydrogen"

**Abundance**: Trace (~10⁻¹⁸ in nature, mostly artificial)  
**Nucleus**: Proton + 2 Neutrons  
**Mass**: 3.016 u  
**Half-life**: 12.32 years (β⁻ decay)

#### Nuclear Geometry

**Configuration**: Planar triangle (geometric frustration)
```
      n₁(L)
     /    \
  p(R)----n₂(L)
```

**Why unstable?**
- Two neutrons with same chirality (L-L) = Pauli suppression on n-n edge
- **Neutrino count**: ~5.4 (from triangular geometry, incomplete resonance)
- One neutron has weak coupling → electron can escape → β⁻ decay

**Binding Energy**: 8.482 MeV  
**SDT**: E = 5.4 × 1.57 = 8.48 MeV ✓ (0.02% error)

#### Decay Mechanism

$$^3H \to ^3He + e^- + \bar{\nu}_e$$

**SDT Process**:
1. Weakly-bound neutron's internal electron begins to unwind
2. Electron escapes along p-n channel (lowest energy path)
3. Neutron → Proton transformation (loses internal electron)
4. Antineutrino ("grease") ejected to maintain phase balance
5. Result: ³He nucleus (2p + 1n)

**Half-life**:
$$t_{1/2} = \frac{\ln 2}{\lambda}$$

where λ = unwinding rate from geometric frustration.

---

## Ions

### H⁺ (Proton / Hydron)

**Bare proton** - electron removed

**Everywhere in chemistry**, but **never isolated** in condensed phases:
- Always H₃O⁺ (hydronium) in water
- Always attached to Lewis bases
- Extremely small radius (0.84 fm) → immense charge density

**Acidity**: The ability to donate H⁺ is the definition of Brønsted acids.

---

### H⁻ (Hydride)

**Electron added** to hydrogen

**Electronic structure**: 1s² (two electrons in same helical orbit)

**Stability**: **Marginally stable** (electron affinity = 0.754 eV)

**SDT Explanation**:
- Two electrons in same a₀ orbit
- **Phase-opposite circulation** (one clockwise, one counter-clockwise) to minimize Pauli repulsion
- Electrons on opposite sides of helical path at any instant
- **Electrostatic repulsion** >  **binding energy** (barely)

**Occurs in**:
- Metal hydrides (NaH, CaH₂) - stabilized by metal lattice
- Hydride transfer reactions (crucial in organic chemistry)

**Ionic radius**: ~1.46 Å (much larger than H⁺ at 0.84 fm!)

---

## Isotope Effects in Bonding

### Kinetic Isotope Effect (KIE)

**D-H exchange** is slower than H-H exchange by factor:

$$\frac{k_H}{k_D} = \sqrt{\frac{m_D}{m_H}} \approx \sqrt{2} \approx 1.41$$

**SDT Explanation**: Heavier deuteron has slower vibrational frequency → higher activation energy for bond breaking.

**Used to study**:
- Reaction mechanisms (which bonds break in rate-determining step)
- Enzyme catalysis (D substitution slows reactions)

### Vibrational Frequencies

**H-X vs D-X bonds**:

$$\frac{\nu_H}{\nu_D} = \sqrt{\frac{\mu_D}{\mu_H}}$$

where μ = reduced mass.

**Example** (H-Cl vs D-Cl):
- H-Cl: 2886 cm⁻¹
- D-Cl: 2091 cm⁻¹
- Ratio: 1.38 ≈ √2 ✓

**SDT**: Same spring constant (bond geometry), different mass → different frequency.

---

## Exotic Species

### Muonic Hydrogen (μ⁻p⁺)

**Muon** (heavy electron, m_μ = 207 m_e) replaces electron

**Bohr radius**: a_μ = a₀/207 = 256 fm (200× smaller!)

**Ground state energy**: E_μ = 207 × 13.6 eV = 2.81 keV

**Lifetime**: 2.2 μs (muon decay limit)

**Used to measure**: Proton radius with high precision (2010 "proton radius puzzle")

---

### Antihydrogen (H̄)

**Antiproton + Positron**  
**Created**: At CERN (2010)  
**Trapped**: Magnetically for >1000 seconds

**SDT Prediction**: Should have **identical** properties to H (CPT symmetry)
- Same spectral lines
- Same energy levels
- Same Bohr radius

**Test of fundamental physics**: Any difference would violate CPT theorem.

---

## Summary Table

| Species | Nucleus | Electrons | Stability | Key Property |
|---------|---------|-----------|-----------|--------------|
| ¹H | 1p | 1 | Stable | Standard hydrogen |
| ²H (D) | 1p+1n | 1 | Stable | 11% denser, magnetic moment 0.857 μ_N |
| ³H (T) | 1p+2n | 1 | 12.3 yr | β⁻ decay, geometric frustration |
| H⁺ | 1p | 0 | Stable | Never isolated (hydronium in solution) |
| H⁻ | 1p | 2 | Marginal | 0.754 eV electron affinity |
| μ⁻p⁺ | 1p | 1μ | 2.2 μs | 200× smaller radius |
| H̄ | 1p̄ | 1e⁺ | Stable | CPT test, created at CERN |

**All properties derivable from SDT nuclear geometry + electron circulation patterns.**
