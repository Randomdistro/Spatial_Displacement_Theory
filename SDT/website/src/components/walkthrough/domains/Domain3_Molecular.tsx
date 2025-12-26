/**
 * Domain 3: Molecular Scale
 * 10^-10 to 10^-6 m
 * Chemical bonds, pressure equilibria
 */

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { ScalePoint } from '../ScaleManager';
import { IDomainVisualization } from './DomainBase';

interface Domain3Props {
  scene: THREE.Scene;
  scale: ScalePoint;
}

export class Domain3Visualization implements IDomainVisualization {
  private scene: THREE.Scene;
  private molecules: THREE.Group[] = [];

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  initialize(scale: ScalePoint): void {
    this.clear();
    
    if (scale.name === 'H₂ Bond') {
      this.createH2Molecule();
    } else if (scale.name === 'Water Molecule') {
      this.createWaterMolecule();
    }
  }

  private createH2Molecule(): void {
    const group = new THREE.Group();
    
    // Two hydrogen nuclei
    const h1 = this.createNucleus(0x4a90e2, [-0.37e-10 * 1e12, 0, 0]);
    const h2 = this.createNucleus(0x4a90e2, [0.37e-10 * 1e12, 0, 0]);
    group.add(h1);
    group.add(h2);
    
    // Pressure field equilibria visualization
    this.createPressureEquilibria(group);
    
    this.molecules.push(group);
    this.scene.add(group);
  }

  private createWaterMolecule(): void {
    const group = new THREE.Group();
    
    // Oxygen nucleus
    const o = this.createNucleus(0xff4444, [0, 0, 0]);
    group.add(o);
    
    // Two hydrogen nuclei at 104.45° angle
    const angle = 104.45 * Math.PI / 180;
    const h1 = this.createNucleus(0x4a90e2, [Math.cos(angle/2), Math.sin(angle/2), 0]);
    const h2 = this.createNucleus(0x4a90e2, [Math.cos(-angle/2), Math.sin(-angle/2), 0]);
    group.add(h1);
    group.add(h2);
    
    this.molecules.push(group);
    this.scene.add(group);
  }

  private createNucleus(color: number, position: [number, number, number]): THREE.Mesh {
    const geometry = new THREE.SphereGeometry(0.1, 16, 16);
    const material = new THREE.MeshStandardMaterial({
      color: color,
      metalness: 0.9,
      roughness: 0.1,
      emissive: color,
      emissiveIntensity: 0.3,
    });
    const nucleus = new THREE.Mesh(geometry, material);
    nucleus.position.set(position[0], position[1], position[2]);
    return nucleus;
  }

  private createPressureEquilibria(group: THREE.Group): void {
    // Show pressure field around molecule
    const positions: number[] = [];
    const colors: number[] = [];
    
    for (let x = -2; x < 2; x += 0.2) {
      for (let y = -2; y < 2; y += 0.2) {
        const distance = Math.sqrt(x * x + y * y);
        if (distance > 0.5 && distance < 2) {
          positions.push(x, y, 0);
          const pressure = 1 - distance / 2;
          const color = new THREE.Color();
          color.lerpColors(new THREE.Color(0x1a365d), new THREE.Color(0xd69e2e), pressure);
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
    
    const points = new THREE.Points(geometry, material);
    group.add(points);
  }

  update(deltaTime: number): void {
    // Rotate molecules slowly
    this.molecules.forEach(mol => {
      mol.rotation.y += deltaTime * 0.2;
    });
  }

  private clear(): void {
    this.molecules.forEach(mol => {
      this.scene.remove(mol);
      mol.traverse((child) => {
        if (child instanceof THREE.Mesh || child instanceof THREE.Points) {
          child.geometry.dispose();
          if (child.material instanceof THREE.Material) {
            child.material.dispose();
          }
        }
      });
    });
    this.molecules = [];
  }

  dispose(): void {
    this.clear();
  }
}

export const Domain3_Molecular: React.FC<Domain3Props> = ({ scene, scale }) => {
  const vizRef = useRef<Domain3Visualization | null>(null);
  
  useEffect(() => {
    if (!vizRef.current) {
      vizRef.current = new Domain3Visualization(scene);
    }
    vizRef.current.initialize(scale);
  }, [scene, scale]);
  
  return null;
};

