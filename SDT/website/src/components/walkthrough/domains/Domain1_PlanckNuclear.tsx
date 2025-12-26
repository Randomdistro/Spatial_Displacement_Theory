/**
 * Domain 1: Planck/Nuclear Scale
 * 10^-35 to 10^-15 m
 * Spation lattice, K_bulk, nuclear forces from CMB pressure focusing
 */

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { ScalePoint } from '../ScaleManager';
import { IDomainVisualization } from './DomainBase';

interface Domain1Props {
  scene: THREE.Scene;
  scale: ScalePoint;
  onComplete?: () => void;
}

export class Domain1Visualization implements IDomainVisualization {
  private scene: THREE.Scene;
  private spationLattice: THREE.Group | null = null;
  private kBulkVisualization: THREE.Mesh | null = null;
  private pressureFocusing: THREE.Line | null = null;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  initialize(scale: ScalePoint): void {
    this.clear();
    
    if (scale.name === 'Spation Lattice') {
      this.createSpationLattice();
      this.createKBulkVisualization();
    } else if (scale.name === 'Proton Radius') {
      this.createProtonStructure();
      this.createPressureFocusing();
    }
  }

  private createSpationLattice(): void {
    // Create dodecahedral packing visualization
    const group = new THREE.Group();
    
    // Create central spation
    const centralGeometry = new THREE.SphereGeometry(0.1, 16, 16);
    const centralMaterial = new THREE.MeshStandardMaterial({
      color: 0x4a90e2,
      metalness: 0.9,
      roughness: 0.1,
      emissive: 0x001122,
      emissiveIntensity: 0.3,
    });
    const central = new THREE.Mesh(centralGeometry, centralMaterial);
    group.add(central);

    // Create 12 surrounding spations (dodecahedral packing)
    const radius = 0.2;
    const positions = this.getDodecahedralPositions(radius);
    
    positions.forEach((pos, index) => {
      const geometry = new THREE.SphereGeometry(0.08, 16, 16);
      const material = new THREE.MeshStandardMaterial({
        color: 0x1a365d,
        metalness: 0.8,
        roughness: 0.2,
        emissive: 0x000811,
        emissiveIntensity: 0.2,
      });
      const spation = new THREE.Mesh(geometry, material);
      spation.position.set(pos.x, pos.y, pos.z);
      group.add(spation);

      // Add connection lines
      const lineGeometry = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(pos.x, pos.y, pos.z),
      ]);
      const lineMaterial = new THREE.LineBasicMaterial({
        color: 0x4a90e2,
        transparent: true,
        opacity: 0.3,
      });
      const line = new THREE.Line(lineGeometry, lineMaterial);
      group.add(line);
    });

    this.spationLattice = group;
    this.scene.add(group);
  }

  private getDodecahedralPositions(radius: number): THREE.Vector3[] {
    // Simplified dodecahedral positions (12-around-1)
    const positions: THREE.Vector3[] = [];
    const phi = (1 + Math.sqrt(5)) / 2; // Golden ratio
    
    // Icosahedral vertices (simplified)
    const vertices = [
      [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi],
      [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
      [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1],
    ];

    vertices.forEach(([x, y, z]) => {
      const length = Math.sqrt(x * x + y * y + z * z);
      positions.push(new THREE.Vector3(
        (x / length) * radius,
        (y / length) * radius,
        (z / length) * radius
      ));
    });

    return positions;
  }

  private createKBulkVisualization(): void {
    // Visualize K_bulk = 4.6×10¹¹³ Pa as pressure field intensity
    const geometry = new THREE.SphereGeometry(2, 32, 32);
    const material = new THREE.MeshStandardMaterial({
      color: 0xd69e2e,
      metalness: 0.9,
      roughness: 0.1,
      emissive: 0x332200,
      emissiveIntensity: 0.5,
      transparent: true,
      opacity: 0.4,
    });
    
    this.kBulkVisualization = new THREE.Mesh(geometry, material);
    this.scene.add(this.kBulkVisualization);

    // Add pulsing animation
    const pulse = () => {
      if (this.kBulkVisualization) {
        const scale = 1 + Math.sin(Date.now() * 0.001) * 0.1;
        this.kBulkVisualization.scale.set(scale, scale, scale);
      }
      requestAnimationFrame(pulse);
    };
    pulse();
  }

  private createProtonStructure(): void {
    // Proton as pressure structure
    const geometry = new THREE.SphereGeometry(0.5, 32, 32);
    const material = new THREE.MeshStandardMaterial({
      color: 0xff4444,
      metalness: 0.9,
      roughness: 0.1,
      emissive: 0x330000,
      emissiveIntensity: 0.6,
    });
    
    const proton = new THREE.Mesh(geometry, material);
    this.scene.add(proton);
  }

  private createPressureFocusing(): void {
    // Show pressure focusing from cosmos to proton scale
    const points: THREE.Vector3[] = [];
    const steps = 50;
    
    for (let i = 0; i <= steps; i++) {
      const t = i / steps;
      const angle = t * Math.PI * 2;
      const radius = 5 * (1 - t);
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;
      const z = t * 10 - 5;
      points.push(new THREE.Vector3(x, y, z));
    }

    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({
      color: 0xd69e2e,
      transparent: true,
      opacity: 0.6,
      linewidth: 2,
    });

    this.pressureFocusing = new THREE.Line(geometry, material);
    this.scene.add(this.pressureFocusing);
  }

  update(deltaTime: number): void {
    // Rotate spation lattice slowly
    if (this.spationLattice) {
      this.spationLattice.rotation.y += deltaTime * 0.1;
    }
  }

  private clear(): void {
    if (this.spationLattice) {
      this.scene.remove(this.spationLattice);
      this.spationLattice.traverse((child) => {
        if (child instanceof THREE.Mesh || child instanceof THREE.Line) {
          child.geometry.dispose();
          if (child.material instanceof THREE.Material) {
            child.material.dispose();
          }
        }
      });
    }
    if (this.kBulkVisualization) {
      this.scene.remove(this.kBulkVisualization);
      this.kBulkVisualization.geometry.dispose();
      if (this.kBulkVisualization.material instanceof THREE.Material) {
        this.kBulkVisualization.material.dispose();
      }
    }
    if (this.pressureFocusing) {
      this.scene.remove(this.pressureFocusing);
      this.pressureFocusing.geometry.dispose();
      if (this.pressureFocusing.material instanceof THREE.Material) {
        this.pressureFocusing.material.dispose();
      }
    }
  }

  dispose(): void {
    this.clear();
  }
}

export const Domain1_PlanckNuclear: React.FC<Domain1Props> = ({
  scene,
  scale,
  onComplete,
}) => {
  const visualizationRef = useRef<Domain1Visualization | null>(null);

  useEffect(() => {
    if (!visualizationRef.current) {
      visualizationRef.current = new Domain1Visualization(scene);
    }

    visualizationRef.current.initialize(scale);

    return () => {
      // Cleanup handled by dispose
    };
  }, [scene, scale]);

  return null;
};

