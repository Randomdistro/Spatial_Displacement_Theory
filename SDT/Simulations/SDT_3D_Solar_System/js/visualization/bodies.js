// Body Rendering - Point Particle Visualization
// Renders celestial bodies as point particles with proper scaling

import * as THREE from 'three';

export class BodyRenderer {
    constructor(scene) {
        this.scene = scene;
        this.bodies = [];
        this.meshes = new Map();
        this.trails = new Map();
        this.trailLength = 1000;
    }
    
    /**
     * Initialize bodies for rendering
     * @param {Array} bodies - Array of celestial bodies
     */
    initialize(bodies) {
        this.bodies = bodies;
        
        // Create meshes for each body
        for (const body of bodies) {
            this.createBodyMesh(body);
        }
    }
    
    /**
     * Create a mesh for a celestial body
     * @param {Object} body - Celestial body
     */
    createBodyMesh(body) {
        // Create sphere geometry
        const geometry = new THREE.SphereGeometry(1, 16, 16);
        
        // Create material with emissive color
        const material = new THREE.MeshBasicMaterial({
            color: body.color,
            emissive: body.color,
            emissiveIntensity: 0.5
        });
        
        // Scale based on body size (visual scaling, not physical)
        const scale = body.size * 1e8;  // Scale factor for visibility
        geometry.scale(scale, scale, scale);
        
        const mesh = new THREE.Mesh(geometry, material);
        mesh.userData.body = body;
        mesh.position.copy(body.position);
        
        this.scene.add(mesh);
        this.meshes.set(body.name, mesh);
        
        // Create trail if enabled
        this.createTrail(body);
    }
    
    /**
     * Create trail for a body
     * @param {Object} body - Celestial body
     */
    createTrail(body) {
        const trailGeometry = new THREE.BufferGeometry();
        const positions = new Float32Array(this.trailLength * 3);
        trailGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        
        const trailMaterial = new THREE.LineBasicMaterial({
            color: body.color,
            opacity: 0.3,
            transparent: true
        });
        
        const trail = new THREE.Line(trailGeometry, trailMaterial);
        trail.visible = false;
        this.scene.add(trail);
        
        this.trails.set(body.name, {
            line: trail,
            positions: positions,
            index: 0,
            count: 0
        });
    }
    
    /**
     * Update body positions and trails
     */
    update() {
        for (const body of this.bodies) {
            const mesh = this.meshes.get(body.name);
            if (mesh) {
                mesh.position.copy(body.position);
            }
            
            // Update trail
            const trail = this.trails.get(body.name);
            if (trail && trail.line.visible) {
                this.updateTrail(body, trail);
            }
        }
    }
    
    /**
     * Update trail for a body
     * @param {Object} body - Celestial body
     * @param {Object} trail - Trail data structure
     */
    updateTrail(body, trail) {
        const pos = body.position;
        const idx = trail.index * 3;
        
        trail.positions[idx] = pos.x;
        trail.positions[idx + 1] = pos.y;
        trail.positions[idx + 2] = pos.z;
        
        trail.index = (trail.index + 1) % this.trailLength;
        trail.count = Math.min(trail.count + 1, this.trailLength);
        
        trail.line.geometry.setAttribute('position', 
            new THREE.BufferAttribute(trail.positions, 3));
        trail.line.geometry.setDrawRange(0, trail.count);
        trail.line.geometry.attributes.position.needsUpdate = true;
    }
    
    /**
     * Toggle trail visibility
     * @param {string} bodyName - Body name
     * @param {boolean} visible - Visibility state
     */
    setTrailVisible(bodyName, visible) {
        const trail = this.trails.get(bodyName);
        if (trail) {
            trail.line.visible = visible;
        }
    }
    
    /**
     * Get mesh for a body (for raycasting)
     * @param {string} bodyName - Body name
     * @returns {THREE.Mesh} Mesh object
     */
    getMesh(bodyName) {
        return this.meshes.get(bodyName);
    }
    
    /**
     * Get all meshes
     * @returns {Array} Array of mesh objects
     */
    getAllMeshes() {
        return Array.from(this.meshes.values());
    }
}

