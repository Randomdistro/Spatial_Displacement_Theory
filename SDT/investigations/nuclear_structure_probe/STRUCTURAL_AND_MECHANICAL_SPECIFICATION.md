# Structural and Mechanical Specification: Nuclear Packing and Occlusion-Based Binding

**Document type:** Technical specification (single-source outline)  
**Scope:** Geometric structure, occlusion mechanics, calibration hierarchy, validation pipeline, and integration with the 6π trefoil / NUCLEAR_STRUCTURE system.  
**Units:** Lengths in femtometres (fm); solid angle in steradians (sr); binding energy in MeV; velocities in units of c where stated.

---

## 1. Axiomatic and Physical Basis

### 1.1 Binding–occlusion relation

Binding energy \(B\) is taken to be proportional to the total solid-angle occlusion \(\Omega_{\mathrm{total}}\) subtended by the nucleus (or subsystem) with respect to a defined observer frame:

\[
B = \kappa_B \cdot \Omega_{\mathrm{total}}
\]

where \(\kappa_B\) is the nuclear binding constant (MeV/sr). *Symbol hygiene:* \(\kappa_B\) is reserved for this; orbital/velocity uses \(v\) and \(\kappa_v \equiv v/c\) (see SDT_COMPILER_SPEC_v0.9.md §0). The proportionality is motivated by an effective pressure field (e.g. CMB-sourced) whose work integral scales with occlusion: \(P_{\mathrm{eff}} \propto \Omega\) so that \(B \propto \int P_{\mathrm{eff}}\,d(\mathrm{volume})\) reduces to \(B \propto \Omega\) under the model’s assumptions. No other degrees of freedom (e.g. velocity, charge) enter this binding formula; they are treated as contextual (trefoil kinematics, electron-sharing) elsewhere.

### 1.2 Single calibration nucleus

The constant \(\kappa_B\) is fixed from one nucleus only, the deuteron (²H), so that \(\kappa_B = B_{\mathrm{exp}}(^2\mathrm{H}) / \Omega(^2\mathrm{H})\). All other nuclei are structural predictions under this \(\kappa_B\). No fit to ¹²C, ¹⁶O, or ⁸Be is used to set \(\kappa_B\).

---

## 2. Geometric Hierarchy

### 2.1 Icosahedral base (Shell 0)

- **Locus:** `Phase_01_Nuclear_Packing/01_01_icosahedral_base_geometry.py`
- **Structure:** One central sphere (radius \(r\)) at the origin; 12 equivalent spheres with centres on an icosahedron at radial distance \(2r\). All spheres have radius \(r = R_{\mathrm{NUCLEON}}\) (0.84 fm). Pairwise separation of outer centres is \(2r\). Total span 6r along any axis through the cluster.
- **Role:** Defines the coordinate system and the two octahedral interstitial volumes used for the first shell (deuteron and alpha).

### 2.2 First shell (deuteron and alpha)

- **Locus:** `01_02_first_shell_completion.py`
- **Deuteron:** One proton and one neutron placed in one octahedral interstitial; separation \(d_{\mathrm{deuteron}} = 2.10\) fm (DIST_DEUTERON_FM). Occlusion \(\Omega(^2\mathrm{H})\) is the solid angle of one sphere of radius \(R\) at distance \(d\) (single p–n “bond”).
- **Alpha (⁴He):** Four nucleons in a tetrahedral arrangement with edge length derived from \(d_\alpha = \mathrm{DIST\_ALPHA\_FM}\) (1.479 fm). Six bonds; total occlusion \(\Omega_\alpha = 6 \cdot \Omega_{\mathrm{bond}}(d_\alpha)\). \(d_\alpha\) is chosen so that \(\kappa_B \cdot \Omega_\alpha = B_{\mathrm{exp}}(^4\mathrm{He})\) with \(\kappa_B\) from the deuteron (deuteron–alpha parity).

### 2.3 Second layer: 20 triangular interstices (Shell 2)

- **Locus:** `01_03_second_layer_structure.py`
- **Construction:** The icosahedron has 20 triangular faces. Each face is the convex hull of three first-shell vertices. The centroid of each triangle is a **triangular interstice**. There are therefore 20 interstices; their positions are computed from the first-shell vertex coordinates. They are the candidate sites for alpha clusters in the A ≤ 40 regime.
- **Isolation:** Interstices are verified to be mutually separated by more than \(2r\) so that spheres placed there do not overlap.
- **Alignment:** Conceptually identical to “Shell 2” in `generate_trefoil_mappings.py` (20 positions from icosahedral faces); that implementation uses a fixed list of \((\theta,\phi)\) at \(R_2 \approx 2.5r\); Phase 01 derives positions from the same icosahedral geometry.

