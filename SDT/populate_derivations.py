import os
import shutil

ROOT_DIR = r"c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\Papers\SDT_Foundation\Part_I_Axioms_and_Core_Equations"
TEMPLATE_PATH = r"c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\Derivation_Template.md"

def populate_derivations():
    print("Populating missing Derivation files...")
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # We are looking for the "leaf" folders that contain the Axiom.md files
        # These folders were created in the previous steps.
        
        # Heuristic: If the folder contains a .md file but NO "Derivation.md", add it.
        has_md = any(f.endswith(".md") for f in files)
        has_derivation = "Derivation.md" in files
        
        if has_md and not has_derivation:
            # Check if this is a content folder (not a category folder like 01_Atomic_Physics)
            # Category folders might have .md files if I missed moving some, but generally 
            # the content folders are the ones we want.
            # Actually, my previous script moved ALL .md files into subfolders.
            # So any folder with a .md file is likely a topic folder.
            
            target_path = os.path.join(root, "Derivation.md")
            print(f"Creating {target_path}")
            shutil.copy(TEMPLATE_PATH, target_path)

if __name__ == "__main__":
    populate_derivations()
