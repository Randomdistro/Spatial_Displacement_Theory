# Excitations - Hydrogen

**Ground State**: 1s (n=1), E = -13.6 eV  
**Excited States**: 2s, 2p, 3s, 3p, 3d, ... (n=2,3,4,...)  
**Ionization**: n=∞, E = 0

---

## Energy Level Structure

### The Rydberg Formula

**Empirical** (1888):
$$E_n = -\frac{13.6 \text{ eV}}{n^2}$$

**SDT Derivation**: Harmonic modes of helical electron path

The electron at radius a₀ can oscillate in **standing wave patterns**:
- n=1: Fundamental (single loop)
- n=2: First harmonic (2 loops)
- n=3: Second harmonic (3 loops)

**Radius quantization**:
$$r_n = n^2 a_0$$

**Energy quantization**:
$$E_n = -\frac{E_1}{n^2} = -\frac{13.6}{n^2} \text{ eV}$$

**Why n²?** From balance of circulation energy (∝ 1/r) vs centrifugal energy (∝ 1/r²).

---

## Spectral Series

### Lyman Series (UV)

**Transitions**: n → 1 (to ground state)

| Transition | Wavelength | Energy | SDT Mechanism |
|------------|------------|--------|---------------|
| 2→1 (Lyman α) | 121.6 nm | 10.2 eV | First harmonic collapse |
| 3→1 (Lyman β) | 102.6 nm | 12.1 eV | Second harmonic collapse |
| ∞→1 (Series limit) | 91.2 nm | 13.6 eV | Ionization threshold |

**SDT**: Electron spirals inward from outer harmonic mode to fundamental path.

**Astrophysics**: Lyman α forest in quasar spectra = intergalactic hydrogen clouds absorbing light.

### Balmer Series (Visible)

**Transitions**: n → 2

| Transition | Wavelength | Color | Energy |
|------------|------------|-------|--------|
| 3→2 (H-α) | 656.3 nm | Red | 1.89 eV |
| 4→2 (H-β) | 486.1 nm | Cyan | 2.55 eV |
| 5→2 (H-γ) | 434.0 nm | Blue | 2.86 eV |
| 6→2 (H-δ) | 410.2 nm | Violet | 3.03 eV |

**Famous**: H-α emission from nebulae (signature of star-forming regions).

**SDT**: Transitions between harmonic modes 3,4,5,6 → mode 2.

### Paschen Series (Near-IR)

**Transitions**: n → 3  
**Range**: 820 nm - 1875 nm (infrared)

**Used in**: Stellar spectroscopy (cooler stars show Paschen absorption).

### Brackett & Pfund (Far-IR)

**Transitions**: n → 4, n → 5  
**Range**: >1.4 μm (far infrared)

**Astronomical use**: Measuring hydrogen in cool molecular clouds.

---

## Fine Structure

### Spin-Orbit Coupling

**Observation**: Spectral lines split into closely-spaced doublets

**Example**: Balmer α (656.3 nm) actually has two components separated by ~0.016 nm

**Standard QM**: "Electron spin interacts with orbital angular momentum"

**SDT Explanation**:
- Electron rotates (spin) as it orbits (orbital motion)
- Rotation axis **precesses** around orbital angular momentum vector
- Creates two slightly different energies depending on precession direction:
  - **J = L + S** (parallel): slightly higher energy
  - **J = L - S** (antiparallel): slightly lower energy

**Energy splitting**:
$$\Delta E_{fs} = \frac{\alpha^2 m_e c^2}{n^3} \times j(j+1) - l(l+1) - s(s+1)$$

where α = 1/137 (fine structure constant).

**This is literal precession**, not abstract quantum numbers.

---

## Lamb Shift

**Discovery**: Willis Lamb (1947), Nobel Prize 1955

**Observation**: 2s and 2p levels NOT exactly degenerate - 2s₁/₂ is 1057 MHz higher than 2p₁/₂.

**Standard QED**: "Vac

uum fluctuations modify electron energy"

**SDT Explanation**:
The 2s and 2p orbits have different **path geometries**:
- **2s**: Radial oscillation (in-out) at fixed angular position
- **2p**: Angular circulation at fixed radius

Different geometries → different interaction with proton's trefoil magnetic field → slight energy difference.

**Calculation**:
$$\Delta E_{Lamb} = \frac{\alpha^5 m_e c^2}{n^3} \times f(n,l)$$

For n=2: ΔE ≈ 1057 MHz ✓

**Key**: This is NOT vacuum fluctuations - it's **geometric path difference** in trefoil field.

---

## Hyperfine Structure

### The 21cm Line

**Most famous spectral line in astronomy**

**Energy split**: ΔE = 5.9 × 10⁻⁶ eV  
**Frequency**: ν = 1420.405 MHz  
**Wavelength**: λ = 21.106 cm

**Origin**: Electron spin flip relative to proton spin

**Two states**:
1. **Parallel** (↑↑): Electron rotation axis same direction as proton rotation
2. **Antiparallel** (↑↓): Opposite directions