### 2.4 Alpha-cluster arrangements (Phase 01)

- **Carbon-12 (¹²C):** Three alpha centres on an equilateral triangle in the \(z=0\) plane; side length DIST_INTER_ALPHA_FM (2.9 fm). One vertex at the origin.
- **Oxygen-16 (¹⁶O):** Four alpha centres at the vertices of a regular tetrahedron; all edges 2.9 fm. One vertex at the origin; remaining vertices from that basis.
- **Nitrogen-14 (¹⁴N):** Same triangular alpha layout as ¹²C, plus one extra nucleon (or pair) at the triangle centroid.
- **Beryllium-8 (⁸Be):** Two alpha centres (dumbbell); separation 2.9 fm along one axis (no Phase 01 class; positions defined in Phase 02).

---

## 3. Constants and Units

| Symbol | Value | Unit | Derivation / source |
|--------|--------|------|---------------------|
| \(R_{\mathrm{NUCLEON}}\) | 0.84 | fm | Nucleon charge radius; used as effective occlusion radius |
| \(d_{\mathrm{deuteron}}\) | 2.10 | fm | Deuteron p–n separation (experimental) |
| \(d_\alpha\) | 1.479 | fm | Alpha internal bond length; set by \(B_{\mathrm{exp}}(^4\mathrm{He})\) and \(\kappa_B\) |
| \(d_{\mathrm{inter}\alpha}\) | 2.9 | fm | Inter-alpha centre–centre spacing (¹²C, ¹⁶O geometry) |

**Derived:**

- **Alpha tetrahedron:** Centre-to-vertex distance \(d_\alpha \sqrt{3/8}\); effective alpha radius for inter-alpha occlusion \(R_\alpha = d_\alpha \sqrt{3/8} + R_{\mathrm{NUCLEON}}\).
- **Inter-alpha sphere radius (arrangement-dependent):**  
  \(R(n_{\mathrm{bonds}}) = R_{\mathrm{base}} \bigl(1 + \beta\,(n_{\mathrm{bonds}} - 3)/3\bigr)\)  
  with \(R_{\mathrm{base}} = 0.70\) fm, \(\beta = 0.2747\). Thus: triangle (3 bonds) → 0.70 fm; tetrahedron (6 bonds) → ≈ 0.8923 fm; dumbbell (1 bond) → ≈ 0.57 fm. Used as the sphere radius in the overlap-corrected inter-alpha occlusion (observer at cluster centre viewing alpha centres as spheres).
- **¹⁴N centre–alpha distance:** \(d_{\mathrm{center}} = 2.9/\sqrt{3}\) fm (triangle centroid to vertex).

**Experimental binding energies (MeV), AME:** ²H 2.2246; ⁴He 28.296; ¹²C 92.162; ¹⁴N 104.66; ¹⁶O 127.619; ⁸Be 56.5 (unstable).

---

## 4. Occlusion Mechanics

### 4.1 Single sphere (spherical occlusion)

An observer at distance \(d\) from the centre of a sphere of radius \(R\) sees a solid angle:

\[
\Omega = 2\pi\,(1 - \cos\theta), \qquad \sin\theta = \frac{R}{d}, \quad \cos\theta = \sqrt{1 - (R/d)^2}.
\]

**Edge cases:** \(d \le 0 \Rightarrow \Omega = 0\); \(d < R \Rightarrow \Omega = 4\pi\); \(d = R \Rightarrow \Omega = 2\pi\); \(d > R\) use the formula; implementation clamps \(\Omega \le 4\pi\).

**Loci:** `02_01_occlusion_binding_calculator.spherical_occlusion`, `01_05_geometric_calculations.spherical_occlusion`.

### 4.2 Multiple spheres: overlap correction

For several spheres at positions \(\{\mathbf{p}_i\}\) and common radius \(R\), the **uncorrected** total occlusion from an observer at \(\mathbf{o}\) is \(\sum_i \Omega(R, |\mathbf{o} - \mathbf{p}_i|)\), capped at \(4\pi\).

**Overlap correction:** For each pair \((i,j)\), an overlap term is computed from the two individual occlusions \(\Omega_i, \Omega_j\), the inter-centre distance \(d_{ij}\), and \(R\). If \(d_{ij} \ge 2R\), overlap is zero. Otherwise a heuristic fraction \(\eta = (2R - d_{ij})/(2R)\) (clamped to \([0,1]\)) is applied: overlap \(\propto \tfrac{1}{2}(\Omega_i + \Omega_j)\,\eta \cdot 0.5\). The **corrected total occlusion** is the sum of single-sphere occlusions minus the sum of pairwise overlaps, then clamped to \([0, 4\pi]\).

**Function:** `01_05_geometric_calculations.corrected_total_occlusion(observer_position, sphere_positions, sphere_radius)`.

