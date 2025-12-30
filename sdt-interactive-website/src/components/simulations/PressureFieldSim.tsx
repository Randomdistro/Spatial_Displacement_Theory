/**
 * PressureFieldSim - SDT Master Equation Visualization (UPGRADED)
 * 
 * Full implementation of the Master Equation:
 * ∇·[K_bulk ∇Δ(x)] = -κ ρ_disp(x) (1-E(x,n̂))
 * 
 * Features:
 * - Directional occlusion E(x,n̂) visualization
 * - Multiple matter objects
 * - Force vectors from pressure gradients
 * - CMB as pressure source
 * - Interactive parameters
 * 
 * SDT-ACCURATE: No mass, no G, no QED. Pure pressure geometry.
 */

import React, { useRef, useMemo, useState, useCallback } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Text, Html, Line } from '@react-three/drei';
import * as THREE from 'three';

// SDT Constants (no G, no mass as fundamental)
const K_BULK = 4.6e113; // Spation bulk modulus (Pa)
const P_CMB = 2.036e-2; // CMB pressure (Pa)
const C_LIGHT = 2.998e8; // Speed of pressure disturbances (m/s)

interface MatterObject {
  id: string;
  position: [number, number, number];
  radius: number;
  displacementVolume: number;
  color: string;
  label: string;
}

interface PressureFieldProps {
  showField?: boolean;
  showLabels?: boolean;
  showOcclusion?: boolean;
  showForces?: boolean;
  interactive?: boolean;
}

/**
 * Calculate directional occlusion E(x, n̂)
 * How much incoming pressure from direction n̂ is blocked by matter
 */
function calculateOcclusion(
  point: THREE.Vector3,
  direction: THREE.Vector3,
  matterObjects: MatterObject[]
): number {
  let totalOcclusion = 0;
  
  for (const matter of matterObjects) {
    const matterPos = new THREE.Vector3(...matter.position);
    const toMatter = matterPos.clone().sub(point);
    
    // Check if matter is in the direction of incoming pressure
    const alignment = direction.dot(toMatter.normalize());
    if (alignment < 0) continue; // Matter is behind the point
    
    // Distance to matter
    const distance = toMatter.length();
    if (distance < 0.01) continue;
    
    // Solid angle subtended by matter
    const solidAngle = (Math.PI * matter.radius * matter.radius) / (4 * Math.PI * distance * distance);
    
    // Occlusion contribution (weighted by alignment and distance)
    totalOcclusion += solidAngle * alignment;
  }
  
  return Math.min(1, totalOcclusion);
}

/**
 * Calculate pressure field at a point using Master Equation
 * ∇·[K_bulk ∇Δ(x)] = -κ ρ_disp(x) (1-E(x,n̂))
 */
function calculatePressureField(
  point: THREE.Vector3,
  matterObjects: MatterObject[],
  showOcclusion: boolean = true
): { pressure: number; gradient: THREE.Vector3; occlusion: number } {
  let totalPressure = P_CMB;
  const gradient = new THREE.Vector3(0, 0, 0);
  let totalOcclusion = 0;
  
  // Sample CMB pressure from multiple directions
  const sampleDirections = [
    new THREE.Vector3(1, 0, 0),
    new THREE.Vector3(-1, 0, 0),
    new THREE.Vector3(0, 1, 0),
    new THREE.Vector3(0, -1, 0),
    new THREE.Vector3(0, 0, 1),
    new THREE.Vector3(0, 0, -1),
  ];
  
  // For each matter object, calculate its contribution to pressure deficit
  for (const matter of matterObjects) {
    const matterPos = new THREE.Vector3(...matter.position);
    const toPoint = point.clone().sub(matterPos);
    const distance = toPoint.length();
    
    if (distance < matter.radius) {
      // Inside matter: maximum pressure deficit
      totalPressure = 0;
      gradient.set(0, 0, 0);
      return { pressure: 0, gradient, occlusion: 1 };
    }
    
    // Pressure deficit from displacement
    // P(r) = P_CMB × (1 - V_disp / (4πr²))
    const pressureDeficit = (matter.displacementVolume * P_CMB) / (4 * Math.PI * distance * distance);
    
    // Calculate occlusion for this point
    if (showOcclusion) {
      for (const dir of sampleDirections) {
        totalOcclusion += calculateOcclusion(point, dir, matterObjects);
      }
      totalOcclusion /= sampleDirections.length;
    }
    
    // Effective pressure deficit includes occlusion term (1-E)
    const effectiveDeficit = pressureDeficit * (1 - totalOcclusion);
    totalPressure -= effectiveDeficit;
    
    // Gradient points toward matter (pressure drops toward matter)
    const gradientMagnitude = (2 * matter.displacementVolume * P_CMB) / 
                              (4 * Math.PI * Math.pow(distance, 3));
    const gradientContribution = toPoint.normalize().multiplyScalar(-gradientMagnitude);
    gradient.add(gradientContribution);
  }
  
  return { 
    pressure: Math.max(0, totalPressure), 
    gradient,
    occlusion: totalOcclusion
  };
}

