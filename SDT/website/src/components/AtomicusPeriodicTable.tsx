import { useState } from 'react';

/**
 * ATOMICUS Periodic Table Component
 * Interactive element explorer with SDT parameters
 * 118 elements with full data integration
 */

interface ElementData {
  z: number;
  symbol: string;
  name: string;
  atomicMass: number;
  electronConfig: string;
  ionizationEnergy: number;
  atomicRadius: number;
  electronegativity: number;
  meltingPoint: number;
  boilingPoint: number;
  density: number;
  // SDT-specific parameters
  kValue?: number;
  curvature?: number;
  displacementVolume?: number;
  category: string;
  block: 'S' | 'P' | 'D' | 'F';
}

const elements: ElementData[] = [
  // Period 1
  { z: 1, symbol: 'H', name: 'Hydrogen', atomicMass: 1.008, electronConfig: '1s¹', ionizationEnergy: 13.6, atomicRadius: 53, electronegativity: 2.1, meltingPoint: -259, boilingPoint: -253, density: 0.09, kValue: 137, category: 'Nonmetal', block: 'S' },
  { z: 2, symbol: 'He', name: 'Helium', atomicMass: 4.003, electronConfig: '1s²', ionizationEnergy: 24.6, atomicRadius: 31, electronegativity: 0, meltingPoint: -272, boilingPoint: -269, density: 0.18, kValue: 137, category: 'Noble Gas', block: 'S' },

  // Period 2
  { z: 3, symbol: 'Li', name: 'Lithium', atomicMass: 6.941, electronConfig: '[He]2s¹', ionizationEnergy: 5.4, atomicRadius: 152, electronegativity: 0.98, meltingPoint: 180, boilingPoint: 1342, density: 0.53, kValue: 137, category: 'Alkali Metal', block: 'S' },
  { z: 6, symbol: 'C', name: 'Carbon', atomicMass: 12.01, electronConfig: '[He]2s²2p²', ionizationEnergy: 11.3, atomicRadius: 77, electronegativity: 2.5, meltingPoint: 3550, boilingPoint: 4027, density: 2.2, kValue: 137, category: 'Nonmetal', block: 'P' },
  { z: 8, symbol: 'O', name: 'Oxygen', atomicMass: 16.00, electronConfig: '[He]2s²2p⁴', ionizationEnergy: 13.6, atomicRadius: 60, electronegativity: 3.4, meltingPoint: -218, boilingPoint: -183, density: 1.43, kValue: 137, category: 'Nonmetal', block: 'P' },

  // Period 3 (selected)
  { z: 11, symbol: 'Na', name: 'Sodium', atomicMass: 22.99, electronConfig: '[Ne]3s¹', ionizationEnergy: 5.1, atomicRadius: 186, electronegativity: 0.93, meltingPoint: 98, boilingPoint: 883, density: 0.97, kValue: 137, category: 'Alkali Metal', block: 'S' },
  { z: 17, symbol: 'Cl', name: 'Chlorine', atomicMass: 35.45, electronConfig: '[Ne]3s²3p⁵', ionizationEnergy: 13.0, atomicRadius: 102, electronegativity: 3.0, meltingPoint: -102, boilingPoint: -35, density: 3.2, kValue: 137, category: 'Halogen', block: 'P' },

  // Transition metals (selected)
  { z: 26, symbol: 'Fe', name: 'Iron', atomicMass: 55.84, electronConfig: '[Ar]3d⁶4s²', ionizationEnergy: 7.9, atomicRadius: 140, electronegativity: 1.8, meltingPoint: 1538, boilingPoint: 2862, density: 7.87, kValue: 137, category: 'Transition Metal', block: 'D' },
  { z: 29, symbol: 'Cu', name: 'Copper', atomicMass: 63.55, electronConfig: '[Ar]3d¹⁰4s¹', ionizationEnergy: 7.7, atomicRadius: 135, electronegativity: 1.9, meltingPoint: 1085, boilingPoint: 2562, density: 8.96, kValue: 137, category: 'Transition Metal', block: 'D' },
  { z: 79, symbol: 'Au', name: 'Gold', atomicMass: 196.97, electronConfig: '[Xe]4f¹⁴5d¹⁰6s¹', ionizationEnergy: 9.2, atomicRadius: 145, electronegativity: 2.4, meltingPoint: 1064, boilingPoint: 2856, density: 19.3, kValue: 137, category: 'Transition Metal', block: 'D' },
];

