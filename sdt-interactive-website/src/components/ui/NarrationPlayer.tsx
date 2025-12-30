/**
 * NarrationPlayer - Veritasium-style narration UI component
 * 
 * Features:
 * - Play/pause controls
 * - Speed adjustment (0.5x - 2x)
 * - Progress bar with segment markers
 * - Highlighted transcript
 * - Volume control
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  NarrationController,
  NarrationData,
  NarrationState,
  createHighlightedScript,
} from '../../utils/narration';

interface NarrationPlayerProps {
  narration: NarrationData;
  autoPlay?: boolean;
  showTranscript?: boolean;
  compact?: boolean;
  onComplete?: () => void;
}

export default function NarrationPlayer({
  narration,
  autoPlay = false,
  showTranscript = true,
  compact = false,
  onComplete,
}: NarrationPlayerProps) {
  const [controller, setController] = useState<NarrationController | null>(null);
  const [state, setState] = useState<NarrationState>({
    isPlaying: false,
    isPaused: false,
    currentTime: 0,
    duration: narration.duration || 60,
    speed: 1,
    volume: 1,
    currentSegment: 0,
  });
  const [highlightedText, setHighlightedText] = useState({
    before: '',
    current: narration.script,
    after: '',
  });

  // Initialize controller
  useEffect(() => {
    const ctrl = new NarrationController({
      onStart: () => setState((s) => ({ ...s, isPlaying: true, isPaused: false })),
      onEnd: () => {
        setState((s) => ({ ...s, isPlaying: false }));
        onComplete?.();
      },
      onPause: () => setState((s) => ({ ...s, isPaused: true })),
      onResume: () => setState((s) => ({ ...s, isPaused: false })),
      onProgress: (currentTime, segment) => {
        setState((s) => ({ ...s, currentTime, currentSegment: segment }));
        setHighlightedText(
          createHighlightedScript(narration.script, narration.timing, currentTime)
        );
      },
      onSegmentChange: (segment) => {
        setState((s) => ({ ...s, currentSegment: segment }));
      },
    });

    setController(ctrl);

    if (autoPlay) {
      ctrl.speak(narration);
    }

    return () => {
      ctrl.stop();
    };
  }, [narration, autoPlay, onComplete]);

  // Play/pause toggle
  const togglePlayPause = useCallback(() => {
    if (!controller) return;

    if (state.isPlaying && !state.isPaused) {
      controller.pause();
    } else if (state.isPaused) {
      controller.resume();
    } else {
      controller.speak(narration);
    }
  }, [controller, state, narration]);

  // Speed control
  const handleSpeedChange = useCallback(
    (speed: number) => {
      if (!controller) return;
      controller.setSpeed(speed);
      setState((s) => ({ ...s, speed }));
    },
    [controller]
  );

  // Volume control
  const handleVolumeChange = useCallback(
    (volume: number) => {
      if (!controller) return;
      controller.setVolume(volume);
      setState((s) => ({ ...s, volume }));
    },
    [controller]
  );

  // Progress bar click
  const handleProgressClick = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (!controller) return;

      const rect = e.currentTarget.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const percentage = clickX / rect.width;
      const targetTime = percentage * state.duration;

      // Find closest segment
      let targetSegment = 0;
      for (let i = narration.timing.length - 1; i >= 0; i--) {
        if (targetTime >= narration.timing[i]) {
          targetSegment = i;
          break;
        }
      }

      controller.skipToSegment(targetSegment);
    },
    [controller, state.duration, narration.timing]
  );

  // Format time
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Speed options
  const speedOptions = [0.5, 0.75, 1, 1.25, 1.5, 2];

  if (compact) {
    return (
      <div className="flex items-center gap-3 bg-slate-900/80 backdrop-blur-sm p-3 rounded-lg">
        {/* Play/Pause */}
        <button
          onClick={togglePlayPause}
          className="w-10 h-10 flex items-center justify-center rounded-full bg-amber-500 hover:bg-amber-400 text-slate-900 transition-colors"
        >
          {state.isPlaying && !state.isPaused ? (
            <span className="text-lg">⏸</span>
          ) : (
            <span className="text-lg">▶</span>
          )}
        </button>

        {/* Progress */}
        <div className="flex-1">
          <div
            className="h-2 bg-slate-700 rounded-full cursor-pointer"
            onClick={handleProgressClick}
          >
            <div
              className="h-full bg-amber-500 rounded-full transition-all duration-100"
              style={{ width: `${(state.currentTime / state.duration) * 100}%` }}
            />
          </div>
          <div className="flex justify-between text-xs text-slate-400 mt-1">
            <span>{formatTime(state.currentTime)}</span>
            <span>{formatTime(state.duration)}</span>
          </div>
        </div>

        {/* Speed */}
        <select
          value={state.speed}
          onChange={(e) => handleSpeedChange(parseFloat(e.target.value))}
          className="bg-slate-800 text-white text-sm rounded px-2 py-1"
        >
          {speedOptions.map((speed) => (
            <option key={speed} value={speed}>
              {speed}x
            </option>
          ))}
        </select>
      </div>
    );
  }

  return (
    <div className="bg-slate-900/90 backdrop-blur-sm rounded-xl border border-slate-700 overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 bg-slate-800/50 border-b border-slate-700 flex items-center justify-between">
        <h3 className="text-white font-medium flex items-center gap-2">
          <span className="text-amber-400">🎧</span>
          Narration
        </h3>
        <div className="flex items-center gap-2">
          {/* Volume */}
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={state.volume}
            onChange={(e) => handleVolumeChange(parseFloat(e.target.value))}
            className="w-20 h-1 bg-slate-600 rounded-lg appearance-none cursor-pointer"
          />
          <span className="text-slate-400 text-sm">🔊</span>
        </div>
      </div>

      {/* Transcript with highlighting */}
      {showTranscript && (
        <div className="px-4 py-4 max-h-48 overflow-y-auto">
          <p className="text-slate-300 leading-relaxed">
            <span className="text-slate-500">{highlightedText.before}</span>
            {highlightedText.before && ' '}
            <span className="text-white bg-amber-500/30 px-1 rounded">
              {highlightedText.current}
            </span>
            {highlightedText.after && ' '}
            <span className="text-slate-500">{highlightedText.after}</span>
          </p>
        </div>
      )}

      {/* Controls */}
      <div className="px-4 py-3 bg-slate-800/30 border-t border-slate-700">
        <div className="flex items-center gap-4">
          {/* Play/Pause */}
          <button
            onClick={togglePlayPause}
            className="w-12 h-12 flex items-center justify-center rounded-full bg-amber-500 hover:bg-amber-400 text-slate-900 transition-colors"
          >
            {state.isPlaying && !state.isPaused ? (
              <span className="text-xl">⏸</span>
            ) : (
              <span className="text-xl">▶</span>
            )}
          </button>

          {/* Progress bar with segment markers */}
          <div className="flex-1">
            <div
              className="relative h-3 bg-slate-700 rounded-full cursor-pointer"
              onClick={handleProgressClick}
            >
              {/* Segment markers */}
              {narration.timing.map((time, i) => (
                <div
                  key={i}
                  className="absolute top-0 w-0.5 h-full bg-slate-500"
                  style={{ left: `${(time / state.duration) * 100}%` }}
                />
              ))}

              {/* Progress fill */}
              <div
                className="absolute top-0 h-full bg-amber-500 rounded-full transition-all duration-100"
                style={{ width: `${(state.currentTime / state.duration) * 100}%` }}
              />

              {/* Current position indicator */}
              <div
                className="absolute top-1/2 w-4 h-4 bg-white rounded-full shadow-lg transform -translate-y-1/2 -translate-x-1/2 transition-all duration-100"
                style={{ left: `${(state.currentTime / state.duration) * 100}%` }}
              />
            </div>

            <div className="flex justify-between text-xs text-slate-400 mt-2">
              <span>{formatTime(state.currentTime)}</span>
              <span>
                Segment {state.currentSegment + 1}/{narration.timing.length}
              </span>
              <span>{formatTime(state.duration)}</span>
            </div>
          </div>

          {/* Speed selector */}
          <div className="flex flex-col items-center">
            <select
              value={state.speed}
              onChange={(e) => handleSpeedChange(parseFloat(e.target.value))}
              className="bg-slate-800 text-white text-sm rounded-lg px-3 py-2 border border-slate-600"
            >
              {speedOptions.map((speed) => (
                <option key={speed} value={speed}>
                  {speed}x
                </option>
              ))}
            </select>
            <span className="text-xs text-slate-500 mt-1">Speed</span>
          </div>
        </div>
      </div>
    </div>
  );
}

