#include "sdt/chemistry/designer.hpp"
#include "sdt/chemistry/properties.hpp"
#include "sdt/chemistry/geometry.hpp"
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>

int main(int argc, char* argv[]) {
    std::cout << "SDT Chemistry Compound Designer\n";
    std::cout << "================================\n\n";
    
    // Example: Design a molecule with target properties
    std::vector<PropertyTarget> targets;
    
    // Target: High stability
    PropertyTarget stability_target;
    stability_target.property_name = "stability";
    stability_target.target_value = 500.0;  // kJ/mol
    stability_target.tolerance = 100.0;
    stability_target.weight = 0.5;
    targets.push_back(stability_target);
    
    // Target: Specific melting point
    PropertyTarget mp_target;
    mp_target.property_name = "melting_point";
    mp_target.target_value = 300.0;  // K
    mp_target.tolerance = 50.0;
    mp_target.weight = 0.3;
    targets.push_back(mp_target);
    
    // Target: Moderate dipole moment
    PropertyTarget dipole_target;
    dipole_target.property_name = "dipole_moment";
    dipole_target.target_value = 2.0;  // Debye
    dipole_target.tolerance = 1.0;
    dipole_target.weight = 0.2;
    targets.push_back(dipole_target);
    
    std::cout << "Designing compound with target properties:\n";
    for (const auto& target : targets) {
        std::cout << "  - " << target.property_name 
                  << ": " << target.target_value 
                  << " ± " << target.tolerance << "\n";
    }
    std::cout << "\n";
    
    // Design compound
    DesignResult result = CompoundDesigner::design_compound(targets, 10);
    
    std::cout << "Design Result:\n";
    std::cout << "  Fitness Score: " << std::fixed << std::setprecision(3) 
              << result.fitness_score << "\n";
    std::cout << "  Optimized: " << (result.optimized ? "Yes" : "No") << "\n";
    std::cout << "  Message: " << result.message << "\n\n";
    
    // Display properties
    std::cout << "Calculated Properties:\n";
    for (size_t i = 0; i < targets.size() && i < result.property_values.size(); ++i) {
        std::cout << "  " << targets[i].property_name << ": " 
                  << std::fixed << std::setprecision(2) 
                  << result.property_values[i] << "\n";
    }
    std::cout << "\n";
    
    // Display molecule info
    std::cout << "Molecule Information:\n";
    std::cout << "  Name: " << result.molecule.name() << "\n";
    std::cout << "  Number of atoms: " << result.molecule.num_atoms() << "\n";
    std::cout << "  Number of bonds: " << result.molecule.num_bonds() << "\n";
    std::cout << "  Total energy: " << std::fixed << std::setprecision(2)
              << Properties::total_energy(result.molecule) << " kJ/mol\n";
    std::cout << "  Binding energy: " << std::fixed << std::setprecision(2)
              << Properties::binding_energy(result.molecule) << " kJ/mol\n";
    
    // Export to JSON
    std::cout << "\nMolecule JSON:\n";
    std::cout << result.molecule.to_json() << "\n";
    
    return 0;
}

