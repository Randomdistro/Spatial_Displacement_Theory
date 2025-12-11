import { useEffect, useRef } from 'react';
import * as THREE from 'three';

/**
 * ToroidalElectron - 3D visualization of SDT's electron model
 * Renders a toroidal vortex with helical wake
 * This is the signature visual of SDT - the electron is NOT a point!
 */

interface Props {
  className?: string;
  autoRotate?: boolean;
  showHelicalWake?: boolean;
  interactive?: boolean;
}

export default function ToroidalElectron({
  className = '',
  autoRotate = true,
  showHelicalWake = true,
  interactive = true,
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a1a);

    // Camera
    const camera = new THREE.PerspectiveCamera(
      45,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    camera.position.set(4, 3, 5);
    camera.lookAt(0, 0, 0);

    // Renderer
    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404060, 0.5);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 10, 5);
    directionalLight.castShadow = true;
    scene.add(directionalLight);

    const pointLight1 = new THREE.PointLight(0x3b82f6, 2, 10);
    pointLight1.position.set(3, 2, 3);
    scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0xf59e0b, 1.5, 10);
    pointLight2.position.set(-3, -2, -3);
    scene.add(pointLight2);

    // Create the electron group
    const electronGroup = new THREE.Group();
    scene.add(electronGroup);

    // Main torus (the electron body)
    const torusGeometry = new THREE.TorusGeometry(1, 0.35, 64, 128);
    const torusMaterial = new THREE.MeshPhysicalMaterial({
      color: 0x3b82f6,
      metalness: 0.3,
      roughness: 0.2,
      transmission: 0.3,
      thickness: 0.5,
      envMapIntensity: 1,
      clearcoat: 1,
      clearcoatRoughness: 0.1,
    });
    const torus = new THREE.Mesh(torusGeometry, torusMaterial);
    torus.castShadow = true;
    torus.receiveShadow = true;
    electronGroup.add(torus);

    // Inner glow
    const innerGlowGeometry = new THREE.TorusGeometry(1, 0.36, 32, 64);
    const innerGlowMaterial = new THREE.MeshBasicMaterial({
      color: 0x60a5fa,
      transparent: true,
      opacity: 0.3,
      side: THREE.BackSide,
    });
    const innerGlow = new THREE.Mesh(innerGlowGeometry, innerGlowMaterial);
    electronGroup.add(innerGlow);

    // Helical wake particles
    if (showHelicalWake) {
      const wakeGroup = new THREE.Group();
      electronGroup.add(wakeGroup);

      const wakeParticleCount = 500;
      const wakeGeometry = new THREE.BufferGeometry();
      const wakePositions = new Float32Array(wakeParticleCount * 3);
      const wakeSizes = new Float32Array(wakeParticleCount);
      const wakeColors = new Float32Array(wakeParticleCount * 3);

      for (let i = 0; i < wakeParticleCount; i++) {
        // Helical path extending from torus
        const t = (i / wakeParticleCount) * Math.PI * 6;
        const helixRadius = 1 + (i / wakeParticleCount) * 0.5;
        const z = (i / wakeParticleCount) * 3 - 1.5;

        wakePositions[i * 3] = Math.cos(t) * helixRadius;
        wakePositions[i * 3 + 1] = Math.sin(t) * helixRadius;
        wakePositions[i * 3 + 2] = z;

        wakeSizes[i] = Math.max(0.05, 0.2 - (i / wakeParticleCount) * 0.15);

        // Color gradient from blue to gold
        const colorT = i / wakeParticleCount;
        wakeColors[i * 3] = 0.23 + colorT * 0.73; // R
        wakeColors[i * 3 + 1] = 0.51 - colorT * 0.13; // G
        wakeColors[i * 3 + 2] = 0.96 - colorT * 0.53; // B
      }

      wakeGeometry.setAttribute('position', new THREE.BufferAttribute(wakePositions, 3));
      wakeGeometry.setAttribute('size', new THREE.BufferAttribute(wakeSizes, 1));
      wakeGeometry.setAttribute('color', new THREE.BufferAttribute(wakeColors, 3));

      const wakeMaterial = new THREE.PointsMaterial({
        size: 0.1,
        vertexColors: true,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending,
      });

      const wakePoints = new THREE.Points(wakeGeometry, wakeMaterial);
      wakeGroup.add(wakePoints);
    }

    // Circulation lines (showing vortex flow)
    const circulationCount = 12;
    for (let i = 0; i < circulationCount; i++) {
      const curve = new THREE.CurvePath<THREE.Vector3>();
      const angle = (i / circulationCount) * Math.PI * 2;

      // Poloidal circulation around the torus
      const points: THREE.Vector3[] = [];
      for (let j = 0; j <= 64; j++) {
        const phi = (j / 64) * Math.PI * 2;
        const x = (1 + 0.35 * Math.cos(phi)) * Math.cos(angle);
        const y = (1 + 0.35 * Math.cos(phi)) * Math.sin(angle);
        const z = 0.35 * Math.sin(phi);
        points.push(new THREE.Vector3(x, y, z));
      }

      const lineGeometry = new THREE.BufferGeometry().setFromPoints(points);
      const lineMaterial = new THREE.LineBasicMaterial({
        color: 0xf59e0b,
        transparent: true,
        opacity: 0.4,
      });
      const line = new THREE.Line(lineGeometry, lineMaterial);
      electronGroup.add(line);
    }

    // Axis indicators (subtle)
    const axisLength = 2.5;
    const axisMaterial = new THREE.LineBasicMaterial({
      color: 0x4a5568,
      transparent: true,
      opacity: 0.3,
    });

    // X axis
    const xAxisGeometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-axisLength, 0, 0),
      new THREE.Vector3(axisLength, 0, 0),
    ]);
    scene.add(new THREE.Line(xAxisGeometry, axisMaterial));

    // Y axis
    const yAxisGeometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, -axisLength, 0),
      new THREE.Vector3(0, axisLength, 0),
    ]);
    scene.add(new THREE.Line(yAxisGeometry, axisMaterial));

    // Z axis
    const zAxisGeometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, 0, -axisLength),
      new THREE.Vector3(0, 0, axisLength),
    ]);
    scene.add(new THREE.Line(zAxisGeometry, axisMaterial));

    // Interactive controls
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };

    if (interactive) {
      const onMouseDown = (e: MouseEvent) => {
        isDragging = true;
        previousMousePosition = { x: e.clientX, y: e.clientY };
      };

      const onMouseMove = (e: MouseEvent) => {
        if (!isDragging) return;

        const deltaX = e.clientX - previousMousePosition.x;
        const deltaY = e.clientY - previousMousePosition.y;

        electronGroup.rotation.y += deltaX * 0.01;
        electronGroup.rotation.x += deltaY * 0.01;

        previousMousePosition = { x: e.clientX, y: e.clientY };
      };

      const onMouseUp = () => {
        isDragging = false;
      };

      renderer.domElement.addEventListener('mousedown', onMouseDown);
      window.addEventListener('mousemove', onMouseMove);
      window.addEventListener('mouseup', onMouseUp);
    }

    // Animation
    let animationId: number;
    const clock = new THREE.Clock();

    const animate = () => {
      animationId = requestAnimationFrame(animate);

      const elapsedTime = clock.getElapsedTime();

      // Auto-rotation
      if (autoRotate && !isDragging) {
        electronGroup.rotation.y = elapsedTime * 0.3;
        electronGroup.rotation.x = Math.sin(elapsedTime * 0.2) * 0.1;
      }

      // Pulsing glow
      innerGlow.scale.setScalar(1 + Math.sin(elapsedTime * 2) * 0.03);

      // Animate wake
      if (showHelicalWake) {
        const wakeGroup = electronGroup.children.find(
          (c) => c instanceof THREE.Group && c !== electronGroup
        );
        if (wakeGroup) {
          wakeGroup.rotation.z = elapsedTime * 0.5;
        }
      }

      // Animate point lights
      pointLight1.position.x = Math.cos(elapsedTime * 0.5) * 3;
      pointLight1.position.z = Math.sin(elapsedTime * 0.5) * 3;

      renderer.render(scene, camera);
    };
    animate();

    // Resize handler
    const handleResize = () => {
      const width = container.clientWidth;
      const height = container.clientHeight;

      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', handleResize);

      // Dispose of geometries and materials
      scene.traverse((object) => {
        if (object instanceof THREE.Mesh) {
          object.geometry.dispose();
          if (Array.isArray(object.material)) {
            object.material.forEach((m) => m.dispose());
          } else {
            object.material.dispose();
          }
        }
      });

      renderer.dispose();
      container.removeChild(renderer.domElement);
    };
  }, [autoRotate, showHelicalWake, interactive]);

  return (
    <div
      ref={containerRef}
      className={`w-full h-full min-h-[400px] ${className}`}
      style={{ touchAction: 'none' }}
    >
      {/* Loading placeholder */}
      <div className="absolute inset-0 flex items-center justify-center bg-slate-900 rounded-xl">
        <div className="text-slate-500 text-sm">Loading 3D visualization...</div>
      </div>
    </div>
  );
}
