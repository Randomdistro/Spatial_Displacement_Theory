"""
SDT 3D Particle CMB Model — Toggleable Arrangements

6π trefoils, helical vortices, pairing (L-R chirality) as dynamic toggles.
Structural alignments from Investigation_Structural_Alignments_and_Pairing.
"""

import math
from typing import List, Tuple, Optional
from dataclasses import dataclass
import numpy as np

from .particles import Proton, Neutron, Particle


@dataclass
class ArrangementConfig:
    """
    Toggleable arrangement options for the 3D model.
    """
    # 6π trefoil: enable trefoil topology for protons
    trefoil_enabled: bool = True
    # Helical vortex: enable helical circulation pattern
    helical_vortex_enabled: bool = True
    # Pairing: L-R chirality binding rules (L-R bind, L-L/R-R Pauli suppressed)
    pairing_enabled: bool = True
    # Three-velocity system (v1, v2, v3) for trefoil
    three_velocity_enabled: bool = True
    # Poloidal circulation for magnetic moment
    poloidal_circulation_enabled: bool = True
    # Neutrino trapping in multi-nucleon systems
    neutrino_trapping_enabled: bool = False


def trefoil_sample_points(
    R_major: float,
    R_minor: float,
    n: int = 3,
    m: int = 2,
    num_points: int = 64
) -> np.ndarray:
    """
    Sample points on a trefoil knot (3₁) on a torus.
    Parametric: poloidal n=3, toroidal m=2.
    """
    t = np.linspace(0, 2 * math.pi, num_points, endpoint=False)
    x = (R_major + R_minor * math.cos(n * t)) * math.cos(m * t)
    y = (R_major + R_minor * math.cos(n * t)) * math.sin(m * t)
    z = R_minor * math.sin(n * t)
    return np.column_stack([x, y, z])


def helical_velocity_field(
    position: np.ndarray,
    center: np.ndarray,
    axis: np.ndarray,
    circulation: float,
    pitch: float
) -> np.ndarray:
    """
    Helical vortex velocity at position.
    Uses circulation + pitch for helical flow.
    """
    r_vec = position - center
    r_vec = r_vec - np.dot(r_vec, axis) * axis  # Perpendicular component
    r_perp = np.linalg.norm(r_vec)
    if r_perp < 1e-30:
        return np.zeros(3)
    # Azimuthal velocity
    v_az = circulation / (2 * math.pi * r_perp)
    tangent = np.cross(axis, r_vec) / (r_perp + 1e-30)
    v_az_vec = v_az * tangent
    # Axial (helical pitch)
    v_axial = pitch * axis
    return v_az_vec + v_axial


def pairing_contribution(
    p1: Particle,
    p2: Particle,
    separation: float
) -> float:
    """
    Pairing contribution from structural alignment.
    L-R binds; L-L and R-R are Pauli suppressed (reduce contribution).
    Returns factor in [0, 1] for binding strength.
    """
    if p1.chirality != p2.chirality:
        return 1.0  # L-R: full pairing
    return 0.0  # L-L or R-R: Pauli suppressed, no pairing


def compute_pairing_matrix(
    particles: List[Particle],
    positions: List[np.ndarray],
    threshold: float = 3.0e-15
) -> np.ndarray:
    """
    Matrix of pairing contributions between nucleons.
    threshold: max separation for pairing (e.g. 3 fm).
    """
    n = len(particles)
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(positions[i] - positions[j])
            if d <= threshold:
                M[i, j] = pairing_contribution(particles[i], particles[j], d)
                M[j, i] = M[i, j]
    return M


def apply_trefoil_geometry(proton: Proton, config: ArrangementConfig) -> dict:
    """
    Apply trefoil geometry parameters based on config.
    Returns dict of effective parameters for use in pressure/energy.
    """
    if not config.trefoil_enabled:
        return {"radius": proton.radius, "k": proton.k_value}
    # Full trefoil with 6π winding
    return {
        "radius": proton.radius,
        "minor_radius": proton.minor_radius,
        "k": proton.k_value,
        "n": proton.n_poloidal,
        "m": proton.m_toroidal,
        "delta_topo": proton.delta_topo,
        "v1": proton.v1_c * 299792458,
        "v2": proton.v2_c * 299792458,
        "v3": proton.v3_c * 299792458,
    }


def apply_helical_velocity(
    position: np.ndarray,
    source: Proton,
    config: ArrangementConfig
) -> np.ndarray:
    """Apply helical vortex velocity if enabled."""
    if not config.helical_vortex_enabled:
        return np.zeros(3)
    axis = np.array([0, 0, 1])
    circulation = source.v_surface() * 2 * math.pi * source.radius
    pitch = 0.1 * circulation  # Helical pitch factor
    return helical_velocity_field(
        position, source.position, axis, circulation, pitch
    )
