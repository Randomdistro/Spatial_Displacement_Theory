# SDT Core Language and Compiler Spec

**Purpose:** Formal SDT-only derivation pipeline. No GM/GR/Newton inside the generator; comparison-only mapping at output. This document gives (1) the primitive set and state descriptor **S**, (2) the **current formal definitions** of the occlusion functional \(\Sigma_{\mathrm{occ}}\) and the presence/density scalar \(\rho_{\mathrm{pres}}\), and (3) the compiler-style pipeline so that \(R\) (and hence \(v(r)\), \(\kappa_v(r)\)) is computable from structure without orbital velocities as input.

**Constraint set (internal SDT):** Geometry, velocity, occlusion, presence/density, nuclear packing, \(c\), \(\lambda\), \(\pi\), \(\varphi/\Phi\), and the 28-aspect recursion \(n = n + n!\). GM/GR/Newton only as external benchmark.

**Symbol hygiene:** Binding vs velocity must not share the same symbol. This spec and the compiler use **\(\kappa_B\)** (MeV/sr) for nuclear binding proportionality (\(B = \kappa_B \cdot \Omega_{\mathrm{total}}\)), and **\(v\)** (m/s) / **\(\kappa_v \equiv v/c\)** for orbital/structure velocity. See **SDT_COMPILER_SPEC_v0.9.md** §0.

---

## 1. Constants and scalars (SDT primitives)

| Symbol | Dimension | Role |
|--------|-----------|------|
| \(c\) | m/s | Invariant speed (structure velocity scale) |
| \(\pi\) | 1 | Circle constant (solid angle \(2\pi(1-\cos\theta)\), etc.) |
| \(\varphi\), \(\Phi\) | 1 | Phase / flux (dimensionless) |
| \(\lambda\) | m | Characteristic wavelength; **subscript by regime**: \(\lambda_{\mathrm{H}}\) (hydrogen spectral), \(\lambda_{\mathrm{B}}\) (body structural), \(\lambda_{\mathrm{L}}\) (lattice mode), etc. Same symbol, regime-specific definition; no ambiguity. |

No \(\hbar\), \(G\), or \(M\) as primitives. \(\alpha\) (fine structure constant) is **defined** as the structure velocity fraction \(\kappa_{\mathrm{H}} = v_{e,1}/c\) at hydrogen, derived from packing + occlusion (see §6).

---

## 2. State descriptor (structure only)

Every macroscopic field parameter is a **functional of the structural state**:

\[
S \equiv \bigl( G_{\mathrm{pack}},\ \rho_{\mathrm{pres}},\ \Sigma_{\mathrm{occ}},\ \Lambda,\ A_{28} \bigr)
\]

- **\(G_{\mathrm{pack}}\)**: SDT nuclear packing descriptor. Computable from nucleon/electron layout rules (icosahedral base, first shell, second layer, alpha-cluster positions; see Structural and Mechanical Specification). No “mass” input.
- **\(\rho_{\mathrm{pres}}\)**: Presence/density scalar. Defined below (§4). Operationally: spation-exclusion per effective volume (or dimensionless ratio).
- **\(\Sigma_{\mathrm{occ}}\)**: Occlusion functional (dimensionless). Defined below (§3). Solid-angle occlusion integrated over the external boundary as “seen” by the lattice (or by a designated observer).
- **\(\Lambda\)**: Characteristic structural wavelengths (one \(\lambda_{\mathrm{B}}\) or a spectrum of modes). Same symbol \(\lambda\), subscripted by regime.
- **\(A_{28}\)**: 28-aspect vector from the recursion \(n = n + n!\). Multiscale stack of “views” of the same structure. \(A_{28}: \{\rho_{\mathrm{pres}}, \Sigma_{\mathrm{occ}}, G_{\mathrm{pack}}, \Lambda\} \to \{\text{level } 1, \ldots, 28\}\).

**Hard requirement:** \(R\) (or the binding-depth scale that sets \(v(r)\)) must be computable from \(S\) **without** using orbital velocities as inputs:

\[
\boxed{R = \mathcal{R}\bigl( \Sigma_{\mathrm{occ}},\ \rho_{\mathrm{pres}},\ G_{\mathrm{pack}},\ \Lambda,\ A_{28} \bigr)}
\]

If this recipe exists, SDT is generative. If \(R\) is inferred from observed \(v(r)\), SDT is descriptive curve-fitting.

---

## 3. Formal definition of \(\Sigma_{\mathrm{occ}}\) (occlusion functional)

### 3.1 Operational meaning

\(\Sigma_{\mathrm{occ}}\) is the **total solid-angle occlusion** (steradians, or normalised by \(4\pi\) so dimensionless in [0,1]) that the structure presents to the ambient pressure field from a defined **observer frame**. In the nuclear-structure probe it is computed per nucleus (or cluster) and used in \(B = \kappa_B \cdot \Omega_{\mathrm{total}}\).

