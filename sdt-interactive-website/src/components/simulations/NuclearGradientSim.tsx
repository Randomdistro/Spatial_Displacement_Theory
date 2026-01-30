/**
 * NuclearGradientSim - SDT Nuclear Pressure Field Visualization
 *
 * Demonstrates the concept that ionization energy resides in the
 * nuclear pressure field geometry (the gradient), not the electron itself.
 * 
 * Ported from Three.js HTML artifact to React Three Fiber.
 */

import React, { useState, useMemo, useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Html } from '@react-three/drei';
import * as THREE from 'three';

// --- SDT Data Constants ---

const ELEMENT_DATA: Record<string, {
    name: string;
    Z: number;
    levels: { shell: string; E_i: number; koppa: number; n: number }[];
}> = {
    H: {
        name: "Hydrogen",
        Z: 1,
        levels: [{ shell: "1s¹", E_i: 13.5984, koppa: 137.04, n: 1 }]
    },
    He: {
        name: "Helium",
        Z: 2,
        levels: [{ shell: "1s²", E_i: 24.5874, koppa: 101.94, n: 1 }]
    },
    Li: {
        name: "Lithium",
        Z: 3,
        levels: [
            { shell: "2s¹", E_i: 5.3917, koppa: 217.69, n: 2 },
            { shell: "1s²", E_i: 75.64, koppa: 58.1, n: 1 }
        ]
    },
    Be: {
        name: "Beryllium",
        Z: 4,
        levels: [
            { shell: "2s²", E_i: 9.3227, koppa: 165.55, n: 2 },
            { shell: "1s²", E_i: 153.89, koppa: 40.8, n: 1 }
        ]
    },
    B: {
        name: "Boron",
        Z: 5,
        levels: [
            { shell: "2p¹", E_i: 8.2980, koppa: 175.47, n: 2 },
            { shell: "1s²", E_i: 259.37, koppa: 31.4, n: 1 }
        ]
    },
    C: {
        name: "Carbon",
        Z: 6,
        levels: [
            { shell: "2p²", E_i: 11.2603, koppa: 150.63, n: 2 },
            { shell: "1s²", E_i: 392.1, koppa: 25.5, n: 1 }
        ]
    },
    N: {
        name: "Nitrogen",
        Z: 7,
        levels: [
            { shell: "2p³", E_i: 14.5341, koppa: 132.59, n: 2 },
            { shell: "1s²", E_i: 552.1, koppa: 21.5, n: 1 }
        ]
    },
    O: {
        name: "Oxygen",
        Z: 8,
        levels: [
            { shell: "2p⁴", E_i: 13.6181, koppa: 136.97, n: 2 },
            { shell: "1s²", E_i: 739.3, koppa: 18.6, n: 1 }
        ]
    },
    F: {
        name: "Fluorine",
        Z: 9,
        levels: [
            { shell: "2p⁵", E_i: 17.4228, koppa: 121.10, n: 2 },
            { shell: "1s²", E_i: 953.9, koppa: 16.4, n: 1 }
        ]
    },
    Ne: {
        name: "Neon",
        Z: 10,
        levels: [
            { shell: "2p⁶", E_i: 21.5645, koppa: 108.85, n: 2 },
            { shell: "1s²", E_i: 1195.8, koppa: 14.6, n: 1 }
        ]
    },
    Na: {
        name: "Sodium",
        Z: 11,
        levels: [
            { shell: "3s¹", E_i: 5.1391, koppa: 222.97, n: 3 },
            { shell: "2p⁶", E_i: 47.2864, koppa: 73.5, n: 2 },
            { shell: "2s²", E_i: 172.18, koppa: 38.3, n: 2 },
            { shell: "1s²", E_i: 1465.12, koppa: 13.2, n: 1 }
        ]
    }
};

const BUILD_SEQUENCE = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na'];

// Mapping energy to visual radius (logarithmic)
const energyToRadius = (E_i: number, maxE: number) => {
    const minR = 1;
    const maxR = 15;
    // Lower energy = larger radius (further from nucleus)
    const ratio = Math.log(maxE / E_i) / Math.log(maxE / 1);
    return Math.max(minR, Math.min(maxR, minR + (maxR - minR) * ratio));
};

// --- Sub-Components ---

