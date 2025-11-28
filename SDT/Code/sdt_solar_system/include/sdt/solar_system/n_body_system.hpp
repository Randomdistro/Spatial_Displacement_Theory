#pragma once

#include "integrator.hpp"
#include "data_loader.hpp"
#include <memory>
#include <functional>
#include <fstream>
#include <cmath>

namespace sdt::solar_system {

    // Main n-body simulation system
    class NBodySystem {
    public:
        NBodySystem(
            SystemState initial_state,
            std::unique_ptr<Integrator> integrator
        ) : state_(std::move(initial_state)), integrator_(std::move(integrator)) {
            // Calculate initial energy and angular momentum
            initial_energy_ = state_.calculate_total_energy();
            initial_angular_momentum_ = state_.calculate_angular_momentum_magnitude();
        }
        
        // Run simulation until end_time
        void run_until(time_t end_time, time_t output_interval = 0.0) {
            const time_t start_time = state_.current_time;
            time_t last_output_time = start_time;
            
            size_t step_count = 0;
            const size_t progress_interval = 10000;  // Print progress every N steps
            
            while (state_.current_time < end_time) {
                // Calculate time step
                time_t dt = integrator_->get_current_dt();
                if (state_.current_time + dt > end_time) {
                    dt = end_time - state_.current_time;
                }
                
                // Integrate one step
                integrator_->step(state_, dt);
                step_count++;
                
                // Update energy and angular momentum
                state_.total_energy = state_.calculate_total_energy();
                state_.total_angular_momentum = state_.calculate_angular_momentum_magnitude();
                
                // Output callback
                if (output_interval > 0.0 && 
                    state_.current_time - last_output_time >= output_interval) {
                    if (output_callback_) {
                        output_callback_(state_);
                    }
                    last_output_time = state_.current_time;
                }
                
                // Progress reporting
                if (step_count % progress_interval == 0) {
                    const time_t elapsed = state_.current_time - start_time;
                    const time_t remaining = end_time - state_.current_time;
                    const double progress = 100.0 * (state_.current_time - start_time) / 
                                         (end_time - start_time);
                    
                    // Calculate energy drift
                    const scalar_t energy_drift = std::abs(
                        (state_.total_energy - initial_energy_) / initial_energy_
                    ) * 100.0;
                    
                    // Print progress (can be redirected to log file)
                    // std::cout << fmt::format(
                    //     "Time: {:.2e} s, Progress: {:.2f}%, Energy drift: {:.6f}%, Steps: {}\n",
                    //     state_.current_time, progress, energy_drift, step_count
                    // );
                }
            }
        }
        
        // Run single step
        void step(time_t dt) {
            integrator_->step(state_, dt);
            state_.total_energy = state_.calculate_total_energy();
            state_.total_angular_momentum = state_.calculate_angular_momentum_magnitude();
        }
        
        // Get current state
        const SystemState& get_state() const {
            return state_;
        }
        
        SystemState& get_state() {
            return state_;
        }
        
        // Set output callback (called at intervals)
        void set_output_callback(std::function<void(const SystemState&)> callback) {
            output_callback_ = callback;
        }
        
        // Get conservation metrics
        scalar_t get_energy_drift() const {
            if (std::abs(initial_energy_) < 1e-10) {
                return 0.0;
            }
            return std::abs((state_.total_energy - initial_energy_) / initial_energy_) * 100.0;
        }
        
        scalar_t get_angular_momentum_drift() const {
            if (std::abs(initial_angular_momentum_) < 1e-10) {
                return 0.0;
            }
            return std::abs((state_.total_angular_momentum - initial_angular_momentum_) / 
                          initial_angular_momentum_) * 100.0;
        }
        
        // Get step count
        size_t get_step_count() const {
            return step_count_;
        }
        
        // Save trajectory to file
        void save_trajectory(const std::string& filename, time_t interval = 86400.0) const {
            // This would save trajectory data
            // Implementation depends on format requirements
        }
        
    private:
        SystemState state_;
        std::unique_ptr<Integrator> integrator_;
        std::function<void(const SystemState&)> output_callback_;
        size_t step_count_ = 0;
        scalar_t initial_energy_ = 0.0;
        scalar_t initial_angular_momentum_ = 0.0;
    };

} // namespace sdt::solar_system

