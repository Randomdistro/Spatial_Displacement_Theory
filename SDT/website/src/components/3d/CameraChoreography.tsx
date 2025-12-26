/**
 * Creative Agent: Camera Choreography Component
 * 
 * TEKNE: Camera movement IS understanding
 * Orbital motion, arrival effects, idle breathing
 * 
 * Design Philosophy:
 * - Transition motion: Orbital arc (not linear)
 * - Arrival: Slight overshoot, settle back
 * - Idle: Subtle orbital motion, breathing
 * - Smooth, organic, never jarring
 */

import React, { useRef, useEffect } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import { PerspectiveCamera, Vector3 } from 'three';
import { gsap } from 'gsap';
import { CameraPathGenerator, EasingFunctions } from '../../framework';
import { useNavigationStore } from '../../store/navigationStore';

export interface CameraChoreographyProps {
  targetPosition?: Vector3;
  targetLookAt?: Vector3;
  duration?: number;
}

/**
 * CameraChoreography - Enhanced camera system
 * 
 * Features:
 * - Orbital arc transitions (Catmull-Rom splines)
 * - Arrival overshoot effect
 * - Idle orbital motion (0.1 RPM)
 * - Breathing effect (distance: 4 ± 0.2 units)
 * - Smooth, organic easing
 */
export default function CameraChoreography({
  targetPosition,
  targetLookAt,
  duration = 3500,
}: CameraChoreographyProps) {
  const { camera } = useThree();
  const { isTransitioning, cameraPosition, cameraTarget } = useNavigationStore();
  const cameraRef = useRef(camera as PerspectiveCamera);
  const isIdleRef = useRef(true);
  const transitionStartRef = useRef(0);
  const startPositionRef = useRef<Vector3>(new Vector3());
  const startLookAtRef = useRef<Vector3>(new Vector3());
  const pathRef = useRef<Vector3[]>([]);

  // Initialize camera
  useEffect(() => {
    cameraRef.current = camera as PerspectiveCamera;
    startPositionRef.current.copy(camera.position);
    startLookAtRef.current.copy(camera.position.clone().add(new Vector3(0, 0, -1)));
  }, [camera]);

  // Start transition
  useEffect(() => {
    if (!isTransitioning || !targetPosition || !targetLookAt) {
      isIdleRef.current = true;
      return;
    }

    isIdleRef.current = false;
    transitionStartRef.current = performance.now();
    
    // Store start position
    startPositionRef.current.copy(camera.position);
    
    // Calculate look-at direction
    const lookDirection = new Vector3().subVectors(
      camera.position.clone().add(new Vector3(0, 0, -1)),
      camera.position
    ).normalize();
    startLookAtRef.current.copy(camera.position.clone().add(lookDirection));

    // Generate orbital path
    const currentPos = camera.position.clone();
    const midPoint = new Vector3().addVectors(currentPos, targetPosition).multiplyScalar(0.5);
    midPoint.y += 1.0; // Arc upward
    
    pathRef.current = CameraPathGenerator.generatePath(
      [currentPos, midPoint, targetPosition],
      50
    );
  }, [isTransitioning, targetPosition, targetLookAt, camera]);

  // Camera update loop
  useFrame((state) => {
    const now = performance.now();
    
    if (!isIdleRef.current && pathRef.current.length > 0) {
      // Transition animation
      const elapsed = now - transitionStartRef.current;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = EasingFunctions.organic(progress);
      
      // Get position along path
      const pathIndex = Math.floor(easedProgress * (pathRef.current.length - 1));
      const currentPathPos = pathRef.current[pathIndex];
      
      if (currentPathPos) {
        camera.position.copy(currentPathPos);
        
        // Look at target (smooth interpolation)
        const lookAtTarget = targetLookAt || cameraTarget;
        const lookAt = new Vector3().lerpVectors(
          startLookAtRef.current,
          lookAtTarget,
          easedProgress
        );
        
        camera.lookAt(lookAt);
      }
      
      // Arrival effect (slight overshoot, then settle)
      if (progress >= 1) {
        // Overshoot
        const overshootProgress = Math.min((elapsed - duration) / 500, 1);
        if (overshootProgress < 1) {
          const overshootScale = 1.05 - (overshootProgress * 0.05);
          const direction = new Vector3().subVectors(
            targetPosition!,
            startPositionRef.current
          );
          camera.position.copy(startPositionRef.current.clone().add(
            direction.multiplyScalar(overshootScale)
          ));
        } else {
          // Settle to final position
          camera.position.copy(targetPosition!);
          camera.lookAt(targetLookAt || cameraTarget);
          isIdleRef.current = true;
        }
      }
    } else if (isIdleRef.current) {
      // Idle: Subtle orbital motion and breathing
      const time = state.clock.elapsedTime;
      
      // Orbital motion (0.1 RPM = 0.1 * 2π / 60 radians per second)
      const orbitalSpeed = (0.1 * Math.PI * 2) / 60;
      const angle = time * orbitalSpeed;
      
      // Current distance from target
      const target = targetLookAt || cameraTarget;
      const currentDistance = camera.position.distanceTo(target);
      const baseDistance = 4.0;
      
      // Breathing effect (distance: 4 ± 0.2 units, 8s cycle)
      const breath = Math.sin(time * (Math.PI / 4)) * 0.2;
      const targetDistance = baseDistance + breath;
      
      // Orbital position
      const orbitalRadius = targetDistance;
      const x = Math.cos(angle) * orbitalRadius;
      const z = Math.sin(angle) * orbitalRadius;
      
      // Smooth interpolation to orbital position
      const orbitalPos = target.clone().add(new Vector3(x, 0.5, z));
      camera.position.lerp(orbitalPos, 0.05);
      camera.lookAt(target);
    }
  });

  return null; // This component only manages camera, doesn't render
}


