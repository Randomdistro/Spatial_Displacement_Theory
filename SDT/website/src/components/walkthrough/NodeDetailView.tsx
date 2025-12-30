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
import SimulationViewer from './SimulationViewer';
import LoadingSpinner from '../ui/LoadingSpinner';

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
      <LoadingSpinner
        size="lg"
        message="Loading content..."
        fullScreen={true}
      />
    );
  }

  if (!content) {
    return (
      <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
        <div className="max-w-md w-full bg-slate-800/90 backdrop-blur-sm rounded-xl p-8 border border-slate-700 text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-yellow-500/20 flex items-center justify-center">
            <svg className="w-8 h-8 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">Content Not Found</h2>
          <p className="text-slate-400 mb-6">
            The content for this node is being prepared.
          </p>
          <button
            onClick={() => returnToPath()}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 overflow-y-auto">
      <div className="max-w-4xl mx-auto p-4 sm:p-8 bg-slate-900/95 rounded-lg my-4 sm:my-8 border border-slate-700/50 shadow-2xl">
        {/* Enhanced Header */}
        <div className="flex items-start justify-between mb-6 pb-6 border-b border-slate-700">
          <div className="flex-1">
            <h1 className="text-3xl sm:text-4xl font-bold text-white mb-2">{content.title}</h1>
            <div className="flex items-center gap-4 text-sm text-slate-400">
              <span className="flex items-center gap-1">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {content.readingTime} min read
              </span>
              {content.path && (
                <span className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs font-medium">
                  {content.path === 'path1' ? 'Quick Tour' : content.path === 'path2' ? 'Deep Dive' : 'Scientific'}
                </span>
              )}
            </div>
          </div>
          <button
            onClick={() => {
              narrationSystem.stop();
              returnToPath();
              if (onClose) onClose();
            }}
            className="ml-4 p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors"
            aria-label="Close"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Main content - Enhanced */}
        <div className="prose prose-invert max-w-none mb-8">
          <div 
            className="text-slate-300 leading-relaxed text-base sm:text-lg"
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
                <div key={key} className="border border-slate-700 rounded-lg overflow-hidden transition-all hover:border-sdt-gold-500/50">
                  <button
                    onClick={() => toggleExpansion(key)}
                    className="w-full px-4 py-3 bg-slate-800 hover:bg-slate-700 text-left flex items-center justify-between text-white transition-all group"
                  >
                    <span className="font-semibold group-hover:text-sdt-gold-400 transition-colors">
                      {expansionData.title || key}
                    </span>
                    <span className="text-xl text-slate-400 group-hover:text-sdt-gold-400 transition-all transform group-hover:scale-110">
                      {isExpanded ? '−' : '+'}
                    </span>
                  </button>
                  {isExpanded && (
                    <div className="p-4 bg-slate-800/50 text-slate-300">
                      {typeof expansionData === 'string' ? (
                        <div dangerouslySetInnerHTML={{ __html: expansionData.replace(/\n/g, '<br />') }} />
                      ) : expansionData.simulationId ? (
                        <div className="text-center py-8">
                          <SimulationViewer
                            simulationId={expansionData.simulationId}
                            parameters={expansionData.parameters || {}}
                          />
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

        {/* Enhanced Navigation */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pt-6 border-t border-slate-700">
          <button
            onClick={handlePrevious}
            disabled={!content.previousNodeId}
            className="flex-1 sm:flex-none px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg transition-all font-medium flex items-center justify-center gap-2 hover:scale-105 disabled:hover:scale-100"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Previous
          </button>
          <button
            onClick={() => {
              narrationSystem.stop();
              returnToPath();
              if (onClose) onClose();
            }}
            className="flex-1 sm:flex-none px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-all font-medium hover:scale-105"
          >
            Back to Path
          </button>
          <button
            onClick={handleNext}
            disabled={!content.nextNodeId}
            className="flex-1 sm:flex-none px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg transition-all font-medium flex items-center justify-center gap-2 hover:scale-105 disabled:hover:scale-100"
          >
            Next
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

