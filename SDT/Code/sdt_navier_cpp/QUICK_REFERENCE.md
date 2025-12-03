# SDT Calculator Quick Reference

## Build & Run (Windows)

```powershell
# One-time setup
cd C:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\Code\sdt_navier_cpp
mkdir build
cd build
cmake ..
cmake --build . --config Release

# Run calculators
.\tools\Release\stellar_calculator.exe --example
.\tools\Release\atomic_calculator.exe --all
.\tools\Release\galactic_rotation.exe --validate

# Run tests
.\tests\Release\test_calculators.exe
```

## Quick Examples

### Stellar Calculator
```powershell
# TRAPPIST-1 system
stellar_calculator --star "TRAPPIST-1" --mass 0.089 --radius 0.121 ^
                   --planet-a 0.01111 --planet-v 53.1

# Sun only
stellar_calculator --star "Sun" --mass 1.0 --radius 1.0
```

### Atomic Calculator
```powershell
# Lyman-α (UV line)
atomic_calculator --transition "2->1"

# Complete demo
atomic_calculator --all

# Hydrogen 21cm line
atomic_calculator --hyperfine

# Oxygen screening
atomic_calculator --screening "8,4,2p"
```

### Galactic Rotation
```powershell
# Milky Way with visualization
galactic_rotation --R_d 2.5 --v_flat 220 --viz

# Validate theory
galactic_rotation --validate

# Compare with dark matter
galactic_rotation --galaxy MW --compare-dm
```

## Validation Status

| Tool | Benchmark | Error | Status |
|------|-----------|-------|--------|
| Atomic | B02 | <0.01% | ✓ CERTIFIED |
| Atomic | B05 | <0.003% | ✓ CERTIFIED |
| Stellar | B20 | <1% | ✓ CERTIFIED |
| Galactic | B14 | ~2.3% | 🔬 Validating |

## File Locations

- **Headers**: `include/*.hpp` (header-only)
- **CLI Tools**: `tools/*.cpp`  
- **Tests**: `tests/test_calculators.cpp`
- **Build**: `build/tools/Release/` (executables)
- **Docs**: `tools/README.md`