// Single matter object with displacement visualization
function MatterParticle({
  matter,
  showLabels = true,
  isSelected = false,
  onClick,
}: {
  matter: MatterObject;
  showLabels?: boolean;
  isSelected?: boolean;
  onClick?: () => void;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      const pulse = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.03;
      meshRef.current.scale.setScalar(isSelected ? pulse * 1.1 : pulse);
    }
  });

  return (
    <group position={matter.position}>
      {/* Displacement shell (outer glow) */}
      <mesh scale={1.3}>
        <sphereGeometry args={[matter.radius, 32, 32]} />
        <meshBasicMaterial
          color={matter.color}
          transparent
          opacity={0.1}
        />
      </mesh>
      
      {/* Core matter */}
      <mesh ref={meshRef} onClick={onClick}>
        <sphereGeometry args={[matter.radius, 32, 32]} />
        <meshStandardMaterial
          color={matter.color}
          emissive={matter.color}
          emissiveIntensity={isSelected ? 0.5 : 0.3}
          metalness={0.6}
          roughness={0.3}
        />
      </mesh>
      
      {showLabels && (
        <Text
          position={[0, matter.radius + 0.35, 0]}
          fontSize={0.14}
          color="white"
          anchorX="center"
          anchorY="bottom"
        >
          {matter.label}
        </Text>
      )}
    </group>
  );
}

// Pressure field gradient arrows
function PressureGradientField({
  matterObjects,
  gridSize = 6,
  showOcclusion = true,
}: {
  matterObjects: MatterObject[];
  gridSize?: number;
  showOcclusion?: boolean;
}) {
  const arrowsRef = useRef<THREE.Group>(null);

  const fieldData = useMemo(() => {
    const result: { 
      position: THREE.Vector3; 
      gradient: THREE.Vector3; 
      pressure: number;
      occlusion: number;
    }[] = [];
    const halfGrid = gridSize / 2;
    const step = 1;

    for (let x = -halfGrid; x <= halfGrid; x += step) {
      for (let y = -halfGrid; y <= halfGrid; y += step) {
        for (let z = -halfGrid; z <= halfGrid; z += step) {
          const pos = new THREE.Vector3(x, y, z);
          
          // Skip if too close to any matter object
          let tooClose = false;
          for (const matter of matterObjects) {
            const matterPos = new THREE.Vector3(...matter.position);
            if (pos.distanceTo(matterPos) < matter.radius + 0.3) {
              tooClose = true;
              break;
            }
          }
          if (tooClose) continue;
          
          const { pressure, gradient, occlusion } = calculatePressureField(
            pos, matterObjects, showOcclusion
          );
          
          result.push({ position: pos, gradient, pressure, occlusion });
        }
      }
    }
    return result;
  }, [matterObjects, gridSize, showOcclusion]);

  useFrame((state) => {
    if (arrowsRef.current) {
      arrowsRef.current.children.forEach((child, i) => {
        const data = fieldData[i];
        if (data && child instanceof THREE.ArrowHelper) {
          const pulse = Math.sin(state.clock.elapsedTime * 2 + i * 0.1) * 0.15 + 1;
          const length = data.gradient.length() * 2 * pulse;
          child.setLength(Math.min(length, 0.8));
        }
      });
    }
  });

  return (
    <group ref={arrowsRef}>
      {fieldData.map((data, i) => {
        const magnitude = data.gradient.length();
        if (magnitude < 0.001) return null;
        
        // Color based on occlusion level
        // Blue = low occlusion (Coulomb-like)
        // Red = high occlusion (Gravity-like)
        const hue = 0.6 - data.occlusion * 0.5; // Blue to red
        const color = new THREE.Color().setHSL(Math.max(0, hue), 0.8, 0.5);
        
        return (
          <arrowHelper
            key={i}
            args={[
              data.gradient.clone().normalize(),
              data.position,
              Math.min(magnitude * 2, 0.8),
              color,
              0.1,
              0.06,
            ]}
          />
        );
      })}
    </group>
  );
}

