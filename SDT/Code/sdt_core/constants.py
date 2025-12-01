"""
SDT Core Constants
Central repository for all physical constants and parameters in Spatial Displacement Theory.
"""

# ==============================================================================
# FUNDAMENTAL CONSTANTS
# ==============================================================================

# The Lattice Limit (Speed of Light) in m/s
C_LATTICE = 299792458.0

# Spation Density (rho_s) in kg/m^3
# Derived from Phase 15 calculations
RHO_S = 5.2e96

# ==============================================================================
# CELESTIAL BODIES (Phase 15 Parameters)
# ==============================================================================
# Replaces Mass/G/Beta with R_eff (Effective Radius) and Kappa (Velocity Factor).
# a = c^2 * R_eff / (Kappa^2 * r^2)

CELESTIAL_BODIES = {
    'Sun':     {'R_eff': 6.957e8, 'Kappa': 6.86398e2},
    'Mercury': {'R_eff': 2.4397e6, 'Kappa': 9.97613e4},
    'Venus':   {'R_eff': 6.0518e6, 'Kappa': 4.09181e4},
    'Earth':   {'R_eff': 6.371e6, 'Kappa': 3.79014e4},
    'Mars':    {'R_eff': 3.390e6, 'Kappa': 8.43441e4},
    'Jupiter': {'R_eff': 6.991e7, 'Kappa': 7.04247e3},
    'Saturn':  {'R_eff': 5.8232e7, 'Kappa': 1.17464e4},
    'Uranus':  {'R_eff': 2.5362e7, 'Kappa': 1.98347e4},
    'Neptune': {'R_eff': 2.4622e7, 'Kappa': 1.79914e4}
}

# ==============================================================================
# FIELD PARAMETERS (NAVIER)
# ==============================================================================

# Curvature force coefficient (N*m^2)
# Drives flow from high to low curvature
ALPHA_CURV = 1.0e-10

# Slip damping coefficient (kg/(m^3*s))
# Represents energy loss to slip (heat, radiation)
BETA_SLIP = 1.0e15

# Curvature creation coefficient (m^2/s)
# Creation by converging flow
GAMMA_CREATE = 1.0e-24

# Curvature destruction coefficient (1/s)
# Destruction via slip
DELTA_DESTROY = 1.0e-9

# Slip strain coefficient (m^2/s)
# Slip increase from strain
EPSILON_STRAIN = 1.0e-24

# Slip healing coefficient (m/s)
# Slip decrease from stable curvature
ZETA_HEAL = 1.0e-9

# ==============================================================================
# ATOMIC & NUCLEAR PARAMETERS (Neutron Regime)
# ==============================================================================

# Neutron Genesis Velocity (Phase Velocity at Proton Surface)
# v = c * sqrt(r_e / R_p)
NEUTRON_GENESIS_VELOCITY = 1.836 * C_LATTICE

# Geometric Anomaly Ratio (Schwinger Term)
# a_e = r_e / lambda_C = alpha / 2pi
ANOMALY_RATIO = 0.00116140973

