"""
Nuclear System Models for SDT-Navier

Defines turbine cells for protons and neutrons, and implements nuclear systems:
- Deuteron (p-n)
- Triton (³H: n-p-n)
- Helion (³He: p-n-p)
- Alpha (⁴He: 2p-2n tetrahedral)

All parameters from Phase 19.
"""

import numpy as np
from typing import Tuple, Optional, List
from dataclasses import dataclass

from .fields import FieldSystem, initialize_fields, add_turbine_source
from .solver import SDTNavierSolver
from .equations import SDTNavierEquations


@dataclass
class TurbineCell:
    """
    Base class for a turbine cell (proton or neutron).
    """
    position: Tuple[int, int, int]  # Grid indices
    radius_cells: float  # Radius in grid cells
    kappa: float  # Curvature density (m⁻¹)
    Gamma: float  # Circulation factor
    eta: float  # Slip (0 ≤ η ≤ 1)
    cell_type: str  # "proton" or "neutron"


class ProtonTurbine(TurbineCell):
    """
    Proton turbine cell with parameters from Phase 19.
    """
    
    # Phase 19 parameters
    R_P = 8.40e-16  # m (proton radius)
    KAPPA_P = 1.190e15  # m⁻¹ (1/R_p)
    GAMMA_P = 0.546  # Circulation factor
    ETA_P_BOUND = 0.0003  # Slip when bound (1 - 0.9997)
    ETA_P_FREE = 0.0003  # Slip when free (approximately same)
    
    def __init__(
        self,
        position: Tuple[int, int, int],
        radius_cells: float,
        bound: bool = True,
    ):
        """
        Initialize proton turbine.
        
        Parameters
        ----------
        position : tuple (i, j, k)
            Grid indices of turbine center
        radius_cells : float
            Turbine radius in grid cells
        bound : bool
            Whether proton is bound (affects slip)
        """
        eta = self.ETA_P_BOUND if bound else self.ETA_P_FREE
        
        super().__init__(
            position=position,
            radius_cells=radius_cells,
            kappa=self.KAPPA_P,
            Gamma=self.GAMMA_P,
            eta=eta,
            cell_type="proton",
        )


class NeutronTurbine(TurbineCell):
    """
    Neutron turbine cell with parameters from Phase 19.
    
    Neutron is composite: internal electron orbit with higher slip.
    """
    
    # Phase 19 parameters
    R_N = 8.70e-16  # m (neutron radius)
    R_E_N = 3.00e-15  # m (internal electron orbit radius)
    KAPPA_N = 1.0 / R_N  # m⁻¹
    KAPPA_E_N = 3.333e14  # m⁻¹ (1/R_E_N)
    GAMMA_E_N = 0.531  # Internal electron circulation
    ETA_N_BOUND = 0.0019  # Slip when bound (1 - 0.9981)
    ETA_N_FREE = 0.9981  # Slip when free (high, unstable)
    
    def __init__(
        self,
        position: Tuple[int, int, int],
        radius_cells: float,
        bound: bool = True,
    ):
        """
        Initialize neutron turbine.
        
        Parameters
        ----------
        position : tuple (i, j, k)
            Grid indices of turbine center
        radius_cells : float
            Turbine radius in grid cells
        bound : bool
            Whether neutron is bound (affects slip significantly)
        """
        eta = self.ETA_N_BOUND if bound else self.ETA_N_FREE
        
        super().__init__(
            position=position,
            radius_cells=radius_cells,
            kappa=self.KAPPA_N,
            Gamma=self.GAMMA_E_N,  # Use internal electron circulation
            eta=eta,
            cell_type="neutron",
        )


