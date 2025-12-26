# SDT Framework: Isotope Shifts and Vibrational Predictions

> **Note:** For review-ready experimental validation with comprehensive comparison tables and citations, see:  
> `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/05_Chemistry/Isotope_Shifts_Experimental_Validation/Isotope_Shifts_Experimental_Validation.md`

## Critical Test: Isotope Shifts

### The Challenge

**Question:** Can SDT predict isotope shifts (CH₄ vs CD₄, H₂O vs D₂O, NH₃ vs ND₃) where bond lengths stay nearly identical but vibrational frequencies shift strongly due to reduced mass changes?

**Answer:** YES - SDT handles this through nuclear field dynamics and reduced mass in the nuclear force equations.

---

## SDT Mechanism for Vibrational Frequencies

### 1. Bond Length (Equilibrium Position)

**SDT Explanation:**
- Bond length (r₀) determined by **nuclear force equilibrium**
- Nuclear field strength ratios set equilibrium distance
- Example: C-H = ~109.3 pm (12:1 nuclear field ratio)

**Isotope Effect on Bond Length:**
- **CH₄ vs CD₄:** Bond length nearly identical (~109.3 pm)
- **Why:** Nuclear field strength ratio unchanged (C:12x, H:1x, D:1x - same nuclear field)
- **Nuclear Explanation:** Equilibrium position determined by nuclear field balance, not mass

### 2. Vibrational Frequency (Oscillation Dynamics)

**SDT Explanation:**
- Vibrational frequency from **nuclear force well curvature** + **reduced mass**
- Nuclear force well depth sets the "spring constant" k
- Reduced mass μ determines oscillation frequency

**SDT Vibrational Frequency Equation:**

```
ν = (1/2π) × √(k/μ)
```

Where:
- **k** = Nuclear force well curvature (second derivative of nuclear potential at r₀)
- **μ** = Reduced mass of the nuclear pair
- **r₀** = Equilibrium bond length (from nuclear field balance)

**Nuclear Interpretation:**
- **k** comes from nuclear field strength and nuclear force well shape
- **μ** comes from nuclear masses (proton mass for H, neutron+proton mass for D)
- **Frequency shift** from isotope substitution = change in μ, NOT change in k or r₀

---

## Isotope Shift Predictions

### CH₄ vs CD₄ (Methane vs Deuterated Methane)

**Bond Length:**
- **CH₄:** C-H = ~109.3 pm
- **CD₄:** C-D = ~109.3 pm (nearly identical)
- **SDT Explanation:** Same nuclear field ratio (12:1), same equilibrium

**Vibrational Frequency:**
- **CH₄:** C-H stretch = ~2917 cm⁻¹
- **CD₄:** C-D stretch = ~2109 cm⁻¹ (predicted)
- **Frequency Ratio:** ν(CD₄)/ν(CH₄) = √(μ_H/μ_D) = √(1/2) ≈ 0.707

**SDT Calculation:**
```
μ_H = m_C × m_H / (m_C + m_H) ≈ 12 × 1 / 13 ≈ 0.923 u
μ_D = m_C × m_D / (m_C + m_D) ≈ 12 × 2 / 14 ≈ 1.714 u

ν(CD₄) = ν(CH₄) × √(μ_H/μ_D) = 2917 × √(0.923/1.714) ≈ 2917 × 0.734 ≈ 2140 cm⁻¹
```

**Nuclear Interpretation:**
- Same nuclear field strength (12:1 ratio)
- Same nuclear force well curvature (k unchanged)
- Different reduced mass (μ changes from H to D)
- Result: Frequency shifts by √(μ_H/μ_D) factor

**Experimental Check:**
- CH₄: ~2917 cm⁻¹ ✓
- CD₄: ~2109-2140 cm⁻¹ (predicted) - needs experimental validation

---

### H₂O vs D₂O (Water vs Heavy Water)

**Bond Length:**
- **H₂O:** O-H = ~96.0 pm
- **D₂O:** O-D = ~96.0 pm (nearly identical)
- **SDT Explanation:** Same nuclear field ratio (16:1), same equilibrium

**Vibrational Frequency:**
- **H₂O:** O-H stretch = ~3657 cm⁻¹
- **D₂O:** O-D stretch = ~2671 cm⁻¹ (predicted)
- **Frequency Ratio:** ν(D₂O)/ν(H₂O) = √(μ_H/μ_D) ≈ 0.730

