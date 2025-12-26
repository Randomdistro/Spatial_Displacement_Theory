/**
 * Expandable Content System
 * "Do you want to know more?" tabs and expandable sections
 */

import React, { useState } from 'react';
import { FormulaRenderer, MasterEquation, KLawFormula } from '../simulations/FormulaRenderer';

export type ExpansionType = 'conceptual' | 'technical' | 'simulation' | 'benchmark';

export interface ExpansionContent {
  type: ExpansionType;
  title: string;
  content: React.ReactNode;
}

interface ExpandableContentProps {
  title: string;
  expansions: ExpansionContent[];
  defaultExpanded?: boolean;
}

export const ExpandableContent: React.FC<ExpandableContentProps> = ({
  title,
  expansions,
  defaultExpanded = false,
}) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const [activeExpansion, setActiveExpansion] = useState<ExpansionType | null>(null);

  const getExpansionIcon = (type: ExpansionType): string => {
    switch (type) {
      case 'conceptual': return '💡';
      case 'technical': return '⚙️';
      case 'simulation': return '🎮';
      case 'benchmark': return '📊';
    }
  };

  const getExpansionColor = (type: ExpansionType): string => {
    switch (type) {
      case 'conceptual': return 'bg-blue-500/20 border-blue-500/50';
      case 'technical': return 'bg-purple-500/20 border-purple-500/50';
      case 'simulation': return 'bg-green-500/20 border-green-500/50';
      case 'benchmark': return 'bg-amber-500/20 border-amber-500/50';
    }
  };

  return (
    <div className="mt-4">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full text-left p-3 bg-slate-800/50 hover:bg-slate-800/70 rounded-lg transition-colors flex items-center justify-between"
      >
        <span className="text-amber-400 font-semibold">{title}</span>
        <span className="text-slate-400">{isExpanded ? '▼' : '▶'}</span>
      </button>

      {isExpanded && (
        <div className="mt-2 space-y-2">
          {expansions.map((expansion, index) => (
            <div
              key={index}
              className={`p-4 rounded-lg border ${getExpansionColor(expansion.type)} transition-all ${
                activeExpansion === expansion.type ? 'ring-2 ring-amber-400' : ''
              }`}
            >
              <button
                onClick={() => setActiveExpansion(
                  activeExpansion === expansion.type ? null : expansion.type
                )}
                className="w-full flex items-center justify-between mb-2"
              >
                <div className="flex items-center gap-2">
                  <span>{getExpansionIcon(expansion.type)}</span>
                  <span className="font-semibold text-white">{expansion.title}</span>
                </div>
                <span className="text-slate-400 text-sm">
                  {activeExpansion === expansion.type ? '▼' : '▶'}
                </span>
              </button>
              
              {activeExpansion === expansion.type && (
                <div className="mt-3 text-slate-300 text-sm">
                  {expansion.content}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

/**
 * Pre-built expansion content for common concepts
 */
export const createConceptualExpansion = (content: string): ExpansionContent => ({
  type: 'conceptual',
  title: 'Why does this matter?',
  content: <p>{content}</p>,
});

export const createTechnicalExpansion = (formula: string, derivation: string): ExpansionContent => ({
  type: 'technical',
  title: 'Technical Details',
  content: (
    <div className="space-y-3">
      <FormulaRenderer formula={formula} displayMode="block" />
      <p className="text-slate-400">{derivation}</p>
    </div>
  ),
});

export const createSimulationExpansion = (simulationId: string, description: string): ExpansionContent => ({
  type: 'simulation',
  title: 'Interactive Simulation',
  content: (
    <div>
      <p className="mb-2">{description}</p>
      <p className="text-slate-400 text-xs">Simulation ID: {simulationId}</p>
    </div>
  ),
});

export const createBenchmarkExpansion = (benchmarkId: string, error: string, description: string): ExpansionContent => ({
  type: 'benchmark',
  title: 'Benchmark Validation',
  content: (
    <div>
      <p className="mb-2">{description}</p>
      <div className="flex items-center gap-2 mt-2">
        <span className="text-emerald-400 font-mono text-xs">Error: {error}</span>
        <span className="text-slate-400 text-xs">Benchmark: {benchmarkId}</span>
      </div>
    </div>
  ),
});

