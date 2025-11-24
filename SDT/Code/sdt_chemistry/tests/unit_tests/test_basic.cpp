#include "sdt/chemistry/elements.hpp"
#include "sdt/chemistry/bonds.hpp"
#include "sdt/chemistry/molecules.hpp"
#include "sdt/chemistry/pressure_field.hpp"
#include "sdt/chemistry/master_equation.hpp"
#include <cassert>
#include <iostream>

void test_elements() {
    std::cout << "Testing Elements...\n";
    
    // Test element lookup
    const ElementData& H = Elements::get_element("H");
    assert(H.Z == 1);
    assert(H.symbol == "H");
    
    const ElementData& C = Elements::get_element(6);
    assert(C.Z == 6);
    assert(C.symbol == "C");
    
    // Test existence
    assert(Elements::exists("H"));
    assert(Elements::exists(1));
    assert(!Elements::exists("Xx"));  // Non-existent element
    
    std::cout << "  ✓ Elements tests passed\n";
}

void test_bonds() {
    std::cout << "Testing Bonds...\n";
    
    const ElementData& H = Elements::get_element("H");
    const ElementData& O = Elements::get_element("O");
    
    // Test covalent bond length
    double r_OH = Bonds::covalent_bond_length(H, O, 1);
    assert(r_OH > 0.0);
    assert(r_OH < 200.0);  // Reasonable range
    
    // Test bond energy
    double E_OH = Bonds::covalent_bond_energy(H, O, r_OH, 1);
    assert(E_OH > 0.0);
    assert(E_OH < 1000.0);  // Reasonable range (kJ/mol)
    
    std::cout << "  ✓ Bonds tests passed\n";
}

void test_molecules() {
    std::cout << "Testing Molecules...\n";
    
    Molecule water("Water");
    
    // Add atoms
    size_t O_idx = water.add_atom(8, Vec3d(0, 0, 0));  // Oxygen
    size_t H1_idx = water.add_atom(1, Vec3d(1e-10, 0, 0));  // Hydrogen 1
    size_t H2_idx = water.add_atom(1, Vec3d(-1e-10, 0, 0));  // Hydrogen 2
    
    // Add bonds
    water.add_bond(O_idx, H1_idx, BondType::COVALENT, 1);
    water.add_bond(O_idx, H2_idx, BondType::COVALENT, 1);
    
    assert(water.num_atoms() == 3);
    assert(water.num_bonds() == 2);
    assert(water.is_valid());
    
    // Test connectivity
    std::vector<size_t> neighbors = water.neighbors(O_idx);
    assert(neighbors.size() == 2);
    
    std::cout << "  ✓ Molecules tests passed\n";
}

void test_pressure_field() {
    std::cout << "Testing Pressure Field...\n";
    
    double R1 = 1e-21;  // m
    double R2 = 1e-21;  // m
    double r = 1e-10;  // m (~1 Å)
    
    double force = PressureField::occlusion_force(R1, R2, r);
    assert(force > 0.0);
    
    // Test bond energy
    double E = PressureField::bond_energy_kJ_per_mol(R1, R2, r);
    assert(E > 0.0);
    
    std::cout << "  ✓ Pressure Field tests passed\n";
}

void test_master_equation() {
    std::cout << "Testing Master Equation...\n";
    
    // Test power throughput calculation
    double P = 1.65e31;  // Pa (nuclear scale)
    double A = 5e-30;  // m²
    double Gamma = 0.546;
    double kappa = 1.19e15;  // m⁻¹
    double traction = 0.9997;
    
    double power = MasterEquation::calculate_power_throughput(P, A, Gamma, kappa, traction);
    assert(power > 0.0);
    
    std::cout << "  ✓ Master Equation tests passed\n";
}

int main() {
    std::cout << "Running SDT Chemistry Unit Tests\n";
    std::cout << "================================\n\n";
    
    try {
        test_elements();
        test_bonds();
        test_molecules();
        test_pressure_field();
        test_master_equation();
        
        std::cout << "\nAll tests passed! ✓\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Test failed: " << e.what() << "\n";
        return 1;
    }
}

