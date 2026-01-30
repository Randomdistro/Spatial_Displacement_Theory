#!/usr/bin/env python3
"""
Add magnetic properties section to ATOMICUS files based on unpaired electrons.

Key insight: Unpaired electrons = Unpaired protons in nucleus
Maximum alphas = (Z - unpaired_electrons) / 2
"""

import re
from pathlib import Path
from typing import Optional, Tuple

ATOMICUS_DIR = Path(r'c:\Users\Jimmi\Spatial_Displacement_Theory\SDT\ATOMICUS')

# Import the unpaired electron calculation
import sys
sys.path.append(str(Path(__file__).parent))
from index_unpaired_electrons import (
    parse_filename, build_electron_config, calculate_unpaired_electrons,
    config_to_string, determine_magnetic_type, calculate_magnetic_moment,
    count_unpaired_in_subshell, SUBSHELL_CAPACITY
)


def generate_magnetic_section(Z: int, symbol: str, name: str, 
                              config: dict, unpaired_count: int,
                              unpaired_details: dict) -> str:
    """Generate Part V: Magnetic Properties section."""
    
    config_str = config_to_string(config)
    magnetic_type = determine_magnetic_type(unpaired_count, Z)
    magnetic_moment = calculate_magnetic_moment(unpaired_count)
    
    # Calculate maximum alphas
    max_alphas = (Z - unpaired_count) // 2
    unpaired_protons = unpaired_count
    
    # Generate subshell breakdown
    subshell_breakdown = []
    for (n, l), electrons in sorted(config.items()):
        if electrons > 0:
            unpaired_in_subshell = count_unpaired_in_subshell(electrons, l)
            if unpaired_in_subshell > 0:
                subshell_breakdown.append(f"{n}{l}⁽{electrons}⁾: {unpaired_in_subshell} unpaired")
    
    section = f"""
---

## Part V: Magnetic Properties from Unpaired Electrons

### Unpaired Electron Analysis

**Electron Configuration:** `{config_str}`

**Unpaired Electron Count:**
- **Total Unpaired:** {unpaired_count} electrons
- **Unpaired by Subshell:** {", ".join(subshell_breakdown) if subshell_breakdown else "None"}

### Nuclear Structure Constraint

**Critical SDT Principle:** Unpaired electrons = Unpaired protons in nucleus

- **Unpaired Protons:** {unpaired_protons} protons cannot form alpha particles (2p+2n)
- **Maximum Alpha Particles:** ({Z} - {unpaired_count}) / 2 = **{max_alphas} alphas**
- **Remaining Structure:** {unpaired_protons} protons + additional neutrons must form:
  - Tritons (p-n-n) if neutrons available
  - Deuterons (p-n) if limited neutrons
  - Or remain unpaired

**Nuclear Structure Implication:**
- This element **CANNOT** have {Z//2} alphas (would require all protons paired)
- Maximum alpha structure: **{max_alphas} alphas** + remaining unpaired protons/neutrons
- The {unpaired_count} unpaired electrons directly constrain the nuclear packing geometry

### Magnetic Properties

**Magnetic Type:** {magnetic_type}

**Magnetic Moment:**
- **Spin-only:** μ = {magnetic_moment:.2f} μ_B
- **Formula:** μ = √[n(n+2)] μ_B where n = {unpaired_count} unpaired electrons

**SDT Interpretation:**
- **Unpaired Protons:** {unpaired_protons} protons in the nucleus are not geometrically paired into alphas
- **Magnetic Wake:** The {unpaired_count} unpaired electrons create asymmetric helical wake patterns
- **CMB Pressure:** Magnetic properties emerge from CMB pressure field occlusion geometry
- **Nuclear-Electron Coupling:** The unpaired protons create pressure field asymmetries that manifest as unpaired electrons

### Connection to Chemistry

- The {unpaired_count} unpaired electrons affect:
  - Chemical reactivity (unpaired electrons available for bonding)
  - Magnetic susceptibility ({magnetic_type} behavior)
  - Coordination geometry (asymmetric electron distribution)
- The {unpaired_protons} unpaired protons affect:
  - Nuclear stability (cannot form perfect alpha lattice)
  - Nuclear magnetic moment (if applicable)
  - Isotope distribution patterns

---

"""
    
    return section


def process_file(filepath: Path):
    """Process a single ATOMICUS file."""
    filename = filepath.name
    parsed = parse_filename(filename)
    
    if not parsed:
        return
    
    Z, N, symbol, name = parsed
    
    # Skip deuterium
    if "Deuterium" in name:
        return
    
    # Read file
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return
    
    # Check if magnetic section already exists
    if "## Part V: Magnetic Properties from Unpaired Electrons" in content:
        print(f"Skipping {name} - magnetic section already exists")
        return
    
    # Build electron configuration
    config = build_electron_config(Z)
    unpaired_count, unpaired_details = calculate_unpaired_electrons(config)
    
    # Generate magnetic section
    magnetic_section = generate_magnetic_section(Z, symbol, name, config, 
                                                 unpaired_count, unpaired_details)
    
    # Insert before end marker or append at end
    if "*(End of Chapter" in content:
        end_pos = content.rfind("*(End of Chapter")
        if end_pos != -1:
            new_content = content[:end_pos] + magnetic_section + content[end_pos:]
        else:
            new_content = content + magnetic_section
    else:
        new_content = content + magnetic_section
    
    # Write back
    try:
        filepath.write_text(new_content, encoding='utf-8')
        print(f"Added magnetic properties to {name} (Z={Z}): {unpaired_count} unpaired → max {((Z - unpaired_count) // 2)} alphas")
    except Exception as e:
        print(f"Error writing {filename}: {e}")


def main():
    """Process all ATOMICUS files."""
    files = sorted(ATOMICUS_DIR.glob("*.md"))
    files = [f for f in files if f.name not in ["ATOMICUS_INDEX.md", "On the Nature of Atomicus Rules.md", 
                                                 "SDT_Master_Geometric_Table.md", "UNPAIRED_ELECTRONS_INDEX.md"]]
    
    print(f"Processing {len(files)} ATOMICUS files...\n")
    
    for filepath in files:
        process_file(filepath)
    
    print(f"\nCompleted adding magnetic properties sections.")


if __name__ == "__main__":
    main()
