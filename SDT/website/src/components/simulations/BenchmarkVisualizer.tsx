/**
 * Benchmark Visualizer Component
 * Agent 3: Physics/Simulation
 * 
 * Interactive visualization of SDT benchmark validation results
 * Shows prediction vs observation with error analysis
 */

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { SimulationBase, SimulationProps } from './SimulationBase';

export interface BenchmarkData {
  id: string;
  name: string;
  category: string;
  status: 'certified' | 'investigation' | 'predicted';
  error?: string;
  predicted?: number;
  observed?: number;
  units?: string;
  description?: string;
  details?: {
    dataPoints?: Array<{
      label: string;
      predicted: number;
      observed: number;
      error: number;
    }>;
  };
}

interface BenchmarkVisualizerProps extends SimulationProps {
  parameters: {
    selectedBenchmark?: string;
    showAll?: boolean;
    categoryFilter?: string;
    statusFilter?: 'certified' | 'investigation' | 'predicted' | 'all';
    viewMode?: '3d' | '2d' | 'comparison';
  };
  benchmarks?: BenchmarkData[];
}

// Default benchmark data
const defaultBenchmarks: BenchmarkData[] = [
  {
    id: 'B01',
    name: 'Atomic Structure',
    category: 'Atomic',
    status: 'certified',
    error: '<0.8%',
    description: 'Energy levels from helical standing waves',
    details: {
      dataPoints: [
        { label: 'n=1', predicted: -13.598, observed: -13.598, error: 0.001 },
        { label: 'n=2', predicted: -3.400, observed: -3.400, error: 0.004 },
        { label: 'n=3', predicted: -1.511, observed: -1.511, error: 0.001 },
        { label: 'n=4', predicted: -0.850, observed: -0.850, error: 0.048 },
      ],
    },
  },
  {
    id: 'B02',
    name: 'Rydberg Formula',
    category: 'Atomic',
    status: 'certified',
    error: '<0.01%',
    description: 'Spectral lines from helical quantization',
  },
  {
    id: 'B03',
    name: 'Fine Structure',
    category: 'Atomic',
    status: 'certified',
    error: '<0.1%',
    description: 'Spectral splittings for He⁺, Li²⁺, Be³⁺',
  },
  {
    id: 'B05',
    name: 'Hyperfine Structure',
    category: 'Atomic',
    status: 'certified',
    error: '<0.01%',
    description: '21 cm line from magnetic moment overlap',
  },
  {
    id: 'B07',
    name: 'k-Law Universality',
    category: 'Unification',
    status: 'certified',
    error: '<0.8%',
    description: 'v(r)=(c/k)√(R/r) across 53 orders of magnitude',
  },
  {
    id: 'B08',
    name: 'Orbital Mechanics',
    category: 'Planetary',
    status: 'certified',
    error: '<0.5%',
    description: 'All 8 planets without G or M',
  },
  {
    id: 'B11',
    name: 'Planetary Oblateness',
    category: 'Planetary',
    status: 'certified',
    error: '±3%',
    description: 'Earth J₂ from movement budget',
  },
  {
    id: 'B12',
    name: 'Stellar Structure',
    category: 'Stellar',
    status: 'certified',
    error: '±5%',
    description: '50+ star validation',
  },
  {
    id: 'B13',
    name: 'CMB Redshift',
    category: 'Cosmology',
    status: 'certified',
    error: 'Exact',
    description: 'Pressure horizon z=1089',
  },
  {
    id: 'B14',
    name: 'Galactic Rotation',
    category: 'Galactic',
    status: 'certified',
    error: '<1%',
    description: 'Disk eclipse (no dark matter)',
  },
  {
    id: 'B15',
    name: 'BAO Scale',
    category: 'Cosmology',
    status: 'certified',
    error: '±3%',
    description: 'Pressure waves 147 Mpc',
  },
  {
    id: 'B16',
    name: 'Transport Coefficients',
    category: 'Thermodynamic',
    status: 'certified',
    error: '<0.05%',
    description: 'T^(1/2) scaling',
  },
];

