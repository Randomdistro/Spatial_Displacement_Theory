/**
 * Chemical Bonding Simulation
 * Agent 3: Physics/Simulation
 *
 * Visualizes chemical bonding as pressure field overlap between atoms
 * Shows how bonds form, bond energy, and molecular geometry prediction
 * 
 * TEKNE Design: Bonds ARE pressure field overlap - no quantum orbitals
 */

import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as THREE from 'three';
import { SimulationBase, SimulationProps } from './SimulationBase';

interface AtomConfig {
  element: string;
  position: [number, number, number];
  radius: number;
  atomicNumber: number;
}

interface BondInfo {
  atom1Index: number;
  atom2Index: number;
  energy: number;
  distance: number;
  strength: number;
}

interface ChemicalBondingSimProps extends SimulationProps {
  parameters: {
    atoms?: AtomConfig[];
    showPressureFields?: boolean;
    showBonds?: boolean;
    showEnergy?: boolean;
    showGeometry?: boolean;
    interactive?: boolean;
    moleculePreset?: 'H2' | 'H2O' | 'CH4' | 'CO2' | 'custom';
  };
}

// Element data with SDT-relevant properties
const ELEMENT_DATA: Record<string, { 
  radius: number; 
  color: number; 
  atomicNumber: number;
  name: string;
  exclusionRadius: number;
}> = {
  H: { radius: 5.29177e-11, color: 0xffffff, atomicNumber: 1, name: 'Hydrogen', exclusionRadius: 1.2e-10 },
  He: { radius: 3.1e-11, color: 0xd9ffff, atomicNumber: 2, name: 'Helium', exclusionRadius: 1.4e-10 },
  Li: { radius: 1.67e-10, color: 0xcc80ff, atomicNumber: 3, name: 'Lithium', exclusionRadius: 1.82e-10 },
  C: { radius: 7.0e-11, color: 0x404040, atomicNumber: 6, name: 'Carbon', exclusionRadius: 1.7e-10 },
  N: { radius: 6.5e-11, color: 0x3050f8, atomicNumber: 7, name: 'Nitrogen', exclusionRadius: 1.55e-10 },
  O: { radius: 6.0e-11, color: 0xff4040, atomicNumber: 8, name: 'Oxygen', exclusionRadius: 1.52e-10 },
};

// Molecule presets
const MOLECULE_PRESETS: Record<string, AtomConfig[]> = {
  H2: [
    { element: 'H', position: [-0.74e-10, 0, 0], radius: 5.29177e-11, atomicNumber: 1 },
    { element: 'H', position: [0.74e-10, 0, 0], radius: 5.29177e-11, atomicNumber: 1 },
  ],
  H2O: [
    { element: 'O', position: [0, 0, 0], radius: 6.0e-11, atomicNumber: 8 },
    { element: 'H', position: [-0.96e-10, 0.59e-10, 0], radius: 5.29177e-11, atomicNumber: 1 },
    { element: 'H', position: [0.96e-10, 0.59e-10, 0], radius: 5.29177e-11, atomicNumber: 1 },
  ],
  CH4: [
    { element: 'C', position: [0, 0, 0], radius: 7.0e-11, atomicNumber: 6 },
    { element: 'H', position: [1.09e-10, 1.09e-10, 1.09e-10], radius: 5.29177e-11, atomicNumber: 1 },
    { element: 'H', position: [-1.09e-10, -1.09e-10, 1.09e-10], radius: 5.29177e-11, atomicNumber: 1 },
    { element: 'H', position: [-1.09e-10, 1.09e-10, -1.09e-10], radius: 5.29177e-11, atomicNumber: 1 },
    { element: 'H', position: [1.09e-10, -1.09e-10, -1.09e-10], radius: 5.29177e-11, atomicNumber: 1 },
  ],
  CO2: [
    { element: 'C', position: [0, 0, 0], radius: 7.0e-11, atomicNumber: 6 },
    { element: 'O', position: [-1.16e-10, 0, 0], radius: 6.0e-11, atomicNumber: 8 },
    { element: 'O', position: [1.16e-10, 0, 0], radius: 6.0e-11, atomicNumber: 8 },
  ],
};

