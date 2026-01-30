/**
 * Helical Orbitals 3D Visualization
 * Shows electron orbitals as helical standing waves on toroidal surfaces
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface HelicalOrbitalsProps {
  element?: string;
  orbital?: string;
  animated?: boolean;
  showWaveFunction?: boolean;
  scale?: number;
}

export default function HelicalOrbitals({
  element = 'Hydrogen',
  orbital = '1s',
  animated = true,
  showWaveFunction = true,
  scale = 1
}: HelicalOrbitalsProps) {
  const groupRef = useRef<THREE.Group>(null);

  // Parse orbital quantum numbers
  const orbitalConfig = useMemo(() => {
    const match = orbital.match(/(\d+)([spdf])(\d*)/);
    if (!match) return { n: 1, l: 0, m: 0 };

    const n = parseInt(match[1]);
    const l = 'spdf'.indexOf(match[2]);
    const m = match[3] ? parseInt(match[3]) : 0;

    return { n, l, m };
  }, [orbital]);

  // Generate helical wave pattern
  const helicalPath = useMemo(() => {
    const points: THREE.Vector3[] = [];
    const segments = 200;
    const radius = 0.3 * scale;
    const height = 0.2 * scale;
    const turns = orbitalConfig.n; // Number of turns relates to principal quantum number

    for (let i = 0; i <= segments; i++) {
      const t = (i / segments) * Math.PI * 2 * turns;
      const x = radius * Math.cos(t);
      const y = (height / turns) * (t / (Math.PI * 2));
      const z = radius * Math.sin(t);

      // Add wave modulation based on orbital type
      const waveAmplitude = showWaveFunction ? 0.05 * Math.sin(t * orbitalConfig.l + 1) : 0;
      const radialModulation = 1 + waveAmplitude * Math.cos(t * orbitalConfig.m);

      points.push(new THREE.Vector3(
        x * radialModulation,
        y,
        z * radialModulation
      ));
    }

    return points;
  }, [orbitalConfig, showWaveFunction, scale]);

  // Create torus surface for orbital
  const torusGeometry = useMemo(() => {
    const majorRadius = 0.3 * scale;
    const minorRadius = 0.08 * scale;
    return new THREE.TorusGeometry(majorRadius, minorRadius, 16, 100);
  }, [scale]);

  useFrame((state) => {
    if (!groupRef.current || !animated) return;

    // Rotate the orbital
    groupRef.current.rotation.y = state.clock.elapsedTime * 0.3;
    groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.2) * 0.2;
  });

  // Generate wave function visualization
  const wavePoints = useMemo(() => {
    if (!showWaveFunction) return [];

    const points: { position: THREE.Vector3; intensity: number }[] = [];
    const samples = 50;

    for (let i = 0; i < samples; i++) {
      for (let j = 0; j < samples; j++) {
        const u = (i / samples) * Math.PI * 2;
        const v = (j / samples) * Math.PI * 2;

        // Toroidal coordinates
        const R = 0.3 * scale;
        const r = 0.08 * scale;

        const x = (R + r * Math.cos(v)) * Math.cos(u);
        const y = r * Math.sin(v);
        const z = (R + r * Math.cos(v)) * Math.sin(u);

        // Wave function (simplified hydrogen-like orbital)
        const rho = Math.sqrt(x*x + y*y + z*z);
        const theta = Math.acos(y / rho);
        const phi = Math.atan2(z, x);

        // Simplified radial wave function R_nl(rho)
        const R_nl = Math.exp(-rho / orbitalConfig.n) * Math.pow(rho, orbitalConfig.l);

        // Angular part Y_lm(theta, phi)
        const Y_lm = Math.pow(Math.sin(theta), Math.abs(orbitalConfig.m)) *
                    Math.cos(orbitalConfig.m * phi);

        const psi = R_nl * Y_lm;
        const intensity = Math.abs(psi) * Math.abs(psi); // Probability density

        if (intensity > 0.01) {
          points.push({
            position: new THREE.Vector3(x, y, z),
            intensity: Math.min(intensity * 10, 1)
          });
        }
      }
    }

    return points;
  }, [orbitalConfig, showWaveFunction, scale]);

  return (
    <div className="w-full h-96 bg-slate-900 rounded-lg border border-slate-700 relative">
      <div className="absolute top-4 left-4 text-white text-sm font-medium">
        {element} - {orbital} Orbital
      </div>
      <div className="absolute top-4 right-4 text-slate-400 text-xs">
        n={orbitalConfig.n}, l={orbitalConfig.l}, m={orbitalConfig.m}
      </div>

      {/* 3D Scene */}
      <div className="w-full h-full flex items-center justify-center">
        <div className="text-center">
          <div className="relative w-64 h-64 mx-auto mb-4">
            {/* Toroidal orbital surface */}
            <div
              className="absolute inset-0 border-2 border-blue-500/30 rounded-full"
              style={{
                width: '200px',
                height: '200px',
                left: '50%',
                top: '50%',
                transform: 'translate(-50%, -50%)',
                background: 'radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%)'
              }}
            />

            {/* Helical wave path */}
            <svg
              className="absolute inset-0 w-full h-full"
              viewBox="-1 -1 2 2"
              style={{ transform: 'rotateX(60deg)' }}
            >
              <path
                d={`M ${helicalPath[0]?.x || 0} ${helicalPath[0]?.z || 0} ${helicalPath.map(p =>
                  `L ${p.x} ${p.z}`
                ).join(' ')}`}
                stroke="#3b82f6"
                strokeWidth="0.02"
                fill="none"
                opacity="0.8"
              />
            </svg>

            {/* Wave function probability density */}
            {showWaveFunction && wavePoints.slice(0, 200).map((point, i) => (
              <div
                key={i}
                className="absolute w-1 h-1 bg-blue-400 rounded-full"
                style={{
                  left: `${50 + point.position.x * 80}%`,
                  top: `${50 + point.position.z * 80}%`,
                  opacity: point.intensity,
                  transform: 'translate(-50%, -50%)',
                  boxShadow: `0 0 2px rgba(59, 130, 246, ${point.intensity})`
                }}
              />
            ))}
          </div>

          <div className="text-slate-400 text-sm">
            <div>Helical Standing Wave Orbital</div>
            <div className="text-xs mt-1 text-slate-500">
              SDT toroidal electron geometry
            </div>
          </div>
        </div>
      </div>

      <div className="absolute bottom-4 left-4 right-4 flex justify-between text-xs text-slate-500">
        <span>Standing wave on torus surface</span>
        <span>Pressure-mediated quantization</span>
      </div>
    </div>
  );
}

