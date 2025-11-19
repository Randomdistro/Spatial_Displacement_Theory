"""
SDT Atomic Calculator

Main calculator class integrating all components.
Pure SDT formulations only - no quantum mechanical postulates.
"""

from typing import List, Tuple, Dict, Optional
import numpy as np
from . import constants as const
from . import hydrogenic
from . import energy_levels
from . import transitions
from . import ionization
from . import elements
from . import geometry


class AtomicCalculator:
    """
    SDT Atomic Calculator.
    
    Calculates energy levels, transitions, ionizations, and geometric structure
    using ONLY SDT formulations and geometric rules.
    """
    
    def __init__(self, element: str, ionization_state: int = 0, isotope: Optional[str] = None):
        """
        Initialize atomic calculator.
        
        Parameters:
        -----------
        element : str
            Element symbol (e.g., 'H', 'He', 'Li')
        ionization_state : int
            Ionization state (0 = neutral, 1 = singly ionized, etc.)
        isotope : str, optional
            Isotope identifier (e.g., '1H', '2H', '4He')
        """
        self.element = element.strip().capitalize()
        self.ionization_state = ionization_state
        self.isotope = isotope
        
        # Get element data
        try:
            self.element_data = elements.get_element_data(self.element)
            self.Z = self.element_data['Z']
            self.effective_Z = self.Z - ionization_state
        except ValueError:
            # Default for unknown elements
            Z_map = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8}
            self.Z = Z_map.get(self.element, 1)
            self.effective_Z = self.Z - ionization_state
            self.element_data = None
        
        # Get electron configuration
        if self.element_data:
            self.base_config = elements.get_ground_state_config(self.element)
        else:
            # Default: single electron in n=1
            self.base_config = [(1, 0)]
        
        # Get isotope data
        if self.isotope:
            try:
                self.isotope_data = elements.get_nuclear_data(self.isotope)
            except ValueError:
                self.isotope_data = None
        else:
            self.isotope_data = None
    
    def energy_level(self, n: int, l: int = 0, j: float = 0.5, F: Optional[float] = None,
                    include_fine: bool = True,
                    include_hf: bool = False,
                    include_lamb: bool = True) -> float:
        """
        Calculate total energy level.
        
        Parameters:
        -----------
        n : int
            Principal quantum number
        l : int
            Angular momentum quantum number
        j : float
            Total angular momentum (j = l ± 1/2)
        F : float, optional
            Total angular momentum including nuclear spin (for hyperfine)
        include_fine : bool
            Include fine structure correction
        include_hf : bool
            Include hyperfine structure correction
        include_lamb : bool
            Include Lamb shift correction
        
        Returns:
        --------
        E : float
            Total energy level (eV)
        """
        return energy_levels.calculate_total_energy(
            n, l, j, F,
            self.effective_Z, self.base_config, self.isotope,
            include_fine, include_hf, include_lamb,
            use_reduced_mass=(self.Z == 1)
        )
    
    def transition(self, initial_state: Tuple[int, int, float],
                  final_state: Tuple[int, int, float],
                  F_i: Optional[float] = None,
                  F_f: Optional[float] = None) -> Dict:
        """
        Calculate transition energy and wavelength.
        
        Parameters:
        -----------
        initial_state : Tuple[int, int, float]
            Initial state (n_i, l_i, j_i)
        final_state : Tuple[int, int, float]
            Final state (n_f, l_f, j_f)
        F_i : float, optional
            Initial total angular momentum (including nuclear spin)
        F_f : float, optional
            Final total angular momentum (including nuclear spin)
        
        Returns:
        --------
        transition : dict
            Dictionary with:
            - 'delta_E': transition energy (eV)
            - 'wavelength': wavelength (nm)
            - 'frequency': frequency (Hz)
            - 'allowed': whether transition is allowed
        """
        n_i, l_i, j_i = initial_state
        n_f, l_f, j_f = final_state
        
        delta_E = transitions.calculate_transition_energy(
            n_i, l_i, j_i, n_f, l_f, j_f,
            self.effective_Z, self.base_config, self.base_config,
            F_i, F_f, self.isotope
        )
        
        wavelength = transitions.calculate_wavelength(delta_E)
        frequency = transitions.calculate_frequency(delta_E)
        allowed = transitions.is_allowed_transition(l_i, l_f, j_i, j_f)
        
        return {
            'delta_E': delta_E,
            'wavelength': wavelength,
            'frequency': frequency,
            'allowed': allowed,
            'initial': initial_state,
            'final': final_state
        }
    
    def ionization(self, ionization_number: int) -> float:
        """
        Calculate ionization energy.
        
        Parameters:
        -----------
        ionization_number : int
            Ionization number (1 = first ionization, 2 = second, etc.)
        
        Returns:
        --------
        IE : float
            Ionization energy (eV)
        """
        return ionization.calculate_ionization_energy(
            self.element, self.ionization_state + ionization_number - 1,
            self.base_config
        )
    
    def all_ionizations(self, max_ionization: Optional[int] = None) -> List[Dict]:
        """
        Calculate all ionization energies.
        
        Parameters:
        -----------
        max_ionization : int, optional
            Maximum ionization state. If None, calculates all up to Z.
        
        Returns:
        --------
        ionizations : List[Dict]
            List of ionization dictionaries with:
            - 'ionization_state': ionization state
            - 'IE': ionization energy (eV)
            - 'element': element symbol
        """
        if max_ionization is None:
            max_ionization = self.Z
        
        return ionization.find_all_ionization_states(self.element)
    
    def spectrum(self, max_n: int = 10, series_types: Optional[List[str]] = None) -> List[Dict]:
        """
        Generate complete spectrum.
        
        Parameters:
        -----------
        max_n : int
            Maximum principal quantum number
        series_types : List[str], optional
            Series types to include. If None, includes all transitions.
            Options: ['Lyman', 'Balmer', 'Paschen', 'Brackett', 'Pfund', 'all']
        
        Returns:
        --------
        spectrum : List[Dict]
            List of all transitions
        """
        if series_types is None or 'all' in series_types:
            # Get all transitions
            return transitions.find_all_transitions(
                max_n, self.effective_Z, self.base_config, allowed_only=False
            )
        else:
            # Get specific series
            spectrum = []
            for series_type in series_types:
                series = transitions.spectral_series(
                    self.element, series_type, max_n, self.ionization_state
                )
                spectrum.extend(series)
            return spectrum
    
    def geometric_structure(self, n: int) -> geometry.GeometricStructure:
        """
        Calculate complete geometric structure for state.
        
        Parameters:
        -----------
        n : int
            Principal quantum number
        
        Returns:
        --------
        structure : GeometricStructure
            Complete geometric structure with all speeds and distances
        """
        return geometry.analyze_geometric_structure(
            n, self.Z, self.ionization_state,
            use_reduced_mass=(self.Z == 1)
        )
    
    def __repr__(self) -> str:
        """String representation."""
        return f"AtomicCalculator(element='{self.element}', Z={self.Z}, ionization_state={self.ionization_state})"

