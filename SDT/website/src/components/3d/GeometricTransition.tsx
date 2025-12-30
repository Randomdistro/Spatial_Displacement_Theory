/**
 * Creative Agent: Geometric Transition Effect
 * 
 * TEKNE: Transitions ARE transformations
 * 
 * Sacred geometry-based transition effects between views:
 * - Vesica Piscis portal opening
 * - Golden spiral expansion
 * - Flower of Life bloom
 * 
 * The beauty of geometry transforms space itself.
 */

import React, { useRef, useEffect, useMemo, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Group, Mesh, MeshStandardMaterial, Color, Vector3 } from 'three';
import { Line, Ring } from '@react-three/drei';
import { 
  PHI, 
  PHI_INVERSE, 
  GOLDEN_ANGLE,
  seedOfLife,
  goldenSpiral,
  fibonacci
} from '../../utils/sacred-geometry';
import { EasingFunctions } from '../../framework/animation/AnimationChoreographer';

// Design system colors
const COLORS = {
  goldPrimary: new Color(0xd69e2e),
  goldBright: new Color(0xf6ad55),
  goldLight: new Color(0xfbbf24),
  spaceDeep: new Color(0x1a365d),
  spaceLight: new Color(0x4299e1),
} as const;

export interface GeometricTransitionProps {
  active: boolean;
  variant?: 'portal' | 'spiral' | 'bloom';
  duration?: number;
  onComplete?: () => void;
}

/**
 * GeometricTransition - Sacred geometry transition effects
 * 
 * Variants:
 * - portal: Vesica Piscis opening/closing
 * - spiral: Golden spiral expansion
 * - bloom: Flower of Life blooming outward
 */
