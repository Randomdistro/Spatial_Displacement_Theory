/**
 * Simulations Module
 * Agent 3: Physics/Simulation
 * 
 * Exports all simulation components
 */

export { SimulationBase, type SimulationProps, type SimulationState } from './SimulationBase';
export { PressureFieldSim, type PressureFieldSimProps } from './PressureFieldSim';
export { OrbitalSim, type OrbitalSimProps } from './OrbitalSim';
export { AtomicStructureSim, type AtomicStructureSimProps } from './AtomicStructureSim';
export { GalaxyRotationSim, type GalaxyRotationSimProps } from './GalaxyRotationSim';
export { BenchmarkVisualizer, type BenchmarkVisualizerProps, type BenchmarkData } from './BenchmarkVisualizer';
export { 
  FormulaRenderer, 
  AnimatedFormula,
  MasterEquation,
  KLawFormula,
  type FormulaRendererProps,
  type AnimatedFormulaProps,
} from './FormulaRenderer';