class BenchmarkVisualization extends SimulationBase {
  private benchmarkCards: THREE.Mesh[] = [];
  private selectedCard: THREE.Mesh | null = null;
  private comparisonChart: THREE.Mesh | null = null;
  private grid: THREE.GridHelper | null = null;
  
  private benchmarks: BenchmarkData[] = [];
  private selectedBenchmark: string | null = null;
  private viewMode: '3d' | '2d' | 'comparison' = '3d';

  init(): void {
    // Clear existing objects
    while (this.scene.children.length > 0) {
      const child = this.scene.children[0];
      if (child instanceof THREE.Light) {
        // Keep lights
      } else {
        this.scene.remove(child);
        if (child instanceof THREE.Mesh || child instanceof THREE.Line) {
          child.geometry.dispose();
          if (child.material instanceof THREE.Material) {
            child.material.dispose();
          }
        }
      }
    }

    this.benchmarks = this.parameters.benchmarks || defaultBenchmarks;
    this.selectedBenchmark = this.parameters.selectedBenchmark || null;
    this.viewMode = this.parameters.viewMode || '3d';

    if (this.viewMode === '3d') {
      this.create3DGrid();
    } else if (this.viewMode === 'comparison') {
      this.createComparisonChart();
    } else {
      this.create2DLayout();
    }

    // Position camera based on view mode
    if (this.viewMode === '3d') {
      this.camera.position.set(0, 8, 12);
      this.camera.lookAt(0, 0, 0);
    } else {
      this.camera.position.set(0, 5, 10);
      this.camera.lookAt(0, 0, 0);
    }
  }

  private create3DGrid(): void {
    // Create 3D grid of benchmark cards
    const gridSize = Math.ceil(Math.sqrt(this.benchmarks.length));
    const spacing = 2.5;
    const startX = -(gridSize - 1) * spacing / 2;
    const startZ = -(gridSize - 1) * spacing / 2;

    this.benchmarkCards = [];
    this.benchmarks.forEach((benchmark, index) => {
      const row = Math.floor(index / gridSize);
      const col = index % gridSize;
      const x = startX + col * spacing;
      const z = startZ + row * spacing;
      const y = 0;

      const card = this.createBenchmarkCard(benchmark, x, y, z);
      this.benchmarkCards.push(card);
      this.scene.add(card);
    });

    // Add grid helper
    this.grid = new THREE.GridHelper(20, 20, 0x444444, 0x222222);
    this.scene.add(this.grid);
  }

  private createBenchmarkCard(benchmark: BenchmarkData, x: number, y: number, z: number): THREE.Mesh {
    const cardGeometry = new THREE.BoxGeometry(2, 1.5, 0.1);
    
    // Color based on status
    let color: number;
    if (benchmark.status === 'certified') {
      color = 0x10b981; // Green
    } else if (benchmark.status === 'investigation') {
      color = 0xf59e0b; // Amber
    } else {
      color = 0x6b7280; // Gray
    }

    const cardMaterial = new THREE.MeshStandardMaterial({
      color: color,
      metalness: 0.7,
      roughness: 0.3,
      emissive: benchmark.id === this.selectedBenchmark ? 0x333300 : 0x000000,
      emissiveIntensity: benchmark.id === this.selectedBenchmark ? 0.3 : 0,
    });

    const card = new THREE.Mesh(cardGeometry, cardMaterial);
    card.position.set(x, y, z);
    card.userData = { benchmark: benchmark };

    // Add text label (simplified - in real implementation, use TextGeometry or HTML overlay)
    // For now, we'll use a simple indicator

    return card;
  }

