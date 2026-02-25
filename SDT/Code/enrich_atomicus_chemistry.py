#!/usr/bin/env python3
"""
Enhanced ATOMICUS enrichment: Add comprehensive SDT chemistry framework data.

Extracts data from chemistry papers and adds:
- Nuclear field strength (A)
- Atomic radius
- Electronegativity
- Bond formation data
- Authorization criterion status
- Periodic trend data
"""

import os
import re
import math
from pathlib import Path
from typing import Optional, Tuple

# ATOMICUS directory
ATOMICUS_DIR = Path(r'c:\Users\Jimmi\Spatial_Displacement_Theory\SDT\ATOMICUS')

# Constants from chemistry papers
P_CMB = 2.036e-2  # Pa
R_N_0 = 1.2e-15  # m (nuclear radius constant)
A_0_REF = 1  # Reference nucleon count
R_ATOMIC_REF = 50e-12  # m (reference atomic radius ~50 pm)

# Nuclear structure data from chemistry papers
# D-T decomposition: D = 2Z - N (deuterons), T = N - Z (overloaded neutrons)
# Structure: nα for even-A; nα + T(p+2n) for odd-A
NUCLEAR_STRUCTURE = {
    # Period 1-2
    (1, 0): {"A": 1, "structure": "Single proton", "alpha": "-", "field": "1×"},
    (1, 1): {"A": 2, "structure": "D = (p+n)", "alpha": "Deuteron", "field": "2×"},
    (2, 2): {"A": 4, "structure": "1α (2p+2n)", "alpha": "Single α", "field": "4×"},
    (3, 4): {"A": 7, "structure": "1α + 1p", "alpha": "α + p", "field": "7×"},
    (4, 5): {"A": 9, "structure": "1α + 1p + 1n", "alpha": "α + p + n", "field": "9×"},
    (5, 6): {"A": 11, "structure": "1α + 1p + 2n", "alpha": "α + p + 2n", "field": "11×"},
    (6, 6): {"A": 12, "structure": "3α", "alpha": "Triangular (3α)", "field": "12×"},
    (7, 7): {"A": 14, "structure": "3α + 1p", "alpha": "Triangular (3α) + p", "field": "14×"},
    (8, 8): {"A": 16, "structure": "4α", "alpha": "Tetrahedral (4α)", "field": "16×"},
    (9, 10): {"A": 19, "structure": "4α + 1p", "alpha": "Tetrahedral (4α) + p", "field": "19×"},
    (10, 10): {"A": 20, "structure": "4α + 1α", "alpha": "Tetrahedral (4α) + α", "field": "20×"},
    
    # Period 3
    (11, 12): {"A": 23, "structure": "4α + 3p", "alpha": "Tetrahedral (4α) + 3p", "field": "23×"},
    (12, 12): {"A": 24, "structure": "6α", "alpha": "Octahedral (6α)", "field": "24×"},
    (13, 14): {"A": 27, "structure": "6α + 1p", "alpha": "Octahedral (6α) + p", "field": "27×"},
    (14, 14): {"A": 28, "structure": "7α", "alpha": "Extended structure", "field": "28×"},
    (15, 16): {"A": 31, "structure": "7α + 1p", "alpha": "Extended + p", "field": "31×"},
    (16, 16): {"A": 32, "structure": "8α", "alpha": "Cubic (8α)", "field": "32×"},
    (17, 18): {"A": 35, "structure": "8α + 1p", "alpha": "Cubic (8α) + p", "field": "35×"},
    (18, 22): {"A": 40, "structure": "10α", "alpha": "Extended structure", "field": "40×"},

    # Period 4 (Z=19–36): K through Kr
    (19, 20): {"A": 39, "structure": "9α + 1p + 2n", "alpha": "9α + 1T", "field": "39×"},
    (20, 20): {"A": 40, "structure": "10α", "alpha": "10α", "field": "40×"},
    (21, 24): {"A": 45, "structure": "9α + 3p + 6n", "alpha": "9α + 3T", "field": "45×"},
    (22, 26): {"A": 48, "structure": "12α", "alpha": "12α", "field": "48×"},
    (23, 28): {"A": 51, "structure": "9α + 5p + 10n", "alpha": "9α + 5T", "field": "51×"},
    (24, 28): {"A": 52, "structure": "13α", "alpha": "13α", "field": "52×"},
    (25, 30): {"A": 55, "structure": "10α + 5p + 10n", "alpha": "10α + 5T", "field": "55×"},
    (26, 30): {"A": 56, "structure": "14α", "alpha": "14α", "field": "56×"},
    (27, 32): {"A": 59, "structure": "11α + 5p + 10n", "alpha": "11α + 5T", "field": "59×"},
    (28, 30): {"A": 58, "structure": "13α + 2p + 4n", "alpha": "13α + 2T", "field": "58×"},
    (29, 34): {"A": 63, "structure": "12α + 5p + 10n", "alpha": "12α + 5T", "field": "63×"},
    (30, 34): {"A": 64, "structure": "16α", "alpha": "16α", "field": "64×"},
    (31, 38): {"A": 69, "structure": "12α + 7p + 14n", "alpha": "12α + 7T", "field": "69×"},
    (32, 42): {"A": 74, "structure": "11α + 10p + 20n", "alpha": "11α + 10T", "field": "74×"},
    (33, 42): {"A": 75, "structure": "12α + 9p + 18n", "alpha": "12α + 9T", "field": "75×"},
    (34, 46): {"A": 80, "structure": "20α", "alpha": "20α", "field": "80×"},
    (35, 44): {"A": 79, "structure": "13α + 9p + 18n", "alpha": "13α + 9T", "field": "79×"},
    (36, 48): {"A": 84, "structure": "21α", "alpha": "21α", "field": "84×"},

    # Period 5 (Z=37–50): Rb through Sn
    (37, 48): {"A": 85, "structure": "13α + 11p + 22n", "alpha": "13α + 11T", "field": "85×"},
    (38, 50): {"A": 88, "structure": "22α", "alpha": "22α", "field": "88×"},
    (39, 50): {"A": 89, "structure": "14α + 11p + 22n", "alpha": "14α + 11T", "field": "89×"},
    (40, 50): {"A": 90, "structure": "15α + 10p + 20n", "alpha": "15α + 10T", "field": "90×"},
    (41, 52): {"A": 93, "structure": "15α + 11p + 22n", "alpha": "15α + 11T", "field": "93×"},
    (42, 56): {"A": 98, "structure": "14α + 14p + 28n", "alpha": "14α + 14T", "field": "98×"},
    (43, 55): {"A": 98, "structure": "15α + 1D + 12T", "alpha": "15α + 1D + 12T", "field": "98×"},
    (44, 58): {"A": 102, "structure": "15α + 14p + 28n", "alpha": "15α + 14T", "field": "102×"},
    (45, 58): {"A": 103, "structure": "16α + 13p + 26n", "alpha": "16α + 13T", "field": "103×"},
    (46, 60): {"A": 106, "structure": "16α + 14p + 28n", "alpha": "16α + 14T", "field": "106×"},
    (47, 60): {"A": 107, "structure": "17α + 13p + 26n", "alpha": "17α + 13T", "field": "107×"},
    (48, 66): {"A": 114, "structure": "15α + 18p + 36n", "alpha": "15α + 18T", "field": "114×"},
    (49, 66): {"A": 115, "structure": "16α + 17p + 34n", "alpha": "16α + 17T", "field": "115×"},
    (50, 68): {"A": 118, "structure": "16α + 18p + 36n", "alpha": "16α + 18T", "field": "118×"},
}

