/**
 * Dodecahedron Geometry Generator
 * Creates dodecahedral unit cells for spation lattice visualization
 * All original implementation - no Three.js dependencies
 */

import { GeometryGenerator, GeometryParams, Geometry } from './GeometryGenerator';

/**
 * Dodecahedron Generator
 * Creates a regular dodecahedron (12 pentagonal faces, 20 vertices)
 * Used for spation lattice unit cell visualization
 */
export class DodecahedronGenerator implements GeometryGenerator {
  generate(params: GeometryParams): Geometry {
    const radius = (params.radius as number) || 1.0;
    const detail = Math.max(0, Math.floor((params.detail as number) || 0));

    const vertices: number[] = [];
    const normals: number[] = [];
    const uvs: number[] = [];
    const indices: number[] = [];

    // Golden ratio constant
    const phi = (1 + Math.sqrt(5)) / 2;

    // Dodecahedron vertices (20 vertices)
    // Coordinates of a regular dodecahedron centered at origin
    const dodecahedronVertices = [
      // (±1, ±1, ±1) permutations
      [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
      [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
      // (0, ±1/φ, ±φ) permutations
      [0, 1/phi, phi], [0, 1/phi, -phi], [0, -1/phi, phi], [0, -1/phi, -phi],
      // (±1/φ, ±φ, 0) permutations
      [1/phi, phi, 0], [1/phi, -phi, 0], [-1/phi, phi, 0], [-1/phi, -phi, 0],
      // (±φ, 0, ±1/φ) permutations
      [phi, 0, 1/phi], [phi, 0, -1/phi], [-phi, 0, 1/phi], [-phi, 0, -1/phi],
    ];

    // Normalize and scale vertices
    const normalizedVertices = dodecahedronVertices.map(v => {
      const length = Math.sqrt(v[0]**2 + v[1]**2 + v[2]**2);
      return [
        (v[0] / length) * radius,
        (v[1] / length) * radius,
        (v[2] / length) * radius,
      ];
    });

    // Dodecahedron faces (12 pentagonal faces)
    // Each face is defined by 5 vertices
    const faces = [
      [0, 8, 10, 2, 16],    // Face 1
      [0, 16, 18, 1, 12],   // Face 2
      [0, 12, 14, 4, 8],    // Face 3
      [1, 9, 11, 3, 17],    // Face 4
      [1, 17, 19, 5, 13],   // Face 5
      [1, 13, 15, 4, 12],   // Face 6
      [2, 10, 11, 3, 19],   // Face 7
      [2, 19, 18, 0, 16],   // Face 8
      [3, 11, 9, 1, 17],    // Face 9
      [4, 14, 15, 5, 13],   // Face 10
      [5, 15, 14, 12, 13],  // Face 11
      [6, 7, 19, 2, 10],    // Face 12
    ];

    // Generate vertices, normals, and UVs for each face
    let vertexIndex = 0;
    const vertexMap = new Map<string, number>();

    faces.forEach((face, faceIndex) => {
      const faceVertices = face.map(i => normalizedVertices[i]);
      
      // Calculate face normal (average of vertex positions)
      const center = [0, 0, 0];
      faceVertices.forEach(v => {
        center[0] += v[0];
        center[1] += v[1];
        center[2] += v[2];
      });
      center[0] /= faceVertices.length;
      center[1] /= faceVertices.length;
      center[2] /= faceVertices.length;

      const normal = [
        center[0] / radius,
        center[1] / radius,
        center[2] / radius,
      ];
      const normalLength = Math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2);
      normal[0] /= normalLength;
      normal[1] /= normalLength;
      normal[2] /= normalLength;

      // Add vertices for this face
      const faceIndices: number[] = [];
      faceVertices.forEach((v, i) => {
        const key = `${v[0]},${v[1]},${v[2]}`;
        let idx = vertexMap.get(key);
        
        if (idx === undefined) {
          idx = vertexIndex++;
          vertexMap.set(key, idx);
          vertices.push(v[0], v[1], v[2]);
          normals.push(normal[0], normal[1], normal[2]);
          
          // UV coordinates (simple mapping)
          const u = i / faceVertices.length;
          const v_uv = faceIndex / faces.length;
          uvs.push(u, v_uv);
        }
        
        faceIndices.push(idx);
      });

      // Triangulate pentagon (fan triangulation from first vertex)
      for (let i = 1; i < faceIndices.length - 1; i++) {
        indices.push(faceIndices[0], faceIndices[i], faceIndices[i + 1]);
      }
    });

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

