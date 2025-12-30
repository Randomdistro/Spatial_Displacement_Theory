/**
 * The Clearing Simulation - Recombination Era from SDT Perspective
 * Agent 3: Physics/Simulation
 *
 * Visualizes the moment when the universe became transparent,
 * showing the transition from opaque plasma to clear space
 * and what this means from Spatial Displacement Theory perspective.
 */

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { SimulationBase, SimulationProps } from './SimulationBase';

interface TheClearingSimProps extends SimulationProps {
  parameters: {
    temperature?: number; // Current temperature in Kelvin
    opacity?: number; // Plasma opacity (0-1)
    particleCount?: number; // Number of particles to simulate
    transitionSpeed?: number; // Speed of phase transition
    showPressureFields?: boolean; // Show SDT pressure field visualization
  };
}

enum Phase {
  PLASMA_OPAQUE = 'plasma_opaque',
  COOLING_TRANSITION = 'cooling_transition',
  RECOMBINATION = 'recombination',
  CLEAR_TRANSPARENT = 'clear_transparent'
}

class TheClearingSimulation extends SimulationBase {
  // Plasma particles (baryons and electrons)
  private baryonParticles: THREE.Points | null = null;
  private electronParticles: THREE.Points | null = null;

  // Photon scattering visualization
  private photonCloud: THREE.Points | null = null;

  // Pressure field visualization (SDT)
  private pressureField: THREE.Points | null = null;

  // Matter clumps (nuclei with bound electrons)
  private matterClumps: THREE.Group | null = null;

  // Phase tracking
  private currentPhase: Phase = Phase.PLASMA_OPAQUE;
  private phaseProgress: number = 0; // 0-1 within current phase

  // Physical constants for simulation
  private readonly RECOMBINATION_TEMP = 2970; // Kelvin
  private readonly PLASMA_TEMP_START = 10000; // Kelvin
  private readonly PLASMA_TEMP_END = 2500; // Kelvin

  init(): void {
    // Clear existing objects
    while (this.scene.children.length > 0) {
      const child = this.scene.children[0];
      if (child instanceof THREE.Light) {
        // Keep lights
        continue;
      }
      this.scene.remove(child);
      this.disposeObject(child);
    }

    // Set initial camera position
    this.camera.position.set(0, 0, 15);
    this.camera.lookAt(0, 0, 0);

    // Create the simulation elements
    this.createPlasmaSoup();
    this.createPhotonScattering();
    this.createPressureFields();
    this.createMatterClumps();

    // Start in plasma phase
    this.setPhase(Phase.PLASMA_OPAQUE);
  }

