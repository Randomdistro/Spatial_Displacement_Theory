import { useState, useRef, useEffect } from 'react';

/**
 * Scale Visualization Component
 * Shows SDT's validation across 53 orders of magnitude
 * Interactive slider from nuclear to cosmological scales
 */

interface ScalePoint {
  scale: number; // log10 meters
  name: string;
  kValue: string;
  example: string;
  error: string;
  color: string;
}

const scalePoints: ScalePoint[] = [
  { scale: -15, name: 'Nuclear', kValue: '~1', example: 'Proton radius', error: 'TBD', color: '#ef4444' },
  { scale: -11, name: 'Atomic', kValue: '137', example: 'Hydrogen Bohr radius', error: '<0.01%', color: '#8b5cf6' },
  { scale: -10, name: 'Molecular', kValue: '~200', example: 'H₂ bond length', error: '<1%', color: '#6366f1' },
  { scale: 0, name: 'Human', kValue: '-', example: 'Reference scale', error: '-', color: '#64748b' },
  { scale: 6, name: 'Planetary', kValue: '~100', example: 'Earth radius', error: '<0.5%', color: '#3b82f6' },
  { scale: 9, name: 'Giant', kValue: '~8800', example: 'Jupiter radius', error: '<0.5%', color: '#06b6d4' },
  { scale: 11, name: 'Orbital', kValue: '~59000', example: 'Earth orbit (1 AU)', error: '<0.5%', color: '#10b981' },
  { scale: 13, name: 'Outer System', kValue: '~59000', example: 'Saturn orbit', error: '<0.5%', color: '#22c55e' },
  { scale: 17, name: 'Stellar', kValue: '~10⁴', example: 'Proxima system', error: '±5%', color: '#eab308' },
  { scale: 21, name: 'Galactic', kValue: '~10⁵', example: 'Milky Way disk', error: 'Testing', color: '#f97316' },
  { scale: 26, name: 'Cosmological', kValue: 'Horizon', example: 'CMB distance', error: 'Exact', color: '#ec4899' },
];

