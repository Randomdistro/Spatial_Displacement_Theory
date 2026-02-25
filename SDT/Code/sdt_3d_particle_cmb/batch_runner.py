"""
SDT 3D Particle CMB Model — Batch Runner

Fast parameter sweeps over arrangements and particle setups.
Run many configurations in short time for validation/screening.
"""

import itertools
from typing import List, Callable, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field
import numpy as np

from .simulation import Simulation, SimulationResult
from .arrangements import ArrangementConfig


@dataclass
class BatchConfig:
    """Configuration for a batch run."""
    arrangement_configs: List[ArrangementConfig]
    cmb_resolution: str = "12"
    cmb_num_dirs: int = 12


def make_arrangement_grid(
    trefoil: Optional[bool] = None,
    helical: Optional[bool] = None,
    pairing: Optional[bool] = None,
    three_velocity: Optional[bool] = None,
) -> List[ArrangementConfig]:
    """
    Generate all combinations of arrangement toggles.
    None = sweep both True/False.
    """
    opts = {
        "trefoil": [True, False] if trefoil is None else [trefoil],
        "helical": [True, False] if helical is None else [helical],
        "pairing": [True, False] if pairing is None else [pairing],
        "three_velocity": [True, False] if three_velocity is None else [three_velocity],
    }
    configs = []
    for t, h, p, v3 in itertools.product(
        opts["trefoil"], opts["helical"], opts["pairing"], opts["three_velocity"]
    ):
        configs.append(ArrangementConfig(
            trefoil_enabled=t,
            helical_vortex_enabled=h,
            pairing_enabled=p,
            three_velocity_enabled=v3,
        ))
    return configs


def run_batch(
    arrangement_configs: List[ArrangementConfig],
    setup_func: Callable[[Simulation], None],
    cmb_resolution: str = "12"
) -> List[SimulationResult]:
    """
    Run many arrangements with a single particle setup.
    Fast: one setup function, N configs.
    """
    results = []
    for config in arrangement_configs:
        sim = Simulation(cmb_resolution=cmb_resolution)
        sim.arrangement = config
        setup_func(sim)
        results.append(sim.run())
    return results


def run_batch_multi_setup(
    arrangement_configs: List[ArrangementConfig],
    setup_funcs: List[Callable[[Simulation], None]],
    cmb_resolution: str = "12"
) -> List[SimulationResult]:
    """
    Run Cartesian product: configs × setups.
    """
    results = []
    for config in arrangement_configs:
        for setup in setup_funcs:
            sim = Simulation(cmb_resolution=cmb_resolution)
            sim.arrangement = config
            setup(sim)
            results.append(sim.run())
    return results


# -----------------------------------------------------------------------------
# Predefined setup functions
# -----------------------------------------------------------------------------

def setup_single_proton(sim: Simulation) -> None:
    """Single proton at origin."""
    sim.add_proton(np.zeros(3), chirality="R")


def setup_single_proton_L(sim: Simulation) -> None:
    """Single proton L chirality."""
    sim.add_proton(np.zeros(3), chirality="L")


def setup_deuteron(sim: Simulation) -> None:
    """p + n at deuteron separation ~1.94 fm."""
    d = 1.942e-15
    sim.add_proton(np.array([0, 0, 0]), chirality="R")
    sim.add_neutron(np.array([d, 0, 0]), chirality="L")


def setup_deuteron_LR(sim: Simulation) -> None:
    """Deuteron with L-R pairing (full pairing)."""
    setup_deuteron(sim)


def setup_pp_pair(sim: Simulation) -> None:
    """Two protons - L-R for pairing, L-L for Pauli suppressed."""
    d = 2.0e-15
    sim.add_proton(np.array([0, 0, 0]), chirality="R")
    sim.add_proton(np.array([d, 0, 0]), chirality="L")


def setup_pp_nopair(sim: Simulation) -> None:
    """Two protons L-L (Pauli suppressed)."""
    d = 2.0e-15
    sim.add_proton(np.array([0, 0, 0]), chirality="L")
    sim.add_proton(np.array([d, 0, 0]), chirality="L")


