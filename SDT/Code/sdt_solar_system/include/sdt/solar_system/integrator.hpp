#pragma once

#include "celestial_body.hpp"
#include "pressure_field.hpp"
#include "occlusion.hpp"
#include "constants.hpp"
#include <vector>
#include <cmath>
#include <limits>

namespace sdt::solar_system {

    // System state for n-body simulation
    struct SystemState {
        std::vector<CelestialBody> bodies;
        time_t current_time = 0.0;
        scalar_t total_energy = 0.0;
        scalar_t total_angular_momentum = 0.0;
        
        // Calculate total energy (kinetic + potential from pressure fields)
        scalar_t calculate_total_energy() const {
            scalar_t E = 0.0;
            
            // Kinetic energy: E_k = ½ m v²
            for (const auto& body : bodies) {
                if (body.mass_conv > 0.0) {
                    E += 0.5 * body.mass_conv * body.velocity.squaredNorm();
                }
            }
            
            // Potential energy from pressure gradients
            // From Phase 15: E_pot = -β ρ_s / r for each pair
            for (size_t i = 0; i < bodies.size(); ++i) {
                for (size_t j = i + 1; j < bodies.size(); ++j) {
                    const Vec3d r_vec = bodies[j].position - bodies[i].position;
                    const scalar_t r = r_vec.norm();
                    if (r > 0.0) {
                        // Effective beta for pair interaction
                        const scalar_t beta_i = bodies[i].sdt_params.beta();
                        const scalar_t beta_j = bodies[j].sdt_params.beta();
                        const scalar_t beta_eff = std::sqrt(beta_i * beta_j);
                        
                        // Potential energy: E_pot = -β_eff ρ_s / r
                        E -= beta_eff * constants::rho_s / r;
                    }
                }
            }
            
            return E;
        }
        
        // Calculate total angular momentum
        Vec3d calculate_angular_momentum_vector() const {
            Vec3d L_total = Vec3d::Zero();
            for (const auto& body : bodies) {
                if (body.mass_conv > 0.0) {
                    L_total += body.mass_conv * body.position.cross(body.velocity);
                }
            }
            return L_total;
        }
        
        scalar_t calculate_angular_momentum_magnitude() const {
            return calculate_angular_momentum_vector().norm();
        }
    };

    // Base integrator interface
    class Integrator {
    public:
        virtual ~Integrator() = default;
        
        // Integrate one step
        virtual void step(SystemState& state, time_t dt) = 0;
        
        // Get current time step (for adaptive integrators)
        virtual time_t get_current_dt() const { return dt_; }
        
        // Set time step
        virtual void set_dt(time_t dt) { dt_ = dt; }
        
        // Get error estimate (for adaptive integrators)
        virtual scalar_t get_error_estimate() const { return 0.0; }
        
    protected:
        time_t dt_ = constants::default_timestep;
    };

    // Symplectic (energy-conserving) Leapfrog integrator
    // Best for long-term stability in billion-year simulations
    class SymplecticIntegrator : public Integrator {
    public:
        SymplecticIntegrator(bool use_occlusion = false)
            : use_occlusion_(use_occlusion) {}
        
        void step(SystemState& state, time_t dt) override {
            const size_t n = state.bodies.size();
            
            // Half-step velocity update (kick)
            for (size_t i = 0; i < n; ++i) {
                // Skip Sun (fixed at origin)
                if (state.bodies[i].name == "Sun") continue;
                
                Vec3d accel;
                if (use_occlusion_) {
                    accel = Occlusion::occlusion_corrected_acceleration(
                        state.bodies[i].position,
                        state.bodies,
                        i
                    );
                } else {
                    accel = PressureField::net_acceleration(
                        state.bodies[i].position,
                        state.bodies,
                        i
                    );
                }
                state.bodies[i].velocity += 0.5 * dt * accel;
            }
            
            // Full-step position update (drift)
            for (size_t i = 0; i < n; ++i) {
                // Skip Sun (fixed at origin)
                if (state.bodies[i].name == "Sun") continue;
                
                state.bodies[i].position += dt * state.bodies[i].velocity;
            }
            
            // Half-step velocity update (kick)
            for (size_t i = 0; i < n; ++i) {
                // Skip Sun (fixed at origin)
                if (state.bodies[i].name == "Sun") continue;
                
                Vec3d accel;
                if (use_occlusion_) {
                    accel = Occlusion::occlusion_corrected_acceleration(
                        state.bodies[i].position,
                        state.bodies,
                        i
                    );
                } else {
                    accel = PressureField::net_acceleration(
                        state.bodies[i].position,
                        state.bodies,
                        i
                    );
                }
                state.bodies[i].velocity += 0.5 * dt * accel;
            }
            
            state.current_time += dt;
        }
        
    private:
        bool use_occlusion_;
    };

    // Adaptive symplectic integrator
    // Adjusts time step based on close encounters
    class AdaptiveSymplecticIntegrator : public Integrator {
    public:
        AdaptiveSymplecticIntegrator(
            scalar_t tolerance = 1e-9,
            scalar_t min_dt = constants::min_timestep,
            scalar_t max_dt = constants::max_timestep,
            bool use_occlusion = false
        ) : tolerance_(tolerance), min_dt_(min_dt), max_dt_(max_dt),
            use_occlusion_(use_occlusion) {}
        
        void step(SystemState& state, time_t dt_attempt) override {
            dt_ = dt_attempt;  // Use attempted time step
            
            // Calculate minimum separation to determine appropriate time step
            scalar_t min_separation = std::numeric_limits<scalar_t>::max();
            for (size_t i = 0; i < state.bodies.size(); ++i) {
                for (size_t j = i + 1; j < state.bodies.size(); ++j) {
                    const scalar_t r = state.bodies[i].distance_to(state.bodies[j]);
                    min_separation = std::min(min_separation, r);
                }
            }
            
            // Adaptive time step: smaller for close encounters
            // Use a fraction of the orbital period at minimum separation
            time_t adaptive_dt = dt_attempt;
            if (min_separation < 1.0e12) {  // Within 1 AU
                // Estimate orbital period at this separation
                // T ≈ 2π √(r³ / (c² R_eff / Ϟ²))
                // Use Sun's parameters as reference
                const scalar_t c = 299792458.0;
                const scalar_t R_sun = 6.957e8;
                const scalar_t kappa_sun = 686.42;
                const scalar_t beta_sun = (c * c * R_sun) / (kappa_sun * kappa_sun);
                
                // Estimate period: T ≈ 2π √(r³ / β)
                const scalar_t estimated_period = 2.0 * constants::pi * 
                    std::sqrt(min_separation * min_separation * min_separation / beta_sun);
                
                // Use 1/1000 of period as time step
                adaptive_dt = std::min(dt_attempt, estimated_period / 1000.0);
                adaptive_dt = std::max(min_dt_, std::min(max_dt_, adaptive_dt));
            }
            
            // Use symplectic integrator with adaptive time step
            SymplecticIntegrator symplectic(use_occlusion_);
            symplectic.step(state, adaptive_dt);
            
            dt_ = adaptive_dt;
            error_estimate_ = 0.0;  // Symplectic integrators don't provide error estimates
        }
        
        time_t get_current_dt() const override {
            return dt_;
        }
        
    private:
        scalar_t tolerance_;
        time_t min_dt_;
        time_t max_dt_;
        bool use_occlusion_;
        scalar_t error_estimate_ = 0.0;
    };

} // namespace sdt::solar_system

