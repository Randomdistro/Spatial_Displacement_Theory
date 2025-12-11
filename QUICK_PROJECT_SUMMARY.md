# Spatial Displacement Theory - Quick Project Summary

**Status:** Active Research - 16/24 Benchmarks Certified  
**Scale:** 644 files, 12 MB (2.2 MB code + 9.8 MB theory)  
**Development:** Commits within 2 weeks, high velocity

---

## What Is This?

An **alternative physics framework** proposing that:
- Gravity = pressure gradients from matter occlusion in an incompressible medium ("spation")
- Electromagnetism = deformation of the pressure field
- Atoms = toroidal vortices with helical standing wave structures
- No need for dark matter, quantum weirdness, or spacetime curvature

**Validation:** Matches quantum mechanics, relativity, and experimental data to <1% error across 53 orders of magnitude (atoms to galaxies).

---

## Architecture at a Glance

### Code (2.2 MB)
```
Python Modules (2,007 lines):
  ├── sdt_core/        - Constants, core physics
  ├── sdt_navier/      - Field theory (2,007 lines)
  ├── sdt_redshift/    - Cosmology
  └── sdt_stars/       - Stellar calculations (under dev)

C++ Simulators (7,000+ lines):
  ├── sdt_navier_cpp/      - Field solver (1,152 lines)
  ├── sdt_chemistry/       - Molecules (4,939 lines)
  ├── sdt_atomic_sim/      - Orbital visualization
  ├── sdt_orbital_sim/     - Galaxy dynamics
  └── sdt_solar_system/    - N-body systems

Tools & Scripts:
  ├── 30+ investigation scripts (.py)
  ├── Visualization tools (.html, C++)
  └── Utility calculators
```

### Theory Documentation (9.8 MB, 137 papers)
```
Main Structure:
  ├── Complete Treatise (410 KB)
  ├── Part I: Axioms & Core Equations (52+ files)
  │   ├── 00_Foundations (6 subdirs)
  │   ├── 01_Atomic_Physics (8 subdirs)
  │   ├── 02_Electromagnetism (5 subdirs)
  │   ├── 03_Gravitation_and_Cosmology (7 subdirs)
  │   ├── 04_Thermodynamics (5 subdirs)
  │   ├── 05_Chemistry (34 subdirs!)
  │   └── 06_Nuclear_Physics (8 files)
  ├── ATOMICUS Library (118 elements, element-by-element)
  └── Benchmarks (validation tracking, JSON reports)
```

---

## Benchmark Status (16/24 Certified)

### Certified Results
| Domain | Benchmark | Error | Physics |
|--------|-----------|-------|---------|
| **Atoms** | Rydberg formula | <0.01% | Helical quantization |
| **Atoms** | Fine structure | <0.1% | Vortex relativistic effects |
| **Atoms** | Lamb shift | <0.01% | Wake asymmetry |
| **Atoms** | Hyperfine | <0.003% | Magnetic moment overlap |
| **Atoms** | Multi-electron | <5% | Occlusion screening |
| **Gravity** | Orbital mechanics | <0.01% | Pressure balance |
| **Gravity** | Mercury precession | <0.1% | Strong field test |
| **Gravity** | Light deflection | <0.1% | Pressure field topology |
| **Gravity** | Planetary oblateness | ±3% | Spin-pressure coupling |
| **Cosmology** | CMB redshift | Exact | Pressure horizon z=1089 |
| **Cosmology** | BAO scale | ±3% | Pressure waves 147 Mpc |
| **Stars** | Stellar structure | ±5% | 50+ star validation |
| **Rotations** | Galactic curves | <1% | Disk eclipse (no dark matter) |
| **Thermo** | Transport | <0.05% | T^(1/2) scaling |
| **Universal** | k-law | <0.8% | v(r)=(c/k)√(R/r), 53 orders |
| **Universal** | z·k² relation | <1% | Continuous mass systems |

