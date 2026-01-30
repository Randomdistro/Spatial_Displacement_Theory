#!/usr/bin/env python3
"""
Phase 1 Test Suite

Runs all Phase 1 tests and validates the nuclear packing geometry foundation.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def run_all_tests():
    """Run all Phase 1 tests"""
    print("="*80)
    print("PHASE 1: NUCLEAR PACKING GEOMETRY FOUNDATION - TEST SUITE")
    print("="*80)
    
    tests = [
        ("1.1 Icosahedral Base Geometry", "01_01_icosahedral_base_geometry", "test_icosahedral_base"),
        ("1.2 First Shell Completion", "01_02_first_shell_completion", "test_first_shell"),
        ("1.3 Second Layer Structure", "01_03_second_layer_structure", "test_second_layer"),
        ("1.4 Higher Shells", "01_04_higher_shells", "test_higher_shells"),
        ("1.5 Geometric Calculations", "01_05_geometric_calculations", "test_geometric_calculations"),
    ]
    
    results = []
    
    for test_name, module_name, test_func_name in tests:
        print(f"\n{'='*80}")
        print(f"Running: {test_name}")
        print('='*80)
        
        try:
            # Import and run test
            module_path = Path(__file__).parent / f"{module_name}.py"
            import importlib.util
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Run test function
            test_func = getattr(module, test_func_name, None)
            if test_func:
                test_func()
                results.append((test_name, "PASSED", None))
            else:
                results.append((test_name, "SKIPPED", "No test function found"))
        
        except Exception as e:
            results.append((test_name, "FAILED", str(e)))
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print('='*80)
    
    passed = sum(1 for _, status, _ in results if status == "PASSED")
    failed = sum(1 for _, status, _ in results if status == "FAILED")
    skipped = sum(1 for _, status, _ in results if status == "SKIPPED")
    
    for test_name, status, error in results:
        status_symbol = "[PASS]" if status == "PASSED" else "[FAIL]" if status == "FAILED" else "[SKIP]"
        print(f"  {status_symbol} {test_name}: {status}")
        if error:
            print(f"      {error}")
    
    print(f"\nTotal: {len(results)} tests")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Skipped: {skipped}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
