/**
 * Integration Agent: Node Detail View Component
 * Displays full content for a selected node with expansions, simulations, narration
 */

import React, { useEffect, useState } from 'react';
import { useNavigationStore } from '../../store/navigationStore';
import { NodeContent } from '../../types/content';
import { loadNodeContent } from '../../utils/content-loader';
import FormulaRenderer from '../FormulaRenderer';
import { narrationSystem } from '../../utils/narration';

export interface NodeDetailViewProps {
  nodeId: string;
  onClose?: () => void;
}

/**
 * NodeDetailView - Full content display for a selected node
 * 
 * Features:
 * - Main content display
 * - Expansion points ("Do you want to know more?", "Tech Specs", "Simulation")
 * - Formula rendering
 * - Narration playback
 * - Navigation to next/previous nodes
 */
export default function NodeDetailView({ nodeId, onClose }: NodeDetailViewProps) {
  const { returnToPath, navigateToNode } = useNavigationStore();
  const [content, setContent] = useState<NodeContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set());
  const [isNarrating, setIsNarrating] = useState(false);

  useEffect(() => {
    const loadContent = async () => {
      setLoading(true);
      try {
        const nodeContent = await loadNodeContent(nodeId);
        setContent(nodeContent);
      } catch (error) {
        console.error('Failed to load node content:', error);
      } finally {
        setLoading(false);
      }
    };

    loadContent();
  }, [nodeId]);

  // Auto-play narration when content loads
  useEffect(() => {
    if (content?.narration?.script && !isNarrating) {
      setIsNarrating(true);
      narrationSystem.play(content.narration.script).finally(() => {
        setIsNarrating(false);
      });
    }
  }, [content, isNarrating]);

  const toggleExpansion = (sectionId: string) => {
    setExpandedSections((prev) => {
      const next = new Set(prev);
      if (next.has(sectionId)) {
        next.delete(sectionId);
      } else {
        next.add(sectionId);
      }
      return next;
    });
  };

  const handleNext = () => {
    if (content?.nextNodeId) {
      navigateToNode(content.nextNodeId);
    }
  };

  const handlePrevious = () => {
    if (content?.previousNodeId) {
      navigateToNode(content.previousNodeId);
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  if (!content) {
    return (
      <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
        <div className="text-white text-xl">Content not found</div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 overflow-y-auto">
      <div className="max-w-4xl mx-auto p-8 bg-slate-900/95 rounded-lg my-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-4xl font-bold text-white">{content.title}</h1>
          <button
            onClick={() => {
              narrationSystem.stop();
              returnToPath();
              if (onClose) onClose();
            }}
            className="text-white hover:text-slate-300 text-2xl"
          >
            ×
          </button>
        </div>

        {/* Reading time */}
        <div className="text-slate-400 mb-6">
          {content.readingTime} min read
        </div>

        {/* Main content */}
        <div className="prose prose-invert max-w-none mb-8">
          <div 
            className="text-slate-300 leading-relaxed"
            dangerouslySetInnerHTML={{ __html: content.content.main.replace(/\n/g, '<br />') }}
          />
        </div>

        {/* Expansion points */}
        {content.content.expansions && (
          <div className="space-y-4 mb-8">
            {Object.entries(content.content.expansions).map(([key, expansion]) => {
              const isExpanded = expandedSections.has(key);
              const expansionData = typeof expansion === 'string' 
                ? { content: expansion, title: key }
                : expansion;

              return (
                <div key={key} className="border border-slate-700 rounded-lg overflow-hidden">
                  <button
                    onClick={() => toggleExpansion(key)}
                    className="w-full px-4 py-3 bg-slate-800 hover:bg-slate-700 text-left flex items-center justify-between text-white transition-colors"
                  >
                    <span className="font-semibold">
                      {expansionData.title || key}
                    </span>
                    <span className="text-xl">{isExpanded ? '−' : '+'}</span>
                  </button>
                  {isExpanded && (
                    <div className="p-4 bg-slate-800/50 text-slate-300">
                      {typeof expansionData === 'string' ? (
                        <div dangerouslySetInnerHTML={{ __html: expansionData.replace(/\n/g, '<br />') }} />
                      ) : expansionData.simulationId ? (
                        <div className="text-center py-8">
                          <div className="text-slate-400">
                            Simulation: {expansionData.simulationId}
                            <br />
                            <span className="text-sm">(Simulation integration pending)</span>
                          </div>
                        </div>
                      ) : (
                        <div dangerouslySetInnerHTML={{ __html: expansionData.content.replace(/\n/g, '<br />') }} />
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* Formulas */}
        {content.visualizations?.formulas && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">Formulas</h2>
            {content.visualizations.formulas.map((formula, index) => (
              <div key={index} className="mb-4">
                <FormulaRenderer formula={formula} displayMode="block" />
              </div>
            ))}
          </div>
        )}

        {/* Navigation */}
        <div className="flex items-center justify-between pt-6 border-t border-slate-700">
          <button
            onClick={handlePrevious}
            disabled={!content.previousNodeId}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
          >
            ← Previous
          </button>
          <button
            onClick={() => {
              narrationSystem.stop();
              returnToPath();
              if (onClose) onClose();
            }}
            className="px-6 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
          >
            Back to Path
          </button>
          <button
            onClick={handleNext}
            disabled={!content.nextNodeId}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  );
}

