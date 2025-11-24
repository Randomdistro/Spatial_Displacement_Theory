#pragma once

#include "constants.hpp"
#include "master_equation.hpp"
#include <Eigen/Dense>
#include <vector>
#include <cmath>

namespace sdt::chemistry {

    using Vec3d = Eigen::Vector3d;
    using Mat3d = Eigen::Matrix3d;

    /**
     * Pressure field calculator for SDT chemistry
     * 
     * Calculates pressure fields, gradients, and forces from occlusion geometry
     */
    class PressureField {
    public:
        /**
         * Calculate occlusion force between two particles
         * 
         * From Phase 1: F = (π/4) P_CMB (R_N² R_e²) / r²
         * 
         * @param R1 Effective occlusion radius of particle 1 (m)
         * @param R2 Effective occlusion radius of particle 2 (m)
         * @param r Distance between particles (m)
         * @param P_pressure Pressure value (Pa), defaults to P_CMB for atomic scale
         * @return Force magnitude (N)
         */
        static double occlusion_force(
            double R1,
            double R2,
            double r,
            double P_pressure = constants::P_CMB
        ) {
            if (r <= 0.0) {
                return 0.0;
            }
            return (constants::pi / 4.0) * P_pressure * (R1 * R1 * R2 * R2) / (r * r);
        }
        
        /**
         * Calculate occlusion force vector (direction from particle 1 to particle 2)
         */
        static Vec3d occlusion_force_vector(
            const Vec3d& pos1,
            const Vec3d& pos2,
            double R1,
            double R2,
            double P_pressure = constants::P_CMB
        ) {
            Vec3d r_vec = pos2 - pos1;
            double r = r_vec.norm();
            if (r <= 0.0) {
                return Vec3d::Zero();
            }
            
            double F_mag = occlusion_force(R1, R2, r, P_pressure);
            return F_mag * r_vec.normalized();
        }
        
        /**
         * Calculate pressure at position from a single source
         * 
         * @param position Position vector (m)
         * @param source_position Source position (m)
         * @param source_radius Source occlusion radius (m)
         * @param P_background Background pressure (Pa)
         * @return Pressure at position (Pa)
         */
        static double pressure_at_position(
            const Vec3d& position,
            const Vec3d& source_position,
            double source_radius,
            double P_background = constants::P_CMB
        ) {
            Vec3d r_vec = position - source_position;
            double r = r_vec.norm();
            
            if (r <= 0.0) {
                return P_background;  // At source, pressure equals background
            }
            
            // Pressure deficit from occlusion
            // Simplified model: ΔP = -P_CMB * (R² / r²) for r >> R
            double pressure_deficit = P_background * (source_radius * source_radius) / (r * r);
            return P_background - pressure_deficit;
        }
        
        /**
         * Calculate pressure gradient at position
         * 
         * @param position Position vector (m)
         * @param source_position Source position (m)
         * @param source_radius Source occlusion radius (m)
         * @param P_background Background pressure (Pa)
         * @return Pressure gradient vector (Pa/m)
         */
        static Vec3d pressure_gradient(
            const Vec3d& position,
            const Vec3d& source_position,
            double source_radius,
            double P_background = constants::P_CMB
        ) {
            Vec3d r_vec = position - source_position;
            double r = r_vec.norm();
            
            if (r <= 0.0) {
                return Vec3d::Zero();
            }
            
            // Gradient magnitude: dP/dr = 2 * P_CMB * (R² / r³)
            double grad_mag = 2.0 * P_background * (source_radius * source_radius) / (r * r * r);
            return grad_mag * r_vec.normalized();
        }
        
        /**
         * Calculate total pressure from multiple sources
         */
        static double total_pressure(
            const Vec3d& position,
            const std::vector<Vec3d>& source_positions,
            const std::vector<double>& source_radii,
            double P_background = constants::P_CMB
        ) {
            double total_p = P_background;
            
            for (size_t i = 0; i < source_positions.size(); ++i) {
                Vec3d r_vec = position - source_positions[i];
                double r = r_vec.norm();
                
                if (r > 0.0 && i < source_radii.size()) {
                    double pressure_deficit = P_background * (source_radii[i] * source_radii[i]) / (r * r);
                    total_p -= pressure_deficit;
                }
            }
            
            return total_p;
        }
        
        /**
         * Calculate mutual occlusion factor (screening effect)
         * 
         * @param R1 Radius of particle 1 (m)
         * @param R2 Radius of particle 2 (m)
         * @param r Distance between particles (m)
         * @return Occlusion factor (0 to 1)
         */
        static double mutual_occlusion_factor(double R1, double R2, double r) {
            if (r <= 0.0) {
                return 1.0;  // Full occlusion when overlapping
            }
            
            double R_combined = R1 + R2;
            if (r < R_combined) {
                return 1.0;  // Full occlusion
            }
            
            // Solid angle fraction: Ω / 4π ≈ (π R²) / (4π r²) = R² / (4r²)
            double solid_angle_fraction = (R_combined * R_combined) / (4.0 * r * r);
            return std::max(0.0, std::min(1.0, solid_angle_fraction));
        }
        
        /**
         * Calculate bond energy from pressure field integration
         * 
         * @param R1 Effective radius of atom 1 (m)
         * @param R2 Effective radius of atom 2 (m)
         * @param r_bond Bond length (m)
         * @param P_pressure Pressure value (Pa)
         * @return Bond energy (J)
         */
        static double bond_energy(
            double R1,
            double R2,
            double r_bond,
            double P_pressure = constants::P_CMB
        ) {
            if (r_bond <= 0.0) {
                return 0.0;
            }
            
            // Energy = ∫ F dr from r_bond to infinity
            // F = (π/4) P (R1² R2²) / r²
            // E = (π/4) P (R1² R2²) / r_bond
            return (constants::pi / 4.0) * P_pressure * (R1 * R1 * R2 * R2) / r_bond;
        }
        
        /**
         * Calculate bond energy in eV
         */
        static double bond_energy_eV(
            double R1,
            double R2,
            double r_bond,
            double P_pressure = constants::P_CMB
        ) {
            return bond_energy(R1, R2, r_bond, P_pressure) * constants::J_to_eV;
        }
        
        /**
         * Calculate bond energy per mole (kJ/mol)
         */
        static double bond_energy_kJ_per_mol(
            double R1,
            double R2,
            double r_bond,
            double P_pressure = constants::P_CMB
        ) {
            double E_J = bond_energy(R1, R2, r_bond, P_pressure);
            double E_per_molecule_J = E_J;  // Energy per molecule
            double E_per_mol_J = E_per_molecule_J * constants::N_A;
            return E_per_mol_J / 1000.0;  // Convert to kJ/mol
        }
    };

} // namespace sdt::chemistry