class DeuteronSystem:
    """
    Deuteron (²H): p-n two-cell system.
    
    Binding energy: B = 2.224 MeV
    Separation: r ≈ 2 fm
    """
    
    BINDING_ENERGY_EXP = 2.224e6 * 1.602e-19  # J (2.224 MeV)
    SEPARATION = 2.0e-15  # m (2 fm)
    
    def __init__(
        self,
        fields: FieldSystem,
        center: Tuple[int, int, int],
        separation_cells: float,
        equations: Optional[SDTNavierEquations] = None,
    ):
        """
        Initialize deuteron system.
        
        Parameters
        ----------
        fields : FieldSystem
            Field system to add turbines to
        center : tuple (i, j, k)
            Center of mass position
        separation_cells : float
            Separation between p and n in grid cells
        equations : SDTNavierEquations, optional
            Equations for solver. If None, use defaults.
        """
        self.fields = fields
        self.center = center
        self.separation_cells = separation_cells
        
        # Calculate positions
        # Place proton and neutron along x-axis
        dx = separation_cells * fields.dx
        i0, j0, k0 = center
        
        # Proton at -dx/2, neutron at +dx/2
        i_p = int(i0 - separation_cells / 2)
        i_n = int(i0 + separation_cells / 2)
        
        # Turbine radius in cells (proton radius ~ 0.84 fm, grid spacing ~ 0.1-0.2 fm)
        radius_cells = max(1.0, 0.84e-15 / fields.dx)
        
        # Create turbines
        self.proton = ProtonTurbine(
            position=(i_p, j0, k0),
            radius_cells=radius_cells,
            bound=True,
        )
        
        self.neutron = NeutronTurbine(
            position=(i_n, j0, k0),
            radius_cells=radius_cells,
            bound=True,
        )
        
        # Add turbines to fields
        add_turbine_source(
            fields,
            self.proton.position,
            self.proton.radius_cells,
            self.proton.kappa,
            self.proton.Gamma,
            self.proton.eta,
            profile="gaussian",
        )
        
        add_turbine_source(
            fields,
            self.neutron.position,
            self.neutron.radius_cells,
            self.neutron.kappa,
            self.neutron.Gamma,
            self.neutron.eta,
            profile="gaussian",
        )
        
        # Store equations for binding energy calculation
        self.equations = equations or SDTNavierEquations()
    
    def compute_binding_energy(self) -> float:
        """
        Compute binding energy from energy balance.
        
        B = Σ_i P_∞ Γ_i κ_i (1-η_i)|bound - Σ_i P_∞ Γ_i κ_i (1-η_i)|free
        
        Returns
        -------
        B : float
            Binding energy (J)
        """
        # Energy per unit volume from master equation
        # For bound state: use current field values
        sigma_bound = (
            self.proton.Gamma * self.proton.kappa * (1 - self.proton.eta) +
            self.neutron.Gamma * self.neutron.kappa * (1 - self.neutron.eta)
        )
        
        # For free state: use free slip values
        proton_free = ProtonTurbine(
            self.proton.position,
            self.proton.radius_cells,
            bound=False,
        )
        neutron_free = NeutronTurbine(
            self.neutron.position,
            self.neutron.radius_cells,
            bound=False,
        )
        
        sigma_free = (
            proton_free.Gamma * proton_free.kappa * (1 - proton_free.eta) +
            neutron_free.Gamma * neutron_free.kappa * (1 - neutron_free.eta)
        )
        
        # Energy difference per unit volume
        P_infinity = 1.65e31  # Pa (nuclear scale)
        delta_sigma = sigma_bound - sigma_free
        
        # Convert to total energy
        # Approximate volume: 4π/3 * (separation/2)^3 for each turbine
        volume_per_turbine = (4.0 * np.pi / 3.0) * (self.SEPARATION / 2.0)**3
        total_volume = 2.0 * volume_per_turbine
        
        # Binding energy
        B = P_infinity * delta_sigma * total_volume
        
        # Characteristic time
        tau_char = 8.4e-16 / 2.998e8  # ~2.8e-24 s
        B = B * tau_char
        
        return B
    
    def compute_binding_energy_mev(self) -> float:
        """
        Compute binding energy in MeV.
        
        Returns
        -------
        B_mev : float
            Binding energy (MeV)
        """
        B_j = self.compute_binding_energy()
        B_mev = B_j / (1.602e-13)  # Convert J to MeV
        return B_mev


