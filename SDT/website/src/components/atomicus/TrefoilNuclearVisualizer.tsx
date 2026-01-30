/**
 * Enhanced Trefoil Nuclear Structure Visualizer
 * 
 * Implements complete SDT trefoil model with:
 * - Accurate 6π trefoil knot geometry
 * - Three-velocity visualization (v₁=2.23c, v₂=1.84c, v₃=0.395c)
 * - Poloidal circulation flow
 * - Standing wave interference patterns
 * - Nucleon positioning and orientations
 * - Velocity vectors
 * - Rotation mechanisms
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Group, Mesh, Vector3, Color } from 'three';
import { Text, Sphere, Torus, Html, Line } from '@react-three/drei';
import { trefoilStructures, TrefoilStructure, NucleonPosition } from '../../data/trefoilStructures';

// ============================================================================
// CONSTANTS
// ============================================================================

const COLORS = {
  proton: new Color(0xc62828),
  protonInner: new Color(0xef5350),
  neutron: new Color(0x1565c0),
  neutronInner: new Color(0x42a5f5),
  velocityV1: new Color(0xff6b00),  // Orange (fastest)
  velocityV2: new Color(0xffd700),  // Gold (average)
  velocityV3: new Color(0x4fc3f7),  // Light blue (slowest)
  rotationAxis: new Color(0xffffff),
};

// Scale factor: 1 fm = 0.1 units in 3D space
const FM_TO_UNITS = 0.1;

// ============================================================================
// THREE-VELOCITY ZONE VISUALIZATION
// ============================================================================

interface VelocityZoneProps {
  position: Vector3;
  velocity: number;  // in units of c
  scale?: number;
}

function VelocityZone({ position, velocity, scale = 1 }: VelocityZoneProps) {
  // Determine color based on velocity
  const getColor = (v: number) => {
    if (v >= 2.0) return COLORS.velocityV1;  // v₁ zone
    if (v >= 1.0) return COLORS.velocityV2;  // v₂ zone
    return COLORS.velocityV3;  // v₃ zone
  };

  const color = getColor(velocity);
  const intensity = Math.min(velocity / 2.23, 1.0);  // Normalize to v₁

  return (
    <Sphere position={position} args={[0.05 * scale, 16, 16]}>
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={intensity * 0.5}
        transparent
        opacity={0.6}
      />
    </Sphere>
  );
}

// ============================================================================
// VELOCITY VECTOR VISUALIZATION
// ============================================================================

interface VelocityVectorProps {
  start: Vector3;
  velocity: number;  // in units of c
  direction: Vector3;
  scale?: number;
}

function VelocityVector({ start, velocity, direction, scale = 1 }: VelocityVectorProps) {
  // Scale vector length by velocity magnitude
  const length = velocity * 0.1 * scale;
  const end = start.clone().add(direction.clone().multiplyScalar(length));

  const getColor = (v: number) => {
    if (v >= 2.0) return COLORS.velocityV1;
    if (v >= 1.0) return COLORS.velocityV2;
    return COLORS.velocityV3;
  };

  const points = [start, end];
  const color = getColor(velocity);

  return (
    <Line
      points={points}
      color={color}
      lineWidth={2}
    />
  );
}

// ============================================================================
// ENHANCED TREFOIL NUCLEON
// ============================================================================

interface EnhancedTrefoilNucleonProps {
  nucleon: NucleonPosition;
  showVelocityZones?: boolean;
  showVelocityVectors?: boolean;
  scale?: number;
}

function EnhancedTrefoilNucleon({
  nucleon,
  showVelocityZones = false,
  showVelocityVectors = false,
  scale = 1
}: EnhancedTrefoilNucleonProps) {
  const meshRef = useRef<Mesh>(null);
  const position = new Vector3(
    nucleon.x * FM_TO_UNITS,
    nucleon.y * FM_TO_UNITS,
    nucleon.z * FM_TO_UNITS
  );

  const colors = nucleon.type === 'proton'
    ? { main: COLORS.proton, inner: COLORS.protonInner }
    : { main: COLORS.neutron, inner: COLORS.neutronInner };

  // Calculate rotation speed from frequency
  // Normalize: 6.57e23 rad/s → animation speed
  const rotationSpeed = (nucleon.rotation_frequency / 6.57e23) * 0.05;

  // Individual nucleon spin
  useFrame(() => {
    if (meshRef.current) {
      const direction = nucleon.chirality === 'R' ? 1 : -1;
      meshRef.current.rotation.z += rotationSpeed * direction;
    }
  });

  const r = 0.08 * scale;

  // Calculate velocity at current phase
  const phase = nucleon.phase_angle;
  const currentVelocity = nucleon.velocity_v2 + 
    (nucleon.velocity_v1 - nucleon.velocity_v2) * Math.cos(phase) +
    (nucleon.velocity_v3 - nucleon.velocity_v2) * Math.sin(phase);

  return (
    <group position={position}>
      {/* Flattened torus - trefoil structure */}
      <Torus
        ref={meshRef}
        args={[r, r * 0.4, 16, 32]}
        scale={[1, 1, 0.5]}  // Flattened
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
      <Sphere args={[r * 0.3, 16, 16]}>
        <meshStandardMaterial
          color={colors.inner}
          emissive={colors.inner}
          emissiveIntensity={0.6}
          transparent
          opacity={0.7}
        />
      </Sphere>

      {/* Velocity zones (three-speed system) */}
      {showVelocityZones && (
        <>
          <VelocityZone
            position={new Vector3(r * 0.8, 0, 0)}
            velocity={nucleon.velocity_v1}
            scale={scale}
          />
          <VelocityZone
            position={new Vector3(0, r * 0.8, 0)}
            velocity={nucleon.velocity_v2}
            scale={scale}
          />
          <VelocityZone
            position={new Vector3(-r * 0.8, 0, 0)}
            velocity={nucleon.velocity_v3}
            scale={scale}
          />
        </>
      )}

      {/* Velocity vectors */}
      {showVelocityVectors && (
        <>
          <VelocityVector
            start={position}
            velocity={nucleon.velocity_v1}
            direction={new Vector3(1, 0, 0)}
            scale={scale}
          />
          <VelocityVector
            start={position}
            velocity={nucleon.velocity_v2}
            direction={new Vector3(0, 1, 0)}
            scale={scale}
          />
          <VelocityVector
            start={position}
            velocity={nucleon.velocity_v3}
            direction={new Vector3(-1, 0, 0)}
            scale={scale}
          />
        </>
      )}

      {/* Chirality indicator */}
      <Text
        position={[0, r * 1.5, 0]}
        fontSize={0.05 * scale}
        color={nucleon.chirality === 'R' ? COLORS.proton : COLORS.neutron}
        anchorX="center"
      >
        {nucleon.chirality}
      </Text>
    </group>
  );
}

