/**
 * Domain 4: Macroscopic Scale
 * 10^-6 to 10^6 m
 * Human scale, planetary scale, gravity from pressure gradients
 */

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { ScalePoint } from '../ScaleManager';
import { IDomainVisualization } from './DomainBase';

interface Domain4Props {
  scene: THREE.Scene;
  scale: ScalePoint;
}

export class Domain4Visualization implements IDomainVisualization {
  private scene: THREE.Scene;
  private earth: THREE.Mesh | null = null;
  private gravityField: THREE.Points | null = null;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  initialize(scale: ScalePoint): void {
    this.clear();
    
    if (scale.name === 'Earth Radius') {
      this.createEarth();
      this.createGravityField();
    }
  }

  private createEarth(): void {
    const geometry = new THREE.SphereGeometry(1, 32, 32);
    const material = new THREE.MeshStandardMaterial({
      color: 0x4a90e2,
      metalness: 0.3,
      roughness: 0.7,
    });
    
    // Add texture or simple color
    this.earth = new THREE.Mesh(geometry, material);
    this.scene.add(this.earth);
  }

  private createGravityField(): void {
    // Show pressure gradients creating gravity
    const positions: number[] = [];
    const colors: number[] = [];
    
    for (let r = 1.5; r < 5; r += 0.3) {
      for (let theta = 0; theta < Math.PI * 2; theta += 0.3) {
        const x = r * Math.cos(theta);
        const z = r * Math.sin(theta);
        const y = 0;
        
        positions.push(x, y, z);
        
        // Pressure decreases with distance
        const pressure = 1 / (r * r);
        const color = new THREE.Color();
        color.lerpColors(new THREE.Color(0x1a365d), new THREE.Color(0xd69e2e), pressure);
        colors.push(color.r, color.g, color.b);
      }
    }
    
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    
    const material = new THREE.PointsMaterial({
      size: 0.2,
      vertexColors: true,
      transparent: true,
      opacity: 0.6,
    });
    
    this.gravityField = new THREE.Points(geometry, material);
    this.scene.add(this.gravityField);
  }

  update(deltaTime: number): void {
    if (this.earth) {
      this.earth.rotation.y += deltaTime * 0.1;
    }
  }

  private clear(): void {
    const objects = [this.earth, this.gravityField];
    objects.forEach(obj => {
      if (obj) {
        this.scene.remove(obj);
        obj.geometry.dispose();
        if (obj.material instanceof THREE.Material) {
          obj.material.dispose();
        }
      }
    });
  }

  dispose(): void {
    this.clear();
  }
}

export const Domain4_Macroscopic: React.FC<Domain4Props> = ({ scene, scale }) => {
  const vizRef = useRef<Domain4Visualization | null>(null);
  
  useEffect(() => {
    if (!vizRef.current) {
      vizRef.current = new Domain4Visualization(scene);
    }
    vizRef.current.initialize(scale);
  }, [scene, scale]);
  
  return null;
};

