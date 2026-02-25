"""
SDT 3D Particle CMB Model — Particle Models

Proton (trefoil), neutron (p+e internal), electron, neutrino, spation.
Geometric parameters from SDT dataset and Part I Axioms.
"""

import math
from typing import Optional, List
from dataclasses import dataclass, field
import numpy as np

from .constants import (
    C, R_P, A_OVER_R, K_P, R_MINOR, R_NODE, A_0, V_ELECTRON,
    R_NU, L_P, P_CMB, KAPPA_PROTON, N_POLOIDAL, M_TOROIDAL, DELTA_TOPO,
)


@dataclass
class Particle:
    """Base particle with position and geometric parameters."""
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))
    radius: float = 0.0
    k_value: float = 1.0  # Ϟ = c/v_surface
    chirality: str = "R"   # L or R for pairing

    def R_c(self) -> float:
        """c-boundary radius: R_c = R_phys / k²"""
        return self.radius / (self.k_value ** 2)

    def v_surface(self) -> float:
        """Surface velocity: c/Ϟ"""
        return C / self.k_value

    def effective_occlusion_radius(self) -> float:
        """Radius for occlusion calculations."""
        return self.radius


@dataclass
class Proton(Particle):
    """
    Proton: 6π trefoil knot on fat torus.
    n=3, m=2; Δ_topo=5; k_p²=5α⁻¹; a/R=1/√2.
    """
    radius: float = R_P
    k_value: float = K_P
    # Trefoil geometry
    minor_radius: float = field(default_factory=lambda: R_P * A_OVER_R)
    n_poloidal: int = N_POLOIDAL
    m_toroidal: int = M_TOROIDAL
    delta_topo: int = DELTA_TOPO
    kappa_internal: float = KAPPA_PROTON
    # Three-velocity system (TREFoil)
    v1_c: float = 2.23   # Perihelion
    v2_c: float = 1.84   # Rim (operational)
    v3_c: float = 0.395  # Aphelion

    def A_eff(self) -> float:
        """Effective capture area for Core Engine."""
        return math.pi * self.radius ** 2

    def Gamma_circulation(self) -> float:
        """Γ = v_poloidal/c. Using v2 as operational."""
        return self.v2_c

    def curvature_kappa(self) -> float:
        """κ = 1/r_minor (m⁻¹)"""
        return 1.0 / (self.minor_radius + 1e-30)


@dataclass
class Neutron(Particle):
    """
    Neutron = p⁺ + e⁻_internal. Electron bound at trefoil node.
    r_node ≈ 0.25 fm.
    """
    radius: float = 0.87e-15  # Slightly larger than proton
    k_value: float = K_P
    has_internal_electron: bool = True
    node_radius: float = R_NODE * 1e-15  # Convert fm to m

    def A_eff(self) -> float:
        return math.pi * self.radius ** 2


@dataclass
class Electron(Particle):
    """
    Electron: orbital at Bohr radius in hydrogen.
    Ϟ_H = 137.036 = c/v_electron.
    """
    radius: float = 1.1e-21  # Electron point presence (from Coulomb Force)
    k_value: float = 137.036  # Ϟ_H
    orbital_radius: float = A_0  # Bohr radius when bound

    def v_orbital(self) -> float:
        return V_ELECTRON


@dataclass
class Neutrino(Particle):
    """
    Neutrino: circulating pressure pattern.
    r_ν = 993 ℓ_P = 1.60e-32 m.
    """
    radius: float = R_NU
    k_value: float = 1.0  # Propagates at c
    circulation_radius: float = R_NU


@dataclass
class Spation(Particle):
    """
    Spation: discrete unit of the Euclidean lattice.
    Diameter ~ Planck length.
    """
    radius: float = L_P / 2
    k_value: float = 1.0
