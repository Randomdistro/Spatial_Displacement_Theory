# ULTRAPROMPT: NUCLEI PER NUCLEI — SDT Canonical Nuclear Packing Geometry Document

**Purpose:** This ultraprompt instructs the author (human or AI) to produce the **single canonical** SDT document that defines nuclear packing geometry for all nuclei in the probe (and by extension A ≤ 40 and trefoil-mapped nuclei), using **polar coordinates** and **trefoil structuring** exclusively. The output document must be exhaustive, unambiguous, and implementation-ready.

**Output document title:** *NUCLEI PER NUCLEI: Canonical Nuclear Packing Geometry in Polar Coordinates with Trefoil Structuring*

---

## PART 0: MANDATORY CONSTRAINTS

1. **Coordinate system:** All nucleon and cluster positions MUST be given in **spherical polar coordinates** \((r, \theta, \phi)\) as the **primary** representation. Cartesian \((x,y,z)\) may appear only as derived quantities with an explicit conversion formula. State the convention: e.g. \(r \ge 0\), \(\theta \in [0, 2\pi]\) (azimuthal), \(\phi \in [0, \pi]\) (polar from \(+z\)), with \(x = r\sin\phi\cos\theta\), \(y = r\sin\phi\sin\theta\), \(z = r\cos\phi\) (math convention), OR physics convention if different — and stick to it for the entire document.

2. **Trefoil structuring:** Every nucleus MUST be described in terms of:
   - **Building blocks:** deuteron (D), triton (T), alpha (α), and where applicable tri-alpha, linear chains, or Shell 2 placements.
   - **Chirality:** Each nucleon or each building block MUST be assigned a chirality (L or R) consistent with the 6π trefoil model and with interleaving rules (L–R–L–R for alpha, etc.).
   - **6π trefoil parameters:** Where relevant, state major radius \(R_p\), minor radius \(r = R_p/3\), winding 6π, and the three-velocity system (v₁, v₂, v₃ with v₁·v₃ = c²) as contextual kinematics — and how they constrain or label the geometry (e.g. phase angle for velocity variation).

3. **Single source of truth:** The document must be the **only** place a reader needs to look to recover, for any listed nucleus, (a) polar coordinates of every nucleon or every cluster centre, (b) bond topology (which pairs are bonded, inter-centre distances), (c) observer position(s) for occlusion, (d) arrangement type (dumbbell, triangle, tetrahedron, Shell 2 index, etc.). No “see Phase 01” without reproducing the essential numbers in polar form.

4. **Units and constants:** All lengths in **femtometres (fm)**. All angles in **radians** in equations; degrees may be given in parentheses for readability. Use the constants from NUCLEAR_CONSTANTS.md: \(R_{\mathrm{NUCLEON}} = 0.84\) fm, \(d_{\mathrm{deuteron}} = 2.10\) fm, \(d_\alpha = 1.479\) fm, \(d_{\mathrm{inter}\alpha} = 2.9\) fm, \(R(n_{\mathrm{bonds}})\) with \(R_{\mathrm{base}} = 0.70\) fm and \(\beta = 0.2747\). State κ_B only where binding is quoted; symbol hygiene: κ_B for binding, v/κ_v for velocity.

5. **Occlusion compatibility:** Every geometry MUST be specified so that occlusion can be computed without further choices: observer position(s), list of sphere centres (in polar and optionally Cartesian), sphere radius (per-nucleon \(R_{\mathrm{NUCLEON}}\) or arrangement-specific \(R(n_{\mathrm{bonds}})\)), and bond set for overlap correction. The document must state explicitly which observer is used (e.g. cluster geometric centre) and which radius rule applies to each arrangement.

---

## PART 1: GLOBAL COORDINATE AND CONVENTION SECTION

The output document MUST open with a section that defines:

1. **Origin:** Where is the origin of the coordinate system? (e.g. geometric centre of the cluster, or a designated nucleon, or centre of mass — state which and why.)
2. **Polar convention:** Exact definitions of \(r\), \(\theta\), \(\phi\) and the conversion to Cartesian. Diagram or table: “\(r\) = …, \(\theta\) = …, \(\phi\) = …”.
3. **Handedness:** Right-handed or left-handed system; how \(\theta\) and \(\phi\) increase.
4. **Icosahedral reference (Shell 0):** The 12 vertices of the icosahedral base in polar coordinates \((r, \theta, \phi)\) with \(r = 2 R_{\mathrm{NUCLEON}}\). Provide the full list (e.g. from golden-ratio construction) so that Shell 1 interstices (deuteron, alpha) and Shell 2 (20 triangular interstices) can be derived or referenced. If the document adopts the same Shell 2 list as `generate_trefoil_mappings.py` (SHELL2_INTERSTICES), give that list in polar form with \(R_2 = 2.5\,R_{\mathrm{NUCLEON}}\) and document the source.
5. **First-shell interstices (octahedral):** The two interstitial sites for deuteron and alpha in polar form, and how they relate to the icosahedral vertices (e.g. which octant or face).

