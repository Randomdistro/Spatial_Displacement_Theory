/**
 * Creative Agent: Sacred Geometry Utilities
 * 
 * TEKNE: Mathematics IS beauty, beauty IS mathematics
 * 
 * The precision of geometry at the forefront:
 * - Golden Ratio (φ = 1.618033988749895)
 * - Fibonacci Sequence (1, 1, 2, 3, 5, 8, 13, 21, 34, 55...)
 * - Sacred Proportions (√2, √3, √5)
 * - Platonic Solids vertices
 * - Flower of Life coordinates
 * 
 * All original implementations. No dependencies.
 */

// The Golden Ratio - nature's proportion
export const PHI = (1 + Math.sqrt(5)) / 2; // 1.618033988749895
export const PHI_INVERSE = 1 / PHI; // 0.618033988749895
export const PHI_SQUARED = PHI * PHI; // 2.618033988749895

// Sacred roots
export const SQRT_2 = Math.sqrt(2); // 1.4142135623730951
export const SQRT_3 = Math.sqrt(3); // 1.7320508075688772
export const SQRT_5 = Math.sqrt(5); // 2.23606797749979

// Degrees to radians
export const DEG_TO_RAD = Math.PI / 180;

/**
 * Fibonacci sequence generator
 * @param n - Number of terms to generate
 * @returns Array of Fibonacci numbers
 */
export function fibonacci(n: number): number[] {
  const sequence: number[] = [1, 1];
  for (let i = 2; i < n; i++) {
    sequence[i] = sequence[i - 1] + sequence[i - 2];
  }
  return sequence.slice(0, n);
}

/**
 * Golden angle in radians (137.507764° ≈ 2.39996... rad)
 * Used for Fibonacci spiral distribution
 */
export const GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5)); // ~137.5°

/**
 * Generate points in a Fibonacci spiral pattern
 * Perfect for organic particle distribution
 * 
 * @param count - Number of points
 * @param radius - Maximum radius
 * @param height - Optional height variation
 * @returns Array of [x, y, z] coordinates
 */
export function fibonacciSphere(
  count: number,
  radius: number = 1,
  height: number = 0
): [number, number, number][] {
  const points: [number, number, number][] = [];
  
  for (let i = 0; i < count; i++) {
    // Distribute evenly on sphere using golden angle
    const theta = GOLDEN_ANGLE * i;
    const phi = Math.acos(1 - 2 * (i + 0.5) / count);
    
    const x = radius * Math.sin(phi) * Math.cos(theta);
    const y = radius * Math.sin(phi) * Math.sin(theta) + (height * (i / count - 0.5));
    const z = radius * Math.cos(phi);
    
    points.push([x, y, z]);
  }
  
  return points;
}

/**
 * Generate Fibonacci spiral in 2D
 * @param count - Number of points
 * @param scale - Scale factor
 * @returns Array of [x, y] coordinates
 */
export function fibonacciSpiral2D(
  count: number,
  scale: number = 1
): [number, number][] {
  const points: [number, number][] = [];
  
  for (let i = 0; i < count; i++) {
    const angle = i * GOLDEN_ANGLE;
    const r = scale * Math.sqrt(i);
    
    const x = r * Math.cos(angle);
    const y = r * Math.sin(angle);
    
    points.push([x, y]);
  }
  
  return points;
}

/**
 * Flower of Life - Sacred Geometry Pattern
 * 
 * The Flower of Life is composed of overlapping circles
 * arranged in a hexagonal pattern. The ratio between
 * the circles creates perfect proportions.
 * 
 * @param radius - Radius of each circle
 * @param layers - Number of layers (1 = 7 circles, 2 = 19 circles, etc.)
 * @returns Array of circle center coordinates [x, y]
 */