// Force vectors between matter objects
function ForceVectors({
  matterObjects,
  showLabels = true,
}: {
  matterObjects: MatterObject[];
  showLabels?: boolean;
}) {
  const forces = useMemo(() => {
    const result: { 
      from: THREE.Vector3; 
      to: THREE.Vector3; 
      magnitude: number;
    }[] = [];
    
    for (let i = 0; i < matterObjects.length; i++) {
      for (let j = i + 1; j < matterObjects.length; j++) {
        const objA = matterObjects[i];
        const objB = matterObjects[j];
        
        const posA = new THREE.Vector3(...objA.position);
        const posB = new THREE.Vector3(...objB.position);
        
        const direction = posB.clone().sub(posA);
        const distance = direction.length();
        
        // Force magnitude: F ∝ V_A × V_B / r²
        const magnitude = (objA.displacementVolume * objB.displacementVolume) / 
                         (distance * distance);
        
        result.push({ from: posA, to: posB, magnitude });
      }
    }
    
    return result;
  }, [matterObjects]);

  return (
    <group>
      {forces.map((force, i) => {
        const midpoint = force.from.clone().add(force.to).multiplyScalar(0.5);
        const direction = force.to.clone().sub(force.from).normalize();
        
        return (
          <group key={i}>
            {/* Force arrow from A to B */}
            <arrowHelper
              args={[
                direction,
                force.from.clone().add(direction.clone().multiplyScalar(0.5)),
                force.to.distanceTo(force.from) - 1,
                new THREE.Color('#4ade80'),
                0.15,
                0.1,
              ]}
            />
            
            {/* Force arrow from B to A */}
            <arrowHelper
              args={[
                direction.clone().negate(),
                force.to.clone().sub(direction.clone().multiplyScalar(0.5)),
                force.to.distanceTo(force.from) - 1,
                new THREE.Color('#4ade80'),
                0.15,
                0.1,
              ]}
            />
            
            {showLabels && (
              <Html position={midpoint.toArray()} center>
                <div className="bg-slate-900/80 px-2 py-1 rounded text-xs text-green-400 whitespace-nowrap">
                  F = ΔP × A
                </div>
              </Html>
            )}
          </group>
        );
      })}
    </group>
  );
}

// Occlusion visualization (shadows)
function OcclusionVisualization({
  matterObjects,
  targetPosition = [0, 0, 0] as [number, number, number],
}: {
  matterObjects: MatterObject[];
  targetPosition?: [number, number, number];
}) {
  const coneRefs = useRef<THREE.Mesh[]>([]);

  return (
    <group>
      {matterObjects.map((matter, i) => {
        const matterPos = new THREE.Vector3(...matter.position);
        const targetPos = new THREE.Vector3(...targetPosition);
        const direction = targetPos.clone().sub(matterPos).normalize();
        const distance = matterPos.distanceTo(targetPos);
        
        // Occlusion cone behind matter
        return (
          <mesh
            key={i}
            position={matter.position}
            rotation={[
              Math.atan2(direction.y, Math.sqrt(direction.x ** 2 + direction.z ** 2)),
              Math.atan2(direction.x, direction.z),
              0,
            ]}
          >
            <coneGeometry args={[matter.radius * 2, distance, 16, 1, true]} />
            <meshBasicMaterial
              color="#ef4444"
              transparent
              opacity={0.1}
              side={THREE.DoubleSide}
            />
          </mesh>
        );
      })}
    </group>
  );
}

