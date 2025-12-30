/**
 * Creative Agent: Atomic Structure Visualizer
 * 
 * TEKNE: The visualization IS the structure
 * 
 * "Necessarily false" but representative abstractions of SDT nuclear structure.
 * Shows the geometric essence of:
 * - D (Deuteron): (np) - dumbbell
 * - A (Alpha): (np)(np) - tetrahedron
 * - tri-A: (np)n(np) - wobble carrier
 * - Triple: (np)n(np)n(np) - chain
 * 
 * Representative abstraction - the model IS impossible to show entirely.
 * We show the truth of its geometry, not its impossible detail.
 */

import React, { useRef, useMemo, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Group, Mesh, Color, Vector3 } from 'three';
import { Text, Line, Sphere, Torus } from '@react-three/drei';
import { PHI, PHI_INVERSE, GOLDEN_ANGLE, fibonacci } from '../../utils/sacred-geometry';

// SDT Color Palette for Nuclear Visualization
const NUCLEAR_COLORS = {
  // Nucleons
  proton: new Color(0xff6b6b),        // Warm coral-red
  neutron: new Color(0x4ecdc4),       // Cool teal
  protonGlow: new Color(0xff8787),
  neutronGlow: new Color(0x6ee7de),
  
  // Building blocks
  deuteron: new Color(0xffd93d),      // Golden yellow
  alpha: new Color(0xf6ad55),         // Amber
  triAlpha: new Color(0xa78bfa),      // Violet
  triple: new Color(0x60a5fa),        // Blue
  
  // Electrons
  electronOrbit: new Color(0x94a3b8), // Silver-gray
  electronPath: new Color(0xfbbf24),  // Gold trace
  electron: new Color(0xe2e8f0),      // Bright white
  
  // Bonds/Bridges
  neutrinoBridge: new Color(0xd69e2e), // Gold flux
  
  // Background
  spaceDeep: new Color(0x0a0e1a),
} as const;

// Element configurations based on Atomica Sentis
interface ElementConfig {
  symbol: string;
  name: string;
  Z: number;
  N: number;
  structure: string;
  alphas: number;
  deuterons: number;
  triAlphas: number;
  triples: number;
  bridges: number;
  geometry: 'linear' | 'triangular' | 'tetrahedral' | 'octahedral' | 'complex';
  description: string;
}

