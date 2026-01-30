/**
 * SDT Atomic Structure Visualizer
 * 
 * Implements Spatial Displacement Theory nuclear model:
 * 
 * DEUTERON (D): Two flattened trefoil toroids (proton + neutron)
 *   - Hole-to-hole, interleaved on one edge
 *   - Shared electron traces path between contact surfaces
 * 
 * ALPHA (α): Two deuterons side by side
 *   - One rotated 90° to the other
 *   - Electron paths run between them
 * 
 * NUCLEAR ROTATION: Whole nucleus rotates, matching electron shell positions
 * NUCLEON SPIN: Individual p/n spin in place (not with the whole)
 * 
 * ELECTRON POSITIONS: Match experimental probability clouds
 *   - s orbitals: spherical
 *   - p orbitals: dumbbell lobes
 *   - d orbitals: clover shapes
 * 
 * Valence positions: opposite side of nucleus from shared electron
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Group, Mesh, Color, Vector3 } from 'three';
import { Text, Sphere, Torus, Html } from '@react-three/drei';
import TrefoilNuclearVisualizer from './TrefoilNuclearVisualizer';

// ============================================================================
// SDT COLORS
// ============================================================================

const FAMILY_COLORS: Record<string, Color> = {
  'hydrogen':          new Color(0x66d9e8),
  'alkali-metal':      new Color(0xff6b6b),
  'alkaline-earth':    new Color(0xffa94d),
  'boron-group':       new Color(0xa9e34b),
  'carbon-group':      new Color(0x51cf66),
  'nitrogen-group':    new Color(0x4dabf7),
  'chalcogen':         new Color(0xbe4bdb),
  'halogen':           new Color(0xf06595),
  'noble-gas':         new Color(0xffd43b),
  'transition-metal':  new Color(0x868e96),
};

const COLORS = {
  proton: new Color(0xc62828),
  protonInner: new Color(0xef5350),
  neutron: new Color(0x1565c0),
  neutronInner: new Color(0x42a5f5),
  sharedElectron: new Color(0xffeb3b),
  valenceCloud: new Color(0xffd54f),
  coreCloud: new Color(0x90caf9),
  electronPath: new Color(0xffc107),
};

// ============================================================================
// TREFOIL TOROID NUCLEON
// ============================================================================

interface TrefoilNucleonProps {
  position: Vector3;
  type: 'proton' | 'neutron';
  rotation?: [number, number, number];
  spinSpeed?: number;
  scale?: number;
}

/**
 * Flattened trefoil toroid nucleon
 * Each nucleon spins in place (not with nuclear rotation)
 */
function TrefoilNucleon({ 
  position, 
  type, 
  rotation = [0, 0, 0], 
  spinSpeed = 1,
  scale = 1 
}: TrefoilNucleonProps) {
  const meshRef = useRef<Mesh>(null);
  const colors = type === 'proton' 
    ? { main: COLORS.proton, inner: COLORS.protonInner }
    : { main: COLORS.neutron, inner: COLORS.neutronInner };
  
  // Individual nucleon spin (fast, in place)
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.z += 0.05 * spinSpeed * (type === 'proton' ? 1 : -1);
    }
  });
  
  const r = 0.08 * scale;
  
  return (
    <group position={position} rotation={rotation}>
      {/* Flattened torus - trefoil-like shape */}
      <Torus
        ref={meshRef}
        args={[r, r * 0.4, 8, 24]}
        scale={[1, 1, 0.5]} // Flattened
      >
        <meshStandardMaterial
          color={colors.main}
          emissive={colors.inner}
          emissiveIntensity={0.4}
          metalness={0.3}
          roughness={0.5}
        />
      </Torus>
      
      {/* Inner glow showing circulation */}
      <Sphere args={[r * 0.3, 8, 8]}>
        <meshStandardMaterial
          color={colors.inner}
          emissive={colors.inner}
          emissiveIntensity={0.6}
          transparent
          opacity={0.7}
        />
      </Sphere>
    </group>
  );
}

// ============================================================================
// DEUTERON - Two trefoil toroids with shared electron
// ============================================================================