  private createComparisonChart(): void {
    // Create comparison chart showing prediction vs observation
    if (!this.selectedBenchmark) return;

    const benchmark = this.benchmarks.find(b => b.id === this.selectedBenchmark);
    if (!benchmark || !benchmark.details?.dataPoints) return;

    const dataPoints = benchmark.details.dataPoints;
    const maxValue = Math.max(
      ...dataPoints.map(d => Math.max(Math.abs(d.predicted), Math.abs(d.observed)))
    );
    const scale = 3 / maxValue;

    // Create bars for predicted and observed
    dataPoints.forEach((point, index) => {
      const x = (index - dataPoints.length / 2) * 1.5;
      
      // Predicted bar (blue)
      const predHeight = Math.abs(point.predicted) * scale;
      const predGeometry = new THREE.BoxGeometry(0.4, predHeight, 0.4);
      const predMaterial = new THREE.MeshStandardMaterial({ color: 0x4a90e2 });
      const predBar = new THREE.Mesh(predGeometry, predMaterial);
      predBar.position.set(x, predHeight / 2, 0);
      this.scene.add(predBar);

      // Observed bar (gold)
      const obsHeight = Math.abs(point.observed) * scale;
      const obsGeometry = new THREE.BoxGeometry(0.4, obsHeight, 0.4);
      const obsMaterial = new THREE.MeshStandardMaterial({ color: 0xd69e2e });
      const obsBar = new THREE.Mesh(obsGeometry, obsMaterial);
      obsBar.position.set(x, obsHeight / 2, 0.5);
      this.scene.add(obsBar);

      // Error indicator line
      const error = Math.abs(point.predicted - point.observed) * scale;
      if (error > 0.01) {
        const errorGeometry = new THREE.BufferGeometry().setFromPoints([
          new THREE.Vector3(x, predHeight, 0.2),
          new THREE.Vector3(x, obsHeight, 0.5),
        ]);
        const errorMaterial = new THREE.LineBasicMaterial({ color: 0xff4444, linewidth: 2 });
        const errorLine = new THREE.Line(errorGeometry, errorMaterial);
        this.scene.add(errorLine);
      }
    });

    // Add axis labels (simplified)
    const axisGeometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-5, 0, 0),
      new THREE.Vector3(5, 0, 0),
    ]);
    const axisMaterial = new THREE.LineBasicMaterial({ color: 0xffffff, opacity: 0.5 });
    const axis = new THREE.Line(axisGeometry, axisMaterial);
    this.scene.add(axis);
  }

  private create2DLayout(): void {
    // Create 2D layout (similar to 3D but flat)
    this.create3DGrid();
    // Cards are already created, just adjust camera
  }

  update(deltaTime: number): void {
    // Animate selected card
    if (this.selectedBenchmark) {
      const selectedCard = this.benchmarkCards.find(
        card => card.userData.benchmark?.id === this.selectedBenchmark
      );
      if (selectedCard) {
        selectedCard.rotation.y += deltaTime * 0.5;
        selectedCard.position.y = 0.5 + 0.2 * Math.sin(this.time * 2);
      }
    }

    // Rotate scene slowly
    if (this.viewMode === '3d') {
      this.scene.rotation.y += deltaTime * 0.1;
    }
  }

  protected onParametersChanged(): void {
    this.init();
  }

  dispose(): void {
    this.benchmarkCards.forEach(card => {
      card.geometry.dispose();
      if (card.material instanceof THREE.Material) {
        card.material.dispose();
      }
    });
    if (this.grid) {
      this.grid.dispose();
    }
  }
}

