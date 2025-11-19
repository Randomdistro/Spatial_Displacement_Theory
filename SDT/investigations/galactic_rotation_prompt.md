# Galactic Rotation Investigation Prompt

*Disk eclipse saturation mechanism for flat rotation curves*

**Status:** Under development  
**Last Updated:** November 2025

---

## Objective

Validate SDT prediction that flat galactic rotation curves arise from disk eclipse saturation, not dark matter.

---

## Key Prediction

For disk geometry, the directional occlusion function E(r) becomes radius-invariant at large r, producing constant acceleration:

**a(r) ∝ 1/r** → **v(r) = constant**

**Test:** R_flat should correlate with disk scale length R_d as:

**R_flat ≈ 2.5 R_d**

---

## Investigation Steps

1. **Calculate E(r) for disk geometry**
   - Directional occlusion function
   - Pressure gradient from occlusion
   - Rotation velocity v(r)

2. **Compare to SPARC database**
   - Extract R_d and R_flat for each galaxy
   - Test R_flat/R_d ≈ 2.5 correlation
   - Analyze scatter and systematic trends

3. **Compare to dark matter models**
   - SDT predictions vs. NFW halo fits
   - Statistical significance of differences

---

## Data Sources

- SPARC database (Spitzer Photometry & Accurate Rotation Curves)
- `data/galaxy_rotation_sparc.csv` (under development)

---

## Related Documents

- `Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/Phase_24_Galactic_Rotation_Curves_Disk_Eclipse_Saturation.md`
- `Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/Phase_25_Flat_Galactic_Rotation_Curves_from_Disk_Eclipse_Saturation.md`
- `Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/Phase_Y_Galactic_Dynamics_Rotation_Curves_from_Displacement_and_Occlusion.md`

---

## Falsification Criteria

If R_flat/R_d shows no correlation or differs systematically from 2.5, the disk eclipse saturation hypothesis fails.

---

*This investigation is ongoing. Results will be documented in Part IV: Certified Benchmarks.*