interface DeuteronProps {
  position: Vector3;
  rotation?: [number, number, number];
  scale?: number;
  showElectronPath?: boolean;
}

/**
 * Deuteron: proton + neutron as two toroids
 * Two toruses with holes aligned poloidally (both pointing same direction)
 * Tilted so their rims touch on one side
 */
function Deuteron({ 
  position, 
  rotation = [0, 0, 0], 
  scale = 1,
  showElectronPath = true 
}: DeuteronProps) {
  const groupRef = useRef<Group>(null);
  const electronRef = useRef<Mesh>(null);
  
  const ringRadius = 0.08 * scale; // Major radius of torus
  const spacing = ringRadius * 1.6; // Gap between centers
  const tiltAngle = Math.PI / 5; // ~36° tilt so rims touch
  
  // Contact point is where the tilted rims meet
  const contactY = ringRadius * Math.sin(tiltAngle);
  
  // Electron circulates around the contact point
  useFrame((state) => {
    if (electronRef.current) {
      const t = state.clock.elapsedTime * 4;
      const r = 0.025 * scale;
      const x = Math.cos(t) * r;
      const y = contactY + Math.sin(t) * r * 0.5;
      const z = Math.sin(t) * r;
      electronRef.current.position.set(x, y, z);
    }
  });
  
  return (
    <group ref={groupRef} position={position} rotation={rotation}>
      {/* Proton torus - left, hole pointing up (+Y), tilted right toward neutron */}
      <group position={[-spacing / 2, 0, 0]} rotation={[0, 0, tiltAngle]}>
        <TrefoilNucleon
          position={new Vector3(0, 0, 0)}
          type="proton"
          rotation={[Math.PI / 2, 0, 0]} // Hole points up (along Y)
          scale={scale}
          spinSpeed={1.2}
        />
      </group>
      
      {/* Neutron torus - right, hole pointing up (+Y), tilted left toward proton */}
      <group position={[spacing / 2, 0, 0]} rotation={[0, 0, -tiltAngle]}>
        <TrefoilNucleon
          position={new Vector3(0, 0, 0)}
          type="neutron"
          rotation={[Math.PI / 2, 0, 0]} // Hole points up (along Y)
          scale={scale}
          spinSpeed={0.9}
        />
      </group>
      
      {/* Shared electron at the contact point where rims touch */}
      {showElectronPath && (
        <Sphere ref={electronRef} args={[0.02 * scale, 8, 8]}>
          <meshStandardMaterial
            color={COLORS.sharedElectron}
            emissive={COLORS.sharedElectron}
            emissiveIntensity={0.8}
          />
        </Sphere>
      )}
    </group>
  );
}

// ============================================================================
// ALPHA PARTICLE - Two deuterons at 90°
// ============================================================================

interface AlphaProps {
  position: Vector3;
  rotation?: [number, number, number];
  scale?: number;
  showElectronPaths?: boolean;
}

/**
 * Alpha particle: two deuterons side by side, one rotated 90°
 * Electron paths run between them
 */
function Alpha({ 
  position, 
  rotation = [0, 0, 0], 
  scale = 1,
  showElectronPaths = true 
}: AlphaProps) {
  const spacing = 0.12 * scale;
  
  return (
    <group position={position} rotation={rotation}>
      {/* First deuteron */}
      <Deuteron
        position={new Vector3(-spacing/2, 0, 0)}
        rotation={[0, 0, 0]}
        scale={scale * 0.8}
        showElectronPath={showElectronPaths}
      />
      
      {/* Second deuteron - rotated 90° */}
      <Deuteron
        position={new Vector3(spacing/2, 0, 0)}
        rotation={[0, 0, Math.PI / 2]} // 90° rotation around Z
        scale={scale * 0.8}
        showElectronPath={showElectronPaths}
      />
    </group>
  );
}

// ============================================================================
// TRI-ALPHA - Two deuterons bridged by neutron: (np)n(np)
// ============================================================================

interface TriAlphaProps {
  position: Vector3;
  rotation?: [number, number, number];
  scale?: number;
  showElectronPaths?: boolean;
}

