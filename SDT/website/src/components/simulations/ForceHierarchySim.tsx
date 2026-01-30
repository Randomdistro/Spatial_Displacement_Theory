/**
 * Force Hierarchy Simulation
 * Agent 3: Physics/Simulation
 *
 * Visualizes how all forces emerge from the same pressure field
 * with different occlusion regimes (Coulomb: E→0, Gravity: E→1-η)
 * 
 * TEKNE Design: The unification of forces revealed through visualization
 */

import React, { useEffect, useRef, useState, useCallback } from 'react';
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

// Design System Colors (TEKNE)
const COLORS = {
  spaceDeep: 0x1a365d,
  spaceMedium: 0x2d5a87,
  spaceLight: 0x4299e1,
  goldPrimary: 0xd69e2e,
  goldBright: 0xf6ad55,
  goldLight: 0xfbbf24,
  bgDeep: 0x0a0e1a,
  silver: 0xcbd5e0,
  coulombBlue: 0x63b3ed,
  gravityGold: 0xecc94b,
};

class ForceHierarchySimulation extends SimulationBase {
  private object1: THREE.Mesh | null = null;
  private object2: THREE.Mesh | null = null;
  private object1Glow: THREE.Mesh | null = null;
  private object2Glow: THREE.Mesh | null = null;
  private pressureField: THREE.Points | null = null;
  private forceVector1: THREE.ArrowHelper | null = null;
  private forceVector2: THREE.ArrowHelper | null = null;
  private cmbBoundary: THREE.Mesh | null = null;
  private cmbGlow: THREE.Mesh | null = null;
  private pressureGradients: THREE.ArrowHelper[] = [];
  private connectionLine: THREE.Line | null = null;
  private ambientParticles: THREE.Points | null = null;

  // Force calculations
  private coulombForce: number = 0;
  private gravityForce: number = 0;
  private currentForce: number = 0;

  // Animation state
  private pulsePhase: number = 0;
  private forceFlowPhase: number = 0;

  init(): void {
    // Clear existing objects except lights
    const objectsToRemove = this.scene.children.filter(
      child => !(child instanceof THREE.Light)
    );
    objectsToRemove.forEach(child => {
      this.scene.remove(child);
      this.disposeObject(child);
    });

    // Get parameters
    const R1 = this.parameters.object1Radius ?? 5.29177e-11;
    const R2 = this.parameters.object2Radius ?? 5.29177e-11;
    const r = this.parameters.separation ?? 1e-10;
    const E = this.parameters.occlusionE ?? 0.5;
    const showCMB = this.parameters.showCMBSource ?? true;
    const showPressure = this.parameters.showPressureField ?? true;

    // Scale for visualization
    const scaleFactor = 1e10;
    const R1_scaled = R1 * scaleFactor;
    const R2_scaled = R2 * scaleFactor;
    const r_scaled = r * scaleFactor;

    // Scene setup
    this.scene.background = new THREE.Color(COLORS.bgDeep);
    this.scene.fog = new THREE.FogExp2(COLORS.bgDeep, 0.008);

    // Create ambient environment
    this.createAmbientEnvironment(r_scaled);

    // Interpolate color based on occlusion
    const forceColor = this.getForceColor(E);

    // Create object 1 (particle 1)
    this.createObject1(R1_scaled, r_scaled, forceColor);

    // Create object 2 (particle 2)
    this.createObject2(R2_scaled, r_scaled, forceColor);

    // Create connection line between objects
    this.createConnectionLine(r_scaled, forceColor);

    // Create CMB boundary
    if (showCMB) {
      this.createCMBBoundary(r_scaled);
    }

    // Create pressure field visualization
    if (showPressure) {
      this.createPressureField(R1_scaled, R2_scaled, r_scaled, E);
    }

    // Calculate forces
    this.calculateForces(R1, R2, r, E);

    // Create force vectors
    this.createForceVectors(R1_scaled, R2_scaled, r_scaled, forceColor);

    // Create pressure gradients
    if (showPressure) {
      this.createPressureGradients(R1_scaled, R2_scaled, r_scaled, E);
    }

    // Position camera
    this.camera.position.set(0, r_scaled * 1.2, r_scaled * 2.5);
    this.camera.lookAt(0, 0, 0);
  }