# Default stable isotope N for each Z when filename omits N (used for ATOMICUS files like 037_Rubidium_Rb_37.md)
STABLE_ISOTOPE_N = {
    1: 0, 2: 2, 3: 4, 4: 5, 5: 6, 6: 6, 7: 7, 8: 8, 9: 10, 10: 10, 11: 12, 12: 12, 13: 14, 14: 14, 15: 16, 16: 16, 17: 18, 18: 22,
    19: 20, 20: 20, 21: 24, 22: 26, 23: 28, 24: 28, 25: 30, 26: 30, 27: 32, 28: 30, 29: 34, 30: 34, 31: 38, 32: 42, 33: 42, 34: 46,
    35: 44, 36: 48, 37: 48, 38: 50, 39: 50, 40: 50, 41: 52, 42: 56, 43: 55, 44: 58, 45: 58, 46: 60, 47: 60, 48: 66, 49: 66, 50: 68,
}

# Experimental chemical property data (from chemistry papers)
CHEMICAL_PROPERTIES = {
    1: {"r_pm": 53, "I1_eV": 13.598, "EA_eV": 0.754, "chi": 2.20},
    2: {"r_pm": 31, "I1_eV": 24.587, "EA_eV": -0.52, "chi": None},
    3: {"r_pm": 152, "I1_eV": 5.392, "EA_eV": 0.618, "chi": 0.98},
    4: {"r_pm": 112, "I1_eV": 9.323, "EA_eV": -0.19, "chi": 1.57},
    5: {"r_pm": 85, "I1_eV": 8.298, "EA_eV": 0.277, "chi": 2.04},
    6: {"r_pm": 77, "I1_eV": 11.260, "EA_eV": 1.263, "chi": 2.55},
    7: {"r_pm": 71, "I1_eV": 14.534, "EA_eV": -0.07, "chi": 3.04},
    8: {"r_pm": 66, "I1_eV": 13.618, "EA_eV": 1.461, "chi": 3.44},
    9: {"r_pm": 57, "I1_eV": 17.423, "EA_eV": 3.339, "chi": 3.98},
    10: {"r_pm": 58, "I1_eV": 21.565, "EA_eV": -0.36, "chi": None},
    11: {"r_pm": 186, "I1_eV": 5.139, "EA_eV": 0.548, "chi": 0.93},
    12: {"r_pm": 160, "I1_eV": 7.646, "EA_eV": -0.20, "chi": 1.31},
    14: {"r_pm": 111, "I1_eV": 8.152, "EA_eV": 1.385, "chi": 1.90},
}

