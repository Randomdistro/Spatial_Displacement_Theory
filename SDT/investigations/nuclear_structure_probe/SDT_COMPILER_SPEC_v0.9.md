# SDT COMPILER SPEC v1.0

**Nuclear packing → occlusion → presence/density → velocity field (no GM; compare-only)**

*One-shot runnable: canonical macro occluder (§2.1.1), canonical \(\mathcal{H}\) (§2.2.1), deterministic \(\mathcal{W}\) (§9.4), \(\mathcal{U} = R_{\mathrm{eff}}/r\). Remaining degrees of freedom bounded (§12).*

---

## 0) Reserved names and symbol hygiene

**Collision removed:** Nuclear binding constant vs orbital velocity parameter must not share the same symbol.

| Meaning | Symbol | Units | Use |
|--------|--------|-------|-----|
| **Nuclear binding proportionality** | \(\kappa_B\) | MeV/sr | \(B = \kappa_B \cdot \Omega_{\mathrm{total}}\) |
| **Orbital / structure velocity** | \(v\) | m/s | Velocity field from binding depth |
| **Dimensionless velocity fraction** | \(\kappa_v \equiv v/c\) | 1 | \(\kappa_v(r) = v(r)/c\) |

**Compiler rule:** Internally the pipeline uses \(\kappa_B\) for binding and \(v\), \(\kappa_v\) for velocities. If SDT prose calls orbital speed “k,” that is **prose only**; the compiler keeps \(\kappa_B\) vs \(v\)/\(\kappa_v\) strictly separate.

---

## 1) Inputs (primitives allowed)

### 1.1 Micro (nuclear) inputs

- \(R_{\mathrm{NUCLEON}}\) (fm)
- Nuclear packing geometry generator \(G_{\mathrm{pack}}(Z,N)\) returning nucleon/alpha centres \(\{\mathbf{p}_i\}\) and bonds \(\{(i,j)\}\)
- Occlusion operators: \(\Omega_{\mathrm{sphere}}(R,d)\), \(\Omega_{\mathrm{total}}(\mathbf{o}, \{\mathbf{p}_i\}, R)\) with overlap correction
- Calibration nucleus: **deuteron only** for \(\kappa_B\)

### 1.2 Meso/macro (structural body) inputs

A body is represented as a **structure state**

\[
S \equiv \bigl( \mathcal{M},\ \mathcal{G},\ \Lambda,\ A_{28} \bigr)
\]

- **\(\mathcal{M}\)**: Material composition **expressed structurally** (distributions of building blocks: alpha/deuteron/T-units, electron dyads, etc.), not “mass”
- **\(\mathcal{G}\)**: Geometry of the body (shape, radius field, anisotropy)
- **\(\Lambda\)**: Wavelength set(s) for the regime (\(\lambda_{\mathrm{H}}\), \(\lambda_{\mathrm{B}}\), \(\lambda_{\mathrm{L}}\), trefoil modes, etc.)
- **\(A_{28}\)**: 28-aspect stack (recursion / multiscale lift of all measures below)

**No \(G\), no \(M\), no \(GM\)** in the SDT forward path.

---

## 2) Core operators

### 2.1 Occlusion operator family

**Point-observer occlusion (existing):**

- Single sphere: \(\Omega(R,d) = 2\pi\bigl(1 - \sqrt{1-(R/d)^2}\bigr)\), \(d \ge R\); edge cases as in spec.
- Multi-sphere overlap-corrected:
\[
\Omega_{\mathrm{corr}}(\mathbf{o}) = \mathrm{clamp}_{[0,4\pi]}\Bigl( \sum_i \Omega_i - \sum_{i<j} \Omega_{ij}^{\mathrm{overlap}} \Bigr)
\]

**Global occlusion functional (macroscopic):**

Pick an external boundary \(\partial\mathcal{B}\) (e.g. spherical far field or CMB proxy). Observers \(\mathbf{o}_m \in \partial\mathcal{B}\). Then

