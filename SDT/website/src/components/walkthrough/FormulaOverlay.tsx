/**
 * Formula Overlay System
 * Displays formulas at appropriate moments with animations
 * World-class presentation of mathematical content
 */

import React, { useEffect, useState } from 'react';
import { FormulaRenderer, MasterEquation, KLawFormula } from '../simulations/FormulaRenderer';
import { ScalePoint } from './ScaleManager';

interface FormulaOverlayProps {
  scale: ScalePoint;
  showFormulas: boolean;
  highlightedFormula?: string;
}

export const FormulaOverlay: React.FC<FormulaOverlayProps> = ({
  scale,
  showFormulas,
  highlightedFormula,
}) => {
  const [visibleFormulas, setVisibleFormulas] = useState<string[]>([]);
  const [animationState, setAnimationState] = useState<'entering' | 'visible' | 'exiting'>('entering');

  useEffect(() => {
    // Determine which formulas to show based on scale
    const formulas: string[] = [];

    if (scale.domain === 'planck') {
      formulas.push('K_bulk');
      if (scale.name === 'Proton Radius') {
        formulas.push('P_nuc');
      }
    } else if (scale.domain === 'atomic') {
      formulas.push('Coulomb');
      if (scale.name === 'Bohr Radius') {
        formulas.push('Rydberg');
      }
    } else if (scale.domain === 'macroscopic') {
      formulas.push('Gravity');
    } else if (scale.domain === 'stellar') {
      formulas.push('k-law');
    } else if (scale.domain === 'galactic') {
      formulas.push('Eclipse');
    } else if (scale.domain === 'cosmological') {
      formulas.push('CMB');
      if (scale.name === 'CMB Boundary') {
        formulas.push('Master');
      }
    }

    setVisibleFormulas(formulas);
    setAnimationState('entering');
    
    // Animate in
    setTimeout(() => setAnimationState('visible'), 300);
  }, [scale]);

  if (!showFormulas || visibleFormulas.length === 0) return null;

  const getFormulaContent = (formulaId: string): React.ReactNode => {
    switch (formulaId) {
      case 'K_bulk':
        return (
          <div className="space-y-2">
            <FormulaRenderer 
              formula="K_{bulk} = 4.6 \\times 10^{113} \\text{ Pa}"
              displayMode="block"
              animated={true}
            />
            <p className="text-xs text-slate-400">Spation bulk modulus</p>
          </div>
        );
      
      case 'P_nuc':
        return (
          <div className="space-y-2">
            <FormulaRenderer 
              formula="P_{nuc} \\approx K_{bulk} \\times \\left(\\frac{R_p}{R_{univ}}\\right)^2"
              displayMode="block"
              animated={true}
            />
            <p className="text-xs text-slate-400">Nuclear pressure from CMB focusing</p>
          </div>
        );
      
      case 'Coulomb':
        return (
          <div className="space-y-2">
            <FormulaRenderer 
              formula="F_C = \\frac{\\pi}{4} P_{CMB} \\frac{R_N^2 R_e^2}{r^2}"
              displayMode="block"
              animated={true}
            />
            <p className="text-xs text-slate-400">Coulomb force from CMB mutual occlusion</p>
          </div>
        );
      
      case 'Rydberg':
        return (
          <div className="space-y-2">
            <FormulaRenderer 
              formula="E_n = -\\frac{R_H}{n^2}"
              displayMode="block"
              animated={true}
            />
            <p className="text-xs text-slate-400">Energy levels from helical quantization</p>
          </div>
        );
      
      case 'Gravity':
        return (
          <div className="space-y-2">
            <FormulaRenderer 
              formula="a(r) = -\\beta \\frac{1-E(r)}{r^2}"
              displayMode="block"
              animated={true}
            />
            <p className="text-xs text-slate-400">Gravity from pressure gradients</p>
          </div>
        );
      
      case 'k-law':
        return (
          <div className="space-y-2">
            <KLawFormula animated={true} />
            <p className="text-xs text-slate-400">Universal velocity law</p>
          </div>
        );
      
      case 'Eclipse':
        return (
          <div className="space-y-2">
            <FormulaRenderer 
              formula="E_{disk}(r) \\to E_{sat} \\quad \\text{(constant for } r > R_{flat})"
              displayMode="block"
              animated={true}
            />
            <p className="text-xs text-slate-400">Disk eclipse saturation</p>
          </div>
        );
      
      case 'CMB':
        return (
          <div className="space-y-2">
            <FormulaRenderer 
              formula="P_{CMB} = 2.036 \\times 10^{-2} \\text{ Pa}"
              displayMode="block"
              animated={true}
            />
            <p className="text-xs text-slate-400">CMB boundary pressure</p>
          </div>
        );
      
      case 'Master':
        return (
          <div className="space-y-2">
            <MasterEquation animated={true} />
            <p className="text-xs text-slate-400">Master equation - all forces unified</p>
          </div>
        );
      
      default:
        return null;
    }
  };

  const isHighlighted = (formulaId: string): boolean => {
    return highlightedFormula === formulaId;
  };

  return (
    <div className={`absolute top-1/2 right-4 -translate-y-1/2 bg-black/80 backdrop-blur-md text-white p-6 rounded-xl border border-amber-500/30 shadow-2xl transition-all duration-500 ${
      animationState === 'entering' ? 'opacity-0 translate-x-8' : 'opacity-100 translate-x-0'
    }`}>
      <div className="font-semibold mb-4 text-amber-400 text-sm uppercase tracking-wide">
        Key Formula{visibleFormulas.length > 1 ? 's' : ''}
      </div>
      <div className="space-y-4">
        {visibleFormulas.map((formulaId, index) => (
          <div
            key={formulaId}
            className={`transition-all duration-300 ${
              isHighlighted(formulaId) 
                ? 'ring-2 ring-amber-400 bg-amber-500/10 p-3 rounded-lg' 
                : ''
            }`}
            style={{
              animationDelay: `${index * 200}ms`,
            }}
          >
            {getFormulaContent(formulaId)}
          </div>
        ))}
      </div>
    </div>
  );
};

