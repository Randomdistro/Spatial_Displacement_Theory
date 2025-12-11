import os
import re

ATOMICUS_DIR = r'c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\ATOMICUS'
OUTPUT_FILE = r'c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\ATOMICUS\SDT_Master_Geometric_Table.md'

def main():
    files = [f for f in os.listdir(ATOMICUS_DIR) if f.endswith(".md") and "Rules" not in f and "Master" not in f]
    
    entries = []
    
    for filename in files:
        filepath = os.path.join(ATOMICUS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract Z from filename
        # On the Nature of [Name] [Symbol] [Z] [N].md
        meta = re.match(r'On the Nature of ([A-Z][a-z]+) ([A-Z][a-z]?) (\d+)', filename)
        if not meta: continue
        
        name = meta.group(1)
        symbol = meta.group(2)
        z = int(meta.group(3))
        
        # Extract k-factor
        # Pattern: k = c/v = 172.28
        k_match = re.search(r'k\s*=\s*c/v\s*=\s*(\d+\.?\d*)', content)
        k = k_match.group(1) if k_match else "-"
        
        # Extract v/c
        # Pattern: Relativistic Ratio ($v/c$): 0.00580
        # or v/c = ...
        vc_match = re.search(r'v/c\)?\s*[:=]\s*(\d+\.?\d*)', content)
        if not vc_match:
             vc_match = re.search(r'Ratio to c.*?(\d+\.\d+)', content, re.DOTALL)
        vc = vc_match.group(1) if vc_match else "-"
        
        # Extract IE
        ie_match = re.search(r'(?:Observation:|Energy:)\s*E_?\{?i1\}?\s*=\s*(\d+\.?\d*)', content)
        if not ie_match:
            ie_match = re.search(r'(\d+\.?\d*)\s*eV', content) # Loose fallback for "Observed Ionization Energy: 8.6 eV" pattern
            
        # Better IE search: look for "Observed Ionization Energy: X eV" specifically
        ie_strict = re.search(r'Observed Ionization Energy:\s*(\d+\.?\d*)', content) 
        ie = ie_strict.group(1) if ie_strict else "-"
        
        entries.append({
            'z': z,
            'name': name,
            'symbol': symbol,
            'k': k,
            'vc': vc,
            'ie': ie
        })
        
    # Sort by Z
    entries.sort(key=lambda x: x['z'])
    
    # Generate Markdown Table
    md = "# SDT Master Geometric Table\n\n"
    md += "A consolidated reference of the kinematic and geometric properties of the elements as derived from Spatial Displacement Theory.\n\n"
    md += "| Z | Element | Symbol | Ionization Energy (eV) | Velocity Ratio (v/c) | Geometric k-factor |\n"
    md += "|:--|:--------|:-------|:-----------------------|:---------------------|:-------------------|\n"
    
    for e in entries:
        md += f"| {e['z']} | {e['name']} | {e['symbol']} | {e['ie']} | {e['vc']} | {e['k']} |\n"
        
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"Generated Master Table with {len(entries)} entries.")

if __name__ == "__main__":
    main()