class TritonSystem:
    """
    Triton (³H): n-p-n linear configuration.
    
    Binding energy: B = 8.482 MeV
    """
    
    BINDING_ENERGY_EXP = 8.482e6 * 1.602e-19  # J
    
    def __init__(
        self,
        fields: FieldSystem,
        center: Tuple[int, int, int],
        separation_cells: float,
    ):
        """
        Initialize triton system (n-p-n).
        """
        self.fields = fields
        self.center = center
        
        i0, j0, k0 = center
        radius_cells = max(1.0, 0.84e-15 / fields.dx)
        
        # Linear: n - p - n
        self.neutron1 = NeutronTurbine((i0 - separation_cells, j0, k0), radius_cells, bound=True)
        self.proton = ProtonTurbine((i0, j0, k0), radius_cells, bound=True)
        self.neutron2 = NeutronTurbine((i0 + separation_cells, j0, k0), radius_cells, bound=True)
        
        for turbine in [self.neutron1, self.proton, self.neutron2]:
            add_turbine_source(
                fields,
                turbine.position,
                turbine.radius_cells,
                turbine.kappa,
                turbine.Gamma,
                turbine.eta,
                profile="gaussian",
            )


class HelionSystem:
    """
    Helion (³He): p-n-p linear configuration.
    
    Binding energy: B = 7.718 MeV
    """
    
    BINDING_ENERGY_EXP = 7.718e6 * 1.602e-19  # J
    
    def __init__(
        self,
        fields: FieldSystem,
        center: Tuple[int, int, int],
        separation_cells: float,
    ):
        """
        Initialize helion system (p-n-p).
        """
        self.fields = fields
        self.center = center
        
        i0, j0, k0 = center
        radius_cells = max(1.0, 0.84e-15 / fields.dx)
        
        # Linear: p - n - p
        self.proton1 = ProtonTurbine((i0 - separation_cells, j0, k0), radius_cells, bound=True)
        self.neutron = NeutronTurbine((i0, j0, k0), radius_cells, bound=True)
        self.proton2 = ProtonTurbine((i0 + separation_cells, j0, k0), radius_cells, bound=True)
        
        for turbine in [self.proton1, self.neutron, self.proton2]:
            add_turbine_source(
                fields,
                turbine.position,
                turbine.radius_cells,
                turbine.kappa,
                turbine.Gamma,
                turbine.eta,
                profile="gaussian",
            )


class AlphaSystem:
    """
    Alpha particle (⁴He): 2p-2n tetrahedral configuration.
    
    Binding energy: B = 28.296 MeV
    """
    
    BINDING_ENERGY_EXP = 28.296e6 * 1.602e-19  # J
    
    def __init__(
        self,
        fields: FieldSystem,
        center: Tuple[int, int, int],
        separation_cells: float,
    ):
        """
        Initialize alpha system (tetrahedral 2p-2n).
        """
        self.fields = fields
        self.center = center
        
        i0, j0, k0 = center
        radius_cells = max(1.0, 0.84e-15 / fields.dx)
        
        # Tetrahedral positions (simplified: place in plane for now)
        # In full 3D, would use tetrahedral coordinates
        positions = [
            (i0 - separation_cells, j0, k0),  # p1
            (i0 + separation_cells, j0, k0),  # p2
            (i0, j0 - separation_cells, k0),  # n1
            (i0, j0 + separation_cells, k0),  # n2
        ]
        
        self.proton1 = ProtonTurbine(positions[0], radius_cells, bound=True)
        self.proton2 = ProtonTurbine(positions[1], radius_cells, bound=True)
        self.neutron1 = NeutronTurbine(positions[2], radius_cells, bound=True)
        self.neutron2 = NeutronTurbine(positions[3], radius_cells, bound=True)
        
        for turbine in [self.proton1, self.proton2, self.neutron1, self.neutron2]:
            add_turbine_source(
                fields,
                turbine.position,
                turbine.radius_cells,
                turbine.kappa,
                turbine.Gamma,
                turbine.eta,
                profile="gaussian",
            )