/**
 * Tri-Alpha (τ): Two deuterons bridged by a neutron
 * Structure: (np)n(np) = 2p + 3n
 * The bridging neutron connects two deuterons
 */
function TriAlpha({ 
  position, 
  rotation = [0, 0, 0], 
  scale = 1,
  showElectronPaths = true 
}: TriAlphaProps) {
  const spacing = 0.15 * scale;
  
  return (
    <group position={position} rotation={rotation}>
      {/* First deuteron */}
      <Deuteron
        position={new Vector3(-spacing, 0, 0)}
        rotation={[0, 0, 0]}
        scale={scale * 0.7}
        showElectronPath={showElectronPaths}
      />
      
      {/* Bridging neutron in the middle */}
      <TrefoilNucleon
        position={new Vector3(0, 0, 0)}
        type="neutron"
        rotation={[Math.PI / 2, 0, 0]}
        scale={scale * 0.8}
        spinSpeed={1.0}
      />
      
      {/* Second deuteron */}
      <Deuteron
        position={new Vector3(spacing, 0, 0)}
        rotation={[0, 0, Math.PI / 2]} // Rotated 90°
        scale={scale * 0.7}
        showElectronPath={showElectronPaths}
      />
    </group>
  );
}

// ============================================================================
// ELECTRON PROBABILITY CLOUDS
// ============================================================================

interface OrbitalCloudProps {
  type: 's' | 'p' | 'd';
  radius: number;
  isValence: boolean;
  electrons: number;
  orientation?: number;
  scale?: number;
}

/**
 * Electron probability cloud - where electrons are experimentally found
 * s: spherical
 * p: dumbbell lobes (3 orientations)
 * d: clover (5 orientations)
 */
function OrbitalCloud({ 
  type, 
  radius, 
  isValence, 
  electrons,
  orientation = 0,
  scale = 1 
}: OrbitalCloudProps) {
  const groupRef = useRef<Group>(null);
  const color = isValence ? COLORS.valenceCloud : COLORS.coreCloud;
  const opacity = isValence ? 0.4 : 0.2;
  const r = radius * scale;
  
  // Subtle pulsing for probability cloud
  useFrame((state) => {
    if (groupRef.current) {
      const pulse = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.05;
      groupRef.current.scale.setScalar(pulse);
    }
  });
  
  if (type === 's') {
    // Spherical s-orbital
    return (
      <group ref={groupRef}>
        <Sphere args={[r * 0.3, 16, 16]}>
          <meshStandardMaterial
            color={color}
            emissive={color}
            emissiveIntensity={isValence ? 0.3 : 0.1}
            transparent
            opacity={opacity}
          />
        </Sphere>
      </group>
    );
  }
  
  if (type === 'p') {
    // Dumbbell p-orbital (two lobes)
    const rotations: [number, number, number][] = [
      [0, 0, 0],                    // pz
      [0, 0, Math.PI / 2],          // px  
      [Math.PI / 2, 0, 0],          // py
    ];
    const rot = rotations[orientation % 3];
    
    return (
      <group ref={groupRef} rotation={rot}>
        {/* Two lobes of dumbbell */}
        <Sphere args={[r * 0.25, 12, 12]} position={[0, r * 0.35, 0]}>
          <meshStandardMaterial
            color={color}
            emissive={color}
            emissiveIntensity={isValence ? 0.3 : 0.1}
            transparent
            opacity={opacity}
          />
        </Sphere>
        <Sphere args={[r * 0.25, 12, 12]} position={[0, -r * 0.35, 0]}>
          <meshStandardMaterial
            color={color}
            emissive={color}
            emissiveIntensity={isValence ? 0.3 : 0.1}
            transparent
            opacity={opacity}
          />
        </Sphere>
      </group>
    );
  }
  
  if (type === 'd') {
    // Clover d-orbital (4 lobes in xy plane for dxy)
    const angle = (orientation % 5) * (Math.PI / 5);
    
    return (
      <group ref={groupRef} rotation={[0, angle, 0]}>
        {[0, 1, 2, 3].map((i) => {
          const a = (i / 4) * Math.PI * 2 + Math.PI / 4;
          return (
            <Sphere 
              key={i} 
              args={[r * 0.2, 10, 10]} 
              position={[Math.cos(a) * r * 0.3, 0, Math.sin(a) * r * 0.3]}
            >
              <meshStandardMaterial
                color={color}
                emissive={color}
                emissiveIntensity={isValence ? 0.3 : 0.1}
                transparent
                opacity={opacity}
              />
            </Sphere>
          );
        })}
      </group>
    );
  }
  
  return null;
}

