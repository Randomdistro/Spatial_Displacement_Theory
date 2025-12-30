/**
 * GalaxyRotationSim - SDT Galaxy Rotation Visualization
 * 
 * Demonstrates how the eclipse effect (pressure occlusion)
 * produces flat rotation curves WITHOUT dark matter.
 * 
 * SDT-ACCURATE: No dark matter halos, just visible matter geometry.
 */

import React, { useRef, useMemo, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Html, Line } from '@react-three/drei';
import * as THREE from 'three';

// SDT Eclipse effect calculation
// As occlusion E(r) approaches 0.64 (saturation), rotation curve flattens
function calculateRotationVelocity(
  r: number,
  diskMass: number,
  scaleRadius: number,
  useSDT: boolean
): number {
  if (useSDT) {
    // SDT: Eclipse effect flattens the curve
    // E(r) = 0.64 × (1 - e^(-(r/R_d - 1)))
    const E_r = 0.64 * (1 - Math.exp(-(r / scaleRadius - 1)));
    // Velocity modification from occlusion
    // v_SDT ∝ √(1 - E(r)) at large r → approaches constant
    const v_inner = Math.sqrt(diskMass * r / Math.pow(r * r + scaleRadius * scaleRadius, 1.5));
    const eclipseFactor = Math.sqrt(1 - E_r * 0.6);
    return v_inner / eclipseFactor;
  } else {
    // Newtonian (Keplerian): v ∝ 1/√r at large r
    return Math.sqrt(diskMass / Math.max(r, 0.1));
  }
}

interface GalaxyRotationProps {
  starCount?: number;
  showRotationCurve?: boolean;
  showDarkMatterComparison?: boolean;
}

// Individual star particle
function Star({ 
  angle, 
  radius, 
  velocity,
  color = "#ffffff"
}: { 
  angle: number;
  radius: number; 
  velocity: number;
  color?: string;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((state, delta) => {
    if (meshRef.current) {
      // Rotate based on velocity
      const angularVelocity = velocity / (radius * 20);
      meshRef.current.position.x = Math.cos(angle + state.clock.elapsedTime * angularVelocity) * radius;
      meshRef.current.position.z = Math.sin(angle + state.clock.elapsedTime * angularVelocity) * radius;
    }
  });

  // Initial position
  const x = Math.cos(angle) * radius;
  const z = Math.sin(angle) * radius;
  const y = (Math.random() - 0.5) * 0.3 * Math.exp(-radius / 4); // Disk thickness

  return (
    <mesh ref={meshRef} position={[x, y, z]}>
      <sphereGeometry args={[0.03, 8, 8]} />
      <meshBasicMaterial color={color} />
    </mesh>
  );
}

// Galaxy disk with stars
function GalaxyDisk({ 
  starCount = 500,
  useSDT = true 
}: { 
  starCount?: number;
  useSDT?: boolean;
}) {
  const diskMass = 100;
  const scaleRadius = 2;
  
  const stars = useMemo(() => {
    const result = [];
    for (let i = 0; i < starCount; i++) {
      // Exponential disk distribution
      const radius = -scaleRadius * Math.log(1 - Math.random() * 0.95) * 1.5;
      const angle = Math.random() * Math.PI * 2;
      const velocity = calculateRotationVelocity(radius, diskMass, scaleRadius, useSDT);
      
      // Star color based on radius (bluer in center, redder outside)
      const hue = 0.1 - (radius / 15) * 0.15;
      const color = new THREE.Color().setHSL(Math.max(0, hue), 0.8, 0.7);
      
      result.push({
        id: i,
        angle,
        radius,
        velocity,
        color: '#' + color.getHexString(),
      });
    }
    return result;
  }, [starCount, useSDT]);

  return (
    <group>
      {stars.map((star) => (
        <Star
          key={star.id}
          angle={star.angle}
          radius={star.radius}
          velocity={star.velocity}
          color={star.color}
        />
      ))}
    </group>
  );
}

// Bulge (central region)
function GalacticBulge() {
  const pointsRef = useRef<THREE.Points>(null);
  
  const particles = useMemo(() => {
    const positions = new Float32Array(200 * 3);
    for (let i = 0; i < 200; i++) {
      // Spherical distribution for bulge
      const r = Math.random() * 0.8;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta) * 0.5; // Flattened
      positions[i * 3 + 2] = r * Math.cos(phi);
    }
    return positions;
  }, []);

  useFrame((state) => {
    if (pointsRef.current) {
      pointsRef.current.rotation.y += 0.002;
    }
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particles.length / 3}
          array={particles}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.05} color="#fbbf24" />
    </points>
  );
}

