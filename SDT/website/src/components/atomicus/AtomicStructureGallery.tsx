/**
 * SDT Atomic Structure Gallery
 * 
 * Interactive gallery showing atoms visualized according to
 * Spatial Displacement Theory principles:
 * - Nuclear geometry determines electron positioning
 * - Electrons as toroidal circulations in pressure minima
 * - Element families emerge from valence structure
 */

import React, { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Environment } from '@react-three/drei';
import AtomicStructureVisualizer, { ELEMENTS, FAMILY_COLORS } from './AtomicStructureVisualizer';
import GeometricSpinner from '../ui/GeometricSpinner';

// Elements to display in gallery - organized to show families
const GALLERY_ELEMENTS = [
  // Period 1
  'H', 'D', 'He4',
  // Period 2 - shows all families
  'Li7', 'Be9', 'C12', 'N14', 'O16', 'F19', 'Ne20',
  // Period 3 examples
  'Na23', 'Cl35',
  // Transition metal
  'Fe56'
] as const;

// Family display names
const FAMILY_NAMES: Record<string, string> = {
  'hydrogen': 'Hydrogen',
  'alkali-metal': 'Alkali Metal',
  'alkaline-earth': 'Alkaline Earth',
  'boron-group': 'Boron Group',
  'carbon-group': 'Carbon Group',
  'nitrogen-group': 'Nitrogen Group',
  'chalcogen': 'Chalcogen',
  'halogen': 'Halogen',
  'noble-gas': 'Noble Gas',
  'transition-metal': 'Transition Metal',
};

// Nuclear structure display
const STRUCTURE_NAMES: Record<string, string> = {
  'proton': 'Single proton',
  'deuteron': 'Deuteron (p+n)',
  'alpha': 'Alpha (2D at 90°)',
  'alpha-d': 'Alpha + extras',
  'tri-alpha-d': 'Tri-alpha (τ) + D',
  'multi-alpha': 'Multi-alpha cluster',
};

interface ElementCardProps {
  elementKey: keyof typeof ELEMENTS;
  selected: boolean;
  onClick: () => void;
}

function ElementCard({ elementKey, selected, onClick }: ElementCardProps) {
  const config = ELEMENTS[elementKey];
  if (!config) return null;
  
  const familyColor = FAMILY_COLORS[config.family];
  const colorHex = familyColor ? `#${familyColor.getHexString()}` : '#ffffff';
  
  // Count valence electrons
  const valenceCount = config.shells.reduce((sum, shell) => 
    sum + shell.subshells.filter(s => s.isValence).reduce((s, sub) => s + sub.electrons, 0), 0
  );

  return (
    <button
      onClick={onClick}
      className={`
        relative p-4 rounded-xl border-2 transition-all duration-300 min-w-[100px]
        ${selected 
          ? 'scale-105 shadow-lg' 
          : 'border-slate-700 bg-slate-800/50 hover:border-slate-500 hover:bg-slate-700/50'
        }
      `}
      style={{
        borderColor: selected ? colorHex : undefined,
        backgroundColor: selected ? `${colorHex}20` : undefined,
        boxShadow: selected ? `0 10px 25px ${colorHex}40` : undefined,
      }}
    >
      {/* Element symbol */}
      <div 
        className="text-3xl font-bold mb-1"
        style={{ color: selected ? colorHex : 'white' }}
      >
        {config.symbol}
      </div>
      
      {/* Element name */}
      <div className="text-xs text-slate-400 mb-2">
        {config.name}
      </div>
      
      {/* Valence electrons badge */}
      <div 
        className="inline-block px-2 py-0.5 text-xs rounded-full"
        style={{ 
          backgroundColor: `${colorHex}30`,
          color: colorHex,
        }}
      >
        {valenceCount}e⁻ valence
      </div>
      
      {/* Selection indicator */}
      {selected && (
        <div 
          className="absolute -top-1 -right-1 w-3 h-3 rounded-full animate-pulse"
          style={{ backgroundColor: colorHex }}
        />
      )}
    </button>
  );
}

