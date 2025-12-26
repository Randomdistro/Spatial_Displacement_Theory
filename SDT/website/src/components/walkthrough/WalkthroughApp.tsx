/**
 * Complete SDT Walkthrough Application
 * Main component orchestrating the 43-order-of-magnitude journey
 */

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { ScaleManager, ScalePoint, SCALE_POINTS } from './ScaleManager';
import { PressureFieldVisualization } from './PressureFieldRenderer';
import { Domain1Visualization } from './domains/Domain1_PlanckNuclear';
import { Domain2Visualization } from './domains/Domain2_Atomic';
import { Domain3Visualization } from './domains/Domain3_Molecular';
import { Domain4Visualization } from './domains/Domain4_Macroscopic';
import { Domain5Visualization } from './domains/Domain5_Stellar';
import { Domain6Visualization } from './domains/Domain6_Galactic';
import { Domain7Visualization } from './domains/Domain7_Cosmological';
import { IDomainVisualization } from './domains/DomainBase';
import { NarrationSystem } from './NarrationSystem';
import { WALKTHROUGH_NARRATION } from './WalkthroughNarration';
import { ExpandableContent, createConceptualExpansion, createTechnicalExpansion } from './ExpandableContent';
import { MasterEquation, KLawFormula } from '../simulations/FormulaRenderer';
import { CameraChoreography } from './CameraChoreography';
import { FormulaOverlay } from './FormulaOverlay';
import { ScaleTransitionEffectsComponent } from './ScaleTransitionEffects';
import { ForceHierarchyVisualization } from './ForceHierarchyVisualization';

interface WalkthroughAppProps {
  mode?: 'continuous' | 'interactive' | 'hybrid';
  onComplete?: () => void;
  onGetOut?: (scale: ScalePoint) => void;
}

