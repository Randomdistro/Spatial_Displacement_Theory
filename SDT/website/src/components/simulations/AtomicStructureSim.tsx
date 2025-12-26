/**
 * Atomic Structure Simulation
 * Agent 3: Physics/Simulation
 * 
 * 3D visualization of SDT's toroidal electron model
 * Shows helical standing waves and orbital structure
 */

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { SimulationBase, SimulationProps } from './SimulationBase';

interface AtomicStructureSimProps extends SimulationProps {
  parameters: {
    element?: string; // Element symbol (default: 'H')
    atomicNumber?: number; // Z
    principalQuantumNumber?: number; // n
    showElectrons?: boolean;
    showPressureField?: boolean;
    showHelicalWaves?: boolean;
    showNucleus?: boolean;
  };
}

class AtomicStructureSimulation extends SimulationBase {
  private nucleus: THREE.Mesh | null = null;
  private electronTorus: THREE.Mesh | null = null;
  private helicalWave: THREE.Line | null = null;
  private pressureField: THREE.Points | null = null;
  private orbitalPlane: THREE.Mesh | null = null;
  
  private time: number = 0;
  private n: number = 1; // Principal quantum number
  private Z: number = 1; // Atomic number

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
      }
    }

    this.n = this.parameters.principalQuantumNumber || 1;
    this.Z = this.parameters.atomicNumber || 1;

    // Calculate orbital radius (Bohr model: r = n² a₀ / Z)
    const a0 = 5.29177e-11; // Bohr radius
    const orbitalRadius = (this.n * this.n * a0) / this.Z;
    const scaledRadius = Math.log10(orbitalRadius / a0 + 1) * 2 + 0.5;

    // Create nucleus
    if (this.parameters.showNucleus !== false) {
      const nucleusRadius = 0.2;
      const nucleusGeometry = new THREE.SphereGeometry(nucleusRadius, 32, 32);
      const nucleusMaterial = new THREE.MeshStandardMaterial({
        color: 0xff4444, // Red
        metalness: 0.9,
        roughness: 0.1,
        emissive: 0x330000,
        emissiveIntensity: 0.5,
      });
      this.nucleus = new THREE.Mesh(nucleusGeometry, nucleusMaterial);
      this.scene.add(this.nucleus);
    }

    // Create toroidal electron
    if (this.parameters.showElectrons !== false) {
      const torusRadius = scaledRadius;
      const tubeRadius = 0.15;
      const torusGeometry = new THREE.TorusGeometry(torusRadius, tubeRadius, 16, 64);
      const torusMaterial = new THREE.MeshStandardMaterial({
        color: 0x4a90e2, // Blue
        metalness: 0.7,
        roughness: 0.3,
        transparent: true,
        opacity: 0.8,
        side: THREE.DoubleSide,
      });
      this.electronTorus = new THREE.Mesh(torusGeometry, torusMaterial);
      this.electronTorus.rotation.x = Math.PI / 2;
      this.scene.add(this.electronTorus);
    }

    // Create helical standing wave
    if (this.parameters.showHelicalWaves !== false) {
      this.createHelicalWave(scaledRadius);
    }

    // Create pressure field
    if (this.parameters.showPressureField) {
      this.createPressureField(scaledRadius);
    }

    // Create orbital plane indicator
    const planeGeometry = new THREE.RingGeometry(scaledRadius * 0.9, scaledRadius * 1.1, 64);
    const planeMaterial = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.05,
      side: THREE.DoubleSide,
    });
    this.orbitalPlane = new THREE.Mesh(planeGeometry, planeMaterial);
    this.orbitalPlane.rotation.x = Math.PI / 2;
    this.scene.add(this.orbitalPlane);

    // Position camera
    this.camera.position.set(0, 5, 8);
    this.camera.lookAt(0, 0, 0);
  }

  private createHelicalWave(radius: number): void {
    const points: THREE.Vector3[] = [];
    const segments = 200;
    const n = this.n; // Number of helical turns
    const m = this.Z; // Number of nodes

    for (let i = 0; i <= segments; i++) {
      const t = (i / segments) * Math.PI * 2;
      const r = radius * (1 + 0.1 * Math.sin(n * t)); // Radial modulation
      const x = r * Math.cos(t);
      const y = r * Math.sin(t);
      const z = (i / segments - 0.5) * 0.5 * Math.sin(m * t); // Helical component
      points.push(new THREE.Vector3(x, z, y));
    }

    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({
      color: 0x00ff88, // Cyan-green
      linewidth: 2,
      transparent: true,
      opacity: 0.7,
    });
    this.helicalWave = new THREE.Line(geometry, material);
    this.scene.add(this.helicalWave);
  }

  private createPressureField(radius: number): void {
    const positions: number[] = [];
    const colors: number[] = [];
    const resolution = 20;
    const gridSize = radius * 3;

    for (let x = -gridSize; x < gridSize; x += gridSize / resolution) {
      for (let y = -gridSize; y < gridSize; y += gridSize / resolution) {
        for (let z = -gridSize / 2; z < gridSize / 2; z += gridSize / resolution) {
          const distance = Math.sqrt(x * x + y * y + z * z);
          if (distance < radius * 0.3) continue;
          if (distance > radius * 2) continue;

          // Pressure field with angular dependence (electron exclusion)
          const angle = Math.atan2(y, x);
          const pressure = 1.0 - 0.4 / (distance + 0.1) * (1 + 0.3 * Math.cos(n * angle));
          
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
      size: 0.08,
      vertexColors: true,
      transparent: true,
      opacity: 0.3,
    });

    this.pressureField = new THREE.Points(geometry, material);
    this.scene.add(this.pressureField);
  }

  update(deltaTime: number): void {
    this.time += deltaTime;

    // Rotate electron torus
    if (this.electronTorus) {
      this.electronTorus.rotation.z += deltaTime * 0.5;
    }

    // Animate helical wave
    if (this.helicalWave) {
      // Update wave geometry with time-dependent phase
      const points: THREE.Vector3[] = [];
      const segments = 200;
      const n = this.n;
      const m = this.Z;
      const radius = Math.log10((this.n * this.n * 5.29177e-11) / this.Z / 5.29177e-11 + 1) * 2 + 0.5;
      const phase = this.time * 2; // Wave propagation

      for (let i = 0; i <= segments; i++) {
        const t = (i / segments) * Math.PI * 2;
        const r = radius * (1 + 0.1 * Math.sin(n * t + phase));
        const x = r * Math.cos(t);
        const y = r * Math.sin(t);
        const z = (i / segments - 0.5) * 0.5 * Math.sin(m * t + phase);
        points.push(new THREE.Vector3(x, z, y));
      }

      this.helicalWave.geometry.dispose();
      this.helicalWave.geometry = new THREE.BufferGeometry().setFromPoints(points);
    }

    // Rotate scene slowly
    this.scene.rotation.y += deltaTime * 0.1;
  }

  protected onParametersChanged(): void {
    this.init();
  }

  dispose(): void {
    if (this.nucleus) {
      this.nucleus.geometry.dispose();
      if (this.nucleus.material instanceof THREE.Material) {
        this.nucleus.material.dispose();
      }
    }
    if (this.electronTorus) {
      this.electronTorus.geometry.dispose();
      if (this.electronTorus.material instanceof THREE.Material) {
        this.electronTorus.material.dispose();
      }
    }
    if (this.helicalWave) {
      this.helicalWave.geometry.dispose();
      if (this.helicalWave.material instanceof THREE.Material) {
        this.helicalWave.material.dispose();
      }
    }
    if (this.pressureField) {
      this.pressureField.geometry.dispose();
      if (this.pressureField.material instanceof THREE.Material) {
        this.pressureField.material.dispose();
      }
    }
    if (this.orbitalPlane) {
      this.orbitalPlane.geometry.dispose();
      if (this.orbitalPlane.material instanceof THREE.Material) {
        this.orbitalPlane.material.dispose();
      }
    }
  }
}