export default function AtomicStructureGallery() {
  const [selectedElement, setSelectedElement] = useState<keyof typeof ELEMENTS>('O16');
  const [showElectrons, setShowElectrons] = useState(true);
  const [showLabels, setShowLabels] = useState(true);
  const [autoRotate, setAutoRotate] = useState(true);
  
  const config = ELEMENTS[selectedElement];
  
  // Count electrons
  const valenceCount = config?.shells.reduce((sum, shell) => 
    sum + shell.subshells.filter(s => s.isValence).reduce((s, sub) => s + sub.electrons, 0), 0
  ) || 0;
  
  const coreCount = config?.shells.reduce((sum, shell) => 
    sum + shell.subshells.filter(s => !s.isValence).reduce((s, sub) => s + sub.electrons, 0), 0
  ) || 0;
  
  const familyColor = config ? FAMILY_COLORS[config.family] : null;
  const colorHex = familyColor ? `#${familyColor.getHexString()}` : '#ffd54f';

  return (
    <div className="w-full min-h-screen bg-slate-900">
      {/* Header */}
      <div className="text-center py-8 px-4">
        <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
          <span className="bg-gradient-to-r from-amber-400 via-orange-400 to-amber-400 bg-clip-text text-transparent">
            SDT Atomic Structure
          </span>
        </h1>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Atoms visualized as <strong className="text-amber-400">pressure-displacement systems</strong>. 
          Nuclear packing creates occlusion geometry that determines where electrons are found.
        </p>
        <p className="text-slate-500 text-sm mt-2">
          Electrons shown in experimental probability cloud positions (s=spherical, p=dumbbell lobes)
        </p>
      </div>

      {/* Element selector */}
      <div className="px-4 pb-4">
        <div className="max-w-5xl mx-auto">
          <div className="flex flex-wrap justify-center gap-3">
            {GALLERY_ELEMENTS.map((key) => (
              <ElementCard
                key={key}
                elementKey={key}
                selected={selectedElement === key}
                onClick={() => setSelectedElement(key)}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Main 3D viewer */}
      <div className="relative w-full h-[500px] md:h-[600px]">
        <Canvas gl={{ antialias: true, alpha: false }}>
          <Suspense fallback={null}>
            {/* Lighting */}
            <ambientLight intensity={0.4} />
            <directionalLight position={[5, 5, 5]} intensity={0.7} />
            <directionalLight position={[-5, -5, -5]} intensity={0.3} />
            <pointLight position={[0, 0, 0]} intensity={0.2} color="#ffd54f" />
            
            {/* Camera */}
            <PerspectiveCamera makeDefault position={[0, 0, 5]} fov={50} />
            
            {/* Controls */}
            <OrbitControls
              enablePan={false}
              minDistance={2}
              maxDistance={10}
              autoRotate={autoRotate}
              autoRotateSpeed={0.3}
            />
            
            {/* Atomic structure */}
            <AtomicStructureVisualizer
              element={selectedElement}
              showElectrons={showElectrons}
              showLabels={showLabels}
              scale={1}
            />
            
            {/* Environment */}
            <Environment preset="night" />
            <color attach="background" args={['#0f172a']} />
          </Suspense>
        </Canvas>
        
        {/* Loading overlay */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <Suspense fallback={<GeometricSpinner size="lg" variant="flower" />}>
            <div />
          </Suspense>
        </div>
      </div>

      {/* Info panel */}
      {config && (
        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 md:p-8 border border-slate-700">
            {/* Title row */}
            <div className="flex items-start justify-between mb-6">
              <div>
                <h2 className="text-3xl font-bold text-white">
                  {config.symbol}
                </h2>
                <p className="text-xl text-slate-400">{config.name}</p>
                <span 
                  className="inline-block mt-2 px-3 py-1 text-sm rounded-full"
                  style={{ backgroundColor: `${colorHex}30`, color: colorHex }}
                >
                  {FAMILY_NAMES[config.family] || config.family}
                </span>
              </div>
            <div className="text-right">
              <div className="text-sm text-slate-500">Nuclear Structure</div>
              <div className="font-mono text-lg text-amber-400">
                {STRUCTURE_NAMES[config.nuclearStructure] || config.nuclearStructure}
              </div>
              {config.alphaCount > 0 && (
                <div className="text-xs text-slate-500">
                  {config.alphaCount}α{config.extraDeuterons > 0 ? ` + ${config.extraDeuterons}D` : ''}
                  {config.extraProtons > 0 ? ` + ${config.extraProtons}p` : ''}
                  {config.extraNeutrons > 0 ? ` + ${config.extraNeutrons}n` : ''}
                </div>
              )}
            </div>
            </div>

            {/* Stats grid */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
              <div className="bg-slate-900/50 rounded-lg p-4">
                <div className="text-2xl font-bold text-red-400">{config.Z}</div>
                <div className="text-xs text-slate-500">Protons</div>
              </div>
              <div className="bg-slate-900/50 rounded-lg p-4">
                <div className="text-2xl font-bold text-blue-400">{config.N}</div>
                <div className="text-xs text-slate-500">Neutrons</div>
              </div>
              <div className="bg-slate-900/50 rounded-lg p-4">
                <div className="text-2xl font-bold text-cyan-400">{coreCount}</div>
                <div className="text-xs text-slate-500">Core e⁻</div>
              </div>
              <div className="bg-slate-900/50 rounded-lg p-4">
                <div className="text-2xl font-bold" style={{ color: colorHex }}>
                  {valenceCount}
                </div>
                <div className="text-xs text-slate-500">Valence e⁻</div>
              </div>
              <div className="bg-slate-900/50 rounded-lg p-4">
                <div className="text-2xl font-bold text-slate-300">{config.shells.length}</div>
                <div className="text-xs text-slate-500">Shells</div>
              </div>
            </div>

            {/* Shell structure */}
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-slate-400 mb-3">
                Electron Shell Structure
              </h3>
              <div className="flex flex-wrap gap-2">
                {config.shells.map((shell, i) => (
                  <div key={i} className="flex gap-1">
                    {shell.subshells.map((sub, j) => (
                      <span
                        key={j}
                        className={`px-2 py-1 text-sm rounded font-mono ${
                          sub.isValence 
                            ? 'bg-amber-500/30 text-amber-300 border border-amber-500/50' 
                            : 'bg-slate-700/50 text-slate-400'
                        }`}
                      >
                        {shell.n}{sub.type}<sup>{sub.electrons}</sup>
                      </span>
                    ))}
                  </div>
                ))}
              </div>
            </div>

            {/* Description */}
            <p className="text-slate-300 mb-6">{config.description}</p>

            {/* Legend */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-red-600 border border-red-400" />
                <span className="text-slate-400">Proton (trefoil toroid)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-blue-600 border border-blue-400" />
                <span className="text-slate-400">Neutron (trefoil toroid)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-cyan-400/50 border border-cyan-400" />
                <span className="text-slate-400">Core orbital cloud</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-amber-400/50 border border-amber-400" />
                <span className="text-slate-400">Valence orbital cloud</span>
              </div>
            </div>

            {/* Controls */}
            <div className="flex flex-wrap gap-4">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={showElectrons}
                  onChange={(e) => setShowElectrons(e.target.checked)}
                  className="w-4 h-4 rounded border-slate-600 bg-slate-800 text-amber-500 focus:ring-amber-500"
                />
                <span className="text-slate-300">Show Electrons</span>
              </label>
              
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={showLabels}
                  onChange={(e) => setShowLabels(e.target.checked)}
                  className="w-4 h-4 rounded border-slate-600 bg-slate-800 text-amber-500 focus:ring-amber-500"
                />
                <span className="text-slate-300">Show Labels</span>
              </label>
              
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={autoRotate}
                  onChange={(e) => setAutoRotate(e.target.checked)}
                  className="w-4 h-4 rounded border-slate-600 bg-slate-800 text-amber-500 focus:ring-amber-500"
                />
                <span className="text-slate-300">Auto Rotate</span>
              </label>
            </div>
          </div>
        </div>
      )}

      {/* SDT Principles */}
      <div className="max-w-4xl mx-auto px-4 pb-8">
        <div className="bg-gradient-to-r from-amber-900/20 to-orange-900/20 rounded-xl p-6 border border-amber-700/30">
          <h3 className="text-lg font-semibold text-amber-300 mb-3">
            SDT Atomic Visualization Principles
          </h3>
          <ul className="space-y-2 text-slate-300 text-sm">
            <li className="flex gap-2">
              <span className="text-amber-400">●</span>
              <span><strong>Deuteron</strong>: Two flattened toroids (proton + neutron) stacked coaxially with shared electron path</span>
            </li>
            <li className="flex gap-2">
              <span className="text-amber-400">●</span>
              <span><strong>Alpha particle</strong>: Two deuterons at 90° to each other — electron paths run between them</span>
            </li>
            <li className="flex gap-2">
              <span className="text-amber-400">●</span>
              <span><strong>Nuclear rotation</strong>: Whole nucleus rotates, matching electron shell positions</span>
            </li>
            <li className="flex gap-2">
              <span className="text-amber-400">●</span>
              <span><strong>Nucleon spin</strong>: Individual protons/neutrons spin "crazy fast" in place, not with nuclear rotation</span>
            </li>
            <li className="flex gap-2">
              <span className="text-amber-400">●</span>
              <span><strong>Electrons found</strong> in experimental probability cloud positions — nuclear packing determines where</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