const ELEMENTS: Record<string, ElementConfig> = {
  H: { symbol: 'H', name: 'Hydrogen', Z: 1, N: 0, structure: 'p', alphas: 0, deuterons: 0, triAlphas: 0, triples: 0, bridges: 0, geometry: 'linear', description: 'Single proton - primordial building block' },
  D: { symbol: 'D', name: 'Deuterium', Z: 1, N: 1, structure: 'p-n', alphas: 0, deuterons: 1, triAlphas: 0, triples: 0, bridges: 0, geometry: 'linear', description: 'Deuteron - atomic mortar' },
  He3: { symbol: '³He', name: 'Helium-3', Z: 2, N: 1, structure: 'p-n-p', alphas: 0, deuterons: 0, triAlphas: 0, triples: 0, bridges: 0, geometry: 'linear', description: 'Two protons bridged by neutron' },
  He4: { symbol: '⁴He', name: 'Helium-4', Z: 2, N: 2, structure: '[α]', alphas: 1, deuterons: 0, triAlphas: 0, triples: 0, bridges: 0, geometry: 'tetrahedral', description: 'Alpha particle - diamond of nuclear physics' },
  Li6: { symbol: '⁶Li', name: 'Lithium-6', Z: 3, N: 3, structure: '[α]+D', alphas: 1, deuterons: 1, triAlphas: 0, triples: 0, bridges: 1, geometry: 'linear', description: 'Alpha plus deuteron attachment' },
  Li7: { symbol: '⁷Li', name: 'Lithium-7', Z: 3, N: 4, structure: '[α]+T', alphas: 1, deuterons: 0, triAlphas: 1, triples: 0, bridges: 1, geometry: 'linear', description: 'Alpha plus triton' },
  Be9: { symbol: '⁹Be', name: 'Beryllium-9', Z: 4, N: 5, structure: '[α]-n-[α]', alphas: 2, deuterons: 0, triAlphas: 0, triples: 0, bridges: 1, geometry: 'linear', description: 'Two alphas - neutron bridge' },
  C12: { symbol: '¹²C', name: 'Carbon-12', Z: 6, N: 6, structure: '[α]₃', alphas: 3, deuterons: 0, triAlphas: 0, triples: 0, bridges: 3, geometry: 'triangular', description: 'Three alphas in triangular arrangement' },
  N14: { symbol: '¹⁴N', name: 'Nitrogen-14', Z: 7, N: 7, structure: '[α]₃-p', alphas: 3, deuterons: 0, triAlphas: 0, triples: 0, bridges: 3, geometry: 'triangular', description: 'Three alphas plus proton' },
  O16: { symbol: '¹⁶O', name: 'Oxygen-16', Z: 8, N: 8, structure: '[α]₄', alphas: 4, deuterons: 0, triAlphas: 0, triples: 0, bridges: 6, geometry: 'tetrahedral', description: 'Four alphas in tetrahedral arrangement' },
  Fe56: { symbol: '⁵⁶Fe', name: 'Iron-56', Z: 26, N: 30, structure: '[α]₁₄', alphas: 14, deuterons: 0, triAlphas: 0, triples: 0, bridges: 30, geometry: 'complex', description: 'Maximum binding - stellar endpoint' },
};

export interface AtomicStructureVisualizerProps {
  element: keyof typeof ELEMENTS;
  showElectrons?: boolean;
  showLabels?: boolean;
  showBuildingBlocks?: boolean;
  scale?: number;
  animated?: boolean;
}

/**
 * ProtonVisual - Toroidal turbine cell representation
 */
function ProtonVisual({ position, scale = 1 }: { position: Vector3; scale?: number }) {
  const meshRef = useRef<Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      // Slow rotation representing turbine circulation
      meshRef.current.rotation.z += 0.01 * PHI_INVERSE;
    }
  });
  
  return (
    <group position={position}>
      {/* Main toroidal body */}
      <Torus
        ref={meshRef}
        args={[0.3 * scale, 0.12 * scale, 16, 32]}
      >
        <meshStandardMaterial
          color={NUCLEAR_COLORS.proton}
          emissive={NUCLEAR_COLORS.protonGlow}
          emissiveIntensity={0.4}
          metalness={0.7}
          roughness={0.3}
        />
      </Torus>
      
      {/* Inner glow - circulation center */}
      <Sphere args={[0.08 * scale, 16, 16]}>
        <meshStandardMaterial
          color={NUCLEAR_COLORS.protonGlow}
          emissive={NUCLEAR_COLORS.proton}
          emissiveIntensity={0.8}
          transparent
          opacity={0.6}
        />
      </Sphere>
    </group>
  );
}

/**
 * NeutronVisual - Toroidal turbine cell with internal structure
 */
function NeutronVisual({ position, scale = 1 }: { position: Vector3; scale?: number }) {
  const meshRef = useRef<Mesh>(null);
  const innerRef = useRef<Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.z += 0.008 * PHI_INVERSE;
    }
    if (innerRef.current) {
      // Internal electron orbit (opposite direction)
      innerRef.current.rotation.z -= 0.02 * PHI;
    }
  });
  
  return (
    <group position={position}>
      {/* Main toroidal body - slightly larger than proton */}
      <Torus
        ref={meshRef}
        args={[0.33 * scale, 0.13 * scale, 16, 32]}
      >
        <meshStandardMaterial
          color={NUCLEAR_COLORS.neutron}
          emissive={NUCLEAR_COLORS.neutronGlow}
          emissiveIntensity={0.3}
          metalness={0.6}
          roughness={0.4}
        />
      </Torus>
      
      {/* Internal electron orbit representation */}
      <Torus
        ref={innerRef}
        args={[0.15 * scale, 0.02 * scale, 8, 24]}
        rotation={[Math.PI / 2, 0, 0]}
      >
        <meshStandardMaterial
          color={NUCLEAR_COLORS.electron}
          emissive={NUCLEAR_COLORS.electronPath}
          emissiveIntensity={0.5}
          transparent
          opacity={0.7}
        />
      </Torus>
    </group>
  );
}

