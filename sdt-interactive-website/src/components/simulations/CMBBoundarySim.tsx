/**
 * CMBBoundarySim - CMB as Source of All Pressure
 * 
 * Visualizes the Cosmic Microwave Background as the origin
 * of all pressure in the universe:
 * - CMB boundary at z=1089, r=4.4×10^26 m
 * - Pressure volume counting (z×k²=1 shells)
 * - BAO features
 * - Inward pressure flow
 * 
 * SDT-ACCURATE: CMB is the structural boundary, not just radiation.
 */

import React, { useRef, useMemo, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Html, Sphere, Line } from '@react-three/drei';
import * as THREE from 'three';

// SDT Constants
const CMB_REDSHIFT = 1089; // z at last scattering
const CMB_RADIUS = 4.4e26; // meters (comoving)
const P_CMB = 2.036e-2; // CMB pressure (Pa)
const BAO_SCALE = 150e6; // BAO scale in light-years

// Scale levels for visualization
const COSMIC_SCALES = [
  { name: 'Solar System', radius: 1e13, label: '100 AU' },
  { name: 'Local Bubble', radius: 3e18, label: '300 ly' },
  { name: 'Milky Way', radius: 1e21, label: '100,000 ly' },
  { name: 'Local Group', radius: 3e22, label: '3 Mly' },
  { name: 'Observable Universe', radius: 4.4e26, label: '46 Bly' },
];

interface CMBBoundaryProps {
  showPressureFlow?: boolean;
  showBAO?: boolean;
  showZKShells?: boolean;
  animationSpeed?: number;
}

// CMB boundary sphere with pulsing effect
function CMBSphere({
  radius = 5,
  showPressure = true,
}: {
  radius?: number;
  showPressure?: boolean;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.0003;
      meshRef.current.rotation.x += 0.0001;
    }
    if (glowRef.current) {
      const pulse = 1 + Math.sin(state.clock.elapsedTime * 0.5) * 0.02;
      glowRef.current.scale.setScalar(pulse);
    }
  });

  return (
    <group>
      {/* Outer glow */}
      <mesh ref={glowRef} scale={1.05}>
        <sphereGeometry args={[radius, 64, 64]} />
        <meshBasicMaterial
          color="#ef4444"
          transparent
          opacity={0.05}
          side={THREE.BackSide}
        />
      </mesh>
      
      {/* CMB surface */}
      <mesh ref={meshRef}>
        <sphereGeometry args={[radius, 64, 64]} />
        <meshStandardMaterial
          color="#ef4444"
          emissive="#ef4444"
          emissiveIntensity={0.2}
          wireframe
          transparent
          opacity={0.3}
        />
      </mesh>
      
      {/* Surface features (anisotropies) */}
      <CMBAnisotropies radius={radius} />
    </group>
  );
}

// CMB temperature anisotropies (spots)
function CMBAnisotropies({ radius }: { radius: number }) {
  const spots = useMemo(() => {
    const result: { position: THREE.Vector3; size: number; isHot: boolean }[] = [];
    
    // Generate random anisotropies
    for (let i = 0; i < 50; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      
      const position = new THREE.Vector3(
        Math.sin(phi) * Math.cos(theta) * radius,
        Math.cos(phi) * radius,
        Math.sin(phi) * Math.sin(theta) * radius
      );
      
      result.push({
        position,
        size: 0.1 + Math.random() * 0.2,
        isHot: Math.random() > 0.5,
      });
    }
    
    return result;
  }, [radius]);

  return (
    <group>
      {spots.map((spot, i) => (
        <mesh key={i} position={spot.position.toArray()}>
          <sphereGeometry args={[spot.size, 16, 16]} />
          <meshBasicMaterial
            color={spot.isHot ? '#fbbf24' : '#3b82f6'}
            transparent
            opacity={0.4}
          />
        </mesh>
      ))}
    </group>
  );
}

