/**
 * Codemonkey Agent: Node Connector Component
 * Draws visual connections between nodes in a path
 */

import React from 'react';
import { Line } from '@react-three/drei';
import { Color } from 'three';

export interface NodeConnectorProps {
  from: [number, number, number];
  to: [number, number, number];
  color?: Color | string | number;
  opacity?: number;
}

/**
 * NodeConnector - Draws a line connecting two nodes
 */
export default function NodeConnector({
  from,
  to,
  color = 0x4299e1,
  opacity = 0.3,
}: NodeConnectorProps) {
  return (
    <Line
      points={[from, to]}
      color={color}
      lineWidth={2}
      transparent
      opacity={opacity}
      dashed={false}
    />
  );
}

