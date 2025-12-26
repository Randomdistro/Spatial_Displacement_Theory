/**
 * Domain 2: Atomic Scale
 * 10^-15 to 10^-10 m
 * Proton structure, electron torus, Bohr radius, Coulomb force from CMB occlusion
 */

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { ScalePoint } from '../ScaleManager';
import { IDomainVisualization } from './DomainBase';

interface Domain2Props {
  scene: THREE.Scene;
  scale: ScalePoint;
  onComplete?: () => void;
}

export class Domain2Visualization implements IDomainVisualization {
  private scene: THREE.Scene;
  private proton: THREE.Mesh | null = null;
  private electronTorus: THREE.Mesh | null = null;
  private helicalWave: THREE.Line | null = null;
  private occlusionVisualization: THREE.Points | null = null;
  private time: number = 0;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  initialize(scale: ScalePoint): void {
    this.clear();

    if (scale.name === 'Electron Torus') {
      this.createElectronTorus();
      this.createHelicalWave();
    } else if (scale.name === 'Bohr Radius') {
      this.createCompleteAtom();
      this.createOcclusionVisualization();
    }
  }

  private createElectronTorus(): void {
    const torusRadius = 1.0;
    const tubeRadius = 0.15;
    const geometry = new THREE.TorusGeometry(torusRadius, tubeRadius, 16, 64);
    const material = new THREE.MeshStandardMaterial({
      color: 0x4a90e2,
      metalness: 0.7,
      roughness: 0.3,
      transparent: true,
      opacity: 0.8,
      side: THREE.DoubleSide,
    });
    
    this.electronTorus = new THREE.Mesh(geometry, material);
    this.electronTorus.rotation.x = Math.PI / 2;
    this.scene.add(this.electronTorus);
  }

  private createHelicalWave(): void {
    const points: THREE.Vector3[] = [];
    const segments = 200;
    const n = 1; // Principal quantum number
    const radius = 1.0;

    for (let i = 0; i <= segments; i++) {
      const t = (i / segments) * Math.PI * 2;
      const r = radius * (1 + 0.1 * Math.sin(n * t));
      const x = r * Math.cos(t);
      const y = r * Math.sin(t);
      const z = (i / segments - 0.5) * 0.5 * Math.sin(t);
      points.push(new THREE.Vector3(x, z, y));
    }

    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({
      color: 0x00ff88,
      linewidth: 2,
      transparent: true,
      opacity: 0.7,
    });

    this.helicalWave = new THREE.Line(geometry, material);
    this.scene.add(this.helicalWave);
  }

  private createCompleteAtom(): void {
    // Proton (nucleus)
    const protonGeometry = new THREE.SphereGeometry(0.2, 32, 32);
    const protonMaterial = new THREE.MeshStandardMaterial({
      color: 0xff4444,
      metalness: 0.9,
      roughness: 0.1,
      emissive: 0x330000,
      emissiveIntensity: 0.5,
    });
    this.proton = new THREE.Mesh(protonGeometry, protonMaterial);
    this.scene.add(this.proton);

    // Electron torus at Bohr radius
    const bohrRadius = 2.0; // Scaled for visualization
    const torusGeometry = new THREE.TorusGeometry(bohrRadius, 0.15, 16, 64);
    const torusMaterial = new THREE.MeshStandardMaterial({
      color: 0x4a90e2,
      metalness: 0.7,
      roughness: 0.3,
      transparent: true,
      opacity: 0.8,
    });
    this.electronTorus = new THREE.Mesh(torusGeometry, torusMaterial);
    this.electronTorus.rotation.x = Math.PI / 2;
    this.scene.add(this.electronTorus);
  }

  private createOcclusionVisualization(): void {
    // Show mutual occlusion creating Coulomb force
    const positions: number[] = [];
    const colors: number[] = [];
    const resolution = 20;
    const gridSize = 5;

    for (let x = -gridSize; x < gridSize; x += gridSize / resolution) {
      for (let y = -gridSize; y < gridSize; y += gridSize / resolution) {
        for (let z = -gridSize / 2; z < gridSize / 2; z += gridSize / resolution) {
          const distance = Math.sqrt(x * x + y * y + z * z);
          if (distance < 0.3 || distance > 4) continue;

          // Occlusion: particles block each other's view of CMB
          const occlusion = this.calculateOcclusion(x, y, z);
          
          positions.push(x, y, z);
          
          const color = new THREE.Color();
          color.lerpColors(
            new THREE.Color(0x1a365d), // Low occlusion (blue)
            new THREE.Color(0xd69e2e), // High occlusion (gold)
            occlusion
          );
          colors.push(color.r, color.g, color.b);
        }
      }
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.1,
      vertexColors: true,
      transparent: true,
      opacity: 0.5,
    });

    this.occlusionVisualization = new THREE.Points(geometry, material);
    this.scene.add(this.occlusionVisualization);
  }

  private calculateOcclusion(x: number, y: number, z: number): number {
    // Simplified occlusion: particles block CMB view
    const distToProton = Math.sqrt(x * x + y * y + z * z);
    const distToElectron = Math.sqrt((x - 2) * (x - 2) + y * y + z * z);
    
    // Occlusion increases when both particles are in line of sight
    const occlusion = Math.max(0, 1 - distToProton / 5) * Math.max(0, 1 - distToElectron / 5);
    return Math.min(1, occlusion);
  }

  update(deltaTime: number): void {
    this.time += deltaTime;

    // Rotate electron torus
    if (this.electronTorus) {
      this.electronTorus.rotation.z += deltaTime * 0.5;
    }

    // Animate helical wave
    if (this.helicalWave) {
      const points: THREE.Vector3[] = [];
      const segments = 200;
      const n = 1;
      const radius = 1.0;
      const phase = this.time * 2;

      for (let i = 0; i <= segments; i++) {
        const t = (i / segments) * Math.PI * 2;
        const r = radius * (1 + 0.1 * Math.sin(n * t + phase));
        const x = r * Math.cos(t);
        const y = r * Math.sin(t);
        const z = (i / segments - 0.5) * 0.5 * Math.sin(t + phase);
        points.push(new THREE.Vector3(x, z, y));
      }

      this.helicalWave.geometry.dispose();
      this.helicalWave.geometry = new THREE.BufferGeometry().setFromPoints(points);
    }
  }

  private clear(): void {
    const objects = [this.proton, this.electronTorus, this.helicalWave, this.occlusionVisualization];
    objects.forEach(obj => {
      if (obj) {
        this.scene.remove(obj);
        if (obj instanceof THREE.Mesh || obj instanceof THREE.Line || obj instanceof THREE.Points) {
          obj.geometry.dispose();
          if (obj.material instanceof THREE.Material) {
            obj.material.dispose();
          }
        }
      }
    });
  }

  dispose(): void {
    this.clear();
  }
}

export const Domain2_Atomic: React.FC<Domain2Props> = ({
  scene,
  scale,
  onComplete,
}) => {
  const visualizationRef = useRef<Domain2Visualization | null>(null);

  useEffect(() => {
    if (!visualizationRef.current) {
      visualizationRef.current = new Domain2Visualization(scene);
    }

    visualizationRef.current.initialize(scale);

    return () => {
      // Cleanup handled by dispose
    };
  }, [scene, scale]);

  return null;
};

