/**
 * Creative Agent: Atmospheric Effects
 * 
 * TEKNE: Atmosphere IS the spation medium
 * Depth fog, spation particles, and ambient glow
 * 
 * Design Philosophy:
 * - Atmosphere IS the medium itself
 * - Fog, particles, and glow ARE the medium's presence
 * - Subtle, not distracting
 * - Creates immersion
 * 
 * Enhanced with Sacred Geometry:
 * - Fibonacci sphere distribution (golden angle)
 * - Golden ratio proportions
 * - Harmonic pulsing frequencies
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Mesh, MeshStandardMaterial, Color, Points, BufferGeometry, BufferAttribute, PointsMaterial } from 'three';
import { fibonacciSphere, PHI, GOLDEN_ANGLE, harmonicSeries } from '../../utils/sacred-geometry';

// Design system colors
const COLORS = {
  spaceDeep: new Color(0x1a365d),
  spaceLight: new Color(0x4299e1),
  goldPrimary: new Color(0xd69e2e),
  goldBright: new Color(0xf6ad55),
} as const;

export interface AtmosphericEffectsProps {
  particleCount?: number;
  fogDensity?: number;
  glowIntensity?: number;
}

/**
 * AtmosphericEffects - Depth fog, particles, and glow
 * 
 * Features:
 * - Fibonacci sphere particle distribution (perfect uniformity)
 * - Golden ratio animation frequencies
 * - Harmonic pulsing (natural, organic)
 * - Ambient glow (bloom effect simulation)
 */
export default function AtmosphericEffects({
  particleCount = 1000,
  fogDensity = 0.02,
  glowIntensity = 0.3,
}: AtmosphericEffectsProps) {
  const particlesRef = useRef<Points>(null);
  const glowRef = useRef<Mesh>(null);

  // Generate spation particles using Fibonacci sphere distribution
  // This creates perfectly uniform distribution - the beauty of geometry
  const particlesGeometry = useMemo(() => {
    const geometry = new BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);
    
    // Use Fibonacci sphere for perfect distribution
    const fibPoints = fibonacciSphere(particleCount, 10, 0);
    
    for (let i = 0; i < particleCount; i++) {
      // Fibonacci-distributed positions (organic, natural)
      positions[i * 3] = fibPoints[i][0];
      positions[i * 3 + 1] = fibPoints[i][1];
      positions[i * 3 + 2] = fibPoints[i][2];
      
      // Size varies by golden ratio harmonics
      // Larger particles near center, smaller at edges
      const distFromCenter = Math.sqrt(
        fibPoints[i][0] ** 2 + 
        fibPoints[i][1] ** 2 + 
        fibPoints[i][2] ** 2
      );
      const sizeScale = 1 - (distFromCenter / 12); // 0-1 based on distance
      sizes[i] = (sizeScale * 0.015 + 0.005) * (1 + (i % 8 === 0 ? PHI - 1 : 0));
    }
    
    geometry.setAttribute('position', new BufferAttribute(positions, 3));
    geometry.setAttribute('size', new BufferAttribute(sizes, 1));
    
    return geometry;
  }, [particleCount]);

  // Harmonic frequencies for pulsing (based on golden ratio)
  const harmonics = useMemo(() => harmonicSeries(1, 5), []);

  // Particle animation - golden ratio orbital flow
  useFrame((state) => {
    if (!particlesRef.current || !particlesRef.current.geometry) return;
    
    const time = state.clock.elapsedTime;
    const positions = particlesRef.current.geometry.getAttribute('position') as BufferAttribute;
    
    // Golden ratio orbital flow - particles orbit using golden angle
    for (let i = 0; i < particleCount; i++) {
      const i3 = i * 3;
      
      // Each particle orbits at its Fibonacci-derived angle
      const orbitalAngle = (i * GOLDEN_ANGLE) + time * 0.05 * (1 + (i % 5) * 0.1);
      const orbitalRadius = 0.002;
      
      // Drift in golden spiral pattern (organic, natural)
      positions.array[i3] += Math.cos(orbitalAngle) * orbitalRadius;
      positions.array[i3 + 1] += Math.sin(orbitalAngle * PHI) * orbitalRadius * 0.5;
      positions.array[i3 + 2] += Math.sin(orbitalAngle) * orbitalRadius;
      
      // Soft boundary - particles slow near edges, reverse gently
      const dist = Math.sqrt(
        positions.array[i3] ** 2 +
        positions.array[i3 + 1] ** 2 +
        positions.array[i3 + 2] ** 2
      );
      
      if (dist > 11) {
        // Gently push back toward center
        const factor = -0.001;
        positions.array[i3] += positions.array[i3] * factor;
        positions.array[i3 + 1] += positions.array[i3 + 1] * factor;
        positions.array[i3 + 2] += positions.array[i3 + 2] * factor;
      }
    }
    
    positions.needsUpdate = true;
    
    // Harmonic pulsing (golden ratio frequencies)
    if (particlesRef.current.material instanceof PointsMaterial) {
      // Sum of harmonics creates organic pulsing
      const pulse = harmonics.reduce((sum, h, idx) => {
        return sum + Math.sin(time * h * PHI) * (1 / (idx + 1));
      }, 0) / harmonics.length;
      
      particlesRef.current.material.opacity = 0.5 + pulse * 0.2;
    }
  });

  // Ambient glow (bloom effect simulation)
  useFrame((state) => {
    if (!glowRef.current) return;
    
    const time = state.clock.elapsedTime;
    // Subtle pulsing glow
    const pulse = Math.sin(time * 0.5) * 0.1 + 1.0;
    if (glowRef.current.material instanceof MeshStandardMaterial) {
      glowRef.current.material.emissiveIntensity = glowIntensity * pulse;
    }
  });

  return (
    <group>
      {/* Spation Particles */}
      <points ref={particlesRef} geometry={particlesGeometry}>
        <pointsMaterial
          color={COLORS.spaceLight}
          size={0.01}
          transparent
          opacity={0.6}
          emissive={COLORS.goldPrimary}
          emissiveIntensity={0.3}
          sizeAttenuation={true}
        />
      </points>

      {/* Ambient Glow (large sphere for bloom effect) */}
      <mesh ref={glowRef}>
        <sphereGeometry args={[15, 32, 32]} />
        <meshStandardMaterial
          color={COLORS.spaceDeep}
          emissive={COLORS.goldPrimary}
          emissiveIntensity={glowIntensity}
          transparent
          opacity={0.05}
          side={2} // DoubleSide
        />
      </mesh>
    </group>
  );
}

