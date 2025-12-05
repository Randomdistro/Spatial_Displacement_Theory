#include <iostream>
#include <iomanip>
#include <format>
#include "../include/nuclear_geometry.hpp"

using namespace sdt::nuclear;

void print_header() {
    std::cout << "\n";
    std::cout << "╔═══════════════════════════════════════════════════════════════════╗\n";
    std::cout << "║     SDT NUCLEAR GEOMETRY CALCULATOR - Deterministic Physics      ║\n";
    std::cout << "║              Binding Energies from Pure Geometry                 ║\n";
    std::cout << "╚═══════════════════════════════════════════════════════════════════╝\n";
    std::cout << "\n";
}

void print_deuteron_analysis() {
    std::cout << "═══ DEUTERON (²H): The Seed Crystal ═══\n\n";
    
    auto d = create_deuteron();
    
    std::cout << "Geometry:\n";
    std::cout << std::format("  Proton:    {}\n", d.proton.full_name());
    std::cout << std::format("  Neutron:   {}\n", d.neutron.full_name());
    std::cout << std::format("  Structure: Coaxial stack (parallel spins, S=1)\n");
    std::cout << std::format("  Separation: {:.2f} fm\n", d.separation_fm);
    std::cout << std::format("  Electron unwinding: {:.1f}% of 6π\n", 
                           d.electron_unwinding * 100);
    
    std::cout << "\nNeutrino Analysis:\n";
    std::cout << std::format("  Neutrino count: {:.2f} (partial resonance)\n", 
                           d.neutrino_count());
    std::cout << std::format("  E_ν per neutrino: {:.3f} MeV\n", 
                           constants::E_nu_MeV);
    
    std::cout << "\nBinding Energy:\n";
    std::cout << std::format("  Predicted:     {:.4f} MeV\n", 
                           d.binding_energy_predicted());
    std::cout << std::format("  Experimental:  {:.4f} MeV\n", 
                           d.binding_energy_experimental());
    std::cout << std::format("  Error:         {:.3f}%\n\n", d.error_percent());
}

void print_alpha_analysis() {
    std::cout << "═══ ALPHA (⁴He): The Tetrahedral Lock ═══\n\n";
    
    auto alpha = create_alpha();
    
    std::cout << "Geometry:\n";
    std::cout << "  Structure: Tetrahedral (most compact 3D shape)\n";
    std::cout << "  Nucleons:\n";
    for (size_t i = 0; i < alpha.nucleons.size(); ++i) {
        std::cout << std::format("    {} - {}\n", i, alpha.nucleons[i].full_name());
    }
    
    std::cout << "\nBinding Channels:\n";
    auto channels = alpha.get_channels();
    for (const auto& ch : channels) {
        std::cout << std::format("  {} → {:.1f} neutrinos {}\n",
                               ch.description(alpha.nucleons),
                               ch.neutrino_contribution,
                               ch.is_pn_pair ? "(strong)" : "(Pauli)");
    }
    
    std::cout << "\nNeutrino Analysis:\n";
    std::cout << std::format("  Total neutrinos: {:.1f}\n", alpha.neutrino_count());
    std::cout << std::format("  Expected: {} (from architecture)\n", 
                           constants::alpha_neutrinos);
    
    std::cout << "\nBinding Energy:\n";
    std::cout << std::format("  Predicted:     {:.4f} MeV\n", 
                           alpha.binding_energy_predicted());
    std::cout << std::format("  Experimental:  {:.4f} MeV\n", 
                           alpha.binding_energy_experimental());
    std::cout << std::format("  Error:         {:.3f}%\n\n", alpha.error_percent());
}

