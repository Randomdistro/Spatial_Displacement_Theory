/**
 * Orbital Mechanics Simulation
 * Agent 3: Physics/Simulation
 * 
 * 3D visualization of orbital motion using SDT k-law
 * Demonstrates universal velocity law across scales
 */

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { SimulationBase, SimulationProps } from './SimulationBase';

interface OrbitalSimProps extends SimulationProps {
  parameters: {
    kValue?: number; // Scale-dependent k
    R_eff?: number; // Effective radius of central body (m)
    orbitalRadius?: number; // Orbital radius (m)
    scale?: 'atomic' | 'planetary' | 'galactic';
    showTrail?: boolean;
    showVelocityVector?: boolean;
    showPressureField?: boolean;
  };
}

// Physical constants
const C = 299792458; // Speed of light (m/s)

class OrbitalSimulation extends SimulationBase {
  private centralBody: THREE.Mesh | null = null;
  private orbiter: THREE.Mesh | null = null;
  private trail: THREE.Line | null = null;
  private trailPoints: THREE.Vector3[] = [];
  private velocityVector: THREE.ArrowHelper | null = null;
  private pressureField: THREE.Points | null = null;
  
  private currentAngle: number = 0;
  private orbitalRadius: number = 5;
  private orbitalVelocity: number = 0;
  private orbitalPeriod: number = 0;
  private timeScale: number = 1; // Speed multiplier for visualization

