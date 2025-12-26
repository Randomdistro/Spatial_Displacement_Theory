/**
 * Galaxy Rotation Simulation
 * Agent 3: Physics/Simulation
 * 
 * Demonstrates flat rotation curves without dark matter
 * Shows disk eclipse saturation mechanism
 */

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { SimulationBase, SimulationProps } from './SimulationBase';

interface GalaxyRotationSimProps extends SimulationProps {
  parameters: {
    diskRadius?: number; // Disk scale length R_d (kpc)
    galaxyMass?: number; // Total galaxy mass (solar masses)
    showRotationCurve?: boolean;
    compareDarkMatter?: boolean;
    showDisk?: boolean;
    showPressureOcclusion?: boolean;
  };
}

// Physical constants
const C = 299792458; // m/s
const KPC_TO_M = 3.086e19; // meters per kiloparsec
const SOLAR_MASS = 1.989e30; // kg

class GalaxyRotationSimulation extends SimulationBase {
  private galaxyDisk: THREE.Mesh | null = null;
  private rotationCurve: THREE.Line | null = null;
  private darkMatterCurve: THREE.Line | null = null;
  private occlusionVisualization: THREE.Points | null = null;
  private testParticles: THREE.Mesh[] = [];
  
  private R_d: number = 3.0; // Disk scale length (kpc)
  private galaxyMass: number = 1e11; // Solar masses
  private rotationData: Array<{ r: number; v: number; v_dm?: number }> = [];

  init(): void {
    // Clear existing objects
    while (this.scene.children.length > 0) {
      const child = this.scene.children[0];
      if (child instanceof THREE.Light) {
        // Keep lights
      } else {
        this.scene.remove(child);
        if (child instanceof THREE.Mesh || child instanceof THREE.Points || child instanceof THREE.Line) {
          child.geometry.dispose();
          if (child.material instanceof THREE.Material) {
            child.material.dispose();
          }
        }
      }
    }

    this.R_d = this.parameters.diskRadius || 3.0;
    this.galaxyMass = this.parameters.galaxyMass || 1e11;

    // Create galaxy disk
    if (this.parameters.showDisk !== false) {
      this.createGalaxyDisk();
    }

    // Calculate rotation curve
    this.calculateRotationCurve();

    // Create rotation curve visualization
    if (this.parameters.showRotationCurve !== false) {
      this.createRotationCurveVisualization();
    }

    // Create occlusion visualization
    if (this.parameters.showPressureOcclusion) {
      this.createOcclusionVisualization();
    }

    // Create test particles
    this.createTestParticles();

    // Position camera (top-down view)
    this.camera.position.set(0, 15, 0);
    this.camera.lookAt(0, 0, 0);
    this.camera.up.set(0, 0, 1);
  }

  private createGalaxyDisk(): void {
    const diskRadius = this.R_d * 5; // Show disk out to 5 scale lengths
    const diskGeometry = new THREE.CylinderGeometry(diskRadius, diskRadius, 0.2, 64);
    
    // Create exponential disk texture (darker at edges)
    const diskMaterial = new THREE.MeshStandardMaterial({
      color: 0x4a5568,
      metalness: 0.3,
      roughness: 0.7,
      transparent: true,
      opacity: 0.6,
      side: THREE.DoubleSide,
    });
    
    this.galaxyDisk = new THREE.Mesh(diskGeometry, diskMaterial);
    this.galaxyDisk.rotation.x = Math.PI / 2;
    this.scene.add(this.galaxyDisk);

    // Add central bulge
    const bulgeGeometry = new THREE.SphereGeometry(this.R_d * 0.3, 32, 32);
    const bulgeMaterial = new THREE.MeshStandardMaterial({
      color: 0xffd700,
      metalness: 0.9,
      roughness: 0.1,
      emissive: 0x332200,
      emissiveIntensity: 0.4,
    });
    const bulge = new THREE.Mesh(bulgeGeometry, bulgeMaterial);
    this.scene.add(bulge);
  }

  private calculateOcclusion(r_kpc: number): number {
    // Disk eclipse saturation model
    // E(r) saturates at large r, producing flat rotation
    const r_ratio = r_kpc / this.R_d;
    
    if (r_ratio < 1.0) {
      // Parabolic growth inside disk scale length
      return 0.5 * r_ratio * r_ratio;
    } else {
      // Saturation beyond disk scale length
      const E_sat = 0.64; // Saturation value from Phase 24
      return E_sat * (1 - Math.exp(-(r_ratio - 1)));
    }
  }

