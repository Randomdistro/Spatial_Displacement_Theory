#!/usr/bin/env python3
"""
Locate underperformance: where B_pred < B_exp and by how much.
Outputs nucleus, shortfall (MeV), shortfall in Omega (sr), and responsible term.
"""

import sys
import importlib.util
from pathlib import Path

PROBE_ROOT = Path(__file__).resolve().parent
PHASE02 = PROBE_ROOT / "Phase_02_Binding_Energy"


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, PHASE02 / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    mod_02_02 = load("deut", "02_02_deuteron_calibration.py")
    mod_02_03 = load("alpha", "02_03_alpha_structure.py")
    mod_02_04 = load("clusters", "02_04_alpha_clusters.py")
    calc = load("calc", "02_01_occlusion_binding_calculator.py")

    deut = mod_02_02.DeuteronCalibration()
    deut.calculate_occlusion()
    k = deut.calibrate_k()

    B_exp_14N = 104.66  # MeV
    c12 = mod_02_04.Carbon12Structure()
    c12.calculate_total_occlusion()
    omega_14N = mod_02_04.nitrogen14_occlusion(c12.total_occlusion)
    B_pred_14N = k * omega_14N

    shortfall_MeV = B_exp_14N - B_pred_14N
    shortfall_sr = shortfall_MeV / k

    R_tetra = mod_02_04._inter_alpha_sphere_radius("tetrahedron")
    d_center = mod_02_04.D_CENTER_TRIANGLE_FM
    omega_per_alpha = calc.spherical_occlusion(R_tetra, d_center)
    extra_current = 3.0 * omega_per_alpha

    print("Underperformance (B_pred < B_exp)")
    print("=" * 60)
    print("Nucleus: 14N")
    print("  B_exp       = {:.3f} MeV".format(B_exp_14N))
    print("  B_pred      = {:.3f} MeV".format(B_pred_14N))
    print("  Shortfall   = {:.4f} MeV ({:.2f}%)".format(
        shortfall_MeV, shortfall_MeV / B_exp_14N * 100.0))
    print()
    print("Location: nitrogen14_occlusion() in 02_04_alpha_clusters.py")
    print("  Omega_14N   = C12_total + extra")
    print("  extra       = 3 * spherical_occlusion(R_tetra, d_center)")
    print("  R_tetra     = {:.4f} fm".format(R_tetra))
    print("  d_center    = {:.4f} fm (2.9/sqrt(3))".format(d_center))
    print("  extra       = {:.6f} sr".format(extra_current))
    print()
    print("Required additional Omega to match B_exp: {:.6f} sr".format(shortfall_sr))
    print("  (approx. {:.2f}% increase on current extra term)".format(
        shortfall_sr / extra_current * 100.0))
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
