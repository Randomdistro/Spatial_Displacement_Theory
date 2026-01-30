/**
 * Pressure Field 3D Visualization
 * Shows CMB pressure field and gradients that drive all forces in SDT
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface PressureFieldProps {
  showCMB?: boolean;
  showGradients?: boolean;
  showOcclusion?: boolean;
  animated?: boolean;
  scale?: number;
}

export default function PressureField({
  showCMB = true,
  showGradients = true,
  showOcclusion = false,
  animated = true,
  scale = 1
}: PressureFieldProps) {
  const groupRef = useRef<THREE.Group>(null);

  // Generate pressure field points
  const pressureField = useMemo(() => {
    const points: { position: THREE.Vector3; pressure: number; gradient: THREE.Vector3 }[] = [];
    const gridSize = 20;
    const spacing = 0.1 * scale;

    for (let x = -gridSize/2; x <= gridSize/2; x++) {
      for (let y = -gridSize/2; y <= gridSize/2; y++) {
        for (let z = -gridSize/2; z <= gridSize/2; z++) {
          const pos = new THREE.Vector3(x * spacing, y * spacing, z * spacing);
          const distance = pos.length();

          if (distance < gridSize * spacing / 2) {
            // CMB pressure: P ∝ 1/r² (spherical spreading)
            let pressure = 0;
            if (showCMB) {
              pressure = 1 / (distance * distance + 0.1); // Avoid singularity
            }

            // Add occlusion effects
            if (showOcclusion && distance < 0.3 * scale) {
              // Matter creates pressure deficit
              pressure *= (1 - Math.exp(-distance * 10));
            }

            // Calculate pressure gradient
            const gradient = new THREE.Vector3();
            if (showGradients && distance > 0.01) {
              const gradMagnitude = -2 * pressure / distance; // d(1/r²)/dr = -2/r³
              gradient.copy(pos).normalize().multiplyScalar(gradMagnitude);
            }

            points.push({ position: pos, pressure, gradient });
          }
        }
      }
    }

    return points;
  }, [showCMB, showGradients, showOcclusion, scale]);

  useFrame((state) => {
    if (!groupRef.current || !animated) return;

    // Gentle rotation to show 3D nature
    groupRef.current.rotation.y = state.clock.elapsedTime * 0.1;
    groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.05) * 0.1;
  });

  // Get pressure color based on intensity
  const getPressureColor = (pressure: number): string => {
    const intensity = Math.min(pressure * 100, 1);
    const r = Math.floor(255 * intensity);
    const g = Math.floor(100 * (1 - intensity));
    const b = Math.floor(255 * (1 - intensity));
    return `rgb(${r}, ${g}, ${b})`;
  };

  return (
    <div className="w-full h-96 bg-slate-900 rounded-lg border border-slate-700 relative">
      <div className="absolute top-4 left-4 text-white text-sm font-medium">
        Spation Pressure Field
      </div>
      <div className="absolute top-4 right-4 text-slate-400 text-xs">
        CMB-Driven Forces
      </div>

      {/* 3D Scene */}
      <div className="w-full h-full flex items-center justify-center">
        <div className="relative w-80 h-80">
          {/* Pressure field visualization */}
          <div className="absolute inset-0">
            {pressureField.slice(0, 1000).map((point, i) => (
              <div
                key={i}
                className="absolute w-1 h-1 rounded-full"
                style={{
                  left: `${50 + point.position.x * 200}%`,
                  top: `${50 + point.position.z * 200}%`,
                  backgroundColor: getPressureColor(point.pressure),
                  opacity: Math.min(point.pressure * 10, 0.8),
                  transform: 'translate(-50%, -50%)',
                  boxShadow: point.pressure > 0.1 ? `0 0 2px ${getPressureColor(point.pressure)}` : 'none'
                }}
              />
            ))}
          </div>

          {/* CMB radiation visualization */}
          {showCMB && (
            <div className="absolute inset-0">
              <div
                className="absolute rounded-full border border-yellow-500/20"
                style={{
                  width: '400px',
                  height: '400px',
                  left: '50%',
                  top: '50%',
                  transform: 'translate(-50%, -50%)',
                  background: 'radial-gradient(circle, rgba(245, 158, 11, 0.05) 0%, transparent 50%)'
                }}
              />
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-yellow-400 text-xs">
                CMB Radiation
              </div>
            </div>
          )}

          {/* Pressure gradients */}
          {showGradients && pressureField.slice(0, 50).map((point, i) => {
            if (point.gradient.length() < 0.01) return null;

            const gradLength = point.gradient.length() * 50;
            const gradAngle = Math.atan2(point.gradient.z, point.gradient.x);

            return (
              <div
                key={`grad-${i}`}
                className="absolute border-l-2 border-r-2 border-red-400"
                style={{
                  width: `${Math.min(gradLength, 20)}px`,
                  height: '1px',
                  left: `${50 + point.position.x * 200}%`,
                  top: `${50 + point.position.z * 200}%`,
                  transform: `translate(-50%, -50%) rotate(${gradAngle}rad)`,
                  transformOrigin: 'left center',
                  opacity: 0.6
                }}
              />
            );
          })}

          {/* Matter occlusion */}
          {showOcclusion && (
            <div
              className="absolute rounded-full border-2 border-slate-600"
              style={{
                width: '60px',
                height: '60px',
                left: '50%',
                top: '50%',
                transform: 'translate(-50%, -50%)',
                background: 'radial-gradient(circle, rgba(100, 116, 139, 0.3) 0%, transparent 70%)'
              }}
            >
              <div className="absolute inset-0 flex items-center justify-center text-slate-300 text-xs">
                Matter
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="absolute bottom-4 left-4 right-4 flex justify-between text-xs text-slate-500">
        <span>
          {showCMB && 'CMB influx • '}
          {showGradients && 'Pressure gradients • '}
          {showOcclusion && 'Matter occlusion'}
        </span>
        <span>Force = -V ∇P</span>
      </div>

      {/* Color legend */}
      <div className="absolute bottom-12 right-4 text-xs text-slate-600">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-red-500 rounded"></div>
          <span>High Pressure</span>
        </div>
        <div className="flex items-center gap-2 mt-1">
          <div className="w-3 h-3 bg-blue-500 rounded"></div>
          <span>Low Pressure</span>
        </div>
      </div>
    </div>
  );
}

