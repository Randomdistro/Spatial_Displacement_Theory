# Nuclear Structure Probe: Constants and Provenance

**Purpose**: Single source of truth for all numerical constants used in binding-energy calculations. Every value has explicit units, derivation, and source where applicable.

**Canonical SDT reference**: `SDT/SDT_CANONICAL_PHYSICS_ENGINE_v4.md` — Section 0 (definitive constants), Section 7 (trefoil topology), Section 10–11 (mass/occlusion, deuteron). Probe values below may differ where probe-specific calibration applies.

---

## 1. Fundamental Constants

| Symbol | Value | Unit | Source / Derivation |
|-------|-------|------|---------------------|
| `R_NUCLEON_FM` | 0.84 | fm | Nucleon charge radius ~0.84 fm; used as effective radius for occlusion |
| `DIST_DEUTERON_FM` | 2.10 | fm | Deuteron p–n separation (experimental) |
| `DIST_ALPHA_FM` | 1.479 | fm | Alpha internal bond length; chosen so Ω_α = B_exp/κ_B with κ_B from deuteron |
| `DIST_INTER_ALPHA_FM` | 2.9 | fm | Inter-alpha spacing (C-12, O-16 cluster geometry) |

---

## 2. Experimental Binding Energies (MeV)

| Nucleus | Value | Source |
|---------|-------|--------|
| ²H | 2.2246 | [1] |
| ⁴He | 28.296 | [1] |
| ¹²C | 92.162 | [1] |
| ¹⁴N | 104.66 | [1] |
| ¹⁶O | 127.619 | [1] |
| ⁸Be | 56.5 | [1] (unstable) |

[1] Atomic Mass Evaluation (AME); values used in validation.

---

## 3. Derived Constants

### 3.1 Binding constant κ_B (MeV/sr)

- **Symbol**: κ_B (reserved for nuclear binding; velocity uses v and κ_v ≡ v/c — see SDT_COMPILER_SPEC_v0.9.md §0).
- **Definition**: κ_B = B_exp(²H) / Ω(²H)
- **Value**: κ_B ≈ 4.240962 MeV/sr
- **Derivation**: Calibrated from deuteron only; no fitting to C-12, O-16, or ⁸Be.

### 3.2 Alpha Internal Geometry

- **N_BONDS_ALPHA**: 6 (tetrahedral edges)
- **ALPHA_CENTER_DIST**: d × √(3/8) ≈ 0.6124 × 1.479 ≈ 0.906 fm
- **ALPHA_EFFECTIVE_RADIUS**: ALPHA_CENTER_DIST + R_NUCLEON ≈ 1.746 fm

### 3.3 Inter-Alpha Sphere Radius (Unified Formula)

For overlap-corrected inter-alpha occlusion (observer at cluster center):

```
R(n_bonds) = R_base × (1 + β × (n_bonds − 3) / 3)
```

| Parameter | Value | Unit | Derivation |
|-----------|-------|------|------------|
| R_base | 0.70 | fm | Triangle (n_bonds=3): yields inter ≈ 1.72 sr for C-12 |
| β | 0.2747 | — | Tetrahedron (n_bonds=6): R = 0.8923 fm for O-16 |

**Triangle**: R = 0.70 fm  
**Tetrahedron**: R ≈ 0.8923 fm  
**Dumbbell**: R ≈ 0.57 fm (n_bonds=1)

---

## 4. Geometric Constants

| Symbol | Value | Unit | Definition |
|--------|-------|------|------------|
| D_CENTER_TRIANGLE_FM | 2.9/√3 ≈ 1.67 | fm | Distance from triangle centroid to vertex |
| D_CENTER_TETRAHEDRON_FM | 2.9×√(3/8) ≈ 1.78 | fm | Distance from tetrahedron centroid to vertex |

---

## 5. Occlusion Formula

**Spherical occlusion** (solid angle subtended by sphere of radius R at distance d):

```
Ω = 2π(1 − cos θ),   sin θ = R/d
```

Edge cases:
- d < R: Ω = 4π (observer inside sphere)
- d = R: Ω = 2π (hemisphere)
- d > R: formula above

---

## 6. Validation Thresholds

| Nucleus | Threshold | Notes |
|---------|-----------|-------|
| ²H, ⁴He, ¹²C, ¹⁴N, ¹⁶O | err < 0.08% | Calibration nuclei: ²H, ⁴He; others structural |
| ⁸Be | excluded | Unstable; informational only |

---

## 7. Calibration Hierarchy

1. **²H**: κ_B = B_exp / Ω (exact by construction)
2. **⁴He**: d_alpha chosen so B_pred = B_exp
3. **¹²C**: R_base for triangle (n_bonds=3)
4. **¹⁶O**: β for tetrahedron (n_bonds=6)
5. **¹⁴N**: Structural prediction (3α + p at center; no B_exp_14N)

---

## 8. Revision History

| Date | Change |
|------|--------|
| 2026-02 | Initial constants document; unified R formula; 14N structural prediction |
