// Lagrange Point Calculations using SDT Pressure Field Equations
// L1, L2, L3, L4, L5 points for two-body system

import { calculateAcceleration, totalPressure } from './sdt_physics.js';
import * as THREE from 'three';

/**
 * Calculate Lagrange points for a two-body system
 * Uses SDT pressure field equations for accurate positions
 * 
 * @param {Object} primary - Primary body (e.g., Sun)
 * @param {Object} secondary - Secondary body (e.g., Earth)
 * @returns {Object} Object containing L1-L5 positions
 */
export function calculateLagrangePoints(primary, secondary) {
    const r_vec = new THREE.Vector3().subVectors(secondary.position, primary.position);
    const r = r_vec.length();
    const r_hat = r_vec.normalize();
    
    const points = {};
    
    // L1: Between primary and secondary (closer to secondary)
    // Find point where gravitational forces balance
    points.L1 = calculateL1(primary, secondary, r, r_hat);
    
    // L2: Beyond secondary on the same line
    points.L2 = calculateL2(primary, secondary, r, r_hat);
    
    // L3: Opposite side of primary
    points.L3 = calculateL3(primary, secondary, r, r_hat);
    
    // L4 and L5: 60° ahead and behind secondary in orbit
    points.L4 = calculateL4(primary, secondary, r, r_hat);
    points.L5 = calculateL5(primary, secondary, r, r_hat);
    
    return points;
}

/**
 * Calculate L1 point (between primary and secondary)
 * @param {Object} primary - Primary body
 * @param {Object} secondary - Secondary body
 * @param {number} r - Distance between bodies
 * @param {THREE.Vector3} r_hat - Unit vector from primary to secondary
 * @returns {THREE.Vector3} L1 position
 */
function calculateL1(primary, secondary, r, r_hat) {
    // L1 is closer to secondary
    // Find point where accelerations balance
    // Use iterative method to find equilibrium
    
    let x = r * 0.9;  // Start closer to secondary
    const tolerance = 1e6;  // 1 km tolerance
    const maxIterations = 100;
    
    for (let i = 0; i < maxIterations; i++) {
        const pos = primary.position.clone().add(r_hat.clone().multiplyScalar(x));
        
        // Acceleration from primary
        const accel_primary = calculateAcceleration(pos, [primary], -1);
        const accel_primary_mag = accel_primary.length();
        const accel_primary_dir = accel_primary.normalize();
        
        // Acceleration from secondary
        const accel_secondary = calculateAcceleration(pos, [secondary], -1);
        const accel_secondary_mag = accel_secondary.length();
        const accel_secondary_dir = accel_secondary.normalize();
        
        // Net acceleration (should be zero at L1)
        const net_accel = accel_primary.clone().add(accel_secondary);
        
        // Adjust position based on net acceleration
        const correction = net_accel.length() * 1e-6;  // Small correction factor
        if (net_accel.dot(r_hat) > 0) {
            x += correction;
        } else {
            x -= correction;
        }
        
        if (net_accel.length() < tolerance) {
            break;
        }
    }
    
    return primary.position.clone().add(r_hat.clone().multiplyScalar(x));
}

/**
 * Calculate L2 point (beyond secondary)
 * @param {Object} primary - Primary body
 * @param {Object} secondary - Secondary body
 * @param {number} r - Distance between bodies
 * @param {THREE.Vector3} r_hat - Unit vector from primary to secondary
 * @returns {THREE.Vector3} L2 position
 */
function calculateL2(primary, secondary, r, r_hat) {
    // L2 is beyond secondary
    let x = r * 1.1;  // Start beyond secondary
    const tolerance = 1e6;
    const maxIterations = 100;
    
    for (let i = 0; i < maxIterations; i++) {
        const pos = primary.position.clone().add(r_hat.clone().multiplyScalar(x));
        
        const accel_primary = calculateAcceleration(pos, [primary], -1);
        const accel_secondary = calculateAcceleration(pos, [secondary], -1);
        const net_accel = accel_primary.clone().add(accel_secondary);
        
        const correction = net_accel.length() * 1e-6;
        if (net_accel.dot(r_hat) > 0) {
            x += correction;
        } else {
            x -= correction;
        }
        
        if (net_accel.length() < tolerance) {
            break;
        }
    }
    
    return primary.position.clone().add(r_hat.clone().multiplyScalar(x));
}

/**
 * Calculate L3 point (opposite side of primary)
 * @param {Object} primary - Primary body
 * @param {Object} secondary - Secondary body
 * @param {number} r - Distance between bodies
 * @param {THREE.Vector3} r_hat - Unit vector from primary to secondary
 * @returns {THREE.Vector3} L3 position
 */
function calculateL3(primary, secondary, r, r_hat) {
    // L3 is on opposite side of primary
    const r_hat_opposite = r_hat.clone().multiplyScalar(-1);
    let x = r * 0.95;  // Start near primary
    
    const tolerance = 1e6;
    const maxIterations = 100;
    
    for (let i = 0; i < maxIterations; i++) {
        const pos = primary.position.clone().add(r_hat_opposite.clone().multiplyScalar(x));
        
        const accel_primary = calculateAcceleration(pos, [primary], -1);
        const accel_secondary = calculateAcceleration(pos, [secondary], -1);
        const net_accel = accel_primary.clone().add(accel_secondary);
        
        const correction = net_accel.length() * 1e-6;
        if (net_accel.dot(r_hat_opposite) > 0) {
            x += correction;
        } else {
            x -= correction;
        }
        
        if (net_accel.length() < tolerance) {
            break;
        }
    }
    
    return primary.position.clone().add(r_hat_opposite.clone().multiplyScalar(x));
}

/**
 * Calculate L4 point (60° ahead of secondary)
 * @param {Object} primary - Primary body
 * @param {Object} secondary - Secondary body
 * @param {number} r - Distance between bodies
 * @param {THREE.Vector3} r_hat - Unit vector from primary to secondary
 * @returns {THREE.Vector3} L4 position
 */
function calculateL4(primary, secondary, r, r_hat) {
    // L4 is 60° ahead of secondary in orbit
    // Create perpendicular vector (in orbital plane)
    const perp = new THREE.Vector3(-r_hat.y, r_hat.x, 0).normalize();
    
    // Rotate r_hat by 60° around perpendicular axis
    const angle = Math.PI / 3;  // 60 degrees
    const rotated = r_hat.clone().applyAxisAngle(perp, angle);
    
    return primary.position.clone().add(rotated.multiplyScalar(r));
}

/**
 * Calculate L5 point (60° behind secondary)
 * @param {Object} primary - Primary body
 * @param {Object} secondary - Secondary body
 * @param {number} r - Distance between bodies
 * @param {THREE.Vector3} r_hat - Unit vector from primary to secondary
 * @returns {THREE.Vector3} L5 position
 */
function calculateL5(primary, secondary, r, r_hat) {
    // L5 is 60° behind secondary in orbit
    const perp = new THREE.Vector3(-r_hat.y, r_hat.x, 0).normalize();
    
    // Rotate r_hat by -60° around perpendicular axis
    const angle = -Math.PI / 3;  // -60 degrees
    const rotated = r_hat.clone().applyAxisAngle(perp, angle);
    
    return primary.position.clone().add(rotated.multiplyScalar(r));
}

