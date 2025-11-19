"""
Element Database

Element data, nuclear data, and reference experimental values.
"""

from typing import Dict, Optional, Tuple, List
from .constants import *


# Element database
ELEMENT_DATA = {
    'H': {
        'Z': 1,
        'name': 'Hydrogen',
        'mass': 1.007825,  # Atomic mass (u)
        'ground_state': [(1, 0)],  # [(n, l), ...]
        'isotopes': ['1H', '2H', '3H'],
        'ionization_energies': [13.59843]  # eV, experimental
    },
    'He': {
        'Z': 2,
        'name': 'Helium',
        'mass': 4.002602,
        'ground_state': [(1, 0), (1, 0)],
        'isotopes': ['3He', '4He'],
        'ionization_energies': [24.58741, 54.41778]
    },
    'Li': {
        'Z': 3,
        'name': 'Lithium',
        'mass': 7.016004,
        'ground_state': [(1, 0), (1, 0), (2, 0)],
        'isotopes': ['6Li', '7Li'],
        'ionization_energies': [5.39172, 75.6400, 122.454]
    },
    'Be': {
        'Z': 4,
        'name': 'Beryllium',
        'mass': 9.012182,
        'ground_state': [(1, 0), (1, 0), (2, 0), (2, 0)],
        'isotopes': ['9Be'],
        'ionization_energies': [9.32270, 18.21115, 153.896, 217.718]
    },
    'B': {
        'Z': 5,
        'name': 'Boron',
        'mass': 11.009305,
        'ground_state': [(1, 0), (1, 0), (2, 0), (2, 0), (2, 1)],
        'isotopes': ['10B', '11B'],
        'ionization_energies': [8.29803, 25.15484, 37.93064, 259.37, 340.22]
    },
    'C': {
        'Z': 6,
        'name': 'Carbon',
        'mass': 12.0,
        'ground_state': [(1, 0), (1, 0), (2, 0), (2, 0), (2, 1), (2, 1)],
        'isotopes': ['12C', '13C'],
        'ionization_energies': [11.26030, 24.38332, 47.88779, 64.49388, 392.087, 489.993]
    },
    'N': {
        'Z': 7,
        'name': 'Nitrogen',
        'mass': 14.003074,
        'ground_state': [(1, 0), (1, 0), (2, 0), (2, 0), (2, 1), (2, 1), (2, 1)],
        'isotopes': ['14N', '15N'],
        'ionization_energies': [14.53414, 29.60130, 47.44924, 77.47347, 97.89014, 552.0718, 667.046]
    },
    'O': {
        'Z': 8,
        'name': 'Oxygen',
        'mass': 15.994915,
        'ground_state': [(1, 0), (1, 0), (2, 0), (2, 0), (2, 1), (2, 1), (2, 1), (2, 1)],
        'isotopes': ['16O', '17O', '18O'],
        'ionization_energies': [13.61806, 35.12112, 54.93555, 77.41353, 113.8990, 138.1189, 739.29, 871.41]
    },
}


# Nuclear data
NUCLEAR_DATA = {
    '1H': {
        'g_factor': G_P,
        'spin': 0.5,
        'mass': M_P,
        'radius': R_P
    },
    '2H': {
        'g_factor': 0.8574382311,
        'spin': 1.0,
        'mass': M_P + M_N,  # Approximate
        'radius': 2.1e-15  # Approximate
    },
    '4He': {
        'g_factor': 0.0,
        'spin': 0.0,
        'mass': 2 * M_P + 2 * M_N,  # Approximate
        'radius': 1.7e-15  # Approximate
    },
}


def get_element_data(element: str) -> Dict:
    """
    Get element data.
    
    Parameters:
    -----------
    element : str
        Element symbol (e.g., 'H', 'He')
    
    Returns:
    --------
    data : dict
        Element data dictionary
    """
    element = element.strip().capitalize()
    if element not in ELEMENT_DATA:
        raise ValueError(f"Element {element} not found in database")
    
    return ELEMENT_DATA[element].copy()


def get_nuclear_data(isotope: str) -> Dict:
    """
    Get nuclear data for isotope.
    
    Parameters:
    -----------
    isotope : str
        Isotope identifier (e.g., '1H', '2H', '4He')
    
    Returns:
    --------
    data : dict
        Nuclear data dictionary
    """
    isotope = isotope.strip()
    if isotope not in NUCLEAR_DATA:
        raise ValueError(f"Isotope {isotope} not found in database")
    
    return NUCLEAR_DATA[isotope].copy()


def get_ground_state_config(element: str) -> List[Tuple[int, int]]:
    """
    Get ground state electron configuration.
    
    Parameters:
    -----------
    element : str
        Element symbol
    
    Returns:
    --------
    config : List[Tuple[int, int]]
        Ground state configuration [(n, l), ...]
    """
    data = get_element_data(element)
    return data['ground_state'].copy()


def get_ionization_energies(element: str) -> List[float]:
    """
    Get experimental ionization energies.
    
    Parameters:
    -----------
    element : str
        Element symbol
    
    Returns:
    --------
    IEs : List[float]
        List of ionization energies (eV)
    """
    data = get_element_data(element)
    return data['ionization_energies'].copy()

