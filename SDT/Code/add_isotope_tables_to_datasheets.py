#!/usr/bin/env python3
"""
Add isotope tables to existing Part V datasheets in ATOMICUS files.
"""

import re
from pathlib import Path

ATOMICUS_DIR = Path(r'c:\Users\Jimmi\Spatial_Displacement_Theory\SDT\ATOMICUS')


def extract_isotopes_from_content(content: str, Z: int, symbol: str, name: str) -> list:
    """Extract isotope information from content."""
    isotopes = []
    
    # Pattern: "Carbon-12", "Carbon-13", etc.
    patterns = [rf'{symbol}-(\d+)', rf'{name}-(\d+)']
    
    matches = []
    for pattern in patterns:
        matches.extend(re.finditer(pattern, content, re.IGNORECASE))
    
    seen = set()
    for match in matches:
        A = int(match.group(1))
        if A in seen:
            continue
        seen.add(A)
        
        # Look for context around the match
        start_pos = max(0, match.start() - 100)
        end_pos = min(len(content), match.end() + 200)
        context = content[start_pos:end_pos]
        
        isotope = {"A": A, "N": A - Z, "mass": A, "abundance": "-", "half_life": "Stable", "notes": ""}
        
        # Extract abundance
        abund_match = re.search(r'(\d+\.?\d*)\s*%', context)
        if abund_match:
            isotope["abundance"] = f"{float(abund_match.group(1)):.2f}%"
        
        # Extract half-life
        half_life_match = re.search(r't_?\{?1/2\}?\s*[=:]\s*([\d.]+)\s*(years?|days?|hours?|minutes?|seconds?|ms|μs|ns)', context, re.IGNORECASE)
        if half_life_match:
            isotope["half_life"] = f"{half_life_match.group(1)} {half_life_match.group(2)}"
        
        # Check for stability mentions
        if "stable" in context.lower() and isotope["half_life"] == "Stable":
            pass  # Already set
        elif isotope["half_life"] == "Stable" and "decay" in context.lower():
            # Might be unstable, check more carefully
            if half_life_match:
                isotope["half_life"] = f"{half_life_match.group(1)} {half_life_match.group(2)}"
        
        isotopes.append(isotope)
    
    isotopes.sort(key=lambda x: x["A"])
    return isotopes


def generate_isotope_table(isotopes: list, symbol: str) -> str:
    """Generate isotope properties table."""
    if not isotopes:
        return ""
    
    table = "\n### Isotope Properties\n\n"
    table += "| Isotope | A | N | Mass (u) | Abundance (%) | Half-life | Notes |\n"
    table += "|---------|---|---|----------|---------------|-----------|-------|\n"
    
    for iso in isotopes:
        notes = iso.get("notes", "")
        if not notes:
            if iso["half_life"] == "Stable":
                notes = "Stable isotope"
            else:
                notes = f"{iso['N']} neutrons"
        
        table += f"| {symbol}-{iso['A']} | {iso['A']} | {iso['N']} | {iso['mass']:.3f} | {iso['abundance']} | {iso['half_life']} | {notes} |\n"
    
    table += "\n"
    return table


def process_file(filepath: Path):
    """Process a single ATOMICUS file."""
    filename = filepath.name
    
    # Skip Hydrogen - keep its CMB section
    if "Hydrogen" in filename and "Deuterium" not in filename:
        return
    
    # Skip index files
    if filename in ["ATOMICUS_INDEX.md", "On the Nature of Atomicus Rules.md", 
                    "SDT_Master_Geometric_Table.md", "UNPAIRED_ELECTRONS_INDEX.md"]:
        return
    
    # Parse filename
    match = re.match(r'(\d+)_([A-Za-z]+)_([A-Za-z]+)_(\d+)(?:_(\d+))?\.md', filename)
    if not match:
        return
    
    _, name, symbol, z_str, n_str = match.groups()
    Z = int(z_str)
    
    # Read file
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return
    
    # Check if Part V exists
    if "## Part V: Atomic Technical Specifications" not in content:
        return
    
    # Check if isotope table already exists
    if "### Isotope Properties" in content:
        print(f"Skipping {name} - isotope table already exists")
        return
    
    # Extract isotopes
    isotopes = extract_isotopes_from_content(content, Z, symbol, name)
    
    if not isotopes:
        print(f"No isotopes found for {name}")
        return
    
    # Generate isotope table
    isotope_table = generate_isotope_table(isotopes, symbol)
    
    # Find insertion point - after the ionization series table ends, before "Electron Shell Velocities"
    # Look for the end of the ionization table (after the last row, before next section)
    insertion_pattern = r'(### Complete Ionization Series.*?\n\n\|.*?\n\|.*?\n(?:.*?\n)*?)\n(### Electron Shell Velocities)'
    match = re.search(insertion_pattern, content, re.DOTALL)
    
    if match:
        # Insert after the ionization table, before Electron Shell section
        insertion_point = match.end(1)
        new_content = content[:insertion_point] + isotope_table + content[insertion_point:]
    else:
        # Fallback: try to find after "Complete Ionization Series" header
        insertion_pattern2 = r'(### Complete Ionization Series.*?\n\n)'
        match2 = re.search(insertion_pattern2, content, re.DOTALL)
        if match2:
            insertion_point = match2.end()
            new_content = content[:insertion_point] + isotope_table + content[insertion_point:]
        else:
            print(f"Could not find insertion point in {name}")
            return
    
    try:
        filepath.write_text(new_content, encoding='utf-8')
        print(f"Added isotope table to {name} ({len(isotopes)} isotopes)")
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
    
    print(f"\nCompleted adding isotope tables to datasheets.")


if __name__ == "__main__":
    main()
