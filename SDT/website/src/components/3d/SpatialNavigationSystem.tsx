/**
 * Creative Agent: Spatial Navigation System
 * 
 * TEKNE: Navigation IS spatial understanding
 * Complete visualization of path through conceptual space
 * 
 * Design Philosophy:
 * - Gold path tubes connecting nodes
 * - Node indicators showing progress
 * - Progress trail showing path taken
 * - Smooth, flowing, organic
 */

import React, { useMemo } from 'react';
import { NodeContent } from '../../types/content';
import SpatialPath from './SpatialPath';
import NodeIndicator from './NodeIndicator';

export interface SpatialNavigationSystemProps {
  nodes: NodeContent[];
  currentPath: 'path1' | 'path2' | 'path3' | null;
  currentNode: string | null;
  visitedNodes?: Set<string>;
}

/**
 * SpatialNavigationSystem - Complete path visualization
 * 
 * Features:
 * - Gold gradient tubes connecting all nodes
 * - Node indicators (gold/blue/silver)
 * - Progress trail (animated gold)
 * - Flow animation
 */
export default function SpatialNavigationSystem({
  nodes,
  currentPath,
  currentNode,
  visitedNodes = new Set(),
}: SpatialNavigationSystemProps) {
  // Filter nodes by current path
  const pathNodes = useMemo(() => {
    if (!currentPath) return [];
    return nodes.filter(node => node.path === currentPath);
  }, [nodes, currentPath]);

  // Calculate progress for each node
  const nodeProgress = useMemo(() => {
    const progress: Record<string, number> = {};
    let visitedCount = 0;
    
    for (const node of pathNodes) {
      if (visitedNodes.has(node.id)) {
        visitedCount++;
        progress[node.id] = visitedCount / pathNodes.length;
      } else {
        progress[node.id] = visitedCount / pathNodes.length;
      }
    }
    
    return progress;
  }, [pathNodes, visitedNodes]);

  if (!currentPath || pathNodes.length === 0) return null;

  return (
    <group>
      {/* Connection paths between nodes */}
      {pathNodes.map((node, index) => {
        if (index === pathNodes.length - 1) return null; // Last node
        
        const nextNode = pathNodes[index + 1];
        const visited = visitedNodes.has(node.id);
        const current = currentNode === node.id;
        const progress = nodeProgress[node.id] || 0;
        
        return (
          <SpatialPath
            key={`path-${node.id}-${nextNode.id}`}
            from={node.position}
            to={nextNode.position}
            visited={visited}
            current={current}
            progress={progress}
          />
        );
      })}

      {/* Node indicators */}
      {pathNodes.map((node) => {
        const visited = visitedNodes.has(node.id);
        const current = currentNode === node.id;
        const state = current ? 'current' : visited ? 'visited' : 'unvisited';
        
        return (
          <NodeIndicator
            key={`indicator-${node.id}`}
            position={node.position}
            state={state}
            size={0.15}
          />
        );
      })}
    </group>
  );
}



