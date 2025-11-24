#include "sdt/chemistry/designer.hpp"
#include "sdt/chemistry/geometry.hpp"
#include <random>
#include <algorithm>
#include <cmath>
#include <cctype>

namespace sdt::chemistry {

    static std::random_device rd;
    static std::mt19937 gen(rd());

    DesignResult CompoundDesigner::design_compound(
        const std::vector<PropertyTarget>& targets,
        int max_atoms,
        const std::vector<std::string>& allowed_elements
    ) {
        DesignResult result;
        result.optimized = false;
        
        // Generate initial candidates
        std::vector<Molecule> candidates = generate_candidates(std::nullopt, 20);
        
        // Evaluate fitness
        double best_fitness = -1e10;
        Molecule best_molecule;
        
        for (auto& candidate : candidates) {
            double fitness = evaluate_fitness(candidate, targets);
            if (fitness > best_fitness) {
                best_fitness = fitness;
                best_molecule = candidate;
            }
        }
        
        // Optimize best candidate
        result = optimize_for_properties(best_molecule, targets);
        result.fitness_score = best_fitness;
        
        return result;
    }

    std::vector<Molecule> CompoundDesigner::generate_candidates(
        const std::optional<Molecule>& base_molecule,
        int num_candidates
    ) {
        std::vector<Molecule> candidates;
        
        if (base_molecule.has_value()) {
            // Generate variations of base molecule
            for (int i = 0; i < num_candidates; ++i) {
                Molecule candidate = mutate(base_molecule.value());
                candidates.push_back(candidate);
            }
        } else {
            // Generate random molecules
            std::uniform_int_distribution<int> atom_dist(2, 10);
            for (int i = 0; i < num_candidates; ++i) {
                int num_atoms = atom_dist(gen);
                Molecule candidate = generate_random(num_atoms);
                candidates.push_back(candidate);
            }
        }
        
        return candidates;
    }

    DesignResult CompoundDesigner::optimize_for_properties(
        Molecule& molecule,
        const std::vector<PropertyTarget>& targets
    ) {
        DesignResult result;
        result.molecule = molecule;
        result.optimized = false;
        
        // Optimize geometry first
        GeometryOptimizer::optimize(molecule, 1e-6, 100);
        
        // Evaluate properties
        for (const auto& target : targets) {
            double value = get_property_value(molecule, target.property_name);
            result.property_values.push_back(value);
        }
        
        result.fitness_score = evaluate_fitness(molecule, targets);
        result.optimized = true;
        result.message = "Optimization complete";
        
        return result;
    }

    double CompoundDesigner::evaluate_fitness(
        const Molecule& molecule,
        const std::vector<PropertyTarget>& targets
    ) {
        double fitness = 0.0;
        double total_weight = 0.0;
        
        for (const auto& target : targets) {
            double value = get_property_value(molecule, target.property_name);
            double error = std::abs(value - target.target_value);
            double normalized_error = error / (target.tolerance + 1e-10);
            
            // Fitness = 1 / (1 + normalized_error) weighted
            double score = 1.0 / (1.0 + normalized_error);
            fitness += target.weight * score;
            total_weight += target.weight;
        }
        
        if (total_weight > 0.0) {
            fitness /= total_weight;
        }
        
        return fitness;
    }

    Molecule CompoundDesigner::mutate(const Molecule& molecule, double mutation_rate) {
        Molecule mutated = molecule;
        
        std::uniform_real_distribution<double> prob_dist(0.0, 1.0);
        
        // Random mutations
        if (prob_dist(gen) < mutation_rate && mutated.num_atoms() < 20) {
            // Add atom
            mutated = add_random_atom(mutated, {});
        }
        
        if (prob_dist(gen) < mutation_rate && mutated.num_atoms() > 2) {
            // Remove atom
            mutated = remove_random_atom(mutated);
        }
        
        if (prob_dist(gen) < mutation_rate && mutated.num_bonds() > 0) {
            // Modify bond
            mutated = modify_random_bond(mutated);
        }
        
        // Optimize geometry
        GeometryOptimizer::optimize(mutated, 1e-4, 50);
        
        return mutated;
    }

    Molecule CompoundDesigner::crossover(const Molecule& parent1, const Molecule& parent2) {
        // Simple crossover: take atoms from both parents
        Molecule child;
        child = parent1;  // Start with parent1
        
        // Add some atoms from parent2
        std::uniform_int_distribution<size_t> atom_dist(0, parent2.num_atoms() - 1);
        for (size_t i = 0; i < std::min(parent2.num_atoms(), size_t(3)); ++i) {
            size_t idx = atom_dist(gen);
            const Atom& atom = parent2.atom(idx);
            child.add_atom(atom.element_Z, atom.position);
        }
        
        // Optimize
        GeometryOptimizer::optimize(child, 1e-4, 50);
        
        return child;
    }