\[
\Sigma_{\mathrm{occ}}(S) \equiv \frac{1}{|\partial\mathcal{B}|} \int_{\partial\mathcal{B}} \Omega_{\mathrm{body}}(\mathbf{o})\, dA
\]

where \(\Omega_{\mathrm{body}}(\mathbf{o})\) is computed by approximating the body as occluding primitives (spheres/patches) from \(\mathcal{M}\), \(\mathcal{G}\). **Result:** scalar occlusion measure for any body without mass.

**Hostile note:** If \(\Sigma_{\mathrm{occ}}\) is not invariant under the 28-aspect lift, the theory is coordinate-dependent; the compiler must enforce invariance or document the choice.

#### 2.1.1 Canonical macro occluder decomposition

\(\Omega_{\mathrm{body}}(\mathbf{o})\) must **not** be left to arbitrary choice of primitives. The following rendering is **required** so that \(\Sigma_{\mathrm{occ}}\) is reproducible.

**Body surface tessellation model**

- Represent the body surface \(\partial S\) (from \(\mathcal{G}\)) as \(N\) surface patches \(P_j\) with area \(a_j\), outward normal \(\hat{n}_j\), and **patch radius** \(R_j\) (equivalent radius: \(R_j = \sqrt{a_j/\pi}\)).
- Treat each patch as an occluding disk approximated by an **equivalent sphere** of radius \(R_j\) at patch centroid \(\mathbf{p}_j\).

Then for observer \(\mathbf{o}\):

\[
\Omega_{\mathrm{body}}(\mathbf{o}) \equiv \Omega_{\mathrm{corr}}\bigl( \mathbf{o},\, \{\mathbf{p}_j\},\, \{R_j\} \bigr)
\]

using the existing overlap-corrected multi-sphere routine, with **per-patch radii** \(\{R_j\}\) (not a single shared \(R\)).

**Implementation:** The compiler may support either (i) constant \(R_j = R\) for all patches, or (ii) per-patch \(R_j = \sqrt{a_j/\pi}\). **One must be declared**; no ad hoc mix. This closes the “free choice of primitives” loophole and makes \(\Sigma_{\mathrm{occ}}\) reproducible.

### 2.2 Presence/density operator

“Presence” = compression / volumetric exposure from occlusion networks. “Bonding reduces volumetrics” → effective exposed volume shrinks.

- \(V_{\mathrm{geom}}(S)\): geometric volume from \(\mathcal{G}\)
- \(V_{\mathrm{eff}}(S)\): effective exposed volume after bonding/occlusion collapse

**Presence density (dimensionless):**

\[
\rho_{\mathrm{pres}}(S) \equiv \frac{V_{\mathrm{geom}}(S)}{V_{\mathrm{eff}}(S)}
\]

Larger occlusion ⇒ smaller effective volume ⇒ higher \(\rho_{\mathrm{pres}}\). Practical form:

\[
V_{\mathrm{eff}}(S) = V_{\mathrm{geom}}(S) \cdot \mathcal{H}\bigl( \Sigma_{\mathrm{occ}}(S),\ A_{28} \bigr), \qquad \mathcal{H} \in (0,1].
\]

For nuclear clusters: use overlap-corrected occlusion to estimate exposed surface fraction, then map to volume via an aspect-specific operator in \(A_{28}\). For atomic/solid: ATOMICUS serenity closures as boundary conditions that reduce exposed patches.

#### 2.2.1 Canonical presence mapping \(\mathcal{H}\)

\(\mathcal{H}\) must be a **single** monotone map, not a black box. Otherwise it is a second fitting channel.

**Lock-in:** Choose one monotone map that is bounded in \((0,1]\), decreases with \(\Sigma_{\mathrm{occ}}\), and is modulated by Level 5–7 aspects in \(A_{28}\):

\[
\mathcal{H}(\Sigma_{\mathrm{occ}}, A_{28}) = \exp\Bigl( -\eta\, \Sigma_{\mathrm{occ}} \cdot \Xi(A_{28}) \Bigr)
\]