---

## PART 2: NUCLEUS-BY-NUCLEUS CANONICAL GEOMETRY

For **each** of the following nuclei, the document MUST contain a dedicated subsection with the following structure. No exceptions.

### Nuclei to cover (minimum)

- **²H (deuteron)**  
- **⁴He (alpha)**  
- **⁸Be (dumbbell)**  
- **¹²C (triangle of three alphas)**  
- **¹⁴N (triangle + centre)**  
- **¹⁶O (tetrahedron of four alphas)**  
- Optionally: **³H, ³He** and any other trefoil-mapped isotopes if the document scope extends to them.

For each nucleus, provide:

#### 2.A Identity and arrangement type

- \((Z, N)\), symbol, name.
- **Arrangement type:** e.g. “single deuteron”, “tetrahedral alpha”, “equilateral triangle of alpha centres”, “tetrahedron of alpha centres”, “dumbbell”, “triangle + central nucleon(s)”.
- **Building-block decomposition:** e.g. “1 D”, “1 α”, “2 α”, “3 α”, “3 α + 1 D” (or “3 α + 1 n”), “4 α”. State how this matches NUCLEAR_STRUCTURE / trefoil building_blocks.

#### 2.B Polar coordinates of every nucleon (or every cluster centre)

- **Primary:** Table or list: nucleon (or cluster) index, type (p/n or “alpha centre”), \((r, \theta, \phi)\) in fm and rad.
- **Derived:** Cartesian \((x, y, z)\) from the stated conversion formula (for verification and occlusion code).
- **Chirality:** For each nucleon, L or R. For alpha clusters, state the chirality pattern of the four constituent nucleons if needed for trefoil consistency (e.g. L–R–L–R).
- If the nucleus is described at **cluster level** (alpha centres only), then separately state the **internal** geometry of each alpha: tetrahedral edge length \(d_\alpha\), centre in polar relative to cluster origin, and the four nucleon positions in polar relative to that alpha centre (or relative to cluster origin). So that a full nucleon-level polar list can be recovered.

#### 2.C Bond topology and distances

- List of bonds: pairs \((i, j)\) and inter-centre distance \(d_{ij}\) in fm. For alpha clusters: internal bonds (six per alpha) and inter-alpha bonds. Verify that inter-alpha distance is \(d_{\mathrm{inter}\alpha} = 2.9\) fm where applicable.
- **Observer for occlusion:** Position of the “observer” (e.g. cluster centre) in polar coordinates. State explicitly: “Observer at \(\mathbf{o} = (r_{\mathrm{obs}}, \theta_{\mathrm{obs}}, \phi_{\mathrm{obs}})\)” or “at origin \((0, 0, 0)\)”.

#### 2.D Occlusion parameters

- **Sphere radius for occlusion:** Per nucleon: \(R = R_{\mathrm{NUCLEON}}\). For inter-alpha occlusion (observer at cluster centre viewing alpha centres as spheres): state \(R = R(n_{\mathrm{bonds}})\) with \(n_{\mathrm{bonds}}\) for this arrangement (1 for dumbbell, 3 for triangle, 6 for tetrahedron) and the numerical value (0.57, 0.70, 0.8923 fm from NUCLEAR_CONSTANTS).
- **Overlap correction:** State that pairwise overlap correction applies, and list which pairs are overlapping (or refer to the bond list). No free parameters beyond the constants already given.

#### 2.E Trefoil-specific data (where applicable)

- **Phase angle:** For each nucleon, the phase angle (rad) used in the three-velocity system (v₁, v₂, v₃) if the document includes kinematics.
- **Internal electrons (electron-sharing):** For ¹⁴N and other multi-proton systems, state which nucleons share an internal electron (p–p–e, four-way, etc.) and the position of the mediation point in polar coordinates if specified in the trefoil model.
- **Nuclear rotation axis and frequency:** If the document includes rotation, give axis direction (polar angles) and frequency (rad/s) from trefoil constants.

#### 2.F Cross-references and validation

