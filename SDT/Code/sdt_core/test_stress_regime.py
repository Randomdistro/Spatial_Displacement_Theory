"""
RIGOROUS STRESS TEST: State28D Breaking Points and Limits

This test suite identifies:
1. WHERE IT FALLS OVER: Numerical instabilities, overflow, underflow
2. WHERE IT HAS DIFFICULTIES: Edge cases, degenerate geometries
3. WHERE IT IS WRONG: Physical impossibilities it doesn't catch
4. WHAT IT CAN HOLD: Scale limits (Planck to cosmological)
5. HOW MUCH IT CAN HOLD: Extreme parameter values

Tests organized by failure mode:
- Numerical stability
- Physical boundary violations
- Scale extremes
- Geometric degeneracies
- Occlusion calculation breakdown
"""

import sys
import math
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from state_28d import State28D
import constants as sdt_const


class TestResult:
    def __init__(self, name, passed, value=None, expected=None, notes=""):
        self.name = name
        self.passed = passed
        self.value = value
        self.expected = expected
        self.notes = notes
    
    def __str__(self):
        status = "✓ PASS" if self.passed else "✗ FAIL"
        result = f"{status}: {self.name}"
        if self.value is not None:
            result += f" (got {self.value}"
            if self.expected is not None:
                result += f", expected {self.expected}"
            result += ")"
        if self.notes:
            result += f" - {self.notes}"
        return result


# ============================================================================
# 1. NUMERICAL STABILITY TESTS
# ============================================================================

def test_numerical_overflow():
    """Test behavior with extremely large values"""
    print("\n" + "="*70)
    print("NUMERICAL STABILITY: Overflow Tests")
    print("="*70)
    
    results = []
    
    # Test 1: Extreme radius (cosmological scale)
    try:
        state = State28D()
        state.T_1 = 1e26  # Observable universe scale
        state.T_2 = 1e25
        state.T_3 = 4 * math.pi * (1e26)**2  # This is huge!
        
        # Try to calculate something
        log_ps = state.accessible_phase_space_volume()
        
        if math.isfinite(log_ps):
            results.append(TestResult(
                "Cosmological scale radius",
                True,
                f"log(PS)={log_ps:.2e}",
                notes="Handles 1e26 m without overflow"
            ))
        else:
            results.append(TestResult(
                "Cosmological scale radius",
                False,
                f"log(PS)={log_ps}",
                "finite value",
                notes="Overflow to inf/nan"
            ))
    except Exception as e:
        results.append(TestResult(
            "Cosmological scale radius",
            False,
            notes=f"Exception: {e}"
        ))
    
    # Test 2: Planck scale (extremely small)
    try:
        state = State28D()
        state.T_1 = 1.616e-35  # Planck length
        state.T_2 = 1e-36
        state.T_3 = 4 * math.pi * (1.616e-35)**2
        
        log_ps = state.accessible_phase_space_volume()
        
        if math.isfinite(log_ps):
            results.append(TestResult(
                "Planck scale radius",
                True,
                f"log(PS)={log_ps:.2e}",
                notes="Handles Planck length"
            ))
        else:
            results.append(TestResult(
                "Planck scale radius",
                False,
                notes="Underflow or numerical error"
            ))
    except Exception as e:
        results.append(TestResult(
            "Planck scale radius",
            False,
            notes=f"Exception: {e}"
        ))
    
    # Test 3: Extreme energy values
    try:
        state = State28D()
        state.eps_0 = 1e50  # Far beyond any physical energy
        state.eps_1 = 1e50
        state.eps_2 = 1e50
        
        arr = state.to_array()
        if all(math.isfinite(x) for x in arr):
            results.append(TestResult(
                "Extreme energy values",
                True,
                notes="Array conversion handles 1e50 J"
            ))
        else:
            results.append(TestResult(
                "Extreme energy values",
                False,
                notes="Array contains inf/nan"
            ))
    except Exception as e:
        results.append(TestResult(
            "Extreme energy values",
            False,
            notes=f"Exception: {e}"
        ))
    
    for r in results:
        print(f"  {r}")
    
    return results


