// SDT Physics Engine - CMB Pressure Field Propagation
// From Phase 15: All forces arise from CMB pressure gradients
// NO FUDGED NUMBERS - All formulas are exact SDT derivations

import { SDT_CONSTANTS } from '../data/constants.js';
import * as THREE from 'three';

/**
 * Calculate CMB pressure at a position from a single source body
 * From Phase 15: Π_s(r) = P_CMB - β ρ_s / r
 * 
 * @param {THREE.Vector3} position - Position vector (m)
 * @param {Object} source - Source celestial body
 * @returns {number} Pressure at position (Pa)
 */
export function calculateCMBPressure(position, source) {
    const r_vec = new THREE.Vector3().subVectors(position, source.position);
    const r = r_vec.length();
    
    if (r <= 0.0) {
        return SDT_CONSTANTS.P_CMB;  // At origin, pressure equals CMB pressure
    }
    
    // Pressure deficit: ΔΠ = -β ρ_s / r
    // From Phase 15: β = c² R_eff / Ϟ²
    const beta = source.sdt_params.beta();
    const pressure_deficit = beta * SDT_CONSTANTS.rho_s / r;
    
    return SDT_CONSTANTS.P_CMB - pressure_deficit;
}

/**
 * Calculate pressure gradient at position from a single source
 * From Phase 15: ∇Π = +β ρ_s / r² * r_hat
 * 
 * @param {THREE.Vector3} position - Position vector (m)
 * @param {Object} source - Source celestial body
 * @returns {THREE.Vector3} Pressure gradient vector (Pa/m)
 */
export function calculatePressureGradient(position, source) {
    const r_vec = new THREE.Vector3().subVectors(position, source.position);
    const r = r_vec.length();
    
    if (r <= 0.0) {
        return new THREE.Vector3(0, 0, 0);
    }
    
    // Pressure gradient magnitude: dΠ/dr = +β ρ_s / r²
    const beta = source.sdt_params.beta();
    const gradient_magnitude = beta * SDT_CONSTANTS.rho_s / (r * r);
    
        // Direction is unit vector from source to position
        const r_hat = r_vec.clone().normalize();
        
        return r_hat.multiplyScalar(gradient_magnitude);
}

/**
 * Calculate net acceleration from CMB pressure field
 * From Phase 15: a(r) = -β / r² * r_hat
 * Acceleration = -pressure_gradient / ρ_s
 * 
 * @param {THREE.Vector3} position - Position vector (m)
 * @param {Array} sources - Array of source celestial bodies
 * @param {number} excludeIndex - Index of body to exclude (self)
 * @returns {THREE.Vector3} Net acceleration vector (m/s²)
 */
export function calculateAcceleration(position, sources, excludeIndex = -1) {
    let total_accel = new THREE.Vector3(0, 0, 0);
    
    for (let i = 0; i < sources.length; i++) {
        if (i === excludeIndex) {
            continue;
        }
        
        const source = sources[i];
        const r_vec = new THREE.Vector3().subVectors(position, source.position);
        const r = r_vec.length();
        
        if (r <= 0.0) {
            continue;
        }
        
        // Acceleration from pressure gradient: a = -β / r² * r_hat
        // From Phase 15: a(r) = -c² R_eff / (Ϟ² r²)
        const r_hat = r_vec.normalize();
        const beta = source.sdt_params.beta();
        const accel_mag = beta / (r * r);
        
        // Acceleration points toward source (negative r_hat)
        const accelVec = r_hat.clone().multiplyScalar(-accel_mag);
        total_accel.add(accelVec);
    }
    
    return total_accel;
}

/**
 * Calculate total pressure field from multiple sources
 * 
 * @param {THREE.Vector3} position - Position vector (m)
 * @param {Array} sources - Array of source celestial bodies
 * @returns {number} Total pressure at position (Pa)
 */
export function totalPressure(position, sources) {
    let total_p = SDT_CONSTANTS.P_CMB;  // Background CMB pressure
    
    for (const source of sources) {
        const r_vec = new THREE.Vector3().subVectors(position, source.position);
        const r = r_vec.length();
        
        if (r > 0.0) {
            // Pressure deficit: ΔP = -β ρ_s / r
            const beta = source.sdt_params.beta();
            total_p -= beta * SDT_CONSTANTS.rho_s / r;
        }
    }
    
    return total_p;
}

/**
 * Calculate mutual occlusion factor between two bodies
 * Accounts for screening effect when bodies occlude each other's CMB access
 * 
 * @param {Object} body1 - First celestial body
 * @param {Object} body2 - Second celestial body
 * @returns {number} Occlusion factor (0-1)
 */
export function mutualOcclusionFactor(body1, body2) {
    const r_vec = new THREE.Vector3().subVectors(body2.position, body1.position);
    const r = r_vec.length();
    
    if (r <= 0.0) {
        return 0.0;
    }
    
    // Simple geometric occlusion model
    // More sophisticated models can be added based on SDT Phase 15
    const r1_eff = body1.sdt_params.R_eff;
    const r2_eff = body2.sdt_params.R_eff;
    
    // Solid angle subtended by body2 as seen from body1
    const solid_angle = Math.PI * (r2_eff * r2_eff) / (r * r);
    const max_solid_angle = Math.PI;  // Half sphere
    
    // Occlusion factor (0 = no occlusion, 1 = full occlusion)
    const occlusion = Math.min(solid_angle / max_solid_angle, 1.0);
    
    return occlusion;
}

