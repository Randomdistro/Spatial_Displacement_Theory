/**
 * Formula Renderer Component
 * Agent 3: Physics/Simulation
 * 
 * Renders LaTeX formulas using KaTeX with animation support
 */

import React, { useEffect, useState } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

export interface FormulaRendererProps {
  formula: string; // LaTeX string
  displayMode?: 'inline' | 'block';
  animated?: boolean;
  highlightTerms?: string[]; // Term IDs to highlight
  className?: string;
}

export const FormulaRenderer: React.FC<FormulaRendererProps> = ({
  formula,
  displayMode = 'block',
  animated = false,
  highlightTerms = [],
  className = '',
}) => {
  const [renderedFormula, setRenderedFormula] = useState<string>('');
  const [isVisible, setIsVisible] = useState(!animated);

  useEffect(() => {
    try {
      const html = katex.renderToString(formula, {
        displayMode: displayMode === 'block',
        throwOnError: false,
        errorColor: '#cc0000',
      });
      setRenderedFormula(html);
      
      if (animated) {
        // Animate in after a short delay
        setTimeout(() => setIsVisible(true), 100);
      }
    } catch (error) {
      console.error('KaTeX rendering error:', error);
      setRenderedFormula(`<span class="text-red-500">Formula Error: ${formula}</span>`);
    }
  }, [formula, displayMode]);

  const baseClasses = displayMode === 'block' 
    ? 'block my-4 text-center' 
    : 'inline mx-1';

  return (
    <div
      className={`${baseClasses} ${className} ${
        animated && !isVisible ? 'opacity-0 translate-y-2' : 'opacity-100 translate-y-0'
      } transition-all duration-500`}
      dangerouslySetInnerHTML={{ __html: renderedFormula }}
    />
  );
};

/**
 * Animated formula that reveals terms sequentially
 */
export interface AnimatedFormulaProps {
  formula: string;
  terms: Array<{ id: string; latex: string; description?: string }>;
  onTermRevealed?: (termId: string) => void;
  className?: string;
}

export const AnimatedFormula: React.FC<AnimatedFormulaProps> = ({
  formula,
  terms,
  onTermRevealed,
  className = '',
}) => {
  const [revealedTerms, setRevealedTerms] = useState<Set<string>>(new Set());

  useEffect(() => {
    // Reveal terms sequentially
    terms.forEach((term, index) => {
      setTimeout(() => {
        setRevealedTerms((prev) => new Set([...prev, term.id]));
        if (onTermRevealed) {
          onTermRevealed(term.id);
        }
      }, index * 500); // 500ms between terms
    });
  }, [terms, onTermRevealed]);

  // Build formula with revealed terms highlighted
  let displayFormula = formula;
  terms.forEach((term) => {
    if (revealedTerms.has(term.id)) {
      // Highlight revealed terms
      displayFormula = displayFormula.replace(
        term.latex,
        `\\colorbox{#d69e2e}{${term.latex}}`
      );
    } else {
      // Hide unrevealed terms
      displayFormula = displayFormula.replace(term.latex, '\\phantom{' + term.latex + '}');
    }
  });

  return (
    <div className={className}>
      <FormulaRenderer formula={displayFormula} displayMode="block" />
      {terms.some((t) => revealedTerms.has(t.id)) && (
        <div className="mt-4 text-sm text-slate-400 space-y-2">
          {terms
            .filter((t) => revealedTerms.has(t.id))
            .map((term) => (
              <div key={term.id} className="flex items-center gap-2">
                <span className="text-amber-400">●</span>
                <span className="font-mono">{term.latex}</span>
                {term.description && (
                  <span className="text-slate-500">: {term.description}</span>
                )}
              </div>
            ))}
        </div>
      )}
    </div>
  );
};

/**
 * Master Equation component with all terms
 */
export const MasterEquation: React.FC<{ animated?: boolean }> = ({ animated = false }) => {
  const formula = '\\nabla \\cdot [K_{bulk} \\nabla \\Delta(x)] = -\\kappa \\rho_{disp}(x) (1 - E(x,\\hat{n}))';
  
  const terms = [
    { id: 'K_bulk', latex: 'K_{bulk}', description: 'Bulk Modulus: 4.6×10¹¹³ Pa' },
    { id: 'Delta', latex: '\\Delta(x)', description: 'Pressure field' },
    { id: 'kappa', latex: '\\kappa', description: 'Coupling constant' },
    { id: 'rho_disp', latex: '\\rho_{disp}(x)', description: 'Displacement density' },
    { id: 'E', latex: 'E(x,\\hat{n})', description: 'Directional occlusion' },
  ];

  if (animated) {
    return <AnimatedFormula formula={formula} terms={terms} className="my-8" />;
  }

  return (
    <div className="my-8">
      <FormulaRenderer formula={formula} displayMode="block" />
      <div className="mt-4 text-sm text-slate-400 space-y-2">
        {terms.map((term) => (
          <div key={term.id} className="flex items-center gap-2">
            <span className="font-mono">{term.latex}</span>
            <span className="text-slate-500">: {term.description}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

/**
 * k-Law formula component
 */
export const KLawFormula: React.FC<{ animated?: boolean }> = ({ animated = false }) => {
  const formula = 'v(r) = \\frac{c}{k} \\sqrt{\\frac{R}{r}}';
  
  return (
    <div className="my-4">
      <FormulaRenderer 
        formula={formula} 
        displayMode="block" 
        animated={animated}
        className="text-xl"
      />
      <div className="mt-2 text-sm text-slate-400 text-center">
        Universal velocity law across 53 orders of magnitude
      </div>
    </div>
  );
};