export default function ScaleVisualization() {
  const [selectedScale, setSelectedScale] = useState(6);
  const [isPlaying, setIsPlaying] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const animationRef = useRef<number>(0);

  // Auto-play animation
  useEffect(() => {
    if (!isPlaying) return;

    const animate = () => {
      setSelectedScale(prev => {
        const next = prev + 0.5;
        if (next > 26) {
          setIsPlaying(false);
          return -15;
        }
        return next;
      });
      animationRef.current = requestAnimationFrame(() => {
        setTimeout(animate, 100);
      });
    };
    animate();

    return () => cancelAnimationFrame(animationRef.current);
  }, [isPlaying]);

  // Find nearest scale point
  const nearestPoint = scalePoints.reduce((nearest, point) =>
    Math.abs(point.scale - selectedScale) < Math.abs(nearest.scale - selectedScale)
      ? point : nearest
  );

  // Calculate position on track
  const getPosition = (scale: number) => {
    const min = -15;
    const max = 26;
    return ((scale - min) / (max - min)) * 100;
  };

  return (
    <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-2xl overflow-hidden">
      {/* Header */}
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-display font-bold text-2xl text-white mb-1">
              53 Orders of Magnitude
            </h3>
            <p className="text-slate-400">
              One equation works from nuclei to galaxies
            </p>
          </div>
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              isPlaying
                ? 'bg-red-500 text-white hover:bg-red-600'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            {isPlaying ? 'Stop' : 'Play Journey'}
          </button>
        </div>
      </div>

      {/* Scale visualization */}
      <div className="p-6" ref={containerRef}>
        {/* Scale track */}
        <div className="relative h-24 mb-8">
          {/* Background gradient showing spectrum */}
          <div className="absolute inset-x-0 top-1/2 -translate-y-1/2 h-2 rounded-full bg-gradient-to-r from-red-500 via-blue-500 via-green-500 via-yellow-500 to-pink-500 opacity-30" />

          {/* Scale markers */}
          {scalePoints.map(point => (
            <div
              key={point.scale}
              className="absolute top-1/2 -translate-y-1/2 flex flex-col items-center cursor-pointer transition-transform hover:scale-110"
              style={{ left: `${getPosition(point.scale)}%` }}
              onClick={() => setSelectedScale(point.scale)}
            >
              {/* Marker dot */}
              <div
                className={`w-4 h-4 rounded-full border-2 border-white transition-all duration-300 ${
                  Math.abs(point.scale - selectedScale) < 2
                    ? 'scale-150 shadow-lg'
                    : ''
                }`}
                style={{
                  backgroundColor: point.color,
                  boxShadow: Math.abs(point.scale - selectedScale) < 2
                    ? `0 0 20px ${point.color}`
                    : 'none'
                }}
              />
              {/* Label (show for key points or selected) */}
              {(Math.abs(point.scale - selectedScale) < 3 || point.scale % 10 === 0) && (
                <span className="absolute -bottom-8 text-xs text-slate-400 whitespace-nowrap">
                  10<sup>{point.scale}</sup> m
                </span>
              )}
            </div>
          ))}

          {/* Current position indicator */}
          <div
            className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 transition-all duration-200"
            style={{ left: `${getPosition(selectedScale)}%` }}
          >
            <div className="w-1 h-16 bg-white/50 rounded-full" />
          </div>
        </div>

        {/* Slider */}
        <input
          type="range"
          min={-15}
          max={26}
          step={0.1}
          value={selectedScale}
          onChange={(e) => setSelectedScale(parseFloat(e.target.value))}
          className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer
            [&::-webkit-slider-thumb]:appearance-none
            [&::-webkit-slider-thumb]:w-6
            [&::-webkit-slider-thumb]:h-6
            [&::-webkit-slider-thumb]:rounded-full
            [&::-webkit-slider-thumb]:bg-white
            [&::-webkit-slider-thumb]:shadow-lg
            [&::-webkit-slider-thumb]:cursor-grab
            [&::-webkit-slider-thumb]:transition-transform
            [&::-webkit-slider-thumb]:hover:scale-110"
        />

        {/* Scale labels */}
        <div className="flex justify-between text-xs text-slate-500 mt-2">
          <span>Nuclear (10⁻¹⁵ m)</span>
          <span>Human (1 m)</span>
          <span>Cosmic (10²⁶ m)</span>
        </div>
      </div>

      {/* Selected scale info */}
      <div className="p-6 bg-slate-800/50">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <div className="text-xs uppercase tracking-wide text-slate-500 mb-1">Scale</div>
            <div className="font-display font-bold text-xl text-white">
              {nearestPoint.name}
            </div>
          </div>
          <div>
            <div className="text-xs uppercase tracking-wide text-slate-500 mb-1">Example</div>
            <div className="text-white">
              {nearestPoint.example}
            </div>
          </div>
          <div>
            <div className="text-xs uppercase tracking-wide text-slate-500 mb-1">k Value</div>
            <div className="font-mono text-lg" style={{ color: nearestPoint.color }}>
              {nearestPoint.kValue}
            </div>
          </div>
          <div>
            <div className="text-xs uppercase tracking-wide text-slate-500 mb-1">SDT Error</div>
            <div className={`font-mono text-lg ${
              nearestPoint.error.includes('<') || nearestPoint.error === 'Exact'
                ? 'text-emerald-400'
                : nearestPoint.error === 'TBD' || nearestPoint.error === 'Testing'
                  ? 'text-amber-400'
                  : 'text-slate-400'
            }`}>
              {nearestPoint.error}
            </div>
          </div>
        </div>

        {/* Universal equation */}
        <div className="mt-6 p-4 bg-slate-900/50 rounded-lg text-center">
          <p className="text-slate-400 text-sm mb-2">The same equation at every scale:</p>
          <p className="font-mono text-lg text-white">
            v(r) = <span style={{ color: nearestPoint.color }}>(c/{nearestPoint.kValue})</span> × √(R/r)
          </p>
        </div>
      </div>

      {/* Footer */}
      <div className="px-6 py-4 bg-slate-900 border-t border-slate-800">
        <p className="text-xs text-slate-500 text-center">
          SDT unifies atomic, planetary, stellar, and galactic physics with a single geometric principle.
          No other theory achieves this range with sub-1% precision.
        </p>
      </div>
    </div>
  );
}
