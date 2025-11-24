#pragma once

#include "sdt/core/types.hpp"
#include "sdt/numerics/integrator.hpp"
#include <memory>
#include <functional>

namespace sdt::simulation {

    // Main simulation engine
    class SimulationEngine {
    public:
        SimulationEngine(
            SystemState initial_state,
            std::unique_ptr<numerics::Integrator> integrator
        );
        
        // Run simulation until end_time
        void run_until(time_t end_time, time_t output_interval = 0.0);
        
        // Run single step
        void step(time_t dt);
        
        // Get current state
        SystemState get_state() const;
        
        // Set output callback (called at intervals)
        void set_output_callback(std::function<void(const SystemState&)> callback);
        
        // Get conservation metrics
        scalar_t get_energy_drift() const;
        scalar_t get_angular_momentum_drift() const;
        
        // Get step count
        size_t get_step_count() const { return step_count_; }
        
    private:
        SystemState state_;
        std::unique_ptr<numerics::Integrator> integrator_;
        std::function<void(const SystemState&)> output_callback_;
        size_t step_count_ = 0;
        scalar_t initial_energy_ = 0.0;
        scalar_t initial_angular_momentum_ = 0.0;
    };

} // namespace sdt::simulation

