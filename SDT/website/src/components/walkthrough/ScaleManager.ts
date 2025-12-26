/**
 * Scale Manager
 * Manages transitions across 43 orders of magnitude
 * Handles logarithmic scaling and smooth transitions
 */

export type ScaleDomain = 
  | 'planck'      // 10^-35 to 10^-15 m
  | 'atomic'      // 10^-15 to 10^-10 m
  | 'molecular'   // 10^-10 to 10^-6 m
  | 'macroscopic' // 10^-6 to 10^6 m
  | 'stellar'     // 10^6 to 10^15 m
  | 'galactic'    // 10^15 to 10^21 m
  | 'cosmological'; // 10^21 to 10^26 m

export interface ScalePoint {
  domain: ScaleDomain;
  name: string;
  meters: number;
  log10: number;
  description: string;
  kValue?: number;
  keyConcept: string;
}

export const SCALE_POINTS: ScalePoint[] = [
  // Domain 1: Planck/Nuclear
  { domain: 'planck', name: 'Spation Lattice', meters: 1.616e-35, log10: -34.79, description: 'Planck length - spation spacing', keyConcept: 'K_bulk = 4.6×10¹¹³ Pa' },
  { domain: 'planck', name: 'Proton Radius', meters: 8.41e-16, log10: -15.08, description: 'Nuclear scale', kValue: 5.28e-7, keyConcept: 'Nuclear pressure from CMB focusing' },
  
  // Domain 2: Atomic
  { domain: 'atomic', name: 'Electron Torus', meters: 2.82e-15, log10: -14.55, description: 'Classical electron radius', keyConcept: 'Toroidal structure' },
  { domain: 'atomic', name: 'Bohr Radius', meters: 5.292e-11, log10: -10.28, description: 'Hydrogen ground state', kValue: 137.036, keyConcept: 'Pressure balance creates orbit' },
  
  // Domain 3: Molecular
  { domain: 'molecular', name: 'H₂ Bond', meters: 7.4e-11, log10: -10.13, description: 'Hydrogen molecule bond length', keyConcept: 'Pressure equilibria' },
  { domain: 'molecular', name: 'Water Molecule', meters: 2.8e-10, log10: -9.55, description: 'H₂O size', keyConcept: '104.45° from pressure minimization' },
  
  // Domain 4: Macroscopic
  { domain: 'macroscopic', name: 'Human Scale', meters: 1, log10: 0, description: 'Reference scale', keyConcept: 'Reference point' },
  { domain: 'macroscopic', name: 'Earth Radius', meters: 6.371e6, log10: 6.80, description: 'Planetary scale', kValue: 59254, keyConcept: 'Gravity from pressure gradients' },
  
  // Domain 5: Stellar
  { domain: 'stellar', name: 'Solar Radius', meters: 6.963e8, log10: 8.84, description: 'Stellar scale', keyConcept: 'Stellar pressure balance' },
  { domain: 'stellar', name: 'Earth Orbit', meters: 1.496e11, log10: 11.17, description: '1 AU', kValue: 59254, keyConcept: 'k-law universality' },
  
  // Domain 6: Galactic
  { domain: 'galactic', name: 'Galactic Disk', meters: 5e20, log10: 20.70, description: 'Milky Way scale', kValue: 1e5, keyConcept: 'Disk eclipse saturation' },
  
  // Domain 7: Cosmological
  { domain: 'cosmological', name: 'BAO Scale', meters: 1.47e24, log10: 24.17, description: '147 Mpc - Baryon Acoustic Oscillation', keyConcept: 'Pressure waves' },
  { domain: 'cosmological', name: 'CMB Boundary', meters: 4.4e26, log10: 26.64, description: 'z=1089 - Cosmic Microwave Background', keyConcept: 'Ultimate boundary - where counting stops' },
];

export class ScaleManager {
  private currentScaleIndex: number = 0;
  private targetScaleIndex: number = 0;
  private transitionProgress: number = 0;
  private isTransitioning: boolean = false;
  
  private onScaleChangeCallbacks: Array<(scale: ScalePoint) => void> = [];
  private onTransitionCompleteCallbacks: Array<() => void> = [];

  getCurrentScale(): ScalePoint {
    return SCALE_POINTS[this.currentScaleIndex];
  }

  getTargetScale(): ScalePoint {
    return SCALE_POINTS[this.targetScaleIndex];
  }

  getScaleAt(index: number): ScalePoint {
    return SCALE_POINTS[index];
  }

  getAllScales(): ScalePoint[] {
    return SCALE_POINTS;
  }

