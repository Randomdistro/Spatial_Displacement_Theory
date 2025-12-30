# SDT Website: Comprehensive Simulation Audit & Upgrade Plan

**Document Type:** Excessively Detailed, Excessively Structured Implementation Prompt  
**Date:** 2025-01-XX  
**Purpose:** Complete audit of all simulation components, identification of gaps, and comprehensive upgrade roadmap  
**Target Audience:** Simulations Expert Agent (Agent 3) + Integration Agent (Agent 4)

---

## EXECUTIVE SUMMARY

**Current State:** 7 simulation components exist with basic functionality  
**Completion Status:** ~40% complete  
**Critical Gaps:** Missing SDT-specific visualizations, incomplete integration, performance issues, scientific accuracy gaps  
**Priority:** HIGH - Simulations are core to SDT's educational mission

---

## PART I: CURRENT SIMULATION INVENTORY

### 1.1 Existing Simulations

#### ✅ **SimulationBase.tsx** (Foundation)
**Location:** `src/components/simulations/SimulationBase.tsx`  
**Status:** COMPLETE - Base class functional  
**Purpose:** Abstract base class providing common Three.js scene setup, animation loop, parameter management

**Current Implementation:**
- Three.js scene initialization
- Camera setup (PerspectiveCamera, 60° FOV)
- Renderer configuration (WebGLRenderer with antialiasing)
- Basic lighting (Ambient + Directional)
- Animation loop (~60 FPS target)
- Parameter management system
- Lifecycle methods (init, update, dispose, destroy)

**Strengths:**
- Clean abstraction
- Proper memory management
- Resize handling

**Weaknesses:**
- Fixed deltaTime (0.016s) - should use actual frame timing
- No performance monitoring
- No LOD system
- No Web Worker support for heavy calculations
- No viewport culling (always renders)

---

#### ✅ **PressureFieldSim.tsx** (Basic)
**Location:** `src/components/simulations/PressureFieldSim.tsx`  
**Status:** FUNCTIONAL but SIMPLIFIED  
**Purpose:** Visualizes spation pressure field around matter exclusion zones

**Current Implementation:**
- Matter sphere (exclusion zone)
- Pressure field point cloud (grid-based)
- Color gradient: Blue (low pressure) → Gold (high pressure)
- Simplified pressure calculation: `P = 1.0 - 0.5 / (distance + 0.1)`
- Rotating scene animation

**Parameters:**
- `density` (default: 5.2e96 kg/m³)
- `bulkModulus` (default: 4.6e113 Pa)
- `matterRadius` (default: 1.0)
- `fieldResolution` (default: 20)

**Strengths:**
- Basic visualization works
- Parameter system functional
- Clean React wrapper

**Critical Gaps:**
1. **Simplified Physics:** Uses `P = 1.0 - 0.5/(r+0.1)` instead of actual SDT pressure equation
2. **No Master Equation:** Doesn't implement `∇·[K_bulk ∇Δ(x)] = -κρ_disp(x)(1-E(x,ñ))`
3. **No Directional Occlusion:** Missing `E(x,ñ)` term (directional occlusion function)
4. **Static Field:** Pressure field doesn't respond to matter movement
5. **No Pressure Gradients:** Can't visualize force generation from pressure gradients
6. **Limited Resolution:** Fixed grid, no adaptive refinement
7. **No Vector Fields:** Missing pressure gradient vectors (force arrows)
8. **No Multiple Matter Objects:** Only supports single sphere
9. **No CMB Integration:** Doesn't show CMB boundary as pressure source

**Required Upgrades:**
- Implement full Master Equation solver
- Add directional occlusion visualization
- Add pressure gradient vectors (force visualization)
- Support multiple matter objects
- Add CMB boundary visualization
- Implement adaptive grid refinement
- Add interactive matter placement

---

#### ✅ **OrbitalSim.tsx** (Functional)
**Location:** `src/components/simulations/OrbitalSim.tsx`  
**Status:** FUNCTIONAL with k-law implementation  
**Purpose:** Demonstrates universal velocity law `v(r) = (c/k)√(R/r)` across scales

**Current Implementation:**
- Central body (gold sphere)
- Orbiter (blue sphere)
- Orbital trail (fading line)
- Velocity vector (green arrow)
- Optional pressure field visualization
- Scale support: atomic, planetary, galactic
- Real-time orbital parameter calculation

**Parameters:**
- `kValue` (default: 137.036)
- `R_eff` (default: 5.29177e-11 m, Bohr radius)
- `orbitalRadius` (default: 5.29177e-11 m)
- `scale` ('atomic' | 'planetary' | 'galactic')
- `showTrail` (default: true)
- `showVelocityVector` (default: true)
- `showPressureField` (default: false)

