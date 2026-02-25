# Constants Consolidation Audit Report

**Generated:** 1769750438.4768324

## Executive Summary

- Total unique constants found: 73
- Files scanned: 117
- Discrepancies identified: 0

## Complete Inventory of Constants

### CODATA 2018 Fundamental Constants

| Constant | Value | Unit | Source |
|----------|-------|------|--------|
| C | 2.997924580000e+08 | - | CODATA 2018 (exact) |
| H | 6.626070150000e-34 | - | CODATA 2018 |
| H_BAR | 1.054571817000e-34 | - | CODATA 2018 |
| E_CHARGE | 1.602176634000e-19 | - | CODATA 2018 |
| M_E | 9.109383701500e-31 | - | CODATA 2018 |
| M_P | 1.672621923690e-27 | - | CODATA 2018 |
| M_N | 1.674927498040e-27 | - | CODATA 2018 |
| ALPHA | 7.297352569300e-03 | - | CODATA 2018 |
| A_0 | 5.291772109030e-11 | - | CODATA 2018 |
| R_INF | 1.097373156816e+07 | - | CODATA 2018 |

### SDT-Specific Constants

| Constant | Value | Unit | Source |
|----------|-------|------|--------|
| R_P | 8.400000000000e-16 | - | CODATA 2018 (0.84 fm) |
| R_N | 8.700000000000e-16 | - | CODATA 2018 (0.87 fm) |
| KAPPA_P | 1.190000000000e+15 | - | Phase 19 (1/R_P) |
| GAMMA_P | 5.460000000000e-01 | - | Phase 19 |
| ETA_P_BOUND | 3.000000000000e-04 | - | Phase 19 |
| GAMMA_E_N | 5.310000000000e-01 | - | Phase 19 |
| ETA_N_BOUND | 1.900000000000e-03 | - | Phase 19 |
| P_INFINITY_NUCLEAR | 1.650000000000e+31 | - | Phase 19 |
| P_CMB | 2.036000000000e-02 | - | CMB recombination (z=1089.9) |
| RHO_S | 5.200000000000e+96 | - | Phase 20 |
| K_BULK | 4.600000000000e+113 | - | Phase 20 |
| R_PLANCK | 1.616000000000e-35 | - | CODATA 2018 |

### Experimental Binding Energies

| Constant | Value | Unit | Source |
|----------|-------|------|--------|
| B_DEUTERON | 2.224000 | MeV | Experimental (MeV) |
| B_ALPHA | 28.296000 | MeV | Experimental (MeV) |
| B_TRITON | 8.482000 | MeV | Experimental (MeV) |
| B_HELION | 7.718000 | MeV | Experimental (MeV) |

## Discrepancy Matrix

### Constants with Multiple Values

#### B_DEUTERON

**Recommended Value:** 2.2246 MeV  
**Recommended Source:** Experimental (MeV) - More precise CODATA value

| File | Value | Comment |
|------|-------|---------|
| Code/sdt_navier_cpp/include/sdt_navier/constants.hpp | 2.224 | Experimental binding energies (MeV) |
| data/nuclei_per_nucei_calculator.py | 2.224 | Experimental Binding Energies (MeV) - Reference values |
| investigations/nuclear_structure_probe/Phase_01_Nuclear_Packing/01_02_first_shell_completion.py | 2.2246 | MeV |
| investigations/nuclear_structure_probe/Phase_02_Binding_Energy/02_01_occlusion_binding_calculator.py | 2.2246 | Deuteron |

**Note:** The value 2.2246 MeV is the more precise experimental value and should be used consistently. Files using 2.224 should be updated to 2.2246.

## Migration Path

### Files Requiring Updates

#### Code/sdt_navier_cpp/include/sdt_navier/constants.hpp

Constants to update:
- `B_DEUTERON`: Change to 2.2246 (from Experimental (MeV))

#### data/nuclei_per_nucei_calculator.py

Constants to update:
- `B_DEUTERON` (in B_EXP dict): Change to 2.2246 (from Experimental (MeV))