### 3.2 Spherical (single-sphere) kernel

For one sphere of radius \(R\) with centre at distance \(d\) from the observer:

\[
\Omega(R, d) = 2\pi\,\bigl(1 - \cos\theta\bigr), \qquad \sin\theta = \frac{R}{d},\quad \cos\theta = \sqrt{1 - (R/d)^2}.
\]

**Edge cases:** \(d \le 0 \Rightarrow \Omega = 0\); \(d < R \Rightarrow \Omega = 4\pi\); \(d = R \Rightarrow \Omega = 2\pi\); \(d > R\) use formula; cap \(\Omega \le 4\pi\).

### 3.3 Multi-body (corrected total occlusion)

Given observer position \(\mathbf{o}\) and a set of spheres (centres \(\{\mathbf{p}_i\}\), common radius \(R\)):

1. **Uncorrected:** \(\Omega_{\mathrm{raw}} = \sum_i \Omega\bigl(R, |\mathbf{o} - \mathbf{p}_i|\bigr)\), capped at \(4\pi\).
2. **Overlap correction:** For each pair \((i,j)\), inter-centre distance \(d_{ij} = |\mathbf{p}_i - \mathbf{p}_j|\). If \(d_{ij} \ge 2R\), overlap \(= 0\). Else \(\eta = (2R - d_{ij})/(2R)\) (clamped to \([0,1]\)), and overlap \(\propto \tfrac{1}{2}(\Omega_i + \Omega_j)\,\eta \cdot 0.5\).
3. **Corrected total:** \(\Sigma_{\mathrm{occ}}^{\mathrm{corrected}} = \max\bigl(0,\ \min\bigl(4\pi,\ \Omega_{\mathrm{raw}} - \sum_{\mathrm{pairs}} \text{overlap}\bigr)\bigr)\).

So \(\Sigma_{\mathrm{occ}}\) is **observer-dependent** and **structure-dependent** (positions and \(R\) from \(G_{\mathrm{pack}}\) and arrangement-specific radius, e.g. \(R(n_{\mathrm{bonds}})\) in the probe).

### 3.4 Integral form (for arbitrary bodies)

For a continuous body or lattice, the **occlusion functional** as used in the compiler is the integral over the **external boundary** of the solid angle subtended by the structure, as seen from each point of the lattice (or from a designated observer surface):

\[
\Sigma_{\mathrm{occ}}(S) = \int_{\partial V} \sigma_{\mathrm{occ}}(\mathbf{x}; S)\, dA \quad \text{or} \quad \Sigma_{\mathrm{occ}}(S) = \sum_{\mathrm{observers}} \Omega_{\mathrm{total}}(\mathrm{observer}; S).
\]

In the nuclear probe, “observer” is the geometric centre of the cluster and “spheres” are nucleon or alpha centres with effective radii; \(\Omega_{\mathrm{total}}\) is the corrected sum above. So **currently** \(\Sigma_{\mathrm{occ}}\) is implemented as a **discrete sum over sphere occlusions with pairwise overlap correction**, not yet as a continuum boundary integral. The continuum form is the target for the compiler when \(G_{\mathrm{pack}}\) describes an extended body.

### 3.5 Summary (for compiler)

- **Inputs:** \(G_{\mathrm{pack}}\) (positions and radii of occluding spheres or boundary), observer position(s).
- **Output:** \(\Sigma_{\mathrm{occ}} \in [0, 4\pi]\) (sr), or normalised \(\Sigma_{\mathrm{occ}}/(4\pi) \in [0,1]\).
- **No** \(v(r)\), \(M\), or \(G\) in the recipe.

---

## 4. Formal definition of \(\rho_{\mathrm{pres}}\) (presence/density scalar)

### 4.1 Operational meaning (SDT intent)

“Presence” is the degree to which the structure **excludes spation** (displacement medium) from a region. **Density** in this context is not “mass per volume” but **spation-exclusion per effective volume**: how much of the ambient field is occluded or displaced per unit effective structural volume (or per unit volume of the lattice). So \(\rho_{\mathrm{pres}}\) is a **structural** measure: high where matter is dense in the geometric/packing sense, zero in vacuum.

### 4.2 Current status in SDT documents

- **Nuclear probe:** No explicit symbol \(\rho_{\mathrm{pres}}\). Packing is described by \(G_{\mathrm{pack}}\) (positions, radii, bond counts). “Density” appears in ATOMICUS as **specific volume** (minimize specific volume → maximize wake cancellation) and in chemistry docs as **packing density** (e.g. FCC 0.74, icosahedral ~0.69).
- **Embellishment Gaps / core:** \(\rho_s\) (spation mass density) appears in equations (e.g. \(P = \rho_s c^2 R_{\mathrm{uni}}/r\)); “electron point presence” \(R_e\) is a length scale. So “presence” has been used for a **scale** (point presence) and “density” for a **field** (\(\rho_s\)).