// ============================================================================
// ELEMENT DATABASE
// ============================================================================

interface ElectronShell {
  n: number;
  subshells: {
    type: 's' | 'p' | 'd' | 'f';
    electrons: number;
    isValence: boolean;
  }[];
}

interface ElementConfig {
  symbol: string;
  name: string;
  Z: number;
  N: number;
  family: string;
  shells: ElectronShell[];
  nuclearStructure: 'proton' | 'deuteron' | 'alpha' | 'alpha-d' | 'multi-alpha' | 'tri-alpha-d';
  alphaCount: number;
  triAlphaCount?: number;
  extraDeuterons: number;
  extraProtons: number;
  extraNeutrons: number;
  description: string;
}

const ELEMENTS: Record<string, ElementConfig> = {
  H: {
    symbol: 'H', name: 'Hydrogen', Z: 1, N: 0,
    family: 'hydrogen',
    shells: [{ n: 1, subshells: [{ type: 's', electrons: 1, isValence: true }] }],
    nuclearStructure: 'proton',
    alphaCount: 0, extraDeuterons: 0, extraProtons: 1, extraNeutrons: 0,
    description: 'Single proton - simplest atom'
  },
  D: {
    symbol: 'D', name: 'Deuterium', Z: 1, N: 1,
    family: 'hydrogen',
    shells: [{ n: 1, subshells: [{ type: 's', electrons: 1, isValence: true }] }],
    nuclearStructure: 'deuteron',
    alphaCount: 0, extraDeuterons: 1, extraProtons: 0, extraNeutrons: 0,
    description: 'Deuteron - proton+neutron with shared electron path'
  },
  He4: {
    symbol: '⁴He', name: 'Helium-4', Z: 2, N: 2,
    family: 'noble-gas',
    shells: [{ n: 1, subshells: [{ type: 's', electrons: 2, isValence: true }] }],
    nuclearStructure: 'alpha',
    alphaCount: 1, extraDeuterons: 0, extraProtons: 0, extraNeutrons: 0,
    description: 'Alpha particle - two deuterons at 90°, complete 1s shell'
  },
  Li7: {
    symbol: '⁷Li', name: 'Lithium-7', Z: 3, N: 4,
    family: 'alkali-metal',
    shells: [
      { n: 1, subshells: [{ type: 's', electrons: 2, isValence: false }] },
      { n: 2, subshells: [{ type: 's', electrons: 1, isValence: true }] }
    ],
    nuclearStructure: 'tri-alpha-d',
    alphaCount: 0, extraDeuterons: 1, extraProtons: 0, extraNeutrons: 0,
    triAlphaCount: 1,
    description: 'Tri-alpha (τ) + deuteron (D) - 1 valence electron in L-shell'
  },
  Be9: {
    symbol: '⁹Be', name: 'Beryllium-9', Z: 4, N: 5,
    family: 'alkaline-earth',
    shells: [
      { n: 1, subshells: [{ type: 's', electrons: 2, isValence: false }] },
      { n: 2, subshells: [{ type: 's', electrons: 2, isValence: true }] }
    ],
    nuclearStructure: 'multi-alpha',
    alphaCount: 2, extraDeuterons: 0, extraProtons: 0, extraNeutrons: 1,
    description: 'Two alphas bridged by neutron - 2 valence electrons'
  },
  C12: {
    symbol: '¹²C', name: 'Carbon-12', Z: 6, N: 6,
    family: 'carbon-group',
    shells: [
      { n: 1, subshells: [{ type: 's', electrons: 2, isValence: false }] },
      { n: 2, subshells: [
        { type: 's', electrons: 2, isValence: true },
        { type: 'p', electrons: 2, isValence: true }
      ]}
    ],
    nuclearStructure: 'multi-alpha',
    alphaCount: 3, extraDeuterons: 0, extraProtons: 0, extraNeutrons: 0,
    description: 'Three alphas in triangle - 4 valence for tetravalent bonding'
  },
  N14: {
    symbol: '¹⁴N', name: 'Nitrogen-14', Z: 7, N: 7,
    family: 'nitrogen-group',
    shells: [
      { n: 1, subshells: [{ type: 's', electrons: 2, isValence: false }] },
      { n: 2, subshells: [
        { type: 's', electrons: 2, isValence: true },
        { type: 'p', electrons: 3, isValence: true }
      ]}
    ],
    nuclearStructure: 'multi-alpha',
    alphaCount: 3, extraDeuterons: 0, extraProtons: 1, extraNeutrons: 1,
    description: 'Three alphas + pn pair - 5 valence electrons'
  },
  O16: {
    symbol: '¹⁶O', name: 'Oxygen-16', Z: 8, N: 8,
    family: 'chalcogen',
    shells: [
      { n: 1, subshells: [{ type: 's', electrons: 2, isValence: false }] },
      { n: 2, subshells: [
        { type: 's', electrons: 2, isValence: true },
        { type: 'p', electrons: 4, isValence: true }
      ]}
    ],
    nuclearStructure: 'multi-alpha',
    alphaCount: 4, extraDeuterons: 0, extraProtons: 0, extraNeutrons: 0,
    description: 'Four alphas in tetrahedron - 6 valence, divalent bonding'
  },
  F19: {
    symbol: '¹⁹F', name: 'Fluorine-19', Z: 9, N: 10,
    family: 'halogen',
    shells: [
      { n: 1, subshells: [{ type: 's', electrons: 2, isValence: false }] },
      { n: 2, subshells: [
        { type: 's', electrons: 2, isValence: true },
        { type: 'p', electrons: 5, isValence: true }
      ]}
    ],
    nuclearStructure: 'multi-alpha',
    alphaCount: 4, extraDeuterons: 0, extraProtons: 1, extraNeutrons: 2,
    description: '7 valence - most electronegative, needs 1 electron'
  },
  Ne20: {
    symbol: '²⁰Ne', name: 'Neon-20', Z: 10, N: 10,
    family: 'noble-gas',
    shells: [
      { n: 1, subshells: [{ type: 's', electrons: 2, isValence: false }] },
      { n: 2, subshells: [
        { type: 's', electrons: 2, isValence: true },
        { type: 'p', electrons: 6, isValence: true }
      ]}
    ],
    nuclearStructure: 'multi-alpha',
    alphaCount: 5, extraDeuterons: 0, extraProtons: 0, extraNeutrons: 0,
    description: 'Five alphas - complete L-shell, chemically inert'
  },
  Na23: {
    symbol: '²³Na', name: 'Sodium-23', Z: 11, N: 12,
    family: 'alkali-metal',
    shells: [
      { n: 1, subshells: [{ type: 's', electrons: 2, isValence: false }] },
      { n: 2, subshells: [
        { type: 's', electrons: 2, isValence: false },
        { type: 'p', electrons: 6, isValence: false }
      ]},
      { n: 3, subshells: [{ type: 's', electrons: 1, isValence: true }] }
    ],
    nuclearStructure: 'multi-alpha',
    alphaCount: 5, extraDeuterons: 0, extraProtons: 1, extraNeutrons: 2,
    description: '1 valence in M-shell - same chemistry as Lithium'
  },
  Cl35: {
    symbol: '³⁵Cl', name: 'Chlorine-35', Z: 17, N: 18,
    family: 'halogen',
    shells: [
      { n: 1, subshells: [{ type: 's', electrons: 2, isValence: false }] },
      { n: 2, subshells: [
        { type: 's', electrons: 2, isValence: false },
        { type: 'p', electrons: 6, isValence: false }
      ]},
      { n: 3, subshells: [
        { type: 's', electrons: 2, isValence: true },
        { type: 'p', electrons: 5, isValence: true }
      ]}
    ],
    nuclearStructure: 'multi-alpha',
    alphaCount: 8, extraDeuterons: 0, extraProtons: 1, extraNeutrons: 2,
    description: '7 valence in M-shell - same chemistry as Fluorine'
  },
  Fe56: {
    symbol: '⁵⁶Fe', name: 'Iron-56', Z: 26, N: 30,
    family: 'transition-metal',
    shells: [
      { n: 1, subshells: [{ type: 's', electrons: 2, isValence: false }] },
      { n: 2, subshells: [
        { type: 's', electrons: 2, isValence: false },
        { type: 'p', electrons: 6, isValence: false }
      ]},
      { n: 3, subshells: [
        { type: 's', electrons: 2, isValence: false },
        { type: 'p', electrons: 6, isValence: false },
        { type: 'd', electrons: 6, isValence: true }
      ]},
      { n: 4, subshells: [{ type: 's', electrons: 2, isValence: true }] }
    ],
    nuclearStructure: 'multi-alpha',
    alphaCount: 14, extraDeuterons: 0, extraProtons: 0, extraNeutrons: 0,
    description: 'Maximum binding energy per nucleon - stellar endpoint'
  },
};

