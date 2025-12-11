import os

# Define the base directory for source files
base_dir = r"c:\Users\Jimmi\OneDrive\Documents\Spatial_Displacement_Theory\SDT"
source_dir = os.path.join(base_dir, "Papers", "SDT_Foundation", "Part_I_Axioms_and_Core_Equations")
output_dir = os.path.join(base_dir, "Papers", "SDT_Foundation", "De_Rerum_Todo_Existens")
output_file = os.path.join(output_dir, "DE_RERUM_TODO_EXISTENS_COMPLETE.md")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define the structure using CURRENT Part_I organized files
structure = {
    "Volume I: Foundations of Spatial Displacement": [
        ("Book 1: The Nature of Reality (Composition & Ontology)", [
            "00_Foundations/Foundational_Principles/Foundational_Principles.md",
            "00_Foundations/SDT_Navier_Field_Theory/SDT_Navier_Field_Theory.md"
        ]),
        ("Book 2: The Axiomatic Framework", [
            "00_Foundations/Core_Engine_Mathematical_Proof/Core_Engine_Mathematical_Proof.md",
            "00_Foundations/Unified_Physics_from_Master_Equation/Unified_Physics_from_Master_Equation.md"
        ]),
    ],
    "Volume II: Atomic Physics": [
        ("Book 3: The Coulomb Mechanism", [
            "01_Atomic_Physics/Coulomb_Force/Coulomb_Force.md",
            "01_Atomic_Physics/Universal_Spiral_Model/Universal_Spiral_Model.md"
        ]),
        ("Book 4: Spectral Lines and Wave Mechanics", [
            "01_Atomic_Physics/Rydberg_Spectrum_from_Helical_Standing_Waves/Rydberg_Spectrum_from_Helical_Standing_Waves.md",
            "01_Atomic_Physics/Fine_Structure/Fine_Structure.md"
        ]),
        ("Book 5: Complex Atomic Systems", [
            "01_Atomic_Physics/Hyperfine_Structure_from_Magnetic_Moment_Overlap/Hyperfine_Structure_from_Magnetic_Moment_Overlap.md",
            "01_Atomic_Physics/Multi_Electron_Atoms_from_Occlusion_Geometry/Multi_Electron_Atoms_from_Occlusion_Geometry.md"
        ]),
    ],
    "Volume III: Thermodynamics and Statistical Mechanics": [
        ("Book 6: The Origin of Heat and Entropy", [
            "04_Thermodynamics/Thermodynamics_from_Spation_Contact_Mechanics/Thermodynamics_from_Spation_Contact_Mechanics.md",
            "04_Thermodynamics/Phase_Transitions_from_Pressure_Stability/Phase_Transitions_from_Pressure_Stability.md"
        ]),
    ],
    "Volume IV: Electromagnetism": [
        ("Book 7: Electric and Magnetic Fields", [
            "02_Electromagnetism/Electricity_from_Spation_Pressure_Deformation/Electricity_from_Spation_Pressure_Deformation.md",
            "02_Electromagnetism/Magnetic_Moments_from_Toroidal_Circulation/Magnetic_Moments_from_Toroidal_Circulation.md"
        ]),
        ("Book 8: Electromagnetic Propagation", [
            "02_Electromagnetism/Electromagnetic_Mechanisms_and_Effects_Part1/Electromagnetic_Mechanisms_and_Effects_Part1.md",
            "02_Electromagnetism/Electromagnetic_Mechanisms_and_Effects_Part2/Electromagnetic_Mechanisms_and_Effects_Part2.md"
        ]),
    ],
    "Volume V: Nuclear Physics": [
        ("Book 9: Nuclear Structure and Decay", [
            "06_Nuclear_Physics/The_Proton_Engine.md",
            "06_Nuclear_Physics/The_Neutron_Genesis.md",
            "06_Nuclear_Physics/The_Alpha_Architecture.md",
            "06_Nuclear_Physics/The_Deuteron_and_Alpha.md"
        ]),
    ],
    "Volume VI: Gravitation and Orbital Dynamics": [
        ("Book 10: The Mechanism of Gravity", [
            "03_Gravitation_and_Cosmology/Gravitation_from_Spation_Pressure_Gradients/Gravitation_from_Spation_Pressure_Gradients.md",
            "03_Gravitation_and_Cosmology/Stellar_Structure_from_Pressure_Geometry/Stellar_Structure_from_Pressure_Geometry.md"
        ]),
        ("Book 11: Planetary and Stellar Systems", [
            "03_Gravitation_and_Cosmology/Oblateness_Spin_Correlation/Oblateness_Spin_Correlation.md"
        ]),
    ],
    "Volume VII: Cosmology and Galactic Dynamics": [
        ("Book 12: Galactic Rotation and Dark Matter Replacement", [
            "03_Gravitation_and_Cosmology/Galactic_Rotation_from_Disk_Occlusion/Galactic_Rotation_from_Disk_Occlusion.md",
            "03_Gravitation_and_Cosmology/Galactic_Dynamics.md"
        ]),
        ("Book 13: Galactic Mass from Luminosity and the z×k² Invariant", [
            os.path.join(output_dir, "Galactic_Mass_from_Luminosity.md")
        ]),
        ("Book 14: Cosmological Structure", [
            "03_Gravitation_and_Cosmology/Cosmological_Structure_from_Pressure_Topology/Cosmological_Structure_from_Pressure_Topology.md"
        ]),
    ],
    "Volume VIII: Advanced Topics and Validation": [
        ("Book 15: Computational Validation", [
            os.path.join(output_dir, "Validation_Results.md")
        ]),
    ],
    "Volume IX: Computational Implementation": [
        ("Book 16: World-Class C++20 Calculator Suite", [
            os.path.join(output_dir, "Calculator_Suite_Documentation.md")
        ]),
    ]
}

