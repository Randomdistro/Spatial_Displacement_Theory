/**
 * SDT Simulations Index
 * 
 * All interactive 3D simulations demonstrating SDT principles.
 * SDT-ACCURATE: No mass, no G, no QED - pure pressure geometry.
 */

export { default as PressureFieldSim } from './PressureFieldSim';
export { default as ToroidalElectronSim } from './ToroidalElectronSim';
export { default as GalaxyRotationSim } from './GalaxyRotationSim';
export { default as KLawScaleSim } from './KLawScaleSim';
export { default as SpationLatticeSim } from './SpationLatticeSim';
export { default as ForceHierarchySim } from './ForceHierarchySim';
export { default as CMBBoundarySim } from './CMBBoundarySim';

// Simulation registry for dynamic loading
export const SIMULATION_REGISTRY = {
  'pressure-field': {
    component: 'PressureFieldSim',
    name: 'Pressure Field (Master Equation)',
    description: 'Full Master Equation visualization with directional occlusion',
    path: ['path1', 'path2', 'path3'],
  },
  'spation-lattice': {
    component: 'SpationLatticeSim',
    name: 'Spation Lattice',
    description: 'Dodecahedral packing at Planck scale - the fundamental medium',
    path: ['path2', 'path3'],
  },
  'force-hierarchy': {
    component: 'ForceHierarchySim',
    name: 'Force Hierarchy (Coulomb = Gravity)',
    description: 'Same force, different occlusion regimes - from E=0 to E=1',
    path: ['path1', 'path2', 'path3'],
  },
  'cmb-boundary': {
    component: 'CMBBoundarySim',
    name: 'CMB Boundary (Origin of All Pressure)',
    description: 'The cosmic microwave background as structural boundary',
    path: ['path1', 'path2', 'path3'],
  },
  'toroidal-electron': {
    component: 'ToroidalElectronSim',
    name: 'Toroidal Electron Model',
    description: 'Electron as extended toroidal vortex with helical standing waves',
    path: ['path2', 'path3'],
  },
  'galaxy-rotation': {
    component: 'GalaxyRotationSim',
    name: 'Galaxy Rotation (No Dark Matter)',
    description: 'Eclipse effect produces flat rotation curves without dark matter',
    path: ['path1', 'path2'],
  },
  'k-law-scale-slider': {
    component: 'KLawScaleSim',
    name: 'Universal k-Law',
    description: 'Same velocity law from atoms to galaxies with different k values',
    path: ['path1', 'path2', 'path3'],
  },
} as const;

export type SimulationId = keyof typeof SIMULATION_REGISTRY;

