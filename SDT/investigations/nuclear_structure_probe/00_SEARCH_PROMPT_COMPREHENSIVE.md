# Comprehensive Nuclear Packing File Search Prompt

## Purpose

This document provides an **excessively detailed** search strategy to locate and catalog every file in the codebase that relates to nuclear packing, geometry, structure, binding energies, transformations, electron participation, and all related atomic/nuclear phenomena.

## Search Categories

### 1. Nuclear Packing Geometry Files

**Search Terms:**

- "nuclear packing"
- "nuclear geometry"
- "nuclear structure"
- "icosahedral packing"
- "octahedral space"
- "deuteron geometry"
- "alpha particle geometry"
- "tetrahedral nucleus"
- "nuclear building blocks"
- "nuc_primordial"
- "2nuc_H"
- "2nuc_He"
- "tri-alpha"
- "alpha cluster"
- "nuclear shell"
- "nuclear layer"
- "interstitial space"
- "triangular interstice"
- "dodecahedral"
- "nuclear lattice"

**File Patterns:**

- `*nuclear*packing*.md`
- `*nuclear*geometry*.md`
- `*nuclear*structure*.md`
- `*packing*geometry*.md`
- `*building*block*.md`
- `*alpha*cluster*.md`
- `*deuteron*.md`
- `*alpha*.md` (in nuclear context)

**Expected Locations:**

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/05_Chemistry/`
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/06_Nuclear_Physics/`
- `SDT/Code/sdt_navier*/`
- `SDT/investigations/`
- `SDT/data/`

### 2. Binding Energy Calculation Files

**Search Terms:**

- "binding energy"
- "nuclear binding"
- "B_exp"
- "B_alpha"
- "28.296 MeV"
- "2.224 MeV"
- "neutrino flux"
- "18 neutrinos"
- "E_nu"
- "binding energy calculation"
- "nuclei per nucei"
- "nuclear calculator"
- "binding energy predicted"
- "binding energy experimental"

**File Patterns:**

- `*binding*energy*.py`
- `*binding*energy*.cpp`
- `*binding*energy*.md`
- `*nuclear*calculator*.py`
- `*nuclei*calculator*.py`
- `*nuclei_per_nucei*.py`
- `*nuclear*energy*.py`

**Expected Locations:**

- `SDT/Code/sdt_navier*/`
- `SDT/data/`
- `SDT/tools/`
- `SDT/investigations/`

### 3. Electron Positioning and Participation Files

**Search Terms:**

- "electron positioning"
- "electron participation"
- "electron placement"
- "pressure gradient field"
- "solid angle occlusion"
- "occlusion factor"
- "electron orbital"
- "electron vortex"
- "toroidal vortex"
- "pressure minima"
- "electron parking"
- "electron density"
- "participating electron"
- "electron structure"
- "atomic structure"
- "electron configuration"
- "orbital geometry"
- "electron cloud"
- "electron probability"

**File Patterns:**

- `*electron*position*.py`
- `*electron*position*.md`
- `*electron*participation*.py`
- `*occlusion*.py`
- `*solid*angle*.py`
- `*pressure*gradient*.py`
- `*atomic*structure*.py`
- `*orbital*.py`

**Expected Locations:**

- `SDT/Code/`
- `SDT/tools/sdt_atomic/`
- `SDT/data/`
- `SDT/investigations/`
- Root directory (`electron_positioning_models.py`, `sdt_electron_positioning_real.py`)

### 4. Nuclear Transformation Files (Decay, Fusion, Fission)

**Search Terms:**

- "nuclear decay"
- "beta decay"
- "alpha decay"
- "gamma decay"
- "nuclear fusion"
- "nuclear fission"
- "nuclear reaction"
- "transformation"
- "decay chain"
- "radioactive decay"
- "weak interaction"
- "strong interaction"
- "neutrino circulation"
- "electron ejection"
- "antineutrino"
- "nuclear transition"
- "isomer"
- "excited state"
- "ground state"

**File Patterns:**

- `*decay*.py`
- `*decay*.md`
- `*fusion*.py`
- `*fusion*.md`
- `*fission*.py`
- `*fission*.md`
- `*transformation*.py`
- `*reaction*.py`
- `*weak*interaction*.md`
- `*strong*interaction*.md`

