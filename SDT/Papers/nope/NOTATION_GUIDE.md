# De Rerum Todo Existens: Unified Notation Guide

**Purpose:** Standardize all symbols, terminology, and equation numbering across the complete principia.

---

## Symbol Standardization

### Fundamental Quantities

**Space and Medium:**
- **Spation:** The incompressible medium filling space (always use "spation" not "spation medium")
- **K_bulk:** Bulk modulus of spation [Pa] = 4.6×10¹¹³ Pa
- **ρ_s:** Spation density [kg/m³] = K_bulk/c²
- **r_P:** Planck radius [m] = 1.616255×10⁻³⁵ m
- **c:** Speed of light (EM propagation limit) [m/s] = 2.99792458×10⁸ m/s

**Matter and Displacement:**
- **V_disp:** Displacement volume [m³] - volume of spation excluded by particle
- **R_e:** Electron exclusion radius [m] ≈ 10⁻²¹ m
- **R_p:** Proton radius [m] = 8.4×10⁻¹⁶ m
- **ρ_disp(x):** Displacement density [dimensionless or m⁻³]
- **Δ(x):** Displacement potential [m] or [dimensionless]

**Pressure and Forces:**
- **Π(x):** Pressure field [Pa] - primary symbol for pressure
- **P:** Used only for power [W] or when Π is ambiguous
- **p:** Used only for momentum [kg·m/s]
- **F:** Force [N]
- **∇Π:** Pressure gradient [Pa/m]

**Occlusion:**
- **E(x,n̂):** Occlusion function [dimensionless] - directional shadowing
- **ε:** Use only for permittivity or strain, NOT occlusion
- **ξ:** Screening factor [dimensionless] ≈ 10⁻⁹

**Movement and Shunts:**
- **ν:** Frequency [Hz] - primary symbol (not f)
- **f:** Use only for force per unit area or function notation
- **ω:** Angular frequency [rad/s] = 2πν
- **v:** Velocity [m/s] - particle velocity
- **u:** Displacement field [m] or velocity field [m/s] in continuum mechanics
- **Shunt:** Always use "shunt" or "shunt event" (not "shunting")

**Time:**
- **t:** Time [s] - coordinate time
- **τ:** Proper time [s] or period [s]
- **T:** Temperature [K] or period [s] (context-dependent)
- **N:** Number of shunts or oscillations [dimensionless]

**Energy and Related:**
- **E:** Energy [J] - total energy
- **U:** Internal energy [J] - thermodynamic
- **W:** Work [J]
- **Q:** Heat [J]
- **S:** Entropy [J/K] or action [J·s] (context-dependent)

**Geometry:**
- **r:** Radial distance [m]
- **R:** Radius [m] - characteristic radius
- **a₀:** Bohr radius [m] = 5.29177210903×10⁻¹¹ m
- **λ:** Wavelength [m] or decay constant [s⁻¹] (context-dependent)
- **λ_C:** Compton wavelength [m] = h/(mc)

**Constants:**
- **h:** Planck constant [J·s] = 6.62607015×10⁻³⁴ J·s
- **ℏ:** Reduced Planck constant [J·s] = h/(2π)
- **k_B:** Boltzmann constant [J/K] = 1.380649×10⁻²³ J/K
- **e:** Elementary charge [C] = 1.602176634×10⁻¹⁹ C
- **α:** Fine structure constant [dimensionless] = 7.2973525693×10⁻³
- **G:** Gravitational constant [m³/(kg·s²)] - used only for comparison, not in SDT
- **β:** Gravitational parameter [m³/s²] - replaces GM in SDT
- **κ:** Geometric efficiency factor [dimensionless] ≈ 1
- **Ϟ (Kappa):** Velocity factor Ϟ = c/v_surface
- **ϟ (Koppa):** c-boundary position ϟ = R/Ϟ²

---

## Equation Numbering System

### Format: Volume.Book.Chapter.Section.Equation

**Example:** I.1.3.5.2 means:
- Volume I (Foundations)
- Book 1 (The Four Ingredients)
- Chapter 3 (Movement)
- Section 5 (Single Shunt Quantification)
- Equation 2

**Master Equation:** I.2.1.1.1 (Volume I, Book 2, Chapter 1, Section 1, Equation 1)

**Cross-References:**
- Within same volume: "See equation (1.3.5.2)" or "As shown in (I.1.3.5.2)"
- Different volume: "See equation (II.4.2.3.1)" or "As derived in Volume II, equation (2.4.2.3.1)"

---

## Terminology Standardization

### Core Concepts

**Spation:**
- Always: "spation" (not "spation medium", "spation lattice" only when referring to discrete structure)
- Definition: The incompressible, deformable medium that fills all space

**Displacement:**
- Use "displacement" for the geometric exclusion of spation
- Use "displacement volume" for V_disp
- Use "displacement density" for ρ_disp
- Avoid "exclusion" except when specifically contrasting with "inclusion"

