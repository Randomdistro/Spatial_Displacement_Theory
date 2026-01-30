/**
 * ExpansionCard - "Would you like to know more?" Pattern
 * 
 * Starship Troopers-style progressive disclosure with:
 * - Punchy hook headlines
 * - Animated expand/collapse
 * - Visual category indicators
 * - Simulation integration support
 */

import React, { useState, useRef, useEffect } from 'react';

export interface ExpansionData {
  id: string;
  title: string;
  content: string;
  simulationId?: string;
  category?: 'know-more' | 'tech-specs' | 'simulation' | 'example' | 'history';
}

interface ExpansionCardProps {
  expansion: ExpansionData;
  defaultExpanded?: boolean;
  onExpand?: (id: string) => void;
  onSimulationRequest?: (simulationId: string) => void;
}

// Category icons and colors
const CATEGORY_STYLES: Record<string, { icon: string; color: string; bgColor: string }> = {
  'know-more': {
    icon: '🎬',
    color: 'text-amber-400',
    bgColor: 'bg-amber-400/10 border-amber-400/30',
  },
  'tech-specs': {
    icon: '📊',
    color: 'text-blue-400',
    bgColor: 'bg-blue-400/10 border-blue-400/30',
  },
  simulation: {
    icon: '🔬',
    color: 'text-green-400',
    bgColor: 'bg-green-400/10 border-green-400/30',
  },
  example: {
    icon: '💡',
    color: 'text-purple-400',
    bgColor: 'bg-purple-400/10 border-purple-400/30',
  },
  history: {
    icon: '📜',
    color: 'text-orange-400',
    bgColor: 'bg-orange-400/10 border-orange-400/30',
  },
};

