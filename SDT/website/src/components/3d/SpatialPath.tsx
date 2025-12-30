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
import { PHI, PHI_INVERSE, GOLDEN_ANGLE } from '../../utils/sacred-geometry';

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

  // Create smooth curve between points using GOLDEN RATIO proportions
  const curve = useMemo(() => {
    const start = new Vector3(...from);
    const end = new Vector3(...to);
    
    // Calculate distance for proportional arc height
    const distance = start.distanceTo(end);
    
    // Golden ratio arc: height = distance * PHI_INVERSE (0.618...)
    // This creates naturally beautiful, harmonious curves
    const arcHeight = distance * PHI_INVERSE * 0.5;
    
    // Create control points using golden section
    // First control point at 1/PHI of the way
    const t1 = PHI_INVERSE; // 0.382...
    const t2 = 1 - PHI_INVERSE; // 0.618...
    
    const ctrl1 = new Vector3().lerpVectors(start, end, t1);
    ctrl1.y += arcHeight;
    
    const ctrl2 = new Vector3().lerpVectors(start, end, t2);
    ctrl2.y += arcHeight * PHI; // Slightly higher at golden point
    
    // Catmull-Rom curve with golden-proportioned control points
    const points = [start, ctrl1, ctrl2, end];
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

  // Flow animation - golden ratio frequencies
  useFrame((state) => {
    if (!tubeRef.current || !materialRef.current) return;
    
    const time = state.clock.elapsedTime;
    
    // Golden ratio frequency for flow animation
    // Creates naturally pleasing pulsing rhythm
    const goldenFreq = PHI_INVERSE * 2; // ~1.236 Hz
    const flow = Math.sin(time * goldenFreq + progress * Math.PI * PHI) * 0.3 + 0.7;
    materialRef.current.emissiveIntensity = flow;
    
    // Subtle rotation using golden angle for organic feel
    tubeRef.current.rotation.z = Math.sin(time * PHI_INVERSE * 0.5) * 0.08;
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