**Shunt:**
- Always: "shunt" or "shunt event"
- Definition: Micro-collision between particle boundary and spation
- Use "shunt dynamics" for the mechanism
- Use "shunt frequency" for ν_shunt
- Avoid "shunting" as a verb

**Occlusion:**
- Always: "occlusion" or "occlusion function E(x,n̂)"
- Definition: Directional shadowing that reduces pressure
- Use "mutual occlusion" for E→1 limit (gravity)
- Use "negligible occlusion" for E→0 limit (Coulomb)

**Vortex:**
- Use "toroidal vortex" for particle structure
- Use "vortex geometry" for particle shape
- Use "helical wake" for the pressure pattern created by moving vortices

### Force Terminology

**Coulomb Force:**
- "Coulomb attraction" or "electrostatic force"
- Always note: "E→0 limit of pressure gradient"

**Gravitational Force:**
- "Gravitational acceleration" or "gravity"
- Always note: "E→1 limit of pressure gradient"

**Strong Force:**
- "Baryonic confinement" or "nuclear binding"
- Always note: "Confinement pressure at femtoscale"

### Scale Terminology

**Atomic Scale:** 10⁻¹⁰ m (Bohr radius scale)
**Nuclear Scale:** 10⁻¹⁵ m (femtoscale)
**Planetary Scale:** 10⁹ m (Earth radius)
**Stellar Scale:** 10¹² m (solar radius)
**Galactic Scale:** 10²¹ m (kiloparsec)
**Cosmological Scale:** 10²⁶ m (gigaparsec)

---

## Mathematical Notation

### Operators

- **∇:** Gradient operator
- **∇·:** Divergence operator
- **∇×:** Curl operator
- **∇²:** Laplacian operator
- **∂/∂t:** Partial time derivative
- **d/dt:** Total time derivative
- **∫:** Integral
- **Σ:** Summation
- **∏:** Product

### Vectors and Tensors

- **Bold lowercase:** Vectors (v, F, E, B)
- **Bold uppercase:** Matrices or tensor fields (when needed)
- **Hat notation:** Unit vectors (r̂, n̂, ẑ)
- **Arrow notation:** Avoid - use bold instead

### Functions

- **Standard:** f(x), g(t), etc.
- **Special functions:** Use standard notation (sin, cos, exp, ln, log)
- **Probability:** Use ρ for density, P for probability (context-dependent)

### Sets and Spaces

- **ℝ:** Real numbers
- **ℂ:** Complex numbers
- **ℤ:** Integers
- **ℕ:** Natural numbers

---

## Units and Dimensions

### Base Units (SI)

- **Length:** meter [m]
- **Mass:** kilogram [kg]
- **Time:** second [s]
- **Current:** ampere [A]
- **Temperature:** kelvin [K]
- **Amount:** mole [mol]
- **Luminous intensity:** candela [cd]

### Derived Units

- **Force:** newton [N] = kg·m/s²
- **Energy:** joule [J] = N·m = kg·m²/s²
- **Power:** watt [W] = J/s
- **Pressure:** pascal [Pa] = N/m² = kg/(m·s²)
- **Frequency:** hertz [Hz] = s⁻¹
- **Charge:** coulomb [C] = A·s

### Dimensional Analysis

Always include dimensional checks:
- [Quantity] = [dimension]
- Example: [F] = [N] = [kg·m/s²] ✓

---

## Cross-Reference Format

### Internal References

**To sections:**
- "See Section I.1.3" or "As discussed in Chapter 3"
- "See Volume II, Book 4, Chapter 2"

**To equations:**
- "Equation (I.2.1.1.1)" or "As shown in (2.1.1.1)"
- "From equation (I.1.3.5.2), we find..."

**To figures:**
- "Figure I.1.2" or "See Figure 1.2 in Volume I"

**To tables:**
- "Table I.3.1" or "As shown in Table 3.1"

**To benchmarks:**
- "Benchmark B02" or "As validated in B02 (Rydberg Formula)"

**To phase documents:**
- "See Phase 1 (Coulomb Force)" or "As derived in Phase 15"
- Include file reference: "Phase_1_Coulomb_Force.md"

---

## Special Notation

### Limits

- **E→0:** Negligible occlusion (Coulomb limit)
- **E→1:** Strong occlusion (gravitational limit)
- **r→0:** Approach to origin
- **r→∞:** Far-field limit

### Approximations

- **≈:** Approximately equal
- **~:** Order of magnitude
- **≪:** Much less than
- **≫:** Much greater than
- **∝:** Proportional to

### Boxed Equations

Use \boxed{} for:
- Master equations
- Final results
- Key formulas
- Certified benchmark results

---

## Implementation Notes

1. **Apply this guide** during compilation of each volume
2. **Update symbols** to match this guide where conflicts exist
3. **Add to glossary** any new symbols introduced
4. **Verify consistency** in final integration phase

---

**End of Notation Guide**

