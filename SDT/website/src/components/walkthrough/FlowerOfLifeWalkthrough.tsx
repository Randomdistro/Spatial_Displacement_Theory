/**
 * Flower of Life Walkthrough - Main Entry Point
 * 
 * TEKNE: The walkthrough IS the spatial experience
 * 
 * Integrates:
 * - Flower of Life landing page with sacred geometry
 * - Three narrative paths (Fibonacci: 3, 5, 11 nodes)
 * - Sacred geometry background and transitions
 * - Golden ratio animations throughout
 */

import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Environment } from '@react-three/drei';
import * as THREE from 'three';
import { gsap } from 'gsap';
import FlowerOfLife from '../3d/FlowerOfLife';
import { useNavigationStore } from '../../store/navigationStore';
import PathView from './PathView';
import NodeDetailView from './NodeDetailView';
import LoadingSpinner from '../ui/LoadingSpinner';
import BreadcrumbNav from '../ui/BreadcrumbNav';
import ProgressIndicator from '../ui/ProgressIndicator';
import { ErrorBoundary } from '../ui/ErrorBoundary';
import PathCard from './PathCard';
import KeyboardShortcuts from '../ui/KeyboardShortcuts';
import MobileMenu from '../ui/MobileMenu';
import { useKeyboardShortcuts } from '../../hooks/useKeyboardShortcuts';

// Sacred geometry components
import SacredGeometryBackground from '../3d/SacredGeometryBackground';
import GeometricTransition from '../3d/GeometricTransition';
import AtmosphericEffects from '../3d/AtmosphericEffects';
import { PHI, PHI_INVERSE } from '../../utils/sacred-geometry';

