#!/usr/bin/env python3
"""
SDT Chemistry Predictor (from nuclear packing).

This is the executable counterpart to the chemistry papers: given an isotope (Z,N),
compute predicted atomic-scale observables from SDT primitives + packing-derived inputs.

Current scope:
- atomic radius (shell-index based)
- first ionization energy I1 (work integral of occlusion force)

Notes:
- Electron affinity / electronegativity / molecule-level quantities require additional
  executable derivations not yet present as code (will be added under chem-03/chem-04).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

from sdt_occlusion_factors import R_E_POINT, OcclusionFactors, occlusion_factors

# Physical constants
E_CHARGE = 1.602176634e-19  # J/eV

# SDT constants from the chemistry papers
P_CMB = 2.036e-2  # Pa (atomic/molecular scale)
A0_BOHR = 5.292e-11  # m (hydrogen reference radius)


@dataclass(frozen=True)
class AtomicPrediction:
    Z: int
    N: int
    A: int

    n_shell: int
    R_N: float
    Xi_val: float
    Xi_ion: float

    r_atomic_m: float
    I1_eV: float

    # Placeholders until the derivations are implemented:
    EA_eV: Optional[float] = None
    EN: Optional[float] = None


def period_shell_index(Z: int) -> int:
    """
    Map atomic number to a principal shell index (period).
    This is a deterministic periodic-table mapping used as a proxy for available valence cavity.
    """

    if Z <= 2:
        return 1
    if Z <= 10:
        return 2
    if Z <= 18:
        return 3
    if Z <= 36:
        return 4
    if Z <= 54:
        return 5
    if Z <= 86:
        return 6
    return 7


def predict_atomic_radius_m(Z: int, N: int, occ: OcclusionFactors) -> float:
    """
    Predict atomic radius via SDT control law:
      r_atom = a0 * n^2 / (Z * Xi_val)
    """

    n = period_shell_index(Z)
    Z_eff = max(1e-12, Z * occ.Xi_val)
    return A0_BOHR * (n**2) / Z_eff


def predict_I1_eV(Z: int, N: int, occ: OcclusionFactors, r_atomic_m: float) -> float:
    """
    First ionization energy from work integral of occlusion force:

      I1 = (pi/4) * P_CMB * (R_N^2 * R_e^2 * (Z * Xi_ion)) / r_atomic
    """

    Z_eff_ion = Z * occ.Xi_ion
    I1_J = (math.pi / 4.0) * P_CMB * (occ.R_N**2) * (R_E_POINT**2) * Z_eff_ion / r_atomic_m
    return I1_J / E_CHARGE


def predict_atomic(Z: int, N: int) -> AtomicPrediction:
    occ = occlusion_factors(Z=Z, N=N)
    r_atomic_m = predict_atomic_radius_m(Z=Z, N=N, occ=occ)
    I1_eV = predict_I1_eV(Z=Z, N=N, occ=occ, r_atomic_m=r_atomic_m)

    return AtomicPrediction(
        Z=Z,
        N=N,
        A=Z + N,
        n_shell=period_shell_index(Z),
        R_N=occ.R_N,
        Xi_val=occ.Xi_val,
        Xi_ion=occ.Xi_ion,
        r_atomic_m=r_atomic_m,
        I1_eV=I1_eV,
    )


def main():
    # Minimal smoke test output
    for (Z, N, label) in [
        (1, 0, "H-1"),
        (2, 2, "He-4"),
        (6, 6, "C-12"),
        (8, 8, "O-16"),
    ]:
        pred = predict_atomic(Z, N)
        print(f"{label}: n={pred.n_shell} r={pred.r_atomic_m:.3e} m I1={pred.I1_eV:.3f} eV (Xi_val={pred.Xi_val}, Xi_ion={pred.Xi_ion})")


if __name__ == "__main__":
    main()


