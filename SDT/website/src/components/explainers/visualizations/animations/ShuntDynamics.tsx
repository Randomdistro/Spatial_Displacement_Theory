/**
 * Shunt Dynamics Animation
 * Animated sequence showing RESISTANCE → RECOIL → TRANSFERENCE
 */

import React, { useState, useRef, useEffect } from 'react';
import { gsap } from 'gsap';

interface ShuntDynamicsProps {
  showSteps?: boolean;
  showPressure?: boolean;
  showFlow?: boolean;
  speed?: number;
  onComplete?: () => void;
}

export default function ShuntDynamics({
  showSteps = true,
  showPressure = true,
  showFlow = true,
  speed = 1.0,
  onComplete,
}: ShuntDynamicsProps) {
  const [currentStep, setCurrentStep] = useState<'resistance' | 'recoil' | 'transference' | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const resistanceRef = useRef<HTMLDivElement>(null);
  const recoilRef = useRef<HTMLDivElement>(null);
  const transferenceRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isPlaying) return;

    const timeline = gsap.timeline({
      onComplete: () => {
        setIsPlaying(false);
        setCurrentStep(null);
        onComplete?.();
      },
    });

    // RESISTANCE phase
    timeline
      .set({}, {}, 0)
      .to(resistanceRef.current, {
        opacity: 1,
        scale: 1.1,
        duration: 1 / speed,
        ease: 'power2.out',
      })
      .call(() => setCurrentStep('resistance'), [], 0.5 / speed);

    // RECOIL phase
    timeline
      .to(resistanceRef.current, {
        scale: 0.9,
        duration: 0.5 / speed,
        ease: 'power2.in',
      })
      .to(recoilRef.current, {
        opacity: 1,
        x: 20,
        duration: 1 / speed,
        ease: 'power2.out',
      })
      .call(() => setCurrentStep('recoil'), [], 1.5 / speed);

    // TRANSFERENCE phase
    timeline
      .to(recoilRef.current, {
        x: 40,
        opacity: 0.5,
        duration: 0.5 / speed,
      })
      .to(transferenceRef.current, {
        opacity: 1,
        x: 60,
        duration: 1 / speed,
        ease: 'power2.out',
      })
      .call(() => setCurrentStep('transference'), [], 2.5 / speed);

    // Reset
    timeline.to(
      [resistanceRef.current, recoilRef.current, transferenceRef.current],
      {
        opacity: 0.3,
        x: 0,
        scale: 1,
        duration: 0.5 / speed,
      }
    );

    return () => {
      timeline.kill();
    };
  }, [isPlaying, speed, onComplete]);

  const handlePlay = () => {
    setIsPlaying(true);
  };

  const handleReset = () => {
    setIsPlaying(false);
    setCurrentStep(null);
    gsap.set([resistanceRef.current, recoilRef.current, transferenceRef.current], {
      opacity: 0.3,
      x: 0,
      scale: 1,
    });
  };

  return (
    <div className="w-full bg-slate-800/50 rounded-lg p-6 border border-slate-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">Shunt Dynamics Sequence</h3>
        <div className="flex gap-2">
          <button
            onClick={handlePlay}
            disabled={isPlaying}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:opacity-50 text-white rounded transition-colors"
          >
            {isPlaying ? 'Playing...' : 'Play'}
          </button>
          <button
            onClick={handleReset}
            className="px-4 py-2 bg-slate-600 hover:bg-slate-700 text-white rounded transition-colors"
          >
            Reset
          </button>
        </div>
      </div>

      {/* Animation Canvas */}
      <div className="relative h-48 bg-slate-900 rounded overflow-hidden">
        {/* RESISTANCE */}
        <div
          ref={resistanceRef}
          className={`absolute left-10 top-1/2 -translate-y-1/2 w-16 h-16 rounded-full border-4 transition-all ${
            currentStep === 'resistance'
              ? 'bg-red-500 border-red-400 scale-110'
              : 'bg-red-500/30 border-red-500/50'
          }`}
        >
          <div className="absolute inset-0 flex items-center justify-center text-white font-bold text-xs">
            R
          </div>
        </div>

        {/* Arrow */}
        <div className="absolute left-26 top-1/2 -translate-y-1/2 w-8 h-0.5 bg-slate-600"></div>
        <div className="absolute left-32 top-1/2 -translate-y-1/2 w-0 h-0 border-l-4 border-l-slate-600 border-t-2 border-t-transparent border-b-2 border-b-transparent"></div>

        {/* RECOIL */}
        <div
          ref={recoilRef}
          className={`absolute left-40 top-1/2 -translate-y-1/2 w-16 h-16 rounded-full border-4 transition-all ${
            currentStep === 'recoil'
              ? 'bg-yellow-500 border-yellow-400'
              : 'bg-yellow-500/30 border-yellow-500/50'
          }`}
        >
          <div className="absolute inset-0 flex items-center justify-center text-white font-bold text-xs">
            R
          </div>
        </div>

        {/* Arrow */}
        <div className="absolute left-56 top-1/2 -translate-y-1/2 w-8 h-0.5 bg-slate-600"></div>
        <div className="absolute left-62 top-1/2 -translate-y-1/2 w-0 h-0 border-l-4 border-l-slate-600 border-t-2 border-t-transparent border-b-2 border-b-transparent"></div>

        {/* TRANSFERENCE */}
        <div
          ref={transferenceRef}
          className={`absolute left-70 top-1/2 -translate-y-1/2 w-16 h-16 rounded-full border-4 transition-all ${
            currentStep === 'transference'
              ? 'bg-green-500 border-green-400'
              : 'bg-green-500/30 border-green-500/50'
          }`}
        >
          <div className="absolute inset-0 flex items-center justify-center text-white font-bold text-xs">
            T
          </div>
        </div>
      </div>

      {/* Labels */}
      {showSteps && (
        <div className="flex justify-between mt-4 text-sm text-slate-400">
          <div className={`${currentStep === 'resistance' ? 'text-red-400 font-semibold' : ''}`}>
            RESISTANCE
          </div>
          <div className={`${currentStep === 'recoil' ? 'text-yellow-400 font-semibold' : ''}`}>
            RECOIL
          </div>
          <div className={`${currentStep === 'transference' ? 'text-green-400 font-semibold' : ''}`}>
            TRANSFERENCE
          </div>
        </div>
      )}
    </div>
  );
}

