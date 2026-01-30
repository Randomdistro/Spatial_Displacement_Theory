/**
 * Spation Lattice 3D Visualization
 * Visualizes the dodecahedral packing structure of the spation medium
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface SpationLatticeProps {
  showPacking?: boolean;
  showPressure?: boolean;
  scale?: number;
  animated?: boolean;
}

export default function SpationLattice({
  showPacking = true,
  showPressure = false,
  scale = 1,
  animated = true,
}: SpationLatticeProps) {
  const groupRef = useRef<THREE.Group>(null);
  const timeRef = useRef(0);

  // Create dodecahedral packing structure
  const geometry = useMemo(() => {
    // Simplified representation - in full implementation would show actual dodecahedral packing
    const geo = new THREE.IcosahedronGeometry(0.1 * scale, 0);
    return geo;
  }, [scale]);

  useFrame((state, delta) => {
    if (!groupRef.current || !animated) return;
    
    timeRef.current += delta;
    
    // Subtle rotation
    groupRef.current.rotation.y = timeRef.current * 0.1;
    groupRef.current.rotation.x = Math.sin(timeRef.current * 0.05) * 0.1;
  });

  // Generate dodecahedral lattice points
  const latticePoints = useMemo(() => {
    const points: THREE.Vector3[] = [];
    const layers = showPacking ? 5 : 3;

    // Simple cubic lattice approximation for visualization
    for (let x = -layers; x <= layers; x++) {
      for (let y = -layers; y <= layers; y++) {
        for (let z = -layers; z <= layers; z++) {
          const distance = Math.sqrt(x*x + y*y + z*z);
          if (distance <= layers && distance > 0.5) {
            points.push(new THREE.Vector3(x * 0.15 * scale, y * 0.15 * scale, z * 0.15 * scale));
          }
        }
      }
    }

    return points;
  }, [showPacking, scale]);

  return (
    <div className="w-full h-96 bg-slate-900 rounded-lg border border-slate-700 relative">
      <div className="absolute top-4 left-4 text-white text-sm font-medium">
        Spation Lattice Structure
      </div>
      <div className="absolute top-4 right-4 text-slate-400 text-xs">
        Icosa-dodecahedral Packing
      </div>

      {/* 3D Scene visualization */}
      <div className="w-full h-full flex items-center justify-center">
        <div className="relative w-64 h-64">
          {/* Spation spheres */}
          <div className="absolute inset-0">
            {latticePoints.slice(0, 100).map((point, i) => (
              <div
                key={i}
                className="absolute w-2 h-2 bg-cyan-400 rounded-full border border-cyan-300/50"
                style={{
                  left: `${50 + point.x * 100}%`,
                  top: `${50 + point.z * 100}%`,
                  transform: 'translate(-50%, -50%)',
                  boxShadow: '0 0 4px rgba(34, 211, 238, 0.3)',
                  opacity: 0.8
                }}
              />
            ))}
          </div>

          {/* Pressure field overlay */}
          {showPressure && (
            <div
              className="absolute inset-0 rounded-full"
              style={{
                background: 'radial-gradient(circle, rgba(239, 68, 68, 0.1) 0%, rgba(34, 197, 94, 0.05) 50%, transparent 70%)'
              }}
            />
          )}

          {/* Central spation highlight */}
          <div
            className="absolute w-4 h-4 bg-cyan-300 rounded-full border-2 border-cyan-200"
            style={{
              left: '50%',
              top: '50%',
              transform: 'translate(-50%, -50%)',
              boxShadow: '0 0 12px rgba(34, 211, 238, 0.6)'
            }}
          />
        </div>
      </div>

      <div className="absolute bottom-4 left-4 right-4 flex justify-between text-xs text-slate-500">
        <span>12-fold coordination</span>
        <span>Pressure propagation medium</span>
      </div>

      <div className="absolute bottom-12 left-4 text-xs text-slate-600">
        Planck scale: {scale} × λ_P
      </div>
    </div>
  );
}
