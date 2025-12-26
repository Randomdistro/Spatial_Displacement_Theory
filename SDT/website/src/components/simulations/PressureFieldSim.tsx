/**
 * Pressure Field Simulation
 * Agent 3: Physics/Simulation
 * 
 * Visualizes the spation pressure field around matter
 */

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { SimulationBase, SimulationProps } from './SimulationBase';

interface PressureFieldSimProps extends SimulationProps {
  parameters: {
    density?: number; // Spation density (default: 5.2e96)
    bulkModulus?: number; // K_bulk (default: 4.6e113)
    matterRadius?: number; // Matter exclusion radius
    fieldResolution?: number; // Grid resolution for field visualization
  };
}

class PressureFieldSimulation extends SimulationBase {
  private matterSphere: THREE.Mesh | null = null;
  private fieldGeometry: THREE.BufferGeometry | null = null;
  private fieldMaterial: THREE.PointsMaterial | null = null;
  private fieldPoints: THREE.Points | null = null;
  private gridSize: number = 20;
  private gridResolution: number = 30;

  init(): void {
    // Clear existing objects
    while (this.scene.children.length > 0) {
      const child = this.scene.children[0];
      if (child instanceof THREE.Light) {
        // Keep lights
      } else {
        this.scene.remove(child);
        if (child instanceof THREE.Mesh || child instanceof THREE.Points) {
          child.geometry.dispose();
          if (child.material instanceof THREE.Material) {
            child.material.dispose();
          }
        }
      }
    }

    // Create matter sphere (exclusion zone)
    const matterRadius = this.parameters.matterRadius || 1.0;
    const sphereGeometry = new THREE.SphereGeometry(matterRadius, 32, 32);
    const sphereMaterial = new THREE.MeshStandardMaterial({
      color: 0x1a365d,
      metalness: 0.8,
      roughness: 0.2,
      emissive: 0x000000,
    });
    this.matterSphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    this.scene.add(this.matterSphere);

    // Create pressure field visualization
    this.createPressureField();

    // Position camera
    this.camera.position.set(0, 5, 8);
    this.camera.lookAt(0, 0, 0);
  }

  private createPressureField(): void {
    const resolution = this.parameters.fieldResolution || this.gridResolution;
    const positions: number[] = [];
    const colors: number[] = [];
    const sizes: number[] = [];

    const gridSize = this.gridSize;
    const step = gridSize / resolution;
    const matterRadius = this.parameters.matterRadius || 1.0;

    for (let x = -gridSize / 2; x < gridSize / 2; x += step) {
      for (let y = -gridSize / 2; y < gridSize / 2; y += step) {
        for (let z = -gridSize / 2; z < gridSize / 2; z += step) {
          const distance = Math.sqrt(x * x + y * y + z * z);
          
          // Skip points inside matter
          if (distance < matterRadius * 1.1) continue;

          // Calculate pressure (simplified: P = P_inf - k * (1/r))
          const pressure = 1.0 - 0.5 / (distance + 0.1);
          
          positions.push(x, y, z);
          
          // Color based on pressure: blue (low) to gold (high)
          const color = new THREE.Color();
          color.lerpColors(
            new THREE.Color(0x1a365d), // Deep blue (low pressure)
            new THREE.Color(0xd69e2e), // Gold (high pressure)
            Math.max(0, Math.min(1, pressure))
          );
          colors.push(color.r, color.g, color.b);
          
          // Size based on pressure gradient
          sizes.push(0.1 + pressure * 0.2);
        }
      }
    }

    this.fieldGeometry = new THREE.BufferGeometry();
    this.fieldGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    this.fieldGeometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    this.fieldGeometry.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));

    this.fieldMaterial = new THREE.PointsMaterial({
      size: 0.15,
      vertexColors: true,
      transparent: true,
      opacity: 0.6,
      sizeAttenuation: true,
    });

    this.fieldPoints = new THREE.Points(this.fieldGeometry, this.fieldMaterial);
    this.scene.add(this.fieldPoints);
  }

  update(deltaTime: number): void {
    // Rotate the scene for better visualization
    if (this.scene) {
      this.scene.rotation.y += deltaTime * 0.2;
    }
  }

  protected onParametersChanged(): void {
    // Recreate field when parameters change
    if (this.fieldPoints) {
      this.scene.remove(this.fieldPoints);
      this.fieldPoints.geometry.dispose();
      if (this.fieldPoints.material instanceof THREE.Material) {
        this.fieldPoints.material.dispose();
      }
    }
    this.createPressureField();
  }

  dispose(): void {
    if (this.fieldGeometry) this.fieldGeometry.dispose();
    if (this.fieldMaterial) this.fieldMaterial.dispose();
    if (this.matterSphere) {
      this.matterSphere.geometry.dispose();
      if (this.matterSphere.material instanceof THREE.Material) {
        this.matterSphere.material.dispose();
      }
    }
  }
}

export const PressureFieldSim: React.FC<PressureFieldSimProps> = ({
  id,
  parameters,
  onParameterChange,
  showFormulas = true,
  showLabels = true,
  narrationEnabled = false,
  onReady,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const simulationRef = useRef<PressureFieldSimulation | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Initialize simulation
    const sim = new PressureFieldSimulation(containerRef.current);
    sim.setParameters({
      density: 5.2e96,
      bulkModulus: 4.6e113,
      matterRadius: 1.0,
      fieldResolution: 20,
      ...parameters,
    });
    sim.init();
    simulationRef.current = sim;

    // Notify ready
    if (onReady) {
      setTimeout(onReady, 100);
    }

    // Auto-play
    sim.play();

    // Cleanup
    return () => {
      sim.destroy();
      simulationRef.current = null;
    };
  }, [onReady]);

  // Update parameters when they change
  useEffect(() => {
    if (simulationRef.current) {
      simulationRef.current.setParameters(parameters);
    }
  }, [parameters]);

  return (
    <div className="relative w-full h-full">
      <div
        ref={containerRef}
        className="w-full h-full min-h-[400px] bg-slate-900 rounded-lg"
      />
      {showLabels && (
        <div className="absolute bottom-4 left-4 bg-black/50 backdrop-blur-sm text-white p-3 rounded-lg text-sm">
          <div className="font-semibold mb-2">Pressure Field Visualization</div>
          <div className="text-xs space-y-1">
            <div>Spation Density: {parameters.density?.toExponential(1) || '5.2×10⁹⁶'} kg/m³</div>
            <div>Bulk Modulus: {parameters.bulkModulus?.toExponential(1) || '4.6×10¹¹³'} Pa</div>
            <div className="mt-2 text-slate-300">
              Blue = Low Pressure | Gold = High Pressure
            </div>
          </div>
        </div>
      )}
      {showFormulas && (
        <div className="absolute top-4 right-4 bg-black/50 backdrop-blur-sm text-white p-3 rounded-lg text-xs font-mono">
          <div>P(r) = P_∞ - κ·ρ_disp(r)</div>
        </div>
      )}
    </div>
  );
};