export function flowerOfLifeCircles(
  radius: number = 1,
  layers: number = 2
): [number, number][] {
  const circles: [number, number][] = [];
  
  // Center circle
  circles.push([0, 0]);
  
  // Generate concentric hexagonal layers
  for (let layer = 1; layer <= layers; layer++) {
    // 6 directions from center (hexagonal)
    for (let direction = 0; direction < 6; direction++) {
      const baseAngle = (direction * Math.PI) / 3;
      
      // Points along each edge of the hexagonal layer
      for (let step = 0; step < layer; step++) {
        // Start position
        const startX = layer * radius * Math.cos(baseAngle);
        const startY = layer * radius * Math.sin(baseAngle);
        
        // Next corner direction
        const nextAngle = baseAngle + (2 * Math.PI) / 3;
        const dx = radius * Math.cos(nextAngle);
        const dy = radius * Math.sin(nextAngle);
        
        const x = startX + step * dx;
        const y = startY + step * dy;
        
        circles.push([x, y]);
      }
    }
  }
  
  return circles;
}

/**
 * Seed of Life - The core pattern within Flower of Life
 * 7 overlapping circles forming the genesis pattern
 * 
 * @param radius - Radius of each circle
 * @returns Array of circle center coordinates [x, y]
 */
export function seedOfLife(radius: number = 1): [number, number][] {
  const circles: [number, number][] = [];
  
  // Center circle
  circles.push([0, 0]);
  
  // 6 surrounding circles at 60° intervals
  for (let i = 0; i < 6; i++) {
    const angle = (i * Math.PI) / 3;
    const x = radius * Math.cos(angle);
    const y = radius * Math.sin(angle);
    circles.push([x, y]);
  }
  
  return circles;
}

/**
 * Vesica Piscis - The intersection of two circles
 * Fundamental sacred geometry shape
 * 
 * @param radius - Radius of the circles
 * @param segments - Number of segments for the path
 * @returns Array of points forming the vesica piscis outline
 */
export function vesicaPiscis(
  radius: number = 1,
  segments: number = 32
): [number, number][] {
  const points: [number, number][] = [];
  const separation = radius; // Distance between circle centers
  
  // Upper arc (from circle 1)
  for (let i = 0; i <= segments / 2; i++) {
    const t = (i / (segments / 2)) * (2 * Math.PI / 3) + (Math.PI / 3);
    const x = -separation / 2 + radius * Math.cos(t);
    const y = radius * Math.sin(t);
    points.push([x, y]);
  }
  
  // Lower arc (from circle 2)
  for (let i = 0; i <= segments / 2; i++) {
    const t = (i / (segments / 2)) * (2 * Math.PI / 3) + (2 * Math.PI / 3);
    const x = separation / 2 + radius * Math.cos(t);
    const y = radius * Math.sin(t);
    points.push([x, y]);
  }
  
  return points;
}

/**
 * Platonic Solid Vertices
 * The 5 perfect 3D shapes with equal faces
 */
