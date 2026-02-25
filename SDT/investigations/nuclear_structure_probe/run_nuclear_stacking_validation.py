#!/usr/bin/env python3
"""
Nuclear stacking validation: single source of truth for binding-energy tests.

For each nucleus 2H, 4He, 12C, 14N, 16O (8Be excluded: unstable).
- Computes total occlusion (from Phase 02; corrected when overlap is implemented).
- Computes B_pred = k * Omega (deuteron-calibrated k).
- Compares to experimental binding; asserts error thresholds.

Exit code: 0 if all assertions pass, 1 otherwise (for automation: run -> fix -> re-run).

Thresholds: error must satisfy < 0.08% to pass (all nuclei).
"""

import sys
import importlib.util
from pathlib import Path
from typing import List, Tuple

# Paths
PROBE_ROOT = Path(__file__).resolve().parent
PHASE02 = PROBE_ROOT / "Phase_02_Binding_Energy"


def _load_phase02_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, PHASE02 / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    # Load Phase 02 modules
    mod_02_02 = _load_phase02_module("deuteron", "02_02_deuteron_calibration.py")
    mod_02_03 = _load_phase02_module("alpha", "02_03_alpha_structure.py")
    mod_02_04 = _load_phase02_module("clusters", "02_04_alpha_clusters.py")

    DeuteronCalibration = mod_02_02.DeuteronCalibration
    AlphaParticleStructure = mod_02_03.AlphaParticleStructure
    Carbon12Structure = mod_02_04.Carbon12Structure
    Oxygen16Structure = mod_02_04.Oxygen16Structure
    Beryllium8Structure = mod_02_04.Beryllium8Structure

    # Calibrate k from deuteron
    deut = DeuteronCalibration()
    deut.calculate_occlusion()
    k = deut.calibrate_k()

    # Threshold (percent): error must be < 0.08% to pass
    THRESHOLD_PERCENT = 0.08

    results: List[Tuple[str, float, float, float, bool, float]] = []

    # ----- 2H -----
    B_exp_2H = deut.B_experimental
    B_pred_2H = k * deut.occlusion
    err_2H = abs(B_pred_2H - B_exp_2H) / B_exp_2H * 100.0
    pass_2H = err_2H < THRESHOLD_PERCENT
    results.append(("2H", B_exp_2H, B_pred_2H, err_2H, pass_2H, THRESHOLD_PERCENT))

    # ----- 4He -----
    alpha = AlphaParticleStructure()
    alpha.calculate_total_occlusion()
    B_exp_4He = alpha.B_experimental
    B_pred_4He = k * alpha.total_occlusion
    err_4He = abs(B_pred_4He - B_exp_4He) / B_exp_4He * 100.0
    pass_4He = err_4He < THRESHOLD_PERCENT
    results.append(("4He", B_exp_4He, B_pred_4He, err_4He, pass_4He, THRESHOLD_PERCENT))

    # ----- 12C -----
    c12 = Carbon12Structure()
    c12.calculate_total_occlusion()
    B_exp_12C = c12.B_experimental
    B_pred_12C = c12.predict_binding_energy(k)
    err_12C = abs(B_pred_12C - B_exp_12C) / B_exp_12C * 100.0
    pass_12C = err_12C < THRESHOLD_PERCENT
    results.append(("12C", B_exp_12C, B_pred_12C, err_12C, pass_12C, THRESHOLD_PERCENT))

    # ----- 14N: 3α + p at center; structural prediction (no B_exp_14N fitting) -----
    B_exp_14N = 104.66  # MeV
    omega_14N = mod_02_04.nitrogen14_occlusion(c12.total_occlusion)
    B_pred_14N = k * omega_14N
    err_14N = abs(B_pred_14N - B_exp_14N) / B_exp_14N * 100.0
    pass_14N = err_14N < THRESHOLD_PERCENT
    results.append(("14N", B_exp_14N, B_pred_14N, err_14N, pass_14N, THRESHOLD_PERCENT))

    # ----- 16O -----
    o16 = Oxygen16Structure()
    o16.calculate_total_occlusion()
    B_exp_16O = o16.B_experimental
    B_pred_16O = o16.predict_binding_energy(k)
    err_16O = abs(B_pred_16O - B_exp_16O) / B_exp_16O * 100.0
    pass_16O = err_16O < THRESHOLD_PERCENT
    results.append(("16O", B_exp_16O, B_pred_16O, err_16O, pass_16O, THRESHOLD_PERCENT))

    # ----- 8Be (informational only; unstable, excluded from pass) -----
    be8 = Beryllium8Structure()
    be8.calculate_total_occlusion()
    B_exp_8Be = be8.B_experimental
    B_pred_8Be = be8.predict_binding_energy(k)
    err_8Be = abs(B_pred_8Be - B_exp_8Be) / B_exp_8Be * 100.0
    results.append(("8Be*", B_exp_8Be, B_pred_8Be, err_8Be, True, 0.0))  # * = excluded

    # ----- Report -----
    print("Nuclear stacking validation")
    print("k (deuteron-calibrated) = {:.6f} MeV/sr".format(k))
    print("-" * 72)
    print("{:6s} {:>10s} {:>10s} {:>10s} {:>8s}".format(
        "Nucleus", "B_exp", "B_pred", "err%", "Pass"))
    print("-" * 72)
    all_pass = True
    for name, B_exp, B_pred, err, passed, thresh in results:
        excluded = name.endswith("*")
        status = "PASS" if passed else ("FAIL" if not excluded else "—")
        if not excluded and not passed:
            all_pass = False
        thresh_str = "—" if excluded else "{:.2f}%".format(thresh)
        print("{:6s} {:10.3f} {:10.3f} {:9.2f}% {:>8s} (threshold {})".format(
            name, B_exp, B_pred, err, status, thresh_str))
    print("-" * 72)
    print("Overall:", "PASS" if all_pass else "FAIL")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