  getScalesInDomain(domain: ScaleDomain): ScalePoint[] {
    return SCALE_POINTS.filter(s => s.domain === domain);
  }

  /**
   * Transition to a specific scale index
   */
  transitionTo(index: number, duration: number = 3000): void {
    if (index < 0 || index >= SCALE_POINTS.length) return;
    
    this.targetScaleIndex = index;
    this.isTransitioning = true;
    this.transitionProgress = 0;

    // Animate transition
    const startTime = performance.now();
    const animate = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      this.transitionProgress = Math.min(elapsed / duration, 1);
      
      // Easing function (ease-in-out)
      const eased = this.easeInOutCubic(this.transitionProgress);
      
      if (this.transitionProgress < 1) {
        requestAnimationFrame(animate);
      } else {
        this.currentScaleIndex = this.targetScaleIndex;
        this.isTransitioning = false;
        this.transitionProgress = 0;
        this.onTransitionCompleteCallbacks.forEach(cb => cb());
      }
      
      // Notify scale change during transition
      this.onScaleChangeCallbacks.forEach(cb => {
        const interpolatedScale = this.interpolateScale(eased);
        cb(interpolatedScale);
      });
    };
    
    requestAnimationFrame(animate);
  }

  /**
   * Transition to next scale
   */
  transitionToNext(duration: number = 3000): void {
    if (this.currentScaleIndex < SCALE_POINTS.length - 1) {
      this.transitionTo(this.currentScaleIndex + 1, duration);
    }
  }

  /**
   * Transition to previous scale
   */
  transitionToPrevious(duration: number = 3000): void {
    if (this.currentScaleIndex > 0) {
      this.transitionTo(this.currentScaleIndex - 1, duration);
    }
  }

  /**
   * Jump to a specific domain
   */
  jumpToDomain(domain: ScaleDomain): void {
    const domainScales = this.getScalesInDomain(domain);
    if (domainScales.length > 0) {
      const index = SCALE_POINTS.indexOf(domainScales[0]);
      this.transitionTo(index, 5000); // Longer transition for domain jumps
    }
  }

  /**
   * Get interpolated scale during transition
   */
  private interpolateScale(t: number): ScalePoint {
    const current = SCALE_POINTS[this.currentScaleIndex];
    const target = SCALE_POINTS[this.targetScaleIndex];
    
    // Logarithmic interpolation for meters
    const logCurrent = Math.log10(current.meters);
    const logTarget = Math.log10(target.meters);
    const logInterpolated = logCurrent + (logTarget - logCurrent) * t;
    
    return {
      ...current,
      meters: Math.pow(10, logInterpolated),
      log10: logInterpolated,
      name: t < 0.5 ? current.name : target.name,
      domain: t < 0.5 ? current.domain : target.domain,
    };
  }

  /**
   * Easing function: cubic ease-in-out
   */
  private easeInOutCubic(t: number): number {
    return t < 0.5
      ? 4 * t * t * t
      : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  /**
   * Calculate scale factor for visualization
   * Converts real-world meters to scene units
   */
  getScaleFactor(referenceMeters: number = 1): number {
    const current = this.getCurrentScale();
    // Use logarithmic scaling for visualization
    return Math.log10(current.meters / referenceMeters + 1) * 2 + 0.5;
  }

  /**
   * Get camera position for current scale
   */
  getCameraPosition(): [number, number, number] {
    const current = this.getCurrentScale();
    const log10 = current.log10;
    
    // Camera distance scales logarithmically
    const distance = Math.max(5, Math.abs(log10) * 0.5 + 5);
    
    return [0, distance * 0.6, distance];
  }

  /**
   * Register callback for scale changes
   */
  onScaleChange(callback: (scale: ScalePoint) => void): () => void {
    this.onScaleChangeCallbacks.push(callback);
    return () => {
      const index = this.onScaleChangeCallbacks.indexOf(callback);
      if (index > -1) {
        this.onScaleChangeCallbacks.splice(index, 1);
      }
    };
  }

  /**
   * Register callback for transition completion
   */
  onTransitionComplete(callback: () => void): () => void {
    this.onTransitionCompleteCallbacks.push(callback);
    return () => {
      const index = this.onTransitionCompleteCallbacks.indexOf(callback);
      if (index > -1) {
        this.onTransitionCompleteCallbacks.splice(index, 1);
      }
    };
  }

  isInTransition(): boolean {
    return this.isTransitioning;
  }

  getTransitionProgress(): number {
    return this.transitionProgress;
  }
}

