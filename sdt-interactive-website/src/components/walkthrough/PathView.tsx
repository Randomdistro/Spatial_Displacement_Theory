/**
 * PathView - Displays the selected path's node structure
 */

import React from 'react';
import { useNavigationStore } from '../../store/navigationStore';
import { PathType } from '../../types/content';

interface PathViewProps {
  pathId: PathType;
  onReturn: () => void;
}

export default function PathView({ pathId, onReturn }: PathViewProps) {
  const { navigateToNode } = useNavigationStore();

  // Path metadata
  const pathInfo = {
    path1: {
      name: 'Quick Tour',
      description: 'A 15-minute introduction to SDT\'s core ideas',
      nodes: [
        { id: 'node1', title: 'What if Space Isn\'t Empty?', readingTime: 2 },
        { id: 'node2', title: 'The Master Equation', readingTime: 3 },
        { id: 'node3', title: 'From Atoms to Galaxies', readingTime: 4 },
        { id: 'node4', title: 'No Dark Matter Needed', readingTime: 3 },
        { id: 'node5', title: 'Validated Predictions', readingTime: 5 },
      ],
    },
    path2: {
      name: 'Deep Dive',
      description: 'Comprehensive exploration of all SDT concepts',
      nodes: [
        { id: 'node1', title: 'Complete Axiomatic Foundation', readingTime: 15 },
        { id: 'node2', title: 'Full Derivation Tree', readingTime: 20 },
        { id: 'node3', title: 'All 24 Benchmarks', readingTime: 30 },
      ],
    },
    path3: {
      name: 'Scientific Framework',
      description: 'Complete mathematical and physical derivation',
      nodes: [
        { id: 'node1', title: 'Mathematical Foundation', readingTime: 20 },
        { id: 'node2', title: 'Derivation Tree (Complete)', readingTime: 30 },
        { id: 'node3', title: 'Validation Protocol', readingTime: 20 },
      ],
    },
  };

  const path = pathInfo[pathId || 'path1'];

  return (
    <div className="absolute inset-0 bg-slate-900/95 backdrop-blur-sm text-white p-8 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={onReturn}
            className="mb-4 text-slate-400 hover:text-white transition-colors flex items-center gap-2"
          >
            ← Back to Landing
          </button>
          <h1 className="text-4xl font-display font-bold mb-2">{path.name}</h1>
          <p className="text-xl text-slate-300">{path.description}</p>
        </div>

        {/* Node List */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {path.nodes.map((node, index) => (
            <button
              key={node.id}
              onClick={() => navigateToNode(node.id)}
              className="bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl p-6 text-left transition-all hover:scale-105"
            >
              <div className="text-2xl font-bold text-slate-400 mb-2">
                {String(index + 1).padStart(2, '0')}
              </div>
              <h3 className="text-xl font-display font-semibold mb-2">{node.title}</h3>
              <div className="text-sm text-slate-400">{node.readingTime} min read</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}