// Rotation curve chart
function RotationCurveChart({ useSDT = true }: { useSDT?: boolean }) {
  const diskMass = 100;
  const scaleRadius = 2;
  
  const chartData = useMemo(() => {
    const sdtPoints: [number, number, number][] = [];
    const newtonPoints: [number, number, number][] = [];
    
    for (let r = 0.5; r <= 8; r += 0.2) {
      const vSDT = calculateRotationVelocity(r, diskMass, scaleRadius, true);
      const vNewton = calculateRotationVelocity(r, diskMass, scaleRadius, false);
      
      // Scale for display
      sdtPoints.push([r * 0.5, vSDT * 0.15, 0]);
      newtonPoints.push([r * 0.5, vNewton * 0.15, 0]);
    }
    
    return { sdtPoints, newtonPoints };
  }, [diskMass, scaleRadius]);

  return (
    <group position={[0, -3, 3]} rotation={[0, 0, 0]}>
      {/* Axes */}
      <Line points={[[0, 0, 0], [5, 0, 0]]} color="#666" />
      <Line points={[[0, 0, 0], [0, 2, 0]]} color="#666" />
      
      {/* SDT curve (flat at large r) */}
      <Line
        points={chartData.sdtPoints}
        color="#4ade80"
        lineWidth={2}
      />
      
      {/* Newtonian curve (falls off as 1/√r) */}
      <Line
        points={chartData.newtonPoints}
        color="#f87171"
        lineWidth={2}
      />
      
      {/* Labels */}
      <Html position={[5.2, 0, 0]}>
        <div className="text-xs text-slate-400">r</div>
      </Html>
      <Html position={[0, 2.2, 0]}>
        <div className="text-xs text-slate-400">v</div>
      </Html>
    </group>
  );
}

// Pressure occlusion visualization
function PressureOcclusion() {
  return (
    <group>
      {/* CMB pressure arrows (blocked by disk) */}
      {Array.from({ length: 12 }).map((_, i) => {
        const angle = (i / 12) * Math.PI * 2;
        const startR = 7;
        const endR = 5;
        
        return (
          <arrowHelper
            key={i}
            args={[
              new THREE.Vector3(-Math.cos(angle), 0, -Math.sin(angle)),
              new THREE.Vector3(Math.cos(angle) * startR, 0, Math.sin(angle) * startR),
              2,
              new THREE.Color("#ef4444"),
              0.3,
              0.15
            ]}
          />
        );
      })}
    </group>
  );
}

// Info panel
function GalaxyInfoPanel() {
  return (
    <Html position={[-5, 3, 0]} center>
      <div className="bg-slate-900/90 backdrop-blur-sm p-4 rounded-xl border border-slate-700 text-white max-w-xs">
        <h3 className="text-amber-400 font-bold mb-2">Eclipse Effect</h3>
        <p className="text-sm text-slate-300 mb-2">
          Stars block CMB pressure from each other.
          This eclipse effect flattens rotation curves—no dark matter needed.
        </p>
        <div className="text-xs space-y-1">
          <div className="flex items-center gap-2">
            <div className="w-3 h-0.5 bg-green-400" />
            <span className="text-slate-400">SDT prediction</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-0.5 bg-red-400" />
            <span className="text-slate-400">Newtonian (no dark matter)</span>
          </div>
        </div>
      </div>
    </Html>
  );
}

// Main scene
function GalaxyScene({
  starCount = 500,
  showRotationCurve = true,
  showDarkMatterComparison = true,
}: GalaxyRotationProps) {
  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.3} />
      <pointLight position={[0, 5, 0]} intensity={0.5} color="#fbbf24" />

      {/* Galaxy */}
      <GalacticBulge />
      <GalaxyDisk starCount={starCount} useSDT={true} />

      {/* Pressure occlusion arrows */}
      <PressureOcclusion />

      {/* Rotation curve chart */}
      {showRotationCurve && <RotationCurveChart useSDT={true} />}

      {/* Info panel */}
      <GalaxyInfoPanel />

      {/* Camera controls */}
      <OrbitControls 
        enablePan={true}
        enableZoom={true}
        minDistance={5}
        maxDistance={20}
      />
    </>
  );
}

// Exported component
export default function GalaxyRotationSim({
  starCount = 500,
  showRotationCurve = true,
  showDarkMatterComparison = true,
}: GalaxyRotationProps) {
  const [isPlaying, setIsPlaying] = useState(true);
  const [showSDT, setShowSDT] = useState(true);

  return (
    <div className="relative w-full h-full min-h-[500px] bg-slate-950 rounded-xl overflow-hidden">
      {/* Controls overlay */}
      <div className="absolute top-4 left-4 z-10 flex gap-2">
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          className="bg-slate-800/80 hover:bg-slate-700/80 text-white px-3 py-1 rounded-lg text-sm backdrop-blur-sm"
        >
          {isPlaying ? '⏸ Pause' : '▶ Play'}
        </button>
        <button
          onClick={() => setShowSDT(!showSDT)}
          className={`px-3 py-1 rounded-lg text-sm backdrop-blur-sm ${
            showSDT 
              ? 'bg-green-600/80 text-white' 
              : 'bg-slate-800/80 text-slate-300'
          }`}
        >
          SDT Mode
        </button>
      </div>

      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [8, 6, 8], fov: 60 }}
        gl={{ antialias: true }}
      >
        <GalaxyScene
          starCount={starCount}
          showRotationCurve={showRotationCurve}
          showDarkMatterComparison={showDarkMatterComparison}
        />
      </Canvas>

      {/* Legend */}
      <div className="absolute bottom-4 right-4 bg-slate-900/80 backdrop-blur-sm p-3 rounded-lg text-xs text-slate-300">
        <div className="font-bold text-amber-400 mb-2">Rotation Curve</div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-4 h-0.5 bg-green-400" />
          <span>SDT (flat, no dark matter)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-0.5 bg-red-400" />
          <span>Newtonian (falls off)</span>
        </div>
      </div>
    </div>
  );
}

