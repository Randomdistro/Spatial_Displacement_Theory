/**
 * Codemonkey Agent: React Hook for Animation Choreography
 * 
 * Convenient hook for Creative Agent to orchestrate animations
 */

import { useEffect, useRef, useCallback, useState } from 'react';
import { AnimationChoreographer, AnimationSequence, EasingFunction, EasingFunctions } from '../animation/AnimationChoreographer';

export interface UseAnimationOptions {
  sequences: AnimationSequence[];
  autoPlay?: boolean;
  onComplete?: () => void;
}

export interface UseAnimationReturn {
  play: () => Promise<void>;
  pause: () => void;
  stop: () => void;
  seek: (time: number) => void;
  getProgress: (id: string) => number;
  isPlaying: boolean;
}

/**
 * Hook for animation choreography
 * 
 * @example
 * ```tsx
 * const { play, isPlaying } = useAnimation({
 *   sequences: [
 *     {
 *       id: 'fade-in',
 *       duration: 1000,
 *       easing: EasingFunctions.organic,
 *       onUpdate: (progress) => {
 *         // Update animation
 *       }
 *     }
 *   ]
 * });
 * ```
 */
export function useAnimation(options: UseAnimationOptions): UseAnimationReturn {
  const choreographerRef = useRef<AnimationChoreographer | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    const choreographer = new AnimationChoreographer();
    
    // Add all sequences
    for (const sequence of options.sequences) {
      choreographer.addSequence(sequence);
    }

    choreographerRef.current = choreographer;

    // Auto-play if requested
    if (options.autoPlay) {
      choreographer.play().then(() => {
        setIsPlaying(false);
        if (options.onComplete) {
          options.onComplete();
        }
      });
      setIsPlaying(true);
    }

    // Cleanup
    return () => {
      if (choreographerRef.current) {
        choreographerRef.current.stop();
      }
    };
  }, [options.sequences, options.autoPlay]);

  const play = useCallback(async () => {
    if (!choreographerRef.current) return;
    
    setIsPlaying(true);
    await choreographerRef.current.play();
    setIsPlaying(false);
    
    if (options.onComplete) {
      options.onComplete();
    }
  }, [options.onComplete]);

  const pause = useCallback(() => {
    if (!choreographerRef.current) return;
    choreographerRef.current.pause();
    setIsPlaying(false);
  }, []);

  const stop = useCallback(() => {
    if (!choreographerRef.current) return;
    choreographerRef.current.stop();
    setIsPlaying(false);
  }, []);

  const seek = useCallback((time: number) => {
    if (!choreographerRef.current) return;
    choreographerRef.current.seek(time);
  }, []);

  const getProgress = useCallback((id: string) => {
    if (!choreographerRef.current) return 0;
    return choreographerRef.current.getProgress(id);
  }, []);

  return {
    play,
    pause,
    stop,
    seek,
    getProgress,
    isPlaying,
  };
}

// Re-export easing functions for convenience
export { EasingFunctions };

