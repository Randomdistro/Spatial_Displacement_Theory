# Phase 2: Binding Energy from Geometry

## Overview

Phase 2 calculates binding energies from pure geometric occlusion using a **discovery-first methodology**. We don't assume the binding constant `k` - we discover it from data.

## Key Principle: Discovery-First

**We DISCOVER k, we don't assume it.**

1. Measure `k_i = B_exp / Omega_i` for each nucleus
2. Analyze patterns: mean, stddev, CV, family splits
3. Test universality: CV < 5%?
4. Test family-specific: Different k per family?
5. Test corrections: Overlap, compression, pairing

## Components

### 2.1 Occlusion Binding Calculator (`02_01_occlusion_binding_calculator.py`)

**Purpose**: Core calculator for binding energy from solid angle occlusion.

**Key Features**:
- Solid angle occlusion: `Omega = 2*pi*(1 - cos theta)` where `sin theta = R/d`
- Bond classification and counting
- Overlap corrections
- Discovery data structures

**Classes**:
- `Bond`: Represents a single bond between nucleons
- `NucleusBinding`: Binding energy calculation for a nucleus

### 2.2 Deuteron Calibration (`02_02_deuteron_calibration.py`)

**Purpose**: Calibrates binding constant `k` from deuteron (simplest nucleus).

**Key Features**:
- Single p-n bond
- Separation: 2.10 fm
- Binding: 2.2246 MeV
- `k = B_exp / Omega`

**Classes**:
- `DeuteronCalibration`: Calibrates k from deuteron

### 2.3 Alpha Particle Structure (`02_03_alpha_structure.py`)

**Purpose**: Analyzes alpha particle (4He) structure.

**Key Features**:
- 6 bonds in tetrahedral arrangement
- Vacuum lock compression: d = 1.45 fm
- Binding: 28.296 MeV
- Validates k from deuteron calibration

**Classes**:
- `AlphaParticleStructure`: Alpha particle analysis

### 2.4 Alpha Cluster Nuclei (`02_04_alpha_clusters.py`)

**Purpose**: Analyzes nuclei built from alpha clusters.

**Key Features**:
- C-12: 3 alphas in triangle
- O-16: 4 alphas in tetrahedron
- Be-8: 2 alphas (unstable)
- Inter-alpha bonding geometry

**Classes**:
- `AlphaClusterNucleus`: Base class for alpha clusters
- `Carbon12Structure`: C-12 analysis
- `Oxygen16Structure`: O-16 analysis
- `Beryllium8Structure`: Be-8 analysis

### 2.5 Odd-A Nuclei (`02_05_odd_A_nuclei.py`)

**Purpose**: Analyzes odd-A and mixed nuclei.

**Key Features**:
- Triton (³H): n-p-n linear
- Helion (³He): p-n-p linear
- Li-6: Alpha + Deuteron attachment
- Pairing effects and corrections

**Classes**:
- `TritonStructure`: Triton analysis
- `HelionStructure`: Helion analysis
- `Lithium6Structure`: Li-6 analysis

### 2.6 Binding Energy Discovery (`02_06_binding_energy_discovery.py`)

**Purpose**: Implements discovery-first methodology.

**Key Features**:
- Measure `k_i` for each nucleus
- Analyze patterns (mean, stddev, CV)
- Test universality
- Test family-specific k
- Identify outliers

**Classes**:
- `NucleusDiscovery`: Discovery data for single nucleus
- `DiscoveryAnalysis`: Analysis across all nuclei
- `BindingEnergyDiscovery`: Main discovery engine

### 2.7 Fit Quality Analysis (`02_07_fit_quality_analysis.py`)

**Purpose**: Comprehensive fit quality validation.

**Key Features**:
- Error metrics (RMS, mean, max)
- Correlation (R²)
- Chi-squared
- Outlier identification

**Classes**:
- `FitQualityMetrics`: Fit quality metrics
- `BindingEnergyFit`: Single fit result
- `FitQualityAnalyzer`: Quality analyzer

## Mathematical Framework

### Core Equation

```
B = k * Omega_total
```

where:
- `B` = binding energy (MeV)
- `k` = binding constant (MeV/sr) - **DISCOVERED, not assumed**
- `Omega_total` = total solid angle occlusion (steradians)

### Solid Angle Occlusion

```
Omega = 2*pi*(1 - cos theta)
```

where:
```
sin theta = R / d
```

- `R` = nucleon radius (0.84 fm)
- `d` = separation distance (fm)

### Discovery Methodology

1. **Measure k_i**: `k_i = B_exp_i / Omega_i` for each nucleus
2. **Analyze patterns**:
   - Mean: `k_mean = mean(k_i)`
   - Stddev: `k_std = std(k_i)`
   - CV: `CV = (k_std / k_mean) * 100%`
3. **Test universality**: `CV < 5%?`
4. **Test family-specific**: Different k per family?
5. **Test corrections**: Overlap, compression, pairing

## Usage

### Basic Usage

```python
from Phase_02_Binding_Energy import (
    DeuteronCalibration,
    AlphaParticleStructure,
    Carbon12Structure,
    BindingEnergyDiscovery
)

# Calibrate k from deuteron
deut_cal = DeuteronCalibration()
k = deut_cal.calibrate_k()
print(f"k = {k:.6f} MeV/sr")

# Verify with alpha
alpha = AlphaParticleStructure()
verification = alpha.verify_with_deuteron_k()
print(f"Alpha error: {verification['error_percent']:.2f}%")

# Predict C-12 binding
c12 = Carbon12Structure()
c12.calculate_total_occlusion()
B_pred = c12.predict_binding_energy(k)
print(f"C-12 predicted: {B_pred:.4f} MeV")
```

### Discovery Analysis

```python
# Create discovery engine
discovery = BindingEnergyDiscovery()

# Add nuclei
# ... add nuclei with occlusion and experimental binding ...

# Analyze
analysis = discovery.analyze()
print(analysis.get_discovery_report())

# Get best k
best_k = discovery.get_best_k()
```

## Key Constants

- `R_NUCLEON_FM = 0.84` fm (nucleon radius)
- `DIST_DEUTERON_FM = 2.10` fm (deuteron separation)
- `DIST_ALPHA_FM = 1.45` fm (alpha internal separation, compressed)
- `DIST_INTER_ALPHA_FM = 2.9` fm (inter-alpha spacing)
- `B_DEUTERON_EXP = 2.2246` MeV
- `B_ALPHA_EXP = 28.296` MeV

## Validation

Phase 2 validates:
- ✅ Deuteron calibration (k inference)
- ✅ Alpha binding (using deuteron k)
- ✅ Alpha cluster nuclei (C-12, O-16)
- ✅ Odd-A nuclei (Triton, Helion, Li-6)
- ✅ Discovery methodology (universality test)
- ✅ Fit quality (R², chi-squared, outliers)

## Next Steps

After Phase 2 is complete and validated:
- Proceed to Phase 3: Nuclear Transformations
- Use discovered k for all binding energy calculations
- Apply corrections if needed (overlap, compression, pairing)

---

**Status**: Implementation complete, ready for testing
**Date**: 2026-01-02
