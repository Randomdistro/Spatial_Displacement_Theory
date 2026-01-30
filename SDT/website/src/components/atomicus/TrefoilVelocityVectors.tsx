/**
 * Trefoil Velocity Vector Visualization
 * 
 * Shows velocity vectors for all nucleons with three-speed system coloring
 */

import React from 'react';
import { Vector3 } from 'three';
import { Line } from '@react-three/drei';
import { NucleonPosition } from '../../data/trefoilStructures';

const COLORS = {
  velocityV1: 0xff6b00,  // Orange (fastest, v₁=2.23c)
  velocityV2: 0xffd700,  // Gold (average, v₂=1.84c)
  velocityV3: 0x4fc3f7,  // Light blue (slowest, v₃=0.395c)
};

const FM_TO_UNITS = 0.1;

interface TrefoilVelocityVectorsProps {
  nucleons: NucleonPosition[];
  scale?: number;
  showV1?: boolean;
  showV2?: boolean;
  showV3?: boolean;
}

export default function TrefoilVelocityVectors({
  nucleons,
  scale = 1,
  showV1 = true,
  showV2 = true,
  showV3 = true
}: TrefoilVelocityVectorsProps) {
  const vectors: JSX.Element[] = [];

  nucleons.forEach((nucleon, index) => {
    const position = new Vector3(
      nucleon.x * FM_TO_UNITS,
      nucleon.y * FM_TO_UNITS,
      nucleon.z * FM_TO_UNITS
    );

    // Three velocity vectors (perihelion, average, aphelion)
    if (showV1) {
      const v1Length = nucleon.velocity_v1 * 0.1 * scale;
      const v1End = position.clone().add(new Vector3(1, 0, 0).multiplyScalar(v1Length));
      vectors.push(
        <Line
          key={`${index}-v1`}
          points={[position, v1End]}
          color={COLORS.velocityV1}
          lineWidth={3}
        />
      );
    }

    if (showV2) {
      const v2Length = nucleon.velocity_v2 * 0.1 * scale;
      const v2End = position.clone().add(new Vector3(0, 1, 0).multiplyScalar(v2Length));
      vectors.push(
        <Line
          key={`${index}-v2`}
          points={[position, v2End]}
          color={COLORS.velocityV2}
          lineWidth={2}
        />
      );
    }

    if (showV3) {
      const v3Length = nucleon.velocity_v3 * 0.1 * scale;
      const v3End = position.clone().add(new Vector3(-1, 0, 0).multiplyScalar(v3Length));
      vectors.push(
        <Line
          key={`${index}-v3`}
          points={[position, v3End]}
          color={COLORS.velocityV3}
          lineWidth={1}
        />
      );
    }
  });

  return <>{vectors}</>;
}
