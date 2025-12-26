/**
 * Codemonkey Agent: Node Room Component
 * Enhanced 3D visualization using framework geometry system
 * Production-ready, no stubs
 */

import React, { useRef, useEffect, useState, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Mesh, MeshStandardMaterial, Color, BufferGeometry } from 'three';
import * as THREE from 'three';
import { Text } from '@react-three/drei';
import { gsap } from 'gsap';
import { NodeContent } from '../../types/content';
import { useNavigationStore } from '../../store/navigationStore';
import { geometryRegistry, geometryToThreeJS } from '../../framework';

export interface NodeRoomProps {
  nodeId: string;
  position: [number, number, number];
  content: NodeContent;
  onEnter?: () => void;
  onExit?: () => void;
}

/**
 * NodeRoom - 3D toroidal chamber representing a content node
 * 
 * Uses framework's custom geometry generator for toroidal chambers
 * Features:
 * - Toroidal chamber geometry (custom, no Three.js dependency)
 * - Hover/selection states with gold glow
 * - Click to navigate to node
 * - Visual connection indicators
 * - Performance optimized
 */
export default function NodeRoom({
  nodeId,
  position,
  content,
  onEnter,
  onExit,
}: NodeRoomProps) {
  const { currentNode, navigateToNode } = useNavigationStore();
  const [hovered, setHovered] = useState(false);
  const [selected, setSelected] = useState(false);
  const [mounted, setMounted] = useState(false);
  const roomRef = useRef<Mesh>(null);
  const materialRef = useRef<MeshStandardMaterial>(null);
  const innerRef = useRef<Mesh>(null);
  const innerMaterialRef = useRef<MeshStandardMaterial>(null);

  // Generate toroidal chamber geometry using framework
  const chamberGeometry = useMemo(() => {
    const geometry = geometryRegistry.generate('toroidal-chamber', {
      innerRadius: 0.3,
      outerRadius: 1.0,
      height: 1.0,
      radialSegments: 24,
      tubularSegments: 32,
    });
    return geometryToThreeJS(geometry);
  }, []);

  // Inner indicator geometry
  const innerGeometry = useMemo(() => {
    const geometry = geometryRegistry.generate('toroidal-chamber', {
      innerRadius: 0.2,
      outerRadius: 0.6,
      height: 0.8,
      radialSegments: 16,
      tubularSegments: 24,
    });
    return geometryToThreeJS(geometry);
  }, []);

  // Update selection state
  useEffect(() => {
    setSelected(currentNode === nodeId);
  }, [currentNode, nodeId]);

  // Mount animation
  useEffect(() => {
    if (!roomRef.current) return;
    
    setMounted(true);
    
    // Entry animation
    roomRef.current.scale.set(0, 0, 0);
    gsap.to(roomRef.current.scale, {
      x: 1,
      y: 1,
      z: 1,
      duration: 0.8,
      ease: 'back.out(1.7)',
      delay: 0.1,
    });
  }, []);

  // Animate on selection/hover
  useEffect(() => {
    if (!roomRef.current || !materialRef.current || !mounted) return;

    if (selected) {
      // Selected: Scale up, bright gold glow
      gsap.to(roomRef.current.scale, {
        x: 1.25,
        y: 1.25,
        z: 1.25,
        duration: 0.5,
        ease: 'power2.out',
      });
      gsap.to(materialRef.current, {
        emissiveIntensity: 2.0,
        opacity: 1,
        duration: 0.5,
      });
      if (innerMaterialRef.current) {
        gsap.to(innerMaterialRef.current, {
          emissiveIntensity: 1.5,
          opacity: 0.5,
          duration: 0.5,
        });
      }
    } else if (hovered) {
      // Hovered: Slight scale, increased glow
      gsap.to(roomRef.current.scale, {
        x: 1.1,
        y: 1.1,
        z: 1.1,
        duration: 0.3,
        ease: 'power2.out',
      });
      gsap.to(materialRef.current, {
        emissiveIntensity: 1.0,
        duration: 0.3,
      });
    } else {
      // Normal: Return to base
      gsap.to(roomRef.current.scale, {
        x: 1,
        y: 1,
        z: 1,
        duration: 0.3,
        ease: 'power2.out',
      });
      gsap.to(materialRef.current, {
        emissiveIntensity: 0.3,
        opacity: 0.6,
        duration: 0.3,
      });
      if (innerMaterialRef.current) {
        gsap.to(innerMaterialRef.current, {
          emissiveIntensity: 0.2,
          opacity: 0.3,
          duration: 0.3,
        });
      }
    }
  }, [selected, hovered, mounted]);

  // Subtle floating animation
  useFrame((state) => {
    if (!roomRef.current) return;
    const time = state.clock.elapsedTime;
    const floatAmount = Math.sin(time * 0.5 + position[0] * 0.5) * 0.1;
    roomRef.current.position.y = position[1] + floatAmount;
    
    // Subtle rotation
    roomRef.current.rotation.y = Math.sin(time * 0.3 + position[2] * 0.5) * 0.1;
  });

  const handleClick = () => {
    navigateToNode(nodeId);
    if (onEnter) onEnter();
  };

  // Color based on path
  const getPathColor = (path: string): Color => {
    switch (path) {
      case 'path1':
        return new Color(0x4299e1); // Light blue
      case 'path2':
        return new Color(0x2d5a87); // Medium blue
      case 'path3':
        return new Color(0x1a365d); // Deep blue
      default:
        return new Color(0x4a90e2);
    }
  };

  const baseColor = getPathColor(content.path);
  const emissiveColor = selected 
    ? new Color(0xd69e2e) // Gold when selected
    : baseColor.clone().multiplyScalar(0.5);

  const innerEmissiveColor = selected
    ? new Color(0xf6ad55) // Bright gold when selected
    : baseColor.clone().multiplyScalar(0.3);

  return (
    <group position={position}>
      {/* Main toroidal chamber */}
      <mesh
        ref={roomRef}
        geometry={chamberGeometry}
        onClick={handleClick}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <meshStandardMaterial
          ref={materialRef}
          color={selected ? new Color(0xd69e2e) : baseColor}
          emissive={emissiveColor}
          emissiveIntensity={0.3}
          metalness={0.7}
          roughness={0.3}
          transparent
          opacity={0.6}
        />
      </mesh>

      {/* Inner content indicator */}
      <mesh
        ref={innerRef}
        geometry={innerGeometry}
        position={[0, 0, 0]}
      >
        <meshStandardMaterial
          ref={innerMaterialRef}
          color={baseColor}
          emissive={innerEmissiveColor}
          emissiveIntensity={selected ? 1.5 : 0.2}
          transparent
          opacity={selected ? 0.5 : 0.3}
        />
      </mesh>

      {/* Node title label */}
      <Text
        position={[0, 1.5, 0]}
        fontSize={0.2}
        color={selected ? '#d69e2e' : '#ffffff'}
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.02}
        outlineColor="#000000"
        maxWidth={3}
        textAlign="center"
      >
        {content.title}
      </Text>

      {/* Reading time indicator */}
      <Text
        position={[0, -1.5, 0]}
        fontSize={0.1}
        color="#94a3b8"
        anchorX="center"
        anchorY="middle"
      >
        {content.readingTime} min
      </Text>

      {/* Connection indicator (arrow pointing to next node) */}
      {content.nextNodeId && (
        <mesh position={[1.2, 0, 0]} rotation={[0, 0, -Math.PI / 2]}>
          <coneGeometry args={[0.05, 0.2, 8]} />
          <meshStandardMaterial
            color={baseColor}
            emissive={baseColor}
            emissiveIntensity={0.5}
          />
        </mesh>
      )}
    </group>
  );
}