/**
 * DeuteronVisual - (np) dumbbell structure
 */
function DeuteronVisual({ position, rotation = [0, 0, 0], scale = 1 }: { 
  position: Vector3; 
  rotation?: [number, number, number];
  scale?: number;
}) {
  const groupRef = useRef<Group>(null);
  
  useFrame((state) => {
    if (groupRef.current) {
      // Slow wobble
      groupRef.current.rotation.y += 0.005 * PHI_INVERSE;
    }
  });
  
  const offset = 0.5 * scale;
  
  return (
    <group ref={groupRef} position={position} rotation={rotation}>
      {/* Proton */}
      <ProtonVisual position={new Vector3(-offset, 0, 0)} scale={scale * 0.8} />
      
      {/* Neutron */}
      <NeutronVisual position={new Vector3(offset, 0, 0)} scale={scale * 0.8} />
      
      {/* Neutrino flux bond - golden spiral */}
      <Line
        points={[[-offset, 0, 0], [offset, 0, 0]]}
        color={NUCLEAR_COLORS.neutrinoBridge}
        lineWidth={2}
        transparent
        opacity={0.6}
      />
    </group>
  );
}

/**
 * AlphaVisual - (np)(np) tetrahedral structure
 * The "diamond of nuclear physics"
 */
function AlphaVisual({ position, scale = 1 }: { position: Vector3; scale?: number }) {
  const groupRef = useRef<Group>(null);
  
  useFrame((state) => {
    if (groupRef.current) {
      // Slow tumble
      groupRef.current.rotation.x += 0.003 * PHI_INVERSE;
      groupRef.current.rotation.y += 0.005 * PHI_INVERSE;
    }
  });
  
  // Tetrahedral vertices
  const tetraVertices = useMemo(() => {
    const a = 0.6 * scale;
    return [
      new Vector3(a, a, a),      // Top-front-right (proton)
      new Vector3(-a, -a, a),    // Bottom-back-right (neutron)
      new Vector3(-a, a, -a),    // Top-back-left (neutron)
      new Vector3(a, -a, -a),    // Bottom-front-left (proton)
    ];
  }, [scale]);
  
  // Edges of tetrahedron
  const edges = useMemo(() => {
    const v = tetraVertices;
    return [
      [v[0], v[1]], [v[0], v[2]], [v[0], v[3]],
      [v[1], v[2]], [v[1], v[3]], [v[2], v[3]],
    ];
  }, [tetraVertices]);
  
  return (
    <group ref={groupRef} position={position}>
      {/* Two protons at opposite vertices */}
      <ProtonVisual position={tetraVertices[0]} scale={scale * 0.5} />
      <ProtonVisual position={tetraVertices[3]} scale={scale * 0.5} />
      
      {/* Two neutrons at other vertices */}
      <NeutronVisual position={tetraVertices[1]} scale={scale * 0.5} />
      <NeutronVisual position={tetraVertices[2]} scale={scale * 0.5} />
      
      {/* Neutrino flux bonds */}
      {edges.map((edge, i) => (
        <Line
          key={i}
          points={[edge[0].toArray(), edge[1].toArray()]}
          color={NUCLEAR_COLORS.neutrinoBridge}
          lineWidth={1.5}
          transparent
          opacity={0.4}
        />
      ))}
      
      {/* Central glow - the binding flux */}
      <Sphere args={[0.2 * scale, 16, 16]}>
        <meshStandardMaterial
          color={NUCLEAR_COLORS.alpha}
          emissive={NUCLEAR_COLORS.neutrinoBridge}
          emissiveIntensity={0.6}
          transparent
          opacity={0.3}
        />
      </Sphere>
    </group>
  );
}

