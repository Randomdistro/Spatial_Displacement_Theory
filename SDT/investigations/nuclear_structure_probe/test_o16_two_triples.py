#!/usr/bin/env python3
"""
Mathematical test: O-16 as one tetrahedron vs two triples.

Tests whether modeling ¹⁶O as two triangular (3-alpha) units yields a different
inter-alpha occlusion—and thus B_pred—than the single-tetrahedron model.
Uses the same overlap correction (01_05) and constants as 02_04.
"""

import sys
import importlib.util
from pathlib import Path

PROBE_ROOT = Path(__file__).resolve().parent
PHASE01 = PROBE_ROOT / "Phase_01_Nuclear_Packing"
PHASE02 = PROBE_ROOT / "Phase_02_Binding_Energy"

# Load 01_05 (overlap correction)
geom05_path = PHASE01 / "01_05_geometric_calculations.py"
spec = importlib.util.spec_from_file_location("geom05", geom05_path)
geom05 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geom05)

# Load 01_03 (O-16 and C-12 positions)
geom03_path = PHASE01 / "01_03_second_layer_structure.py"
spec = importlib.util.spec_from_file_location("geom03", geom03_path)
geom03 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geom03)

# Load 02_02 (k), 02_03 (alpha internal occlusion), 02_04 (constants)
deut_path = PHASE02 / "02_02_deuteron_calibration.py"
spec = importlib.util.spec_from_file_location("deut", deut_path)
deut = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deut)

alpha_path = PHASE02 / "02_03_alpha_structure.py"
spec = importlib.util.spec_from_file_location("alpha_mod", alpha_path)
alpha_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alpha_mod)

# Constants from 02_04 (must match NUCLEAR_CONSTANTS / 02_04)
R_INTER_ALPHA_BASE_FM = 0.70
R_INTER_ALPHA_BETA = 0.2747
B_O16_EXP = 127.619  # MeV


def geometric_center(positions):
    n = len(positions)
    cx = sum(p[0] for p in positions) / n
    cy = sum(p[1] for p in positions) / n
    cz = sum(p[2] for p in positions) / n
    return (cx, cy, cz)


def R_triangle():
    return R_INTER_ALPHA_BASE_FM


def R_tetrahedron():
    return R_INTER_ALPHA_BASE_FM * (1.0 + R_INTER_ALPHA_BETA)


def main():
    # O-16 tetrahedron: 4 alpha positions (same as Oxygen16Arrangement)
    o16 = geom03.Oxygen16Arrangement()
    positions_4 = o16.get_alpha_positions()
    assert len(positions_4) == 4, "O-16 must have 4 positions"

    # --- Model A: one tetrahedron (current code) ---
    center_tet = geometric_center(positions_4)
    Omega_inter_tetrahedron = geom05.corrected_total_occlusion(
        center_tet, positions_4, R_tetrahedron()
    )

    # --- Model B: two triples (two triangles sharing edge 0-1) ---
    # Triple 1: alphas 0, 1, 2 (one face of tetrahedron)
    # Triple 2: alphas 0, 1, 3 (face sharing edge 0-1)
    triple1 = [positions_4[0], positions_4[1], positions_4[2]]
    triple2 = [positions_4[0], positions_4[1], positions_4[3]]
    center1 = geometric_center(triple1)
    center2 = geometric_center(triple2)

    Omega_triple1 = geom05.corrected_total_occlusion(
        center1, triple1, R_triangle()
    )
    Omega_triple2 = geom05.corrected_total_occlusion(
        center2, triple2, R_triangle()
    )
    # Shared alphas (0 and 1) are counted in both triples; subtract once.
    shared_positions = [positions_4[0], positions_4[1]]
    Omega_shared = geom05.corrected_total_occlusion(
        center1, shared_positions, R_triangle()
    )
    Omega_inter_two_triples = Omega_triple1 + Omega_triple2 - Omega_shared

    # Internal occlusion (same for both: 4 alphas)
    alpha_s = alpha_mod.AlphaParticleStructure()
    alpha_s.calculate_total_occlusion()
    internal_total = 4.0 * alpha_s.total_occlusion

    # Total occlusion and B_pred
    Omega_total_tet = internal_total + Omega_inter_tetrahedron
    Omega_total_two_triples = internal_total + Omega_inter_two_triples

    deut_cal = deut.DeuteronCalibration()
    deut_cal.calculate_occlusion()
    k = deut_cal.calibrate_k()

    B_pred_tet = k * Omega_total_tet
    B_pred_two_triples = k * Omega_total_two_triples

    err_tet = abs(B_pred_tet - B_O16_EXP) / B_O16_EXP * 100.0
    err_two_triples = abs(B_pred_two_triples - B_O16_EXP) / B_O16_EXP * 100.0

    # --- Report ---
    print("O-16: Tetrahedron vs Two Triples (mathematical test)")
    print("=" * 60)
    print(f"B_exp(O-16) = {B_O16_EXP:.3f} MeV")
    print(f"k (deuteron) = {k:.6f} MeV/sr")
    print()
    print("Model A — One tetrahedron (4 alphas, 6 pairs, center observer):")
    print(f"  Omega_inter = {Omega_inter_tetrahedron:.6f} sr")
    print(f"  Omega_total = {Omega_total_tet:.6f} sr")
    print(f"  B_pred      = {B_pred_tet:.3f} MeV")
    print(f"  error       = {err_tet:.2f}%")
    print()
    print("Model B — Two triples (triple1: 0,1,2; triple2: 0,1,3; R_triangle):")
    print(f"  Omega_triple1 = {Omega_triple1:.6f} sr")
    print(f"  Omega_triple2 = {Omega_triple2:.6f} sr")
    print(f"  Omega_shared  = {Omega_shared:.6f} sr (subtract once)")
    print(f"  Omega_inter   = {Omega_inter_two_triples:.6f} sr")
    print(f"  Omega_total   = {Omega_total_two_triples:.6f} sr")
    print(f"  B_pred        = {B_pred_two_triples:.3f} MeV")
    print(f"  error         = {err_two_triples:.2f}%")
    print()
    print("Conclusion:")
    if err_two_triples < err_tet:
        print(f"  Two-triples model is closer to B_exp by {err_tet - err_two_triples:.2f}% error.")
    elif err_two_triples > err_tet:
        print(f"  Tetrahedron model is closer to B_exp by {err_two_triples - err_tet:.2f}% error.")
    else:
        print("  Both models give the same error.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