**Expected Locations:**

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/06_Nuclear_Physics/`
- `SDT/investigations/`
- `SDT/Code/`

### 5. Ionization and Charge State Files

**Search Terms:**

- "ionization"
- "ionisation"
- "ionization energy"
- "ionization potential"
- "cation"
- "anion"
- "charge state"
- "ionic state"
- "Z_eff"
- "effective charge"
- "ionization series"
- "first ionization"
- "second ionization"
- "multiple ionization"
- "removal energy"
- "electron removal"
- "electron affinity"

**File Patterns:**

- `*ionization*.py`
- `*ionization*.md`
- `*ionisation*.py`
- `*ionisation*.md`
- `*cation*.py`
- `*anion*.py`
- `*charge*state*.py`
- `*Z_eff*.py`

**Expected Locations:**

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/05_Chemistry/`
- `SDT/data/`
- `SDT/tools/`
- `SDT/investigations/`

### 6. Excitation and Energy Level Files

**Search Terms:**

- "excitation"
- "excited state"
- "energy level"
- "transition"
- "spectral line"
- "emission"
- "absorption"
- "photon emission"
- "photon absorption"
- "electronic transition"
- "atomic transition"
- "energy state"
- "quantum state"
- "n, l, j"
- "principal quantum number"
- "angular momentum"
- "fine structure"
- "hyperfine structure"

**File Patterns:**

- `*excitation*.py`
- `*excitation*.md`
- `*energy*level*.py`
- `*transition*.py`
- `*spectral*.py`
- `*emission*.py`
- `*absorption*.py`

**Expected Locations:**

- `SDT/tools/sdt_atomic/`
- `SDT/data/`
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/01_Atomic_Physics/`

### 7. Velocity, Speed, and Timing Files

**Search Terms:**

- "velocity"
- "speed"
- "timing"
- "time scale"
- "characteristic time"
- "tau"
- "timescale"
- "orbital velocity"
- "electron velocity"
- "nuclear velocity"
- "reaction time"
- "decay time"
- "half-life"
- "lifetime"
- "rate constant"
- "kinetic energy"
- "momentum"
- "angular velocity"
- "rotation speed"
- "circulation speed"

**File Patterns:**

- `*velocity*.py`
- `*speed*.py`
- `*timing*.py`
- `*time*.py` (in context)
- `*rate*.py`
- `*kinetic*.py`
- `*momentum*.py`

**Expected Locations:**

- `SDT/Code/`
- `SDT/investigations/`
- `SDT/Papers/`

### 8. Turbine Cell and Field System Files

**Search Terms:**

- "turbine cell"
- "turbine"
- "ProtonTurbine"
- "NeutronTurbine"
- "field system"
- "FieldSystem"
- "pressure field"
- "velocity field"
- "sigma"
- "Gamma"
- "kappa"
- "eta"
- "slip"
- "circulation"
- "diversion density"
- "P_infinity"
- "pressure infinity"
- "master equation"
- "SDT Navier"
- "Navier-Stokes"

**File Patterns:**

- `*turbine*.py`
- `*turbine*.cpp`
- `*turbine*.hpp`
- `*field*.py`
- `*field*.cpp`
- `*navier*.py`
- `*navier*.cpp`
- `*sdt_navier*.py`
- `*sdt_navier*.cpp`

**Expected Locations:**

- `SDT/Code/sdt_navier/`
- `SDT/Code/sdt_navier_cpp/`

### 9. Geometry and Coordinate System Files

**Search Terms:**

- "spherical coordinates"
- "icosahedral coordinates"
- "tetrahedral coordinates"
- "coordinate system"
- "geometry calculation"
- "geometric structure"
- "packing arrangement"
- "cluster geometry"
- "nuclear arrangement"
- "spatial arrangement"
- "distance calculation"
- "separation"
- "radius"
- "R_p"
- "R_n"
- "effective radius"
- "geometric center"

**File Patterns:**

- `*geometry*.py`
- `*geometry*.cpp`
- `*geometry*.hpp`
- `*coordinate*.py`
- `*coordinate*.cpp`
- `*packing*.py`
- `*arrangement*.py`

**Expected Locations:**

- `SDT/Code/`
- `SDT/tools/sdt_atomic/`
- `SDT/Papers/`

### 10. Chemical and Molecular Structure Files

**Search Terms:**

- "chemical bonding"
- "molecular structure"
- "bond angle"
- "bond length"
- "lone pair"
- "bonding pair"
- "valence electron"
- "chemical property"
- "periodic table"
- "element"
- "atomic number"
- "mass number"
- "isotope"
- "nuclear charge"
- "Z"
- "N"
- "A"

**File Patterns:**

- `*chemical*.py`
- `*chemical*.md`
- `*molecular*.py`
- `*molecular*.md`
- `*bond*.py`
- `*periodic*.py`
- `*element*.py`
- `*isotope*.py`

**Expected Locations:**

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/05_Chemistry/`
- `SDT/data/`
- `SDT/Molecular_Structures/`

