#include "sdt/chemistry/visualizer.hpp"
#include "sdt/chemistry/molecules.hpp"
#include "sdt/chemistry/designer.hpp"
#include "sdt/chemistry/bonds.hpp"
#include <iostream>
#include <string>
#include <vector>
#include <numbers>
#include <cmath>

void print_usage() {
    std::cout << "SDT Chemistry Molecule Viewer\n";
    std::cout << "=============================\n\n";
    std::cout << "Usage: molecule_viewer <command> [options]\n\n";
    std::cout << "Commands:\n";
    std::cout << "  visualize <molecule_file> [output_format] [output_file]\n";
    std::cout << "    - Create visualization from molecule JSON\n";
    std::cout << "    - Formats: obj, ply, pdb, xyz, pov\n";
    std::cout << "    - Default: obj\n\n";
    std::cout << "  design <output_file> [format]\n";
    std::cout << "    - Design a molecule and visualize it\n";
    std::cout << "    - Default format: obj\n\n";
    std::cout << "  example\n";
    std::cout << "    - Generate example water molecule visualization\n\n";
}

void create_example_water() {
    std::cout << "Creating example: Water molecule (H2O)\n";
    
    // Create water molecule using SDT geometry
    Molecule water("Water");
    
    // Add atoms (positions in meters, will be converted to Angstroms)
    constexpr double m_to_A = 1e10;
    
    // Oxygen at origin
    size_t O_idx = water.add_atom(8, Vec3d(0, 0, 0));
    
    // Hydrogen atoms (O-H bond length ~95.84 pm from Phase 17)
    double OH_bond_length = 95.84e-12;  // 95.84 pm in meters
    double HOH_angle = 104.5 * std::numbers::pi / 180.0;  // 104.5 degrees
    
    size_t H1_idx = water.add_atom(1, Vec3d(
        OH_bond_length * std::sin(HOH_angle / 2.0),
        0,
        OH_bond_length * std::cos(HOH_angle / 2.0)
    ));
    
    size_t H2_idx = water.add_atom(1, Vec3d(
        -OH_bond_length * std::sin(HOH_angle / 2.0),
        0,
        OH_bond_length * std::cos(HOH_angle / 2.0)
    ));
    
    // Add bonds
    water.add_bond(O_idx, H1_idx, BondType::COVALENT, 1);
    water.add_bond(O_idx, H2_idx, BondType::COVALENT, 1);
    
    std::cout << "  Atoms: " << water.num_atoms() << "\n";
    std::cout << "  Bonds: " << water.num_bonds() << "\n";
    
    // Create visualization
    MolecularVisualization viz = Visualizer::create_stick_ball_model(
        water, 1.0f, 0.15f, true  // CPK colors
    );
    
    std::cout << "  Visualization created:\n";
    std::cout << "    Atoms (spheres): " << viz.atoms.size() << "\n";
    std::cout << "    Bonds (cylinders): " << viz.bonds.size() << "\n";
    std::cout << "    Center: (" << viz.center.x() << ", " 
              << viz.center.y() << ", " << viz.center.z() << ") Å\n";
    
    // Export to multiple formats
    std::cout << "\nExporting to various formats...\n";
    
    if (Visualizer::export_to_obj(viz, "water.obj")) {
        std::cout << "  ✓ OBJ: water.obj\n";
    }
    
    if (Visualizer::export_to_pdb(water, "water.pdb")) {
        std::cout << "  ✓ PDB: water.pdb\n";
    }
    
    if (Visualizer::export_to_xyz(water, "water.xyz")) {
        std::cout << "  ✓ XYZ: water.xyz\n";
    }
    
    if (Visualizer::export_to_pov(viz, "water.pov")) {
        std::cout << "  ✓ POV-Ray: water.pov\n";
    }
    
    std::cout << "\nVisualization complete!\n";
    std::cout << "You can view these files in:\n";
    std::cout << "  - OBJ: Blender, MeshLab, or any 3D viewer\n";
    std::cout << "  - PDB: PyMOL, VMD, or ChimeraX\n";
    std::cout << "  - XYZ: Avogadro, Jmol\n";
    std::cout << "  - POV-Ray: Render with POV-Ray\n";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        print_usage();
        return 1;
    }
    
    std::string command = argv[1];
    
    if (command == "example") {
        create_example_water();
        return 0;
    }
    
    if (command == "visualize") {
        if (argc < 3) {
            std::cerr << "Error: molecule_file required\n";
            return 1;
        }
        
        std::string input_file = argv[2];
        std::string format = (argc > 3) ? argv[3] : "obj";
        std::string output_file = (argc > 4) ? argv[4] : "molecule." + format;
        
        std::cout << "Visualizing molecule from: " << input_file << "\n";
        std::cout << "Format: " << format << "\n";
        std::cout << "Output: " << output_file << "\n";
        
        // TODO: Load molecule from JSON file
        std::cout << "Note: JSON loading not yet implemented\n";
        std::cout << "Use 'example' command to see visualization in action\n";
        
        return 0;
    }
    
    if (command == "design") {
        std::string output_file = (argc > 2) ? argv[2] : "designed_molecule.obj";
        std::string format = (argc > 3) ? argv[3] : "obj";
        
        std::cout << "Designing molecule with target properties...\n";
        
        // Design a molecule
        std::vector<PropertyTarget> targets;
        PropertyTarget target;
        target.property_name = "stability";
        target.target_value = 400.0;
        target.tolerance = 50.0;
        target.weight = 1.0;
        targets.push_back(target);
        
        DesignResult result = CompoundDesigner::design_compound(targets, 8);
        
        std::cout << "  Fitness: " << result.fitness_score << "\n";
        std::cout << "  Atoms: " << result.molecule.num_atoms() << "\n";
        std::cout << "  Bonds: " << result.molecule.num_bonds() << "\n";
        
        // Create visualization
        MolecularVisualization viz = Visualizer::create_stick_ball_model(
            result.molecule, 1.0f, 0.15f, true
        );
        
        // Export
        bool success = false;
        if (format == "obj") {
            success = Visualizer::export_to_obj(viz, output_file);
        } else if (format == "pdb") {
            success = Visualizer::export_to_pdb(result.molecule, output_file);
        } else if (format == "xyz") {
            success = Visualizer::export_to_xyz(result.molecule, output_file);
        } else if (format == "pov") {
            success = Visualizer::export_to_pov(viz, output_file);
        }
        
        if (success) {
            std::cout << "\n✓ Exported to: " << output_file << "\n";
        } else {
            std::cerr << "\n✗ Export failed\n";
            return 1;
        }
        
        return 0;
    }
    
    std::cerr << "Unknown command: " << command << "\n";
    print_usage();
    return 1;
}

