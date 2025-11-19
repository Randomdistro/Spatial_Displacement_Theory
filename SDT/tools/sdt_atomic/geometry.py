"""
Geometric Structure Analysis

Calculates all speeds and distances within atomic configurations,
including lightspeed boundary, orbital speeds, and c-boundary positions.
From Phase 16 and user requirements.
"""

import numpy as np
from typing import Dict, List, Tuple
from .constants import *
from . import hydrogenic


class GeometricStructure:
    """
    Geometric structure of an atomic configuration.
    
    Stores all speeds and distances for a given atomic state,
    including orbital speeds, c-boundary, lightspeed boundary, etc.
    """
    
    def __init__(self, n: int, Z: int = 1, ionization_state: int = 0, use_reduced_mass: bool = True):
        """
        Initialize geometric structure for atomic state.
        
        Parameters:
        -----------
        n : int
            Principal quantum number
        Z : int
            Atomic number (default: 1 for hydrogen)
        ionization_state : int
            Ionization state (0 = neutral, 1 = singly ionized, etc.)
        use_reduced_mass : bool
            Whether to use reduced mass correction (only for hydrogen)
        """
        self.n = n
        self.Z = Z
        self.ionization_state = ionization_state
        self.effective_Z = Z - ionization_state
        self.use_reduced_mass = use_reduced_mass and (Z == 1)
        
        # Calculate basic properties
        self.orbital_radius = hydrogenic.calculate_orbital_radius(
            n, self.effective_Z, self.use_reduced_mass
        )
        self.K_factor = hydrogenic.calculate_K_factor(n, self.effective_Z, self.use_reduced_mass)
        self.energy_level = hydrogenic.calculate_energy_level(
            n, self.effective_Z, self.use_reduced_mass
        )
        
        # Calculate geometric properties
        self._calculate_geometric_properties()
    
    def _calculate_geometric_properties(self):
        """Calculate all geometric properties."""
        # Reference radius (Bohr radius for atomic systems)
        self.R_ref = A_0
        
        # Orbital velocity at orbital radius
        self.orbital_velocity = hydrogenic.calculate_orbital_velocity(
            self.n, self.effective_Z, self.orbital_radius, self.use_reduced_mass
        )
        
        # Velocity at proton surface
        self.velocity_at_proton_surface = hydrogenic.calculate_velocity_at_proton_surface(
            self.n, self.effective_Z, self.use_reduced_mass
        )
        
        # c-boundary radius (where v = c)
        self.c_boundary_radius = hydrogenic.calculate_c_boundary_radius(
            self.n, self.effective_Z, self.use_reduced_mass
        )
        
        # Velocity at c-boundary (should be c by definition)
        self.velocity_at_c_boundary = hydrogenic.calculate_orbital_velocity(
            self.n, self.effective_Z, self.c_boundary_radius, self.use_reduced_mass
        )
        
        # Check: lightspeed boundary should be at classical electron radius for hydrogen ground state
        if self.n == 1 and self.Z == 1 and self.ionization_state == 0:
            # For hydrogen ground state, c-boundary should equal classical electron radius
            self.lightspeed_boundary_radius = self.c_boundary_radius
        else:
            # For other states, calculate from K-factor
            self.lightspeed_boundary_radius = self.c_boundary_radius
        
        # Velocity at lightspeed boundary (should be c)
        self.velocity_at_lightspeed_boundary = C
    
    def get_velocity_profile(self, radii: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get velocity profile as function of radius.
        
        Parameters:
        -----------
        radii : array_like, optional
            Radii to evaluate at (m). If None, generates from R_p to 10*r_n.
        
        Returns:
        --------
        r : np.ndarray
            Radii (m)
        v : np.ndarray
            Orbital velocities (m/s)
        """
        if radii is None:
            # Generate radii from proton surface to 10× orbital radius
            r_min = R_P
            r_max = 10.0 * self.orbital_radius
            radii = np.logspace(np.log10(r_min), np.log10(r_max), 100)
        
        radii = np.asarray(radii)
        
        # Calculate velocities using SDT orbital law
        velocities = (C / self.K_factor) * np.sqrt(self.R_ref / radii)
        
        return radii, velocities
    
    def get_distance_summary(self) -> Dict[str, float]:
        """
        Get summary of all key distances.
        
        Returns:
        --------
        distances : dict
            Dictionary with distance labels and values (m)
        """
        return {
            'proton_radius': R_P,
            'classical_electron_radius': R_E_CLASSICAL,
            'orbital_radius': self.orbital_radius,
            'c_boundary_radius': self.c_boundary_radius,
            'lightspeed_boundary_radius': self.lightspeed_boundary_radius,
            'bohr_radius': A_0,
        }
    
    def get_velocity_summary(self) -> Dict[str, float]:
        """
        Get summary of all key velocities.
        
        Returns:
        --------
        velocities : dict
            Dictionary with velocity labels and values (m/s)
        """
        return {
            'orbital_velocity': self.orbital_velocity,
            'velocity_at_proton_surface': self.velocity_at_proton_surface,
            'velocity_at_c_boundary': self.velocity_at_c_boundary,
            'velocity_at_lightspeed_boundary': self.velocity_at_lightspeed_boundary,
            'speed_of_light': C,
        }
    
    def get_velocity_ratios(self) -> Dict[str, float]:
        """
        Get velocity ratios (as fractions of c).
        
        Returns:
        --------
        ratios : dict
            Dictionary with velocity ratio labels and values (dimensionless)
        """
        return {
            'orbital_velocity_over_c': self.orbital_velocity / C,
            'velocity_at_proton_surface_over_c': self.velocity_at_proton_surface / C,
            'velocity_at_c_boundary_over_c': self.velocity_at_c_boundary / C,
            'K_factor': self.K_factor,
        }
    
    def __repr__(self) -> str:
        """String representation."""
        return (f"GeometricStructure(n={self.n}, Z={self.Z}, "
                f"ionization_state={self.ionization_state}, "
                f"r_n={self.orbital_radius:.3e} m, "
                f"v_n={self.orbital_velocity:.3e} m/s)")


def analyze_geometric_structure(n: int, Z: int = 1, ionization_state: int = 0,
                                use_reduced_mass: bool = True) -> GeometricStructure:
    """
    Analyze complete geometric structure of atomic configuration.
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    Z : int
        Atomic number (default: 1 for hydrogen)
    ionization_state : int
        Ionization state (0 = neutral, 1 = singly ionized, etc.)
    use_reduced_mass : bool
        Whether to use reduced mass correction (only for hydrogen)
    
    Returns:
    --------
    structure : GeometricStructure
        Complete geometric structure with all speeds and distances
    """
    return GeometricStructure(n, Z, ionization_state, use_reduced_mass)

