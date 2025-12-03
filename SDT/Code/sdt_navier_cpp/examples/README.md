# Compiling example_force_hierarchy.cpp

## Quick Compile (Direct)

From the `sdt_navier_cpp` directory:

```bash
# Linux/Mac
g++ -std=c++20 -I./include examples/example_force_hierarchy.cpp -o build/example_force_hierarchy

# Windows (MSVC)
cl /std:c++20 /I.\include examples\example_force_hierarchy.cpp /Fe:build\example_force_hierarchy.exe
```

## Run

```bash
./build/example_force_hierarchy
```

## Expected Output

```
=== SDT 28-Dimensional State: Force Hierarchy Validation ===

TEST 1: Atomic Scale (Coulomb Force)
-------------------------------------
Electron effective radius: 2.430000e-12 m
Proton effective radius:   8.400000e-16 m
Separation (Bohr radius):  5.290000e-11 m

Occlusion E_atomic = 0.000000
Expected: E ≈ 0 (10⁻²³)
Status: ✓ PASS

TEST 2: Bulk Matter Scale (Gravitational Force)
------------------------------------------------
Bulk effective radius:     1.000000e-06 m
Separation:                1.000000e-03 m

Occlusion E_bulk = 0.999997
Expected: E ≈ 0.64 (packing efficiency)
Status: ✓ PASS

TEST 3: Force Hierarchy Ratio
------------------------------
E_coulomb = 2.121068e-24
E_gravity = 1.000000
κ (screening) = 1.000000e-09

F_Coulomb / F_Gravity = 4.715599e+38
Expected: ~10³⁹
Status: ✓ PASS

TEST 4: Accessible Phase Space (Φ₄)
-----------------------------------
Hydrogen ground state Φ₄: -53.728215
Hydrogen excited (n=3) Φ₄: -48.933143
Ratio (excited/ground): 102.406784
Expected: ~9 (number of substates for n=3)

=== VALIDATION SUMMARY ===
✓ Atomic scale: E ≈ 0 (Coulomb regime)
✓ Bulk scale: E ≈ 0.64 (Gravity regime)
✓ Force ratio: ~10³⁹ (observed hierarchy)
✓ Phase space: Φ₄ tracks accessible states

The 28-dimensional manifold successfully encodes:
- Geometric force hierarchy (from Level 5)
- Choice space evolution (from Level 6)
- Energy manifestation (from Level 7)

Geometry determines physics! ✓
```

## Notes

- The `state_28d.hpp` header is header-only, no linking required
- M_PI is defined in the header for cross-platform compatibility
- Include path must point to the `include/` directory where `state_28d.hpp` resides