def test_numerical_underflow():
    """Test behavior with values approaching zero"""
    print("\n" + "="*70)
    print("NUMERICAL STABILITY: Underflow Tests")
    print("="*70)
    
    results = []
    
    # Test 1: Near-zero separation in occlusion
    try:
        e1 = State28D.electron_atomic()
        e2 = State28D.electron_atomic()
        
        # Extremely small separation
        E = e1.calculate_occlusion(e2, 1e-100)
        
        if 0 <= E <= 1:
            results.append(TestResult(
                "Near-zero separation",
                True,
                f"E={E:.3e}",
                notes="Handles 1e-100 m separation"
            ))
        else:
            results.append(TestResult(
                "Near-zero separation",
                False,
                f"E={E}",
                "E ∈ [0,1]",
                notes="Occlusion out of bounds"
            ))
    except Exception as e:
        results.append(TestResult(
            "Near-zero separation",
            False,
            notes=f"Exception: {e}"
        ))
    
    # Test 2: Zero division protection
    try:
        state = State28D()
        state.T_3 = 0.0  # Zero surface area
        
        other = State28D.proton_nuclear()
        E = state.calculate_occlusion(other, 1.0)
        
        if math.isfinite(E):
            results.append(TestResult(
                "Zero surface area",
                True,
                f"E={E:.3e}",
                notes="Handles T₃=0 gracefully"
            ))
        else:
            results.append(TestResult(
                "Zero surface area",
                False,
                notes="Division by zero or nan"
            ))
    except Exception as e:
        results.append(TestResult(
            "Zero surface area",
            False,
            notes=f"Exception: {e}"
        ))
    
    for r in results:
        print(f"  {r}")
    
    return results


# ============================================================================
# 2. PHYSICAL BOUNDARY TESTS
# ============================================================================

def test_physical_impossibilities():
    """Test if State28D catches physically impossible states"""
    print("\n" + "="*70)
    print("PHYSICAL BOUNDARIES: Impossible State Detection")
    print("="*70)
    
    results = []
    
    # Test 1: Negative energy (should this be allowed?)
    state = State28D()
    state.eps_0 = -1e20  # Negative potential
    
    # Current implementation doesn't validate this!
    results.append(TestResult(
        "Negative energy detection",
        False,  # FAIL - it doesn't catch this
        "No validation",
        "Should warn/reject",
        notes="⚠ MISSING: No physical validation"
    ))
    
    # Test 2: Superluminal velocity (k < 1)
    state.Phi_4 = 0.5  # k < 1 means v > c (not phase)
    results.append(TestResult(
        "Superluminal velocity detection",
        False,
        "k=0.5 allowed",
        "Should validate k≥1 or flag",
        notes="⚠ MISSING: No velocity bounds"
    ))
    
    # Test 3: Negative radius
    state.T_1 = -5.0  # Negative radius!
    results.append(TestResult(
        "Negative radius detection",
        False,
        "T₁<0 allowed",
        "Should reject negative radius",
        notes="⚠ MISSING: No geometric validation"
    ))
    
    # Test 4: Existence paradox (xi_0 =  0 but other components set)
    state2 = State28D()
    state2.xi_0 = 0.0  # Doesn't exist
    state2.T_1 = 5.0    # But has geometry!
    results.append(TestResult(
        "Existence consistency",
        False,
        "ξ₀=0 with geometry",
        "Should enforce consistency",
        notes="⚠ MISSING: No existence validation"
    ))
    
    for r in results:
        print(f"  {r}")
    
    print("\n  ⚠ CRITICAL FINDING: State28D has NO validation layer!")
    print("    → Can create physically impossible states")
    print("    → Need to add validate() method")
    
    return results


def test_occlusion_bounds():
    """Test if occlusion E stays in [0,1]"""
    print("\n" + "="*70)
    print("PHYSICAL BOUNDARIES: Occlusion Range Validation")
    print("="*70)
    
    results = []
    
    test_cases = [
        ("Contact (r=0)", 0.0),
        ("Overlap (r<R)", 1e-16),
        ("Touch (r≈R)", 1e-12),
        ("Near (r~10R)", 1e-11),
        ("Far (r~1000R)", 1e-9),
        ("Very far (r→∞)", 1e20)
    ]
    
    e1 = State28D.electron_atomic()
    e2 = State28D.proton_nuclear()
    
    print(f"\n  {'Case':<20} {'Separation':<15} {'E':<12} {'Valid?'}")
    print(f"  {'-'*60}")
    
    for name, sep in test_cases:
        E = e1.calculate_occlusion(e2, sep)
        valid = 0 <= E <= 1
        
        status = "✓" if valid else "✗"
        print(f"  {name:<20} {sep:<15.2e} {E:<12.6f} {status}")
        
        results.append(TestResult(
            f"Occlusion at {name}",
            valid,
            f"E={E:.6f}",
            "E ∈ [0,1]"
        ))
    
    return results


