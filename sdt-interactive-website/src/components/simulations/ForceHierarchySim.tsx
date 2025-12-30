/**
 * ForceHierarchySim - Coulomb = Gravity Demonstration
 * 
 * Shows how Coulomb and Gravity are the SAME force
 * in different occlusion regimes:
 * - E → 0: Coulomb regime (low occlusion)
 * - E → 1-η: Gravity regime (high occlusion)
 * 
 * SDT-ACCURATE: Same CMB pressure source, different E values.
 */

import React, { useRef, useMemo, useState, useCallback } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Html, Line } from '@react-three/drei';
import * as THREE from 'three';

// SDT Constants
const P_CMB = 2.036e-2; // CMB pressure (Pa)
const K_BULK = 4.6e113; // Spation bulk modulus

// Force regimes
interface ForceRegime {
  name: string;
  occlusion: number;
  description: string;
  color: string;
  example: string;
}

const FORCE_REGIMES: ForceRegime[] = [
  {
    name: 'Coulomb',
    occlusion: 0,
    description: 'Negligible occlusion',
    color: '#60a5fa',
    example: 'Electron-proton',
  },
  {
    name: 'Van der Waals',
    occlusion: 0.2,
    description: 'Weak occlusion',
    color: '#818cf8',
    example: 'Molecular bonds',
  },
  {
    name: 'Chemical',
    occlusion: 0.4,
    description: 'Moderate occlusion',
    color: '#a78bfa',
    example: 'Covalent bonds',
  },
  {
    name: 'Nuclear',
    occlusion: 0.6,
    description: 'Strong occlusion',
    color: '#f472b6',
    example: 'Nuclear binding',
  },
  {
    name: 'Gravity',
    occlusion: 0.99,
    description: 'Near-complete occlusion',
    color: '#ef4444',
    example: 'Planetary orbits',
  },
];

interface ForceHierarchyProps {
  initialOcclusion?: number;
  showComparison?: boolean;
  showEquation?: boolean;
}

/**
 * Calculate force at given occlusion level
 * F = ΔP × A_eff × (1 - E)
 * As E increases, effective force changes regime
 */
function calculateForce(
  distance: number,
  volume1: number,
  volume2: number,
  occlusion: number
): number {
  // Base pressure interaction (1/r² falloff)
  const baseForce = (volume1 * volume2 * P_CMB) / (4 * Math.PI * distance * distance);
  
  // Occlusion modifies effective force
  // Low E (Coulomb): Full force, fast falloff
  // High E (Gravity): Reduced force, slower falloff
  const effectiveFactor = Math.pow(1 - occlusion, 0.5);
  
  return baseForce * effectiveFactor;
}