### 4.3 Proposed operational definition (for compiler lock-in)

So that \(R = \mathcal{R}(S)\) can be closed without GM:

**Option A (dimensionless):**  
\(\rho_{\mathrm{pres}}\) = **fraction of a reference volume that is “filled” by the structure** (spation-exclusion fraction). For a nucleus: (volume enclosed by nucleon spheres) / (convex hull or circumscribed volume). For a lattice: packing fraction (e.g. icosahedral 12-around-1 ≈ 0.69). So \(\rho_{\mathrm{pres}} \in [0,1]\).

**Option B (with dimension 1/m³):**  
\(\rho_{\mathrm{pres}}\) = **number of occluding centres per unit volume** (e.g. nucleons per fm³, or lattice sites per m³), weighted by an effective occlusion cross-section. So \(\rho_{\mathrm{pres}}\) has dimension L⁻³; “presence” is then density of occluders.

**Option C (structure-only scalar):**  
\(\rho_{\mathrm{pres}} = \mathcal{P}(G_{\mathrm{pack}}, \Lambda)\): a scalar computed from packing geometry and characteristic wavelengths only (e.g. from \(G_{\mathrm{pack}}\) a “count per unit cell” and \(\lambda_{\mathrm{B}}^3\) as cell volume). No mass.

**Recommendation:** Adopt **Option A** for the compiler so that \(\rho_{\mathrm{pres}}\) is dimensionless and clearly structure-derived (packing fraction or occlusion-fill fraction). Then \(\mathcal{R}(S)\) can depend on \(\rho_{\mathrm{pres}}\) without introducing mass or GM.

### 4.4 Summary (for compiler)

- **Inputs:** \(G_{\mathrm{pack}}\) (positions, radii, or boundary), optionally \(\Lambda\) (e.g. \(\lambda_{\mathrm{B}}\) for cell size).
- **Output:** \(\rho_{\mathrm{pres}}\) (dimensionless [0,1] or L⁻³ per regime choice). No \(M\), \(G\), or \(v(r)\) in the recipe.

---

## 5. SDT field generator (occlusion → velocity field)

Binding depth field from structure:

\[
D(\mathbf{x}) = \mathcal{F}\bigl( \Sigma_{\mathrm{occ}}(S),\ \mathbf{x},\ A_{28} \bigr).
\]

Orbital velocity field (SDT observable):

\[
v(\mathbf{x}) = c \cdot \mathcal{G}\bigl(D(\mathbf{x})\bigr).
\]

Circular-orbit ansatz:

\[
v(r)^2 = c^2 \frac{R}{r}.
\]

**Structure-derived scale:**

\[
R = \mathcal{R}\bigl( \Sigma_{\mathrm{occ}},\ \rho_{\mathrm{pres}},\ G_{\mathrm{pack}},\ \Lambda,\ A_{28} \bigr).
\]

So \(R\) is a **mutual occlusion/presence outcome**, not a mass proxy. Speed: \(v(r)\) [m/s]; dimensionless fraction: \(\kappa_v(r) \equiv v(r)/c\) [1].

---

## 6. Hydrogen bridge (\(\alpha \equiv \kappa_{\mathrm{H}}\))

Observed: \(v_{e,1} = \alpha c\) at hydrogen. In SDT:

\[
\kappa_{\mathrm{H}} \equiv \frac{v_{e,1}}{c};
\qquad
\kappa_{\mathrm{H}} = \mathcal{G}\Bigl( D_{\mathrm{H}}\bigl( G_{\mathrm{pack,H}},\ \rho_{\mathrm{pres,H}},\ \Sigma_{\mathrm{occ,H}},\ \Lambda_{\mathrm{H}},\ A_{28,\mathrm{H}} \bigr) \Bigr).
\]

So the fine-structure constant is **reinterpreted** as the structure velocity fraction at hydrogen, derived from packing + occlusion + presence at the atomic scale, **without** \(\hbar\) as a primitive.

---

## 7. Comparison-only mapping (quarantined)

After SDT yields \(v(r)\):

\[
GM_{\mathrm{eq}}(r) \stackrel{\text{compare}}{=} v(r)^2\, r;
\qquad
z_{\mathrm{eq}}(r) \stackrel{\text{compare}}{=} \frac{v(r)^2}{c^2}.
\]

Not used inside SDT; output projection for benchmark and tables.

---

## 8. Rotation and luminosity (SDT-internal)

