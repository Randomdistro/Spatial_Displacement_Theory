// Symplectic Integrator with Variable Timestep
// Velocity scales with dt, but position updates use fixed visual timestep
// This allows velocity scaling without changing movement per visual frame

import { calculateAcceleration } from './sdt_physics.js';
import * as THREE from 'three';

/**
 * Symplectic integrator (Velocity Verlet variant)
 * 
 * Key behavior:
 * - Physics timestep dt affects acceleration: v_new = v_old + a * dt
 * - Position updates use fixed visual timestep: x_new = x_old + v * dt_visual
 * - This allows velocity scaling without changing movement per visual frame
 * 
 * @param {Array} bodies - Array of celestial bodies
 * @param {number} dt - Physics timestep (affects velocity calculations)
 * @param {number} dt_visual - Visual timestep (affects position updates)
 */
export function integrateStep(bodies, dt, dt_visual) {
    const n = bodies.length;
    
    // Step 1: Half-step velocity update (kick)
    for (let i = 0; i < n; i++) {
        const body = bodies[i];
        const accel = calculateAcceleration(body.position, bodies, i);
        const velocityUpdate = accel.clone().multiplyScalar(0.5 * dt);
        body.velocity.add(velocityUpdate);
    }
    
    // Step 2: Full-step position update (drift)
    // Uses dt_visual to keep visual movement consistent
    for (let i = 0; i < n; i++) {
        const body = bodies[i];
        body.position.add(body.velocity.clone().multiplyScalar(dt_visual));
    }
    
    // Step 3: Recalculate accelerations at new positions
    const new_accels = [];
    for (let i = 0; i < n; i++) {
        const body = bodies[i];
        const accel = calculateAcceleration(body.position, bodies, i);
        new_accels.push(accel);
    }
    
    // Step 4: Half-step velocity update (kick)
    for (let i = 0; i < n; i++) {
        const body = bodies[i];
        const velocityUpdate = new_accels[i].clone().multiplyScalar(0.5 * dt);
        body.velocity.add(velocityUpdate);
    }
}

/**
 * Adaptive timestep integrator
 * Automatically adjusts dt based on system dynamics
 * 
 * @param {Array} bodies - Array of celestial bodies
 * @param {number} dt_max - Maximum timestep
 * @param {number} dt_visual - Visual timestep
 * @returns {number} Actual timestep used
 */
export function integrateStepAdaptive(bodies, dt_max, dt_visual) {
    // Estimate appropriate timestep based on velocities
    let v_max = 0.0;
    for (const body of bodies) {
        const v_mag = body.velocity.length();
        if (v_mag > v_max) {
            v_max = v_mag;
        }
    }
    
    // CFL-like condition: dt < min_distance / max_velocity
    let min_distance = Infinity;
    for (let i = 0; i < bodies.length; i++) {
        for (let j = i + 1; j < bodies.length; j++) {
            const dist = bodies[i].position.distanceTo(bodies[j].position);
            if (dist < min_distance) {
                min_distance = dist;
            }
        }
    }
    
    // Adaptive timestep
    let dt = dt_max;
    if (v_max > 0 && min_distance < Infinity) {
        const dt_cfl = min_distance / (v_max * 10.0);  // Safety factor of 10
        dt = Math.min(dt_max, dt_cfl);
    }
    
    // Ensure minimum timestep
    dt = Math.max(dt, 1.0);
    
    integrateStep(bodies, dt, dt_visual);
    
    return dt;
}

