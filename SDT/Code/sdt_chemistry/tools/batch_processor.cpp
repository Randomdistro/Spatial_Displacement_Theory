#include "sdt/chemistry/designer.hpp"
#include "sdt/chemistry/properties.hpp"
#include "sdt/chemistry/data_loader.hpp"
#include <iostream>
#include <fstream>
#include <vector>
#include <string>

int main(int argc, char* argv[]) {
    std::cout << "SDT Chemistry Batch Processor\n";
    std::cout << "=============================\n\n";
    
    if (argc < 2) {
        std::cout << "Usage: batch_processor <input_file> [output_file]\n";
        std::cout << "  input_file: JSON file with design targets\n";
        std::cout << "  output_file: Optional output file for results\n";
        return 1;
    }
    
    std::string input_file = argv[1];
    std::string output_file = (argc > 2) ? argv[2] : "batch_results.json";
    
    std::cout << "Processing: " << input_file << "\n";
    std::cout << "Output: " << output_file << "\n\n";
    
    // TODO: Load batch job from input file
    // For now, process a simple example
    
    std::vector<PropertyTarget> targets;
    PropertyTarget target;
    target.property_name = "stability";
    target.target_value = 400.0;
    target.tolerance = 50.0;
    target.weight = 1.0;
    targets.push_back(target);
    
    std::cout << "Processing batch job...\n";
    
    // Generate multiple candidates
    std::vector<DesignResult> results;
    for (int i = 0; i < 10; ++i) {
        DesignResult result = CompoundDesigner::design_compound(targets, 8);
        results.push_back(result);
        std::cout << "  Candidate " << (i+1) << ": Fitness = " 
                  << result.fitness_score << "\n";
    }
    
    // Find best result
    double best_fitness = -1e10;
    size_t best_idx = 0;
    for (size_t i = 0; i < results.size(); ++i) {
        if (results[i].fitness_score > best_fitness) {
            best_fitness = results[i].fitness_score;
            best_idx = i;
        }
    }
    
    std::cout << "\nBest candidate: " << (best_idx + 1) 
              << " (Fitness = " << best_fitness << ")\n";
    
    // Write results to file
    std::ofstream out(output_file);
    out << "{\n";
    out << "  \"batch_results\": [\n";
    for (size_t i = 0; i < results.size(); ++i) {
        out << "    {\n";
        out << "      \"index\": " << i << ",\n";
        out << "      \"fitness\": " << results[i].fitness_score << ",\n";
        out << "      \"molecule\": " << results[i].molecule.to_json() << "\n";
        out << "    }";
        if (i < results.size() - 1) {
            out << ",";
        }
        out << "\n";
    }
    out << "  ]\n";
    out << "}\n";
    out.close();
    
    std::cout << "\nResults written to: " << output_file << "\n";
    
    return 0;
}

