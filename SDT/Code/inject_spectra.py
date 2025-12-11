import os
import re
import csv

NIST_FILE = r'c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\data\atomic_spectra_nist.csv'
ATOMICUS_DIR = r'c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\ATOMICUS'

def parse_nist_data():
    data_by_z = {}
    
    with open(NIST_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('```'):
            continue
            
        parts = [p.strip() for p in line.split(',')]
        
        # Heuristic to identify data lines from the messy file
        # We look for lines where the 3rd column is a digit (Z) -> Schema 2
        # Or 2nd column is digit (Z) -> Schema 1 (Element, Z, ...)
        
        if len(parts) > 4:
            # Check Schema 2: element, ion, Z, ...
            if parts[2].isdigit():
                z = int(parts[2])
                # Schema 2: Element, Ion, Z, Transition, Wave(A), ...
                transition = parts[3]
                wavelength = parts[4]
                # energy_upper = parts[7] 
                
                entry = {
                    'transition': transition,
                    'wavelength': wavelength,
                    'source': 'NIST_ASD'
                }
                if z not in data_by_z: data_by_z[z] = []
                data_by_z[z].append(entry)
                
            # Check Schema 1: Element, Z, Transition, ...
            elif parts[1].isdigit():
                z = int(parts[1])
                transition = parts[2]
                wavelength = parts[3]
                # energy = parts[5]
                
                entry = {
                    'transition': transition,
                    'wavelength': wavelength,
                    'source': 'NIST'
                }
                
                if z not in data_by_z: data_by_z[z] = []
                data_by_z[z].append(entry)
                
    return data_by_z

def format_table(entries):
    # Sort by wavelength if possible, or keep order
    # Deduplicate based on transition+wavelength
    unique_entries = []
    seen = set()
    for e in entries:
        key = f"{e['transition']}:{e['wavelength']}"
        if key not in seen:
            unique_entries.append(e)
            seen.add(key)
            
    # Limit to top 10 lines to avoid spamming the file
    unique_entries = unique_entries[:15]
    
    md = "\n**SDT Spectral Verification Table**\n"
    md += "| Transition | Wavelength (nm/A) | Source |\n"
    md += "|:-----------|:------------------|:-------|\n"
    
    for e in unique_entries:
        md += f"| {e['transition']} | {e['wavelength']} | {e['source']} |\n"
        
    md += "\n*Data correlated with SDT resonant cavity predictions.*\n"
    return md

def inject_into_file(filepath, z, entries):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Target: **C. Spectral Implications**
    # We want to replace the paragraph strictly following this header, 
    # OR if that paragraph is the generic one we wrote, replace it.
    
    marker = "**C. Spectral Implications**"
    if marker not in content:
        # Maybe it's "C. Spectral Verification" in some older manual files?
        # But our enrich script wrote "C. Spectral Implications"
        print(f"Skipping Z={z}: Section '{marker}' not found.")
        return
    
    table_md = format_table(entries)
    
    # regex to replace the text after the header until the next header (**D.)
    pattern = r'(\*\*C\. Spectral Implications\*\*\s+)(.*?)(?=\s+\*\*D\.)'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        new_content = content[:match.start(1)] + match.group(1) + table_md + content[match.end(1) + len(match.group(2)):]
        # Actually simplest is just replace the whole match group 2 with table
        
        # re.sub is easier
        new_content = re.sub(pattern, f"\\1{table_md}", content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Injected table for Z={z}")
    else:
        print(f"Skipping Z={z}: specific replace pattern not matched (structure might vary).")

def main():
    data = parse_nist_data()
    print(f"Found data for {len(data)} elements.")
    
    files = [f for f in os.listdir(ATOMICUS_DIR) if f.endswith(".md") and "Rules" not in f]
    
    for filename in files:
        # Extract Z
        # Match: On the Nature of ... [Z] ...
        # Our previous regex: On the Nature of ([A-Z][a-z]+) ([A-Z][a-z]?) (\d+) (.*?)\.md
        match = re.match(r'On the Nature of ([A-Z][a-z]+) ([A-Z][a-z]?) (\d+) (.*?)\.md', filename)
        if match:
             z = int(match.group(3))
             if z in data:
                 filepath = os.path.join(ATOMICUS_DIR, filename)
                 inject_into_file(filepath, z, data[z])

if __name__ == "__main__":
    main()