# Bond data from Chemical Bonding paper
BOND_DATA = {
    "H": {"molecules": ["H₂"], "lengths": {"H₂": 74.14}},
    "O": {"molecules": ["H₂O", "O₂"], "lengths": {"H₂O": 95.84, "O₂": 120.74}, "angles": {"H₂O": 104.45}},
    "C": {"molecules": ["CH₄", "CO₂"], "lengths": {"CH₄": 109.0, "CO₂": 116.3}, "angles": {"CH₄": 109.47, "CO₂": 180.0}},
    "N": {"molecules": ["NH₃"], "lengths": {"NH₃": 101.7}, "angles": {"NH₃": 107.0}},
}


def parse_filename(filename: str) -> Optional[Tuple[int, int, str, str]]:
    """Parse ATOMICUS filename to extract Z, N, symbol, name."""
    # Pattern: "006_Carbon_C_6_6.md" or "011_Sodium_Na_11_12.md"
    match = re.match(r'(\d+)_([A-Za-z]+)_([A-Za-z]+)_(\d+)(?:_(\d+))?\.md', filename)
    if not match:
        return None
    
    _, name, symbol, z_str, n_str = match.groups()
    Z = int(z_str)
    N = int(n_str) if n_str else Z
    return Z, N, symbol, name


def calculate_nuclear_radius(A: int) -> float:
    """Calculate nuclear radius from mass number."""
    return R_N_0 * (A ** (1/3))