// The funnel visualizer
function GradientSurface({ maxRadius = 20 }: { maxRadius?: number }) {
    const geometry = useMemo(() => {
        const segments = 64;
        const geom = new THREE.BufferGeometry();
        const vertices = [];
        const colors = [];

        for (let i = 0; i <= segments; i++) {
            const r = 0.3 + (maxRadius - 0.3) * (i / segments);
            const energy = 1500 * Math.pow(0.3 / r, 2); 
            const y = -energy / 150; 

            for (let j = 0; j <= segments; j++) {
                const theta = (j / segments) * Math.PI * 2;
                const x = r * Math.cos(theta);
                const z = r * Math.sin(theta);

                vertices.push(x, y, z);

                const t = i / segments;
                // Color gradient: Blue (deep) to Red (shallow)
                colors.push(t * 0.8 + 0.2, 0.4, (1 - t) * 0.8 + 0.2);
            }
        }

        geom.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geom.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

        const indices = [];
        for (let i = 0; i < segments; i++) {
            for (let j = 0; j < segments; j++) {
                const a = i * (segments + 1) + j;
                const b = a + segments + 1;
                indices.push(a, b, a + 1);
                indices.push(b, b + 1, a + 1);
            }
        }
        geom.setIndex(indices);
        geom.computeVertexNormals();
        return geom;
    }, [maxRadius]);

    return (
        <mesh geometry={geometry}>
            <meshPhongMaterial vertexColors side={THREE.DoubleSide} transparent opacity={0.7} shininess={30} />
        </mesh>
    );
}

function Nucleus() {
    const ref = useRef<THREE.Mesh>(null);
    useFrame(() => {
        if (ref.current) ref.current.rotation.y += 0.01;
    });
    return (
        <mesh ref={ref}>
            <sphereGeometry args={[0.3, 32, 32]} />
            <meshPhongMaterial color={0xff4444} emissive={0xff2222} emissiveIntensity={0.5} />
        </mesh>
    );
}

// Interactive Electron
function Electron({ 
    level, 
    maxE, 
    isSelected, 
    onSelect, 
    isIonized 
}: { 
    level: { shell: string; E_i: number; koppa: number }; 
    maxE: number; 
    isSelected: boolean; 
    onSelect: () => void; 
    isIonized: boolean; 
}) {
    const originalRadius = useMemo(() => energyToRadius(level.E_i, maxE), [level.E_i, maxE]);
    const ref = useRef<THREE.Group>(null);
    const meshRef = useRef<THREE.Mesh>(null);
    const [currentRadius, setCurrentRadius] = useState(originalRadius);
    const [angle, setAngle] = useState(Math.random() * Math.PI * 2);

    // Ionization Animation Logic
    useFrame((state, delta) => {
        // Orbit
        const speed = 0.5 * (10 / originalRadius); // Inner orbit faster
        setAngle(a => a + speed * delta);
        
        // Radius Animation (Ionization)
        const targetR = isIonized ? 25 : originalRadius;
        const diff = targetR - currentRadius;
        if (Math.abs(diff) > 0.01) {
            setCurrentRadius(r => r + diff * delta * 2); // Easing speed
        }

        if (ref.current) {
            ref.current.position.x = Math.cos(angle) * currentRadius;
            ref.current.position.z = Math.sin(angle) * currentRadius;
        }
    });

    return (
        <group ref={ref} onClick={(e) => { e.stopPropagation(); onSelect(); }}>
            <mesh ref={meshRef}>
                <sphereGeometry args={[0.2, 16, 16]} />
                <meshPhongMaterial 
                    color={isSelected ? 0xffff00 : 0x00ff88} 
                    emissive={isSelected ? 0xffaa00 : 0x00ff44} 
                    emissiveIntensity={isSelected ? 0.8 : 0.3} 
                />
            </mesh>
        </group>
    );
}