header = """# De Rerum Todo Existens
## The Complete Canonical Principia of Spatial Displacement Theory

**Version:** Technical Reference 2.0
**Date:** December 2025
**Format:** Unified Theoretical Corpus
**Scope:** Foundations, Atomic Physics, Thermodynamics, Electromagnetism, Nuclear Physics, Gravitation, Cosmology, Validation

---

## About This Document

This is the complete, authoritative treatise of Spatial Displacement Theory (SDT), compiled from the organized Part I structure. All content has been validated against experimental benchmarks with sub-percent accuracy.

**Navigation:** Use the volume and book structure below to find specific topics. Each section is self-contained with full derivations and validation.

---

"""

def read_file_content(filename):
    """Read file from Part_I structure or output directory"""
    
    # If absolute path, use directly
    if os.path.isabs(filename):
        path = filename
    else:
        # Construct path from source_dir
        path = os.path.join(source_dir, filename)
    
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"# Error Reading File\n\nPath: {path}\nError: {str(e)}\n"
    else:
        return f"# Missing File\n\nExpected path: {path}\n\n*This file has not yet been created or the path is incorrect.*\n"

# Generate the complete treatise
print(f"Starting compilation...")
print(f"Source directory: {source_dir}")
print(f"Output file: {output_file}")

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write(header)
    
    for volume, books in structure.items():
        print(f"\n📚 Compiling {volume}...")
        outfile.write(f"# {volume}\n\n")
        
        for book_title, files in books:
            print(f"  📖 {book_title}")
            outfile.write(f"## {book_title}\n\n")
            outfile.write("---\n\n")
            
            for filename in files:
                print(f"    📄 {os.path.basename(filename)}")
                outfile.write(f"### Source: {os.path.basename(filename)}\n\n")
                content = read_file_content(filename)
                outfile.write(content)
                outfile.write("\n\n---\n\n")

print(f"\n✅ Compilation complete!")
print(f"📊 Output: {output_file}")

# Get file size
file_size = os.path.getsize(output_file)
print(f"📏 File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
