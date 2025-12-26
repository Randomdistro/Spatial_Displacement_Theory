/**
 * Domain 7: Cosmological Scale
 * 10^21 to 10^26 m
 * Large-scale structure, BAO scale, CMB boundary
 */

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { ScalePoint } from '../ScaleManager';
import { IDomainVisualization } from './DomainBase';

interface Domain7Props {
  scene: THREE.Scene;
  scale: ScalePoint;
}

export class Domain7Visualization implements IDomainVisualization {
  private scene: THREE.Scene;
  private cmbBoundary: THREE.Mesh | null = null;
  private pressureVolumes: THREE.Mesh[] = [];
  private countingVisualization: THREE.Group | null = null;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  initialize(scale: ScalePoint): void {
    this.clear();
    
    if (scale.name === 'BAO Scale') {
      this.createBAOScale();
    } else if (scale.name === 'CMB Boundary') {
      this.createCMBBoundary();
      this.createCountingVisualization();
    }
  }

  private createBAOScale(): void {
    // Baryon Acoustic Oscillation scale (147 Mpc)
    const radius = 10;
    const geometry = new THREE.SphereGeometry(radius, 64, 64);
    const material = new THREE.MeshStandardMaterial({
      color: 0xec4899,
      transparent: true,
      opacity: 0.2,
      wireframe: true,
    });
    
    const bao = new THREE.Mesh(geometry, material);
    this.scene.add(bao);
  }

  private createCMBBoundary(): void {
    // CMB boundary at z=1089 - the ultimate boundary
    const radius = 100;
    const geometry = new THREE.SphereGeometry(radius, 64, 64);
    const material = new THREE.MeshStandardMaterial({
      color: 0xd69e2e,
      metalness: 0.9,
      roughness: 0.1,
      emissive: 0x332200,
      emissiveIntensity: 0.8,
      transparent: true,
      opacity: 0.4,
      wireframe: true,
    });
    
    this.cmbBoundary = new THREE.Mesh(geometry, material);
    this.scene.add(this.cmbBoundary);

    // Add pulsing effect
    const pulse = () => {
      if (this.cmbBoundary) {
        const scale = 1 + Math.sin(Date.now() * 0.0005) * 0.05;
        this.cmbBoundary.scale.set(scale, scale, scale);
      }
      requestAnimationFrame(pulse);
    };
    pulse();
  }

  private createCountingVisualization(): void {
    // Show nested pressure volumes counting to CMB
    const group = new THREE.Group();
    
    // Create nested spheres representing counted pressure volumes
    for (let i = 1; i <= 10; i++) {
      const radius = i * 10;
      const geometry = new THREE.SphereGeometry(radius, 32, 32);
      const material = new THREE.MeshBasicMaterial({
        color: 0x4a90e2,
        transparent: true,
        opacity: 0.1 / i,
        wireframe: true,
      });
      const sphere = new THREE.Mesh(geometry, material);
      group.add(sphere);
    }

    this.countingVisualization = group;
    this.scene.add(group);
  }

  update(deltaTime: number): void {
    // Rotate counting visualization slowly
    if (this.countingVisualization) {
      this.countingVisualization.rotation.y += deltaTime * 0.02;
    }
  }

  private clear(): void {
    if (this.cmbBoundary) {
      this.scene.remove(this.cmbBoundary);
      this.cmbBoundary.geometry.dispose();
      if (this.cmbBoundary.material instanceof THREE.Material) {
        this.cmbBoundary.material.dispose();
      }
    }
    if (this.countingVisualization) {
      this.scene.remove(this.countingVisualization);
      this.countingVisualization.traverse((child) => {
        if (child instanceof THREE.Mesh) {
          child.geometry.dispose();
          if (child.material instanceof THREE.Material) {
            child.material.dispose();
          }
        }
      });
    }
    this.pressureVolumes.forEach(volume => {
      this.scene.remove(volume);
      volume.geometry.dispose();
      if (volume.material instanceof THREE.Material) {
        volume.material.dispose();
      }
    });
    this.pressureVolumes = [];
  }

  dispose(): void {
    this.clear();
  }
}

export const Domain7_Cosmological: React.FC<Domain7Props> = ({ scene, scale }) => {
  const vizRef = useRef<Domain7Visualization | null>(null);
  
  useEffect(() => {
    if (!vizRef.current) {
      vizRef.current = new Domain7Visualization(scene);
    }
    vizRef.current.initialize(scale);
  }, [scene, scale]);
  
  return null;
};

