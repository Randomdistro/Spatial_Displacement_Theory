/**
 * Force Hierarchy Visualization
 * Shows how all forces emerge from CMB pressure field
 * World-class interactive visualization
 */

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { FormulaRenderer } from '../simulations/FormulaRenderer';

interface ForceHierarchyVisualizationProps {
  scene: THREE.Scene;
  show: boolean;
  highlightForce?: 'coulomb' | 'gravity' | 'nuclear' | 'all';
}

export class ForceHierarchyViz {
  private scene: THREE.Scene;
  private forceBars: THREE.Mesh[] = [];
  private cmbSource: THREE.Mesh | null = null;
  private forceConnections: THREE.Line[] = [];
  private labels: THREE.Group | null = null;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  createVisualization(highlightForce?: 'coulomb' | 'gravity' | 'nuclear' | 'all'): void {
    this.clear();

    // Create CMB source (center)
    const sourceGeometry = new THREE.SphereGeometry(0.3, 32, 32);
    const sourceMaterial = new THREE.MeshStandardMaterial({
      color: 0xd69e2e,
      emissive: 0x332200,
      emissiveIntensity: 0.8,
      metalness: 0.9,
      roughness: 0.1,
    });
    this.cmbSource = new THREE.Mesh(sourceGeometry, sourceMaterial);
    this.scene.add(this.cmbSource);

    // Create force bars (logarithmic scale)
    const forces = [
      { name: 'Nuclear', strength: 1.0, color: 0xff4444, position: [0, 2, 0] },
      { name: 'Coulomb', strength: 10e-2, color: 0x4a90e2, position: [0, 1, 0] },
      { name: 'Weak', strength: 10e-5, color: 0x8b5cf6, position: [0, 0, 0] },
      { name: 'Gravity', strength: 10e-39, color: 0x10b981, position: [0, -1, 0] },
    ];

    forces.forEach((force, index) => {
      // Bar height represents force strength (logarithmic)
      const logStrength = Math.log10(force.strength + 1e-40);
      const height = Math.max(0.1, (logStrength + 40) * 0.1);
      
      const barGeometry = new THREE.BoxGeometry(0.3, height, 0.3);
      const barMaterial = new THREE.MeshStandardMaterial({
        color: force.color,
        metalness: 0.7,
        roughness: 0.3,
        emissive: force.color,
        emissiveIntensity: highlightForce === 'all' || 
          (highlightForce === 'coulomb' && force.name === 'Coulomb') ||
          (highlightForce === 'gravity' && force.name === 'Gravity') ||
          (highlightForce === 'nuclear' && force.name === 'Nuclear')
          ? 0.5 : 0.1,
      });
      
      const bar = new THREE.Mesh(barGeometry, barMaterial);
      bar.position.set(
        force.position[0],
        force.position[1] + height / 2,
        force.position[2]
      );
      
      this.forceBars.push(bar);
      this.scene.add(bar);

      // Connection line from CMB source
      const lineGeometry = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(force.position[0], force.position[1], force.position[2]),
      ]);
      const lineMaterial = new THREE.LineBasicMaterial({
        color: force.color,
        transparent: true,
        opacity: 0.3,
      });
      const line = new THREE.Line(lineGeometry, lineMaterial);
      this.forceConnections.push(line);
      this.scene.add(line);
    });

    // Create label group
    this.createLabels(forces);
  }

  private createLabels(forces: Array<{ name: string; position: number[] }>): void {
    const group = new THREE.Group();
    
    forces.forEach((force) => {
      // Label background
      const labelGeometry = new THREE.PlaneGeometry(0.8, 0.2);
      const labelMaterial = new THREE.MeshBasicMaterial({
        color: 0x000000,
        transparent: true,
        opacity: 0.7,
      });
      const label = new THREE.Mesh(labelGeometry, labelMaterial);
      label.position.set(
        force.position[0] + 0.5,
        force.position[1],
        force.position[2]
      );
      label.lookAt(0, force.position[1], 0);
      group.add(label);
    });

    this.labels = group;
    this.scene.add(group);
  }

  animate(deltaTime: number): void {
    // Pulse CMB source
    if (this.cmbSource) {
      const pulse = 1 + Math.sin(Date.now() * 0.001) * 0.1;
      this.cmbSource.scale.set(pulse, pulse, pulse);
    }

    // Rotate force bars slightly
    this.forceBars.forEach((bar, index) => {
      bar.rotation.y += deltaTime * (0.1 + index * 0.05);
    });
  }

  private clear(): void {
    this.forceBars.forEach(bar => {
      this.scene.remove(bar);
      bar.geometry.dispose();
      if (bar.material instanceof THREE.Material) {
        bar.material.dispose();
      }
    });
    this.forceConnections.forEach(line => {
      this.scene.remove(line);
      line.geometry.dispose();
      if (line.material instanceof THREE.Material) {
        line.material.dispose();
      }
    });
    if (this.cmbSource) {
      this.scene.remove(this.cmbSource);
      this.cmbSource.geometry.dispose();
      if (this.cmbSource.material instanceof THREE.Material) {
        this.cmbSource.material.dispose();
      }
    }
    if (this.labels) {
      this.scene.remove(this.labels);
      this.labels.traverse((child) => {
        if (child instanceof THREE.Mesh) {
          child.geometry.dispose();
          if (child.material instanceof THREE.Material) {
            child.material.dispose();
          }
        }
      });
    }
    this.forceBars = [];
    this.forceConnections = [];
    this.cmbSource = null;
    this.labels = null;
  }

  dispose(): void {
    this.clear();
  }
}

export const ForceHierarchyVisualization: React.FC<ForceHierarchyVisualizationProps> = ({
  scene,
  show,
  highlightForce,
}) => {
  const vizRef = useRef<ForceHierarchyViz | null>(null);
  const animationFrameRef = useRef<number | null>(null);

  useEffect(() => {
    if (!vizRef.current) {
      vizRef.current = new ForceHierarchyViz(scene);
    }

    if (show) {
      vizRef.current.createVisualization(highlightForce);
      
      // Animation loop
      let lastTime = performance.now();
      const animate = () => {
        const currentTime = performance.now();
        const deltaTime = (currentTime - lastTime) / 1000;
        lastTime = currentTime;
        
        if (vizRef.current) {
          vizRef.current.animate(deltaTime);
        }
        
        animationFrameRef.current = requestAnimationFrame(animate);
      };
      animate();
    } else {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      vizRef.current.clear();
    }

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [scene, show, highlightForce]);

  return null;
};

