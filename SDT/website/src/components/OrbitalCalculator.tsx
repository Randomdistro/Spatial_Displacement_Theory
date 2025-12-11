import { useState, useMemo } from 'react';

// Physical constants
const c = 299792458; // Speed of light (m/s)

// Preset systems with their parameters
const presets = {
  hydrogen: {
    name: 'Hydrogen Atom',
    description: 'Electron orbital in ground state',
    k: 137.036,
    R: 5.29177e-11, // Bohr radius (m)
    r: 5.29177e-11, // Orbital radius = Bohr radius
    observedV: 2.1877e6, // m/s
    unit: 'm',
    scale: 'Atomic',
  },
  earth: {
    name: 'Earth Orbit',
    description: 'Earth orbiting the Sun',
    k: 59254,
    R: 696340000, // Solar radius (m)
    r: 1.496e11, // Earth orbital radius (m)
    observedV: 29780, // m/s
    unit: 'm',
    scale: 'Planetary',
  },
  jupiter: {
    name: 'Jupiter Orbit',
    description: 'Jupiter orbiting the Sun',
    k: 59254,
    R: 696340000,
    r: 7.785e11, // Jupiter orbital radius (m)
    observedV: 13070, // m/s
    unit: 'm',
    scale: 'Planetary',
  },
  io: {
    name: 'Io (Jupiter Moon)',
    description: 'Io orbiting Jupiter',
    k: 8847,
    R: 69911000, // Jupiter radius (m)
    r: 4.217e8, // Io orbital radius (m)
    observedV: 17334, // m/s
    unit: 'm',
    scale: 'Planetary',
  },
  milkyway: {
    name: 'Sun in Milky Way',
    description: 'Solar orbit around galactic center',
    k: 4.2e5,
    R: 2.5e20, // Galactic effective radius (m)
    r: 2.5e20, // Sun's distance from center (m)
    observedV: 220000, // m/s
    unit: 'm',
    scale: 'Galactic',
  },
};

type PresetKey = keyof typeof presets;

