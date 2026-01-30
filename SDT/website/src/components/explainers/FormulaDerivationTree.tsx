/**
 * Formula Derivation Tree Component
 * Interactive visualization of how SDT formulas are derived from primitives
 */

import React, { useState, useMemo } from 'react';

interface DerivationStep {
  id: string;
  formula: string;
  description: string;
  justification: string;
  variables: Record<string, string>;
  level: number;
  parentId?: string;
  children?: string[];
}

interface DerivationTree {
  name: string;
  rootFormula: string;
  description: string;
  steps: DerivationStep[];
}

const derivationTrees: DerivationTree[] = [
  {
    name: "Mass-Energy Equivalence",
    rootFormula: "E_0 = m c^2",
    description: "How rest energy emerges from the master equation",
    steps: [
      {
        id: "master-eq",
        formula: "\\dot{E} = P_{\\text{CMB}} A_{\\text{eff}} \\Gamma \\kappa (1-\\eta)",
        description: "SDT Master Equation",
        justification: "Fundamental energy transfer rate from four primitives",
        variables: {
          "Ė": "Energy rate",
          "P_CMB": "CMB pressure",
          "A_eff": "Effective capture area",
          "Γ": "Circulation factor",
          "κ": "Curvature",
          "η": "Slip factor"
        },
        level: 0
      },
      {
        id: "rest-energy",
        formula: "E_0 = \\dot{E}_{\\text{int}} \\tau",
        description: "Rest energy from internal power throughput",
        justification: "Stable systems have constant internal energy transfer",
        variables: {
          "E_0": "Rest energy",
          "Ė_int": "Internal energy transfer rate",
          "τ": "Characteristic time"
        },
        level: 1,
        parentId: "master-eq"
      },
      {
        id: "characteristic-time",
        formula: "\\tau = \\frac{R}{c}",
        description: "Characteristic time from size and speed of light",
        justification: "Time for light to cross the system",
        variables: {
          "τ": "Characteristic time",
          "R": "System radius",
          "c": "Speed of light"
        },
        level: 2,
        parentId: "rest-energy"
      },
      {
        id: "displacement-volume",
        formula: "V_{\\text{disp}} = \\frac{m}{\\rho_{\\text{spation}}}",
        description: "Displacement volume from mass and spation density",
        justification: "Matter excludes spation volume",
        variables: {
          "V_disp": "Displacement volume",
          "m": "Mass",
          "ρ_spation": "Spation density"
        },
        level: 1,
        parentId: "master-eq"
      },
      {
        id: "spation-density",
        formula: "\\rho_{\\text{spation}} = \\frac{K_{\\text{bulk}}}{c^2}",
        description: "Spation density from bulk modulus and c",
        justification: "Incompressible medium properties",
        variables: {
          "ρ_spation": "Spation density",
          "K_bulk": "Bulk modulus",
          "c": "Speed of light"
        },
        level: 2,
        parentId: "displacement-volume"
      },
      {
        id: "energy-equivalence",
        formula: "E_0 = m c^2",
        description: "Mass-energy equivalence",
        justification: "Combining rest energy and displacement definitions",
        variables: {
          "E_0": "Rest energy",
          "m": "Mass",
          "c": "Speed of light"
        },
        level: 3,
        parentId: "rest-energy"
      }
    ]
  },
  {
    name: "Gravitational Constant",
    rootFormula: "G = \\frac{\\kappa c^2}{2\\pi \\rho_{\\text{spation}} r}",
    description: "How G emerges from pressure gradients",
    steps: [
      {
        id: "grav-acceleration",
        formula: "\\mathbf{g} = -\\frac{\\nabla \\Pi}{\\rho_{\\text{spation}}}",
        description: "Gravitational acceleration from pressure gradient",
        justification: "Pressure gradients create effective gravity",
        variables: {
          "g": "Gravitational acceleration",
          "∇Π": "Pressure gradient",
          "ρ_spation": "Spation density"
        },
        level: 0
      },
      {
        id: "pressure-gradient",
        formula: "\\frac{d\\Pi}{dr} = \\frac{\\kappa V_{\\text{disp}} K_{\\text{bulk}}}{2\\pi r^3}",
        description: "Pressure gradient from displacement",
        justification: "Matter creates pressure deficits",
        variables: {
          "dΠ/dr": "Pressure gradient",
          "κ": "Geometric coupling",
          "V_disp": "Displacement volume",
          "K_bulk": "Bulk modulus",
          "r": "Distance"
        },
        level: 1,
        parentId: "grav-acceleration"
      },
      {
        id: "spherical-symmetry",
        formula: "g = \\frac{\\kappa V_{\\text{disp}} K_{\\text{bulk}}}{2\\pi \\rho_{\\text{spation}} r^3}",
        description: "Gravitational acceleration magnitude",
        justification: "Spherical symmetry and incompressibility",
        variables: {
          "g": "Gravitational acceleration",
          "κ": "Geometric coupling",
          "V_disp": "Displacement volume",
          "K_bulk": "Bulk modulus",
          "ρ_spation": "Spation density",
          "r": "Distance"
        },
        level: 2,
        parentId: "grav-acceleration"
      },
      {
        id: "derived-g",
        formula: "G = \\frac{\\kappa c^2}{2\\pi \\rho_{\\text{spation}} r}",
        description: "Gravitational constant as derived quantity",
        justification: "Comparing with conventional g = G m / r²",
        variables: {
          "G": "Gravitational constant",
          "κ": "Geometric coupling",
          "c": "Speed of light",
          "ρ_spation": "Spation density",
          "r": "Distance"
        },
        level: 3,
        parentId: "spherical-symmetry"
      }
    ]
  },
  {
    name: "Fine Structure Constant",
    rootFormula: "\\alpha = \\frac{1}{137.035999} = \\varkappa",
    description: "How α emerges from helical orbital quantization",
    steps: [
      {
        id: "helical-quantization",
        formula: "E_n = \\frac{h c n}{2\\pi r_n}",
        description: "Energy levels from helical standing waves",
        justification: "Toroidal electron orbitals form standing waves",
        variables: {
          "E_n": "Energy level n",
          "h": "Planck constant",
          "c": "Speed of light",
          "n": "Quantum number",
          "r_n": "Orbital radius"
        },
        level: 0
      },
      {
        id: "rydberg-formula",
        formula: "E_n = -\\frac{R_H}{n^2}",
        description: "Hydrogen energy levels (Rydberg formula)",
        justification: "Experimental hydrogen spectrum",
        variables: {
          "E_n": "Energy level n",
          "R_H": "Rydberg constant",
          "n": "Principal quantum number"
        },
        level: 1,
        parentId: "helical-quantization"
      },
      {
        id: "orbital-velocity",
        formula: "v = \\varkappa c",
        description: "Orbital velocity as fraction of c",
        justification: "SDT orbital mechanics",
        variables: {
          "v": "Orbital velocity",
          "κ": "Fine structure constant",
          "c": "Speed of light"
        },
        level: 2,
        parentId: "helical-quantization"
      },
      {
        id: "alpha-definition",
        formula: "\\alpha = \\frac{1}{137.035999} = \\varkappa",
        description: "Fine structure constant definition",
        justification: "Matching helical quantization to experimental spectrum",
        variables: {
          "α": "Fine structure constant",
          "κ": "SDT orbital parameter"
        },
        level: 3,
        parentId: "orbital-velocity"
      }
    ]
  }
];