where

\[
\Xi(A_{28}) = \frac{1}{3}\Bigl( \overline{A}^{(5)} + \overline{A}^{(6)} + \overline{A}^{(7)} \Bigr)
\]

is the mean of the Level 5 (torus), Level 6 (dynamism), and Level 7 (energy) aspect means. **\(\eta\)** is a **single** global constant (dimensionless), fixed once—e.g. from hydrogen or one celestial calibration body. No per-body \(\eta\).

Then

\[
\rho_{\mathrm{pres}}(S) = \frac{1}{\mathcal{H}} = \exp\Bigl( \eta\, \Sigma_{\mathrm{occ}}(S) \cdot \Xi(A_{28}) \Bigr).
\]

**Hostile note:** One constant \(\eta\) is acceptable. A per-body \(\eta\) is a hidden fit.

---

## 3) Binding (micro) — unchanged

### 3.1 Calibration

\[
\kappa_B = \frac{B_{\exp}(^2\mathrm{H})}{\Omega(^2\mathrm{H})}
\]

Alpha internal bond length \(d_\alpha\) is chosen to satisfy deuteron–alpha parity under \(\kappa_B\) (second anchor).

### 3.2 Prediction

\[
B_{\mathrm{pred}}(X) = \kappa_B \cdot \Omega_{\mathrm{total}}(X)
\]

Validation pipeline as-is. **Symbol:** \(\kappa_B\) only for this; no “k” for velocity here.

---

## 4) Bridge: occlusion/presence → velocity field (macro)

**Binding depth** \(D(r)\) (dimensionless): increases with occlusion and presence; decreases with \(r\) (geometric dilution); is the **only** input to \(v(r)\).

### 4.1 Binding depth functional

\[
D(r; S) \equiv \underbrace{\Sigma_{\mathrm{occ}}(S) \cdot \rho_{\mathrm{pres}}(S)}_{\text{structure strength}} \cdot \underbrace{\mathcal{U}\!\left( \frac{R_{\mathrm{eff}}}{r} \right)}_{\text{geometric dilution}} \cdot \underbrace{\mathcal{W}(\Lambda, A_{28})}_{\text{wavelength/aspect modulation}}
\]

- \(\mathcal{U}(x)\): **Lock-in** (classic SDT field \(v^2 \propto 1/r\)): \(\mathcal{U}(R_{\mathrm{eff}}/r) = R_{\mathrm{eff}}/r\). \(R_{\mathrm{eff}}\) is defined from geometry alone: e.g. mean radius of \(\mathcal{G}\), or Level 5 torus radius from \(A_{28}\) (e.g. \(\sqrt{T_3/(4\pi)}\) in state_28d). No free choice of \(\mathcal{U}\) for this regime.
- \(\mathcal{W}(\Lambda, A_{28})\): deterministic operator (§9.4); no arbitrary weight vectors.

### 4.2 Velocity law

\[
\kappa_v(r) \equiv \frac{v(r)}{c} = \sqrt{D(r; S)} \quad \Rightarrow \quad v(r) = c\sqrt{D(r; S)}
\]

No GM. **Hostile note:** If \(D\) cannot be written explicitly from \((\Sigma_{\mathrm{occ}}, \rho_{\mathrm{pres}}, \Lambda, A_{28})\), the model is descriptive, not predictive.

---

## 5) Hydrogen inside the same pipeline

- \(S_{\mathrm{H}}\): nuclear packing = single proton; ATOMICUS electron dyad state; \(\Lambda_{\mathrm{H}}\) = spectral wavelengths
- Compute \(\Sigma_{\mathrm{occ}}(S_{\mathrm{H}})\) at the electron’s locus (micro boundary)
- Compute \(\rho_{\mathrm{pres}}(S_{\mathrm{H}})\) from dyad serenity closure
- Compute \(D(r)\) at the allowed orbital locus
- Output: \(\kappa_v = \alpha \Rightarrow v = \alpha c\)

