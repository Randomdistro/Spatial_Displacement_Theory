/**
 * Creative Agent: Enhanced Scene3D Component
 * 
 * TEKNE: Scene IS the spatial environment
 * Integrated with design system and atmospheric effects
 */

import React, { useRef, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Environment } from '@react-three/drei';
import * as THREE from 'three';
import CameraChoreography from './CameraChoreography';
import AtmosphericEffects from './AtmosphericEffects';
import SacredGeometryBackground from './SacredGeometryBackground';

export interface Scene3DProps {
  children: React.ReactNode;
  cameraPosition?: [number, number, number];
  cameraTarget?: [number, number, number];
  onCameraReady?: () => void;
  enableControls?: boolean;
  controlsMinDistance?: number;
  controlsMaxDistance?: number;
  fov?: number;
  className?: string;
}

/**
 * Base 3D scene wrapper component
 * Provides Three.js scene setup with lighting, camera, and controls
 */
export default function Scene3D({
  children,
  cameraPosition = [0, 0, 5],
  cameraTarget = [0, 0, 0],
  onCameraReady,
  enableControls = true,
  controlsMinDistance = 1,
  controlsMaxDistance = 10,
  fov = 60,
  className = '',
}: Scene3DProps) {
  const cameraRef = useRef<THREE.PerspectiveCamera>(null);

  useEffect(() => {
    if (cameraRef.current && onCameraReady) {
      onCameraReady();
    }
  }, [onCameraReady]);

  return (
    <div className={`w-full h-full ${className}`}>
      <Canvas
        gl={{ antialias: true, alpha: true }}
        dpr={[1, 2]}
        camera={{ position: cameraPosition, fov }}
      >
        {/* Lighting - Creative Agent Design System */}
        <ambientLight intensity={0.3} /> {/* Soft base */}
        <directionalLight
          position={[0, 5, 0]}
          intensity={0.6}
          castShadow
        />
        <pointLight position={[0, 0, 0]} intensity={0.4} color="#d69e2e" /> {/* Gold center glow */}
        
        {/* Sacred Geometry Background - subtle pattern in the deep */}
        <SacredGeometryBackground
          variant="both"
          opacity={0.12}
          scale={8}
          animated={true}
        />
        
        {/* Atmospheric Effects */}
        <AtmosphericEffects
          particleCount={1000}
          fogDensity={0.02}
          glowIntensity={0.3}
        />

        {/* Camera */}
        <PerspectiveCamera
          ref={cameraRef}
          makeDefault
          position={cameraPosition}
          fov={fov}
        />

        {/* Controls */}
        {enableControls && (
          <OrbitControls
            target={cameraTarget}
            minDistance={controlsMinDistance}
            maxDistance={controlsMaxDistance}
            enablePan={true}
            enableZoom={true}
            enableRotate={true}
            maxPolarAngle={Math.PI * 0.95}
            minPolarAngle={Math.PI * 0.05}
            dampingFactor={0.05}
          />
        )}

        {/* Camera Choreography */}
        <CameraChoreography
          targetPosition={cameraPosition ? new THREE.Vector3(...cameraPosition) : undefined}
          targetLookAt={cameraTarget ? new THREE.Vector3(...cameraTarget) : undefined}
          duration={3500}
        />
        
        {/* Environment - Dark space background */}
        <Environment preset="night" />
        <color attach="background" args={['#0a0e1a']} /> {/* Deep Space background */}

        {/* Scene content */}
        {children}
      </Canvas>
    </div>
  );
}