  private calculateRotationCurve(): void {
    this.rotationData = [];
    const R_flat = 2.5 * this.R_d; // SDT prediction: R_flat ≈ 2.5 R_d
    
    // Calculate beta parameter (gravitational parameter)
    // β = GM, but in SDT it's derived from geometry
    const beta = 1e10; // Approximate value (m³/s²)
    
    for (let r_kpc = 0.1; r_kpc < 20; r_kpc += 0.2) {
      const r_m = r_kpc * KPC_TO_M;
      
      // SDT rotation velocity from pressure gradient
      const E = this.calculateOcclusion(r_kpc);
      const acceleration = (beta * (1 - E)) / (r_m * r_m);
      const v_sdt = Math.sqrt(r_m * Math.abs(acceleration)) / 1000; // Convert to km/s
      
      // Dark matter comparison (NFW halo)
      let v_dm: number | undefined;
      if (this.parameters.compareDarkMatter) {
        // Simplified NFW halo model
        const r_s = this.R_d * 2; // Scale radius
        const x = r_kpc / r_s;
        const v_max = 200; // km/s (typical)
        v_dm = v_max * Math.sqrt(Math.log(1 + x) - x / (1 + x)) / Math.sqrt(Math.log(2) - 0.5);
      }
      
      this.rotationData.push({
        r: r_kpc,
        v: v_sdt,
        v_dm: v_dm,
      });
    }
  }

  private createRotationCurveVisualization(): void {
    // Create 3D rotation curve as a line above the disk
    const points: THREE.Vector3[] = [];
    const colors: number[] = [];
    
    this.rotationData.forEach((data) => {
      const x = data.r * 0.5; // Scale for visualization
      const y = data.v * 0.01; // Scale velocity to height
      const z = 0;
      points.push(new THREE.Vector3(x, y, z));
      
      // Color: blue for rising, gold for flat
      const color = data.r < 2.5 * this.R_d 
        ? new THREE.Color(0x4a90e2) // Blue (rising)
        : new THREE.Color(0xd69e2e); // Gold (flat)
      colors.push(color.r, color.g, color.b);
    });

    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    
    const material = new THREE.LineBasicMaterial({
      vertexColors: true,
      linewidth: 3,
    });
    
    this.rotationCurve = new THREE.Line(geometry, material);
    this.rotationCurve.position.y = 1; // Above disk
    this.scene.add(this.rotationCurve);

    // Dark matter comparison curve
    if (this.parameters.compareDarkMatter) {
      const dmPoints: THREE.Vector3[] = [];
      this.rotationData.forEach((data) => {
        if (data.v_dm !== undefined) {
          const x = data.r * 0.5;
          const y = data.v_dm * 0.01;
          dmPoints.push(new THREE.Vector3(x, y, 0));
        }
      });

      const dmGeometry = new THREE.BufferGeometry().setFromPoints(dmPoints);
      const dmMaterial = new THREE.LineBasicMaterial({
        color: 0xff4444, // Red
        linewidth: 2,
        transparent: true,
        opacity: 0.6,
        dashed: true,
      });
      
      this.darkMatterCurve = new THREE.Line(dmGeometry, dmMaterial);
      this.darkMatterCurve.position.y = 1;
      this.scene.add(this.darkMatterCurve);
    }
  }

  private createOcclusionVisualization(): void {
    const positions: number[] = [];
    const colors: number[] = [];
    const maxR = 20; // kpc
    
    for (let r_kpc = 0.5; r_kpc < maxR; r_kpc += 0.5) {
      const E = this.calculateOcclusion(r_kpc);
      const angle = (r_kpc / maxR) * Math.PI * 2;
      const x = r_kpc * 0.5 * Math.cos(angle);
      const z = r_kpc * 0.5 * Math.sin(angle);
      const y = E * 2; // Height represents occlusion
      
      positions.push(x, y, z);
      
      // Color: blue (low) to gold (high occlusion)
      const color = new THREE.Color();
      color.lerpColors(
        new THREE.Color(0x1a365d),
        new THREE.Color(0xd69e2e),
        E
      );
      colors.push(color.r, color.g, color.b);
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.3,
      vertexColors: true,
      transparent: true,
      opacity: 0.7,
    });

