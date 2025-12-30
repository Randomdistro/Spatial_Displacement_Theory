/**
 * KLawScaleSim - SDT Universal k-Law Visualization
 * 
 * Demonstrates how the same velocity law v = (c/k)√(R/r)
 * applies from atomic to galactic scales with different k values.
 * 
 * SDT-ACCURATE: One law, 53 orders of magnitude.
 */

import React, { useState, useMemo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Html, Line } from '@react-three/drei';
import * as THREE from 'three';

// Physical constants
const C_LIGHT = 2.998e8; // m/s

// Scale configurations
interface ScaleConfig {
  name: string;
  k: number;
  radius: number; // characteristic radius
  description: string;
  color: string;
  examples: string[];
  orders: number; // order of magnitude in meters
}

const SCALES: ScaleConfig[] = [
  {
    name: 'Hydrogen Atom',
    k: 137.036,
    radius: 5.29e-11, // Bohr radius
    description: 'Electron orbiting proton',
    color: '#60a5fa',
    examples: ['Electron orbital', 'Fine structure'],
    orders: -11,
  },
  {
    name: 'Heavy Atom',
    k: 137.036,
    radius: 1e-10,
    description: 'Multi-electron atoms',
    color: '#818cf8',
    examples: ['Uranium atom', 'Noble gases'],
    orders: -10,
  },
  {
    name: 'Planetary',
    k: 59000,
    radius: 1.5e11, // 1 AU
    description: 'Planets orbiting stars',
    color: '#4ade80',
    examples: ['Earth-Sun', 'Mars orbit'],
    orders: 11,
  },
  {
    name: 'Stellar',
    k: 10000,
    radius: 1e13,
    description: 'Binary star systems',
    color: '#fbbf24',
    examples: ['Alpha Centauri', 'Sirius A/B'],
    orders: 13,
  },
  {
    name: 'Galactic',
    k: 100000,
    radius: 1e21,
    description: 'Stars in galaxies',
    color: '#f87171',
    examples: ['Milky Way', 'Solar orbit'],
    orders: 21,
  },
];

interface KLawScaleProps {
  initialScale?: number;
  showVelocityCalc?: boolean;
  showComparison?: boolean;
}

// Orbiting object visualization
function OrbitingBody({
  centralRadius,
  orbitRadius,
  color,
  velocity,
  animationSpeed = 1,
}: {
  centralRadius: number;
  orbitRadius: number;
  color: string;
  velocity: number;
  animationSpeed?: number;
}) {
  const bodyRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (bodyRef.current) {
      const angle = state.clock.elapsedTime * velocity * 0.1 * animationSpeed;
      bodyRef.current.position.x = Math.cos(angle) * orbitRadius;
      bodyRef.current.position.z = Math.sin(angle) * orbitRadius;
    }
  });

  return (
    <group>
      {/* Central body */}
      <mesh>
        <sphereGeometry args={[centralRadius, 32, 32]} />
        <meshStandardMaterial
          color="#fbbf24"
          emissive="#fbbf24"
          emissiveIntensity={0.3}
        />
      </mesh>
      
      {/* Orbit path */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[orbitRadius, 0.02, 16, 100]} />
        <meshBasicMaterial color={color} transparent opacity={0.5} />
      </mesh>
      
      {/* Orbiting body */}
      <mesh ref={bodyRef} position={[orbitRadius, 0, 0]}>
        <sphereGeometry args={[centralRadius * 0.3, 16, 16]} />
        <meshStandardMaterial color={color} />
      </mesh>
    </group>
  );
}

// Scale comparison panel
function ScaleComparisonPanel({
  scales,
  currentIndex,
  onChange,
}: {
  scales: ScaleConfig[];
  currentIndex: number;
  onChange: (index: number) => void;
}) {
  return (
    <Html position={[-4.5, 3, 0]} center>
      <div className="bg-slate-900/95 backdrop-blur-sm p-4 rounded-xl border border-slate-700 text-white w-72">
        <h3 className="text-amber-400 font-bold mb-3">Universal k-Law</h3>
        <div className="text-center font-mono text-lg mb-3">
          v(r) = (c/k) √(R/r)
        </div>
        
        <div className="space-y-2">
          {scales.map((scale, index) => (
            <button
              key={scale.name}
              onClick={() => onChange(index)}
              className={`w-full text-left p-2 rounded-lg transition-all ${
                index === currentIndex
                  ? 'bg-white/10 border border-white/20'
                  : 'hover:bg-white/5'
              }`}
            >
              <div className="flex items-center gap-2">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: scale.color }}
                />
                <span className="font-medium">{scale.name}</span>
              </div>
              <div className="text-xs text-slate-400 ml-5">
                k = {scale.k.toLocaleString()}
              </div>
            </button>
          ))}
        </div>
        
        <div className="mt-4 pt-3 border-t border-slate-700 text-xs text-slate-400">
          <div className="font-medium text-white mb-1">
            {scales[currentIndex].name}
          </div>
          <div>{scales[currentIndex].description}</div>
          <div className="mt-2">
            Scale: 10<sup>{scales[currentIndex].orders}</sup> m
          </div>
        </div>
      </div>
    </Html>
  );
}

