import { useThree } from '@react-three/fiber';
import { useRef, useEffect } from 'react';
import * as THREE from 'three';
import { gsap } from 'gsap';

export interface CameraControllerProps {
  targetPosition: [number, number, number];
  targetLookAt: [number, number, number];
  duration?: number;
  onTransitionComplete?: () => void;
  enabled?: boolean;
}

/**
 * Camera controller component for smooth camera transitions
 * Uses GSAP for smooth animations
 * Note: This works with OrbitControls from drei by animating camera directly
 */
export default function CameraController({
  targetPosition,
  targetLookAt,
  duration = 3.5,
  onTransitionComplete,
  enabled = true,
}: CameraControllerProps) {
  const { camera, controls } = useThree();
  const isTransitioningRef = useRef(false);
  const animationRef = useRef<gsap.core.Tween | null>(null);

  useEffect(() => {
    if (!enabled || isTransitioningRef.current) return;

    isTransitioningRef.current = true;

    // Cancel any existing animation
    if (animationRef.current) {
      animationRef.current.kill();
    }

    const startPosition = new THREE.Vector3().copy(camera.position);
    const endPosition = new THREE.Vector3(...targetPosition);
    const endTarget = new THREE.Vector3(...targetLookAt);

    // Animate camera position
    const positionTween = gsap.to(camera.position, {
      x: endPosition.x,
      y: endPosition.y,
      z: endPosition.z,
      duration: duration,
      ease: 'power2.inOut',
      onUpdate: () => {
        camera.updateProjectionMatrix();
        // Update controls target if available
        if (controls && 'target' in controls) {
          const controlsTarget = controls.target as THREE.Vector3;
          gsap.to(controlsTarget, {
            x: endTarget.x,
            y: endTarget.y,
            z: endTarget.z,
            duration: duration,
            ease: 'power2.inOut',
          });
        } else {
          camera.lookAt(endTarget);
        }
      },
      onComplete: () => {
        isTransitioningRef.current = false;
        if (onTransitionComplete) {
          onTransitionComplete();
        }
      },
    });

    animationRef.current = positionTween;

    // Cleanup on unmount
    return () => {
      if (animationRef.current) {
        animationRef.current.kill();
      }
    };
  }, [targetPosition, targetLookAt, duration, enabled, camera, controls, onTransitionComplete]);

  return null;
}

