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

from sdt_occlusion_factors import (
    R_E_POINT,
    OcclusionFactors,
    effective_pressure_cosmic_focus,
    effective_pressure_planck_focus,
    occlusion_factors,
)

# Physical constants
E_CHARGE = 1.602176634e-19  # J/eV

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
    EA_eV: float
    EN: float


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


CALIBRATION_CONSTANTS = {"planck": None, "cosmic": None}


def _get_pressure_func(pressure_model: str):
    model = pressure_model.lower()
    if model == "planck":
        return effective_pressure_planck_focus
    if model == "cosmic":
        return effective_pressure_cosmic_focus
    raise ValueError(f"Unknown pressure model: {pressure_model}")


def calibrate_pressure_focusing(pressure_model: str, target_I1_H_eV: float = 13.598) -> float:
    """
    Calibrate the pressure focusing model on Hydrogen first ionization energy.
    Returns a multiplicative calibration constant K_cal.
    """

    occ_H = occlusion_factors(Z=1, N=0)
    r_H = predict_atomic_radius_m(Z=1, N=0, occ=occ_H)

    pressure_func = _get_pressure_func(pressure_model)
    P_eff = pressure_func(r_H)

    I1_uncalibrated_J = (math.pi / 4.0) * P_eff * (occ_H.R_N**2) * (R_E_POINT**2) * (1.0 * occ_H.Xi_ion) / r_H
    I1_uncalibrated_eV = I1_uncalibrated_J / E_CHARGE

    if I1_uncalibrated_eV == 0:
        raise ZeroDivisionError("Uncalibrated I1 for hydrogen is zero; cannot calibrate.")

    return target_I1_H_eV / I1_uncalibrated_eV


def get_calibration_constant(pressure_model: str) -> float:
    """Lazy-init calibration constants for each pressure model."""

    model = pressure_model.lower()
    if model not in CALIBRATION_CONSTANTS:
        raise ValueError(f"Unsupported pressure model: {pressure_model}")

    if CALIBRATION_CONSTANTS[model] is None:
        CALIBRATION_CONSTANTS[model] = calibrate_pressure_focusing(pressure_model=model)

    return CALIBRATION_CONSTANTS[model]


def predict_I1_eV(
    Z: int, N: int, occ: OcclusionFactors, r_atomic_m: float, pressure_model: str = "planck"
) -> float:
    """
    First ionization energy from work integral of occlusion force with pressure focusing:

      I1 = (pi/4) * K_cal * P_eff(r) * (R_N^2 * R_e^2 * (Z * Xi_ion)) / r_atomic
    """

    pressure_func = _get_pressure_func(pressure_model)
    P_eff = pressure_func(r_atomic_m)
    K_cal = get_calibration_constant(pressure_model)

    Z_eff_ion = Z * occ.Xi_ion
    I1_J = (math.pi / 4.0) * K_cal * P_eff * (occ.R_N**2) * (R_E_POINT**2) * Z_eff_ion / r_atomic_m
    return I1_J / E_CHARGE


def predict_EA_eV(
    Z: int, N: int, occ: OcclusionFactors, r_atomic_m: float, pressure_model: str = "planck"
) -> float:
    """
    Electron affinity from nuclear field well depth (negative work to add an electron).
    EA = -(pi/4) * K_cal * P_eff(r) * R_N^2 * R_e^2 / r_atomic^2
    """

    pressure_func = _get_pressure_func(pressure_model)
    P_eff = pressure_func(r_atomic_m)
    K_cal = get_calibration_constant(pressure_model)

    EA_J = -(math.pi / 4.0) * K_cal * P_eff * (occ.R_N**2) * (R_E_POINT**2) / (r_atomic_m**2)
    return EA_J / E_CHARGE


def predict_EN(Z: int, occ: OcclusionFactors, r_atomic_m: float) -> float:
    """
    Electronegativity = occlusion-presented nuclear field strength per unit surface area.
    Simple SDT form: chi = (Z * Xi_val) / (4*pi*r_atomic^2)
    """

    Z_eff = Z * occ.Xi_val
    surface_area = 4.0 * math.pi * (r_atomic_m**2)
    return Z_eff / surface_area


def predict_atomic(Z: int, N: int, pressure_model: str = "planck") -> AtomicPrediction:
    occ = occlusion_factors(Z=Z, N=N)
    r_atomic_m = predict_atomic_radius_m(Z=Z, N=N, occ=occ)
    I1_eV = predict_I1_eV(Z=Z, N=N, occ=occ, r_atomic_m=r_atomic_m, pressure_model=pressure_model)
    EA_eV = predict_EA_eV(Z=Z, N=N, occ=occ, r_atomic_m=r_atomic_m, pressure_model=pressure_model)
    EN = predict_EN(Z=Z, occ=occ, r_atomic_m=r_atomic_m)

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
        EA_eV=EA_eV,
        EN=EN,
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