- **Binding:** \(B_{\mathrm{pred}} = \kappa_B \cdot \Omega_{\mathrm{total}}\) with \(\Omega_{\mathrm{total}}\) from the geometry above. Give \(\Omega_{\mathrm{total}}\) (sr) and \(B_{\mathrm{pred}}\) (MeV) and \(B_{\mathrm{exp}}\) (MeV) for validation.
- **Code loci:** Reference the implementation that produces this geometry (e.g. `01_02_first_shell_completion.py`, `02_04_alpha_clusters.py`, `generate_trefoil_mappings.py`) and note any intentional differences (e.g. trefoil alpha at Shell 2 vs Phase 01 triangle/tetrahedron).

---

## PART 3: SHELL 2 AND ICOSAHEDRAL GEOMETRY IN POLAR FORM

The document MUST include a dedicated section that gives:

1. **Icosahedral vertices (Shell 0):** Full set of 12 points in \((r, \theta, \phi)\) with \(r = 2 R_{\mathrm{NUCLEON}}\). Derivation from golden ratio or standard icosahedron construction. Symmetry group / equivalence classes if helpful.

2. **Shell 1 interstices (octahedral):** The two interstitial positions (deuteron and alpha sites) in polar form. How they are computed from the icosahedron (e.g. face centres or edge midpoints of a dual).

3. **Shell 2 (20 triangular interstices):** The 20 positions in polar coordinates \((R_2, \theta_i, \phi_i)\) with \(R_2 = 2.5\,R_{\mathrm{NUCLEON}}\) (or the value from NUCLEAR_CONSTANTS / generate_trefoil_mappings). Provide the full table: index \(i \in 0..19\), \((\theta_i, \phi_i)\) in rad, and optionally \((x_i, y_i, z_i)\) in fm. State that these are the centroids of the 20 triangular faces of the icosahedron (or the adopted convention). This is the canonical list for “Shell 2” placement of alpha clusters in A ≤ 40 and for trefoil mapping.

4. **Mapping from arrangement to Shell 2 indices:** For nuclei that use Shell 2 (e.g. beyond ¹⁶O), state which Shell 2 indices are occupied by which building blocks (e.g. “indices 0, 1, 2 for the three alpha centres of ¹²C equivalent”) and how that aligns or differs from the Phase 01 triangle/tetrahedron (which may use Cartesian 2.9 fm spacing rather than Shell 2 radii).

---

## PART 4: TRFOIL PARAMETERS AND KINEMATICS (CONSOLIDATED)

A single section MUST collect all trefoil-related numbers so that no reader has to hunt through the nucleus-by-nucleus sections:

1. **6π trefoil:** Major radius \(R_p = 0.84\) fm, minor radius \(r = R_p/3\), winding 6π, compactness κ_p (value and formula). Source: TREFoil_NUCLEAR_STRUCTURE_MAPPING.md.

2. **Three-velocity system:** v₁ = 2.23c, v₂ = 1.84c, v₃ = c²/v₁ ≈ 0.4484c. Constraint v₁·v₃ = c². Which velocity applies to which geometric locus (perihelion, rim, aphelion).

3. **Rotation:** Proton rotation frequency (rad/s). How phase angle maps to velocity at each nucleon.

4. **Chirality and interleaving:** Rules for assigning L/R to nucleons in deuteron, alpha, and larger clusters. L–R–L–R for alpha; how tri-alpha and triangle+centre are assigned.

5. **Electron-sharing model:** p–p–e for deuteron pair in neutron, four-way for alpha, T-units. Reference ELECTRON_SHARING_MODEL and how it ties to positions (no new free parameters; positions already given in Part 2).

---

## PART 5: FORMULAE AND ALGORITHMS

The document MUST state explicitly, with equation numbers:

1. **Spherical occlusion:** \(\Omega(R, d) = 2\pi(1 - \cos\theta)\), \(\sin\theta = R/d\), \(\cos\theta = \sqrt{1 - (R/d)^2}\), edge cases \(d \le 0\), \(d < R\), \(d = R\), clamp to \([0, 4\pi]\).

2. **Polar to Cartesian:** \(x = r\sin\phi\cos\theta\), \(y = r\sin\phi\sin\theta\), \(z = r\cos\phi\) (or the chosen convention) with a clear “convention box”.

3. **Overlap correction:** Verbal or symbolic description of pairwise overlap: uncorrected sum \(\sum_i \Omega_i\), overlap term for pair \((i,j)\) when \(d_{ij} < 2R\), corrected total \(\Omega_{\mathrm{corr}} = \mathrm{clamp}(\sum_i \Omega_i - \sum_{i<j} \text{overlap}_{ij})\). Reference 01_05_geometric_calculations.corrected_total_occlusion.

