"""
SDT 3D Particle CMB Model — Constants

All physical constants from SDT_CORE_AXIOMS_AND_DATASET, Core Engine
Mathematical Proof, and Part I Axioms.
"""

import math

# ==============================================================================
# FUNDAMENTAL CONSTANTS (SDT Dataset)
# ==============================================================================

# Speed of light (propagation speed of spation medium)
C = 2.99792458e8  # m/s

# Fine-structure inverse (hydrogen koppa)
ALPHA_INV = 137.035999  # ≈ 137.036

# Planck length (spation lattice spacing)
L_P = 1.616255e-35  # m

# ==============================================================================
# CMB AND PRESSURE (Core Engine, Dataset)
# ==============================================================================

# CMB pressure at atomic/molecular scale
P_CMB = 2.036e-2  # Pa

# Ambient spation pressure (from CMB)
P_INFINITY = 1.39e-14  # Pa

# Confinement pressure (nuclear QCD bag scale)
P_CONF = 1e34  # Pa

# Spation density (nuclear saturation)
RHO_S = 2.3e17  # kg/m³

# ==============================================================================
# PROTON / TREFOIL (Part I 1.3, TREFoil_NUCLEAR_STRUCTURE_MAPPING)
# ==============================================================================

# Proton radius
R_P = 0.84e-15  # m (0.84 fm)

# Trefoil topology: n=3, m=2
N_POLOIDAL = 3
M_TOROIDAL = 2
DELTA_TOPO = N_POLOIDAL**2 - M_TOROIDAL**2  # 5

# Proton displacement parameter
K_P = math.sqrt(DELTA_TOPO * ALPHA_INV)  # ≈ 26.2

# Minor-to-major radius ratio
A_OVER_R = 1.0 / math.sqrt(2)

# Internal κ from torus geometry
KAPPA_PROTON = (math.pi ** 0.25) / (N_POLOIDAL * (1 + A_OVER_R**2) ** 0.25)  # ≈ 0.694

# Trefoil minor radius
R_MINOR = R_P * A_OVER_R  # ≈ 0.59 fm

# ==============================================================================
# NEUTRON (Dataset 2.1)
# ==============================================================================

# Neutron = p + e_internal; electron bound at trefoil node
R_NODE = (R_P - R_MINOR) * 1e15  # fm, ≈ 0.25 fm

# ==============================================================================
# ELECTRON (Bohr, hydrogen)
# ==============================================================================

# Bohr radius
A_0 = 5.292e-11  # m

# Electron orbital speed (ground state)
V_ELECTRON = 2.188e6  # m/s

# ==============================================================================
# NEUTRINO (Weak_Interactions_from_Neutrino_Circulation)
# ==============================================================================

# Neutrino circulation radius
R_NU = 993 * L_P  # 1.60e-32 m

# ==============================================================================
# CMB / COSMOLOGY (Dataset 3.1)
# ==============================================================================

# Universe radius (static model)
R_UNI = 48e9 * 9.461e15  # m (48 Gly)

# CMB z_boundary
Z_BOUNDARY = 1090

# T_CMB observed
T_CMB = 2.725  # K

# ==============================================================================
# NUCLEAR RADIUS (liquid-drop / nuclear scaling)
# ==============================================================================

# Nuclear radius constant: R = R_N_0 * A^(1/3)
R_N_0 = 1.2e-15  # m (1.2 fm)

# ==============================================================================
# DEUTERON (Dataset 2.2)
# ==============================================================================

D_DEUTERON = 1.942e-15  # m

# ==============================================================================
# CORE ENGINE (Core_Engine_Mathematical_Proof)
# ==============================================================================

# Master equation: Ḋ = P_CMB A_eff Γ κ (1-η)
# Γ = v_poloidal/c (circulation factor)
# κ = 1/r_minor (curvature)
# η = slip factor
