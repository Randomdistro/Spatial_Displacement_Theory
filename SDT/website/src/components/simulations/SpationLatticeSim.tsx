/**
 * Spation Lattice Simulation
 * Agent 3: Physics/Simulation
 *
 * Visualizes the fundamental spation lattice structure at Planck scale
 * Shows dodecahedral packing, K_bulk emergence, and pressure visualization
 */

import React, { useEffect, useRef } from 'react';
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

class SpationLatticeSimulation extends SimulationBase {
  private latticeCells: THREE.Group[] = [];
  private latticePoints: THREE.Points | null = null;
  private pressureField: THREE.Points | null = null;
  private deformationVectors: THREE.ArrowHelper[] = [];
  private unitCellWireframes: THREE.LineSegments[] = [];

  // Scale tracking
  private currentScale: number = -35; // log10 meters (Planck scale)
  private currentZoomLevel: number = 0; // 0-35 (orders of magnitude)

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

    // Dodecahedron generator should already be registered in GeometryGenerator.ts
    // If not, register it
    try {
      geometryRegistry.generate('dodecahedron', { radius: 1.0 });
    } catch (e) {
      // Generator not registered, register it now
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

    // Set scene background
    this.scene.background = new THREE.Color(0x0a0e1a);
  }

  private calculateLODResolution(baseResolution: number, zoomLevel: number): number {
    // Reduce resolution at extreme scales for performance
    if (zoomLevel < 10) return baseResolution;
    if (zoomLevel < 20) return Math.max(2, Math.floor(baseResolution / 2));
    if (zoomLevel < 30) return Math.max(1, Math.floor(baseResolution / 4));
    return 1; // Minimum detail at extreme scales
  }