  private createPlasmaSoup(): void {
    const particleCount = this.parameters.particleCount || 2000;

    // Baryon particles (protons/neutrons) - slightly larger, blue-ish
    const baryonGeometry = new THREE.BufferGeometry();
    const baryonPositions = new Float32Array(particleCount * 3);
    const baryonColors = new Float32Array(particleCount * 3);
    const baryonSizes = new Float32Array(particleCount);

    // Electron particles - smaller, red-orange
    const electronGeometry = new THREE.BufferGeometry();
    const electronPositions = new Float32Array(particleCount * 3);
    const electronColors = new Float32Array(particleCount * 3);
    const electronSizes = new Float32Array(particleCount);

    // Distribute particles in a rough sphere representing the universe
    for (let i = 0; i < particleCount; i++) {
      // Random spherical distribution
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const radius = Math.random() * 8 + 2; // 2-10 unit radius

      const x = radius * Math.sin(phi) * Math.cos(theta);
      const y = radius * Math.sin(phi) * Math.sin(theta);
      const z = radius * Math.cos(phi);

      // Baryons (more massive, clustered)
      baryonPositions[i * 3] = x + (Math.random() - 0.5) * 0.5;
      baryonPositions[i * 3 + 1] = y + (Math.random() - 0.5) * 0.5;
      baryonPositions[i * 3 + 2] = z + (Math.random() - 0.5) * 0.5;

      // Red hot plasma color
      baryonColors[i * 3] = 1.0;     // R
      baryonColors[i * 3 + 1] = 0.3; // G
      baryonColors[i * 3 + 2] = 0.1; // B
      baryonSizes[i] = 2.0;

      // Electrons (more spread out)
      electronPositions[i * 3] = x + (Math.random() - 0.5) * 1.0;
      electronPositions[i * 3 + 1] = y + (Math.random() - 0.5) * 1.0;
      electronPositions[i * 3 + 2] = z + (Math.random() - 0.5) * 1.0;

      // Hot electron color
      electronColors[i * 3] = 1.0;     // R
      electronColors[i * 3 + 1] = 0.6; // G
      electronColors[i * 3 + 2] = 0.2; // B
      electronSizes[i] = 1.0;
    }

    baryonGeometry.setAttribute('position', new THREE.BufferAttribute(baryonPositions, 3));
    baryonGeometry.setAttribute('color', new THREE.BufferAttribute(baryonColors, 3));
    baryonGeometry.setAttribute('size', new THREE.BufferAttribute(baryonSizes, 1));

    const baryonMaterial = new THREE.PointsMaterial({
      size: 0.05,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      sizeAttenuation: true
    });

    this.baryonParticles = new THREE.Points(baryonGeometry, baryonMaterial);
    this.scene.add(this.baryonParticles);

    electronGeometry.setAttribute('position', new THREE.BufferAttribute(electronPositions, 3));
    electronGeometry.setAttribute('color', new THREE.BufferAttribute(electronColors, 3));
    electronGeometry.setAttribute('size', new THREE.BufferAttribute(electronSizes, 1));

    const electronMaterial = new THREE.PointsMaterial({
      size: 0.03,
      vertexColors: true,
      transparent: true,
      opacity: 0.9,
      sizeAttenuation: true
    });

    this.electronParticles = new THREE.Points(electronGeometry, electronMaterial);
    this.scene.add(this.electronParticles);
  }

  private createPhotonScattering(): void {
    const photonCount = 1000;

    const photonGeometry = new THREE.BufferGeometry();
    const photonPositions = new Float32Array(photonCount * 3);
    const photonColors = new Float32Array(photonCount * 3);

    // Photons scattering everywhere in the plasma
    for (let i = 0; i < photonCount; i++) {
      photonPositions[i * 3] = (Math.random() - 0.5) * 20;
      photonPositions[i * 3 + 1] = (Math.random() - 0.5) * 20;
      photonPositions[i * 3 + 2] = (Math.random() - 0.5) * 20;

      // CMB photon colors (blackbody spectrum)
      photonColors[i * 3] = 1.0;     // R
      photonColors[i * 3 + 1] = 0.8; // G
      photonColors[i * 3 + 2] = 0.6; // B
    }

    photonGeometry.setAttribute('position', new THREE.BufferAttribute(photonPositions, 3));
    photonGeometry.setAttribute('color', new THREE.BufferAttribute(photonColors, 3));

    const photonMaterial = new THREE.PointsMaterial({
      size: 0.02,
      vertexColors: true,
      transparent: true,
      opacity: 0.3,
      sizeAttenuation: false
    });

    this.photonCloud = new THREE.Points(photonGeometry, photonMaterial);
    this.scene.add(this.photonCloud);
  }