**Strengths:**
- Correct k-law implementation: `v = (C/k)√(R_eff/r)`
- Proper orbital period calculation
- Multiple scale support
- Good visualization elements

**Critical Gaps:**
1. **Single Orbiter:** Only shows one orbiting body, not multi-body systems
2. **No Precession:** Missing orbital precession effects
3. **No Eccentricity:** Circular orbits only, no elliptical orbits
4. **No Relativistic Effects:** Missing relativistic corrections for high velocities
5. **Simplified Pressure Field:** Pressure field visualization is basic, not SDT-accurate
6. **No Scale Comparison:** Can't show same law at different scales simultaneously
7. **No Energy Visualization:** Missing kinetic/potential energy displays
8. **No Angular Momentum:** Missing angular momentum conservation visualization

**Required Upgrades:**
- Multi-body orbital systems
- Elliptical orbit support
- Orbital precession visualization
- Scale comparison mode (show atomic + planetary + galactic simultaneously)
- Energy bar charts
- Angular momentum vectors
- Relativistic corrections for high-k systems

---

#### ✅ **AtomicStructureSim.tsx** (Basic)
**Location:** `src/components/simulations/AtomicStructureSim.tsx`  
**Status:** FUNCTIONAL but SIMPLIFIED  
**Purpose:** 3D visualization of SDT's toroidal electron model with helical standing waves

**Current Implementation:**
- Nucleus (red sphere)
- Toroidal electron (blue torus)
- Helical standing wave (cyan-green line)
- Optional pressure field visualization
- Orbital plane indicator
- Animated electron rotation
- Wave propagation animation

**Parameters:**
- `element` (default: 'H')
- `atomicNumber` (Z, default: 1)
- `principalQuantumNumber` (n, default: 1)
- `showElectrons` (default: true)
- `showPressureField` (default: false)
- `showHelicalWaves` (default: true)
- `showNucleus` (default: true)

**Strengths:**
- Toroidal electron visualization
- Helical wave animation
- Quantum number support

**Critical Gaps:**
1. **Simplified Helical Wave:** Uses `z = sin(m*t)` instead of proper helical quantization
2. **No Multi-Electron Atoms:** Only hydrogen (Z=1), no multi-electron systems
3. **No Electron Spin:** Missing spin visualization
4. **No Orbital Shapes:** Missing p, d, f orbital shapes
5. **No Energy Levels:** Missing energy level visualization
6. **No Spectral Lines:** Can't show transitions between energy levels
7. **Incorrect Wave Function:** Helical wave doesn't match SDT's actual quantization
8. **No Pressure Field Integration:** Pressure field doesn't show electron exclusion properly
9. **No Chemical Bonding:** Can't show how atoms bond via pressure field interactions

**Required Upgrades:**
- Proper helical quantization: `ψ(r,θ,φ) = R(r)Y(θ,φ)e^(imφ)` with toroidal topology
- Multi-electron atom support (He, Li, etc.)
- Orbital shape visualization (s, p, d, f)
- Energy level diagram
- Spectral line transitions
- Electron spin visualization
- Chemical bonding visualization (pressure field overlap)
- Proper SDT wave function implementation

---

#### ✅ **GalaxyRotationSim.tsx** (Functional)
**Location:** `src/components/simulations/GalaxyRotationSim.tsx`  
**Status:** FUNCTIONAL with SDT disk eclipse model  
**Purpose:** Demonstrates flat rotation curves without dark matter using disk eclipse saturation

**Current Implementation:**
- Galaxy disk (exponential profile)
- Central bulge
- Rotation curve visualization (3D line)
- Dark matter comparison curve (optional)
- Test particles at different radii
- Occlusion visualization (optional)
- Animated particle orbits

**Parameters:**
- `diskRadius` (R_d, default: 3.0 kpc)
- `galaxyMass` (default: 1e11 solar masses)
- `showRotationCurve` (default: true)
- `compareDarkMatter` (default: false)
- `showDisk` (default: true)
- `showPressureOcclusion` (default: false)

**Strengths:**
- SDT disk eclipse model implemented
- Rotation curve calculation: `E(r)` saturation → flat rotation
- Dark matter comparison option
- Good visualization

**Critical Gaps:**
1. **Simplified Occlusion:** Uses `E(r) = 0.64*(1-exp(-(r/R_d-1)))` approximation, not full calculation
2. **No Spiral Arms:** Disk is featureless, missing spiral arm structure
3. **No 3D Structure:** Flat disk only, no vertical structure
4. **No Gas/Dust:** Missing interstellar medium visualization
5. **No Star Formation:** Can't show star formation in spiral arms
6. **No CMB Integration:** Doesn't show CMB as pressure source
7. **No Pressure Field Visualization:** Pressure occlusion shown as points, not field
8. **No Velocity Dispersion:** Missing velocity dispersion (σ) visualization

