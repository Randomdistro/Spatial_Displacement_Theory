/**
 * Camera Choreography System
 * World-class camera movements for scale transitions
 * Smooth, cinematic, purposeful
 */

import * as THREE from 'three';
import { ScalePoint } from './ScaleManager';

export interface CameraKeyframe {
  position: [number, number, number];
  target: [number, number, number];
  fov?: number;
  duration: number;
  easing?: (t: number) => number;
}

export class CameraChoreography {
  private camera: THREE.PerspectiveCamera;
  private currentKeyframe: CameraKeyframe | null = null;
  private animationProgress: number = 0;
  private isAnimating: boolean = false;

  constructor(camera: THREE.PerspectiveCamera) {
    this.camera = camera;
  }

  /**
   * Get camera position for a specific scale
   */
  getCameraPositionForScale(scale: ScalePoint): CameraKeyframe {
    const log10 = scale.log10;
    
    // Camera distance scales logarithmically with scale
    const baseDistance = Math.max(5, Math.abs(log10) * 0.3 + 5);
    const height = baseDistance * 0.6;
    const distance = baseDistance;

    // Domain-specific camera angles
    let position: [number, number, number];
    let target: [number, number, number] = [0, 0, 0];

    switch (scale.domain) {
      case 'planck':
        // Close-up, looking down at lattice
        position = [0, baseDistance * 0.8, baseDistance * 0.5];
        target = [0, 0, 0];
        break;
      
      case 'atomic':
        // Slightly elevated, orbital view
        position = [0, baseDistance * 0.7, baseDistance * 0.8];
        target = [0, 0, 0];
        break;
      
      case 'molecular':
        // Side view of molecules
        position = [baseDistance * 0.6, baseDistance * 0.4, baseDistance * 0.8];
        target = [0, 0, 0];
        break;
      
      case 'macroscopic':
        // Elevated overview
        position = [0, baseDistance * 0.9, baseDistance];
        target = [0, 0, 0];
        break;
      
      case 'stellar':
        // Top-down orbital view
        position = [0, baseDistance * 1.2, 0];
        target = [0, 0, 0];
        break;
      
      case 'galactic':
        // Edge-on galaxy view
        position = [baseDistance * 0.8, baseDistance * 0.3, baseDistance * 0.5];
        target = [0, 0, 0];
        break;
      
      case 'cosmological':
        // Pulled back, showing boundary
        position = [0, baseDistance * 0.5, baseDistance * 1.5];
        target = [0, 0, 0];
        break;
      
      default:
        position = [0, height, distance];
    }

    return {
      position,
      target,
      duration: 3000,
      easing: this.easeInOutCubic,
    };
  }

  /**
   * Animate camera to scale position
   */
  animateToScale(scale: ScalePoint, onComplete?: () => void): void {
    const keyframe = this.getCameraPositionForScale(scale);
    this.animateToKeyframe(keyframe, onComplete);
  }

  /**
   * Animate camera through keyframes
   */
  animateToKeyframe(keyframe: CameraKeyframe, onComplete?: () => void): void {
    if (this.isAnimating) return;

    const startPosition = new THREE.Vector3().copy(this.camera.position);
    const startTarget = new THREE.Vector3(
      this.camera.position.x,
      this.camera.position.y - 1,
      this.camera.position.z - 1
    );
    
    const endPosition = new THREE.Vector3(...keyframe.position);
    const endTarget = new THREE.Vector3(...keyframe.target);

    this.currentKeyframe = keyframe;
    this.isAnimating = true;
    this.animationProgress = 0;

    const startTime = performance.now();
    const easing = keyframe.easing || this.easeInOutCubic;

    const animate = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      this.animationProgress = Math.min(elapsed / keyframe.duration, 1);
      
      const t = easing(this.animationProgress);
      
      // Interpolate position
      this.camera.position.lerpVectors(startPosition, endPosition, t);
      
      // Update FOV if specified
      if (keyframe.fov) {
        this.camera.fov = THREE.MathUtils.lerp(this.camera.fov, keyframe.fov, t);
        this.camera.updateProjectionMatrix();
      }
      
      // Look at target (smooth interpolation)
      const currentTarget = new THREE.Vector3().lerpVectors(startTarget, endTarget, t);
      this.camera.lookAt(currentTarget);

      if (this.animationProgress < 1) {
        requestAnimationFrame(animate);
      } else {
        this.isAnimating = false;
        this.animationProgress = 0;
        if (onComplete) {
          onComplete();
        }
      }
    };

    requestAnimationFrame(animate);
  }

  /**
   * Special camera movements for key moments
   */
  revealCMBBoundary(onComplete?: () => void): void {
    // Pull back dramatically to reveal CMB boundary
    const keyframes: CameraKeyframe[] = [
      {
        position: [0, 50, 100],
        target: [0, 0, 0],
        duration: 2000,
        easing: this.easeOutCubic,
      },
      {
        position: [0, 200, 300],
        target: [0, 0, 0],
        duration: 3000,
        easing: this.easeInOutCubic,
      },
    ];

    this.animateKeyframeSequence(keyframes, onComplete);
  }

  /**
   * Count through scales - camera moves through counting sequence
   */
  countThroughScales(scales: ScalePoint[], onComplete?: () => void): void {
    const keyframes = scales.map(scale => this.getCameraPositionForScale(scale));
    keyframes.forEach((kf, i) => {
      kf.duration = i === 0 ? 2000 : 1500; // First transition slower
    });
    
    this.animateKeyframeSequence(keyframes, onComplete);
  }

  private animateKeyframeSequence(keyframes: CameraKeyframe[], onComplete?: () => void): void {
    let currentIndex = 0;

    const animateNext = () => {
      if (currentIndex >= keyframes.length) {
        if (onComplete) onComplete();
        return;
      }

      this.animateToKeyframe(keyframes[currentIndex], () => {
        currentIndex++;
        setTimeout(animateNext, 200); // Small pause between keyframes
      });
    };

    animateNext();
  }

  /**
   * Easing functions
   */
  private easeInOutCubic(t: number): number {
    return t < 0.5
      ? 4 * t * t * t
      : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  private easeOutCubic(t: number): number {
    return 1 - Math.pow(1 - t, 3);
  }

  private easeInCubic(t: number): number {
    return t * t * t;
  }

  isCurrentlyAnimating(): boolean {
    return this.isAnimating;
  }

  getProgress(): number {
    return this.animationProgress;
  }
}

