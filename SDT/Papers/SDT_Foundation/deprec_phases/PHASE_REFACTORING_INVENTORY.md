# Deprecated Phases Refactoring Inventory

## Status Tracking

### Phase 1.1: Complete File Inventory
**Total Files:** 41
**Status:** ✓ Complete

### Categorization

**Atomic Physics:**
- Phase_2_Rydberg_Spectrum_from_Helical_Standing_Waves.md
- Phase_3_Fine_structure.md
- Phase_4_Lamb_Shift.md
- Phase_6_Multi_Electron_Atoms_from_Occlusion_Geometry.md
- Phase_23_Atomic_Structure_from_Vortex_Geometry.md
- Phase_27A_Foundation_and_Single_Electron_Systems.md
- Phase_27B_Multi_Electron_Occlusion_Mechanics.md
- Phase_27C_Spectral_Calibration_and_k_Values.md

**Nuclear Physics:**
- Phase_17_Toroidal_Structures_and_Pressure_Differentials_at_Femtoscale.md
- Phase_18_Alpha_Particles_and_Beta_Decay.md
- Phase_19_The_Role_of_the_Vortex_and_the_Effect_of_the_Helical_Wake.md

**Gravitational/Stellar:**
- Phase_15_Gravitation_from_Spation_Pressure_Gradients.md
- Phase_15_Gravitation_from_Spation_Pressure_Gradients_PROFESSIONAL.md
- Phase_16_Universal_c-Boundary_Geometry.md
- Phase_22_Exoplanetary_Systems_Deriving_Orbital_Dynamics_from_Stellar_Compactness_and_Luminosity.md
- Phase_22_Validation_10_Star_Systems.md
- Phase_Y_Galactic_Dynamics_Rotation_Curves_from_Displacement_and_Occlusion.md
- Phase_24_Galactic_Rotation_Curves_Disk_Eclipse_Saturation.md
- Phase_25_Flat_Galactic_Rotation_Curves_from_Disk_Eclipse_Saturation.md
- Phase_25_Pressure_Differentials_Across_Scales.md

**Electromagnetic:**
- Phase_1_Coulomb_Force.md
- Phase_1_Coulomb_Force_PROFESSIONAL.md
- Phase_5_Hyperfine_Splitting_from_Central_Pressure_Overlap.md
- Phase_8_Hyperfine_Structure_from_Magnetic_Moment_Overlap.md
- Phase_10_Electromagnetic_Mechanisms_and_Effects.md
- Phase_11_Electricity_from_Spation_Pressure_Deformation.md
- Phase_12_Electromagnetic_Mechanisms_and_Effects.md

**Thermodynamic:**
- Phase_7_Thermodynamics_from_Spation_Contact_Mechanics.md
- Phase_14_Thermodynamic_and_Radiative_Transitions.md

**Planetary/Orbital:**
- Phase_9_Oblateness-Spin_Correlation.md

**Foundational/Organizational:**
- Phase_0_Foundational_Principles.md
- Phase_0_Part1_Space_Matter.md
- Phase_0_Part2_Movement_Now_Derivations.md
- Phase_0_Part3_Orbits_Thermodynamics.md
- Phase_0_Part4_Validation_Philosophy.md
- Phase_0_COORDINATION.md
- Phase_0_PARALLEL_WORK_PLAN.md

**Supporting/Appendix:**
- Phase_20_Spation_Planck_Scales_Global_Stiffness_and_Force_Hierarchy.md
- Phase_21_Screening_Factors_and_the_10^-9_vs_10^-123_Hierarchy.md
- Phase_22_Appendix_k_Value_Derivation_from_Spectral_Data.md
- Phase_26_Pressure_Mediated_Forces_and_Scale_Dependent_Interactions.md

### Dependency Analysis Status
- G/M usage: 82 matches across 21 files
- Benchmark status: 892 matches across 40 files
- Status: In progress

## Refactoring Progress

### Group 1 (High Priority - Core Extensions)
1. [ ] Phase_6_Multi_Electron_Atoms_from_Occlusion_Geometry.md
2. [ ] Phase_7_Thermodynamics_from_Spation_Contact_Mechanics.md
3. [ ] Phase_8_Hyperfine_Structure_from_Magnetic_Moment_Overlap.md
4. [ ] Phase_9_Oblateness-Spin_Correlation.md
5. [ ] Phase_4_Lamb_Shift.md
6. [ ] Phase_5_Hyperfine_Splitting_from_Central_Pressure_Overlap.md

### Group 2 (Medium Priority - Nuclear Physics)
7. [ ] Phase_17_Toroidal_Structures_and_Pressure_Differentials_at_Femtoscale.md
8. [ ] Phase_18_Alpha_Particles_and_Beta_Decay.md
9. [ ] Phase_19_The_Role_of_the_Vortex_and_the_Effect_of_the_Helical_Wake.md

### Group 3 (Medium Priority - Gravitational/Stellar)
10. [ ] Phase_22_Exoplanetary_Systems_Deriving_Orbital_Dynamics_from_Stellar_Compactness_and_Luminosity.md
11. [ ] Phase_22_Validation_10_Star_Systems.md
12. [ ] Phase_Y_Galactic_Dynamics_Rotation_Curves_from_Displacement_and_Occlusion.md
13. [ ] Phase_24_Galactic_Rotation_Curves_Disk_Eclipse_Saturation.md
14. [ ] Phase_25_Flat_Galactic_Rotation_Curves_from_Disk_Eclipse_Saturation.md
15. [ ] Phase_25_Pressure_Differentials_Across_Scales.md

### Group 4 (Lower Priority - Supporting/Validation)
16. [ ] Remaining phases

## Refactoring Checklist (per phase)
- [ ] Remove all G (gravitational constant) dependencies
- [ ] Remove all M (mass) dependencies
- [ ] Replace with orbital equations: $v = (c/Ϟ)\sqrt{R_{\text{eff}}/r}$
- [ ] Replace with pressure gradient: $a = c^2 R_{\text{eff}}/(Ϟ^2 r^2)$
- [ ] Standardize notation: P_CMB (not P_0, P_∞)
- [ ] Standardize notation: Ϟ (not kappa) for velocity factor
- [ ] Standardize notation: R_eff for effective radius
- [ ] Add Benchmark Certification section
- [ ] Verify ≤0.8% error on all predictions
- [ ] Update all constants to CODATA 2018
- [ ] Rename file to remove numbers
- [ ] Update cross-references

