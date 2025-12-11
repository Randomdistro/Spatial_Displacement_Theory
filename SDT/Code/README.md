# SDT Atomic Properties Calculator

## Build Instructions

### Requirements
- C++20 compiler (MSVC 2022, GCC 11+, or Clang 13+)
- No external dependencies

### Windows (MSVC)
```powershell
cl /std:c++20 /EHsc /O2 demo_atomic_calc.cpp /Fe:sdt_atomic.exe
.\sdt_atomic.exe
```

### Linux/Mac (GCC/Clang)
```bash
g++ -std=c++20 -O3 demo_atomic_calc.cpp -o sdt_atomic
./sdt_atomic
```

## Usage

### As a Library
```cpp
#include "sdt_atomic_properties.hpp"

// Calculate properties for any element
auto props = sdt::calculate_properties(5.1391);  // Na ionization energy

std::cout << "ϟ = " << props.koppa << "\n";
std::cout << "λ = " << props.wavelength_nm << " nm\n";
```

### Standalone Calculator
```cpp
// Multi-ionization sequence
std::vector<double> energies = {5.14, 47.29, 71.62};  // Na: 3s, 2p, 2p
for (double E_i : energies) {
    auto props = sdt::calculate_properties(E_i);
    std::cout << sdt::format_properties(props) << "\n\n";
}
```

## Features

- ✅ Zero lookup tables
- ✅ No empirical constants
- ✅ Pure calculation from fundamental physics
- ✅ Validates energy conservation
- ✅ Predicts recombination photon wavelengths
- ✅ Header-only library (easy integration)
- ✅ `constexpr` calculations (compile-time if needed)

## Output Example

```
SODIUM (3s¹) - Alkali Metal
────────────────────────────────────
E_i:      5.1391 eV
ϟ:        222.97
ϟ²:       49729
v:        1.345e+06 m/s (0.4485% c)
λ_ion:    241.27 nm
Ω:        49729
n_eff:    1.627
Photon λ: 241.27 nm (for recombination)

Quantum defect δ: 1.373
  (n = 3, n_eff = 1.627)
```

## Theory

**Universal formulas implemented:**
```
ϟ = 137 × √(13.6/E_i)
λ = 2λ_C × ϟ²
Ω = ϟ²
v = c/ϟ
```

Where:
- α⁻¹ = 137.036 (fine structure constant)
- Ry = 13.606 eV (Rydberg energy)
- λ_C = 2.426 pm (Compton wavelength)

See `sdt_predictive_algorithm.md` for complete derivation.
