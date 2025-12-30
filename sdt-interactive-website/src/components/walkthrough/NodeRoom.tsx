/**
 * NodeRoom - Displays individual node content with 3D visualization
 * 
 * Features:
 * - Dynamic content loading from JSON files
 * - Veritasium-style narration integration
 * - "Would you like to know more?" expansion pattern
 * - Simulation embedding
 */

import React, { useState, useEffect, useMemo } from 'react';
import { useNavigationStore } from '../../store/navigationStore';
import { loadNodeContent } from '../../utils/content-loader';
import type { NodeContent, PathType } from '../../types/content';
import NarrationPlayer from '../ui/NarrationPlayer';
import ExpansionCard, { ExpansionCardList, ExpansionData } from '../ui/ExpansionCard';
import { PressureFieldSim, ToroidalElectronSim, GalaxyRotationSim, KLawScaleSim } from '../simulations';

interface NodeRoomProps {
  onReturn: () => void;
}

// Simulation component registry
const SIMULATION_COMPONENTS: Record<string, React.FC<any>> = {
  'pressure-field': PressureFieldSim,
  'toroidal-electron': ToroidalElectronSim,
  'galaxy-rotation': GalaxyRotationSim,
  'k-law-scale-slider': KLawScaleSim,
};

export default function NodeRoom({ onReturn }: NodeRoomProps) {
  const { currentNode, currentPath } = useNavigationStore();
  const [content, setContent] = useState<NodeContent | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeSimulation, setActiveSimulation] = useState<string | null>(null);

  // Load content
  useEffect(() => {
    if (!currentNode || !currentPath) return;

    setIsLoading(true);
    loadNodeContent(currentPath as PathType, currentNode)
      .then((data) => {
        setContent(data);
        setIsLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load content:', err);
        setIsLoading(false);
      });
  }, [currentNode, currentPath]);

  // Convert content expansions to ExpansionData format
  const expansions: ExpansionData[] = useMemo(() => {
    if (!content?.content.expansions) return [];

    return Object.entries(content.content.expansions).map(([id, expansion]) => {
      // Determine category from id
      let category: ExpansionData['category'] = 'know-more';
      if (id.includes('tech') || id.includes('spec')) category = 'tech-specs';
      if (id.includes('sim')) category = 'simulation';
      if (id.includes('example')) category = 'example';
      if (id.includes('history')) category = 'history';

      if (typeof expansion === 'string') {
        return { id, title: id, content: expansion, category };
      }
      return {
        id,
        title: expansion.title || id,
        content: expansion.content,
        simulationId: expansion.simulationId,
        category,
      };
    });
  }, [content]);

  // Handle simulation request
  const handleSimulationRequest = (simulationId: string) => {
    setActiveSimulation(simulationId);
  };

  // Render simulation
  const renderSimulation = () => {
    if (!activeSimulation) return null;

    const SimComponent = SIMULATION_COMPONENTS[activeSimulation];
    if (!SimComponent) {
      return (
        <div className="bg-slate-800 rounded-xl p-8 text-center">
          <p className="text-slate-400">Simulation "{activeSimulation}" coming soon!</p>
        </div>
      );
    }

    return (
      <div className="relative">
        <button
          onClick={() => setActiveSimulation(null)}
          className="absolute top-4 right-4 z-10 bg-slate-800/80 hover:bg-slate-700 text-white px-3 py-1 rounded-lg text-sm"
        >
          ✕ Close
        </button>
        <div className="h-[500px] rounded-xl overflow-hidden">
          <SimComponent />
        </div>
      </div>
    );
  };

  // Parse markdown-like content
  const renderMainContent = (text: string) => {
    const paragraphs = text.split('\n\n');
    return paragraphs.map((para, i) => {
      // Bold
      let html = para.replace(/\*\*(.*?)\*\*/g, '<strong class="text-white">$1</strong>');
      // Italics
      html = html.replace(/\*(.*?)\*/g, '<em class="text-amber-300">$1</em>');
      // Code
      html = html.replace(/`(.*?)`/g, '<code class="bg-slate-700 px-1 rounded text-amber-300 font-mono text-sm">$1</code>');

      return (
        <p
          key={i}
          className="mb-4 text-lg leading-relaxed text-slate-200"
          dangerouslySetInnerHTML={{ __html: html }}
        />
      );
    });
  };

  if (isLoading) {
    return (
      <div className="absolute inset-0 bg-slate-900/95 flex items-center justify-center">
        <div className="text-white text-xl">Loading content...</div>
      </div>
    );
  }

  if (!content) {
    return (
      <div className="absolute inset-0 bg-slate-900/95 flex flex-col items-center justify-center text-white">
        <p className="text-xl mb-4">Content not found</p>
        <button
          onClick={onReturn}
          className="text-amber-400 hover:text-amber-300"
        >
          ← Return to path
        </button>
      </div>
    );
  }

  return (
    <div className="absolute inset-0 bg-slate-900/95 backdrop-blur-sm text-white overflow-y-auto">
      <div className="max-w-4xl mx-auto p-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={onReturn}
            className="mb-4 text-slate-400 hover:text-white transition-colors flex items-center gap-2 group"
          >
            <span className="group-hover:-translate-x-1 transition-transform">←</span>
            Back to Path
          </button>

          {/* Hook (Starship Troopers style) */}
          {(content as any).hook && (
            <div className="mb-4 text-amber-400 text-lg font-bold tracking-wide uppercase">
              {(content as any).hook}
            </div>
          )}

          <h1 className="text-4xl font-display font-bold mb-3 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
            {content.title}
          </h1>
          <div className="flex items-center gap-4 text-sm text-slate-400">
            <span>📖 {content.readingTime} min read</span>
            {content.narration && (
              <span>🎧 Narration available</span>
            )}
          </div>
        </div>

        {/* Narration Player */}
        {content.narration && (
          <div className="mb-8">
            <NarrationPlayer narration={content.narration} showTranscript={true} />
          </div>
        )}

        {/* Active Simulation */}
        {activeSimulation && (
          <div className="mb-8">
            {renderSimulation()}
          </div>
        )}

        {/* Main Content */}
        <div className="mb-12 prose prose-invert max-w-none">
          {renderMainContent(content.content.main)}
        </div>

        {/* Expansion Cards - "Would you like to know more?" */}
        {expansions.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <span className="text-3xl">🎬</span>
              Would you like to know more?
            </h2>
            <ExpansionCardList
              expansions={expansions}
              onSimulationRequest={handleSimulationRequest}
            />
          </div>
        )}

        {/* Formulas */}
        {content.visualizations?.formulas && content.visualizations.formulas.length > 0 && (
          <div className="mb-8 p-6 bg-slate-800/50 rounded-xl border border-slate-700">
            <h3 className="text-lg font-bold mb-4 text-amber-400">Key Formulas</h3>
            <div className="space-y-3">
              {content.visualizations.formulas.map((formula, i) => (
                <div key={i} className="font-mono text-lg text-center p-3 bg-slate-900/50 rounded-lg">
                  {formula}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Navigation */}
        <div className="border-t border-slate-700 pt-8 flex justify-between">
          <button
            onClick={onReturn}
            className="px-6 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors"
          >
            ← Back to Path
          </button>
          
          {content.nextNodeId && (
            <button
              onClick={() => {
                const { navigateToNode } = useNavigationStore.getState();
                navigateToNode(content.nextNodeId!);
              }}
              className="px-6 py-3 rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-900 font-bold transition-colors"
            >
              Continue →
            </button>
          )}
        </div>
      </div>
    </div>
  );
}





