#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Trefoil Nuclear Structure Mappings

Calculates for all 118 elements:
- Proton and neutron positions (spatial coordinates)
- Orientations (chirality: L/R, alignment angles)
- Velocities (three-speed system: v₁=2.23c, v₂=1.84c, v₃=0.395c)
- Relative velocities between nucleons
- Rotation mechanisms (individual spin vs. nuclear rotation)

Outputs:
- JSON data for 3D models
- Markdown tables
- TypeScript data for visualizations
"""

import sys
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import numpy as np

# Fix encoding for Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ============================================================================
# CONSTANTS
# ============================================================================

# Trefoil parameters
R_P_FM = 0.84  # fm (proton radius)
R_N_FM = 0.87  # fm (neutron radius)
R_NUCLEON_FM = 0.84  # fm (used for calculations)

# Three-velocity system
V1_C = 2.23  # Fastest (perihelion)
V2_C = 1.84  # Average (rim velocity)
V3_C = 0.395  # Slowest (aphelion)
C = 299792458.0  # m/s

# Rotation
OMEGA_P = 6.57e23  # rad/s (proton rotation frequency)

# Building block separations
DIST_DEUTERON_FM = 2.10  # fm
DIST_ALPHA_FM = 1.45  # fm (compressed)
DIST_INTER_ALPHA_FM = 2.9  # fm

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class NucleonPosition:
    """Position and orientation of a single nucleon"""
    type: str  # "proton" or "neutron"
    x: float  # fm
    y: float  # fm
    z: float  # fm
    chirality: str  # "L" or "R"
    velocity_v1: float  # c (perihelion)
    velocity_v2: float  # c (average)
    velocity_v3: float  # c (aphelion)
    rotation_frequency: float  # rad/s
    phase_angle: float  # rad (for velocity calculation)

@dataclass
class TrefoilStructure:
    """Complete trefoil structure for an element"""
    Z: int
    N: int
    A: int
    element_name: str
    element_symbol: str
    building_blocks: str  # e.g., "3α" for Carbon-12
    nucleons: List[NucleonPosition]
    nuclear_rotation_axis: Tuple[float, float, float]
    nuclear_rotation_frequency: float  # rad/s
    relative_velocities: Dict[str, float]  # Pairwise relative velocities

# ============================================================================
# BUILDING BLOCK GEOMETRY
# ============================================================================

def generate_deuteron_positions(center: Tuple[float, float, float], 
                                orientation: str = "L-R") -> Tuple[NucleonPosition, NucleonPosition]:
    """Generate positions for a deuteron (p+n pair)"""
    x0, y0, z0 = center
    d = DIST_DEUTERON_FM / 2
    
    # Coaxial stack: proton and neutron along z-axis
    if orientation == "L-R":
        proton_chirality = "L"
        neutron_chirality = "R"
    else:
        proton_chirality = "R"
        neutron_chirality = "L"
    
    # Calculate phase angles (for velocity variation)
    proton_phase = 0.0
    neutron_phase = math.pi  # Opposite phase
    
    proton = NucleonPosition(
        type="proton",
        x=x0,
        y=y0,
        z=z0 - d,
        chirality=proton_chirality,
        velocity_v1=V1_C,
        velocity_v2=V2_C,
        velocity_v3=V3_C,
        rotation_frequency=OMEGA_P,
        phase_angle=proton_phase
    )
    
    neutron = NucleonPosition(
        type="neutron",
        x=x0,
        y=y0,
        z=z0 + d,
        chirality=neutron_chirality,
        velocity_v1=V1_C,
        velocity_v2=V2_C * 0.992,  # Slightly slower due to electron drag
        velocity_v3=V3_C,
        rotation_frequency=OMEGA_P * 0.995,  # Slightly slower
        phase_angle=neutron_phase
    )
    
    return proton, neutron

def generate_alpha_positions(center: Tuple[float, float, float]) -> List[NucleonPosition]:
    """Generate positions for an alpha particle (tetrahedral 2p+2n)"""
    x0, y0, z0 = center
    d = DIST_ALPHA_FM / math.sqrt(2)  # Tetrahedral edge length
    
    # Tetrahedral vertices
    # Optimal chirality: L-R-L-R pattern
    positions = [
        (x0 + d, y0 + d, z0 + d, "L"),  # Proton 1
        (x0 - d, y0 - d, z0 + d, "R"),  # Neutron 1
        (x0 + d, y0 - d, z0 - d, "L"),  # Proton 2
        (x0 - d, y0 + d, z0 - d, "R"),  # Neutron 2
    ]
    
    nucleons = []
    for i, (x, y, z, chirality) in enumerate(positions):
        is_proton = (i % 2 == 0)
        phase = i * math.pi / 2  # 90° phase difference
        
        nucleon = NucleonPosition(
            type="proton" if is_proton else "neutron",
            x=x,
            y=y,
            z=z,
            chirality=chirality,
            velocity_v1=V1_C,
            velocity_v2=V2_C if is_proton else V2_C * 0.992,
            velocity_v3=V3_C,
            rotation_frequency=OMEGA_P if is_proton else OMEGA_P * 0.995,
            phase_angle=phase
        )
        nucleons.append(nucleon)
    
    return nucleons

def generate_tri_alpha_positions(center: Tuple[float, float, float]) -> List[NucleonPosition]:
    """Generate positions for tri-alpha (2p+3n)"""
    # Tri-alpha: (np)n(np) = D + n + D
    # Linear arrangement with neutron in center
    x0, y0, z0 = center
    d = DIST_DEUTERON_FM
    
    nucleons = []
    
    # First deuteron (L-R)
    p1, n1 = generate_deuteron_positions((x0 - d, y0, z0), "L-R")
    nucleons.extend([p1, n1])
    
    # Central neutron
    n_center = NucleonPosition(
        type="neutron",
        x=x0,
        y=y0,
        z=z0,
        chirality="L",  # Matches first deuteron
        velocity_v1=V1_C,
        velocity_v2=V2_C * 0.992,
        velocity_v3=V3_C,
        rotation_frequency=OMEGA_P * 0.995,
        phase_angle=math.pi
    )
    nucleons.append(n_center)
    
    # Second deuteron (R-L)
    p2, n2 = generate_deuteron_positions((x0 + d, y0, z0), "R-L")
    nucleons.extend([p2, n2])
    
    return nucleons

def generate_triple_positions(center: Tuple[float, float, float]) -> List[NucleonPosition]:
    """Generate positions for triple (3p+5n) = (np)n(np)n(np)"""
    # Extended chain structure
    x0, y0, z0 = center
    d = DIST_DEUTERON_FM
    
    nucleons = []
    
    # Three deuterons in chain with neutrons between
    for i in range(3):
        offset = (i - 1) * d * 1.5
        chirality = "L-R" if i % 2 == 0 else "R-L"
        p, n = generate_deuteron_positions((x0 + offset, y0, z0), chirality)
        nucleons.extend([p, n])
        
        # Add neutron between deuterons (except at ends)
        if i < 2:
            n_bridge = NucleonPosition(
                type="neutron",
                x=x0 + offset + d * 0.75,
                y=y0,
                z=z0,
                chirality="L" if i % 2 == 0 else "R",
                velocity_v1=V1_C,
                velocity_v2=V2_C * 0.992,
                velocity_v3=V3_C,
                rotation_frequency=OMEGA_P * 0.995,
                phase_angle=math.pi * (i + 0.5)
            )
            nucleons.append(n_bridge)
    
    return nucleons

# ============================================================================
# NUCLEAR STRUCTURE CALCULATION
# ============================================================================

def calculate_relative_velocity(n1: NucleonPosition, n2: NucleonPosition) -> float:
    """Calculate relative velocity between two nucleons"""
    # Use average velocity (v2) for relative velocity calculation
    v1 = n1.velocity_v2 * C
    v2 = n2.velocity_v2 * C
    
    # Calculate distance
    dx = n1.x - n2.x
    dy = n1.y - n2.y
    dz = n1.z - n2.z
    distance = math.sqrt(dx*dx + dy*dy + dz*dz) * 1e-15  # Convert fm to m
    
    # Relative velocity magnitude (simplified)
    dv = abs(v1 - v2)
    
    return dv / C  # Return in units of c

def calculate_nuclear_rotation_axis(nucleons: List[NucleonPosition]) -> Tuple[float, float, float]:
    """Calculate nuclear rotation axis (through center of mass)"""
    # Center of mass
    total_mass = len(nucleons)
    cx = sum(n.x for n in nucleons) / total_mass
    cy = sum(n.y for n in nucleons) / total_mass
    cz = sum(n.z for n in nucleons) / total_mass
    
    # Rotation axis through center (simplified: z-axis)
    return (0.0, 0.0, 1.0)

def calculate_nuclear_rotation_frequency(nucleons: List[NucleonPosition]) -> float:
    """Calculate whole-nucleus rotation frequency"""
    # Average of individual spin frequencies, but much slower
    avg_individual = sum(n.rotation_frequency for n in nucleons) / len(nucleons)
    
    # Nuclear rotation is much slower (factor of ~10^10)
    return avg_individual / 1e10

def decompose_nucleus(Z: int, N: int) -> Dict[str, int]:
    """Decompose nucleus into building blocks"""
    A = Z + N
    
    # Simple decomposition (can be enhanced with actual building block logic)
    if A == 1:
        return {"proton": 1}
    elif A == 2:
        return {"deuteron": 1}
    elif A == 4:
        return {"alpha": 1}
    elif A <= 8:
        # Small nuclei: mostly alphas
        n_alpha = A // 4
        remainder = A % 4
        result = {"alpha": n_alpha}
        if remainder == 2:
            result["deuteron"] = 1
        elif remainder == 1:
            result["proton"] = 1
        return result
    else:
        # Heavier nuclei: alpha clusters
        n_alpha = A // 4
        remainder = A % 4
        result = {"alpha": n_alpha}
        if remainder >= 2:
            result["deuteron"] = remainder // 2
        if remainder % 2 == 1:
            result["proton"] = 1
        return result

def generate_trefoil_structure(Z: int, N: int, element_name: str, 
                               element_symbol: str) -> TrefoilStructure:
    """Generate complete trefoil structure for an element"""
    A = Z + N
    
    # Decompose into building blocks
    blocks = decompose_nucleus(Z, N)
    
    # Generate nucleon positions
    nucleons = []
    center = (0.0, 0.0, 0.0)
    
    if A == 1:
        # Single proton
        nucleon = NucleonPosition(
            type="proton",
            x=0.0, y=0.0, z=0.0,
            chirality="R",  # Arbitrary for single nucleon
            velocity_v1=V1_C,
            velocity_v2=V2_C,
            velocity_v3=V3_C,
            rotation_frequency=OMEGA_P,
            phase_angle=0.0
        )
        nucleons.append(nucleon)
        building_blocks_str = "1p"
    elif "deuteron" in blocks and blocks["deuteron"] == 1 and A == 2:
        # Deuteron
        p, n = generate_deuteron_positions(center)
        nucleons = [p, n]
        building_blocks_str = "1D"
    elif "alpha" in blocks:
        # Alpha particle or alpha clusters
        n_alpha = blocks.get("alpha", 0)
        if n_alpha == 1:
            nucleons = generate_alpha_positions(center)
            building_blocks_str = "1alpha"
        else:
            # Multiple alphas: arrange in cluster
            # Simplified: linear arrangement
            nucleons = []
            spacing = DIST_INTER_ALPHA_FM
            for i in range(n_alpha):
                offset = (i - (n_alpha - 1) / 2) * spacing
                alpha_nucleons = generate_alpha_positions((offset, 0.0, 0.0))
                nucleons.extend(alpha_nucleons)
            building_blocks_str = f"{n_alpha}alpha"
            
            # Add extra nucleons if needed
            if "deuteron" in blocks:
                for i in range(blocks["deuteron"]):
                    offset = (n_alpha / 2 + i + 1) * spacing
                    p, n = generate_deuteron_positions((offset, 0.0, 0.0))
                    nucleons.extend([p, n])
                    building_blocks_str += "+1D"
    else:
        # Fallback: simple arrangement
        nucleons = []
        for i in range(Z):
            nucleon = NucleonPosition(
                type="proton",
                x=i * 1.0, y=0.0, z=0.0,
                chirality="L" if i % 2 == 0 else "R",
                velocity_v1=V1_C,
                velocity_v2=V2_C,
                velocity_v3=V3_C,
                rotation_frequency=OMEGA_P,
                phase_angle=i * math.pi / 4
            )
            nucleons.append(nucleon)
        for i in range(N):
            nucleon = NucleonPosition(
                type="neutron",
                x=(Z + i) * 1.0, y=0.0, z=0.0,
                chirality="R" if i % 2 == 0 else "L",
                velocity_v1=V1_C,
                velocity_v2=V2_C * 0.992,
                velocity_v3=V3_C,
                rotation_frequency=OMEGA_P * 0.995,
                phase_angle=(Z + i) * math.pi / 4
            )
            nucleons.append(nucleon)
        building_blocks_str = f"{Z}p+{N}n"
    
    # Calculate relative velocities
    relative_velocities = {}
    for i, n1 in enumerate(nucleons):
        for j, n2 in enumerate(nucleons[i+1:], start=i+1):
            key = f"{i}-{j}"
            relative_velocities[key] = calculate_relative_velocity(n1, n2)
    
    # Calculate nuclear rotation
    rotation_axis = calculate_nuclear_rotation_axis(nucleons)
    rotation_frequency = calculate_nuclear_rotation_frequency(nucleons)
    
    return TrefoilStructure(
        Z=Z,
        N=N,
        A=A,
        element_name=element_name,
        element_symbol=element_symbol,
        building_blocks=building_blocks_str,
        nucleons=nucleons,
        nuclear_rotation_axis=rotation_axis,
        nuclear_rotation_frequency=rotation_frequency,
        relative_velocities=relative_velocities
    )

# ============================================================================
# ELEMENT DATA
# ============================================================================

# Complete list of all 118 elements (most common isotopes)
ELEMENT_NAMES = [
    "Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon",
    "Nitrogen", "Oxygen", "Fluorine", "Neon", "Sodium", "Magnesium",
    "Aluminum", "Silicon", "Phosphorus", "Sulfur", "Chlorine", "Argon",
    "Potassium", "Calcium", "Scandium", "Titanium", "Vanadium", "Chromium",
    "Manganese", "Iron", "Cobalt", "Nickel", "Copper", "Zinc", "Gallium",
    "Germanium", "Arsenic", "Selenium", "Bromine", "Krypton", "Rubidium",
    "Strontium", "Yttrium", "Zirconium", "Niobium", "Molybdenum", "Technetium",
    "Ruthenium", "Rhodium", "Palladium", "Silver", "Cadmium", "Indium",
    "Tin", "Antimony", "Tellurium", "Iodine", "Xenon", "Cesium", "Barium",
    "Lanthanum", "Cerium", "Praseodymium", "Neodymium", "Promethium", "Samarium",
    "Europium", "Gadolinium", "Terbium", "Dysprosium", "Holmium", "Erbium",
    "Thulium", "Ytterbium", "Lutetium", "Hafnium", "Tantalum", "Tungsten",
    "Rhenium", "Osmium", "Iridium", "Platinum", "Gold", "Mercury", "Thallium",
    "Lead", "Bismuth", "Polonium", "Astatine", "Radon", "Francium", "Radium",
    "Actinium", "Thorium", "Protactinium", "Uranium", "Neptunium", "Plutonium",
    "Americium", "Curium", "Berkelium", "Californium", "Einsteinium", "Fermium",
    "Mendelevium", "Nobelium", "Lawrencium", "Rutherfordium", "Dubnium", "Seaborgium",
    "Bohrium", "Hassium", "Meitnerium", "Darmstadtium", "Roentgenium", "Copernicium",
    "Nihonium", "Flerovium", "Moscovium", "Livermorium", "Tennessine", "Oganesson"
]

ELEMENT_SYMBOLS = [
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
    "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
    "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
    "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
]

# Most common isotope neutron numbers (simplified - can be enhanced)
def get_most_common_N(Z: int) -> int:
    """Get most common neutron number for element Z"""
    # Simplified: use stable isotope ratios
    if Z == 1:
        return 0  # H-1
    elif Z == 2:
        return 2  # He-4
    elif Z <= 20:
        # Light elements: roughly N ≈ Z
        return Z
    elif Z <= 50:
        # Medium elements: N ≈ 1.2*Z
        return int(Z * 1.2)
    elif Z <= 82:
        # Heavy elements: N ≈ 1.5*Z
        return int(Z * 1.5)
    else:
        # Superheavy: N ≈ 1.6*Z
        return int(Z * 1.6)

# Generate complete element list
ELEMENTS = []
for Z in range(1, 119):
    N = get_most_common_N(Z)
    name = ELEMENT_NAMES[Z-1]
    symbol = ELEMENT_SYMBOLS[Z-1]
    ELEMENTS.append((Z, N, name, symbol))

# ============================================================================
# OUTPUT FUNCTIONS
# ============================================================================

def generate_json_output(structures: List[TrefoilStructure], output_path: Path):
    """Generate JSON output for 3D models"""
    data = []
    for structure in structures:
        structure_dict = {
            "Z": structure.Z,
            "N": structure.N,
            "A": structure.A,
            "element_name": structure.element_name,
            "element_symbol": structure.element_symbol,
            "building_blocks": structure.building_blocks,
            "nucleons": [asdict(n) for n in structure.nucleons],
            "nuclear_rotation_axis": structure.nuclear_rotation_axis,
            "nuclear_rotation_frequency": structure.nuclear_rotation_frequency,
            "relative_velocities": structure.relative_velocities
        }
        data.append(structure_dict)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def generate_typescript_output(structures: List[TrefoilStructure], output_path: Path):
    """Generate TypeScript data for visualizations"""
    lines = [
        "// Trefoil Nuclear Structure Data",
        "// Generated by generate_trefoil_mappings.py",
        "",
        "export interface NucleonPosition {",
        "  type: 'proton' | 'neutron';",
        "  x: number;  // fm",
        "  y: number;  // fm",
        "  z: number;  // fm",
        "  chirality: 'L' | 'R';",
        "  velocity_v1: number;  // c",
        "  velocity_v2: number;  // c",
        "  velocity_v3: number;  // c",
        "  rotation_frequency: number;  // rad/s",
        "  phase_angle: number;  // rad",
        "}",
        "",
        "export interface TrefoilStructure {",
        "  Z: number;",
        "  N: number;",
        "  A: number;",
        "  element_name: string;",
        "  element_symbol: string;",
        "  building_blocks: string;",
        "  nucleons: NucleonPosition[];",
        "  nuclear_rotation_axis: [number, number, number];",
        "  nuclear_rotation_frequency: number;  // rad/s",
        "  relative_velocities: Record<string, number>;",
        "}",
        "",
        "export const trefoilStructures: TrefoilStructure[] = ["
    ]
    
    for structure in structures:
        lines.append("  {")
        lines.append(f"    Z: {structure.Z},")
        lines.append(f"    N: {structure.N},")
        lines.append(f"    A: {structure.A},")
        lines.append(f'    element_name: "{structure.element_name}",')
        lines.append(f'    element_symbol: "{structure.element_symbol}",')
        lines.append(f'    building_blocks: "{structure.building_blocks}",')
        lines.append("    nucleons: [")
        for n in structure.nucleons:
            lines.append("      {")
            lines.append(f'        type: "{n.type}",')
            lines.append(f"        x: {n.x:.6f},")
            lines.append(f"        y: {n.y:.6f},")
            lines.append(f"        z: {n.z:.6f},")
            lines.append(f'        chirality: "{n.chirality}",')
            lines.append(f"        velocity_v1: {n.velocity_v1:.6f},")
            lines.append(f"        velocity_v2: {n.velocity_v2:.6f},")
            lines.append(f"        velocity_v3: {n.velocity_v3:.6f},")
            lines.append(f"        rotation_frequency: {n.rotation_frequency:.6e},")
            lines.append(f"        phase_angle: {n.phase_angle:.6f},")
            lines.append("      },")
        lines.append("    ],")
        lines.append(f"    nuclear_rotation_axis: [{structure.nuclear_rotation_axis[0]:.6f}, {structure.nuclear_rotation_axis[1]:.6f}, {structure.nuclear_rotation_axis[2]:.6f}],")
        lines.append(f"    nuclear_rotation_frequency: {structure.nuclear_rotation_frequency:.6e},")
        lines.append("    relative_velocities: {")
        for key, value in structure.relative_velocities.items():
            lines.append(f'      "{key}": {value:.6f},')
        lines.append("    },")
        lines.append("  },")
    
    lines.append("];")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def main():
    """Generate all trefoil mappings"""
    print("Generating trefoil nuclear structure mappings...")
    
    # Generate structures for all elements
    structures = []
    for Z, N, name, symbol in ELEMENTS:
        try:
            structure = generate_trefoil_structure(Z, N, name, symbol)
            structures.append(structure)
            print(f"Generated: {name} (Z={Z}, N={N}) - {structure.building_blocks}")
        except Exception as e:
            print(f"Error generating {name}: {e}")
    
    # Create output directories
    data_dir = Path("SDT/data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    website_data_dir = Path("SDT/website/src/data")
    website_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate outputs
    print("\nGenerating JSON output...")
    generate_json_output(structures, data_dir / "trefoil_mappings.json")
    
    print("Generating TypeScript output...")
    generate_typescript_output(structures, website_data_dir / "trefoilStructures.ts")
    
    print(f"\nGenerated {len(structures)} element structures")
    print(f"JSON: {data_dir / 'trefoil_mappings.json'}")
    print(f"TypeScript: {website_data_dir / 'trefoilStructures.ts'}")

if __name__ == "__main__":
    main()
