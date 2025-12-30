/**
 * Force Hierarchy Simulation
 * Agent 3: Physics/Simulation
 *
 * Visualizes how all forces emerge from the same pressure field
 * with different occlusion regimes (Coulomb: E→0, Gravity: E→1-η)
 */

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { SimulationBase, SimulationProps } from './SimulationBase';

interface ForceHierarchySimProps extends SimulationProps {
  parameters: {
    object1Radius?: number;      // R₁ in meters (default: 5.29e-11, Bohr radius)
    object2Radius?: number;      // R₂ in meters (default: 5.29e-11)
    separation?: number;         // r in meters (default: 1e-10)
    occlusionE?: number;         // E (0 to 1-η), default: 0.5
    showCMBSource?: boolean;     // Show CMB boundary (default: true)
    compareForces?: boolean;      // Show both forces side-by-side (default: true)
    showPressureField?: boolean; // Show pressure field visualization (default: true)
  };
}

// SDT Physical Constants
const CMB_PRESSURE = 2.036e-2;   // Pa
const ETA = 0.01;                // Small parameter for gravity regime
const MAX_OCCLUSION = 1 - ETA;   // Maximum occlusion (gravity regime)

class ForceHierarchySimulation extends SimulationBase {
  private object1: THREE.Mesh | null = null;
  private object2: THREE.Mesh | null = null;
  private pressureField: THREE.Points | null = null;
  private forceVector1: THREE.ArrowHelper | null = null;
  private forceVector2: THREE.ArrowHelper | null = null;
  private cmbBoundary: THREE.Mesh | null = null;
  private pressureGradients: THREE.ArrowHelper[] = [];

  // Force calculations
  private coulombForce: number = 0;
  private gravityForce: number = 0;
  private currentForce: number = 0;

  init(): void {
    // Clear existing objects
    while (this.scene.children.length > 0) {
      const child = this.scene.children[0];
      if (child instanceof THREE.Light) {
        continue;
      }
      this.scene.remove(child);
      this.disposeObject(child);
    }

    // Get parameters
    const R1 = this.parameters.object1Radius ?? 5.29177e-11; // Bohr radius
    const R2 = this.parameters.object2Radius ?? 5.29177e-11;
    const r = this.parameters.separation ?? 1e-10;
    const E = this.parameters.occlusionE ?? 0.5;
    const showCMB = this.parameters.showCMBSource ?? true;
    const showPressure = this.parameters.showPressureField ?? true;

    // Scale for visualization (atomic scale → visible)
    const scaleFactor = 1e10; // Scale up atomic sizes
    const R1_scaled = R1 * scaleFactor;
    const R2_scaled = R2 * scaleFactor;
    const r_scaled = r * scaleFactor;

    // Create object 1 (nucleus/particle)
    const obj1Geometry = new THREE.SphereGeometry(R1_scaled, 32, 32);
    // STYLING PLACEHOLDER: Object 1 material
    // Creative Agent: Use --color-space-medium for object 1
    // Subtle emissive glow, metallic sheen
    const obj1Material = new THREE.MeshStandardMaterial({
      color: 0x2d5a87, // PLACEHOLDER: Use --color-space-medium
      metalness: 0.8,
      roughness: 0.2,
      emissive: 0x1a365d,
      emissiveIntensity: 0.2
    });
    this.object1 = new THREE.Mesh(obj1Geometry, obj1Material);
    this.object1.position.set(-r_scaled / 2, 0, 0);
    this.scene.add(this.object1);

    // Create object 2
    const obj2Geometry = new THREE.SphereGeometry(R2_scaled, 32, 32);
    // STYLING PLACEHOLDER: Object 2 material
    // Creative Agent: Use --color-space-light for object 2
    // Slightly different shade to distinguish
    const obj2Material = new THREE.MeshStandardMaterial({
      color: 0x4299e1, // PLACEHOLDER: Use --color-space-light
      metalness: 0.8,
      roughness: 0.2,
      emissive: 0x2d5a87,
      emissiveIntensity: 0.2
    });
    this.object2 = new THREE.Mesh(obj2Geometry, obj2Material);
    this.object2.position.set(r_scaled / 2, 0, 0);
    this.scene.add(this.object2);

    // Create CMB boundary (distant sphere)
    if (showCMB) {
      // STYLING PLACEHOLDER: CMB boundary visualization
      // Creative Agent: Large translucent sphere, gold tint
      // Represents the source of all pressure
      // Position: Far away, visible but not intrusive
      const cmbRadius = r_scaled * 10; // Much larger than objects
      const cmbGeometry = new THREE.SphereGeometry(cmbRadius, 32, 32);
      const cmbMaterial = new THREE.MeshStandardMaterial({
        color: 0xd69e2e, // PLACEHOLDER: Use --color-gold-primary
        transparent: true,
        opacity: 0.1, // PLACEHOLDER: Very subtle
        side: THREE.DoubleSide,
        wireframe: true // PLACEHOLDER: Wireframe or solid?
      });
      this.cmbBoundary = new THREE.Mesh(cmbGeometry, cmbMaterial);
      this.cmbBoundary.position.set(0, 0, -r_scaled * 5); // Behind objects
      this.scene.add(this.cmbBoundary);
    }

    // Create pressure field visualization
    if (showPressure) {
      this.createPressureField(R1_scaled, R2_scaled, r_scaled, E);
    }

    // Calculate forces
    this.calculateForces(R1, R2, r, E);

    // Create force vectors
    this.createForceVectors(R1_scaled, R2_scaled, r_scaled);

    // Create pressure gradient visualization
    if (showPressure) {
      this.createPressureGradients(R1_scaled, R2_scaled, r_scaled, E);
    }

    // Position camera
    this.camera.position.set(0, r_scaled * 1.5, r_scaled * 2);
    this.camera.lookAt(0, 0, 0);
  }