// ============================================================================
// NUCLEUS BUILDER
// ============================================================================

interface NucleusProps {
  config: ElementConfig;
  scale: number;
  showElectronPaths: boolean;
}

function Nucleus({ config, scale, showElectronPaths }: NucleusProps) {
  const groupRef = useRef<Group>(null);
  
  // Nuclear rotation (whole nucleus rotates to match electrons)
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.3;
    }
  });
  
  const alphaSpacing = 0.25 * scale;
  
  // Generate nuclear geometry based on alpha count
  const renderNucleus = () => {
    const elements: JSX.Element[] = [];
    
    if (config.nuclearStructure === 'proton') {
      // Single proton
      elements.push(
        <TrefoilNucleon
          key="proton"
          position={new Vector3(0, 0, 0)}
          type="proton"
          scale={scale}
        />
      );
    } else if (config.nuclearStructure === 'deuteron') {
      // Single deuteron
      elements.push(
        <Deuteron
          key="deuteron"
          position={new Vector3(0, 0, 0)}
          scale={scale}
          showElectronPath={showElectronPaths}
        />
      );
    } else if (config.nuclearStructure === 'alpha') {
      // Single alpha
      elements.push(
        <Alpha
          key="alpha"
          position={new Vector3(0, 0, 0)}
          scale={scale}
          showElectronPaths={showElectronPaths}
        />
      );
    } else if (config.nuclearStructure === 'alpha-d') {
      // Alpha + extra nucleons
      elements.push(
        <Alpha
          key="alpha"
          position={new Vector3(0, 0, 0)}
          scale={scale * 0.9}
          showElectronPaths={showElectronPaths}
        />
      );
      // Extra nucleons attached
      if (config.extraProtons > 0) {
        elements.push(
          <TrefoilNucleon
            key="extra-p"
            position={new Vector3(alphaSpacing, 0, 0)}
            type="proton"
            scale={scale * 0.8}
          />
        );
      }
      for (let i = 0; i < config.extraNeutrons; i++) {
        elements.push(
          <TrefoilNucleon
            key={`extra-n-${i}`}
            position={new Vector3(alphaSpacing, (i + 1) * 0.1 * scale, 0)}
            type="neutron"
            scale={scale * 0.8}
          />
        );
      }
    } else if (config.nuclearStructure === 'tri-alpha-d') {
      // Tri-alpha + deuteron (e.g., Lithium-7)
      // τ = (np)n(np) = 2p + 3n
      // D = 1p + 1n
      // Total: 3p + 4n = Li-7 ✓
      elements.push(
        <TriAlpha
          key="tri-alpha"
          position={new Vector3(0, 0, 0)}
          scale={scale * 0.8}
          showElectronPaths={showElectronPaths}
        />
      );
      // Deuteron attached
      if (config.extraDeuterons > 0) {
        elements.push(
          <Deuteron
            key="extra-d"
            position={new Vector3(alphaSpacing * 1.2, 0, 0)}
            rotation={[0, Math.PI / 4, 0]}
            scale={scale * 0.7}
            showElectronPath={showElectronPaths}
          />
        );
      }
    } else {
      // Multi-alpha arrangement
      const alphaPositions = getAlphaPositions(config.alphaCount, alphaSpacing);
      
      alphaPositions.forEach((pos, i) => {
        elements.push(
          <Alpha
            key={`alpha-${i}`}
            position={pos}
            rotation={[(i * Math.PI) / 4, (i * Math.PI) / 3, 0]}
            scale={scale * 0.6}
            showElectronPaths={showElectronPaths && i < 2}
          />
        );
      });
      
      // Extra nucleons
      if (config.extraProtons > 0 || config.extraNeutrons > 0) {
        const offset = alphaSpacing * Math.max(1, Math.cbrt(config.alphaCount));
        for (let i = 0; i < config.extraProtons; i++) {
          elements.push(
            <TrefoilNucleon
              key={`extra-p-${i}`}
              position={new Vector3(offset + i * 0.1, 0, 0)}
              type="proton"
              scale={scale * 0.5}
            />
          );
        }
        for (let i = 0; i < config.extraNeutrons; i++) {
          elements.push(
            <TrefoilNucleon
              key={`extra-n-${i}`}
              position={new Vector3(offset, (i + 1) * 0.08 * scale, 0)}
              type="neutron"
              scale={scale * 0.5}
            />
          );
        }
      }
    }
    
    return elements;
  };
  
  return (
    <group ref={groupRef}>
      {renderNucleus()}
    </group>
  );
}

