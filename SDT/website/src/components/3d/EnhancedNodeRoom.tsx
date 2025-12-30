/**
 * Creative Agent: Enhanced Node Room Component
 * 
 * TEKNE: The space IS the concept, the concept IS the space
 * Complete integration of all visual elements
 * 
 * Design Philosophy:
 * - Toroidal chamber IS the concept space
 * - Pressure field IS the medium
 * - Content cards ARE spatial entities
 * - Everything flows, everything breathes
 */

import React, { useRef, useState, useEffect, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Group, Vector3 } from 'three';
import { NodeContent } from '../../types/content';
import { useNavigationStore } from '../../store/navigationStore';
import { useAnimation, EasingFunctions } from '../../framework/hooks';
import { ErrorBoundary } from '../../framework';

// Import Creative Agent components
import NodeRoomChamber from './NodeRoomChamber';
import ContentCard from './ContentCard';
import ContentRenderer3D from './ContentRenderer3D';
import PressureFieldVisualization from './PressureFieldVisualization';
import AtmosphericEffects from './AtmosphericEffects';
import SimulationIntegration from './SimulationIntegration';

export interface EnhancedNodeRoomProps {
  nodeId: string;
  position: [number, number, number];
  content: NodeContent;
  onEnter?: () => void;
  onExit?: () => void;
  visible?: boolean;
}

/**
 * EnhancedNodeRoom - Complete visual integration
 * 
 * Features:
 * - Toroidal chamber (concept space)
 * - Pressure field visualization
 * - Content cards floating in space
 * - Atmospheric effects
 * - Smooth animations
 * - Proper lighting
 */
export default function EnhancedNodeRoom({
  nodeId,
  position,
  content,
  onEnter,
  onExit,
  visible = true,
}: EnhancedNodeRoomProps) {
  const { currentNode } = useNavigationStore();
  const [contentVisible, setContentVisible] = useState(false);
  const groupRef = useRef<Group>(null);
  const isActive = currentNode === nodeId;

  // Content appearance animation - Staggered
  const { play: playContentAnimation } = useAnimation({
    sequences: [
      {
        id: 'content-appear',
        duration: 2000,
        delay: 1500, // After chamber materializes
        easing: EasingFunctions.organic,
        onStart: () => {
          setContentVisible(true);
        },
      },
    ],
    autoPlay: visible && isActive,
  });

  // Content card positions (arranged in space)
  const cardPositions: [number, number, number][] = useMemo(() => {
    const positions: [number, number, number][] = [];
    const cardCount = 3; // Main content + 2 expansions
    
    // Arrange cards in a circle around center
    for (let i = 0; i < cardCount; i++) {
      const angle = (i / cardCount) * Math.PI * 2;
      const radius = 1.5;
      positions.push([
        Math.cos(angle) * radius,
        Math.sin(angle) * 0.5,
        Math.sin(angle) * radius,
      ]);
    }
    
    return positions;
  }, []);

  // Extract content for cards
  const mainContent = content.content.main.substring(0, 100) + '...';
  const expansionContent = content.content.expansions 
    ? Object.values(content.content.expansions).slice(0, 2).map(exp => 
        typeof exp === 'string' ? exp.substring(0, 80) + '...' : exp.content?.substring(0, 80) + '...' || ''
      )
    : [];

  if (!visible) return null;

  return (
    <ErrorBoundary>
      <group ref={groupRef} position={position}>
        {/* Atmospheric Effects */}
        <AtmosphericEffects
          particleCount={500}
          fogDensity={0.02}
          glowIntensity={0.3}
        />

        {/* Pressure Field Visualization */}
        <PressureFieldVisualization
          center={[0, 0, 0]}
          radius={3}
          density={0.6}
          showFlowLines={true}
        />

        {/* Toroidal Chamber */}
        <NodeRoomChamber
          nodeId={nodeId}
          position={[0, 0, 0]}
          content={content}
          onEnter={onEnter}
          onExit={onExit}
          visible={visible}
        />

        {/* Content Cards - Floating in space */}
        {contentVisible && (
          <>
            {/* Main content card */}
            <ContentCard
              content={mainContent}
              position={cardPositions[0]}
              index={0}
              visible={contentVisible}
            />

            {/* Expansion cards */}
            {expansionContent.map((expContent, index) => (
              <ContentCard
                key={index}
                content={expContent}
                position={cardPositions[index + 1]}
                index={index + 1}
                visible={contentVisible}
              />
            ))}

            {/* 3D Content Renderer for main content */}
            <ContentRenderer3D
              content={content.content.main}
              position={[0, 2, 0]}
              maxWidth={4}
              fontSize={0.12}
              visible={contentVisible}
            />

            {/* Simulation integration if present */}
            {content.content.expansions && Object.entries(content.content.expansions).map(([key, expansion]) => {
              const expansionData = typeof expansion === 'string' ? null : expansion;
              if (expansionData?.simulationId) {
                return (
                  <SimulationIntegration
                    key={key}
                    simulationId={expansionData.simulationId}
                    position={[0, -1.5, 0]}
                    visible={contentVisible}
                    parameters={expansionData.parameters}
                  />
                );
              }
              return null;
            })}
          </>
        )}
      </group>
    </ErrorBoundary>
  );
}

