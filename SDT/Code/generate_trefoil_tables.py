#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Comprehensive Trefoil Element Mapping Tables

Creates detailed Markdown tables with:
- Proton and neutron positions
- Orientations (chirality)
- Velocities (three-speed system)
- Relative velocities
- Rotation mechanisms
"""

import json
import math
from pathlib import Path
from typing import List, Dict

# Load generated data
DATA_FILE = Path("SDT/data/trefoil_mappings.json")
OUTPUT_FILE = Path("SDT/investigations/nuclear_structure_probe/TREFoil_ELEMENT_MAPPING_TABLES.md")

# Constants
V1_C = 2.23
V2_C = 1.84
V3_C = 0.395
C = 299792458.0
OMEGA_P = 6.57e23

def format_position(x: float, y: float, z: float) -> str:
    """Format position coordinates"""
    return f"({x:.3f}, {y:.3f}, {z:.3f})"

def format_velocity(v: float) -> str:
    """Format velocity in units of c"""
    return f"{v:.3f}c"

def format_frequency(omega: float) -> str:
    """Format rotation frequency"""
    if omega >= 1e20:
        return f"{omega/1e23:.2f}×10²³ rad/s"
    elif omega >= 1e10:
        return f"{omega/1e10:.2f}×10¹⁰ rad/s"
    else:
        return f"{omega:.2e} rad/s"

def generate_element_table(structures: List[Dict]) -> str:
    """Generate comprehensive element mapping table"""
    
    lines = [
        "# Trefoil Element Mapping Tables",
        "",
        "## Complete Element-by-Element Trefoil Structure Mapping",
        "",
        "**Date**: 2026-01-02",
        "**Status**: Complete for all 118 elements",
        "",
        "---",
        "",
        "## Summary Table",
        "",
        "| Element | Z | N | A | Structure | Nucleons | Chirality Pattern | v₁ (c) | v₂ (c) | v₃ (c) | Rotation (rad/s) |",
        "|---------|---|---|---|-----------|----------|-------------------|--------|--------|--------|------------------|"
    ]
    
    for struct in structures:
        Z = struct["Z"]
        N = struct["N"]
        A = struct["A"]
        name = struct["element_name"]
        symbol = struct["element_symbol"]
        blocks = struct["building_blocks"]
        nucleons = struct["nucleons"]
        
        # Count nucleons
        n_protons = sum(1 for n in nucleons if n["type"] == "proton")
        n_neutrons = sum(1 for n in nucleons if n["type"] == "neutron")
        
        # Chirality pattern
        chirality_pattern = "".join([n["chirality"] for n in nucleons[:min(8, len(nucleons))]])
        if len(nucleons) > 8:
            chirality_pattern += "..."
        
        # Velocities (use first nucleon as representative)
        if nucleons:
            v1 = nucleons[0]["velocity_v1"]
            v2 = nucleons[0]["velocity_v2"]
            v3 = nucleons[0]["velocity_v3"]
        else:
            v1 = v2 = v3 = 0.0
        
        # Rotation frequency
        rot_freq = struct["nuclear_rotation_frequency"]
        
        lines.append(
            f"| {symbol} ({name}) | {Z} | {N} | {A} | {blocks} | "
            f"{n_protons}p+{n_neutrons}n | {chirality_pattern} | "
            f"{v1:.2f} | {v2:.2f} | {v3:.2f} | {format_frequency(rot_freq)} |"
        )
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Detailed tables for first 20 elements
    lines.append("## Detailed Element Tables (First 20 Elements)")
    lines.append("")
    
    for struct in structures[:20]:
        Z = struct["Z"]
        N = struct["N"]
        A = struct["A"]
        name = struct["element_name"]
        symbol = struct["element_symbol"]
        blocks = struct["building_blocks"]
        nucleons = struct["nucleons"]
        
        lines.append(f"### {symbol} - {name} (Z={Z}, N={N}, A={A})")
        lines.append("")
        lines.append(f"**Building Blocks**: {blocks}")
        lines.append("")
        lines.append("#### Nucleon Positions and Properties")
        lines.append("")
        lines.append("| # | Type | Position (fm) | Chirality | v₁ (c) | v₂ (c) | v₃ (c) | ω (rad/s) | Phase (rad) |")
        lines.append("|---|------|---------------|-----------|--------|--------|--------|------------|-------------|")
        
        for i, n in enumerate(nucleons, 1):
            pos_str = format_position(n["x"], n["y"], n["z"])
            v1_str = format_velocity(n["velocity_v1"])
            v2_str = format_velocity(n["velocity_v2"])
            v3_str = format_velocity(n["velocity_v3"])
            omega_str = format_frequency(n["rotation_frequency"])
            phase_str = f"{n['phase_angle']:.3f}"
            
            lines.append(
                f"| {i} | {n['type']} | {pos_str} | {n['chirality']} | "
                f"{v1_str} | {v2_str} | {v3_str} | {omega_str} | {phase_str} |"
            )
        
        lines.append("")
        
        # Relative velocities
        if struct["relative_velocities"]:
            lines.append("#### Relative Velocities Between Nucleons")
            lines.append("")
            lines.append("| Pair | Relative Velocity (c) |")
            lines.append("|------|----------------------|")
            
            # Show first 10 pairs
            pairs = list(struct["relative_velocities"].items())[:10]
            for pair_key, rel_v in pairs:
                i, j = pair_key.split("-")
                lines.append(f"| {i}-{j} | {rel_v:.6f} |")
            
            if len(struct["relative_velocities"]) > 10:
                lines.append(f"| ... | ({len(struct['relative_velocities']) - 10} more pairs) |")
            
            lines.append("")
        
        # Rotation mechanism
        lines.append("#### Rotation Mechanism")
        lines.append("")
        rot_axis = struct["nuclear_rotation_axis"]
        rot_freq = struct["nuclear_rotation_frequency"]
        lines.append(f"- **Nuclear Rotation Axis**: ({rot_axis[0]:.3f}, {rot_axis[1]:.3f}, {rot_axis[2]:.3f})")
        lines.append(f"- **Nuclear Rotation Frequency**: {format_frequency(rot_freq)}")
        lines.append(f"- **Individual Nucleon Spin**: ~{format_frequency(OMEGA_P)} (in-place rotation)")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)

def main():
    """Generate comprehensive tables"""
    print("Loading trefoil mappings...")
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        structures = json.load(f)
    
    print(f"Loaded {len(structures)} element structures")
    print("Generating comprehensive tables...")
    
    table_content = generate_element_table(structures)
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(table_content)
    
    print(f"Generated tables: {OUTPUT_FILE}")
    print(f"Total elements: {len(structures)}")

if __name__ == "__main__":
    main()