export const PLATONIC_SOLIDS = {
  /**
   * Tetrahedron - 4 vertices, 4 triangular faces
   * Fire element in classical philosophy
   */
  tetrahedron: (): [number, number, number][] => {
    const a = 1 / Math.sqrt(3);
    return [
      [a, a, a],
      [a, -a, -a],
      [-a, a, -a],
      [-a, -a, a],
    ];
  },

  /**
   * Cube (Hexahedron) - 8 vertices, 6 square faces
   * Earth element
   */
  cube: (): [number, number, number][] => {
    const vertices: [number, number, number][] = [];
    for (let x = -1; x <= 1; x += 2) {
      for (let y = -1; y <= 1; y += 2) {
        for (let z = -1; z <= 1; z += 2) {
          vertices.push([x * 0.5, y * 0.5, z * 0.5]);
        }
      }
    }
    return vertices;
  },

  /**
   * Octahedron - 6 vertices, 8 triangular faces
   * Air element
   */
  octahedron: (): [number, number, number][] => [
    [1, 0, 0],
    [-1, 0, 0],
    [0, 1, 0],
    [0, -1, 0],
    [0, 0, 1],
    [0, 0, -1],
  ],

  /**
   * Dodecahedron - 20 vertices, 12 pentagonal faces
   * Spirit/Aether element
   * Uses golden ratio in construction
   */
  dodecahedron: (): [number, number, number][] => {
    const vertices: [number, number, number][] = [];
    
    // Cube vertices
    for (let x = -1; x <= 1; x += 2) {
      for (let y = -1; y <= 1; y += 2) {
        for (let z = -1; z <= 1; z += 2) {
          vertices.push([x, y, z]);
        }
      }
    }
    
    // Rectangle vertices using golden ratio
    const phi = PHI;
    const invPhi = PHI_INVERSE;
    
    // xy-plane rectangles
    vertices.push([0, phi, invPhi], [0, phi, -invPhi]);
    vertices.push([0, -phi, invPhi], [0, -phi, -invPhi]);
    
    // xz-plane rectangles
    vertices.push([phi, invPhi, 0], [phi, -invPhi, 0]);
    vertices.push([-phi, invPhi, 0], [-phi, -invPhi, 0]);
    
    // yz-plane rectangles
    vertices.push([invPhi, 0, phi], [-invPhi, 0, phi]);
    vertices.push([invPhi, 0, -phi], [-invPhi, 0, -phi]);
    
    return vertices;
  },

  /**
   * Icosahedron - 12 vertices, 20 triangular faces
   * Water element
   * Uses golden ratio in construction
   */
  icosahedron: (): [number, number, number][] => {
    const phi = PHI;
    const vertices: [number, number, number][] = [];
    
    // Three orthogonal golden rectangles
    // xy-plane
    vertices.push([0, 1, phi], [0, 1, -phi]);
    vertices.push([0, -1, phi], [0, -1, -phi]);
    
    // xz-plane
    vertices.push([1, phi, 0], [1, -phi, 0]);
    vertices.push([-1, phi, 0], [-1, -phi, 0]);
    
    // yz-plane
    vertices.push([phi, 0, 1], [-phi, 0, 1]);
    vertices.push([phi, 0, -1], [-phi, 0, -1]);
    
    return vertices;
  },
};

/**
 * Golden Spiral Points
 * Generate points along a logarithmic spiral based on golden ratio
 * 
 * @param turns - Number of spiral turns
 * @param pointsPerTurn - Points per turn
 * @param scale - Scale factor
 * @returns Array of [x, y] coordinates
 */
export function goldenSpiral(
  turns: number = 3,
  pointsPerTurn: number = 32,
  scale: number = 1
): [number, number][] {
  const points: [number, number][] = [];
  const totalPoints = turns * pointsPerTurn;
  const b = Math.log(PHI) / (Math.PI / 2); // Growth factor
  
  for (let i = 0; i < totalPoints; i++) {
    const theta = (i / pointsPerTurn) * 2 * Math.PI;
    const r = scale * Math.exp(b * theta);
    
    const x = r * Math.cos(theta);
    const y = r * Math.sin(theta);
    
    points.push([x, y]);
  }
  
  return points;
}

/**
 * Torus Knot Parameters
 * Generate parameters for torus knots with golden proportions
 * 
 * @param p - Winds around the torus axis
 * @param q - Winds around the torus cross-section
 * @returns Object with geometric parameters
 */
export function goldenTorusKnot(
  p: number = 2,
  q: number = 3
): { majorRadius: number; minorRadius: number; p: number; q: number } {
  return {
    majorRadius: PHI,
    minorRadius: PHI_INVERSE,
    p,
    q,
  };
}

/**
 * Harmonic Proportions
 * Generate a series of harmonically related values
 * 
 * @param base - Base value
 * @param count - Number of harmonics
 * @returns Array of harmonic values
 */
export function harmonicSeries(base: number, count: number): number[] {
  const harmonics: number[] = [];
  for (let i = 1; i <= count; i++) {
    harmonics.push(base / i);
  }
  return harmonics;
}

