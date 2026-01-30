#include <iostream>
#include <iomanip>
#include <format>
#include "../include/nuclear_geometry_occlusion.hpp"

using namespace sdt::nuclear::occlusion;

void print_header() {
    std::cout << "\n";
    std::cout << "╔═══════════════════════════════════════════════════════════════════╗\n";
    std::cout << "║     SDT NUCLEAR GEOMETRY CALCULATOR v2.0 - Occlusion Model       ║\n";
    std::cout << "║              Binding Energies from Pure Geometry                 ║\n";
    std::cout << "╚═══════════════════════════════════════════════════════════════════╝\n";
    std::cout << "\n";
}

void print_deuteron_analysis() {
    std::cout << "═══ DEUTERON (²H): The Seed Calibration ═══\n\n";
    
    DeuteronGeometry d;
    
    std::cout << "Geometry:\n";
    std::cout << std::format("  Radius (p):    {:.2f} fm\n", constants::proton_radius_fm);
    std::cout << std::format("  Separation:    {:.2f} fm\n", constants::dist_deuteron_fm);
    
    std::cout << "\nOcclusion Analysis:\n";
    std::cout << std::format("  Solid Angle:   {:.3f} sr\n", d.occlusion_solid_angle());
    std::cout << std::format("  Field Strength: {:.3f} MeV/sr (Universal Constant)\n", 
                           constants::k_binding_MeV_per_sr);
    
    std::cout << "\nBinding Energy:\n";
    std::cout << std::format("  Predicted:     {:.4f} MeV\n", d.binding_energy_predicted());
    std::cout << std::format("  Experimental:  {:.4f} MeV\n", DeuteronGeometry::binding_energy_experimental());
}

void print_alpha_analysis() {
    std::cout << "\n═══ ALPHA (⁴He): Vacuum Lock ═══\n\n";
    
    AlphaGeometry alpha;
    
    std::cout << "Geometry:\n";
    std::cout << std::format("  Structure:     Tetrahedral (4 nucleons, 6 edges)\n");
    std::cout << std::format("  Separation:    {:.2f} fm (Compressed)\n", constants::dist_alpha_fm);
    
    std::cout << "\nOcclusion Analysis:\n";
    std::cout << std::format("  Single Bond:   {:.3f} sr\n", math::spherical_occlusion(constants::proton_radius_fm, constants::dist_alpha_fm));
    std::cout << std::format("  Total (6x):    {:.3f} sr\n", alpha.total_occlusion());
    
    std::cout << "\nBinding Energy:\n";
    std::cout << std::format("  Predicted:     {:.4f} MeV\n", alpha.binding_energy_predicted());
    std::cout << std::format("  Experimental:  {:.4f} MeV\n", AlphaGeometry::binding_energy_experimental());
    
    double error = std::abs(alpha.binding_energy_predicted() - AlphaGeometry::binding_energy_experimental()) 
                   / AlphaGeometry::binding_energy_experimental() * 100.0;
    std::cout << std::format("  Error:         {:.2f}%\n", error);
}

void print_heavier_nuclei() {
    std::cout << "\n═══ CLUSTER NUCLEI: C-12 & O-16 ═══\n\n";
    
    Carbon12Geometry c12;
    Oxygen16Geometry o16;
    
    std::cout << "Carbon-12 (3-Alpha Triangle):\n";
    std::cout << std::format("  Structure:     3 Alphas + 3 Inter-bonds\n");
    std::cout << std::format("  Cluster Sep:   {:.2f} fm\n", constants::dist_inter_alpha_fm);
    std::cout << std::format("  Predicted:     {:.4f} MeV\n", c12.binding_energy_predicted());
    std::cout << std::format("  Experimental:  {:.4f} MeV\n", Carbon12Geometry::binding_energy_experimental());
    std::cout << std::format("  Error:         {:.2f}%\n\n", 
        std::abs(c12.binding_energy_predicted() - Carbon12Geometry::binding_energy_experimental()) / Carbon12Geometry::binding_energy_experimental() * 100.0);

    std::cout << "Oxygen-16 (4-Alpha Tetrahedron):\n";
    std::cout << std::format("  Structure:     4 Alphas + 6 Inter-bonds\n");
    std::cout << std::format("  Predicted:     {:.4f} MeV\n", o16.binding_energy_predicted());
    std::cout << std::format("  Experimental:  {:.4f} MeV\n", Oxygen16Geometry::binding_energy_experimental());
    std::cout << std::format("  Error:         {:.2f}%\n", 
        std::abs(o16.binding_energy_predicted() - Oxygen16Geometry::binding_energy_experimental()) / Oxygen16Geometry::binding_energy_experimental() * 100.0);
}

void print_electron_rule() {
    std::cout << "\n═══ CHEMISTRY BRIDGE ═══\n\n";
    std::cout << ElectronPositionRule::get_rule_description() << "\n\n";
}

int main(int argc, char* argv[]) {
    print_header();
    
    print_deuteron_analysis();
    print_alpha_analysis();
    print_heavier_nuclei();
    print_electron_rule();
    
    return 0;
}
