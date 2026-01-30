/**
 * Nuclear Packing 3D Visualization
 * Shows how nucleons are packed in atomic nuclei according to SDT toroidal geometry
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface NuclearPackingProps {
  element?: string;
  showStructure?: boolean;
  animated?: boolean;
  scale?: number;
}

export default function NuclearPacking({
  element = 'Helium-4',
  showStructure = true,
  animated = true,
  scale = 1
}: NuclearPackingProps) {
  const groupRef = useRef<THREE.Group>(null);

  // Get nucleon configuration for the element
  const nucleonConfig = useMemo(() => {
    const configs: Record<string, { protons: number, neutrons: number, geometry: string }> = {
      'Helium-4': { protons: 2, neutrons: 2, geometry: 'alpha' },
      'Carbon-12': { protons: 6, neutrons: 6, geometry: 'cluster' },
      'Iron-56': { protons: 26, neutrons: 30, geometry: 'fermi' },
      'Lead-208': { protons: 82, neutrons: 126, geometry: 'fermi' }
    };
    return configs[element] || configs['Helium-4'];
  }, [element]);

  // Create toroidal geometry for nucleons
  const nucleonGeometry = useMemo(() => {
    // Torus geometry represents toroidal nucleon structure
    return new THREE.TorusGeometry(0.08 * scale, 0.03 * scale, 8, 16);
  }, [scale]);

  useFrame((state) => {
    if (!groupRef.current || !animated) return;

    // Gentle rotation
    groupRef.current.rotation.y = state.clock.elapsedTime * 0.2;
    groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.1) * 0.1;
  });

  // Generate nucleon positions based on element
  const nucleons = useMemo(() => {
    const { protons, neutrons, geometry } = nucleonConfig;
    const totalNucleons = protons + neutrons;
    const positions: THREE.Vector3[] = [];
    const colors: string[] = [];

    if (geometry === 'alpha') {
      // Alpha particle: tetrahedral arrangement
      positions.push(new THREE.Vector3(-0.1, 0.1, 0)); // Proton 1
      positions.push(new THREE.Vector3(0.1, 0.1, 0));  // Proton 2
      positions.push(new THREE.Vector3(0, -0.1, 0.1)); // Neutron 1
      positions.push(new THREE.Vector3(0, -0.1, -0.1)); // Neutron 2
    } else if (geometry === 'cluster') {
      // Carbon-12: alpha cluster arrangement
      const clusterPositions = [
        new THREE.Vector3(-0.15, 0.15, 0),   // Cluster 1 center
        new THREE.Vector3(0.15, 0.15, 0),    // Cluster 2 center
        new THREE.Vector3(0, -0.15, 0.15),   // Cluster 3 center
      ];
      // Add small offsets for individual nucleons within clusters
      clusterPositions.forEach(cluster => {
        for (let i = 0; i < 4; i++) { // 4 nucleons per alpha cluster
          const angle = (i / 4) * Math.PI * 2;
          positions.push(new THREE.Vector3(
            cluster.x + Math.cos(angle) * 0.05,
            cluster.y + Math.sin(angle) * 0.05,
            cluster.z
          ));
        }
      });
    } else {
      // Fermi gas approximation for heavy nuclei
      for (let i = 0; i < Math.min(totalNucleons, 50); i++) {
        const phi = Math.random() * Math.PI * 2;
        const theta = Math.acos(2 * Math.random() - 1);
        const r = 0.2 * Math.cbrt(i / totalNucleons); // Scale with cube root of nucleon number

        positions.push(new THREE.Vector3(
          r * Math.sin(theta) * Math.cos(phi),
          r * Math.sin(theta) * Math.sin(phi),
          r * Math.cos(theta)
        ));
      }
    }

    // Assign colors (red for protons, blue for neutrons)
    for (let i = 0; i < positions.length; i++) {
      colors.push(i < nucleonConfig.protons ? '#ef4444' : '#3b82f6');
    }

    return { positions, colors };
  }, [nucleonConfig]);

  return (
    <div className="w-full h-96 bg-slate-900 rounded-lg border border-slate-700 relative">
      <div className="absolute top-4 left-4 text-white text-sm font-medium">
        {element} Nuclear Structure
      </div>
      <div className="absolute top-4 right-4 text-slate-400 text-xs">
        {nucleonConfig.protons}p {nucleonConfig.neutrons}n
      </div>

      {/* 3D Scene - simplified representation */}
      <div className="w-full h-full flex items-center justify-center">
        <div className="text-center">
          <div className="text-slate-300 mb-4">
            <div className="w-32 h-32 mx-auto mb-4 relative">
              {/* Visual representation of nucleons */}
              <div className="absolute inset-0 flex flex-wrap justify-center items-center">
                {nucleons.positions.slice(0, 16).map((pos, i) => (
                  <div
                    key={i}
                    className="w-3 h-3 rounded-full border border-white/20"
                    style={{
                      backgroundColor: nucleons.colors[i],
                      position: 'absolute',
                      left: `${50 + pos.x * 40}%`,
                      top: `${50 + pos.y * 40}%`,
                      transform: 'translate(-50%, -50%)',
                      boxShadow: `0 0 4px ${nucleons.colors[i]}40`
                    }}
                  />
                ))}
              </div>
            </div>
          </div>

          <div className="text-slate-400 text-sm">
            <div>Toroidal Nucleon Packing</div>
            {showStructure && (
              <div className="text-xs mt-1 text-slate-500">
                {nucleonConfig.geometry === 'alpha' && 'Alpha cluster arrangement'}
                {nucleonConfig.geometry === 'cluster' && 'Multi-alpha cluster structure'}
                {nucleonConfig.geometry === 'fermi' && 'Fermi gas approximation'}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="absolute bottom-4 left-4 right-4 flex justify-between text-xs text-slate-500">
        <span>SDT Nuclear Geometry</span>
        <span>Pressure-mediated binding</span>
      </div>
    </div>
  );
}

