/**
 * Codemonkey Agent: Spatial Navigation System
 * 
 * TEKNE: State management IS spatial position
 * All original implementation - enables Creative Agent's spatial navigation
 */

import { Vector3, Euler } from 'three';

export interface SpatialPosition {
  position: Vector3;
  rotation: Euler;
  scale: Vector3;
}

export interface CameraState {
  position: Vector3;
  target: Vector3;
  up: Vector3;
  fov: number;
}

export interface NavigationTransition {
  from: SpatialPosition;
  to: SpatialPosition;
  duration: number;
  easing: (t: number) => number;
  onComplete?: () => void;
}

/**
 * Spatial Navigation Manager
 * Manages 3D spatial navigation state and transitions
 */
export class SpatialNavigationManager {
  private currentPosition: SpatialPosition;
  private targetPosition: SpatialPosition | null = null;
  private isTransitioning: boolean = false;
  private transitionStartTime: number = 0;
  private transitionDuration: number = 0;
  private transitionEasing: (t: number) => number = (t) => t;
  private transitionOnComplete?: () => void;

  constructor(initialPosition: SpatialPosition) {
    this.currentPosition = initialPosition;
  }

  /**
   * Get current spatial position
   */
  getCurrentPosition(): SpatialPosition {
    return { ...this.currentPosition };
  }

  /**
   * Set target position (triggers transition)
   */
  navigateTo(
    target: SpatialPosition,
    duration: number = 1000,
    easing?: (t: number) => number,
    onComplete?: () => void
  ): void {
    this.targetPosition = target;
    this.isTransitioning = true;
    this.transitionStartTime = performance.now();
    this.transitionDuration = duration;
    this.transitionEasing = easing || ((t) => t);
    this.transitionOnComplete = onComplete;
  }

  /**
   * Update navigation (call in animation loop)
   */
  update(): SpatialPosition {
    if (!this.isTransitioning || !this.targetPosition) {
      return this.getCurrentPosition();
    }

    const elapsed = performance.now() - this.transitionStartTime;
    const progress = Math.min(elapsed / this.transitionDuration, 1);
    const easedProgress = this.transitionEasing(progress);

    // Interpolate position
    this.currentPosition.position.lerpVectors(
      this.currentPosition.position,
      this.targetPosition.position,
      easedProgress
    );

    // Interpolate rotation (simplified - could use quaternions)
    // Interpolate scale
    this.currentPosition.scale.lerpVectors(
      this.currentPosition.scale,
      this.targetPosition.scale,
      easedProgress
    );

    if (progress >= 1) {
      this.isTransitioning = false;
      this.currentPosition = { ...this.targetPosition };
      this.targetPosition = null;
      
      if (this.transitionOnComplete) {
        this.transitionOnComplete();
        this.transitionOnComplete = undefined;
      }
    }

    return this.getCurrentPosition();
  }

  /**
   * Check if currently transitioning
   */
  isInTransition(): boolean {
    return this.isTransitioning;
  }

  /**
   * Cancel current transition
   */
  cancelTransition(): void {
    this.isTransitioning = false;
    this.targetPosition = null;
    this.transitionOnComplete = undefined;
  }

  /**
   * Set position immediately (no transition)
   */
  setPosition(position: SpatialPosition): void {
    this.cancelTransition();
    this.currentPosition = { ...position };
  }
}

/**
 * Camera path generator using Catmull-Rom splines
 * All original implementation
 */
export class CameraPathGenerator {
  /**
   * Generate smooth camera path between points
   */
  static generatePath(
    points: Vector3[],
    segments: number = 100
  ): Vector3[] {
    if (points.length < 2) return points;
    if (points.length === 2) {
      return this.interpolateLinear(points[0], points[1], segments);
    }

    const path: Vector3[] = [];
    
    for (let i = 0; i < points.length - 1; i++) {
      const p0 = i > 0 ? points[i - 1] : points[i];
      const p1 = points[i];
      const p2 = points[i + 1];
      const p3 = i < points.length - 2 ? points[i + 2] : points[i + 1];

      for (let j = 0; j < segments; j++) {
        const t = j / segments;
        const point = this.catmullRom(p0, p1, p2, p3, t);
        path.push(point);
      }
    }

    return path;
  }

  /**
   * Catmull-Rom spline interpolation
   */
  private static catmullRom(
    p0: Vector3,
    p1: Vector3,
    p2: Vector3,
    p3: Vector3,
    t: number
  ): Vector3 {
    const t2 = t * t;
    const t3 = t2 * t;

    const x = 0.5 * (
      (2 * p1.x) +
      (-p0.x + p2.x) * t +
      (2 * p0.x - 5 * p1.x + 4 * p2.x - p3.x) * t2 +
      (-p0.x + 3 * p1.x - 3 * p2.x + p3.x) * t3
    );

    const y = 0.5 * (
      (2 * p1.y) +
      (-p0.y + p2.y) * t +
      (2 * p0.y - 5 * p1.y + 4 * p2.y - p3.y) * t2 +
      (-p0.y + 3 * p1.y - 3 * p2.y + p3.y) * t3
    );

    const z = 0.5 * (
      (2 * p1.z) +
      (-p0.z + p2.z) * t +
      (2 * p0.z - 5 * p1.z + 4 * p2.z - p3.z) * t2 +
      (-p0.z + 3 * p1.z - 3 * p2.z + p3.z) * t3
    );

    return new Vector3(x, y, z);
  }

  /**
   * Linear interpolation between two points
   */
  private static interpolateLinear(
    p0: Vector3,
    p1: Vector3,
    segments: number
  ): Vector3[] {
    const path: Vector3[] = [];
    for (let i = 0; i <= segments; i++) {
      const t = i / segments;
      const point = new Vector3().lerpVectors(p0, p1, t);
      path.push(point);
    }
    return path;
  }
}

