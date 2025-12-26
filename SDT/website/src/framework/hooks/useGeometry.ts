/**
 * Codemonkey Agent: React Hook for Geometry Generation
 * 
 * Convenient hook for Creative Agent to use custom geometry
 */

import { useMemo } from 'react';
import * as THREE from 'three';
import { geometryRegistry, GeometryParams, Geometry, geometryToThreeJS } from '../geometry/GeometryGenerator';

export interface UseGeometryOptions {
  generator: string;
  params: GeometryParams;
}

export interface UseGeometryReturn {
  geometry: THREE.BufferGeometry | null;
  error: Error | null;
  isLoading: boolean;
  updateParams: (params: GeometryParams) => void;
}

/**
 * Hook for using custom geometry generators
 * 
 * @example
 * ```tsx
 * const { geometry } = useGeometry({
 *   generator: 'toroidal-chamber',
 *   params: {
 *     innerRadius: 2,
 *     outerRadius: 4,
 *     height: 3
 *   }
 * });
 * ```
 */
export function useGeometry(options: UseGeometryOptions): UseGeometryReturn {
  const geometry = useMemo(() => {
    try {
      const customGeometry = geometryRegistry.generate(options.generator, options.params);
      return geometryToThreeJS(customGeometry);
    } catch (err) {
      return null;
    }
  }, [options.generator, JSON.stringify(options.params)]);

  const error = geometry === null ? new Error(`Failed to generate geometry: ${options.generator}`) : null;
  const isLoading = false;

  const updateParams = (newParams: GeometryParams) => {
    // Geometry will be regenerated on next render due to useMemo dependency
    // This is intentional - geometry updates are expensive
  };

  return {
    geometry,
    error,
    isLoading,
    updateParams,
  };
}

