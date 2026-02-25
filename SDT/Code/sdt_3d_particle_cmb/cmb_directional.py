"""
SDT 3D Particle CMB Model — CMB Directional

Configurable directional CMB: gross incoming event (12-direction dodecahedral)
for compute savings, up to finer resolutions.

Largest coarse: 12 directions (dodecahedral/decahedral) around every spherical
object. Finer resolutions subdivide the unit sphere.
"""

import math
from typing import List, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class CMBDirection:
    """Single CMB incoming direction with unit vector and solid angle weight."""
    unit_vec: Tuple[float, float, float]  # normalized
    weight: float  # solid angle fraction (1/N for uniform coarse)
    theta: float   # polar angle (rad)
    phi: float     # azimuthal angle (rad)


def _normalize(v: Tuple[float, float, float]) -> Tuple[float, float, float]:
    n = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    return (v[0]/n, v[1]/n, v[2]/n)


def _dodecahedral_vertices() -> List[Tuple[float, float, float]]:
    """
    Vertices of a regular dodecahedron on unit sphere.
    Golden ratio φ = (1+√5)/2.
    """
    phi = (1 + math.sqrt(5)) / 2
    inv_phi = 1 / phi
    verts = [
        (1, 1, 1),
        (1, 1, -1),
        (1, -1, 1),
        (1, -1, -1),
        (-1, 1, 1),
        (-1, 1, -1),
        (-1, -1, 1),
        (-1, -1, -1),
        (0, phi, inv_phi),
        (0, phi, -inv_phi),
        (0, -phi, inv_phi),
        (0, -phi, -inv_phi),
        (inv_phi, 0, phi),
        (inv_phi, 0, -phi),
        (-inv_phi, 0, phi),
        (-inv_phi, 0, -phi),
        (phi, inv_phi, 0),
        (phi, -inv_phi, 0),
        (-phi, inv_phi, 0),
        (-phi, -inv_phi, 0),
    ]
    return [_normalize(v) for v in verts]


def _icosahedral_vertices() -> List[Tuple[float, float, float]]:
    """Vertices of icosahedron (12 vertices)."""
    phi = (1 + math.sqrt(5)) / 2
    verts = [
        (-1, phi, 0), (1, phi, 0), (-1, -phi, 0), (1, -phi, 0),
        (0, -1, phi), (0, 1, phi), (0, -1, -phi), (0, 1, -phi),
        (phi, 0, -1), (phi, 0, 1), (-phi, 0, -1), (-phi, 0, 1),
    ]
    return [_normalize(v) for v in verts]


def _cart_to_spherical(x: float, y: float, z: float) -> Tuple[float, float]:
    r = math.sqrt(x**2 + y**2 + z**2)
    if r < 1e-12:
        return 0.0, 0.0
    theta = math.acos(max(-1, min(1, z / r)))
    phi = math.atan2(y, x)
    return theta, phi


class CMBDirectional:
    """
    Configurable directional CMB incidence.

    Coarsest: 12 directions (dodecahedral face normals or icosahedral vertices).
    Finer: subdivide each coarse direction or use Fibonacci sphere.
    """

    RESOLUTION_12 = "12"    # Icosahedral vertices (12 dirs)
    RESOLUTION_20 = "20"    # Dodecahedral vertices (20 dirs)
    RESOLUTION_42 = "42"    # Icosahedral + midpoints
    RESOLUTION_FIB = "fib"  # Fibonacci sphere (configurable N)

    def __init__(self, resolution: str = "12", num_directions: int = 12):
        """
        Args:
            resolution: "12", "20", "42", or "fib"
            num_directions: For "fib", number of directions on sphere.
        """
        self.resolution = resolution
        self.num_directions = num_directions
        self._directions: List[CMBDirection] = []
        self._build_directions()

    def _build_directions(self) -> None:
        if self.resolution == self.RESOLUTION_12:
            verts = _icosahedral_vertices()
        elif self.resolution == self.RESOLUTION_20:
            verts = _dodecahedral_vertices()
        elif self.resolution == self.RESOLUTION_42:
            # Icosahedral + face midpoints (approximate)
            verts = _icosahedral_vertices()
            # Add midpoints between adjacent pairs for denser sampling
            midpoints = []
            n = len(verts)
            for i in range(n):
                for j in range(i + 1, n):
                    mx = (verts[i][0] + verts[j][0]) / 2
                    my = (verts[i][1] + verts[j][1]) / 2
                    mz = (verts[i][2] + verts[j][2]) / 2
                    midpoints.append(_normalize((mx, my, mz)))
            verts = verts + midpoints[:22]  # Keep ~42 total
        elif self.resolution == self.RESOLUTION_FIB:
            verts = self._fibonacci_sphere(self.num_directions)
        else:
            verts = _icosahedral_vertices()

        weight = 1.0 / len(verts)
        self._directions = []
        for v in verts:
            theta, phi = _cart_to_spherical(v[0], v[1], v[2])
            self._directions.append(CMBDirection(
                unit_vec=v,
                weight=weight,
                theta=theta,
                phi=phi
            ))

    def _fibonacci_sphere(self, n: int) -> List[Tuple[float, float, float]]:
        """Fibonnaci lattice on unit sphere."""
        verts = []
        phi = math.pi * (3 - math.sqrt(5))
        for i in range(n):
            y = 1 - (i / (n - 1)) * 2 if n > 1 else 0
            r = math.sqrt(1 - y * y)
            theta = phi * i
            x = math.cos(theta) * r
            z = math.sin(theta) * r
            verts.append(_normalize((x, y, z)))
        return verts

    @property
    def directions(self) -> List[CMBDirection]:
        return self._directions

    @property
    def num_dirs(self) -> int:
        return len(self._directions)

    def get_unit_vectors(self) -> np.ndarray:
        """Return (N, 3) array of unit vectors."""
        return np.array([d.unit_vec for d in self._directions])

    def get_weights(self) -> np.ndarray:
        """Return (N,) array of solid angle weights."""
        return np.array([d.weight for d in self._directions])