// Pressure flow arrows from CMB toward center
function PressureFlowArrows({
  cmbRadius = 5,
  arrowCount = 24,
  showAnimation = true,
}: {
  cmbRadius?: number;
  arrowCount?: number;
  showAnimation?: boolean;
}) {
  const groupRef = useRef<THREE.Group>(null);
  
  const arrows = useMemo(() => {
    const result: { 
      start: THREE.Vector3; 
      direction: THREE.Vector3;
      phase: number;
    }[] = [];
    
    // Create arrows from multiple directions on CMB surface
    const rings = 4;
    const perRing = Math.floor(arrowCount / rings);
    
    for (let ring = 0; ring < rings; ring++) {
      const phi = ((ring + 0.5) / rings) * Math.PI;
      for (let i = 0; i < perRing; i++) {
        const theta = (i / perRing) * Math.PI * 2;
        
        const start = new THREE.Vector3(
          Math.sin(phi) * Math.cos(theta) * cmbRadius,
          Math.cos(phi) * cmbRadius,
          Math.sin(phi) * Math.sin(theta) * cmbRadius
        );
        
        const direction = start.clone().normalize().negate();
        
        result.push({
          start,
          direction,
          phase: Math.random() * Math.PI * 2,
        });
      }
    }
    
    return result;
  }, [cmbRadius, arrowCount]);

  useFrame((state) => {
    if (groupRef.current && showAnimation) {
      groupRef.current.children.forEach((child, i) => {
        if (child instanceof THREE.ArrowHelper) {
          const arrow = arrows[i];
          if (!arrow) return;
          
          // Animate arrows flowing inward
          const t = (state.clock.elapsedTime * 0.5 + arrow.phase) % 1;
          const currentPos = arrow.start.clone().lerp(
            new THREE.Vector3(0, 0, 0),
            t * 0.6
          );
          child.position.copy(currentPos);
          
          // Fade based on distance from CMB
          const distance = currentPos.length();
          const opacity = distance / cmbRadius;
          (child as any).setColor?.(new THREE.Color().setHSL(0, 0.8, opacity * 0.5));
        }
      });
    }
  });

  return (
    <group ref={groupRef}>
      {arrows.map((arrow, i) => (
        <arrowHelper
          key={i}
          args={[
            arrow.direction,
            arrow.start,
            0.6,
            new THREE.Color('#ef4444'),
            0.12,
            0.08,
          ]}
        />
      ))}
    </group>
  );
}

// BAO (Baryon Acoustic Oscillation) rings
function BAORings({ cmbRadius = 5 }: { cmbRadius?: number }) {
  const rings = useMemo(() => {
    // BAO creates characteristic scale patterns
    const baoRadii = [
      cmbRadius * 0.95,
      cmbRadius * 0.90,
      cmbRadius * 0.85,
    ];
    return baoRadii;
  }, [cmbRadius]);

  return (
    <group>
      {rings.map((radius, i) => (
        <mesh key={i} rotation={[Math.PI / 2 + i * 0.2, 0, i * 0.3]}>
          <torusGeometry args={[radius, 0.02, 16, 64]} />
          <meshBasicMaterial
            color="#fbbf24"
            transparent
            opacity={0.2 - i * 0.05}
          />
        </mesh>
      ))}
      
      <Html position={[0, cmbRadius * 0.92 + 0.5, 0]} center>
        <div className="text-xs text-amber-400/70 whitespace-nowrap">
          BAO Scale: 150 Mpc
        </div>
      </Html>
    </group>
  );
}

// z×k² = 1 pressure shells
function PressureShells({
  cmbRadius = 5,
  shellCount = 4,
}: {
  cmbRadius?: number;
  shellCount?: number;
}) {
  const shells = useMemo(() => {
    const result: { radius: number; z: number; k: number }[] = [];
    
    // z×k² = 1 defines pressure equilibrium shells
    for (let i = 1; i <= shellCount; i++) {
      const z = Math.pow(10, -i * 2);
      const k = 1 / Math.sqrt(z);
      const radius = cmbRadius * Math.pow(i / shellCount, 0.5);
      
      result.push({ radius, z, k });
    }
    
    return result;
  }, [cmbRadius, shellCount]);

  return (
    <group>
      {shells.map((shell, i) => (
        <group key={i}>
          <mesh>
            <sphereGeometry args={[shell.radius, 32, 32]} />
            <meshBasicMaterial
              color="#60a5fa"
              transparent
              opacity={0.05 + (i / shells.length) * 0.1}
              wireframe
            />
          </mesh>
          
          <Html position={[shell.radius + 0.3, 0, 0]} center>
            <div className="text-xs text-blue-400/60 whitespace-nowrap">
              z×k² = 1
            </div>
          </Html>
        </group>
      ))}
    </group>
  );
}