export default function OrbitalCalculator() {
  const [selectedPreset, setSelectedPreset] = useState<PresetKey>('hydrogen');
  const [customMode, setCustomMode] = useState(false);
  const [customK, setCustomK] = useState('137');
  const [customR, setCustomR] = useState('5.29e-11');
  const [customr, setCustomr] = useState('5.29e-11');

  const preset = presets[selectedPreset];

  // Calculate predicted velocity using SDT formula: v = (c/k) * sqrt(R/r)
  const calculation = useMemo(() => {
    const k = customMode ? parseFloat(customK) : preset.k;
    const R = customMode ? parseFloat(customR) : preset.R;
    const r = customMode ? parseFloat(customr) : preset.r;

    if (isNaN(k) || isNaN(R) || isNaN(r) || k <= 0 || R <= 0 || r <= 0) {
      return null;
    }

    const predictedV = (c / k) * Math.sqrt(R / r);
    const observedV = customMode ? predictedV : preset.observedV;
    const error = customMode ? 0 : Math.abs((predictedV - observedV) / observedV) * 100;

    return {
      k,
      R,
      r,
      predictedV,
      observedV,
      error,
    };
  }, [selectedPreset, customMode, customK, customR, customr, preset]);

  const formatNumber = (num: number, precision = 4): string => {
    if (num === 0) return '0';
    const exp = Math.floor(Math.log10(Math.abs(num)));
    if (exp > 6 || exp < -3) {
      return num.toExponential(precision);
    }
    return num.toPrecision(precision);
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden max-w-4xl mx-auto">
      {/* Header */}
      <div className="bg-gradient-to-r from-sdt-primary-600 to-sdt-primary-700 text-white px-6 py-4">
        <h3 className="font-display font-semibold text-xl mb-1">Universal Orbital Law Calculator</h3>
        <p className="text-sdt-primary-100 text-sm font-mono">
          v(r) = (c/k) &times; &radic;(R/r)
        </p>
      </div>

      <div className="p-6">
        {/* Preset Selection */}
        <div className="mb-6">
          <label className="block text-sm font-display font-medium text-slate-700 mb-2">
            Select System
          </label>
          <div className="flex flex-wrap gap-2">
            {(Object.keys(presets) as PresetKey[]).map((key) => (
              <button
                key={key}
                onClick={() => {
                  setSelectedPreset(key);
                  setCustomMode(false);
                }}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedPreset === key && !customMode
                    ? 'bg-sdt-primary-600 text-white'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                {presets[key].name}
              </button>
            ))}
            <button
              onClick={() => setCustomMode(true)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                customMode
                  ? 'bg-sdt-gold-500 text-white'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              Custom
            </button>
          </div>
        </div>

        {/* System Description */}
        {!customMode && (
          <div className="mb-6 p-4 bg-slate-50 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="font-display font-semibold text-slate-900">{preset.name}</span>
              <span className="text-xs px-2 py-1 bg-sdt-primary-100 text-sdt-primary-700 rounded-full">
                {preset.scale} Scale
              </span>
            </div>
            <p className="text-sm text-slate-600">{preset.description}</p>
          </div>
        )}

        {/* Custom Inputs */}
        {customMode && (
          <div className="mb-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                k (scale factor)
              </label>
              <input
                type="text"
                value={customK}
                onChange={(e) => setCustomK(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sdt-primary-500 focus:border-transparent font-mono text-sm"
                placeholder="137"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                R (central radius, m)
              </label>
              <input
                type="text"
                value={customR}
                onChange={(e) => setCustomR(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sdt-primary-500 focus:border-transparent font-mono text-sm"
                placeholder="5.29e-11"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                r (orbital radius, m)
              </label>
              <input
                type="text"
                value={customr}
                onChange={(e) => setCustomr(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sdt-primary-500 focus:border-transparent font-mono text-sm"
                placeholder="5.29e-11"
              />
            </div>
          </div>
        )}

        {/* Parameters Display */}
        <div className="mb-6 grid grid-cols-3 gap-4 text-center">
          <div className="p-3 bg-slate-50 rounded-lg">
            <div className="text-xs text-slate-500 uppercase tracking-wide mb-1">k</div>
            <div className="font-mono text-lg text-slate-900">
              {calculation ? formatNumber(calculation.k) : '-'}
            </div>
          </div>
          <div className="p-3 bg-slate-50 rounded-lg">
            <div className="text-xs text-slate-500 uppercase tracking-wide mb-1">R</div>
            <div className="font-mono text-lg text-slate-900">
              {calculation ? formatNumber(calculation.R) : '-'} m
            </div>
          </div>
          <div className="p-3 bg-slate-50 rounded-lg">
            <div className="text-xs text-slate-500 uppercase tracking-wide mb-1">r</div>
            <div className="font-mono text-lg text-slate-900">
              {calculation ? formatNumber(calculation.r) : '-'} m
            </div>
          </div>
        </div>

        {/* Results */}
        {calculation && (
          <div className="border-t border-slate-200 pt-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {/* Predicted */}
              <div className="p-4 bg-sdt-primary-50 rounded-lg border border-sdt-primary-200">
                <div className="text-sm text-sdt-primary-600 font-medium mb-1">
                  SDT Predicted Velocity
                </div>
                <div className="font-mono text-2xl text-sdt-primary-900">
                  {formatNumber(calculation.predictedV)} m/s
                </div>
              </div>

              {/* Observed */}
              <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                <div className="text-sm text-slate-600 font-medium mb-1">
                  {customMode ? 'Reference' : 'Observed Velocity'}
                </div>
                <div className="font-mono text-2xl text-slate-900">
                  {formatNumber(calculation.observedV)} m/s
                </div>
              </div>
            </div>

            {/* Error */}
            {!customMode && (
              <div className="mt-4 p-4 bg-green-50 rounded-lg border border-green-200 text-center">
                <div className="text-sm text-green-600 font-medium mb-1">Agreement</div>
                <div className="font-mono text-3xl text-green-700">
                  {calculation.error < 0.01 ? '< 0.01' : calculation.error.toFixed(2)}% error
                </div>
                {calculation.error < 1 && (
                  <div className="text-green-600 text-sm mt-1">
                    SDT prediction matches observation
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Formula Explanation */}
        <div className="mt-6 p-4 bg-slate-50 rounded-lg text-sm text-slate-600">
          <p className="mb-2">
            <strong>The k-Law:</strong> SDT predicts that orbital velocity follows{' '}
            <code className="bg-slate-200 px-1 rounded">v = (c/k)&radic;(R/r)</code> across all
            scales - from electrons in atoms (k&asymp;137) to stars in galaxies (k&asymp;10<sup>5</sup>).
          </p>
          <p>
            This single formula replaces Kepler's laws, the Bohr model, and galactic dynamics
            with a unified geometric principle.
          </p>
        </div>
      </div>
    </div>
  );
}
