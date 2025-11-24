#include "sdt/simulation/engine.hpp"
#include "sdt/physics/pressure_field.hpp"
#include <algorithm>
#include <iostream>

namespace sdt::simulation {

    SimulationEngine::SimulationEngine(
        SystemState initial_state,
        std::unique_ptr<numerics::Integrator> integrator
    ) : state_(std::move(initial_state)),
        integrator_(std::move(integrator))
    {
        initial_energy_ = state_.calculate_total_energy();
        initial_angular_momentum_ = state_.calculate_angular_momentum();
    }
    
    void SimulationEngine::run_until(time_t end_time, time_t output_interval) {
        while (state_.current_time < end_time) {
            const time_t dt = std::min(
                integrator_->get_current_dt(),
                end_time - state_.current_time
            );
            
            step(dt);
            
            if (output_interval > 0.0 && 
                static_cast<int>(state_.current_time / output_interval) != 
                static_cast<int>((state_.current_time - dt) / output_interval)) {
                
                output_callback_(state_);
            }
        }
    }
    
    void SimulationEngine::step(time_t dt) {
        integrator_->step(state_, dt);
        step_count_++;
        
        // Update conserved quantities
        state_.energy = state_.calculate_total_energy();
        state_.angular_momentum = state_.calculate_angular_momentum();
    }
    
    SystemState SimulationEngine::get_state() const {
        return state_;
    }
    
    void SimulationEngine::set_output_callback(std::function<void(const SystemState&)> callback) {
        output_callback_ = callback;
    }
    
    scalar_t SimulationEngine::get_energy_drift() const {
        const scalar_t current_energy = state_.calculate_total_energy();
        if (std::abs(initial_energy_) > 1e-10) {
            return std::abs((current_energy - initial_energy_) / initial_energy_) * 100.0;
        }
        return 0.0;
    }
    
    scalar_t SimulationEngine::get_angular_momentum_drift() const {
        const scalar_t current_L = state_.calculate_angular_momentum();
        if (std::abs(initial_angular_momentum_) > 1e-10) {
            return std::abs((current_L - initial_angular_momentum_) / initial_angular_momentum_) * 100.0;
        }
        return 0.0;
    }

} // namespace sdt::simulation