// Particle pair visualization
function ParticlePair({
  separation,
  occlusion,
  showForceVectors = true,
}: {
  separation: number;
  occlusion: number;
  showForceVectors?: boolean;
}) {
  const groupRef = useRef<THREE.Group>(null);
  const particle1Ref = useRef<THREE.Mesh>(null);
  const particle2Ref = useRef<THREE.Mesh>(null);
  
  // Get current regime color
  const regimeColor = useMemo(() => {
    const regime = FORCE_REGIMES.reduce((prev, curr) => 
      Math.abs(curr.occlusion - occlusion) < Math.abs(prev.occlusion - occlusion) ? curr : prev
    );
    return regime.color;
  }, [occlusion]);
  
  // Calculate force magnitude
  const forceMagnitude = useMemo(() => {
    return calculateForce(separation, 1, 1, occlusion);
  }, [separation, occlusion]);
  
  useFrame((state) => {
    if (particle1Ref.current && particle2Ref.current) {
      const pulse = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.05;
      particle1Ref.current.scale.setScalar(pulse);
      particle2Ref.current.scale.setScalar(pulse);
    }
  });

  const halfSep = separation / 2;

  return (
    <group ref={groupRef}>
      {/* Particle 1 */}
      <group position={[-halfSep, 0, 0]}>
        <mesh ref={particle1Ref}>
          <sphereGeometry args={[0.4, 32, 32]} />
          <meshStandardMaterial
            color={regimeColor}
            emissive={regimeColor}
            emissiveIntensity={0.4}
            metalness={0.6}
            roughness={0.3}
          />
        </mesh>
        <Text
          position={[0, 0.7, 0]}
          fontSize={0.15}
          color="white"
          anchorX="center"
        >
          Object A
        </Text>
      </group>

      {/* Particle 2 */}
      <group position={[halfSep, 0, 0]}>
        <mesh ref={particle2Ref}>
          <sphereGeometry args={[0.4, 32, 32]} />
          <meshStandardMaterial
            color={regimeColor}
            emissive={regimeColor}
            emissiveIntensity={0.4}
            metalness={0.6}
            roughness={0.3}
          />
        </mesh>
        <Text
          position={[0, 0.7, 0]}
          fontSize={0.15}
          color="white"
          anchorX="center"
        >
          Object B
        </Text>
      </group>

      {/* Force vectors */}
      {showForceVectors && (
        <>
          {/* Force on A toward B */}
          <arrowHelper
            args={[
              new THREE.Vector3(1, 0, 0),
              new THREE.Vector3(-halfSep + 0.5, 0, 0),
              forceMagnitude * 20,
              new THREE.Color(regimeColor),
              0.15,
              0.1,
            ]}
          />
          {/* Force on B toward A */}
          <arrowHelper
            args={[
              new THREE.Vector3(-1, 0, 0),
              new THREE.Vector3(halfSep - 0.5, 0, 0),
              forceMagnitude * 20,
              new THREE.Color(regimeColor),
              0.15,
              0.1,
            ]}
          />
        </>
      )}

      {/* Connection line */}
      <Line
        points={[[-halfSep, 0, 0], [halfSep, 0, 0]]}
        color={regimeColor}
        lineWidth={1}
        dashed
        dashSize={0.1}
        gapSize={0.1}
      />

      {/* Distance label */}
      <Html position={[0, -0.6, 0]} center>
        <div className="bg-slate-900/80 px-2 py-1 rounded text-xs text-white whitespace-nowrap">
          r = {separation.toFixed(1)} units
        </div>
      </Html>
    </group>
  );
}

// Occlusion visualization (shadow cones)
function OcclusionVisualization({
  separation,
  occlusion,
}: {
  separation: number;
  occlusion: number;
}) {
  const halfSep = separation / 2;
  const coneAngle = Math.PI / 4 * occlusion; // Wider cone = more occlusion
  
  return (
    <group>
      {/* Occlusion from A blocking B */}
      <mesh
        position={[-halfSep, 0, 0]}
        rotation={[0, 0, -Math.PI / 2]}
      >
        <coneGeometry args={[occlusion * 2, separation * 0.8, 16, 1, true]} />
        <meshBasicMaterial
          color="#ef4444"
          transparent
          opacity={0.1 + occlusion * 0.1}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Occlusion from B blocking A */}
      <mesh
        position={[halfSep, 0, 0]}
        rotation={[0, 0, Math.PI / 2]}
      >
        <coneGeometry args={[occlusion * 2, separation * 0.8, 16, 1, true]} />
        <meshBasicMaterial
          color="#ef4444"
          transparent
          opacity={0.1 + occlusion * 0.1}
          side={THREE.DoubleSide}
        />
      </mesh>
    </group>
  );
}

// CMB pressure arrows coming from all directions
function CMBPressureArrows({ radius = 4, count = 12 }: { radius?: number; count?: number }) {
  const arrows = useMemo(() => {
    const result: THREE.Vector3[] = [];
    
    // Create arrows from multiple directions
    for (let i = 0; i < count; i++) {
      const theta = (i / count) * Math.PI * 2;
      for (let j = 0; j < 3; j++) {
        const phi = ((j + 0.5) / 3) * Math.PI;
        result.push(new THREE.Vector3(
          Math.sin(phi) * Math.cos(theta) * radius,
          Math.cos(phi) * radius,
          Math.sin(phi) * Math.sin(theta) * radius,
        ));
      }
    }
    
    return result;
  }, [radius, count]);

  return (
    <group>
      {arrows.map((pos, i) => (
        <arrowHelper
          key={i}
          args={[
            pos.clone().negate().normalize(),
            pos,
            0.8,
            new THREE.Color('#ef4444'),
            0.12,
            0.08,
          ]}
        />
      ))}
    </group>
  );
}

