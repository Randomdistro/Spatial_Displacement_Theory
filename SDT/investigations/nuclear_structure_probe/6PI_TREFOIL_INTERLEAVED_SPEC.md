# 6π Trefoil Interleaved Nuclear Structure Specification

**Status:** Specification  
**Version:** 1.0  
**Related:** ELECTRON_SHARING_MODEL.md, NUCLEAR_PACKING_STRUCTURE_AND_DATA.md, D-01

---

## 1. Overview

Nuclei are modelled as **interleaved 6π trefoils** where each nucleon (proton or neutron) is a 6π winding torus. The neutron's internal electron is explicitly shared with adjacent protons (neutron→proton mediation). Geometry accounts for binding energies, exchanges, and anomalies.

---

## 2. 6π Trefoil per Nucleon

**Proton:**
- 6π winding torus (R_p ≈ 0.84 fm, minor radius r = R_p/3)
- Riemann surface topology
- Unpaired electron available for external bonding (atomic shell)

**Neutron:**
- Same 6π trefoil as proton
- **Nestled electron:** n = p⁺ + e⁻_internal (SDT composite)
- Internal electron bound at trefoil node; r_node ≈ 0.25 fm
- Electron **shared with adjacent protons** for nuclear binding

---

## 3. Interleaving (Meshing) Rules

**Definition:** Adjacent trefoils **mesh** rather than stack. Internal electron vortices synchronize; "donut holes" align for electron-sharing paths.

1. **Deuterons:** When two deuterons collide to form an alpha, they **interlock**. L–R chirality alternates (L–R–L–R) for tetrahedral stability.
2. **Alpha clusters:** Place alphas at shell interstices (triangular, tetrahedral, octahedral) so adjacent trefoils interlock. Target geometry is icosahedral/shell-based for A ≤ 40.
3. **T-units:** Bridge alphas at inter-alpha vertices or interstices.
4. **Orientation:** Adjacent trefoils oriented so flux-line crossing is maximized for electron-sharing paths.

---

## 4. Neutron-to-Proton Electron Sharing

**Deuteron (p–p–e):**
- 1 internal electron (from neutron) mediates between both protons
- Electron at gap center; D − d_p ≈ 0.26 fm
- E_bind ≈ 3 k_e e²/D ≈ 2.22 MeV (D-01)

**Alpha (four-way):**
- 2 internal electrons (one per neutron) weave between all 4 protons
- Tetrahedral L–R–L–R chirality
- E_bind ≈ 28.3 MeV

**T-units:**
- 1 internal electron per T-unit (1p + 2n)
- Mediates between that T's nucleons and adjacent alphas

---

## 5. Link to Binding

| System | Binding | Mechanism |
|--------|---------|-----------|
| Deuteron | ~2.22 MeV | p–p–e; shared electron pressure well |
| Alpha | ~28.3 MeV | Four-way electron sharing + tetrahedral lock |
| Heavy nuclei | D–T decomposition | Shared-electron mediation + occlusion |

---

## 6. Architecture Summary

```
Proton (6π) → Deuteron (L–R p–n, 1e shared) → Alpha (2D mesh, 2e four-way)
     → T-units (1e per T) → Heavier nuclei (interleaved alphas + T)
```

---

## 7. Geometry Implementation

**A ≤ 40:** Alpha clusters placed at Shell 2 triangular interstices (20 positions from icosahedral faces). T-units at inter-alpha bridges or remaining interstices. See NUCLEAR_PACKING_STRUCTURE_AND_DATA.md for (r, θ, φ) coordinates.

**A > 40:** Linear alpha stacking used as approximation; shell layers + Fibonacci or similar for remainder may be documented in future. Full icosahedral placement for heavy nuclei is an open investigation.

---

## 8. Cross-References

- **ELECTRON_SHARING_MODEL.md:** Deuteron, alpha, T-unit rules; E_bind formulas
- **NUCLEAR_PACKING_STRUCTURE_AND_DATA.md:** Interleaving geometry; Shell 1/2 coordinates
- **SDT_CORE_AXIOMS §2.1–2.2:** Neutron composite; deuteron bond
- **D-01:** Deuteron certification
- **trefoil_mappings.json:** Nucleon positions, internal_electrons, shared_with
- **generate_trefoil_mappings.py:** Implementation; icosahedral placement for A ≤ 40
- **TREFOIL_STACKING_INTEGRATION.md:** Application of trefoil model to nuclear stacking (binding) solution; alignment of NUCLEAR_STRUCTURE, Shell 2, and run_nuclear_stacking_validation

---

*(End of 6PI_TREFOIL_INTERLEAVED_SPEC.md)*
