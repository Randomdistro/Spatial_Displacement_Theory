/**
 * Creative Agent: Node Indicator Component
 * 
 * TEKNE: Visual indicators ARE spatial markers
 * Spheres at node positions with pulsing animation
 * 
 * Design Philosophy:
 * - Gold (visited), Blue (unvisited), Silver (current)
 * - Pulsing animation (scale: 1 ± 0.1, 2s cycle)
 * - Size: 0.15 units
 * - Subtle, not distracting
 */

import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Mesh, MeshStandardMaterial, Color } from 'three';
import { PHI, PHI_INVERSE, GOLDEN_ANGLE } from '../../utils/sacred-geometry';

// Design system colors
const COLORS = {
  goldPrimary: new Color(0xd69e2e),
  spaceDeep: new Color(0x1a365d),
  spaceMedium: new Color(0x2d5a87),
  spaceLight: new Color(0x4299e1),
  silver: new Color(0xcbd5e0),
} as const;

export interface NodeIndicatorProps {
  position: [number, number, number];
  state: 'visited' | 'unvisited' | 'current';
  size?: number;
}

/**
 * NodeIndicator - Sphere marker for node position
 * 
 * Features:
 * - Color based on state (gold/blue/silver)
 * - Pulsing animation (scale: 1 ± 0.1, 2s cycle)
 * - Size: 0.15 units (default)
 * - Gold glow for visited/current
 */
export default function NodeIndicator({
  position,
  state,
  size = 0.15,
}: NodeIndicatorProps) {
  const indicatorRef = useRef<Mesh>(null);
  const materialRef = useRef<MeshStandardMaterial>(null);

  // Determine color based on state
  const getColor = (): Color => {
    switch (state) {
      case 'visited':
        return COLORS.goldPrimary;
      case 'current':
        return COLORS.silver;
      case 'unvisited':
        return COLORS.spaceMedium;
      default:
        return COLORS.spaceMedium;
    }
  };

  const baseColor = getColor();
  const emissiveColor = state === 'visited' || state === 'current'
    ? COLORS.goldPrimary.clone().multiplyScalar(0.5)
    : COLORS.spaceLight.clone().multiplyScalar(0.2);

  // Pulsing animation - golden ratio frequency
  // PHI_INVERSE Hz (~0.618 Hz) creates organic, natural rhythm
  useFrame((frameState) => {
    if (!indicatorRef.current || !materialRef.current) return;
    
    const time = frameState.clock.elapsedTime;
    
    // Golden ratio pulse: frequency = PHI_INVERSE (natural, organic)
    // Amplitude = 0.1 (1 ± 0.1)
    const pulse = Math.sin(time * Math.PI * PHI_INVERSE) * 0.1 + 1.0;
    indicatorRef.current.scale.setScalar(pulse);
    
    // Secondary micro-rotation for depth (using golden angle)
    indicatorRef.current.rotation.y = time * PHI_INVERSE * 0.5;
    
    // Emissive intensity pulses with golden ratio amplitude
    materialRef.current.emissiveIntensity = (pulse - 1) * PHI + 0.3;
  });

  return (
    <mesh ref={indicatorRef} position={position}>
      <sphereGeometry args={[size, 16, 16]} />
      <meshStandardMaterial
        ref={materialRef}
        color={baseColor}
        emissive={emissiveColor}
        emissiveIntensity={0.3}
        metalness={0.8}
        roughness={0.2}
        transparent
        opacity={0.8}
      />
    </mesh>
  );
}

