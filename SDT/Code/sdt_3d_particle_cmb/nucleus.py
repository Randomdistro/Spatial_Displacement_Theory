"""
SDT 3D Particle CMB Model — Nucleus Geometry

Builds nucleon positions for any isotope (Z, A) from hydrogen through tin.
Uses SDT alpha-cluster concepts where applicable; sphere packing for generic nuclei.
"""

import math
from typing import List, Tuple, Optional
import numpy as np

from .constants import R_P, R_N_0, D_DEUTERON
from .particles import Proton, Neutron, Particle
from .isotopes import get_isotope, Isotope


def nuclear_radius(A: int) -> float:
    """R = R_0 * A^(1/3) in meters."""
    return R_N_0 * (A ** (1.0 / 3.0))


def nucleon_positions(Z: int, A: int, center: Optional[np.ndarray] = None) -> Tuple[List[np.ndarray], List[str]]:
    """
    Generate nucleon positions for isotope (Z, A).
    Returns (positions, types) where types is "p" or "n".

    Geometry:
    - A=1: single proton at center
    - A=2: deuteron (p-n at D_DEUTERON)
    - A=3: H-3 (2n + p) or He-3 (2p + n) - triangle
    - A=4: alpha (2p+2n tetrahedron)
    - A=6: Li-6 style (2 alphas don't bind; use triangle)
    - A=12: C-12 (3 alphas triangle)
    - A=16: O-16 (4 alphas tetrahedron)
    - Generic: spherical shell / FCC packing
    """
    center = center if center is not None else np.zeros(3)
    N = A - Z
    positions: List[np.ndarray] = []
    types: List[str] = []

    # Known small-nucleus geometries (SDT from alpha clusters)
    if A == 1:
        positions = [center.copy()]
        types = ["p"]
        return positions, types

    if A == 2:
        # Deuteron: p at origin, n at d
        d = D_DEUTERON
        positions = [center + np.array([0, 0, 0]), center + np.array([d, 0, 0])]
        types = ["p", "n"] if Z == 1 else ["n", "p"]
        return positions, types

    if A == 3:
        # Triangle, side ~2 fm
        s = 2.0e-15
        a = np.array([0, 0, 0])
        b = np.array([s, 0, 0])
        c = np.array([s / 2, s * 0.866, 0])
        pos = [a, b, c]
        if Z == 1:  # H-3: n, n, p
            types = ["n", "n", "p"]
        else:  # He-3: p, p, n
            types = ["p", "p", "n"]
        positions = [center + p for p in pos]
        return positions, types

    if A == 4:
        # Alpha: tetrahedron
        a = 1.7e-15  # fm scale
        pos = [
            np.array([0, 0, 0]),
            np.array([a, 0, 0]),
            np.array([a/2, a * 0.866, 0]),
            np.array([a/2, a * 0.289, a * 0.817]),
        ]
        # 2p + 2n: alternate p,n
        types = ["p", "n", "p", "n"]
        positions = [center + p for p in pos]
        return positions, types

    # Generic: place nucleons on spherical shell(s)
    # Use Fibonacci sphere for roughly uniform distribution
    R = nuclear_radius(A)
    n_total = A

    # Fibonacci sphere algorithm
    def fib_sphere(n: int, r: float) -> List[np.ndarray]:
        pts = []
        phi = math.pi * (3.0 - math.sqrt(5.0))  # golden angle
        for i in range(n):
            y = 1 - (i / (n - 1)) * 2 if n > 1 else 0
            radius_at_y = math.sqrt(1 - y * y)
            theta = phi * i
            x = math.cos(theta) * radius_at_y
            z = math.sin(theta) * radius_at_y
            pts.append(r * np.array([x, y, z]))
        return pts

    pts = fib_sphere(n_total, R * 0.8)  # Slightly inside R for packing
    for i, p in enumerate(pts):
        if i < Z:
            types.append("p")
        else:
            types.append("n")
        positions.append(center + p)

    return positions, types


def build_nucleus(
    Z: int,
    A: int,
    center: Optional[np.ndarray] = None,
    chirality_alternate: bool = True
) -> Tuple[List[Particle], List[np.ndarray]]:
    """
    Build list of Proton/Neutron particles and positions for isotope (Z, A).

    chirality_alternate: alternate L/R for pairing (L-R binds).
    """
    pos_list, type_list = nucleon_positions(Z, A, center)
    particles: List[Particle] = []
    positions: List[np.ndarray] = []

    for i, (pos, t) in enumerate(zip(pos_list, type_list)):
        chirality = "L" if (i % 2 == 0 and chirality_alternate) else "R"
        if t == "p":
            particles.append(Proton(position=pos.copy(), chirality=chirality))
        else:
            particles.append(Neutron(position=pos.copy(), chirality=chirality))
        positions.append(pos.copy())

    return particles, positions


def validate_isotope(Z: int, A: int) -> Optional[Isotope]:
    """Check (Z, A) is in database; return Isotope or None."""
    iso = get_isotope(Z, A)
    if iso is None:
        raise ValueError(f"Isotope Z={Z} A={A} not in database (H through Sn)")
    return iso