- **Rotation:** \(v_{\mathrm{rot}} = \mathcal{H}(S, \Lambda, A_{28})\). Preferred eigenmode of lattice-pressure redistribution; correlates with occlusion anisotropy, packing asymmetry, mode-locking via \(\Lambda\).
- **Luminosity:** \(L \propto \int_{\partial V} \dot{\epsilon}(\mathbf{x})\, dA\) with \(\dot{\epsilon}(\mathbf{x}) = \mathcal{J}(\nabla D, \Lambda, A_{28})\). Luminosity from **gradient stress + mode spectrum**, not mass.

---

## 9. 28-aspect recursion

\(A_{28}\) maps base structural measures into a multiscale stack:

\[
A_{28}:\ \bigl\{ \rho_{\mathrm{pres}},\ \Sigma_{\mathrm{occ}},\ G_{\mathrm{pack}},\ \Lambda \bigr\} \to \{\text{level } 1, \ldots, 28\}.
\]

Recursion rule: \(n = n + n!\) (each aspect encloses/compresses prior aspects). Field generator:

\[
D(\mathbf{x}) = \sum_{n=1}^{28} w_n\, D_n(\mathbf{x}; A_{28,n}).
\]

---

## 10. One-page compiler pipeline

| Step | Action | Input | Output |
|------|--------|--------|--------|
| 1 | **Input** | Nuclear packing schema + body geometry + density proxy + wavelength set (\(\Lambda\)) | \(G_{\mathrm{pack}}\), \(\Lambda\), and raw structure |
| 2 | **Compute \(\Sigma_{\mathrm{occ}}\)** | \(G_{\mathrm{pack}}\), observer(s) | Solid-angle occlusion (spherical kernel + overlap correction); §3 |
| 3 | **Compute \(\rho_{\mathrm{pres}}\)** | \(G_{\mathrm{pack}}\), \(\Lambda\) | Presence/density scalar (§4; e.g. packing fraction) |
| 4 | **Compute \(A_{28}\)** | \(\rho_{\mathrm{pres}}\), \(\Sigma_{\mathrm{occ}}\), \(G_{\mathrm{pack}}\), \(\Lambda\) | 28-level aspect stack |
| 5 | **Generate \(D(\mathbf{x})\)** | \(\Sigma_{\mathrm{occ}}\), \(A_{28}\), \(\mathbf{x}\) | Binding depth field |
| 6 | **Output** | \(D\), \(R = \mathcal{R}(S)\) | \(v(r)\), \(\kappa_v(r) = v(r)/c\); rotation mode; luminosity proxy |
| 7 | **Compare only** | \(v(r)\) | \(GM_{\mathrm{eq}}(r)\), \(z_{\mathrm{eq}}(r)\) for tables |

**Current formal definitions (to lock in):**

- **(a) \(\Sigma_{\mathrm{occ}}\):** Discrete form: observer at \(\mathbf{o}\), spheres at \(\{\mathbf{p}_i\}\) with radius \(R\); \(\Sigma_{\mathrm{occ}} = \mathrm{corrected\_total\_occlusion}(\mathbf{o}, \{\mathbf{p}_i\}, R)\) per §3.2–3.3. Continuum form: integral over boundary of solid angle subtended by structure (§3.4). No \(v(r)\) or \(M\) in the recipe.
- **(b) \(\rho_{\mathrm{pres}}\):** Proposed: packing fraction or occlusion-fill fraction from \(G_{\mathrm{pack}}\) (Option A, dimensionless). Alternative: occluder density (Option B, L⁻³). To be fixed so that \(\mathcal{R}(S)\) is closed.

---

## 11. References

- **SDT_COMPILER_SPEC_v0.9.md** — Full compiler: symbol hygiene (κ_B vs v/κ_v), Σ_occ boundary-integrated, ρ_pres = V_geom/V_eff, D(r;S), v(r)=c√D, 𝒲(Λ,A_28), hostile checks, compare-only.
- **STRUCTURAL_AND_MECHANICAL_SPECIFICATION.md** — Occlusion formula, overlap correction, \(G_{\mathrm{pack}}\) (icosahedral, Shell 2, alpha arrangements); binding \(B = \kappa_B \cdot \Omega\).
- **NUCLEAR_CONSTANTS.md** — \(R_{\mathrm{NUCLEON}}\), \(d_{\mathrm{deuteron}}\), \(d_\alpha\), \(\kappa_B\), \(R(n_{\mathrm{bonds}})\).
- **01_05_geometric_calculations.py** — `corrected_total_occlusion`, `spherical_occlusion`.
- **02_04_alpha_clusters.py** — \(\Omega_{\mathrm{total}}\) for clusters; observer at cluster centre; binding constant in code as `k` (spec symbol \(\kappa_B\)).

---

*(End of SDT Core Language and Compiler Spec)*