  private createPressureFields(): void {
    if (!this.parameters.showPressureFields) return;

    const fieldPoints = 500;
    const fieldGeometry = new THREE.BufferGeometry();
    const fieldPositions = new Float32Array(fieldPoints * 3);
    const fieldColors = new Float32Array(fieldPoints * 3);

    // SDT pressure field - spation lattice structure
    for (let i = 0; i < fieldPoints; i++) {
      // Create lattice-like structure
      const x = (i % 10 - 5) * 2;
      const y = (Math.floor(i / 10) % 10 - 5) * 2;
      const z = (Math.floor(i / 100) - 2) * 2;

      fieldPositions[i * 3] = x;
      fieldPositions[i * 3 + 1] = y;
      fieldPositions[i * 3 + 2] = z;

      // Pressure field color (subtle blue)
      fieldColors[i * 3] = 0.2;     // R
      fieldColors[i * 3 + 1] = 0.4; // G
      fieldColors[i * 3 + 2] = 0.8; // B
    }

    fieldGeometry.setAttribute('position', new THREE.BufferAttribute(fieldPositions, 3));
    fieldGeometry.setAttribute('color', new THREE.BufferAttribute(fieldColors, 3));

    const fieldMaterial = new THREE.PointsMaterial({
      size: 0.1,
      vertexColors: true,
      transparent: true,
      opacity: 0.0, // Start invisible
      sizeAttenuation: true
    });

    this.pressureField = new THREE.Points(fieldGeometry, fieldMaterial);
    this.scene.add(this.pressureField);
  }

  private createMatterClumps(): void {
    this.matterClumps = new THREE.Group();

    // Create some hydrogen atoms (proton + electron)
    const clumpCount = 20;
    for (let i = 0; i < clumpCount; i++) {
      const clump = new THREE.Group();

      // Proton (nucleus)
      const protonGeometry = new THREE.SphereGeometry(0.1, 8, 8);
      const protonMaterial = new THREE.MeshStandardMaterial({
        color: 0x4a90e2,
        emissive: 0x1a365d,
        emissiveIntensity: 0.2
      });
      const proton = new THREE.Mesh(protonGeometry, protonMaterial);

      // Electron orbiting
      const electronGeometry = new THREE.SphereGeometry(0.05, 6, 6);
      const electronMaterial = new THREE.MeshStandardMaterial({
        color: 0xff6b35,
        emissive: 0xff4500,
        emissiveIntensity: 0.3
      });
      const electron = new THREE.Mesh(electronGeometry, electronMaterial);
      electron.position.set(0.3, 0, 0);

      clump.add(proton);
      clump.add(electron);

      // Position clumps randomly but clustered
      clump.position.set(
        (Math.random() - 0.5) * 6,
        (Math.random() - 0.5) * 6,
        (Math.random() - 0.5) * 6
      );

      clump.visible = false; // Start invisible
      this.matterClumps.add(clump);
    }

    this.scene.add(this.matterClumps);
  }

  private setPhase(phase: Phase): void {
    this.currentPhase = phase;
    this.phaseProgress = 0;
  }

  update(deltaTime: number): void {
    const temperature = this.parameters.temperature || 3000;
    const opacity = this.parameters.opacity || 0.5;

    // Update phase based on temperature
    if (temperature > this.PLASMA_TEMP_START) {
      this.setPhase(Phase.PLASMA_OPAQUE);
    } else if (temperature > this.RECOMBINATION_TEMP) {
      this.setPhase(Phase.COOLING_TRANSITION);
    } else if (temperature >= this.PLASMA_TEMP_END) {
      this.setPhase(Phase.RECOMBINATION);
    } else {
      this.setPhase(Phase.CLEAR_TRANSPARENT);
    }

    // Update phase progress
    this.phaseProgress = Math.min(this.phaseProgress + deltaTime * (this.parameters.transitionSpeed || 0.5), 1);

    // Update visualization based on phase
    this.updatePlasmaPhase(opacity);
    this.updatePhotonScattering(opacity);
    this.updatePressureFields();
    this.updateMatterClumps();

    // Animate particles
    this.animateParticles(deltaTime);
  }