### 4.3 Inter-alpha occlusion (alpha-cluster nuclei)

- **Observer:** Geometric centre of the alpha centres (triangle: centroid; tetrahedron: centroid; dumbbell: midpoint).
- **Spheres:** One sphere per alpha centre; radius is the arrangement-dependent \(R(n_{\mathrm{bonds}})\) above (triangle / tetrahedron / dumbbell).
- **Value:** \(\Omega_{\mathrm{inter}} = \mathrm{corrected\_total\_occlusion}(\mathrm{centre}, \mathrm{alpha\_positions}, R)\).
- **Total occlusion (cluster):** \(\Omega_{\mathrm{total}} = n_\alpha \cdot \Omega_\alpha^{\mathrm{internal}} + \Omega_{\mathrm{inter}}\), where \(\Omega_\alpha^{\mathrm{internal}}\) is the tetrahedral alpha occlusion (6 bonds at \(d_\alpha\)). Scale factor on \(\Omega_{\mathrm{inter}}\) is 1.0 (no C-12 or Be-8 fit).

**Locus:** `02_04_alpha_clusters.py`: `_overlap_corrected_inter_alpha_occlusion(positions, arrangement_type)`, `AlphaClusterNucleus.calculate_total_occlusion()`.

---

## 5. Calibration and Prediction Flow

1. **Deuteron:** \(\Omega(^2\mathrm{H}) = \mathrm{spherical\_occlusion}(R_{\mathrm{NUCLEON}}, d_{\mathrm{deuteron}})\). \(\kappa_B = B_{\mathrm{exp}}(^2\mathrm{H}) / \Omega(^2\mathrm{H})\). So \(B_{\mathrm{pred}}(^2\mathrm{H}) = B_{\mathrm{exp}}(^2\mathrm{H})\) by construction.
2. **Alpha:** \(\Omega_\alpha\) from 6 bonds at \(d_\alpha\); \(d_\alpha\) chosen so \(\kappa_B \cdot \Omega_\alpha = B_{\mathrm{exp}}(^4\mathrm{He})\). So \(B_{\mathrm{pred}}(^4\mathrm{He}) = B_{\mathrm{exp}}(^4\mathrm{He})\) by construction.
3. **¹²C:** Three alphas; triangle positions from Phase 01; \(\Omega_{\mathrm{total}} = 3\Omega_\alpha^{\mathrm{internal}} + \Omega_{\mathrm{inter}}\) with triangle \(R\); \(B_{\mathrm{pred}} = \kappa_B \cdot \Omega_{\mathrm{total}}\).
4. **¹⁶O:** Four alphas; tetrahedron positions; \(\Omega_{\mathrm{inter}}\) with tetrahedron \(R\); \(B_{\mathrm{pred}} = \kappa_B \cdot \Omega_{\mathrm{total}}\).
5. **⁸Be:** Two alphas; dumbbell positions; same formula; informational only (unstable).
6. **¹⁴N:** \(\Omega(^{14}\mathrm{N}) = \Omega(^{12}\mathrm{C}) + 3 \cdot \mathrm{spherical\_occlusion}(R_{\mathrm{tetra}}, d_{\mathrm{center}})\). The extra term is the occlusion of three “alpha” spheres (radius \(R_{\mathrm{tetra}}\)) as seen from the triangle centre at distance \(d_{\mathrm{center}}\). No fit to \(B_{\mathrm{exp}}(^{14}\mathrm{N})\).

**Binding prediction:** \(B_{\mathrm{pred}} = \kappa_B \cdot \Omega_{\mathrm{total}}\) in all cases.

---

## 6. Validation Pipeline

- **Script:** `run_nuclear_stacking_validation.py` (probe root).
- **Inputs:** Phase 02 modules (deuteron calibration, alpha structure, alpha clusters); experimental \(B_{\mathrm{exp}}\) for ²H, ⁴He, ¹²C, ¹⁴N, ¹⁶O; ⁸Be optional/informational.
- **Process:** Compute \(\kappa_B\) from deuteron; for each nucleus compute \(\Omega_{\mathrm{total}}\) and \(B_{\mathrm{pred}} = \kappa_B \cdot \Omega_{\mathrm{total}}\); compute relative error \(\varepsilon = |B_{\mathrm{pred}} - B_{\mathrm{exp}}| / B_{\mathrm{exp}}\).
- **Assertions:** \(\varepsilon < 0.08\%\) for ²H, ⁴He, ¹²C, ¹⁴N, ¹⁶O (configurable threshold). ⁸Be excluded from pass/fail.
- **Exit code:** 0 if all asserted nuclei pass; non-zero otherwise (for automation: run → fix → re-run).

---

## 7. Integration with 6π Trefoil and NUCLEAR_STRUCTURE

