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
  const animationFrameRef = useRef<number | null>(null);
  
  const scaleManagerRef = useRef<ScaleManager | null>(null);
  const pressureFieldRef = useRef<PressureFieldVisualization | null>(null);
  const domainVisualizationRef = useRef<IDomainVisualization | null>(null);
  const narrationRef = useRef<NarrationSystem | null>(null);
  const cameraChoreographyRef = useRef<CameraChoreography | null>(null);
  
  const [currentScale, setCurrentScale] = useState<ScalePoint>(SCALE_POINTS[0]);
  const [currentScaleIndex, setCurrentScaleIndex] = useState(0);
  const [previousScale, setPreviousScale] = useState<ScalePoint | null>(null);
  const [transitionProgress, setTransitionProgress] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [showGetOutPrompt, setShowGetOutPrompt] = useState(false);
  const [currentNarrationText, setCurrentNarrationText] = useState<string>('');
  const [showExpandableContent, setShowExpandableContent] = useState(false);
  const [showForceHierarchy, setShowForceHierarchy] = useState(false);
  const [highlightedFormula, setHighlightedFormula] = useState<string | undefined>();
  const [showTutorial, setShowTutorial] = useState(() => {
    // Check if user has seen tutorial before
    const hasSeenTutorial = localStorage.getItem('sdt-tutorial-seen');
    return !hasSeenTutorial;
  });
  const [initializationError, setInitializationError] = useState<Error | null>(null);

  useEffect(() => {
    try {
      if (!containerRef.current) {
        setInitializationError(new Error('Container element not found'));
        return;
      }

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

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    const width = containerRef.current.clientWidth || window.innerWidth;
    const height = containerRef.current.clientHeight || window.innerHeight;
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    containerRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

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
    pressureField.update(SCALE_POINTS[0], 1.0, true, false); // Use SCALE_POINTS[0] instead of currentScale

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
    // FIX #1: Use functional updates to avoid stale closure. FIX #3: Compare by name/log10, update index in same callback.
    const unsubscribeScaleChange = scaleManager.onScaleChange((scale) => {
      setCurrentScale(prev => {
        setPreviousScale(prev); // Use previous value from state
        return scale;
      });
      const newIndex = SCALE_POINTS.findIndex(s =>
        s.name === scale.name && s.log10 === scale.log10
      );
      if (newIndex >= 0) {
        setCurrentScaleIndex(newIndex);
      }
      
      // Update pressure field with new scale
      if (pressureFieldRef.current) {
        pressureFieldRef.current.update(scale, 1.0, true, scale.domain === 'cosmological');
      }
      
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
      
      // Create domain visualization
      const domainMap: Record<string, new (scene: THREE.Scene) => IDomainVisualization> = {
        planck: Domain1Visualization,
        atomic: Domain2Visualization,
        molecular: Domain3Visualization,
        macroscopic: Domain4Visualization,
        stellar: Domain5Visualization,
        galactic: Domain6Visualization,
        cosmological: Domain7Visualization,
      };
      
      const DomainClass = domainMap[scale.domain];
      if (DomainClass) {
        const newVisualization = new DomainClass(scene);
        domainVisualizationRef.current = newVisualization;
        newVisualization.initialize(scale);
        
        if (scale.domain === 'atomic' || scale.domain === 'macroscopic') {
          setShowForceHierarchy(true);
        }
        
        if (scale.domain === 'cosmological' && scale.name === 'CMB Boundary' && cameraChoreographyRef.current) {
          setTimeout(() => cameraChoreographyRef.current?.revealCMBBoundary(), 1000);
        }
      }
    });

    // Track transition progress
    const unsubscribeTransitionComplete = scaleManager.onTransitionComplete(() => {
      setTransitionProgress(0);
    });

    // Animation loop
    // FIX #4: Proper cleanup for animation loop
    let isMounted = true;
    let lastTime = performance.now();
    const animate = () => {
      if (!isMounted) return; // Stop if unmounted
      
      animationFrameRef.current = requestAnimationFrame(animate);
      
      const currentTime = performance.now();
      const deltaTime = (currentTime - lastTime) / 1000; // Convert to seconds
      lastTime = currentTime;
      
      // Update domain visualization
      if (domainVisualizationRef.current) {
        domainVisualizationRef.current.update(deltaTime);
      }
      
      if (renderer && scene && camera && isMounted) {
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
      isMounted = false;
      
      window.removeEventListener('resize', handleResize);
      
      if (animationFrameRef.current !== null) {
        cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }
      
      // Cleanup domain visualization
      if (domainVisualizationRef.current) {
        domainVisualizationRef.current.dispose();
        domainVisualizationRef.current = null;
      }
      
      if (pressureFieldRef.current) {
        pressureFieldRef.current.dispose();
        pressureFieldRef.current = null;
      }
      
      if (rendererRef.current) {
        if (containerRef.current && containerRef.current.contains(rendererRef.current.domElement)) {
          containerRef.current.removeChild(rendererRef.current.domElement);
        }
        rendererRef.current.dispose();
        rendererRef.current = null;
      }
      
      // Cleanup narration
      if (narrationRef.current) {
        narrationRef.current.stop();
        narrationRef.current = null;
      }
      
      unsubscribeScaleChange?.();
      unsubscribeTransitionComplete?.();
    };
    } catch (error) {
      setInitializationError(error instanceof Error ? error : new Error('Unknown initialization error'));
    }
  }, []);

  // Auto-play continuous mode

  useEffect(() => {
    if (mode !== 'continuous' || isPaused || !scaleManagerRef.current) return;
    
    const interval = setInterval(() => {
      if (currentScaleIndex < SCALE_POINTS.length - 1) {
        scaleManagerRef.current?.transitionToNext(3000);
      } else {
        onComplete?.();
        clearInterval(interval);
      }
    }, 3500);

    return () => clearInterval(interval);
  }, [mode, isPaused, currentScaleIndex, onComplete]);

  // Show "Get Out" prompt at domain transitions
  useEffect(() => {
    if (mode === 'continuous' || currentScaleIndex === 0) return;
    
    const isDomainTransition = 
      SCALE_POINTS[currentScaleIndex].domain !== SCALE_POINTS[currentScaleIndex - 1].domain;
    
    if (isDomainTransition) {
      setShowGetOutPrompt(true);
      setIsPaused(true);
    }
  }, [currentScaleIndex, mode]);

  const handleGetOut = () => {
    onGetOut?.(currentScale);
    setShowGetOutPrompt(false);
  };

  const handleContinue = () => {
    setShowGetOutPrompt(false);
    setIsPaused(false);
    scaleManagerRef.current?.transitionToNext(3000);
  };

  const handlePlayPause = () => {
    setIsPaused(prev => {
      narrationRef.current?.[prev ? 'resume' : 'pause']();
      return !prev;
    });
  };

  const handleStartNarration = () => {
    narrationRef.current?.play();
    setIsPlaying(true);
  };

  if (initializationError) {
    return (
      <div className="fixed inset-0 bg-slate-900 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-slate-800 rounded-xl p-8 border border-red-500/50">
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-500/20 flex items-center justify-center">
              <svg className="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">Initialization Error</h2>
            <p className="text-slate-400 mb-6">
              Failed to initialize the walkthrough. Please refresh the page.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium"
            >
              Refresh Page
            </button>
            {process.env.NODE_ENV === 'development' && (
              <details className="mt-4 text-left">
                <summary className="text-slate-400 cursor-pointer text-sm">Error Details</summary>
                <pre className="text-xs text-red-400 bg-slate-900 p-4 rounded mt-2 overflow-auto">
                  {initializationError.toString()}
                  {initializationError.stack}
                </pre>
              </details>
            )}
          </div>
        </div>
      </div>
    );
  }

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
    <div className="fixed inset-0 overflow-hidden z-[1]">
      {process.env.NODE_ENV === 'development' && (
        <div className="absolute top-2.5 right-2.5 bg-red-500 text-white px-2.5 py-2.5 text-[10px] z-[9999]">
          Dev
        </div>
      )}
      <div
        ref={containerRef}
        className="w-full h-full bg-[#0a0a0a] relative"
        style={{ touchAction: 'none' }} // Prevent default touch behaviors
      />
      
      {/* UI Overlay - Mobile Responsive */}
      <div className="absolute top-4 left-4 bg-black/70 backdrop-blur-sm text-white p-3 sm:p-4 rounded-lg text-xs sm:text-sm max-w-xs sm:max-w-md">
        <div className="font-semibold mb-2 text-amber-400">Current Scale</div>
        <div className="space-y-1 text-[10px] sm:text-xs">
          <div className="flex justify-between">
            <span className="text-slate-400">Domain:</span>
            <span className="font-mono capitalize">{currentScale.domain}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Scale:</span>
            <span className="font-mono text-[9px] sm:text-xs">{currentScale.name}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Size:</span>
            <span className="font-mono">{currentScale.meters.toExponential(1)} m</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">log₁₀:</span>
            <span className="font-mono">{currentScale.log10.toFixed(1)}</span>
          </div>
          {currentScale.kValue && (
            <div className="flex justify-between">
              <span className="text-slate-400">k-value:</span>
              <span className="font-mono text-[9px] sm:text-xs">{currentScale.kValue.toExponential(1)}</span>
            </div>
          )}
          <div className="mt-2 pt-2 border-t border-slate-600 text-slate-300 text-[10px] sm:text-xs leading-tight">
            {currentScale.keyConcept}
          </div>
        </div>
      </div>

      {/* Controls - Mobile Responsive */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-black/70 backdrop-blur-sm text-white p-2 sm:p-3 rounded-lg flex gap-1 sm:gap-2">
        <button
          onClick={handlePlayPause}
          className="px-3 sm:px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded transition-colors btn-focus text-sm"
          aria-label={isPaused ? 'Resume narration' : 'Pause narration'}
        >
          {isPaused ? '▶ Play' : '⏸ Pause'}
        </button>
        {scaleManagerRef.current && (
          <>
            <button
              onClick={() => scaleManagerRef.current?.transitionToPrevious(3000)}
              className="px-2 sm:px-3 py-2 bg-slate-600 hover:bg-slate-700 rounded transition-colors btn-focus text-xs sm:text-sm"
              aria-label="Go to previous scale"
            >
              ← Prev
            </button>
            <button
              onClick={() => scaleManagerRef.current?.transitionToNext(3000)}
              className="px-2 sm:px-3 py-2 bg-slate-600 hover:bg-slate-700 rounded transition-colors btn-focus text-xs sm:text-sm"
              aria-label="Go to next scale"
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
                className="px-6 py-3 bg-amber-600 hover:bg-amber-700 rounded-lg transition-colors font-semibold btn-focus"
                aria-label="Explore this scale in detail"
              >
                Explore
              </button>
              <button
                onClick={handleContinue}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors font-semibold btn-focus"
                aria-label="Continue to the next scale"
              >
                Continue Journey
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Scale Progress Indicator */}
      {/* FIX #3: Use currentScaleIndex instead of object comparison */}
      <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm text-white p-3 rounded-lg text-xs">
        <div className="font-semibold mb-2">Scale Progress</div>
        <div className="w-64 h-2 bg-slate-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-blue-500 to-amber-500 transition-all duration-300"
            style={{
              width: `${((currentScaleIndex + 1) / SCALE_POINTS.length) * 100}%`,
            }}
          />
        </div>
        <div className="mt-2 text-slate-400">
          {currentScaleIndex + 1} / {SCALE_POINTS.length} scales
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
      {/* FIX #5: Add null check instead of non-null assertion */}
      {showForceHierarchy && sceneRef.current && (
        <ForceHierarchyVisualization
          scene={sceneRef.current}
          show={showForceHierarchy}
          highlightForce={
            currentScale.domain === 'atomic' ? 'coulomb' :
            currentScale.domain === 'macroscopic' ? 'gravity' :
            'all'
          }
        />
      )}

      {/* Scale Transition Effects */}
      {/* FIX #5: Add null check instead of non-null assertion */}
      {previousScale && sceneRef.current && (
        <ScaleTransitionEffectsComponent
          scene={sceneRef.current}
          fromScale={previousScale}
          toScale={currentScale}
          progress={transitionProgress}
        />
      )}

      {/* Expandable Content Panel */}
      <div className="absolute top-20 right-4 bg-black/70 backdrop-blur-sm text-white p-4 rounded-lg max-w-sm max-h-96 overflow-y-auto z-10">
        <button
          onClick={() => setShowExpandableContent(!showExpandableContent)}
          className="w-full text-left mb-2 text-amber-400 font-semibold hover:text-amber-300 transition-colors focus-ring"
          aria-expanded={showExpandableContent}
          aria-controls="expandable-content"
          aria-label={showExpandableContent ? 'Hide detailed information' : 'Show detailed information'}
        >
          {showExpandableContent ? '▼ Hide Details' : '▶ Learn More'}
        </button>
        {showExpandableContent && (
          <div id="expandable-content">
            {getExpandableContent()}
          </div>
        )}
      </div>

      {/* Start Narration Button */}
      {!isPlaying && (
        <button
          onClick={handleStartNarration}
          className="absolute top-20 left-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors font-semibold btn-focus"
          aria-label="Start the narrated explanation of the current scale"
        >
          ▶ Start Narration
        </button>
      )}

      {/* First-Time User Tutorial */}
      {showTutorial && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/80 backdrop-blur-sm z-50 p-4">
          <div className="max-w-md w-full bg-slate-800/95 backdrop-blur-sm rounded-xl p-6 border border-slate-700 text-center text-white">
            <h2 className="text-xl font-semibold mb-4 text-amber-400">
              Welcome to Spatial Displacement Theory
            </h2>
            <div className="space-y-3 text-sm text-slate-300 mb-6">
              <p>
                You're about to journey through 43 orders of magnitude, from Planck scale to the observable universe.
              </p>
              <div className="bg-slate-700/50 rounded-lg p-3 text-left">
                <p className="font-semibold text-amber-300 mb-2">How to explore:</p>
                <ul className="space-y-1 text-xs">
                  <li>• <strong>Desktop:</strong> Click rings to navigate paths</li>
                  <li>• <strong>Mobile:</strong> Touch rings or use pinch gestures</li>
                  <li>• <strong>Keyboard:</strong> Tab/Enter to navigate, Space to play/pause</li>
                  <li>• <strong>Learn More:</strong> Click expandable sections for details</li>
                </ul>
              </div>
            </div>
            <button
              onClick={() => {
                setShowTutorial(false);
                localStorage.setItem('sdt-tutorial-seen', 'true');
              }}
              className="w-full px-6 py-3 bg-amber-600 hover:bg-amber-700 rounded-lg transition-colors font-semibold btn-focus"
              aria-label="Start the journey"
            >
              Begin Journey
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

// Default export for compatibility with existing imports
export default WalkthroughApp;