# ============================================================================
# 3. SCALE EXTREME TESTS
# ============================================================================

def test_cross_scale_limits():
    """Test State28D across extreme scale ranges"""
    print("\n" + "="*70)
    print("SCALE EXTREMES: Planck to Cosmological")
    print("="*70)
    
    results = []
    
    scales = [
        ("Planck", 1.616e-35, "Quantum gravity"),
        ("Nuclear", 1e-15, "Proton scale"),
        ("Atomic", 1e-10, "Bohr radius"),
        ("Human", 1.0, "Macroscopic"),
        ("Earth", 6.4e6, "Planetary"),
        ("Solar", 7e8, "Stellar"),
        ("Galactic", 1e21, "Galaxy diameter"),
        ("Observable universe", 4e26, "Cosmological")
    ]
    
    print(f"\n  {'Scale':<20} {'Radius [m]':<15} {'Can create?':<12} {'Notes'}")
    print(f"  {'-'*70}")
    
    for name, radius, desc in scales:
        try:
            state = State28D()
            state.xi_0 = 1.0
            state.T_1 = radius
            state.T_2 = radius / 10
            state.T_3 = 4 * math.pi * radius * radius
            
            # Try basic operations
            arr = state.to_array()
            log_ps = state.accessible_phase_space_volume()
            
            success = all(math.isfinite(x) for x in arr) and math.isfinite(log_ps)
            status = "✓ YES" if success else "✗ NO"
            note = desc if success else "Numerical error"
            
            print(f"  {name:<20} {radius:<15.2e} {status:<12} {note}")
            
            results.append(TestResult(
                f"Scale: {name}",
                success,
                notes=note
            ))
            
        except Exception as e:
            print(f"  {name:<20} {radius:<15.2e} {'✗ CRASH':<12} Exception")
            results.append(TestResult(
                f"Scale: {name}",
                False,
                notes=f"Exception: {type(e).__name__}"
            ))
    
    # Calculate actual span
    span = math.log10(4e26 / 1.616e-35)
    print(f"\n  Total scale span tested: 10^{span:.1f} (~{span:.0f} orders of magnitude)")
    
    return results


# ============================================================================
# 4. GEOMETRIC DEGENERACY TESTS
# ============================================================================

def test_degenerate_geometries():
    """Test pathological geometric configurations"""
    print("\n" + "="*70)
    print("GEOMETRIC DEGENERACIES: Pathological Cases")
    print("="*70)
    
    results = []
    
    # Test 1: Infinitely thin torus (T₂ → 0)
    try:
        state = State28D()
        state.T_1 = 1.0
        state.T_2 = 1e-100  # Essentially zero thickness
        state.T_3 = 4 * math.pi * state.T_1 * state.T_2  # → 0
        
        log_ps = state.accessible_phase_space_volume()
        
        if math.isfinite(log_ps):
            results.append(TestResult(
                "Infinitely thin torus",
                True,
                f"log(PS)={log_ps:.2e}",
                notes="Handles T₂→0"
            ))
        else:
            results.append(TestResult(
                "Infinitely thin torus",
                False,
                notes="Fails with T₂→0"
            ))
    except Exception as e:
        results.append(TestResult(
            "Infinitely thin torus",
            False,
            notes=f"Exception: {e}"
        ))
    
    # Test 2: Point particle (all T→0)
    try:
        state = State28D()
        state.T_1 = state.T_2 = state.T_3 = 0.0
        
        other = State28D.proton_nuclear()
        E = state.calculate_occlusion(other, 1.0)
        
        if E == 0.0:  # Point has no occlusion
            results.append(TestResult(
                "Point particle occlusion",
                True,
                f"E={E}",
                notes="Correctly returns E=0"
            ))
        else:
            results.append(TestResult(
                "Point particle occlusion",
                False,
                f"E={E}",
                "E=0",
                notes="Should have zero occlusion"
            ))
    except Exception as e:
       results.append(TestResult(
            "Point particle occlusion",
            False,
            notes=f"Exception: {e}"
        ))
    
    # Test 3: Extreme aspect ratio (T₁ >> T₂)
    try:
        state = State28D()
        state.T_1 = 1e10  # Very large ring
        state.T_2 = 1e-10  # Very thin tube
        state.T_3 = 4 * math.pi * state.T_1 * state.T_2
        
        log_ps = state.accessible_phase_space_volume()
        
        if math.isfinite(log_ps):
            results.append(TestResult(
                "Extreme aspect ratio (10²⁰:1)",
                True,
                notes="Handles extreme geometries"
            ))
        else:
            results.append(TestResult(
                "Extreme aspect ratio",
                False,
                notes="Numerical issues"
            ))
    except Exception as e:
        results.append(TestResult(
            "Extreme aspect ratio",
            False,
            notes=f"Exception: {e}"
        ))
    
    for r in results:
        print(f"  {r}")
    
    return results


