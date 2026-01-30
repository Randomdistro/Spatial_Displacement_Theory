"""
Geometric Screening Calculations - Actual Science
================================================

Calculate screening from geometry:
- Solid angle occlusion from other electrons/nucleons
- Spatial blocking of fields
- Actual geometric calculations, not "effective charge"
"""

import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass

# CODATA 2018
C = 2.99792458e8  # m/s
HBAR = 1.054571817e-34  # J·s
E_CHARGE = 1.602176634e-19  # C
EPSILON_0 = 8.8541878128e-12  # F/m
M_E = 9.1093837015e-31  # kg
K_E = 1.0 / (4.0 * np.pi * EPSILON_0)
A_0 = 5.29177210903e-11  # m

# Physical scales
R_PROTON = 0.84e-15  # m (proton radius)
R_NEUTRON = 0.84e-15  # m
R_ELECTRON = 2.818e-15  # m (classical electron radius)

@dataclass
class Particle:
    """Particle with position and radius."""
    position: np.ndarray  # 3D position (m)
    radius: float  # Effective radius (m)
    type: str  # 'p', 'n', 'e'

def solid_angle_occlusion(R: float, d: float) -> float:
    """
    Calculate solid angle occlusion of a sphere of radius R at distance d.
    
    Formula: Ω = 2π(1 - cos(θ)) where sin(θ) = R/d
    
    Returns: Solid angle in steradians
    """
    if d <= R:
        return 2.0 * np.pi  # Full immersion
    
    sin_theta = R / d
    if sin_theta >= 1.0:
        return 2.0 * np.pi
    
    cos_theta = np.sqrt(1.0 - sin_theta * sin_theta)
    omega = 2.0 * np.pi * (1.0 - cos_theta)
    
    return omega

def occlusion_fraction(R: float, d: float) -> float:
    """
    Calculate occlusion fraction (fraction of 4π steradians blocked).
    
    For small angles: E ≈ R²/(4r²)
    Exact: E = Ω/(4π) where Ω = 2π(1 - cos(θ))
    """
    omega = solid_angle_occlusion(R, d)
    return omega / (4.0 * np.pi)

def calculate_geometric_screening(target_electron: Particle,
                                  other_particles: List[Particle],
                                  nucleus_center: np.ndarray) -> float:
    """
    Calculate geometric screening factor for target electron.
    
    Screening = how much field is blocked by other particles between
    target electron and nucleus.
    
    Returns: Screening factor (0 = fully screened, 1 = no screening)
    """
    # Position of target electron
    r_target = np.linalg.norm(target_electron.position - nucleus_center)
    direction_target = (target_electron.position - nucleus_center) / r_target
    
    # Total occlusion from all other particles
    total_occlusion = 0.0
    
    for other in other_particles:
        # Skip self
        if np.allclose(other.position, target_electron.position):
            continue
        
        # Position of other particle
        r_other = np.linalg.norm(other.position - nucleus_center)
        direction_other = (other.position - nucleus_center) / r_other
        
        # Check if other particle is between target and nucleus
        # (closer to nucleus and in similar direction)
        if r_other >= r_target:
            continue  # Other particle is further out, doesn't screen
        
        # Angle between directions
        cos_angle = np.dot(direction_target, direction_other)
        
        # If angle is small, particle is in the line of sight
        # Use angular cutoff: if cos(angle) > 0.9, consider it blocking
        if cos_angle < 0.9:
            continue  # Not in line of sight
        
        # Distance from target to other particle
        d_to_other = np.linalg.norm(target_electron.position - other.position)
        
        # Occlusion from this particle
        # Use the particle's radius
        occlusion = occlusion_fraction(other.radius, d_to_other)
        
        # Weight by angular alignment (more aligned = more blocking)
        angular_weight = cos_angle  # 1.0 = perfectly aligned, 0.9 = slightly off
        
        total_occlusion += occlusion * angular_weight
    
    # Screening factor: 1.0 = no screening, 0.0 = fully screened
    # But we need to cap it - can't have more than 4π steradians blocked
    screening_factor = max(0.0, 1.0 - total_occlusion)
    
    return screening_factor

