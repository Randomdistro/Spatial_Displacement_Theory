"""
SDT Core Module
Core functionality for Spatial Displacement Theory calculations
"""

from .state_28d import State28D, validate_force_hierarchy

__version__ = "0.1.0"
__all__ = ['State28D', 'validate_force_hierarchy']