### Under Investigation
- B17: Magnetism (g-factors)
- B18: Nuclear structure (binding energies)
- B19: Weak interactions (beta decay)
- B21: Screening factors (10^-9 hierarchy)
- B23-24: Multi-electron/scale systems

---

## Key Components

### Python Core
- **sdt_core**: Physical constants, particle states
- **sdt_navier**: Master equation on discrete lattice
  - Fields: P (pressure), v (velocity), κ (curvature), η (slip), e (energy)
  - Equations: Ė = P∞ A_eff Γ κ (1-η)
  - Solver: RK4 with incompressibility (∇·v = 0)

### C++ Simulators
1. **sdt_navier_cpp**: Field theory solver
   - Nuclear systems (deuteron, triton, helion, alpha)
   - Binding energies, magnetic moments
   - Python bindings via pybind11

2. **sdt_chemistry**: Molecular design
   - 20+ elements with SDT parameters
   - Bond typing (ionic, covalent, metallic, etc.)
   - Property prediction without quantum chemistry
   - Visualization (OBJ, PDB, XYZ, POV-Ray)

3. **sdt_atomic_sim**: Atomic physics
   - Helical standing wave orbitals
   - Rydberg spectra generation
   - Fine structure, hyperfine, transitions
   - 3D visualization with VTK

4. **sdt_orbital_sim**: Galaxy dynamics
5. **sdt_solar_system**: N-body planetary systems

---

## Development Status

### What's Done
- Atomic physics (Rydberg through hyperfine) ✓
- Orbital mechanics (Kepler laws) ✓
- Gravitational physics (without spacetime curvature) ✓
- Thermodynamics (k-law, transport) ✓
- CMB cosmology (pressure horizon) ✓
- Chemistry framework (bonding geometry) - Partial
- ATOMICUS library (periodic table analysis) - Ongoing

### What's In Progress
- Nuclear structure (binding energies for A>4)
- Galactic rotation (validating no dark matter hypothesis)
- Gravitational waves (LIGO/LISA analysis)
- Weak interactions (beta decay)
- Electromagnetism details (g-factors, etc.)

### What's Missing
- Quark physics / particle physics
- Black hole thermodynamics
- Quantum entanglement (speculative)
- GPU acceleration

---

## Documentation Structure

### Theory Organization
- **Main Physics** → Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/
- **Element Atlas** → ATOMICUS/ (H through Oganesson)
- **Validation** → benchmarks/B01_B24_TrackingSheet.csv
- **Data** → data/ (NIST spectra, exoplanet parameters, rotation curves)
- **Glossary** → TERMS.md (11 KB)
- **Roadmap** → SDT_INDEX.md (8 KB)

### Code Documentation
- Every C++ project: README.md, API.md, BUILD.md
- Python modules: docstrings + __init__.py exports
- Investigation scripts: inline comments explaining hypotheses

---

## Build & Run

### Python
```bash
cd SDT/Code
python -m sdt_navier              # Field theory module
python sdt_core/__init__.py       # Core constants
python investigate_*.py           # Active hypotheses
```

### C++
```bash
cd SDT/Code/sdt_navier_cpp
mkdir build && cd build
cmake ..
make -j$(nproc)

# Run tools
./tools/simulate_deuteron           # Nuclear systems
./tools/stellar_calculator          # Star parameters
./tools/atomic_calculator           # Spectroscopy
```

### Chemistry Simulator
```bash
cd SDT/Code/sdt_chemistry
mkdir build && cd build
cmake ..
make -j$(nproc)

./compound_designer                 # Interactive design
./molecule_viewer design output.obj # 3D visualization
```

---

## Key Physics Principles

### Master Equation (All Forces)
```
∇·[K_bulk ∇Δ(x)] = -κ ρ_disp(x) (1 - E(x,n̂))
```
Where:
- **K_bulk** = 4.6×10^113 Pa (spation stiffness)
- **ρ_disp** = displacement volume density (matter)
- **E(x,n̂)** = occlusion function (directional shadowing)

### Pressure-Based Forces
```
F = -V_disp ∇P(x)
```

