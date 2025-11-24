#pragma once

#include "constants.hpp"
#include <cmath>

namespace sdt::chemistry {

    /**
     * Master Equation: Ė = P_∞ · A_eff · Γ · κ · (1-η)
     * 
     * This is the fundamental equation for power throughput in the spation medium.
     * Scale-dependent pressure values:
     * - Atomic/Molecular scale: P_CMB = 2.036e-2 Pa
     * - Nuclear scale: P_∞ = 1.65e31 Pa (toroidal geometry)
     */
    class MasterEquation {
    public:
        /**
         * Calculate power throughput using master equation
         * 
         * @param P_infinity Spation pressure (Pa) - scale-dependent
         * @param A_eff Effective capture area (m²)
         * @param Gamma Circulation factor (v_pol/c), dimensionless
         * @param kappa Curvature (1/r_minor), m⁻¹
         * @param traction (1-η), dimensionless, 0 to 1
         * @return Power throughput (W)
         */
        static double calculate_power_throughput(
            double P_infinity,
            double A_eff,
            double Gamma,
            double kappa,
            double traction
        ) {
            return P_infinity * A_eff * Gamma * kappa * traction;
        }
        
        /**
         * Calculate power throughput for proton (nuclear scale)
         */
        static double proton_power_throughput() {
            using namespace constants;
            return calculate_power_throughput(
                P_infinity_nuclear,
                A_eff_proton,
                Gamma_proton,
                kappa_proton,
                traction_proton
            );
        }
        
        /**
         * Calculate power throughput for electron (nuclear scale, free)
         */
        static double electron_power_throughput() {
            using namespace constants;
            return calculate_power_throughput(
                P_infinity_nuclear,
                A_eff_electron,
                Gamma_electron,
                kappa_electron,
                traction_electron_free
            );
        }
        
        /**
         * Calculate energy from power throughput and characteristic time
         * 
         * @param power_throughput Power (W)
         * @param characteristic_time Characteristic time (s)
         * @return Energy (J)
         */
        static double energy_from_power(double power_throughput, double characteristic_time) {
            return power_throughput * characteristic_time;
        }
        
        /**
         * Calculate characteristic time from radius
         * 
         * @param radius Characteristic radius (m)
         * @return Characteristic time (s) = radius / c
         */
        static double characteristic_time(double radius) {
            return radius / constants::c;
        }
        
        /**
         * Calculate binding energy from traction change
         * 
         * @param E_iso Isolated energy (J)
         * @param delta_traction Change in traction (1-η)
         * @return Binding energy (J)
         */
        static double binding_energy_from_traction(double E_iso, double delta_traction) {
            return E_iso * delta_traction;
        }
        
        /**
         * Calculate effective capture area for spherical geometry
         * 
         * @param radius Radius (m)
         * @return Capture area (m²) = π * radius²
         */
        static double spherical_capture_area(double radius) {
            return constants::pi * radius * radius;
        }
        
        /**
         * Calculate effective capture area for toroidal geometry
         * 
         * @param R_major Major radius (m)
         * @param r_minor Minor radius (m)
         * @return Capture area (m²) ≈ 2π² R_major r_minor
         */
        static double toroidal_capture_area(double R_major, double r_minor) {
            return 2.0 * constants::pi * constants::pi * R_major * r_minor;
        }
        
        /**
         * Calculate curvature for toroidal geometry
         * 
         * @param r_minor Minor radius (m)
         * @return Curvature (m⁻¹) = 1/r_minor
         */
        static double toroidal_curvature(double r_minor) {
            if (r_minor <= 0.0) {
                return 0.0;
            }
            return 1.0 / r_minor;
        }
        
        /**
         * Calculate circulation factor from velocity
         * 
         * @param velocity Velocity (m/s)
         * @return Circulation factor = velocity / c
         */
        static double circulation_factor(double velocity) {
            return velocity / constants::c;
        }
    };

} // namespace sdt::chemistry