  private createLatticeStructure(resolution: number, showWireframes: boolean): void {
    this.latticeCells = [];
    this.unitCellWireframes = [];

    // Calculate cell size in visualization units
    // At Planck scale (10⁻³⁵ m), we scale to visible size
    const cellSize = this.scaleToVisualUnits(LATTICE_SPACING, this.currentScale);

    // Generate dodecahedral unit cells in 3D grid
    const offset = (resolution - 1) / 2;
    
    for (let x = 0; x < resolution; x++) {
      for (let y = 0; y < resolution; y++) {
        for (let z = 0; z < resolution; z++) {
          const position = new THREE.Vector3(
            (x - offset) * cellSize * 2.5,
            (y - offset) * cellSize * 2.5,
            (z - offset) * cellSize * 2.5
          );

          // Create dodecahedron geometry
          const geometry = geometryRegistry.generate('dodecahedron', {
            radius: cellSize,
            detail: 0
          });
          const threeGeometry = geometryToThreeJS(geometry);

          // STYLING PLACEHOLDER: Material properties for dodecahedral cells
          // Creative Agent: Apply subtle gold wireframe with low opacity
          // Color: Use --color-gold-primary with low emissive
          // Opacity: 0.3-0.5 for subtle visibility
          // Metalness: 0.7-0.8 for subtle metallic sheen
          const material = new THREE.MeshStandardMaterial({
            color: 0xd69e2e, // PLACEHOLDER: Use --color-gold-primary
            metalness: 0.7,  // PLACEHOLDER: Use --material-metallic
            roughness: 0.3,  // PLACEHOLDER: Use --material-roughness
            emissive: 0x332200,
            emissiveIntensity: 0.1, // PLACEHOLDER: Use --material-emissive
            transparent: true,
            opacity: 0.4, // PLACEHOLDER: Adjust for visibility
            wireframe: false,
            side: THREE.DoubleSide
          });

          const cell = new THREE.Mesh(threeGeometry, material);
          cell.position.copy(position);
          this.scene.add(cell);
          this.latticeCells.push(new THREE.Group().add(cell));

          // Create wireframe if requested
          if (showWireframes) {
            const wireframeGeometry = threeGeometry.clone();
            const wireframeMaterial = new THREE.LineBasicMaterial({
              color: 0xd69e2e, // PLACEHOLDER: Use --color-gold-primary
              transparent: true,
              opacity: 0.2 // PLACEHOLDER: Very subtle wireframe
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

    // Create lattice point cloud for pressure visualization
    this.createLatticePoints(resolution, cellSize);
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

          // STYLING PLACEHOLDER: Pressure color coding
          // Creative Agent: Gradient from deep blue (low pressure) to gold (high pressure)
          // Use --color-space-deep → --color-gold-primary gradient
          // Base pressure calculation (simplified for now)
          const pressure = this.calculatePressureAtPoint(pos);
          const normalizedPressure = Math.max(0, Math.min(1, pressure));

          const color = new THREE.Color();
          color.lerpColors(
            new THREE.Color(0x1a365d), // PLACEHOLDER: Use --color-space-deep
            new THREE.Color(0xd69e2e), // PLACEHOLDER: Use --color-gold-primary
            normalizedPressure
          );
          colors.push(color.r, color.g, color.b);
        }
      }
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    // STYLING PLACEHOLDER: Points material
    // Creative Agent: Subtle point size with vertex colors
    const material = new THREE.PointsMaterial({
      size: cellSize * 0.1, // PLACEHOLDER: Scale appropriately
      vertexColors: true,
      transparent: true,
      opacity: 0.6, // PLACEHOLDER: Adjust visibility
      sizeAttenuation: true
    });

    this.latticePoints = new THREE.Points(geometry, material);
    this.scene.add(this.latticePoints);
  }

  private createPressureVisualization(resolution: number): void {
    // STYLING PLACEHOLDER: Pressure field visualization
    // Creative Agent: Show pressure gradients as subtle field
    // Use particle system or volume rendering
    // Colors: --color-space-deep (low) → --color-gold-primary (high)
    // This is a placeholder - full implementation would calculate pressure field
    // from Master Equation: ∇·[K_bulk ∇Δ(x)] = -κρ_disp(x)(1-E(x,ñ))
  }

  private createDeformationVectors(resolution: number): void {
    // STYLING PLACEHOLDER: Deformation vector visualization
    // Creative Agent: Show lattice deformation as arrows
    // Arrow color: --color-gold-primary
    // Arrow length: proportional to deformation magnitude
    // This is a placeholder - full implementation would calculate deformation
    // from pressure field and K_bulk
  }

  private calculatePressureAtPoint(position: THREE.Vector3): number {
    // STYLING PLACEHOLDER: Pressure calculation
    // Simplified pressure calculation for visualization
    // Full implementation would solve Master Equation
    const distance = position.length();
    const basePressure = 1.0;
    const pressureGradient = 0.1 / (distance + 0.1);
    return basePressure - pressureGradient;
  }

  private scaleToVisualUnits(meters: number, log10Scale: number): number {
    // Convert physical scale to visualization units
    // At Planck scale, we need to scale up to visible size
    const scaleFactor = Math.pow(10, -log10Scale + 1); // Scale up from Planck
    return meters * scaleFactor;
  }

  private updateCameraForScale(): void {
    // Adjust camera based on current scale
    const scaleFactor = Math.pow(10, -this.currentScale + 1);
    const baseDistance = 10;
    const cameraDistance = baseDistance * scaleFactor;

    this.camera.position.set(0, cameraDistance * 0.7, cameraDistance);
    this.camera.lookAt(0, 0, 0);
  }

  update(deltaTime: number): void {
    this.time += deltaTime;

    // STYLING PLACEHOLDER: Idle animations
    // Creative Agent: Subtle breathing/pulsing of lattice cells
    // Organic motion: slight scale variation, gentle rotation
    // Use GSAP or manual animation with sine waves
    // Timing: --timing-slow (1000ms), easing: --ease-organic

    // Subtle rotation of entire lattice
    this.scene.rotation.y += deltaTime * 0.1;

    // Subtle pulsing of cells (breathing effect)
    this.latticeCells.forEach((cell, index) => {
      const pulse = Math.sin(this.time * 0.5 + index * 0.1) * 0.02;
      cell.scale.setScalar(1.0 + pulse);
    });
  }

  protected onParametersChanged(): void {
    // Reinitialize when parameters change
    this.init();
  }

  dispose(): void {
    this.disposeObject(this.latticePoints);
    this.disposeObject(this.pressureField);
    this.latticeCells.forEach(cell => this.disposeObject(cell));
    this.unitCellWireframes.forEach(wireframe => this.disposeObject(wireframe));
    this.deformationVectors.forEach(arrow => {
      if (arrow) arrow.dispose();
    });

    this.latticeCells = [];
    this.latticePoints = null;
    this.pressureField = null;
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
  const [latticeData, setLatticeData] = React.useState({
    scale: -35,
    cellCount: 0,
    pressure: 0,
  });

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

    // Calculate lattice data
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

  return (
    <div className="relative w-full h-full">
      {/* STYLING PLACEHOLDER: Simulation container */}
      {/* Creative Agent: Apply consistent simulation container styling */}
      {/* Background: --color-bg-deep, rounded corners, proper sizing */}
      <div
        ref={containerRef}
        className="w-full h-full min-h-[500px] bg-slate-900 rounded-lg"
        style={{ touchAction: 'none' }}
      />

      {/* STYLING PLACEHOLDER: Labels panel */}
      {/* Creative Agent: Match existing simulation label panel styling */}
      {/* Position: absolute bottom-left, glassmorphism effect */}
      {/* Colors: Use design system colors, proper contrast */}
      {showLabels && (
        <div className="absolute bottom-4 left-4 bg-black/70 backdrop-blur-sm text-white p-4 rounded-lg text-sm max-w-xs">
          <div className="font-semibold mb-3 text-amber-400">Spation Lattice</div>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Scale (log₁₀):</span>
              <span className="font-mono">{latticeData.scale.toFixed(1)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Cell Count:</span>
              <span className="font-mono">{latticeData.cellCount}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">K_bulk:</span>
              <span className="font-mono text-[10px]">{BULK_MODULUS.toExponential(1)} Pa</span>
            </div>
            <div className="mt-3 pt-3 border-t border-slate-600 text-slate-300">
              <div className="text-xs">Dodecahedral Packing</div>
              <div className="text-xs text-slate-400">Planck-scale structure</div>
            </div>
          </div>
        </div>
      )}

      {/* STYLING PLACEHOLDER: Formula overlay */}
      {/* Creative Agent: Match existing formula overlay styling */}
      {/* Position: absolute top-right, subtle background */}
      {showFormulas && (
        <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm text-white p-3 rounded-lg text-xs font-mono">
          <div>K_{bulk} = 4.6×10¹¹³ Pa</div>
          <div className="mt-2 text-slate-400 text-[10px]">
            Spation Lattice Bulk Modulus
          </div>
        </div>
      )}

      {/* STYLING PLACEHOLDER: Scale indicator */}
      {/* Creative Agent: Show current scale with zoom controls */}
      {/* Position: absolute top-left, interactive controls */}
      {/* Style: Match existing control panel styling */}
    </div>
  );
};

