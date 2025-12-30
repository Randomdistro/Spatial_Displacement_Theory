import React, { useRef, useMemo, useState, useEffect } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import { Mesh, TorusGeometry, MeshStandardMaterial, Color, Vector3 } from 'three';
import * as THREE from 'three';
import { gsap } from 'gsap';
import { 
  flowerOfLifeCircles, 
  seedOfLife, 
  PHI, 
  PHI_INVERSE,
  GOLDEN_ANGLE 
} from '../../utils/sacred-geometry';

// Design system colors - Creative Agent
const COLORS = {
  spaceDeep: new Color(0x1a365d),      // Deep Space Blue
  spaceMedium: new Color(0x2d5a87),    // Medium Blue
  spaceLight: new Color(0x4299e1),      // Light Blue
  goldPrimary: new Color(0xd69e2e),     // Metallic Gold
  goldBright: new Color(0xf6ad55),      // Bright Gold
  goldLight: new Color(0xfbbf24),       // Light Gold
  silver: new Color(0xcbd5e0),           // Subtle Silver
} as const;

export interface FlowerOfLifeProps {
  onPathSelect: (pathId: 'path1' | 'path2' | 'path3') => void;
  isTransitioning?: boolean;
}

/**
 * Flower of Life component - Creative Agent Enhanced
 * 
 * Sacred geometry pattern with interleaved rings creating hexagonal Flower of Life.
 * Subtle, subdued, visceral. The obviousness of it all, effortlessly revealed.
 * 
 * Design Philosophy:
 * - Geometry sings: Every shape has meaning
 * - Subtle, not shy: Colors whisper, gold glimmers
 * - Visceral understanding: Users feel the flow
 * - The obviousness: When right, it's obvious
 * 
 * Enhanced by Creative Agent with:
 * - Design system colors (Deep Space Blue, Metallic Gold)
 * - Organic, flowing animations
 * - Subtle breathing/pulsing effects
 * - Gold gradient on selection (revelation)
 * - True sacred geometry pattern
 */