export const BenchmarkVisualizer: React.FC<BenchmarkVisualizerProps> = ({
  id,
  parameters,
  onParameterChange,
  showFormulas = false,
  showLabels = true,
  narrationEnabled = false,
  onReady,
  benchmarks,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const simulationRef = useRef<BenchmarkVisualization | null>(null);
  const [selectedBenchmark, setSelectedBenchmark] = useState<string | null>(
    parameters.selectedBenchmark || null
  );
  const [stats, setStats] = useState({
    certified: 0,
    investigation: 0,
    predicted: 0,
    total: 0,
  });

  useEffect(() => {
    if (!containerRef.current) return;

    const benchData = benchmarks || defaultBenchmarks;
    
    // Calculate statistics
    const certified = benchData.filter(b => b.status === 'certified').length;
    const investigation = benchData.filter(b => b.status === 'investigation').length;
    const predicted = benchData.filter(b => b.status === 'predicted').length;

    setStats({
      certified,
      investigation,
      predicted,
      total: benchData.length,
    });

    // Initialize simulation
    const sim = new BenchmarkVisualization(containerRef.current);
    sim.setParameters({
      selectedBenchmark: selectedBenchmark,
      showAll: true,
      viewMode: '3d',
      benchmarks: benchData,
      ...parameters,
    });
    sim.init();
    simulationRef.current = sim;

    if (onReady) {
      setTimeout(onReady, 100);
    }

    sim.play();

    return () => {
      sim.destroy();
      simulationRef.current = null;
    };
  }, [onReady, benchmarks]);

  useEffect(() => {
    if (simulationRef.current) {
      simulationRef.current.setParameters({
        ...parameters,
        selectedBenchmark: selectedBenchmark,
      });
    }
  }, [parameters, selectedBenchmark]);

  const handleBenchmarkClick = (benchmarkId: string) => {
    setSelectedBenchmark(benchmarkId === selectedBenchmark ? null : benchmarkId);
    if (onParameterChange) {
      onParameterChange('selectedBenchmark', benchmarkId);
    }
  };

  const selectedBenchmarkData = (benchmarks || defaultBenchmarks).find(
    b => b.id === selectedBenchmark
  );

  return (
    <div className="relative w-full h-full">
      <div
        ref={containerRef}
        className="w-full h-full min-h-[500px] bg-slate-900 rounded-lg"
      />
      {showLabels && (
        <div className="absolute bottom-4 left-4 bg-black/70 backdrop-blur-sm text-white p-4 rounded-lg text-sm max-w-xs">
          <div className="font-semibold mb-3 text-amber-400">Benchmark Status</div>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Certified:</span>
              <span className="font-mono text-emerald-400">{stats.certified}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Investigation:</span>
              <span className="font-mono text-amber-400">{stats.investigation}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Total:</span>
              <span className="font-mono">{stats.total}</span>
            </div>
            {selectedBenchmarkData && (
              <div className="mt-3 pt-3 border-t border-slate-600">
                <div className="text-slate-300 font-semibold">{selectedBenchmarkData.name}</div>
                <div className="text-slate-400 text-xs mt-1">
                  {selectedBenchmarkData.description}
                </div>
                {selectedBenchmarkData.error && (
                  <div className="text-emerald-400 text-xs mt-1">
                    Error: {selectedBenchmarkData.error}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
      
      {/* Benchmark selector overlay */}
      <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm text-white p-3 rounded-lg text-xs max-w-xs max-h-96 overflow-y-auto">
        <div className="font-semibold mb-2 text-amber-400">Benchmarks</div>
        <div className="space-y-1">
          {(benchmarks || defaultBenchmarks).map((benchmark) => (
            <button
              key={benchmark.id}
              onClick={() => handleBenchmarkClick(benchmark.id)}
              className={`w-full text-left p-2 rounded transition-colors ${
                selectedBenchmark === benchmark.id
                  ? 'bg-amber-500/30 text-amber-400'
                  : 'hover:bg-white/10'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-mono">{benchmark.id}</span>
                <span
                  className={`text-[10px] ${
                    benchmark.status === 'certified'
                      ? 'text-emerald-400'
                      : benchmark.status === 'investigation'
                      ? 'text-amber-400'
                      : 'text-slate-400'
                  }`}
                >
                  {benchmark.status}
                </span>
              </div>
              <div className="text-slate-400 text-[10px] mt-1">{benchmark.name}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