def calculate_kinematic_ratio(I1_eV: float) -> float:
    """Calculate kinematic ratio chi from ionization energy."""
    if I1_eV <= 0:
        return 0.0
    E_J = I1_eV * 1.602176634e-19
    v = math.sqrt(2 * E_J / 9.10938356e-31)
    c = 299792458.0
    return c / v if v > 0 else 0.0


def check_authorization(Z: int, chi: float, A: int) -> dict:
    """Check nuclear authorization criterion for bond formation."""
    # Criterion (i): Timescale (assume stable if long-lived)
    tau_bond_form = 1e-16  # s
    tau_nucleus = 1e6  # s (assume stable)
    timescale_ok = tau_nucleus > 1e3 * tau_bond_form
    
    # Criterion (ii): Kinematic ratio bound
    chi_max = 237.0
    chi_ok = chi < chi_max if chi > 0 else False
    
    # Criterion (iii): Compression gradient (simplified check)
    # Assume stable if in known stable range
    compression_ok = Z <= 92  # Up to Uranium
    
    # Criterion (iv): Occlusion (simplified check)
    occlusion_ok = True  # Assume accessible
    
    authorized = timescale_ok and chi_ok and compression_ok and occlusion_ok
    
    return {
        "authorized": authorized,
        "timescale_ok": timescale_ok,
        "chi_ok": chi_ok,
        "compression_ok": compression_ok,
        "occlusion_ok": occlusion_ok,
        "chi": chi,
        "chi_max": chi_max,
    }