// Central observer (Earth/you)
function CentralObserver() {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.01;
    }
  });

  return (
    <group>
      <mesh ref={meshRef}>
        <sphereGeometry args={[0.2, 32, 32]} />
        <meshStandardMaterial
          color="#4ade80"
          emissive="#22c55e"
          emissiveIntensity={0.5}
        />
      </mesh>
      
      <Text
        position={[0, 0.4, 0]}
        fontSize={0.12}
        color="white"
        anchorX="center"
      >
        Observer
      </Text>
    </group>
  );
}

// Info panels
function CMBInfoPanel() {
  return (
    <Html position={[-4, 2.5, 0]} center>
      <div className="bg-slate-900/95 backdrop-blur-sm p-4 rounded-xl border border-slate-700 text-white w-72">
        <h3 className="text-amber-400 font-bold mb-2">CMB: Origin of All Pressure</h3>
        
        <p className="text-sm text-slate-300 mb-3">
          The Cosmic Microwave Background isn't just "leftover radiation"—it's 
          the <span className="text-amber-400 font-bold">structural boundary</span> of 
          the observable universe, producing all inward pressure.
        </p>
        
        <div className="space-y-2 text-xs">
          <div className="flex justify-between">
            <span className="text-red-400">z (redshift):</span>
            <span>1089</span>
          </div>
          <div className="flex justify-between">
            <span className="text-red-400">Distance:</span>
            <span>4.4×10²⁶ m (46 Bly)</span>
          </div>
          <div className="flex justify-between">
            <span className="text-blue-400">P_CMB:</span>
            <span>2.036×10⁻² Pa</span>
          </div>
        </div>
        
        <div className="mt-3 pt-3 border-t border-slate-700 text-xs text-slate-400">
          All forces originate from this boundary
        </div>
      </div>
    </Html>
  );
}

function ScaleInfoPanel({ currentScale }: { currentScale: number }) {
  return (
    <Html position={[4, 2.5, 0]} center>
      <div className="bg-slate-900/90 backdrop-blur-sm p-4 rounded-xl border border-slate-700 text-white w-64">
        <h4 className="text-amber-400 font-bold mb-3">Cosmic Scales</h4>
        
        <div className="space-y-2">
          {COSMIC_SCALES.map((scale, i) => {
            const isActive = i === currentScale;
            
            return (
              <div
                key={scale.name}
                className={`p-2 rounded-lg text-xs transition-all ${
                  isActive ? 'bg-white/10 border border-white/20' : ''
                }`}
              >
                <div className={`font-medium ${isActive ? 'text-white' : 'text-slate-400'}`}>
                  {scale.name}
                </div>
                <div className="text-slate-500">{scale.label}</div>
              </div>
            );
          })}
        </div>
        
        <div className="mt-3 text-xs text-slate-500 text-center">
          CMB pressure is constant at all scales
        </div>
      </div>
    </Html>
  );
}

