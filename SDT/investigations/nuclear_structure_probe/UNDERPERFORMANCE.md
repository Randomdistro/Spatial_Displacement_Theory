# Underperformance (B_pred < B_exp)

**Current underperformer:** **14N** only.

| Nucleus | B_exp (MeV) | B_pred (MeV) | Shortfall | Location |
|---------|-------------|--------------|-----------|----------|
| 14N     | 104.660     | 104.486      | 0.17 MeV (0.17%) | `nitrogen14_occlusion()` |

## Where it comes from

- **Function:** `nitrogen14_occlusion(c12_total_occlusion)` in **`Phase_02_Binding_Energy/02_04_alpha_clusters.py`**.
- **Formula:** Omega_14N = C12_total + **extra**, with  
  **extra** = 3 × spherical_occlusion(R_tetra, d_center).  
  (Center nucleon views 3 alphas; R_tetra = tetrahedron inter-alpha radius, d_center = 2.9/√3 fm.)
- **Cause:** The **extra** term is ~1.41% too small, so total Omega_14N is slightly low and B_pred falls short of B_exp by ~0.04 sr in occlusion (~0.17 MeV).

## How to reproduce

Run:

```bash
python underperformance_diagnostic.py
```

for the exact shortfall (MeV and sr) and the required increase on the extra term.

## Possible fixes

- Slightly increase the center–alpha contribution (e.g. scale extra by ~1.014, or reduce d_center / increase R for the center view), or
- Add a small structural term for the nucleon pair at the triangle center, or
- Revisit the distance/radius used for the center nucleon (d_center, R_tetra) from Phase 01 geometry.
