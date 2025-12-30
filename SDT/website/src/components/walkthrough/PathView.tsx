/**
 * Codemonkey Agent: Path View Component
 * Displays all nodes for a selected path with spatial navigation
 */

import React, { useEffect, useState } from 'react';
import { useNavigationStore, PathType } from '../../store/navigationStore';
import { loadPathContent } from '../../utils/content-loader';
import { NodeContent } from '../../types/content';
import NodeRoom from './NodeRoom';
import EnhancedNodeRoom from '../3d/EnhancedNodeRoom';
import NodeConnector from './NodeConnector';
import SpatialPath from '../3d/SpatialPath';

export interface PathViewProps {
  pathId: PathType;
  onNodeSelect?: (nodeId: string) => void;
}

/**
 * PathView - Displays all nodes for a path in 3D space
 * 
 * Features:
 * - Loads and displays all nodes for a path
 * - Spatial layout of nodes
 * - Navigation between nodes
 * - Visual path connections
 */
export default function PathView({ pathId, onNodeSelect }: PathViewProps) {
  const { currentNode } = useNavigationStore();
  const [nodes, setNodes] = useState<NodeContent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!pathId) {
      setNodes([]);
      setLoading(false);
      return;
    }

    const loadNodes = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const content = await loadPathContent(pathId);
        setNodes(content);
      } catch (err) {
        console.error('Failed to load path content:', err);
        setError('Failed to load path content');
      } finally {
        setLoading(false);
      }
    };

    loadNodes();
  }, [pathId]);

  if (loading) {
    return (
      <group>
        {/* Loading indicator */}
        <mesh position={[0, 0, 0]}>
          <boxGeometry args={[0.5, 0.5, 0.5]} />
          <meshStandardMaterial color="#4299e1" emissive="#4299e1" emissiveIntensity={0.5} />
        </mesh>
      </group>
    );
  }

  if (error) {
    return (
      <group>
        {/* Error indicator */}
        <mesh position={[0, 0, 0]}>
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial color="#ef4444" />
        </mesh>
      </group>
    );
  }

  if (nodes.length === 0) {
    return null;
  }

  // Get path color for connections
  const getPathColor = (path: PathType): number => {
    switch (path) {
      case 'path1':
        return 0x4299e1; // Light blue
      case 'path2':
        return 0x2d5a87; // Medium blue
      case 'path3':
        return 0x1a365d; // Deep blue
      default:
        return 0x4a90e2;
    }
  };

  const pathColor = getPathColor(pathId);

  return (
    <group>
      {/* Render nodes - Use EnhancedNodeRoom for better visuals */}
      {nodes.map((node) => {
        const isCurrent = currentNode === node.id;
        
        // Use EnhancedNodeRoom for current node, basic NodeRoom for others
        if (isCurrent) {
          return (
            <EnhancedNodeRoom
              key={node.id}
              nodeId={node.id}
              position={node.position}
              content={node}
              visible={true}
              onEnter={() => {
                if (onNodeSelect) {
                  onNodeSelect(node.id);
                }
              }}
            />
          );
        }
        
        return (
          <NodeRoom
            key={node.id}
            nodeId={node.id}
            position={node.position}
            content={node}
            onEnter={() => {
              if (onNodeSelect) {
                onNodeSelect(node.id);
              }
            }}
          />
        );
      })}

      {/* Render connections between nodes - Use SpatialPath for better visuals */}
      {nodes.map((node, index) => {
        if (!node.nextNodeId) return null;
        
        const nextNode = nodes.find((n) => n.id === node.nextNodeId);
        if (!nextNode) return null;

        const isVisited = nodes.slice(0, index + 1).some(n => n.id === node.id);
        const isCurrent = currentNode === node.id;

        return (
          <SpatialPath
            key={`path-${node.id}-${nextNode.id}`}
            from={node.position}
            to={nextNode.position}
            visited={isVisited}
            current={isCurrent}
            progress={isVisited ? 1 : 0}
          />
        );
      })}
    </group>
  );
}