// Main scene
function CMBBoundaryScene({
  showPressureFlow = true,
  showBAO = true,
  showZKShells = true,
  currentScale = 4,
}: {
  showPressureFlow?: boolean;
  showBAO?: boolean;
  showZKShells?: boolean;
  currentScale?: number;
}) {
  const cmbRadius = 5;
  
  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.3} />
      <pointLight position={[0, 0, 0]} intensity={0.5} color="#4ade80" />

      {/* CMB boundary */}
      <CMBSphere radius={cmbRadius} showPressure={showPressureFlow} />

      {/* Pressure flow arrows */}
      {showPressureFlow && (
        <PressureFlowArrows cmbRadius={cmbRadius} arrowCount={32} />
      )}

      {/* BAO rings */}
      {showBAO && <BAORings cmbRadius={cmbRadius} />}

      {/* z×k² = 1 shells */}
      {showZKShells && <PressureShells cmbRadius={cmbRadius} shellCount={3} />}

      {/* Central observer */}
      <CentralObserver />

      {/* Info panels */}
      <CMBInfoPanel />
      <ScaleInfoPanel currentScale={currentScale} />

      {/* Camera controls */}
      <OrbitControls
        enablePan={true}
        enableZoom={true}
        minDistance={2}
        maxDistance={10}
        autoRotate
        autoRotateSpeed={0.3}
      />
    </>
  );
}

// Exported component
export default function CMBBoundarySim({
  showPressureFlow = true,
  showBAO = true,
  showZKShells = true,
  animationSpeed = 1,
}: CMBBoundaryProps) {
  const [currentScale, setCurrentScale] = useState(4);
  const [features, setFeatures] = useState({
    pressureFlow: showPressureFlow,
    bao: showBAO,
    zkShells: showZKShells,
  });

  const toggleFeature = (feature: keyof typeof features) => {
    setFeatures((prev) => ({ ...prev, [feature]: !prev[feature] }));
  };

  return (
    <div className="relative w-full h-full min-h-[500px] bg-slate-950 rounded-xl overflow-hidden">
      {/* Feature toggles */}
      <div className="absolute top-4 left-4 z-10 flex flex-wrap gap-2">
        <button
          onClick={() => toggleFeature('pressureFlow')}
          className={`px-3 py-1.5 rounded-lg text-sm backdrop-blur-sm transition-colors ${
            features.pressureFlow
              ? 'bg-red-500/80 text-white'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700/80'
          }`}
        >
          {features.pressureFlow ? '✓' : '+'} Pressure Flow
        </button>
        <button
          onClick={() => toggleFeature('bao')}
          className={`px-3 py-1.5 rounded-lg text-sm backdrop-blur-sm transition-colors ${
            features.bao
              ? 'bg-amber-500/80 text-slate-900'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700/80'
          }`}
        >
          {features.bao ? '✓' : '+'} BAO Rings
        </button>
        <button
          onClick={() => toggleFeature('zkShells')}
          className={`px-3 py-1.5 rounded-lg text-sm backdrop-blur-sm transition-colors ${
            features.zkShells
              ? 'bg-blue-500/80 text-white'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700/80'
          }`}
        >
          {features.zkShells ? '✓' : '+'} z×k²=1 Shells
        </button>
      </div>

      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [6, 4, 6], fov: 60 }}
        gl={{ antialias: true }}
      >
        <CMBBoundaryScene
          showPressureFlow={features.pressureFlow}
          showBAO={features.bao}
          showZKShells={features.zkShells}
          currentScale={currentScale}
        />
      </Canvas>

      {/* Key insight */}
      <div className="absolute bottom-4 left-4 bg-slate-900/90 backdrop-blur-sm p-4 rounded-xl border border-slate-700 max-w-sm">
        <h4 className="text-amber-400 font-bold mb-2">The Key Insight</h4>
        <p className="text-sm text-slate-300">
          Everything in the universe—from atoms to galaxies—is held together by 
          <span className="text-red-400 font-bold"> pressure from the CMB</span>.
          There is no gravity "force"—only pressure gradients.
        </p>
      </div>

      {/* Legend */}
      <div className="absolute bottom-4 right-4 bg-slate-900/80 backdrop-blur-sm p-3 rounded-lg text-xs text-slate-300">
        <div className="font-bold text-amber-400 mb-2">CMB Boundary</div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-3 rounded-full border border-red-400" />
          <span>CMB surface (z=1089)</span>
        </div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-0.5 bg-red-400" />
          <span>Inward pressure</span>
        </div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-3 rounded-full border border-amber-400" />
          <span>BAO features</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-green-400" />
          <span>Observer (you)</span>
        </div>
      </div>
    </div>
  );
}