/**
 * Generate positions for multiple alpha particles
 * Following SDT packing rules:
 * - 2 alphas: linear or bridged
 * - 3 alphas: triangle
 * - 4 alphas: tetrahedron
 * - 5+ alphas: extending structures
 */
function getAlphaPositions(count: number, spacing: number): Vector3[] {
  const positions: Vector3[] = [];
  
  if (count === 1) {
    positions.push(new Vector3(0, 0, 0));
  } else if (count === 2) {
    positions.push(new Vector3(-spacing/2, 0, 0));
    positions.push(new Vector3(spacing/2, 0, 0));
  } else if (count === 3) {
    // Triangle
    const r = spacing * 0.6;
    for (let i = 0; i < 3; i++) {
      const angle = (i / 3) * Math.PI * 2 - Math.PI / 2;
      positions.push(new Vector3(Math.cos(angle) * r, 0, Math.sin(angle) * r));
    }
  } else if (count === 4) {
    // Tetrahedron
    const a = spacing * 0.5;
    positions.push(new Vector3(a, a, a));
    positions.push(new Vector3(-a, -a, a));
    positions.push(new Vector3(-a, a, -a));
    positions.push(new Vector3(a, -a, -a));
  } else {
    // Extended structure - build from tetrahedron + additions
    const a = spacing * 0.5;
    positions.push(new Vector3(0, 0, 0));
    for (let i = 1; i < count; i++) {
      const layer = Math.floor((i - 1) / 6);
      const idx = (i - 1) % 6;
      const r = spacing * (0.8 + layer * 0.4);
      const phi = (idx / 6) * Math.PI * 2;
      const theta = Math.PI / 2 + (layer % 2) * 0.3;
      positions.push(new Vector3(
        r * Math.sin(theta) * Math.cos(phi),
        r * Math.cos(theta),
        r * Math.sin(theta) * Math.sin(phi)
      ));
    }
  }
  
  return positions;
}