void print_heavier_nuclei() {
    std::cout << "═══ HEAVIER NUCLEI: Alpha Cluster Model ═══\n\n";
    
    // Carbon-12
    auto c12 = create_carbon12();
    std::cout << "Carbon-12 (¹²C):\n";
    std::cout << "  Structure: 3 alphas in triangular ring\n";
    std::cout << std::format("  3× Alpha binding: {:.2f} MeV\n", 
                           3.0 * AlphaGeometry::binding_energy_experimental());
    std::cout << std::format("  Inter-alpha coupling: {:.2f} MeV\n", 
                           c12.inter_alpha_coupling_MeV());
    std::cout << std::format("  Predicted:     {:.4f} MeV\n", 
                           c12.binding_energy_predicted());
    std::cout << std::format("  Experimental:  {:.4f} MeV\n", 
                           c12.binding_energy_experimental());
    std::cout << std::format("  Error:         {:.3f}%\n\n", c12.error_percent());
    
    // Oxygen-16
    auto o16 = create_oxygen16();
    std::cout << "Oxygen-16 (¹⁶O):\n";
    std::cout << "  Structure: 4 alphas in tetrahedron\n";
    std::cout << std::format("  4× Alpha binding: {:.2f} MeV\n", 
                           4.0 * AlphaGeometry::binding_energy_experimental());
    std::cout << std::format("  Inter-alpha coupling: {:.2f} MeV\n", 
                           o16.inter_alpha_coupling_MeV());
    std::cout << std::format("  Predicted:     {:.4f} MeV\n", 
                           o16.binding_energy_predicted());
    std::cout << std::format("  Experimental:  {:.4f} MeV\n", 
                           o16.binding_energy_experimental());
    std::cout << std::format("  Error:         {:.3f}%\n\n", o16.error_percent());
}

void print_validation_table() {
    std::cout << "═══ VALIDATION SUMMARY ═══\n\n";
    
    auto results = validate_all();
    
    std::cout << "┌────────────────┬──────────────┬──────────────┬─────────┬────────────┐\n";
    std::cout << "│ Nucleus        │  Predicted   │ Experimental │  Error  │   Status   │\n";
    std::cout << "│                │    (MeV)     │    (MeV)     │   (%)   │            │\n";
    std::cout << "├────────────────┼──────────────┼──────────────┼─────────┼────────────┤\n";
    
    for (const auto& r : results) {
        std::cout << std::format("│ {:<14} │ {:>12.4f} │ {:>12.4f} │ {:>7.3f} │ {:<10} │\n",
                               r.nucleus, r.predicted_MeV, r.experimental_MeV,
                               r.error_percent, r.status());
    }
    
    std::cout << "└────────────────┴──────────────┴──────────────┴─────────┴────────────┘\n\n";
    
    // Count certified
    int certified = 0;
    for (const auto& r : results) {
        if (r.certified) ++certified;
    }
    
    std::cout << std::format("Certified (<1% error): {}/{}\n", certified, results.size());
    std::cout << "\n";
}

void print_theory_comparison() {
    std::cout << "═══ THEORY COMPARISON ═══\n\n";
    
    std::cout << "QED/QCD Standard Model:\n";
    std::cout << "  • Quarks (uud, udd) as fundamental\n";
    std::cout << "  • Probability clouds for particle positions\n";
    std::cout << "  • Strong force from gluon exchange\n";
    std::cout << "  • No geometric determinism\n";
    std::cout << "  • Requires lattice QCD for binding energies\n\n";
    
    std::cout << "SDT Geometric Model:\n";
    std::cout << "  • Proton = 6π trefoil torus (deterministic)\n";
    std::cout << "  • Electron positions FIXED by nuclear geometry\n";
    std::cout << "  • Binding = neutrino circulation (count × 1.57 MeV)\n";
    std::cout << "  • Chirality rules determine pairing\n";
    std::cout << "  • Pure geometric calculation → <1% accuracy\n\n";
    
    std::cout << "KEY DIFFERENCE:\n";
    std::cout << "  QED: 'Electron might be anywhere' (probability)\n";
    std::cout << "  SDT: 'Electron IS at (x,y,z)' (determinism)\n\n";
    
    std::cout << "If SDT predicts all binding energies to <1% from geometry alone,\n";
    std::cout << "QED probability interpretation is WRONG.\n\n";
}

int main(int argc, char* argv[]) {
    print_header();
    
    bool show_all = (argc > 1 && std::string(argv[1]) == "--all");
    
    if (show_all) {
        print_deuteron_analysis();
        print_alpha_analysis();
        print_heavier_nuclei();
        print_theory_comparison();
    }
    
    print_validation_table();
    
    std::cout << "Run with --all for detailed analysis\n";
    std::cout << "\n";
    
    return 0;
}