export const AtomicStructureSim: React.FC<AtomicStructureSimProps> = ({
  id,
  parameters,
  onParameterChange,
  showFormulas = true,
  showLabels = true,
  narrationEnabled = false,
  onReady,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const simulationRef = useRef<AtomicStructureSimulation | null>(null);
  const [atomicData, setAtomicData] = useState({
    element: 'H',
    Z: 1,
    n: 1,
    radius: 0,
  });

  useEffect(() => {
    if (!containerRef.current) return;

    const element = parameters.element || 'H';
    const Z = parameters.atomicNumber || 1;
    const n = parameters.principalQuantumNumber || 1;

    // Initialize simulation
    const sim = new AtomicStructureSimulation(containerRef.current);
    sim.setParameters({
      element: element,
      atomicNumber: Z,
      principalQuantumNumber: n,
      showElectrons: true,
      showPressureField: false,
      showHelicalWaves: true,
      showNucleus: true,
      ...parameters,
    });
    sim.init();
    simulationRef.current = sim;

    // Calculate atomic data
    const a0 = 5.29177e-11;
    const radius = (n * n * a0) / Z;

    setAtomicData({
      element: element,
      Z: Z,
      n: n,
      radius: radius,
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
      
      const element = parameters.element || 'H';
      const Z = parameters.atomicNumber || 1;
      const n = parameters.principalQuantumNumber || 1;
      const a0 = 5.29177e-11;
      const radius = (n * n * a0) / Z;

      setAtomicData({
        element: element,
        Z: Z,
        n: n,
        radius: radius,
      });
    }
  }, [parameters]);

  return (
    <div className="relative w-full h-full">
      <div
        ref={containerRef}
        className="w-full h-full min-h-[500px] bg-slate-900 rounded-lg"
      />
      {showLabels && (
        <div className="absolute bottom-4 left-4 bg-black/70 backdrop-blur-sm text-white p-4 rounded-lg text-sm max-w-xs">
          <div className="font-semibold mb-3 text-amber-400">Atomic Structure</div>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Element:</span>
              <span className="font-mono">{atomicData.element}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Z (Atomic #):</span>
              <span className="font-mono">{atomicData.Z}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">n (Quantum #):</span>
              <span className="font-mono">{atomicData.n}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Orbital Radius:</span>
              <span className="font-mono">{(atomicData.radius * 1e12).toFixed(2)} pm</span>
            </div>
            <div className="mt-3 pt-3 border-t border-slate-600 text-slate-300">
              <div className="text-xs">Toroidal Electron Model</div>
              <div className="text-xs text-slate-400">Helical standing waves</div>
            </div>
          </div>
        </div>
      )}
      {showFormulas && (
        <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm text-white p-3 rounded-lg text-xs font-mono">
          <div>r = n²a₀/Z</div>
          <div className="mt-2 text-slate-400 text-[10px]">
            SDT Atomic Model
          </div>
        </div>
      )}
    </div>
  );
};