// Design System Colors (TEKNE)
const COLORS = {
  spaceDeep: 0x1a365d,
  spaceMedium: 0x2d5a87,
  spaceLight: 0x4299e1,
  goldPrimary: 0xd69e2e,
  goldBright: 0xf6ad55,
  goldLight: 0xfbbf24,
  bgDeep: 0x0a0e1a,
  bondStrong: 0xecc94b,
  bondMedium: 0xd69e2e,
  bondWeak: 0xa0aec0,
  overlapGlow: 0xf6e05e,
};

class ChemicalBondingSimulation extends SimulationBase {
  private atoms: THREE.Mesh[] = [];
  private atomGlows: THREE.Mesh[] = [];
  private pressureFields: THREE.Mesh[] = [];
  private bondMeshes: THREE.Mesh[] = [];
  private bondGlows: THREE.Mesh[] = [];
  private overlapRegions: THREE.Mesh[] = [];
  private ambientParticles: THREE.Points | null = null;
  private moleculeCenter: THREE.Vector3 = new THREE.Vector3();

  private atomConfigs: AtomConfig[] = [];
  private bondInfos: BondInfo[] = [];

  // Animation state
  private breathPhase: number = 0;
  private vibrationPhase: number = 0;

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
    const preset = this.parameters.moleculePreset ?? 'H2';
    const atoms = this.parameters.atoms ?? MOLECULE_PRESETS[preset] ?? MOLECULE_PRESETS.H2;
    const showPressure = this.parameters.showPressureFields ?? true;
    const showBonds = this.parameters.showBonds ?? true;
    const showEnergy = this.parameters.showEnergy ?? true;
    const showGeometry = this.parameters.showGeometry ?? true;

    this.atomConfigs = atoms;
    this.bondInfos = [];

    // Scene setup
    this.scene.background = new THREE.Color(COLORS.bgDeep);
    this.scene.fog = new THREE.FogExp2(COLORS.bgDeep, 0.006);

    // Scale factor for visualization
    const scaleFactor = 1e10;

    // Calculate molecule center
    this.calculateMoleculeCenter(atoms, scaleFactor);

    // Create ambient environment
    this.createAmbientEnvironment(scaleFactor);

    // Create atoms and pressure fields
    atoms.forEach((atomConfig, index) => {
      this.createAtom(atomConfig, index, scaleFactor, showPressure);
    });

    // Calculate and visualize bonds
    if (showBonds) {
      this.calculateAndVisualizeBonds(scaleFactor);
    }

    // Show molecular geometry
    if (showGeometry && atoms.length > 2) {
      this.visualizeMolecularGeometry(scaleFactor);
    }

