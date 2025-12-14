// Dodecahedral Wireframe Shells
// Creates nested dodecahedral shells pairing celestial bodies
// Shows pressure field structure with light colors and subtle opacity

import * as THREE from 'three';

export class DodecahedralShells {
    constructor(scene) {
        this.scene = scene;
        this.shells = new Map();
        this.visible = true;
    }
    
    /**
     * Create dodecahedral shell for a body pair
     * @param {Object} primary - Primary body (e.g., Sun)
     * @param {Object} secondary - Secondary body (e.g., Earth)
     */
    createShell(primary, secondary) {
        const key = `${primary.name}-${secondary.name}`;
        
        // Create dodecahedron geometry
        const geometry = new THREE.DodecahedronGeometry(1, 0);
        
        // Create wireframe material with light color and low opacity
        const material = new THREE.MeshBasicMaterial({
            color: this.getShellColor(primary, secondary),
            wireframe: true,
            transparent: true,
            opacity: 0.15,
            side: THREE.DoubleSide
        });
        
        const mesh = new THREE.Mesh(geometry, material);
        mesh.userData.primary = primary;
        mesh.userData.secondary = secondary;
        
        // Scale shell based on orbital distance
        const distance = primary.position.distanceTo(secondary.position);
        mesh.scale.setScalar(distance * 1.1);  // Slightly larger than orbit
        
        // Position at midpoint between bodies
        const midpoint = new THREE.Vector3()
            .addVectors(primary.position, secondary.position)
            .multiplyScalar(0.5);
        mesh.position.copy(midpoint);
        
        this.scene.add(mesh);
        this.shells.set(key, mesh);
    }
    
    /**
     * Get shell color based on body pair
     * Light colors, warmer for inner shells
     * @param {Object} primary - Primary body
     * @param {Object} secondary - Secondary body
     * @returns {number} Color hex value
     */
    getShellColor(primary, secondary) {
        // Color based on orbital distance (warmer for inner, cooler for outer)
        const distance = primary.position.distanceTo(secondary.position);
        const maxDistance = 5e12;  // Neptune orbit approximately
        const ratio = Math.min(distance / maxDistance, 1.0);
        
        // Interpolate from warm (inner) to cool (outer)
        const warmColor = 0xffaa44;  // Warm orange/yellow
        const coolColor = 0x44aaff;   // Cool blue
        
        // Simple interpolation
        const r1 = (warmColor >> 16) & 0xff;
        const g1 = (warmColor >> 8) & 0xff;
        const b1 = warmColor & 0xff;
        
        const r2 = (coolColor >> 16) & 0xff;
        const g2 = (coolColor >> 8) & 0xff;
        const b2 = coolColor & 0xff;
        
        const r = Math.floor(r1 + (r2 - r1) * ratio);
        const g = Math.floor(g1 + (g2 - g1) * ratio);
        const b = Math.floor(b1 + (b2 - b1) * ratio);
        
        return (r << 16) | (g << 8) | b;
    }
    
    /**
     * Update all shells based on current body positions
     * @param {Array} bodies - Array of celestial bodies
     * @param {boolean} forceUpdate - Force update even if should skip
     */
    update(bodies, forceUpdate = false) {
        const sun = bodies.find(b => b.name === 'Sun');
        if (!sun) return;
        
        // Create/update shells for Sun-planet pairs
        for (const body of bodies) {
            if (body.name === 'Sun') continue;
            
            const key = `${sun.name}-${body.name}`;
            const shell = this.shells.get(key);
            
            if (shell) {
                // Update shell position and scale
                const distance = sun.position.distanceTo(body.position);
                shell.scale.setScalar(distance * 1.1);
                
                const midpoint = new THREE.Vector3()
                    .addVectors(sun.position, body.position)
                    .multiplyScalar(0.5);
                shell.position.copy(midpoint);
            } else {
                // Create new shell
                this.createShell(sun, body);
            }
        }
        
        // Create Earth-Moon shell
        const earth = bodies.find(b => b.name === 'Earth');
        const moon = bodies.find(b => b.name === 'Moon');
        if (earth && moon) {
            const key = `${earth.name}-${moon.name}`;
            if (!this.shells.has(key)) {
                this.createShell(earth, moon);
            } else {
                const shell = this.shells.get(key);
                const distance = earth.position.distanceTo(moon.position);
                shell.scale.setScalar(distance * 1.1);
                const midpoint = new THREE.Vector3()
                    .addVectors(earth.position, moon.position)
                    .multiplyScalar(0.5);
                shell.position.copy(midpoint);
            }
        }
    }
    
    /**
     * Set visibility of all shells
     * @param {boolean} visible - Visibility state
     */
    setVisible(visible) {
        this.visible = visible;
        for (const shell of this.shells.values()) {
            shell.visible = visible;
        }
    }
    
    /**
     * Get shell for a body pair (for hover info)
     * @param {string} primaryName - Primary body name
     * @param {string} secondaryName - Secondary body name
     * @returns {THREE.Mesh} Shell mesh
     */
    getShell(primaryName, secondaryName) {
        const key = `${primaryName}-${secondaryName}`;
        return this.shells.get(key);
    }
}