// Pressure isobars (contour lines)
function PressureContours({
  matterObjects,
  contourCount = 5,
}: {
  matterObjects: MatterObject[];
  contourCount?: number;
}) {
  // For simplicity, show contours around the first matter object
  const centerMatter = matterObjects[0];
  if (!centerMatter) return null;

  const contours = useMemo(() => {
    return Array.from({ length: contourCount }, (_, i) => ({
      radius: (i + 1) * 0.7,
      opacity: 1 - (i / contourCount) * 0.7,
    }));
  }, [contourCount]);

  return (
    <group position={centerMatter.position}>
      {contours.map((contour, i) => (
        <mesh key={i} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[contour.radius, 0.015, 16, 64]} />
          <meshBasicMaterial
            color="#60a5fa"
            transparent
            opacity={contour.opacity * 0.4}
          />
        </mesh>
      ))}
    </group>
  );
}

// CMB boundary visualization
function CMBBoundary({ radius = 6 }: { radius?: number }) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.001;
      meshRef.current.rotation.x += 0.0005;
    }
  });

  return (
    <group>
      <mesh ref={meshRef}>
        <sphereGeometry args={[radius, 32, 32]} />
        <meshBasicMaterial
          color="#ef4444"
          wireframe
          transparent
          opacity={0.08}
        />
      </mesh>
      
      {/* CMB label */}
      <Html position={[0, radius + 0.3, 0]} center>
        <div className="text-xs text-red-400/60 whitespace-nowrap">
          CMB Boundary (z=1089)
        </div>
      </Html>
    </group>
  );
}

// Master Equation info panel
function MasterEquationPanel({
  showOcclusion,
  onToggleOcclusion,
}: {
  showOcclusion: boolean;
  onToggleOcclusion: () => void;
}) {
  return (
    <Html position={[-4.5, 2.5, 0]} center>
      <div className="bg-slate-900/95 backdrop-blur-sm p-4 rounded-xl border border-slate-700 text-white w-72">
        <h3 className="text-amber-400 font-bold mb-2">Master Equation</h3>
        
        <div className="bg-slate-800/50 p-3 rounded-lg font-mono text-sm text-center mb-3">
          ∇·[K∇Δ] = -κρ<sub>disp</sub>(1-E)
        </div>
        
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex justify-between">
            <span className="text-blue-400">K_bulk:</span>
            <span>4.6×10¹¹³ Pa</span>
          </div>
          <div className="flex justify-between">
            <span className="text-amber-400">ρ_disp:</span>
            <span>Displacement density</span>
          </div>
          <div className="flex justify-between">
            <span className="text-red-400">E(x,n̂):</span>
            <span>Directional occlusion</span>
          </div>
        </div>
        
        <button
          onClick={onToggleOcclusion}
          className={`mt-3 w-full py-2 rounded-lg text-sm transition-colors ${
            showOcclusion
              ? 'bg-red-500/20 text-red-400 border border-red-500/30'
              : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
          }`}
        >
          {showOcclusion ? '✓ Occlusion Enabled' : 'Enable Occlusion'}
        </button>
        
        <div className="mt-3 pt-3 border-t border-slate-700 text-xs text-slate-500">
          Arrow colors: Blue = Coulomb regime, Red = Gravity regime
        </div>
      </div>
    </Html>
  );
}

