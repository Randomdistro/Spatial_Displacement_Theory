/**
 * Codemonkey Agent: Framework Core
 * 
 * Main entry point for framework systems
 * TEKNE: Framework architecture IS the theory's structure
 */

export * from './geometry/GeometryGenerator';
export * from './shader/ShaderRegistry';
export * from './animation/AnimationChoreographer';
export * from './performance/PerformanceMonitor';
export * from './spatial/SpatialNavigation';
export * from './errors/ErrorBoundary';
export * from './hooks';

// Re-export for convenience
export { geometryRegistry } from './geometry/GeometryGenerator';
export { shaderRegistry } from './shader/ShaderRegistry';
export { performanceMonitor } from './performance/PerformanceMonitor';

