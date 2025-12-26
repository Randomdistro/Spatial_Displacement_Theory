/**
 * Domain 5: Stellar Scale
 * 10^6 to 10^15 m
 * Solar system, k-law universality
 */

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { ScalePoint } from '../ScaleManager';
import { IDomainVisualization } from './DomainBase';

interface Domain5Props {
  scene: THREE.Scene;
  scale: ScalePoint;
}

export class Domain5Visualization implements IDomainVisualization {
  private scene: THREE.Scene;
  private sun: THREE.Mesh | null = null;
  private planets: THREE.Mesh[] = [];
  private orbits: THREE.Line[] = [];

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  initialize(scale: ScalePoint): void {
    this.clear();
    
    if (scale.name === 'Solar Radius' || scale.name === 'Earth Orbit') {
      this.createSolarSystem();
    }
  }

  private createSolarSystem(): void {
    // Sun
    const sunGeometry = new THREE.SphereGeometry(0.5, 32, 32);
    const sunMaterial = new THREE.MeshStandardMaterial({
      color: 0xffd700,
      emissive: 0xffaa00,
      emissiveIntensity: 0.8,
    });
    this.sun = new THREE.Mesh(sunGeometry, sunMaterial);
    this.scene.add(this.sun);

    // Earth orbit
    const earthOrbitRadius = 3;
    const orbitGeometry = new THREE.RingGeometry(earthOrbitRadius * 0.95, earthOrbitRadius * 1.05, 64);
    const orbitMaterial = new THREE.MeshBasicMaterial({
      color: 0x4a90e2,
      transparent: true,
      opacity: 0.3,
      side: THREE.DoubleSide,
    });
    const orbit = new THREE.Mesh(orbitGeometry, orbitMaterial);
    orbit.rotation.x = Math.PI / 2;
    this.scene.add(orbit);

    // Earth
    const earthGeometry = new THREE.SphereGeometry(0.1, 16, 16);
    const earthMaterial = new THREE.MeshStandardMaterial({ color: 0x4a90e2 });
    const earth = new THREE.Mesh(earthGeometry, earthMaterial);
    earth.position.set(earthOrbitRadius, 0, 0);
    this.planets.push(earth);
    this.scene.add(earth);
  }

  update(deltaTime: number): void {
    // Animate planets in orbit (simplified)
    this.planets.forEach((planet, index) => {
      const radius = 3 + index * 0.5;
      const angle = Date.now() * 0.0001 * (1 / Math.sqrt(radius)); // Kepler's law
      planet.position.set(
        radius * Math.cos(angle),
        0,
        radius * Math.sin(angle)
      );
    });
  }

  private clear(): void {
    if (this.sun) {
      this.scene.remove(this.sun);
      this.sun.geometry.dispose();
      if (this.sun.material instanceof THREE.Material) {
        this.sun.material.dispose();
      }
    }
    this.planets.forEach(planet => {
      this.scene.remove(planet);
      planet.geometry.dispose();
      if (planet.material instanceof THREE.Material) {
        planet.material.dispose();
      }
    });
    this.orbits.forEach(orbit => {
      this.scene.remove(orbit);
      orbit.geometry.dispose();
      if (orbit.material instanceof THREE.Material) {
        orbit.material.dispose();
      }
    });
    this.planets = [];
    this.orbits = [];
  }

  dispose(): void {
    this.clear();
  }
}

export const Domain5_Stellar: React.FC<Domain5Props> = ({ scene, scale }) => {
  const vizRef = useRef<Domain5Visualization | null>(null);
  
  useEffect(() => {
    if (!vizRef.current) {
      vizRef.current = new Domain5Visualization(scene);
    }
    vizRef.current.initialize(scale);
  }, [scene, scale]);
  
  return null;
};

