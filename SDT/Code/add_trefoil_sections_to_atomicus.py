#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Trefoil Structure sections to all ATOMICUS files

Adds comprehensive trefoil mapping data to each element file.
"""

import json
import re
from pathlib import Path

try:
    from enrich_atomicus_chemistry import STABLE_ISOTOPE_N
except ImportError:
    STABLE_ISOTOPE_N = {}

_SCRIPT_DIR = Path(__file__).resolve().parent
_SDT_ROOT = _SCRIPT_DIR.parent
ATOMICUS_DIR = _SDT_ROOT / "ATOMICUS"
DATA_FILE = _SDT_ROOT / "data" / "trefoil_mappings.json"

# Constants: v₁·v₃ = c² (energy conservation)
V1_C = 2.23
V2_C = 1.84
V3_C = 1.0 / 2.23  # ≈ 0.4484c

# Load trefoil data; build lookups by (Z,N) and by symbol (stable isotope preferred)
_data = json.load(open(DATA_FILE, 'r', encoding='utf-8'))
structures_by_zn = {(s['Z'], s['N']): s for s in _data}
structures_by_symbol = {}  # symbol -> structure; first listed per symbol
for s in _data:
    key = s['element_symbol']
    if key not in structures_by_symbol:
        structures_by_symbol[key] = s

def format_position(x, y, z):
    """Format position coordinates"""
    return f"({x:.3f}, {y:.3f}, {z:.3f}) fm"

def format_velocity(v):
    """Format velocity"""
    return f"{v:.3f}c"

def generate_trefoil_section(structure):
    """Generate trefoil structure section for an element"""
    
    Z = structure['Z']
    N = structure['N']
    A = structure['A']
    name = structure['element_name']
    symbol = structure['element_symbol']
    blocks = structure['building_blocks']
    nucleons = structure['nucleons']
    
    section = f"""
---

## Part VI: Trefoil Nuclear Structure Mapping

### Nuclear Building Block Structure

**Composition**: {blocks}
- **Total Nucleons**: {len(nucleons)} ({Z} protons, {N} neutrons)
- **Mass Number**: A = {A}

### Nucleon Positions and Orientations

