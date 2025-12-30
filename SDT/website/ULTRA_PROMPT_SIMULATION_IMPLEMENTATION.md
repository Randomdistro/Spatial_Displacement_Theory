# ULTRA PROMPT: SDT Website Simulation Implementation Guide
## Excessively Descriptive, Excessively Structured Implementation Specification

**Document Purpose:** Complete implementation guide for all SDT website simulations with exhaustive toolchain, library, styling, and architecture documentation  
**Target:** Simulations Expert Agent (Agent 3) + Integration Agent (Agent 4)  
**Status:** 
- ✅ CMBBoundarySim (LET THERE BE LIGHT!) - COMPLETE
- ✅ TheClearingSim (Recombination Era) - COMPLETE  
**Date:** 2025-01-XX

---

## TABLE OF CONTENTS

1. [Complete Toolchain Documentation](#part-i-complete-toolchain-documentation)
2. [Library Specifications & Usage](#part-ii-library-specifications--usage)
3. [Styling System Deep Dive](#part-iii-styling-system-deep-dive)
4. [Architecture & File Structure](#part-iv-architecture--file-structure)
5. [Code Patterns & Conventions](#part-v-code-patterns--conventions)
6. [Simulation Implementation Specifications](#part-vi-simulation-implementation-specifications)
7. [Integration Patterns](#part-vii-integration-patterns)
8. [Performance Optimization](#part-viii-performance-optimization)
9. [Testing & Quality Assurance](#part-ix-testing--quality-assurance)
10. [Deployment & Build Process](#part-x-deployment--build-process)

---

## PART I: COMPLETE TOOLCHAIN DOCUMENTATION

### 1.1 Core Framework Stack

#### **Astro 4.0.0** (Static Site Generator)
**Purpose:** Base framework for static site generation with island architecture  
**Configuration:** `astro.config.mjs`

**Key Features Used:**
- **Static Site Generation (SSG):** Pre-renders pages at build time
- **Island Architecture:** React components hydrated only when needed (`client:load`, `client:visible`)
- **Markdown Support:** Shiki syntax highlighting with `github-dark` theme
- **Path Aliases:** Configured in `vite.resolve.alias` for clean imports

**Configuration Details:**
```javascript
// astro.config.mjs
export default defineConfig({
  site: 'https://sdt-theory.org',
  server: { port: 3001, host: true },
  integrations: [react(), tailwind()],
  markdown: {
    shikiConfig: { theme: 'github-dark', wrap: true }
  },
  vite: {
    resolve: {
      alias: {
        '@': './src',
        '@components': './src/components',
        '@layouts': './src/layouts',
        '@store': './src/store',
        '@utils': './src/utils',
        '@types': './src/types',
      }
    }
  }
});
```

**Build Process:**
- `npm run build` → Generates static HTML/CSS/JS in `dist/`
- `npm run preview` → Serves built site locally
- `npm run dev` → Development server with HMR

**Island Architecture Pattern:**
```astro
---
// Astro component (server-side)
import SimulationComponent from '@components/simulations/PressureFieldSim';
---
<SimulationComponent 
  id="pressure-field"
  parameters={{ density: 5.2e96 }}
  client:load  // Hydrate immediately
  // OR
  client:visible  // Hydrate when visible
/>
```

---

#### **React 18.2.0** (UI Framework)
**Purpose:** Interactive component framework for simulations  
**Integration:** Via `@astrojs/react` v3.0.0

**Key React Patterns Used:**
- **Functional Components:** All simulations use function components with hooks
- **Hooks:** `useState`, `useEffect`, `useRef`, `useMemo`, `useCallback`
- **Refs:** For DOM elements (`containerRef`) and Three.js objects (`simulationRef`)
- **Effect Cleanup:** Proper disposal in `useEffect` return functions

**Component Structure Pattern:**
```typescript
export const SimulationComponent: React.FC<SimulationProps> = ({
  id,
  parameters,
  showFormulas = true,
  showLabels = true,
  onReady,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const simulationRef = useRef<SimulationClass | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    
    // Initialize simulation
    const sim = new SimulationClass(containerRef.current);
    sim.setParameters(parameters);
    sim.init();
    simulationRef.current = sim;
    sim.play();

    // Cleanup
    return () => {
      sim.destroy();
      simulationRef.current = null;
    };
  }, []);

  // Parameter updates
  useEffect(() => {
    if (simulationRef.current) {
      simulationRef.current.setParameters(parameters);
    }
  }, [parameters]);

  return (
    <div ref={containerRef} className="w-full h-full min-h-[400px]" />
  );
};
```

---

#### **TypeScript 5.3.0** (Type Safety)
**Purpose:** Type-safe development with strict checking  
**Configuration:** `tsconfig.json` (implicit, Astro-managed)

**Type Patterns:**
- **Interfaces:** All props use `interface` definitions
- **Type Exports:** Re-exported from `index.ts` files
- **Generic Types:** Used in framework utilities
- **Strict Null Checks:** All refs checked before use

**Example Type Definitions:**
```typescript
export interface SimulationProps {
  id: string;
  parameters: Record<string, number>;
  onParameterChange?: (key: string, value: number) => void;
  showFormulas?: boolean;
  showLabels?: boolean;
  narrationEnabled?: boolean;
  onReady?: () => void;
}

export interface SimulationState {
  isPlaying: boolean;
  time: number;
  cameraPosition?: [number, number, number];
}
```

---

### 1.2 3D Rendering Stack

#### **Three.js 0.160.0** (3D Graphics Library)
**Purpose:** WebGL-based 3D rendering engine  
**Usage Pattern:** Direct Three.js API (not React Three Fiber for simulations)

**Key Three.js APIs Used:**

**Scene Management:**
```typescript
import * as THREE from 'three';

// Scene creation
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0a);

// Camera setup
const camera = new THREE.PerspectiveCamera(
  60,  // FOV
  width / height,  // Aspect
  0.1,  // Near plane
  1000  // Far plane
);
camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0);

// Renderer setup
const renderer = new THREE.WebGLRenderer({ 
  antialias: true, 
  alpha: true 
});
renderer.setSize(width, height);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
```

**Geometry Creation:**
```typescript
// Sphere
const geometry = new THREE.SphereGeometry(radius, widthSegments, heightSegments);

// Torus (for electron model)
const torusGeometry = new THREE.TorusGeometry(
  radius,      // Major radius
  tubeRadius,  // Minor radius
  radialSegments,
  tubularSegments
);

// Custom BufferGeometry (for particle systems)
const geometry = new THREE.BufferGeometry();
geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
```

**Material System:**
```typescript
// Standard material (PBR)
const material = new THREE.MeshStandardMaterial({
  color: 0x1a365d,
  metalness: 0.8,
  roughness: 0.2,
  emissive: 0x000000,
  emissiveIntensity: 0.3,
  transparent: true,
  opacity: 0.8
});

// Points material (for particle systems)
const pointsMaterial = new THREE.PointsMaterial({
  size: 0.05,
  vertexColors: true,
  transparent: true,
  opacity: 0.8,
  sizeAttenuation: true
});
```

**Animation Loop:**
```typescript
const animate = () => {
  requestAnimationFrame(animate);
  
  const deltaTime = 0.016; // ~60 FPS
  time += deltaTime;
  
  // Update simulation
  update(deltaTime);
  
  // Render
  renderer.render(scene, camera);
};
animate();
```

**Memory Management:**
```typescript
// Proper disposal
geometry.dispose();
material.dispose();
renderer.dispose();

// Remove from scene
scene.remove(mesh);
```

---

#### **@react-three/fiber 8.15.0** (React Three.js Integration)
**Purpose:** Declarative Three.js in React (used for 3D components, not simulations)  
**Usage:** For `FlowerOfLife`, `NodeRoom`, `Scene3D` components

**Key APIs:**
```typescript
import { Canvas, useFrame, useThree } from '@react-three/fiber';

// Canvas wrapper
<Canvas gl={{ antialias: true, alpha: true }} dpr={[1, 2]}>
  <mesh>
    <torusGeometry args={[1, 0.02, 16, 64]} />
    <meshStandardMaterial color={0x4299e1} />
  </mesh>
</Canvas>

// useFrame hook (animation)
useFrame((state, delta) => {
  meshRef.current.rotation.y += delta * 0.5;
});

// useThree hook (access Three.js objects)
const { camera, gl } = useThree();
```

**Note:** Simulations use direct Three.js API, not React Three Fiber, for performance and control.

---

#### **@react-three/drei 9.88.0** (Three.js Helpers)
**Purpose:** Useful helpers for React Three Fiber  
**Usage:** `OrbitControls`, `PerspectiveCamera`, `Environment`, `Text`, `Line`

**Key Components:**
```typescript
import { OrbitControls, PerspectiveCamera, Environment, Text, Line } from '@react-three/drei';

// Camera controls
<OrbitControls
  target={[0, 0, 0]}
  minDistance={1}
  maxDistance={10}
  enablePan={true}
  enableZoom={true}
  enableRotate={true}
/>

// 3D Text
<Text
  position={[0, 1.5, 0]}
  fontSize={0.2}
  color="#d69e2e"
  anchorX="center"
  anchorY="middle"
>
  Node Title
</Text>

// Line between points
<Line
  points={[[0, 0, 0], [5, 5, 5]]}
  color="#4299e1"
  lineWidth={2}
/>
```

---

### 1.3 Animation & Interaction

#### **GSAP 3.12.0** (Animation Library)
**Purpose:** High-performance animations for UI and 3D objects  
**Usage Pattern:** Animating material properties, scales, rotations

**Key GSAP APIs:**
```typescript
import { gsap } from 'gsap';

// Animate Three.js object properties
gsap.to(mesh.scale, {
  x: 1.25,
  y: 1.25,
  z: 1.25,
  duration: 0.6,
  ease: 'power2.out'
});

// Animate material properties
gsap.to(material, {
  emissiveIntensity: 2.0,
  opacity: 1,
  duration: 0.5,
  ease: 'power2.out'
});

// Color interpolation
const goldColor = new THREE.Color(0xd69e2e);
gsap.to(material, {
  emissive: goldColor,
  duration: 0.6
});

// Easing functions used:
// - 'power2.out' - Smooth deceleration
// - 'back.out(1.7)' - Bounce effect
// - 'elastic.out' - Elastic bounce
```

**Animation Patterns:**
- **Hover Effects:** Scale + emissive intensity
- **Selection:** Gold color transition + scale
- **Entry Animations:** Scale from 0 with bounce
- **Phase Transitions:** Smooth opacity/color changes

---

### 1.4 State Management

#### **Zustand 4.4.0** (State Management)
**Purpose:** Lightweight state management for navigation and UI state  
**Usage:** `src/store/navigationStore.ts`

**Store Pattern:**
```typescript
import { create } from 'zustand';

interface NavigationStore {
  currentPath: PathType;
  currentState: NavigationState;
  currentNode: string | null;
  selectPath: (path: PathType) => void;
  navigateToNode: (nodeId: string) => void;
  returnToLanding: () => void;
}

export const useNavigationStore = create<NavigationStore>((set) => ({
  currentPath: null,
  currentState: 'landing',
  currentNode: null,
  
  selectPath: (path) => set({ 
    currentPath: path,
    currentState: 'path' 
  }),
  
  navigateToNode: (nodeId) => set({ 
    currentNode: nodeId,
    currentState: 'node' 
  }),
  
  returnToLanding: () => set({ 
    currentPath: null,
    currentState: 'landing',
    currentNode: null
  }),
}));
```

**Usage in Components:**
```typescript
const { currentNode, navigateToNode } = useNavigationStore();
```

---

### 1.5 Mathematical Rendering

#### **KaTeX 0.16.9** (LaTeX Renderer)
**Purpose:** Render mathematical formulas in LaTeX syntax  
**Integration:** Via `react-katex` v3.0.1 wrapper

**Usage Pattern:**
```typescript
import katex from 'katex';
import 'katex/dist/katex.min.css';

// Render formula
const html = katex.renderToString('v(r) = \\frac{c}{k} \\sqrt{\\frac{R}{r}}', {
  displayMode: true,
  throwOnError: false,
  errorColor: '#cc0000'
});

// React component wrapper
<div dangerouslySetInnerHTML={{ __html: html }} />
```

**Formula Components:**
- `FormulaRenderer` - Basic LaTeX rendering
- `AnimatedFormula` - Sequential term reveal
- `MasterEquation` - SDT master equation component
- `KLawFormula` - Universal k-law component

**Common Formulas:**
```latex
% Master Equation
\nabla \cdot [K_{bulk} \nabla \Delta(x)] = -\kappa \rho_{disp}(x) (1 - E(x,\hat{n}))

% k-Law
v(r) = \frac{c}{k} \sqrt{\frac{R}{r}}

% Pressure field
P(r) = P_{\infty} - \kappa \cdot \rho_{disp}(r)

% Coulomb force
F_C = \frac{\pi}{4} P_{CMB} \frac{R_N^2 R_e^2}{r^2}
```

---

### 1.6 Build Tools

#### **Rollup 4.54.0** (Module Bundler)
**Purpose:** Bundles JavaScript modules (used by Astro/Vite)  
**Native Module:** `@rollup/rollup-win32-x64-msvc` v4.54.0 (Windows-specific)

**Configuration:** Handled by Astro/Vite automatically  
**Note:** Windows requires explicit native module installation due to npm optional dependency bug

---

#### **Vite** (Build Tool - Astro Internal)
**Purpose:** Fast dev server and build tool (Astro uses Vite internally)  
**Configuration:** Via `astro.config.mjs` → `vite` section

**Key Features:**
- **HMR:** Hot Module Replacement in dev mode
- **Path Aliases:** Configured in `vite.resolve.alias`
- **Optimization:** Automatic code splitting, tree shaking

---

### 1.7 Development Tools

#### **Node.js** (Runtime)
**Version:** Compatible with Astro 4.0.0 (Node 18+)  
**Package Manager:** npm (comes with Node.js)

**Scripts:**
```json
{
  "scripts": {
    "dev": "astro dev",        // Development server
    "build": "astro build",    // Production build
    "preview": "astro preview", // Preview production build
    "start": "astro dev"       // Alias for dev
  }
}
```

---

## PART II: LIBRARY SPECIFICATIONS & USAGE

### 2.1 Styling Libraries

#### **Tailwind CSS 3.4.0** (Utility-First CSS)
**Purpose:** Rapid UI development with utility classes  
**Integration:** `@astrojs/tailwind` v5.0.0

**Configuration:** `tailwind.config.mjs`

**Custom Theme Extensions:**
```javascript
theme: {
  extend: {
    colors: {
      'sdt-primary': { /* Blue scale 50-950 */ },
      'sdt-gold': { /* Gold scale 50-900 */ },
      'sdt-dark': '#0f172a',
      'sdt-light': '#f8fafc',
    },
    fontFamily: {
      'display': ['Inter', 'system-ui', 'sans-serif'],
      'body': ['Source Serif Pro', 'Georgia', 'serif'],
      'mono': ['JetBrains Mono', 'Fira Code', 'monospace'],
    }
  }
}
```

**Usage Patterns:**
```tsx
// Background colors
className="bg-slate-900"           // Dark background
className="bg-black/70"            // Black with 70% opacity
className="bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900"

// Text colors
className="text-white"              // White text
className="text-amber-400"          // Gold accent
className="text-slate-300"         // Muted text

// Spacing
className="p-4"                     // Padding 1rem
className="mb-6"                    // Margin bottom 1.5rem
className="space-y-4"               // Vertical spacing between children

// Layout
className="flex items-center justify-between"
className="grid grid-cols-1 md:grid-cols-2 gap-8"
className="absolute top-4 left-4"

// Effects
className="backdrop-blur-sm"        // Glassmorphism
className="rounded-lg"              // Border radius
className="transition-colors"       // Smooth color transitions
className="hover:bg-blue-700"      // Hover state
```

**Responsive Breakpoints:**
- `sm:` 640px
- `md:` 768px
- `lg:` 1024px
- `xl:` 1280px
- `2xl:` 1536px

**Custom Utilities:**
```css
/* Defined in global.css */
.focus-ring {
  @apply focus-visible:outline-none focus-visible:ring-2 
         focus-visible:ring-sdt-gold-500 focus-visible:ring-offset-2 
         focus-visible:ring-offset-slate-900;
}

.btn-focus {
  @apply focus-visible:outline-none focus-visible:ring-2 
         focus-visible:ring-sdt-gold-500 focus-visible:ring-offset-2 
         focus-visible:ring-offset-slate-900;
}
```

---

#### **CSS Custom Properties (Design Tokens)**
**Location:** `src/styles/design-tokens.css`

**Color System:**
```css
/* Spation Medium Colors */
--color-space-deep: #1a365d;      /* Deep Space Blue */
--color-space-medium: #2d5a87;   /* Medium Blue */
--color-space-light: #4299e1;    /* Light Blue */

/* Pressure Gradient Colors */
--color-gold-primary: #d69e2e;    /* Metallic Gold */
--color-gold-bright: #f6ad55;     /* Bright Gold */
--color-gold-light: #fbbf24;     /* Light Gold */

/* Matter Colors */
--color-silver: #cbd5e0;          /* Subtle Silver */
--color-eclipse: #0f172a;        /* Matter Exclusion */
```

**Spacing System (8px base unit):**
```css
--space-xs: 0.5rem;    /* 8px */
--space-sm: 1rem;      /* 16px */
--space-md: 2rem;      /* 32px */
--space-lg: 4rem;      /* 64px */
--space-xl: 8rem;      /* 128px */
```

**Typography Scale:**
```css
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1.125rem; /* 18px */
--font-size-lg: 1.5rem;     /* 24px */
--font-size-xl: 1.875rem;   /* 30px */
--font-size-2xl: 2.5rem;    /* 40px */
--font-size-3xl: 3.5rem;     /* 56px */
```

**Timing Functions:**
```css
--timing-fast: 150ms;
--timing-medium: 300ms;
--timing-slow: 1000ms;
--ease-organic: cubic-bezier(0.34, 1.56, 0.64, 1); /* Bouncy */
```

**Usage:**
```css
.element {
  color: var(--color-gold-primary);
  padding: var(--space-md);
  transition-duration: var(--timing-medium);
  transition-timing-function: var(--ease-organic);
}
```

---

### 2.2 Framework Utilities

#### **Custom Geometry System**
**Location:** `src/framework/geometry/GeometryGenerator.ts`

**Purpose:** Generate custom geometries without Three.js primitive dependencies

**Interface:**
```typescript
export interface Geometry {
  vertices: Float32Array;
  normals: Float32Array;
  uvs: Float32Array;
  indices: Uint16Array;
  vertexCount: number;
  faceCount: number;
}

export interface GeometryGenerator {
  generate(params: GeometryParams): Geometry;
  update(geometry: Geometry, params: GeometryParams): void;
  dispose(geometry: Geometry): void;
}
```

**Registry Pattern:**
```typescript
import { geometryRegistry } from '@framework';

// Generate toroidal chamber
const geometry = geometryRegistry.generate('toroidal-chamber', {
  innerRadius: 0.3,
  outerRadius: 1.0,
  height: 1.0,
  radialSegments: 24,
  tubularSegments: 32,
});

// Convert to Three.js BufferGeometry
const threeGeometry = geometryToThreeJS(geometry);
```

**Available Generators:**
- `toroidal-chamber` - Donut-shaped chamber geometry

---

#### **Shader System**
**Location:** `src/framework/shader/ShaderRegistry.ts`

**Purpose:** Manage custom GLSL shaders

**Interface:**
```typescript
export interface IShader {
  vertexShader: string;
  fragmentShader: string;
  uniforms?: Record<string, { value: any }>;
}

export class ShaderRegistry {
  register(name: string, shader: IShader): void;
  get(name: string): THREE.ShaderMaterial;
  compile(name: string): THREE.ShaderMaterial;
}
```

**Usage:**
```typescript
import { shaderRegistry } from '@framework';

// Register custom shader
shaderRegistry.register('pressure-field', {
  vertexShader: `...`,
  fragmentShader: `...`,
  uniforms: {
    time: { value: 0 },
    pressure: { value: 1.0 }
  }
});

// Use in material
const material = shaderRegistry.get('pressure-field');
```

---

#### **Animation Choreographer**
**Location:** `src/framework/animation/AnimationChoreographer.ts`

**Purpose:** Orchestrate complex animation sequences

**Interface:**
```typescript
export interface IAnimationSequence {
  duration: number;
  easing: string;
  stagger?: number;
  animations: Array<{
    target: any;
    properties: Record<string, any>;
  }>;
}

export class AnimationChoreographer {
  addSequence(sequence: IAnimationSequence): void;
  play(): Promise<void>;
  pause(): void;
  resume(): void;
  stop(): void;
}
```

**Usage:**
```typescript
const choreographer = new AnimationChoreographer();

choreographer.addSequence({
  duration: 2000,
  easing: 'power2.out',
  stagger: 100,
  animations: [
    { target: mesh1.scale, properties: { x: 1.5, y: 1.5, z: 1.5 } },
    { target: mesh2.scale, properties: { x: 1.5, y: 1.5, z: 1.5 } },
  ]
});

await choreographer.play();
```

---

#### **Performance Monitor**
**Location:** `src/framework/performance/PerformanceMonitor.ts`

**Purpose:** Track FPS, frame times, memory usage

**Interface:**
```typescript
export class PerformanceMonitor {
  start(): void;
  stop(): void;
  getFPS(): number;
  getFrameTime(): number;
  getMemoryUsage(): number;
  onFrame(callback: (fps: number) => void): void;
}
```

**Usage:**
```typescript
const monitor = new PerformanceMonitor();
monitor.start();

monitor.onFrame((fps) => {
  if (fps < 30) {
    // Reduce quality
  }
});
```

---

## PART III: STYLING SYSTEM DEEP DIVE

### 3.1 Design System Philosophy

**TEKNE Principle:** Form is function, function drives form  
**Aesthetic:** Subtle, subdued, visceral. The obviousness of it all.

**Color Semantics:**
- **Deep Blue (#1a365d):** Spation medium, fundamental space
- **Gold (#d69e2e):** Pressure gradient, revelation, understanding
- **Silver (#cbd5e0):** Matter, exclusion zones
- **Eclipse (#0f172a):** Matter exclusion, voids

**Visual Language:**
- **Organic Motion:** Flowing, breathing, pulsing animations
- **Geometric Precision:** Clean lines, mathematical forms
- **Subtle Glows:** Pressure revelation, not flashy effects
- **Depth Through Opacity:** Layered transparency creates depth

---

### 3.2 Component Styling Patterns

#### **Simulation Container:**
```tsx
<div
  ref={containerRef}
  className="w-full h-full min-h-[400px] bg-slate-900 rounded-lg"
  style={{ touchAction: 'none' }} // Prevent default touch behaviors
/>
```

#### **UI Overlay Panels:**
```tsx
<div className="absolute top-4 left-4 bg-black/70 backdrop-blur-sm text-white p-4 rounded-lg text-sm max-w-md">
  {/* Glassmorphism effect */}
</div>
```

#### **Control Buttons:**
```tsx
<button
  onClick={handleAction}
  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded transition-colors btn-focus"
  aria-label="Action description"
>
  Label
</button>
```

#### **Formulas Overlay:**
```tsx
<div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm text-white p-3 rounded-lg text-xs font-mono">
  <div>v(r) = (c/k)√(R/r)</div>
</div>
```

#### **Data Display:**
```tsx
<div className="space-y-2 text-xs">
  <div className="flex justify-between">
    <span className="text-slate-400">Label:</span>
    <span className="font-mono">{value}</span>
  </div>
</div>
```

---

### 3.3 Responsive Design Patterns

**Mobile-First Approach:**
```tsx
// Base (mobile)
className="text-xs p-2"

// Tablet
className="text-xs p-2 sm:text-sm sm:p-3"

// Desktop
className="text-xs p-2 sm:text-sm sm:p-3 md:text-base md:p-4"
```

**Grid Layouts:**
```tsx
// Single column mobile, multi-column desktop
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
```

**Touch Targets:**
```tsx
// Minimum 44×44px for touch
className="px-3 py-2 sm:px-4 sm:py-2" // Ensures adequate size
```

---

### 3.4 Animation Styling

**GSAP Integration with CSS:**
```typescript
// GSAP animates Three.js objects
gsap.to(mesh.scale, { x: 1.25, duration: 0.6, ease: 'power2.out' });

// CSS handles UI transitions
className="transition-colors duration-200" // Tailwind
// OR
style={{ transition: 'color 200ms var(--ease-organic)' }} // CSS vars
```

**Reduced Motion Support:**
```css
@media (prefers-reduced-motion: reduce) {
  :root {
    --timing-fast: 0ms;
    --timing-medium: 0ms;
    --timing-slow: 0ms;
  }
}
```

---

## PART IV: ARCHITECTURE & FILE STRUCTURE

### 4.1 Project Structure

```
SDT/website/
├── src/
│   ├── components/
│   │   ├── 3d/                    # 3D scene components (React Three Fiber)
│   │   │   ├── Scene3D.tsx
│   │   │   ├── FlowerOfLife.tsx
│   │   │   ├── CameraController.tsx
│   │   │   └── SpatialPath.tsx
│   │   ├── simulations/           # Simulation components (Direct Three.js)
│   │   │   ├── SimulationBase.tsx
│   │   │   ├── PressureFieldSim.tsx
│   │   │   ├── OrbitalSim.tsx
│   │   │   ├── AtomicStructureSim.tsx
│   │   │   ├── GalaxyRotationSim.tsx
│   │   │   ├── BenchmarkVisualizer.tsx
│   │   │   ├── TheClearingSim.tsx
│   │   │   ├── FormulaRenderer.tsx
│   │   │   └── index.ts
│   │   ├── walkthrough/           # Walkthrough-specific components
│   │   │   ├── WalkthroughApp.tsx
│   │   │   ├── NodeRoom.tsx
│   │   │   ├── PathView.tsx
│   │   │   ├── SimulationViewer.tsx
│   │   │   └── ...
│   │   └── ui/                    # Reusable UI components
│   │       ├── LoadingSpinner.tsx
│   │       ├── ErrorBoundary.tsx
│   │       └── ...
│   ├── framework/                 # Custom framework utilities
│   │   ├── geometry/
│   │   ├── shader/
│   │   ├── animation/
│   │   └── performance/
│   ├── layouts/                   # Astro layouts
│   │   └── BaseLayout.astro
│   ├── pages/                     # Astro pages (routes)
│   │   ├── index.astro
│   │   ├── walkthrough/
│   │   ├── simulations/
│   │   └── ...
│   ├── store/                     # Zustand stores
│   │   └── navigationStore.ts
│   ├── styles/                    # Global styles
│   │   ├── global.css
│   │   ├── design-tokens.css
│   │   └── animations.css
│   ├── types/                     # TypeScript types
│   │   └── content.ts
│   ├── utils/                     # Utility functions
│   │   ├── content-loader.ts
│   │   └── narration.ts
│   └── content/                   # Content JSON files
│       └── path1/
├── public/                        # Static assets
│   └── content/                   # Served content JSON
├── astro.config.mjs
├── tailwind.config.mjs
├── package.json
└── tsconfig.json
```

---

### 4.2 Component Architecture

#### **Simulation Component Pattern:**

**Base Class (SimulationBase.tsx):**
```typescript
export abstract class SimulationBase {
  protected scene: THREE.Scene;
  protected camera: THREE.PerspectiveCamera;
  protected renderer: THREE.WebGLRenderer;
  protected container: HTMLElement;
  protected animationId: number | null = null;
  protected isPlaying: boolean = false;
  protected time: number = 0;
  protected parameters: Record<string, number> = {};

  constructor(container: HTMLElement) {
    // Initialize Three.js scene, camera, renderer
  }

  abstract init(): void;
  abstract update(deltaTime: number): void;
  abstract dispose(): void;

  play(): void { /* Start animation loop */ }
  pause(): void { /* Stop animation loop */ }
  reset(): void { /* Reset to initial state */ }
  destroy(): void { /* Cleanup everything */ }
}
```

**Concrete Simulation Class:**
```typescript
class PressureFieldSimulation extends SimulationBase {
  private matterSphere: THREE.Mesh | null = null;
  private fieldPoints: THREE.Points | null = null;

  init(): void {
    // Create 3D objects
    this.createMatterSphere();
    this.createPressureField();
  }

  update(deltaTime: number): void {
    // Update animation state
    this.scene.rotation.y += deltaTime * 0.2;
  }

  dispose(): void {
    // Cleanup geometries and materials
    if (this.matterSphere) {
      this.matterSphere.geometry.dispose();
      this.matterSphere.material.dispose();
    }
  }
}
```

**React Wrapper Component:**
```typescript
export const PressureFieldSim: React.FC<PressureFieldSimProps> = ({
  id,
  parameters,
  showFormulas = true,
  showLabels = true,
  onReady,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const simulationRef = useRef<PressureFieldSimulation | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const sim = new PressureFieldSimulation(containerRef.current);
    sim.setParameters(parameters);
    sim.init();
    simulationRef.current = sim;
    sim.play();

    if (onReady) setTimeout(onReady, 100);

    return () => {
      sim.destroy();
      simulationRef.current = null;
    };
  }, []);

  useEffect(() => {
    if (simulationRef.current) {
      simulationRef.current.setParameters(parameters);
    }
  }, [parameters]);

  return (
    <div className="relative w-full h-full">
      <div ref={containerRef} className="w-full h-full min-h-[400px] bg-slate-900 rounded-lg" />
      {showLabels && <LabelsPanel parameters={parameters} />}
      {showFormulas && <FormulaOverlay />}
    </div>
  );
};
```

---

### 4.3 Import Patterns

**Path Aliases (from astro.config.mjs):**
```typescript
// Instead of:
import { SimulationBase } from '../../../components/simulations/SimulationBase';

// Use:
import { SimulationBase } from '@components/simulations/SimulationBase';
// OR
import { SimulationBase } from '@/components/simulations/SimulationBase';
```

**Available Aliases:**
- `@` → `./src`
- `@components` → `./src/components`
- `@layouts` → `./src/layouts`
- `@store` → `./src/store`
- `@utils` → `./src/utils`
- `@types` → `./src/types`

**Framework Imports:**
```typescript
import { geometryRegistry, shaderRegistry } from '@framework';
```

**Simulation Imports:**
```typescript
import { 
  PressureFieldSim,
  OrbitalSim,
  AtomicStructureSim,
  TheClearingSim
} from '@components/simulations';
```

---

## PART V: CODE PATTERNS & CONVENTIONS

### 5.1 TypeScript Patterns

#### **Interface Definitions:**
```typescript
// Props interfaces extend base SimulationProps
interface PressureFieldSimProps extends SimulationProps {
  parameters: {
    density?: number;
    bulkModulus?: number;
    matterRadius?: number;
    fieldResolution?: number;
  };
}

// Use optional properties with defaults
parameters: {
  density?: number; // Optional, has default in implementation
}
```

#### **Type Guards:**
```typescript
// Always check refs before use
if (!containerRef.current) return;
if (!simulationRef.current) return;

// Check Three.js object types
if (child instanceof THREE.Mesh) {
  child.geometry.dispose();
}
```

#### **Null Safety:**
```typescript
// Use nullish coalescing for defaults
const density = parameters.density ?? 5.2e96;

// Use optional chaining
simulationRef.current?.setParameters(parameters);

// Avoid non-null assertions (!) - use proper checks instead
```

---

### 5.2 React Patterns

#### **Hooks Usage:**
```typescript
// useState for component state
const [isPlaying, setIsPlaying] = useState(false);

// useRef for DOM elements and persistent values
const containerRef = useRef<HTMLDivElement>(null);
const simulationRef = useRef<SimulationClass | null>(null);

// useEffect for side effects
useEffect(() => {
  // Setup
  return () => {
    // Cleanup
  };
}, [dependencies]);

// useMemo for expensive calculations
const geometry = useMemo(() => {
  return new THREE.SphereGeometry(radius, 32, 32);
}, [radius]);
```

#### **Effect Dependencies:**
```typescript
// Empty array = run once on mount
useEffect(() => {
  // Initialization
}, []);

// With dependencies = run when dependencies change
useEffect(() => {
  // Update when parameters change
}, [parameters]);

// No array = run on every render (avoid unless necessary)
```

---

### 5.3 Three.js Patterns

#### **Object Creation:**
```typescript
// Geometry
const geometry = new THREE.SphereGeometry(radius, widthSegments, heightSegments);

// Material
const material = new THREE.MeshStandardMaterial({
  color: 0x1a365d,
  metalness: 0.8,
  roughness: 0.2
});

// Mesh
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);
```

#### **BufferGeometry for Particles:**
```typescript
const positions = new Float32Array(particleCount * 3);
const colors = new Float32Array(particleCount * 3);

// Fill arrays
for (let i = 0; i < particleCount; i++) {
  positions[i * 3] = x;
  positions[i * 3 + 1] = y;
  positions[i * 3 + 2] = z;
  
  colors[i * 3] = r;
  colors[i * 3 + 1] = g;
  colors[i * 3 + 2] = b;
}

// Create geometry
const geometry = new THREE.BufferGeometry();
geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

// Create points
const material = new THREE.PointsMaterial({ vertexColors: true });
const points = new THREE.Points(geometry, material);
scene.add(points);
```

#### **Animation Updates:**
```typescript
// Update buffer attributes
const positions = points.geometry.attributes.position.array as Float32Array;
for (let i = 0; i < positions.length; i += 3) {
  positions[i] += deltaX;
  positions[i + 1] += deltaY;
  positions[i + 2] += deltaZ;
}
points.geometry.attributes.position.needsUpdate = true;
```

#### **Memory Management:**
```typescript
// Dispose pattern
if (geometry) geometry.dispose();
if (material) {
  if (Array.isArray(material)) {
    material.forEach(m => m.dispose());
  } else {
    material.dispose();
  }
}

// Remove from scene
scene.remove(mesh);
```

---

### 5.4 Error Handling Patterns

#### **Error Boundaries:**
```typescript
import { ErrorBoundary } from '@framework';

<ErrorBoundary fallback={<ErrorDisplay />}>
  <SimulationComponent />
</ErrorBoundary>
```

#### **Try-Catch in Initialization:**
```typescript
useEffect(() => {
  try {
    const sim = new SimulationClass(containerRef.current!);
    sim.init();
  } catch (error) {
    console.error('Simulation initialization failed:', error);
    // Show error UI
  }
}, []);
```

#### **Graceful Degradation:**
```typescript
// Check WebGL support
if (!renderer.getContext()) {
  // Show fallback message
  return <WebGLNotSupported />;
}
```

---

## PART VI: SIMULATION IMPLEMENTATION SPECIFICATIONS

### 6.1 Missing Simulations (Priority 1)

#### **SpationLatticeSim.tsx** (MISSING - HIGH PRIORITY)

**File:** `src/components/simulations/SpationLatticeSim.tsx`

**Purpose:** Visualize fundamental spation lattice at Planck scale

**SDT Physics:**
- Spation density: ρ_spation = 5.2×10⁹⁶ kg/m³
- Bulk modulus: K_bulk = 4.6×10¹¹³ Pa
- Lattice spacing: a₀ ≈ 10⁻³⁵ m (Planck scale)
- Dodecahedral packing geometry

**Required Features:**
1. **Dodecahedral Unit Cell Generation:**
   - Generate dodecahedron vertices (20 vertices, 12 faces)
   - Pack multiple unit cells in 3D space
   - Show packing structure

2. **Scale Navigation:**
   - Zoom from 1 m to 10⁻³⁵ m (35 orders of magnitude)
   - Logarithmic scale transitions
   - LOD system (reduce detail at extreme scales)

3. **Pressure Visualization:**
   - Color-code lattice points by pressure
   - Show K_bulk emergence from geometry
   - Visualize deformation under load

4. **Interactive Controls:**
   - Rotate lattice
   - Select lattice points (show pressure value)
   - Deform lattice interactively
   - Toggle unit cell boundaries

**Parameters:**
```typescript
interface SpationLatticeSimProps extends SimulationProps {
  parameters: {
    scale?: number;              // Current scale (log10 meters), default: -35
    showPressure?: boolean;      // Show pressure color coding
    showDeformation?: boolean;   // Show deformation vectors
    latticeResolution?: number;  // Unit cells per dimension, default: 5
    zoomLevel?: number;          // 0-35 (orders of magnitude)
    showUnitCells?: boolean;     // Show cell boundaries
  };
}
```

**Implementation Steps:**
1. Create `DodecahedronGenerator` in `@framework/geometry`
2. Generate dodecahedral packing structure
3. Create lattice visualization (wireframe + points)
4. Implement scale navigation (logarithmic zoom)
5. Add pressure calculation and color coding
6. Add interactive controls
7. Implement LOD system for performance

**Visualization:**
- Dodecahedral wireframe (gold lines, subtle)
- Lattice points (colored by pressure: blue → gold)
- Unit cell boundaries (optional, translucent)
- Scale indicator (showing current log10 scale)
- Pressure value display (on point selection)

**Performance Considerations:**
- Use instanced rendering for repeated unit cells
- LOD: Reduce cell count at extreme scales
- Frustum culling for off-screen cells
- Web Worker for pressure calculations (if needed)

---

#### **ForceHierarchySim.tsx** (MISSING - HIGH PRIORITY)

**File:** `src/components/simulations/ForceHierarchySim.tsx`

**Purpose:** Visualize force unification via occlusion regimes

**SDT Physics:**
- Coulomb: F_C = (π/4)P_CMB (R_N²R_e²/r²) when E→0
- Gravity: F_G = (π/4)P_CMB (R₁²R₂²/r²)(1-η) when E→1-η
- Same pressure source (CMB), different occlusion

**Required Features:**
1. **Two-Body System:**
   - Two objects with exclusion zones
   - Pressure field visualization between them
   - Force vector arrows

2. **Occlusion Control:**
   - Slider: E from 0 to 1-η
   - Show transition between force regimes
   - Real-time force calculation

3. **Force Comparison:**
   - Side-by-side visualization
   - Log scale comparison
   - Same CMB pressure source

4. **CMB Source Visualization:**
   - Distant CMB boundary sphere
   - Pressure propagation arrows
   - Force generation mechanism

**Parameters:**
```typescript
interface ForceHierarchySimProps extends SimulationProps {
  parameters: {
    object1Radius?: number;      // R₁ in meters
    object2Radius?: number;      // R₂ in meters
    separation?: number;         // r in meters
    occlusionE?: number;         // E (0 to 1-η), default: 0.5
    showCMBSource?: boolean;     // Show CMB boundary
    compareForces?: boolean;      // Show both forces side-by-side
    showPressureField?: boolean; // Show pressure field visualization
  };
}
```

**Implementation:**
- Use `PressureFieldSim` as base
- Add two objects instead of one
- Calculate forces based on occlusion parameter
- Visualize force vectors (arrow helpers)
- Show CMB boundary (distant sphere)

---

#### **ChemicalBondingSim.tsx** (MISSING - HIGH PRIORITY)

**File:** `src/components/simulations/ChemicalBondingSim.tsx`

**Purpose:** Visualize bonding as pressure field overlap

**SDT Physics:**
- Bonds form when pressure fields overlap
- Bond strength from pressure gradient
- Nuclear structure determines chemistry

**Required Features:**
1. **Multi-Atom System:**
   - Place multiple atoms (drag-and-drop)
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

**Parameters:**
```typescript
interface ChemicalBondingSimProps extends SimulationProps {
  parameters: {
    atoms?: Array<{
      element: string;           // Element symbol
      position: [number, number, number];
    }>;
    showPressureFields?: boolean;
    showBonds?: boolean;
    showEnergy?: boolean;
    showGeometry?: boolean;
  };
}
```

**Implementation:**
- Extend `PressureFieldSim` for multi-object support
- Add atom placement UI
- Calculate overlap regions
- Visualize bonds (cylinders between atoms)
- Display bond energy

---

### 6.2 Upgrade Specifications

#### **PressureFieldSim.tsx → PressureFieldSimAdvanced.tsx**

**Upgrades Required:**

1. **Master Equation Solver:**
   ```typescript
   // Implement: ∇·[K_bulk ∇Δ(x)] = -κρ_disp(x)(1-E(x,ñ))
   
   // Use finite difference method or finite element method
   // Solve on 3D grid
   // Update pressure field visualization
   ```

2. **Directional Occlusion E(x,ñ):**
   ```typescript
   // Calculate occlusion in direction ñ
   // Visualize occlusion as transparency/color
   // Show how occlusion affects pressure
   ```

3. **Pressure Gradient Vectors:**
   ```typescript
   // Calculate ∇P at each point
   // Draw arrows showing gradient direction
   // Arrow length = gradient magnitude
   // Color = pressure value
   ```

4. **Multiple Matter Objects:**
   ```typescript
   // Support array of matter objects
   // Each with position, radius, mass
   // Calculate combined pressure field
   // Show interactions between objects
   ```

5. **CMB Integration:**
   ```typescript
   // Add CMB boundary sphere (distant)
   // Show pressure originating from CMB
   // Visualize pressure propagation
   ```

**Implementation Approach:**
- Create new `PressureFieldSimAdvanced.tsx`
- Keep `PressureFieldSim.tsx` as simple version
- Use Web Worker for heavy calculations
- Implement adaptive grid refinement

---

#### **AtomicStructureSim.tsx → AtomicStructureSimAdvanced.tsx**

**Upgrades Required:**

1. **Proper Helical Quantization:**
   ```typescript
   // SDT wave function: ψ(r,θ,φ) = R(r)Y(θ,φ)e^(imφ)
   // With toroidal topology
   // Quantization conditions from helical standing waves
   ```

2. **Multi-Electron Atoms:**
   ```typescript
   // Support He, Li, Be, etc.
   // Show electron-electron interactions
   // Pressure field overlap
   ```

3. **Orbital Shapes:**
   ```typescript
   // s, p, d, f orbitals
   // Visualize probability density
   // Show angular momentum
   ```

4. **Energy Levels:**
   ```typescript
   // Calculate from helical quantization
   // Display energy level diagram
   // Show transitions
   ```

---

## PART VII: INTEGRATION PATTERNS

### 7.1 SimulationViewer Expansion

**Current State:** Only supports `'pressure-field'`

**Required Expansion:**
```typescript
// src/components/walkthrough/SimulationViewer.tsx

const renderSimulation = () => {
  switch (simulationId) {
    case 'pressure-field':
      return <PressureFieldSim {...props} />;
    
    case 'orbital-mechanics':
      return <OrbitalSim {...props} />;
    
    case 'atomic-structure':
      return <AtomicStructureSim {...props} />;
    
    case 'galaxy-rotation':
      return <GalaxyRotationSim {...props} />;
    
    case 'the-clearing':
    case 'let-there-be-light':
      return <TheClearingSim {...props} />;
    
    case 'spation-lattice':
      return <SpationLatticeSim {...props} />;
    
    case 'force-hierarchy':
      return <ForceHierarchySim {...props} />;
    
    case 'chemical-bonding':
      return <ChemicalBondingSim {...props} />;
    
    case 'cmb-boundary':
    case 'let-there-be-light':
      return <CMBBoundarySim {...props} />; // ✅ COMPLETE - LET THERE BE LIGHT!
    
    case 'benchmark-visualizer':
      return <BenchmarkVisualizer {...props} />;
    
    default:
      return <SimulationNotFound id={simulationId} />;
  }
};
```

**Parameter Mapping:**
```typescript
// Map from content JSON to simulation parameters
const mapParameters = (simulationConfig: any) => {
  return {
    ...simulationConfig.parameters,
    showFormulas: simulationConfig.showFormulas ?? true,
    showLabels: simulationConfig.showLabels ?? true,
  };
};
```

---

### 7.2 Content JSON Integration

**Content Structure:**
```json
{
  "expansions": {
    "simulation": {
      "id": "pressure-field",
      "parameters": {
        "density": 5.2e96,
        "bulkModulus": 4.6e113,
        "matterRadius": 1.0
      },
      "showFormulas": true,
      "showLabels": true
    }
  }
}
```

**Loading Pattern:**
```typescript
// In NodeDetailView.tsx
const simulationConfig = content.expansions?.simulation;

{simulationConfig && (
  <SimulationViewer
    simulationId={simulationConfig.id}
    parameters={simulationConfig.parameters}
    showFormulas={simulationConfig.showFormulas}
    showLabels={simulationConfig.showLabels}
  />
)}
```

---

### 7.3 Walkthrough Integration

**Scale Point Simulations:**
```typescript
// In WalkthroughApp.tsx
const getSimulationForScale = (scale: ScalePoint) => {
  switch (scale.domain) {
    case 'planck':
      return 'spation-lattice';
    case 'atomic':
      return 'atomic-structure';
    case 'molecular':
      return 'chemical-bonding';
    case 'macroscopic':
      return 'force-hierarchy';
    case 'stellar':
      return 'orbital-mechanics';
    case 'galactic':
      return 'galaxy-rotation';
    case 'cosmological':
      return 'cmb-boundary'; // ✅ Already exists
    default:
      return null;
  }
};
```

---

## PART VIII: PERFORMANCE OPTIMIZATION

### 8.1 Frame Rate Targets

**Desktop:** 60 FPS  
**Mobile:** 30 FPS  
**Tablet:** 45 FPS

**Monitoring:**
```typescript
import { PerformanceMonitor } from '@framework/performance';

const monitor = new PerformanceMonitor();
monitor.start();

monitor.onFrame((fps) => {
  if (fps < targetFPS) {
    // Reduce quality
    reduceQuality();
  }
});
```

---

### 8.2 LOD System

**Implementation:**
```typescript
const getLODLevel = (): 'low' | 'medium' | 'high' => {
  const fps = monitor.getFPS();
  const isMobile = window.innerWidth < 768;
  
  if (isMobile || fps < 30) return 'low';
  if (fps < 45) return 'medium';
  return 'high';
};

const particleCount = {
  low: 500,
  medium: 1000,
  high: 2000
}[getLODLevel()];
```

---

### 8.3 Viewport Culling

**Implementation:**
```typescript
const isInViewport = (object: THREE.Object3D, camera: THREE.Camera): boolean => {
  const frustum = new THREE.Frustum();
  const matrix = new THREE.Matrix4().multiplyMatrices(
    camera.projectionMatrix,
    camera.matrixWorldInverse
  );
  frustum.setFromProjectionMatrix(matrix);
  return frustum.containsPoint(object.position);
};

// In update loop
if (!isInViewport(mesh, camera)) {
  mesh.visible = false;
  return; // Skip update
}
mesh.visible = true;
```

---

### 8.4 Web Workers

**For Heavy Calculations:**
```typescript
// worker.ts
self.onmessage = (e) => {
  const { data } = e;
  // Perform calculation
  const result = calculatePressureField(data);
  self.postMessage(result);
};

// In simulation
const worker = new Worker(new URL('./worker.ts', import.meta.url));
worker.postMessage({ gridSize, matterObjects });
worker.onmessage = (e) => {
  updatePressureField(e.data);
};
```

---

## PART IX: TESTING & QUALITY ASSURANCE

### 9.1 Unit Tests

**Framework:** Jest + React Testing Library (to be added)

**Test Structure:**
```typescript
describe('PressureFieldSimulation', () => {
  it('initializes correctly', () => {
    const container = document.createElement('div');
    const sim = new PressureFieldSimulation(container);
    sim.init();
    expect(sim.scene).toBeDefined();
  });

  it('updates parameters correctly', () => {
    // Test parameter updates
  });

  it('disposes resources correctly', () => {
    // Test memory cleanup
  });
});
```

---

### 9.2 Integration Tests

**Test SimulationViewer:**
```typescript
describe('SimulationViewer', () => {
  it('renders correct simulation for ID', () => {
    render(<SimulationViewer simulationId="pressure-field" />);
    expect(screen.getByTestId('pressure-field-sim')).toBeInTheDocument();
  });
});
```

---

### 9.3 Performance Tests

**Frame Rate Test:**
```typescript
it('maintains 60 FPS', async () => {
  const container = document.createElement('div');
  const sim = new PressureFieldSimulation(container);
  sim.init();
  sim.play();
  
  await waitFor(() => {
    const fps = monitor.getFPS();
    expect(fps).toBeGreaterThan(55);
  });
});
```

---

## PART X: DEPLOYMENT & BUILD PROCESS

### 10.1 Build Commands

```bash
# Development
npm run dev          # Start dev server (port 3001)

# Production Build
npm run build        # Generate static site in dist/
npm run preview      # Preview production build locally
```

### 10.2 Build Output

**Structure:**
```
dist/
├── index.html
├── walkthrough/
│   └── index.html
├── simulations/
│   ├── the-clearing.html
│   └── ...
├── _astro/
│   └── [hashed assets]
└── content/
    └── [content JSON files]
```

### 10.3 Deployment

**Static Hosting:** Netlify, Vercel, GitHub Pages compatible  
**Site URL:** `https://sdt-theory.org` (configured in astro.config.mjs)

---

## IMPLEMENTATION CHECKLIST

### Priority 1 (Critical)
- [ ] Expand SimulationViewer to support all 8 simulations
- [ ] Implement SpationLatticeSim
- [ ] Implement ForceHierarchySim  
- [ ] Implement ChemicalBondingSim
- [ ] Upgrade PressureFieldSim (Master Equation)
- [ ] Upgrade AtomicStructureSim (proper quantization)
- [ ] Fix scientific accuracy in all simulations
- [ ] Integrate into content nodes
- [ ] Integrate into walkthrough

### Priority 2 (High)
- [ ] Performance monitoring
- [ ] LOD system
- [ ] Mobile optimization
- [ ] Viewport culling
- [ ] Enhanced UI controls

### Priority 3 (Medium)
- [ ] Web Workers for heavy calculations
- [ ] Guided tours
- [ ] Comparison modes
- [ ] Data export

---

## CONCLUSION

This ultraprompt provides exhaustive documentation of:
- Complete toolchain (Astro, React, Three.js, GSAP, etc.)
- Library specifications and usage patterns
- Styling system (Tailwind, CSS vars, design tokens)
- Architecture and file structure
- Code patterns and conventions
- Detailed simulation specifications
- Integration patterns
- Performance optimization
- Testing requirements

**Status:** 
- ✅ CMBBoundarySim (LET THERE BE LIGHT!) - COMPLETE
- ✅ TheClearingSim (Recombination Era) - COMPLETE

**Next Steps:** Implement Priority 1 simulations following these specifications:
1. SpationLatticeSim (fundamental lattice structure)
2. ForceHierarchySim (force unification visualization)
3. ChemicalBondingSim (bonding from pressure fields)
4. Upgrade existing simulations (Master Equation, proper quantization)
5. Expand SimulationViewer integration

---

**End of Ultra Prompt**

