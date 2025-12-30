/**
 * Chemical Bonding Simulation
 * Agent 3: Physics/Simulation
 *
 * Visualizes chemical bonding as pressure field overlap between atoms
 * Shows how bonds form, bond energy, and molecular geometry prediction
 */

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { SimulationBase, SimulationProps } from './SimulationBase';

interface AtomConfig {
  element: string;
  position: [number, number, number];
  radius: number; // Exclusion zone radius
  atomicNumber: number;
}

interface ChemicalBondingSimProps extends SimulationProps {
  parameters: {
    atoms?: AtomConfig[];        // Array of atom configurations
    showPressureFields?: boolean; // Show pressure exclusion zones (default: true)
    showBonds?: boolean;          // Show bonds between atoms (default: true)
    showEnergy?: boolean;         // Show bond energy display (default: true)
    showGeometry?: boolean;       // Show molecular geometry (default: true)
    interactive?: boolean;        // Allow dragging atoms (default: false)
  };
}

// Element data (simplified - full implementation would use periodic table)
const ELEMENT_DATA: Record<string, { radius: number; color: number; atomicNumber: number }> = {
  H: { radius: 5.29177e-11, color: 0xffffff, atomicNumber: 1 },
  He: { radius: 3.1e-11, color: 0xd9ffff, atomicNumber: 2 },
  Li: { radius: 1.67e-10, color: 0xcc80ff, atomicNumber: 3 },
  C: { radius: 7.0e-11, color: 0x909090, atomicNumber: 6 },
  N: { radius: 6.5e-11, color: 0x3050f8, atomicNumber: 7 },
  O: { radius: 6.0e-11, color: 0xff0d0d, atomicNumber: 8 },
};

class ChemicalBondingSimulation extends SimulationBase {
  private atoms: THREE.Mesh[] = [];
  private pressureFields: THREE.Mesh[] = [];
  private bonds: THREE.CylinderGeometry[] = [];
  private bondMeshes: THREE.Mesh[] = [];
  private overlapRegions: THREE.Mesh[] = [];
  private energyDisplay: THREE.Group | null = null;

  // Atom configurations
  private atomConfigs: AtomConfig[] = [];

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
    const atoms = this.parameters.atoms ?? this.getDefaultAtoms();
    const showPressure = this.parameters.showPressureFields ?? true;
    const showBonds = this.parameters.showBonds ?? true;
    const showEnergy = this.parameters.showEnergy ?? true;
    const showGeometry = this.parameters.showGeometry ?? true;

    this.atomConfigs = atoms;

    // Scale factor for visualization (atomic → visible)
    const scaleFactor = 1e10;

    // Create atoms and pressure fields
    atoms.forEach((atomConfig, index) => {
      const elementData = ELEMENT_DATA[atomConfig.element] || ELEMENT_DATA.H;
      const radius_scaled = atomConfig.radius * scaleFactor;

      // Create atom sphere (nucleus)
      const atomGeometry = new THREE.SphereGeometry(radius_scaled * 0.1, 16, 16);
      // STYLING PLACEHOLDER: Atom material
      // Creative Agent: Use element-specific colors
      // Subtle emissive glow, metallic sheen
      const atomMaterial = new THREE.MeshStandardMaterial({
        color: elementData.color,
        metalness: 0.7,
        roughness: 0.3,
        emissive: elementData.color,
        emissiveIntensity: 0.2
      });
      const atom = new THREE.Mesh(atomGeometry, atomMaterial);
      atom.position.set(...atomConfig.position.map(p => p * scaleFactor));
      atom.userData = { element: atomConfig.element, index };
      this.scene.add(atom);
      this.atoms.push(atom);

      // Create pressure exclusion zone
      if (showPressure) {
        const fieldGeometry = new THREE.SphereGeometry(radius_scaled, 32, 32);
        // STYLING PLACEHOLDER: Pressure field material
        // Creative Agent: Translucent sphere showing exclusion zone
        // Color: Use --color-space-medium with low opacity
        // Wireframe or solid? Subtle glow?
        const fieldMaterial = new THREE.MeshStandardMaterial({
          color: 0x2d5a87, // PLACEHOLDER: Use --color-space-medium
          transparent: true,
          opacity: 0.2, // PLACEHOLDER: Adjust for visibility
          side: THREE.DoubleSide,
          wireframe: false // PLACEHOLDER: Wireframe or solid?
        });
        const pressureField = new THREE.Mesh(fieldGeometry, fieldMaterial);
        pressureField.position.copy(atom.position);
        this.scene.add(pressureField);
        this.pressureFields.push(pressureField);
      }
    });

    // Calculate and visualize bonds
    if (showBonds) {
      this.calculateBonds(scaleFactor);
    }