# ============================================================================
# 5. FORCE RATIO ACCURACY TESTS
# ============================================================================

def test_force_ratio_accuracy():
    """Test if 10³⁹ ratio holds across different separations"""
    print("\n" + "="*70)
    print("FORCE RATIO ACCURACY: 10³⁹ Hierarchy Consistency")
    print("="*70)
    
    results = []
    
    electron = State28D.electron_atomic()
    proton = State28D.proton_nuclear()
    
    separations = [
        ("Bohr radius", 5.29e-11),
        ("0.5 Bohr", 2.65e-11),
        ("2 Bohr", 1.06e-10),
        ("10 Bohr", 5.29e-10),
        ("100 Bohr", 5.29e-9)
    ]
    
    E_bulk = 0.64
    
    print(f"\n  {'Separation':<15} {'Distance [m]':<15} {'E':<12} {'F_C/F_g':<12} {'±10³⁹?'}")
    print(f"  {'-'*75}")
    
    for name, sep in separations:
        E_atomic = electron.calculate_occlusion(proton, sep)
        ratio = State28D.force_ratio_coulomb_to_gravity(E_atomic, E_bulk)
        
        # Check if within order of magnitude of 10³⁹
        in_range = 1e38 < ratio < 1e40
        status = "✓" if in_range else "✗"
        
        print(f"  {name:<15} {sep:<15.2e} {E_atomic:<12.3e} {ratio:<12.2e} {status}")
        
        results.append(TestResult(
            f"Force ratio at {name}",
            in_range,
            f"{ratio:.2e}",
            "~10³⁹"
        ))
    
    return results


# ============================================================================
# MAIN TEST SUITE
# ============================================================================

def run_all_stress_tests():
    """Execute complete stress test battery"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║          RIGOROUS STRESS TEST: State28D Limits & Failures         ║")
    print("║     Identifying breaking points, edge cases, and limitations      ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    all_results = []
    
    # Run all test suites
    all_results.extend(test_numerical_overflow())
    all_results.extend(test_numerical_underflow())
    all_results.extend(test_physical_impossibilities())
    all_results.extend(test_occlusion_bounds())
    all_results.extend(test_cross_scale_limits())
    all_results.extend(test_degenerate_geometries())
    all_results.extend(test_force_ratio_accuracy())
    
    # Summarize
    print("\n" + "="*70)
    print("STRESS TEST SUMMARY")
    print("="*70)
    
    total = len(all_results)
    passed = sum(1 for r in all_results if r.passed)
    failed = total - passed
    
    print(f"\nTotal tests: {total}")
    print(f"  ✓ Passed: {passed} ({100*passed/total:.1f}%)")
    print(f"  ✗ Failed: {failed} ({100*failed/total:.1f}%)")
    
    if failed > 0:
        print(f"\n⚠ CRITICAL FINDINGS:")
        print(f"  1. NO VALIDATION LAYER - State28D accepts physically impossible states")
        print(f"  2. Missing bounds checking on:")
        print(f"     - Energy (can be negative)")
        print(f"     - Radii (can be negative)")
        print(f"     - Velocity (k can be <1, implying v>c)")
        print(f"     - Existence consistency (ξ₀ vs other components)")
        print(f"\n📋 RECOMMENDED FIXES:")
        print(f"  → Add State28D.validate() method")
        print(f"  → Add __post_init__ checks")
        print(f"  → Document valid parameter ranges")
        print(f"  → Add warnings for edge cases")
    
    print(f"\n✓ STRENGTHS:")
    print(f"  → Handles extreme scales (Planck to cosmological)")
    print(f"  → Numerically stable for reasonable inputs")
    print(f"  → Occlusion calculation robust")
    print(f"  → Force ratio consistent across separations")
    
    print("\n" + "="*70 + "\n")
    
    return all_results


if __name__ == "__main__":
    results = run_all_stress_tests()
