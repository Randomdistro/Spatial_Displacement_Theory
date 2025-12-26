/**
 * Codemonkey Agent: Performance Monitoring System
 * 
 * All original performance monitoring - tracks FPS, frame times, and bottlenecks
 */

export interface PerformanceMetrics {
  fps: number;
  frameTime: number;
  frameTimeHistory: number[];
  componentRenderTimes: Map<string, number[]>;
  memoryUsage?: number;
  drawCalls?: number;
  triangles?: number;
}

export interface PerformanceReport {
  metrics: PerformanceMetrics;
  warnings: string[];
  recommendations: string[];
}

/**
 * Performance Monitor
 * Tracks and reports performance metrics
 */
export class PerformanceMonitor {
  private frameCount: number = 0;
  private lastFrameTime: number = performance.now();
  private frameTimeHistory: number[] = [];
  private componentRenderTimes: Map<string, number[]> = new Map();
  private maxHistoryLength: number = 60; // Keep last 60 frames
  private warnings: string[] = [];
  private targetFPS: number = 60;
  private targetFrameTime: number = 1000 / 60; // ~16.67ms

  /**
   * Record frame
   */
  recordFrame(): void {
    const now = performance.now();
    const frameTime = now - this.lastFrameTime;
    
    this.frameTimeHistory.push(frameTime);
    if (this.frameTimeHistory.length > this.maxHistoryLength) {
      this.frameTimeHistory.shift();
    }

    this.lastFrameTime = now;
    this.frameCount++;

    // Check for performance issues
    this.checkPerformance(frameTime);
  }

  /**
   * Record component render time
   */
  recordComponentRender(componentName: string, renderTime: number): void {
    if (!this.componentRenderTimes.has(componentName)) {
      this.componentRenderTimes.set(componentName, []);
    }

    const times = this.componentRenderTimes.get(componentName)!;
    times.push(renderTime);
    
    if (times.length > this.maxHistoryLength) {
      times.shift();
    }
  }

  /**
   * Get current metrics
   */
  getMetrics(): PerformanceMetrics {
    const avgFrameTime = this.getAverageFrameTime();
    const fps = avgFrameTime > 0 ? 1000 / avgFrameTime : 0;

    return {
      fps: Math.round(fps),
      frameTime: avgFrameTime,
      frameTimeHistory: [...this.frameTimeHistory],
      componentRenderTimes: new Map(this.componentRenderTimes),
    };
  }

  /**
   * Get average frame time
   */
  getAverageFrameTime(): number {
    if (this.frameTimeHistory.length === 0) return 0;
    
    const sum = this.frameTimeHistory.reduce((a, b) => a + b, 0);
    return sum / this.frameTimeHistory.length;
  }

  /**
   * Get FPS
   */
  getFPS(): number {
    const avgFrameTime = this.getAverageFrameTime();
    return avgFrameTime > 0 ? Math.round(1000 / avgFrameTime) : 0;
  }

  /**
   * Check for performance issues
   */
  private checkPerformance(frameTime: number): void {
    this.warnings = [];

    // Check frame time
    if (frameTime > this.targetFrameTime * 1.5) {
      this.warnings.push(`Frame time ${frameTime.toFixed(2)}ms exceeds target (${this.targetFrameTime.toFixed(2)}ms)`);
    }

    // Check FPS
    const fps = 1000 / frameTime;
    if (fps < this.targetFPS * 0.9) {
      this.warnings.push(`FPS ${fps.toFixed(1)} below target (${this.targetFPS})`);
    }

    // Check for slow components
    for (const [component, times] of this.componentRenderTimes) {
      const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
      if (avgTime > 5) { // 5ms threshold
        this.warnings.push(`Component "${component}" average render time: ${avgTime.toFixed(2)}ms`);
      }
    }
  }

  /**
   * Generate performance report
   */
  generateReport(): PerformanceReport {
    const metrics = this.getMetrics();
    const recommendations: string[] = [];

    // Generate recommendations
    if (metrics.fps < this.targetFPS * 0.9) {
      recommendations.push('Consider reducing geometry complexity');
      recommendations.push('Enable LOD (Level of Detail) system');
      recommendations.push('Reduce particle counts');
      recommendations.push('Simplify shaders');
    }

    // Find slowest components
    const componentAverages = new Map<string, number>();
    for (const [component, times] of metrics.componentRenderTimes) {
      const avg = times.reduce((a, b) => a + b, 0) / times.length;
      componentAverages.set(component, avg);
    }

    const sortedComponents = Array.from(componentAverages.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3);

    if (sortedComponents.length > 0) {
      recommendations.push(`Optimize slowest components: ${sortedComponents.map(c => c[0]).join(', ')}`);
    }

    return {
      metrics,
      warnings: [...this.warnings],
      recommendations,
    };
  }

  /**
   * Reset metrics
   */
  reset(): void {
    this.frameCount = 0;
    this.frameTimeHistory = [];
    this.componentRenderTimes.clear();
    this.warnings = [];
  }
}

// Global monitor instance
export const performanceMonitor = new PerformanceMonitor();