export default function FlowerOfLife({
  onPathSelect,
  isTransitioning = false,
}: FlowerOfLifeProps) {
  const [hoveredRing, setHoveredRing] = useState<number | null>(null);
  const [selectedPath, setSelectedPath] = useState<'path1' | 'path2' | 'path3' | null>(null);
  const ringsRef = useRef<(Mesh | null)[]>([]);
  const { camera, gl } = useThree();

  // Touch gesture handling for mobile
  const touchStartRef = useRef<{ x: number; y: number } | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  // Flower of Life ring configuration
  // Path 1: rings 0-2 (3 rings, lighter blue, faster rotation)
  // Path 2: rings 3-9 (7 rings, medium blue, moderate rotation)
  // Path 3: rings 10-22 (13 rings, darker blue, slower rotation)
  const ringConfig = useMemo(() => {
    const configs = [];
    const baseRadius = 1;
    const ringThickness = 0.02;
    const ringSegments = 64;

    // Path 1 rings (3 rings) - Lighter, faster, more accessible
    // True Flower of Life pattern: interleaved circles creating hexagons
    for (let i = 0; i < 3; i++) {
      const angle = (i * 2 * Math.PI) / 3;
      const radius = baseRadius * (0.9 + i * 0.15);
      configs.push({
        id: i,
        path: 'path1' as const,
        radius: radius,
        position: [
          Math.cos(angle) * 0.5,
          Math.sin(angle) * 0.3,
          Math.sin(i * 0.5) * 0.1, // Slight depth variation
        ] as [number, number, number],
        rotationSpeed: 0.6 + i * 0.1, // Faster rotation - accessible feel
        color: COLORS.spaceLight.clone(), // Lighter blue - more inviting
        scale: 1,
        baseEmissive: 0.08, // Subtle glow
      });
    }

    // Path 2 rings (7 rings) - Medium weight, balanced
    for (let i = 0; i < 7; i++) {
      const angle = (i * 2 * Math.PI) / 7;
      const radius = baseRadius * (1.1 + i * 0.1);
      configs.push({
        id: i + 3,
        path: 'path2' as const,
        radius: radius,
        position: [
          Math.cos(angle) * 0.8,
          Math.sin(angle) * 0.5,
          Math.sin(i * 0.7) * 0.15, // More depth variation
        ] as [number, number, number],
        rotationSpeed: 0.5 + i * 0.05, // Moderate rotation - balanced
        color: COLORS.spaceMedium.clone(), // Medium blue - balanced
        scale: 1,
        baseEmissive: 0.1, // Slightly more glow
      });
    }

    // Path 3 rings (13 rings) - Heavier, slower, contemplative
    for (let i = 0; i < 13; i++) {
      const angle = (i * 2 * Math.PI) / 13;
      const radius = baseRadius * (1.3 + i * 0.08);
      configs.push({
        id: i + 10,
        path: 'path3' as const,
        radius: radius,
        position: [
          Math.cos(angle) * 1.2,
          Math.sin(angle) * 0.7,
          Math.sin(i * 0.9) * 0.2, // Most depth variation
        ] as [number, number, number],
        rotationSpeed: 0.4 + i * 0.03, // Slower rotation - contemplative
        color: COLORS.spaceDeep.clone(), // Deep blue - serious, profound
        scale: 1,
        baseEmissive: 0.12, // Strongest base glow
      });
    }

    return configs;
  }, []);

  // Create ring geometries and materials
  const rings = useMemo(() => {
    return ringConfig.map((config) => {
      const geometry = new TorusGeometry(
        config.radius,
        0.02, // thickness
        16, // radial segments
        64 // tubular segments
      );
      // Enhanced material - Creative Agent design system
      const material = new MeshStandardMaterial({
        color: config.color,
        metalness: 0.8, // Subtle metallic sheen
        roughness: 0.2, // Smooth but not mirror
        emissive: config.color.clone().multiplyScalar(config.baseEmissive || 0.1),
        emissiveIntensity: 1,
        transparent: true,
        opacity: 1,
      });

      return { geometry, material, config };
    });
  }, [ringConfig]);

  // Touch gesture handling for mobile
  useEffect(() => {
    const canvas = gl.domElement;
    let touchStartPos: { x: number; y: number } | null = null;
    let isDragging = false;

    const handleTouchStart = (e: TouchEvent) => {
      if (e.touches.length === 1) {
        isDragging = true;
        touchStartPos = {
          x: e.touches[0].clientX,
          y: e.touches[0].clientY
        };
      }
    };

    const handleTouchMove = (e: TouchEvent) => {
      if (!isDragging || !touchStartPos) return;
      e.preventDefault();

      if (e.touches.length === 1) {
        // Single finger: rotate camera
        const deltaX = e.touches[0].clientX - touchStartPos.x;
        const deltaY = e.touches[0].clientY - touchStartPos.y;

        camera.rotation.y -= deltaX * 0.005;
        camera.rotation.x -= deltaY * 0.005;

        touchStartPos = {
          x: e.touches[0].clientX,
          y: e.touches[0].clientY
        };
      } else if (e.touches.length === 2) {
        // Two fingers: pinch to zoom
        const touch1 = e.touches[0];
        const touch2 = e.touches[1];
        const currentDistance = Math.sqrt(
          Math.pow(touch2.clientX - touch1.clientX, 2) +
          Math.pow(touch2.clientY - touch1.clientY, 2)
        );

        // Simple zoom
        const zoomSpeed = 0.02;
        camera.position.z = Math.max(2, Math.min(10, camera.position.z + (300 - currentDistance) * zoomSpeed));
      }
    };

    const handleTouchEnd = () => {
      isDragging = false;
      touchStartPos = null;
    };

    canvas.addEventListener('touchstart', handleTouchStart, { passive: false });
    canvas.addEventListener('touchmove', handleTouchMove, { passive: false });
    canvas.addEventListener('touchend', handleTouchEnd);

    return () => {
      canvas.removeEventListener('touchstart', handleTouchStart);
      canvas.removeEventListener('touchmove', handleTouchMove);
      canvas.removeEventListener('touchend', handleTouchEnd);
    };
  }, [camera, gl]);

  // Enhanced animation loop - Sacred Geometry: Golden Ratio Motion
  useFrame((state, delta) => {
    rings.forEach((ring, index) => {
      const mesh = ringsRef.current[index];
      if (!mesh) return;

      const config = ringConfig[index];
      const material = mesh.material as MeshStandardMaterial;
      const time = state.clock.elapsedTime;

      // Idle rotation - golden ratio frequencies
      if (!isTransitioning && selectedPath === null) {
        // Rotation speed based on golden ratio harmonics
        const goldenFreq = config.rotationSpeed * PHI_INVERSE;
        mesh.rotation.y += (goldenFreq * delta) / 8;
        
        // Breathing uses golden ratio phase offset
        // Each ring breathes at slightly different phase for organic feel
        const phase = index * GOLDEN_ANGLE;
        const breath = Math.sin(time * PHI_INVERSE + phase) * 0.04;
        
        // Rotation axes use golden ratio proportions
        mesh.rotation.x = Math.sin(time * PHI_INVERSE * 0.5 + phase) * 0.08 + breath;
        mesh.rotation.z = Math.cos(time * PHI_INVERSE * 0.4 + phase * PHI) * 0.04;
        
        // Scale breathing with golden ratio amplitude
        const scaleBreath = 1 + Math.sin(time * PHI_INVERSE * 0.6 + phase) * PHI_INVERSE * 0.03;
        mesh.scale.setScalar(scaleBreath);
      }

      // Hover effect - smooth, organic
      if (hoveredRing === index) {
        // Smooth scale with organic easing
        gsap.to(mesh.scale, {
          x: 1.12,
          y: 1.12,
          z: 1.12,
          duration: 0.4,
          ease: 'power2.out',
        });
        
        // Gold glow on hover - revelation
        const goldEmissive = COLORS.goldPrimary.clone().multiplyScalar(0.3);
        gsap.to(material, {
          emissive: goldEmissive,
          emissiveIntensity: 1.5,
          duration: 0.4,
          ease: 'power2.out',
        });
      } else if (selectedPath !== config.path || !isTransitioning) {
        // Return to normal - smooth
        gsap.to(mesh.scale, {
          x: config.scale,
          y: config.scale,
          z: config.scale,
          duration: 0.4,
          ease: 'power2.out',
        });
        
        // Return to base emissive
        const baseEmissive = config.color.clone().multiplyScalar(config.baseEmissive || 0.1);
        gsap.to(material, {
          emissive: baseEmissive,
          emissiveIntensity: 1,
          duration: 0.4,
          ease: 'power2.out',
        });
      }

      // Selection animation - refined, beautiful
      if (selectedPath === config.path && isTransitioning) {
        // Phase 1: Scale up selected with gold glow
        gsap.to(mesh.scale, {
          x: 1.25,
          y: 1.25,
          z: 1.25,
          duration: 0.6,
          ease: 'power2.out',
        });
        
        // Gold gradient on selection - the revelation
        const goldGradient = COLORS.goldBright.clone();
        gsap.to(material, {
          emissive: goldGradient,
          emissiveIntensity: 2,
          color: COLORS.goldPrimary,
          duration: 0.6,
          ease: 'power2.out',
        });
        
        gsap.to(material, {
          opacity: 1,
          duration: 0.6,
        });
      } else if (selectedPath !== null && selectedPath !== config.path && isTransitioning) {
        // Fade others - subtle
        gsap.to(material, {
          opacity: 0.2,
          duration: 0.6,
          ease: 'power2.out',
        });
      }

      // Phase 2: Flip and rotate - organic motion
      if (selectedPath === config.path && isTransitioning && time > 0.6) {
        const flipProgress = Math.min((time - 0.6) / 1.0, 1);
        mesh.rotation.x = Math.PI * flipProgress;
        mesh.rotation.y += delta * 2; // Continuous rotation
      }
    });
  });

  const getPathDescription = (pathId: 'path1' | 'path2' | 'path3'): string => {
    switch (pathId) {
      case 'path1':
        return 'Quick Tour: 5-minute overview of Spatial Displacement Theory';
      case 'path2':
        return 'Deep Dive: Comprehensive exploration of all concepts';
      case 'path3':
        return 'Scientific Framework: Rigorous physics and mathematics';
      default:
        return 'Navigation path';
    }
  };

  const handleClick = (pathId: 'path1' | 'path2' | 'path3') => {
    if (isTransitioning) return;
    setSelectedPath(pathId);

    // Smooth transition trigger
    rings.forEach((ring, index) => {
      const mesh = ringsRef.current[index];
      if (!mesh) return;
      const config = ringConfig[index];

      if (config.path === pathId) {
        // Selected rings get gold treatment immediately
        const material = mesh.material as MeshStandardMaterial;
        const goldGradient = COLORS.goldBright.clone();
        gsap.to(material, {
          emissive: goldGradient,
          emissiveIntensity: 2,
          duration: 0.3,
          ease: 'power2.out',
        });
      }
    });

    onPathSelect(pathId);
  };

  return (
    <group>
      {rings.map((ring, index) => {
        const config = ringConfig[index];
        return (
          <mesh
            key={config.id}
            ref={(el) => {
              if (el) ringsRef.current[index] = el;
            }}
            geometry={ring.geometry}
            material={ring.material}
            position={config.position}
            onPointerOver={() => setHoveredRing(index)}
            onPointerOut={() => setHoveredRing(null)}
            onClick={() => handleClick(config.path)}
            role="button"
            aria-label={`Navigate to ${getPathDescription(config.path)}`}
            aria-describedby={`path-${config.path}-description`}
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                handleClick(config.path);
              }
            }}
          />
        );
      })}
    </group>
  );
}