export default function GeometricTransition({
  active,
  variant = 'bloom',
  duration = 1500,
  onComplete,
}: GeometricTransitionProps) {
  const groupRef = useRef<Group>(null);
  const [progress, setProgress] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const startTimeRef = useRef<number | null>(null);

  // Seed of Life positions for bloom effect
  const seedPositions = useMemo(() => {
    return seedOfLife(1).map(([x, y]) => new Vector3(x, y, 0));
  }, []);

  // Golden spiral points for spiral effect
  const spiralPoints = useMemo(() => {
    return goldenSpiral(2, 24, 0.5).map(([x, y]) => new Vector3(x, y, 0));
  }, []);

  // Fibonacci sequence for timing
  const fibSequence = useMemo(() => fibonacci(8), []);

  // Start animation when active changes
  useEffect(() => {
    if (active && !isAnimating) {
      setIsAnimating(true);
      startTimeRef.current = null;
    }
  }, [active, isAnimating]);

  // Animation loop
  useFrame((state) => {
    if (!isAnimating) return;

    // Initialize start time
    if (startTimeRef.current === null) {
      startTimeRef.current = state.clock.elapsedTime * 1000;
    }

    const elapsed = state.clock.elapsedTime * 1000 - startTimeRef.current;
    const rawProgress = Math.min(elapsed / duration, 1);
    
    // Apply golden easing
    const easedProgress = EasingFunctions.goldenEaseInOut(rawProgress);
    setProgress(easedProgress);

    // Rotate group slowly
    if (groupRef.current) {
      groupRef.current.rotation.z = easedProgress * Math.PI * PHI_INVERSE;
    }

    // Complete animation
    if (rawProgress >= 1) {
      setIsAnimating(false);
      startTimeRef.current = null;
      if (onComplete) onComplete();
    }
  });

  // Don't render if not active and not animating
  if (!active && !isAnimating && progress === 0) return null;

  return (
    <group ref={groupRef} position={[0, 0, 2]}>
      {/* PORTAL VARIANT - Vesica Piscis opening */}
      {variant === 'portal' && (
        <>
          {/* Two overlapping circles that separate */}
          <Ring
            args={[0.9, 1, 64]}
            position={[-progress * PHI * 0.5, 0, 0]}
          >
            <meshStandardMaterial
              color={COLORS.goldPrimary}
              emissive={COLORS.goldBright}
              emissiveIntensity={0.5}
              transparent
              opacity={1 - progress * 0.5}
              side={2}
            />
          </Ring>
          <Ring
            args={[0.9, 1, 64]}
            position={[progress * PHI * 0.5, 0, 0]}
          >
            <meshStandardMaterial
              color={COLORS.goldPrimary}
              emissive={COLORS.goldBright}
              emissiveIntensity={0.5}
              transparent
              opacity={1 - progress * 0.5}
              side={2}
            />
          </Ring>
          
          {/* Central glow expanding */}
          <mesh scale={[progress * 3, progress * 3, 1]}>
            <circleGeometry args={[1, 32]} />
            <meshStandardMaterial
              color={COLORS.spaceDeep}
              emissive={COLORS.goldLight}
              emissiveIntensity={progress}
              transparent
              opacity={progress * 0.8}
            />
          </mesh>
        </>
      )}

      {/* SPIRAL VARIANT - Golden spiral expansion */}
      {variant === 'spiral' && (
        <>
          {/* Animated spiral line */}
          <Line
            points={spiralPoints.slice(0, Math.floor(spiralPoints.length * progress))}
            color={COLORS.goldPrimary}
            lineWidth={2}
            transparent
            opacity={0.8}
          />
          
          {/* Spiral markers at Fibonacci positions */}
          {spiralPoints
            .filter((_, idx) => fibSequence.includes(idx + 1) && idx < spiralPoints.length * progress)
            .map((pos, idx) => (
              <mesh
                key={`spiral-node-${idx}`}
                position={pos}
                scale={[progress, progress, progress]}
              >
                <sphereGeometry args={[0.05 + idx * 0.02, 16, 16]} />
                <meshStandardMaterial
                  color={COLORS.goldBright}
                  emissive={COLORS.goldLight}
                  emissiveIntensity={0.6}
                  transparent
                  opacity={0.9}
                />
              </mesh>
            ))}
          
          {/* Center point */}
          <mesh>
            <sphereGeometry args={[0.1 * progress, 16, 16]} />
            <meshStandardMaterial
              color={COLORS.goldLight}
              emissive={COLORS.goldBright}
              emissiveIntensity={1}
            />
          </mesh>
        </>
      )}

      {/* BLOOM VARIANT - Flower of Life blooming */}
      {variant === 'bloom' && (
        <>
          {/* Seed of Life circles expanding */}
          {seedPositions.map((pos, idx) => {
            // Stagger based on Fibonacci timing
            const delay = idx * PHI_INVERSE * 0.15;
            const circleProgress = Math.max(0, Math.min(1, (progress - delay) / (1 - delay)));
            
            // Scale from 0 to full
            const scale = circleProgress;
            
            // Position moves outward
            const expandedPos = pos.clone().multiplyScalar(1 + circleProgress * PHI_INVERSE);
            
            return (
              <group key={`seed-${idx}`}>
                {/* Ring */}
                <Ring
                  args={[0.3 * scale, 0.35 * scale, 32]}
                  position={expandedPos}
                  rotation={[0, 0, idx * GOLDEN_ANGLE]}
                >
                  <meshStandardMaterial
                    color={idx === 0 ? COLORS.goldBright : COLORS.spaceLight}
                    emissive={idx === 0 ? COLORS.goldLight : COLORS.spaceLight}
                    emissiveIntensity={0.4 + circleProgress * 0.3}
                    transparent
                    opacity={circleProgress * 0.8}
                    side={2}
                  />
                </Ring>
                
                {/* Connecting line to center */}
                {idx > 0 && circleProgress > 0.5 && (
                  <Line
                    points={[new Vector3(0, 0, 0), expandedPos]}
                    color={COLORS.goldPrimary}
                    lineWidth={1}
                    transparent
                    opacity={(circleProgress - 0.5) * 2 * 0.3}
                  />
                )}
              </group>
            );
          })}
          
          {/* Outer ring expanding last */}
          <Ring
            args={[
              PHI * progress, 
              PHI * progress + 0.1, 
              64
            ]}
          >
            <meshStandardMaterial
              color={COLORS.goldPrimary}
              emissive={COLORS.goldBright}
              emissiveIntensity={0.3}
              transparent
              opacity={progress * 0.5}
              side={2}
            />
          </Ring>
          
          {/* Particle burst at completion */}
          {progress > 0.8 && (
            <>
              {Array.from({ length: 12 }).map((_, idx) => {
                const angle = idx * GOLDEN_ANGLE;
                const burstProgress = (progress - 0.8) / 0.2;
                const distance = burstProgress * PHI * 2;
                
                return (
                  <mesh
                    key={`burst-${idx}`}
                    position={[
                      Math.cos(angle) * distance,
                      Math.sin(angle) * distance,
                      0
                    ]}
                    scale={[(1 - burstProgress) * 0.5, (1 - burstProgress) * 0.5, 1]}
                  >
                    <sphereGeometry args={[0.05, 8, 8]} />
                    <meshStandardMaterial
                      color={COLORS.goldLight}
                      emissive={COLORS.goldBright}
                      emissiveIntensity={1}
                      transparent
                      opacity={(1 - burstProgress) * 0.8}
                    />
                  </mesh>
                );
              })}
            </>
          )}
        </>
      )}
    </group>
  );
}