  private createPressureField(R1_scaled: number, R2_scaled: number, r_scaled: number, E: number): void {
    const positions: number[] = [];
    const colors: number[] = [];
    const resolution = 20;
    const fieldSize = r_scaled * 3;

    for (let x = -fieldSize; x < fieldSize; x += fieldSize / resolution) {
      for (let y = -fieldSize / 2; y < fieldSize / 2; y += fieldSize / resolution) {
        for (let z = -fieldSize / 2; z < fieldSize / 2; z += fieldSize / resolution) {
          const pos = new THREE.Vector3(x, y, z);
          
          // Skip points inside objects
          const dist1 = pos.distanceTo(this.object1!.position);
          const dist2 = pos.distanceTo(this.object2!.position);
          if (dist1 < R1_scaled * 1.1 || dist2 < R2_scaled * 1.1) continue;
          if (dist1 > fieldSize || dist2 > fieldSize) continue;

          positions.push(x, y, z);

          // Calculate pressure at this point
          const pressure = this.calculatePressureAtPoint(pos, R1_scaled, R2_scaled, r_scaled, E);
          const normalizedPressure = Math.max(0, Math.min(1, pressure));

          // STYLING PLACEHOLDER: Pressure color gradient
          // Creative Agent: Blue (low) → Gold (high) gradient
          // Use --color-space-deep → --color-gold-primary
          const color = new THREE.Color();
          color.lerpColors(
            new THREE.Color(0x1a365d), // PLACEHOLDER: --color-space-deep
            new THREE.Color(0xd69e2e), // PLACEHOLDER: --color-gold-primary
            normalizedPressure
          );
          colors.push(color.r, color.g, color.b);
        }
      }
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    // STYLING PLACEHOLDER: Pressure field material
    const material = new THREE.PointsMaterial({
      size: fieldSize / resolution * 0.5,
      vertexColors: true,
      transparent: true,
      opacity: 0.4, // PLACEHOLDER: Adjust visibility
      sizeAttenuation: true
    });

    this.pressureField = new THREE.Points(geometry, material);
    this.scene.add(this.pressureField);
  }

  private calculatePressureAtPoint(
    pos: THREE.Vector3,
    R1_scaled: number,
    R2_scaled: number,
    r_scaled: number,
    E: number
  ): number {
    // Simplified pressure calculation
    // Full implementation would solve Master Equation with occlusion
    const dist1 = pos.distanceTo(this.object1!.position);
    const dist2 = pos.distanceTo(this.object2!.position);
    
    // Pressure decreases with distance from objects
    // Occlusion affects pressure field
    const pressure1 = (1 - E) / (dist1 + R1_scaled);
    const pressure2 = (1 - E) / (dist2 + R2_scaled);
    
    return Math.min(1, (pressure1 + pressure2) * 0.5);
  }

  private calculateForces(R1: number, R2: number, r: number, E: number): void {
    // SDT Force Equations
    
    // Coulomb force: F_C = (π/4)P_CMB (R_N²R_e²/r²) when E→0
    this.coulombForce = (Math.PI / 4) * CMB_PRESSURE * (R1 * R1) * (R2 * R2) / (r * r);
    
    // Gravity: F_G = (π/4)P_CMB (R₁²R₂²/r²)(1-η) when E→1-η
    this.gravityForce = (Math.PI / 4) * CMB_PRESSURE * (R1 * R1) * (R2 * R2) / (r * r) * (1 - ETA);
    
    // Current force based on occlusion
    // Interpolate between Coulomb (E=0) and Gravity (E=1-η)
    const normalizedE = E / MAX_OCCLUSION;
    this.currentForce = this.coulombForce * (1 - normalizedE) + this.gravityForce * normalizedE;
  }

  private createForceVectors(R1_scaled: number, R2_scaled: number, r_scaled: number): void {
    // Force vector on object 1 (points toward object 2)
    const direction1 = new THREE.Vector3(1, 0, 0); // Toward object 2
    const forceLength1 = Math.min(this.currentForce * 1e20, r_scaled * 0.3); // Scaled for visualization
    
    // STYLING PLACEHOLDER: Force vector arrows
    // Creative Agent: Color based on force type
    // Coulomb (E→0): Blue tint
    // Gravity (E→1-η): Gold tint
    // Use --color-space-light for Coulomb, --color-gold-primary for Gravity
    const forceColor = this.parameters.occlusionE! < 0.3 
      ? 0x4299e1 // PLACEHOLDER: --color-space-light (Coulomb)
      : 0xd69e2e; // PLACEHOLDER: --color-gold-primary (Gravity)

    this.forceVector1 = new THREE.ArrowHelper(
      direction1,
      this.object1!.position,
      forceLength1,
      forceColor,
      forceLength1 * 0.1,
      forceLength1 * 0.05
    );
    this.scene.add(this.forceVector1);

    // Force vector on object 2 (points toward object 1)
    const direction2 = new THREE.Vector3(-1, 0, 0); // Toward object 1
    this.forceVector2 = new THREE.ArrowHelper(
      direction2,
      this.object2!.position,
      forceLength1,
      forceColor,
      forceLength1 * 0.1,
      forceLength1 * 0.05
    );
    this.scene.add(this.forceVector2);
  }

  private createPressureGradients(
    R1_scaled: number,
    R2_scaled: number,
    r_scaled: number,
    E: number
  ): void {
    // STYLING PLACEHOLDER: Pressure gradient arrows
    // Creative Agent: Show pressure gradient direction
    // Arrows point from high to low pressure
    // Color: Match pressure field colors
    // This is a placeholder - full implementation would calculate ∇P
  }

  update(deltaTime: number): void {
    this.time += deltaTime;

    // Update forces if occlusion changed
    const R1 = this.parameters.object1Radius ?? 5.29177e-11;
    const R2 = this.parameters.object2Radius ?? 5.29177e-11;
    const r = this.parameters.separation ?? 1e-10;
    const E = this.parameters.occlusionE ?? 0.5;

    this.calculateForces(R1, R2, r, E);

    // Update force vectors
    if (this.forceVector1 && this.forceVector2) {
      const r_scaled = r * 1e10;
      const forceLength = Math.min(this.currentForce * 1e20, r_scaled * 0.3);
      
      this.forceVector1.setLength(forceLength);
      this.forceVector2.setLength(forceLength);

      // Update color based on occlusion
      const forceColor = E < 0.3 ? 0x4299e1 : 0xd69e2e;
      // STYLING PLACEHOLDER: Update arrow colors
      // Creative Agent: Smooth color transition as occlusion changes
    }

    // STYLING PLACEHOLDER: Idle animations
    // Creative Agent: Subtle pulsing of objects, pressure field animation
    // Organic motion, breathing effect
  }

  protected onParametersChanged(): void {
    this.init();
  }

  dispose(): void {
    this.disposeObject(this.object1);
    this.disposeObject(this.object2);
    this.disposeObject(this.pressureField);
    this.disposeObject(this.cmbBoundary);
    if (this.forceVector1) this.forceVector1.dispose();
    if (this.forceVector2) this.forceVector2.dispose();
    this.pressureGradients.forEach(arrow => {
      if (arrow) arrow.dispose();
    });

    this.object1 = null;
    this.object2 = null;
    this.pressureField = null;
    this.cmbBoundary = null;
    this.forceVector1 = null;
    this.forceVector2 = null;
    this.pressureGradients = [];
  }

  private disposeObject(object: THREE.Object3D | null): void {
    if (!object) return;

    object.traverse((child) => {
      if (child instanceof THREE.Mesh || child instanceof THREE.Points) {
        child.geometry.dispose();
        if (Array.isArray(child.material)) {
          child.material.forEach(m => m.dispose());
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
export const ForceHierarchySim: React.FC<ForceHierarchySimProps> = ({
  id,
  parameters,
  onParameterChange,
  showFormulas = true,
  showLabels = true,
  narrationEnabled = false,
  onReady,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const simulationRef = useRef<ForceHierarchySimulation | null>(null);
  const [forceData, setForceData] = useState({
    coulomb: 0,
    gravity: 0,
    current: 0,
    occlusion: 0.5,
  });

  useEffect(() => {
    if (!containerRef.current) return;

    const sim = new ForceHierarchySimulation(containerRef.current);
    sim.setParameters({
      object1Radius: 5.29177e-11,
      object2Radius: 5.29177e-11,
      separation: 1e-10,
      occlusionE: 0.5,
      showCMBSource: true,
      compareForces: true,
      showPressureField: true,
      ...parameters,
    });
    sim.init();
    simulationRef.current = sim;

    // Calculate force data
    const R1 = parameters.object1Radius ?? 5.29177e-11;
    const R2 = parameters.object2Radius ?? 5.29177e-11;
    const r = parameters.separation ?? 1e-10;
    const E = parameters.occlusionE ?? 0.5;

    const coulomb = (Math.PI / 4) * CMB_PRESSURE * (R1 * R1) * (R2 * R2) / (r * r);
    const gravity = (Math.PI / 4) * CMB_PRESSURE * (R1 * R1) * (R2 * R2) / (r * r) * (1 - ETA);
    const normalizedE = E / MAX_OCCLUSION;
    const current = coulomb * (1 - normalizedE) + gravity * normalizedE;

    setForceData({
      coulomb,
      gravity,
      current,
      occlusion: E,
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
      
      // Recalculate forces
      const R1 = parameters.object1Radius ?? 5.29177e-11;
      const R2 = parameters.object2Radius ?? 5.29177e-11;
      const r = parameters.separation ?? 1e-10;
      const E = parameters.occlusionE ?? 0.5;

      const coulomb = (Math.PI / 4) * CMB_PRESSURE * (R1 * R1) * (R2 * R2) / (r * r);
      const gravity = (Math.PI / 4) * CMB_PRESSURE * (R1 * R1) * (R2 * R2) / (r * r) * (1 - ETA);
      const normalizedE = E / MAX_OCCLUSION;
      const current = coulomb * (1 - normalizedE) + gravity * normalizedE;

      setForceData({
        coulomb,
        gravity,
        current,
        occlusion: E,
      });
    }
  }, [parameters]);

  const formatForce = (force: number): string => {
    if (force >= 1e-6) return `${(force * 1e6).toFixed(2)} μN`;
    if (force >= 1e-9) return `${(force * 1e9).toFixed(2)} nN`;
    return `${force.toExponential(2)} N`;
  };

  return (
    <div className="relative w-full h-full">
      {/* STYLING PLACEHOLDER: Simulation container */}
      <div
        ref={containerRef}
        className="w-full h-full min-h-[500px] bg-slate-900 rounded-lg"
        style={{ touchAction: 'none' }}
      />

      {/* STYLING PLACEHOLDER: Labels panel */}
      {showLabels && (
        <div className="absolute bottom-4 left-4 bg-black/70 backdrop-blur-sm text-white p-4 rounded-lg text-sm max-w-xs">
          <div className="font-semibold mb-3 text-amber-400">Force Hierarchy</div>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Occlusion E:</span>
              <span className="font-mono">{(forceData.occlusion * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Coulomb (E→0):</span>
              <span className="font-mono text-blue-400">{formatForce(forceData.coulomb)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Gravity (E→1-η):</span>
              <span className="font-mono text-amber-400">{formatForce(forceData.gravity)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Current Force:</span>
              <span className="font-mono">{formatForce(forceData.current)}</span>
            </div>
            <div className="mt-3 pt-3 border-t border-slate-600 text-slate-300">
              <div className="text-xs">Same Pressure Source</div>
              <div className="text-xs text-slate-400">Different Occlusion</div>
            </div>
          </div>
        </div>
      )}

      {/* STYLING PLACEHOLDER: Formula overlay */}
      {showFormulas && (
        <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm text-white p-3 rounded-lg text-xs font-mono">
          <div>F_C = (π/4)P_CMB (R₁²R₂²/r²)</div>
          <div className="mt-1">F_G = (π/4)P_CMB (R₁²R₂²/r²)(1-η)</div>
          <div className="mt-2 text-slate-400 text-[10px]">
            Force Unification via Occlusion
          </div>
        </div>
      )}

      {/* STYLING PLACEHOLDER: Occlusion control slider */}
      {/* Creative Agent: Add interactive slider for occlusion parameter */}
      {/* Position: Top-left or bottom-right */}
      {/* Style: Match existing control sliders */}
    </div>
  );
};

