/**
 * Cross-Reference Graph Component
 * Interactive graph visualization showing concept relationships
 * Uses force-directed layout for node positioning
 */

import React, { useEffect, useRef, useState } from 'react';
import type { ReferenceGraph, ReferenceGraphNode, ReferenceGraphEdge } from '../../types/explainers';
import { buildReferenceGraph } from '../../utils/explainer-loader';
import { useExplainerRegistry } from './ExplainerRegistry';

interface CrossReferenceGraphProps {
  explainerIds?: string[];
  selectedId?: string;
  onNodeClick?: (nodeId: string) => void;
  filterByDomain?: string[];
  filterByCategory?: string[];
  className?: string;
  width?: number;
  height?: number;
}

export default function CrossReferenceGraph({
  explainerIds,
  selectedId,
  onNodeClick,
  filterByDomain,
  filterByCategory,
  className = '',
  width = 800,
  height = 600,
}: CrossReferenceGraphProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [graph, setGraph] = useState<ReferenceGraph | null>(null);
  const [loading, setLoading] = useState(true);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);
  const { registry } = useExplainerRegistry();

  // Load graph data
  useEffect(() => {
    async function loadGraph() {
      setLoading(true);
      try {
        const graphData = await buildReferenceGraph(explainerIds);
        
        // Apply filters
        let filteredNodes = graphData.nodes;
        let filteredEdges = graphData.edges;

        if (filterByDomain) {
          filteredNodes = filteredNodes.filter(node => 
            filterByDomain.includes(node.domain)
          );
          filteredEdges = filteredEdges.filter(edge =>
            filteredNodes.some(n => n.id === edge.source) &&
            filteredNodes.some(n => n.id === edge.target)
          );
        }

        if (filterByCategory) {
          filteredNodes = filteredNodes.filter(node =>
            filterByCategory.includes(node.category)
          );
          filteredEdges = filteredEdges.filter(edge =>
            filteredNodes.some(n => n.id === edge.source) &&
            filteredNodes.some(n => n.id === edge.target)
          );
        }

        setGraph({ nodes: filteredNodes, edges: filteredEdges });
      } catch (error) {
        console.error('Error loading reference graph:', error);
      } finally {
        setLoading(false);
      }
    }

    loadGraph();
  }, [explainerIds, filterByDomain, filterByCategory]);

  // Simple force-directed layout and rendering
  useEffect(() => {
    if (!graph || !canvasRef.current || loading) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Initialize positions
    const nodes = graph.nodes.map(node => ({
      ...node,
      x: node.x ?? Math.random() * width,
      y: node.y ?? Math.random() * height,
      vx: 0,
      vy: 0,
    }));

    // Simple force-directed layout
    let animationFrame: number;
    let frameCount = 0;
    const maxFrames = 300; // Run simulation for 300 frames

    function simulate() {
      // Reset velocities
      nodes.forEach(node => {
        node.vx = 0;
        node.vy = 0;
      });

      // Repulsion between nodes
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[j].x! - nodes[i].x!;
          const dy = nodes[j].y! - nodes[i].y!;
          const dist = Math.sqrt(dx * dx + dy * dy) || 1;
          const force = 1000 / (dist * dist);
          
          nodes[i].vx! -= (dx / dist) * force * 0.01;
          nodes[i].vy! -= (dy / dist) * force * 0.01;
          nodes[j].vx! += (dx / dist) * force * 0.01;
          nodes[j].vy! += (dy / dist) * force * 0.01;
        }
      }

      // Attraction along edges
      graph.edges.forEach(edge => {
        const source = nodes.find(n => n.id === edge.source);
        const target = nodes.find(n => n.id === edge.target);
        if (!source || !target) return;

        const dx = target.x! - source.x!;
        const dy = target.y! - source.y!;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1;
        const force = dist * 0.01;

        source.vx! += (dx / dist) * force;
        source.vy! += (dy / dist) * force;
        target.vx! -= (dx / dist) * force;
        target.vy! -= (dy / dist) * force;
      });

      // Update positions
      nodes.forEach(node => {
        node.x! += node.vx!;
        node.y! += node.vy!;
        
        // Keep nodes in bounds
        node.x! = Math.max(20, Math.min(width - 20, node.x!));
        node.y! = Math.max(20, Math.min(height - 20, node.y!));
      });

      frameCount++;
      if (frameCount < maxFrames) {
        animationFrame = requestAnimationFrame(simulate);
      } else {
        render();
      }
    }

    function render() {
      // Clear canvas
      ctx.clearRect(0, 0, width, height);

      // Draw edges
      graph.edges.forEach(edge => {
        const source = nodes.find(n => n.id === edge.source);
        const target = nodes.find(n => n.id === edge.target);
        if (!source || !target) return;

        ctx.strokeStyle = getEdgeColor(edge.type);
        ctx.lineWidth = (edge.strength ?? 0.5) * 2;
        ctx.globalAlpha = 0.3;
        ctx.beginPath();
        ctx.moveTo(source.x!, source.y!);
        ctx.lineTo(target.x!, target.y!);
        ctx.stroke();
      });

      ctx.globalAlpha = 1;

      // Draw nodes
      nodes.forEach(node => {
        const isSelected = node.id === selectedId;
        const isHovered = node.id === hoveredNode;
        const radius = isSelected ? 12 : isHovered ? 10 : 8;

        // Node circle
        ctx.fillStyle = getNodeColor(node.category, isSelected, isHovered);
        ctx.beginPath();
        ctx.arc(node.x!, node.y!, radius, 0, Math.PI * 2);
        ctx.fill();

        // Node border
        ctx.strokeStyle = isSelected ? '#d69e2e' : '#4a5568';
        ctx.lineWidth = isSelected ? 3 : 1;
        ctx.stroke();

        // Node label
        ctx.fillStyle = '#ffffff';
        ctx.font = '12px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(node.label, node.x!, node.y! + radius + 15);
      });
    }

    // Handle mouse interactions
    function handleMouseMove(event: MouseEvent) {
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      let found = false;
      nodes.forEach(node => {
        const dx = x - node.x!;
        const dy = y - node.y!;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 15) {
          setHoveredNode(node.id);
          canvas.style.cursor = 'pointer';
          found = true;
        }
      });

      if (!found) {
        setHoveredNode(null);
        canvas.style.cursor = 'default';
      }
    }

    function handleClick(event: MouseEvent) {
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      nodes.forEach(node => {
        const dx = x - node.x!;
        const dy = y - node.y!;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 15 && onNodeClick) {
          onNodeClick(node.id);
        }
      });
    }

    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('click', handleClick);

    // Start simulation
    simulate();

    return () => {
      if (animationFrame) {
        cancelAnimationFrame(animationFrame);
      }
      canvas.removeEventListener('mousemove', handleMouseMove);
      canvas.removeEventListener('click', handleClick);
    };
  }, [graph, selectedId, hoveredNode, width, height, onNodeClick, loading]);

  function getNodeColor(
    category: string,
    isSelected: boolean,
    isHovered: boolean
  ): string {
    if (isSelected) return '#d69e2e';
    if (isHovered) return '#f6ad55';
    
    const colors: Record<string, string> = {
      paper: '#3b82f6',
      phase: '#8b5cf6',
      benchmark: '#10b981',
      formula: '#ec4899',
      rule: '#f59e0b',
      element: '#06b6d4',
    };
    
    return colors[category] || '#6b7280';
  }

  function getEdgeColor(type: string): string {
    const colors: Record<string, string> = {
      DERIVES: '#ec4899',
      VALIDATES: '#10b981',
      USES: '#3b82f6',
      EXTENDS: '#8b5cf6',
      DEPENDS_ON: '#f59e0b',
      RELATED_TO: '#6b7280',
    };
    
    return colors[type] || '#6b7280';
  }

  if (loading) {
    return (
      <div className={`flex items-center justify-center ${className}`} style={{ width, height }}>
        <div className="text-slate-400">Loading graph...</div>
      </div>
    );
  }

  if (!graph || graph.nodes.length === 0) {
    return (
      <div className={`flex items-center justify-center ${className}`} style={{ width, height }}>
        <div className="text-slate-400">No references found</div>
      </div>
    );
  }

  return (
    <div className={`bg-slate-900 rounded-lg border border-slate-700 overflow-hidden ${className}`}>
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        className="w-full h-full"
      />
      <div className="p-4 bg-slate-800/50 border-t border-slate-700">
        <div className="flex flex-wrap gap-4 text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
            <span>Papers</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-purple-500"></div>
            <span>Phases</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span>Benchmarks</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-pink-500"></div>
            <span>Formulas</span>
          </div>
        </div>
      </div>
    </div>
  );
}

