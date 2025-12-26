/**
 * Codemonkey Agent: Animation Choreography System
 * 
 * All original animation orchestration - supports Creative Agent's choreography
 */

export interface AnimationSequence {
  id: string;
  duration: number;
  delay?: number;
  easing?: EasingFunction;
  onStart?: () => void;
  onComplete?: () => void;
  onUpdate?: (progress: number) => void;
}

export type EasingFunction = (t: number) => number;

/**
 * Custom easing functions (all original)
 */
export const EasingFunctions = {
  /**
   * Linear easing
   */
  linear: (t: number): number => t,

  /**
   * Organic easing - cubic bezier (0.34, 1.56, 0.64, 1)
   * Slight overshoot, smooth settle
   */
  organic: (t: number): number => {
    // Cubic bezier approximation
    // P0 = (0, 0), P1 = (0.34, 1.56), P2 = (0.64, 1), P3 = (1, 1)
    const p1x = 0.34;
    const p1y = 1.56;
    const p2x = 0.64;
    const p2y = 1;

    // Binary search for t given x
    let low = 0;
    let high = 1;
    let mid = 0.5;

    for (let i = 0; i < 20; i++) {
      mid = (low + high) / 2;
      const x = bezierX(mid, p1x, p2x);
      if (Math.abs(x - t) < 0.001) break;
      if (x < t) low = mid;
      else high = mid;
    }

    return bezierY(mid, p1y, p2y);
  },

  /**
   * Pressure flow easing - exponential ease-out
   * Represents pressure gradient
   */
  pressureFlow: (t: number): number => {
    return 1 - Math.pow(2, -10 * t);
  },

  /**
   * Ease in-out cubic
   */
  easeInOutCubic: (t: number): number => {
    return t < 0.5
      ? 4 * t * t * t
      : 1 - Math.pow(-2 * t + 2, 3) / 2;
  },

  /**
   * Ease out cubic
   */
  easeOutCubic: (t: number): number => {
    return 1 - Math.pow(1 - t, 3);
  },
};

/**
 * Cubic bezier X coordinate
 */
function bezierX(t: number, p1x: number, p2x: number): number {
  return 3 * (1 - t) * (1 - t) * t * p1x + 3 * (1 - t) * t * t * p2x + t * t * t;
}

/**
 * Cubic bezier Y coordinate
 */
function bezierY(t: number, p1y: number, p2y: number): number {
  return 3 * (1 - t) * (1 - t) * t * p1y + 3 * (1 - t) * t * t * p2y + t * t * t;
}

/**
 * Animation Choreographer
 * Orchestrates multiple animation sequences
 */
export class AnimationChoreographer {
  private sequences: Map<string, AnimationSequence> = new Map();
  private activeAnimations: Map<string, AnimationState> = new Map();
  private startTime: number = 0;
  private rafId: number | null = null;
  private isPlaying: boolean = false;

  /**
   * Add animation sequence
   */
  addSequence(sequence: AnimationSequence): void {
    this.sequences.set(sequence.id, sequence);
  }

  /**
   * Remove animation sequence
   */
  removeSequence(id: string): void {
    this.sequences.delete(id);
    this.activeAnimations.delete(id);
  }

  /**
   * Play all sequences
   */
  play(): Promise<void> {
    return new Promise((resolve) => {
      if (this.isPlaying) {
        this.stop();
      }

      this.isPlaying = true;
      this.startTime = performance.now();

      // Initialize all sequences
      for (const [id, sequence] of this.sequences) {
        const delay = sequence.delay || 0;
        const state: AnimationState = {
          sequence,
          startTime: this.startTime + delay,
          progress: 0,
          completed: false,
        };
        this.activeAnimations.set(id, state);

        // Call onStart if provided
        if (sequence.onStart) {
          setTimeout(() => sequence.onStart!(), delay);
        }
      }

      // Start animation loop
      this.animate(resolve);
    });
  }

  /**
   * Animation loop
   */
  private animate(onComplete: () => void): void {
    const now = performance.now();
    let allComplete = true;

    for (const [id, state] of this.activeAnimations) {
      if (state.completed) continue;

      const elapsed = now - state.startTime;
      const duration = state.sequence.duration;

      if (elapsed < 0) {
        // Not started yet (delay)
        allComplete = false;
        continue;
      }

      if (elapsed >= duration) {
        // Completed
        state.progress = 1;
        state.completed = true;

        const easing = state.sequence.easing || EasingFunctions.linear;
        const easedProgress = easing(1);

        if (state.sequence.onUpdate) {
          state.sequence.onUpdate(easedProgress);
        }

        if (state.sequence.onComplete) {
          state.sequence.onComplete();
        }
      } else {
        // In progress
        allComplete = false;
        state.progress = elapsed / duration;

        const easing = state.sequence.easing || EasingFunctions.linear;
        const easedProgress = easing(state.progress);

        if (state.sequence.onUpdate) {
          state.sequence.onUpdate(easedProgress);
        }
      }
    }

    if (allComplete) {
      this.isPlaying = false;
      this.rafId = null;
      onComplete();
    } else {
      this.rafId = requestAnimationFrame(() => this.animate(onComplete));
    }
  }

  /**
   * Pause animation
   */
  pause(): void {
    if (this.rafId) {
      cancelAnimationFrame(this.rafId);
      this.rafId = null;
    }
  }

  /**
   * Stop animation
   */
  stop(): void {
    this.pause();
    this.isPlaying = false;
    this.activeAnimations.clear();
  }

  /**
   * Seek to time
   */
  seek(time: number): void {
    // Implementation for seeking
    // Would need to update all active animations
  }

  /**
   * Get progress for sequence
   */
  getProgress(id: string): number {
    const state = this.activeAnimations.get(id);
    return state ? state.progress : 0;
  }
}

interface AnimationState {
  sequence: AnimationSequence;
  startTime: number;
  progress: number;
  completed: boolean;
}

/**
 * Calculate stagger delay
 */
export function calculateStagger(
  index: number,
  stagger: number,
  baseDelay: number = 0
): number {
  return baseDelay + index * stagger;
}

