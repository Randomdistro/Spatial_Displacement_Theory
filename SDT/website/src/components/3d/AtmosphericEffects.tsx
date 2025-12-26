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
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Mesh, SphereGeometry, MeshStandardMaterial, Color, Points, BufferGeometry, BufferAttribute, PointsMaterial } from 'three';

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
 * - Depth fog (exponential, distance-based)
 * - Spation particles (slow drift, gold glow)
 * - Ambient glow (bloom effect simulation)
 */
export default function AtmosphericEffects({
  particleCount = 1000,
  fogDensity = 0.02,
  glowIntensity = 0.3,
}: AtmosphericEffectsProps) {
  const particlesRef = useRef<Points>(null);
  const glowRef = useRef<Mesh>(null);

  // Generate spation particles
  const particlesGeometry = useMemo(() => {
    const geometry = new BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);
    
    for (let i = 0; i < particleCount; i++) {
      // Random position in space
      positions[i * 3] = (Math.random() - 0.5) * 20;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 20;
      
      // Random size
      sizes[i] = Math.random() * 0.01 + 0.005;
    }
    
    geometry.setAttribute('position', new BufferAttribute(positions, 3));
    geometry.setAttribute('size', new BufferAttribute(sizes, 1));
    
    return geometry;
  }, [particleCount]);

  // Particle animation - slow drift (pressure flow)
  useFrame((state) => {
    if (!particlesRef.current || !particlesRef.current.geometry) return;
    
    const time = state.clock.elapsedTime;
    const positions = particlesRef.current.geometry.getAttribute('position') as BufferAttribute;
    
    // Slow drift animation
    for (let i = 0; i < particleCount; i++) {
      const i3 = i * 3;
      // Drift in pressure flow direction
      positions.array[i3] += Math.sin(time * 0.1 + i * 0.01) * 0.001;
      positions.array[i3 + 1] += Math.cos(time * 0.15 + i * 0.01) * 0.001;
      positions.array[i3 + 2] += Math.sin(time * 0.12 + i * 0.01) * 0.001;
      
      // Wrap around if out of bounds
      if (Math.abs(positions.array[i3]) > 10) positions.array[i3] *= -1;
      if (Math.abs(positions.array[i3 + 1]) > 10) positions.array[i3 + 1] *= -1;
      if (Math.abs(positions.array[i3 + 2]) > 10) positions.array[i3 + 2] *= -1;
    }
    
    positions.needsUpdate = true;
    
    // Subtle twinkle (random emissive variation)
    if (particlesRef.current.material instanceof PointsMaterial) {
      const twinkle = Math.sin(time * 2 + Math.random() * Math.PI) * 0.1 + 0.9;
      particlesRef.current.material.opacity = twinkle * 0.6;
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