  private updatePlasmaPhase(opacity: number): void {
    if (!this.baryonParticles || !this.electronParticles) return;

    const baryonMaterial = this.baryonParticles.material as THREE.PointsMaterial;
    const electronMaterial = this.electronParticles.material as THREE.PointsMaterial;

    switch (this.currentPhase) {
      case Phase.PLASMA_OPAQUE:
        // Hot, opaque plasma - particles close together, high scattering
        baryonMaterial.opacity = opacity * 0.9;
        electronMaterial.opacity = opacity;
        break;

      case Phase.COOLING_TRANSITION:
        // Cooling down - particles starting to pair up
        const transitionOpacity = opacity * (1 - this.phaseProgress * 0.3);
        baryonMaterial.opacity = transitionOpacity;
        electronMaterial.opacity = transitionOpacity * 0.8;
        break;

      case Phase.RECOMBINATION:
        // Recombination event - electrons binding to nuclei
        baryonMaterial.opacity = opacity * 0.3;
        electronMaterial.opacity = opacity * 0.1; // Electrons mostly bound
        break;

      case Phase.CLEAR_TRANSPARENT:
        // Universe becomes clear - particles settled, space transparent
        baryonMaterial.opacity = opacity * 0.2;
        electronMaterial.opacity = opacity * 0.05;
        break;
    }
  }

  private updatePhotonScattering(opacity: number): void {
    if (!this.photonCloud) return;

    const photonMaterial = this.photonCloud.material as THREE.PointsMaterial;

    switch (this.currentPhase) {
      case Phase.PLASMA_OPAQUE:
        // Photons trapped, scattering everywhere
        photonMaterial.opacity = opacity * 0.8;
        break;

      case Phase.COOLING_TRANSITION:
        // Photons starting to free up
        photonMaterial.opacity = opacity * 0.6;
        break;

      case Phase.RECOMBINATION:
        // Recombination flash - photons suddenly released
        photonMaterial.opacity = opacity * 1.5 * Math.sin(this.time * 10);
        break;

      case Phase.CLEAR_TRANSPARENT:
        // CMB photons free to travel - universe becomes transparent
        photonMaterial.opacity = opacity * 0.1;
        break;
    }
  }

  private updatePressureFields(): void {
    if (!this.pressureField || !this.parameters.showPressureFields) return;

    const fieldMaterial = this.pressureField.material as THREE.PointsMaterial;

    switch (this.currentPhase) {
      case Phase.PLASMA_OPAQUE:
        // Pressure fields opaque/compressed
        fieldMaterial.opacity = 0.0;
        break;

      case Phase.COOLING_TRANSITION:
        // Fields starting to emerge
        fieldMaterial.opacity = this.phaseProgress * 0.3;
        break;

      case Phase.RECOMBINATION:
        // Fields become visible during recombination
        fieldMaterial.opacity = 0.6 + Math.sin(this.time * 5) * 0.2;
        break;

      case Phase.CLEAR_TRANSPARENT:
        // Clear pressure field structure emerges (SDT revelation)
        fieldMaterial.opacity = 0.8;
        break;
    }
  }

  private updateMatterClumps(): void {
    if (!this.matterClumps) return;

    switch (this.currentPhase) {
      case Phase.PLASMA_OPAQUE:
      case Phase.COOLING_TRANSITION:
        // No stable atoms yet
        this.matterClumps.children.forEach(clump => {
          clump.visible = false;
        });
        break;

      case Phase.RECOMBINATION:
        // Atoms forming during recombination
        this.matterClumps.children.forEach((clump, index) => {
          clump.visible = Math.random() < this.phaseProgress;
          // Animate electron orbiting
          const electron = clump.children[1] as THREE.Mesh;
          const angle = this.time * 2 + index;
          electron.position.set(
            Math.cos(angle) * 0.3,
            Math.sin(angle) * 0.3,
            0
          );
        });
        break;

      case Phase.CLEAR_TRANSPARENT:
        // Stable atoms formed
        this.matterClumps.children.forEach((clump, index) => {
          clump.visible = true;
          // Slower, stable orbits
          const electron = clump.children[1] as THREE.Mesh;
          const angle = this.time * 0.5 + index;
          electron.position.set(
            Math.cos(angle) * 0.3,
            Math.sin(angle) * 0.3,
            Math.sin(angle * 0.5) * 0.1
          );
        });
        break;
    }
  }