// Velocity calculation display
function VelocityCalc({ scale }: { scale: ScaleConfig }) {
  const velocity = (C_LIGHT / scale.k) * Math.sqrt(1); // At R = r
  const velocityFormatted = velocity.toExponential(2);
  
  return (
    <Html position={[4, 2.5, 0]} center>
      <div className="bg-slate-900/90 backdrop-blur-sm p-4 rounded-xl border border-slate-700 text-white max-w-xs">
        <h4 className="text-amber-400 font-bold mb-2">Calculation</h4>
        <div className="font-mono text-sm space-y-1">
          <div>c = 2.998×10⁸ m/s</div>
          <div>k = {scale.k.toLocaleString()}</div>
          <div className="pt-2 border-t border-slate-700 mt-2">
            v = c/k × √(R/r)
          </div>
          <div className="text-green-400">
            v ≈ {velocityFormatted} m/s
          </div>
        </div>
      </div>
    </Html>
  );
}

// Scale indicator (logarithmic ruler)
function ScaleIndicator({ currentOrders }: { currentOrders: number }) {
  const marks = [-15, -10, -5, 0, 5, 10, 15, 20, 25];
  
  return (
    <Html position={[0, -3.5, 0]} center>
      <div className="bg-slate-900/90 backdrop-blur-sm px-4 py-2 rounded-lg text-white">
        <div className="text-xs text-slate-400 mb-1 text-center">
          Scale (meters, log₁₀)
        </div>
        <div className="flex items-center gap-1">
          {marks.map((mark) => (
            <div key={mark} className="flex flex-col items-center">
              <div
                className={`w-1 ${
                  mark === currentOrders
                    ? 'h-4 bg-amber-400'
                    : 'h-2 bg-slate-600'
                }`}
              />
              <div
                className={`text-xs ${
                  mark === currentOrders ? 'text-amber-400' : 'text-slate-500'
                }`}
              >
                {mark}
              </div>
            </div>
          ))}
        </div>
        <div className="text-center text-xs mt-1 text-slate-400">
          ◄ Atomic ━━━━━━━━━━ Galactic ►
        </div>
      </div>
    </Html>
  );
}

// Main scene
function KLawScene({
  currentScale,
  animationSpeed = 1,
}: {
  currentScale: ScaleConfig;
  animationSpeed?: number;
}) {
  // Normalize to visual scale
  const centralRadius = 0.5;
  const orbitRadius = 2.5;
  const velocity = 1 / Math.sqrt(currentScale.k / 137); // Relative velocity
  
  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.4} />
      <pointLight position={[5, 5, 5]} intensity={0.8} />
      <pointLight position={[-5, -5, -5]} intensity={0.3} />

      {/* Orbiting system */}
      <OrbitingBody
        centralRadius={centralRadius}
        orbitRadius={orbitRadius}
        color={currentScale.color}
        velocity={velocity}
        animationSpeed={animationSpeed}
      />

      {/* Formula label */}
      <Text
        position={[0, 3.5, 0]}
        fontSize={0.3}
        color="white"
        anchorX="center"
      >
        v = (c/k) √(R/r)
      </Text>

      {/* k-value label */}
      <Text
        position={[0, -2.5, 0]}
        fontSize={0.25}
        color={currentScale.color}
        anchorX="center"
      >
        {`k = ${currentScale.k.toLocaleString()}`}
      </Text>

      {/* Camera controls */}
      <OrbitControls
        enablePan={true}
        enableZoom={true}
        minDistance={4}
        maxDistance={12}
      />
    </>
  );
}

// Exported component
export default function KLawScaleSim({
  initialScale = 0,
  showVelocityCalc = true,
  showComparison = true,
}: KLawScaleProps) {
  const [isPlaying, setIsPlaying] = useState(true);
  const [currentScaleIndex, setCurrentScaleIndex] = useState(initialScale);
  const currentScale = SCALES[currentScaleIndex];

  return (
    <div className="relative w-full h-full min-h-[500px] bg-slate-950 rounded-xl overflow-hidden">
      {/* Controls overlay */}
      <div className="absolute top-4 right-4 z-10 flex gap-2">
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          className="bg-slate-800/80 hover:bg-slate-700/80 text-white px-3 py-1 rounded-lg text-sm backdrop-blur-sm"
        >
          {isPlaying ? '⏸ Pause' : '▶ Play'}
        </button>
      </div>

      {/* Slider */}
      <div className="absolute bottom-20 left-1/2 transform -translate-x-1/2 z-10 w-80">
        <input
          type="range"
          min={0}
          max={SCALES.length - 1}
          value={currentScaleIndex}
          onChange={(e) => setCurrentScaleIndex(parseInt(e.target.value))}
          className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
        />
        <div className="flex justify-between text-xs text-slate-400 mt-1 px-1">
          <span>Atomic</span>
          <span>Planetary</span>
          <span>Galactic</span>
        </div>
      </div>

      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [5, 4, 5], fov: 60 }}
        gl={{ antialias: true }}
      >
        <KLawScene
          currentScale={currentScale}
          animationSpeed={isPlaying ? 1 : 0}
        />
        
        {/* UI overlays in 3D space */}
        <ScaleComparisonPanel
          scales={SCALES}
          currentIndex={currentScaleIndex}
          onChange={setCurrentScaleIndex}
        />
        
        {showVelocityCalc && <VelocityCalc scale={currentScale} />}
        <ScaleIndicator currentOrders={currentScale.orders} />
      </Canvas>

      {/* Current scale info */}
      <div className="absolute top-4 left-4 bg-slate-900/80 backdrop-blur-sm p-3 rounded-lg text-white">
        <div className="text-sm font-bold" style={{ color: currentScale.color }}>
          {currentScale.name}
        </div>
        <div className="text-xs text-slate-400 mt-1">
          {currentScale.description}
        </div>
      </div>
    </div>
  );
}

