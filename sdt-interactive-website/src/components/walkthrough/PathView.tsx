/**
 * PathView - Displays the selected path's node structure
 * 
 * TEKNE-styled path navigation with:
 * - Golden ratio proportions
 * - Veritasium-style hooks
 * - Visual hierarchy indicating content depth
 */

import React, { useEffect, useState } from 'react';
import { useNavigationStore } from '../../store/navigationStore';
import type { PathType } from '../../types/content';
import { getPathNodeSummaries, PATH_METADATA, type NodeSummary } from '../../utils/content-loader';

interface PathViewProps {
  pathId: PathType;
  onReturn: () => void;
}

// Path-specific styling
const PATH_STYLES: Record<PathType, { gradient: string; icon: string; accentColor: string }> = {
  path1: {
    gradient: 'from-amber-500/20 to-amber-600/10',
    icon: '⚡',
    accentColor: 'text-amber-400',
  },
  path2: {
    gradient: 'from-blue-500/20 to-blue-600/10',
    icon: '🔬',
    accentColor: 'text-blue-400',
  },
  path3: {
    gradient: 'from-purple-500/20 to-purple-600/10',
    icon: '📐',
    accentColor: 'text-purple-400',
  },
};

export default function PathView({ pathId, onReturn }: PathViewProps) {
  const { navigateToNode } = useNavigationStore();
  const [nodes, setNodes] = useState<NodeSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load node summaries
  useEffect(() => {
    setIsLoading(true);
    getPathNodeSummaries(pathId)
      .then((summaries) => {
        setNodes(summaries);
        setIsLoading(false);
      })
      .catch(() => setIsLoading(false));
  }, [pathId]);

  const pathMeta = PATH_METADATA[pathId];
  const pathStyle = PATH_STYLES[pathId];

  // Fallback nodes if loading fails
  const displayNodes = nodes.length > 0 ? nodes : [
    { id: 'node1', title: 'Introduction', readingTime: 5 },
  ];

  return (
    <div className="absolute inset-0 bg-slate-900/95 backdrop-blur-sm text-white overflow-y-auto">
      {/* Background gradient */}
      <div className={`absolute inset-0 bg-gradient-to-br ${pathStyle.gradient} opacity-50`} />
      
      <div className="relative max-w-6xl mx-auto p-8">
        {/* Header */}
        <div className="mb-12">
          <button
            onClick={onReturn}
            className="mb-6 text-slate-400 hover:text-white transition-colors flex items-center gap-2 group"
          >
            <span className="group-hover:-translate-x-1 transition-transform">←</span>
            Back to Landing
          </button>

          <div className="flex items-start gap-4">
            <span className="text-5xl">{pathStyle.icon}</span>
            <div>
              <h1 className={`text-5xl font-display font-bold mb-3 ${pathStyle.accentColor}`}>
                {pathMeta.name}
              </h1>
              <p className="text-xl text-slate-300 max-w-2xl">
                {pathMeta.description}
              </p>
              <div className="flex gap-4 mt-4 text-sm text-slate-400">
                <span>🎯 {pathMeta.targetAudience}</span>
                <span>📝 {pathMeta.tone}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Loading state */}
        {isLoading ? (
          <div className="flex items-center justify-center h-48">
            <div className="text-slate-400">Loading content...</div>
          </div>
        ) : (
          <>
            {/* Journey progress indicator */}
            <div className="mb-8 relative">
              <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
                <div 
                  className={`h-full bg-gradient-to-r ${pathStyle.gradient.replace('/20', '/80').replace('/10', '/60')} rounded-full`}
                  style={{ width: '0%' }}
                />
              </div>
              <div className="flex justify-between mt-2 text-xs text-slate-500">
                <span>Start</span>
                <span>{displayNodes.length} topics</span>
                <span>Complete</span>
              </div>
            </div>

            {/* Node List */}
            <div className="space-y-4">
              {displayNodes.map((node, index) => (
                <button
                  key={node.id}
                  onClick={() => navigateToNode(node.id)}
                  className={`
                    w-full text-left p-6 rounded-2xl
                    bg-white/5 hover:bg-white/10 
                    border border-white/10 hover:border-white/20
                    transition-all duration-300 
                    hover:scale-[1.02] hover:shadow-lg
                    group
                  `}
                >
                  <div className="flex items-start gap-6">
                    {/* Number */}
                    <div className={`
                      w-14 h-14 rounded-xl flex items-center justify-center
                      bg-gradient-to-br ${pathStyle.gradient}
                      ${pathStyle.accentColor} text-2xl font-bold font-display
                      group-hover:scale-110 transition-transform
                    `}>
                      {String(index + 1).padStart(2, '0')}
                    </div>

                    {/* Content */}
                    <div className="flex-1">
                      {/* Hook */}
                      {node.hook && (
                        <div className="text-xs text-amber-400 font-bold uppercase tracking-wider mb-1">
                          {node.hook}
                        </div>
                      )}

                      <h3 className="text-xl font-display font-bold mb-2 group-hover:text-white transition-colors">
                        {node.title}
                      </h3>

                      <div className="flex items-center gap-4 text-sm text-slate-400">
                        <span>📖 {node.readingTime} min read</span>
                        <span className="opacity-0 group-hover:opacity-100 transition-opacity text-amber-400">
                          Click to explore →
                        </span>
                      </div>
                    </div>

                    {/* Arrow */}
                    <div className={`
                      w-10 h-10 rounded-full flex items-center justify-center
                      bg-white/5 group-hover:bg-white/10
                      ${pathStyle.accentColor}
                      transition-all group-hover:translate-x-1
                    `}>
                      →
                    </div>
                  </div>
                </button>
              ))}
            </div>

            {/* Continue journey prompt */}
            <div className="mt-12 text-center">
              <p className="text-slate-400 mb-4">
                Ready to begin your journey through SDT?
              </p>
              <button
                onClick={() => navigateToNode(displayNodes[0]?.id || 'node1')}
                className={`
                  px-8 py-4 rounded-xl font-bold text-lg
                  bg-gradient-to-r from-amber-500 to-amber-600
                  hover:from-amber-400 hover:to-amber-500
                  text-slate-900 transition-all
                  shadow-lg shadow-amber-500/20
                  hover:shadow-xl hover:shadow-amber-500/30
                  hover:scale-105
                `}
              >
                Start with "{displayNodes[0]?.title || 'Introduction'}" →
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}