| # | Type | Position (fm) | Chirality | Orientation |
|---|------|---------------|-----------|-------------|
"""
    
    for i, n in enumerate(nucleons[:20], 1):  # Show first 20 nucleons
        pos_str = format_position(n['x'], n['y'], n['z'])
        section += f"| {i} | {n['type']} | {pos_str} | {n['chirality']} | {n['chirality']}-handed trefoil |\n"
    
    if len(nucleons) > 20:
        section += f"| ... | ({len(nucleons) - 20} more nucleons) | | | |\n"
    
    section += "\n### Three-Velocity System\n\n"
    section += "**Velocity Components:**\n\n"
    section += f"- **v₁ (Perihelion)**: {format_velocity(V1_C)} - Fastest component\n"
    section += f"- **v₂ (Average)**: {format_velocity(V2_C)} - Rim velocity (operational)\n"
    section += f"- **v₃ (Aphelion)**: {format_velocity(V3_C)} - Slowest component\n\n"
    section += "**Constraint**: v₁·v₃ = c² (energy conservation)\n\n"
    
    section += "| Nucleon | v₁ (c) | v₂ (c) | v₃ (c) | Phase (rad) |\n"
    section += "|---------|--------|--------|--------|-------------|\n"
    
    for i, n in enumerate(nucleons[:10], 1):  # Show first 10
        section += f"| {i} ({n['type']}) | {format_velocity(n['velocity_v1'])} | {format_velocity(n['velocity_v2'])} | {format_velocity(n['velocity_v3'])} | {n['phase_angle']:.3f} |\n"
    
    if len(nucleons) > 10:
        section += f"| ... | ({len(nucleons) - 10} more) | | | |\n"
    
    section += "\n### Rotation Mechanisms\n\n"
    
    rot_axis = structure['nuclear_rotation_axis']
    rot_freq = structure['nuclear_rotation_frequency']
    
    section += "**Individual Nucleon Spin:**\n"
    section += "- Each nucleon rotates in-place at ~6.57×10²³ rad/s\n"
    section += "- Rotation direction determined by chirality (R = clockwise, L = counterclockwise)\n"
    section += "- Creates spin ½ℏ angular momentum\n\n"
    
    section += "**Nuclear Rotation:**\n"
    section += f"- Whole nucleus rotates as a unit\n"
    section += f"- Rotation axis: ({rot_axis[0]:.3f}, {rot_axis[1]:.3f}, {rot_axis[2]:.3f})\n"
    section += f"- Rotation frequency: {rot_freq:.2e} rad/s\n"
    section += "- Much slower than individual nucleon spin\n\n"
    
    # Relative velocities
    if structure['relative_velocities']:
        section += "### Relative Velocities Between Nucleons\n\n"
        section += "**Key Relative Velocities:**\n\n"
        section += "| Pair | Relative Velocity (c) |\n"
        section += "|------|----------------------|\n"
        
        # Show first 10 pairs
        pairs = list(structure['relative_velocities'].items())[:10]
        for pair_key, rel_v in pairs:
            i, j = pair_key.split("-")
            n1_type = nucleons[int(i)]['type'] if int(i) < len(nucleons) else '?'
            n2_type = nucleons[int(j)]['type'] if int(j) < len(nucleons) else '?'
            section += f"| {i}-{j} ({n1_type}-{n2_type}) | {rel_v:.6f} |\n"
        
        if len(structure['relative_velocities']) > 10:
            section += f"| ... | ({len(structure['relative_velocities']) - 10} more pairs) |\n"
        
        section += "\n"
    
    # Electron-sharing summary (from ELECTRON_SHARING_MODEL)
    internal_electrons = structure.get('internal_electrons', [])
    if internal_electrons:
        section += "### Internal Electron Sharing\n\n"
        section += "**Electron-sharing model:** Neutrons contribute internal electrons that mediate between protons. "
        section += f"This nucleus has **{len(internal_electrons)} internal electron(s)** at mediation points.\n\n"
        section += "| # | Position (fm) | Mediates (nucleon indices) |\n"
        section += "|---|---------------|----------------------------|\n"
        for i, e in enumerate(internal_electrons[:10], 1):
            pos_str = format_position(e['x'], e['y'], e['z'])
            shared = ", ".join(str(idx) for idx in e['shared_with'])
            section += f"| {i} | {pos_str} | {shared} |\n"
        if len(internal_electrons) > 10:
            section += f"| ... | ({len(internal_electrons) - 10} more) | |\n"
        section += "\n*See ELECTRON_SHARING_MODEL.md for deuteron (p-p-e), alpha (four-way), and T-unit rules.*\n\n"
    
    section += "### Physical Interpretation\n\n"
    section += "- **Three-velocity system** creates differential contraction → poloidal flow\n"
    section += "- **Standing wave interference patterns** determine binding energies\n"
    section += "- **Chirality patterns** (L-R pairs) create strong binding\n"
    section += "- **Rotation mechanisms** maintain nuclear stability\n"
    section += "- All properties emerge from trefoil geometry and CMB pressure field\n"
    
    section += "\n---\n"
    
    return section

def process_file(filepath: Path):
    """Process a single ATOMICUS file"""
    filename = filepath.name
    
    # Parse filename
    match = re.match(r'(\d+)_([A-Za-z]+)_([A-Za-z]+)_(\d+)(?:_(\d+))?\.md', filename)
    if not match:
        return
    
    _, name, symbol, z_str, n_str = match.groups()
    Z = int(z_str)
    N = int(n_str) if n_str else STABLE_ISOTOPE_N.get(Z, Z)
    
    # Find structure: (Z,N) when N in filename; else (Z, stable_N) or symbol
    lookup_n = N
    structure = structures_by_zn.get((Z, lookup_n)) or structures_by_symbol.get(symbol)
    if not structure:
        structure = next((s for s in _data if s['Z'] == Z), None)
    
    if not structure:
        print(f"No structure found for {symbol} (Z={Z})")
        return
    
    # Read file
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return
    
    # Check if section already exists
    if "## Part VI: Trefoil Nuclear Structure Mapping" in content:
        print(f"Skipping {name} - trefoil section already exists")
        return
    
    # Generate section
    trefoil_section = generate_trefoil_section(structure)
    
    # Find insertion point - before "*(End of Chapter)*" or at end
    end_marker = "*(End of Chapter)*"
    if end_marker in content:
        insertion_point = content.find(end_marker)
        new_content = content[:insertion_point] + trefoil_section + "\n" + content[insertion_point:]
    else:
        # Append at end
        new_content = content + trefoil_section
    
    # Write back
    try:
        filepath.write_text(new_content, encoding='utf-8')
        print(f"Added trefoil section to {name} (Z={Z})")
    except Exception as e:
        print(f"Error writing {filename}: {e}")

def main():
    """Process all ATOMICUS files"""
    files = sorted(ATOMICUS_DIR.glob("*.md"))
    files = [f for f in files if f.name not in [
        "ATOMICUS_INDEX.md", "On the Nature of Atomicus Rules.md",
        "SDT_Master_Geometric_Table.md", "UNPAIRED_ELECTRONS_INDEX.md"
    ]]
    
    print(f"Processing {len(files)} ATOMICUS files...\n")
    
    for filepath in files:
        process_file(filepath)
    
    print(f"\nCompleted adding trefoil sections to ATOMICUS files.")

if __name__ == "__main__":
    main()
