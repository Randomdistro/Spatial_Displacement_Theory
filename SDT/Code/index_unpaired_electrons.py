#!/usr/bin/env python3
"""
Index unpaired electrons across all ATOMICUS entries.

Unpaired electrons indicate unconnected protons and should be represented
in magnetic properties.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

ATOMICUS_DIR = Path(r'c:\Users\Jimmi\Spatial_Displacement_Theory\SDT\ATOMICUS')

# Electron configuration capacity
SUBSHELL_CAPACITY = {
    's': 2,
    'p': 6,
    'd': 10,
    'f': 14
}

# Aufbau order
AUFBAU_ORDER = [
    (1, 's'), (2, 's'), (2, 'p'), (3, 's'), (3, 'p'), (4, 's'),
    (3, 'd'), (4, 'p'), (5, 's'), (4, 'd'), (5, 'p'), (6, 's'),
    (4, 'f'), (5, 'd'), (6, 'p'), (7, 's'), (5, 'f'), (6, 'd'), (7, 'p')
]


@dataclass
class ElementUnpaired:
    """Unpaired electron data for an element."""
    Z: int
    symbol: str
    name: str
    config: str
    unpaired_count: int
    unpaired_details: Dict[str, int]  # subshell -> unpaired count
    magnetic_type: str  # paramagnetic, diamagnetic, ferromagnetic
    magnetic_moment: Optional[float]  # in Bohr magnetons
    notes: str


def parse_filename(filename: str) -> Optional[Tuple[int, int, str, str]]:
    """Parse ATOMICUS filename."""
    match = re.match(r'(\d+)_([A-Za-z]+)_([A-Za-z]+)_(\d+)(?:_(\d+))?\.md', filename)
    if not match:
        return None
    _, name, symbol, z_str, n_str = match.groups()
    Z = int(z_str)
    N = int(n_str) if n_str else Z
    return Z, N, symbol, name


def build_electron_config(Z: int) -> Dict[Tuple[int, str], int]:
    """Build electron configuration using Aufbau principle."""
    config = {}
    remaining = Z
    
    for n, l in AUFBAU_ORDER:
        if remaining <= 0:
            break
        capacity = SUBSHELL_CAPACITY[l]
        fill = min(capacity, remaining)
        config[(n, l)] = fill
        remaining -= fill
    
    return config


def count_unpaired_in_subshell(electrons: int, subshell_type: str) -> int:
    """Count unpaired electrons in a subshell following Hund's rule."""
    capacity = SUBSHELL_CAPACITY[subshell_type]
    
    if electrons == 0:
        return 0
    elif electrons == capacity:
        # Fully filled: all paired
        return 0
    elif electrons <= capacity // 2:
        # First half: all unpaired (maximize unpaired)
        return electrons
    else:
        # Second half: pair up, remaining unpaired
        # For capacity 10 (d): first 5 unpaired, next 5 pair with first 5
        # For capacity 6 (p): first 3 unpaired, next 3 pair with first 3
        # For capacity 2 (s): first 1 unpaired, second pairs
        paired = capacity // 2
        unpaired = capacity - electrons  # Remaining slots
        return unpaired


def calculate_unpaired_electrons(config: Dict[Tuple[int, str], int]) -> Tuple[int, Dict[str, int]]:
    """Calculate total unpaired electrons and per-subshell breakdown."""
    total_unpaired = 0
    details = {}
    
    for (n, l), electrons in config.items():
        subshell_key = f"{n}{l}"
        unpaired = count_unpaired_in_subshell(electrons, l)
        details[subshell_key] = unpaired
        total_unpaired += unpaired
    
    return total_unpaired, details


def determine_magnetic_type(unpaired: int, Z: int) -> str:
    """Determine magnetic type from unpaired electrons."""
    if unpaired == 0:
        return "diamagnetic"
    elif Z in [26, 27, 28]:  # Fe, Co, Ni - ferromagnetic
        return "ferromagnetic"
    else:
        return "paramagnetic"


def calculate_magnetic_moment(unpaired: int) -> float:
    """Calculate magnetic moment in Bohr magnetons (spin-only)."""
    # Spin-only formula: μ = √[n(n+2)] μ_B
    # where n is number of unpaired electrons
    if unpaired == 0:
        return 0.0
    return (unpaired * (unpaired + 2)) ** 0.5


def config_to_string(config: Dict[Tuple[int, str], int]) -> str:
    """Convert config dict to standard notation string."""
    parts = []
    for (n, l), electrons in sorted(config.items()):
        if electrons > 0:
            parts.append(f"{n}{l}^{electrons}")
    return " ".join(parts)