So \(\alpha\) is hydrogen’s structure velocity fraction from the same compiler. No GR language.

---

## 6) Rotation and luminosity (SDT-only)

### 6.1 Rotation

\[
v_{\mathrm{rot}} = c \cdot \mathcal{R}_{\mathrm{mode}}(\Sigma_{\mathrm{occ}}, \rho_{\mathrm{pres}}, \Lambda, A_{28})
\]

\(\mathcal{R}_{\mathrm{mode}}\): selects stable mode-locking frequencies from \(\Lambda\) under the 28-aspect recursion.

### 6.2 Luminosity

\[
L \propto \int_{\partial S} \mathcal{E}(\nabla D, \Lambda, A_{28})\, dA
\]

Emission rate from gradient relaxation. Can stay dimensionless (“luminosity index”) and map to watts only for comparison.

---

## 7) Compare-only outputs (quarantined)

After SDT outputs \(v(r)\):

\[
GM_{\mathrm{eq}}(r) \equiv v(r)^2\, r; \qquad z_{\mathrm{eq}}(r) \equiv \frac{v(r)^2}{c^2}
\]

Printed in a comparison appendix only; never feed back into SDT.

---

## 8) Hostile checks (nuclear spec)

1. **Overlap correction** is heuristic (pairwise only; triple overlaps ignored). Flag as: approximation class, controllable error term, sensitivity knob in the validator.
2. **Two calibrated anchors:** ²H fixes \(\kappa_B\); ⁴He fixes \(d_\alpha\). Do not claim “one calibration.”
3. **\(R(n_{\mathrm{bonds}})\)** (unified inter-alpha radius) is a fitted structure function. Acceptable, but document as an implicit calibration family unless \(\beta\) is derived from packing/serenity rules.

None of these kill the model; they must be explicit so the compiler stays honest.

---

## 9) Explicit form of \(\mathcal{W}(\Lambda, A_{28})\)

**Role:** Wavelength sets and the 28-aspect recursion modulate binding depth into the velocity field across scales. \(\mathcal{W}\) must be written so that \(D(r; S)\) is computable from structure alone.

### 9.1 28-aspect stack (from state_28d)

The 28 components are grouped into **levels** (1+2+3+4+5+6+7 = 28):

| Level | Count | Content (summary) |
|-------|--------|-------------------|
| 1 | 1 | Zero-point (existence) |
| 2 | 2 | Line: position, velocity |
| 3 | 3 | Plane: boundaries, rotation |
| 4 | 4 | Sphere: volume, orientation |
| 5 | 5 | Torus: matter structure (topology); T₃ → effective surface for occlusion |
| 6 | 6 | Dynamism: Φ₀ (solid angle), translocation, oscillation, chirality, variance, phase potential |
| 7 | 7 | Energy: potential, kinetic, rotational, **field (pressure-occlusion)**, binding, flux, transmission |

So \(A_{28} = (A_1, \ldots, A_{28})\) with level-wise interpretation. Level 5 contains toroidal/structure radii; Level 7 contains \(\epsilon_3\) (field/pressure-occlusion) and \(\epsilon_{\mathrm{b}}\) (binding).

### 9.2 Wavelength set \(\Lambda\)

Regime-specific: \(\lambda_{\mathrm{H}}\) (hydrogen spectral), \(\lambda_{\mathrm{B}}\) (body structural), \(\lambda_{\mathrm{L}}\) (lattice), trefoil/compton scales. Same symbol \(\lambda\), subscripted; no ambiguity.

### 9.3 Level 7 index map (state_28d → \(A_{28}\))

For deterministic \(\mathcal{W}\) and \(\mathcal{H}\), Level 7 must be unambiguous. From `state_28d.py` the 28 components map as:

| Index \(n\) | Level | Symbol (state_28d) | Role |
|-------------|-------|-------------------|------|
| 1 | 1 | xi_0 | Existence |
| 2–3 | 2 | xi_10, xi_11 | Position, velocity |
| 4–6 | 3 | xi_p0, xi_p1, xi_p2 | Plane |
| 7–10 | 4 | xi_s0 … xi_s3 | Sphere |
| 11–15 | 5 | T_1 … T_5 | Torus (matter structure) |
| 16–21 | 6 | Phi_0 … Phi_5 | Dynamism |
| 22 | 7 | eps_0 | Potential |
| 23 | 7 | eps_1 | Kinetic |
| 24 | 7 | eps_2 | Rotational |
| **25** | **7** | **eps_3** | **Field (pressure-occlusion)** |
| **26** | **7** | **eps_b** | **Binding** |
| **27** | **7** | **eps_4** | **Flux** |
| 28 | 7 | eps_5 | Transmission |

So \(\overline{A}^{(7)}_{\mathrm{field}} = A_{25}\), \(\overline{A}^{(7)}_{\mathrm{binding}} = A_{26}\), \(\overline{A}^{(7)}_{\mathrm{flux}} = A_{27}\) (or level-7 means over those components, as declared).

### 9.4 Deterministic \(\mathcal{W}(\Lambda, A_{28})\) (no weight vectors)

Arbitrary \(w_n(\Lambda)\) over 28 aspects would reintroduce 28 free knobs. **Forbidden.** Lock-in a form that privileges Level 7 (field/binding/flux) and uses a **compiler-selected** wavelength:

\[
\mathcal{W}(\Lambda, A_{28}) = \left( \frac{\lambda_{\mathrm{ref}}}{\lambda_{\mathrm{eff}}(\Lambda)} \right)^{\!p} \cdot \Psi(A_{28})
\]

**Wavelength selection rule (mandatory):** \(\lambda_{\mathrm{eff}}(\Lambda)\) is chosen by **regime**, not by fit:

| Regime | \(\lambda_{\mathrm{eff}}\) | Source in \(\Lambda\) |
|--------|---------------------------|------------------------|
| Atomic | \(\lambda_{\mathrm{H}}\) | Hydrogen spectral (or Compton/de Broglie if defined) |
| Nuclear | \(\lambda_{\mathrm{nuc}}\) | Trefoil / NUCLEAR_STRUCTURE mode |
| Celestial | \(\lambda_{\mathrm{B}}\) | Body structural |

The compiler **declares** which regime applies to \(S\); no “pick the wavelength that works.”

**Reference wavelength:** \(\lambda_{\mathrm{ref}}\) is a **fixed** global constant (e.g. \(\lambda_{\mathrm{H}}\) for hydrogen anchoring). **Exponent:** \(p\) is a **single** global exponent, calibrated once.

**Aspect factor:**

\[
\Psi(A_{28}) = \frac{1}{1 + \gamma\,\Bigl( \overline{A}^{(7)}_{\mathrm{field}} + \overline{A}^{(7)}_{\mathrm{binding}} + \overline{A}^{(7)}_{\mathrm{flux}} \Bigr)}
\]

with \(\gamma\) a **single** global constant. Using state_28d indices: \(\overline{A}^{(7)}_{\mathrm{field}} \leftrightarrow \mathrm{eps}_3\), \(\overline{A}^{(7)}_{\mathrm{binding}} \leftrightarrow \mathrm{eps}_{\mathrm{b}}\), \(\overline{A}^{(7)}_{\mathrm{flux}} \leftrightarrow \mathrm{eps}_4\) (or their level-7 mean). Optionally collapse to one macro constant by setting \(\gamma = 1\).

**Hostile note:** If you allow \(w_n(\Lambda)\) as an arbitrary vector, you have 28 free knobs. Don’t. This lock-in gives **two** global degrees of freedom \((p, \gamma)\) for the macro law, or one if \(\gamma\) is fixed.

---

## 10) Full macro law (one-shot computable)

With the three lock-ins (§2.1.1, §2.2.1, §9.4) and \(\mathcal{U}(R_{\mathrm{eff}}/r) = R_{\mathrm{eff}}/r\):

