/**
 * SpationLatticeSim - Fundamental Spation Medium Visualization
 * 
 * Visualizes the spation lattice at Planck scale:
 * - Dodecahedral packing structure (12-faced polyhedra)
 * - K_bulk = 4.6×10^113 Pa visualization
 * - Zoom from macroscopic to 10^-35 m
 * - Pressure deformation under load
 * 
 * SDT-ACCURATE: Spation is incompressible, inviscid superfluid.
 */

import React, { useRef, useMemo, useState, useCallback } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Text, Html, Line } from '@react-three/drei';
import * as THREE from 'three';

// SDT Constants
const K_BULK = 4.6e113; // Spation bulk modulus (Pa)
const PLANCK_LENGTH = 1.616e-35; // Planck length (m)
const C_LIGHT = 2.998e8; // Pressure propagation speed

// Scale levels for zoom
const SCALE_LEVELS = [
  { name: 'Macroscopic', scale: 1, meters: '1 m', description: 'Human scale' },
  { name: 'Microscopic', scale: 1e-6, meters: '1 μm', description: 'Cell scale' },
  { name: 'Atomic', scale: 1e-10, meters: '0.1 nm', description: 'Atomic scale' },
  { name: 'Nuclear', scale: 1e-15, meters: '1 fm', description: 'Proton radius' },
  { name: 'Substructure', scale: 1e-22, meters: '10⁻²² m', description: 'Electron vortex' },
  { name: 'Planck', scale: 1e-35, meters: '10⁻³⁵ m', description: 'Spation lattice' },
];

interface SpationLatticeProps {
  showDeformation?: boolean;
  showPressure?: boolean;
  initialZoom?: number;
}

// Generate dodecahedron vertices
function getDodecahedronVertices(radius: number = 1): THREE.Vector3[] {
  const phi = (1 + Math.sqrt(5)) / 2; // Golden ratio
  const vertices: THREE.Vector3[] = [];
  
  // 8 vertices from cube
  for (let i = -1; i <= 1; i += 2) {
    for (let j = -1; j <= 1; j += 2) {
      for (let k = -1; k <= 1; k += 2) {
        vertices.push(new THREE.Vector3(i, j, k).multiplyScalar(radius));
      }
    }
  }
  
  // 12 vertices from golden rectangles
  for (let i = -1; i <= 1; i += 2) {
    for (let j = -1; j <= 1; j += 2) {
      vertices.push(new THREE.Vector3(0, i / phi, j * phi).multiplyScalar(radius));
      vertices.push(new THREE.Vector3(i / phi, j * phi, 0).multiplyScalar(radius));
      vertices.push(new THREE.Vector3(i * phi, 0, j / phi).multiplyScalar(radius));
    }
  }
  
  return vertices;
}

