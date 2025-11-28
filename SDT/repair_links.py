import os
import re

# Map of old filenames to new relative paths (from Part_I root)
# Note: The keys are the old filenames (e.g. "Phase_1_Coulomb_Force.md")
# The values are the new paths relative to Part_I root (e.g. "01_Atomic_Physics/Coulomb_Force.md")

FILE_MAP = {
    "Phase_0_Foundational_Principles.md": "00_Foundations/Foundational_Principles.md",
    "Phase_1_Core_Engine_Mathematical_Proof.md": "00_Foundations/Core_Engine_Mathematical_Proof.md",
    "Phase_5_Unified_Physics_from_Master_Equation.md": "00_Foundations/Unified_Physics_from_Master_Equation.md",
    "atomica sentis.md": "00_Foundations/Atomica_Sentis.md",
    "Phase_SDT_Navier_Field_Theory.md": "00_Foundations/SDT_Navier_Field_Theory.md",
    "Phase_0_Foundational_Principles_OLD.md": "00_Foundations/Foundational_Principles_OLD.md",
    "PRECISION_AUDIT.md": "00_Foundations/PRECISION_AUDIT.md",

    "Phase_1_Coulomb_Force.md": "01_Atomic_Physics/Coulomb_Force.md",
    "Phase_2_Rydberg_Spectrum_from_Helical_Standing_Waves.md": "01_Atomic_Physics/Rydberg_Spectrum_from_Helical_Standing_Waves.md",
    "Phase_3_Fine_Structure.md": "01_Atomic_Physics/Fine_Structure.md",
    "Phase_6_Multi_Electron_Atoms_from_Occlusion_Geometry.md": "01_Atomic_Physics/Multi_Electron_Atoms_from_Occlusion_Geometry.md",
    "Phase_8_Hyperfine_Structure_from_Magnetic_Moment_Overlap.md": "01_Atomic_Physics/Hyperfine_Structure_from_Magnetic_Moment_Overlap.md",

    "Phase_4_Magnetic_Moments_from_Toroidal_Circulation.md": "02_Electromagnetism/Magnetic_Moments_from_Toroidal_Circulation.md",
    "Phase_10_Electromagnetic_Mechanisms_and_Effects.md": "02_Electromagnetism/Electromagnetic_Mechanisms_and_Effects_Part1.md",
    "Phase_11_Electricity_from_Spation_Pressure_Deformation.md": "02_Electromagnetism/Electricity_from_Spation_Pressure_Deformation.md",
    "Phase_12_Electromagnetic_Mechanisms_and_Effects.md": "02_Electromagnetism/Electromagnetic_Mechanisms_and_Effects_Part2.md",

    "Phase_9_Oblateness_Spin_Correlation.md": "03_Gravitation_and_Cosmology/Oblateness_Spin_Correlation.md",
    "Phase_15_Gravitation_from_Spation_Pressure_Gradients.md": "03_Gravitation_and_Cosmology/Gravitation_from_Spation_Pressure_Gradients.md",
    "Phase_16_Stellar_Structure_from_Pressure_Geometry.md": "03_Gravitation_and_Cosmology/Stellar_Structure_from_Pressure_Geometry.md",
    "Phase_24_Galactic_Rotation_from_Disk_Occlusion.md": "03_Gravitation_and_Cosmology/Galactic_Rotation_from_Disk_Occlusion.md",
    "Phase_25_Cosmological_Structure_from_Pressure_Topology.md": "03_Gravitation_and_Cosmology/Cosmological_Structure_from_Pressure_Topology.md",

    "Phase_7_Thermodynamics_from_Spation_Contact_Mechanics.md": "04_Thermodynamics/Thermodynamics_from_Spation_Contact_Mechanics.md",
    "Phase_14_Thermodynamic_and_Radiative_Transitions.md": "04_Thermodynamics/Thermodynamic_and_Radiative_Transitions.md",
    "Phase_21_Phase_Transitions_from_Pressure_Stability.md": "04_Thermodynamics/Phase_Transitions_from_Pressure_Stability.md",
    "Phase_22_Mechanical_Properties_from_Pressure_Response.md": "04_Thermodynamics/Mechanical_Properties_from_Pressure_Response.md",
    "Phase_23_Crystal_Defects_from_Pressure_Distortions.md": "04_Thermodynamics/Crystal_Defects_from_Pressure_Distortions.md",

    "Phase_2_Bonding_Geometry_Mathematical_Proof.md": "05_Chemistry/Bonding_Geometry_Mathematical_Proof.md",
    "Phase_3_Properties_Reactions_Mathematical_Proof.md": "05_Chemistry/Properties_Reactions_Mathematical_Proof.md",
    "Phase_4_Compound_Designer_Mathematical_Proof.md": "05_Chemistry/Compound_Designer_Mathematical_Proof.md",
    "Phase_5_Commercial_Features_Mathematical_Proof.md": "05_Chemistry/Commercial_Features_Mathematical_Proof.md",
    "Phase_17_Chemical_Bonding_from_Multi_Atom_Occlusion.md": "05_Chemistry/Chemical_Bonding_from_Multi_Atom_Occlusion.md",
    "Phase_18_Van_der_Waals_from_Pressure_Fluctuations.md": "05_Chemistry/Van_der_Waals_from_Pressure_Fluctuations.md",
    "Phase_19_Reaction_Kinetics_from_Pressure_Barriers.md": "05_Chemistry/Reaction_Kinetics_from_Pressure_Barriers.md",
    "Phase_20_Crystal_Structures_from_Pressure_Equilibrium.md": "05_Chemistry/Crystal_Structures_from_Pressure_Equilibrium.md",
    "Phase_27_Protein_Folding_from_Pressure_Optimization.md": "05_Chemistry/Protein_Folding_from_Pressure_Optimization.md",
    "Phase_28_Enzyme_Catalysis_from_Pressure_Stabilization.md": "05_Chemistry/Enzyme_Catalysis_from_Pressure_Stabilization.md",
    "CHEMISTRY_FRAMEWORK_COMPLETE.md": "05_Chemistry/CHEMISTRY_FRAMEWORK_COMPLETE.md",
    "CHEMISTRY_FRAMEWORK_TEST_REPORT.md": "05_Chemistry/CHEMISTRY_FRAMEWORK_TEST_REPORT.md",

    "Phase_19_Nuclear_Packing_Master_Equation.md": "06_Nuclear_Physics/Nuclear_Packing_Master_Equation.md"
}

