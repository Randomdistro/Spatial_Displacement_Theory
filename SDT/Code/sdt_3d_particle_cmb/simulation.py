"""
SDT 3D Particle CMB Model — Simulation

Orchestrates particles, CMB directional, pressure mechanics, and
arrangement configs. Supports batch runs for testing many arrangements.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import numpy as np

from .constants import P_CMB
from .cmb_directional import CMBDirectional
from .pressure_mechanics import PressureMechanics, energy_rate_core_engine
from .particles import Proton, Neutron, Electron, Neutrino, Spation, Particle
from .arrangements import (
    ArrangementConfig,
    apply_trefoil_geometry,
    compute_pairing_matrix,
)
from .nucleus import build_nucleus

@dataclass
class SimulationResult:
    """Result of a single simulation run."""
    config_hash: str
    pressure_centroid: float
    total_occlusion: float
    energy_rate_proton: float
    pairing_matrix_sum: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class Simulation:
    """
    Main simulation engine.
    Combines CMB directional, pressure mechanics, and particles
    with toggleable arrangement configs.
    """

    def __init__(
        self,
        cmb_resolution: str = "12",
        cmb_num_dirs: int = 12,
        arrangement: Optional[ArrangementConfig] = None
    ):
        self.cmb = CMBDirectional(resolution=cmb_resolution, num_directions=cmb_num_dirs)
        self.pressure = PressureMechanics(self.cmb, P_background=P_CMB)
        self.arrangement = arrangement or ArrangementConfig()
        self.particles: List[Particle] = []
        self.positions: List[np.ndarray] = []

    def add_proton(self, position: np.ndarray, chirality: str = "R") -> None:
        p = Proton(position=position.copy(), chirality=chirality)
        self.particles.append(p)
        self.positions.append(position.copy())

    def add_neutron(self, position: np.ndarray, chirality: str = "L") -> None:
        n = Neutron(position=position.copy(), chirality=chirality)
        self.particles.append(n)
        self.positions.append(position.copy())

    def add_electron(self, position: np.ndarray) -> None:
        e = Electron(position=position.copy())
        self.particles.append(e)
        self.positions.append(position.copy())

    def add_nucleus(self, Z: int, A: int, center: Optional[np.ndarray] = None) -> None:
        """Add nucleus (Z, A) - all isotopes from H through Sn."""
        particles, positions = build_nucleus(Z, A, center)
        self.particles.extend(particles)
        self.positions.extend(positions)

    def clear(self) -> None:
        self.particles.clear()
        self.positions.clear()

    def _occlusion_sources(self) -> List[tuple]:
        """List of (position, radius) for occlusion."""
        return [
            (pos.copy(), p.effective_occlusion_radius())
            for pos, p in zip(self.positions, self.particles)
        ]

    def run(self) -> SimulationResult:
        """Run single simulation and return result."""
        sources = self._occlusion_sources()
        if not sources:
            return SimulationResult(
                config_hash="empty",
                pressure_centroid=P_CMB,
                total_occlusion=0.0,
                energy_rate_proton=0.0,
                pairing_matrix_sum=0.0,
                metadata={"n_particles": 0}
            )

        # Centroid for pressure sampling
        centroid = np.mean(np.array(self.positions), axis=0)
        pressure_centroid = self.pressure.pressure_at_point(centroid, sources)
        total_occlusion = self.pressure.total_occlusion_at_point(centroid, sources)

        # Energy rate from Core Engine (first proton if any)
        # Ḋ = P_CMB A_eff Γ κ (1-η); Γ = v_poloidal/c
        energy_rate_proton = 0.0
        for p in self.particles:
            if isinstance(p, Proton):
                geom = apply_trefoil_geometry(p, self.arrangement)
                A_eff = np.pi * geom["radius"] ** 2
                Gamma = (
                    min(1.0, p.v2_c) if self.arrangement.three_velocity_enabled
                    else p.v_surface() / 299792458
                )
                kappa = 1.0 / (p.minor_radius + 1e-30)
                energy_rate_proton = energy_rate_core_engine(
                    P_CMB, A_eff, Gamma, kappa, 0.0
                )
                break

        # Pairing matrix sum
        pairing_sum = 0.0
        if self.arrangement.pairing_enabled and len(self.particles) >= 2:
            M = compute_pairing_matrix(self.particles, self.positions)
            pairing_sum = float(np.sum(M))

        config_hash = self._config_hash()
        return SimulationResult(
            config_hash=config_hash,
            pressure_centroid=pressure_centroid,
            total_occlusion=total_occlusion,
            energy_rate_proton=energy_rate_proton,
            pairing_matrix_sum=pairing_sum,
            metadata={
                "n_particles": len(self.particles),
                "n_protons": sum(1 for p in self.particles if isinstance(p, Proton)),
                "n_neutrons": sum(1 for p in self.particles if isinstance(p, Neutron)),
                "trefoil": self.arrangement.trefoil_enabled,
                "pairing": self.arrangement.pairing_enabled,
            }
        )

    def _config_hash(self) -> str:
        """Short hash of arrangement config."""
        t = "T" if self.arrangement.trefoil_enabled else "t"
        h = "H" if self.arrangement.helical_vortex_enabled else "h"
        p = "P" if self.arrangement.pairing_enabled else "p"
        return f"{t}{h}{p}"


def batch_run(
    configs: List[ArrangementConfig],
    particle_setups: List[callable],
    cmb_resolution: str = "12"
) -> List[SimulationResult]:
    """
    Run many arrangements in batch.
    configs: list of ArrangementConfig
    particle_setups: list of callables f(sim: Simulation) that add particles
    """
    results = []
    for config in configs:
        for setup in particle_setups:
            sim = Simulation(cmb_resolution=cmb_resolution)
            sim.arrangement = config
            setup(sim)
            results.append(sim.run())
    return results
