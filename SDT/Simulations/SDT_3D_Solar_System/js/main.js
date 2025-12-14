// Main Application Entry Point
// Ties together all components: physics, visualization, UI

import { loadJPLData, validateInitialConditions } from './data/jpl_ephemeris.js';
import { integrateStep } from './physics/integrator.js';
import { calculateTotalEnergy, calculateTotalAngularMomentum, validateConservation } from './physics/conservation.js';
import { SceneManager } from './visualization/scene_setup.js';
import { BodyRenderer } from './visualization/bodies.js';
import { DodecahedralShells } from './visualization/dodecahedral_shells.js';
import { OrbitalMarkers } from './visualization/orbital_markers.js';
import { CameraController } from './visualization/camera_controls.js';
import { HoverInfo } from './visualization/hover_info.js';
import { UIControls } from './ui/controls.js';
import * as THREE from 'three';

class Simulation {
    constructor() {
        this.bodies = [];
        this.sceneManager = null;
        this.bodyRenderer = null;
        this.shells = null;
        this.markers = null;
        this.cameraController = null;
        this.hoverInfo = null;
        this.uiControls = null;
        
        // Simulation state
        this.isPaused = false;
        this.timestep = 86400.0;  // 1 day
        this.dtVisual = 86400.0;  // Visual timestep (fixed)
        this.speed = 10.0;  // Speed multiplier
        this.time = 0.0;
        
        // Conservation tracking
        this.initialEnergy = 0.0;
        this.initialAngularMomentum = null;
        
        // Performance tracking
        this.frameCount = 0;
        this.lastFPSUpdate = Date.now();
        this.fps = 60;
        
        // Raycasting for hover detection
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        
        this.init();
    }
    