// Single spation cell (dodecahedron)
function SpationCell({
  position,
  radius = 0.3,
  pressure = 1,
  deformation = 0,
  highlighted = false,
}: {
  position: [number, number, number];
  radius?: number;
  pressure?: number;
  deformation?: number;
  highlighted?: boolean;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  // Color based on pressure (blue = high, red = low)
  const color = useMemo(() => {
    const hue = 0.6 - pressure * 0.3; // Blue to cyan
    return new THREE.Color().setHSL(Math.max(0.3, hue), 0.8, 0.5 + pressure * 0.2);
  }, [pressure]);
  
  // Apply deformation
  const scale = useMemo(() => {
    const base = 1 - deformation * 0.3;
    return [base, base * (1 + deformation * 0.1), base] as [number, number, number];
  }, [deformation]);
  
  useFrame((state) => {
    if (meshRef.current) {
      // Subtle vibration at Planck scale
      const vibration = Math.sin(state.clock.elapsedTime * 20 + position[0] * 10) * 0.02;
      meshRef.current.rotation.x = vibration;
      meshRef.current.rotation.y = vibration * 0.7;
    }
  });

  return (
    <mesh ref={meshRef} position={position} scale={scale}>
      <dodecahedronGeometry args={[radius, 0]} />
      <meshStandardMaterial
        color={color}
        emissive={highlighted ? '#fbbf24' : color}
        emissiveIntensity={highlighted ? 0.5 : 0.2}
        metalness={0.4}
        roughness={0.6}
        transparent
        opacity={0.85}
        wireframe={false}
      />
    </mesh>
  );
}

// Lattice grid of spation cells
function SpationLattice({
  gridSize = 5,
  cellRadius = 0.25,
  showDeformation = false,
  deformationCenter = [0, 0, 0] as [number, number, number],
}: {
  gridSize?: number;
  cellRadius?: number;
  showDeformation?: boolean;
  deformationCenter?: [number, number, number];
}) {
  const groupRef = useRef<THREE.Group>(null);
  
  const cells = useMemo(() => {
    const result: { position: [number, number, number]; pressure: number; deformation: number }[] = [];
    const spacing = cellRadius * 2.2;
    const half = (gridSize - 1) / 2;
    
    for (let x = 0; x < gridSize; x++) {
      for (let y = 0; y < gridSize; y++) {
        for (let z = 0; z < gridSize; z++) {
          const pos: [number, number, number] = [
            (x - half) * spacing,
            (y - half) * spacing,
            (z - half) * spacing,
          ];
          
          // Calculate distance from deformation center
          const dx = pos[0] - deformationCenter[0];
          const dy = pos[1] - deformationCenter[1];
          const dz = pos[2] - deformationCenter[2];
          const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
          
          // Pressure decreases near matter (deformation center)
          const pressure = showDeformation ? Math.min(1, distance / 2) : 1;
          
          // Deformation increases near matter
          const deformation = showDeformation ? Math.max(0, 1 - distance / 1.5) : 0;
          
          result.push({ position: pos, pressure, deformation });
        }
      }
    }
    
    return result;
  }, [gridSize, cellRadius, showDeformation, deformationCenter]);
  
  useFrame((state) => {
    if (groupRef.current) {
      // Slow rotation
      groupRef.current.rotation.y += 0.001;
    }
  });

  return (
    <group ref={groupRef}>
      {cells.map((cell, i) => (
        <SpationCell
          key={i}
          position={cell.position}
          radius={cellRadius}
          pressure={cell.pressure}
          deformation={cell.deformation}
        />
      ))}
    </group>
  );
}

// Matter object creating displacement
function MatterDisplacement({
  position = [0, 0, 0] as [number, number, number],
  radius = 0.4,
}: {
  position?: [number, number, number];
  radius?: number;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      // Pulsing effect
      const pulse = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.05;
      meshRef.current.scale.setScalar(pulse);
    }
  });

  return (
    <group position={position}>
      <mesh ref={meshRef}>
        <sphereGeometry args={[radius, 32, 32]} />
        <meshStandardMaterial
          color="#fbbf24"
          emissive="#f59e0b"
          emissiveIntensity={0.5}
          metalness={0.6}
          roughness={0.3}
        />
      </mesh>
      <Text
        position={[0, radius + 0.2, 0]}
        fontSize={0.12}
        color="white"
        anchorX="center"
      >
        Matter (displacement)
      </Text>
    </group>
  );
}

// Pressure flow arrows
function PressureFlow({
  center = [0, 0, 0] as [number, number, number],
  radius = 2,
}: {
  center?: [number, number, number];
  radius?: number;
}) {
  const arrows = useMemo(() => {
    const result: { start: THREE.Vector3; end: THREE.Vector3 }[] = [];
    const count = 16;
    
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2;
      const start = new THREE.Vector3(
        Math.cos(angle) * radius,
        0,
        Math.sin(angle) * radius
      );
      const end = start.clone().multiplyScalar(0.6);
      result.push({ start, end });
    }
    
    return result;
  }, [radius]);

  return (
    <group position={center}>
      {arrows.map((arrow, i) => (
        <arrowHelper
          key={i}
          args={[
            arrow.start.clone().sub(arrow.end).normalize().negate(),
            arrow.start,
            0.4,
            new THREE.Color('#60a5fa'),
            0.1,
            0.06,
          ]}
        />
      ))}
    </group>
  );
}

// Scale indicator panel
function ScalePanel({
  currentLevel,
  onLevelChange,
}: {
  currentLevel: number;
  onLevelChange: (level: number) => void;
}) {
  return (
    <Html position={[-3.5, 2.5, 0]} center>
      <div className="bg-slate-900/95 backdrop-blur-sm p-4 rounded-xl border border-slate-700 text-white w-64">
        <h3 className="text-amber-400 font-bold mb-3">Zoom Level</h3>
        
        <input
          type="range"
          min={0}
          max={SCALE_LEVELS.length - 1}
          value={currentLevel}
          onChange={(e) => onLevelChange(parseInt(e.target.value))}
          className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer mb-3"
        />
        
        <div className="space-y-2">
          {SCALE_LEVELS.map((level, i) => (
            <button
              key={i}
              onClick={() => onLevelChange(i)}
              className={`w-full text-left p-2 rounded-lg text-xs transition-all ${
                i === currentLevel
                  ? 'bg-amber-500/20 border border-amber-500/50'
                  : 'hover:bg-white/5'
              }`}
            >
              <div className="font-medium">{level.name}</div>
              <div className="text-slate-400">{level.meters}</div>
            </button>
          ))}
        </div>
        
        <div className="mt-4 pt-3 border-t border-slate-700 text-xs text-slate-400">
          <div className="font-mono">K_bulk = 4.6×10¹¹³ Pa</div>
          <div className="mt-1">Incompressible superfluid</div>
        </div>
      </div>
    </Html>
  );
}

