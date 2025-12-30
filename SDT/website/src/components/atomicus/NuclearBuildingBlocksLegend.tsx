/**
 * Creative Agent: Nuclear Building Blocks Legend
 * 
 * TEKNE: The key IS the understanding
 * 
 * Visual legend showing the four fundamental building blocks:
 * - D (Deuteron): (np) - "Atomic mortar"
 * - A (Alpha): (np)(np) - "Diamond of nuclear physics"
 * - tri-A: (np)n(np) - "Wobble carrier"
 * - Triple: (np)n(np)n(np) - "Post-boundary chain"
 */

import React from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import { Vector3 } from 'three';

interface BuildingBlockCardProps {
  symbol: string;
  name: string;
  structure: string;
  composition: string;
  role: string;
  color: string;
  bindingEnergy?: string;
}

function BuildingBlockCard({
  symbol,
  name,
  structure,
  composition,
  role,
  color,
  bindingEnergy,
}: BuildingBlockCardProps) {
  return (
    <div className={`bg-slate-800/80 backdrop-blur-sm rounded-xl p-6 border border-slate-700 hover:border-${color} transition-all hover:scale-105`}>
      {/* Symbol badge */}
      <div className={`inline-flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-br from-${color} to-${color}/50 text-white font-bold text-xl mb-4`}>
        {symbol}
      </div>
      
      {/* Name */}
      <h3 className="text-xl font-bold text-white mb-2">{name}</h3>
      
      {/* Structure notation */}
      <div className="font-mono text-lg text-amber-400 mb-3">{structure}</div>
      
      {/* Details */}
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-slate-400">Composition:</span>
          <span className="text-slate-200">{composition}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-400">Role:</span>
          <span className="text-slate-200 text-right max-w-[60%]">{role}</span>
        </div>
        {bindingEnergy && (
          <div className="flex justify-between">
            <span className="text-slate-400">Binding:</span>
            <span className="text-emerald-400 font-mono">{bindingEnergy}</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default function NuclearBuildingBlocksLegend() {
  const buildingBlocks = [
    {
      symbol: 'D',
      name: 'Deuteron',
      structure: '(np)',
      composition: '1p + 1n',
      role: 'Atomic mortar - the fundamental building block',
      color: 'amber-500',
      bindingEnergy: '~2.22 MeV',
    },
    {
      symbol: 'α',
      name: 'Alpha Particle',
      structure: '(np)(np)',
      composition: '2p + 2n',
      role: 'Diamond of nuclear physics - perfect geometric closure',
      color: 'orange-500',
      bindingEnergy: '~28.3 MeV',
    },
    {
      symbol: 'τ',
      name: 'Tri-Alpha',
      structure: '(np)n(np)',
      composition: '2p + 3n',
      role: 'Wobble carrier - magnetic properties',
      color: 'violet-500',
      bindingEnergy: '~7.7 MeV',
    },
    {
      symbol: '3×',
      name: 'Triple',
      structure: '(np)n(np)n(np)',
      composition: '3p + 5n',
      role: 'Post-boundary chain - heavy nuclei',
      color: 'blue-500',
      bindingEnergy: 'Complex',
    },
  ];

  return (
    <div className="w-full bg-slate-900 rounded-2xl p-8 border border-slate-700">
      {/* Header */}
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-4">
          Nuclear Building Blocks
        </h2>
        <p className="text-slate-400 max-w-2xl mx-auto">
          In SDT, all nuclei are geometric assemblies of these four fundamental structures.
          Every element from Hydrogen to Uranium is built from combinations of deuterons
          and alpha particles.
        </p>
      </div>

      {/* Building blocks grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {buildingBlocks.map((block) => (
          <BuildingBlockCard key={block.symbol} {...block} />
        ))}
      </div>

      {/* Visual notation key */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-white mb-4">Notation Key</h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {/* Proton */}
          <div className="flex items-center gap-3">
            <div className="w-6 h-6 rounded-full bg-gradient-to-br from-red-400 to-red-600" />
            <span className="text-slate-300">
              <span className="font-mono text-red-400">p</span> = Proton
            </span>
          </div>
          
          {/* Neutron */}
          <div className="flex items-center gap-3">
            <div className="w-6 h-6 rounded-full bg-gradient-to-br from-teal-400 to-teal-600" />
            <span className="text-slate-300">
              <span className="font-mono text-teal-400">n</span> = Neutron
            </span>
          </div>
          
          {/* Bond */}
          <div className="flex items-center gap-3">
            <div className="w-8 h-1 bg-gradient-to-r from-amber-400 to-amber-600 rounded" />
            <span className="text-slate-300">
              <span className="font-mono text-amber-400">-</span> = Neutrino flux
            </span>
          </div>
          
          {/* Pairing */}
          <div className="flex items-center gap-3">
            <div className="flex items-center">
              <span className="text-amber-400 font-mono">(</span>
              <span className="text-slate-400">...</span>
              <span className="text-amber-400 font-mono">)</span>
            </div>
            <span className="text-slate-300">
              = Paired structure
            </span>
          </div>
        </div>
      </div>

      {/* Geometry patterns */}
      <div className="mt-6 bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-white mb-4">Geometric Arrangements</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div>
            <h4 className="text-amber-400 font-semibold mb-2">Linear</h4>
            <p className="text-slate-400">
              Deuterons, Tritium, He-3: Nucleons in a line (dumbbell or chain)
            </p>
          </div>
          
          <div>
            <h4 className="text-amber-400 font-semibold mb-2">Triangular</h4>
            <p className="text-slate-400">
              Carbon-12: Three alphas forming a triangle — foundation of organic chemistry
            </p>
          </div>
          
          <div>
            <h4 className="text-amber-400 font-semibold mb-2">Tetrahedral</h4>
            <p className="text-slate-400">
              He-4, O-16: Perfect 3D symmetry — maximum stability per nucleon
            </p>
          </div>
        </div>
      </div>

      {/* The key insight */}
      <div className="mt-6 p-6 bg-gradient-to-r from-amber-900/30 to-orange-900/30 rounded-xl border border-amber-700/30">
        <blockquote className="text-lg text-amber-200 italic text-center">
          "The nucleus drives everything. All chemistry emerges from these geometric building blocks."
        </blockquote>
        <p className="text-center text-amber-400 text-sm mt-2">
          — Atomica Sentis
        </p>
      </div>
    </div>
  );
}

