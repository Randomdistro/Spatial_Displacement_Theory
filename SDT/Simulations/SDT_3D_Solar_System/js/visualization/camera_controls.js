// Camera Controls - 3D navigation with body focus
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import * as THREE from 'three';

export class CameraController {
    constructor(camera, renderer, scene) {
        this.camera = camera;
        this.renderer = renderer;
        this.scene = scene;
        this.controls = null;
        this.focusedBody = null;
        this.focusMode = 'free';  // 'free', 'body', 'overview'
        
        this.setupControls();
    }
    
    /**
     * Setup OrbitControls
     */
    setupControls() {
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        
        // Control settings
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.minDistance = 1e10;
        this.controls.maxDistance = 1e14;
        this.controls.enablePan = true;
        this.controls.enableZoom = true;
        this.controls.enableRotate = true;
        
        // Auto-rotate (optional)
        this.controls.autoRotate = false;
        this.controls.autoRotateSpeed = 0.5;
    }
    
    /**
     * Focus camera on a specific body
     * @param {Object} body - Celestial body to focus on
     */
    focusOnBody(body) {
        if (!body) {
            this.focusMode = 'free';
            this.focusedBody = null;
            return;
        }
        
        this.focusedBody = body;
        this.focusMode = 'body';
        
        // Set controls target to body position
        this.controls.target.copy(body.position);
        this.controls.update();
    }
    
    /**
     * Set overview mode (show all bodies)
     */
    setOverviewMode() {
        this.focusMode = 'overview';
        this.focusedBody = null;
        
        // Position camera to show entire system
        this.camera.position.set(0, 5e12, 5e12);
        this.controls.target.set(0, 0, 0);
        this.controls.update();
    }
    
    /**
     * Update camera controls
     * Should be called every frame
     */
    update() {
        // If focusing on a body, update target to follow it
        if (this.focusMode === 'body' && this.focusedBody) {
            this.controls.target.copy(this.focusedBody.position);
        }
        
        this.controls.update();
    }
    
    /**
     * Handle window resize
     */
    handleResize() {
        // Camera aspect ratio is handled by SceneManager
        // Controls don't need resize handling
    }
    
    /**
     * Get controls object (for external access)
     * @returns {THREE.OrbitControls} Controls object
     */
    getControls() {
        return this.controls;
    }
}

// Export OrbitControls type for reference
export { OrbitControls };