### 11. Validation and Benchmark Files

**Search Terms:**

- "validation"
- "benchmark"
- "experimental"
- "comparison"
- "error"
- "precision"
- "accuracy"
- "verification"
- "test"
- "B01"
- "B02"
- "B17"
- "B18"
- "B19"
- "B20"
- "B21"
- "B22"
- "B23"
- "B24"

**File Patterns:**

- `*validation*.py`
- `*validation*.json`
- `*validation*.md`
- `*benchmark*.py`
- `*benchmark*.json`
- `*benchmark*.md`
- `*test*.py`
- `*verify*.py`

**Expected Locations:**

- `SDT/benchmarks/`
- `SDT/tools/`
- `SDT/investigations/`

### 12. Documentation and Theory Files

**Search Terms:**

- "theory"
- "derivation"
- "proof"
- "mathematical"
- "equation"
- "formula"
- "postulate"
- "axiom"
- "principle"
- "framework"
- "model"
- "mechanism"
- "explanation"
- "description"
- "analysis"
- "investigation"

**File Patterns:**

- `*.md` (all markdown files)
- `*theory*.md`
- `*derivation*.md`
- `*proof*.md`
- `*framework*.md`
- `*model*.md`
- `*analysis*.md`
- `*investigation*.md`

**Expected Locations:**

- `SDT/Papers/`
- `SDT/investigations/`
- `SDT/benchmarks/`
- Root directory

## Search Execution Strategy

### Phase 1: Broad Semantic Search

Use codebase_search with broad queries:

1. "nuclear packing geometry structure"
2. "electron positioning orbital structure"
3. "binding energy calculation nuclear"
4. "nuclear decay fusion fission transformation"
5. "ionization cation anion charge state"
6. "excitation energy level transition"
7. "velocity speed timing nuclear atomic"
8. "turbine cell field system pressure"
9. "chemical bonding molecular structure"
10. "validation benchmark experimental comparison"

### Phase 2: Pattern-Based File Search

Use glob_file_search with patterns:

1. `**/*nuclear*.py`
2. `**/*nuclear*.cpp`
3. `**/*nuclear*.hpp`
4. `**/*nuclear*.md`
5. `**/*packing*.py`
6. `**/*packing*.md`
7. `**/*electron*.py`
8. `**/*electron*.md`
9. `**/*binding*.py`
10. `**/*binding*.md`
11. `**/*ionization*.py`
12. `**/*ionization*.md`
13. `**/*excitation*.py`
14. `**/*excitation*.md`
15. `**/*decay*.py`
16. `**/*decay*.md`
17. `**/*fusion*.py`
18. `**/*fusion*.md`
19. `**/*geometry*.py`
20. `**/*geometry*.cpp`
21. `**/*geometry*.hpp`
22. `**/*occlusion*.py`
23. `**/*turbine*.py`
24. `**/*turbine*.cpp`
25. `**/*field*.py`
26. `**/*field*.cpp`

### Phase 3: Specific Term Grep Search

Use grep with case-insensitive search:

1. `grep -i "nuclear packing"`
2. `grep -i "deuteron"`
3. `grep -i "alpha particle"`
4. `grep -i "binding energy"`
5. `grep -i "electron positioning"`
6. `grep -i "ionization"`
7. `grep -i "excitation"`
8. `grep -i "decay"`
9. `grep -i "fusion"`
10. `grep -i "fission"`
11. `grep -i "turbine"`
12. `grep -i "occlusion"`
13. `grep -i "solid angle"`
14. `grep -i "pressure gradient"`
15. `grep -i "velocity"`
16. `grep -i "speed"`
17. `grep -i "timing"`

