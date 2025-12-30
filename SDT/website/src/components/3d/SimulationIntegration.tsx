/**
 * Creative Agent: Simulation Integration Component
 * 
 * TEKNE: Simulation IS visualization, visualization IS understanding
 * Integrates physics simulations into 3D space
 * 
 * Design Philosophy:
 * - Simulations exist in the same space as content
 * - Pressure field visualizations are part of the environment
 * - Interactive controls are spatial, not UI overlays
 */

/**
 * Creative Agent: Simulation Integration Component
 * 
 * TEKNE: Simulation IS visualization, visualization IS understanding
 * Marks simulation positions in 3D space
 * 
 * Note: Actual simulations render in HTML (see SimulationViewer)
 * This component provides a 3D marker/indicator for simulation positions
 */

import React, { useRef } from 'react';
import { Group, Mesh } from 'three';
import { useFrame } from '@react-three/fiber';
import { ErrorBoundary } from '../../framework';

export interface SimulationIntegrationProps {
  simulationId?: string;
  position?: [number, number, number];
  visible?: boolean;
  parameters?: Record<string, any>;
  onReady?: () => void;
}

/**
 * SimulationIntegration - Marks simulation positions in 3D space
 * 
 * Features:
 * - Visual indicator for simulation location
 * - Pulsing animation to draw attention
 * - Gold glow matching design system
 * - Integrates with EnhancedNodeRoom
 */
export default function SimulationIntegration({
  simulationId,
  position = [0, 0, 0],
  visible = true,
  parameters = {},
  onReady,
}: SimulationIntegrationProps) {
  const groupRef = useRef<Group>(null);
  const indicatorRef = useRef<Mesh>(null);

  // Pulsing animation
  useFrame((state) => {
    if (indicatorRef.current && visible) {
      const time = state.clock.elapsedTime;
      const scale = 1.0 + Math.sin(time * 2) * 0.1;
      indicatorRef.current.scale.setScalar(scale);
    }
  });

  if (!visible || !simulationId) return null;

  return (
    <ErrorBoundary>
      <group ref={groupRef} position={position}>
        {/* Visual indicator for simulation position */}
        <mesh ref={indicatorRef}>
          <sphereGeometry args={[0.3, 16, 16]} />
          <meshStandardMaterial
            color={0xd69e2e}
            emissive={0xd69e2e}
            emissiveIntensity={0.5}
            transparent
            opacity={0.6}
          />
        </mesh>
        {/* Outer glow ring */}
        <mesh>
          <ringGeometry args={[0.35, 0.45, 32]} />
          <meshStandardMaterial
            color={0xd69e2e}
            emissive={0xd69e2e}
            emissiveIntensity={0.3}
            transparent
            opacity={0.4}
            side={2}
          />
        </mesh>
      </group>
    </ErrorBoundary>
  );
}