/**
 * Metatron's Cube Vertices
 * The sacred geometry pattern containing all Platonic solids
 * 13 circles connected by 78 lines
 * 
 * @param radius - Radius of the pattern
 * @returns Array of circle center coordinates
 */
export function metatronsCube(radius: number = 1): [number, number][] {
  const centers: [number, number][] = [];
  
  // Center
  centers.push([0, 0]);
  
  // First ring (6 circles)
  for (let i = 0; i < 6; i++) {
    const angle = (i * Math.PI) / 3;
    centers.push([
      radius * Math.cos(angle),
      radius * Math.sin(angle),
    ]);
  }
  
  // Second ring (6 circles at √3 * radius)
  const outerRadius = radius * SQRT_3;
  for (let i = 0; i < 6; i++) {
    const angle = (i * Math.PI) / 3 + Math.PI / 6;
    centers.push([
      outerRadius * Math.cos(angle),
      outerRadius * Math.sin(angle),
    ]);
  }
  
  return centers;
}

/**
 * Sri Yantra Basic Structure
 * 9 interlocking triangles forming the sacred pattern
 * Simplified version returning triangle vertices
 * 
 * @param size - Size of the pattern
 * @returns Array of triangles, each as 3 [x, y] coordinates
 */
export function sriYantraTriangles(
  size: number = 1
): [[number, number], [number, number], [number, number]][] {
  const triangles: [[number, number], [number, number], [number, number]][] = [];
  
  // 4 upward pointing triangles (Shiva - masculine)
  const upwardHeights = [0.9, 0.7, 0.5, 0.3];
  upwardHeights.forEach((h, i) => {
    const width = h * PHI;
    const yBase = -h * 0.5 + (i * 0.1);
    triangles.push([
      [0, yBase + h * size],
      [-width * size / 2, yBase],
      [width * size / 2, yBase],
    ]);
  });
  
  // 5 downward pointing triangles (Shakti - feminine)
  const downwardHeights = [0.85, 0.65, 0.45, 0.35, 0.2];
  downwardHeights.forEach((h, i) => {
    const width = h * PHI;
    const yBase = h * 0.5 - (i * 0.08);
    triangles.push([
      [0, yBase - h * size],
      [-width * size / 2, yBase],
      [width * size / 2, yBase],
    ]);
  });
  
  return triangles;
}

/**
 * Calculate distance between two 3D points
 */
export function distance3D(
  a: [number, number, number],
  b: [number, number, number]
): number {
  return Math.sqrt(
    Math.pow(b[0] - a[0], 2) +
    Math.pow(b[1] - a[1], 2) +
    Math.pow(b[2] - a[2], 2)
  );
}

/**
 * Linear interpolation with golden easing
 * Smooth transitions that feel natural
 */
export function goldenLerp(a: number, b: number, t: number): number {
  // Apply golden ratio-based easing
  const goldenT = Math.pow(t, PHI_INVERSE);
  return a + (b - a) * goldenT;
}

/**
 * Generate a Lissajous curve with golden ratio frequencies
 * Beautiful, complex curves from simple parameters
 * 
 * @param points - Number of points
 * @param scale - Scale factor
 * @returns Array of [x, y, z] coordinates
 */
export function goldenLissajous(
  points: number = 256,
  scale: number = 1
): [number, number, number][] {
  const curve: [number, number, number][] = [];
  
  const freqX = 3;
  const freqY = 5; // Fibonacci pair
  const freqZ = 8; // Fibonacci pair
  
  for (let i = 0; i < points; i++) {
    const t = (i / points) * Math.PI * 2 * PHI;
    
    const x = scale * Math.sin(freqX * t);
    const y = scale * Math.sin(freqY * t + Math.PI / PHI);
    const z = scale * Math.sin(freqZ * t + Math.PI / PHI_SQUARED);
    
    curve.push([x, y, z]);
  }
  
  return curve;
}

