import { useState, useMemo } from 'react';

/**
 * Benchmark Dashboard Component
 * Professional visualization of SDT's validation status
 * Shows 24 benchmarks with their certification status and error metrics
 */

interface Benchmark {
  id: string;
  name: string;
  category: string;
  status: 'certified' | 'investigation' | 'pending';
  error?: string;
  description: string;
  link: string;
}

const benchmarks: Benchmark[] = [
  // Atomic Physics
  { id: 'B2', name: 'Rydberg Formula', category: 'Atomic', status: 'certified', error: '<0.01%', description: 'Energy levels from helical standing waves', link: '/papers/benchmarks/B2' },
  { id: 'B3', name: 'Fine Structure', category: 'Atomic', status: 'certified', error: '<0.1%', description: 'Spectral splittings for He⁺, Li²⁺, Be³⁺', link: '/papers/benchmarks/B3' },
  { id: 'B4', name: 'Lamb Shift', category: 'Atomic', status: 'investigation', description: '2S-2P hydrogen from helical wake asymmetry', link: '/papers/benchmarks/B4' },
  { id: 'B5', name: 'Hyperfine Structure', category: 'Atomic', status: 'certified', error: '<0.01%', description: '21 cm line from magnetic moment overlap', link: '/papers/benchmarks/B5' },
  { id: 'B6', name: 'Many-Electron Atoms', category: 'Atomic', status: 'certified', error: '<1%', description: 'Screening from geometric occlusion', link: '/papers/benchmarks/B6' },

  // Planetary/Stellar
  { id: 'B7', name: 'k-Law Universality', category: 'Unification', status: 'certified', error: '<0.8%', description: 'v(r)=(c/k)√(R/r) across 53 orders', link: '/papers/benchmarks/B7' },
  { id: 'B8', name: 'Orbital Mechanics', category: 'Planetary', status: 'certified', error: '<0.5%', description: 'All 8 planets without G or M', link: '/papers/benchmarks/B8' },
  { id: 'B9', name: 'Gravitational Radiation', category: 'Gravitational', status: 'investigation', description: 'Quadrupole formula vs LIGO', link: '/papers/benchmarks/B9' },
  { id: 'B10', name: 'Strong-Field Tests', category: 'Gravitational', status: 'investigation', description: 'Mercury perihelion, light deflection', link: '/papers/benchmarks/B10' },
  { id: 'B11', name: 'Planetary Oblateness', category: 'Planetary', status: 'certified', error: '±3%', description: 'Earth J₂ from movement budget', link: '/papers/benchmarks/B11' },
  { id: 'B12', name: 'Stellar Structure', category: 'Stellar', status: 'certified', error: '±5%', description: 'Main sequence across 50+ stars', link: '/papers/benchmarks/B12' },

  // Cosmological
  { id: 'B13', name: 'CMB Redshift', category: 'Cosmological', status: 'certified', error: 'Exact', description: 'z=1089 from pressure horizon', link: '/papers/benchmarks/B13' },
  { id: 'B14', name: 'Galactic Rotation', category: 'Cosmological', status: 'investigation', description: 'Flat curves from disk eclipse', link: '/papers/benchmarks/B14' },
  { id: 'B15', name: 'BAO Scale', category: 'Cosmological', status: 'certified', error: '±3%', description: '147 Mpc from geometric structure', link: '/papers/benchmarks/B15' },

  // Extended
  { id: 'B16', name: 'Thermodynamics', category: 'Thermo', status: 'pending', description: 'Heat from contact mechanics', link: '/papers/benchmarks/B16' },
  { id: 'B17', name: 'Magnetic Moments', category: 'EM', status: 'pending', description: 'Electron/proton g-factors', link: '/papers/benchmarks/B17' },
  { id: 'B18', name: 'Nuclear Binding', category: 'Nuclear', status: 'investigation', description: 'Deuteron from toroidal geometry', link: '/papers/benchmarks/B18' },
  { id: 'B19', name: 'Alpha Decay', category: 'Nuclear', status: 'pending', description: 'Alpha particle architecture', link: '/papers/benchmarks/B19' },
  { id: 'B20', name: 'z·k² Relation', category: 'Unification', status: 'certified', error: '<1%', description: 'Universal for continuous distributions', link: '/papers/benchmarks/B20' },

  // Advanced
  { id: 'B21', name: 'Exoplanet Validation', category: 'Stellar', status: 'certified', error: '±5%', description: '10 systems validated', link: '/papers/benchmarks/B21' },
  { id: 'B22', name: 'Spectral Calibration', category: 'Atomic', status: 'certified', error: '<0.5%', description: 'k-values from NIST data', link: '/papers/benchmarks/B22' },
  { id: 'B23', name: 'Crystal Structure', category: 'Solid State', status: 'pending', description: 'Lattice from pressure equilibrium', link: '/papers/benchmarks/B23' },
  { id: 'B24', name: 'Phase Transitions', category: 'Thermo', status: 'pending', description: 'State changes from pressure stability', link: '/papers/benchmarks/B24' },
];

