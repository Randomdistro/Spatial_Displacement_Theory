/**
 * Pressure Field Renderer
 * Visualizes CMB pressure field at all scales
 * Shows pressure waves emanating from CMB boundary
 */

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { ScalePoint } from './ScaleManager';

interface PressureFieldRendererProps {
  scale: ScalePoint;
  intensity?: number;
  showWaves?: boolean;
  showBoundary?: boolean;
}

export class PressureFieldVisualization {
  private scene: THREE.Scene;
  private pressureField: THREE.Points | null = null;
  private waveGeometry: THREE.BufferGeometry | null = null;
  private waveMaterial: THREE.ShaderMaterial | null = null;
  private waveMesh: THREE.Mesh | null = null;
  private boundarySphere: THREE.Mesh | null = null;
  private time: number = 0;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  update(scale: ScalePoint, intensity: number = 1.0, showWaves: boolean = true, showBoundary: boolean = false): void {
    this.time += 0.016; // ~60 FPS

    // Clear existing pressure field
    if (this.pressureField) {
      this.scene.remove(this.pressureField);
      this.pressureField.geometry.dispose();
      if (this.pressureField.material instanceof THREE.Material) {
        this.pressureField.material.dispose();
      }
    }

    // Create pressure field visualization
    this.createPressureField(scale, intensity);

    // Create pressure waves
    if (showWaves) {
      this.createPressureWaves(scale, intensity);
    }

    // Create CMB boundary visualization
    if (showBoundary && scale.domain === 'cosmological') {
      this.createCMBBoundary(scale);
    }
  }

  private createPressureField(scale: ScalePoint, intensity: number): void {
    const resolution = 30;
    const gridSize = this.getGridSize(scale);
    const positions: number[] = [];
    const colors: number[] = [];
    const sizes: number[] = [];

    for (let x = -gridSize; x < gridSize; x += gridSize / resolution) {
      for (let y = -gridSize; y < gridSize; y += gridSize / resolution) {
        for (let z = -gridSize / 2; z < gridSize / 2; z += gridSize / resolution) {
          const distance = Math.sqrt(x * x + y * y + z * z);
          
          // Pressure decreases with distance from CMB boundary
          // At cosmological scales, show pressure gradient
          // At smaller scales, show local pressure field
          const pressure = this.calculatePressure(distance, scale, intensity);
          
          positions.push(x, y, z);
          
          // Color: blue (low) to gold (high pressure)
          const color = new THREE.Color();
          color.lerpColors(
            new THREE.Color(0x1a365d), // Deep blue
            new THREE.Color(0xd69e2e), // Gold
            Math.max(0, Math.min(1, pressure))
          );
          colors.push(color.r, color.g, color.b);
          
          sizes.push(0.1 + pressure * 0.2);
        }
      }
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    geometry.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));

    const material = new THREE.PointsMaterial({
      size: 0.15,
      vertexColors: true,
      transparent: true,
      opacity: 0.6 * intensity,
      sizeAttenuation: true,
    });

