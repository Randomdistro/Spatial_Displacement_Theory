/**
 * Architect Designer Agent: Simulation Viewer Component
 * Displays simulations in expansion points with proper error handling
 */

import React from 'react';
import {
  PressureFieldSim,
  OrbitalSim,
  AtomicStructureSim,
  GalaxyRotationSim,
  BenchmarkVisualizer,
  TheClearingSim,
  SpationLatticeSim,
  ForceHierarchySim,
  ChemicalBondingSim,
} from '../simulations';

interface SimulationViewerProps {
  simulationId: string;
  parameters?: Record<string, any>;
  showFormulas?: boolean;
  showLabels?: boolean;
  narrationEnabled?: boolean;
}

export default function SimulationViewer({
  simulationId,
  parameters = {},
  showFormulas = true,
  showLabels = true,
  narrationEnabled = false,
}: SimulationViewerProps) {
  // Map simulation IDs to components
  const renderSimulation = () => {
    switch (simulationId) {
      case 'pressure-field':
        return (
          <PressureFieldSim
            id="pressure-field"
            parameters={{
              density: parameters.density || 5.2e96,
              bulkModulus: parameters.bulkModulus || 4.6e113,
              matterRadius: parameters.matterRadius || 1.0,
              fieldResolution: parameters.fieldResolution || 20,
            }}
            showFormulas={showFormulas}
            showLabels={showLabels}
            narrationEnabled={narrationEnabled}
          />
        );

      case 'orbital-mechanics':
      case 'orbital':
        return (
          <OrbitalSim
            id="orbital-mechanics"
            parameters={{
              centralMass: parameters.centralMass || 1.989e30,
              orbitalRadius: parameters.orbitalRadius || 1.496e11,
              kValue: parameters.kValue || 1.0,
              ...parameters,
            }}
            showFormulas={showFormulas}
            showLabels={showLabels}
            narrationEnabled={narrationEnabled}
          />
        );

      case 'atomic-structure':
      case 'atomic':
        return (
          <AtomicStructureSim
            id="atomic-structure"
            parameters={{
              element: parameters.element || 'H',
              showElectron: parameters.showElectron !== false,
              showNucleus: parameters.showNucleus !== false,
              ...parameters,
            }}
            showFormulas={showFormulas}
            showLabels={showLabels}
            narrationEnabled={narrationEnabled}
          />
        );

      case 'galaxy-rotation':
      case 'galaxy':
        return (
          <GalaxyRotationSim
            id="galaxy-rotation"
            parameters={{
              stellarMass: parameters.stellarMass || 1e10,
              orbitalRadius: parameters.orbitalRadius || 1e20,
              ...parameters,
            }}
            showFormulas={showFormulas}
            showLabels={showLabels}
            narrationEnabled={narrationEnabled}
          />
        );

      case 'the-clearing':
      case 'let-there-be-light':
      case 'recombination':
        return (
          <TheClearingSim
            id="the-clearing"
            parameters={{
              temperature: parameters.temperature || 10000,
              opacity: parameters.opacity || 0.8,
              particleCount: parameters.particleCount || 2000,
              transitionSpeed: parameters.transitionSpeed || 0.5,
              showPressureFields: parameters.showPressureFields !== false,
            }}
            showFormulas={showFormulas}
            showLabels={showLabels}
            narrationEnabled={narrationEnabled}
          />
        );

      case 'spation-lattice':
      case 'lattice':
        return (
          <SpationLatticeSim
            id="spation-lattice"
            parameters={{
              scale: parameters.scale || -35,
              showPressure: parameters.showPressure !== false,
              showDeformation: parameters.showDeformation || false,
              latticeResolution: parameters.latticeResolution || 5,
              zoomLevel: parameters.zoomLevel || 0,
              showUnitCells: parameters.showUnitCells !== false,
            }}
            showFormulas={showFormulas}
            showLabels={showLabels}
            narrationEnabled={narrationEnabled}
          />
        );

      case 'force-hierarchy':
      case 'force-unification':
        return (
          <ForceHierarchySim
            id="force-hierarchy"
            parameters={{
              object1Radius: parameters.object1Radius || 5.29177e-11,
              object2Radius: parameters.object2Radius || 5.29177e-11,
              separation: parameters.separation || 1e-10,
              occlusionE: parameters.occlusionE || 0.5,
              showCMBSource: parameters.showCMBSource !== false,
              compareForces: parameters.compareForces !== false,
              showPressureField: parameters.showPressureField !== false,
            }}
            showFormulas={showFormulas}
            showLabels={showLabels}
            narrationEnabled={narrationEnabled}
          />
        );

      case 'chemical-bonding':
      case 'bonding':
        return (
          <ChemicalBondingSim
            id="chemical-bonding"
            parameters={{
              atoms: parameters.atoms,
              showPressureFields: parameters.showPressureFields !== false,
              showBonds: parameters.showBonds !== false,
              showEnergy: parameters.showEnergy !== false,
              showGeometry: parameters.showGeometry !== false,
              interactive: parameters.interactive || false,
            }}
            showFormulas={showFormulas}
            showLabels={showLabels}
            narrationEnabled={narrationEnabled}
          />
        );

      case 'cmb-boundary':
      case 'cmb':
        // STYLING PLACEHOLDER: CMBBoundarySim integration
        // Creative Agent: CMBBoundarySim (LET THERE BE LIGHT!) is already complete
        // Import and integrate when available
        return (
          <div className="text-center py-12 text-slate-400">
            <p className="mb-2">CMB Boundary Simulation</p>
            <p className="text-sm">LET THERE BE LIGHT! - Already complete</p>
            <p className="text-xs mt-2">Integration pending</p>
          </div>
        );

      case 'benchmark-visualizer':
      case 'benchmark':
        return (
          <BenchmarkVisualizer
            id="benchmark-visualizer"
            parameters={parameters}
            showFormulas={showFormulas}
            showLabels={showLabels}
            narrationEnabled={narrationEnabled}
          />
        );

      default:
        return (
          <div className="text-center py-12 text-slate-400">
            <p className="mb-2">Simulation: {simulationId}</p>
            <p className="text-sm">This simulation is being prepared.</p>
            <p className="text-xs mt-2">Available simulations:</p>
            <ul className="text-xs mt-1 space-y-1 text-slate-500">
              <li>pressure-field, orbital-mechanics, atomic-structure</li>
              <li>galaxy-rotation, the-clearing, spation-lattice</li>
              <li>force-hierarchy, chemical-bonding, benchmark-visualizer</li>
            </ul>
          </div>
        );
    }
  };

  return (
    <div className="w-full">
      {renderSimulation()}
    </div>
  );
}