def extract_config_from_file(content: str, Z: int) -> Optional[Dict[Tuple[int, str], int]]:
    """Try to extract electron configuration from file content."""
    # Look for patterns like [Ar] 3d⁸ 4s² or 3d⁸ 4s²
    patterns = [
        r'\[([A-Z][a-z]?)\]\s*([0-9a-z⁰¹²³⁴⁵⁶⁷⁸⁹]+(?:\s+[0-9a-z⁰¹²³⁴⁵⁶⁷⁸⁹]+)*)',
        r'([0-9a-z⁰¹²³⁴⁵⁶⁷⁸⁹]+(?:\s+[0-9a-z⁰¹²³⁴⁵⁶⁷⁸⁹]+)+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            # Try to parse, but for now just use calculated config
            pass
    
    # Default: calculate from Z
    return build_electron_config(Z)


def process_atomicus_file(filepath: Path) -> Optional[ElementUnpaired]:
    """Process a single ATOMICUS file."""
    filename = filepath.name
    parsed = parse_filename(filename)
    
    if not parsed:
        return None
    
    Z, N, symbol, name = parsed
    
    # Skip deuterium (special case)
    if "Deuterium" in name:
        return None
    
    # Read file
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None
    
    # Build electron configuration
    config = extract_config_from_file(content, Z)
    if not config:
        config = build_electron_config(Z)
    
    # Calculate unpaired electrons
    unpaired_count, unpaired_details = calculate_unpaired_electrons(config)
    
    # Determine magnetic properties
    magnetic_type = determine_magnetic_type(unpaired_count, Z)
    magnetic_moment = calculate_magnetic_moment(unpaired_count)
    
    # Generate notes
    notes = []
    if unpaired_count == 0:
        notes.append("All electrons paired - diamagnetic")
    elif unpaired_count == 1:
        notes.append("Single unpaired electron - weak paramagnetic")
    elif unpaired_count >= 2:
        notes.append(f"{unpaired_count} unpaired electrons - {magnetic_type}")
    
    # Check for special cases mentioned in text
    if "unpaired" in content.lower():
        notes.append("Unpaired electrons explicitly mentioned in text")
    
    config_str = config_to_string(config)
    
    return ElementUnpaired(
        Z=Z,
        symbol=symbol,
        name=name,
        config=config_str,
        unpaired_count=unpaired_count,
        unpaired_details=unpaired_details,
        magnetic_type=magnetic_type,
        magnetic_moment=magnetic_moment,
        notes="; ".join(notes)
    )


def generate_index_report(elements: List[ElementUnpaired]) -> str:
    """Generate comprehensive index report."""
    
    report = []
    report.append("# Unpaired Electrons Index: ATOMICUS Database")
    report.append("")
    report.append("**Generated:** December 2025")
    report.append("**Purpose:** Index unpaired electrons across all elements to identify unconnected protons and magnetic properties")
    report.append("")
    report.append("---")
    report.append("")
    report.append("## Executive Summary")
    report.append("")
    
    # Statistics
    total_elements = len(elements)
    paramagnetic = sum(1 for e in elements if e.magnetic_type == "paramagnetic")
    diamagnetic = sum(1 for e in elements if e.magnetic_type == "diamagnetic")
    ferromagnetic = sum(1 for e in elements if e.magnetic_type == "ferromagnetic")
    
    max_unpaired = max(e.unpaired_count for e in elements)
    max_unpaired_elem = [e for e in elements if e.unpaired_count == max_unpaired][0]
    
    report.append(f"- **Total Elements Indexed:** {total_elements}")
    report.append(f"- **Paramagnetic:** {paramagnetic} (have unpaired electrons)")
    report.append(f"- **Diamagnetic:** {diamagnetic} (all electrons paired)")
    report.append(f"- **Ferromagnetic:** {ferromagnetic} (Fe, Co, Ni)")
    report.append(f"- **Maximum Unpaired Electrons:** {max_unpaired} ({max_unpaired_elem.name}, Z={max_unpaired_elem.Z})")
    report.append("")
    
    report.append("## Key Findings")
    report.append("")
    report.append("1. **Unpaired electrons indicate unconnected protons:** Each unpaired electron represents a proton that is not fully paired with another electron in the same geometric configuration.")
    report.append("")
    report.append("2. **Magnetic properties correlate with unpaired count:**")
    report.append("   - 0 unpaired: Diamagnetic (repelled by magnetic field)")
    report.append("   - 1-2 unpaired: Weak paramagnetic (attracted by magnetic field)")
    report.append("   - 3-5 unpaired: Strong paramagnetic or ferromagnetic")
    report.append("")
    report.append("3. **Transition metals show highest unpaired counts:** The d-shell allows for up to 5 unpaired electrons (half-filled d⁵ configuration).")
    report.append("")
    
    report.append("---")
    report.append("")
    report.append("## Complete Index")
    report.append("")
    report.append("| Z | Element | Symbol | Config | Unpaired | Magnetic Type | μ (μ_B) | Notes |")
    report.append("|---|---------|--------|--------|----------|---------------|---------|------|")
    
    for elem in sorted(elements, key=lambda x: x.Z):
        config_short = elem.config[:30] + "..." if len(elem.config) > 30 else elem.config
        mu_str = f"{elem.magnetic_moment:.2f}" if elem.magnetic_moment else "0.00"
        notes_short = elem.notes[:40] + "..." if len(elem.notes) > 40 else elem.notes
        report.append(f"| {elem.Z} | {elem.name} | {elem.symbol} | `{config_short}` | {elem.unpaired_count} | {elem.magnetic_type} | {mu_str} | {notes_short} |")
    
    report.append("")
    report.append("---")
    report.append("")
    report.append("## Recommendations")
    report.append("")
    
    report.append("### 1. Add Magnetic Properties Section to Each ATOMICUS Entry")
    report.append("")
    report.append("**Recommended Format:**")
    report.append("")
    report.append("```markdown")
    report.append("## Part V: Magnetic Properties from Unpaired Electrons")
    report.append("")
    report.append("### Unpaired Electron Count")
    report.append("- **Total Unpaired:** N")
    report.append("- **Configuration:** [config]")
    report.append("- **Unpaired by Subshell:** [breakdown]")
    report.append("")
    report.append("### Magnetic Properties")
    report.append("- **Type:** [paramagnetic/diamagnetic/ferromagnetic]")
    report.append("- **Magnetic Moment:** μ = X.XX μ_B (spin-only)")
    report.append("- **SDT Interpretation:** Unpaired electrons indicate N unconnected protons")
    report.append("")
    report.append("### Connection to Nuclear Structure")
    report.append("- **Unconnected Protons:** Each unpaired electron corresponds to a proton that is not fully geometrically paired")
    report.append("- **Magnetic Wake:** Unpaired electrons create asymmetric helical wake patterns")
    report.append("- **CMB Pressure:** Magnetic properties emerge from CMB pressure field occlusion geometry")
    report.append("```")
    report.append("")
    
    report.append("### 2. Special Attention to Transition Metals")
    report.append("")
    report.append("Transition metals (Groups 3-12) show the most complex unpaired electron patterns:")
    report.append("- **Sc-Ti-V-Cr-Mn:** Increasing unpaired electrons (1→5)")
    report.append("- **Fe-Co-Ni:** Ferromagnetic (4, 3, 2 unpaired respectively)")
    report.append("- **Cu-Zn:** Decreasing unpaired (1→0)")
    report.append("")
    report.append("These should have detailed magnetic property sections.")
    report.append("")
    
    report.append("### 3. Link to Nuclear Structure")
    report.append("")
    report.append("For each element, explicitly state:")
    report.append("- How many protons are 'unconnected' (equal to unpaired electron count)")
    report.append("- How this affects nuclear geometry and stability")
    report.append("- How magnetic properties emerge from the nuclear-electron coupling")
    report.append("")
    
    report.append("---")
    report.append("")
    report.append("## Detailed Examples")
    report.append("")
    
    return "\n".join(report)


def generate_nickel_example(nickel: ElementUnpaired) -> str:
    """Generate detailed example for Nickel."""
    
    example = []
    example.append("### Example 1: Nickel (Z=28)")
    example.append("")
    example.append("**Electron Configuration:**")
    example.append(f"- Full: `{nickel.config}`")
    example.append("- Valence: `3d⁸ 4s²`")
    example.append("")
    example.append("**Unpaired Electron Analysis:**")
    example.append("- **3d⁸ subshell:** 8 electrons in d-shell (capacity 10)")
    example.append("  - First 5 electrons: all unpaired (Hund's rule)")
    example.append("  - Next 3 electrons: pair with first 3, leaving 2 unpaired")
    example.append("  - **Unpaired in 3d:** 2 electrons")
    example.append("- **4s² subshell:** 2 electrons, fully paired")
    example.append("- **Total Unpaired:** 2 electrons")
    example.append("")
    example.append("**Magnetic Properties:**")
    example.append(f"- **Type:** {nickel.magnetic_type}")
    example.append(f"- **Magnetic Moment:** μ = {nickel.magnetic_moment:.2f} μ_B (spin-only)")
    example.append("- **Experimental:** ~2.8 μ_B (includes orbital contribution)")
    example.append("- **Curie Temperature:** 627 K (weakest ferromagnet)")
    example.append("")
    example.append("**SDT Interpretation:**")
    example.append("- **Unconnected Protons:** 2 protons in the nucleus are not fully geometrically paired")
    example.append("- **Nuclear Structure:** Ni-58 is 14-Alpha lattice + 2 neutrons")
    example.append("- **Magnetic Wake:** The 2 unpaired electrons create asymmetric helical wake patterns")
    example.append("- **Geometric Asymmetry:** The 3d⁸ configuration creates a 'Cube Minus Two' geometry")
    example.append("")
    example.append("**Connection to Chemistry:**")
    example.append("- The 2 unpaired electrons allow weak ferromagnetic coupling")
    example.append("- This is weaker than Iron (4 unpaired) or Cobalt (3 unpaired)")
    example.append("- The geometric symmetry of 3d⁸ makes it less reactive than earlier transition metals")
    example.append("")
    
    return "\n".join(example)


def generate_iron_example(iron: ElementUnpaired) -> str:
    """Generate detailed example for Iron."""
    
    example = []
    example.append("### Example 2: Iron (Z=26)")
    example.append("")
    example.append("**Electron Configuration:**")
    example.append(f"- Full: `{iron.config}`")
    example.append("- Valence: `3d⁶ 4s²`")
    example.append("")
    example.append("**Unpaired Electron Analysis:**")
    example.append("- **3d⁶ subshell:** 6 electrons in d-shell (capacity 10)")
    example.append("  - First 5 electrons: all unpaired (Hund's rule)")
    example.append("  - 6th electron: pairs with one, leaving 4 unpaired")
    example.append("  - **Unpaired in 3d:** 4 electrons")
    example.append("- **4s² subshell:** 2 electrons, fully paired")
    example.append("- **Total Unpaired:** 4 electrons")
    example.append("")
    example.append("**Magnetic Properties:**")
    example.append(f"- **Type:** {iron.magnetic_type}")
    example.append(f"- **Magnetic Moment:** μ = {iron.magnetic_moment:.2f} μ_B (spin-only)")
    example.append("- **Experimental:** ~2.2 μ_B per atom (bulk ferromagnetic)")
    example.append("- **Curie Temperature:** 1043 K (strongest ferromagnet)")
    example.append("")
    example.append("**SDT Interpretation:**")
    example.append("- **Unconnected Protons:** 4 protons in the nucleus are not fully geometrically paired")
    example.append("- **Nuclear Structure:** Fe-56 is the 'Geometric Apex' - tightest alpha packing")
    example.append("- **Magnetic Wake:** The 4 unpaired electrons create strong asymmetric helical wake patterns")
    example.append("- **Geometric Asymmetry:** The 3d⁶ configuration creates maximum asymmetry for ferromagnetic coupling")
    example.append("")
    example.append("**Connection to Chemistry:**")
    example.append("- The 4 unpaired electrons allow strong ferromagnetic coupling")
    example.append("- This makes Iron the strongest ferromagnet among the 3d metals")
    example.append("- The asymmetry drives both magnetic properties and chemical reactivity")
    example.append("")
    
    return "\n".join(example)


def main():
    """Main execution."""
    print("Indexing unpaired electrons across ATOMICUS database...")
    
    files = sorted(ATOMICUS_DIR.glob("*.md"))
    files = [f for f in files if f.name not in ["ATOMICUS_INDEX.md", "On the Nature of Atomicus Rules.md", "SDT_Master_Geometric_Table.md"]]
    
    elements = []
    for filepath in files:
        elem = process_atomicus_file(filepath)
        if elem:
            elements.append(elem)
            print(f"Processed {elem.name} (Z={elem.Z}): {elem.unpaired_count} unpaired electrons")
    
    print(f"\nProcessed {len(elements)} elements")
    
    # Generate report
    report = generate_index_report(elements)
    
    # Add examples
    nickel = next((e for e in elements if e.Z == 28), None)
    iron = next((e for e in elements if e.Z == 26), None)
    
    if nickel:
        report += generate_nickel_example(nickel)
    if iron:
        report += generate_iron_example(iron)
    
    # Write report
    report_path = ATOMICUS_DIR / "UNPAIRED_ELECTRONS_INDEX.md"
    report_path.write_text(report, encoding='utf-8')
    
    print(f"\nReport written to: {report_path}")
    print(f"\nSummary:")
    print(f"  - Total elements: {len(elements)}")
    print(f"  - Paramagnetic: {sum(1 for e in elements if e.magnetic_type == 'paramagnetic')}")
    print(f"  - Diamagnetic: {sum(1 for e in elements if e.magnetic_type == 'diamagnetic')}")
    print(f"  - Ferromagnetic: {sum(1 for e in elements if e.magnetic_type == 'ferromagnetic')}")


if __name__ == "__main__":
    main()