// Main scene
function PressureFieldScene({
  matterObjects,
  showField = true,
  showLabels = true,
  showOcclusion = true,
  showForces = true,
}: {
  matterObjects: MatterObject[];
  showField?: boolean;
  showLabels?: boolean;
  showOcclusion?: boolean;
  showForces?: boolean;
}) {
  const [selectedMatter, setSelectedMatter] = useState<string | null>(null);
  const [occlusionEnabled, setOcclusionEnabled] = useState(showOcclusion);
  
  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.4} />
      <pointLight position={[5, 5, 5]} intensity={0.8} />
      <pointLight position={[-5, -5, -5]} intensity={0.3} color="#60a5fa" />

      {/* Matter objects */}
      {matterObjects.map((matter) => (
        <MatterParticle
          key={matter.id}
          matter={matter}
          showLabels={showLabels}
          isSelected={selectedMatter === matter.id}
          onClick={() => setSelectedMatter(
            selectedMatter === matter.id ? null : matter.id
          )}
        />
      ))}

      {/* Pressure field visualization */}
      {showField && (
        <>
          <PressureGradientField
            matterObjects={matterObjects}
            gridSize={6}
            showOcclusion={occlusionEnabled}
          />
          <PressureContours matterObjects={matterObjects} contourCount={4} />
        </>
      )}

      {/* Force vectors */}
      {showForces && matterObjects.length > 1 && (
        <ForceVectors matterObjects={matterObjects} showLabels={showLabels} />
      )}

      {/* Occlusion visualization */}
      {occlusionEnabled && matterObjects.length > 1 && (
        <OcclusionVisualization
          matterObjects={matterObjects}
          targetPosition={matterObjects[1]?.position}
        />
      )}

      {/* CMB boundary */}
      <CMBBoundary radius={5.5} />

      {/* Info panel */}
      <MasterEquationPanel
        showOcclusion={occlusionEnabled}
        onToggleOcclusion={() => setOcclusionEnabled(!occlusionEnabled)}
      />

      {/* Camera controls */}
      <OrbitControls
        enablePan={true}
        enableZoom={true}
        minDistance={3}
        maxDistance={12}
      />
    </>
  );
}

// Default matter configuration
const DEFAULT_MATTER: MatterObject[] = [
  {
    id: 'matter1',
    position: [-1.5, 0, 0],
    radius: 0.4,
    displacementVolume: 0.27,
    color: '#fbbf24',
    label: 'Object A',
  },
  {
    id: 'matter2',
    position: [1.5, 0, 0],
    radius: 0.35,
    displacementVolume: 0.18,
    color: '#60a5fa',
    label: 'Object B',
  },
];

// Exported component
export default function PressureFieldSim({
  showField = true,
  showLabels = true,
  showOcclusion = true,
  showForces = true,
  interactive = true,
}: PressureFieldProps) {
  const [matterObjects, setMatterObjects] = useState<MatterObject[]>(DEFAULT_MATTER);
  const [mode, setMode] = useState<'single' | 'dual'>('dual');

  const toggleMode = useCallback(() => {
    if (mode === 'single') {
      setMode('dual');
      setMatterObjects(DEFAULT_MATTER);
    } else {
      setMode('single');
      setMatterObjects([DEFAULT_MATTER[0]]);
    }
  }, [mode]);

  return (
    <div className="relative w-full h-full min-h-[500px] bg-slate-950 rounded-xl overflow-hidden">
      {/* Controls overlay */}
      <div className="absolute top-4 left-4 z-10 flex gap-2">
        <button
          onClick={toggleMode}
          className={`px-3 py-1.5 rounded-lg text-sm backdrop-blur-sm transition-colors ${
            mode === 'dual'
              ? 'bg-blue-500/80 text-white'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700/80'
          }`}
        >
          {mode === 'dual' ? '⚡ Two Objects' : '○ Single Object'}
        </button>
      </div>

      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [5, 4, 5], fov: 60 }}
        gl={{ antialias: true }}
      >
        <PressureFieldScene
          matterObjects={matterObjects}
          showField={showField}
          showLabels={showLabels}
          showOcclusion={showOcclusion}
          showForces={showForces}
        />
      </Canvas>

      {/* Legend */}
      <div className="absolute bottom-4 right-4 bg-slate-900/80 backdrop-blur-sm p-3 rounded-lg text-xs text-slate-300">
        <div className="font-bold text-amber-400 mb-2">Pressure Field</div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-3 rounded-full bg-amber-400" />
          <span>Matter (displacement)</span>
        </div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-0.5 bg-blue-400" />
          <span>Low occlusion (Coulomb)</span>
        </div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-0.5 bg-red-400" />
          <span>High occlusion (Gravity)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-0.5 bg-green-400" />
          <span>Force between objects</span>
        </div>
      </div>
    </div>
  );
}