    Molecule CompoundDesigner::generate_random(
        int num_atoms,
        const std::vector<std::string>& allowed_elements
    ) {
        Molecule molecule("Random");
        
        // Default elements if none specified
        std::vector<std::string> elements = allowed_elements;
        if (elements.empty()) {
            elements = {"H", "C", "N", "O", "F", "Cl"};
        }
        
        std::uniform_int_distribution<size_t> elem_dist(0, elements.size() - 1);
        std::uniform_real_distribution<double> pos_dist(-1e-9, 1e-9);  // nm scale
        
        // Add atoms
        for (int i = 0; i < num_atoms; ++i) {
            std::string symbol = elements[elem_dist(gen)];
            int Z = Elements::get_element(symbol).Z;
            
            Vec3d position(
                pos_dist(gen),
                pos_dist(gen),
                pos_dist(gen)
            );
            
            molecule.add_atom(Z, position);
        }
        
        // Add bonds (simplified: connect nearby atoms)
        for (size_t i = 0; i < molecule.num_atoms(); ++i) {
            for (size_t j = i + 1; j < molecule.num_atoms(); ++j) {
                Vec3d r_vec = molecule.atom(j).position - molecule.atom(i).position;
                double r = r_vec.norm();
                
                // Bond if within reasonable distance
                if (r < 2e-10) {  // ~2 Å
                    try {
                        molecule.add_bond(i, j, BondType::COVALENT, 1);
                    } catch (...) {
                        // Bond already exists or invalid
                    }
                }
            }
        }
        
        // Optimize geometry
        GeometryOptimizer::optimize(molecule, 1e-4, 50);
        
        return molecule;
    }

    std::vector<std::string> CompoundDesigner::suggest_synthesis_pathway(const Molecule& target) {
        // Simplified synthesis pathway suggestion
        std::vector<std::string> pathway;
        
        pathway.push_back("1. Identify key functional groups");
        pathway.push_back("2. Break down into simpler precursors");
        pathway.push_back("3. Plan retrosynthetic analysis");
        pathway.push_back("4. Select appropriate reagents");
        pathway.push_back("5. Optimize reaction conditions");
        
        return pathway;
    }

    double CompoundDesigner::get_property_value(const Molecule& molecule, const std::string& property_name) {
        if (property_name == "binding_energy") {
            return Properties::binding_energy(molecule);
        } else if (property_name == "stability") {
            return Properties::stability(molecule);
        } else if (property_name == "melting_point") {
            return Properties::melting_point(molecule);
        } else if (property_name == "boiling_point") {
            return Properties::boiling_point(molecule);
        } else if (property_name == "dipole_moment") {
            return Properties::dipole_moment(molecule);
        } else if (property_name == "molecular_volume") {
            return Properties::molecular_volume(molecule);
        } else if (property_name == "total_energy") {
            return Properties::total_energy(molecule);
        } else {
            return 0.0;
        }
    }

    Molecule CompoundDesigner::add_random_atom(
        const Molecule& molecule,
        const std::vector<std::string>& allowed_elements
    ) {
        Molecule new_mol = molecule;
        
        std::vector<std::string> elements = allowed_elements;
        if (elements.empty()) {
            elements = {"H", "C", "N", "O"};
        }
        
        std::uniform_int_distribution<size_t> elem_dist(0, elements.size() - 1);
        std::uniform_real_distribution<double> pos_dist(-1e-9, 1e-9);
        
        std::string symbol = elements[elem_dist(gen)];
        int Z = Elements::get_element(symbol).Z;
        
        Vec3d position(
            pos_dist(gen),
            pos_dist(gen),
            pos_dist(gen)
        );
        
        new_mol.add_atom(Z, position);
        return new_mol;
    }

    Molecule CompoundDesigner::remove_random_atom(const Molecule& molecule) {
        Molecule new_mol = molecule;
        
        if (new_mol.num_atoms() > 1) {
            std::uniform_int_distribution<size_t> atom_dist(0, new_mol.num_atoms() - 1);
            size_t idx = atom_dist(gen);
            new_mol.remove_atom(idx);
        }
        
        return new_mol;
    }

    Molecule CompoundDesigner::modify_random_bond(const Molecule& molecule) {
        Molecule new_mol = molecule;
        
        if (new_mol.num_bonds() > 0) {
            std::uniform_int_distribution<size_t> bond_dist(0, new_mol.num_bonds() - 1);
            size_t idx = bond_dist(gen);
            
            Bond& bond = new_mol.bond(idx);
            // Modify bond order
            bond.bond_order = (bond.bond_order % 3) + 1;
        }
        
        return new_mol;
    }

} // namespace sdt::chemistry