**Required Upgrades:**
- Full disk eclipse calculation (not approximation)
- Spiral arm structure
- 3D disk structure (vertical scale height)
- Interstellar medium (gas/dust)
- CMB pressure source visualization
- Pressure field gradient visualization
- Velocity dispersion maps
- Star formation regions

---

#### ✅ **BenchmarkVisualizer.tsx** (Basic)
**Location:** `src/components/simulations/BenchmarkVisualizer.tsx`  
**Status:** FUNCTIONAL but LIMITED  
**Purpose:** Interactive visualization of SDT benchmark validation results

**Current Implementation:**
- 3D grid of benchmark cards
- Color coding by status (certified/investigation/predicted)
- Comparison chart mode (predicted vs observed bars)
- 2D layout mode
- Statistics display
- Benchmark selection

**Parameters:**
- `selectedBenchmark` (string ID)
- `showAll` (default: true)
- `categoryFilter` (string)
- `statusFilter` ('certified' | 'investigation' | 'predicted' | 'all')
- `viewMode` ('3d' | '2d' | 'comparison')

**Strengths:**
- Multiple view modes
- Status tracking
- Basic comparison visualization

**Critical Gaps:**
1. **No Text Labels:** Cards have no text (simplified indicator only)
2. **No Error Visualization:** Error bars not properly visualized
3. **No Data Export:** Can't export benchmark data
4. **No Filtering:** Category/status filters not implemented
5. **No Detailed View:** Clicking benchmark doesn't show detailed analysis
6. **No Historical Data:** Can't show benchmark evolution over time
7. **No Statistical Analysis:** Missing error distribution, confidence intervals
8. **Hardcoded Data:** Uses default benchmarks, not loaded from API

**Required Upgrades:**
- Text labels on cards (use TextGeometry or HTML overlay)
- Proper error bar visualization
- Detailed benchmark view (expanded card)
- Category/status filtering
- Data export (CSV, JSON)
- Statistical analysis (error distributions, confidence intervals)
- API integration for benchmark data
- Historical tracking

---

#### ✅ **TheClearingSim.tsx** (NEW - Complete)
**Location:** `src/components/simulations/TheClearingSim.tsx`  
**Status:** COMPLETE - Just created  
**Purpose:** Visualizes recombination era from SDT perspective

**Current Implementation:**
- Four-phase system (Plasma Opaque → Cooling → Recombination → Clear)
- Baryon/electron particle soup
- Photon scattering cloud
- Pressure field emergence
- Matter clump formation (hydrogen atoms)
- Temperature-driven phase transitions
- Interactive controls

**Strengths:**
- Complete phase system
- Good particle dynamics
- SDT pressure field integration
- Educational value

**Minor Gaps:**
1. **Simplified Physics:** Particle interactions are simplified
2. **No Sound Waves:** Missing sound wave propagation (user mentioned sound favored)
3. **No Heat Emission:** Missing "emitted heat every step of the way down"
4. **No BAO Connection:** Doesn't show BAO as blast radii (user's hypothesis)

**Future Enhancements:**
- Add sound wave visualization
- Add heat emission visualization
- Connect to BAO scale visualization
- Add more realistic particle interactions

---

#### ✅ **FormulaRenderer.tsx** (Complete)
**Location:** `src/components/simulations/FormulaRenderer.tsx`  
**Status:** COMPLETE  
**Purpose:** Renders LaTeX formulas using KaTeX with animation support

**Current Implementation:**
- KaTeX integration
- Inline and block modes
- Animated formula reveal
- Term highlighting
- Master Equation component
- k-Law Formula component

**Strengths:**
- Fully functional
- Good animation support
- Clean API

**Minor Enhancements:**
- Add more formula templates
- Add interactive formula exploration
- Add formula derivation steps

---

### 1.2 Integration Components

#### ✅ **SimulationViewer.tsx** (Stub)
**Location:** `src/components/walkthrough/SimulationViewer.tsx`  
**Status:** STUB - Only supports PressureFieldSim  
**Purpose:** Maps simulation IDs to components for use in content nodes

**Current Implementation:**
- Switch statement mapping `simulationId` to component
- Only `'pressure-field'` case implemented
- Default case shows "being prepared" message

**Critical Gap:**
- **Missing All Other Simulations:** Only PressureFieldSim integrated
- Need to add: OrbitalSim, AtomicStructureSim, GalaxyRotationSim, BenchmarkVisualizer, TheClearingSim

**Required:**
- Add all simulation cases
- Add parameter mapping from content JSON
- Add error handling
- Add loading states

---

#### ✅ **SimulationIntegration.tsx** (Visual Marker)
**Location:** `src/components/3d/SimulationIntegration.tsx`  
**Status:** COMPLETE - Visual indicator only  
**Purpose:** Marks simulation positions in 3D space