/**
 * TriAlphaVisual - (np)n(np) wobble carrier
 */
function TriAlphaVisual({ position, scale = 1 }: { position: Vector3; scale?: number }) {
  const groupRef = useRef<Group>(null);
  
  useFrame((state) => {
    if (groupRef.current) {
      // Wobble motion (it's the wobble carrier!)
      const t = state.clock.elapsedTime;
      groupRef.current.rotation.x = Math.sin(t * PHI_INVERSE) * 0.1;
      groupRef.current.rotation.z = Math.cos(t * PHI_INVERSE * 0.7) * 0.1;
    }
  });
  
  return (
    <group ref={groupRef} position={position}>
      {/* Left deuteron */}
      <DeuteronVisual 
        position={new Vector3(-1.2 * scale, 0, 0)} 
        rotation={[0, 0, Math.PI / 4]}
        scale={scale * 0.7} 
      />
      
      {/* Central bridging neutron */}
      <NeutronVisual position={new Vector3(0, 0, 0)} scale={scale * 0.9} />
      
      {/* Right deuteron */}
      <DeuteronVisual 
        position={new Vector3(1.2 * scale, 0, 0)} 
        rotation={[0, 0, -Math.PI / 4]}
        scale={scale * 0.7} 
      />
      
      {/* Bridge bonds */}
      <Line
        points={[[-0.6 * scale, 0, 0], [0, 0, 0]]}
        color={NUCLEAR_COLORS.triAlpha}
        lineWidth={2}
        transparent
        opacity={0.5}
      />
      <Line
        points={[[0, 0, 0], [0.6 * scale, 0, 0]]}
        color={NUCLEAR_COLORS.triAlpha}
        lineWidth={2}
        transparent
        opacity={0.5}
      />
    </group>
  );
}

/**
 * ElectronOrbit - Orbital path visualization
 */
function ElectronOrbit({ 
  radius, 
  electrons = 1,
  tilt = 0,
  phase = 0,
  color = NUCLEAR_COLORS.electronOrbit 
}: { 
  radius: number; 
  electrons?: number;
  tilt?: number;
  phase?: number;
  color?: Color;
}) {
  const groupRef = useRef<Group>(null);
  const electronRefs = useRef<Mesh[]>([]);
  
  useFrame((state) => {
    const t = state.clock.elapsedTime + phase;
    
    electronRefs.current.forEach((ref, i) => {
      if (ref) {
        const angle = t * 2 + (i * Math.PI * 2) / electrons;
        ref.position.x = Math.cos(angle) * radius;
        ref.position.z = Math.sin(angle) * radius;
      }
    });
  });
  
  return (
    <group ref={groupRef} rotation={[tilt, 0, 0]}>
      {/* Orbital ring */}
      <Torus args={[radius, 0.01, 8, 64]} rotation={[Math.PI / 2, 0, 0]}>
        <meshStandardMaterial
          color={color}
          emissive={NUCLEAR_COLORS.electronPath}
          emissiveIntensity={0.2}
          transparent
          opacity={0.3}
        />
      </Torus>
      
      {/* Electrons */}
      {Array.from({ length: electrons }).map((_, i) => (
        <Sphere
          key={i}
          ref={(el) => { if (el) electronRefs.current[i] = el; }}
          args={[0.06, 8, 8]}
        >
          <meshStandardMaterial
            color={NUCLEAR_COLORS.electron}
            emissive={NUCLEAR_COLORS.electronPath}
            emissiveIntensity={0.8}
          />
        </Sphere>
      ))}
    </group>
  );
}