def calculate_screening_for_all_electrons(electrons: List[Particle],
                                          nucleons: List[Particle],
                                          nucleus_center: np.ndarray) -> Dict[int, float]:
    """
    Calculate geometric screening for all electrons.
    
    Returns: Dictionary mapping electron index to screening factor
    """
    all_particles = electrons + nucleons
    screening = {}
    
    for i, electron in enumerate(electrons):
        # Other particles (all except this electron)
        other_particles = [p for j, p in enumerate(all_particles) 
                          if not (j < len(electrons) and j == i)]
        
        screening[i] = calculate_geometric_screening(
            electron, other_particles, nucleus_center
        )
    
    return screening

def calculate_effective_field_strength(Z: int, 
                                       electron_screening: float,
                                       r: float) -> float:
    """
    Calculate effective field strength at distance r with geometric screening.
    
    NOT "effective charge" - this is the actual field strength reduced by
    geometric blocking.
    
    Field from nucleus: E = kZe²/r²
    With screening: E_eff = E × screening_factor
    
    But screening is geometric, not charge-based.
    """
    # Base field (no screening)
    E_base = K_E * E_CHARGE * Z / (r * r)
    
    # Apply geometric screening
    E_eff = E_base * electron_screening
    
    return E_eff

def calculate_orbital_radius_with_screening(Z: int,
                                           n: int,
                                           screening: float) -> float:
    """
    Calculate orbital radius accounting for geometric screening.
    
    For circular orbit: mv²/r = kZe²/r² × screening
    v² = kZe²/(mr) × screening
    Also: v = nh/(2πmr) from angular momentum quantization
    
    Combining: r = n²a₀/(Z × screening)
    """
    # Bohr radius
    a_0 = A_0
    
    # With screening: r = n²a₀/(Z × screening_factor)
    # But this is approximate - need proper calculation
    
    # More accurate: solve for r from force balance
    # F = kZe²/r² × screening = mv²/r
    # v = nh/(2πmr)
    # So: kZe²/r² × screening = m(nh/(2πmr))²/r
    # kZe²/r² × screening = m(n²h²/(4π²m²r²))/r
    # kZe²/r² × screening = n²h²/(4π²mr³)
    # r³ = n²h²/(4π²m × kZe² × screening)
    # r = (n²h²/(4π²m × kZe² × screening))^(1/3)
    
    # But simpler approximation for now:
    r = n * n * a_0 / (Z * screening) if screening > 0 else n * n * a_0 / Z
    
    return r

# ==============================================================================
# TEST CALCULATIONS
# ==============================================================================

def test_hydrogen():
    """Test geometric screening for Hydrogen."""
    nucleus_center = np.array([0.0, 0.0, 0.0])
    
    # H: 1 proton, 1 electron
    proton = Particle(
        position=nucleus_center + np.array([0.0, 0.0, 1.7e-15]),
        radius=R_PROTON,
        type='p'
    )
    
    electron = Particle(
        position=nucleus_center + np.array([0.0, 0.0, A_0]),
        radius=R_ELECTRON,
        type='e'
    )
    
    # No other particles to screen
    screening = calculate_geometric_screening(
        electron, [proton], nucleus_center
    )
    
    print(f"H (Z=1):")
    print(f"  Electron position: r = {np.linalg.norm(electron.position - nucleus_center)*1e10:.3f} Å")
    print(f"  Screening factor: {screening:.6f}")
    print(f"  Expected: ~1.0 (no screening)")
    
    return screening

