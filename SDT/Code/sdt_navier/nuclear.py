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
        Compute binding energy from field energy functional.
        
        PREDICTIVE VERSION: Computes energy as integral of energy density over space.
        No free parameters - uses field values and grid spacing.
        
        B = E_bound - E_free
        where E = ∫ e(r) d³r = ∫ P(r) · σ(r) d³r
        
        Returns
        -------
        B : float
            Binding energy (J)
        """
        # Compute energy from field energy density: e = P · σ
        # where σ = Γ · κ · (1-η) is the diversion density
        
        # Energy density at each grid point
        sigma = self.fields.Gamma * self.fields.kappa * (1 - self.fields.eta)
        e_bound = self.fields.P * sigma  # Energy density (J/m³)
        
        # Integrate over space
        dV = self.fields.dx * self.fields.dy * self.fields.dz
        E_bound = np.sum(e_bound) * dV
        
        # For free state: need to compute energy of separated turbines
        # Create temporary fields with free slip values
        # (This is a simplified approach - full version would run separate simulation)
        
        # Extract turbine regions
        i_p, j_p, k_p = self.proton.position
        i_n, j_n, k_n = self.neutron.position
        radius_cells = self.proton.radius_cells
        
        # Create mask for turbine regions
        i = np.arange(self.fields.nx)
        j = np.arange(self.fields.ny)
        k = np.arange(self.fields.nz)
        I, J, K = np.meshgrid(i, j, k, indexing='ij')
        
        # Distance from proton
        r_p = np.sqrt(
            ((I - i_p) * self.fields.dx)**2 +
            ((J - j_p) * self.fields.dy)**2 +
            ((K - k_p) * self.fields.dz)**2
        )
        mask_p = r_p <= (radius_cells * self.fields.dx)
        
        # Distance from neutron
        r_n = np.sqrt(
            ((I - i_n) * self.fields.dx)**2 +
            ((J - j_n) * self.fields.dy)**2 +
            ((K - k_n) * self.fields.dz)**2
        )
        mask_n = r_n <= (radius_cells * self.fields.dx)
        
        # Compute free state energy (with free slip values)
        # In free state, slip is higher → lower energy
        sigma_free = sigma.copy()
        
        # In proton region: use free slip
        eta_p_free = ProtonTurbine.ETA_P_FREE
        sigma_free[mask_p] = (
            self.fields.Gamma[mask_p] * 
            self.fields.kappa[mask_p] * 
            (1 - eta_p_free)
        )
        
        # In neutron region: use free slip
        eta_n_free = NeutronTurbine.ETA_N_FREE
        sigma_free[mask_n] = (
            self.fields.Gamma[mask_n] * 
            self.fields.kappa[mask_n] * 
            (1 - eta_n_free)
        )
        
        e_free = self.fields.P * sigma_free
        E_free = np.sum(e_free) * dV
        
        # Binding energy
        B = E_bound - E_free
        
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

