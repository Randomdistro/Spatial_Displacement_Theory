/**
 * Base interface for all domain visualizations
 */

import { ScalePoint } from '../ScaleManager';

export interface IDomainVisualization {
  initialize(scale: ScalePoint): void;
  update(deltaTime: number): void;
  dispose(): void;
}