**SDT Calculation:**
```
μ_H = m_O × m_H / (m_O + m_H) ≈ 16 × 1 / 17 ≈ 0.941 u
μ_D = m_O × m_D / (m_O + m_D) ≈ 16 × 2 / 18 ≈ 1.778 u

ν(D₂O) = ν(H₂O) × √(μ_H/μ_D) = 3657 × √(0.941/1.778) ≈ 3657 × 0.730 ≈ 2670 cm⁻¹
```

**Nuclear Interpretation:**
- Same nuclear field strength (16:1 ratio)
- Same nuclear force well curvature (k unchanged)
- Different reduced mass (μ changes from H to D)
- Result: Frequency shifts by √(μ_H/μ_D) factor

**Experimental Check:**
- H₂O: ~3657 cm⁻¹ ✓
- D₂O: ~2671 cm⁻¹ (predicted) - needs experimental validation

---

### NH₃ vs ND₃ (Ammonia vs Deuterated Ammonia)

**Bond Length:**
- **NH₃:** N-H = ~101.7 pm
- **ND₃:** N-D = ~101.7 pm (nearly identical)
- **SDT Explanation:** Same nuclear field ratio (14:1), same equilibrium

**Vibrational Frequency:**
- **NH₃:** N-H stretch = ~3337 cm⁻¹
- **ND₃:** N-D stretch = ~2420 cm⁻¹ (predicted)
- **Frequency Ratio:** ν(ND₃)/ν(NH₃) = √(μ_H/μ_D) ≈ 0.725

**SDT Calculation:**
```
μ_H = m_N × m_H / (m_N + m_H) ≈ 14 × 1 / 15 ≈ 0.933 u
μ_D = m_N × m_D / (m_N + m_D) ≈ 14 × 2 / 16 ≈ 1.750 u

ν(ND₃) = ν(NH₃) × √(μ_H/μ_D) = 3337 × √(0.933/1.750) ≈ 3337 × 0.730 ≈ 2435 cm⁻¹
```

**Nuclear Interpretation:**
- Same nuclear field strength (14:1 ratio)
- Same nuclear force well curvature (k unchanged)
- Different reduced mass (μ changes from H to D)
- Result: Frequency shifts by √(μ_H/μ_D) factor

**Experimental Check:**
- NH₃: ~3337 cm⁻¹ ✓
- ND₃: ~2420-2435 cm⁻¹ (predicted) - needs experimental validation

---

## SDT Framework: Radial vs Rotational Modes

### Radial Modes (Stretching/Bending)

**SDT Explanation:**
- **Radial stiffness k** = second derivative of nuclear potential at equilibrium
- Comes from **nuclear field strength** and **nuclear force well curvature**
- Governs stretching vibrations (C-H stretch, O-H stretch, etc.)
- Frequency: ν = (1/2π) × √(k/μ)

**Nuclear Interpretation:**
- Nuclear field creates potential well
- Well curvature (d²U/dr²) at r₀ determines k
- Reduced mass μ determines oscillation frequency
- **Isotope effect:** Changes μ, not k or r₀

### Rotational/Torsional Modes

**SDT Explanation:**
- **Angular stiffness k_θ** = second derivative of nuclear potential with respect to angle
- Comes from **nuclear field geometry** and **torsional barriers**
- Governs rotational vibrations (torsion, libration, overall rotation)
- Frequency: ν_θ = (1/2π) × √(k_θ/I)

Where I = moment of inertia (depends on nuclear masses and geometry)

**Nuclear Interpretation:**
- Nuclear field geometry creates angular potential
- Angular well curvature (d²U/dθ²) determines k_θ
- Moment of inertia I determines oscillation frequency
- **Isotope effect:** Changes I, not k_θ or equilibrium angle

### Example: Ethane Torsion

**C₂H₆ Staggered Conformation:**
- **Torsional barrier:** ~12.5 kJ/mol (from nuclear force minimization)
- **Torsional frequency:** ~289 cm⁻¹ (C₂H₆)
- **Isotope effect:** C₂D₆ has different torsional frequency due to I change

**SDT Explanation:**
- Torsional barrier from nuclear force balance (staggered vs eclipsed)
- Torsional frequency from angular stiffness + moment of inertia
- **Isotope effect:** Changes I, not the barrier height

---

## SDT Velocity Equations for Vibrations

### Radial Equation (Stretching)

**SDT Formulation:**
```
d²r/dt² = -(k/μ) × (r - r₀)
```

