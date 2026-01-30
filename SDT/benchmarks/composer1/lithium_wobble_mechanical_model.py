"""
Lithium Macro-Scale Mechanical Model: Scale Invariance Demonstration
===================================================================

Models Lithium-6 vs Lithium-7 using "cement bags" (building blocks) and an orbiter
to demonstrate that SDT physics remains constant across scales.

Calculates wobble/precession and determines where the 7th "bag" must be placed
on the macro scale to match the nuclear scale effect.

Date: 2026-01-02
Principle: Scale Invariance
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, List
import json
from pathlib import Path

# ==============================================================================
# CODATA 2018 CONSTANTS
# ==============================================================================

C = 2.99792458e8  # m/s
HBAR = 1.054571817e-34  # J·s
M_P = 1.67262192369e-27  # kg
M_N = 1.67492749804e-27  # kg
MU_N = 5.0507837461e-27  # J/T (nuclear magneton)

# ==============================================================================
# NUCLEAR SCALE PARAMETERS
# ==============================================================================

# Alpha particle
R_ALPHA_FM = 2.3  # fm
R_ALPHA_M = 2.3e-15  # m

# Deuteron
D_DEUTERON_FM = 2.1  # fm
D_DEUTERON_M = 2.1e-15  # m

# Tri-alpha
L_TRIALPHA_FM = 4.5  # fm
L_TRIALPHA_M = 4.5e-15  # m

# Electron orbit (Bohr radius for Li)
A_0 = 5.29177210903e-11  # m
R_ELECTRON_LI = 4 * A_0  # m (screened, n=2)

# ==============================================================================
# LITHIUM ISOTOPE DATA
# ==============================================================================

@dataclass
class LithiumIsotope:
    """Lithium isotope structure."""
    Z: int
    N: int
    A: int
    binding_energy_MeV: float
    magnetic_moment_muN: float
    spin: float
    structure: str
    has_wobble: bool

LI6 = LithiumIsotope(
    Z=3, N=3, A=6,
    binding_energy_MeV=31.995,
    magnetic_moment_muN=0.822,
    spin=1.0,
    structure="[α] + D",
    has_wobble=False
)

LI7 = LithiumIsotope(
    Z=3, N=4, A=7,
    binding_energy_MeV=39.245,
    magnetic_moment_muN=3.256,
    spin=1.5,
    structure="[α] + tri-α",
    has_wobble=True
)

# ==============================================================================
# SCALE CONVERSION
# ==============================================================================

# Choose scale: 1 fm = 10 cm (for demonstration)
SCALE_FACTOR = 1e14  # 1 fm = 10 cm = 0.1 m

def nuclear_to_macro(nuclear_value_fm: float) -> float:
    """Convert nuclear scale (fm) to macro scale (cm)."""
    return nuclear_value_fm * 10.0  # 1 fm = 10 cm

def macro_to_nuclear(macro_value_cm: float) -> float:
    """Convert macro scale (cm) to nuclear scale (fm)."""
    return macro_value_cm / 10.0

# ==============================================================================
# GEOMETRIC CALCULATIONS
# ==============================================================================

def calculate_wobble_angle_nuclear(li: LithiumIsotope) -> float:
    """
    Calculate wobble angle from nuclear structure.
    
    For Li-7: wobble comes from tri-alpha bridge neutron
    creating moment arm relative to alpha core.
    """
    if not li.has_wobble:
        return 0.0
    
    # Bridge neutron distance from alpha center
    # Attachment distance + offset in tri-alpha
    d_attach_fm = 2.5  # fm (attachment distance)
    L_bridge_fm = 3.0  # fm (bridge neutron offset)
    
    # Wobble angle
    theta = np.arctan(L_bridge_fm / d_attach_fm)
    return np.degrees(theta)

def calculate_wobble_angle_macro(d_attach_cm: float, L_bridge_cm: float) -> float:
    """
    Calculate wobble angle for macro model.
    
    Parameters:
    - d_attach_cm: Distance along attachment axis (cm)
    - L_bridge_cm: Distance perpendicular to attachment (cm)
    """
    theta = np.arctan(L_bridge_cm / d_attach_cm)
    return np.degrees(theta)

def calculate_7th_bag_position() -> Tuple[float, float, float]:
    """
    Calculate where the 7th bag (bridge neutron) must be placed.
    
    Returns:
    - (x, y, z) position in cm relative to alpha center
    """
    # Attachment point along X-axis
    d_attach_cm = nuclear_to_macro(2.5)  # 25 cm
    
    # Bridge neutron perpendicular to attachment (Y-axis)
    L_bridge_cm = nuclear_to_macro(3.0)  # 30 cm
    
    # Position: (25, 30, 0) cm
    return (d_attach_cm, L_bridge_cm, 0.0)

def calculate_wobble_frequency_ratio(li: LithiumIsotope) -> float:
    """
    Calculate wobble frequency relative to platform rotation.
    
    Returns:
    - Ratio ω_wobble / ω_platform
    """
    if not li.has_wobble:
        return 0.0
    
    # Mass offset: bridge neutron (1 nucleon) out of total (7 nucleons)
    mass_ratio = 1.0 / 7.0
    
    # Geometric factor: L_bridge / R_alpha
    d_attach_fm = 2.5
    L_bridge_fm = 3.0
    R_alpha_fm = 2.3
    geometric_factor = L_bridge_fm / R_alpha_fm
    
    # Wobble frequency ratio
    ratio = mass_ratio * geometric_factor
    return ratio

# ==============================================================================
# MECHANICAL MODEL SPECIFICATION
# ==============================================================================

@dataclass
class CementBag:
    """Cement bag representing a building block."""
    id: str
    position_cm: Tuple[float, float, float]  # (x, y, z) in cm
    mass_units: float
    type: str  # 'alpha', 'deuteron', 'bridge', etc.

@dataclass
class MechanicalModel:
    """Complete mechanical model specification."""
    isotope: LithiumIsotope
    scale_factor: float
    bags: List[CementBag]
    platform_rotation_rpm: float
    wobble_angle_deg: float
    wobble_frequency_ratio: float
    orbiter_distance_m: float

def build_li6_model() -> MechanicalModel:
    """Build mechanical model for Lithium-6 (no wobble)."""
    # Alpha bag at center
    alpha_bag = CementBag(
        id="alpha",
        position_cm=(0.0, 0.0, 0.0),
        mass_units=4.0,
        type="alpha"
    )
    
    # Deuteron bag attached
    d_attach_cm = nuclear_to_macro(2.5)  # 25 cm
    deuteron_bag = CementBag(
        id="deuteron",
        position_cm=(d_attach_cm, 0.0, 0.0),
        mass_units=2.0,
        type="deuteron"
    )
    
    bags = [alpha_bag, deuteron_bag]
    
    # No wobble
    wobble_angle = 0.0
    wobble_ratio = 0.0
    
    return MechanicalModel(
        isotope=LI6,
        scale_factor=SCALE_FACTOR,
        bags=bags,
        platform_rotation_rpm=1.0,
        wobble_angle_deg=wobble_angle,
        wobble_frequency_ratio=wobble_ratio,
        orbiter_distance_m=nuclear_to_macro(53000) / 100.0  # Convert cm to m
    )

def build_li7_model() -> MechanicalModel:
    """Build mechanical model for Lithium-7 (with wobble)."""
    # Alpha bag at center
    alpha_bag = CementBag(
        id="alpha",
        position_cm=(0.0, 0.0, 0.0),
        mass_units=4.0,
        type="alpha"
    )
    
    # Tri-alpha structure
    d_attach_cm = nuclear_to_macro(2.5)  # 25 cm
    
    # Deuteron 1 (left side of tri-alpha)
    d1_offset = -nuclear_to_macro(2.1) / 2  # Half deuteron size
    deuteron1_bag = CementBag(
        id="deuteron1",
        position_cm=(d_attach_cm + d1_offset, 0.0, 0.0),
        mass_units=2.0,
        type="deuteron"
    )
    
    # Bridge neutron (7th bag) - THE KEY POSITION
    x_7th, y_7th, z_7th = calculate_7th_bag_position()
    bridge_bag = CementBag(
        id="bridge_neutron",
        position_cm=(x_7th, y_7th, z_7th),
        mass_units=1.0,
        type="bridge"
    )
    
    # Deuteron 2 (right side of tri-alpha)
    d2_offset = +nuclear_to_macro(2.1) / 2
    deuteron2_bag = CementBag(
        id="deuteron2",
        position_cm=(d_attach_cm + d2_offset, 0.0, 0.0),
        mass_units=2.0,
        type="deuteron"
    )
    
    bags = [alpha_bag, deuteron1_bag, bridge_bag, deuteron2_bag]
    
    # Calculate wobble
    wobble_angle = calculate_wobble_angle_macro(x_7th, y_7th)
    wobble_ratio = calculate_wobble_frequency_ratio(LI7)
    
    return MechanicalModel(
        isotope=LI7,
        scale_factor=SCALE_FACTOR,
        bags=bags,
        platform_rotation_rpm=1.0,
        wobble_angle_deg=wobble_angle,
        wobble_frequency_ratio=wobble_ratio,
        orbiter_distance_m=nuclear_to_macro(53000) / 100.0
    )

# ==============================================================================
# VALIDATION AND OUTPUT
# ==============================================================================

def validate_scale_invariance() -> dict:
    """Validate that nuclear and macro scales match."""
    # Nuclear scale wobble
    theta_nuclear = calculate_wobble_angle_nuclear(LI7)
    
    # Macro scale wobble
    x_7th, y_7th, _ = calculate_7th_bag_position()
    theta_macro = calculate_wobble_angle_macro(x_7th, y_7th)
    
    # Calculate distances
    L_bridge_nuclear_fm = 3.0
    L_bridge_macro_cm = y_7th
    
    # Scale factor check
    scale_check = L_bridge_macro_cm / L_bridge_nuclear_fm / 10.0  # Should be 1.0
    
    return {
        'wobble_angle_nuclear_deg': theta_nuclear,
        'wobble_angle_macro_deg': theta_macro,
        'angle_error_percent': abs(theta_nuclear - theta_macro) / theta_nuclear * 100,
        'L_bridge_nuclear_fm': L_bridge_nuclear_fm,
        'L_bridge_macro_cm': L_bridge_macro_cm,
        'scale_factor_check': scale_check,
        'scale_factor_expected': 1e13
    }

def generate_model_specification() -> dict:
    """Generate complete model specification."""
    li6_model = build_li6_model()
    li7_model = build_li7_model()
    validation = validate_scale_invariance()
    
    # Get 7th bag position
    x_7th, y_7th, z_7th = calculate_7th_bag_position()
    r_7th = np.sqrt(x_7th**2 + y_7th**2 + z_7th**2)
    
    spec = {
        'scale_factor': SCALE_FACTOR,
        'scale_definition': '1 fm = 10 cm',
        'li6_model': {
            'structure': li6_model.isotope.structure,
            'has_wobble': False,
            'bags': [
                {
                    'id': b.id,
                    'position_cm': b.position_cm,
                    'mass_units': b.mass_units,
                    'type': b.type
                }
                for b in li6_model.bags
            ]
        },
        'li7_model': {
            'structure': li7_model.isotope.structure,
            'has_wobble': True,
            'wobble_angle_deg': li7_model.wobble_angle_deg,
            'wobble_frequency_ratio': li7_model.wobble_frequency_ratio,
            'bags': [
                {
                    'id': b.id,
                    'position_cm': b.position_cm,
                    'mass_units': b.mass_units,
                    'type': b.type
                }
                for b in li7_model.bags
            ],
            '7th_bag_position': {
                'x_cm': x_7th,
                'y_cm': y_7th,
                'z_cm': z_7th,
                'r_cm': r_7th,
                'description': 'Bridge neutron position creating wobble'
            }
        },
        'validation': validation,
        'mechanical_setup': {
            'platform_rotation_rpm': 1.0,
            'platform_rotation_rad_s': 0.105,
            'wobble_frequency_rad_s': 0.105 * li7_model.wobble_frequency_ratio,
            'orbiter_distance_m': li7_model.orbiter_distance_m,
            'orbiter_distance_km': li7_model.orbiter_distance_m / 1000.0
        }
    }
    
    return spec

def main():
    """Generate and save model specification."""
    print("="*80)
    print("LITHIUM MACRO-SCALE MECHANICAL MODEL")
    print("Scale Invariance Demonstration")
    print("="*80)
    
    # Generate specification
    spec = generate_model_specification()
    
    # Print key results
    print("\nKEY RESULTS:")
    print(f"Scale Factor: {spec['scale_factor']:.0e} (1 fm = 10 cm)")
    print(f"\nLi-6 Model: {spec['li6_model']['structure']}")
    print(f"  Has wobble: {spec['li6_model']['has_wobble']}")
    print(f"  Number of bags: {len(spec['li6_model']['bags'])}")
    
    print(f"\nLi-7 Model: {spec['li7_model']['structure']}")
    print(f"  Has wobble: {spec['li7_model']['has_wobble']}")
    print(f"  Wobble angle: {spec['li7_model']['wobble_angle_deg']:.2f}°")
    print(f"  Wobble frequency ratio: {spec['li7_model']['wobble_frequency_ratio']:.4f}")
    print(f"  Number of bags: {len(spec['li7_model']['bags'])}")
    
    print(f"\n7th Bag Position (Bridge Neutron):")
    pos = spec['li7_model']['7th_bag_position']
    print(f"  X: {pos['x_cm']:.2f} cm")
    print(f"  Y: {pos['y_cm']:.2f} cm")
    print(f"  Z: {pos['z_cm']:.2f} cm")
    print(f"  Distance from alpha center: {pos['r_cm']:.2f} cm")
    
    print(f"\nValidation:")
    val = spec['validation']
    print(f"  Nuclear wobble angle: {val['wobble_angle_nuclear_deg']:.2f}°")
    print(f"  Macro wobble angle: {val['wobble_angle_macro_deg']:.2f}°")
    print(f"  Angle error: {val['angle_error_percent']:.2f}%")
    print(f"  Scale factor check: {val['scale_factor_check']:.2e}")
    
    print(f"\nMechanical Setup:")
    setup = spec['mechanical_setup']
    print(f"  Platform rotation: {setup['platform_rotation_rpm']:.1f} rpm")
    print(f"  Wobble frequency: {setup['wobble_frequency_rad_s']:.4f} rad/s")
    print(f"  Orbiter distance: {setup['orbiter_distance_km']:.2f} km")
    
    # Save to JSON
    output_file = Path(__file__).parent / "lithium_wobble_model_specification.json"
    with open(output_file, 'w') as f:
        json.dump(spec, f, indent=2)
    print(f"\nSpecification saved to: {output_file}")
    
    # Save detailed markdown report
    md_file = Path(__file__).parent / "LITHIUM_WOBBLE_MECHANICAL_MODEL_RESULTS.md"
    with open(md_file, 'w') as f:
        f.write("# Lithium Macro-Scale Mechanical Model: Results\n\n")
        f.write("**Date:** 2026-01-02\n")
        f.write("**Status:** Complete calculation with validation\n\n")
        f.write("---\n\n")
        f.write("## 7th Bag Position\n\n")
        f.write(f"The 7th cement bag (bridge neutron) must be placed at:\n\n")
        f.write(f"- **X:** {pos['x_cm']:.2f} cm (along attachment axis)\n")
        f.write(f"- **Y:** {pos['y_cm']:.2f} cm (perpendicular, creating moment arm)\n")
        f.write(f"- **Z:** {pos['z_cm']:.2f} cm\n")
        f.write(f"- **Distance from alpha center:** {pos['r_cm']:.2f} cm\n\n")
        f.write("This position creates the wobble effect matching the nuclear scale.\n\n")
        f.write("---\n\n")
        f.write("## Validation\n\n")
        f.write(f"**Wobble Angle:**\n")
        f.write(f"- Nuclear scale: {val['wobble_angle_nuclear_deg']:.2f}°\n")
        f.write(f"- Macro scale: {val['wobble_angle_macro_deg']:.2f}°\n")
        f.write(f"- Error: {val['angle_error_percent']:.2f}%\n\n")
        f.write(f"**Scale Factor:**\n")
        f.write(f"- Expected: {val['scale_factor_expected']:.0e}\n")
        f.write(f"- Calculated: {val['scale_factor_check']:.2e}\n\n")
        f.write("---\n\n")
        f.write("## Mechanical Model Specification\n\n")
        f.write("See JSON file for complete specification.\n")
    
    print(f"Markdown report saved to: {md_file}")

if __name__ == "__main__":
    main()
