/**
 * SDT Physics Engine
 * Implements SDT acceleration formula and symplectic integrator
 */

export const SDT_CONSTANTS = {
    c: 299792458.0, // m/s - speed of light
};

/**
 * Calculate SDT acceleration: a = c² * R_eff / (κ² * r²)
 * @param {Object} source - Source body with R_eff and kappa
 * @param {THREE.Vector3} rVec - Vector from test particle to source
 * @returns {THREE.Vector3} Acceleration vector
 */
export function calculateSDTAcceleration(source, rVec) {
    const r = rVec.length();
    
    if (r <= 0) {
        return new THREE.Vector3(0, 0, 0);
    }
    
    // SDT acceleration formula: a = c² * R_eff / (κ² * r²)
    const c2 = SDT_CONSTANTS.c * SDT_CONSTANTS.c;
    const rEff = source.R_eff;
    const kappa = source.kappa;
    
    const accelMagnitude = (c2 * rEff) / (kappa * kappa * r * r);
    
    // Direction is towards source (rVec points from particle to source)
    const direction = rVec.clone().normalize();
    
    return direction.multiplyScalar(accelMagnitude);
}

/**
 * Calculate net acceleration on a body from all other bodies
 * @param {Object} body - Body to calculate acceleration for
 * @param {Array} allBodies - All bodies in the system
 * @returns {THREE.Vector3} Net acceleration vector
 */
export function calculateNetAcceleration(body, allBodies) {
    const netAccel = new THREE.Vector3(0, 0, 0);
    
    for (const other of allBodies) {
        if (other === body) continue;
        
        // Vector from body to other
        const rVec = other.position.clone().sub(body.position);
        const accel = calculateSDTAcceleration(other, rVec);
        netAccel.add(accel);
    }
    
    return netAccel;
}

/**
 * Symplectic Leapfrog Integrator (Kick-Drift-Kick)
 * Maintains energy and angular momentum conservation for long-term stability
 * 
 * @param {Array} bodies - Array of body objects with position, velocity, acceleration
 * @param {number} dt - Time step in seconds
 */
export function symplecticLeapfrogStep(bodies, dt) {
    // Step 1: Half-step velocity update (kick)
    for (const body of bodies) {
        if (body.isFixed) continue; // Skip fixed bodies (e.g., Sun at origin)
        
        body.acceleration = calculateNetAcceleration(body, bodies);
        body.velocity.add(body.acceleration.clone().multiplyScalar(0.5 * dt));
    }
    
    // Step 2: Full-step position update (drift)
    for (const body of bodies) {
        if (body.isFixed) continue;
        
        body.position.add(body.velocity.clone().multiplyScalar(dt));
    }
    
    // Step 3: Half-step velocity update (kick)
    for (const body of bodies) {
        if (body.isFixed) continue;
        
        body.acceleration = calculateNetAcceleration(body, bodies);
        body.velocity.add(body.acceleration.clone().multiplyScalar(0.5 * dt));
    }
}

/**
 * Calculate total energy of the system (kinetic + potential)
 * @param {Array} bodies - All bodies in the system
 * @returns {Object} {kinetic, potential, total}
 */
export function calculateTotalEnergy(bodies) {
    let kinetic = 0;
    let potential = 0;
    
    for (let i = 0; i < bodies.length; i++) {
        const body = bodies[i];
        if (body.isFixed) continue;
        
        // Kinetic energy: E_k = ½ m v²
        // Using mass approximation: m ≈ R_eff (for SDT)
        const mass = body.R_eff;
        const v2 = body.velocity.lengthSq();
        kinetic += 0.5 * mass * v2;
        
        // Potential energy: E_p = -β / r for each pair
        // β = c² R_eff / κ²
        for (let j = i + 1; j < bodies.length; j++) {
            const other = bodies[j];
            const rVec = other.position.clone().sub(body.position);
            const r = rVec.length();
            
            if (r > 0) {
                const c2 = SDT_CONSTANTS.c * SDT_CONSTANTS.c;
                const beta_i = (c2 * body.R_eff) / (body.kappa * body.kappa);
                const beta_j = (c2 * other.R_eff) / (other.kappa * other.kappa);
                const beta_eff = Math.sqrt(beta_i * beta_j);
                
                potential -= beta_eff / r;
            }
        }
    }
    
    return {
        kinetic,
        potential,
        total: kinetic + potential
    };
}

/**
 * Calculate total angular momentum
 * @param {Array} bodies - All bodies in the system
 * @returns {THREE.Vector3} Total angular momentum vector
 */
export function calculateAngularMomentum(bodies) {
    const L_total = new THREE.Vector3(0, 0, 0);
    
    for (const body of bodies) {
        if (body.isFixed) continue;
        
        const mass = body.R_eff;
        const L = body.position.clone().cross(body.velocity).multiplyScalar(mass);
        L_total.add(L);
    }
    
    return L_total;
}

