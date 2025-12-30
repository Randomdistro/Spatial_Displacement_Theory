/**
 * Creative Agent: Volumetric Pressure Field Component
 * 
 * TEKNE: Visualization IS the pressure field
 * Uses custom GLSL shader for volumetric rendering
 * 
 * Design Philosophy:
 * - The shader IS the pressure field
 * - Volumetric gradient from center to edge
 * - Gold flow lines showing direction
 * - Animated flow
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Mesh, SphereGeometry, ShaderMaterial, Color, Vector3 } from 'three';
import { useShader } from '../../framework/hooks';
import { shaderRegistry } from '../../framework';

// Design system colors
const COLORS = {
  spaceDeep: new Color(0x1a365d),
  spaceMedium: new Color(0x2d5a87),
  spaceLight: new Color(0x4299e1),
  goldPrimary: new Color(0xd69e2e),
} as const;

export interface VolumetricPressureFieldProps {
  center: [number, number, number];
  radius: number;
  density?: number;
}

/**
 * VolumetricPressureField - Custom shader-based pressure field
 * 
 * Features:
 * - Custom GLSL shader for volumetric rendering
 * - Pressure gradient visualization
 * - Gold flow lines
 * - Animated flow
 */
export default function VolumetricPressureField({
  center,
  radius,
  density = 0.5,
}: VolumetricPressureFieldProps) {
  const meshRef = useRef<Mesh>(null);
  const timeRef = useRef(0);

  // Register pressure field shader
  const shaderSource = useMemo(() => ({
    vertex: `
      attribute vec3 position;
      attribute vec3 normal;
      attribute vec2 uv;
      
      uniform mat4 modelViewMatrix;
      uniform mat4 projectionMatrix;
      uniform mat3 normalMatrix;
      
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      
      void main() {
        vPosition = position;
        vNormal = normalize(normalMatrix * normal);
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragment: `
      precision highp float;
      
      uniform float time;
      uniform float pressureDensity;
      uniform vec3 center;
      uniform float radius;
      uniform vec3 colorDeep;
      uniform vec3 colorMedium;
      uniform vec3 colorLight;
      uniform vec3 colorGold;
      
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      
      float distanceFromCenter(vec3 pos) {
        return length(pos - center);
      }
      
      float calculatePressure(vec3 pos) {
        float dist = distanceFromCenter(pos);
        float normalizedDist = clamp(dist / radius, 0.0, 1.0);
        return exp(-normalizedDist * 2.0) * pressureDensity;
      }
      
      vec3 pressureColor(float pressure) {
        if (pressure > 0.7) {
          return mix(colorMedium, colorDeep, (pressure - 0.7) / 0.3);
        } else if (pressure > 0.3) {
          return mix(colorLight, colorMedium, (pressure - 0.3) / 0.4);
        } else {
          return colorLight;
        }
      }
      
      float flowLines(vec3 pos) {
        vec3 dir = normalize(pos - center);
        float angle = atan(dir.z, dir.x);
        float flow = sin(angle * 6.0 + time * 2.0) * 0.5 + 0.5;
        float dist = distanceFromCenter(pos);
        float distFactor = 1.0 - clamp(dist / radius, 0.0, 1.0);
        return flow * distFactor * 0.3;
      }
      
      float fresnel(vec3 normal, vec3 viewDir) {
        return pow(1.0 - dot(normal, viewDir), 2.0);
      }
      
      void main() {
        float pressure = calculatePressure(vPosition);
        vec3 color = pressureColor(pressure);
        
        float flow = flowLines(vPosition);
        color = mix(color, colorGold, flow);
        
        vec3 viewDir = normalize(-vPosition);
        float fresnelFactor = fresnel(vNormal, viewDir);
        color = mix(color, colorGold, fresnelFactor * 0.2);
        
        float emissive = pressure * 0.2 + flow * 0.3;
        float opacity = pressure * 0.3 + fresnelFactor * 0.1;
        
        gl_FragColor = vec4(color, opacity);
        gl_FragColor.rgb += color * emissive;
      }
    `,
    uniforms: {
      time: { type: 'float', value: 0 },
      pressureDensity: { type: 'float', value: density },
      center: { type: 'vec3', value: new Vector3(...center) },
      radius: { type: 'float', value: radius },
      colorDeep: { type: 'vec3', value: COLORS.spaceDeep },
      colorMedium: { type: 'vec3', value: COLORS.spaceMedium },
      colorLight: { type: 'vec3', value: COLORS.spaceLight },
      colorGold: { type: 'vec3', value: COLORS.goldPrimary },
    },
  }), [center, radius, density]);

  // Register and get shader
  const { compiledShader } = useShader({
    shader: shaderSource,
  });

  // Create shader material
  const material = useMemo(() => {
    if (!compiledShader) return null;
    
    return new ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        pressureDensity: { value: density },
        center: { value: new Vector3(...center) },
        radius: { value: radius },
        colorDeep: { value: COLORS.spaceDeep },
        colorMedium: { value: COLORS.spaceMedium },
        colorLight: { value: COLORS.spaceLight },
        colorGold: { value: COLORS.goldPrimary },
      },
      vertexShader: shaderSource.vertex,
      fragmentShader: shaderSource.fragment,
      transparent: true,
      side: 2, // DoubleSide
    });
  }, [compiledShader, density, center, radius]);

  // Update time uniform
  useFrame((state) => {
    if (material && material.uniforms.time) {
      material.uniforms.time.value = state.clock.elapsedTime;
    }
  });

  if (!material) return null;

  return (
    <mesh ref={meshRef} position={center}>
      <sphereGeometry args={[radius, 64, 64]} />
      <primitive object={material} attach="material" />
    </mesh>
  );
}