\[
D(r; S) = \Sigma_{\mathrm{occ}}(S) \cdot \rho_{\mathrm{pres}}(S) \cdot \frac{R_{\mathrm{eff}}}{r} \cdot \mathcal{W}(\Lambda, A_{28})
\]

\[
v(r) = c\sqrt{D(r; S)}
\]

The only remaining degrees of freedom are: **one** calibration anchor for macro constants (\(\eta\); and optionally \(p\), \(\gamma\))—fixed from hydrogen alone or from one celestial body alone—and the **regime selection** for \(\lambda_{\mathrm{eff}}\). No hidden fits.

---

## 11) Compiler pipeline summary

| Step | Action | Output |
|------|--------|--------|
| 1 | Input: \(G_{\mathrm{pack}}\), \(\mathcal{G}\), \(\mathcal{M}\), \(\Lambda\); **declare** regime and \(R_j\) (constant or per-patch) | Raw structure |
| 2 | Tessellate \(\partial S\) → patches \(\{P_j, \mathbf{p}_j, R_j\}\); compute \(\Sigma_{\mathrm{occ}}(S)\) via §2.1.1 | Occlusion scalar |
| 3 | Compute \(\rho_{\mathrm{pres}}(S) = 1/\mathcal{H}\) with canonical \(\mathcal{H}\) (§2.2.1) | Presence density |
| 4 | Compute \(A_{28}\) from \((\mathcal{M}, \mathcal{G}, \Lambda)\) (mapping rules; see §12) | Aspect stack |
| 5 | \(D(r; S) = \Sigma_{\mathrm{occ}}\,\rho_{\mathrm{pres}}\,(R_{\mathrm{eff}}/r)\,\mathcal{W}(\Lambda, A_{28})\) (§9.4) | Binding depth |
| 6 | \(v(r) = c\sqrt{D(r; S)}\); rotation; luminosity proxy | SDT observables |
| 7 | **Compare only:** \(GM_{\mathrm{eq}}(r)\), \(z_{\mathrm{eq}}(r)\) | Benchmark tables |

**Binding (micro):** \(B = \kappa_B \cdot \Omega_{\mathrm{total}}\) throughout; \(\kappa_B\) from ²H only; \(v\) and \(\kappa_v\) reserved for velocity field.

---

## 12) What’s still missing (bounded list)

1. **Numerical mapping \((\mathcal{M}, \mathcal{G}, \Lambda) \to A_{28}\):** The semantic grouping (Levels 1–7) and index map (§9.3) are fixed. The **mapping rules** that assign numeric values to the 28 components from structure must be written explicitly (even coarse). **Coarse direction:** Level 1 (xi_0) = existence/scale flag; Level 2–4 from position, velocity, boundaries, volume in \(\mathcal{G}\); Level 5 (T_1…T_5) from body geometry (e.g. T_3 = surface → \(4\pi R_{\mathrm{eff}}^2\)); Level 6 from dynamism/phase; Level 7 (eps_3, eps_b, eps_4) from occlusion-derived field, binding energy, and flux. Normalisation (e.g. to [0,1] or physical units) must be declared. Once added, this removes the last ambiguity channel.
2. **Regime selection rule:** The compiler must **declare** which regime (atomic / nuclear / celestial) applies to each \(S\), so that \(\lambda_{\mathrm{eff}}(\Lambda)\) is chosen by rule, not by fit. §9.4 table is the contract.
3. **One calibration anchor for macro constants:** \(\eta\) (and optionally \(p\), \(\gamma\)) are fixed **once**—e.g. from hydrogen alone (so that \(\kappa_v = \alpha\) at \(S_{\mathrm{H}}\)), or from one celestial body alone. Declare which anchor is used; no per-body tuning.

After those three are specified, the examiner can only attack (a) overlap-heuristic error bounds, (b) sufficiency of occlusion-to-presence mapping, and (c) cross-scale wavelength selection—not “you smuggled GM,” because the compiler structure makes that mechanically impossible.

---

*(End of SDT COMPILER SPEC v1.0)*
