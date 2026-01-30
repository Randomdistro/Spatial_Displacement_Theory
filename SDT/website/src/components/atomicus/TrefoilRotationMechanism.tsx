/**
 * Trefoil Rotation Mechanism Visualization
 * 
 * Shows individual nucleon spin vs. whole nucleus rotation
 */

import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Group, Mesh, Vector3 } from 'three';
import { Line, Text } from '@react-three/drei';
import { TrefoilStructure } from '../../data/trefoilStructures';

const COLORS = {
  rotationAxis: 0xffffff,
  individualSpin: 0x00ff00,
  nuclearRotation: 0xff00ff,
};

interface TrefoilRotationMechanismProps {
  structure: TrefoilStructure;
  showIndividualSpin?: boolean;
  showNuclearRotation?: boolean;
  showRotationAxis?: boolean;
  animationSpeed?: number;
  scale?: number;
}

export default function TrefoilRotationMechanism({
  structure,
  showIndividualSpin = true,
  showNuclearRotation = true,
  showRotationAxis = true,
  animationSpeed = 1,
  scale = 1
}: TrefoilRotationMechanismProps) {
  const nuclearGroupRef = useRef<Group>(null);
  const individualSpinsRef = useRef<Mesh[]>([]);

  // Nuclear rotation (whole nucleus)
  useFrame((state) => {
    if (nuclearGroupRef.current && showNuclearRotation) {
      const speed = structure.nuclear_rotation_frequency / 1e10 * animationSpeed;
      nuclearGroupRef.current.rotation.y = state.clock.elapsedTime * speed * 0.01;
    }

    // Individual nucleon spins (in-place rotation)
    if (showIndividualSpin) {
      structure.nucleons.forEach((nucleon, index) => {
        const mesh = individualSpinsRef.current[index];
        if (mesh) {
          const speed = (nucleon.rotation_frequency / 6.57e23) * 0.05 * animationSpeed;
          const direction = nucleon.chirality === 'R' ? 1 : -1;
          mesh.rotation.z += speed * direction;
        }
      });
    }
  });

  const [ax, ay, az] = structure.nuclear_rotation_axis;
  const axisVector = new Vector3(ax, ay, az).normalize();
  const axisLength = 2 * scale;

  return (
    <group ref={nuclearGroupRef}>
      {/* Rotation axis visualization */}
      {showRotationAxis && (
        <>
          <Line
            points={[
              [0, 0, 0],
              [axisVector.x * axisLength, axisVector.y * axisLength, axisVector.z * axisLength]
            ]}
            color={COLORS.rotationAxis}
            lineWidth={3}
            dashed
          />
          <Text
            position={[
              axisVector.x * axisLength * 1.2,
              axisVector.y * axisLength * 1.2,
              axisVector.z * axisLength * 1.2
            ]}
            fontSize={0.1 * scale}
            color={COLORS.rotationAxis}
          >
            Rotation Axis
          </Text>
        </>
      )}

      {/* Individual spin indicators */}
      {showIndividualSpin && structure.nucleons.map((nucleon, index) => {
        const position = new Vector3(
          nucleon.x * 0.1,
          nucleon.y * 0.1,
          nucleon.z * 0.1
        );

        return (
          <group key={index} position={position}>
            {/* Spin indicator ring */}
            <mesh
              ref={(el) => {
                if (el) individualSpinsRef.current[index] = el;
              }}
            >
              <torusGeometry args={[0.05 * scale, 0.01 * scale, 8, 16]} />
              <meshStandardMaterial
                color={COLORS.individualSpin}
                emissive={COLORS.individualSpin}
                emissiveIntensity={0.5}
              />
            </mesh>
          </group>
        );
      })}

      {/* Nuclear rotation indicator */}
      {showNuclearRotation && (
        <group>
          <mesh>
            <ringGeometry args={[1.5 * scale, 1.6 * scale, 32]} />
            <meshStandardMaterial
              color={COLORS.nuclearRotation}
              emissive={COLORS.nuclearRotation}
              emissiveIntensity={0.3}
              transparent
              opacity={0.5}
            />
          </mesh>
        </group>
      )}
    </group>
  );
}