4. **Inter-alpha radius:** \(R(n_{\mathrm{bonds}}) = R_{\mathrm{base}}(1 + \beta(n_{\mathrm{bonds}} - 3)/3)\) with \(R_{\mathrm{base}} = 0.70\) fm, \(\beta = 0.2747\). Table: \(n_{\mathrm{bonds}} = 1, 3, 6\) → R in fm.

5. **Alpha internal geometry:** Tetrahedron edge \(d_\alpha = 1.479\) fm; centre-to-vertex \(d_\alpha\sqrt{3/8}\); effective alpha radius for inter-alpha occlusion \(R_\alpha = d_\alpha\sqrt{3/8} + R_{\mathrm{NUCLEON}}\). In polar: if alpha centre is at \((r_c, \theta_c, \phi_c)\), the four nucleon positions relative to centre (local Cartesian or polar) and then converted to global polar.

---

## PART 6: TABLES AND INDICES

1. **Master table (nuclei):** One table listing every nucleus covered: Z, N, symbol, arrangement type, building blocks, number of nucleons, observer position (polar), \(R\) used for occlusion, \(\Omega_{\mathrm{total}}\) (sr), \(B_{\mathrm{pred}}\) (MeV), \(B_{\mathrm{exp}}\) (MeV), reference to subsection (e.g. §2.3).

2. **Master table (Shell 2):** Index 0..19, \((\theta, \phi)\) in rad, \((x, y, z)\) in fm, and optionally which standard nuclei (if any) use this index in the current document.

3. **Constants index:** Single table of every named constant used: symbol, value, unit, meaning, source (NUCLEAR_CONSTANTS.md or this document).

---

## PART 7: IMPLEMENTATION AND CONSISTENCY NOTES

1. **Phase 01 vs trefoil:** State where the canonical geometry agrees with Phase 01 (01_01, 01_02, 01_03) and where it agrees with generate_trefoil_mappings.py. Document any known discrepancy (e.g. alpha internal 1.45 fm vs 1.479 fm, or Shell 2 radius vs 2.9 fm triangle side) and which value the present document adopts as canonical.

2. **Occlusion pipeline:** Short “recipe”: given nucleus (Z,N), (1) look up arrangement and building blocks, (2) get all nucleon or cluster positions in polar, (3) convert to Cartesian if needed, (4) set observer, (5) set R (per-nucleon or \(R(n_{\mathrm{bonds}})\)), (6) compute \(\Omega_{\mathrm{total}}\) with overlap correction, (7) \(B_{\mathrm{pred}} = \kappa_B \cdot \Omega_{\mathrm{total}}\). No steps left implicit.

3. **Extensibility:** For nuclei not explicitly listed (e.g. A > 40 or exotic), state the rule: e.g. “Use Shell 2 polar list for cluster centres; building blocks from NUCLEAR_STRUCTURE; observer at geometric centre; R from \(R(n_{\mathrm{bonds}})\) or from arrangement type.”

---

## PART 8: DOCUMENT METADATA AND REVISION

The output document MUST end with:

- **Version and date.**  
- **Author/source:** “Generated per NUCLEI_PER_NUCLEI_ULTRAPROMPT.”  
- **References:** STRUCTURAL_AND_MECHANICAL_SPECIFICATION.md, NUCLEAR_CONSTANTS.md, TREFoil_NUCLEAR_STRUCTURE_MAPPING.md, TREFOIL_STACKING_INTEGRATION.md, SDT_COMPILER_SPEC_v0.9.md (for κ_B and symbols), generate_trefoil_mappings.py, Phase_01_Nuclear_Packing scripts, 02_04_alpha_clusters.py.  
- **Revision history:** Table (date, change).  
- **Certification:** “This document is the canonical nuclear packing geometry for SDT nuclear structure probe. All polar coordinates and trefoil structuring are defined here or by reference to the formulae and constants above; no geometry is left to implementation choice.”

---

## PART 9: TONE AND EXHAUSTION CRITERIA

- **Excessively detailed** means: a competent implementer can write code (or check numbers by hand) without guessing. Every position, every radius, every convention appears explicitly or by a unique reference to a formula/table in this document.
- **Polar coordinates** means: no “see Phase 01 for coordinates” without also giving the polar form in this document. Cartesian may be derived; polar is primary.
- **Trefoil structuring** means: every nucleus is labeled with building blocks, chirality, and (where used) phase and velocity context; the 6π trefoil and Shell 2 are defined in polar and tied to the same coordinate system.
- **Ultraprompt compliance:** If any subsection above is skipped or shortened, the output document must state “Intentionally omitted: [section]; reason: …” so that the omission is visible and reviewable.

---

*End of ultraprompt. The resulting document is NUCLEI PER NUCLEI: Canonical Nuclear Packing Geometry in Polar Coordinates with Trefoil Structuring.*