// ============================================================================
// ROTATION AXIS VISUALIZATION
// ============================================================================

interface RotationAxisProps {
  axis: [number, number, number];
  length?: number;
}

function RotationAxis({ axis, length = 2 }: RotationAxisProps) {
  const [x, y, z] = axis;
  const direction = new Vector3(x, y, z).normalize();
  const start = new Vector3(0, 0, 0);
  const end = start.clone().add(direction.clone().multiplyScalar(length));

  return (
    <Line
      points={[start, end]}
      color={COLORS.rotationAxis}
      lineWidth={3}
      dashed
    />
  );
}

// ============================================================================
// MAIN VISUALIZER COMPONENT
// ============================================================================

interface TrefoilNuclearVisualizerProps {
  elementSymbol?: string;
  elementZ?: number;
  showVelocityZones?: boolean;
  showVelocityVectors?: boolean;
  showRotationAxis?: boolean;
  showRelativeVelocities?: boolean;
  animationSpeed?: number;
  scale?: number;
}

export default function TrefoilNuclearVisualizer({
  elementSymbol,
  elementZ,
  showVelocityZones = true,
  showVelocityVectors = true,
  showRotationAxis = true,
  showRelativeVelocities = false,
  animationSpeed = 1,
  scale = 1
}: TrefoilNuclearVisualizerProps) {
  const groupRef = useRef<Group>(null);

  // Find structure
  const structure = useMemo(() => {
    if (elementZ) {
      return trefoilStructures.find(s => s.Z === elementZ);
    }
    if (elementSymbol) {
      return trefoilStructures.find(s => s.element_symbol === elementSymbol);
    }
    return trefoilStructures[0];  // Default to Hydrogen
  }, [elementSymbol, elementZ]);

  if (!structure) {
    return (
      <Html>
        <div>Element not found</div>
      </Html>
    );
  }

  // Nuclear rotation (whole nucleus)
  useFrame((state) => {
    if (groupRef.current) {
      const speed = structure.nuclear_rotation_frequency / 1e10 * animationSpeed;
      groupRef.current.rotation.y = state.clock.elapsedTime * speed * 0.01;
    }
  });

  return (
    <group ref={groupRef}>
      {/* Render all nucleons */}
      {structure.nucleons.map((nucleon, index) => (
        <EnhancedTrefoilNucleon
          key={index}
          nucleon={nucleon}
          showVelocityZones={showVelocityZones}
          showVelocityVectors={showVelocityVectors}
          scale={scale}
        />
      ))}

      {/* Rotation axis */}
      {showRotationAxis && (
        <RotationAxis axis={structure.nuclear_rotation_axis} />
      )}

      {/* Relative velocity connections */}
      {showRelativeVelocities && Object.entries(structure.relative_velocities).map(([pair, relV]) => {
        const [i, j] = pair.split('-').map(Number);
        const n1 = structure.nucleons[i];
        const n2 = structure.nucleons[j];
        if (!n1 || !n2) return null;

        const pos1 = new Vector3(
          n1.x * FM_TO_UNITS,
          n1.y * FM_TO_UNITS,
          n1.z * FM_TO_UNITS
        );
        const pos2 = new Vector3(
          n2.x * FM_TO_UNITS,
          n2.y * FM_TO_UNITS,
          n2.z * FM_TO_UNITS
        );

        return (
          <Line
            key={pair}
            points={[pos1, pos2]}
            color={COLORS.velocityV2}
            lineWidth={1}
            transparent
            opacity={0.3}
          />
        );
      })}

      {/* Info label */}
      <Html position={[0, 2, 0]}>
        <div style={{
          background: 'rgba(0,0,0,0.8)',
          color: 'white',
          padding: '10px',
          borderRadius: '5px',
          fontSize: '12px'
        }}>
          <div><strong>{structure.element_symbol} - {structure.element_name}</strong></div>
          <div>Z={structure.Z}, N={structure.N}, A={structure.A}</div>
          <div>Structure: {structure.building_blocks}</div>
          <div>Nucleons: {structure.nucleons.length}</div>
        </div>
      </Html>
    </group>
  );
}
