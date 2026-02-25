"""
SDT 3D Particle CMB Model — Pressure Density Mechanics

Occlusion, pressure kernel, Core Engine (Ḋ = P_CMB A_eff Γ κ (1-η)),
and pressure-density from SDT formulations.
"""

import math
from typing import List, Tuple, Optional
import numpy as np

from .constants import C, P_CMB, P_INFINITY, R_P
from .cmb_directional import CMBDirectional, CMBDirection


def solid_angle_exact(R: float, r: float) -> float:
    """
    Exact solid angle subtended by sphere of radius R at distance r.
    Ω(r) = 2π(1 − √(1 − R²/r²))
    """
    if r <= R:
        return 2.0 * math.pi
    x = R * R / (r * r)
    if x >= 1:
        return 2.0 * math.pi
    return 2.0 * math.pi * (1.0 - math.sqrt(1.0 - x))


def occlusion_far_field(R: float, r: float) -> float:
    """
    Far-field occlusion O(r) = R²/(4r²).
    Fraction of sky blocked by sphere of radius R at distance r.
    """
    if r <= 0:
        return 1.0
    return (R * R) / (4.0 * r * r)


def pressure_at_position(
    position: np.ndarray,
    source_position: np.ndarray,
    source_radius: float,
    P_background: float = P_CMB
) -> float:
    """
    Pressure at position from a single occlusion source.
    P(r) ∝ P_background × (1 - occlusion); pressure deficit from occlusion.
    """
    r_vec = position - source_position
    r = np.linalg.norm(r_vec)
    if r < 1e-30:
        return 0.0
    occ = occlusion_far_field(source_radius, r)
    return P_background * (1.0 - min(1.0, occ))


def velocity_at_radius(r: float, R_c: float) -> float:
    """
    Master orbital equation: v(r) = c √(R_c/r).
    v² = c² R_c/r
    """
    if r <= 0:
        return 0.0
    return C * math.sqrt(R_c / r)


def R_c_from_k(R_phys: float, k: float) -> float:
    """c-boundary radius: R_c = R_phys / k²"""
    return R_phys / (k * k)


def acceleration_radial(r: float, R_c: float) -> float:
    """a(r) = c² R_c / r² (Rule 2, F10)"""
    if r <= 0:
        return 0.0
    return (C * C) * R_c / (r * r)


def energy_rate_core_engine(
    P_cmb: float,
    A_eff: float,
    Gamma: float,
    kappa: float,
    eta: float = 0.0
) -> float:
    """
    Core Engine Master Equation: Ḋ = P_CMB A_eff Γ κ (1-η)
    
    From Core_Engine_Mathematical_Proof.md
    """
    return P_cmb * A_eff * Gamma * kappa * (1.0 - eta)


def occlusion_directional(
    observer_pos: np.ndarray,
    source_pos: np.ndarray,
    source_radius: float,
    direction: np.ndarray
) -> float:
    """
    Occlusion in a single direction: is the source blocking this direction
    from the observer? Returns 1 if blocked, 0 if not.
    Simplified: ray from observer in direction; does it hit the source sphere?
    """
    # Vector from observer to source
    to_source = source_pos - observer_pos
    dist = np.linalg.norm(to_source)
    if dist < 1e-30:
        return 1.0
    # Project direction onto to_source
    d_norm = direction / (np.linalg.norm(direction) + 1e-30)
    # Angular size of source from observer
    sin_theta = source_radius / dist
    if sin_theta >= 1:
        return 1.0
    # Dot product: cos(angle between direction and to_source)
    cos_angle = np.dot(d_norm, to_source / dist)
    # Source blocks if we're looking within its angular radius
    cos_half_angle = math.sqrt(1 - sin_theta * sin_theta)
    if cos_angle >= cos_half_angle:
        return 1.0
    return 0.0


class PressureMechanics:
    """
    Pressure-density mechanics with directional CMB.
    
    Integrates occlusion over CMB directions; supports compounding
    for multiple sources.
    """

    def __init__(self, cmb: CMBDirectional, P_background: float = P_CMB):
        self.cmb = cmb
        self.P_background = P_background

    def pressure_at_point(
        self,
        position: np.ndarray,
        sources: List[Tuple[np.ndarray, float]]
    ) -> float:
        """
        Net pressure at position from multiple occlusion sources.
        P = P_background × (1 - effective_occlusion)
        """
        dirs = self.cmb.get_unit_vectors()
        weights = self.cmb.get_weights()
        total_occlusion = 0.0
        for i, (d, w) in enumerate(zip(dirs, weights)):
            blocked = 0.0
            for src_pos, src_R in sources:
                b = occlusion_directional(position, src_pos, src_R, d)
                if b > 0.5:
                    blocked = 1.0
                    break
            total_occlusion += w * blocked
        return self.P_background * (1.0 - total_occlusion)

    def pressure_gradient(
        self,
        position: np.ndarray,
        sources: List[Tuple[np.ndarray, float]],
        eps: float = 1e-20
    ) -> np.ndarray:
        """Numerical gradient of pressure."""
        grad = np.zeros(3)
        P0 = self.pressure_at_point(position, sources)
        for i in range(3):
            pos_plus = position.copy()
            pos_plus[i] += eps
            grad[i] = (self.pressure_at_point(pos_plus, sources) - P0) / eps
        return grad

    def total_occlusion_at_point(
        self,
        position: np.ndarray,
        sources: List[Tuple[np.ndarray, float]]
    ) -> float:
        """Effective occlusion (0 to 1) at position."""
        dirs = self.cmb.get_unit_vectors()
        weights = self.cmb.get_weights()
        total_occlusion = 0.0
        for d, w in zip(dirs, weights):
            blocked = 0.0
            for src_pos, src_R in sources:
                if occlusion_directional(position, src_pos, src_R, d) > 0.5:
                    blocked = 1.0
                    break
            total_occlusion += w * blocked
        return total_occlusion