export default function FlowerOfLifeWalkthrough() {
  const { currentState, currentPath, selectPath, returnToLanding } = useNavigationStore();
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [showTransitionEffect, setShowTransitionEffect] = useState(false);
  const [transitionVariant, setTransitionVariant] = useState<'portal' | 'spiral' | 'bloom'>('bloom');
  const [cameraPosition, setCameraPosition] = useState<[number, number, number]>([0, 0, 5]);
  const [cameraTarget, setCameraTarget] = useState<[number, number, number]>([0, 0, 0]);
  const cameraRef = React.useRef<THREE.PerspectiveCamera>(null);

  // Enable keyboard shortcuts
  useKeyboardShortcuts();

  // Update camera position when state changes
  useEffect(() => {
    if (cameraRef.current) {
      cameraRef.current.position.set(...cameraPosition);
      cameraRef.current.lookAt(...cameraTarget);
      cameraRef.current.updateProjectionMatrix();
    }
  }, [cameraPosition, cameraTarget]);

  // Path-specific camera positions (from prompt spec)
  const pathCameraPositions: Record<string, [number, number, number]> = {
    path1: [0, 1, 3], // Elevated, overview perspective
    path2: [0, 0, 4], // Centered, detailed view
    path3: [0, -1, 5], // Lowered, technical perspective
  };

  // Handle path selection with sacred geometry transition
  const handlePathSelect = (pathId: 'path1' | 'path2' | 'path3') => {
    setIsTransitioning(true);
    
    // Show geometric transition effect based on path
    // Path 1: Bloom (accessible, opening)
    // Path 2: Portal (diving deeper)
    // Path 3: Spiral (scientific precision)
    const variants: Record<string, 'portal' | 'spiral' | 'bloom'> = {
      path1: 'bloom',
      path2: 'portal',
      path3: 'spiral'
    };
    setTransitionVariant(variants[pathId]);
    setShowTransitionEffect(true);
    
    selectPath(pathId);

    // Animate camera transition using golden ratio timing
    const targetPosition = pathCameraPositions[pathId];
    const baseDuration = PHI; // Golden ratio base duration (~1.618s)

    // Phase 1-4 camera animation with golden ratio timing
    const timeline = gsap.timeline();
    
    // Phase 1: Move closer (quick approach)
    timeline.to({}, {
      duration: baseDuration * PHI_INVERSE, // ~1s
      ease: 'power2.out',
      onUpdate: function() {
        const progress = this.progress();
        // Golden easing
        const eased = Math.pow(progress, PHI_INVERSE);
        const z = 5 - (5 - 2) * eased;
        setCameraPosition([0, 0, z]);
      }
    });
    
    // Phase 2: Rotate around (orbital motion)
    timeline.to({}, {
      duration: baseDuration, // ~1.618s
      ease: 'none',
      onUpdate: function() {
        const progress = this.progress();
        const angle = progress * Math.PI * PHI_INVERSE; // Golden angle partial
        const radius = 2;
        const x = Math.sin(angle) * radius;
        const z = 2 + Math.cos(angle) * radius;
        setCameraPosition([x, 0, z]);
      }
    });
    
    // Phase 3: Move through rings
    timeline.to({}, {
      duration: baseDuration * PHI_INVERSE,
      ease: 'power2.inOut',
      onUpdate: function() {
        const progress = this.progress();
        const z = 2 - 4 * progress;
        setCameraPosition([0, 0, z]);
      },
      onComplete: () => {
        // Hide transition effect after camera passes through
        setShowTransitionEffect(false);
      }
    });
    
    // Phase 4: Settle into path position
    timeline.to({}, {
      duration: baseDuration * PHI_INVERSE * PHI_INVERSE, // Quick settle
      ease: 'power3.out',
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
    <ErrorBoundary>
      <div className="relative w-full h-screen bg-slate-900 overflow-hidden">
        {/* 3D Scene */}
        <Canvas
        gl={{ antialias: true, alpha: false }}
        dpr={[1, 2]}
        camera={{ position: cameraPosition, fov: 60 }}
      >
        {/* Sacred Geometry Background - subtle, always present */}
        <SacredGeometryBackground
          variant="both"
          opacity={0.08}
          scale={12}
          animated={!isTransitioning}
        />
        
        {/* Atmospheric Effects - spation medium visualization */}
        <AtmosphericEffects
          particleCount={800}
          fogDensity={0.015}
          glowIntensity={0.25}
        />
        
        {/* Geometric Transition Effect */}
        <GeometricTransition
          active={showTransitionEffect}
          variant={transitionVariant}
          duration={1500}
          onComplete={() => setShowTransitionEffect(false)}
        />
        
        {/* Lighting - Creative Agent Design System */}
        <ambientLight intensity={0.35} />
        <directionalLight position={[5, 5, 5]} intensity={0.7} castShadow />
        <pointLight position={[0, 0, 0]} intensity={0.3} color="#d69e2e" /> {/* Gold center */}
        
        {/* Environment for realistic reflections */}
        <Environment preset="night" />

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

         {/* Path View - 3D nodes */}
         {currentState === 'path' && currentPath && (
           <PathView pathId={currentPath} />
         )}
       </Canvas>

      {/* UI Overlay */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Landing Page Text - Enhanced */}
        {currentState === 'landing' && (
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-auto">
            <div className="text-center max-w-4xl px-4 animate-fade-in">
              <h1 className="text-5xl sm:text-6xl lg:text-7xl font-display font-bold text-white mb-6 leading-tight">
                <span className="bg-gradient-to-r from-blue-400 via-sdt-gold-400 to-blue-400 bg-clip-text text-transparent animate-gradient">
                  Spatial Displacement Theory
                </span>
              </h1>
              <p className="text-xl sm:text-2xl text-slate-300 mb-12 leading-relaxed">
                Choose your journey through the complete structural outline
              </p>
              
              {/* Enhanced Path Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
                <PathCard
                  pathId="path1"
                  title="Quick Tour"
                  description="15-minute introduction"
                  icon="⚡"
                  color="from-blue-400 to-blue-600"
                  onClick={() => handlePathSelect('path1')}
                />
                <PathCard
                  pathId="path2"
                  title="Deep Dive"
                  description="Comprehensive exploration"
                  icon="🌊"
                  color="from-blue-500 to-blue-700"
                  onClick={() => handlePathSelect('path2')}
                />
                <PathCard
                  pathId="path3"
                  title="Scientific Framework"
                  description="Rigorous physics language"
                  icon="🔬"
                  color="from-blue-600 to-blue-800"
                  onClick={() => handlePathSelect('path3')}
                />
              </div>

              {/* Hint text */}
              <p className="mt-12 text-sm text-slate-500 animate-pulse">
                Click on the rings above or select a path below
              </p>
            </div>
          </div>
        )}

         {/* Path View UI Overlay - Enhanced */}
         {currentState === 'path' && currentPath && (
           <div className="absolute inset-0 pointer-events-auto">
             {/* Enhanced Back Button */}
             <button
               onClick={handleReturnToLanding}
               className="absolute top-4 left-4 z-10 group bg-black/60 backdrop-blur-md text-white px-4 py-2 rounded-lg hover:bg-black/80 transition-all border border-slate-700/50 hover:border-sdt-gold-500/50"
             >
               <span className="flex items-center gap-2">
                 <svg className="w-4 h-4 group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                 </svg>
                 Back to Landing
               </span>
             </button>

             {/* Path Info Card */}
             <div className="absolute top-4 right-4 z-10 bg-black/60 backdrop-blur-md text-white px-4 py-2 rounded-lg border border-slate-700/50">
               <div className="flex items-center gap-2">
                 <div className="w-2 h-2 rounded-full bg-sdt-gold-500 animate-pulse" />
                 <span className="text-sm font-medium">
                   {currentPath === 'path1' ? 'Quick Tour' : currentPath === 'path2' ? 'Deep Dive' : 'Scientific Framework'}
                 </span>
               </div>
             </div>

             {/* Helpful Instructions */}
             <div className="absolute bottom-20 left-1/2 -translate-x-1/2 z-10 bg-black/60 backdrop-blur-md text-white px-4 py-2 rounded-lg border border-slate-700/50 text-xs text-center max-w-md">
               <p className="text-slate-400">
                 Click on any node to explore • Use mouse to rotate view • Scroll to zoom
               </p>
             </div>
           </div>
         )}

         {/* Node Detail View */}
         {currentState === 'node' && (
           <div className="absolute inset-0 pointer-events-auto">
             <NodeDetailView
               nodeId={useNavigationStore.getState().currentNode || ''}
               onClose={() => useNavigationStore.getState().returnToPath()}
             />
           </div>
         )}
      </div>

        {/* Enhanced Loading Indicator - uses GeometricSpinner */}
        {isTransitioning && (
          <LoadingSpinner
            size="lg"
            message={currentPath ? `Entering ${currentPath === 'path1' ? 'Quick Tour' : currentPath === 'path2' ? 'Deep Dive' : 'Scientific Framework'}...` : 'Transitioning...'}
            fullScreen={true}
            variant="geometric"
          />
        )}

        {/* Breadcrumb Navigation */}
        <BreadcrumbNav />

        {/* Progress Indicator */}
        {currentState === 'path' && <ProgressIndicator />}

        {/* Keyboard Shortcuts Helper */}
        {currentState !== 'landing' && <KeyboardShortcuts />}

        {/* Mobile Menu */}
        <MobileMenu />
      </div>
    </ErrorBoundary>
  );
}