**Current Implementation:**
- Gold pulsing sphere indicator
- Position marking
- Visibility control

**Note:** This is just a visual marker. Actual simulations render in HTML via SimulationViewer.

---

## PART II: MISSING SIMULATIONS (Critical Gaps)

### 2.1 SDT-Specific Visualizations (HIGH PRIORITY)

#### ❌ **SpationLatticeSim.tsx** (MISSING)
**Purpose:** Visualize the fundamental spation lattice structure at Planck scale

**Required Features:**
- Dodecahedral packing structure
- Planck-scale spacing visualization
- K_bulk emergence from lattice geometry
- Lattice deformation under pressure
- 3D interactive exploration
- Zoom from macroscopic to Planck scale

**SDT Concepts:**
- Spation density: ρ_spation = 5.2×10⁹⁶ kg/m³
- Bulk modulus: K_bulk = 4.6×10¹¹³ Pa
- Lattice spacing: ~10⁻³⁵ m (Planck scale)
- Dodecahedral geometry

**Implementation Requirements:**
- Custom geometry generator for dodecahedral packing
- Pressure visualization on lattice
- Interactive zoom (43 orders of magnitude)
- Lattice vibration modes
- Connection to Master Equation

---

#### ❌ **CMBBoundarySim.tsx** (MISSING)
**Purpose:** Visualize CMB boundary as the structural boundary where all pressure originates

**Required Features:**
- CMB boundary sphere (z=1089, r=4.4×10²⁶ m)
- Pressure volume counting visualization
- Pressure gradient from CMB to observer
- Photon decoupling visualization
- Redshift mechanism (pressure gradient climbing)
- BAO scale visualization (147 Mpc pressure waves)

**SDT Concepts:**
- CMB pressure: P_CMB = 2.036×10⁻² Pa
- Pressure volume counting: z×k²=1 shells
- BAO as pressure wave features
- Redshift from pressure gradient, not expansion

**Implementation Requirements:**
- Large-scale visualization (cosmological scale)
- Pressure gradient arrows
- Volume counting animation
- BAO feature highlighting
- Redshift visualization

---

#### ❌ **ForceHierarchySim.tsx** (MISSING)
**Purpose:** Visualize how all forces emerge from the same pressure field with different occlusion regimes

**Required Features:**
- Coulomb force: E→0 (low occlusion)
- Gravity: E→1-η (high occlusion)
- Force comparison visualization
- Occlusion regime visualization
- Force strength comparison (log scale)
- CMB as source visualization

**SDT Concepts:**
- F_Coulomb = (π/4)P_CMB (R_N²R_e²/r²) when E→0
- F_Gravity = (π/4)P_CMB (R₁²R₂²/r²)(1-η) when E→1-η
- Same pressure source (CMB), different occlusion

**Implementation Requirements:**
- Two-body force visualization
- Occlusion parameter slider
- Force strength comparison
- CMB source visualization
- Transition between force regimes

---

#### ❌ **ChemicalBondingSim.tsx** (MISSING)
**Purpose:** Visualize chemical bonding as pressure field overlap between atoms

**Required Features:**
- Multiple atoms with pressure exclusion zones
- Pressure field overlap visualization
- Bond formation animation
- Bond energy visualization
- Molecular geometry (VSEPR)
- Periodic table connection

**SDT Concepts:**
- Bonds form when pressure fields overlap
- Bond strength from pressure gradient
- Nuclear structure determines chemistry
- No quantum orbitals needed

**Implementation Requirements:**
- Multi-atom pressure field visualization
- Overlap region highlighting
- Bond energy calculation
- Molecular structure prediction
- Connection to atomic structure sim

---

#### ❌ **BAOBlastRadiusSim.tsx** (MISSING - User Hypothesis)
**Purpose:** Visualize BAO scale as blast radii of supermassive black holes

**Required Features:**
- SMBH visualization
- Blast radius calculation
- BAO scale (147 Mpc) overlay
- Pressure wave propagation
- Multiple SMBH blast radii
- Comparison to observed BAO

**User's Hypothesis:**
- BAO are blast radii of SMBHs
- Each 10⁸⁰ baryon/electron pair emitted heat
- Sound waves favored (straight run capability)
- BAO scale matches SMBH blast radii

**Implementation Requirements:**
- SMBH visualization
- Blast radius calculation
- Pressure wave visualization
- BAO scale comparison
- Heat emission visualization

---

### 2.2 Enhanced Versions of Existing Simulations

#### 🔄 **PressureFieldSim.tsx** → **PressureFieldSimAdvanced.tsx**
**Upgrade Required:** Full Master Equation implementation

**New Features:**
- Master Equation solver: `∇·[K_bulk ∇Δ(x)] = -κρ_disp(x)(1-E(x,ñ))`
- Directional occlusion `E(x,ñ)` visualization
- Multiple matter objects
- Pressure gradient vectors (force arrows)
- CMB boundary integration
- Adaptive grid refinement
- Interactive matter placement
- Real-time field updates

