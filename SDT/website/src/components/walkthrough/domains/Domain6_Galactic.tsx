/**
 * Domain 6: Galactic Scale
 * 10^15 to 10^21 m
 * Galaxy disk, eclipse saturation, rotation curves
 */

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { ScalePoint } from '../ScaleManager';
import { IDomainVisualization } from './DomainBase';

interface Domain6Props {
  scene: THREE.Scene;
  scale: ScalePoint;
}

export class Domain6Visualization implements IDomainVisualization {
  private scene: THREE.Scene;
  private galaxyDisk: THREE.Mesh | null = null;
  private rotationCurve: THREE.Line | null = null;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  initialize(scale: ScalePoint): void {
    this.clear();
    
    if (scale.name === 'Galactic Disk') {
      this.createGalaxy();
      this.createRotationCurve();
    }
  }

  private createGalaxy(): void {
    const diskRadius = 5;
    const diskGeometry = new THREE.CylinderGeometry(diskRadius, diskRadius, 0.2, 64);
    const diskMaterial = new THREE.MeshStandardMaterial({
      color: 0x4a5568,
      metalness: 0.3,
      roughness: 0.7,
      transparent: true,
      opacity: 0.6,
      side: THREE.DoubleSide,
    });
    
    this.galaxyDisk = new THREE.Mesh(diskGeometry, diskMaterial);
    this.galaxyDisk.rotation.x = Math.PI / 2;
    this.scene.add(this.galaxyDisk);

    // Central bulge
    const bulgeGeometry = new THREE.SphereGeometry(0.3, 32, 32);
    const bulgeMaterial = new THREE.MeshStandardMaterial({
      color: 0xffd700,
      emissive: 0x332200,
      emissiveIntensity: 0.4,
    });
    const bulge = new THREE.Mesh(bulgeGeometry, bulgeMaterial);
    this.scene.add(bulge);
  }

  private createRotationCurve(): void {
    // Flat rotation curve from eclipse saturation
    const points: THREE.Vector3[] = [];
    for (let r = 0.5; r < 5; r += 0.2) {
      const v = r < 2.5 ? Math.sqrt(r) : Math.sqrt(2.5); // Flat beyond R_flat
      points.push(new THREE.Vector3(r, v * 0.5, 0));
    }

    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({
      color: 0xd69e2e,
      linewidth: 3,
    });

    this.rotationCurve = new THREE.Line(geometry, material);
    this.rotationCurve.position.y = 1;
    this.scene.add(this.rotationCurve);
  }

  update(deltaTime: number): void {
    if (this.galaxyDisk) {
      this.scene.rotation.y += deltaTime * 0.05;
    }
  }

  private clear(): void {
    const objects = [this.galaxyDisk, this.rotationCurve];
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

export const Domain6_Galactic: React.FC<Domain6Props> = ({ scene, scale }) => {
  const vizRef = useRef<Domain6Visualization | null>(null);
  
  useEffect(() => {
    if (!vizRef.current) {
      vizRef.current = new Domain6Visualization(scene);
    }
    vizRef.current.initialize(scale);
  }, [scene, scale]);
  
  return null;
};