  init(): void {
    // Clear existing objects
    while (this.scene.children.length > 0) {
      const child = this.scene.children[0];
      if (child instanceof THREE.Light) {
        // Keep lights
      } else {
        this.scene.remove(child);
        if (child instanceof THREE.Mesh || child instanceof THREE.Points || child instanceof THREE.Line) {
          child.geometry.dispose();
          if (child.material instanceof THREE.Material) {
            child.material.dispose();
          }
        }
        if (child instanceof THREE.ArrowHelper) {
          child.dispose();
        }
      }
    }

    const k = this.parameters.kValue || 137.036;
    const R_eff = this.parameters.R_eff || 5.29177e-11; // Default: Bohr radius
    const r = this.parameters.orbitalRadius || 5.29177e-11;
    
    // Calculate orbital parameters using SDT k-law
    this.orbitalRadius = this.scaleRadius(r, R_eff);
    this.orbitalVelocity = (C / k) * Math.sqrt(R_eff / r);
    this.orbitalPeriod = (2 * Math.PI * k * Math.sqrt(r * r * r / R_eff)) / C;
    
    // Scale time for visualization (make orbits visible)
    this.timeScale = this.calculateTimeScale(this.orbitalPeriod);

    // Create central body
    const centralRadius = this.scaleRadius(R_eff, R_eff) * 0.1;
    const centralGeometry = new THREE.SphereGeometry(centralRadius, 32, 32);
    const centralMaterial = new THREE.MeshStandardMaterial({
      color: 0xffd700, // Gold
      metalness: 0.9,
      roughness: 0.1,
      emissive: 0x332200,
      emissiveIntensity: 0.3,
    });
    this.centralBody = new THREE.Mesh(centralGeometry, centralMaterial);
    this.scene.add(this.centralBody);

    // Create orbiter
    const orbiterRadius = centralRadius * 0.3;
    const orbiterGeometry = new THREE.SphereGeometry(orbiterRadius, 16, 16);
    const orbiterMaterial = new THREE.MeshStandardMaterial({
      color: 0x4a90e2, // Blue
      metalness: 0.7,
      roughness: 0.3,
    });
    this.orbiter = new THREE.Mesh(orbiterGeometry, orbiterMaterial);
    this.orbiter.position.set(this.orbitalRadius, 0, 0);
    this.scene.add(this.orbiter);

    // Create orbital trail
    if (this.parameters.showTrail !== false) {
      this.trailPoints = [];
      const trailGeometry = new THREE.BufferGeometry();
      const trailMaterial = new THREE.LineBasicMaterial({
        color: 0x4a90e2,
        transparent: true,
        opacity: 0.6,
        linewidth: 2,
      });
      this.trail = new THREE.Line(trailGeometry, trailMaterial);
      this.scene.add(this.trail);
    }

    // Create velocity vector
    if (this.parameters.showVelocityVector !== false) {
      const direction = new THREE.Vector3(0, 1, 0); // Perpendicular to radius
      const origin = this.orbiter.position.clone();
      const length = this.orbitalVelocity * 0.1; // Scaled for visualization
      this.velocityVector = new THREE.ArrowHelper(
        direction,
        origin,
        length,
        0x00ff00, // Green
        0.1,
        0.05
      );
      this.scene.add(this.velocityVector);
    }

    // Create pressure field visualization
    if (this.parameters.showPressureField) {
      this.createPressureField();
    }

    // Create orbital plane indicator
    const planeGeometry = new THREE.RingGeometry(this.orbitalRadius * 0.9, this.orbitalRadius * 1.1, 64);
    const planeMaterial = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.1,
      side: THREE.DoubleSide,
    });
    const plane = new THREE.Mesh(planeGeometry, planeMaterial);
    plane.rotation.x = Math.PI / 2;
    this.scene.add(plane);

    // Position camera
    this.camera.position.set(0, 8, 12);
    this.camera.lookAt(0, 0, 0);
  }

  private scaleRadius(radius: number, reference: number): number {
    // Scale radius for visualization (logarithmic scaling for atomic scales)
    if (this.parameters.scale === 'atomic') {
      // Atomic: scale to visible size
      return Math.log10(radius / reference + 1) * 2 + 0.5;
    } else if (this.parameters.scale === 'planetary') {
      // Planetary: direct scaling with reduction
      return radius / 1e10; // Scale down for visualization
    } else {
      // Galactic: logarithmic scaling
      return Math.log10(radius / reference + 1) * 3;
    }
  }

  private calculateTimeScale(period: number): number {
    // Calculate time scale to make orbit visible (target: 10 seconds per orbit)
    const targetPeriod = 10; // seconds
    return targetPeriod / period;
  }

  private createPressureField(): void {
    const positions: number[] = [];
    const colors: number[] = [];
    const resolution = 15;
    const gridSize = this.orbitalRadius * 3;

    for (let x = -gridSize; x < gridSize; x += gridSize / resolution) {
      for (let y = -gridSize; y < gridSize; y += gridSize / resolution) {
        for (let z = -gridSize / 2; z < gridSize / 2; z += gridSize / resolution) {
          const distance = Math.sqrt(x * x + y * y + z * z);
          if (distance < this.orbitalRadius * 0.2) continue;
          if (distance > this.orbitalRadius * 2) continue;

          const pressure = 1.0 - 0.3 / (distance + 0.1);
          positions.push(x, y, z);

          const color = new THREE.Color();
          color.lerpColors(
            new THREE.Color(0x1a365d),
            new THREE.Color(0xd69e2e),
            Math.max(0, Math.min(1, pressure))
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
      opacity: 0.4,
    });

    this.pressureField = new THREE.Points(geometry, material);
    this.scene.add(this.pressureField);
  }

  update(deltaTime: number): void {
    if (!this.orbiter) return;

    // Update orbital angle
    const angularVelocity = (2 * Math.PI) / this.orbitalPeriod * this.timeScale;
    this.currentAngle += angularVelocity * deltaTime;

    // Update orbiter position
    const x = this.orbitalRadius * Math.cos(this.currentAngle);
    const y = this.orbitalRadius * Math.sin(this.currentAngle);
    this.orbiter.position.set(x, 0, y);

    // Update trail
    if (this.trail && this.parameters.showTrail !== false) {
      this.trailPoints.push(new THREE.Vector3(x, 0, y));
      // Limit trail length
      if (this.trailPoints.length > 200) {
        this.trailPoints.shift();
      }
      const trailGeometry = new THREE.BufferGeometry().setFromPoints(this.trailPoints);
      this.trail.geometry.dispose();
      this.trail.geometry = trailGeometry;
    }

    // Update velocity vector
    if (this.velocityVector && this.parameters.showVelocityVector !== false) {
      const tangent = new THREE.Vector3(-Math.sin(this.currentAngle), 0, Math.cos(this.currentAngle));
      const length = this.orbitalVelocity * 0.1;
      this.velocityVector.setDirection(tangent);
      this.velocityVector.position.copy(this.orbiter.position);
      this.velocityVector.setLength(length);
    }

    // Rotate scene slowly for better view
    this.scene.rotation.y += deltaTime * 0.1;
  }

  protected onParametersChanged(): void {
    // Reinitialize when parameters change
    this.init();
  }

  dispose(): void {
    if (this.centralBody) {
      this.centralBody.geometry.dispose();
      if (this.centralBody.material instanceof THREE.Material) {
        this.centralBody.material.dispose();
      }
    }
    if (this.orbiter) {
      this.orbiter.geometry.dispose();
      if (this.orbiter.material instanceof THREE.Material) {
        this.orbiter.material.dispose();
      }
    }
    if (this.trail) {
      this.trail.geometry.dispose();
      if (this.trail.material instanceof THREE.Material) {
        this.trail.material.dispose();
      }
    }
    if (this.pressureField) {
      this.pressureField.geometry.dispose();
      if (this.pressureField.material instanceof THREE.Material) {
        this.pressureField.material.dispose();
      }
    }
    if (this.velocityVector) {
      this.velocityVector.dispose();
    }
  }
}

export const OrbitalSim: React.FC<OrbitalSimProps> = ({
  id,
  parameters,
  onParameterChange,
  showFormulas = true,
  showLabels = true,
  narrationEnabled = false,
  onReady,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const simulationRef = useRef<OrbitalSimulation | null>(null);
  const [orbitalData, setOrbitalData] = useState({
    velocity: 0,
    period: 0,
    k: 0,
  });

  useEffect(() => {
    if (!containerRef.current) return;

    // Initialize simulation
    const sim = new OrbitalSimulation(containerRef.current);
    sim.setParameters({
      kValue: 137.036,
      R_eff: 5.29177e-11, // Bohr radius
      orbitalRadius: 5.29177e-11,
      scale: 'atomic',
      showTrail: true,
      showVelocityVector: true,
      showPressureField: false,
      ...parameters,
    });
    sim.init();
    simulationRef.current = sim;

    // Calculate and display orbital data
    const k = parameters.kValue || 137.036;
    const R_eff = parameters.R_eff || 5.29177e-11;
    const r = parameters.orbitalRadius || 5.29177e-11;
    const v = (C / k) * Math.sqrt(R_eff / r);
    const T = (2 * Math.PI * k * Math.sqrt(r * r * r / R_eff)) / C;
    
    setOrbitalData({
      velocity: v,
      period: T,
      k: k,
    });

    if (onReady) {
      setTimeout(onReady, 100);
    }

    sim.play();

    return () => {
      sim.destroy();
      simulationRef.current = null;
    };
  }, [onReady]);

  useEffect(() => {
    if (simulationRef.current) {
      simulationRef.current.setParameters(parameters);
      
      // Update orbital data
      const k = parameters.kValue || 137.036;
      const R_eff = parameters.R_eff || 5.29177e-11;
      const r = parameters.orbitalRadius || 5.29177e-11;
      const v = (C / k) * Math.sqrt(R_eff / r);
      const T = (2 * Math.PI * k * Math.sqrt(r * r * r / R_eff)) / C;
      
      setOrbitalData({
        velocity: v,
        period: T,
        k: k,
      });
    }
  }, [parameters]);

  const formatValue = (value: number, unit: string): string => {
    if (value >= 1e6) return `${(value / 1e6).toFixed(2)} M${unit}`;
    if (value >= 1e3) return `${(value / 1e3).toFixed(2)} k${unit}`;
    if (value >= 1) return `${value.toFixed(2)} ${unit}`;
    if (value >= 1e-3) return `${(value * 1e3).toFixed(2)} m${unit}`;
    if (value >= 1e-6) return `${(value * 1e6).toFixed(2)} μ${unit}`;
    return `${value.toExponential(2)} ${unit}`;
  };

  return (
    <div className="relative w-full h-full">
      <div
        ref={containerRef}
        className="w-full h-full min-h-[500px] bg-slate-900 rounded-lg"
      />
      {showLabels && (
        <div className="absolute bottom-4 left-4 bg-black/70 backdrop-blur-sm text-white p-4 rounded-lg text-sm max-w-xs">
          <div className="font-semibold mb-3 text-amber-400">Orbital Parameters</div>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">k-value:</span>
              <span className="font-mono">{orbitalData.k.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Velocity:</span>
              <span className="font-mono">{formatValue(orbitalData.velocity, 'm/s')}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Period:</span>
              <span className="font-mono">{formatValue(orbitalData.period, 's')}</span>
            </div>
            <div className="mt-3 pt-3 border-t border-slate-600 text-slate-300">
              <div className="text-xs">v = (c/k)√(R/r)</div>
            </div>
          </div>
        </div>
      )}
      {showFormulas && (
        <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm text-white p-3 rounded-lg text-xs font-mono">
          <div>v(r) = (c/k)√(R/r)</div>
          <div className="mt-2 text-slate-400 text-[10px]">
            Universal k-law
          </div>
        </div>
      )}
    </div>
  );
};