def test_helium():
    """Test geometric screening for Helium."""
    nucleus_center = np.array([0.0, 0.0, 0.0])
    
    # He: 2 protons, 2 electrons (diametrically opposite)
    pole_axis = np.array([0.0, 0.0, 1.0])
    alpha_radius = 1.7e-15
    
    proton1 = Particle(
        position=nucleus_center + pole_axis * alpha_radius,
        radius=R_PROTON,
        type='p'
    )
    proton2 = Particle(
        position=nucleus_center - pole_axis * alpha_radius,
        radius=R_PROTON,
        type='p'
    )
    
    electron1 = Particle(
        position=nucleus_center + pole_axis * (A_0 / 2),  # Closer due to Z=2
        radius=R_ELECTRON,
        type='e'
    )
    electron2 = Particle(
        position=nucleus_center - pole_axis * (A_0 / 2),  # Opposite
        radius=R_ELECTRON,
        type='e'
    )
    
    # Each electron screened by the other
    screening1 = calculate_geometric_screening(
        electron1, [electron2, proton1, proton2], nucleus_center
    )
    screening2 = calculate_geometric_screening(
        electron2, [electron1, proton1, proton2], nucleus_center
    )
    
    print(f"\nHe (Z=2):")
    print(f"  Electron 1 position: r = {np.linalg.norm(electron1.position - nucleus_center)*1e10:.3f} Å")
    print(f"  Electron 2 position: r = {np.linalg.norm(electron2.position - nucleus_center)*1e10:.3f} Å")
    print(f"  Screening factor 1: {screening1:.6f}")
    print(f"  Screening factor 2: {screening2:.6f}")
    print(f"  Expected: < 1.0 (some screening from other electron)")
    
    return screening1, screening2

def test_lithium():
    """Test geometric screening for Lithium."""
    nucleus_center = np.array([0.0, 0.0, 0.0])
    
    # Li: 3 protons, 3 electrons
    # 2 electrons in 1s (close, paired), 1 electron in 2s (further out)
    pole_axis = np.array([0.0, 0.0, 1.0])
    
    # Protons (simplified - need proper alpha + extra proton structure)
    protons = [
        Particle(nucleus_center + pole_axis * 1.7e-15, R_PROTON, 'p'),
        Particle(nucleus_center - pole_axis * 1.7e-15, R_PROTON, 'p'),
        Particle(nucleus_center + np.array([1.7e-15, 0.0, 0.0]), R_PROTON, 'p'),
    ]
    
    # 1s electrons (close, paired)
    r_1s = A_0 / 3  # Z_eff ≈ 3 for 1s
    electron1s1 = Particle(
        nucleus_center + pole_axis * r_1s,
        R_ELECTRON, 'e'
    )
    electron1s2 = Particle(
        nucleus_center - pole_axis * r_1s,
        R_ELECTRON, 'e'
    )
    
    # 2s electron (further out, screened by 1s²)
    r_2s = 4 * A_0  # n=2, screened
    electron2s = Particle(
        nucleus_center + pole_axis * r_2s,
        R_ELECTRON, 'e'
    )
    
    electrons = [electron1s1, electron1s2, electron2s]
    
    # Calculate screening for 2s electron
    all_particles = electrons + protons
    screening_2s = calculate_geometric_screening(
        electron2s, 
        [p for p in all_particles if not np.allclose(p.position, electron2s.position)],
        nucleus_center
    )
    
    print(f"\nLi (Z=3):")
    print(f"  1s electron 1: r = {r_1s*1e10:.3f} Å")
    print(f"  1s electron 2: r = {r_1s*1e10:.3f} Å")
    print(f"  2s electron: r = {r_2s*1e10:.3f} Å")
    print(f"  2s screening factor: {screening_2s:.6f}")
    print(f"  Expected: < 1.0 (screened by 1s² core)")
    
    return screening_2s

if __name__ == "__main__":
    print("="*60)
    print("GEOMETRIC SCREENING CALCULATIONS")
    print("="*60)
    print("\nCalculating screening from actual geometry:")
    print("- Solid angle occlusion")
    print("- Spatial blocking")
    print("- No 'effective charge' - pure geometry\n")
    
    test_hydrogen()
    test_helium()
    test_lithium()
    
    print("\n" + "="*60)
    print("These are ACTUAL geometric calculations, not abstract concepts.")
    print("="*60)