// Force comparison chart (log scale)
function ForceComparisonChart({
  currentOcclusion,
}: {
  currentOcclusion: number;
}) {
  return (
    <Html position={[4, 2, 0]} center>
      <div className="bg-slate-900/95 backdrop-blur-sm p-4 rounded-xl border border-slate-700 text-white w-64">
        <h4 className="text-amber-400 font-bold mb-3">Force Regimes</h4>
        
        <div className="space-y-2">
          {FORCE_REGIMES.map((regime) => {
            const isActive = Math.abs(regime.occlusion - currentOcclusion) < 0.15;
            
            return (
              <div
                key={regime.name}
                className={`p-2 rounded-lg transition-all ${
                  isActive ? 'bg-white/10 border border-white/20' : ''
                }`}
              >
                <div className="flex items-center gap-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: regime.color }}
                  />
                  <span className={`font-medium ${isActive ? 'text-white' : 'text-slate-400'}`}>
                    {regime.name}
                  </span>
                </div>
                <div className="ml-5 text-xs text-slate-500">
                  E = {regime.occlusion} — {regime.example}
                </div>
              </div>
            );
          })}
        </div>
        
        <div className="mt-4 pt-3 border-t border-slate-700 text-xs text-slate-400">
          <div className="font-mono">
            E → 0: Coulomb
          </div>
          <div className="font-mono">
            E → 1-η: Gravity
          </div>
        </div>
      </div>
    </Html>
  );
}

// Equation display panel
function EquationPanel({ occlusion }: { occlusion: number }) {
  const currentRegime = FORCE_REGIMES.reduce((prev, curr) => 
    Math.abs(curr.occlusion - occlusion) < Math.abs(prev.occlusion - occlusion) ? curr : prev
  );
  
  return (
    <Html position={[-4, 2.5, 0]} center>
      <div className="bg-slate-900/95 backdrop-blur-sm p-4 rounded-xl border border-slate-700 text-white w-72">
        <h3 className="text-amber-400 font-bold mb-2">The Key Insight</h3>
        
        <div className="bg-slate-800/50 p-3 rounded-lg mb-3">
          <p className="text-sm text-slate-300 mb-2">
            Coulomb and Gravity are the <span className="text-amber-400 font-bold">SAME FORCE</span>
          </p>
          <p className="text-xs text-slate-400">
            Only the occlusion level E(x,n̂) differs
          </p>
        </div>
        
        <div className="space-y-2 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-blue-400" />
            <span>Atoms: E ≈ 0 (Coulomb)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-red-400" />
            <span>Planets: E ≈ 0.99 (Gravity)</span>
          </div>
        </div>
        
        <div className="mt-4 p-2 rounded-lg" style={{ backgroundColor: currentRegime.color + '20' }}>
          <div className="text-center">
            <span className="font-bold" style={{ color: currentRegime.color }}>
              {currentRegime.name} Regime
            </span>
            <div className="text-xs text-slate-400 mt-1">
              {currentRegime.description}
            </div>
          </div>
        </div>
        
        <div className="mt-3 font-mono text-xs text-slate-400 text-center">
          F = ΔP × A<sub>eff</sub> × (1-E)
        </div>
      </div>
    </Html>
  );
}