---

#### 🔄 **AtomicStructureSim.tsx** → **AtomicStructureSimAdvanced.tsx**
**Upgrade Required:** Full SDT atomic model

**New Features:**
- Proper helical quantization
- Multi-electron atoms (He, Li, Be, etc.)
- Orbital shapes (s, p, d, f)
- Energy level diagram
- Spectral line transitions
- Electron spin visualization
- Chemical bonding integration
- Periodic table connection

---

#### 🔄 **OrbitalSim.tsx** → **OrbitalSimAdvanced.tsx**
**Upgrade Required:** Multi-body and advanced features

**New Features:**
- Multi-body orbital systems
- Elliptical orbits
- Orbital precession
- Scale comparison mode
- Energy visualization
- Angular momentum vectors
- Relativistic corrections

---

#### 🔄 **GalaxyRotationSim.tsx** → **GalaxyRotationSimAdvanced.tsx**
**Upgrade Required:** Full disk eclipse and structure

**New Features:**
- Full disk eclipse calculation
- Spiral arm structure
- 3D disk (vertical scale height)
- Interstellar medium
- CMB pressure source
- Pressure field gradients
- Velocity dispersion maps

---

## PART III: INTEGRATION GAPS

### 3.1 Content Node Integration

**Current State:**
- `SimulationViewer.tsx` only supports `'pressure-field'`
- Content nodes reference simulations via `simulation-id` in JSON
- No simulation parameters in content JSON structure

**Required:**
1. **Expand SimulationViewer:**
   - Add all simulation cases
   - Map simulation IDs from content JSON
   - Pass parameters from content JSON

2. **Content JSON Structure:**
   ```json
   {
     "expansions": {
       "simulation": {
         "id": "pressure-field",
         "parameters": {
           "density": 5.2e96,
           "bulkModulus": 4.6e113
         }
       }
     }
   }
   ```

3. **Node Room Integration:**
   - Show simulation indicator in 3D space
   - Click to open simulation overlay
   - Simulation renders in expandable content panel

---

### 3.2 Walkthrough Integration

**Current State:**
- `WalkthroughApp.tsx` has domain visualizations
- Simulations not integrated into walkthrough flow
- No simulation triggers at scale points

**Required:**
1. **Scale Point Simulations:**
   - Each scale point should trigger relevant simulation
   - Simulations show SDT perspective at that scale
   - Smooth transitions between simulations

2. **Domain-Specific Simulations:**
   - Domain 1 (Planck): SpationLatticeSim
   - Domain 2 (Atomic): AtomicStructureSimAdvanced
   - Domain 3 (Molecular): ChemicalBondingSim
   - Domain 4 (Macroscopic): ForceHierarchySim
   - Domain 5 (Stellar): OrbitalSimAdvanced
   - Domain 6 (Galactic): GalaxyRotationSimAdvanced
   - Domain 7 (Cosmological): CMBBoundarySim

---

### 3.3 Performance Integration

**Current State:**
- No performance monitoring
- No LOD system
- No viewport culling
- Fixed quality settings

**Required:**
1. **Performance Monitor:**
   - FPS tracking
   - Frame time measurement
   - Component render time
   - Memory usage tracking

2. **LOD System:**
   - Quality levels (low/medium/high)
   - Automatic quality adjustment
   - Mobile optimization

3. **Viewport Culling:**
   - Only render visible simulations
   - Pause off-screen simulations
   - Resume when visible

---

## PART IV: SCIENTIFIC ACCURACY GAPS

### 4.1 Physics Implementation Issues

#### **PressureFieldSim.tsx**
- ❌ Uses simplified `P = 1.0 - 0.5/(r+0.1)` instead of Master Equation
- ❌ Missing directional occlusion `E(x,ñ)`
- ❌ No pressure gradient calculation
- ❌ No force vector visualization

#### **AtomicStructureSim.tsx**
- ❌ Helical wave uses `sin(m*t)` instead of proper quantization
- ❌ Missing SDT wave function: `ψ(r,θ,φ) = R(r)Y(θ,φ)e^(imφ)` with toroidal topology
- ❌ No energy level calculation from helical quantization
- ❌ Missing spectral line predictions

#### **GalaxyRotationSim.tsx**
- ❌ Uses approximation `E(r) = 0.64*(1-exp(-(r/R_d-1)))` instead of full calculation
- ❌ Missing CMB pressure source integration
- ❌ No pressure gradient visualization

#### **OrbitalSim.tsx**
- ✅ Correct k-law implementation
- ❌ Missing relativistic corrections for high velocities
- ❌ No precession effects

---

### 4.2 Missing SDT Concepts

