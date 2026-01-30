/**
 * Flower of Life Walkthrough - Main Entry Point
 * Integrates Flower of Life landing page with three narrative paths
 */

import React, { useState, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';
import { gsap } from 'gsap';
import FlowerOfLife from '../3d/FlowerOfLife';
import { useNavigationStore } from '../../store/navigationStore';
import PathView from './PathView';
import NodeRoom from './NodeRoom';

export default function FlowerOfLifeWalkthrough() {
  const { currentState, currentPath, selectPath, returnToLanding } = useNavigationStore();
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [cameraPosition, setCameraPosition] = useState<[number, number, number]>([0, 0, 5]);
  const [cameraTarget, setCameraTarget] = useState<[number, number, number]>([0, 0, 0]);
  const cameraRef = useRef<THREE.PerspectiveCamera>(null);

  // Path-specific camera positions (from prompt spec)
  const pathCameraPositions: Record<string, [number, number, number]> = {
    path1: [0, 1, 3], // Elevated, overview perspective
    path2: [0, 0, 4], // Centered, detailed view
    path3: [0, -1, 5], // Lowered, technical perspective
  };

  // Handle path selection
  const handlePathSelect = (pathId: 'path1' | 'path2' | 'path3') => {
    setIsTransitioning(true);
    selectPath(pathId);

    // Animate camera transition
    const targetPosition = pathCameraPositions[pathId];
    const duration = 3.5; // seconds

    // Phase 1-4 camera animation (from prompt spec)
    const timeline = gsap.timeline();
    
    // Phase 1: Move closer
    timeline.to({}, {
      duration: 1,
      onUpdate: function() {
        const progress = this.progress();
        const z = 5 - (5 - 2) * progress;
        setCameraPosition([0, 0, z]);
      }
    });
    
    // Phase 2: Rotate around
    timeline.to({}, {
      duration: 1,
      onUpdate: function() {
        const progress = this.progress();
        const angle = progress * Math.PI * 0.5;
        const radius = 2;
        const x = Math.sin(angle) * radius;
        const z = 2 + Math.cos(angle) * radius;
        setCameraPosition([x, 0, z]);
      }
    });
    
    // Phase 3: Move through rings
    timeline.to({}, {
      duration: 1,
      onUpdate: function() {
        const progress = this.progress();
        const z = 2 - 4 * progress;
        setCameraPosition([0, 0, z]);
      }
    });
    
    // Phase 4: Settle into path position
    timeline.to({}, {
      duration: 0.5,
      onUpdate: function() {
        const progress = this.progress();
        const [tx, ty, tz] = targetPosition;
        const [sx, sy, sz] = [0, 0, -2];
        setCameraPosition([
          sx + (tx - sx) * progress,
          sy + (ty - sy) * progress,
          sz + (tz - sz) * progress
        ]);
      },
      onComplete: () => {
        setCameraPosition(targetPosition);
        setIsTransitioning(false);
      }
    });
  };

  // Handle return to landing
  const handleReturnToLanding = () => {
    setIsTransitioning(true);
    returnToLanding();
    
    // Animate camera back to landing position
    gsap.to({}, {
      duration: 2,
      onUpdate: function() {
        const progress = this.progress();
        const [tx, ty, tz] = [0, 0, 5];
        const [sx, sy, sz] = cameraPosition;
        setCameraPosition([
          sx + (tx - sx) * progress,
          sy + (ty - sy) * progress,
          sz + (tz - sz) * progress
        ]);
      },
      onComplete: () => {
        setCameraPosition([0, 0, 5]);
        setCameraTarget([0, 0, 0]);
        setIsTransitioning(false);
      }
    });
  };

  return (
    <div className="relative w-full h-screen bg-slate-900 overflow-hidden">
      {/* 3D Scene */}
      <Canvas
        gl={{ antialias: true, alpha: false }}
        dpr={[1, 2]}
        camera={{ position: cameraPosition, fov: 60 }}
      >
        {/* Lighting */}
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 5, 5]} intensity={0.8} />
        <pointLight position={[0, 0, 0]} intensity={0.3} />

        {/* Camera */}
        <PerspectiveCamera
          ref={cameraRef}
          makeDefault
          position={cameraPosition}
          fov={60}
        />

        {/* Controls - only enable when not transitioning */}
        {!isTransitioning && (
          <OrbitControls
            target={cameraTarget}
            minDistance={1}
            maxDistance={10}
            enablePan={true}
            enableZoom={true}
            enableRotate={true}
            maxPolarAngle={Math.PI * 0.95}
            minPolarAngle={Math.PI * 0.05}
            dampingFactor={0.05}
          />
        )}

        {/* Scene Content */}
        {currentState === 'landing' && (
          <FlowerOfLife
            onPathSelect={handlePathSelect}
            isTransitioning={isTransitioning}
          />
        )}
      </Canvas>

      {/* UI Overlay */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Landing Page Text */}
        {currentState === 'landing' && (
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-auto">
            <div className="text-center max-w-4xl px-4">
              <h1 className="text-5xl sm:text-6xl lg:text-7xl font-display font-bold text-white mb-6 leading-tight">
                Spatial Displacement Theory
              </h1>
              <p className="text-xl sm:text-2xl text-slate-300 mb-8 leading-relaxed">
                Choose your journey through the complete structural outline
              </p>
              <div className="flex flex-wrap justify-center gap-4 text-sm text-slate-400">
              <div className="flex flex-wrap justify-center gap-4 text-sm text-slate-400">
                <button 
                  onClick={() => handlePathSelect('path1')}
                  className="bg-white/10 hover:bg-white/20 hover:scale-105 transition-all backdrop-blur-sm rounded-lg px-4 py-2 text-left cursor-pointer border border-transparent hover:border-amber-500/50"
                >
                  <div className="font-semibold text-white mb-1">Quick Tour ⚡</div>
                  <div>15-minute introduction</div>
                </button>
                <button 
                  onClick={() => handlePathSelect('path2')}
                  className="bg-white/10 hover:bg-white/20 hover:scale-105 transition-all backdrop-blur-sm rounded-lg px-4 py-2 text-left cursor-pointer border border-transparent hover:border-blue-500/50"
                >
                  <div className="font-semibold text-white mb-1">Deep Dive 🔬</div>
                  <div>Comprehensive exploration</div>
                </button>
                <button 
                  onClick={() => handlePathSelect('path3')}
                  className="bg-white/10 hover:bg-white/20 hover:scale-105 transition-all backdrop-blur-sm rounded-lg px-4 py-2 text-left cursor-pointer border border-transparent hover:border-purple-500/50"
                >
                  <div className="font-semibold text-white mb-1">Scientific Framework 📐</div>
                  <div>Rigorous physics language</div>
                </button>
              </div>
              </div>
            </div>
          </div>
        )}

        {/* Path View */}
        {currentState === 'path' && currentPath && (
          <div className="absolute inset-0 pointer-events-auto">
            <PathView pathId={currentPath} onReturn={handleReturnToLanding} />
          </div>
        )}

        {/* Node View */}
        {currentState === 'node' && (
          <div className="absolute inset-0 pointer-events-auto">
            <NodeRoom onReturn={() => useNavigationStore.getState().returnToPath()} />
          </div>
        )}
      </div>

      {/* Loading Indicator */}
      {isTransitioning && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm pointer-events-none">
          <div className="text-white text-lg">Loading...</div>
        </div>
      )}
    </div>
  );
}








