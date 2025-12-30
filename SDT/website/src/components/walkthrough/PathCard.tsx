/**
 * Architect Designer Agent: Path Selection Card
 * Beautiful, intuitive path selection cards
 */

import React from 'react';

interface PathCardProps {
  pathId: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  onClick: () => void;
}

export default function PathCard({
  title,
  description,
  icon,
  color,
  onClick,
}: PathCardProps) {
  return (
    <button
      onClick={onClick}
      className="group relative bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20 hover:border-sdt-gold-500/50 transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-sdt-gold-500/20 text-left"
    >
      {/* Gradient background on hover */}
      <div className={`absolute inset-0 bg-gradient-to-br ${color} opacity-0 group-hover:opacity-10 rounded-xl transition-opacity duration-300`} />
      
      <div className="relative z-10">
        <div className="text-4xl mb-3">{icon}</div>
        <h3 className="text-xl font-bold text-white mb-2 group-hover:text-sdt-gold-400 transition-colors">
          {title}
        </h3>
        <p className="text-sm text-slate-400 group-hover:text-slate-300 transition-colors">
          {description}
        </p>
      </div>

      {/* Arrow indicator */}
      <div className="absolute bottom-4 right-4 text-slate-500 group-hover:text-sdt-gold-500 transition-colors">
        <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </div>
    </button>
  );
}