1. **Pressure Volume Counting:**
   - z×k²=1 shells from Planck to CMB
   - Not visualized anywhere

2. **CMB as Energy Source:**
   - All pressure originates from CMB boundary
   - Not shown in pressure field simulations

3. **Directional Occlusion:**
   - `E(x,ñ)` function not visualized
   - Critical for understanding force hierarchy

4. **Static Universe:**
   - Redshift from pressure gradient climbing
   - Not visualized in cosmological simulations

5. **No Dark Matter:**
   - Galaxy rotation from disk eclipse
   - Shown but could be more detailed

---

## PART V: UI/UX IMPROVEMENTS NEEDED

### 5.1 Interactive Controls

**Current State:**
- Basic parameter sliders
- Limited interactivity
- No tooltips or help text

**Required:**
1. **Enhanced Controls:**
   - Tooltips explaining parameters
   - Real-time value display
   - Parameter presets
   - Reset to defaults button

2. **Visual Feedback:**
   - Highlight changed parameters
   - Show parameter effects immediately
   - Animation previews

3. **Accessibility:**
   - Keyboard navigation
   - Screen reader support
   - High contrast mode
   - Reduced motion support

---

### 5.2 Educational Features

**Current State:**
- Basic labels
- Formula overlays
- Limited explanations

**Required:**
1. **Guided Tours:**
   - Step-by-step explanations
   - Highlight key features
   - Interactive tutorials

2. **Concept Explanations:**
   - Pop-up explanations
   - Expandable details
   - Related concepts links

3. **Comparison Modes:**
   - SDT vs Standard Model
   - Side-by-side comparisons
   - Toggle between views

---

### 5.3 Mobile Optimization

**Current State:**
- Basic responsive design
- Touch gestures not implemented
- Performance not optimized

**Required:**
1. **Touch Controls:**
   - Pinch to zoom
   - Pan to rotate
   - Tap to interact

2. **Performance:**
   - Reduced particle counts
   - Lower quality settings
   - Simplified visualizations

3. **UI Adaptation:**
   - Larger touch targets
   - Simplified controls
   - Mobile-specific layouts

---

## PART VI: TECHNICAL DEBT & CODE QUALITY

### 6.1 Code Issues

1. **Fixed DeltaTime:**
   - `SimulationBase.tsx` uses `deltaTime = 0.016` (fixed)
   - Should use actual frame timing
   - Causes timing issues

2. **Memory Leaks:**
   - Some simulations don't properly dispose geometries
   - Trail points accumulate without limit
   - Need better cleanup

3. **Type Safety:**
   - Some `any` types in parameters
   - Missing TypeScript interfaces
   - Need stricter typing

4. **Error Handling:**
   - Limited error boundaries
   - No graceful degradation
   - Missing error messages

---

### 6.2 Architecture Issues

1. **No Simulation Registry:**
   - Simulations hardcoded in SimulationViewer
   - Should use registry pattern
   - Makes adding simulations difficult

2. **No Parameter Validation:**
   - Parameters not validated
   - Can cause runtime errors
   - Need validation layer

3. **No State Management:**
   - Each simulation manages own state
   - No shared state
   - Difficult to coordinate multiple simulations

---

## PART VII: IMPLEMENTATION PRIORITY MATRIX

### Priority 1: CRITICAL (Must Have)

1. **Expand SimulationViewer** - Add all existing simulations
2. **Fix Scientific Accuracy** - Implement proper Master Equation, wave functions
3. **SpationLatticeSim** - Core SDT visualization
4. **CMBBoundarySim** - Critical cosmological concept
5. **ForceHierarchySim** - Shows force unification

**Timeline:** 2-3 weeks

---

### Priority 2: HIGH (Should Have)

6. **ChemicalBondingSim** - Important for chemistry
7. **Upgrade PressureFieldSim** - Full Master Equation
8. **Upgrade AtomicStructureSim** - Proper quantization
9. **Performance Monitoring** - Ensure 60 FPS
10. **Mobile Optimization** - Touch controls, LOD

**Timeline:** 3-4 weeks

---

### Priority 3: MEDIUM (Nice to Have)

11. **BAOBlastRadiusSim** - User hypothesis visualization
12. **Upgrade OrbitalSim** - Multi-body, elliptical
13. **Upgrade GalaxyRotationSim** - Full structure
14. **Enhanced UI Controls** - Tooltips, presets
15. **Guided Tours** - Educational features

**Timeline:** 4-6 weeks

---

### Priority 4: LOW (Future)

16. **Benchmark Visualizer Upgrades** - Text labels, filtering
17. **Simulation Registry** - Architecture improvement
18. **State Management** - Shared simulation state
19. **Web Workers** - Heavy calculations
20. **VR Support** - Immersive experience

**Timeline:** 6+ weeks

---

