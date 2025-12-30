/**
 * Nuclear Packing 3D Visualization
 * Placeholder - to be implemented
 */

import React from 'react';

interface NuclearPackingProps {
  element?: string;
  showStructure?: boolean;
}

export default function NuclearPacking({ element, showStructure }: NuclearPackingProps) {
  return (
    <div className="w-full h-64 bg-slate-800/50 rounded-lg border border-slate-700 flex items-center justify-center text-slate-400">
      Nuclear Packing Visualization
      {element && ` - ${element}`}
      <br />
      <span className="text-xs">(To be implemented)</span>
    </div>
  );
}

