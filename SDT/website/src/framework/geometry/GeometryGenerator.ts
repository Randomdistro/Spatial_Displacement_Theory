/**
 * Codemonkey Agent: Custom Geometry Generator System
 * 
 * All original geometry generation - no Three.js dependencies for core shapes
 * Supports Creative Agent's custom geometry requirements
 */

import * as THREE from 'three';

export interface GeometryParams {
  [key: string]: number | string | boolean;
}

export interface Geometry {
  vertices: Float32Array;
  normals: Float32Array;
  uvs: Float32Array;
  indices: Uint16Array;
  vertexCount: number;
  faceCount: number;
}

/**
 * Base interface for geometry generators
 * All generators must implement this
 */
export interface GeometryGenerator {
  generate(params: GeometryParams): Geometry;
  update(geometry: Geometry, params: GeometryParams): void;
  dispose(geometry: Geometry): void;
}

/**
 * Geometry Registry
 * Manages all custom geometry generators
 */
export class GeometryRegistry {
  private generators: Map<string, GeometryGenerator> = new Map();
  private cache: Map<string, Geometry> = new Map();

  /**
   * Register a geometry generator
   */
  register(name: string, generator: GeometryGenerator): void {
    this.generators.set(name, generator);
  }

  /**
   * Generate geometry by name
   */
  generate(name: string, params: GeometryParams): Geometry {
    const cacheKey = `${name}-${JSON.stringify(params)}`;
    
    // Check cache
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey)!;
    }

    const generator = this.generators.get(name);
    if (!generator) {
      throw new Error(`Geometry generator "${name}" not found`);
    }

    const geometry = generator.generate(params);
    this.cache.set(cacheKey, geometry);
    return geometry;
  }

  /**
   * Update existing geometry
   */
  update(name: string, geometry: Geometry, params: GeometryParams): void {
    const generator = this.generators.get(name);
    if (!generator) {
      throw new Error(`Geometry generator "${name}" not found`);
    }
    generator.update(geometry, params);
  }

  /**
   * Dispose of geometry
   */
  dispose(name: string, geometry: Geometry): void {
    const generator = this.generators.get(name);
    if (generator) {
      generator.dispose(geometry);
    }
  }

  /**
   * Clear cache
   */
  clearCache(): void {
    this.cache.clear();
  }
}

/**
 * Toroidal Chamber Generator
 * Creates a toroidal (donut-shaped) chamber geometry
 * All original implementation - no Three.js TorusGeometry dependency
 */
export class ToroidalChamberGenerator implements GeometryGenerator {
  generate(params: GeometryParams): Geometry {
    const innerRadius = (params.innerRadius as number) || 2;
    const outerRadius = (params.outerRadius as number) || 4;
    const height = (params.height as number) || 3;
    const radialSegments = (params.radialSegments as number) || 32;
    const tubularSegments = (params.tubularSegments as number) || 64;

    const vertices: number[] = [];
    const normals: number[] = [];
    const uvs: number[] = [];
    const indices: number[] = [];

    // Generate vertices using parametric equations
    for (let i = 0; i <= radialSegments; i++) {
      const v = i / radialSegments;
      const angle = v * Math.PI * 2;

      for (let j = 0; j <= tubularSegments; j++) {
        const u = j / tubularSegments;
        const torusAngle = u * Math.PI * 2;

        // Parametric equations for torus
        const x = (outerRadius + innerRadius * Math.cos(torusAngle)) * Math.cos(angle);
        const y = innerRadius * Math.sin(torusAngle) + (v - 0.5) * height;
        const z = (outerRadius + innerRadius * Math.cos(torusAngle)) * Math.sin(angle);

        vertices.push(x, y, z);

        // Calculate normal
        const nx = Math.cos(torusAngle) * Math.cos(angle);
        const ny = Math.sin(torusAngle);
        const nz = Math.cos(torusAngle) * Math.sin(angle);
        normals.push(nx, ny, nz);

        // UV coordinates
        uvs.push(u, v);
      }
    }

    // Generate faces
    for (let i = 0; i < radialSegments; i++) {
      for (let j = 0; j < tubularSegments; j++) {
        const a = i * (tubularSegments + 1) + j;
        const b = a + tubularSegments + 1;

        // Two triangles per quad
        indices.push(a, b, a + 1);
        indices.push(b, b + 1, a + 1);
      }
    }

    return {
      vertices: new Float32Array(vertices),
      normals: new Float32Array(normals),
      uvs: new Float32Array(uvs),
      indices: new Uint16Array(indices),
      vertexCount: vertices.length / 3,
      faceCount: indices.length / 3,
    };
  }

  update(geometry: Geometry, params: GeometryParams): void {
    // For now, regenerate (could optimize later)
    const newGeometry = this.generate(params);
    geometry.vertices = newGeometry.vertices;
    geometry.normals = newGeometry.normals;
    geometry.uvs = newGeometry.uvs;
    geometry.indices = newGeometry.indices;
    geometry.vertexCount = newGeometry.vertexCount;
    geometry.faceCount = newGeometry.faceCount;
  }

  dispose(geometry: Geometry): void {
    // Cleanup if needed
  }
}

/**
 * Convert custom Geometry to Three.js BufferGeometry
 * Utility function for integration with Three.js
 */
export function geometryToThreeJS(geometry: Geometry): THREE.BufferGeometry {
  const threeGeometry = new THREE.BufferGeometry();
  
  threeGeometry.setAttribute('position', new THREE.BufferAttribute(geometry.vertices, 3));
  threeGeometry.setAttribute('normal', new THREE.BufferAttribute(geometry.normals, 3));
  threeGeometry.setAttribute('uv', new THREE.BufferAttribute(geometry.uvs, 2));
  threeGeometry.setIndex(new THREE.BufferAttribute(geometry.indices, 1));
  
  threeGeometry.computeBoundingBox();
  threeGeometry.computeBoundingSphere();
  
  return threeGeometry;
}

// Global registry instance
export const geometryRegistry = new GeometryRegistry();

// Register default generators
geometryRegistry.register('toroidal-chamber', new ToroidalChamberGenerator());

