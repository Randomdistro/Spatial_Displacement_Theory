# On the Nature of Atomicus — Rules (v5.0)

*Updated March 2026 — aligned with sdt-engine canonical framework*

## Constitutional Basis

Atomicus operates under the SDT v5.0 framework:

- **9 Axioms** (R1–R5: relay medium, M1–M3: matter as exclusion)
- **17 Theorems** (T1–T17: from shell cancellation to c-boundary)
- **6 Irreducible Operators** (throughput, boundary event, traction, wake, propagation, persistence)

All Atomicus derivations must respect the **Prohibitions**: no quarks, no G or M as fundamental, no dark matter, no fields as ontological primitives.

---

## I. The Nuclear Laws (The Architecture of the Core)

### 1. The Law of the Alpha Brick

The fundamental unit of nuclear construction is the **Alpha Particle** ($^4$He), a perfect tetrahedral assembly of 2 protons and 2 neutrons. Heavy nuclei are built by stacking alpha bricks. (Carbon = 3α, Oxygen = 4α, Iron = 13α+2n+2p).

SDT interpretation: each alpha is a **W=3 trefoil quartet** with 4 nucleons sharing a single toroidal circulation cell. Binding energy = $28.3$ MeV per alpha.

### 2. The D–T Code (No Free Neutrons)

Every stable isotope decomposes exactly into:
- **D pairs**: 1p + 1n (mortar)
- **T triples**: 1p + 2n (wedge)

Rule: $D + T = Z$, $D + 2T = N$. No residual neutrons.

### 3. Stability Limit ($D \geq T$)

For $Z \leq 79$ (Gold): stability requires $D \geq T$. The structural skeleton must bear the volume fillers.

### 4. The Golden Boundary ($Z = 79$)

Gold is the last "solid geometry" nucleus. Beyond Gold, $T > D$ becomes possible → liquid nuclear structure → radioactivity cascade.

### 5. The Neutron Bridge

Alpha bricks repel via Coulomb occlusion pressure at close range. Neutrons act as geometric bridges — mediating the contact between charged bricks.

---

## II. The Electronic Laws

### 6. The Law of Geometric Serenity

Electrons fill **geometric voids**, not abstract energy levels:

| Geometry | Electrons | Serenity |
|----------|-----------|----------|
| Dyad (line) | 2 | 1D stable |
| Triangle (plane) | 3 | 2D stable |
| Tetrahedron (solid) | 4 | 3D stable |
| Cube (perfect) | 8 | Maximum serenity |

Noble gas = maximum geometric serenity. Reactivity = geometric stress from incomplete shell.

### 7. The Kinematic Ratio ($\chi = c/v$)

$$\chi = \frac{c}{v} = \frac{c}{\sqrt{2E_\text{ion}/m_e}}$$

| Element | $\chi$ | Interpretation |
|---------|--------|----------------|
| Ne | 109 | Hard, inert |
| H | 137 | Baseline ($1/\alpha$) |
| K | 243 | Floppy, reactive |

**SDT meaning**: $\chi$ is the k-number for the electron orbit. $z \cdot k^2 = 1$ still holds: $z = v^2/c^2 = 1/\chi^2$, so $z \cdot \chi^2 = 1$ always.

### 8. The $Z^2$ Scaling Law

Any atom stripped to a single electron obeys:

$$E_n = -13.6057 \cdot \frac{Z^2}{n^2} \text{ eV}$$

Same physics, no exceptions. Chemistry = geometric shielding of the core.

### 9. The Stroboscopic Electron

The electron is a **hard point** traversing a Hopf fibration track at pattern speeds. Observation = stroboscopic sampling → apparent standing wave → "orbital cloud" is an artefact.

### 10. The Reciprocal Drive

Nuclear toroidal circulation drives electron motion via wake coupling. The nucleus spins the ℓ=2 wake → wake drags the electron along its track. No gravitational orbit — pure mechanical drive.

---

## III. The Interaction Laws (Chemistry & Magnetism)

### 11. The Geometric Vacuum

Reactivity = geometric stress:
- **F, Cl**: Cube minus one vertex → extreme electron vacuum
- **B**: Trigonal plane wanting tetrahedron → electron sponge
- **Na, K**: One electron past a closed shell → easily shed

### 12. The Magnetic Gear Effect

| Type | Mechanism | Example |
|------|-----------|---------|
| Diamagnetic | Paired counter-rotating vortices cancel | Cu, Bi |
| Paramagnetic | Unpaired vortex creates net wake | Al, O₂ |
| Ferromagnetic | 4 unpaired 3d vortices mesh with neighbours | Fe ($3d^6$) |

### 13. The Geometric Anomaly

Cr ($[Ar]3d^5 4s^1$) and Cu ($[Ar]3d^{10} 4s^1$) sacrifice outer shell stability for inner shell geometric perfection. These are not anomalies — they are **geometric corrections**.

---

## IV. The Fundamental Axiom

### 14. The Proton is the Code

The electron shell geometry is a **holographic projection** of nuclear geometry:
- Triangular nucleus (C) → tetrahedral shell
- Octahedral nucleus (Mg) → octahedral shell
- Chemistry is Nuclear Physics geared down by $\chi = 137$

---

## V. Connection to sdt-engine v5.0

| Atomicus Concept | sdt-engine Component | File |
|-----------------|---------------------|------|
| $R_y$, $a_0$, $\alpha$ | `sdt::laws::measured` | `laws.hpp` |
| Rydberg formula | `sdt::laws::atomic::rydberg_energy_eV()` | `laws.hpp` |
| k-number, $zk^2=1$ | `sdt::laws::bridge` | `laws.hpp` |
| Proton $R_p$ (W+1) | `sdt::laws::winding` | `laws.hpp` |
| Coulomb coupling | `sdt::laws::coulomb_identity` | `laws.hpp` |
| Occlusion function | `State28D::calculate_occlusion()` | `state28d.hpp` |
| Force hierarchy | `State28D::force_ratio_coulomb_to_gravity()` | `state28d.hpp` |
| $P_\text{conv}$, $P_\text{eff}$ | `sdt::laws::law_I`, `sdt::laws::law_III` | `laws.hpp` |

---

## Errata from Previous Versions

| Item | Old Value | Correct Value |
|------|-----------|---------------|
| $P_\text{CMB}$ | $2.036 \times 10^{-2}$ Pa | $1.391 \times 10^{-14}$ Pa |
| Author | J.C. Harvey | James Tyndall |
| Framework version | — | v5.0 (March 2026) |