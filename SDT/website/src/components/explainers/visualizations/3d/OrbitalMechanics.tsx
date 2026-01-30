/**
 * Orbital Mechanics 3D Visualization
 * Shows orbital motion driven by pressure gradients in SDT
 */

import React, { useRef, useMemo, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface OrbitalMechanicsProps {
  showVelocity?: boolean;
  showPressure?: boolean;
  system?: 'earth-sun' | 'galaxy' | 'atomic';
  animated?: boolean;
  scale?: number;
}

export default function OrbitalMechanics({
  showVelocity = true,
  showPressure = true,
  system = 'earth-sun',
  animated = true,
  scale = 1
}: OrbitalMechanicsProps) {
  const groupRef = useRef<THREE.Group>(null);
  const [time, setTime] = useState(0);

  // System configurations
  const systemConfig = useMemo(() => {
    const configs = {
      'earth-sun': {
        centralMass: 1.989e30, // kg (Sun)
        orbitalMass: 5.972e24, // kg (Earth)
        distance: 1.496e11, // m (1 AU)
        orbitalPeriod: 365.25 * 24 * 3600, // seconds
        displayScale: 1e-11, // scale for visualization
        centralColor: '#F59E0B',
        orbitalColor: '#3B82F6'
      },
      'galaxy': {
        centralMass: 4.3e41, // kg (Milky Way black hole)
        orbitalMass: 1.989e30, // kg (Sun)
        distance: 8.2e3 * 9.461e15, // m (8.2 kpc in meters)
        orbitalPeriod: 2.4e8 * 365.25 * 24 * 3600, // seconds (240 million years)
        displayScale: 1e-20, // scale for visualization
        centralColor: '#DC2626',
        orbitalColor: '#F59E0B'
      },
      'atomic': {
        centralMass: 1.673e-27, // kg (proton)
        orbitalMass: 9.109e-31, // kg (electron)
        distance: 5.291772e-11, // m (Bohr radius)
        orbitalPeriod: 1.52e-16, // seconds
        displayScale: 1e9, // scale for visualization
        centralColor: '#EF4444',
        orbitalColor: '#8B5CF6'
      }
    };
    return configs[system];
  }, [system]);

  // Calculate orbital parameters
  const orbitalParams = useMemo(() => {
    const config = systemConfig;

    // SDT orbital velocity from pressure balance
    // v = κ × c, where κ is the fine structure constant for atomic orbits
    // For larger scales, κ decreases with distance
    const kappa = system === 'atomic' ? 1/137.036 : Math.max(1e-6, 1e-3 / Math.log(config.distance * config.displayScale + 1));
    const orbitalVelocity = kappa * 2.998e8; // c * κ

    // Pressure gradient force: F = -V_dp ∇P
    // For circular orbit: centrifugal force = pressure gradient force
    // m v²/r = V_dp dP/dr

    return {
      velocity: orbitalVelocity,
      radius: config.distance * config.displayScale * scale,
      period: config.orbitalPeriod,
      centralRadius: Math.max(0.05, Math.cbrt(config.centralMass / config.orbitalMass) * 0.1),
      orbitalRadius: 0.02
    };
  }, [systemConfig, system, scale]);

  useFrame((state, delta) => {
    if (!animated) return;
    setTime(prev => prev + delta);

    if (groupRef.current) {
      // Rotate the entire system slowly
      groupRef.current.rotation.y = time * 0.1;
    }
  });

  // Generate orbital path
  const orbitalPath = useMemo(() => {
    const points: THREE.Vector3[] = [];
    const segments = 100;

    for (let i = 0; i <= segments; i++) {
      const angle = (i / segments) * Math.PI * 2;
      points.push(new THREE.Vector3(
        orbitalParams.radius * Math.cos(angle),
        0,
        orbitalParams.radius * Math.sin(angle)
      ));
    }

    return points;
  }, [orbitalParams.radius]);

  // Calculate current orbital position
  const currentPosition = useMemo(() => {
    if (!animated) return { x: orbitalParams.radius, y: 0, z: 0 };

    const angle = (time / orbitalParams.period) * Math.PI * 2;
    return {
      x: orbitalParams.radius * Math.cos(angle),
      y: 0,
      z: orbitalParams.radius * Math.sin(angle)
    };
  }, [time, orbitalParams, animated]);

  return (
    <div className="w-full h-96 bg-slate-900 rounded-lg border border-slate-700 relative">
      <div className="absolute top-4 left-4 text-white text-sm font-medium">
        {system.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())} System
      </div>
      <div className="absolute top-4 right-4 text-slate-400 text-xs">
        SDT Pressure-Driven Orbits
      </div>

      {/* 3D Scene */}
      <div className="w-full h-full flex items-center justify-center">
        <div className="relative w-80 h-80">
          {/* Central body */}
          <div
            className="absolute rounded-full border-2"
            style={{
              width: `${orbitalParams.centralRadius * 100}px`,
              height: `${orbitalParams.centralRadius * 100}px`,
              left: '50%',
              top: '50%',
              transform: 'translate(-50%, -50%)',
              backgroundColor: systemConfig.centralColor,
              borderColor: systemConfig.centralColor,
              boxShadow: `0 0 20px ${systemConfig.centralColor}40`
            }}
          />

          {/* Orbital path */}
          <svg
            className="absolute inset-0 w-full h-full"
            viewBox="-1 -1 2 2"
          >
            <ellipse
              cx="0"
              cy="0"
              rx={orbitalParams.radius}
              ry={orbitalParams.radius}
              fill="none"
              stroke="#374151"
              strokeWidth="0.01"
              opacity="0.5"
            />
          </svg>

          {/* Orbital body */}
          <div
            className="absolute rounded-full border-2 transition-all duration-75"
            style={{
              width: `${orbitalParams.orbitalRadius * 100}px`,
              height: `${orbitalParams.orbitalRadius * 100}px`,
              left: `${50 + currentPosition.x * 50}%`,
              top: `${50 + currentPosition.z * 50}%`,
              transform: 'translate(-50%, -50%)',
              backgroundColor: systemConfig.orbitalColor,
              borderColor: systemConfig.orbitalColor,
              boxShadow: `0 0 10px ${systemConfig.orbitalColor}40`
            }}
          />

          {/* Velocity vector */}
          {showVelocity && (
            <div
              className="absolute border-l-2 border-t-2 border-green-400"
              style={{
                width: '20px',
                height: '20px',
                left: `${50 + currentPosition.x * 50}%`,
                top: `${50 + currentPosition.z * 50}%`,
                transform: `translate(-50%, -50%) rotate(${Math.atan2(currentPosition.z, currentPosition.x) * 180 / Math.PI}deg)`,
                transformOrigin: 'bottom left'
              }}
            />
          )}

          {/* Pressure gradient visualization */}
          {showPressure && (
            <div className="absolute inset-0">
              {/* Pressure gradient field */}
              <div
                className="absolute rounded-full"
                style={{
                  width: '300px',
                  height: '300px',
                  left: '50%',
                  top: '50%',
                  transform: 'translate(-50%, -50%)',
                  background: 'radial-gradient(circle, rgba(239, 68, 68, 0.1) 0%, transparent 70%)'
                }}
              />
            </div>
          )}
        </div>
      </div>

      <div className="absolute bottom-4 left-4 right-4 flex justify-between text-xs text-slate-500">
        <span>Pressure gradient driven motion</span>
        <span>
          {showVelocity && 'Velocity vectors • '}
          {showPressure && 'Pressure gradients'}
        </span>
      </div>

      {/* System info */}
      <div className="absolute bottom-12 left-4 text-xs text-slate-600">
        κ = {(system === 'atomic' ? 1/137.036 : 1e-3 / Math.log(systemConfig.distance * systemConfig.displayScale + 1)).toExponential(2)}
      </div>
    </div>
  );
}

