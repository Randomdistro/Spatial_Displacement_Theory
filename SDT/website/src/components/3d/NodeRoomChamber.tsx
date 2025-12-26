/**
 * Creative Agent: Node Room Chamber Component
 * 
 * TEKNE: The space IS the concept, the concept IS the space
 * A 3D "chamber" that is the concept space itself
 * 
 * Design Philosophy:
 * - Volumetric space defined by pressure field boundaries
 * - Spatial representation of conceptual structure
 * - Subtle, subdued, visceral
 * - The obviousness, effortlessly revealed
 */

import React, { useRef, useEffect, useState, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Mesh, MeshStandardMaterial, Color, Vector3, PointLight, AmbientLight, DirectionalLight } from 'three';
import { Text } from '@react-three/drei';
import { gsap } from 'gsap';
import { NodeContent } from '../../types/content';
import { useGeometry, useAnimation, EasingFunctions } from '../../framework/hooks';
import { ErrorBoundary } from '../../framework';

// Design system colors - Creative Agent
const COLORS = {
  spaceDeep: new Color(0x1a365d),      // Deep Space Blue
  spaceMedium: new Color(0x2d5a87),    // Medium Blue
  spaceLight: new Color(0x4299e1),      // Light Blue
  goldPrimary: new Color(0xd69e2e),     // Metallic Gold
  goldBright: new Color(0xf6ad55),      // Bright Gold
  goldLight: new Color(0xfbbf24),       // Light Gold
  silver: new Color(0xcbd5e0),           // Subtle Silver
  eclipse: new Color(0x0f172a),         // Eclipse Shadow
} as const;

export interface NodeRoomChamberProps {
  nodeId: string;
  position: [number, number, number];
  content: NodeContent;
  onEnter?: () => void;
  onExit?: () => void;
  visible?: boolean;
}

/**
 * NodeRoomChamber - Creative Agent Enhanced
 * 
 * A toroidal chamber that IS the concept space
 * Features:
 * - Toroidal geometry (using framework generator)
 * - Pressure field visualization (volumetric gradient)
 * - Matter exclusion zones (content cards)
 * - Gold flow lines (pressure direction)
 * - Organic animations (breathing, materialization)
 * - Proper lighting (ambient, directional, point lights)
 * - Glassmorphism content surfaces
 */
