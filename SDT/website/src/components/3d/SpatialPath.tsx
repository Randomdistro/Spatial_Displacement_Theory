/**
 * Creative Agent: Spatial Path Visualization
 * 
 * TEKNE: Navigation IS spatial understanding
 * Gold gradient tubes connecting nodes with flow animation
 * 
 * Design Philosophy:
 * - Navigation IS learning, learning IS navigation
 * - Moving through nodes IS understanding the theory's structure
 * - Subtle, not distracting
 * - Gold flow shows direction
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Mesh, TubeGeometry, MeshStandardMaterial, Color, Vector3, CatmullRomCurve3 } from 'three';
import { useAnimation, EasingFunctions } from '../../framework/hooks';

// Design system colors
const COLORS = {
  goldPrimary: new Color(0xd69e2e),
  goldBright: new Color(0xf6ad55),
  goldLight: new Color(0xfbbf24),
  spaceDeep: new Color(0x1a365d),
} as const;

export interface SpatialPathProps {
  from: [number, number, number];
  to: [number, number, number];
  visited?: boolean;
  current?: boolean;
  progress?: number; // 0-1, for progress visualization
}

/**
 * SpatialPath - Gold gradient tube connecting nodes
 * 
 * Features:
 * - Gold gradient tube (diameter: 0.05 units)
 * - Flow animation (particles moving along path)
 * - Opacity: 0.6 (subtle, not distracting)
 * - Progress visualization (gold trail)
 */
export default function SpatialPath({
  from,
  to,
  visited = false,
  current = false,
  progress = 0,
}: SpatialPathProps) {
  const tubeRef = useRef<Mesh>(null);
  const progressRef = useRef<Mesh>(null);
  const materialRef = useRef<MeshStandardMaterial>(null);
  const progressMaterialRef = useRef<MeshStandardMaterial>(null);

  // Create smooth curve between points
  const curve = useMemo(() => {
    const start = new Vector3(...from);
    const end = new Vector3(...to);
    
    // Create control points for smooth arc
    const mid = new Vector3().addVectors(start, end).multiplyScalar(0.5);
    mid.y += 0.5; // Arc upward
    
    // Catmull-Rom curve for smooth path
    const points = [start, mid, end];
    return new CatmullRomCurve3(points);
  }, [from, to]);

  // Generate tube geometry
  const tubeGeometry = useMemo(() => {
    return new TubeGeometry(curve, 32, 0.05, 8, false);
  }, [curve]);

  // Progress geometry (shorter tube showing progress)
  const progressGeometry = useMemo(() => {
    if (progress <= 0) return null;
    
    // Create curve up to progress point
    const progressPoints: Vector3[] = [];
    const segments = Math.floor(32 * progress);
    
    for (let i = 0; i <= segments; i++) {
      const t = i / 32;
      progressPoints.push(curve.getPoint(t));
    }
    
    if (progressPoints.length < 2) return null;
    
    const progressCurve = new CatmullRomCurve3(progressPoints);
    return new TubeGeometry(progressCurve, segments, 0.06, 8, false);
  }, [curve, progress]);

  // Flow animation - particles moving along path
  useFrame((state) => {
    if (!tubeRef.current || !materialRef.current) return;
    
    const time = state.clock.elapsedTime;
    
    // Animate emissive intensity for flow effect
    const flow = Math.sin(time * 2 + progress * Math.PI * 2) * 0.3 + 0.7;
    materialRef.current.emissiveIntensity = flow;
    
    // Rotate tube slightly for visual interest
    tubeRef.current.rotation.z = Math.sin(time * 0.5) * 0.1;
  });

  // Color based on state
  const baseColor = visited || current 
    ? COLORS.goldPrimary 
    : COLORS.spaceDeep.clone().multiplyScalar(0.5);
  
  const emissiveColor = current 
    ? COLORS.goldBright 
    : COLORS.goldPrimary.clone().multiplyScalar(0.5);

  return (
    <group>
      {/* Main path tube */}
      <mesh ref={tubeRef} geometry={tubeGeometry}>
        <meshStandardMaterial
          ref={materialRef}
          color={baseColor}
          emissive={emissiveColor}
          emissiveIntensity={0.6}
          metalness={0.8}
          roughness={0.2}
          transparent
          opacity={0.6}
        />
      </mesh>

      {/* Progress trail (gold, brighter) */}
      {progressGeometry && progress > 0 && (
        <mesh ref={progressRef} geometry={progressGeometry}>
          <meshStandardMaterial
            ref={progressMaterialRef}
            color={COLORS.goldBright}
            emissive={COLORS.goldLight}
            emissiveIntensity={1.5}
            metalness={0.9}
            roughness={0.1}
            transparent
            opacity={0.8}
          />
        </mesh>
      )}
    </group>
  );
}