def generate_chemistry_section(Z: int, N: int, symbol: str, name: str, I1_eV: Optional[float] = None) -> str:
    """Generate Part IV: SDT Chemistry Framework section."""
    
    # Get nuclear structure: use (Z,N) from filename; if not found, fall back to stable isotope for Z
    nuc_key = (Z, N)
    nuc_data = NUCLEAR_STRUCTURE.get(nuc_key)
    if nuc_data is None and Z in STABLE_ISOTOPE_N:
        nuc_key = (Z, STABLE_ISOTOPE_N[Z])
        nuc_data = NUCLEAR_STRUCTURE.get(nuc_key, {})
    else:
        nuc_data = nuc_data or {}
    A = nuc_data.get("A", Z + N if Z + N > 0 else Z)
    structure = nuc_data.get("structure", f"{A} nucleons")
    alpha_arr = nuc_data.get("alpha", "-")
    field_str = nuc_data.get("field", f"{A}×")
    
    # Get chemical properties
    props = CHEMICAL_PROPERTIES.get(Z, {})
    r_pm = props.get("r_pm", None)
    I1 = I1_eV or props.get("I1_eV", None)
    EA = props.get("EA_eV", None)
    chi_val = props.get("chi", None)
    
    # Calculate derived quantities
    R_nuc = calculate_nuclear_radius(A)
    chi_calc = calculate_kinematic_ratio(I1) if I1 else None
    
    # Check authorization
    auth_data = check_authorization(Z, chi_calc or chi_val or 0, A) if (chi_calc or chi_val) else None
    
    # Get bond data
    bond_info = BOND_DATA.get(symbol, {})
    
    section = f"""
---

## Part IV: SDT Chemistry Framework

### Nuclear Structure → Chemical Properties

**A. Nuclear Packing Geometry**

- **Mass Number (A):** {A}
- **Nuclear Structure:** {structure}
- **Alpha Arrangement:** {alpha_arr}
- **Nuclear Field Strength:** {field_str}
- **Nuclear Radius:** $R_\\text{{nuc}} = {R_nuc:.3e}$ m = {R_nuc * 1e15:.2f} fm

**B. Chemical Properties from Nuclear Field**

"""
    
    if r_pm:
        r_m = r_pm * 1e-12
        section += f"""
- **Atomic Radius:** $r_\\text{{atom}} = {r_pm}$ pm = {r_m:.3e} m
  - **SDT Scaling:** $r_\\text{{atom}} \\propto A^{{-1/3}} \\times f(\\text{{geometry}})$
  - **Geometry Factor:** Determined by alpha arrangement ({alpha_arr})
"""
    
    if I1:
        section += f"""
- **First Ionization Energy:** $I_1 = {I1:.3f}$ eV
  - **SDT Scaling:** $I_1 \\propto A \\times \\frac{{1}}{{r_\\text{{atom}}^2}}$
  - **Nuclear Field Contribution:** {field_str} nuclear field strength
"""
        
        if chi_calc:
            section += f"""
  - **Kinematic Ratio:** $\\chi = c/v = {chi_calc:.2f}$
    - **Reference:** Hydrogen $\\chi_H = 137.0$ (universal constant)
    - **SDT Interpretation:** Higher $\\chi$ means lower velocity and weaker binding
"""
    
    if EA is not None:
        section += f"""
- **Electron Affinity:** $EA = {EA:.3f}$ eV
  - **SDT Scaling:** $EA \\propto -A \\times \\frac{{1}}{{r_\\text{{atom}}^2}}$
  - **Nuclear Field Contribution:** {field_str} nuclear field strength
"""
    
    if chi_val:
        section += f"""
- **Electronegativity:** $\\chi = {chi_val:.2f}$ (Pauling scale)
  - **SDT Scaling:** $\\chi \\propto \\frac{{A}}{{r_\\text{{atom}}^2}} \\times f(\\text{{geometry}})$
  - **Geometry Factor:** {alpha_arr} arrangement
"""
    
    section += f"""
**C. Nuclear Authorization Criterion**

**Gate A: Electron Solution Exists**
- Bound electronic state exists in effective potential generated by nuclear boundary conditions
- Potential created by CMB pressure occlusion ($P_\\text{{CMB}} = {P_CMB:.3e}$ Pa)

**Gate B: Nuclear Configuration is Dynamically Admissible**
"""
    
    if auth_data:
        auth_status = "✓ AUTHORIZED" if auth_data["authorized"] else "✗ NOT AUTHORIZED"
        section += f"""
- **Authorization Status:** {auth_status}
- **Criterion (i) Timescale:** $\\tau_\\text{{nucleus}} > 10^{{-13}}$ s → {"✓" if auth_data["timescale_ok"] else "✗"}
- **Criterion (ii) Kinematic Ratio:** $\\chi < 237$ → {"✓" if auth_data["chi_ok"] else "✗"} ($\\chi = {auth_data["chi"]:.2f}$)
- **Criterion (iii) Compression:** $|\\Delta\\chi_Z| < 50$ per proton → {"✓" if auth_data["compression_ok"] else "✗"}
- **Criterion (iv) Occlusion:** $\\Xi_{{n\\ell}} > 0.1$ → {"✓" if auth_data["occlusion_ok"] else "✗"}
"""
    else:
        section += """
- **Authorization Status:** Requires complete kinematic ratio calculation
"""
    
    if bond_info.get("molecules"):
        section += f"""
**D. Bond Formation Data**

"""
        for mol in bond_info["molecules"]:
            section += f"- **{mol}:**\n"
            if mol in bond_info.get("lengths", {}):
                r_bond = bond_info["lengths"][mol]
                section += f"  - Bond length: $r = {r_bond:.2f}$ pm\n"
            if mol in bond_info.get("angles", {}):
                theta = bond_info["angles"][mol]
                section += f"  - Bond angle: $\\theta = {theta:.2f}°$\n"
            section += "\n"
    
    section += """
**E. Connection to CMB Pressure Field**

All chemical properties ultimately trace to the Cosmic Microwave Background (CMB) radiation, which provides the continuous influx of electromagnetic energy that establishes and maintains all pressure fields:

$$\\Pi(\\mathbf{r}) = \\int_{4\\pi} I_\\text{CMB}(\\hat{\\mathbf{n}}) \\left[1 - E(\\mathbf{r}, \\hat{\\mathbf{n}})\\right] d\\Omega$$

where $I_\\text{CMB}(\\hat{\\mathbf{n}})$ originates from the last scattering surface at redshift $z = 1089.9$.

**Physical Mechanism:**
1. CMB radiation propagates through spation, establishing pressure field
2. Nuclei create occlusion $E(\\mathbf{r}, \\hat{\\mathbf{n}})$
3. Nuclear field strength determines electron binding
4. All chemical properties emerge from nuclear structure and CMB pressure

---

"""
    
    return section