/**
 * Main Atomic Structure Visualizer
 */
export default function AtomicStructureVisualizer({
  element,
  showElectrons = true,
  showLabels = true,
  showBuildingBlocks = true,
  scale = 1,
  animated = true,
}: AtomicStructureVisualizerProps) {
  const config = ELEMENTS[element];
  const groupRef = useRef<Group>(null);
  
  if (!config) {
    return null;
  }
  
  // Generate nuclear structure based on element
  const renderNucleus = () => {
    switch (element) {
      case 'H':
        return <ProtonVisual position={new Vector3(0, 0, 0)} scale={scale} />;
        
      case 'D':
        return <DeuteronVisual position={new Vector3(0, 0, 0)} scale={scale} />;
        
      case 'He3':
        return (
          <group>
            <ProtonVisual position={new Vector3(-0.5 * scale, 0, 0)} scale={scale * 0.8} />
            <NeutronVisual position={new Vector3(0, 0, 0)} scale={scale * 0.9} />
            <ProtonVisual position={new Vector3(0.5 * scale, 0, 0)} scale={scale * 0.8} />
            <Line
              points={[[-0.5 * scale, 0, 0], [0, 0, 0], [0.5 * scale, 0, 0]]}
              color={NUCLEAR_COLORS.neutrinoBridge}
              lineWidth={2}
            />
          </group>
        );
        
      case 'He4':
        return <AlphaVisual position={new Vector3(0, 0, 0)} scale={scale} />;
        
      case 'Li6':
        return (
          <group>
            <AlphaVisual position={new Vector3(-0.8 * scale, 0, 0)} scale={scale * 0.7} />
            <DeuteronVisual position={new Vector3(0.8 * scale, 0, 0)} scale={scale * 0.6} />
            <Line
              points={[[0, 0, 0], [0.3 * scale, 0, 0]]}
              color={NUCLEAR_COLORS.neutrinoBridge}
              lineWidth={2}
            />
          </group>
        );
        
      case 'Li7':
        return (
          <group>
            <AlphaVisual position={new Vector3(-0.8 * scale, 0, 0)} scale={scale * 0.7} />
            <TriAlphaVisual position={new Vector3(1 * scale, 0, 0)} scale={scale * 0.5} />
          </group>
        );
        
      case 'Be9':
        return (
          <group>
            <AlphaVisual position={new Vector3(-1.2 * scale, 0, 0)} scale={scale * 0.6} />
            <NeutronVisual position={new Vector3(0, 0, 0)} scale={scale * 0.8} />
            <AlphaVisual position={new Vector3(1.2 * scale, 0, 0)} scale={scale * 0.6} />
            <Line
              points={[[-0.6 * scale, 0, 0], [0, 0, 0], [0.6 * scale, 0, 0]]}
              color={NUCLEAR_COLORS.neutrinoBridge}
              lineWidth={2.5}
              transparent
              opacity={0.7}
            />
          </group>
        );
        
      case 'C12':
        // Three alphas in triangular arrangement
        const trianglePositions = [
          new Vector3(0, 0.8 * scale, 0),
          new Vector3(-0.7 * scale, -0.4 * scale, 0),
          new Vector3(0.7 * scale, -0.4 * scale, 0),
        ];
        return (
          <group>
            {trianglePositions.map((pos, i) => (
              <AlphaVisual key={i} position={pos} scale={scale * 0.5} />
            ))}
            {/* Bridge lines */}
            <Line
              points={[
                trianglePositions[0].toArray(),
                trianglePositions[1].toArray(),
                trianglePositions[2].toArray(),
                trianglePositions[0].toArray(),
              ]}
              color={NUCLEAR_COLORS.neutrinoBridge}
              lineWidth={2}
              transparent
              opacity={0.5}
            />
          </group>
        );
        
      case 'N14':
        // Three alphas plus proton
        const nTriPos = [
          new Vector3(0, 0.8 * scale, 0),
          new Vector3(-0.7 * scale, -0.4 * scale, 0),
          new Vector3(0.7 * scale, -0.4 * scale, 0),
        ];
        return (
          <group>
            {nTriPos.map((pos, i) => (
              <AlphaVisual key={i} position={pos} scale={scale * 0.45} />
            ))}
            <ProtonVisual position={new Vector3(0, 0, 0.5 * scale)} scale={scale * 0.6} />
          </group>
        );
        
      case 'O16':
        // Four alphas in tetrahedral arrangement
        const tetraPos = [
          new Vector3(0.7 * scale, 0.7 * scale, 0.7 * scale),
          new Vector3(-0.7 * scale, -0.7 * scale, 0.7 * scale),
          new Vector3(-0.7 * scale, 0.7 * scale, -0.7 * scale),
          new Vector3(0.7 * scale, -0.7 * scale, -0.7 * scale),
        ];
        return (
          <group>
            {tetraPos.map((pos, i) => (
              <AlphaVisual key={i} position={pos} scale={scale * 0.4} />
            ))}
          </group>
        );
        
      case 'Fe56':
        // Complex arrangement - 14 alphas (abstracted)
        // Show as nested shells for visual clarity
        return (
          <group>
            {/* Inner tetrahedron (4 alphas) */}
            {[0, 1, 2, 3].map((i) => {
              const angle = (i * Math.PI * 2) / 4 + Math.PI / 4;
              const r = 0.5 * scale;
              return (
                <AlphaVisual
                  key={`inner-${i}`}
                  position={new Vector3(
                    Math.cos(angle) * r,
                    (i % 2 === 0 ? 0.3 : -0.3) * scale,
                    Math.sin(angle) * r
                  )}
                  scale={scale * 0.25}
                />
              );
            })}
            {/* Outer ring (10 alphas) */}
            {Array.from({ length: 10 }).map((_, i) => {
              const angle = (i * Math.PI * 2) / 10;
              const r = 1.2 * scale;
              return (
                <AlphaVisual
                  key={`outer-${i}`}
                  position={new Vector3(
                    Math.cos(angle) * r,
                    Math.sin(i * GOLDEN_ANGLE) * 0.3 * scale,
                    Math.sin(angle) * r
                  )}
                  scale={scale * 0.2}
                />
              );
            })}
          </group>
        );
        
      default:
        return <AlphaVisual position={new Vector3(0, 0, 0)} scale={scale} />;
    }
  };
  
  // Electron shells based on element
  const electronShells = useMemo(() => {
    const shells: Array<{ n: number; electrons: number; radius: number }> = [];
    let remaining = config.Z;
    const shellCapacity = [2, 8, 18, 32, 32, 18, 8];
    
    shellCapacity.forEach((capacity, n) => {
      if (remaining > 0) {
        const inShell = Math.min(remaining, capacity);
        shells.push({ n: n + 1, electrons: inShell, radius: 2 + n * 1.2 });
        remaining -= inShell;
      }
    });
    
    return shells;
  }, [config.Z]);
  
  return (
    <group ref={groupRef}>
      {/* Nucleus */}
      {renderNucleus()}
      
      {/* Electron shells */}
      {showElectrons && electronShells.map((shell, i) => (
        <ElectronOrbit
          key={i}
          radius={shell.radius * scale * 0.5}
          electrons={Math.min(shell.electrons, 8)} // Limit for visual clarity
          tilt={i * Math.PI / 6}
          phase={i * Math.PI / 3}
        />
      ))}
      
      {/* Labels */}
      {showLabels && (
        <Text
          position={[0, -3 * scale, 0]}
          fontSize={0.3 * scale}
          color="#ffffff"
          anchorX="center"
          anchorY="middle"
        >
          {config.symbol} - {config.name}
        </Text>
      )}
    </group>
  );
}

// Export element configurations for use in other components
export { ELEMENTS, NUCLEAR_COLORS };
export type { ElementConfig };

