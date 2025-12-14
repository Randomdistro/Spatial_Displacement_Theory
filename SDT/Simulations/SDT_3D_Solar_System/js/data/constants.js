// SDT Constants - From Phase 15 and CODATA 2018
// All values are exact and verifiable - NO FUDGED NUMBERS
import * as THREE from 'three';

export const SDT_CONSTANTS = {
    // CODATA 2018 Fundamental Constants
    c: 299792458.0,  // Speed of light (m/s), exact
    
    // CMB Pressure (from recombination, Phase 1)
    P_CMB: 2.036e-2,  // Pa (CMB radiation pressure at z=1089.9)
    
    // Spation Lattice Properties (Phase 15)
    r_P: 1.616255e-35,  // Planck radius (m)
    K_bulk: 4.6e113,  // Bulk modulus (Pa)
    rho_s: 5.2e96,  // Spation density (kg/m³)
    
    // Mathematical Constants
    PI: Math.PI,
    TWO_PI: 2.0 * Math.PI,
    FOUR_PI: 4.0 * Math.PI,
    
    // Unit Conversions
    AU: 1.495978707e11,  // Astronomical unit (m)
    DAY_TO_SEC: 86400.0,  // seconds per day
    YEAR_TO_SEC: 3.15576e7,  // seconds per year (Julian year)
    
    // Simulation defaults
    DEFAULT_TIMESTEP: 86400.0,  // 1 day in seconds
    MIN_TIMESTEP: 1.0,  // 1 second minimum
    MAX_TIMESTEP: 86400.0 * 10.0,  // 10 days maximum
    
    // Energy conservation tolerance
    ENERGY_TOLERANCE: 1e-6,  // Relative energy drift tolerance
};

// SDT Parameters structure
export class SDTParameters {
    constructor(kappa = 0.0, R_eff = 0.0) {
        this.kappa = kappa;  // Velocity factor Ϟ (dimensionless)
        this.R_eff = R_eff;  // Effective radius (m)
    }
    
    // Calculate beta parameter: β = c² R_eff / Ϟ²
    // From Phase 15
    beta() {
        if (this.kappa <= 0.0 || this.R_eff <= 0.0) {
            return 0.0;
        }
        return (SDT_CONSTANTS.c * SDT_CONSTANTS.c * this.R_eff) / (this.kappa * this.kappa);
    }
    
    // Calculate orbital velocity at radius r: v(r) = (c/Ϟ) √(R_eff/r)
    // From Phase 15
    orbitalVelocity(r) {
        if (this.kappa <= 0.0 || this.R_eff <= 0.0 || r <= 0.0) {
            return 0.0;
        }
        return (SDT_CONSTANTS.c / this.kappa) * Math.sqrt(this.R_eff / r);
    }
    
    // Calculate orbital period at radius r: T = 2πϞ √(r³/R_eff) / c
    // From Phase 15
    orbitalPeriod(r) {
        if (this.kappa <= 0.0 || this.R_eff <= 0.0 || r <= 0.0) {
            return 0.0;
        }
        return SDT_CONSTANTS.TWO_PI * this.kappa * Math.sqrt(r * r * r / this.R_eff) / SDT_CONSTANTS.c;
    }
    
    // Calculate acceleration magnitude at distance r: a(r) = -c² R_eff / (Ϟ² r²)
    // From Phase 15
    accelerationMagnitude(r) {
        if (this.kappa <= 0.0 || this.R_eff <= 0.0 || r <= 0.0) {
            return 0.0;
        }
        return (SDT_CONSTANTS.c * SDT_CONSTANTS.c * this.R_eff) / (this.kappa * this.kappa * r * r);
    }
}

// Celestial body representation
export class CelestialBody {
    constructor(name, type = 'planet') {
        this.name = name;
        this.type = type;  // "star", "planet", "moon", etc.
        
        // Position and velocity (m, m/s) - Vec3d equivalent
        this.position = new THREE.Vector3(0, 0, 0);
        this.velocity = new THREE.Vector3(0, 0, 0);
        
        // Physical properties
        this.radius = 0.0;  // Physical radius (m)
        this.mass_conv = 0.0;  // Conventional mass (kg) - for comparison only
        
        // SDT-native parameters
        this.sdt_params = new SDTParameters();
        
        // Visual properties
        this.color = 0xffffff;
        this.size = 1.0;
    }
    
    distanceTo(other) {
        return this.position.distanceTo(other.position);
    }
    
    relativeVelocity(other) {
        return this.velocity.clone().sub(other.velocity);
    }
}

