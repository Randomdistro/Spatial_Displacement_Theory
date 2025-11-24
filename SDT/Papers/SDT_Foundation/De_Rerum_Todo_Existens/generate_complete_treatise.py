import os

# Define the base directory for source files
source_dir = r"SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations"
output_dir = r"SDT/Papers/SDT_Foundation/De_Rerum_Todo_Existens"
output_file = os.path.join(output_dir, "DE_RERUM_TODO_EXISTENS_COMPLETE.md")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define the structure: Title -> List of Source Files
# I am mapping the "Books" to the actual Phase files that contain the content.
structure = {
    "Volume I: Foundations of Spatial Displacement": [
        ("Book 1: The Nature of Reality (Composition & Ontology)", [
            "Phase_0_Foundational_Principles.md",
            "Phase_20_Spation_Planck_Scales_Global_Stiffness_and_Force_Hierarchy.md"
        ]),
        ("Book 2: The Axiomatic Framework", [
            "atomica sentis.md",
            "Phase_25_Pressure_Differentials_Across_Scales.md",
            "Phase_26_Pressure_Mediated_Forces_and_Scale_Dependent_Interactions.md"
        ]),
    ],
    "Volume II: Atomic Physics": [
        ("Book 3: The Coulomb Mechanism", [
            "Phase_1_Coulomb_Force.md",
            "Phase_27A_Foundation_and_Single_Electron_Systems.md"
        ]),
        ("Book 4: Spectral Lines and Wave Mechanics", [
            "Phase_2_Rydberg_Spectrum_from_Helical_Standing_Waves.md",
            "Phase_3_Fine_structure.md",
            "Phase_4_Lamb_Shift.md",
            "Phase_27C_Spectral_Calibration_and_k_Values.md"
        ]),
        ("Book 5: Complex Atomic Systems", [
            "Phase_5_Hyperfine_Splitting_from_Central_Pressure_Overlap.md",
            "Phase_6_Multi_Electron_Atoms_from_Occlusion_Geometry.md",
            "Phase_23_Atomic_Structure_from_Vortex_Geometry.md",
            "Phase_27B_Multi_Electron_Occlusion_Mechanics.md"
        ]),
    ],
    "Volume III: Thermodynamics and Statistical Mechanics": [
        ("Book 6: The Origin of Heat and Entropy", [
            "Phase_7_Thermodynamics_from_Spation_Contact_Mechanics.md",
            "Phase_14_Thermodynamic_and_Radiative_Transitions.md"
        ]),
    ],
    "Volume IV: Electromagnetism": [
        ("Book 7: Electric and Magnetic Fields", [
            "Phase_11_Electricity_from_Spation_Pressure_Deformation.md",
            "Phase_8_Hyperfine_Structure_from_Magnetic_Moment_Overlap.md",
            "Phase_9_Oblateness-Spin Correlation.md"
        ]),
        ("Book 8: Electromagnetic Propagation", [
            "Phase_10_Electromagnetic_Mechanisms_and_Effects.md",
            "Phase_12_Electromagnetic_Mechanisms_and_Effects.md"
        ]),
    ],
    "Volume V: Nuclear Physics": [
        ("Book 9: Nuclear Structure and Decay", [
            "Phase_17_Toroidal_Structures_and_Pressure_Differentials_at_Femtoscale.md",
            "Phase_18_Alpha_Particles_and_Beta_Decay.md",
            "Phase_19_The_Role_of_the_Vortex_and_the_Effect_of_the_Helical_Wake.md"
        ]),
    ],
    "Volume VI: Gravitation and Orbital Dynamics": [
        ("Book 10: The Mechanism of Gravity", [
            "Phase_15_Gravitation_from_Spation_Pressure_Gradients.md",
            "Phase_16_Universal_c-Boundary_Geometry.md"
        ]),
        ("Book 11: Planetary and Stellar Systems", [
            "Phase_22_Exoplanetary_Systems_Deriving_Orbital_Dynamics_from_Stellar_Compactness_and_Luminosity.md",
            "Phase_22_Validation_10_Star_Systems.md",
            "Phase_22_Appendix_k_Value_Derivation_from_Spectral_Data.md"
        ]),
    ],
    "Volume VII: Cosmology and Galactic Dynamics": [
        ("Book 12: Galactic Rotation and Dark Matter Replacement", [
            "Phase_24_Galactic_Rotation_Curves_Disk_Eclipse_Saturation.md",
            "Phase_25_Flat_Galactic_Rotation_Curves_from_Disk_Eclipse_Saturation.md",
            "Phase_Y_Galactic_Dynamics_Rotation_Curves_from_Displacement_and_Occlusion.md"
        ]),
        ("Book 13: The Large Scale Structure", [
            "Phase_21_Screening_Factors_and_the_10^-9_vs_10^-123_Hierarchy.md"
        ]),
    ],
    "Volume VIII: Advanced Topics and Validation": [
        ("Book 14: Computational Validation", [
            "Phase_27D_Extended_Elements_and_Advanced_Investigations.md"
        ]),
    ]
}

header = """# De Rerum Todo Existens
## The Complete Canonical Principia of Spatial Displacement Theory

**Version:** Technical Reference 1.0
**Format:** Unified Theoretical Corpus
**Scope:** Foundations, Atomic Physics, Thermodynamics, Electromagnetism, Gravitation, Cosmology, Unification, Validation

---

"""

def read_file_content(filename):
    # Try multiple locations
    paths_to_try = [
        os.path.join(source_dir, filename),
        os.path.join(r"SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations", filename), # Redundant but safe
        os.path.join(r"SDT/Papers/SDT_Foundation", filename),
        os.path.join(r"SDT", filename)
    ]
    
    for path in paths_to_try:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                return f"Error reading {filename}: {str(e)}"
    
    return f"MISSING FILE: {filename}\n"

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write(header)
    
    for volume, books in structure.items():
        outfile.write(f"# {volume}\n\n")
        
        for book_title, files in books:
            outfile.write(f"## {book_title}\n\n")
            outfile.write("---\n\n")
            
            for filename in files:
                outfile.write(f"### Source: {filename}\n\n")
                content = read_file_content(filename)
                outfile.write(content)
                outfile.write("\n\n---\n\n")

print(f"Compilation complete: {output_file}")