  private getForceColor(E: number): THREE.Color {
    const normalizedE = E / MAX_OCCLUSION;
    const color = new THREE.Color();
    color.lerpColors(
      new THREE.Color(COLORS.coulombBlue),
      new THREE.Color(COLORS.gravityGold),
      normalizedE
    );
    return color;
  }

  private createAmbientEnvironment(r_scaled: number): void {
    const particleCount = 300;
    const positions: number[] = [];
    const colors: number[] = [];

    for (let i = 0; i < particleCount; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const radius = r_scaled * (2 + Math.random() * 5);

      positions.push(
        radius * Math.sin(phi) * Math.cos(theta),
        radius * Math.sin(phi) * Math.sin(theta),
        radius * Math.cos(phi)
      );

      const color = new THREE.Color(COLORS.goldPrimary);
      color.multiplyScalar(0.2 + Math.random() * 0.15);
      colors.push(color.r, color.g, color.b);
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.03,
      vertexColors: true,
      transparent: true,
      opacity: 0.4,
      sizeAttenuation: true,
      blending: THREE.AdditiveBlending,
    });

    this.ambientParticles = new THREE.Points(geometry, material);
    this.scene.add(this.ambientParticles);
  }

  private createObject1(R1_scaled: number, r_scaled: number, forceColor: THREE.Color): void {
    // Core sphere
    const geometry = new THREE.SphereGeometry(R1_scaled, 32, 32);
    const material = new THREE.MeshStandardMaterial({
      color: COLORS.spaceMedium,
      metalness: 0.85,
      roughness: 0.15,
      emissive: forceColor,
      emissiveIntensity: 0.3
    });
    this.object1 = new THREE.Mesh(geometry, material);
    this.object1.position.set(-r_scaled / 2, 0, 0);
    this.scene.add(this.object1);

    // Glow sphere
    const glowGeometry = new THREE.SphereGeometry(R1_scaled * 1.8, 32, 32);
    const glowMaterial = new THREE.MeshBasicMaterial({
      color: forceColor,
      transparent: true,
      opacity: 0.15,
      side: THREE.BackSide,
    });
    this.object1Glow = new THREE.Mesh(glowGeometry, glowMaterial);
    this.object1Glow.position.copy(this.object1.position);
    this.scene.add(this.object1Glow);
  }

  private createObject2(R2_scaled: number, r_scaled: number, forceColor: THREE.Color): void {
    const geometry = new THREE.SphereGeometry(R2_scaled, 32, 32);
    const material = new THREE.MeshStandardMaterial({
      color: COLORS.spaceLight,
      metalness: 0.85,
      roughness: 0.15,
      emissive: forceColor,
      emissiveIntensity: 0.3
    });
    this.object2 = new THREE.Mesh(geometry, material);
    this.object2.position.set(r_scaled / 2, 0, 0);
    this.scene.add(this.object2);

    // Glow sphere
    const glowGeometry = new THREE.SphereGeometry(R2_scaled * 1.8, 32, 32);
    const glowMaterial = new THREE.MeshBasicMaterial({
      color: forceColor,
      transparent: true,
      opacity: 0.15,
      side: THREE.BackSide,
    });
    this.object2Glow = new THREE.Mesh(glowGeometry, glowMaterial);
    this.object2Glow.position.copy(this.object2.position);
    this.scene.add(this.object2Glow);
  }

  private createConnectionLine(r_scaled: number, forceColor: THREE.Color): void {
    const points = [
      new THREE.Vector3(-r_scaled / 2, 0, 0),
      new THREE.Vector3(r_scaled / 2, 0, 0),
    ];
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({
      color: forceColor,
      transparent: true,
      opacity: 0.4,
      linewidth: 2,
    });
    this.connectionLine = new THREE.Line(geometry, material);
    this.scene.add(this.connectionLine);
  }

  private createCMBBoundary(r_scaled: number): void {
    const cmbRadius = r_scaled * 8;
    
    // Main CMB sphere (wireframe)
    const geometry = new THREE.SphereGeometry(cmbRadius, 48, 24);
    const material = new THREE.MeshBasicMaterial({
      color: COLORS.goldPrimary,
      transparent: true,
      opacity: 0.08,
      wireframe: true,
    });
    this.cmbBoundary = new THREE.Mesh(geometry, material);
    this.scene.add(this.cmbBoundary);

    // Subtle inner glow
    const glowGeometry = new THREE.SphereGeometry(cmbRadius * 0.98, 32, 32);
    const glowMaterial = new THREE.MeshBasicMaterial({
      color: COLORS.goldLight,
      transparent: true,
      opacity: 0.03,
      side: THREE.BackSide,
    });
    this.cmbGlow = new THREE.Mesh(glowGeometry, glowMaterial);
    this.scene.add(this.cmbGlow);
  }

  private createPressureField(R1_scaled: number, R2_scaled: number, r_scaled: number, E: number): void {
    const positions: number[] = [];
    const colors: number[] = [];
    const resolution = 25;
    const fieldSize = r_scaled * 2.5;

    for (let x = -fieldSize; x < fieldSize; x += fieldSize / resolution) {
      for (let y = -fieldSize / 2; y < fieldSize / 2; y += fieldSize / resolution) {
        for (let z = -fieldSize / 2; z < fieldSize / 2; z += fieldSize / resolution) {
          const pos = new THREE.Vector3(x, y, z);
          
          const dist1 = pos.distanceTo(this.object1!.position);
          const dist2 = pos.distanceTo(this.object2!.position);
          
          if (dist1 < R1_scaled * 1.2 || dist2 < R2_scaled * 1.2) continue;
          if (dist1 > fieldSize * 1.5 && dist2 > fieldSize * 1.5) continue;

          // Random sampling for performance
          if (Math.random() > 0.3) continue;

          positions.push(x, y, z);

          const pressure = this.calculatePressureAtPoint(pos, R1_scaled, R2_scaled, r_scaled, E);
          const normalizedPressure = Math.max(0, Math.min(1, pressure));

          const color = new THREE.Color();
          color.lerpColors(
            new THREE.Color(COLORS.spaceDeep),
            new THREE.Color(COLORS.goldPrimary),
            normalizedPressure
          );
          colors.push(color.r, color.g, color.b);
        }
      }
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: fieldSize / resolution * 0.4,
      vertexColors: true,
      transparent: true,
      opacity: 0.35,
      sizeAttenuation: true,
      blending: THREE.AdditiveBlending,
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
    const dist1 = pos.distanceTo(this.object1!.position);
    const dist2 = pos.distanceTo(this.object2!.position);
    
    const pressure1 = (1 - E * 0.5) / (dist1 / R1_scaled + 0.5);
    const pressure2 = (1 - E * 0.5) / (dist2 / R2_scaled + 0.5);
    
    return Math.min(1, (pressure1 + pressure2) * 0.4);
  }

  private calculateForces(R1: number, R2: number, r: number, E: number): void {
    // Coulomb force: F_C = (π/4)P_CMB (R_N²R_e²/r²) when E→0
    this.coulombForce = (Math.PI / 4) * CMB_PRESSURE * (R1 * R1) * (R2 * R2) / (r * r);
    
    // Gravity: F_G = (π/4)P_CMB (R₁²R₂²/r²)(1-η) when E→1-η
    this.gravityForce = (Math.PI / 4) * CMB_PRESSURE * (R1 * R1) * (R2 * R2) / (r * r) * (1 - ETA);
    
    // Current force based on occlusion
    const normalizedE = E / MAX_OCCLUSION;
    this.currentForce = this.coulombForce * (1 - normalizedE) + this.gravityForce * normalizedE;
  }

  private createForceVectors(R1_scaled: number, R2_scaled: number, r_scaled: number, forceColor: THREE.Color): void {
    const direction1 = new THREE.Vector3(1, 0, 0);
    const forceLength = r_scaled * 0.25;

    this.forceVector1 = new THREE.ArrowHelper(
      direction1,
      new THREE.Vector3(-r_scaled / 2 + R1_scaled * 1.2, 0, 0),
      forceLength,
      forceColor.getHex(),
      forceLength * 0.25,
      forceLength * 0.12
    );
    this.scene.add(this.forceVector1);

    const direction2 = new THREE.Vector3(-1, 0, 0);
    this.forceVector2 = new THREE.ArrowHelper(
      direction2,
      new THREE.Vector3(r_scaled / 2 - R2_scaled * 1.2, 0, 0),
      forceLength,
      forceColor.getHex(),
      forceLength * 0.25,
      forceLength * 0.12
    );
    this.scene.add(this.forceVector2);
  }

  private createPressureGradients(
    R1_scaled: number,
    R2_scaled: number,
    r_scaled: number,
    E: number
  ): void {
    // Radial arrows showing pressure direction from CMB
    const arrowCount = 12;
    const arrowRadius = r_scaled * 1.5;
    const forceColor = this.getForceColor(E);

    for (let i = 0; i < arrowCount; i++) {
      const angle = (i / arrowCount) * Math.PI * 2;
      const x = Math.cos(angle) * arrowRadius;
      const z = Math.sin(angle) * arrowRadius;
      
      const origin = new THREE.Vector3(x, 0, z);
      const direction = origin.clone().negate().normalize();
      
      const arrow = new THREE.ArrowHelper(
        direction,
        origin,
        r_scaled * 0.3,
        forceColor.getHex(),
        r_scaled * 0.08,
        r_scaled * 0.04
      );
      arrow.cone.material = new THREE.MeshBasicMaterial({
        color: forceColor,
        transparent: true,
        opacity: 0.4,
      });
      arrow.line.material = new THREE.LineBasicMaterial({
        color: forceColor,
        transparent: true,
        opacity: 0.3,
      });
      
      this.scene.add(arrow);
      this.pressureGradients.push(arrow);
    }
  }

  update(deltaTime: number): void {
    this.time += deltaTime;
    this.pulsePhase += deltaTime * 1.5;
    this.forceFlowPhase += deltaTime * 2;

    const E = this.parameters.occlusionE ?? 0.5;
    const forceColor = this.getForceColor(E);

    // Pulsing glow on objects
    const pulseIntensity = 0.15 + Math.sin(this.pulsePhase) * 0.05;
    
    if (this.object1Glow) {
      (this.object1Glow.material as THREE.MeshBasicMaterial).opacity = pulseIntensity;
      const scale = 1.8 + Math.sin(this.pulsePhase) * 0.1;
      this.object1Glow.scale.setScalar(scale / 1.8);
    }
    
    if (this.object2Glow) {
      (this.object2Glow.material as THREE.MeshBasicMaterial).opacity = pulseIntensity;
      const scale = 1.8 + Math.sin(this.pulsePhase + 0.5) * 0.1;
      this.object2Glow.scale.setScalar(scale / 1.8);
    }

    // Update emissive colors based on occlusion
    if (this.object1) {
      (this.object1.material as THREE.MeshStandardMaterial).emissive = forceColor;
    }
    if (this.object2) {
      (this.object2.material as THREE.MeshStandardMaterial).emissive = forceColor;
    }

    // Connection line pulse
    if (this.connectionLine) {
      const lineMaterial = this.connectionLine.material as THREE.LineBasicMaterial;
      lineMaterial.opacity = 0.3 + Math.sin(this.forceFlowPhase) * 0.15;
      lineMaterial.color = forceColor;
    }

    // CMB boundary slow rotation
    if (this.cmbBoundary) {
      this.cmbBoundary.rotation.y += deltaTime * 0.02;
      this.cmbBoundary.rotation.x += deltaTime * 0.01;
    }

    // Pressure field gentle rotation
    if (this.pressureField) {
      this.pressureField.rotation.y += deltaTime * 0.015;
    }

    // Ambient particles slow drift
    if (this.ambientParticles) {
      this.ambientParticles.rotation.y += deltaTime * 0.01;
    }
  }

  protected onParametersChanged(): void {
    this.init();
  }

  dispose(): void {
    this.disposeObject(this.object1);
    this.disposeObject(this.object2);
    this.disposeObject(this.object1Glow);
    this.disposeObject(this.object2Glow);
    this.disposeObject(this.pressureField);
    this.disposeObject(this.cmbBoundary);
    this.disposeObject(this.cmbGlow);
    this.disposeObject(this.connectionLine);
    this.disposeObject(this.ambientParticles);
    if (this.forceVector1) this.forceVector1.dispose();
    if (this.forceVector2) this.forceVector2.dispose();
    this.pressureGradients.forEach(arrow => {
      if (arrow) arrow.dispose();
    });

    this.object1 = null;
    this.object2 = null;
    this.object1Glow = null;
    this.object2Glow = null;
    this.pressureField = null;
    this.cmbBoundary = null;
    this.cmbGlow = null;
    this.connectionLine = null;
    this.ambientParticles = null;
    this.forceVector1 = null;
    this.forceVector2 = null;
    this.pressureGradients = [];
  }

  private disposeObject(object: THREE.Object3D | null): void {
    if (!object) return;

    object.traverse((child) => {
      if (child instanceof THREE.Mesh || child instanceof THREE.Points || child instanceof THREE.Line) {
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

  const updateForceData = useCallback((params: typeof parameters) => {
    const R1 = params.object1Radius ?? 5.29177e-11;
    const R2 = params.object2Radius ?? 5.29177e-11;
    const r = params.separation ?? 1e-10;
    const E = params.occlusionE ?? 0.5;

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
  }, []);

  useEffect(() => {
    if (!containerRef.current) return;

    const sim = new ForceHierarchySimulation(containerRef.current);
    const defaultParams = {
      object1Radius: 5.29177e-11,
      object2Radius: 5.29177e-11,
      separation: 1e-10,
      occlusionE: 0.5,
      showCMBSource: true,
      compareForces: true,
      showPressureField: true,
      ...parameters,
    };
    sim.setParameters(defaultParams);
    sim.init();
    simulationRef.current = sim;

    updateForceData(defaultParams);

    if (onReady) {
      setTimeout(onReady, 100);
    }

    sim.play();

    return () => {
      sim.destroy();
      simulationRef.current = null;
    };
  }, [onReady, updateForceData]);

  useEffect(() => {
    if (simulationRef.current) {
      simulationRef.current.setParameters(parameters);
      updateForceData(parameters);
    }
  }, [parameters, updateForceData]);

  const handleOcclusionChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newE = parseFloat(e.target.value);
    if (onParameterChange) {
      onParameterChange({ ...parameters, occlusionE: newE });
    }
  }, [onParameterChange, parameters]);

  const formatForce = (force: number): string => {
    if (force >= 1e-6) return `${(force * 1e6).toFixed(2)} μN`;
    if (force >= 1e-9) return `${(force * 1e9).toFixed(2)} nN`;
    if (force >= 1e-12) return `${(force * 1e12).toFixed(2)} pN`;
    return `${force.toExponential(2)} N`;
  };

  // Calculate regime indicator
  const regime = forceData.occlusion < 0.3 ? 'Coulomb' : forceData.occlusion > 0.7 ? 'Gravity' : 'Transition';
  const regimeColor = forceData.occlusion < 0.3 ? '#63b3ed' : forceData.occlusion > 0.7 ? '#ecc94b' : '#a0aec0';

  return (
    <div className="relative w-full h-full">
      {/* Simulation container */}
      <div
        ref={containerRef}
        className="w-full h-full min-h-[500px] rounded-xl overflow-hidden"
        style={{ 
          touchAction: 'none',
          background: 'linear-gradient(135deg, #0a0e1a 0%, #1a202c 50%, #0a0e1a 100%)',
        }}
      />

      {/* Occlusion slider - top left */}
      <div 
        className="absolute top-4 left-4 p-4 rounded-xl"
        style={{
          background: 'rgba(10, 14, 26, 0.9)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(214, 158, 46, 0.2)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
          minWidth: '200px',
        }}
      >
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-medium" style={{ color: '#94a3b8' }}>
            Occlusion (E)
          </span>
          <span 
            className="text-xs font-mono px-2 py-0.5 rounded"
            style={{ 
              background: `${regimeColor}20`,
              color: regimeColor,
            }}
          >
            {regime}
          </span>
        </div>
        
        <div className="relative mb-2">
          <input
            type="range"
            min="0"
            max={MAX_OCCLUSION}
            step="0.01"
            value={forceData.occlusion}
            onChange={handleOcclusionChange}
            className="w-full h-2 rounded-full appearance-none cursor-pointer"
            style={{
              background: `linear-gradient(to right, #63b3ed, #a0aec0, #ecc94b)`,
            }}
          />
        </div>
        
        <div className="flex justify-between text-[10px]" style={{ color: '#64748b' }}>
          <span>E → 0</span>
          <span className="font-mono" style={{ color: '#e2e8f0' }}>
            {(forceData.occlusion * 100).toFixed(1)}%
          </span>
          <span>E → 1-η</span>
        </div>
        
        <div className="flex justify-between mt-1 text-[10px]" style={{ color: '#475569' }}>
          <span>Coulomb</span>
          <span>Gravity</span>
        </div>
      </div>

      {/* Labels panel - bottom left */}
      {showLabels && (
        <div 
          className="absolute bottom-4 left-4 p-4 rounded-xl text-sm max-w-xs"
          style={{
            background: 'rgba(10, 14, 26, 0.9)',
            backdropFilter: 'blur(12px)',
            border: '1px solid rgba(214, 158, 46, 0.15)',
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
          }}
        >
          <div 
            className="font-semibold mb-3 text-sm tracking-wide"
            style={{ color: '#d69e2e' }}
          >
            FORCE UNIFICATION
          </div>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between items-center">
              <span style={{ color: '#94a3b8' }}>Coulomb (E→0):</span>
              <span className="font-mono" style={{ color: '#63b3ed' }}>
                {formatForce(forceData.coulomb)}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span style={{ color: '#94a3b8' }}>Gravity (E→1-η):</span>
              <span className="font-mono" style={{ color: '#ecc94b' }}>
                {formatForce(forceData.gravity)}
              </span>
            </div>
            <div 
              className="flex justify-between items-center pt-2 mt-2"
              style={{ borderTop: '1px solid rgba(148, 163, 184, 0.2)' }}
            >
              <span style={{ color: '#cbd5e0' }}>Current Force:</span>
              <span className="font-mono font-medium" style={{ color: regimeColor }}>
                {formatForce(forceData.current)}
              </span>
            </div>
            <div className="mt-3 pt-3 text-xs" style={{ borderTop: '1px solid rgba(148, 163, 184, 0.1)' }}>
              <div style={{ color: '#cbd5e0' }}>Same Pressure Source</div>
              <div style={{ color: '#94a3b8' }}>Different Occlusion Regime</div>
            </div>
          </div>
        </div>
      )}

      {/* Formula overlay - top right */}
      {showFormulas && (
        <div 
          className="absolute top-4 right-4 p-4 rounded-xl text-xs font-mono"
          style={{
            background: 'rgba(10, 14, 26, 0.9)',
            backdropFilter: 'blur(12px)',
            border: '1px solid rgba(214, 158, 46, 0.15)',
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
          }}
        >
          <div className="mb-2" style={{ color: '#63b3ed' }}>
            F<sub>C</sub> = (π/4)P<sub>CMB</sub>(R₁²R₂²/r²)
          </div>
          <div className="mb-3" style={{ color: '#ecc94b' }}>
            F<sub>G</sub> = (π/4)P<sub>CMB</sub>(R₁²R₂²/r²)(1-η)
          </div>
          <div 
            className="pt-2 text-[10px]"
            style={{ 
              borderTop: '1px solid rgba(148, 163, 184, 0.2)',
              color: '#94a3b8' 
            }}
          >
            Unified via Occlusion Parameter
          </div>
        </div>
      )}
    </div>
  );
};
