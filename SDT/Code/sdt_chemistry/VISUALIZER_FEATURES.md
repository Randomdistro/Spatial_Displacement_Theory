# SDT Chemistry Visualizer - Features

## Overview

The SDT Chemistry Visualizer creates stick-and-ball molecular models using SDT-calculated geometry. All atom positions and bond lengths are derived from SDT pressure field mechanics, ensuring accurate representation based on first principles.

## Key Features

### 1. SDT-Based Geometry

- **Atom Positions**: Uses SDT-calculated positions from pressure field optimization
- **Bond Lengths**: Derived from SDT bond calculations (covalent, ionic, etc.)
- **Bond Angles**: Calculated from pressure field energy minimization
- **No External Geometry**: All coordinates come from SDT physics

### 2. Stick-and-Ball Model

- **Atoms**: Rendered as spheres with CPK (Corey-Pauling-Koltun) colors
- **Bonds**: Rendered as cylinders connecting atoms
- **Proportional Sizing**: Atom radii based on SDT atomic radii
- **Bond Representation**: Single/double/triple bonds shown with appropriate styling

### 3. CPK Color Scheme

Standard molecular visualization colors:
- **H**: White
- **C**: Black/Gray
- **N**: Blue
- **O**: Red
- **F**: Green
- **P**: Orange
- **S**: Yellow
- **Cl**: Green
- And more...

### 4. Export Formats

#### OBJ (Wavefront)
- Standard 3D format
- Compatible with Blender, MeshLab, 3D viewers
- Includes vertex positions and colors

#### PDB (Protein Data Bank)
- Standard format for molecular structures
- Compatible with PyMOL, VMD, ChimeraX
- Includes atom records and connectivity

#### XYZ
- Simple coordinate format
- Compatible with Avogadro, Jmol
- Easy to parse and process

#### PLY (Stanford Polygon)
- Polygon mesh format
- High-quality mesh representation
- Compatible with many 3D tools

#### POV-Ray
- High-quality ray-traced rendering
- Photorealistic output
- Professional visualization

## Usage Examples

### Basic Visualization

```cpp
#include "sdt/chemistry/visualizer.hpp"
#include "sdt/chemistry/molecules.hpp"

// Create molecule
Molecule water("Water");
// ... add atoms and bonds ...

// Create visualization
MolecularVisualization viz = Visualizer::create_stick_ball_model(
    water, 1.0f, 0.15f, true  // atom_scale, bond_radius, use_cpk_colors
);

// Export
Visualizer::export_to_obj(viz, "water.obj");
Visualizer::export_to_pdb(water, "water.pdb");
```

### Custom Styling

```cpp
// Larger atoms, thinner bonds
MolecularVisualization viz = Visualizer::create_stick_ball_model(
    molecule, 1.5f, 0.1f, true
);

// Custom colors (disable CPK)
MolecularVisualization viz = Visualizer::create_stick_ball_model(
    molecule, 1.0f, 0.15f, false
);
```

## SDT Integration

The visualizer is fully integrated with SDT:

1. **Positions**: Uses `Molecule::atom(i).position` from SDT geometry optimization
2. **Bond Lengths**: Uses `Bond::length_pm` from SDT bond calculations
3. **Atomic Radii**: Uses `ElementData::atomic_radius_pm` from SDT element database
4. **Colors**: Uses element-specific CPK colors based on atomic number

## Technical Details

### Coordinate System

- **Input**: SDT uses meters (m) for positions
- **Output**: Visualization uses Angstroms (Å) for standard molecular viewing
- **Conversion**: 1 m = 10^10 Å

### Sphere Generation

- Atoms are represented as spheres
- Radius based on SDT atomic radius
- CPK colors applied per element

### Cylinder Generation

- Bonds are represented as cylinders
- Cylinders shortened to avoid overlap with atom spheres
- Radius configurable (default 0.15 Å)

### Bounding Box

- Automatically calculated from atom positions
- Used for camera positioning in POV-Ray export
- Can be used for centering molecule

## Future Enhancements

- Interactive 3D viewer (OpenGL/Vulkan)
- Animation support (reaction pathways)
- Surface rendering (van der Waals surfaces)
- Electron density visualization
- Bond order visualization (double/triple bonds)
- Custom color schemes
- Label rendering (atom names, bond orders)

## Conventions

The visualizer follows standard molecular visualization conventions:

1. **CPK Colors**: Industry-standard element colors
2. **Stick-and-Ball**: Standard representation for molecules
3. **Bond Styling**: Single bonds as cylinders, multiple bonds as thicker/multiple cylinders
4. **File Formats**: Standard formats for compatibility

All geometry is derived from SDT physics, ensuring accuracy and consistency with the theoretical framework.