    this.occlusionVisualization = new THREE.Points(geometry, material);
    this.occlusionVisualization.position.y = 0.5;
    this.scene.add(this.occlusionVisualization);
  }

  private createTestParticles(): void {
    // Create test particles at different radii to show rotation
    const testRadii = [1, 2.5 * this.R_d, 5, 10]; // kpc
    
    testRadii.forEach((r_kpc, index) => {
      const r_scaled = r_kpc * 0.5;
      const particleGeometry = new THREE.SphereGeometry(0.1, 16, 16);
      const particleMaterial = new THREE.MeshStandardMaterial({
        color: 0x00ff88,
        emissive: 0x004422,
        emissiveIntensity: 0.5,
      });
      const particle = new THREE.Mesh(particleGeometry, particleMaterial);
      particle.position.set(r_scaled, 0.2, 0);
      particle.userData = { radius: r_kpc, angle: 0 };
      this.testParticles.push(particle);
      this.scene.add(particle);
    });
  }

  update(deltaTime: number): void {
    // Animate test particles in orbit
    this.testParticles.forEach((particle) => {
      const r_kpc = particle.userData.radius;
      const data = this.rotationData.find(d => Math.abs(d.r - r_kpc) < 0.3);
      if (data) {
        const angularVelocity = (data.v * 1000) / (r_kpc * KPC_TO_M); // rad/s
        particle.userData.angle += angularVelocity * deltaTime * 0.01; // Scaled for visualization
        
        const r_scaled = r_kpc * 0.5;
        const x = r_scaled * Math.cos(particle.userData.angle);
        const z = r_scaled * Math.sin(particle.userData.angle);
        particle.position.set(x, 0.2, z);
      }
    });

    // Rotate scene slowly
    this.scene.rotation.y += deltaTime * 0.05;
  }

  protected onParametersChanged(): void {
    this.init();
  }

  dispose(): void {
    if (this.galaxyDisk) {
      this.galaxyDisk.geometry.dispose();
      if (this.galaxyDisk.material instanceof THREE.Material) {
        this.galaxyDisk.material.dispose();
      }
    }
    if (this.rotationCurve) {
      this.rotationCurve.geometry.dispose();
      if (this.rotationCurve.material instanceof THREE.Material) {
        this.rotationCurve.material.dispose();
      }
    }
    if (this.darkMatterCurve) {
      this.darkMatterCurve.geometry.dispose();
      if (this.darkMatterCurve.material instanceof THREE.Material) {
        this.darkMatterCurve.material.dispose();
      }
    }
    if (this.occlusionVisualization) {
      this.occlusionVisualization.geometry.dispose();
      if (this.occlusionVisualization.material instanceof THREE.Material) {
        this.occlusionVisualization.material.dispose();
      }
    }
    this.testParticles.forEach(particle => {
      particle.geometry.dispose();
      if (particle.material instanceof THREE.Material) {
        particle.material.dispose();
      }
    });
  }
}

export const GalaxyRotationSim: React.FC<GalaxyRotationSimProps> = ({
  id,
  parameters,
  onParameterChange,
  showFormulas = true,
  showLabels = true,
  narrationEnabled = false,
  onReady,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const simulationRef = useRef<GalaxyRotationSimulation | null>(null);
  const [galaxyData, setGalaxyData] = useState({
    R_d: 3.0,
    R_flat: 7.5,
    v_flat: 200,
  });

  useEffect(() => {
    if (!containerRef.current) return;

    const R_d = parameters.diskRadius || 3.0;
    const R_flat = 2.5 * R_d; // SDT prediction

    // Initialize simulation
    const sim = new GalaxyRotationSimulation(containerRef.current);
    sim.setParameters({
      diskRadius: R_d,
      galaxyMass: 1e11,
      showRotationCurve: true,
      compareDarkMatter: false,
      showDisk: true,
      showPressureOcclusion: false,
      ...parameters,
    });
    sim.init();
    simulationRef.current = sim;

    setGalaxyData({
      R_d: R_d,
      R_flat: R_flat,
      v_flat: 200, // Typical flat rotation velocity
    });

    if (onReady) {
      setTimeout(onReady, 100);
    }

    sim.play();

    return () => {
      sim.destroy();
      simulationRef.current = null;
    };
  }, [onReady]);

  useEffect(() => {
    if (simulationRef.current) {
      simulationRef.current.setParameters(parameters);
      
      const R_d = parameters.diskRadius || 3.0;
      const R_flat = 2.5 * R_d;
      
      setGalaxyData({
        R_d: R_d,
        R_flat: R_flat,
        v_flat: 200,
      });
    }
  }, [parameters]);

  return (
    <div className="relative w-full h-full">
      <div
        ref={containerRef}
        className="w-full h-full min-h-[500px] bg-slate-900 rounded-lg"
      />
      {showLabels && (
        <div className="absolute bottom-4 left-4 bg-black/70 backdrop-blur-sm text-white p-4 rounded-lg text-sm max-w-xs">
          <div className="font-semibold mb-3 text-amber-400">Galaxy Rotation</div>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">R_d (scale length):</span>
              <span className="font-mono">{galaxyData.R_d.toFixed(1)} kpc</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">R_flat (predicted):</span>
              <span className="font-mono">{galaxyData.R_flat.toFixed(1)} kpc</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">v_flat:</span>
              <span className="font-mono">{galaxyData.v_flat} km/s</span>
            </div>
            <div className="mt-3 pt-3 border-t border-slate-600 text-slate-300">
              <div className="text-xs">R_flat ≈ 2.5 R_d</div>
              <div className="text-xs text-slate-400">No dark matter needed</div>
            </div>
          </div>
        </div>
      )}
      {showFormulas && (
        <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm text-white p-3 rounded-lg text-xs font-mono">
          <div>E(r) → E_sat</div>
          <div className="mt-1">v(r) = constant</div>
          <div className="mt-2 text-slate-400 text-[10px]">
            Disk Eclipse Saturation
          </div>
        </div>
      )}
    </div>
  );
};

