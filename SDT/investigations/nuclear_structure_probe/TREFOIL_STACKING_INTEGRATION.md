# Trefoil Model Applied to Nuclear Stacking (Binding) Solution

This document applies the **6π Trefoil** implementation (velocity constraint, electron-sharing, Shell 2 geometry, NUCLEAR_STRUCTURE) to the **nuclear stacking validation** and Phase 01/02 binding pipeline.

---

## 1. Alignment Summary

| Trefoil (Code/) | Stacking (probe) | Alignment |
|-----------------|------------------|-----------|
| **v₁·v₃ = c²** | Not used in B = κ_B·Ω | Velocity constraint is trefoil kinematics; binding formula uses occlusion only. Optional: document v₁, v₃ in probe as context. |
| **NUCLEAR_STRUCTURE (Z,N)** | 02_04 nuclei (2H, 4He, 12C, 14N, 16O, 8Be) | Same (Z,N); trefoil uses D–T decomposition and Shell 2 placement; probe uses same building blocks (deuteron, alpha, triangle, tetrahedron). |
| **Shell 2 (20 interstices)** | Phase 01 `SecondLayer` (20 triangular interstices) | Same concept (icosahedral face centers). Trefoil: `SHELL2_INTERSTICES` (θ, φ) in generate_trefoil_mappings.py; Phase 01: computed from icosahedral faces in 01_03. For A ≤ 40 both use icosahedral/shell placement. |
| **A ≤ 40 vs A > 40** | Probe validates A ≤ 16 (2H–16O, 8Be) | Subset of A ≤ 40; same rule: shell-based geometry. |
| **Electron-sharing** | Not in B = κ_B·Ω | ELECTRON_SHARING_MODEL (p–p–e, four-way, T-units) is mechanistic context; binding pipeline uses occlusion only. `internal_electrons` / `shared_with` in trefoil JSON can be referenced for future coupling. |
| **Constants** | Phase 02 | Same: R_NUCLEON_FM 0.84 fm, DIST_DEUTERON_FM 2.10 fm, DIST_ALPHA_FM 1.45 fm, DIST_INTER_ALPHA_FM 2.9 fm. |

---

## 2. Building-Block Mapping (Validation Nuclei)

From **NUCLEAR_STRUCTURE** / **trefoil_mappings.json**:

| Nucleus | Z | N | Trefoil building_blocks | Probe model |
|---------|---|---|--------------------------|-------------|
| ²H | 1 | 1 | 1D | DeuteronCalibration (p–n, occlusion) |
| ⁴He | 2 | 2 | 1alpha | AlphaParticleStructure (tetrahedral, 6 bonds) |
| ¹²C | 6 | 6 | 3alpha | Carbon12Structure (triangle, 3 alphas) |
| ¹⁴N | 7 | 7 | 3alpha+1D | nitrogen14_occlusion(C12 + center nucleon extra) |
| ¹⁶O | 8 | 8 | 4alpha | Oxygen16Structure (tetrahedron, 4 alphas) |
| ⁸Be | 4 | 4 | 2alpha (unstable) | Beryllium8Structure (dumbbell) |

The probe does **not** use T-units explicitly for ¹⁴N (models 3α + center nucleon pair instead of 3α+1D); binding is structural (occlusion) and matches NUCLEAR_STRUCTURE (Z,N) and trefoil block list.

---

## 3. How to Run Trefoil and Stacking Together

1. **Regenerate trefoil data (sync with NUCLEAR_STRUCTURE):**
   ```bash
   cd SDT/Code
   python generate_trefoil_mappings.py
   ```
   Outputs: `SDT/data/trefoil_mappings.json`, `SDT/website/src/data/trefoilStructures.ts`.

2. **Validate trefoil mathematics:**
   ```bash
   cd SDT/Code
   python validate_trefoil_mathematics.py
   ```
   Checks: v₁·v₃ = c², rotation frequency, chirality, nuclear rotation. (Alpha geometry check expects internal 1.45 fm; trefoil alpha at Shell 2 uses 2.9 fm edge in current generator—documented discrepancy.)

3. **Run nuclear stacking validation (binding):**
   ```bash
   cd SDT/investigations/nuclear_structure_probe
   python run_nuclear_stacking_validation.py
   ```
   Asserts B_pred vs B_exp for 2H, 4He, 12C, 14N, 16O; 8Be informational.

4. **Optional: compare building blocks**
   ```bash
   cd SDT/investigations/nuclear_structure_probe
   python trefoil_stacking_compare.py
   ```
   (Script below: loads trefoil_mappings.json and prints building_blocks for validation nuclei.)

---

## 4. Constants Shared Between Trefoil and Stacking

- **R_NUCLEON_FM** = 0.84 fm  
- **DIST_DEUTERON_FM** = 2.10 fm  
- **DIST_ALPHA_FM** = 1.45 fm (compressed alpha; trefoil alpha tetrahedron edge in generator may use 2.9 fm for placement)  
- **DIST_INTER_ALPHA_FM** = 2.9 fm  

Single source of truth for these in the probe: Phase 02 modules and NUCLEAR_CONSTANTS.md. Trefoil: generate_trefoil_mappings.py.

---

## 5. References

- **6PI_TREFOIL_INTERLEAVED_SPEC.md** (probe): Interleaving rules; A ≤ 40 Shell 2; A > 40 linear.
- **ELECTRON_SHARING_MODEL.md** (probe): p–p–e, four-way, T-units; binding mechanism context.
- **NUCLEAR_PACKING_STRUCTURE_AND_DATA.md** (Papers/…/05_Chemistry): Shell 1/2, 20 interstices.
- **generate_trefoil_mappings.py** (Code): NUCLEAR_STRUCTURE, Shell 2 interstices, velocity constraint, internal_electrons.
- **add_trefoil_sections_to_atomicus.py** (Code): (Z,N) and STABLE_ISOTOPE_N lookup for ATOMICUS.
- **run_nuclear_stacking_validation.py** (probe): Binding assertions; exit code for automation.
