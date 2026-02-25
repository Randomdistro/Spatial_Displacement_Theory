# Why Oxygen-16 Is the Binding Outlier

## Summary

¹⁶O is the only alpha-cluster nucleus in validation that shows a non-zero error (~4.6% under-prediction: B_pred ≈ 121.7 MeV vs B_exp = 127.6 MeV). The cause is **geometric**, not Lamb shift or absorption shift in the current model.

---

## 1. Structural (Geometric) Reason

**Oxygen is two triples.** ¹⁶O is 4 alphas arranged as **two triangular (3-alpha) units**—not a single tetrahedron as the sole description. C-12 is one triple (one triangle); structurally ¹⁶O = 2×(triangle) with a shared link. The code currently models ¹⁶O as one tetrahedron (6 bonds, 6 pairs for overlap).

- **C-12**: 1 triple → 3 alphas in a **triangle** → 3 inter-alpha bonds, 3 pairs of spheres.
- **¹⁶O**: 2 triples → 4 alphas; in the code, **tetrahedron** → 6 inter-alpha bonds, **6 pairs** of spheres.

The overlap correction in `01_05_geometric_calculations.corrected_total_occlusion()` subtracts pairwise overlaps from the total occlusion seen from the cluster center. So:

- For the **triangle**, we subtract overlap for **3 pairs** of alpha spheres.
- For the **tetrahedron**, we subtract overlap for **6 pairs**.

The same overlap model therefore **reduces the inter-alpha occlusion more for the tetrahedron** than for the triangle. The scale is calibrated from C-12 (so C-12 is exact). As a result, ¹⁶O gets a **smaller** effective total Ω than would be needed to match B_exp, so we **under-predict** binding for oxygen. So the outlier is explained by **tetrahedron vs triangle geometry**—and by modeling O-16 as one 4-alpha body instead of two 3-alpha triples: more pairwise overlaps in the tetrahedron view → stronger overlap correction → lower Ω and lower B_pred for O-16.

(If we had calibrated from O-16 instead, C-12 would then appear as the outlier in the opposite direction.)

---

## 1b. Mathematical test (tetrahedron vs two triples)

A **numerical test** compares the two formulations on the same geometry and constants. Script: **`test_o16_two_triples.py`** (probe root).

- **Model A — One tetrahedron:** Observer at geometric center of all 4 alphas; inter-alpha occlusion = `corrected_total_occlusion(center, positions_4, R_tetrahedron)`. Same as current O-16 path in 02_04 when using arrangement-specific R.
- **Model B — Two triples:** Triple 1 = alphas (0,1,2), triple 2 = alphas (0,1,3) (shared edge 0–1). Omega_inter = Omega_triple1 + Omega_triple2 − Omega_shared, with each triple’s occlusion from its own center and R_triangle. Shared alphas (0,1) subtracted once.

**Result (run on same k, same internal occlusion, same 01_05 overlap correction):**

| Model           | Omega_inter (sr) | B_pred (MeV) | Error vs B_exp |
|-----------------|-------------------|--------------|----------------|
| A: Tetrahedron  | 3.40              | 127.59       | **0.03%**      |
| B: Two triples  | 2.30              | 122.92       | 3.68%          |

So **mathematically**, with the same overlap correction and constants, the **tetrahedron** formulation gives a **larger** inter-alpha occlusion and fits B_exp(O-16) = 127.619 MeV much better than the two-triples formulation (which under-predicts by ~3.7%). The “oxygen is two triples” description is structurally valid (4 alphas = two triangular units sharing an edge), but the **occlusion formula** that uses one tetrahedron and R_tetrahedron currently outperforms the formula that uses two triangle occlusions (R_triangle) with shared-edge subtraction. To make the two-triples model match B_exp, one would need a different R, a different overlap rule, or an extra binding term for the link between the two triples.

---

## 2. Lamb Shift and Absorption Shift

### Lamb shift (SDT / standard physics)

- In SDT and in standard QED, the **Lamb shift** is an **atomic** effect: the 2s–2p level shift in hydrogen (and similar ions) from radiative/self-energy and electron–vacuum interaction at the Compton scale (≈ α⁵, small relative to binding).
- It is **not** implemented or invoked in the **nuclear** binding probe. The nuclear model uses occlusion (solid angle) and deuteron/alpha calibration only; there is no Lamb-shift term in the binding formula.

### “Inverse Lamb shift”

- An “inverse Lamb shift” in the nuclear context would mean some **small level- or binding-energy shift** analogous to the atomic Lamb shift but for nucleons or alpha clusters. The codebase does **not** implement or reference such an effect. If one were to add it, it would be a new theoretical ingredient (e.g. a small correction that could depend on Z, N, or shell closure).

### Absorption shift

- In SDT and in standard spectroscopy, **absorption** and “absorption shift” refer to **optical/electronic** processes: resonant absorption, linewidth, index, pressure shift of spectral lines. They are **electron–photon** or **matter–field** effects, not part of the current **nuclear binding** calculation.
- The nuclear stacking validation uses **binding energies** (B_exp, B_pred) and occlusion only; there is no absorption or line-shift term.

So in the **current** implementation:

- The O-16 outlier is **not** attributed to the Lamb shift or to an absorption shift.
- It is attributed to **geometry**: tetrahedron (6 pairs) vs triangle (3 pairs) and the resulting stronger overlap correction for ¹⁶O.

If the operator wants to **hypothesize** that an “inverse Lamb” or “absorption-like” shift adds a few percent binding specifically for ¹⁶O (e.g. closed-shell effect, or an electromagnetic correction), that would be a separate theoretical step and would need to be formulated and tested outside the current occlusion-only model.

---

## 3. Possible Next Steps (Optional)

- **Refine overlap model**: Make the overlap correction arrangement-dependent (e.g. different effective radius or formula for tetrahedron vs triangle) so that both C-12 and O-16 are fitted without forcing O-16 to be an outlier.
- **Theoretical**: Formulate an “inverse Lamb” or absorption-related **nuclear** binding correction and check whether it correlates with ¹⁶O (or other closed-shell nuclei) and improves B_pred.