export default function ExpansionCard({
  expansion,
  defaultExpanded = false,
  onExpand,
  onSimulationRequest,
}: ExpansionCardProps) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const [contentHeight, setContentHeight] = useState(0);
  const contentRef = useRef<HTMLDivElement>(null);

  // Get category style
  const categoryStyle = CATEGORY_STYLES[expansion.category || 'know-more'];

  // Measure content height for animation
  useEffect(() => {
    if (contentRef.current) {
      setContentHeight(contentRef.current.scrollHeight);
    }
  }, [expansion.content, isExpanded]);

  const handleToggle = () => {
    setIsExpanded(!isExpanded);
    if (!isExpanded) {
      onExpand?.(expansion.id);
    }
  };

  const handleSimulationClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (expansion.simulationId) {
      onSimulationRequest?.(expansion.simulationId);
    }
  };

  // Parse markdown-like content (basic)
  const renderContent = (text: string) => {
    // Split into paragraphs
    const paragraphs = text.split('\n\n');

    return paragraphs.map((paragraph, i) => {
      // Bold text
      const withBold = paragraph.replace(
        /\*\*(.*?)\*\*/g,
        '<strong class="text-white font-semibold">$1</strong>'
      );

      // Inline code
      const withCode = withBold.replace(
        /`(.*?)`/g,
        '<code class="bg-slate-700 px-1 py-0.5 rounded text-amber-300 font-mono text-sm">$1</code>'
      );

      // Check if it's a list item
      if (paragraph.trim().startsWith('- ') || paragraph.trim().startsWith('• ')) {
        return (
          <li
            key={i}
            className="ml-4"
            dangerouslySetInnerHTML={{ __html: withCode.replace(/^[-•]\s*/, '') }}
          />
        );
      }

      // Check if it's a table row
      if (paragraph.includes('|')) {
        const rows = paragraph.split('\n').filter((r) => r.trim());
        const isHeader = rows[1]?.includes('---');

        return (
          <table key={i} className="w-full text-sm my-2">
            <tbody>
              {rows
                .filter((r) => !r.includes('---'))
                .map((row, ri) => {
                  const cells = row
                    .split('|')
                    .filter((c) => c.trim())
                    .map((c) => c.trim());
                  const Tag = ri === 0 && isHeader ? 'th' : 'td';
                  return (
                    <tr
                      key={ri}
                      className={ri === 0 && isHeader ? 'bg-slate-700/50' : ''}
                    >
                      {cells.map((cell, ci) => (
                        <Tag
                          key={ci}
                          className="px-2 py-1 border-b border-slate-700 text-left"
                          dangerouslySetInnerHTML={{ __html: cell }}
                        />
                      ))}
                    </tr>
                  );
                })}
            </tbody>
          </table>
        );
      }

      return (
        <p
          key={i}
          className="mb-3 last:mb-0"
          dangerouslySetInnerHTML={{ __html: withCode }}
        />
      );
    });
  };

  return (
    <div
      className={`
        rounded-xl border overflow-hidden transition-all duration-300
        ${isExpanded ? categoryStyle.bgColor : 'bg-slate-800/50 border-slate-700'}
        ${isExpanded ? 'shadow-lg' : 'shadow'}
      `}
    >
      {/* Header - Clickable */}
      <button
        onClick={handleToggle}
        className={`
          w-full px-5 py-4 text-left flex items-center justify-between
          transition-colors hover:bg-white/5
        `}
      >
        <div className="flex items-center gap-3">
          <span className="text-2xl">{categoryStyle.icon}</span>
          <div>
            <h3 className={`font-bold text-lg ${categoryStyle.color}`}>
              {expansion.title}
            </h3>
            {!isExpanded && (
              <p className="text-sm text-slate-400 mt-0.5">
                Click to expand
              </p>
            )}
          </div>
        </div>

        {/* Expand/Collapse indicator */}
        <div
          className={`
            w-8 h-8 rounded-full flex items-center justify-center
            transition-all duration-300 ${categoryStyle.bgColor}
          `}
        >
          <span
            className={`
              text-lg transition-transform duration-300
              ${isExpanded ? 'rotate-180' : ''}
            `}
          >
            ▼
          </span>
        </div>
      </button>

      {/* Content - Animated */}
      <div
        className="overflow-hidden transition-all duration-300 ease-out"
        style={{
          maxHeight: isExpanded ? '2000px' : 0,
          opacity: isExpanded ? 1 : 0,
        }}
      >
        <div
          ref={contentRef}
          className="px-5 pb-5 pt-2 border-t border-slate-700/50"
        >
          {/* Main content */}
          <div className="text-slate-300 leading-relaxed">
            {renderContent(expansion.content)}
          </div>

          {/* Simulation button if available */}
          {expansion.simulationId && (
            <button
              onClick={handleSimulationClick}
              className={`
                mt-4 flex items-center gap-2 px-4 py-2 rounded-lg
                bg-gradient-to-r from-green-600 to-emerald-600
                hover:from-green-500 hover:to-emerald-500
                text-white font-medium transition-all
                shadow-lg shadow-green-500/20
              `}
            >
              <span>🔬</span>
              <span>Launch Interactive Simulation</span>
            </button>
          )}
        </div>
      </div>

      {/* Glow effect when expanded */}
      {isExpanded && (
        <div
          className={`
            absolute inset-0 pointer-events-none rounded-xl
            bg-gradient-to-b from-transparent to-current opacity-5
          `}
          style={{ color: categoryStyle.color.replace('text-', '') }}
        />
      )}
    </div>
  );
}

/**
 * ExpansionCardList - Renders multiple expansion cards
 */
export function ExpansionCardList({
  expansions,
  onSimulationRequest,
}: {
  expansions: ExpansionData[];
  onSimulationRequest?: (simulationId: string) => void;
}) {
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set());

  const handleExpand = (id: string) => {
    setExpandedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  return (
    <div className="space-y-4">
      {expansions.map((expansion) => (
        <ExpansionCard
          key={expansion.id}
          expansion={expansion}
          defaultExpanded={expandedIds.has(expansion.id)}
          onExpand={handleExpand}
          onSimulationRequest={onSimulationRequest}
        />
      ))}
    </div>
  );
}