  private animateParticles(deltaTime: number): void {
    if (!this.baryonParticles || !this.electronParticles || !this.photonCloud) return;

    // Animate baryons (slower, more massive)
    const baryonPositions = this.baryonParticles.geometry.attributes.position.array as Float32Array;
    for (let i = 0; i < baryonPositions.length; i += 3) {
      const noise = Math.sin(this.time + i * 0.01) * 0.01;
      baryonPositions[i] += noise * deltaTime;
      baryonPositions[i + 1] += noise * deltaTime * 0.5;
    }
    this.baryonParticles.geometry.attributes.position.needsUpdate = true;

    // Animate electrons (faster, lighter)
    const electronPositions = this.electronParticles.geometry.attributes.position.array as Float32Array;
    for (let i = 0; i < electronPositions.length; i += 3) {
      const noise = Math.sin(this.time * 2 + i * 0.01) * 0.02;
      electronPositions[i] += noise * deltaTime;
      electronPositions[i + 1] += noise * deltaTime;
      electronPositions[i + 2] += noise * deltaTime * 0.5;
    }
    this.electronParticles.geometry.attributes.position.needsUpdate = true;

    // Animate photons (very fast scattering)
    const photonPositions = this.photonCloud.geometry.attributes.position.array as Float32Array;
    for (let i = 0; i < photonPositions.length; i += 3) {
      const speed = Math.sin(this.time * 3 + i * 0.001) * 0.1;
      photonPositions[i] += speed * deltaTime;
      photonPositions[i + 1] += speed * deltaTime * 0.7;
      photonPositions[i + 2] += speed * deltaTime * 0.5;

      // Wrap around boundaries
      if (Math.abs(photonPositions[i]) > 12) photonPositions[i] *= -0.9;
      if (Math.abs(photonPositions[i + 1]) > 12) photonPositions[i + 1] *= -0.9;
      if (Math.abs(photonPositions[i + 2]) > 12) photonPositions[i + 2] *= -0.9;
    }
    this.photonCloud.geometry.attributes.position.needsUpdate = true;
  }

  dispose(): void {
    this.disposeObject(this.baryonParticles);
    this.disposeObject(this.electronParticles);
    this.disposeObject(this.photonCloud);
    this.disposeObject(this.pressureField);
    this.disposeObject(this.matterClumps);

    this.baryonParticles = null;
    this.electronParticles = null;
    this.photonCloud = null;
    this.pressureField = null;
    this.matterClumps = null;
  }

  private disposeObject(object: THREE.Object3D | null): void {
    if (!object) return;

    object.traverse((child) => {
      if (child instanceof THREE.Mesh || child instanceof THREE.Points) {
        child.geometry.dispose();
        if (Array.isArray(child.material)) {
          child.material.forEach(material => material.dispose());
        } else {
          child.material.dispose();
        }
      }
    });

    if (object.parent) {
      object.parent.remove(object);
    }
  }
}

// React component wrapper
export default function TheClearingSim(props: TheClearingSimProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const simulationRef = useRef<TheClearingSimulation | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    simulationRef.current = new TheClearingSimulation(containerRef.current);
    simulationRef.current.init();
    simulationRef.current.setParameters(props.parameters);
    simulationRef.current.play();

    if (props.onReady) {
      props.onReady();
    }

    return () => {
      if (simulationRef.current) {
        simulationRef.current.destroy();
      }
    };
  }, []);

  useEffect(() => {
    if (simulationRef.current) {
      simulationRef.current.setParameters(props.parameters);
    }
  }, [props.parameters]);

  return (
    <div
      ref={containerRef}
      className="w-full h-full min-h-[400px] bg-gradient-to-b from-red-900/20 to-blue-900/20 rounded-lg overflow-hidden"
      style={{ touchAction: 'none' }}
    >
      {/* Loading placeholder */}
      <div className="absolute inset-0 flex items-center justify-center bg-slate-900/80 rounded-lg">
        <div className="text-center text-slate-300">
          <div className="text-lg font-semibold mb-2">The Clearing</div>
          <div className="text-sm opacity-75">Recombination Era • SDT Perspective</div>
          <div className="mt-4 w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
        </div>
      </div>
    </div>
  );
}