    this.pressureField = new THREE.Points(geometry, material);
    this.scene.add(this.pressureField);
  }

  private createPressureWaves(scale: ScalePoint, intensity: number): void {
    // FIX #2: Remove old wave mesh before creating new one
    if (this.waveMesh) {
      this.scene.remove(this.waveMesh);
      if (this.waveMesh.geometry !== this.waveGeometry) {
        // Only dispose if it's a different geometry
        this.waveMesh.geometry.dispose();
      }
      if (this.waveMesh.material instanceof THREE.Material && this.waveMesh.material !== this.waveMaterial) {
        this.waveMesh.material.dispose();
      }
      this.waveMesh = null;
    }

    // Create animated pressure waves using shader
    if (!this.waveGeometry) {
      this.waveGeometry = new THREE.PlaneGeometry(20, 20, 64, 64);
    }

    if (!this.waveMaterial) {
      this.waveMaterial = new THREE.ShaderMaterial({
        uniforms: {
          time: { value: 0 },
          scale: { value: 1.0 },
          intensity: { value: 1.0 },
        },
        vertexShader: `
          uniform float time;
          uniform float scale;
          varying vec3 vPosition;
          varying float vElevation;
          
          void main() {
            vPosition = position;
            vElevation = sin(position.x * 0.5 + time) * sin(position.y * 0.5 + time * 0.7) * 0.3;
            vec3 newPosition = position + normal * vElevation;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
          }
        `,
        fragmentShader: `
          uniform float intensity;
          varying vec3 vPosition;
          varying float vElevation;
          
          void main() {
            vec3 color1 = vec3(0.1, 0.2, 0.36); // Deep blue
            vec3 color2 = vec3(0.84, 0.62, 0.18); // Gold
            float mixFactor = (vElevation + 0.3) / 0.6;
            vec3 color = mix(color1, color2, mixFactor);
            gl_FragColor = vec4(color, 0.4 * intensity);
          }
        `,
        transparent: true,
        side: THREE.DoubleSide,
      });
    }

    this.waveMaterial.uniforms.time.value = this.time;
    this.waveMaterial.uniforms.scale.value = this.getGridSize(scale);
    this.waveMaterial.uniforms.intensity.value = intensity;

    // FIX #2: Store reference to wave mesh for cleanup
    this.waveMesh = new THREE.Mesh(this.waveGeometry, this.waveMaterial);
    this.waveMesh.rotation.x = -Math.PI / 2;
    this.waveMesh.position.y = -2;
    this.scene.add(this.waveMesh);
  }

  private createCMBBoundary(scale: ScalePoint): void {
    if (this.boundarySphere) {
      this.scene.remove(this.boundarySphere);
      this.boundarySphere.geometry.dispose();
      if (this.boundarySphere.material instanceof THREE.Material) {
        this.boundarySphere.material.dispose();
      }
    }

    // CMB boundary at z=1089
    const radius = 100; // Scaled for visualization
    const geometry = new THREE.SphereGeometry(radius, 64, 64);
    const material = new THREE.MeshStandardMaterial({
      color: 0xd69e2e,
      metalness: 0.9,
      roughness: 0.1,
      emissive: 0x332200,
      emissiveIntensity: 0.5,
      transparent: true,
      opacity: 0.3,
      wireframe: true,
    });

    this.boundarySphere = new THREE.Mesh(geometry, material);
    this.scene.add(this.boundarySphere);
  }

  private getGridSize(scale: ScalePoint): number {
    // Scale grid size based on current scale domain
    const baseSize = 10;
    const log10 = scale.log10;
    
    if (log10 < -15) return baseSize * 0.1; // Planck scale
    if (log10 < -10) return baseSize * 0.5; // Atomic scale
    if (log10 < 0) return baseSize; // Molecular/macroscopic
    if (log10 < 15) return baseSize * 2; // Stellar
    if (log10 < 21) return baseSize * 5; // Galactic
    return baseSize * 10; // Cosmological
  }

  private calculatePressure(distance: number, scale: ScalePoint, intensity: number): number {
    // Pressure calculation based on scale
    // At cosmological scales: pressure from CMB boundary
    // At smaller scales: local pressure field
    
    if (scale.domain === 'cosmological') {
      // Pressure decreases from CMB boundary
      return Math.max(0, 1.0 - distance / 50) * intensity;
    } else {
      // Local pressure field (simplified)
      return (1.0 - 0.3 / (distance + 0.1)) * intensity;
    }
  }

  dispose(): void {
    // Remove from scene
    if (this.pressureField) {
      this.scene.remove(this.pressureField);
      this.pressureField.geometry.dispose();
      if (this.pressureField.material instanceof THREE.Material) {
        this.pressureField.material.dispose();
      }
      this.pressureField = null;
    }
    
    // FIX #2: Cleanup wave mesh
    if (this.waveMesh) {
      this.scene.remove(this.waveMesh);
      // Geometry and material are shared, dispose separately
      this.waveMesh = null;
    }
    
    if (this.waveGeometry) {
      this.waveGeometry.dispose();
      this.waveGeometry = null;
    }
    if (this.waveMaterial) {
      this.waveMaterial.dispose();
      this.waveMaterial = null;
    }
    
    if (this.boundarySphere) {
      this.scene.remove(this.boundarySphere);
      this.boundarySphere.geometry.dispose();
      if (this.boundarySphere.material instanceof THREE.Material) {
        this.boundarySphere.material.dispose();
      }
      this.boundarySphere = null;
    }
  }
}

export const PressureFieldRenderer: React.FC<PressureFieldRendererProps & { scene: THREE.Scene }> = ({
  scene,
  scale,
  intensity = 1.0,
  showWaves = true,
  showBoundary = false,
}) => {
  const visualizationRef = useRef<PressureFieldVisualization | null>(null);

  useEffect(() => {
    if (!visualizationRef.current) {
      visualizationRef.current = new PressureFieldVisualization(scene);
    }

    visualizationRef.current.update(scale, intensity, showWaves, showBoundary);

    return () => {
      // Cleanup handled by dispose if needed
    };
  }, [scene, scale, intensity, showWaves, showBoundary]);

  return null; // This component doesn't render anything directly
};