# Add Phase_Chemistry mappings
CHEM_PHASES = [
    "Acid_Base_from_Proton_Pressure_Transfer", "Atomic_Properties_from_Pressure_Fields",
    "Chemical_Equilibrium_from_Pressure_Balance", "Coordination_Complexes_from_Ligand_Occlusion",
    "Covalent_Bonding_from_Shared_Occlusion", "Electrochemistry_from_Pressure_Gradients",
    "Intermolecular_Forces_from_Pressure_Fields", "Ionic_Bonding_from_Pressure_Gradients",
    "Lanthanides_Actinides_from_f_Orbital_Occlusion", "Main_Group_Elements_from_Nuclear_Packing",
    "Metallic_Bonding_from_Conduction_Occlusion", "Organic_Alkanes_from_Hydrocarbon_Occlusion",
    "Organic_Alkenes_Alkynes_from_Multiple_Occlusion", "Organic_Aromatics_from_Delocalized_Occlusion",
    "Organic_Functional_Groups_from_Pressure_Geometry", "Organic_Reactions_from_Pressure_Reconfiguration",
    "Organic_Stereochemistry_from_Pressure_Chirality", "Periodic_Table_from_Nuclear_Packing",
    "Redox_from_Electron_Pressure_Transfer", "Solutions_from_Pressure_Dissolution",
    "Thermodynamics_from_Pressure_Energy", "Transition_Metals_from_d_Orbital_Occlusion"
]

for p in CHEM_PHASES:
    FILE_MAP[f"Phase_Chemistry_{p}.md"] = f"05_Chemistry/{p}.md"

ROOT_DIR = r"c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT\Papers\SDT_Foundation\Part_I_Axioms_and_Core_Equations"

def get_relative_path(source_file_path, target_file_path):
    # source_file_path: absolute path of the file containing the link
    # target_file_path: absolute path of the file being linked to
    return os.path.relpath(target_file_path, os.path.dirname(source_file_path)).replace("\\", "/")

def repair_links():
    print("Starting Link Repair...")
    
    # Walk through all files in the directory
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if not file.endswith(".md"):
                continue
                
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Replace links
            for old_name, new_rel_path in FILE_MAP.items():
                # Construct the absolute path of the target
                target_abs_path = os.path.join(ROOT_DIR, new_rel_path)
                
                # Calculate the relative path from the current file to the target
                # This is what the link SHOULD be
                correct_link = get_relative_path(file_path, target_abs_path)
                
                # Regex to find links to the old filename
                # Matches [Link Text](Phase_X_Old_Name.md) or just Phase_X_Old_Name.md
                # We need to be careful not to break existing correct links if any
                
                # Simple replace for now: look for the old filename in link structures
                # Case 1: (Phase_...md)
                content = content.replace(f"({old_name})", f"({correct_link})")
                
                # Case 2: [Phase_...md] (unlikely but possible)
                # content = content.replace(f"[{old_name}]", f"[{correct_link}]")
                
                # Case 3: Link to file in same dir that was moved (e.g. just "Phase_...md")
                # If the file was moved to a different folder, simple replacement might not work 
                # if the link didn't have a path.
                # But since we are restructuring, ALL links to these files need to be updated 
                # to the new relative path.
                
                # However, simple string replacement is dangerous if we don't match the context.
                # Let's assume standard markdown links: ](filename)
                
                content = content.replace(f"]({old_name})", f"]({correct_link})")
                
                # Also handle "See Phase X" text references? 
                # User asked to "remove numbers from phase titles only". 
                # Changing text references might be out of scope or risky.
                # I will stick to fixing the HYPERLINKS.

            if content != original_content:
                print(f"Updating links in: {file}")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

    print("Link Repair Complete.")

if __name__ == "__main__":
    repair_links()