export const WalkthroughApp: React.FC<WalkthroughAppProps> = ({
  mode = 'hybrid',
  onComplete,
  onGetOut,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  
  const scaleManagerRef = useRef<ScaleManager | null>(null);
  const pressureFieldRef = useRef<PressureFieldVisualization | null>(null);
  const domainVisualizationRef = useRef<IDomainVisualization | null>(null);
  const narrationRef = useRef<NarrationSystem | null>(null);
  const cameraChoreographyRef = useRef<CameraChoreography | null>(null);
  
  const [currentScale, setCurrentScale] = useState<ScalePoint>(SCALE_POINTS[0]);
  const [previousScale, setPreviousScale] = useState<ScalePoint | null>(null);
  const [transitionProgress, setTransitionProgress] = useState(0);
  const [time, setTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [showGetOutPrompt, setShowGetOutPrompt] = useState(false);
  const [currentNarrationText, setCurrentNarrationText] = useState<string>('');
  const [showExpandableContent, setShowExpandableContent] = useState(false);
  const [showForceHierarchy, setShowForceHierarchy] = useState(false);
  const [highlightedFormula, setHighlightedFormula] = useState<string | undefined>();

  useEffect(() => {
    if (!containerRef.current) {
      console.error('WalkthroughApp: containerRef.current is null');
      return;
    }

    console.log('WalkthroughApp: Initializing Three.js scene...');

    // Initialize Three.js scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a0a);
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(
      60,
      containerRef.current.clientWidth / containerRef.current.clientHeight,
      0.1,
      10000
    );
    camera.position.set(0, 5, 10);
    camera.lookAt(0, 0, 0);
    cameraRef.current = camera;

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    const width = containerRef.current.clientWidth || window.innerWidth;
    const height = containerRef.current.clientHeight || window.innerHeight;
    console.log(`WalkthroughApp: Renderer size: ${width}x${height}`);
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    containerRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;
    console.log('WalkthroughApp: Three.js initialized successfully');

    // Setup lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);

    // Initialize scale manager
    const scaleManager = new ScaleManager();
    scaleManagerRef.current = scaleManager;

    // Initialize pressure field renderer
    const pressureField = new PressureFieldVisualization(scene);
    pressureFieldRef.current = pressureField;
    pressureField.update(currentScale, 1.0, true, false);

    // Initialize narration system
    const narration = new NarrationSystem();
    narration.loadScript(WALKTHROUGH_NARRATION);
    narration.onSegmentChange((segment) => {
      setCurrentNarrationText(segment.text);
      if (segment.formula) {
        setHighlightedFormula(segment.formula);
      }
    });
    narrationRef.current = narration;

    // Initialize camera choreography
    const cameraChoreography = new CameraChoreography(camera);
    cameraChoreographyRef.current = cameraChoreography;

    // Setup scale change callback
    scaleManager.onScaleChange((scale) => {
      setPreviousScale(currentScale);
      setCurrentScale(scale);
      pressureField.update(scale, 1.0, true, scale.domain === 'cosmological');
      
      // Animate camera with choreography
      if (cameraChoreographyRef.current) {
        cameraChoreographyRef.current.animateToScale(scale, () => {
          // Camera animation complete
        });
      }
      
      // Update domain visualization
      if (domainVisualizationRef.current) {
        domainVisualizationRef.current.dispose();
        domainVisualizationRef.current = null;
      }
      
      // Create appropriate domain visualization
      let newVisualization: IDomainVisualization | null = null;
      switch (scale.domain) {
        case 'planck':
          newVisualization = new Domain1Visualization(scene);
          break;
        case 'atomic':
          newVisualization = new Domain2Visualization(scene);
          setShowForceHierarchy(true);
          break;
        case 'molecular':
          newVisualization = new Domain3Visualization(scene);
          break;
        case 'macroscopic':
          newVisualization = new Domain4Visualization(scene);
          setShowForceHierarchy(true);
          break;
        case 'stellar':
          newVisualization = new Domain5Visualization(scene);
          break;
        case 'galactic':
          newVisualization = new Domain6Visualization(scene);
          break;
        case 'cosmological':
          newVisualization = new Domain7Visualization(scene);
          // Special CMB reveal
          if (cameraChoreographyRef.current && scale.name === 'CMB Boundary') {
            setTimeout(() => {
              cameraChoreographyRef.current?.revealCMBBoundary();
            }, 1000);
          }
          break;
      }
      
      if (newVisualization) {
        domainVisualizationRef.current = newVisualization;
        newVisualization.initialize(scale);
      }
    });

    // Track transition progress
    scaleManager.onTransitionComplete(() => {
      setTransitionProgress(0);
    });

    // Animation loop
    let lastTime = performance.now();
    const animate = () => {
      animationFrameRef.current = requestAnimationFrame(animate);
      
      const currentTime = performance.now();
      const deltaTime = (currentTime - lastTime) / 1000; // Convert to seconds
      lastTime = currentTime;
      
      // Update domain visualization
      if (domainVisualizationRef.current) {
        domainVisualizationRef.current.update(deltaTime);
      }
      
      setTime(prev => prev + deltaTime);
      
      if (renderer && scene && camera) {
        renderer.render(scene, camera);
      }
    };
    animate();

    // Handle resize
    const handleResize = () => {
      if (!containerRef.current || !camera || !renderer) return;
      const width = containerRef.current.clientWidth;
      const height = containerRef.current.clientHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      if (pressureFieldRef.current) {
        pressureFieldRef.current.dispose();
      }
      if (rendererRef.current && containerRef.current) {
        containerRef.current.removeChild(rendererRef.current.domElement);
        rendererRef.current.dispose();
      }
    };
  }, []);

  // Auto-play continuous mode
  useEffect(() => {
    if (mode === 'continuous' && !isPaused && scaleManagerRef.current) {
      const interval = setInterval(() => {
        if (scaleManagerRef.current) {
          const currentIndex = SCALE_POINTS.findIndex(s => s === currentScale);
          if (currentIndex < SCALE_POINTS.length - 1) {
            scaleManagerRef.current.transitionToNext(3000);
          } else {
            // Complete
            if (onComplete) onComplete();
            clearInterval(interval);
          }
        }
      }, 3500); // Transition + pause

      return () => clearInterval(interval);
    }
  }, [mode, isPaused, currentScale, onComplete]);

  // Show "Get Out" prompt at domain transitions
  useEffect(() => {
    const currentIndex = SCALE_POINTS.findIndex(s => s === currentScale);
    const isDomainTransition = currentIndex > 0 && 
      SCALE_POINTS[currentIndex].domain !== SCALE_POINTS[currentIndex - 1].domain;
    
    if (isDomainTransition && mode !== 'continuous') {
      setShowGetOutPrompt(true);
      setIsPaused(true);
    }
  }, [currentScale, mode]);

  const handleGetOut = () => {
    if (onGetOut) {
      onGetOut(currentScale);
    }
    setShowGetOutPrompt(false);
  };

  const handleContinue = () => {
    setShowGetOutPrompt(false);
    setIsPaused(false);
    if (scaleManagerRef.current) {
      scaleManagerRef.current.transitionToNext(3000);
    }
  };

  const handlePlayPause = () => {
    setIsPaused(!isPaused);
    if (narrationRef.current) {
      if (isPaused) {
        narrationRef.current.resume();
      } else {
        narrationRef.current.pause();
      }
    }
  };

  const handleStartNarration = () => {
    if (narrationRef.current) {
      narrationRef.current.play();
      setIsPlaying(true);
    }
  };

  const getExpandableContent = (): React.ReactNode => {
    const expansions = [];
    
    // Add domain-specific expansions
    if (currentScale.domain === 'planck') {
      expansions.push(
        createConceptualExpansion("The spation lattice is the fundamental structure of space. K_bulk represents the stiffness of this lattice—the pressure required to compress it. This enormous value (10¹¹³ Pa) shows why space appears empty at our scale."),
        createTechnicalExpansion(
          "K_{bulk} = 4.6 \\times 10^{113} \\text{ Pa}",
          "The bulk modulus of the spation medium. This value emerges from the dodecahedral packing structure and Planck-scale spacing."
        )
      );
    } else if (currentScale.domain === 'atomic') {
      expansions.push(
        createConceptualExpansion("Coulomb force doesn't come from electric fields—it comes from mutual occlusion in the CMB pressure field. When two particles block each other's view of the CMB boundary, a pressure imbalance creates the force we call 'electromagnetic'."),
        createTechnicalExpansion(
          "F_C = \\frac{\\pi}{4} P_{CMB} \\frac{R_N^2 R_e^2}{r^2}",
          "Coulomb force from CMB mutual occlusion. P_CMB is the pressure from the CMB boundary. R_N and R_e are the effective radii of nucleus and electron."
        )
      );
    } else if (currentScale.domain === 'cosmological') {
      expansions.push(
        createConceptualExpansion("The CMB isn't a historical relic—it's the structural boundary where all pressure originates. We've counted all pressure volumes from Planck scale outward. The CMB is where counting stops. It's the edge. The source of all energy."),
        createTechnicalExpansion(
          "P_{CMB} = 2.036 \\times 10^{-2} \\text{ Pa}",
          "The pressure from the CMB boundary at z=1089. This is the source pressure for all forces in the observable universe."
        )
      );
    }
    
    if (expansions.length === 0) return null;
    
    return (
      <ExpandableContent
        title="Do you want to know more?"
        expansions={expansions}
        defaultExpanded={false}
      />
    );
  };

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', overflow: 'hidden' }}>
      <div
        ref={containerRef}
        style={{ width: '100%', height: '100%', background: '#0a0a0a' }}
      />
      
      {/* UI Overlay */}
      <div className="absolute top-4 left-4 bg-black/70 backdrop-blur-sm text-white p-4 rounded-lg text-sm max-w-md">
        <div className="font-semibold mb-2 text-amber-400">Current Scale</div>
        <div className="space-y-1 text-xs">
          <div className="flex justify-between">
            <span className="text-slate-400">Domain:</span>
            <span className="font-mono capitalize">{currentScale.domain}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Scale:</span>
            <span className="font-mono">{currentScale.name}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Size:</span>
            <span className="font-mono">{currentScale.meters.toExponential(2)} m</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">log₁₀:</span>
            <span className="font-mono">{currentScale.log10.toFixed(2)}</span>
          </div>
          {currentScale.kValue && (
            <div className="flex justify-between">
              <span className="text-slate-400">k-value:</span>
              <span className="font-mono">{currentScale.kValue.toExponential(2)}</span>
            </div>
          )}
          <div className="mt-2 pt-2 border-t border-slate-600 text-slate-300 text-xs">
            {currentScale.keyConcept}
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-black/70 backdrop-blur-sm text-white p-3 rounded-lg flex gap-2">
        <button
          onClick={handlePlayPause}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded transition-colors"
        >
          {isPaused ? '▶ Play' : '⏸ Pause'}
        </button>
        {scaleManagerRef.current && (
          <>
            <button
              onClick={() => scaleManagerRef.current?.transitionToPrevious(3000)}
              className="px-4 py-2 bg-slate-600 hover:bg-slate-700 rounded transition-colors"
            >
              ← Previous
            </button>
            <button
              onClick={() => scaleManagerRef.current?.transitionToNext(3000)}
              className="px-4 py-2 bg-slate-600 hover:bg-slate-700 rounded transition-colors"
            >
              Next →
            </button>
          </>
        )}
      </div>

      {/* "Get Out" Prompt */}
      {showGetOutPrompt && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
          <div className="bg-slate-800 text-white p-6 rounded-lg max-w-md text-center">
            <h3 className="text-xl font-semibold mb-4 text-amber-400">
              Explore This Scale?
            </h3>
            <p className="text-slate-300 mb-6">
              You've reached a new domain. Would you like to explore this scale in detail, or continue the journey?
            </p>
            <div className="flex gap-4 justify-center">
              <button
                onClick={handleGetOut}
                className="px-6 py-3 bg-amber-600 hover:bg-amber-700 rounded-lg transition-colors font-semibold"
              >
                Explore
              </button>
              <button
                onClick={handleContinue}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors font-semibold"
              >
                Continue Journey
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Scale Progress Indicator */}
      <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm text-white p-3 rounded-lg text-xs">
        <div className="font-semibold mb-2">Scale Progress</div>
        <div className="w-64 h-2 bg-slate-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-blue-500 to-amber-500 transition-all duration-300"
            style={{
              width: `${((SCALE_POINTS.findIndex(s => s === currentScale) + 1) / SCALE_POINTS.length) * 100}%`,
            }}
          />
        </div>
        <div className="mt-2 text-slate-400">
          {SCALE_POINTS.findIndex(s => s === currentScale) + 1} / {SCALE_POINTS.length} scales
        </div>
      </div>

      {/* Narration Display */}
      {currentNarrationText && (
        <div className="absolute bottom-24 left-1/2 -translate-x-1/2 bg-black/80 backdrop-blur-sm text-white p-4 rounded-lg max-w-3xl text-center">
          <p className="text-sm leading-relaxed">{currentNarrationText}</p>
        </div>
      )}

      {/* Formula Overlay */}
      <FormulaOverlay
        scale={currentScale}
        showFormulas={true}
        highlightedFormula={highlightedFormula}
      />

      {/* Force Hierarchy Visualization */}
      {showForceHierarchy && (
        <ForceHierarchyVisualization
          scene={sceneRef.current!}
          show={showForceHierarchy}
          highlightForce={
            currentScale.domain === 'atomic' ? 'coulomb' :
            currentScale.domain === 'macroscopic' ? 'gravity' :
            'all'
          }
        />
      )}

      {/* Scale Transition Effects */}
      {previousScale && (
        <ScaleTransitionEffectsComponent
          scene={sceneRef.current!}
          fromScale={previousScale}
          toScale={currentScale}
          progress={transitionProgress}
        />
      )}

      {/* Expandable Content Panel */}
      <div className="absolute top-20 right-4 bg-black/70 backdrop-blur-sm text-white p-4 rounded-lg max-w-sm max-h-96 overflow-y-auto z-10">
        <button
          onClick={() => setShowExpandableContent(!showExpandableContent)}
          className="w-full text-left mb-2 text-amber-400 font-semibold hover:text-amber-300 transition-colors"
        >
          {showExpandableContent ? '▼ Hide Details' : '▶ Learn More'}
        </button>
        {showExpandableContent && getExpandableContent()}
      </div>

      {/* Start Narration Button */}
      {!isPlaying && (
        <button
          onClick={handleStartNarration}
          className="absolute top-20 left-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors font-semibold"
        >
          ▶ Start Narration
        </button>
      )}
    </div>
  );
};

// Default export for compatibility with existing imports
export default WalkthroughApp;
