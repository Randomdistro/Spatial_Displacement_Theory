import React, { useEffect, useRef } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

export interface FormulaRendererProps {
  formula: string; // LaTeX string
  displayMode?: 'inline' | 'block';
  animated?: boolean;
  highlightTerms?: string[]; // Term IDs to highlight
  className?: string;
}

/**
 * Formula renderer component using KaTeX
 * Supports inline and block display modes, animations, and term highlighting
 */
export default function FormulaRenderer({
  formula,
  displayMode = 'block',
  animated = false,
  highlightTerms = [],
  className = '',
}: FormulaRendererProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    try {
      katex.render(formula, containerRef.current, {
        displayMode: displayMode === 'block',
        throwOnError: false,
        errorColor: '#cc0000',
        strict: false,
        trust: true,
      });

      // Apply highlighting if terms are specified
      if (highlightTerms.length > 0 && containerRef.current) {
        highlightTerms.forEach((term) => {
          const elements = containerRef.current?.querySelectorAll(`[data-term="${term}"]`);
          elements?.forEach((el) => {
            el.classList.add('highlight-term');
          });
        });
      }
    } catch (error) {
      console.error('Error rendering formula:', error);
      if (containerRef.current) {
        containerRef.current.textContent = formula;
      }
    }
  }, [formula, displayMode, highlightTerms]);

  const baseClasses = displayMode === 'block' 
    ? 'formula-block my-4 p-4 bg-slate-900 rounded-lg overflow-x-auto' 
    : 'formula-inline';

  return (
    <div
      ref={containerRef}
      className={`${baseClasses} ${className} ${animated ? 'animate-fade-in' : ''}`}
    />
  );
}

