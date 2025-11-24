#!/usr/bin/env python3
"""Compile all 27 books into a single document."""

import os
from pathlib import Path

# Define the order of all 27 books
books = [
    'Volume_I_Foundations/Book_1_The_Four_Ingredients.md',
    'Volume_I_Foundations/Book_2_Axioms_and_Master_Equation.md',
    'Volume_I_Foundations/Book_3_The_Derivation_Tree.md',
    'Volume_II_Atomic_Physics/Book_4_Single_Electron_Systems.md',
    'Volume_II_Atomic_Physics/Book_5_Multi_Electron_Systems.md',
    'Volume_II_Atomic_Physics/Book_6_Nuclear_Structure.md',
    'Volume_III_Thermodynamics/Book_7_Thermodynamic_Laws.md',
    'Volume_III_Thermodynamics/Book_8_Transport_and_Statistical_Mechanics.md',
    'Volume_IV_Electromagnetism/Book_9_Electric_Phenomena.md',
    'Volume_IV_Electromagnetism/Book_10_Magnetic_Phenomena.md',
    'Volume_IV_Electromagnetism/Book_11_Electromagnetic_Waves.md',
    'Volume_V_Gravitation/Book_12_Gravitational_Mechanics.md',
    'Volume_V_Gravitation/Book_13_Orbital_Dynamics.md',
    'Volume_V_Gravitation/Book_14_Strong_Field_and_Wave_Phenomena.md',
    'Volume_VI_Cosmology/Book_15_Cosmic_Structure.md',
    'Volume_VI_Cosmology/Book_16_Large_Scale_Phenomena.md',
    'Volume_VII_Unification/Book_17_Cross_Scale_Mechanics.md',
    'Volume_VII_Unification/Book_18_Master_Equation_Applications.md',
    'Volume_VIII_Validation/Book_19_Certified_Benchmarks.md',
    'Volume_VIII_Validation/Book_20_Active_Investigations.md',
    'Volume_VIII_Validation/Book_21_Scale_by_Scale_Validation.md',
    'Volume_IX_Philosophy/Book_22_Simulation_vs_Abstraction.md',
    'Volume_IX_Philosophy/Book_23_Historical_Context.md',
    'Volume_X_Reference/Book_24_Mathematical_Prerequisites.md',
    'Volume_X_Reference/Book_25_Constants_and_Units.md',
    'Volume_X_Reference/Book_26_Glossary_and_Index.md',
    'Volume_X_Reference/Book_27_Computational_Methods.md',
]

# Header
header = """# De Rerum Todo Existens
## The Complete Canonical Principia of Spatial Displacement Theory

**All 27 Books in a Single Document**

---

**Table of Contents:**

- Volume I: Foundations (De Fundamentis) - Books 1-3
- Volume II: Atomic Physics (De Atomis) - Books 4-6
- Volume III: Thermodynamics (De Calore) - Books 7-8
- Volume IV: Electromagnetism (De Lumine) - Books 9-11
- Volume V: Gravitation (De Gravitate) - Books 12-14
- Volume VI: Cosmology (De Universo) - Books 15-16
- Volume VII: Unification and Scale (De Unificatione) - Books 17-18
- Volume VIII: Validation (De Probatione) - Books 19-21
- Volume IX: Philosophical Foundations (De Philosophia) - Books 22-23
- Volume X: Reference (De Referentia) - Books 24-27

---

"""

# Get the base directory
base_dir = Path(__file__).parent

# Start with header
content = header

# Read and append each book
for i, book_path in enumerate(books, 1):
    full_path = base_dir / book_path
    if full_path.exists():
        print(f"Reading Book {i}/27: {book_path}")
        with open(full_path, 'r', encoding='utf-8') as f:
            book_content = f.read()
        content += f"\n\n{'='*80}\n\n"
        content += book_content
        content += f"\n\n{'='*80}\n\n"
    else:
        print(f"WARNING: Book not found: {book_path}")

# Write the complete document
output_path = base_dir / 'DE_RERUM_TODO_EXISTENS_COMPLETE.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nComplete! Written to: {output_path}")
print(f"Total size: {len(content):,} characters")

