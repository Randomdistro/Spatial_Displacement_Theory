import re
import os

SOURCE_FILE = r'c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\data\atomica_sentis.md'
OUTPUT_DIR = r'c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\ATOMICUS'

def main():
    if not os.path.exists(OUTPUT_DIR):
        print(f"Creating directory: {OUTPUT_DIR}")
        os.makedirs(OUTPUT_DIR)

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extract Rules
    rules_match = re.search(r'(## The Foundational Rules of the Game.*?)(?=10\.2\.|On the Nature of)', content, re.DOTALL)
    if rules_match:
        rules_content = rules_match.group(1).strip()
        rules_filename = "On the Nature of Atomicus Rules.md"
        write_file(rules_filename, rules_content)
        print(f"Created: {rules_filename}")
    else:
        print("Warning: Could not find 'Foundational Rules' section.")

    # 2. Split by "On the Nature of"
    # The file has sections like "On the Nature of [Name] ([Symbol]): ..."
    # and "On the Nature of the Fundamental Triplet..."
    
    # We use a regex to split, but keep the delimiter
    # The pattern matches "On the Nature of " followed by anything until a newline
    sections = re.split(r'(On the Nature of .+)', content)
    
    # sections[0] is intro before first "On the Nature of"
    # sections[1] is title 1, sections[2] is content 1, sections[3] is title 2, etc.
    
    current_title = ""
    for i in range(1, len(sections), 2):
        title_line = sections[i].strip()
        body = sections[i+1]
        full_text = title_line + "\n" + body
        
        if "Fundamental Triplet" in title_line:
            process_triplet(full_text)
        else:
            process_standard_atom(title_line, full_text)

def write_file(filename, content):
    # Remove invalid characters
    clean_filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    path = os.path.join(OUTPUT_DIR, clean_filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_triplet(text):
    # This section contains Hydrogen, Deuterium, Helium
    # We need to manually split them.
    # Pattern: "2. Hydrogen", "3. Deuterium", "4. Helium"
    
    # Hydrogen
    h_match = re.search(r'(2\. Hydrogen .*?)(?=3\. Deuterium)', text, re.DOTALL)
    if h_match:
        content = h_match.group(1).strip()
        # Hydrogen is 1H, Z=1, N=0 usually
        # Let's verify standard H
        z = 1
        n = 0
        name = "Hydrogen"
        symbol = "H"
        filename = f"On the Nature of {name} {symbol} {z} {n}.md"
        write_file(filename, content)
        print(f"Created: {filename}")

    # Deuterium
    d_match = re.search(r'(3\. Deuterium .*?)(?=4\. Helium)', text, re.DOTALL)
    if d_match:
        content = d_match.group(1).strip()
        # Deuterium is 2H, Z=1, N=1
        z = 1
        n = 1
        name = "Deuterium"
        symbol = "H" # Or D? User asked for "Atom name chem symbol". Usually D or H. Let's use H for consistency with PT, or D if specifically distinct. "Deuterium (²H)"
        # Let's check text
        if "(²H)" in content:
            symbol = "H"
        filename = f"On the Nature of {name} {symbol} {z} {n}.md"
        write_file(filename, content)
        print(f"Created: {filename}")

    # Helium
    he_match = re.search(r'(4\. Helium .*?)(?=5\. Conclusion|4\.6\.)', text, re.DOTALL)
    if he_match:
        content = he_match.group(1).strip()
        # Helium 4 is standard
        z = 2
        n = 2
        name = "Helium"
        symbol = "He"
        filename = f"On the Nature of {name} {symbol} {z} {n}.md"
        write_file(filename, content)
        print(f"Created: {filename}")

def process_standard_atom(title_line, full_text):
    # Format: On the Nature of Lithium (³Li): ...
    # Regex to extract Name and Symbol from title
    # Typical title: "On the Nature of Lithium (³Li): The Genesis of Reactivity"
    
    # Regex for Name and Symbol
    # Matches: Name followed by space and parenthesis with optional Isotope number and Symbol
    match = re.search(r'On the Nature of ([A-Z][a-z]+) \([0-9\u00B2\u00B3\u2070-\u2079]*([A-Z][a-z]?)\)', title_line)
    
    name = "Unknown"
    symbol = "X"
    
    if match:
        name = match.group(1)
        symbol = match.group(2)
    else:
        # Retry looser extraction
        # "On the Nature of Gold (79Au)"
        match = re.search(r'On the Nature of ([A-Z][a-z]+) .*?([A-Z][a-z]*)\)', title_line)
        if match:
            name = match.group(1)
            symbol = match.group(2) # potentially just symbol
    
    # Extract Z and N from content
    # Look for "Z=(\d+)" and "N=(\d+)"
    z_match = re.search(r'Z=(\d+)', full_text)
    n_match = re.search(r'N=(\d+)', full_text)
    
    z = z_match.group(1) if z_match else "?"
    n = n_match.group(1) if n_match else "?"
    
    # Sometimes N is not explicitly N=, but "Z=X, N=Y" or "X protons, Y neutrons"
    if n == "?":
       n_match = re.search(r'(\d+) neutrons', full_text) 
       if n_match:
           n = n_match.group(1)
           
    if z == "?":
        # Check for title Z usually not in title but "79Au"
        pass

    if name != "Unknown":
        filename = f"On the Nature of {name} {symbol} {z} {n}.md"
        write_file(filename, full_text)
        print(f"Created: {filename}")
    else:
        print(f"Skipping unrecognized section: {title_line[:50]}...")

if __name__ == "__main__":
    main()
