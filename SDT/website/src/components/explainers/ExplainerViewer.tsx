/**
 * Explainer Viewer Component
 * Main component for displaying explainers with multiple visualization modes
 * Supports interactive 3D, static diagrams, animations, and formula rendering
 */

import React, { useState, useEffect, useMemo } from 'react';
import { useExplainer } from './ExplainerRegistry';
import FormulaRenderer from '../FormulaRenderer';
import LoadingSpinner from '../ui/LoadingSpinner';
import CrossReferenceSidebar from './CrossReferenceSidebar';
import type { VisualizationConfig, FormulaReference } from '../../types/explainers';
import { getExplainerReferences } from '../../utils/explainer-loader';

interface ExplainerViewerProps {
  explainerId: string;
  mode?: 'interactive' | 'static' | 'animation';
  onClose?: () => void;
  onNavigate?: (explainerId: string) => void;
  showCrossReferences?: boolean;
  className?: string;
}

export default function ExplainerViewer({
  explainerId,
  mode = 'interactive',
  onClose,
  onNavigate,
  showCrossReferences = true,
  className = '',
}: ExplainerViewerProps) {
  const { metadata, loading, error } = useExplainer(explainerId);
  const [activeVisualization, setActiveVisualization] = useState<string | null>(null);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set());
  const [crossReferences, setCrossReferences] = useState<any[]>([]);

  // Load cross-references
  useEffect(() => {
    if (explainerId) {
      getExplainerReferences(explainerId).then(refs => {
        setCrossReferences(refs);
      });
    }
  }, [explainerId]);

  // Expand first section by default
  useEffect(() => {
    if (metadata?.content.sections && metadata.content.sections.length > 0) {
      setExpandedSections(new Set([metadata.content.sections[0].id]));
    }
  }, [metadata]);

  const handleNavigate = (targetId: string) => {
    if (onNavigate) {
      onNavigate(targetId);
    }
  };

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev => {
      const next = new Set(prev);
      if (next.has(sectionId)) {
        next.delete(sectionId);
      } else {
        next.add(sectionId);
      }
      return next;
    });
  };

  const renderVisualization = (viz: VisualizationConfig) => {
    // Dynamic component loading based on visualization type
    let Component: React.ComponentType<any> | null = null;

    // Lazy import visualization components
    try {
      switch (viz.component) {
        case 'SpationLattice':
          // eslint-disable-next-line @typescript-eslint/no-require-imports
          Component = require('../visualizations/3d/SpationLattice').default;
          break;
        case 'NuclearPacking':
          // eslint-disable-next-line @typescript-eslint/no-require-imports
          Component = require('../visualizations/3d/NuclearPacking').default;
          break;
        case 'HelicalOrbitals':
          // eslint-disable-next-line @typescript-eslint/no-require-imports
          Component = require('../visualizations/3d/HelicalOrbitals').default;
          break;
        case 'PressureField':
          // eslint-disable-next-line @typescript-eslint/no-require-imports
          Component = require('../visualizations/3d/PressureField').default;
          break;
        case 'OrbitalMechanics':
          // eslint-disable-next-line @typescript-eslint/no-require-imports
          Component = require('../visualizations/3d/OrbitalMechanics').default;
          break;
        case 'ShuntDynamics':
          // eslint-disable-next-line @typescript-eslint/no-require-imports
          Component = require('../visualizations/animations/ShuntDynamics').default;
          break;
        case 'BenchmarkChart':
          Component = () => (
            <div className="w-full h-64 bg-slate-800/50 rounded-lg border border-slate-700 flex items-center justify-center text-slate-400">
              Benchmark Chart (To be implemented)
            </div>
          );
          break;
        case 'FormulaTree':
          Component = () => (
            <div className="w-full bg-slate-800/50 rounded-lg border border-slate-700 p-4 text-slate-400">
              Formula Tree (To be implemented)
            </div>
          );
          break;
        default:
          Component = null;
      }
    } catch (error) {
      console.warn(`Failed to load visualization component: ${viz.component}`, error);
      Component = null;
    }

    if (!Component) {
      return (
        <div key={viz.id} className="my-6">
          <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
            <div className="text-sm text-slate-400 mb-2">
              Visualization: {viz.type} - {viz.component}
            </div>
            {viz.caption && (
              <div className="text-xs text-slate-500 mt-2 italic">{viz.caption}</div>
            )}
            <div className="text-slate-600 text-sm py-8 text-center">
              Component not found: {viz.component}
            </div>
          </div>
        </div>
      );
    }

    return (
      <div key={viz.id} className="my-6">
        {viz.caption && (
          <div className="text-xs text-slate-400 mb-2 italic">{viz.caption}</div>
        )}
        <Component {...viz.props} />
      </div>
    );
  };

  const renderFormula = (formula: FormulaReference) => {
    return (
      <div key={formula.id} className="my-4">
        <FormulaRenderer
          formula={formula.latex}
          displayMode={formula.displayMode}
          className="explainer-formula"
        />
        {formula.label && (
          <div className="text-xs text-slate-400 mt-1 text-right">({formula.label})</div>
        )}
        {formula.description && (
          <div className="text-sm text-slate-300 mt-2">{formula.description}</div>
        )}
        {formula.dimensionalAnalysis && (
          <div className="text-xs text-slate-500 mt-2">
            Dimensions: {formula.dimensionalAnalysis}
          </div>
        )}
        {formula.numericalExample && (
          <div className="text-xs text-slate-400 mt-2 bg-slate-800/50 p-2 rounded">
            Example: {formula.numericalExample.result.toExponential(3)} {formula.numericalExample.units}
          </div>
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-6 text-red-400">
        <h3 className="font-semibold mb-2">Error Loading Explainer</h3>
        <p>{error.message}</p>
      </div>
    );
  }

  if (!metadata) {
    return (
      <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6 text-slate-400">
        <p>Explainer not found: {explainerId}</p>
      </div>
    );
  }

  return (
    <div className={`explainer-viewer ${className}`}>
      <div className="flex gap-6">
        {/* Main Content */}
        <div className="flex-1">
          {/* Header */}
          <div className="mb-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">{metadata.title}</h1>
                <div className="flex items-center gap-3 text-sm text-slate-400">
                  <span className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded capitalize">
                    {metadata.category}
                  </span>
                  <span className="px-2 py-1 bg-slate-700 text-slate-300 rounded capitalize">
                    {metadata.domain}
                  </span>
                  {metadata.difficulty && (
                    <span className="px-2 py-1 bg-amber-500/20 text-amber-400 rounded capitalize">
                      {metadata.difficulty}
                    </span>
                  )}
                  {metadata.estimatedReadTime && (
                    <span className="text-slate-500">
                      {metadata.estimatedReadTime} min read
                    </span>
                  )}
                </div>
              </div>
              {onClose && (
                <button
                  onClick={onClose}
                  className="text-slate-400 hover:text-white transition-colors p-2"
                  aria-label="Close"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
            <p className="text-slate-300 text-lg">{metadata.description}</p>
          </div>

          {/* Validation Status (for benchmarks) */}
          {metadata.validation && (
            <div className="mb-6 p-4 bg-slate-800/50 rounded-lg border border-slate-700">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-green-400 font-semibold">✓ Validated</span>
                {metadata.validation.errorRate !== undefined && (
                  <span className="text-sm text-slate-400">
                    Error: {metadata.validation.errorRate.toFixed(4)}%
                  </span>
                )}
              </div>
              {metadata.validation.experimentalValue !== undefined && 
               metadata.validation.predictedValue !== undefined && (
                <div className="text-sm text-slate-300 mt-2">
                  Predicted: {metadata.validation.predictedValue.toExponential(3)} | 
                  Experimental: {metadata.validation.experimentalValue.toExponential(3)} {metadata.validation.units}
                </div>
              )}
            </div>
          )}

          {/* Content Sections */}
          {metadata.content.sections && metadata.content.sections.length > 0 ? (
            <div className="space-y-4">
              {metadata.content.sections
                .sort((a, b) => a.order - b.order)
                .map(section => (
                  <div key={section.id} className="border border-slate-700 rounded-lg overflow-hidden">
                    <button
                      onClick={() => toggleSection(section.id)}
                      className="w-full px-4 py-3 bg-slate-800/50 hover:bg-slate-800 text-left flex items-center justify-between text-white transition-colors"
                    >
                      <span className="font-semibold">{section.title}</span>
                      <span className="text-xl text-slate-400">
                        {expandedSections.has(section.id) ? '−' : '+'}
                      </span>
                    </button>
                    {expandedSections.has(section.id) && (
                      <div className="p-4 prose prose-invert max-w-none">
                        <div 
                          className="text-slate-300"
                          dangerouslySetInnerHTML={{ __html: section.content.replace(/\n/g, '<br />') }}
                        />
                        
                        {/* Render visualizations in this section */}
                        {section.visualizations?.map(vizId => {
                          const viz = metadata.content.visualizations.find(v => v.id === vizId);
                          return viz ? renderVisualization(viz) : null;
                        })}
                        
                        {/* Render formulas in this section */}
                        {section.formulas?.map(formulaId => {
                          const formula = metadata.content.formulas.find(f => f.id === formulaId);
                          return formula ? renderFormula(formula) : null;
                        })}
                      </div>
                    )}
                  </div>
                ))}
            </div>
          ) : (
            /* Fallback: Render markdown directly */
            <div className="prose prose-invert max-w-none">
              <div 
                className="text-slate-300"
                dangerouslySetInnerHTML={{ __html: metadata.content.markdown.replace(/\n/g, '<br />') }}
              />
            </div>
          )}

          {/* Inline Visualizations */}
          {metadata.content.visualizations
            .filter(viz => viz.position === 'inline')
            .map(viz => renderVisualization(viz))}

          {/* Inline Formulas */}
          {metadata.content.formulas
            .filter(f => f.displayMode === 'block')
            .map(formula => renderFormula(formula))}

          {/* See Also Section */}
          {(metadata.references.papers.length > 0 ||
            metadata.references.phases.length > 0 ||
            metadata.references.benchmarks.length > 0) && (
            <div className="mt-8 pt-6 border-t border-slate-700">
              <h3 className="text-xl font-semibold text-white mb-4">See Also</h3>
              <div className="space-y-2">
                {metadata.references.papers.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-slate-400 mb-2">Related Papers</h4>
                    <div className="flex flex-wrap gap-2">
                      {metadata.references.papers.map(paperId => (
                        <button
                          key={paperId}
                          onClick={() => handleNavigate(paperId)}
                          className="px-3 py-1 bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 rounded text-sm transition-colors"
                        >
                          {paperId}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
                {metadata.references.benchmarks.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-slate-400 mb-2">Validated By</h4>
                    <div className="flex flex-wrap gap-2">
                      {metadata.references.benchmarks.map(benchmarkId => (
                        <button
                          key={benchmarkId}
                          onClick={() => handleNavigate(benchmarkId)}
                          className="px-3 py-1 bg-green-600/20 hover:bg-green-600/30 text-green-400 rounded text-sm transition-colors"
                        >
                          {benchmarkId}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Cross-Reference Sidebar */}
        {showCrossReferences && (
          <div className="w-80 flex-shrink-0">
            <CrossReferenceSidebar
              explainerId={explainerId}
              references={crossReferences}
              metadata={metadata}
              onNavigate={handleNavigate}
            />
          </div>
        )}
      </div>
    </div>
  );
}