def setup_hydrogen(sim: Simulation) -> None:
    """Proton + electron at Bohr radius."""
    sim.add_proton(np.zeros(3), chirality="R")
    sim.add_electron(np.array([5.292e-11, 0, 0]))  # Bohr radius


def setup_alpha(sim: Simulation) -> None:
    """Alpha particle: 2p + 2n in tetrahedral-like arrangement."""
    d = 1.5e-15
    sim.add_proton(np.array([0, 0, 0]), chirality="R")
    sim.add_proton(np.array([d, 0, 0]), chirality="L")
    sim.add_neutron(np.array([d/2, d * 0.866, 0]), chirality="L")
    sim.add_neutron(np.array([d/2, d * 0.289, d * 0.82]), chirality="R")


def setup_isotope(Z: int, A: int):
    """Return a setup function for isotope (Z, A)."""
    def _setup(sim: Simulation) -> None:
        sim.add_nucleus(Z, A)
    return _setup


# -----------------------------------------------------------------------------
# Isotope sweep (all isotopes H through Sn)
# -----------------------------------------------------------------------------

def run_isotope_sweep(
    isotopes: list,
    arrangement_config: Optional[ArrangementConfig] = None,
    cmb_resolution: str = "12"
) -> List[SimulationResult]:
    """
    Run simulation for each (Z, A) in isotopes.
    isotopes: list of (Z, A) tuples
    """
    from .simulation import Simulation, SimulationResult
    config = arrangement_config or ArrangementConfig()
    results = []
    for Z, A in isotopes:
        sim = Simulation(cmb_resolution=cmb_resolution)
        sim.arrangement = config
        sim.add_nucleus(Z, A)
        r = sim.run()
        r.metadata["Z"] = Z
        r.metadata["A"] = A
        results.append(r)
    return results


def run_all_stable_isotopes(
    arrangement_config: Optional[ArrangementConfig] = None,
    cmb_resolution: str = "12"
) -> List[SimulationResult]:
    """Run all stable isotopes from H through Sn."""
    from .isotopes import get_stable_isotopes, ELEMENTS_1_50
    isotopes = []
    for Z, _, _ in ELEMENTS_1_50:
        for iso in get_stable_isotopes(Z):
            isotopes.append((Z, iso.A))
    return run_isotope_sweep(isotopes, arrangement_config, cmb_resolution)


def run_all_isotopes_element(Z: int, cmb_resolution: str = "12") -> List[SimulationResult]:
    """Run all isotopes for element Z."""
    from .isotopes import get_isotopes_for_element
    isotopes = [(iso.Z, iso.A) for iso in get_isotopes_for_element(Z)]
    return run_isotope_sweep(isotopes, ArrangementConfig(), cmb_resolution)


# -----------------------------------------------------------------------------
# Convenience runners
# -----------------------------------------------------------------------------

def quick_sweep_toggles(cmb_resolution: str = "12") -> List[SimulationResult]:
    """
    Quick sweep: all 16 combinations of trefoil, helical, pairing, three_velocity
    with single proton.
    """
    configs = make_arrangement_grid()
    return run_batch(configs, setup_single_proton, cmb_resolution)


def pairing_comparison(cmb_resolution: str = "12") -> List[SimulationResult]:
    """
    Compare L-R (pairing) vs L-L (no pairing) for deuteron and pp.
    """
    configs = [
        ArrangementConfig(pairing_enabled=True),
        ArrangementConfig(pairing_enabled=False),
    ]
    setups = [setup_deuteron, setup_pp_pair, setup_pp_nopair]
    return run_batch_multi_setup(configs, setups, cmb_resolution)


def nuclear_arrangements(cmb_resolution: str = "12") -> List[SimulationResult]:
    """
    Single proton, deuteron, alpha with default arrangement.
    """
    config = [ArrangementConfig()]
    setups = [setup_single_proton, setup_deuteron, setup_alpha]
    return run_batch_multi_setup(config, setups, cmb_resolution)
