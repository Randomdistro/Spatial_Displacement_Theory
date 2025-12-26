/**
 * Creative Agent: Pressure Field Visualization
 * 
 * TEKNE: Visualization IS the medium
 * Volumetric gradient representing the spation pressure field
 * 
 * Design Philosophy:
 * - Deep blue at center (high pressure)
 * - Lighter blue at edges (pressure gradient)
 * - Gold flow lines showing direction
 * - Animated flow (particles or lines)
 * - Emissive: 0.2 intensity
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Mesh, SphereGeometry, MeshStandardMaterial, Color, Vector3 } from 'three';
import { useShader } from '../../framework/hooks';

// Design system colors
const COLORS = {
  spaceDeep: new Color(0x1a365d),      // High pressure (center)
  spaceMedium: new Color(0x2d5a87),    // Medium pressure
  spaceLight: new Color(0x4299e1),      // Low pressure (edges)
  goldPrimary: new Color(0xd69e2e),     // Flow direction
} as const;

export interface PressureFieldVisualizationProps {
  center: [number, number, number];
  radius: number;
  density?: number; // Pressure density (0-1)
  showFlowLines?: boolean;
}

/**
 * PressureFieldVisualization - Volumetric pressure field
 * 
 * Features:
 * - Volumetric gradient from center to edge
 * - Animated flow (particles or lines)
 * - Gold flow lines showing direction
 * - Breathing animation (pressure pulses)
 */
export default function PressureFieldVisualization({
  center,
  radius,
  density = 0.5,
  showFlowLines = true,
}: PressureFieldVisualizationProps) {
  const fieldRef = useRef<Mesh>(null);
  const materialRef = useRef<MeshStandardMaterial>(null);
  const flowLinesRef = useRef<Mesh[]>([]);

  // Pressure field shader (simplified - full volumetric would use custom shader)
  // For now, using multiple layered spheres for gradient effect
  const layers = useMemo(() => {
    const layerCount = 8;
    const layers: { radius: number; opacity: number; color: Color }[] = [];
    
    for (let i = 0; i < layerCount; i++) {
      const t = i / (layerCount - 1);
      const layerRadius = radius * (0.3 + t * 0.7); // Inner to outer
      const opacity = (1 - t) * density * 0.3; // More opaque at center
      
      // Color gradient: deep blue → medium → light
      const color = new Color().lerpColors(
        COLORS.spaceDeep,
        COLORS.spaceLight,
        t
      );
      
      layers.push({ radius: layerRadius, opacity, color });
    }
    
    return layers;
  }, [radius, density]);

  // Breathing animation - pressure field pulses
  useFrame((state) => {
    if (!fieldRef.current || !materialRef.current) return;
    
    const time = state.clock.elapsedTime;
    // Breathing: scale 1 ± 0.03, 4s cycle
    const breath = Math.sin(time * (Math.PI / 2)) * 0.03;
    fieldRef.current.scale.setScalar(1 + breath);
    
    // Emissive intensity pulses with breathing
    materialRef.current.emissiveIntensity = 0.2 + breath * 2;
  });

  return (
    <group position={center}>
      {/* Layered spheres for volumetric gradient effect */}
      {layers.map((layer, index) => (
        <mesh key={index} ref={index === 0 ? fieldRef : undefined}>
          <sphereGeometry args={[layer.radius, 32, 32]} />
          <meshStandardMaterial
            ref={index === 0 ? materialRef : undefined}
            color={layer.color}
            emissive={layer.color.clone().multiplyScalar(0.2)}
            emissiveIntensity={0.2}
            transparent
            opacity={layer.opacity}
            side={2} // DoubleSide
          />
        </mesh>
      ))}

      {/* Gold flow lines (simplified - would use custom shader for proper lines) */}
      {showFlowLines && (
        <group>
          {/* Flow direction indicators */}
          {Array.from({ length: 12 }).map((_, i) => {
            const angle = (i / 12) * Math.PI * 2;
            const distance = radius * 0.7;
            const x = Math.cos(angle) * distance;
            const z = Math.sin(angle) * distance;
            
            return (
              <mesh key={i} position={[x, 0, z]}>
                <coneGeometry args={[0.02, 0.1, 8]} />
                <meshStandardMaterial
                  color={COLORS.goldPrimary}
                  emissive={COLORS.goldPrimary}
                  emissiveIntensity={0.5}
                />
              </mesh>
            );
          })}
        </group>
      )}
    </group>
  );
}

