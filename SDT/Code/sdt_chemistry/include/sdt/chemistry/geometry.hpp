#pragma once

#include "molecules.hpp"
#include "pressure_field.hpp"
#include <Eigen/Dense>
#include <vector>
#include <optional>

namespace sdt::chemistry {

    /**
     * Geometry optimization using pressure field minimization
     */
    class GeometryOptimizer {
    public:
        struct OptimizationResult {
            bool converged;
            int iterations;
            double final_energy;
            double energy_change;
            std::vector<std::string> messages;
        };
        
        /**
         * Optimize molecular geometry using pressure field energy minimization
         * 
         * Uses gradient descent on pressure field energy
         */
        static OptimizationResult optimize(
            Molecule& molecule,
            double tolerance = 1e-6,
            int max_iterations = 1000,
            double step_size = 0.01
        );
        
        /**
         * Optimize bond lengths only
         */
        static OptimizationResult optimize_bond_lengths(
            Molecule& molecule,
            double tolerance = 1e-6,
            int max_iterations = 100
        );
        
        /**
         * Optimize bond angles
         */
        static OptimizationResult optimize_angles(
            Molecule& molecule,
            double tolerance = 1e-6,
            int max_iterations = 100
        );
        
        /**
         * Calculate energy gradient with respect to atom positions
         */
        static std::vector<Vec3d> energy_gradient(const Molecule& molecule);
        
        /**
         * Calculate force on each atom from pressure field
         */
        static std::vector<Vec3d> calculate_forces(const Molecule& molecule);
        
        /**
         * Minimize energy using conjugate gradient method
         */
        static OptimizationResult conjugate_gradient(
            Molecule& molecule,
            double tolerance = 1e-6,
            int max_iterations = 1000
        );
        
    private:
        static double line_search(
            Molecule& molecule,
            const std::vector<Vec3d>& direction,
            double initial_step = 1.0
        );
    };

} // namespace sdt::chemistry

