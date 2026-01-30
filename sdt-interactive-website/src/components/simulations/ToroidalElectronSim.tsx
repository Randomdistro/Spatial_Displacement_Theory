/**
 * ToroidalElectronSim - SDT Electron Model Visualization
 * 
 * Demonstrates the electron as a toroidal vortex in the spation medium,
 * with helical standing waves giving rise to spin and quantization.
 * 
 * SDT-ACCURATE: Electron has physical extent, not a point particle.
 */

import React, { useRef, useMemo, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Html, Line } from '@react-three/drei';
import * as THREE from 'three';

// SDT Constants
const FINE_STRUCTURE = 1 / 137.036; // α - emerges from geometry
const BOHR_RADIUS_SCALE = 5; // Visual scale for Bohr radius (a₀)

interface ToroidalElectronProps {
  showHelicalWave?: boolean;
  showOrbital?: boolean;
  showProton?: boolean;
  animationSpeed?: number;
}

// Generate points along a torus
function torusPoints(
  majorRadius: number,
  minorRadius: number,
  segments: number,
  tubeSegments: number
): THREE.Vector3[] {
  const points: THREE.Vector3[] = [];
  
  for (let i = 0; i <= segments; i++) {
    const u = (i / segments) * Math.PI * 2;
    for (let j = 0; j <= tubeSegments; j++) {
      const v = (j / tubeSegments) * Math.PI * 2;
      const x = (majorRadius + minorRadius * Math.cos(v)) * Math.cos(u);
      const y = (majorRadius + minorRadius * Math.cos(v)) * Math.sin(u);
      const z = minorRadius * Math.sin(v);
      points.push(new THREE.Vector3(x, z, y));
    }
  }
  
  return points;
}

// Generate helical wave on torus surface
function helicalWavePoints(
  majorRadius: number,
  minorRadius: number,
  turns: number,
  pointCount: number
): THREE.Vector3[] {
  const points: THREE.Vector3[] = [];
  
  for (let i = 0; i <= pointCount; i++) {
    const t = (i / pointCount) * Math.PI * 2 * turns;
    const u = t; // Position around the torus
    const v = t * (turns / (turns + 1)); // Helical wrapping
    
    // Slight offset from torus surface for visibility
    const offset = 1.1;
    const x = (majorRadius + minorRadius * offset * Math.cos(v)) * Math.cos(u);
    const y = (majorRadius + minorRadius * offset * Math.cos(v)) * Math.sin(u);
    const z = minorRadius * offset * Math.sin(v);
    
    points.push(new THREE.Vector3(x, z, y));
  }
  
  return points;
}

// Electron torus visualization
function ElectronTorus({ 
  position = [0, 0, 0] as [number, number, number],
  showHelicalWave = true,
  animationSpeed = 1
}: {
  position?: [number, number, number];
  showHelicalWave?: boolean;
  animationSpeed?: number;
}) {
  const groupRef = useRef<THREE.Group>(null);
  const helixRef = useRef<THREE.Line>(null);
  
  const majorRadius = 0.5;
  const minorRadius = 0.15;
  
  // Helical wave points
  const helixPoints = useMemo(() => 
    helicalWavePoints(majorRadius, minorRadius, 4, 200),
    [majorRadius, minorRadius]
  );
  
  useFrame((state) => {
    if (groupRef.current) {
      // Rotate the electron (spin!)
      groupRef.current.rotation.y += 0.01 * animationSpeed;
    }
  });

  return (
    <group ref={groupRef} position={position}>
      {/* Torus body */}
      <mesh>
        <torusGeometry args={[majorRadius, minorRadius, 32, 100]} />
        <meshStandardMaterial
          color="#60a5fa"
          emissive="#3b82f6"
          emissiveIntensity={0.4}
          metalness={0.6}
          roughness={0.3}
          transparent
          opacity={0.8}
        />
      </mesh>
      
      {/* Helical standing wave */}
      {showHelicalWave && (
        <Line
          points={helixPoints}
          color="#fbbf24"
          lineWidth={2}
        />
      )}
      
      {/* Inner glow */}
      <mesh>
        <torusGeometry args={[majorRadius, minorRadius * 0.8, 16, 50]} />
        <meshBasicMaterial
          color="#93c5fd"
          transparent
          opacity={0.3}
        />
      </mesh>
    </group>
  );
}

// Proton (6π trefoil torus - simplified representation)
function ProtonTrefoil({ 
  position = [0, 0, 0] as [number, number, number] 
}: {
  position?: [number, number, number];
}) {
  const groupRef = useRef<THREE.Group>(null);
  
  // Simplified trefoil visualization using overlapping tori
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += 0.005;
      groupRef.current.rotation.x += 0.003;
    }
  });

  return (
    <group ref={groupRef} position={position}>
      {/* Core proton - larger than electron */}
      <mesh>
        <torusGeometry args={[0.08, 0.025, 16, 50]} />
        <meshStandardMaterial
          color="#ef4444"
          emissive="#dc2626"
          emissiveIntensity={0.5}
          metalness={0.7}
          roughness={0.3}
        />
      </mesh>
      
      {/* Second torus at angle (trefoil effect) */}
      <mesh rotation={[Math.PI / 3, 0, Math.PI / 6]}>
        <torusGeometry args={[0.08, 0.025, 16, 50]} />
        <meshStandardMaterial
          color="#f87171"
          emissive="#dc2626"
          emissiveIntensity={0.3}
          metalness={0.7}
          roughness={0.3}
        />
      </mesh>
      
      {/* Third torus */}
      <mesh rotation={[-Math.PI / 3, 0, -Math.PI / 6]}>
        <torusGeometry args={[0.08, 0.025, 16, 50]} />
        <meshStandardMaterial
          color="#fca5a5"
          emissive="#dc2626"
          emissiveIntensity={0.2}
          metalness={0.7}
          roughness={0.3}
        />
      </mesh>
      
      {/* Label */}
      <Text
        position={[0, 0.2, 0]}
        fontSize={0.08}
        color="white"
        anchorX="center"
      >
        Proton (6π trefoil)
      </Text>
    </group>
  );
}