export default function NodeRoomChamber({
  nodeId,
  position,
  content,
  onEnter,
  onExit,
  visible = true,
}: NodeRoomChamberProps) {
  const [mounted, setMounted] = useState(false);
  const [isEntered, setIsEntered] = useState(false);
  const chamberRef = useRef<Mesh>(null);
  const pressureFieldRef = useRef<Mesh>(null);
  const materialRef = useRef<MeshStandardMaterial>(null);
  const pressureMaterialRef = useRef<MeshStandardMaterial>(null);

  // Generate toroidal chamber geometry using framework
  const { geometry: chamberGeometry } = useGeometry({
    generator: 'toroidal-chamber',
    params: {
      innerRadius: 2,      // Concept core
      outerRadius: 4,       // Concept boundary
      height: 3,            // Conceptual depth
      radialSegments: 32,
      tubularSegments: 64,
    },
  });

  // Entry animation - Chamber materializes from pressure field
  const { play: playEntryAnimation } = useAnimation({
    sequences: [
      {
        id: 'chamber-materialize',
        duration: 1500,
        easing: EasingFunctions.organic,
        onStart: () => {
          setMounted(true);
          if (chamberRef.current) {
            chamberRef.current.scale.set(0, 0, 0);
          }
        },
        onUpdate: (progress) => {
          if (chamberRef.current) {
            // Scale with slight overshoot
            const scale = progress < 1 ? progress * 1.05 : 1.0;
            chamberRef.current.scale.set(scale, scale, scale);
          }
          if (materialRef.current) {
            materialRef.current.opacity = progress * 0.15;
          }
        },
        onComplete: () => {
          if (onEnter) onEnter();
          setIsEntered(true);
        },
      },
    ],
    autoPlay: visible,
  });

  // Idle breathing animation - Pressure field pulses
  useFrame((state) => {
    if (!mounted || !isEntered) return;

    const time = state.clock.elapsedTime;
    
    // Breathing effect: scale 1 ± 0.03, 4s cycle
    if (pressureFieldRef.current) {
      const breath = Math.sin(time * (Math.PI / 2)) * 0.03;
      pressureFieldRef.current.scale.setScalar(1 + breath);
    }

    // Subtle chamber rotation
    if (chamberRef.current) {
      chamberRef.current.rotation.y = Math.sin(time * 0.1) * 0.05;
    }
  });

  // Exit animation - Dissolve into pressure field
  const playExitAnimation = () => {
    if (!chamberRef.current || !materialRef.current) return;

    gsap.to(chamberRef.current.scale, {
      x: 0.9,
      y: 0.9,
      z: 0.9,
      duration: 1.0,
      ease: 'power2.in',
    });

    gsap.to(materialRef.current, {
      opacity: 0,
      duration: 1.0,
      ease: 'power2.in',
      onComplete: () => {
        if (onExit) onExit();
      },
    });
  };

  useEffect(() => {
    if (!visible && mounted) {
      playExitAnimation();
    }
  }, [visible, mounted]);

  // Color based on path
  const getPathColor = (path: string): Color => {
    switch (path) {
      case 'path1':
        return COLORS.spaceLight;    // Lighter blue - accessible
      case 'path2':
        return COLORS.spaceMedium;   // Medium blue - balanced
      case 'path3':
        return COLORS.spaceDeep;     // Deep blue - contemplative
      default:
        return COLORS.spaceMedium;
    }
  };

  const baseColor = getPathColor(content.path);
  const emissiveColor = baseColor.clone().multiplyScalar(0.2);

  if (!chamberGeometry || !visible) return null;

  return (
    <ErrorBoundary>
      <group position={position}>
        {/* Lighting Setup - Creative Agent Design */}
        <AmbientLight intensity={0.3} />
        <DirectionalLight position={[0, 5, 0]} intensity={0.6} />
        <PointLight position={[0, 0, 0]} intensity={0.4} color={COLORS.goldPrimary} />
        
        {/* Pressure Field Visualization - Volumetric gradient */}
        <mesh ref={pressureFieldRef}>
          <sphereGeometry args={[3.5, 32, 32]} />
          <meshStandardMaterial
            ref={pressureMaterialRef}
            color={COLORS.spaceDeep}
            emissive={COLORS.spaceLight}
            emissiveIntensity={0.2}
            transparent
            opacity={0.3}
            side={2} // DoubleSide
          />
        </mesh>

        {/* Main Toroidal Chamber */}
        <mesh
          ref={chamberRef}
          geometry={chamberGeometry}
        >
          <meshStandardMaterial
            ref={materialRef}
            color={baseColor}
            emissive={emissiveColor}
            emissiveIntensity={0.1}
            metalness={0.6}
            roughness={0.4}
            transparent
            opacity={0.15}
            side={2} // DoubleSide
          />
        </mesh>

        {/* Gold Edge Glow - Rim lighting */}
        <mesh geometry={chamberGeometry} scale={[1.02, 1.02, 1.02]}>
          <meshStandardMaterial
            color={COLORS.goldPrimary}
            emissive={COLORS.goldBright}
            emissiveIntensity={0.3}
            transparent
            opacity={0.1}
            side={1} // BackSide only for rim effect
          />
        </mesh>

        {/* Node Title - Floating in space */}
        <Text
          position={[0, 2, 0]}
          fontSize={0.3}
          color={COLORS.goldPrimary.getHex()}
          anchorX="center"
          anchorY="middle"
          outlineWidth={0.02}
          outlineColor="#000000"
          maxWidth={4}
          textAlign="center"
          font="/fonts/inter-bold.woff"
        >
          {content.title}
        </Text>

        {/* Reading Time Indicator */}
        <Text
          position={[0, -2.5, 0]}
          fontSize={0.15}
          color={COLORS.silver.getHex()}
          anchorX="center"
          anchorY="middle"
        >
          {content.readingTime} min read
        </Text>
      </group>
    </ErrorBoundary>
  );
}

