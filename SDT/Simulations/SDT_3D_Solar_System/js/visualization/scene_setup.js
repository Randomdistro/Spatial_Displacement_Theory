// Three.js Scene Setup
// Creates the 3D scene with camera, lighting, and renderer

import * as THREE from 'three';

export class SceneManager {
    constructor(canvas) {
        this.canvas = canvas;
        this.scene = new THREE.Scene();
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        
        this.setupScene();
        this.setupCamera();
        this.setupRenderer();
        this.setupLighting();
    }
    
    setupScene() {
        // Deep space background
        this.scene.background = new THREE.Color(0x000000);
        this.scene.fog = new THREE.Fog(0x000000, 1e12, 1e13);
    }
    
    setupCamera() {
        // Perspective camera
        const aspect = this.canvas.clientWidth / this.canvas.clientHeight;
        this.camera = new THREE.PerspectiveCamera(60, aspect, 1e9, 1e14);
        
        // Initial position: view from above the ecliptic
        this.camera.position.set(0, 5e12, 5e12);
        this.camera.lookAt(0, 0, 0);
    }
    
    setupRenderer() {
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            antialias: true,
            alpha: false
        });
        
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        
        // Enable shadows and better rendering
        this.renderer.shadowMap.enabled = false;  // Disable for performance
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.0;
    }
    
    setupLighting() {
        // Ambient light (simulating starlight)
        const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
        this.scene.add(ambientLight);
        
        // Directional light (simulating sunlight)
        const sunLight = new THREE.DirectionalLight(0xffffff, 1.0);
        sunLight.position.set(0, 0, 0);  // At Sun's position
        sunLight.castShadow = false;  // Disable for performance
        this.scene.add(sunLight);
        
        // Point light at Sun position for better illumination
        const pointLight = new THREE.PointLight(0xffffaa, 2.0, 1e13);
        pointLight.position.set(0, 0, 0);
        this.scene.add(pointLight);
    }
    
    resize() {
        const width = this.canvas.clientWidth;
        const height = this.canvas.clientHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        
        this.renderer.setSize(width, height);
    }
    
    render() {
        this.renderer.render(this.scene, this.camera);
    }
    
    getScene() {
        return this.scene;
    }
    
    getCamera() {
        return this.camera;
    }
    
    getRenderer() {
        return this.renderer;
    }
}

