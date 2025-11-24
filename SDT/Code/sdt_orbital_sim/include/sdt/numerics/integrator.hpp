#pragma once

#include "sdt/core/types.hpp"
#include "sdt/physics/pressure_field.hpp"
#include <functional>
#include <vector>
#include <memory>

namespace sdt::numerics {

    // Base class for numerical integrators
    class Integrator {
    public:
        virtual ~Integrator() = default;
        
        // Integrate one step
        virtual void step(SystemState& state, time_t dt) = 0;
        
        // Get current time step (adaptive integrators)
        virtual time_t get_current_dt() const { return dt_; }
        
        // Set time step
        virtual void set_dt(time_t dt) { dt_ = dt; }
        
        // Get error estimate (for adaptive integrators)
        virtual scalar_t get_error_estimate() const { return 0.0; }
        
    protected:
        time_t dt_ = 1.0;  // Default time step (seconds)
    };
    
    // 4th-order Runge-Kutta integrator (RK4)
    class RK4Integrator : public Integrator {
    public:
        void step(SystemState& state, time_t dt) override {
            const size_t n = state.bodies.size();
            
            // Store initial state
            std::vector<Vec3d> k1_v(n), k2_v(n), k3_v(n), k4_v(n);
            std::vector<Vec3d> k1_a(n), k2_a(n), k3_a(n), k4_a(n);
            
            // k1: Evaluate at current state
            for (size_t i = 0; i < n; ++i) {
                k1_v[i] = state.bodies[i].velocity;
                k1_a[i] = physics::PressureField::net_acceleration(
                    state.bodies[i].position,
                    state.bodies,
                    i
                );
            }
            
            // k2: Evaluate at midpoint with k1
            SystemState state_k2 = state;
            for (size_t i = 0; i < n; ++i) {
                state_k2.bodies[i].position += 0.5 * dt * k1_v[i];
                state_k2.bodies[i].velocity += 0.5 * dt * k1_a[i];
            }
            
            for (size_t i = 0; i < n; ++i) {
                k2_v[i] = state_k2.bodies[i].velocity;
                k2_a[i] = physics::PressureField::net_acceleration(
                    state_k2.bodies[i].position,
                    state_k2.bodies,
                    i
                );
            }
            
            // k3: Evaluate at midpoint with k2
            SystemState state_k3 = state;
            for (size_t i = 0; i < n; ++i) {
                state_k3.bodies[i].position += 0.5 * dt * k2_v[i];
                state_k3.bodies[i].velocity += 0.5 * dt * k2_a[i];
            }
            
            for (size_t i = 0; i < n; ++i) {
                k3_v[i] = state_k3.bodies[i].velocity;
                k3_a[i] = physics::PressureField::net_acceleration(
                    state_k3.bodies[i].position,
                    state_k3.bodies,
                    i
                );
            }
            
            // k4: Evaluate at endpoint with k3
            SystemState state_k4 = state;
            for (size_t i = 0; i < n; ++i) {
                state_k4.bodies[i].position += dt * k3_v[i];
                state_k4.bodies[i].velocity += dt * k3_a[i];
            }
            
            for (size_t i = 0; i < n; ++i) {
                k4_v[i] = state_k4.bodies[i].velocity;
                k4_a[i] = physics::PressureField::net_acceleration(
                    state_k4.bodies[i].position,
                    state_k4.bodies,
                    i
                );
            }
            
            // Combine k1, k2, k3, k4
            for (size_t i = 0; i < n; ++i) {
                state.bodies[i].position += (dt / 6.0) * (
                    k1_v[i] + 2.0 * k2_v[i] + 2.0 * k3_v[i] + k4_v[i]
                );
                state.bodies[i].velocity += (dt / 6.0) * (
                    k1_a[i] + 2.0 * k2_a[i] + 2.0 * k3_a[i] + k4_a[i]
                );
            }
            
            state.current_time += dt;
        }
    };
    
    // Adaptive Runge-Kutta-Fehlberg (RKF45) integrator
    class AdaptiveRK45Integrator : public Integrator {
    public:
        AdaptiveRK45Integrator(
            scalar_t tolerance = 1e-9,
            scalar_t min_dt = 1e-6,
            scalar_t max_dt = 86400.0  // 1 day max
        ) : tolerance_(tolerance), min_dt_(min_dt), max_dt_(max_dt) {}
        
        void step(SystemState& state, time_t dt_attempt) override {
            SystemState state_backup = state;
            
            // Use RK4 as base method
            RK4Integrator rk4;
            rk4.step(state, dt_attempt);
            
            // Estimate error (simplified - use position change)
            scalar_t max_error = 0.0;
            for (size_t i = 0; i < state.bodies.size(); ++i) {
                const scalar_t pos_change = (state.bodies[i].position - 
                                            state_backup.bodies[i].position).norm();
                max_error = std::max(max_error, pos_change);
            }
            
            // Adjust time step based on error
            if (max_error > tolerance_) {
                // Error too large - reduce step size
                dt_ = std::max(min_dt_, dt_attempt * 0.8);
                state = state_backup;  // Revert
                step(state, dt_);  // Try again with smaller step
            } else {
                // Error acceptable
                dt_ = std::min(max_dt_, dt_attempt * 1.2);
            }
            
            error_estimate_ = max_error;
        }
        
        scalar_t get_error_estimate() const override {
            return error_estimate_;
        }
        
        time_t get_current_dt() const override {
            return dt_;
        }
        
    private:
        scalar_t tolerance_;
        scalar_t min_dt_;
        scalar_t max_dt_;
        scalar_t error_estimate_ = 0.0;
    };
    
    // Symplectic (energy-conserving) integrator
    class SymplecticIntegrator : public Integrator {
    public:
        void step(SystemState& state, time_t dt) override {
            const size_t n = state.bodies.size();
            
            // Velocity Verlet-like update for pressure field forces
            // Half-step velocity update
            for (size_t i = 0; i < n; ++i) {
                const Vec3d accel = physics::PressureField::net_acceleration(
                    state.bodies[i].position,
                    state.bodies,
                    i
                );
                state.bodies[i].velocity += 0.5 * dt * accel;
            }
            
            // Full-step position update
            for (size_t i = 0; i < n; ++i) {
                state.bodies[i].position += dt * state.bodies[i].velocity;
            }
            
            // Half-step velocity update
            for (size_t i = 0; i < n; ++i) {
                const Vec3d accel = physics::PressureField::net_acceleration(
                    state.bodies[i].position,
                    state.bodies,
                    i
                );
                state.bodies[i].velocity += 0.5 * dt * accel;
            }
            
            state.current_time += dt;
        }
    };

} // namespace sdt::numerics

