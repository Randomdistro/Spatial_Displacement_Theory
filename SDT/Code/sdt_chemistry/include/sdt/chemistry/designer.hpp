#pragma once

#include "molecules.hpp"
#include "geometry.hpp"
#include "properties.hpp"
#include <vector>
#include <string>
#include <functional>
#include <optional>

namespace sdt::chemistry {

    /**
     * Target property specification
     */
    struct PropertyTarget {
        std::string property_name;  // e.g., "binding_energy", "stability", "melting_point"
        double target_value;
        double tolerance;  // Acceptable range
        double weight;  // Importance weight (0-1)
    };
    
    /**
     * Compound design result
     */
    struct DesignResult {
        Molecule molecule;
        double fitness_score;  // How well it matches targets
        std::vector<double> property_values;
        bool optimized;
        std::string message;
    };
    
    /**
     * Compound designer for generating new molecules
     */
    class CompoundDesigner {
    public:
        /**
         * Design a molecule with target properties
         * 
         * @param targets List of target properties
         * @param max_atoms Maximum number of atoms
         * @param allowed_elements List of allowed element symbols
         * @return Designed molecule
         */
        static DesignResult design_compound(
            const std::vector<PropertyTarget>& targets,
            int max_atoms = 20,
            const std::vector<std::string>& allowed_elements = {}
        );
        
        /**
         * Generate candidate structures
         * 
         * @param base_molecule Starting molecule (optional)
         * @param num_candidates Number of candidates to generate
         * @return List of candidate molecules
         */
        static std::vector<Molecule> generate_candidates(
            const std::optional<Molecule>& base_molecule = std::nullopt,
            int num_candidates = 10
        );
        
        /**
         * Optimize molecule to match target properties
         */
        static DesignResult optimize_for_properties(
            Molecule& molecule,
            const std::vector<PropertyTarget>& targets
        );
        
        /**
         * Evaluate how well a molecule matches target properties
         */
        static double evaluate_fitness(
            const Molecule& molecule,
            const std::vector<PropertyTarget>& targets
        );
        
        /**
         * Mutate a molecule (for genetic algorithm)
         */
        static Molecule mutate(const Molecule& molecule, double mutation_rate = 0.1);
        
        /**
         * Crossover two molecules (for genetic algorithm)
         */
        static Molecule crossover(const Molecule& parent1, const Molecule& parent2);
        
        /**
         * Generate random molecule
         */
        static Molecule generate_random(
            int num_atoms,
            const std::vector<std::string>& allowed_elements = {}
        );
        
        /**
         * Suggest synthesis pathway (simplified)
         */
        static std::vector<std::string> suggest_synthesis_pathway(const Molecule& target);
        
    private:
        static double get_property_value(const Molecule& molecule, const std::string& property_name);
        static Molecule add_random_atom(const Molecule& molecule, const std::vector<std::string>& allowed_elements);
        static Molecule remove_random_atom(const Molecule& molecule);
        static Molecule modify_random_bond(const Molecule& molecule);
    };

} // namespace sdt::chemistry