    // Position camera
    const maxDist = Math.max(...atoms.map(a => {
      const dist = Math.sqrt(a.position[0]**2 + a.position[1]**2 + a.position[2]**2);
      return dist * scaleFactor;
    }));
    const cameraDistance = Math.max(maxDist * 3, 15);
    this.camera.position.set(
      cameraDistance * 0.6,
      cameraDistance * 0.4,
      cameraDistance * 0.8
    );
    this.camera.lookAt(this.moleculeCenter);
  }

  private calculateMoleculeCenter(atoms: AtomConfig[], scaleFactor: number): void {
    const center = new THREE.Vector3();
    atoms.forEach(atom => {
      center.add(new THREE.Vector3(...atom.position).multiplyScalar(scaleFactor));
    });
    center.divideScalar(atoms.length);
    this.moleculeCenter = center;
  }

  private createAmbientEnvironment(scaleFactor: number): void {
    const particleCount = 200;
    const positions: number[] = [];
    const colors: number[] = [];

    const radius = 50;
    for (let i = 0; i < particleCount; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const r = radius * (0.5 + Math.random() * 0.5);

      positions.push(
        r * Math.sin(phi) * Math.cos(theta),
        r * Math.sin(phi) * Math.sin(theta),
        r * Math.cos(phi)
      );

      const color = new THREE.Color(COLORS.goldPrimary);
      color.multiplyScalar(0.15 + Math.random() * 0.1);
      colors.push(color.r, color.g, color.b);
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.04,
      vertexColors: true,
      transparent: true,
      opacity: 0.35,
      sizeAttenuation: true,
      blending: THREE.AdditiveBlending,
    });

    this.ambientParticles = new THREE.Points(geometry, material);
    this.scene.add(this.ambientParticles);
  }

  private createAtom(config: AtomConfig, index: number, scaleFactor: number, showPressure: boolean): void {
    const elementData = ELEMENT_DATA[config.element] || ELEMENT_DATA.H;
    const position = new THREE.Vector3(...config.position).multiplyScalar(scaleFactor);
    const radius_scaled = config.radius * scaleFactor;

    // Create atom core (nucleus representation)
    const coreSize = radius_scaled * 0.15;
    const coreGeometry = new THREE.SphereGeometry(coreSize, 24, 24);
    const coreMaterial = new THREE.MeshStandardMaterial({
      color: elementData.color,
      metalness: 0.85,
      roughness: 0.15,
      emissive: new THREE.Color(elementData.color),
      emissiveIntensity: 0.4
    });
    const atomCore = new THREE.Mesh(coreGeometry, coreMaterial);
    atomCore.position.copy(position);
    atomCore.userData = { element: config.element, index };
    this.scene.add(atomCore);
    this.atoms.push(atomCore);

    // Create atom glow
    const glowGeometry = new THREE.SphereGeometry(coreSize * 2, 24, 24);
    const glowMaterial = new THREE.MeshBasicMaterial({
      color: elementData.color,
      transparent: true,
      opacity: 0.2,
      side: THREE.BackSide,
    });
    const atomGlow = new THREE.Mesh(glowGeometry, glowMaterial);
    atomGlow.position.copy(position);
    this.scene.add(atomGlow);
    this.atomGlows.push(atomGlow);

    // Create pressure exclusion zone
    if (showPressure) {
      const exclusionRadius = elementData.exclusionRadius * scaleFactor;
      const fieldGeometry = new THREE.SphereGeometry(exclusionRadius, 32, 32);
      
      // Outer wireframe shell
      const wireframeMaterial = new THREE.MeshBasicMaterial({
        color: COLORS.spaceMedium,
        transparent: true,
        opacity: 0.08,
        wireframe: true,
      });
      const wireframeMesh = new THREE.Mesh(fieldGeometry, wireframeMaterial);
      wireframeMesh.position.copy(position);
      this.scene.add(wireframeMesh);

      // Inner subtle fill
      const fillMaterial = new THREE.MeshBasicMaterial({
        color: COLORS.spaceLight,
        transparent: true,
        opacity: 0.04,
        side: THREE.DoubleSide,
      });
      const fillMesh = new THREE.Mesh(fieldGeometry.clone(), fillMaterial);
      fillMesh.position.copy(position);
      fillMesh.scale.setScalar(0.98);
      this.scene.add(fillMesh);
      
      this.pressureFields.push(wireframeMesh, fillMesh);
    }
  }

  private calculateAndVisualizeBonds(scaleFactor: number): void {
    const maxBondDistance = 3e-10 * scaleFactor;

    for (let i = 0; i < this.atoms.length; i++) {
      for (let j = i + 1; j < this.atoms.length; j++) {
        const atom1 = this.atoms[i];
        const atom2 = this.atoms[j];
        const distance = atom1.position.distanceTo(atom2.position);

        if (distance < maxBondDistance) {
          // Calculate bond energy and strength
          const bondInfo = this.calculateBondProperties(i, j, distance, scaleFactor);
          this.bondInfos.push(bondInfo);

          // Create bond visualization
          this.createBond(atom1, atom2, bondInfo);

          // Create overlap region
          this.createOverlapRegion(atom1, atom2, bondInfo, scaleFactor);
        }
      }
    }
  }

  private calculateBondProperties(
    atom1Index: number,
    atom2Index: number,
    distance: number,
    scaleFactor: number
  ): BondInfo {
    const config1 = this.atomConfigs[atom1Index];
    const config2 = this.atomConfigs[atom2Index];
    const elem1 = ELEMENT_DATA[config1.element] || ELEMENT_DATA.H;
    const elem2 = ELEMENT_DATA[config2.element] || ELEMENT_DATA.H;

    // SDT bond energy from pressure field overlap
    const R1 = elem1.exclusionRadius;
    const R2 = elem2.exclusionRadius;
    const r = distance / scaleFactor;
    
    // Overlap area approximation
    const overlap = Math.max(0, (R1 + R2 - r) / (R1 + R2));
    const energy = overlap * (elem1.atomicNumber * elem2.atomicNumber) * 1e-19; // Simplified
    
    // Strength affects visual appearance
    const strength = Math.min(1, overlap * 2);

    return {
      atom1Index,
      atom2Index,
      energy,
      distance: r,
      strength
    };
  }

  private createBond(atom1: THREE.Mesh, atom2: THREE.Mesh, bondInfo: BondInfo): void {
    const midpoint = new THREE.Vector3()
      .addVectors(atom1.position, atom2.position)
      .multiplyScalar(0.5);
    
    const direction = new THREE.Vector3()
      .subVectors(atom2.position, atom1.position);
    const bondLength = direction.length();
    direction.normalize();

    // Bond thickness based on strength
    const bondRadius = 0.08 + bondInfo.strength * 0.12;
    
    // Create bond cylinder
    const bondGeometry = new THREE.CylinderGeometry(
      bondRadius,
      bondRadius,
      bondLength,
      12
    );
    
    // Color based on bond strength
    const bondColor = new THREE.Color();
    if (bondInfo.strength > 0.7) {
      bondColor.set(COLORS.bondStrong);
    } else if (bondInfo.strength > 0.4) {
      bondColor.set(COLORS.bondMedium);
    } else {
      bondColor.set(COLORS.bondWeak);
    }

    const bondMaterial = new THREE.MeshStandardMaterial({
      color: bondColor,
      emissive: bondColor,
      emissiveIntensity: 0.3 * bondInfo.strength,
      metalness: 0.7,
      roughness: 0.3,
      transparent: true,
      opacity: 0.85,
    });

    const bondMesh = new THREE.Mesh(bondGeometry, bondMaterial);
    bondMesh.position.copy(midpoint);
    
    // Orient cylinder to point along bond direction
    const quaternion = new THREE.Quaternion();
    quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), direction);
    bondMesh.quaternion.copy(quaternion);
    
    bondMesh.userData = { bondInfo };
    this.scene.add(bondMesh);
    this.bondMeshes.push(bondMesh);

    // Bond glow
    const glowGeometry = new THREE.CylinderGeometry(
      bondRadius * 2,
      bondRadius * 2,
      bondLength,
      12
    );
    const glowMaterial = new THREE.MeshBasicMaterial({
      color: bondColor,
      transparent: true,
      opacity: 0.1 * bondInfo.strength,
      side: THREE.BackSide,
    });
    const bondGlow = new THREE.Mesh(glowGeometry, glowMaterial);
    bondGlow.position.copy(midpoint);
    bondGlow.quaternion.copy(quaternion);
    this.scene.add(bondGlow);
    this.bondGlows.push(bondGlow);
  }

  private createOverlapRegion(
    atom1: THREE.Mesh,
    atom2: THREE.Mesh,
    bondInfo: BondInfo,
    scaleFactor: number
  ): void {
    // Create glowing region at bond midpoint representing pressure overlap
    const midpoint = new THREE.Vector3()
      .addVectors(atom1.position, atom2.position)
      .multiplyScalar(0.5);

    const overlapSize = 0.3 + bondInfo.strength * 0.4;
    const geometry = new THREE.SphereGeometry(overlapSize, 16, 16);
    const material = new THREE.MeshBasicMaterial({
      color: COLORS.overlapGlow,
      transparent: true,
      opacity: 0.15 * bondInfo.strength,
      blending: THREE.AdditiveBlending,
    });

    const overlapMesh = new THREE.Mesh(geometry, material);
    overlapMesh.position.copy(midpoint);
    this.scene.add(overlapMesh);
    this.overlapRegions.push(overlapMesh);
  }

  private visualizeMolecularGeometry(scaleFactor: number): void {
    // For molecules with 3+ atoms, show geometry guides
    if (this.atoms.length < 3) return;

    // Find central atom (usually has most bonds)
    const bondCounts = new Array(this.atoms.length).fill(0);
    this.bondInfos.forEach(bond => {
      bondCounts[bond.atom1Index]++;
      bondCounts[bond.atom2Index]++;
    });
    
    const centralIndex = bondCounts.indexOf(Math.max(...bondCounts));
    const centralAtom = this.atoms[centralIndex];

    // Draw angle guides from central atom to bonded atoms
    const bondedIndices = this.bondInfos
      .filter(b => b.atom1Index === centralIndex || b.atom2Index === centralIndex)
      .map(b => b.atom1Index === centralIndex ? b.atom2Index : b.atom1Index);

    // Create subtle angle arcs
    for (let i = 0; i < bondedIndices.length; i++) {
      for (let j = i + 1; j < bondedIndices.length; j++) {
        const atom1 = this.atoms[bondedIndices[i]];
        const atom2 = this.atoms[bondedIndices[j]];

        // Calculate angle
        const v1 = new THREE.Vector3().subVectors(atom1.position, centralAtom.position).normalize();
        const v2 = new THREE.Vector3().subVectors(atom2.position, centralAtom.position).normalize();
        const angle = Math.acos(v1.dot(v2)) * (180 / Math.PI);

        // Create subtle arc visualization
        const arcRadius = 1.5;
        const arcGeometry = new THREE.BufferGeometry();
        const points: THREE.Vector3[] = [];
        const segments = 20;
        
        for (let k = 0; k <= segments; k++) {
          const t = k / segments;
          const lerpedDir = new THREE.Vector3().lerpVectors(v1, v2, t).normalize();
          points.push(centralAtom.position.clone().add(lerpedDir.multiplyScalar(arcRadius)));
        }
        
        arcGeometry.setFromPoints(points);
        const arcMaterial = new THREE.LineBasicMaterial({
          color: COLORS.goldPrimary,
          transparent: true,
          opacity: 0.2,
        });
        
        const arc = new THREE.Line(arcGeometry, arcMaterial);
        this.scene.add(arc);
      }
    }
  }

  update(deltaTime: number): void {
    this.time += deltaTime;
    this.breathPhase += deltaTime * 0.8;
    this.vibrationPhase += deltaTime * 8;

    // Atom breathing/pulsing
    this.atomGlows.forEach((glow, index) => {
      const phaseOffset = index * 0.5;
      const pulse = Math.sin(this.breathPhase + phaseOffset) * 0.05;
      glow.scale.setScalar(2 + pulse);
      (glow.material as THREE.MeshBasicMaterial).opacity = 0.18 + pulse * 0.5;
    });

    // Subtle atom vibration
    this.atoms.forEach((atom, index) => {
      const basePos = new THREE.Vector3(...this.atomConfigs[index].position).multiplyScalar(1e10);
      const vibration = new THREE.Vector3(
        Math.sin(this.vibrationPhase + index) * 0.02,
        Math.cos(this.vibrationPhase + index * 1.3) * 0.02,
        Math.sin(this.vibrationPhase + index * 0.7) * 0.02
      );
      atom.position.copy(basePos.add(vibration));
    });

    // Bond pulsing
    this.bondMeshes.forEach((bond, index) => {
      const bondInfo = bond.userData.bondInfo as BondInfo;
      const pulse = Math.sin(this.breathPhase * 1.5 + index * 0.3) * 0.1;
      const material = bond.material as THREE.MeshStandardMaterial;
      material.emissiveIntensity = (0.3 + pulse) * bondInfo.strength;
    });

    // Overlap region pulsing
    this.overlapRegions.forEach((region, index) => {
      const pulse = Math.sin(this.breathPhase * 2 + index * 0.5);
      const scale = 1 + pulse * 0.15;
      region.scale.setScalar(scale);
      (region.material as THREE.MeshBasicMaterial).opacity = 0.12 + pulse * 0.05;
    });

    // Pressure field breathing
    this.pressureFields.forEach((field, index) => {
      const pulse = Math.sin(this.breathPhase + index * 0.2) * 0.02;
      field.scale.setScalar(1 + pulse);
    });

    // Ambient particles drift
    if (this.ambientParticles) {
      this.ambientParticles.rotation.y += deltaTime * 0.008;
    }
  }

  protected onParametersChanged(): void {
    this.init();
  }

  getBondInfos(): BondInfo[] {
    return this.bondInfos;
  }

  dispose(): void {
    this.atoms.forEach(atom => this.disposeObject(atom));
    this.atomGlows.forEach(glow => this.disposeObject(glow));
    this.pressureFields.forEach(field => this.disposeObject(field));
    this.bondMeshes.forEach(bond => this.disposeObject(bond));
    this.bondGlows.forEach(glow => this.disposeObject(glow));
    this.overlapRegions.forEach(region => this.disposeObject(region));
    this.disposeObject(this.ambientParticles);

    this.atoms = [];
    this.atomGlows = [];
    this.pressureFields = [];
    this.bondMeshes = [];
    this.bondGlows = [];
    this.overlapRegions = [];
    this.ambientParticles = null;
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
export const ChemicalBondingSim: React.FC<ChemicalBondingSimProps> = ({
  id,
  parameters,
  onParameterChange,
  showFormulas = true,
  showLabels = true,
  narrationEnabled = false,
  onReady,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const simulationRef = useRef<ChemicalBondingSimulation | null>(null);
  const [moleculeData, setMoleculeData] = useState({
    atomCount: 0,
    bondCount: 0,
    totalEnergy: 0,
    moleculeName: 'H₂',
  });
  const [selectedPreset, setSelectedPreset] = useState<string>(parameters.moleculePreset ?? 'H2');

  const moleculeNames: Record<string, string> = {
    H2: 'H₂ (Hydrogen)',
    H2O: 'H₂O (Water)',
    CH4: 'CH₄ (Methane)',
    CO2: 'CO₂ (Carbon Dioxide)',
  };

  useEffect(() => {
    if (!containerRef.current) return;

    const sim = new ChemicalBondingSimulation(containerRef.current);
    const defaultParams = {
      showPressureFields: true,
      showBonds: true,
      showEnergy: true,
      showGeometry: true,
      interactive: false,
      moleculePreset: selectedPreset as 'H2' | 'H2O' | 'CH4' | 'CO2',
      ...parameters,
    };
    sim.setParameters(defaultParams);
    sim.init();
    simulationRef.current = sim;

    // Get molecule data
    const atoms = parameters.atoms ?? MOLECULE_PRESETS[selectedPreset] ?? MOLECULE_PRESETS.H2;
    const bondInfos = sim.getBondInfos();
    const totalEnergy = bondInfos.reduce((sum, b) => sum + b.energy, 0);

    setMoleculeData({
      atomCount: atoms.length,
      bondCount: bondInfos.length,
      totalEnergy,
      moleculeName: moleculeNames[selectedPreset] || selectedPreset,
    });

    if (onReady) {
      setTimeout(onReady, 100);
    }

    sim.play();

    return () => {
      sim.destroy();
      simulationRef.current = null;
    };
  }, [onReady, selectedPreset]);

  useEffect(() => {
    if (simulationRef.current) {
      simulationRef.current.setParameters(parameters);
    }
  }, [parameters]);

  const handlePresetChange = useCallback((preset: string) => {
    setSelectedPreset(preset);
    if (onParameterChange) {
      onParameterChange({ ...parameters, moleculePreset: preset as 'H2' | 'H2O' | 'CH4' | 'CO2' });
    }
  }, [onParameterChange, parameters]);

  const formatEnergy = (energy: number): string => {
    if (energy >= 1e-18) return `${(energy * 1e18).toFixed(2)} aJ`;
    return `${energy.toExponential(2)} J`;
  };

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

      {/* Molecule selector - top left */}
      <div 
        className="absolute top-4 left-4 p-4 rounded-xl"
        style={{
          background: 'rgba(10, 14, 26, 0.9)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(214, 158, 46, 0.2)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
        }}
      >
        <div className="text-xs font-medium mb-3" style={{ color: '#94a3b8' }}>
          Select Molecule
        </div>
        <div className="flex flex-wrap gap-2">
          {Object.keys(MOLECULE_PRESETS).map(preset => (
            <button
              key={preset}
              onClick={() => handlePresetChange(preset)}
              className="px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200"
              style={{
                background: selectedPreset === preset 
                  ? 'rgba(214, 158, 46, 0.25)' 
                  : 'rgba(45, 90, 135, 0.2)',
                border: `1px solid ${selectedPreset === preset 
                  ? 'rgba(214, 158, 46, 0.5)' 
                  : 'rgba(66, 153, 225, 0.2)'}`,
                color: selectedPreset === preset ? '#f6ad55' : '#94a3b8',
              }}
            >
              {preset === 'H2' ? 'H₂' : 
               preset === 'H2O' ? 'H₂O' :
               preset === 'CH4' ? 'CH₄' :
               preset === 'CO2' ? 'CO₂' : preset}
            </button>
          ))}
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
            {moleculeData.moleculeName}
          </div>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between items-center">
              <span style={{ color: '#94a3b8' }}>Atoms:</span>
              <span className="font-mono" style={{ color: '#e2e8f0' }}>
                {moleculeData.atomCount}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span style={{ color: '#94a3b8' }}>Bonds:</span>
              <span className="font-mono" style={{ color: '#e2e8f0' }}>
                {moleculeData.bondCount}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span style={{ color: '#94a3b8' }}>Total Energy:</span>
              <span className="font-mono" style={{ color: '#ecc94b' }}>
                {formatEnergy(moleculeData.totalEnergy)}
              </span>
            </div>
            <div 
              className="mt-3 pt-3 text-xs"
              style={{ 
                borderTop: '1px solid rgba(148, 163, 184, 0.2)',
              }}
            >
              <div style={{ color: '#cbd5e0' }}>Pressure Field Overlap</div>
              <div style={{ color: '#94a3b8' }}>No quantum orbitals needed</div>
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
          <div className="mb-2" style={{ color: '#f6ad55' }}>
            E<sub>bond</sub> ∝ (R₁² × R₂²) / r²
          </div>
          <div className="mb-2" style={{ color: '#ecc94b' }}>
            Overlap = (R₁ + R₂ - r) / (R₁ + R₂)
          </div>
          <div 
            className="pt-2 text-[10px]"
            style={{ 
              borderTop: '1px solid rgba(148, 163, 184, 0.2)',
              color: '#94a3b8' 
            }}
          >
            Bond from Pressure Field Exclusion
          </div>
        </div>
      )}

      {/* Legend - bottom right */}
      <div 
        className="absolute bottom-4 right-4 p-3 rounded-xl text-[10px]"
        style={{
          background: 'rgba(10, 14, 26, 0.85)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(148, 163, 184, 0.1)',
        }}
      >
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <div 
              className="w-3 h-3 rounded-full"
              style={{ background: '#ecc94b', boxShadow: '0 0 8px rgba(236, 201, 75, 0.5)' }}
            />
            <span style={{ color: '#cbd5e0' }}>Strong bond</span>
          </div>
          <div className="flex items-center gap-2">
            <div 
              className="w-3 h-3 rounded-full"
              style={{ background: '#d69e2e' }}
            />
            <span style={{ color: '#cbd5e0' }}>Medium bond</span>
          </div>
          <div className="flex items-center gap-2">
            <div 
              className="w-3 h-3 rounded-full"
              style={{ background: '#4299e1', opacity: 0.3 }}
            />
            <span style={{ color: '#94a3b8' }}>Pressure field</span>
          </div>
        </div>
      </div>
    </div>
  );
};