### 7.1 Data and building blocks

- **NUCLEAR_STRUCTURE:** Set of \((Z, N)\) for Z = 1–50 (and stable isotopes for Z > 50) used in `generate_trefoil_mappings.py` and `add_trefoil_sections_to_atomicus.py`. Building-block decomposition (D = 2Z − N, T = N − Z; alphas, T-units, deuterons) is consistent with the probe’s structural assignments: ²H ↔ 1D, ⁴He ↔ 1α, ¹²C ↔ 3α, ¹⁴N ↔ 3α+1D, ¹⁶O ↔ 4α, ⁸Be ↔ 2α (unstable, may be absent in trefoil list).
- **Shell 2:** For A ≤ 40, alpha clusters are placed at 20 Shell 2 interstices in the trefoil generator; Phase 01 uses the same conceptual geometry (20 triangular face centres). A > 40 uses linear stacking in the trefoil code; the probe restricts to A ≤ 16 for validation.

### 7.2 Velocity constraint (trefoil only)

Three-velocity system: \(v_1 \cdot v_3 = c^2\) (e.g. \(v_1 = 2.23c\), \(v_3 = c^2/v_1 \approx 0.4484c\)). Used in trefoil kinematics and `validate_trefoil_mathematics.py`; **not** used in the binding formula \(B = \kappa_B \cdot \Omega\).

### 7.3 Electron-sharing (context only)

ELECTRON_SHARING_MODEL: deuteron p–p–e, alpha four-way sharing, T-units. These are mechanistic/structural context; the probe’s binding pipeline uses only occlusion and does not include an explicit electron-sharing term in \(\Omega\) or \(\kappa_B\).

---

## 8. Implementation Loci (Summary)

| Component | Primary locus |
|-----------|----------------|
| Icosahedral base, 12 vertices | `Phase_01_Nuclear_Packing/01_01_icosahedral_base_geometry.py` |
| First shell (deuteron, alpha) | `01_02_first_shell_completion.py` |
| Second layer, 20 interstices | `01_03_second_layer_structure.py` |
| C-12 / O-16 / N-14 alpha positions | `01_03_second_layer_structure.py` (Carbon12Arrangement, Oxygen16Arrangement, Nitrogen14Arrangement) |
| Spherical occlusion, overlap correction | `01_05_geometric_calculations.py` |
| Deuteron calibration, \(\kappa_B\) | `Phase_02_Binding_Energy/02_02_deuteron_calibration.py` |
| Alpha internal occlusion | `02_03_alpha_structure.py` |
| Alpha-cluster occlusion, R(n_bonds), ¹⁴N | `02_04_alpha_clusters.py` |
| Validation script | `run_nuclear_stacking_validation.py` |
| Constants and provenance | `NUCLEAR_CONSTANTS.md` |

---

## 9. Known Residuals and Structural Notes

- **¹⁶O:** Can be described as two triangular 3-alpha units (two triples) sharing an edge; the code uses a single tetrahedron (4 alphas, 6 pairs) for overlap correction. The tetrahedron formulation yields a larger \(\Omega_{\mathrm{inter}}\) and fits \(B_{\mathrm{exp}}(^{16}\mathrm{O})\) better than a two-triples occlusion model under the same overlap recipe (see `test_o16_two_triples.py`, `O16_OUTLIER_ANALYSIS.md`).
- **¹⁴N:** Slight underprediction (B_pred < B_exp) due to the extra term \(3 \cdot \mathrm{spherical\_occlusion}(R_{\mathrm{tetra}}, d_{\mathrm{center}})\) being ~1.4% low; see `UNDERPERFORMANCE.md`, `underperformance_diagnostic.py`.
- **⁸Be:** Unstable; excluded from validation pass/fail; building-block count may not appear in trefoil NUCLEAR_STRUCTURE.

---

## 10. References (Internal)

- **NUCLEAR_CONSTANTS.md** — Constants, units, calibration order.
- **COMPREHENSIVE_MATHEMATICAL_ANALYSIS.md** — Proofs of occlusion formula and B–Ω relation; validation summary.
- **TREFOIL_STACKING_INTEGRATION.md** — Trefoil ↔ stacking alignment; how to run both pipelines.
- **6PI_TREFOIL_INTERLEAVED_SPEC.md** — Interleaving rules; A ≤ 40 / A > 40; Shell 2.
- **ELECTRON_SHARING_MODEL.md** — p–p–e, four-way, T-units (mechanistic context).
- **O16_OUTLIER_ANALYSIS.md** — ¹⁶O geometry (tetrahedron vs two triples); mathematical test.
- **UNDERPERFORMANCE.md** — ¹⁴N shortfall and location in code.

---

*(End of Structural and Mechanical Specification)*
