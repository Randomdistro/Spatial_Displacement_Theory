/**
 * Creative Agent: Atomic Structure Gallery
 * 
 * TEKNE: The gallery IS the periodic pattern
 * 
 * A beautiful gallery of atomic structures showing:
 * - Progressive complexity from H to Fe
 * - Building block decomposition
 * - Electron shell configurations
 * - Binding energies
 * 
 * "Necessarily false" visualizations - representative abstractions
 * that capture the geometric truth.
 */

import React, { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Environment } from '@react-three/drei';
import AtomicStructureVisualizer, { ELEMENTS, NUCLEAR_COLORS } from './AtomicStructureVisualizer';
import SacredGeometryBackground from '../3d/SacredGeometryBackground';
import AtmosphericEffects from '../3d/AtmosphericEffects';
import GeometricSpinner from '../ui/GeometricSpinner';

// Elements to display in gallery
const GALLERY_ELEMENTS = [
  'H', 'D', 'He3', 'He4', 'Li6', 'Li7', 'Be9', 'C12', 'N14', 'O16', 'Fe56'
] as const;

interface ElementCardProps {
  elementKey: keyof typeof ELEMENTS;
  selected: boolean;
  onClick: () => void;
}

function ElementCard({ elementKey, selected, onClick }: ElementCardProps) {
  const config = ELEMENTS[elementKey];
  if (!config) return null;

  return (
    <button
      onClick={onClick}
      className={`
        relative p-4 rounded-xl border-2 transition-all duration-300
        ${selected 
          ? 'border-amber-500 bg-amber-500/20 scale-105 shadow-lg shadow-amber-500/30' 
          : 'border-slate-700 bg-slate-800/50 hover:border-slate-500 hover:bg-slate-700/50'
        }
      `}
    >
      {/* Element symbol */}
      <div className={`text-3xl font-bold mb-1 ${selected ? 'text-amber-400' : 'text-white'}`}>
        {config.symbol}
      </div>
      
      {/* Element name */}
      <div className="text-xs text-slate-400">
        {config.name}
      </div>
      
      {/* Composition badges */}
      <div className="flex gap-1 mt-2 justify-center">
        {config.alphas > 0 && (
          <span className="px-1.5 py-0.5 text-xs rounded bg-orange-500/30 text-orange-300">
            {config.alphas}α
          </span>
        )}
        {config.deuterons > 0 && (
          <span className="px-1.5 py-0.5 text-xs rounded bg-amber-500/30 text-amber-300">
            {config.deuterons}D
          </span>
        )}
        {config.bridges > 0 && (
          <span className="px-1.5 py-0.5 text-xs rounded bg-slate-500/30 text-slate-300">
            {config.bridges}n
          </span>
        )}
      </div>
      
      {/* Selection indicator */}
      {selected && (
        <div className="absolute -top-1 -right-1 w-3 h-3 bg-amber-500 rounded-full animate-pulse" />
      )}
    </button>
  );
}

export default function AtomicStructureGallery() {
  const [selectedElement, setSelectedElement] = useState<keyof typeof ELEMENTS>('C12');
  const [showElectrons, setShowElectrons] = useState(true);
  const [showLabels, setShowLabels] = useState(true);
  const [autoRotate, setAutoRotate] = useState(true);
  
  const config = ELEMENTS[selectedElement];

  return (
    <div className="w-full min-h-screen bg-slate-900">
      {/* Header */}
      <div className="text-center py-8 px-4">
        <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
          <span className="bg-gradient-to-r from-amber-400 via-orange-400 to-amber-400 bg-clip-text text-transparent">
            Atomic Structure Gallery
          </span>
        </h1>
        <p className="text-slate-400 max-w-2xl mx-auto">
          SDT nuclear architectures visualized. Each nucleus is a geometric assembly 
          of turbine cells — protons and neutrons — held by circulating neutrino flux.
        </p>
        <p className="text-amber-500/70 text-sm mt-2 italic">
          "Necessarily false" visualizations — representative abstractions of impossible detail
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
            {/* Background */}
            <SacredGeometryBackground
              variant="metatron"
              opacity={0.05}
              scale={15}
              animated={true}
            />
            
            {/* Atmosphere */}
            <AtmosphericEffects
              particleCount={300}
              glowIntensity={0.15}
            />
            
            {/* Lighting */}
            <ambientLight intensity={0.4} />
            <directionalLight position={[5, 5, 5]} intensity={0.8} />
            <pointLight position={[0, 0, 0]} intensity={0.3} color="#d69e2e" />
            
            {/* Camera */}
            <PerspectiveCamera makeDefault position={[0, 0, 8]} fov={50} />
            
            {/* Controls */}
            <OrbitControls
              enablePan={false}
              minDistance={4}
              maxDistance={15}
              autoRotate={autoRotate}
              autoRotateSpeed={0.5}
            />
            
            {/* Atomic structure */}
            <AtomicStructureVisualizer
              element={selectedElement}
              showElectrons={showElectrons}
              showLabels={showLabels}
              scale={1.5}
            />
            
            {/* Environment */}
            <Environment preset="night" />
            <color attach="background" args={['#0a0e1a']} />
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
              </div>
              <div className="text-right">
                <div className="text-sm text-slate-500">Structure</div>
                <div className="font-mono text-lg text-amber-400">{config.structure}</div>
              </div>
            </div>

            {/* Stats grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-slate-900/50 rounded-lg p-4">
                <div className="text-2xl font-bold text-red-400">{config.Z}</div>
                <div className="text-xs text-slate-500">Protons (Z)</div>
              </div>
              <div className="bg-slate-900/50 rounded-lg p-4">
                <div className="text-2xl font-bold text-teal-400">{config.N}</div>
                <div className="text-xs text-slate-500">Neutrons (N)</div>
              </div>
              <div className="bg-slate-900/50 rounded-lg p-4">
                <div className="text-2xl font-bold text-orange-400">{config.alphas}</div>
                <div className="text-xs text-slate-500">Alpha Particles</div>
              </div>
              <div className="bg-slate-900/50 rounded-lg p-4">
                <div className="text-2xl font-bold text-slate-300 capitalize">{config.geometry}</div>
                <div className="text-xs text-slate-500">Geometry</div>
              </div>
            </div>

            {/* Description */}
            <p className="text-slate-300 mb-6">{config.description}</p>

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

      {/* Scale comparison callout */}
      <div className="max-w-4xl mx-auto px-4 pb-8">
        <div className="bg-gradient-to-r from-blue-900/30 to-violet-900/30 rounded-xl p-6 border border-blue-700/30">
          <h3 className="text-lg font-semibold text-blue-300 mb-2">
            🌍 Scale Perspective
          </h3>
          <p className="text-slate-300">
            If a proton were the size of the Sun (1.4 billion meters), 
            then <strong className="text-amber-400">10²¹ meters</strong> (100,000 light-years — 
            roughly the diameter of the Milky Way) would appear as{' '}
            <strong className="text-amber-400">~0.6 millimeters</strong> — 
            about the width of a grain of sand.
          </p>
        </div>
      </div>
    </div>
  );
}