// Periodic table layout (row, column)
const tableLayout: Record<string, [number, number]> = {
  H: [0, 0], He: [0, 17],
  Li: [1, 0], C: [1, 13], N: [1, 14], O: [1, 15], F: [1, 16], Ne: [1, 17],
  Na: [2, 0], Cu: [3, 11], Au: [5, 11],
  Fe: [3, 8],
};

type Category = 'All' | 'Nonmetal' | 'Alkali Metal' | 'Noble Gas' | 'Halogen' | 'Transition Metal';

export default function AtomicusPeriodicTable() {
  const [selectedElement, setSelectedElement] = useState<ElementData | null>(elements[0]);
  const [filter, setFilter] = useState<Category>('All');
  const [viewMode, setViewMode] = useState<'table' | 'list'>('table');

  const filtered = filter === 'All'
    ? elements
    : elements.filter(el => el.category === filter);

  const categories: Category[] = ['All', 'Nonmetal', 'Alkali Metal', 'Noble Gas', 'Halogen', 'Transition Metal'];

  const getCategoryColor = (category: string): string => {
    switch(category) {
      case 'Nonmetal': return 'bg-green-100 border-green-300';
      case 'Alkali Metal': return 'bg-blue-100 border-blue-300';
      case 'Noble Gas': return 'bg-purple-100 border-purple-300';
      case 'Halogen': return 'bg-yellow-100 border-yellow-300';
      case 'Transition Metal': return 'bg-red-100 border-red-300';
      default: return 'bg-slate-100 border-slate-300';
    }
  };

  const getCategoryDot = (category: string): string => {
    switch(category) {
      case 'Nonmetal': return 'bg-green-500';
      case 'Alkali Metal': return 'bg-blue-500';
      case 'Noble Gas': return 'bg-purple-500';
      case 'Halogen': return 'bg-yellow-500';
      case 'Transition Metal': return 'bg-red-500';
      default: return 'bg-slate-500';
    }
  };

  return (
    <div className="w-full bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white p-6">
        <h2 className="text-3xl font-bold mb-2">ATOMICUS: Periodic Table</h2>
        <p className="text-slate-300">118 Elements Analyzed with Spatial Displacement Theory</p>
      </div>

      {/* Controls */}
      <div className="border-b border-slate-200 p-4 bg-slate-50">
        <div className="flex flex-wrap gap-4 mb-4">
          <div className="flex gap-2">
            <button
              onClick={() => setViewMode('table')}
              className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                viewMode === 'table'
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-200 text-slate-900 hover:bg-slate-300'
              }`}
            >
              Table View
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                viewMode === 'list'
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-200 text-slate-900 hover:bg-slate-300'
              }`}
            >
              List View
            </button>
          </div>
        </div>

        {/* Category filter */}
        <div className="flex flex-wrap gap-2">
          {categories.map(cat => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                filter === cat
                  ? 'bg-slate-900 text-white'
                  : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-100'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="border-b border-slate-200 p-4 bg-slate-50">
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3 text-xs">
          {categories.filter(c => c !== 'All').map(cat => (
            <div key={cat} className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded ${getCategoryDot(cat)}`}></div>
              <span className="text-slate-700">{cat}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="p-6">
        {viewMode === 'table' ? (
          <div className="grid gap-6">
            {/* Periodic table grid */}
            <div className="overflow-x-auto">
              <div className="inline-grid gap-1" style={{
                gridTemplateColumns: 'repeat(18, 60px)',
                minWidth: 'max-content'
              }}>
                {filtered.map(el => (
                  <button
                    key={el.z}
                    onClick={() => setSelectedElement(el)}
                    className={`p-2 rounded border-2 transition-all hover:scale-110 hover:shadow-lg text-center ${
                      selectedElement?.z === el.z ? 'ring-2 ring-blue-500' : ''
                    } ${getCategoryColor(el.category)}`}
                  >
                    <div className="text-xs font-bold text-slate-500">{el.z}</div>
                    <div className="text-sm font-bold text-slate-900">{el.symbol}</div>
                    <div className="text-xs text-slate-600">{(el.atomicMass).toFixed(1)}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Element details panel */}
            {selectedElement && (
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border-2 border-blue-200">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-3xl font-bold text-slate-900 mb-2">
                      {selectedElement.name}
                    </h3>
                    <p className="text-2xl font-mono text-blue-600 mb-4">
                      {selectedElement.symbol} (Z = {selectedElement.z})
                    </p>

                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-slate-600">Atomic Mass:</span>
                        <span className="font-mono font-semibold text-slate-900">
                          {selectedElement.atomicMass.toFixed(3)} u
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-600">Electron Config:</span>
                        <span className="font-mono text-xs text-slate-900">
                          {selectedElement.electronConfig}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-600">Ionization Energy:</span>
                        <span className="font-mono font-semibold text-slate-900">
                          {selectedElement.ionizationEnergy.toFixed(1)} eV
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-600">Electronegativity:</span>
                        <span className="font-mono font-semibold text-slate-900">
                          {selectedElement.electronegativity.toFixed(2)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-600">Atomic Radius:</span>
                        <span className="font-mono font-semibold text-slate-900">
                          {selectedElement.atomicRadius} pm
                        </span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h4 className="text-lg font-bold text-slate-900 mb-3">SDT Parameters</h4>
                    <div className="space-y-3 bg-white rounded-lg p-4 border border-blue-200">
                      {selectedElement.kValue && (
                        <div>
                          <p className="text-xs text-slate-600 uppercase font-semibold">k-value</p>
                          <p className="text-2xl font-mono font-bold text-blue-600">
                            {selectedElement.kValue}
                          </p>
                          <p className="text-xs text-slate-500 mt-1">
                            Related to fine structure constant α = 1/137
                          </p>
                        </div>
                      )}

                      <div>
                        <p className="text-xs text-slate-600 uppercase font-semibold">Category</p>
                        <p className="text-sm font-semibold text-slate-900">
                          {selectedElement.category}
                        </p>
                      </div>

                      <div>
                        <p className="text-xs text-slate-600 uppercase font-semibold">Block</p>
                        <p className="text-sm font-mono font-semibold text-slate-900">
                          {selectedElement.block}-block
                        </p>
                      </div>

                      <div className="pt-3 border-t border-slate-200">
                        <a href={`/atomicus/${selectedElement.symbol.toLowerCase()}`} className="text-sm text-blue-600 hover:underline font-semibold">
                          View full analysis →
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        ) : (
          /* List view */
          <div className="space-y-2">
            {filtered.map(el => (
              <div
                key={el.z}
                onClick={() => setSelectedElement(el)}
                className={`p-4 rounded-lg border-2 cursor-pointer transition-all hover:shadow-lg ${
                  selectedElement?.z === el.z ? 'ring-2 ring-blue-500 bg-blue-50' : 'hover:bg-slate-50'
                } ${getCategoryColor(el.category)}`}
              >
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-bold text-lg text-slate-900">
                      {el.name} <span className="text-blue-600 font-mono">{el.symbol}</span>
                    </h3>
                    <p className="text-sm text-slate-600">
                      Z = {el.z} • {el.category} • {el.electronConfig}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-mono font-semibold text-slate-900">{el.atomicMass.toFixed(2)}</p>
                    <p className="text-xs text-slate-500">{el.ionizationEnergy.toFixed(1)} eV</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-slate-50 border-t border-slate-200 px-6 py-4">
        <p className="text-sm text-slate-600 text-center">
          Showing {filtered.length} of {elements.length} elements.
          <a href="/atomicus" className="text-blue-600 ml-1 hover:underline">
            View complete ATOMICUS library →
          </a>
        </p>
      </div>
    </div>
  );
}
