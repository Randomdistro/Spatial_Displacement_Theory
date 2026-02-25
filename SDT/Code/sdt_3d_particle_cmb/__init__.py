"""
SDT 3D Particle CMB Model

A 3D calculative model for proton, neutron, electron, neutrino, and spation
with CMB EM shunt kinetics (pressure-density mechanics), configurable
directional CMB (12-direction dodecahedral up to fine resolution), and
toggleable SDT arrangements (6π trefoils, helical vortices, pairing, etc.).

Integrates SDT formulations from SDT_CORE_AXIOMS_AND_DATASET, Core Engine
Mathematical Proof, and Part I Axioms.
"""

from .constants import *
from .cmb_directional import CMBDirectional
from .pressure_mechanics import PressureMechanics
from .particles import Proton, Neutron, Electron, Neutrino, Spation
from .arrangements import ArrangementConfig
from .simulation import Simulation, SimulationResult
from .batch_runner import run_batch, run_batch_multi_setup, make_arrangement_grid
from .isotopes import (
    Isotope,
    get_isotope,
    get_isotopes_for_element,
    get_all_isotopes_up_to_tin,
    ELEMENTS_1_50,
)
from .nucleus import build_nucleus, nuclear_radius

__version__ = "0.2.0"
