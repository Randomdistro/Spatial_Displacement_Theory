/**
 * Spation Lattice Simulation
 * Agent 3: Physics/Simulation
 *
 * Visualizes the fundamental spation lattice structure at Planck scale
 * Shows dodecahedral packing, K_bulk emergence, and pressure visualization
 * 
 * TEKNE Design: Form IS function - the lattice structure reveals the theory
 */

import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as THREE from 'three';
import { SimulationBase, SimulationProps } from './SimulationBase';
import { geometryRegistry, geometryToThreeJS } from '../../framework/geometry/GeometryGenerator';
import { DodecahedronGenerator } from '../../framework/geometry/DodecahedronGenerator';

interface SpationLatticeSimProps extends SimulationProps {
  parameters: {
    scale?: number;              // Current scale (log10 meters), default: -35
    showPressure?: boolean;      // Show pressure color coding
    showDeformation?: boolean;   // Show deformation vectors
    latticeResolution?: number;  // Unit cells per dimension, default: 5
    zoomLevel?: number;          // 0-35 (orders of magnitude), default: 0
    showUnitCells?: boolean;     // Show cell boundaries
  };
}

// SDT Physical Constants
const SPATION_DENSITY = 5.2e96;      // kg/m³
const BULK_MODULUS = 4.6e113;        // Pa
const PLANCK_LENGTH = 1.616e-35;     // m
const LATTICE_SPACING = PLANCK_LENGTH; // ~10⁻³⁵ m

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
};

class SpationLatticeSimulation extends SimulationBase {
  private latticeCells: THREE.Group[] = [];
  private cellMeshes: THREE.Mesh[] = [];
  private latticePoints: THREE.Points | null = null;
  private pressureField: THREE.Points | null = null;
  private deformationVectors: THREE.ArrowHelper[] = [];
  private unitCellWireframes: THREE.LineSegments[] = [];
  private ambientParticles: THREE.Points | null = null;

  // Scale tracking
  private currentScale: number = -35;
  private currentZoomLevel: number = 0;

  // Animation state
  private breathPhase: number = 0;
  private rotationPhase: number = 0;

  init(): void {
    // Clear existing objects except lights
    const objectsToRemove = this.scene.children.filter(
      child => !(child instanceof THREE.Light)
    );
    objectsToRemove.forEach(child => {
      this.scene.remove(child);
      this.disposeObject(child);
    });

    // Register dodecahedron generator if needed
    try {
      geometryRegistry.generate('dodecahedron', { radius: 1.0 });
    } catch (e) {
      geometryRegistry.register('dodecahedron', new DodecahedronGenerator());
    }

    // Get parameters
    this.currentScale = this.parameters.scale ?? -35;
    this.currentZoomLevel = this.parameters.zoomLevel ?? 0;
    const resolution = this.parameters.latticeResolution ?? 5;
    const showPressure = this.parameters.showPressure ?? true;
    const showDeformation = this.parameters.showDeformation ?? false;
    const showUnitCells = this.parameters.showUnitCells ?? true;

    // Calculate LOD based on zoom level
    const lodResolution = this.calculateLODResolution(resolution, this.currentZoomLevel);

    // Create ambient environment
    this.createAmbientEnvironment();

    // Create dodecahedral lattice
    this.createLatticeStructure(lodResolution, showUnitCells);

    // Create pressure visualization
    if (showPressure) {
      this.createPressureVisualization(lodResolution);
    }

    // Create deformation vectors
    if (showDeformation) {
      this.createDeformationVectors(lodResolution);
    }

    // Position camera based on scale
    this.updateCameraForScale();

    // Scene background - deep space
    this.scene.background = new THREE.Color(COLORS.bgDeep);

    // Add fog for depth
    this.scene.fog = new THREE.FogExp2(COLORS.bgDeep, 0.015);
  }