### Universal k-Law
```
v(r) = (c/k)√(R/r)
```
Valid from atoms (k≈137) to galaxies (k≈10^5)

### Key Constants
- **C_LATTICE** = 299,792,458 m/s (speed of light)
- **RHO_S** = 5.2×10^96 kg/m³ (spation density)
- **α** = 1/137.036 (fine structure from geometry)
- **ξ** = 1.0335 (universal packing factor)

---

## Testing & Validation

### Unit Tests
- 4 Python test suites (fields, operators, solver, integration)
- 7 C++ test suites (across projects)
- Catch2 framework for C++

### Benchmark Validation
- CSV tracking sheet (B01-B24)
- JSON validation reports (16 certified)
- Experimental data files (NIST, JPL, SPARC, etc.)

### Continuous Testing
- Investigation scripts for hypothesis testing
- 30+ calculation scripts validating specific claims
- ATOMICUS enrichment scripts

---

## Current Focus (December 2025)

**Priority 1 (Immediate):**
- ATOMICUS library completion
- Benchmark B17-B21 certification
- Documentation cross-referencing

**Priority 2 (Next 3 months):**
- Fast multipole method (occlusion optimization)
- GPU acceleration
- Peer review preparation

**Priority 3 (Next 6 months):**
- Journal submission (Phase 2-3)
- Galactic rotation validation
- LIGO/LISA analysis

---

## Quick Links

- **Main README**: SDT/README.md (comprehensive overview)
- **Theory Entry Point**: Papers/README_START_HERE.md
- **Element Library**: ATOMICUS/ (periodic table)
- **Benchmarks**: benchmarks/B01_B24_TrackingSheet.csv
- **Build Docs**: Each simulator's BUILD.md
- **Full Analysis**: ARCHITECTURAL_ANALYSIS.md (this project's technical review)

---

## Key Metrics

| Metric | Value |
|--------|-------|
| **Code Files** | 644 total |
| **Total Size** | 12.0 MB |
| **Theory Papers** | 137 markdown files |
| **C++ Lines** | 7,000+ |
| **Python Lines** | 2,007 (sdt_navier) |
| **Benchmarks** | 24 defined, 16 certified |
| **Elements Documented** | 118+ (ATOMICUS) |
| **Test Suites** | 11 |
| **CMake Projects** | 7 |
| **Git Commits** | Active (2-week pace) |
| **Peer Review** | Pre-submission |

---

## For Different Audiences

### For Physicists
→ Start: Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/00_Foundations/

**Challenge the theory:**
- Certification protocol: benchmarks/certification_protocol.md
- Falsification criteria: 24 distinct, testable benchmarks

### For Developers
→ Start: SDT/Code/

**Build the simulators:**
- C++ projects: Modern C++20, CMake, modular
- Python modules: Prototyping, validation scripts
- Parallel computing: OpenMP, GPU-ready (design)

### For Data Scientists
→ Start: data/ and benchmarks/

**Validate the claims:**
- 16 certified benchmarks (<1% error)
- NIST, JPL, SPARC validation data
- JSON reports with detailed metrics

### For System Architects
→ Read: ARCHITECTURAL_ANALYSIS.md

**Understand the structure:**
- 7 C++ simulators, layered design
- Python-C++ integration via pybind11
- Dependency graph and data flow

---

## The Big Picture

**What it claims:** Gravity, EM, atoms, and cosmology emerge from a single mechanical principle—pressure gradients in an incompressible medium.

**Why it matters:** 
- If true: Revolution in fundamental physics, no dark matter, quantum mechanics is effective theory
- If false: Reveals deep principles about why standard physics works

**Current evidence:** 16 benchmarks <1% error, 53 orders of magnitude (atoms to galaxies)

**Outstanding work:** Complete nuclear structure, weak interactions, particle physics

**Timeline:** 12-36 months to journal publication (pending benchmark completion + peer review)

---

**Last Updated:** December 11, 2025  
**For Full Details:** See ARCHITECTURAL_ANALYSIS.md (38 KB comprehensive report)
