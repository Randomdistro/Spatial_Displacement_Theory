/**
 * Creative Agent: Content Card Component
 * 
 * TEKNE: Content IS space, space IS content
 * Glassmorphism cards floating in pressure field
 * 
 * Design Philosophy:
 * - Content doesn't sit on surfaces—it exists in the pressure field
 * - Text, formulas, and visualizations are spatial entities
 * - Subtle, subdued, visceral
 */

import React, { useRef, useEffect, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Mesh, MeshStandardMaterial, Color, Vector3 } from 'three';
import { Text } from '@react-three/drei';
import { gsap } from 'gsap';
import { useAnimation, EasingFunctions } from '../../framework/hooks';

// Design system colors
const COLORS = {
  spaceDeep: new Color(0x1a365d),
  goldPrimary: new Color(0xd69e2e),
  goldBright: new Color(0xf6ad55),
  silver: new Color(0xcbd5e0),
} as const;

export interface ContentCardProps {
  content: string;
  position: [number, number, number];
  index: number;
  visible?: boolean;
  onHover?: () => void;
}

/**
 * ContentCard - Glassmorphism card floating in space
 * 
 * Features:
 * - Rounded rectangle (pill-shaped)
 * - Glassmorphism effect (semi-transparent with backdrop)
 * - Gold border glow on hover
 * - Fade in from center with stagger
 * - Depth-based opacity
 */
export default function ContentCard({
  content,
  position,
  index,
  visible = true,
  onHover,
}: ContentCardProps) {
  const [hovered, setHovered] = useState(false);
  const [mounted, setMounted] = useState(false);
  const cardRef = useRef<Mesh>(null);
  const materialRef = useRef<MeshStandardMaterial>(null);
  const borderRef = useRef<Mesh>(null);
  const borderMaterialRef = useRef<MeshStandardMaterial>(null);

  // Content appearance animation - Fade in from center with stagger
  const { play: playAppearAnimation } = useAnimation({
    sequences: [
      {
        id: `card-appear-${index}`,
        duration: 600,
        delay: index * 200, // Stagger: 0.2s between elements
        easing: EasingFunctions.organic,
        onStart: () => {
          setMounted(true);
          if (cardRef.current) {
            cardRef.current.scale.set(0.8, 0.8, 0.8);
            cardRef.current.position.set(...position);
          }
        },
        onUpdate: (progress) => {
          if (cardRef.current) {
            // Scale: 0.8 → 1.0
            const scale = 0.8 + (progress * 0.2);
            cardRef.current.scale.set(scale, scale, scale);
          }
          if (materialRef.current) {
            materialRef.current.opacity = progress * 0.85;
          }
        },
      },
    ],
    autoPlay: visible,
  });

  // Hover animation
  useEffect(() => {
    if (!mounted || !cardRef.current) return;

    if (hovered) {
      // Hover: Slight lift, increased glow
      gsap.to(cardRef.current.position, {
        y: position[1] + 0.1,
        duration: 0.3,
        ease: 'power2.out',
      });
      gsap.to(borderMaterialRef.current, {
        emissiveIntensity: 0.5,
        duration: 0.3,
      });
      if (onHover) onHover();
    } else {
      // Normal: Return to position
      gsap.to(cardRef.current.position, {
        y: position[1],
        duration: 0.3,
        ease: 'power2.out',
      });
      gsap.to(borderMaterialRef.current, {
        emissiveIntensity: 0.2,
        duration: 0.3,
      });
    }
  }, [hovered, mounted, position]);

  // Subtle floating animation
  useFrame((state) => {
    if (!cardRef.current || !mounted) return;
    const time = state.clock.elapsedTime;
    const float = Math.sin(time * 0.5 + index * 0.5) * 0.05;
    cardRef.current.position.y = position[1] + float;
  });

  if (!visible || !mounted) return null;

  // Calculate card size based on content length (simplified)
  const cardWidth = Math.min(content.length * 0.05, 3);
  const cardHeight = 0.8;
  const cardThickness = 0.1;

  return (
    <group>
      {/* Main Card - Rounded rectangle */}
      <mesh
        ref={cardRef}
        position={position}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <boxGeometry args={[cardWidth, cardHeight, cardThickness]} />
        <meshStandardMaterial
          ref={materialRef}
          color={COLORS.spaceDeep}
          emissive={COLORS.spaceDeep.clone().multiplyScalar(0.1)}
          metalness={0.3}
          roughness={0.7}
          transparent
          opacity={0.85}
        />
      </mesh>

      {/* Gold Border Glow */}
      <mesh
        ref={borderRef}
        position={[position[0], position[1], position[2] + 0.01]}
      >
        <boxGeometry args={[cardWidth + 0.02, cardHeight + 0.02, cardThickness + 0.01]} />
        <meshStandardMaterial
          ref={borderMaterialRef}
          color={COLORS.goldPrimary}
          emissive={COLORS.goldBright}
          emissiveIntensity={0.2}
          transparent
          opacity={0.3}
          side={1} // BackSide for border effect
        />
      </mesh>

      {/* Content Text */}
      <Text
        position={[position[0], position[1], position[2] + 0.06]}
        fontSize={0.12}
        color={COLORS.silver.getHex()}
        anchorX="center"
        anchorY="middle"
        maxWidth={cardWidth - 0.2}
        textAlign="center"
      >
        {content}
      </Text>
    </group>
  );
}

