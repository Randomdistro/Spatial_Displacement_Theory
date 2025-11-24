# Deprecated Phases Refactoring Status

## Completed Refactorings

1. **Phase_6_Multi_Electron_Atoms** → **Phase_Multi_Electron_Atoms_from_Occlusion_Geometry.md**
   - Status: Refactored, benchmark section added
   - Issues: Quantum defect calculations need refinement (error ~15%)

2. **Phase_9_Oblateness-Spin** → **Phase_Oblateness_Spin_Correlation.md**
   - Status: Fully refactored, removed GM dependencies
   - Benchmarks: Jupiter (0.31%), Saturn (0.20%), Earth (0.24%) - all within 0.8%
   - Uses SDT orbital equations only

3. **Phase_17_Toroidal_Structures** → **Phase_Toroidal_Structures_and_Pressure_Differentials_at_Femtoscale.md**
   - Status: P_0 → P_CMB standardized
   - No G/M dependencies found
   - Benchmark section needs addition

4. **Phase_18_Alpha_Particles_and_Beta_Decay** → **Phase_Alpha_Particles_and_Beta_Decay.md**
   - Status: Renamed
   - No G/M dependencies found
   - Benchmark section needs addition

## In Progress

5. **Phase_4_Lamb_Shift.md**
   - Status: Has good benchmarks (0.5% error)
   - Needs: Notation standardization, rename

6. **Phase_5_Hyperfine_Splitting.md**
   - Status: Has benchmarks (ppm precision)
   - Needs: Notation standardization, rename

7. **Phase_7_Thermodynamics.md**
   - Status: Uses G in Planck length (acceptable)
   - Needs: Benchmark verification, rename

8. **Phase_8_Hyperfine_Structure.md**
   - Status: Clean, no G/M
   - Needs: Benchmark section, rename

## Remaining Phases (32 files)

### High Priority - Core Extensions
- Phase_4_Lamb_Shift.md
- Phase_5_Hyperfine_Splitting.md  
- Phase_7_Thermodynamics.md
- Phase_8_Hyperfine_Structure.md

### Medium Priority - Nuclear/Atomic
- Phase_19_The_Role_of_the_Vortex...
- Phase_23_Atomic_Structure...
- Phase_27A/B/C (Multi-electron systems)

### Medium Priority - Gravitational/Stellar
- Phase_15_Gravitation... (duplicate?)
- Phase_16_Universal_c-Boundary...
- Phase_22_* (multiple validation files)
- Phase_24_Galactic_Rotation...
- Phase_25_* (multiple files)
- Phase_Y_Galactic_Dynamics...

### Lower Priority - Supporting
- Phase_0_* (foundational/coordination)
- Phase_10/11/12_Electromagnetic...
- Phase_14_Thermodynamic...
- Phase_20/21_Screening...
- Phase_26_Pressure_Mediated...

## Action Items per Phase

For each remaining phase:
1. [ ] Check for G/M dependencies
2. [ ] Replace P_0 → P_CMB
3. [ ] Standardize notation (Ϟ, R_eff)
4. [ ] Add benchmark section with ≤0.8% error target
5. [ ] Rename file (remove numbers)
6. [ ] Update cross-references

## Notes

- Phases that use G only in Planck length formula (r_P = sqrt(ℏG/c³)) are acceptable
- Phases using "G" for Gibbs free energy are acceptable (notation conflict)
- Focus on removing actual gravitational constant dependencies