    // Calculate overlap regions
    if (showPressure) {
      this.calculateOverlapRegions(scaleFactor);
    }

    // Display bond energies
    if (showEnergy) {
      this.createEnergyDisplay(scaleFactor);
    }

    // Show molecular geometry
    if (showGeometry) {
      this.visualizeMolecularGeometry(scaleFactor);
    }

    // Position camera
    const maxDistance = Math.max(...atoms.map(a => {
      const dist = Math.sqrt(a.position[0]**2 + a.position[1]**2 + a.position[2]**2);
      return dist * scaleFactor;
    }));
    this.camera.position.set(0, maxDistance * 0.7, maxDistance * 1.2);
    this.camera.lookAt(0, 0, 0);
  }

  private getDefaultAtoms(): AtomConfig[] {
    // Default: Two hydrogen atoms
    return [
      {
        element: 'H',
        position: [-1e-10, 0, 0],
        radius: 5.29177e-11,
        atomicNumber: 1
      },
      {
        element: 'H',
        position: [1e-10, 0, 0],
        radius: 5.29177e-11,
        atomicNumber: 1
      }
    ];
  }

  private calculateBonds(scaleFactor: number): void {
    // Find pairs of atoms that are close enough to bond
    const bondDistance = 2e-10; // Typical bond distance
    const bondDistance_scaled = bondDistance * scaleFactor;

    for (let i = 0; i < this.atoms.length; i++) {
      for (let j = i + 1; j < this.atoms.length; j++) {
        const atom1 = this.atoms[i];
        const atom2 = this.atoms[j];
        const distance = atom1.position.distanceTo(atom2.position);

        if (distance < bondDistance_scaled * 1.5) {
          // Create bond (cylinder between atoms)
          const bondLength = distance;
          const bondGeometry = new THREE.CylinderGeometry(
            bondLength * 0.02, // Radius
            bondLength * 0.02,
            bondLength,
            8
          );
          
          // Position and orient cylinder
          const midpoint = new THREE.Vector3()
            .addVectors(atom1.position, atom2.position)
            .multiplyScalar(0.5);
          const direction = new THREE.Vector3()
            .subVectors(atom2.position, atom1.position)
            .normalize();

          // STYLING PLACEHOLDER: Bond material
          // Creative Agent: Gold color for bonds
          // Represents pressure field overlap
          // Thickness and glow based on bond strength
          const bondMaterial = new THREE.MeshStandardMaterial({
            color: 0xd69e2e, // PLACEHOLDER: Use --color-gold-primary
            emissive: 0xd69e2e,
            emissiveIntensity: 0.3, // PLACEHOLDER: Adjust based on bond strength
            metalness: 0.8,
            roughness: 0.2
          });

          const bondMesh = new THREE.Mesh(bondGeometry, bondMaterial);
          bondMesh.position.copy(midpoint);
          bondMesh.lookAt(atom2.position);
          bondMesh.rotateX(Math.PI / 2); // Align with bond direction
          
          this.scene.add(bondMesh);
          this.bondMeshes.push(bondMesh);
          this.bonds.push(bondGeometry);

          // Calculate bond energy
          const bondEnergy = this.calculateBondEnergy(atom1, atom2, distance / scaleFactor);
          bondMesh.userData = { energy: bondEnergy, atom1: i, atom2: j };
        }
      }
    }
  }

  private calculateBondEnergy(atom1: THREE.Mesh, atom2: THREE.Mesh, distance: number): number {
    // Simplified bond energy calculation
    // Full SDT implementation would calculate pressure field overlap
    const element1 = atom1.userData.element;
    const element2 = atom2.userData.element;
    const elementData1 = ELEMENT_DATA[element1] || ELEMENT_DATA.H;
    const elementData2 = ELEMENT_DATA[element2] || ELEMENT_DATA.H;

    // Bond energy from pressure field overlap
    // Simplified: E_bond ∝ (R1²R2²)/r²
    const R1 = elementData1.radius;
    const R2 = elementData2.radius;
    const overlap = (R1 * R1 * R2 * R2) / (distance * distance);
    
    // Convert to eV (simplified conversion)
    return overlap * 1e-19; // Placeholder conversion factor
  }

  private calculateOverlapRegions(scaleFactor: number): void {
    // STYLING PLACEHOLDER: Overlap region visualization
    // Creative Agent: Highlight regions where pressure fields overlap
    // Color: Gold gradient, represents bond formation
    // Show as semi-transparent mesh or particle cloud
    // This is a placeholder - full implementation would:
    // 1. Calculate intersection of pressure exclusion zones
    // 2. Visualize overlap volume
    // 3. Show pressure gradient in overlap region
  }

  private createEnergyDisplay(scaleFactor: number): void {
    // STYLING PLACEHOLDER: Energy display
    // Creative Agent: Show bond energies as text or bars
    // Position: Near bonds or in UI overlay
    // Format: Energy in eV or kJ/mol
    // Color: Match bond strength (weaker = blue, stronger = gold)
  }

  private visualizeMolecularGeometry(scaleFactor: number): void {
    // STYLING PLACEHOLDER: Molecular geometry visualization
    // Creative Agent: Show predicted molecular structure
    // VSEPR-like geometry from pressure field
    // Show bond angles, molecular shape
    // Use wireframe or guide lines
  }

  update(deltaTime: number): void {
    this.time += deltaTime;

    // STYLING PLACEHOLDER: Idle animations
    // Creative Agent: Subtle atom vibrations
    // Pressure field breathing/pulsing
    // Bond energy fluctuations
    // Organic, flowing motion

    // Subtle atom rotation/vibration
    this.atoms.forEach((atom, index) => {
      const vibration = Math.sin(this.time * 2 + index) * 0.001;
      atom.position.x += vibration;
      atom.position.y += vibration * 0.5;
    });

    // Update bond visualization if atoms moved
    // (Would need to recalculate bonds if interactive)
  }

  protected onParametersChanged(): void {
    this.init();
  }

  dispose(): void {
    this.atoms.forEach(atom => this.disposeObject(atom));
    this.pressureFields.forEach(field => this.disposeObject(field));
    this.bondMeshes.forEach(bond => this.disposeObject(bond));
    this.overlapRegions.forEach(region => this.disposeObject(region));
    this.disposeObject(this.energyDisplay);

    this.atoms = [];
    this.pressureFields = [];
    this.bonds = [];
    this.bondMeshes = [];
    this.overlapRegions = [];
    this.energyDisplay = null;
  }

  private disposeObject(object: THREE.Object3D | null): void {
    if (!object) return;

    object.traverse((child) => {
      if (child instanceof THREE.Mesh) {
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
  const [bondData, setBondData] = useState({
    bondCount: 0,
    totalEnergy: 0,
    molecules: [] as Array<{ atoms: string[]; energy: number }>,
  });

  useEffect(() => {
    if (!containerRef.current) return;

    const sim = new ChemicalBondingSimulation(containerRef.current);
    sim.setParameters({
      atoms: undefined, // Use defaults
      showPressureFields: true,
      showBonds: true,
      showEnergy: true,
      showGeometry: true,
      interactive: false,
      ...parameters,
    });
    sim.init();
    simulationRef.current = sim;

    // Calculate bond data
    const atoms = parameters.atoms ?? [
      {
        element: 'H',
        position: [-1e-10, 0, 0],
        radius: 5.29177e-11,
        atomicNumber: 1
      },
      {
        element: 'H',
        position: [1e-10, 0, 0],
        radius: 5.29177e-11,
        atomicNumber: 1
      }
    ];
    const bondCount = Math.floor((atoms.length * (atoms.length - 1)) / 2);
    
    setBondData({
      bondCount,
      totalEnergy: 0, // Would calculate from bonds
      molecules: [],
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
      <div
        ref={containerRef}
        className="w-full h-full min-h-[500px] bg-slate-900 rounded-lg"
        style={{ touchAction: 'none' }}
      />

      {/* STYLING PLACEHOLDER: Labels panel */}
      {showLabels && (
        <div className="absolute bottom-4 left-4 bg-black/70 backdrop-blur-sm text-white p-4 rounded-lg text-sm max-w-xs">
          <div className="font-semibold mb-3 text-amber-400">Chemical Bonding</div>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Atoms:</span>
              <span className="font-mono">{(parameters.atoms?.length ?? 2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Bonds:</span>
              <span className="font-mono">{bondData.bondCount}</span>
            </div>
            <div className="mt-3 pt-3 border-t border-slate-600 text-slate-300">
              <div className="text-xs">Pressure Field Overlap</div>
              <div className="text-xs text-slate-400">No quantum orbitals</div>
            </div>
          </div>
        </div>
      )}

      {/* STYLING PLACEHOLDER: Formula overlay */}
      {showFormulas && (
        <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm text-white p-3 rounded-lg text-xs font-mono">
          <div>E_bond ∝ (R₁²R₂²)/r²</div>
          <div className="mt-2 text-slate-400 text-[10px]">
            Bond Energy from Pressure Overlap
          </div>
        </div>
      )}

      {/* STYLING PLACEHOLDER: Atom placement controls */}
      {/* Creative Agent: Add UI for placing atoms, selecting elements */}
      {/* Position: Top-left or side panel */}
      {/* Style: Match existing control panels */}
    </div>
  );
};