## PART VIII: DETAILED IMPLEMENTATION SPECIFICATIONS

### 8.1 SpationLatticeSim.tsx Specification

**File:** `src/components/simulations/SpationLatticeSim.tsx`

**Purpose:** Visualize the fundamental spation lattice structure

**Key Features:**
1. **Dodecahedral Packing:**
   - Generate dodecahedral unit cells
   - Show packing structure
   - Visualize lattice spacing (~10⁻³⁵ m)

2. **Pressure Visualization:**
   - Show pressure on lattice points
   - Visualize K_bulk emergence
   - Deformation under load

3. **Scale Navigation:**
   - Zoom from 1 m to 10⁻³⁵ m (35 orders of magnitude)
   - Smooth scale transitions
   - LOD system for performance

4. **Interactive Exploration:**
   - Rotate lattice
   - Select lattice points
   - Show pressure values
   - Deform lattice interactively

**Parameters:**
```typescript
{
  scale: number; // Current scale (log10 meters)
  showPressure: boolean;
  showDeformation: boolean;
  latticeResolution: number; // Points per unit cell
  zoomLevel: number; // 0-35 (orders of magnitude)
}
```

**SDT Equations:**
- Spation density: ρ_spation = 5.2×10⁹⁶ kg/m³
- Bulk modulus: K_bulk = 4.6×10¹¹³ Pa
- Lattice spacing: a_0 ≈ 10⁻³⁵ m

**Visualization:**
- Dodecahedral wireframe (gold)
- Pressure color coding (blue → gold)
- Deformation vectors
- Scale indicator

---

### 8.2 CMBBoundarySim.tsx Specification

**File:** `src/components/simulations/CMBBoundarySim.tsx`

**Purpose:** Visualize CMB boundary as pressure source

**Key Features:**
1. **CMB Boundary Sphere:**
   - Radius: r_CMB = 4.4×10²⁶ m
   - Redshift: z = 1089
   - Pressure: P_CMB = 2.036×10⁻² Pa

2. **Pressure Volume Counting:**
   - Show z×k²=1 shells
   - Count from Planck to CMB
   - Visualize volume accumulation

3. **Pressure Gradients:**
   - Arrows showing pressure direction
   - Gradient strength visualization
   - Force generation from gradients

4. **BAO Features:**
   - Highlight 147 Mpc scale
   - Show pressure wave features
   - Connect to user's SMBH hypothesis

5. **Redshift Visualization:**
   - Show pressure gradient climbing
   - Compare to expansion model
   - Demonstrate static universe

**Parameters:**
```typescript
{
  showCMBBoundary: boolean;
  showPressureGradients: boolean;
  showBAOFeatures: boolean;
  showVolumeCounting: boolean;
  observerPosition: [number, number, number]; // Observer location
}
```

**SDT Concepts:**
- CMB pressure: P_CMB = 2.036×10⁻² Pa
- Pressure volume counting: z×k²=1
- BAO scale: 147 Mpc
- Redshift: Δz from pressure gradient

**Visualization:**
- CMB boundary (translucent sphere, gold)
- Pressure gradient arrows (blue → gold)
- BAO features (highlighted regions)
- Volume shells (semi-transparent)

---

### 8.3 ForceHierarchySim.tsx Specification

**File:** `src/components/simulations/ForceHierarchySim.tsx`

**Purpose:** Show force unification via occlusion regimes

**Key Features:**
1. **Two-Body System:**
   - Two objects with exclusion zones
   - Pressure field between them
   - Force visualization

2. **Occlusion Regime Control:**
   - Slider: E from 0 to 1-η
   - Show transition between forces
   - E→0: Coulomb force
   - E→1-η: Gravity

3. **Force Comparison:**
   - Side-by-side force visualization
   - Log scale comparison
   - Same pressure source (CMB)

4. **CMB Source:**
   - Show CMB as pressure source
   - Pressure propagation
   - Force generation mechanism

**Parameters:**
```typescript
{
  object1Radius: number; // R₁
  object2Radius: number; // R₂
  separation: number; // r
  occlusionE: number; // E (0 to 1-η)
  showCMBSource: boolean;
  compareForces: boolean; // Show both forces
}
```

**SDT Equations:**
- F_Coulomb = (π/4)P_CMB (R_N²R_e²/r²) when E→0
- F_Gravity = (π/4)P_CMB (R₁²R₂²/r²)(1-η) when E→1-η
- Same pressure source, different occlusion

**Visualization:**
- Two objects (spheres)
- Pressure field (color gradient)
- Force arrows (magnitude/direction)
- CMB source (distant sphere)
- Occlusion visualization (transparency)

---

### 8.4 ChemicalBondingSim.tsx Specification

**File:** `src/components/simulations/ChemicalBondingSim.tsx`

**Purpose:** Visualize bonding as pressure field overlap

