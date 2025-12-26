# API Contracts & Component Interfaces

This document defines the interfaces and contracts between components developed by different "agents" to ensure smooth integration.

## 3D Components (Agent 1)

### FlowerOfLife Component

```typescript
interface FlowerOfLifeProps {
  onPathSelect: (pathId: 'path1' | 'path2' | 'path3') => void;
  isTransitioning?: boolean;
}

// Emits: 'path-selected' event with pathId
```

### Scene3D Component

```typescript
interface Scene3DProps {
  children: React.ReactNode;
  cameraPosition?: [number, number, number];
  cameraTarget?: [number, number, number];
  onCameraReady?: () => void;
}
```

### CameraController

```typescript
interface CameraControllerProps {
  targetPosition: [number, number, number];
  targetLookAt: [number, number, number];
  duration?: number;
  onTransitionComplete?: () => void;
}

// Methods exposed via ref:
// - transitionTo(position, lookAt, duration)
// - reset()
```

### NodeRoom Component

```typescript
interface NodeRoomProps {
  nodeId: string;
  position: [number, number, number];
  content: NodeContent; // From Agent 2
  onEnter?: () => void;
  onExit?: () => void;
}
```

## Content System (Agent 2)

### NodeContent Type

```typescript
interface NodeContent {
  id: string;
  title: string;
  path: 'path1' | 'path2' | 'path3';
  readingTime: number; // minutes
  content: {
    main: string; // Markdown
    expansions?: {
      [key: string]: string; // Expansion content
    };
  };
  narration?: {
    script: string;
    audioFile?: string;
    timing?: number[]; // seconds
  };
  visualizations?: {
    '3dAnimation'?: string; // Animation ID
    formulas?: string[]; // Formula IDs
    charts?: string[]; // Chart IDs
    simulation?: string; // Simulation ID
  };
  position: [number, number, number]; // 3D position
  cameraTarget: [number, number, number];
}
```

### Content Loader

```typescript
// Function signature
function loadNodeContent(nodeId: string): Promise<NodeContent>;
function loadPathContent(pathId: string): Promise<NodeContent[]>;
```

## Simulations (Agent 3)

### Simulation Component Interface

```typescript
interface SimulationProps {
  id: string;
  parameters: Record<string, number>;
  onParameterChange?: (key: string, value: number) => void;
  showFormulas?: boolean;
  showLabels?: boolean;
  narrationEnabled?: boolean;
  onReady?: () => void;
}

interface SimulationState {
  isPlaying: boolean;
  time: number;
  cameraPosition?: [number, number, number];
}
```

### Specific Simulations

#### PressureFieldSim

```typescript
interface PressureFieldSimProps extends SimulationProps {
  parameters: {
    density: number; // Spation density
    bulkModulus: number; // K_bulk
    matterRadius?: number; // Matter exclusion radius
  };
}
```

#### OrbitalSim

```typescript
interface OrbitalSimProps extends SimulationProps {
  parameters: {
    centralMass: number;
    orbitalRadius: number;
    kValue: number; // Scale-dependent k
    scale: 'atomic' | 'planetary' | 'galactic';
  };
}
```

#### AtomicStructureSim

```typescript
interface AtomicStructureSimProps extends SimulationProps {
  parameters: {
    element: string; // Element symbol
    showElectrons: boolean;
    showPressureField: boolean;
  };
}
```

#### GalaxyRotationSim

```typescript
interface GalaxyRotationSimProps extends SimulationProps {
  parameters: {
    galaxyMass: number;
    diskRadius: number;
    showRotationCurve: boolean;
    compareDarkMatter?: boolean;
  };
}
```

### Formula Renderer

```typescript
interface FormulaRendererProps {
  formula: string; // LaTeX string
  displayMode?: 'inline' | 'block';
  animated?: boolean;
  highlightTerms?: string[]; // Term IDs to highlight
}
```

## Integration (Agent 4)

### Navigation Store (Zustand)

```typescript
interface NavigationState {
  currentPath: 'path1' | 'path2' | 'path3' | null;
  currentNode: string | null;
  isTransitioning: boolean;
  cameraPosition: [number, number, number];
  cameraTarget: [number, number, number];
  
  // Actions
  selectPath: (pathId: 'path1' | 'path2' | 'path3') => void;
  navigateToNode: (nodeId: string) => void;
  startTransition: () => void;
  completeTransition: () => void;
  updateCamera: (position: [number, number, number], target: [number, number, number]) => void;
}
```

### Narration System

```typescript
interface NarrationSystem {
  play: (script: string, audioFile?: string) => Promise<void>;
  pause: () => void;
  resume: () => void;
  stop: () => void;
  setSpeed: (speed: number) => void; // 0.5 - 2.0
  setVolume: (volume: number) => void; // 0 - 1
  isPlaying: boolean;
  currentTime: number;
  duration: number;
}
```

### Routing

```typescript
// Astro routes
/path1/[nodeId].astro
/path2/[nodeId].astro
/path3/[nodeId].astro

// React Router (for SPA sections)
<Route path="/path1/:nodeId" element={<NodeView />} />
```

## Event System

### Global Events

Components communicate via custom events:

```typescript
// Path selection
window.dispatchEvent(new CustomEvent('path-selected', { 
  detail: { pathId: 'path1' } 
}));

// Node navigation
window.dispatchEvent(new CustomEvent('node-navigate', { 
  detail: { nodeId: 'path1-node1' } 
}));

// Simulation ready
window.dispatchEvent(new CustomEvent('simulation-ready', { 
  detail: { simulationId: 'pressure-field' } 
}));

// Narration sync
window.dispatchEvent(new CustomEvent('narration-sync', { 
  detail: { time: 5.2, text: '...' } 
}));
```

## Data Flow

```
User Interaction
    ↓
Navigation Store (Agent 4)
    ↓
Camera Controller (Agent 1) + Content Loader (Agent 2)
    ↓
Node Room (Agent 1) renders Content (Agent 2)
    ↓
Simulations (Agent 3) + Narration (Agent 4)
```

## Error Handling

All components should handle errors gracefully:

```typescript
interface ComponentError {
  component: string;
  error: Error;
  timestamp: number;
  context?: Record<string, any>;
}

// Error reporting
function reportError(error: ComponentError): void;
```

## Performance Contracts

- **3D Components**: Must maintain 60 FPS on desktop, 30 FPS on mobile
- **Simulations**: Must initialize in <1 second
- **Content Loading**: Must load in <500ms
- **Narration**: Must start within 100ms of request

## Testing Contracts

Each component should:
- Export its props interface
- Have a default export
- Handle missing props gracefully
- Log errors to console in development
- Be testable in isolation

