# SDT Atomic Properties Calculator (.NET)

## Build and Run

### Prerequisites
- .NET 8.0 SDK or later

### Quick Start
```powershell
cd code\dotnet
dotnet run
```

### Build Only
```powershell
dotnet build
```

### Run Executable
```powershell
dotnet run --configuration Release
```

## Features
- ✅ Pure C# .NET implementation
- ✅ No external dependencies
- ✅ Cross-platform (Windows, Linux, macOS)
- ✅ Zero lookup tables
- ✅ Calculates all atomic properties from ionization energy

## Usage as Library

```csharp
using SDT.AtomicProperties;

// Calculate properties for any element
var props = AtomicProperties.Calculate(5.1391);  // Sodium

Console.WriteLine($"ϟ = {props.Koppa}");
Console.WriteLine($"λ = {props.WavelengthNm} nm");
Console.WriteLine($"Ω = {props.PhaseSpace}");
```

## Output Example

```
SODIUM (3s¹) - Alkali Metal
────────────────────────────────────
E_i:      5.1391 eV
ϟ:        222.97
ϟ²:       49729
v:        1.345E+06 m/s (0.4485% c)
λ_ion:    241.27 nm
Ω:        49729
n_eff:    1.627

Quantum defect δ: 1.373
  (n = 3, n_eff = 1.627)
```

## Theory
Universal formulas:
- `ϟ = 137 × √(13.6/E_i)`
- `λ = 2λ_C × ϟ²`
- `Ω = ϟ²` (phase space volume)