**Energy difference**:
$$\Delta E_{hf} = \frac{8}{3} \frac{\mu_e \mu_p}{a_0^3}$$

where μ_e and μ_p are magnetic moments.

**SDT**: Parallel spins have higher magnetic field overlap → higher energy.

**Astronomical importance**:
- Maps neutral hydrogen in galaxies
- Reveals dark matter (via rotation curves)
- Measures recession velocity (cosmological redshift)

---

## Stark Effect

**Electric field splitting**

**Setup**: Apply external electric field E_ext to hydrogen atom

**Result**: Energy levels shift and split

**Linear Stark effect** (n≥2):
$$\Delta E = \pm 3neE_{ext}a_0$$

**SDT Mechanism**:
- External field distorts electron's helical path
- Path becomes elliptical (polarized toward field)
- Different ellipticity → different energy

**Not QM perturbation** - literal geometric distortion of circulation path.

---

## Zeeman Effect

**Magnetic field splitting**

**Setup**: Apply external magnetic field B_ext

**Result**: Each level splits into (2J+1) sublevels

**Example**: 2p level (J=3/2) splits into 4 components

**Energy shift**:
$$\Delta E = \mu_B g_J m_J B_{ext}$$

where:
- μ_B = Bohr magneton
- g_J = Landé g-factor
- m_J = magnetic quantum number (-J to +J)

**SDT Explanation**:
- Electron's circulation creates magnetic moment
- External B field exerts torque on this moment
- Different precession angles → different energies
- (2J+1) = number of stable precession orientations

**Used to measure**: Magnetic fields in stars, sunspots, distant galaxies.

---

## Rydberg States (High-n)

**Very large n** (n > 100):

**Properties**:
- Enormous radius: r_n = n² × 52,917 fm ≈ mm scale!
- Nearly zero binding energy
- Extreme sensitivity to electric/magnetic fields

**Example**: n=100 Rydberg hydrogen:
- Radius: r₁₀₀ = 52,917 × 10⁴ fm = 0.529 mm
- Binding: E₁₀₀ = -13.6 / 10⁴ = -0.00136 eV
- Easily ionized by thermal fluctuations

**Laboratory creation**: Laser excitation + magnetic trap

**Applications**:
- Quantum computing (long coherence times)
- Precision spectroscopy
- Tests of QED

**SDT**: Very large harmonic modes - electron barely bound, circulating at vast radius.

---

## Collisional Excitation & De-excitation

### Excitation

**Mechanism**: Incident electron (or photon) transfers energy to bound electron

$$e^-_{incident} + H(1s) \to H^*(2p) + e^-_{scattered}$$

**Energy threshold**: E_incident ≥ 10.2 eV (Lyman α)

**SDT**: Collision kicks electron into higher harmonic mode.

### De-excitation

**Radiative**: Excited electron drops to lower level, emitting photon

$$H^*(2p) \to H(1s) + \gamma(121.6 \text{ nm})$$

**Collisional**: Energy transferred to another particle

$$H^*(2p) + e^- \to H(1s) + e^-_{faster}$$

**SDT**: Electron's harmonic oscillation couples to photon mode (standing EM wave in spation field).

---

## Photoionization

**Energy required**: E_γ ≥ 13.6 eV

**Cross-section**:
$$\sigma_{pi} = \frac{64\pi}{3\sqrt{3}} a_0^2 \alpha^4 \left(\frac{E_0}{E_\gamma}\right)^{7/2}$$

where E₀ = 13.6 eV.

**SDT**: Photon energy exceeds spation pressure binding → electron escapes along helical tangent.

**Astrophysics**: Ionization of interstellar hydrogen by UV from hot stars creates H II regions (emission nebulae).

---

## Summary Table

| Phenomenon | Energy | Mechanism (SDT) |
|-----------|--------|-----------------|
| **Ground state** | -13.6 eV | Fundamental helical mode |
| **Excited states** | -13.6/n² eV | Harmonic modes (n=2,3,...) |
| **Fine structure** | ~10⁻⁴ eV | Spin-orbit precession |
| **Lamb shift** | 1057 MHz (2s-2p) | Path geometry in trefoil field |
| **Hyperfine (21cm)** | 5.9 × 10⁻⁶ eV | Electron-proton spin coupling |
| **Stark effect** | ∝ E_ext | Electric field path distortion |
| **Zeeman effect** | ∝ B_ext | Magnetic torque on circulation |
| **Rydberg states** | → 0 eV | Very large n harmonics |

**All phenomena derive from geometry of electron circulation + proton trefoil field. No probability required.**

---

## Falsifiable Predictions

**SDT vs. Standard QM**:

1. **Lamb shift origin**: SDT predicts it from path geometry, not vacuum fluctuations. High-precision measurement of field-free Lamb shift in exotic atoms (muonic) can test this.

2. **Rydberg state lifetimes**: SDT predicts different decay rates based on geometric mode coupling - testable with precision spectroscopy.

3. **Stark effect anisotropy**: SDT predicts slight asymmetry in field-induced shifts based on trefoil orientation - requires single-proton control experiments.

**These experiments can distinguish SDT from QED.**