interface FormulaDerivationTreeProps {
  formulaName?: string;
  interactive?: boolean;
  showVariables?: boolean;
}

export default function FormulaDerivationTree({
  formulaName,
  interactive = true,
  showVariables = true
}: FormulaDerivationTreeProps) {
  const [selectedTree, setSelectedTree] = useState(formulaName || derivationTrees[0].name);
  const [expandedSteps, setExpandedSteps] = useState<Set<string>>(new Set());

  const currentTree = useMemo(() => {
    return derivationTrees.find(t => t.name === selectedTree) || derivationTrees[0];
  }, [selectedTree]);

  const toggleStep = (stepId: string) => {
    if (!interactive) return;
    const newExpanded = new Set(expandedSteps);
    if (newExpanded.has(stepId)) {
      newExpanded.delete(stepId);
    } else {
      newExpanded.add(stepId);
    }
    setExpandedSteps(newExpanded);
  };

  const getStepPosition = (step: DerivationStep, allSteps: DerivationStep[]) => {
    const levelSteps = allSteps.filter(s => s.level === step.level);
    const index = levelSteps.indexOf(step);
    return {
      x: (index + 0.5) / levelSteps.length * 100,
      y: step.level * 120 + 100
    };
  };

  const maxLevel = Math.max(...currentTree.steps.map(s => s.level));

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white p-6">
        <h3 className="font-display font-bold text-2xl mb-2">Formula Derivation Trees</h3>
        <p className="text-emerald-100 text-sm">
          How SDT formulas emerge from the four irreducible primitives
        </p>

        {/* Tree selector */}
        {interactive && (
          <div className="mt-4 flex gap-2 flex-wrap">
            {derivationTrees.map(tree => (
              <button
                key={tree.name}
                onClick={() => setSelectedTree(tree.name)}
                className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                  selectedTree === tree.name
                    ? 'bg-white text-emerald-700'
                    : 'bg-emerald-700 text-white hover:bg-emerald-800'
                }`}
              >
                {tree.name}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Description */}
      <div className="bg-slate-50 border-b border-slate-200 px-6 py-4">
        <div className="flex items-center gap-4">
          <div className="text-lg font-display font-semibold text-slate-900">
            {currentTree.name}
          </div>
          <div className="text-sm text-slate-600">
            {currentTree.description}
          </div>
        </div>
        <div className="mt-2 text-sm text-slate-500">
          Root formula: <span className="font-mono bg-slate-100 px-2 py-0.5 rounded">{currentTree.rootFormula}</span>
        </div>
      </div>

      {/* Tree visualization */}
      <div className="p-6">
        <div className="relative" style={{ height: (maxLevel + 1) * 120 + 200 }}>
          {/* Connection lines */}
          <svg className="absolute inset-0 w-full h-full pointer-events-none">
            {currentTree.steps.map(step => {
              if (!step.parentId) return null;
              const parentStep = currentTree.steps.find(s => s.id === step.parentId);
              if (!parentStep) return null;

              const start = getStepPosition(parentStep, currentTree.steps);
              const end = getStepPosition(step, currentTree.steps);

              return (
                <line
                  key={`${step.id}-line`}
                  x1={`${start.x}%`}
                  y1={start.y}
                  x2={`${end.x}%`}
                  y2={end.y}
                  stroke="#cbd5e1"
                  strokeWidth="2"
                  markerEnd="url(#arrowhead)"
                />
              );
            })}
            <defs>
              <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#cbd5e1" />
              </marker>
            </defs>
          </svg>

          {/* Steps */}
          {currentTree.steps.map(step => {
            const position = getStepPosition(step, currentTree.steps);
            const isExpanded = expandedSteps.has(step.id);

            return (
              <div
                key={step.id}
                className={`absolute transform -translate-x-1/2 -translate-y-1/2 transition-all duration-200 ${
                  interactive ? 'cursor-pointer hover:scale-105' : ''
                }`}
                style={{
                  left: `${position.x}%`,
                  top: position.y,
                  minWidth: '280px'
                }}
                onClick={() => toggleStep(step.id)}
              >
                <div className={`bg-white border-2 rounded-lg shadow-lg p-4 ${
                  step.level === 0 ? 'border-emerald-500 bg-emerald-50' :
                  step.level === maxLevel ? 'border-teal-500 bg-teal-50' :
                  'border-slate-300 hover:border-slate-400'
                }`}>
                  {/* Formula */}
                  <div className="text-center mb-2">
                    <div className="font-mono text-sm bg-slate-100 px-2 py-1 rounded inline-block">
                      {step.formula}
                    </div>
                  </div>

                  {/* Description */}
                  <div className="text-sm font-medium text-slate-900 mb-1">
                    {step.description}
                  </div>

                  {/* Justification */}
                  <div className="text-xs text-slate-600 mb-2">
                    {step.justification}
                  </div>

                  {/* Variables */}
                  {showVariables && Object.keys(step.variables).length > 0 && (
                    <div className={`text-xs space-y-1 ${isExpanded ? 'block' : 'hidden'}`}>
                      <div className="font-medium text-slate-700">Variables:</div>
                      {Object.entries(step.variables).map(([varName, varDesc]) => (
                        <div key={varName} className="flex justify-between">
                          <span className="font-mono text-slate-600">{varName}:</span>
                          <span className="text-slate-500">{varDesc}</span>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Expand indicator */}
                  {interactive && Object.keys(step.variables).length > 0 && (
                    <div className="text-xs text-slate-400 text-center mt-2">
                      {isExpanded ? '▼' : '▶'} Click to {isExpanded ? 'collapse' : 'expand'}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Footer */}
      <div className="bg-slate-50 border-t border-slate-200 px-6 py-4">
        <div className="text-sm text-slate-600 text-center">
          <div className="mb-2">
            <span className="font-medium">Legend:</span>
            <span className="ml-4">Primitives → Intermediate → Final Formula</span>
          </div>
          <div className="text-xs text-slate-500">
            All derivations start from the four irreducible primitives: SPACE, MATTER, MOVEMENT, NOW
          </div>
        </div>
      </div>
    </div>
  );
}