// Electron orbital path
function ElectronOrbit({ 
  radius = BOHR_RADIUS_SCALE,
  showVelocity = true 
}: {
  radius?: number;
  showVelocity?: boolean;
}) {
  const orbitRef = useRef<THREE.Mesh>(null);
  
  return (
    <group>
      {/* Orbital path */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[radius, 0.02, 16, 100]} />
        <meshBasicMaterial
          color="#4ade80"
          transparent
          opacity={0.5}
        />
      </mesh>
      
      {/* Velocity indicator */}
      {showVelocity && (
        <Html position={[radius + 0.5, 0, 0]} center>
          <div className="bg-slate-900/80 p-2 rounded text-xs text-white whitespace-nowrap">
            v = cα ≈ 1.84c
          </div>
        </Html>
      )}
    </group>
  );
}

// Info panel
function AtomInfoPanel() {
  return (
    <Html position={[-4, 2.5, 0]} center>
      <div className="bg-slate-900/90 backdrop-blur-sm p-4 rounded-xl border border-slate-700 text-white max-w-xs">
        <h3 className="text-amber-400 font-bold mb-2">SDT Atomic Model</h3>
        <p className="text-sm text-slate-300 mb-2">
          The electron is a toroidal vortex with helical standing waves.
          The proton is a 6π trefoil torus.
        </p>
        <div className="text-xs text-slate-400 space-y-1">
          <div>• Electron size: ~10⁻²² m</div>
          <div>• Proton size: 0.84 fm</div>
          <div>• k = 137.036 = 1/α</div>
        </div>
      </div>
    </Html>
  );
}

// Main scene
function ToroidalElectronScene({
  showHelicalWave = true,
  showOrbital = true,
  showProton = true,
  animationSpeed = 1,
}: ToroidalElectronProps) {
  const electronRef = useRef<THREE.Group>(null);
  const [electronAngle, setElectronAngle] = useState(0);
  
  useFrame((state) => {
    // Orbit the electron around the proton
    const newAngle = state.clock.elapsedTime * 0.5 * animationSpeed;
    setElectronAngle(newAngle);
    
    if (electronRef.current) {
      electronRef.current.position.x = Math.cos(newAngle) * BOHR_RADIUS_SCALE;
      electronRef.current.position.z = Math.sin(newAngle) * BOHR_RADIUS_SCALE;
    }
  });

  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.4} />
      <pointLight position={[5, 5, 5]} intensity={0.8} />
      <pointLight position={[-5, -5, -5]} intensity={0.3} color="#60a5fa" />

      {/* Proton at center */}
      {showProton && <ProtonTrefoil position={[0, 0, 0]} />}

      {/* Electron on orbit */}
      <group ref={electronRef}>
        <ElectronTorus 
          showHelicalWave={showHelicalWave}
          animationSpeed={animationSpeed}
        />
        <Text
          position={[0, 0.8, 0]}
          fontSize={0.12}
          color="white"
          anchorX="center"
        >
          Electron (toroidal vortex)
        </Text>
      </group>

      {/* Orbital path */}
      {showOrbital && <ElectronOrbit radius={BOHR_RADIUS_SCALE} />}

      {/* Info panel */}
      <AtomInfoPanel />

      {/* Camera controls */}
      <OrbitControls 
        enablePan={true}
        enableZoom={true}
        minDistance={3}
        maxDistance={15}
      />
    </>
  );
}

// Exported component
export default function ToroidalElectronSim({
  showHelicalWave = true,
  showOrbital = true,
  showProton = true,
  animationSpeed = 1,
}: ToroidalElectronProps) {
  const [isPlaying, setIsPlaying] = useState(true);

  return (
    <div className="relative w-full h-full min-h-[400px] bg-slate-950 rounded-xl overflow-hidden">
      {/* Controls overlay */}
      <div className="absolute top-4 left-4 z-10 flex gap-2">
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          className="bg-slate-800/80 hover:bg-slate-700/80 text-white px-3 py-1 rounded-lg text-sm backdrop-blur-sm"
        >
          {isPlaying ? '⏸ Pause' : '▶ Play'}
        </button>
      </div>

      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [6, 4, 6], fov: 60 }}
        gl={{ antialias: true }}
      >
        <ToroidalElectronScene
          showHelicalWave={showHelicalWave}
          showOrbital={showOrbital}
          showProton={showProton}
          animationSpeed={isPlaying ? animationSpeed : 0}
        />
      </Canvas>

      {/* Legend */}
      <div className="absolute bottom-4 right-4 bg-slate-900/80 backdrop-blur-sm p-3 rounded-lg text-xs text-slate-300">
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-3 rounded-full bg-blue-400" />
          <span>Electron (torus)</span>
        </div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-3 rounded-full bg-red-400" />
          <span>Proton (trefoil)</span>
        </div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-0.5 bg-amber-400" />
          <span>Helical wave</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full border border-green-400" />
          <span>Bohr orbit (a₀)</span>
        </div>
      </div>
    </div>
  );
}


