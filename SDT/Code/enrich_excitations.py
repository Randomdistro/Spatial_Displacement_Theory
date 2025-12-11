import os
import re

NIST_FILE = r'c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\data\atomic_spectra_nist.csv'
ATOMICUS_DIR = r'c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\ATOMICUS'

GEO_MAP = {
    's': "Spherical",
    'p': "Toroidal",
    'd': "Lobed",
    'f': "Hyper-Geo"
}

def parse_nist_data():
    data_by_z = {}
    with open(NIST_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('```'): continue
        parts = [p.strip() for p in line.split(',')]
        
        entry = None
        z = None
        if len(parts) > 5:
            if parts[2].isdigit(): 
                z = int(parts[2])
                entry = {'trans': parts[3], 'wave': parts[4]}
            elif parts[1].isdigit(): 
                z = int(parts[1])
                entry = {'trans': parts[2], 'wave': parts[3]}
        
        if z and entry:
            if z not in data_by_z: data_by_z[z] = []
            data_by_z[z].append(entry)
    return data_by_z

def analyze_transition_utilization(trans, wave_str):
    narrative = "Standard Emission"
    utilization = "Spectroscopic calibration"
    
    # Geometric parsing
    found = []
    for char in ['s', 'p', 'd', 'f']:
        if char in trans.lower(): found.append(char)
    
    start_geo = GEO_MAP.get(found[0], "Unknown") if len(found)>0 else "Complex"
    end_geo = GEO_MAP.get(found[1], "Unknown") if len(found)>1 else start_geo
    
    narrative = f"{start_geo} -> {end_geo} Shift"
    
    # Utilization Logic
    try:
        wave = float(wave_str)
        if wave < 300:
            utilization = "**UV Lithography**: High-energy short-wavelength output."
        elif 400 < wave < 700:
            utilization = "**Visible Beacon**: Optical signaling and photonics."
        elif wave > 700:
            utilization = "**IR Thermal Source**: Heating and localized energy deposition."
        
        # Specific element overrides could go here
    except:
        pass
        
    return narrative, utilization

def generate_full_table(z, entries):
    text = "\n**C. Spectral Implications & Utilization**\n\n"
    text += "The following table lists **every** observed excitation level available in our dataset, mapped to its SDT geometric interpretation and potential technological utilization.\n\n"
    text += "| Transition | Wavelength (nm) | SDT Geometry | Utilization Potential |\n"
    text += "|:-----------|:----------------|:-------------|:----------------------|\n"
    
    seen = set()
    
    for e in entries:
        key = f"{e['trans']}-{e['wave']}"
        if key in seen: continue
        seen.add(key)
        
        geo, util = analyze_transition_utilization(e['trans'], e['wave'])
        text += f"| {e['trans']} | {e['wave']} | {geo} | {util} |\n"
        
    return text

def process_files():
    data = parse_nist_data()
    files = [f for f in os.listdir(ATOMICUS_DIR) if f.endswith(".md") and "Rules" not in f]
    
    for filename in files:
        match = re.match(r'On the Nature of ([A-Z][a-z]+) ([A-Z][a-z]?) (\d+)', filename)
        if match:
            z = int(match.group(3))
            if z in data:
                filepath = os.path.join(ATOMICUS_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_block = generate_full_table(z, data[z])
                
                # Replace logic
                # Look for "**D. Spectral Implications" (from enrich_atomicus) 
                # OR "**C. Spectral Implications" (from old enrich_excitations)
                
                # Since we run this AFTER enrich_atomicus, the file will likely have:
                # **C. SDT Utilization...**
                # **D. Spectral Implications**
                # (See Table Below)
                
                # We want to replace "**D. Spectral Implications**\n(See Table Below)" with our big table.
                
                if "**D. Spectral Implications**" in content:
                    pattern = r'\*\*D\. Spectral Implications\*\*.*'
                    # Replace until end of file or something?
                    # enrich_atomicus put D at the end.
                    content = re.sub(pattern, new_block, content, flags=re.DOTALL)
                elif "**C. Spectral Implications**" in content:
                     # Old format fallback
                      pattern = r'\*\*C\. Spectral Implications\*\*.*?(\n\*\*|$)'
                      # Tricky to regex replace correctly without deleting next section if it exists.
                      # Just appending is safer if we can't find clear bounds, 
                      # but we want to avoid duplicates.
                      # Let's try to just replace the whole file content if we matched D.
                      pass
                      
                # Note: `enrich_atomicus` writes D at the END.
                # So replacing D... to end is safe.
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Injected Full Table into {filename}")

if __name__ == "__main__":
    process_files()