### Phase 4: Directory-Specific Search

Search specific directories known to contain relevant files:

1. `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/05_Chemistry/`
2. `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/06_Nuclear_Physics/`
3. `SDT/Code/sdt_navier/`
4. `SDT/Code/sdt_navier_cpp/`
5. `SDT/data/`
6. `SDT/tools/`
7. `SDT/investigations/`
8. `SDT/benchmarks/`
9. Root directory (for top-level files)

## Expected File Inventory

### Core Nuclear Packing Files (High Priority)

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/05_Chemistry/NUCLEAR_PACKING_GEOMETRY.md`
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/05_Chemistry/NUCLEAR_PACKING_STRUCTURE_AND_DATA.md`
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/05_Chemistry/NUCLEAR_PACKING_SOLID_ANGLES.md`
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/05_Chemistry/CORRECTED_PACKING_STRUCTURE.md`
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/05_Chemistry/BUILDING_BLOCK_SOLID_ANGLES.md`
- `SDT/Code/sdt_navier_cpp/include/nuclear_geometry_occlusion.hpp`
- `SDT/Code/sdt_navier_cpp/include/nuclear_geometry.hpp`
- `SDT/Code/sdt_navier/nuclear.py`
- `SDT/data/nuclei_per_nucei_calculator.py`

### Electron Positioning Files (High Priority)

- `electron_positioning_models.py` (root)
- `sdt_electron_positioning_real.py` (root)
- `SDT/electron_positioning_models.py`
- `SDT/Code/carbon12_electron_parking.py`
- `SDT/tools/sdt_atomic/geometry.py`
- `SDT/tools/sdt_atomic/occlusion.py`
- `SDT/data/sdt_occlusion_factors.py`

### Binding Energy Files (High Priority)

- `SDT/data/nuclei_per_nucei_calculator.py`
- `SDT/Code/sdt_navier/nuclear.py`
- `SDT/Code/sdt_navier_cpp/src/nuclear.cpp`
- `SDT/Code/sdt_navier_cpp/tools/nuclear_calculator.cpp`
- `SDT/investigations/nuclear_driven_chemistry_calculations.py`

### Ionization Files (High Priority)

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/05_Chemistry/IONIZATION_FROM_SOLID_ANGLES.md`
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/05_Chemistry/CORRECT_IONIZATION_DERIVATION.md`
- `SDT/data/atomica_sentis_calculator.py`

### Transformation Files (Medium Priority)

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/06_Nuclear_Physics/Weak_Interactions_from_Neutrino_Circulation/`
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/06_Nuclear_Physics/Strong_Interactions_from_Pressure_Confinement/`
- `ex_parte/05_electron_windout_beta_decay.md`
- `ex_parte/06_nuclear_physics_foundation.md`

### Validation Files (Medium Priority)

- `SDT/benchmarks/*/B*_validation_report.json`
- `SDT/tools/validate_*.py`
- `SDT/data/atomica_sentis_validation.py`

## Search Completion Criteria

The search is complete when:

1. ✅ All files matching patterns have been located
2. ✅ All semantic searches have been executed
3. ✅ All grep searches have been executed
4. ✅ All expected high-priority files have been found
5. ✅ A comprehensive inventory has been created
6. ✅ File relationships and dependencies have been mapped
7. ✅ Key constants, equations, and data structures have been identified
8. ✅ All transformation pathways (decay, fusion, fission) have been documented
9. ✅ All electron participation mechanisms have been cataloged
10. ✅ All timing, velocity, and speed calculations have been located

## Next Steps After Search

Once the comprehensive search is complete:

1. Create a master inventory file listing all discovered files
2. Map relationships between files (dependencies, data flow)
3. Extract key constants, equations, and data structures
4. Document all transformation pathways
5. Catalog all electron participation mechanisms
6. Identify all timing, velocity, and speed calculations
7. Build the comprehensive investigation framework

---

**Status:** Search prompt ready for execution
**Date:** 2026-01-02
**Purpose:** Foundation for comprehensive nuclear structure investigation
