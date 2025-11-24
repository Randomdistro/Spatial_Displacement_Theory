#pragma once

#include "sdt/core/types.hpp"
#include <vector>
#include <string>
#include <cmath>

namespace sdt::analysis {

    // Validation metrics
    struct ValidationMetrics {
        scalar_t period_error = 0.0;           // % error in orbital period
        scalar_t velocity_error = 0.0;         // % error in orbital velocity
        scalar_t energy_conservation = 0.0;    // Relative energy change
        scalar_t angular_momentum_conservation = 0.0;  // Relative L change
        scalar_t max_position_error = 0.0;     // Maximum position deviation (m)
        scalar_t rms_position_error = 0.0;     // RMS position error (m)
    };
    
    // Validator for comparing simulation results with observations
    class SystemValidator {
    public:
        // Validate orbital periods against observations
        static std::vector<ValidationMetrics> validate_orbital_periods(
            const SystemState& simulated,
            const SystemState& observed
        ) {
            std::vector<ValidationMetrics> metrics;
            
            if (simulated.bodies.size() != observed.bodies.size()) {
                return metrics;  // Cannot validate
            }
            
            // Assume first body is primary (star)
            if (simulated.bodies.empty() || observed.bodies.empty()) {
                return metrics;
            }
            
            const auto& primary = simulated.bodies[0];
            
            for (size_t i = 1; i < simulated.bodies.size(); ++i) {
                ValidationMetrics m;
                
                // Calculate orbital period for simulated body
                const Vec3d r_sim = simulated.bodies[i].position - primary.position;
                const scalar_t r_sim_mag = r_sim.norm();
                const scalar_t T_sim = primary.sdt_params.orbital_period(r_sim_mag);
                
                // Get observed period (from observed state or stored value)
                const Vec3d r_obs = observed.bodies[i].position - observed.bodies[0].position;
                const scalar_t r_obs_mag = r_obs.norm();
                const scalar_t T_obs = observed.bodies[0].sdt_params.orbital_period(r_obs_mag);
                
                // Calculate error
                if (T_obs > 0.0) {
                    m.period_error = std::abs((T_sim - T_obs) / T_obs) * 100.0;
                }
                
                // Calculate velocity error
                const scalar_t v_sim = simulated.bodies[i].velocity.norm();
                const scalar_t v_obs = observed.bodies[i].velocity.norm();
                if (v_obs > 0.0) {
                    m.velocity_error = std::abs((v_sim - v_obs) / v_obs) * 100.0;
                }
                
                // Position errors
                const Vec3d pos_error = r_sim - r_obs;
                m.max_position_error = pos_error.norm();
                m.rms_position_error = m.max_position_error;  // Simplified
                
                metrics.push_back(m);
            }
            
            return metrics;
        }
        
        // Validate energy conservation
        static ValidationMetrics validate_energy_conservation(
            const SystemState& initial,
            const SystemState& current
        ) {
            ValidationMetrics m;
            
            const scalar_t E_initial = initial.energy;
            const scalar_t E_current = current.calculate_total_energy();
            
            if (std::abs(E_initial) > 1e-10) {
                m.energy_conservation = std::abs((E_current - E_initial) / E_initial) * 100.0;
            }
            
            const scalar_t L_initial = initial.angular_momentum;
            const scalar_t L_current = current.calculate_angular_momentum();
            
            if (std::abs(L_initial) > 1e-10) {
                m.angular_momentum_conservation = std::abs((L_current - L_initial) / L_initial) * 100.0;
            }
            
            return m;
        }
        
        // Generate validation report
        static std::string generate_report(
            const std::vector<ValidationMetrics>& metrics,
            const std::vector<std::string>& body_names
        ) {
            std::stringstream ss;
            ss << "=== SDT Orbital Simulation Validation Report ===\n\n";
            
            for (size_t i = 0; i < metrics.size() && i < body_names.size(); ++i) {
                ss << "Body: " << body_names[i] << "\n";
                ss << "  Period Error: " << metrics[i].period_error << " %\n";
                ss << "  Velocity Error: " << metrics[i].velocity_error << " %\n";
                ss << "  Position Error: " << metrics[i].max_position_error << " m\n";
                ss << "\n";
            }
            
            return ss.str();
        }
    };

} // namespace sdt::analysis

