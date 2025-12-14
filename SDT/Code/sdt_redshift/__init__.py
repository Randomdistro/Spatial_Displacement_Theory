"""
SDT Redshift Module
-------------------

Numerical implementation of the SDT redshift compensator described in
`SDT/Code/sdt_redshift/sdt_redshift.md`.
"""

from .calculator import RedshiftCalculator, StrainModelParameters

__all__ = ["RedshiftCalculator", "StrainModelParameters"]
__version__ = "0.2.0"
