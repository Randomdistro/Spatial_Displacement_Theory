/**
 * Cross-Reference Sidebar Component
 * Displays related concepts, papers, phases, benchmarks, and formulas
 */

import React from 'react';
import type { ExplainerMetadata, CrossReference } from '../../types/explainers';
import { useExplainerRegistry } from './ExplainerRegistry';

interface CrossReferenceSidebarProps {
  explainerId: string;
  references: CrossReference[];
  metadata: ExplainerMetadata;
  onNavigate: (explainerId: string) => void;
}

export default function CrossReferenceSidebar({
  explainerId,
  references,
  metadata,
  onNavigate,
}: CrossReferenceSidebarProps) {
  const { registry } = useExplainerRegistry();

  // Group references by type
  const referencesByType = React.useMemo(() => {
    const groups: Record<string, CrossReference[]> = {
      DERIVES: [],
      VALIDATES: [],
      USES: [],
      EXTENDS: [],
      DEPENDS_ON: [],
      RELATED_TO: [],
      VALIDATED_BY: [],
    };

    references.forEach(ref => {
      if (groups[ref.referenceType]) {
        groups[ref.referenceType].push(ref);
      }
    });

    return groups;
  }, [references]);

  const getExplainerTitle = (id: string): string => {
    const entry = registry.get(id);
    // In a real implementation, we'd load the metadata
    // For now, format the ID nicely
    return id
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const renderReferenceGroup = (
    title: string,
    refs: CrossReference[],
    colorClass: string
  ) => {
    if (refs.length === 0) return null;

    return (
      <div className="mb-6">
        <h4 className="text-sm font-semibold text-slate-400 mb-2">{title}</h4>
        <div className="space-y-2">
          {refs.map((ref, idx) => (
            <button
              key={`${ref.targetId}-${idx}`}
              onClick={() => onNavigate(ref.targetId)}
              className={`w-full text-left px-3 py-2 ${colorClass} rounded text-sm transition-colors hover:opacity-80`}
            >
              <div className="font-medium">{getExplainerTitle(ref.targetId)}</div>
              {ref.context && (
                <div className="text-xs opacity-75 mt-1">{ref.context}</div>
              )}
            </button>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 sticky top-4 max-h-[calc(100vh-2rem)] overflow-y-auto">
      <h3 className="text-lg font-semibold text-white mb-4">Related Concepts</h3>

      {/* Direct References from Metadata */}
      {metadata.references.papers.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-slate-400 mb-2">Related Papers</h4>
          <div className="space-y-2">
            {metadata.references.papers.map(paperId => (
              <button
                key={paperId}
                onClick={() => onNavigate(paperId)}
                className="w-full text-left px-3 py-2 bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 rounded text-sm transition-colors"
              >
                {getExplainerTitle(paperId)}
              </button>
            ))}
          </div>
        </div>
      )}

      {metadata.references.benchmarks.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-slate-400 mb-2">Validated By</h4>
          <div className="space-y-2">
            {metadata.references.benchmarks.map(benchmarkId => (
              <button
                key={benchmarkId}
                onClick={() => onNavigate(benchmarkId)}
                className="w-full text-left px-3 py-2 bg-green-600/20 hover:bg-green-600/30 text-green-400 rounded text-sm transition-colors"
              >
                {getExplainerTitle(benchmarkId)}
              </button>
            ))}
          </div>
        </div>
      )}

      {metadata.references.formulas.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-slate-400 mb-2">Related Formulas</h4>
          <div className="space-y-2">
            {metadata.references.formulas.map(formulaId => (
              <button
                key={formulaId}
                onClick={() => onNavigate(formulaId)}
                className="w-full text-left px-3 py-2 bg-purple-600/20 hover:bg-purple-600/30 text-purple-400 rounded text-sm transition-colors font-mono"
              >
                {formulaId}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Cross-Reference Groups */}
      {renderReferenceGroup(
        'Derives',
        referencesByType.DERIVES,
        'bg-purple-600/20 hover:bg-purple-600/30 text-purple-400'
      )}

      {renderReferenceGroup(
        'Validates',
        referencesByType.VALIDATES,
        'bg-green-600/20 hover:bg-green-600/30 text-green-400'
      )}

      {renderReferenceGroup(
        'Uses',
        referencesByType.USES,
        'bg-blue-600/20 hover:bg-blue-600/30 text-blue-400'
      )}

      {renderReferenceGroup(
        'Depends On',
        referencesByType.DEPENDS_ON,
        'bg-amber-600/20 hover:bg-amber-600/30 text-amber-400'
      )}

      {renderReferenceGroup(
        'Related To',
        referencesByType.RELATED_TO,
        'bg-slate-600/20 hover:bg-slate-600/30 text-slate-400'
      )}

      {/* Prerequisites */}
      {metadata.prerequisites && metadata.prerequisites.length > 0 && (
        <div className="mb-6 pt-4 border-t border-slate-700">
          <h4 className="text-sm font-semibold text-slate-400 mb-2">Prerequisites</h4>
          <div className="space-y-2">
            {metadata.prerequisites.map(prereqId => (
              <button
                key={prereqId}
                onClick={() => onNavigate(prereqId)}
                className="w-full text-left px-3 py-2 bg-slate-700/50 hover:bg-slate-700 text-slate-300 rounded text-sm transition-colors"
              >
                {getExplainerTitle(prereqId)}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Tags */}
      {metadata.tags && metadata.tags.length > 0 && (
        <div className="pt-4 border-t border-slate-700">
          <h4 className="text-sm font-semibold text-slate-400 mb-2">Tags</h4>
          <div className="flex flex-wrap gap-2">
            {metadata.tags.map(tag => (
              <span
                key={tag}
                className="px-2 py-1 bg-slate-700/50 text-slate-300 rounded text-xs"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

