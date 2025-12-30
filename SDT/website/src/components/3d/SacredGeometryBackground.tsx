/**
 * Creative Agent: Sacred Geometry Background
 * 
 * TEKNE: The background IS the medium itself
 * 
 * A subtle, animated sacred geometry pattern that:
 * - Reinforces the Spatial Displacement Theory visual language
 * - Uses Metatron's Cube (contains all Platonic solids)
 * - Animates with golden ratio frequencies
 * - Creates depth and atmosphere without distraction
 * 
 * The beauty of geometry, the simplicity of geometry,
 * the precision of geometry - all in perfect harmony.
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Line, Sphere } from '@react-three/drei';
import { Group, Color, Vector3 } from 'three';
import { 
  metatronsCube, 
  PHI, 
  PHI_INVERSE, 
  GOLDEN_ANGLE,
  goldenSpiral,
  fibonacci
} from '../../utils/sacred-geometry';

// Design system colors
const COLORS = {
  spaceDeep: new Color(0x1a365d),
  spaceLight: new Color(0x4299e1),
  goldPrimary: new Color(0xd69e2e),
  goldLight: new Color(0xfbbf24),
  silver: new Color(0xcbd5e0),
} as const;

export interface SacredGeometryBackgroundProps {
  variant?: 'metatron' | 'spiral' | 'both';
  opacity?: number;
  scale?: number;
  animated?: boolean;
}

/**
 * SacredGeometryBackground - Subtle sacred geometry patterns
 * 
 * Variants:
 * - metatron: Metatron's Cube pattern (13 circles, 78 lines)
 * - spiral: Golden spiral pattern
 * - both: Combined patterns
 */
export default function SacredGeometryBackground({
  variant = 'both',
  opacity = 0.15,
  scale = 5,
  animated = true,
}: SacredGeometryBackgroundProps) {
  const groupRef = useRef<Group>(null);
  const metatronRef = useRef<Group>(null);
  const spiralRef = useRef<Group>(null);

  // Generate Metatron's Cube vertices
  const metatronVertices = useMemo(() => {
    return metatronsCube(scale * 0.3).map(([x, y]) => [x, y, 0] as [number, number, number]);
  }, [scale]);

  // Generate all connections in Metatron's Cube
  const metatronLines = useMemo(() => {
    const lines: Array<[[number, number, number], [number, number, number]]> = [];
    
    // Connect all vertices (creates the sacred pattern)
    for (let i = 0; i < metatronVertices.length; i++) {
      for (let j = i + 1; j < metatronVertices.length; j++) {
        lines.push([metatronVertices[i], metatronVertices[j]]);
      }
    }
    
    return lines;
  }, [metatronVertices]);

  // Generate Golden Spiral points
  const spiralPoints = useMemo(() => {
    const points2D = goldenSpiral(3, 32, scale * 0.15);
    return points2D.map(([x, y]) => new Vector3(x, y, -2));
  }, [scale]);

  // Fibonacci sequence for circle sizing
  const fibSequence = useMemo(() => fibonacci(8), []);

  // Animation - golden ratio frequencies
  useFrame((state) => {
    if (!animated) return;
    
    const time = state.clock.elapsedTime;
    
    // Rotate entire group slowly
    if (groupRef.current) {
      groupRef.current.rotation.z = time * PHI_INVERSE * 0.05;
    }
    
    // Metatron's Cube pulses at golden frequency
    if (metatronRef.current) {
      const pulse = Math.sin(time * PHI_INVERSE) * 0.05 + 1;
      metatronRef.current.scale.setScalar(pulse);
    }
    
    // Spiral rotates at different golden frequency
    if (spiralRef.current) {
      spiralRef.current.rotation.z = time * PHI_INVERSE * PHI_INVERSE * 0.1;
      const spiralPulse = Math.sin(time * PHI_INVERSE * PHI) * 0.03 + 1;
      spiralRef.current.scale.setScalar(spiralPulse);
    }
  });

  return (
    <group ref={groupRef} position={[0, 0, -10]}>
      {/* Metatron's Cube */}
      {(variant === 'metatron' || variant === 'both') && (
        <group ref={metatronRef}>
          {/* Vertex circles - sized by Fibonacci sequence */}
          {metatronVertices.map((pos, idx) => {
            const fibIdx = idx % fibSequence.length;
            const radius = fibSequence[fibIdx] * 0.02 + 0.05;
            
            return (
              <Sphere
                key={`vertex-${idx}`}
                args={[radius, 16, 16]}
                position={pos}
              >
                <meshStandardMaterial
                  color={idx === 0 ? COLORS.goldPrimary : COLORS.spaceLight}
                  emissive={idx === 0 ? COLORS.goldLight : COLORS.spaceLight}
                  emissiveIntensity={0.3}
                  transparent
                  opacity={opacity * (idx === 0 ? 1.5 : 1)}
                />
              </Sphere>
            );
          })}
          
          {/* Connection lines - golden gradient opacity */}
          {metatronLines.map(([from, to], idx) => {
            // Opacity based on golden ratio position
            const lineOpacity = opacity * (0.3 + (Math.sin(idx * GOLDEN_ANGLE) + 1) * 0.35);
            
            return (
              <Line
                key={`line-${idx}`}
                points={[from, to]}
                color={COLORS.silver}
                lineWidth={0.5}
                transparent
                opacity={lineOpacity}
              />
            );
          })}
        </group>
      )}

      {/* Golden Spiral */}
      {(variant === 'spiral' || variant === 'both') && (
        <group ref={spiralRef}>
          <Line
            points={spiralPoints}
            color={COLORS.goldPrimary}
            lineWidth={1.5}
            transparent
            opacity={opacity * 0.8}
          />
          
          {/* Spiral endpoint markers at Fibonacci positions */}
          {spiralPoints
            .filter((_, idx) => fibSequence.includes(idx + 1))
            .map((pos, idx) => (
              <Sphere
                key={`spiral-marker-${idx}`}
                args={[0.05 + idx * 0.02, 8, 8]}
                position={pos}
              >
                <meshStandardMaterial
                  color={COLORS.goldLight}
                  emissive={COLORS.goldPrimary}
                  emissiveIntensity={0.5}
                  transparent
                  opacity={opacity}
                />
              </Sphere>
            ))}
        </group>
      )}

      {/* Central glow - the source */}
      <Sphere args={[0.2, 32, 32]} position={[0, 0, 0]}>
        <meshStandardMaterial
          color={COLORS.goldPrimary}
          emissive={COLORS.goldLight}
          emissiveIntensity={0.8}
          transparent
          opacity={opacity * 1.5}
        />
      </Sphere>
    </group>
  );
}