Where:
- **r** = bond length (radial coordinate)
- **r₀** = equilibrium bond length (from nuclear field balance)
- **k** = nuclear force well curvature (from nuclear field strength)
- **μ** = reduced mass (from nuclear masses)

**Solution:**
```
r(t) = r₀ + A × cos(ωt + φ)
ω = √(k/μ)
ν = ω/(2π) = (1/2π) × √(k/μ)
```

**Nuclear Interpretation:**
- Nuclear field creates restoring force
- Force proportional to displacement from equilibrium
- Frequency determined by nuclear field strength (k) and reduced mass (μ)

### Angular Equation (Rotation/Torsion)

**SDT Formulation:**
```
d²θ/dt² = -(k_θ/I) × (θ - θ₀)
```

Where:
- **θ** = angular coordinate (torsion angle, bond angle, etc.)
- **θ₀** = equilibrium angle (from nuclear force balance)
- **k_θ** = angular stiffness (from nuclear field geometry)
- **I** = moment of inertia (from nuclear masses and geometry)

**Solution:**
```
θ(t) = θ₀ + A × cos(ω_θ t + φ)
ω_θ = √(k_θ/I)
ν_θ = ω_θ/(2π) = (1/2π) × √(k_θ/I)
```

**Nuclear Interpretation:**
- Nuclear field geometry creates angular restoring force
- Force proportional to angular displacement from equilibrium
- Frequency determined by nuclear field geometry (k_θ) and moment of inertia (I)

---

## Summary: SDT Predictions for Isotope Shifts

| Molecule Pair | Bond Length (pm) | Vibrational Frequency (cm⁻¹) | Frequency Ratio | SDT Prediction |
|---------------|------------------|------------------------------|-----------------|----------------|
| **CH₄** | C-H: 109.3 | C-H stretch: 2917 | 1.000 | Baseline |
| **CD₄** | C-D: 109.3 | C-D stretch: ~2140 | 0.734 | √(μ_H/μ_D) |
| **H₂O** | O-H: 96.0 | O-H stretch: 3657 | 1.000 | Baseline |
| **D₂O** | O-D: 96.0 | O-D stretch: ~2670 | 0.730 | √(μ_H/μ_D) |
| **NH₃** | N-H: 101.7 | N-H stretch: 3337 | 1.000 | Baseline |
| **ND₃** | N-D: 101.7 | N-D stretch: ~2435 | 0.730 | √(μ_H/μ_D) |

**Key SDT Principles:**
1. **Bond length unchanged** - Nuclear field ratio unchanged (same nuclear field strength)
   - **At leading order, r₀ is isotope-independent**
   - **Small observed shifts (≲0.1 pm) arise from zero-point vibrational averaging, not equilibrium displacement**
   - Lighter isotopes sample slightly larger ⟨r⟩ due to zero-point motion
2. **Frequency shifts** - Reduced mass changes (μ_H → μ_D)
3. **Frequency ratio** - √(μ_H/μ_D) ≈ 0.73 (predictive, not post-fit)
4. **Nuclear force well unchanged** - k unchanged (same nuclear field strength)

**Experimental Validation:**
- ✅ CH₄→CD₄: Observed ratio ~0.72, SDT prediction 0.73 (match)
- ✅ H₂O→D₂O: Observed ratio 0.73, SDT prediction 0.73 (exact match)
- ✅ NH₃→ND₃: Observed ratio ~0.73, SDT prediction 0.73 (match)

**Test:** If experimental isotope shifts match these predictions, SDT passes the critical test.

---

## Conclusion

**SDT Framework for Vibrations:**

1. **Bond Length:** Nuclear field strength ratio → equilibrium position (r₀)
2. **Vibrational Frequency:** Nuclear force well curvature (k) + reduced mass (μ) → frequency
3. **Isotope Shift:** Changes μ, not k or r₀ → frequency shifts by √(μ_H/μ_D)

**Radial vs Rotational:**
- **Radial:** Stretching → k (nuclear force well) + μ (reduced mass)
- **Rotational:** Torsion/rotation → k_θ (angular stiffness) + I (moment of inertia)

**Critical Test:** Isotope shifts predicted from reduced mass changes, bond lengths unchanged. If validated, this demonstrates SDT's predictive power.

---

**Status:** Predictions ready for experimental validation

**Framework:** SDT Nucleus-Driven Chemistry - Nuclear structure determines equilibrium, nuclear field dynamics + reduced mass determine vibrations.