// Info panel
function InfoPanel({ showDeformation }: { showDeformation: boolean }) {
  return (
    <Html position={[3.5, 2.5, 0]} center>
      <div className="bg-slate-900/90 backdrop-blur-sm p-4 rounded-xl border border-slate-700 text-white max-w-xs">
        <h3 className="text-amber-400 font-bold mb-2">Spation Lattice</h3>
        <p className="text-sm text-slate-300 mb-3">
          The fundamental medium of space: an incompressible, inviscid superfluid
          with dodecahedral packing at the Planck scale.
        </p>
        
        {showDeformation && (
          <div className="bg-slate-800/50 p-2 rounded-lg text-xs">
            <div className="text-amber-400 font-bold mb-1">Deformation Mode</div>
            <p className="text-slate-400">
              Matter displaces spation, creating pressure gradients.
              This is the origin of ALL forces.
            </p>
          </div>
        )}
        
        <div className="mt-3 text-xs text-slate-400">
          <div>• No empty space</div>
          <div>• Pressure propagates at c</div>
          <div>• ∇·v = 0 (incompressible)</div>
        </div>
      </div>
    </Html>
  );
}

// Main scene
function SpationLatticeScene({
  showDeformation = false,
  showPressure = true,
  zoomLevel = 5,
}: {
  showDeformation?: boolean;
  showPressure?: boolean;
  zoomLevel?: number;
}) {
  // Adjust grid size based on zoom level
  const gridSize = zoomLevel >= 5 ? 5 : 3;
  const cellRadius = 0.25;
  
  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.5} />
      <pointLight position={[5, 5, 5]} intensity={0.8} />
      <pointLight position={[-5, -5, -5]} intensity={0.3} color="#60a5fa" />

      {/* Spation lattice */}
      <SpationLattice
        gridSize={gridSize}
        cellRadius={cellRadius}
        showDeformation={showDeformation}
        deformationCenter={[0, 0, 0]}
      />

      {/* Matter displacement (if showing deformation) */}
      {showDeformation && (
        <>
          <MatterDisplacement position={[0, 0, 0]} radius={0.35} />
          <PressureFlow center={[0, 0, 0]} radius={2} />
        </>
      )}

      {/* Camera controls */}
      <OrbitControls
        enablePan={true}
        enableZoom={true}
        minDistance={2}
        maxDistance={8}
        autoRotate={!showDeformation}
        autoRotateSpeed={0.5}
      />
    </>
  );
}

// Exported component
export default function SpationLatticeSim({
  showDeformation = false,
  showPressure = true,
  initialZoom = 5,
}: SpationLatticeProps) {
  const [isPlaying, setIsPlaying] = useState(true);
  const [zoomLevel, setZoomLevel] = useState(initialZoom);
  const [showMatter, setShowMatter] = useState(showDeformation);

  return (
    <div className="relative w-full h-full min-h-[500px] bg-slate-950 rounded-xl overflow-hidden">
      {/* Controls overlay */}
      <div className="absolute top-4 right-4 z-10 flex gap-2">
        <button
          onClick={() => setShowMatter(!showMatter)}
          className={`px-3 py-1 rounded-lg text-sm backdrop-blur-sm transition-colors ${
            showMatter
              ? 'bg-amber-500/80 text-slate-900'
              : 'bg-slate-800/80 text-white hover:bg-slate-700/80'
          }`}
        >
          {showMatter ? '✓ Deformation' : '+ Deformation'}
        </button>
      </div>

      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [4, 3, 4], fov: 60 }}
        gl={{ antialias: true }}
      >
        <SpationLatticeScene
          showDeformation={showMatter}
          showPressure={showPressure}
          zoomLevel={zoomLevel}
        />
        
        <ScalePanel currentLevel={zoomLevel} onLevelChange={setZoomLevel} />
        <InfoPanel showDeformation={showMatter} />
      </Canvas>

      {/* Scale indicator */}
      <div className="absolute bottom-4 left-4 bg-slate-900/80 backdrop-blur-sm px-4 py-2 rounded-lg">
        <div className="text-xs text-slate-400">Current Scale</div>
        <div className="text-lg font-bold text-amber-400">
          {SCALE_LEVELS[zoomLevel].meters}
        </div>
        <div className="text-xs text-slate-500">
          {SCALE_LEVELS[zoomLevel].description}
        </div>
      </div>

      {/* Legend */}
      <div className="absolute bottom-4 right-4 bg-slate-900/80 backdrop-blur-sm p-3 rounded-lg text-xs text-slate-300">
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-3 bg-blue-400 rounded" style={{ clipPath: 'polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%)' }} />
          <span>Spation cell (dodecahedron)</span>
        </div>
        {showMatter && (
          <>
            <div className="flex items-center gap-2 mb-1">
              <div className="w-3 h-3 rounded-full bg-amber-400" />
              <span>Matter (displacement)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-0.5 bg-blue-400" />
              <span>Pressure flow</span>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