  private createAmbientEnvironment(): void {
    // Floating ambient particles for depth
    const particleCount = 500;
    const positions: number[] = [];
    const colors: number[] = [];
    const sizes: number[] = [];

    for (let i = 0; i < particleCount; i++) {
      positions.push(
        (Math.random() - 0.5) * 50,
        (Math.random() - 0.5) * 50,
        (Math.random() - 0.5) * 50
      );

      // Subtle gold-tinted particles
      const color = new THREE.Color(COLORS.goldPrimary);
      color.multiplyScalar(0.3 + Math.random() * 0.2);
      colors.push(color.r, color.g, color.b);

      sizes.push(0.02 + Math.random() * 0.03);
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    geometry.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));

    const material = new THREE.PointsMaterial({
      size: 0.05,
      vertexColors: true,
      transparent: true,
      opacity: 0.4,
      sizeAttenuation: true,
      blending: THREE.AdditiveBlending,
    });

    this.ambientParticles = new THREE.Points(geometry, material);
    this.scene.add(this.ambientParticles);
  }

  private calculateLODResolution(baseResolution: number, zoomLevel: number): number {
    if (zoomLevel < 10) return baseResolution;
    if (zoomLevel < 20) return Math.max(2, Math.floor(baseResolution / 2));
    if (zoomLevel < 30) return Math.max(1, Math.floor(baseResolution / 4));
    return 1;
  }

  private createLatticeStructure(resolution: number, showWireframes: boolean): void {
    this.latticeCells = [];
    this.cellMeshes = [];
    this.unitCellWireframes = [];

    const cellSize = this.scaleToVisualUnits(LATTICE_SPACING, this.currentScale);
    const offset = (resolution - 1) / 2;
    
    for (let x = 0; x < resolution; x++) {
      for (let y = 0; y < resolution; y++) {
        for (let z = 0; z < resolution; z++) {
          const position = new THREE.Vector3(
            (x - offset) * cellSize * 2.5,
            (y - offset) * cellSize * 2.5,
            (z - offset) * cellSize * 2.5
          );

          // Distance from center affects appearance
          const distFromCenter = position.length();
          const maxDist = offset * cellSize * 2.5 * Math.sqrt(3);
          const normalizedDist = Math.min(1, distFromCenter / maxDist);

          // Create dodecahedron geometry
          const geometry = geometryRegistry.generate('dodecahedron', {
            radius: cellSize,
            detail: 0
          });
          const threeGeometry = geometryToThreeJS(geometry);

          // Material: golden with depth-based variation
          const material = new THREE.MeshStandardMaterial({
            color: new THREE.Color(COLORS.goldPrimary).lerp(
              new THREE.Color(COLORS.spaceDeep),
              normalizedDist * 0.3
            ),
            metalness: 0.75,
            roughness: 0.25,
            emissive: new THREE.Color(COLORS.goldPrimary),
            emissiveIntensity: 0.08 * (1 - normalizedDist * 0.5),
            transparent: true,
            opacity: 0.45 - normalizedDist * 0.15,
            side: THREE.DoubleSide
          });

          const cell = new THREE.Mesh(threeGeometry, material);
          cell.position.copy(position);
          cell.userData = { 
            baseScale: 1, 
            phaseOffset: (x + y + z) * 0.2,
            distFromCenter: normalizedDist
          };
          this.scene.add(cell);
          this.cellMeshes.push(cell);

          const group = new THREE.Group();
          group.add(cell);
          this.latticeCells.push(group);

          // Wireframe overlay for structure clarity
          if (showWireframes) {
            const wireframeMaterial = new THREE.LineBasicMaterial({
              color: COLORS.goldBright,
              transparent: true,
              opacity: 0.15 - normalizedDist * 0.05,
              linewidth: 1,
            });
            const wireframe = new THREE.LineSegments(
              new THREE.EdgesGeometry(threeGeometry),
              wireframeMaterial
            );
            wireframe.position.copy(position);
            this.scene.add(wireframe);
            this.unitCellWireframes.push(wireframe);
          }
        }
      }
    }

    // Create central highlight glow
    this.createCentralGlow(cellSize);

    // Create lattice points
    this.createLatticePoints(resolution, cellSize);
  }

  private createCentralGlow(cellSize: number): void {
    // Soft central glow sphere
    const glowGeometry = new THREE.SphereGeometry(cellSize * 2, 32, 32);
    const glowMaterial = new THREE.MeshBasicMaterial({
      color: COLORS.goldPrimary,
      transparent: true,
      opacity: 0.1,
      side: THREE.BackSide,
    });
    const glow = new THREE.Mesh(glowGeometry, glowMaterial);
    this.scene.add(glow);
  }

  private createLatticePoints(resolution: number, cellSize: number): void {
    const positions: number[] = [];
    const colors: number[] = [];
    const offset = (resolution - 1) / 2;

    for (let x = 0; x < resolution; x++) {
      for (let y = 0; y < resolution; y++) {
        for (let z = 0; z < resolution; z++) {
          const pos = new THREE.Vector3(
            (x - offset) * cellSize * 2.5,
            (y - offset) * cellSize * 2.5,
            (z - offset) * cellSize * 2.5
          );

          positions.push(pos.x, pos.y, pos.z);

          // Pressure-based color gradient
          const pressure = this.calculatePressureAtPoint(pos);
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
      size: cellSize * 0.15,
      vertexColors: true,
      transparent: true,
      opacity: 0.7,
      sizeAttenuation: true,
      blending: THREE.AdditiveBlending,
    });

    this.latticePoints = new THREE.Points(geometry, material);
    this.scene.add(this.latticePoints);
  }

  private createPressureVisualization(resolution: number): void {
    // Pressure field as volumetric particle cloud
    const particleCount = 1000;
    const positions: number[] = [];
    const colors: number[] = [];
    const cellSize = this.scaleToVisualUnits(LATTICE_SPACING, this.currentScale);
    const fieldSize = cellSize * resolution * 2;

    for (let i = 0; i < particleCount; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const r = Math.random() * fieldSize * 0.8;

      const x = r * Math.sin(phi) * Math.cos(theta);
      const y = r * Math.sin(phi) * Math.sin(theta);
      const z = r * Math.cos(phi);

      positions.push(x, y, z);

      const pos = new THREE.Vector3(x, y, z);
      const pressure = this.calculatePressureAtPoint(pos);
      
      const color = new THREE.Color();
      color.lerpColors(
        new THREE.Color(COLORS.spaceDeep),
        new THREE.Color(COLORS.goldLight),
        pressure
      );
      colors.push(color.r, color.g, color.b);
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.03,
      vertexColors: true,
      transparent: true,
      opacity: 0.25,
      sizeAttenuation: true,
      blending: THREE.AdditiveBlending,
    });

    this.pressureField = new THREE.Points(geometry, material);
    this.scene.add(this.pressureField);
  }

  private createDeformationVectors(resolution: number): void {
    const cellSize = this.scaleToVisualUnits(LATTICE_SPACING, this.currentScale);
    const offset = (resolution - 1) / 2;

    // Create arrows showing deformation direction
    for (let x = 0; x < resolution; x += 2) {
      for (let y = 0; y < resolution; y += 2) {
        for (let z = 0; z < resolution; z += 2) {
          const pos = new THREE.Vector3(
            (x - offset) * cellSize * 2.5,
            (y - offset) * cellSize * 2.5,
            (z - offset) * cellSize * 2.5
          );

          // Deformation points toward center (pressure gradient)
          const direction = pos.clone().negate().normalize();
          const magnitude = Math.min(0.5, pos.length() * 0.1);

          if (magnitude > 0.1) {
            const arrow = new THREE.ArrowHelper(
              direction,
              pos,
              magnitude,
              COLORS.goldBright,
              magnitude * 0.2,
              magnitude * 0.1
            );
            this.scene.add(arrow);
            this.deformationVectors.push(arrow);
          }
        }
      }
    }
  }

  private calculatePressureAtPoint(position: THREE.Vector3): number {
    const distance = position.length();
    const maxDist = 10;
    // Higher pressure at center, decreasing outward
    return Math.max(0, 1 - distance / maxDist);
  }

  private scaleToVisualUnits(meters: number, log10Scale: number): number {
    const scaleFactor = Math.pow(10, -log10Scale + 1);
    return meters * scaleFactor;
  }

  private updateCameraForScale(): void {
    const scaleFactor = Math.pow(10, -this.currentScale + 1);
    const baseDistance = 10;
    const cameraDistance = baseDistance * scaleFactor;

    this.camera.position.set(
      cameraDistance * 0.5,
      cameraDistance * 0.4,
      cameraDistance * 0.7
    );
    this.camera.lookAt(0, 0, 0);
  }

  update(deltaTime: number): void {
    this.time += deltaTime;
    this.breathPhase += deltaTime * 0.5;
    this.rotationPhase += deltaTime * 0.08;

    // Organic breathing animation for cells
    this.cellMeshes.forEach((cell, index) => {
      const phaseOffset = cell.userData.phaseOffset || 0;
      const distFromCenter = cell.userData.distFromCenter || 0;
      
      // Breathing effect - subtle scale pulsing
      const breathAmount = Math.sin(this.breathPhase + phaseOffset) * 0.03;
      const scale = 1.0 + breathAmount * (1 - distFromCenter * 0.5);
      cell.scale.setScalar(scale);

      // Very subtle rotation
      cell.rotation.y += deltaTime * 0.02 * (1 - distFromCenter);
      cell.rotation.x += deltaTime * 0.01 * (1 - distFromCenter);
    });

    // Wireframes pulse slightly
    this.unitCellWireframes.forEach((wireframe, index) => {
      const material = wireframe.material as THREE.LineBasicMaterial;
      material.opacity = 0.12 + Math.sin(this.breathPhase + index * 0.1) * 0.03;
    });

    // Slow scene rotation
    if (this.ambientParticles) {
      this.ambientParticles.rotation.y = this.rotationPhase * 0.3;
    }

    // Pressure field subtle animation
    if (this.pressureField) {
      this.pressureField.rotation.y += deltaTime * 0.02;
      this.pressureField.rotation.x += deltaTime * 0.01;
    }
  }

  protected onParametersChanged(): void {
    this.init();
  }

  dispose(): void {
    this.disposeObject(this.latticePoints);
    this.disposeObject(this.pressureField);
    this.disposeObject(this.ambientParticles);
    this.cellMeshes.forEach(cell => this.disposeObject(cell));
    this.unitCellWireframes.forEach(wireframe => this.disposeObject(wireframe));
    this.deformationVectors.forEach(arrow => {
      if (arrow) arrow.dispose();
    });

    this.latticeCells = [];
    this.cellMeshes = [];
    this.latticePoints = null;
    this.pressureField = null;
    this.ambientParticles = null;
    this.unitCellWireframes = [];
    this.deformationVectors = [];
  }

  private disposeObject(object: THREE.Object3D | null): void {
    if (!object) return;

    object.traverse((child) => {
      if (child instanceof THREE.Mesh || child instanceof THREE.Points || child instanceof THREE.LineSegments) {
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
export const SpationLatticeSim: React.FC<SpationLatticeSimProps> = ({
  id,
  parameters,
  onParameterChange,
  showFormulas = true,
  showLabels = true,
  narrationEnabled = false,
  onReady,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const simulationRef = useRef<SpationLatticeSimulation | null>(null);
  const [latticeData, setLatticeData] = useState({
    scale: -35,
    cellCount: 0,
    pressure: 0,
  });
  const [currentZoom, setCurrentZoom] = useState(0);

  useEffect(() => {
    if (!containerRef.current) return;

    const sim = new SpationLatticeSimulation(containerRef.current);
    sim.setParameters({
      scale: -35,
      showPressure: true,
      showDeformation: false,
      latticeResolution: 5,
      zoomLevel: 0,
      showUnitCells: true,
      ...parameters,
    });
    sim.init();
    simulationRef.current = sim;

    const resolution = parameters.latticeResolution ?? 5;
    setLatticeData({
      scale: parameters.scale ?? -35,
      cellCount: resolution * resolution * resolution,
      pressure: BULK_MODULUS,
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
    }
  }, [parameters]);

  const handleZoomChange = useCallback((delta: number) => {
    const newZoom = Math.max(0, Math.min(35, currentZoom + delta));
    setCurrentZoom(newZoom);
    if (onParameterChange) {
      onParameterChange({ zoomLevel: newZoom, scale: -35 + newZoom });
    }
  }, [currentZoom, onParameterChange]);

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

      {/* Scale indicator - top left */}
      <div className="absolute top-4 left-4 flex flex-col gap-2">
        <div 
          className="px-3 py-2 rounded-lg text-xs font-mono"
          style={{
            background: 'rgba(10, 14, 26, 0.85)',
            backdropFilter: 'blur(12px)',
            border: '1px solid rgba(214, 158, 46, 0.2)',
            color: '#e2e8f0',
          }}
        >
          <div className="flex items-center gap-2 mb-2">
            <span style={{ color: '#94a3b8' }}>Scale:</span>
            <span style={{ color: '#d69e2e' }}>10<sup>{latticeData.scale.toFixed(0)}</sup> m</span>
          </div>
          <div className="flex gap-1">
            <button 
              onClick={() => handleZoomChange(-5)}
              className="px-2 py-1 rounded text-xs transition-all duration-200"
              style={{
                background: 'rgba(214, 158, 46, 0.15)',
                border: '1px solid rgba(214, 158, 46, 0.3)',
                color: '#d69e2e',
              }}
            >
              ← Smaller
            </button>
            <button 
              onClick={() => handleZoomChange(5)}
              className="px-2 py-1 rounded text-xs transition-all duration-200"
              style={{
                background: 'rgba(214, 158, 46, 0.15)',
                border: '1px solid rgba(214, 158, 46, 0.3)',
                color: '#d69e2e',
              }}
            >
              Larger →
            </button>
          </div>
        </div>
      </div>

      {/* Labels panel - bottom left */}
      {showLabels && (
        <div 
          className="absolute bottom-4 left-4 p-4 rounded-xl text-sm max-w-xs"
          style={{
            background: 'rgba(10, 14, 26, 0.85)',
            backdropFilter: 'blur(12px)',
            border: '1px solid rgba(214, 158, 46, 0.15)',
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
          }}
        >
          <div 
            className="font-semibold mb-3 text-sm tracking-wide"
            style={{ color: '#d69e2e' }}
          >
            SPATION LATTICE
          </div>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between items-center">
              <span style={{ color: '#94a3b8' }}>Scale (log₁₀):</span>
              <span className="font-mono" style={{ color: '#e2e8f0' }}>
                {latticeData.scale.toFixed(1)}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span style={{ color: '#94a3b8' }}>Unit Cells:</span>
              <span className="font-mono" style={{ color: '#e2e8f0' }}>
                {latticeData.cellCount}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span style={{ color: '#94a3b8' }}>K<sub>bulk</sub>:</span>
              <span className="font-mono text-[10px]" style={{ color: '#d69e2e' }}>
                4.6×10¹¹³ Pa
              </span>
            </div>
            <div 
              className="mt-3 pt-3 text-xs"
              style={{ 
                borderTop: '1px solid rgba(148, 163, 184, 0.2)',
                color: '#cbd5e0' 
              }}
            >
              <div>Dodecahedral Packing</div>
              <div style={{ color: '#94a3b8' }}>Planck-scale structure</div>
            </div>
          </div>
        </div>
      )}

      {/* Formula overlay - top right */}
      {showFormulas && (
        <div 
          className="absolute top-4 right-4 p-3 rounded-xl text-xs font-mono"
          style={{
            background: 'rgba(10, 14, 26, 0.85)',
            backdropFilter: 'blur(12px)',
            border: '1px solid rgba(214, 158, 46, 0.15)',
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
            color: '#e2e8f0',
          }}
        >
          <div style={{ color: '#f6ad55' }}>
            K<sub>bulk</sub> = 4.6×10¹¹³ Pa
          </div>
          <div className="mt-1" style={{ color: '#fbbf24' }}>
            ρ<sub>spation</sub> = 5.2×10⁹⁶ kg/m³
          </div>
          <div className="mt-2 text-[10px]" style={{ color: '#94a3b8' }}>
            Incompressible Medium
          </div>
        </div>
      )}
    </div>
  );
};
