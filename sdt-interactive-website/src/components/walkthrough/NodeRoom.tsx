/**
 * NodeRoom - Displays individual node content with 3D visualization
 */

import React, { useState } from 'react';
import { useNavigationStore } from '../../store/navigationStore';

interface NodeRoomProps {
  onReturn: () => void;
}

export default function NodeRoom({ onReturn }: NodeRoomProps) {
  const { currentNode } = useNavigationStore();
  const [expandedSection, setExpandedSection] = useState<string | null>(null);

  // Placeholder content - will be loaded from content files
  const nodeContent = {
    title: 'What if Space Isn\'t Empty?',
    readingTime: 2,
    mainContent: `
For a century, we've described atoms with probability waves and gravity as curved spacetime. 
But what if there's a simpler explanation?

**What if space itself is a pressurized medium, and particles are stable structures within it?**

Instead of starting with quantum postulates, SDT derives atomic structure, orbital mechanics, 
and gravitational phenomena from a single geometric principle:

**Particles are stable toroidal vortices in an incompressible medium ("spation"), and all forces 
arise from pressure gradients—not from fields, curvature, or probability amplitudes.**
    `,
    expansions: {
      'know-more': {
        title: 'Do you want to know more?',
        content: `
**Why does this matter?**
If SDT is correct, it unifies all of physics under a single geometric principle. No more 
incompatibility between quantum mechanics and general relativity.

**How is this different from other theories?**
SDT doesn't require quantum postulates, curved spacetime, or dark matter. Everything emerges 
from pressure dynamics in a single medium.

**What evidence supports this?**
16 out of 24 benchmarks have been validated with errors less than 1%, spanning 53 orders of 
magnitude from atoms to galaxies.
        `,
      },
      'tech-specs': {
        title: 'Technical Specifications',
        content: `
**Spation Density:** ρ_s = 5.2×10⁹⁶ kg/m³

**Bulk Modulus:** K_bulk = 4.6×10¹¹³ Pa

**Master Equation:**
∇·[K_bulk ∇Δ(x)] = -κ ρ_disp(x) (1 - E(x,n̂))

Where:
- K_bulk: Spation stiffness
- ρ_disp: Displacement density (matter)
- E(x,n̂): Directional occlusion function
        `,
      },
      'simulation': {
        title: 'Interactive Simulation',
        content: '3D pressure field visualization will appear here',
        simulationId: 'pressure-field',
      },
    },
  };

  return (
    <div className="absolute inset-0 bg-slate-900/95 backdrop-blur-sm text-white overflow-y-auto">
      <div className="max-w-6xl mx-auto p-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={onReturn}
            className="mb-4 text-slate-400 hover:text-white transition-colors flex items-center gap-2"
          >
            ← Back to Path
          </button>
          <h1 className="text-4xl font-display font-bold mb-2">{nodeContent.title}</h1>
          <div className="text-sm text-slate-400">{nodeContent.readingTime} min read</div>
        </div>

        {/* Main Content */}
        <div className="prose prose-invert max-w-none mb-8">
          <div className="whitespace-pre-line text-lg leading-relaxed">
            {nodeContent.mainContent}
          </div>
        </div>

        {/* Expansion Points */}
        <div className="space-y-4">
          {Object.entries(nodeContent.expansions).map(([key, expansion]) => (
            <div
              key={key}
              className="bg-white/5 border border-white/10 rounded-xl p-6"
            >
              <button
                onClick={() => setExpandedSection(expandedSection === key ? null : key)}
                className="w-full text-left flex items-center justify-between mb-2"
              >
                <h3 className="text-xl font-display font-semibold text-amber-400">
                  {expansion.title}
                </h3>
                <span className="text-2xl">
                  {expandedSection === key ? '▼' : '▶'}
                </span>
              </button>
              {expandedSection === key && (
                <div className="mt-4 prose prose-invert max-w-none">
                  <div className="whitespace-pre-line">{expansion.content}</div>
                  {expansion.simulationId && (
                    <div className="mt-4 p-4 bg-slate-800 rounded-lg">
                      <div className="text-slate-400">Simulation: {expansion.simulationId}</div>
                      {/* Simulation component will be rendered here */}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}