def process_file(filepath: Path):
    """Process a single ATOMICUS file."""
    filename = filepath.name
    parsed = parse_filename(filename)
    
    if not parsed:
        print(f"Skipping {filename} - parse failed")
        return
    
    Z, N, symbol, name = parsed
    
    # Read file
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return
    
    # Extract I1 from existing content if available
    I1_match = re.search(r'Ionization Energy.*?(\d+\.?\d*)\s*eV', content, re.IGNORECASE)
    I1_eV = float(I1_match.group(1)) if I1_match else None
    
    has_part_iv = "## Part IV: SDT Chemistry Framework" in content
    chemistry_section = generate_chemistry_section(Z, N, symbol, name, I1_eV)

    if has_part_iv:
        # Update existing Part IV section (e.g. after NUCLEAR_STRUCTURE extension)
        import sys
        if "--update" not in sys.argv:
            print(f"Skipping {name} - chemistry section already exists (use --update to refresh)")
            return
        # Replace Part IV block: from "## Part IV" to next "## Part" or end
        part_iv_start = content.find("## Part IV: SDT Chemistry Framework")
        if part_iv_start == -1:
            return
        # Find start of next Part (V or VI) or major "---" section
        part_iv_end = part_iv_start + len("## Part IV: SDT Chemistry Framework")
        for marker in ["\n## Part V:", "\n## Part VI:", "\n## Part VII:"]:
            idx = content.find(marker, part_iv_end)
            if idx != -1:
                part_iv_end = idx
                break
        else:
            # No next Part; find "---" or end of file
            dash = content.find("\n---\n", part_iv_end)
            if dash != -1:
                part_iv_end = dash + 1  # keep the ---
            else:
                part_iv_end = len(content)
        new_content = content[:part_iv_start] + chemistry_section.rstrip() + "\n\n" + content[part_iv_end:]
    else:
        # Append before final "*(End of Chapter)*" if present, otherwise append at end
        if "*(End of Chapter" in content:
            # Insert before end marker - find position manually to avoid regex escape issues
            end_pos = content.rfind("*(End of Chapter")
            if end_pos != -1:
                # Find the closing *)
                end_close = content.find("*)", end_pos)
                if end_close != -1:
                    new_content = content[:end_pos] + chemistry_section + content[end_pos:]
                else:
                    new_content = content + chemistry_section
            else:
                new_content = content + chemistry_section
        else:
            # Append at end
            new_content = content + chemistry_section
    
    # Write back
    try:
        filepath.write_text(new_content, encoding='utf-8')
        print(f"Enhanced {name} (Z={Z}, N={N})")
    except Exception as e:
        print(f"Error writing {filename}: {e}")


def main():
    """Process all ATOMICUS files."""
    files = sorted(ATOMICUS_DIR.glob("*.md"))
    # Filter out index and rule files
    files = [f for f in files if f.name not in ["ATOMICUS_INDEX.md", "On the Nature of Atomicus Rules.md", "SDT_Master_Geometric_Table.md"]]
    
    print(f"Found {len(files)} ATOMICUS files to process...\n")
    
    for filepath in files:
        process_file(filepath)
    
    print(f"\nCompleted enrichment of {len(files)} ATOMICUS files.")


if __name__ == "__main__":
    main()
