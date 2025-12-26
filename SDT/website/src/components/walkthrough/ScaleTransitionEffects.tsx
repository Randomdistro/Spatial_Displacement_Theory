/**
 * Scale Transition Effects
 * World-class visual effects for scale transitions
 * Power-of-10 markers, scale comparisons, smooth transitions
 */

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { ScalePoint } from './ScaleManager';

interface ScaleTransitionEffectsProps {
  scene: THREE.Scene;
  fromScale: ScalePoint;
  toScale: ScalePoint;
  progress: number; // 0 to 1
}

export class ScaleTransitionEffects {
  private scene: THREE.Scene;
  private powerOf10Markers: THREE.Group | null = null;
  private scaleComparison: THREE.Group | null = null;
  private transitionParticles: THREE.Points | null = null;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  createTransition(fromScale: ScalePoint, toScale: ScalePoint, progress: number): void {
    this.clear();

    const scaleDiff = toScale.log10 - fromScale.log10;
    
    // Create power-of-10 markers for large transitions
    if (Math.abs(scaleDiff) > 5) {
      this.createPowerOf10Markers(fromScale, toScale, progress);
    }

    // Create scale comparison visualization
    this.createScaleComparison(fromScale, toScale, progress);

    // Create transition particles effect
    if (progress > 0 && progress < 1) {
      this.createTransitionParticles(progress);
    }
  }

  private createPowerOf10Markers(fromScale: ScalePoint, toScale: ScalePoint, progress: number): void {
    const group = new THREE.Group();
    const startLog = fromScale.log10;
    const endLog = toScale.log10;
    const direction = endLog > startLog ? 1 : -1;
    
    // Create markers at each power of 10
    const startPower = Math.floor(startLog);
    const endPower = Math.ceil(endLog);
    
    for (let power = startPower; power <= endPower; power++) {
      const markerProgress = (power - startLog) / (endLog - startLog);
      if (markerProgress < 0 || markerProgress > 1) continue;

      const geometry = new THREE.RingGeometry(0.05, 0.08, 16);
      const material = new THREE.MeshBasicMaterial({
        color: 0xd69e2e,
        transparent: true,
        opacity: 0.6,
        side: THREE.DoubleSide,
      });
      const marker = new THREE.Mesh(geometry, material);
      
      const angle = markerProgress * Math.PI * 2;
      const radius = 3;
      marker.position.set(
        Math.cos(angle) * radius,
        Math.sin(angle) * radius * 0.5,
        0
      );
      
      group.add(marker);

      // Add text label (simplified - in production use TextGeometry)
      const labelGeometry = new THREE.PlaneGeometry(0.3, 0.1);
      const labelMaterial = new THREE.MeshBasicMaterial({
        color: 0xffffff,
        transparent: true,
        opacity: 0.8,
      });
      const label = new THREE.Mesh(labelGeometry, labelMaterial);
      label.position.copy(marker.position);
      label.position.y += 0.2;
      group.add(label);
    }

    this.powerOf10Markers = group;
    this.scene.add(group);
  }

  private createScaleComparison(fromScale: ScalePoint, toScale: ScalePoint, progress: number): void {
    const group = new THREE.Group();

    // Show relative sizes
    const fromSize = Math.log10(fromScale.meters + 1) * 0.5;
    const toSize = Math.log10(toScale.meters + 1) * 0.5;
    const currentSize = fromSize + (toSize - fromSize) * progress;

    // From scale indicator
    const fromGeometry = new THREE.SphereGeometry(fromSize, 16, 16);
    const fromMaterial = new THREE.MeshBasicMaterial({
      color: 0x4a90e2,
      transparent: true,
      opacity: 0.3,
      wireframe: true,
    });
    const fromSphere = new THREE.Mesh(fromGeometry, fromMaterial);
    fromSphere.position.set(-2, 0, 0);
    group.add(fromSphere);

    // To scale indicator
    const toGeometry = new THREE.SphereGeometry(toSize, 16, 16);
    const toMaterial = new THREE.MeshBasicMaterial({
      color: 0xd69e2e,
      transparent: true,
      opacity: 0.3,
      wireframe: true,
    });
    const toSphere = new THREE.Mesh(toGeometry, toMaterial);
    toSphere.position.set(2, 0, 0);
    group.add(toSphere);

    // Current scale (interpolated)
    const currentGeometry = new THREE.SphereGeometry(currentSize, 16, 16);
    const currentMaterial = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.5,
      wireframe: true,
    });
    const currentSphere = new THREE.Mesh(currentGeometry, currentMaterial);
    currentSphere.position.set(0, 0, 0);
    group.add(currentSphere);

    this.scene.add(group);
  }

  private createTransitionParticles(progress: number): void {
    const particleCount = 100;
    const positions: number[] = [];
    const colors: number[] = [];
    const sizes: number[] = [];

    for (let i = 0; i < particleCount; i++) {
      const angle = (i / particleCount) * Math.PI * 2;
      const radius = 5 + Math.sin(progress * Math.PI) * 2;
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;
      const z = (Math.random() - 0.5) * 2;

      positions.push(x, y, z);

      // Color based on progress
      const color = new THREE.Color();
      color.lerpColors(
        new THREE.Color(0x4a90e2),
        new THREE.Color(0xd69e2e),
        progress
      );
      colors.push(color.r, color.g, color.b);

      sizes.push(0.1 + Math.random() * 0.2);
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    geometry.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));

    const material = new THREE.PointsMaterial({
      size: 0.2,
      vertexColors: true,
      transparent: true,
      opacity: 0.6 * (1 - Math.abs(progress - 0.5) * 2),
    });

    this.transitionParticles = new THREE.Points(geometry, material);
    this.scene.add(this.transitionParticles);
  }

  clear(): void {
    const objects = [this.powerOf10Markers, this.scaleComparison, this.transitionParticles];
    objects.forEach(obj => {
      if (obj) {
        this.scene.remove(obj);
        if (obj instanceof THREE.Group) {
          obj.traverse((child) => {
            if (child instanceof THREE.Mesh || child instanceof THREE.Points) {
              child.geometry.dispose();
              if (child.material instanceof THREE.Material) {
                child.material.dispose();
              }
            }
          });
        } else {
          obj.geometry.dispose();
          if (obj.material instanceof THREE.Material) {
            obj.material.dispose();
          }
        }
      }
    });
    this.powerOf10Markers = null;
    this.scaleComparison = null;
    this.transitionParticles = null;
  }

  dispose(): void {
    this.clear();
  }
}

export const ScaleTransitionEffectsComponent: React.FC<ScaleTransitionEffectsProps> = ({
  scene,
  fromScale,
  toScale,
  progress,
}) => {
  const effectsRef = useRef<ScaleTransitionEffects | null>(null);

  useEffect(() => {
    if (!effectsRef.current) {
      effectsRef.current = new ScaleTransitionEffects(scene);
    }

    effectsRef.current.createTransition(fromScale, toScale, progress);

    return () => {
      // Cleanup handled by clear
    };
  }, [scene, fromScale, toScale, progress]);

  return null;
};