// Main scene
function ForceHierarchyScene({
  occlusion,
  separation,
  showEquation = true,
}: {
  occlusion: number;
  separation: number;
  showEquation?: boolean;
}) {
  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.4} />
      <pointLight position={[5, 5, 5]} intensity={0.8} />
      <pointLight position={[-5, -5, -5]} intensity={0.3} />

      {/* Particle pair */}
      <ParticlePair
        separation={separation}
        occlusion={occlusion}
        showForceVectors={true}
      />

      {/* Occlusion visualization */}
      {occlusion > 0.1 && (
        <OcclusionVisualization
          separation={separation}
          occlusion={occlusion}
        />
      )}

      {/* CMB pressure from all directions */}
      <CMBPressureArrows radius={4.5} count={8} />

      {/* Info panels */}
      <EquationPanel occlusion={occlusion} />
      <ForceComparisonChart currentOcclusion={occlusion} />

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
export default function ForceHierarchySim({
  initialOcclusion = 0,
  showComparison = true,
  showEquation = true,
}: ForceHierarchyProps) {
  const [occlusion, setOcclusion] = useState(initialOcclusion);
  const [separation, setSeparation] = useState(3);

  // Get current regime
  const currentRegime = FORCE_REGIMES.reduce((prev, curr) => 
    Math.abs(curr.occlusion - occlusion) < Math.abs(prev.occlusion - occlusion) ? curr : prev
  );

  return (
    <div className="relative w-full h-full min-h-[500px] bg-slate-950 rounded-xl overflow-hidden">
      {/* Control panel */}
      <div className="absolute top-4 left-4 z-10 bg-slate-900/90 backdrop-blur-sm p-4 rounded-xl border border-slate-700 w-64">
        <h4 className="text-white font-bold mb-3">Occlusion Control</h4>
        
        {/* Occlusion slider */}
        <div className="mb-4">
          <div className="flex justify-between text-xs text-slate-400 mb-1">
            <span>Coulomb (E=0)</span>
            <span>Gravity (E=1)</span>
          </div>
          <input
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={occlusion}
            onChange={(e) => setOcclusion(parseFloat(e.target.value))}
            className="w-full h-2 bg-gradient-to-r from-blue-500 to-red-500 rounded-lg appearance-none cursor-pointer"
          />
          <div className="text-center mt-2">
            <span className="text-lg font-bold" style={{ color: currentRegime.color }}>
              E = {occlusion.toFixed(2)}
            </span>
          </div>
        </div>

        {/* Separation slider */}
        <div>
          <label className="text-xs text-slate-400 block mb-1">
            Separation: {separation.toFixed(1)}
          </label>
          <input
            type="range"
            min={1.5}
            max={5}
            step={0.1}
            value={separation}
            onChange={(e) => setSeparation(parseFloat(e.target.value))}
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        {/* Regime quick buttons */}
        <div className="mt-4 grid grid-cols-2 gap-2">
          {FORCE_REGIMES.filter((_, i) => i === 0 || i === 4).map((regime) => (
            <button
              key={regime.name}
              onClick={() => setOcclusion(regime.occlusion)}
              className="py-2 rounded-lg text-xs font-medium transition-colors"
              style={{
                backgroundColor: regime.color + '20',
                color: regime.color,
                border: `1px solid ${regime.color}40`,
              }}
            >
              {regime.name}
            </button>
          ))}
        </div>
      </div>

      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [0, 3, 8], fov: 60 }}
        gl={{ antialias: true }}
      >
        <ForceHierarchyScene
          occlusion={occlusion}
          separation={separation}
          showEquation={showEquation}
        />
      </Canvas>

      {/* Current regime indicator */}
      <div
        className="absolute bottom-4 left-4 px-4 py-2 rounded-lg"
        style={{
          backgroundColor: currentRegime.color + '30',
          border: `1px solid ${currentRegime.color}`,
        }}
      >
        <div className="text-lg font-bold" style={{ color: currentRegime.color }}>
          {currentRegime.name} Regime
        </div>
        <div className="text-xs text-slate-400">
          Example: {currentRegime.example}
        </div>
      </div>

      {/* Legend */}
      <div className="absolute bottom-4 right-4 bg-slate-900/80 backdrop-blur-sm p-3 rounded-lg text-xs text-slate-300">
        <div className="font-bold text-amber-400 mb-2">Same Force, Different E</div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-0.5 bg-red-400" />
          <span>CMB pressure (incoming)</span>
        </div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-3 rounded bg-red-400/30" />
          <span>Occlusion shadow</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-0.5 bg-current" style={{ backgroundColor: currentRegime.color }} />
          <span>Force (current regime)</span>
        </div>
      </div>
    </div>
  );
}

