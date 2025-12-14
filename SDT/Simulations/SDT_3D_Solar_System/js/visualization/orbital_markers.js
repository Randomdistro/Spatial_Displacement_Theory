// Orbital Marker Points
// White point markers at specified orbital radii

import { getOrbitalMarkers } from '../data/planetary_data.js';
import * as THREE from 'three';

export class OrbitalMarkers {
    constructor(scene) {
        this.scene = scene;
        this.markers = [];
        this.visible = true;
    }
    
    /**
     * Initialize orbital markers
     */
    initialize() {
        const markerData = getOrbitalMarkers();
        
        for (const data of markerData) {
            this.createMarker(data.radius, data.label);
        }
    }
    
    /**
     * Create a white point marker at specified radius
     * @param {number} radius - Orbital radius (m)
     * @param {string} label - Marker label
     */
    createMarker(radius, label) {
        // Create small sphere geometry
        const geometry = new THREE.SphereGeometry(5e9, 8, 8);  // Small sphere
        
        // White material
        const material = new THREE.MeshBasicMaterial({
            color: 0xffffff,
            emissive: 0xffffff,
            emissiveIntensity: 0.8
        });
        
        const mesh = new THREE.Mesh(geometry, material);
        mesh.userData.radius = radius;
        mesh.userData.label = label;
        
        // Position at radius along x-axis (will be rotated in update)
        mesh.position.set(radius, 0, 0);
        
        this.scene.add(mesh);
        this.markers.push(mesh);
    }
    
    /**
     * Update marker positions (rotate around Sun)
     * For now, markers stay at fixed positions
     * Future: Could animate or follow orbital plane
     */
    update() {
        // Markers stay at fixed orbital radii
        // They could be rotated or animated if desired
        // For now, they remain static at their orbital positions
    }
    
    /**
     * Set visibility of all markers
     * @param {boolean} visible - Visibility state
     */
    setVisible(visible) {
        this.visible = visible;
        for (const marker of this.markers) {
            marker.visible = visible;
        }
    }
    
    /**
     * Get all markers (for raycasting)
     * @returns {Array} Array of marker meshes
     */
    getMarkers() {
        return this.markers;
    }
}

