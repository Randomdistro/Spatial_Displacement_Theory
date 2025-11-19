"""
SDT Physical Constants and Parameters

All constants from CODATA 2018 and Phase documents.
"""

import numpy as np

# ============================================================================
# Fundamental Physical Constants (CODATA 2018)
# ============================================================================

# Speed of light
C = 2.99792458e8  # m/s

# Planck constant
H = 6.62607015e-34  # J·s
HBAR = 1.054571817e-34  # J·s = h/(2π)

# Elementary charge
E_CHARGE = 1.602176634e-19  # C

# Vacuum permittivity
EPSILON_0 = 8.8541878128e-12  # F/m

# Electron mass
M_E = 9.1093837015e-31  # kg

# Proton mass
M_P = 1.67262192369e-27  # kg

# Neutron mass
M_N = 1.67492749804e-27  # kg

# Fine structure constant
ALPHA = 7.2973525693e-3  # dimensionless
ALPHA_INV = 137.035999084  # 1/α

# ============================================================================
# Derived Constants
# ============================================================================

# Coulomb constant
K_E = 1.0 / (4.0 * np.pi * EPSILON_0)  # N·m²/C²

# Bohr radius
A_0 = 5.29177210903e-11  # m

# Rydberg energy (for infinite mass nucleus)
RYDBERG_EV = 13.605693122994  # eV
RYDBERG_J = RYDBERG_EV * E_CHARGE  # J

# Rydberg constant
RYDBERG_INV_M = 10973731.568160  # m⁻¹

# hc in eV·nm (for wavelength calculations)
HC_EV_NM = 1239.841984  # eV·nm

# Reduced mass for hydrogen
MU_H = M_E * M_P / (M_E + M_P)  # kg
REDUCED_MASS_FACTOR_H = MU_H / M_E  # ≈ 0.9994556

# ============================================================================
# SDT-Specific Parameters (from Phase documents)
# ============================================================================

# Spation medium properties (Phase 20)
K_BULK = 4.6e113  # Pa (bulk modulus)
RHO_S = 5.2e96  # kg/m³ (spation density)
R_PLANCK = 1.616e-35  # m (Planck radius)

# Proton parameters (Phase 27A, Phase 4)
R_P = 0.8414e-15  # m (proton charge radius, CODATA 2018)
R_P_FM = 0.8414  # fm
V_DISP_P = None  # m³ (to be calibrated, see Phase_27A)

# Electron parameters (Phase 27A)
D_E = 1e-21  # m (effective hard-sphere diameter, typical value)
R_E_CLASSICAL = 2.818e-15  # m (classical electron radius)
LAMBDA_C = 2.42631023867e-12  # m (Compton wavelength)
V_DISP_E = None  # m³ (to be calibrated, see Phase_27A)

# Geometric efficiency factor (Phase 27A)
KAPPA = 1.0  # dimensionless (typically ≈ 1)

# Universal compressibility constant (Phase 5, Phase 8)
BETA_GEOM = 0.951  # dimensionless

# Geometric factors
BETA_COMP = 0.0  # displacement volume compression (typically 0, Phase 27A)
EPSILON = 2.0  # toroidal aspect ratio (typical value, Phase 27A)
GAMMA_CIRC = 0.0  # vortex circulation coupling (typically 0 for single electron)
L_WAKE = LAMBDA_C  # wake persistence length (Phase 27A)

# Nuclear g-factors (CODATA 2018)
G_E = 2.00231930436  # electron g-factor
G_P = 5.5856946893  # proton g-factor
G_N = -3.82608545  # neutron g-factor

# Nuclear magneton
MU_N = E_CHARGE * HBAR / (2.0 * M_P)  # J/T

# Bohr magneton
MU_B = E_CHARGE * HBAR / (2.0 * M_E)  # J/T

# ============================================================================
# K-Factor (Ϟ) Relationships (Phase 2, Phase 16)
# ============================================================================

def calculate_K_factor(n: int, Z: int = 1) -> float:
    """
    Calculate K-factor (Ϟ) for hydrogenic atom.
    
    From Phase 2: Ϟ_n = n/(Zα)
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    Z : int
        Atomic number (default: 1 for hydrogen)
    
    Returns:
    --------
    K : float
        K-factor (dimensionless)
    """
    return n / (Z * ALPHA)


def calculate_orbital_velocity_at_radius(r: float, K: float, R_ref: float = None) -> float:
    """
    Calculate orbital velocity at radius r using SDT orbital law.
    
    From Phase 16: v(r) = (c/K) * sqrt(R/r)
    
    Parameters:
    -----------
    r : float
        Orbital radius (m)
    K : float
        K-factor (Ϟ)
    R_ref : float, optional
        Reference radius (m). If None, uses Bohr radius for atomic systems.
    
    Returns:
    --------
    v : float
        Orbital velocity (m/s)
    """
    if R_ref is None:
        R_ref = A_0  # Default to Bohr radius for atomic systems
    
    return (C / K) * np.sqrt(R_ref / r)


def calculate_c_boundary_radius(K: float, R_ref: float = None) -> float:
    """
    Calculate c-boundary radius (ϟ) where orbital velocity equals c.
    
    From Phase 16: ϟ = R/K²
    
    Parameters:
    -----------
    K : float
        K-factor (Ϟ)
    R_ref : float, optional
        Reference radius (m). If None, uses Bohr radius for atomic systems.
    
    Returns:
    --------
    s : float
        c-boundary radius (m) where v(ϟ) = c
    """
    if R_ref is None:
        R_ref = A_0
    
    return R_ref / (K ** 2)

