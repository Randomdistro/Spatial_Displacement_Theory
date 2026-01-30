#!/usr/bin/env python3
"""
SDT occlusion factors derived from Atomica Sentis packing signatures.

This module is intentionally deterministic and contains **no per-element fitted constants**.
It provides the plumbing needed for chemistry validation (chem-02..chem-04):
  - packing-derived nuclear field radius R_N(Z,N)
  - occlusion presentation factors Xi_val(Z,N) and Xi_ion(Z,N)

Important note (current state of the theory-as-code):
The codebase does not yet contain a fully specified, first-principles geometric derivation
for Xi_val/Xi_ion from nuclear packing alone. Until that derivation exists in-code,
we return conservative default values (Xi=1) and surface the dependence explicitly.
The validator will therefore report non-exactness against experimental chemistry data.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

from atomica_sentis_calculator import AtomicaSentisCalculator, Geometry, NuclearStructure

# --- SDT constants used by chemistry papers ---

# Nuclear radius constant (m)
R0_NUC = 1.2e-15

# Electron point presence / exclusion scale (m)
R_E_POINT = 1.1e-21

# Spation/Planck parameters (as used in SDT docs)
L_P = 1.616255e-35  # m
K_BULK = 4.6e113  # Pa

# Cosmic scale (CMB boundary radius). Coulomb_Force.md uses ~46 Gly as the boundary scale.
LY_M = 9.4607304725808e15  # m
R_CMB = 46.0e9 * LY_M  # m

@dataclass(frozen=True)
class OcclusionFactors:
    """Computed geometric inputs for chemistry predictor."""

    R_N: float  # effective nuclear field radius (m)
    Xi_val: float  # valence-visible occlusion fraction (dimensionless)
    Xi_ion: float  # ionization-visible occlusion fraction (dimensionless)
    P_eff: float  # effective pressure used in atomic binding calculations (Pa)


def _polyhedron_circumradius_factor(geometry: Optional[Geometry]) -> Optional[float]:
    """
    Circumradius (center-to-vertex) in units of edge length a for ideal regular polyhedra.
    Returns None when the geometry is not one of the implemented regular solids.
    """

    if geometry is None:
        return None

    if geometry == Geometry.POINT:
        return 0.0
    if geometry == Geometry.LINE:
        return 0.5
    if geometry == Geometry.TRIANGLE:
        return 1.0 / math.sqrt(3.0)
    if geometry == Geometry.TETRAHEDRON:
        return math.sqrt(6.0) / 4.0
    if geometry == Geometry.OCTAHEDRON:
        return math.sqrt(2.0) / 2.0
    if geometry == Geometry.CUBE:
        return math.sqrt(3.0) / 2.0

    # Bipyramid, penta-cap, and other extended stacks are not yet mapped to a closed form.
    return None


def nuclear_field_radius(structure: NuclearStructure) -> float:
    """
    Packing-derived nuclear field radius.

    Strategy:
    - For small alpha-polyhedra with known circumradius factors, compute a cluster radius
      from an alpha-brick size and the polyhedron circumradius (center-to-vertex).
    - Otherwise, fall back to the canonical nuclear scaling R0_NUC * A^(1/3).
    """

    # Alpha "brick" length scale derived from the standard nuclear radius law.
    # Alpha has A=4, so set its radius by the same scaling.
    r_alpha = R0_NUC * (4.0 ** (1.0 / 3.0))
    a_edge = 2.0 * r_alpha

    f = _polyhedron_circumradius_factor(structure.geometry)
    if f is not None and structure.n_alpha > 0:
        r_centers = f * a_edge
        # Outer radius includes the alpha radius itself.
        return r_centers + r_alpha

    # Generic fallback
    return R0_NUC * (structure.A ** (1.0 / 3.0))


def occlusion_factors(Z: int, N: int) -> OcclusionFactors:
    """
    Compute (R_N, Xi_val, Xi_ion) for a given isotope using Atomica Sentis packing.

    Xi_val / Xi_ion:
      Until the codebase contains a formal occlusion derivation from packing geometry,
      we use a shell-aware empirical screening factor to surface dependence and allow
      the chemistry validator to quantify what fails to be exact.
    """

    calc = AtomicaSentisCalculator()
    structure = calc.analyze_nucleus(Z=Z, N=N)

    R_N = nuclear_field_radius(structure)

    # TODO: Replace with first-principles occlusion derivation from packing + shell architecture.
    # Baseline (no screening): matches prior exact state.
    Xi_val, Xi_ion = 1.0, 1.0

    # Default effective pressure is the ambient atomic/molecular CMB pressure.
    # The caller may override this by selecting a pressure focusing model.
    P_eff = 2.036e-2

    return OcclusionFactors(R_N=R_N, Xi_val=Xi_val, Xi_ion=Xi_ion, P_eff=P_eff)


def effective_pressure_planck_focus(r: float) -> float:
    """
    Option A: Planck-to-scale focusing.
      P_eff(r) = K_bulk * (L_P / r)^2
    """
    return K_BULK * (L_P / r) ** 2


def effective_pressure_cosmic_focus(r: float) -> float:
    """
    Option B: cosmic-to-scale focusing, starting from atomic/molecular CMB pressure.
      P_eff(r) = P_CMB * (R_CMB / r)^2
    """
    P_CMB = 2.036e-2
    return P_CMB * (R_CMB / r) ** 2


def electron_shell_architecture(Z: int) -> dict:
    """
    Deterministic shell architecture (capacity model, not QM): fills shells in sequence.
    Retained for future screening derivations.
    """

    shell_capacities = [2, 8, 8, 18, 18, 32, 32]  # simple capacity progression
    remaining = Z
    electrons_per_shell = []
    for cap in shell_capacities:
        if remaining <= 0:
            electrons_per_shell.append(0)
            continue
        take = min(cap, remaining)
        electrons_per_shell.append(take)
        remaining -= take

    n_shells = [i + 1 for i in range(len(shell_capacities))]
    valence_shell_idx = max(i for i, e in enumerate(electrons_per_shell) if e > 0)
    core_electrons = sum(electrons_per_shell[:valence_shell_idx])

    return {
        "n_shells": n_shells,
        "electrons_per_shell": electrons_per_shell,
        "valence_shell": valence_shell_idx + 1,
        "core_electrons": core_electrons,
    }


