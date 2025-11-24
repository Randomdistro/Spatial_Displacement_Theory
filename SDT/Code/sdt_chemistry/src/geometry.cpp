#include "sdt/chemistry/geometry.hpp"
#include <algorithm>
#include <cmath>

namespace sdt::chemistry {

    GeometryOptimizer::OptimizationResult GeometryOptimizer::optimize(
        Molecule& molecule,
        double tolerance,
        int max_iterations,
        double step_size
    ) {
        OptimizationResult result;
        result.converged = false;
        result.iterations = 0;
        
        double E_prev = molecule.total_energy();
        result.final_energy = E_prev;
        
        for (int iter = 0; iter < max_iterations; ++iter) {
            // Calculate forces
            std::vector<Vec3d> forces = calculate_forces(molecule);
            
            // Update positions
            bool moved = false;
            for (size_t i = 0; i < molecule.num_atoms(); ++i) {
                Vec3d force = forces[i];
                double force_mag = force.norm();
                
                if (force_mag > tolerance) {
                    // Move atom in direction of force (minimize energy)
                    Vec3d direction = force.normalized();
                    Vec3d displacement = -step_size * direction * force_mag;
                    Vec3d new_pos = molecule.atom(i).position + displacement;
                    molecule.set_atom_position(i, new_pos);
                    moved = true;
                }
            }
            
            if (!moved) {
                result.converged = true;
                result.iterations = iter + 1;
                break;
            }
            
            // Check convergence
            double E_new = molecule.total_energy();
            result.energy_change = std::abs(E_new - E_prev);
            
            if (result.energy_change < tolerance) {
                result.converged = true;
                result.iterations = iter + 1;
                result.final_energy = E_new;
                break;
            }
            
            E_prev = E_new;
            result.iterations = iter + 1;
        }
        
        result.final_energy = molecule.total_energy();
        
        if (!result.converged) {
            result.messages.push_back("Optimization did not converge");
        }
        
        return result;
    }

    GeometryOptimizer::OptimizationResult GeometryOptimizer::optimize_bond_lengths(
        Molecule& molecule,
        double tolerance,
        int max_iterations
    ) {
        OptimizationResult result;
        result.converged = false;
        result.iterations = 0;
        
        for (int iter = 0; iter < max_iterations; ++iter) {
            bool changed = false;
            
            for (size_t i = 0; i < molecule.num_bonds(); ++i) {
                Bond& bond = molecule.bond(i);
                
                // Calculate optimal bond length from SDT
                const ElementData& elem1 = molecule.atom(bond.atom1_index).element_data();
                const ElementData& elem2 = molecule.atom(bond.atom2_index).element_data();
                
                double r_optimal_pm = Bonds::covalent_bond_length(elem1, elem2, bond.bond_order);
                double r_current_pm = bond.length_pm;
                
                if (std::abs(r_optimal_pm - r_current_pm) > tolerance) {
                    molecule.update_bond_length(i, r_optimal_pm);
                    changed = true;
                }
            }
            
            if (!changed) {
                result.converged = true;
                result.iterations = iter + 1;
                break;
            }
            
            result.iterations = iter + 1;
        }
        
        result.final_energy = molecule.total_energy();
        return result;
    }

    GeometryOptimizer::OptimizationResult GeometryOptimizer::optimize_angles(
        Molecule& molecule,
        double tolerance,
        int max_iterations
    ) {
        // Simplified angle optimization
        // TODO: Implement full angle optimization
        OptimizationResult result;
        result.converged = true;
        result.iterations = 0;
        result.final_energy = molecule.total_energy();
        return result;
    }

    std::vector<Vec3d> GeometryOptimizer::energy_gradient(const Molecule& molecule) {
        return calculate_forces(molecule);
    }

    std::vector<Vec3d> GeometryOptimizer::calculate_forces(const Molecule& molecule) {
        std::vector<Vec3d> forces(molecule.num_atoms(), Vec3d::Zero());
        
        // Forces from bonds
        for (size_t i = 0; i < molecule.num_bonds(); ++i) {
            const Bond& bond = molecule.bond(i);
            const Atom& atom1 = molecule.atom(bond.atom1_index);
            const Atom& atom2 = molecule.atom(bond.atom2_index);
            
            Vec3d r_vec = atom2.position - atom1.position;
            double r = r_vec.norm();
            
            if (r > 0.0) {
                // Calculate force from pressure field
                Vec3d force = PressureField::occlusion_force_vector(
                    atom1.position,
                    atom2.position,
                    bond.occlusion_radius1_m,
                    bond.occlusion_radius2_m
                );
                
                forces[bond.atom1_index] -= force;
                forces[bond.atom2_index] += force;
            }
        }
        
        // Forces from non-bonded interactions
        for (size_t i = 0; i < molecule.num_atoms(); ++i) {
            for (size_t j = i + 1; j < molecule.num_atoms(); ++j) {
                if (!molecule.are_bonded(i, j)) {
                    const Atom& atom1 = molecule.atom(i);
                    const Atom& atom2 = molecule.atom(j);
                    
                    Vec3d force = PressureField::occlusion_force_vector(
                        atom1.position,
                        atom2.position,
                        atom1.effective_radius_m,
                        atom2.effective_radius_m
                    );
                    
                    // Van der Waals is much weaker
                    force *= 0.1;
                    
                    forces[i] -= force;
                    forces[j] += force;
                }
            }
        }
        
        return forces;
    }

    GeometryOptimizer::OptimizationResult GeometryOptimizer::conjugate_gradient(
        Molecule& molecule,
        double tolerance,
        int max_iterations
    ) {
        OptimizationResult result;
        result.converged = false;
        result.iterations = 0;
        
        // Simplified conjugate gradient
        // Use basic gradient descent for now
        return optimize(molecule, tolerance, max_iterations, 0.01);
    }

    double GeometryOptimizer::line_search(
        Molecule& molecule,
        const std::vector<Vec3d>& direction,
        double initial_step
    ) {
        // Simplified line search
        return initial_step;
    }

} // namespace sdt::chemistry

