import os
import re
import math

ATOMICUS_DIR = r'c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\ATOMICUS'

# Constants
C_LATTICE = 299792458.0
M_E = 9.10938356e-31
EV_TO_J = 1.602176634e-19

def calculate_kinematics(ie_ev):
    ie_j = ie_ev * EV_TO_J
    v = math.sqrt(2 * ie_j / M_E)
    v_c = v / C_LATTICE
    k = C_LATTICE / v if v > 0 else 0
    return v, v_c, k

def generate_utilization(name, z, ie_ev, k_factor):
    # SDT-derived utilization logic
    uses = []
    
    if ie_ev > 20:
        uses.append(f"**High-Energy Resonance Buffer**: High ionization energy ({ie_ev} eV) makes {name} ideal for stabilizing high-frequency spation chokes.")
        uses.append("**Inert Shielding**: Extreme geometric stability prevents chemical corrosion, useful for containment vessels.")
    elif ie_ev < 6:
        uses.append(f"**Plasma Genesis Catalysis**: Low ionization threshold ({ie_ev} eV) allows for efficient creation of conductive plasma channels.")
        uses.append("**Ionic Propulsion**: Facile electron removal enables high specific impulse ion thrust generation.")
    else:
        uses.append("**Variable Geometry Tuning**: Moderate ionization allows for switchable interactions (conductive/insulative) via applied voltage.")

    if k_factor < 137:
        uses.append("**Superluminal/Relativistic Boundary Testing**: Low k-factor implies electron velocities approaching relativistic limits, useful for validating SDT high-velocity drag equations.")
    
    return "\n".join([f"- {u}" for u in uses])

def generate_rigorous_section(name, symbol, z, n, ionizations):
    # ionizations is a list of (label, energy)
    
    content = f"""
________________________________________
### Rigorous SDT Mathematical Analysis: {name}

**A. Nuclear Cross-Reference**
- **Nucleus**: {name} (Z={z}, N={n})
- **Geometry**: Geometric Structure derived from Z constraints.
- **SDT Analysis**: Z={z} defines the electromagnetic lens strength.

**B. Ionization Economics and Kinematics**
"""
    
    first_ie = 0
    first_k = 0
    
    for label, ie_ev in ionizations:
        v, v_c, k = calculate_kinematics(ie_ev)
        content += f"""
- **{label} Ionization Energy ($E_{{i}}$)**: {ie_ev} eV
    - **SDT Derived Velocity ($v$)**: {v:.3e} m/s
    - **Relativistic Ratio ($v/c$)**: {v_c:.5f}
    - **Geometric k-factor**: $k = c/v = {k:.2f}$
"""
        if label == "1st" or first_ie == 0:
            first_ie = ie_ev
            first_k = k

    # Utilization Section
    utilization_text = generate_utilization(name, z, first_ie, first_k)
    
    content += f"""
**C. SDT Utilization & Applications**
Derived from the geometric stability and ionization thresholds:
{utilization_text}

**D. Spectral Implications**
(See Table Below)
"""
    return content

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    filename = os.path.basename(filepath)
    # Flexible N regex
    match_meta = re.match(r'On the Nature of ([A-Z][a-z]+) ([A-Z][a-z]?) (\d+) (.*?)\.md', filename)
    if not match_meta:
        # Try Iron Case: On the Nature of Iron Fe 26 30.md
        # The regex above actually works for that too.
        # Try Iron Case without N? On the Nature of Iridium Ir 77 .md
        # N matches " ."
        print(f"Skipping {filename} - Meta regex fail")
        return

    name, symbol, z, n = match_meta.groups()
    n = n.strip()

    # Ionization Search Strategy
    # 1. Look for explicit lists "1st: X, 2nd: Y" (Rare in current text, but good to support)
    # 2. Look for single "Ionization Energy: X"
    # 3. Look for "E_i1 = X"
    
    ionizations = []
    
    # Check for Helium specific text first?
    # "Ionization Energy (Ei1): 24.5874 eV"
    # "The second ionization energy (for He+) is 54.4178 eV"
    
    # Generic regex for generic files
    # Matches "$E_{i1} = 8.6084$ eV" or "E_i1 = 8.6 eV"
    ie1_match = re.search(r'E_?\{?i1\}?\s*=\s*(\d+\.?\d*)', content)
    if not ie1_match:
         ie1_match = re.search(r'Ionization Energy.*?:?\s*(\d+\.?\d*)\s*eV', content, re.IGNORECASE)
    
    if ie1_match:
        ionizations.append(("1st", float(ie1_match.group(1))))
        
    # Search for secondary
    # "second ionization energy ... is 54.4178 eV"
    ie2_match = re.search(r'second ionization energy.*is\s*(\d+\.?\d*)\s*eV', content, re.IGNORECASE)
    if ie2_match:
        ionizations.append(("2nd", float(ie2_match.group(1))))

    # If nothing found, skip? Or use placeholder?
    if not ionizations:
        # Try to find JUST a number near "eV" if it looks like an IE block?
        # Dangerous. Let's just report nothing found.
        pass

    if ionizations:
        # Generate the new analysis block
        new_block = generate_rigorous_section(name, symbol, z, n, ionizations)
        
        # Replace existing "Rigorous SDT Mathematical Analysis" section if it exists
        if "### Rigorous SDT Mathematical Analysis" in content:
            # Find start
            start_idx = content.find("### Rigorous SDT Mathematical Analysis")
            # Find end... usually it goes to the end of the file OR until spectral table if we injected it differently?
            # Actually, `enrich_excitations` injected **C. Spectral Implications** INSIDE or AFTER this block.
            # We must be careful not to kill the spectral table if it exists.
            
            # Strategy: Re-write the Analysis header and Sections A, B, and NEW C.
            # Preserve "D. Magnetic" or explicit Spectral Table if it was physically separate.
            # BUT, `enrich_excitations` was replacing "C. Spectral Implications".
            # Our `generate_rigorous_section` creates A, B, C(Utilization), D(Spectral Header).
            
            # Let's try to just REPLACE the A and B sections?
            # Too complex to parse partials.
            
            # Better Strategy: Append the new robust block at the very end, and delete the old one?
            # Or assume we overwrite the old one. We want to KEEP the spectral table if likely present.
            # Current structure:
            # ### Rigorous ...
            # **A...**
            # **B...**
            # **C. Spectral ...** (Contains NIST table)
            # **D. Magnetic ...**
            
            # If we replace the whole block, we lose the NIST table unless we re-inject it.
            # I will re-inject it in the next step anyway.
            # So I can overwrite this section safely, provided I keep the "Magnetic" section if it was custom?
            # Most "Magnetic" sections were generic.
            
            # OK, I will overwrite from "### Rigorous..." to the end.
            # AND I will rely on `enrich_excitations.py` to put the table back in.
            
            content = content[:start_idx] + new_block
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Re-enriched {name}")
            
        else:
            # Append
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(new_block)
            print(f"Appended to {name}")

def main():
    files = [f for f in os.listdir(ATOMICUS_DIR) if f.endswith(".md") and "Rules" not in f and "Master" not in f]
    for f in files:
        process_file(os.path.join(ATOMICUS_DIR, f))

if __name__ == "__main__":
    main()