// ============================================================================
// SHELL RADII
// ============================================================================

const SHELL_RADII = {
  1: 0.5,   // K shell
  2: 0.9,   // L shell
  3: 1.3,   // M shell
  4: 1.7,   // N shell
};

// ============================================================================
// MAIN VISUALIZER
// ============================================================================

export interface AtomicStructureVisualizerProps {
  element: keyof typeof ELEMENTS;
  showElectrons?: boolean;
  showLabels?: boolean;
  scale?: number;
}

export default function AtomicStructureVisualizer({
  element,
  showElectrons = true,
  showLabels = true,
  scale = 1,
}: AtomicStructureVisualizerProps) {
  const config = ELEMENTS[element];
  const groupRef = useRef<Group>(null);
  
  if (!config) return null;
  
  // Count valence electrons
  const valenceCount = config.shells.reduce((sum, shell) => 
    sum + shell.subshells.filter(s => s.isValence).reduce((s, sub) => s + sub.electrons, 0), 0
  );
  
  const familyColor = FAMILY_COLORS[config.family] || new Color(0xffffff);
  
  return (
    <group ref={groupRef}>
      {/* Nucleus - rotates as whole */}
      <Nucleus 
        config={config} 
        scale={scale} 
        showElectronPaths={showElectrons}
      />
      
      {/* Electron probability clouds - where electrons are found */}
      {showElectrons && config.shells.map((shell, shellIdx) => {
        const baseRadius = SHELL_RADII[shell.n as keyof typeof SHELL_RADII] || (1.7 + (shell.n - 4) * 0.4);
        let subshellOffset = 0;
        
        return (
          <group key={`shell-${shell.n}`}>
            {shell.subshells.map((subshell, subIdx) => {
              const radius = baseRadius + subshellOffset;
              subshellOffset += 0.15;
              
              // Generate orbital clouds based on subshell type
              const clouds: JSX.Element[] = [];
              
              if (subshell.type === 's') {
                clouds.push(
                  <OrbitalCloud
                    key={`${shell.n}s`}
                    type="s"
                    radius={radius}
                    isValence={subshell.isValence}
                    electrons={subshell.electrons}
                    scale={scale}
                  />
                );
              } else if (subshell.type === 'p') {
                // Three p orbitals along x, y, z
                const occupiedOrbitals = Math.ceil(subshell.electrons / 2);
                for (let i = 0; i < occupiedOrbitals; i++) {
                  clouds.push(
                    <OrbitalCloud
                      key={`${shell.n}p-${i}`}
                      type="p"
                      radius={radius}
                      isValence={subshell.isValence}
                      electrons={Math.min(2, subshell.electrons - i * 2)}
                      orientation={i}
                      scale={scale}
                    />
                  );
                }
              } else if (subshell.type === 'd') {
                // Five d orbitals
                const occupiedOrbitals = Math.ceil(subshell.electrons / 2);
                for (let i = 0; i < Math.min(occupiedOrbitals, 5); i++) {
                  clouds.push(
                    <OrbitalCloud
                      key={`${shell.n}d-${i}`}
                      type="d"
                      radius={radius}
                      isValence={subshell.isValence}
                      electrons={Math.min(2, subshell.electrons - i * 2)}
                      orientation={i}
                      scale={scale}
                    />
                  );
                }
              }
              
              return clouds;
            })}
          </group>
        );
      })}
      
      {/* Family indicator */}
      <Torus 
        args={[0.2 * scale, 0.015 * scale, 8, 32]} 
        rotation={[Math.PI / 2, 0, 0]}
        position={[0, -1.5 * scale, 0]}
      >
        <meshStandardMaterial 
          color={familyColor} 
          emissive={familyColor}
          emissiveIntensity={0.5}
        />
      </Torus>
      
      {/* Labels */}
      {showLabels && (
        <Html position={[0, -1.8 * scale, 0]} center>
          <div style={{ 
            textAlign: 'center', 
            color: 'white', 
            fontSize: '14px',
            fontFamily: 'system-ui',
            textShadow: '0 0 10px rgba(0,0,0,0.8)'
          }}>
            <div style={{ fontSize: '18px', fontWeight: 'bold' }}>{config.symbol}</div>
            <div style={{ fontSize: '10px', opacity: 0.7 }}>{valenceCount}e⁻ valence</div>
          </div>
        </Html>
      )}
    </group>
  );
}

export { ELEMENTS, FAMILY_COLORS };
export type { ElementConfig };
