// Energy and Momentum Conservation Validation
// Monitors conservation to ensure simulation accuracy

import * as THREE from 'three';

/**
 * Calculate total energy of the system
 * E = Σ (1/2 m v²) + Σ Σ (-β / r) for pairs
 * 
 * @param {Array} bodies - Array of celestial bodies
 * @returns {number} Total energy (J)
 */
export function calculateTotalEnergy(bodies) {
    let kinetic = 0.0;
    let potential = 0.0;
    
    // Kinetic energy: E_k = 1/2 m v²
    for (const body of bodies) {
        const v_sq = body.velocity.lengthSq();
        // Use conventional mass for energy calculation
        const m = body.mass_conv || estimateMass(body);
        kinetic += 0.5 * m * v_sq;
    }
    
    // Potential energy: E_p = -Σ Σ β / r (for pairs)
    for (let i = 0; i < bodies.length; i++) {
        for (let j = i + 1; j < bodies.length; j++) {
            const r = bodies[i].position.distanceTo(bodies[j].position);
            if (r > 0.0) {
                // Use the primary body's beta for potential
                const beta = bodies[j].sdt_params.beta();
                potential -= beta / r;
            }
        }
    }
    
    return kinetic + potential;
}

/**
 * Calculate total angular momentum of the system
 * L = Σ (r × m v)
 * 
 * @param {Array} bodies - Array of celestial bodies
 * @returns {THREE.Vector3} Total angular momentum vector (kg·m²/s)
 */
export function calculateTotalAngularMomentum(bodies) {
    const L_total = new THREE.Vector3(0, 0, 0);
    
    for (const body of bodies) {
        // Angular momentum: L = r × p = r × (m v)
        const m = body.mass_conv || estimateMass(body);
        const p = body.velocity.clone().multiplyScalar(m);
        const L = new THREE.Vector3().crossVectors(body.position, p);
        L_total.add(L);
    }
    
    return L_total;
}

/**
 * Estimate mass from radius (rough approximation)
 * Used when conventional mass is not available
 * 
 * @param {Object} body - Celestial body
 * @returns {number} Estimated mass (kg)
 */
function estimateMass(body) {
    // Rough density estimate: 5000 kg/m³ for planets
    const density = 5000.0;  // kg/m³
    const volume = (4.0 / 3.0) * Math.PI * body.radius * body.radius * body.radius;
    return density * volume;
}

/**
 * Validate conservation of energy and momentum
 * 
 * @param {Array} bodies - Array of celestial bodies
 * @param {number} initialEnergy - Initial total energy
 * @param {THREE.Vector3} initialAngularMomentum - Initial angular momentum
 * @returns {Object} Validation results
 */
export function validateConservation(bodies, initialEnergy, initialAngularMomentum) {
    const currentEnergy = calculateTotalEnergy(bodies);
    const currentAngularMomentum = calculateTotalAngularMomentum(bodies);
    
    // Calculate relative drift
    const energyDrift = Math.abs((currentEnergy - initialEnergy) / initialEnergy);
    const angularMomentumDrift = currentAngularMomentum.distanceTo(initialAngularMomentum) / initialAngularMomentum.length();
    
    return {
        energy: currentEnergy,
        energyDrift: energyDrift,
        angularMomentum: currentAngularMomentum,
        angularMomentumDrift: angularMomentumDrift,
        passed: energyDrift < 1e-6 && angularMomentumDrift < 1e-6
    };
}

