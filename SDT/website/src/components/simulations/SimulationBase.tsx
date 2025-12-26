/**
 * Base simulation component interface
 * Agent 3: Physics/Simulation
 */

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

export interface SimulationProps {
  id: string;
  parameters: Record<string, number>;
  onParameterChange?: (key: string, value: number) => void;
  showFormulas?: boolean;
  showLabels?: boolean;
  narrationEnabled?: boolean;
  onReady?: () => void;
}

export interface SimulationState {
  isPlaying: boolean;
  time: number;
  cameraPosition?: [number, number, number];
}

export interface SimulationRef {
  play: () => void;
  pause: () => void;
  reset: () => void;
  getState: () => SimulationState;
}

/**
 * Base class for all simulations
 * Provides common functionality: scene setup, animation loop, parameter management
 */
export abstract class SimulationBase {
  protected scene: THREE.Scene;
  protected camera: THREE.PerspectiveCamera;
  protected renderer: THREE.WebGLRenderer;
  protected container: HTMLElement;
  protected animationId: number | null = null;
  protected isPlaying: boolean = false;
  protected time: number = 0;
  protected parameters: Record<string, number> = {};

  constructor(container: HTMLElement) {
    this.container = container;
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(
      60,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(container.clientWidth, container.clientHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(this.renderer.domElement);

    // Setup lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    this.scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 5, 5);
    this.scene.add(directionalLight);

    // Handle resize
    window.addEventListener('resize', this.handleResize.bind(this));
  }

  abstract init(): void;
  abstract update(deltaTime: number): void;
  abstract dispose(): void;

  setParameters(params: Record<string, number>): void {
    this.parameters = { ...this.parameters, ...params };
    this.onParametersChanged();
  }

  protected onParametersChanged(): void {
    // Override in subclasses
  }

  play(): void {
    if (this.isPlaying) return;
    this.isPlaying = true;
    this.animate();
  }

  pause(): void {
    this.isPlaying = false;
    if (this.animationId !== null) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  reset(): void {
    this.time = 0;
    this.pause();
    this.init();
  }

  private animate = (): void => {
    if (!this.isPlaying) return;
    
    const deltaTime = 0.016; // ~60 FPS
    this.time += deltaTime;
    this.update(deltaTime);
    this.renderer.render(this.scene, this.camera);
    
    this.animationId = requestAnimationFrame(this.animate);
  };

  private handleResize(): void {
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  destroy(): void {
    this.pause();
    window.removeEventListener('resize', this.handleResize.bind(this));
    this.dispose();
    this.renderer.dispose();
    if (this.container.contains(this.renderer.domElement)) {
      this.container.removeChild(this.renderer.domElement);
    }
  }
}

