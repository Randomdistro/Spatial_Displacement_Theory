# sdt_navier_cpp/tools — Overview

Standalone C++ executables implementing the SDT benchmark validation suite (B25–B100) and domain-specific calculator CLIs. Each benchmark tool outputs JSON validation reports.

## Files

- **CMakeLists.txt** — Build configuration for all tool executables
- **README.md** — Documentation for the tools directory and benchmark structure
- **benchmarks_b25_b50.cpp** — Benchmarks B25–B50: atomic structure (Rydberg, fine/hyperfine structure, screening, ionisation, Lamb shift, Stark effect)
- **benchmarks_b51_b60.cpp** — 🟡 Benchmarks B51–B60: nuclear and magnetic properties. Contains "quantum" terminology and "Standard Model" comparison references
- **benchmarks_b61_b70.cpp** — 🟡 Benchmarks B61–B70: relativity and gravity (GPS, muon lifetime, Pound-Rebka, Shapiro delay, black hole shadow, GW chirp, binary pulsar, CMB). Contains Schwarzschild references
- **benchmarks_b71_b80.cpp** — 🟡 Benchmarks B71–B80: nuclear structure and particles. Contains "quark" and "gluon" references
- **benchmarks_b81_b100.cpp** — 🟡 Benchmarks B81–B100: stellar and cosmological. Contains `M_SUN` and Chandrasekhar mass references
- **galactic_rotation.cpp** — 🟡 Galactic rotation curve generator with dark matter NFW comparison. Contains explicit dark matter model code
- **stellar_calculator.cpp** — ✅ Stellar calculator CLI: computes c-boundary, effective temperature, luminosity for input k-factor
- **atomic_calculator.cpp** — ✅ Atomic calculator CLI: computes Rydberg transitions, screening, series
- **nuclear_calculator.cpp** — 🟡 Nuclear binding energy calculator. Contains QED/QCD/Standard Model comparison print statements
- **nuclear_calculator_occlusion.cpp** — ✅ Nuclear binding via occlusion model: CMB shadow gives binding energy
- **validate_lk2_relation.cpp** — ✅ Validates L·k² = constant for galaxy sample
- **zk2_systematic_40.cpp** — ✅ Systematic zk²=1 analysis across 40 elements
- **isoelectronic_convergence.cpp** — ✅ Isoelectronic sequence convergence analysis
- **simulate_deuteron.cpp** — ✅ Deuteron simulation from Navier field equations
- **simulate_nuclear.cpp** — ✅ Nuclear system simulation (alpha particle, carbon-12)
- **analyze_results.cpp** — ✅ Result analysis and comparison utility