**Key Features:**
1. **Multi-Atom System:**
   - Place multiple atoms
   - Show pressure exclusion zones
   - Visualize overlap regions

2. **Bond Formation:**
   - Animate atoms approaching
   - Show pressure field overlap
   - Highlight bond region
   - Calculate bond energy

3. **Molecular Geometry:**
   - Predict molecular structure
   - Show VSEPR-like geometry
   - Pressure field determines shape

4. **Periodic Table Connection:**
   - Select elements
   - Show nuclear structure
   - Predict bonding behavior

**Parameters:**
```typescript
{
  atoms: Array<{
    element: string;
    position: [number, number, number];
  }>;
  showPressureFields: boolean;
  showBonds: boolean;
  showEnergy: boolean;
  showGeometry: boolean;
}
```

**SDT Concepts:**
- Bonds from pressure field overlap
- Bond strength from pressure gradient
- Nuclear structure → chemistry
- No quantum orbitals

**Visualization:**
- Atoms (colored by element)
- Pressure fields (exclusion zones)
- Overlap regions (highlighted)
- Bonds (lines/cylinders)
- Energy display (text/bar)

---

## PART IX: TESTING REQUIREMENTS

### 9.1 Unit Tests

**Required Tests:**
1. **SimulationBase:**
   - Initialization
   - Parameter updates
   - Lifecycle methods
   - Memory cleanup

2. **Each Simulation:**
   - Parameter validation
   - Physics calculations
   - Visualization updates
   - Error handling

---

### 9.2 Integration Tests

**Required Tests:**
1. **SimulationViewer:**
   - All simulation IDs map correctly
   - Parameters pass through
   - Error handling works

2. **Content Integration:**
   - Simulations load from JSON
   - Parameters from content work
   - Expandable content integration

---

### 9.3 Performance Tests

**Required Tests:**
1. **Frame Rate:**
   - Maintain 60 FPS on desktop
   - Maintain 30 FPS on mobile
   - No frame drops

2. **Memory:**
   - No memory leaks
   - Proper cleanup
   - Memory usage within limits

3. **Load Time:**
   - Simulations load <1 second
   - No blocking operations
   - Progressive loading

---

## PART X: DOCUMENTATION REQUIREMENTS

### 10.1 Code Documentation

**Required:**
1. **JSDoc Comments:**
   - All public methods
   - Parameter descriptions
   - Return value descriptions
   - Usage examples

2. **README Files:**
   - Each simulation component
   - Usage instructions
   - Parameter reference
   - Examples

---

### 10.2 User Documentation

**Required:**
1. **Simulation Guides:**
   - What each simulation shows
   - How to use controls
   - What SDT concepts it demonstrates

2. **Educational Content:**
   - Physics explanations
   - SDT perspective
   - Comparison to standard model

---

## PART XI: SUCCESS CRITERIA

### 11.1 Functional Requirements

✅ All Priority 1 simulations implemented  
✅ All existing simulations upgraded  
✅ SimulationViewer supports all simulations  
✅ Simulations integrated into content nodes  
✅ Performance targets met (60 FPS desktop, 30 FPS mobile)

---

### 11.2 Scientific Accuracy

✅ Master Equation properly implemented  
✅ SDT wave functions correct  
✅ Pressure calculations accurate  
✅ Force hierarchy demonstrated  
✅ CMB integration shown

---

### 11.3 User Experience

✅ Intuitive controls  
✅ Clear visualizations  
✅ Educational value  
✅ Mobile friendly  
✅ Accessible

---

## PART XII: IMPLEMENTATION TIMELINE

### Week 1-2: Critical Foundations
- Expand SimulationViewer
- Fix scientific accuracy in existing simulations
- Implement SpationLatticeSim
- Implement CMBBoundarySim

### Week 3-4: Core SDT Visualizations
- Implement ForceHierarchySim
- Implement ChemicalBondingSim
- Upgrade PressureFieldSim (Master Equation)
- Upgrade AtomicStructureSim (proper quantization)

### Week 5-6: Integration & Polish
- Integrate into content nodes
- Integrate into walkthrough
- Performance optimization
- Mobile optimization

### Week 7-8: Advanced Features
- BAOBlastRadiusSim (user hypothesis)
- Enhanced UI controls
- Guided tours
- Documentation

---

## CONCLUSION

This document provides an excessively detailed, excessively structured roadmap for completing and upgrading all SDT website simulations. The priority matrix ensures critical SDT concepts are visualized first, while the detailed specifications provide clear implementation guidance.

**Next Steps:**
1. Review and approve this plan
2. Begin Priority 1 implementations
3. Iterate based on user feedback
4. Continue through priority matrix

**Success Metric:** Users can visualize and understand all core SDT concepts through interactive simulations that are scientifically accurate, performant, and educational.

---

**End of Document**