    async init() {
        // Load initial conditions
        this.bodies = loadJPLData();
        validateInitialConditions(this.bodies);
        
        // Store initial energy and momentum
        this.initialEnergy = calculateTotalEnergy(this.bodies);
        this.initialAngularMomentum = calculateTotalAngularMomentum(this.bodies);
        
        // Setup Three.js scene
        const canvas = document.getElementById('simCanvas');
        this.sceneManager = new SceneManager(canvas);
        
        // Setup visualization components
        this.bodyRenderer = new BodyRenderer(this.sceneManager.getScene());
        this.bodyRenderer.initialize(this.bodies);
        
        this.shells = new DodecahedralShells(this.sceneManager.getScene());
        this.shells.update(this.bodies);
        
        this.markers = new OrbitalMarkers(this.sceneManager.getScene());
        this.markers.initialize();
        
        this.cameraController = new CameraController(
            this.sceneManager.getCamera(),
            this.sceneManager.getRenderer(),
            this.sceneManager.getScene()
        );
        
        // Setup hover info
        const infoPanel = document.getElementById('info-panel');
        this.hoverInfo = new HoverInfo(infoPanel);
        
        // Setup UI controls
        this.uiControls = new UIControls(this);
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            this.sceneManager.resize();
        });
        
        // Start animation loop
        this.animate();
    }
    
    setupEventListeners() {
        const canvas = document.getElementById('simCanvas');
        
        // Mouse move for hover detection
        canvas.addEventListener('mousemove', (e) => {
            this.handleMouseMove(e);
        });
        
        // Click for body selection
        canvas.addEventListener('click', (e) => {
            this.handleClick(e);
        });
    }
    
    handleMouseMove(event) {
        const canvas = document.getElementById('simCanvas');
        const rect = canvas.getBoundingClientRect();
        
        this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        
        // Raycast to detect hover
        this.raycaster.setFromCamera(this.mouse, this.sceneManager.getCamera());
        
        // Check bodies
        const bodyMeshes = this.bodyRenderer.getAllMeshes();
        const intersects = this.raycaster.intersectObjects(bodyMeshes);
        
        if (intersects.length > 0) {
            const body = intersects[0].object.userData.body;
            this.hoverInfo.showBodyInfo(body, this.bodies);
            canvas.style.cursor = 'pointer';
        } else {
            // Check shells
            const shellMeshes = Array.from(this.shells.shells.values());
            const shellIntersects = this.raycaster.intersectObjects(shellMeshes);
            
            if (shellIntersects.length > 0) {
                const shell = shellIntersects[0].object;
                const primary = shell.userData.primary;
                const secondary = shell.userData.secondary;
                this.hoverInfo.showPairInfo(primary, secondary);
                canvas.style.cursor = 'pointer';
            } else {
                this.hoverInfo.hide();
                canvas.style.cursor = 'grab';
            }
        }
    }
    
    handleClick(event) {
        const canvas = document.getElementById('simCanvas');
        const rect = canvas.getBoundingClientRect();
        
        this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        
        this.raycaster.setFromCamera(this.mouse, this.sceneManager.getCamera());
        
        const bodyMeshes = this.bodyRenderer.getAllMeshes();
        const intersects = this.raycaster.intersectObjects(bodyMeshes);
        
        if (intersects.length > 0) {
            const body = intersects[0].object.userData.body;
            this.focusOnBody(body.name);
        }
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        if (!this.isPaused) {
            // Update physics
            const steps = Math.max(1, Math.floor(this.speed));
            for (let i = 0; i < steps; i++) {
                integrateStep(this.bodies, this.timestep, this.dtVisual);
                this.time += this.dtVisual;
            }
            
            // Update conservation validation
            this.updateConservation();
        }
        
        // Update visualization (with performance optimization)
        this.bodyRenderer.update();
        
        // Update shells less frequently for performance
        if (this.frameCount % 3 === 0) {
            this.shells.update(this.bodies);
        }
        
        this.markers.update();
        this.cameraController.update();
        
        // Render
        this.sceneManager.render();
        
        // Update FPS
        this.updateFPS();
    }
    
    updateConservation() {
        const validation = validateConservation(
            this.bodies,
            this.initialEnergy,
            this.initialAngularMomentum
        );
        
        // Update UI
        const energyDriftElement = document.getElementById('energyDrift');
        if (energyDriftElement) {
            energyDriftElement.textContent = `${(validation.energyDrift * 100).toFixed(4)}%`;
        }
        
        const timeElement = document.getElementById('timeValue');
        if (timeElement) {
            const days = this.time / 86400.0;
            timeElement.textContent = `${days.toFixed(2)} days`;
        }
    }
    
    updateFPS() {
        this.frameCount++;
        const now = Date.now();
        const elapsed = now - this.lastFPSUpdate;
        
        if (elapsed >= 1000) {
            this.fps = Math.round((this.frameCount * 1000) / elapsed);
            this.frameCount = 0;
            this.lastFPSUpdate = now;
            
            const fpsElement = document.getElementById('fpsValue');
            if (fpsElement) {
                fpsElement.textContent = this.fps;
            }
        }
    }
    
    // Public API for UI controls
    setTimestep(dt) {
        this.timestep = Math.max(1.0, Math.min(dt, 86400.0 * 10));
    }
    
    setSpeed(speed) {
        this.speed = Math.max(0.1, Math.min(speed, 1000));
    }
    
    togglePause() {
        this.isPaused = !this.isPaused;
    }
    
    getIsPaused() {
        return this.isPaused;
    }
    
    reset() {
        // Reload initial conditions
        this.bodies = loadJPLData();
        this.bodyRenderer.initialize(this.bodies);
        this.time = 0.0;
        this.initialEnergy = calculateTotalEnergy(this.bodies);
        this.initialAngularMomentum = calculateTotalAngularMomentum(this.bodies);
    }
    
    focusOnBody(bodyName) {
        const body = this.bodies.find(b => b.name === bodyName);
        if (body) {
            this.cameraController.focusOnBody(body);
        }
    }
    
    setFocusMode(mode) {
        if (mode === 'free') {
            this.cameraController.focusMode = 'free';
            this.cameraController.focusedBody = null;
        } else if (mode === 'overview') {
            this.cameraController.setOverviewMode();
        }
    }
    
    setParticlesVisible(visible) {
        // Body visibility is handled by bodyRenderer
        // For now, bodies are always visible when particles toggle is on
    }
    
    setMarkersVisible(visible) {
        this.markers.setVisible(visible);
    }
    
    setShellsVisible(visible) {
        this.shells.setVisible(visible);
    }
    
    setTrailsVisible(visible) {
        for (const body of this.bodies) {
            this.bodyRenderer.setTrailVisible(body.name, visible);
        }
    }
    
    setGridVisible(visible) {
        // Grid visualization can be added here
    }
    
    hideInfo() {
        this.hoverInfo.hide();
    }
}

// Initialize simulation when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new Simulation();
    });
} else {
    new Simulation();
}