// Component Main
export default function NuclearGradientSim() {
    const [elementKey, setElementKey] = useState("Na");
    const [selectedLevelIndex, setSelectedLevelIndex] = useState(0);
    const [ionizedIndices, setIonizedIndices] = useState<number[]>([]);

    const currentElement = ELEMENT_DATA[elementKey];
    const maxE = Math.max(...currentElement.levels.map(l => l.E_i));

    const handleIonize = () => {
        if (!ionizedIndices.includes(selectedLevelIndex)) {
            setIonizedIndices([...ionizedIndices, selectedLevelIndex]);
        }
    };

    const handleRecombine = () => {
        setIonizedIndices(ionizedIndices.filter(i => i !== selectedLevelIndex));
    };

    const nextElement = () => {
        const idx = BUILD_SEQUENCE.indexOf(elementKey);
        if (idx < BUILD_SEQUENCE.length - 1) {
            setElementKey(BUILD_SEQUENCE[idx + 1]);
            setIonizedIndices([]);
        }
    };
    
    const prevElement = () => {
        const idx = BUILD_SEQUENCE.indexOf(elementKey);
        if (idx > 0) {
            setElementKey(BUILD_SEQUENCE[idx - 1]);
            setIonizedIndices([]);
        }
    };

    return (
        <div className="relative w-full h-full bg-slate-950 rounded-xl overflow-hidden min-h-[500px]">
            {/* UI Overlay */}
            <div className="absolute top-4 left-4 z-10 bg-slate-900/90 backdrop-blur border border-slate-700 p-4 rounded-lg max-w-sm text-slate-200">
                <h3 className="text-xl font-bold text-blue-400 mb-2">Nuclear Pressure Gradient</h3>
                <div className="bg-blue-900/20 border-l-4 border-emerald-500 p-3 text-sm mb-4">
                    <strong>Key Insight:</strong> Energy is stored in the <strong>nuclear geometry</strong> (the gradient), not the electron.
                </div>

                {/* Element Selection */}
                <div className="flex gap-2 mb-4">
                    <button onClick={prevElement} className="bg-slate-800 px-3 py-1 rounded hover:bg-slate-700">←</button>
                    <div className="flex-1 text-center font-mono font-bold text-lg">{elementKey} (Z={currentElement.Z})</div>
                    <button onClick={nextElement} className="bg-slate-800 px-3 py-1 rounded hover:bg-slate-700">→</button>
                </div>

                {/* Ionization Controls */}
                <div className="bg-slate-800/50 p-3 rounded border border-slate-700">
                    <div className="text-xs text-slate-400 mb-1">Selected Shell</div>
                    <div className="font-mono text-emerald-400 text-lg mb-2">
                        {currentElement.levels[selectedLevelIndex]?.shell} 
                        <span className="text-slate-500 text-sm ml-2">
                             ({currentElement.levels[selectedLevelIndex]?.E_i.toFixed(2)} eV)
                        </span>
                    </div>
                    <div className="flex gap-2">
                        <button 
                            onClick={handleIonize}
                            disabled={ionizedIndices.includes(selectedLevelIndex)}
                            className="flex-1 bg-red-600/80 hover:bg-red-500 disabled:opacity-50 text-white text-sm py-1 rounded"
                        >
                            ⚡ Ionize
                        </button>
                        <button 
                             onClick={handleRecombine}
                             disabled={!ionizedIndices.includes(selectedLevelIndex)}
                             className="flex-1 bg-emerald-600/80 hover:bg-emerald-500 disabled:opacity-50 text-white text-sm py-1 rounded"
                        >
                            ↓ Recombine
                        </button>
                    </div>
                </div>

                {/* Legend */}
                <div className="mt-4 text-xs space-y-1">
                    <div className="flex items-center gap-2"><div className="w-3 h-3 bg-red-500 rounded-sm"></div> Nucleus</div>
                    <div className="flex items-center gap-2"><div className="w-3 h-3 bg-gradient-to-r from-blue-500 to-orange-500 rounded-sm"></div> Pressure Gradient (Well)</div>
                    <div className="flex items-center gap-2"><div className="w-3 h-3 bg-emerald-400 rounded-full"></div> Electron</div>
                </div>
            </div>

            <Canvas camera={{ position: [15, 10, 15], fov: 60 }}>
                <color attach="background" args={['#0a0a0f']} />
                <fog attach="fog" args={['#0a0a0f', 20, 50]} />
                
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} color="#00d4ff" intensity={1} />
                
                <OrbitControls enableDamping dampingFactor={0.05} />

                <Nucleus />
                <GradientSurface />
                
                {/* Grid Helper moved down */}
                <gridHelper args={[30, 30, 0x444444, 0x222222]} position={[0, -10, 0]} />

                {currentElement.levels.map((level, idx) => (
                    <Electron 
                        key={`${elementKey}-${idx}`}
                        level={level}
                        maxE={maxE}
                        isSelected={idx === selectedLevelIndex}
                        onSelect={() => setSelectedLevelIndex(idx)}
                        isIonized={ionizedIndices.includes(idx)}
                    />
                ))}
            </Canvas>
        </div>
    );
}