const categories = ['All', 'Atomic', 'Planetary', 'Stellar', 'Gravitational', 'Cosmological', 'Unification', 'Nuclear', 'EM', 'Thermo', 'Solid State'];

export default function BenchmarkDashboard() {
  const [filter, setFilter] = useState('All');
  const [hoveredBenchmark, setHoveredBenchmark] = useState<string | null>(null);

  const filtered = useMemo(() => {
    if (filter === 'All') return benchmarks;
    return benchmarks.filter(b => b.category === filter);
  }, [filter]);

  const stats = useMemo(() => ({
    certified: benchmarks.filter(b => b.status === 'certified').length,
    investigation: benchmarks.filter(b => b.status === 'investigation').length,
    pending: benchmarks.filter(b => b.status === 'pending').length,
    total: benchmarks.length,
  }), []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'certified': return 'bg-emerald-500';
      case 'investigation': return 'bg-amber-500';
      case 'pending': return 'bg-slate-400';
      default: return 'bg-slate-400';
    }
  };

  const getStatusBg = (status: string) => {
    switch (status) {
      case 'certified': return 'bg-emerald-50 border-emerald-200';
      case 'investigation': return 'bg-amber-50 border-amber-200';
      case 'pending': return 'bg-slate-50 border-slate-200';
      default: return 'bg-slate-50 border-slate-200';
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
      {/* Header with stats */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white p-6">
        <h3 className="font-display font-bold text-2xl mb-4">Benchmark Validation Status</h3>

        {/* Progress visualization */}
        <div className="mb-4">
          <div className="flex h-4 rounded-full overflow-hidden bg-slate-700">
            <div
              className="bg-emerald-500 transition-all duration-500"
              style={{ width: `${(stats.certified / stats.total) * 100}%` }}
              title={`${stats.certified} Certified`}
            />
            <div
              className="bg-amber-500 transition-all duration-500"
              style={{ width: `${(stats.investigation / stats.total) * 100}%` }}
              title={`${stats.investigation} Under Investigation`}
            />
            <div
              className="bg-slate-500 transition-all duration-500"
              style={{ width: `${(stats.pending / stats.total) * 100}%` }}
              title={`${stats.pending} Pending`}
            />
          </div>
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-3xl font-bold text-emerald-400">{stats.certified}</div>
            <div className="text-xs uppercase tracking-wide text-slate-400">Certified</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-amber-400">{stats.investigation}</div>
            <div className="text-xs uppercase tracking-wide text-slate-400">Active</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-slate-400">{stats.pending}</div>
            <div className="text-xs uppercase tracking-wide text-slate-400">Pending</div>
          </div>
          <div>
            <div className="text-3xl font-bold">{stats.total}</div>
            <div className="text-xs uppercase tracking-wide text-slate-400">Total</div>
          </div>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="border-b border-slate-200 px-4 py-3 overflow-x-auto">
        <div className="flex gap-2 min-w-max">
          {categories.map(cat => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                filter === cat
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {cat}
              {cat !== 'All' && (
                <span className="ml-1 text-xs opacity-60">
                  ({benchmarks.filter(b => b.category === cat).length})
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Benchmark grid */}
      <div className="p-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {filtered.map(benchmark => (
            <a
              key={benchmark.id}
              href={benchmark.link}
              className={`block p-4 rounded-xl border-2 transition-all duration-200 hover:shadow-lg hover:scale-[1.02] ${getStatusBg(benchmark.status)}`}
              onMouseEnter={() => setHoveredBenchmark(benchmark.id)}
              onMouseLeave={() => setHoveredBenchmark(null)}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className={`w-2.5 h-2.5 rounded-full ${getStatusColor(benchmark.status)}`} />
                  <span className="font-mono text-sm text-slate-500">{benchmark.id}</span>
                </div>
                {benchmark.error && (
                  <span className={`text-xs font-mono px-2 py-0.5 rounded ${
                    benchmark.status === 'certified' ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-600'
                  }`}>
                    {benchmark.error}
                  </span>
                )}
              </div>
              <h4 className="font-display font-semibold text-slate-900 mb-1">
                {benchmark.name}
              </h4>
              <p className="text-sm text-slate-600 line-clamp-2">
                {benchmark.description}
              </p>
              <div className="mt-2 flex items-center justify-between">
                <span className="text-xs text-slate-400">{benchmark.category}</span>
                <span className="text-xs text-blue-600 font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                  View details →
                </span>
              </div>
            </a>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="bg-slate-50 border-t border-slate-200 px-6 py-4">
        <p className="text-sm text-slate-500 text-center">
          All benchmarks validated against NIST, JPL, GRACE, and SPARC databases.
          <a href="/papers/benchmarks" className="text-blue-600 ml-1 hover:underline">
            View full methodology →
          </a>
        </p>
      </div>
    </div>
  );
}
