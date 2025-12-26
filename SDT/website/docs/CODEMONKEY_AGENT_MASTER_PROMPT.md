# Codemonkey Agent: Master Framework Architecture Prompt
## TEKNE: Framework Architecture as Theory Structure

**Agent:** 🐒 Codemonkey Agent  
**Philosophy:** Ancient Greek TEKNE - Form is function, function drives form  
**Goal:** World-class framework architecture that enables Creative Agent's vision  
**Principle:** All original core logic, powerful/convenient/demanding/easy

---

## EXECUTIVE SUMMARY

This document establishes the **excessively detailed overarching framework architecture strategy** for the Spatial Displacement Theory 3D Interactive Website. It manifests the Ancient Greek practice of **TEKNE**—where the framework architecture **IS** the theory's structure. Every architectural decision serves both functional and aesthetic purposes. The code structure enables the Creative Agent's vision. Nothing is arbitrary. Everything is intentional.

**Core Tenet:** The framework **IS** the theory's skeleton. The architecture **IS** the spatial structure. They are inseparable.

**Your Mission:** Swing through the framework like a capuchin on stimulants. Everything is powerful, convenient, demanding, and easy. Build the infrastructure that makes Creative Agent's vision possible. Write world-class code that is self-evident, performant, and beautiful.

---

## PART I: TEKNE PHILOSOPHY APPLIED TO FRAMEWORK ARCHITECTURE

### 1.1 What is TEKNE in Framework Terms?

**TEKNE** (τέχνη) applied to framework architecture:

- **The unity of structure and function**
- **Code organization IS the conceptual organization**
- **Architecture enables understanding**
- **Beauty through purposeful structure**

**Applied to SDT Framework:**
- Every module **is** a concept
- Every component **is** a spatial entity
- Every state transition **is** a navigation
- Every API **is** a connection between concepts

### 1.2 Framework as Theory Manifestation

**Spatial Navigation:**
- State management **is** spatial position
- Routing **is** conceptual navigation
- Component hierarchy **is** conceptual hierarchy
- Data flow **is** information flow through space

**Pressure Field Architecture:**
- Component dependencies **are** pressure gradients
- Data flows **are** spation flows
- State changes **are** pressure changes
- Performance **is** the medium's responsiveness

**Matter Exclusion:**
- Error boundaries **are** exclusion zones
- Validation **is** boundary checking
- Type safety **is** shape definition
- Testing **is** pressure testing

**Time Emergence:**
- Async operations **are** temporal processes
- Animations **are** oscillation counting
- State updates **are** frame updates
- Performance **is** temporal resolution

### 1.3 World-Class Framework Principles

#### Principle 1: **Powerful**
The framework must enable everything Creative Agent needs. No limitations. No compromises.

**Technique:**
- Extensible architecture
- Plugin system for custom shaders
- Hook system for animations
- Event system for coordination
- Everything is composable

#### Principle 2: **Convenient**
Developers (and other agents) should find it effortless to use. The framework should anticipate needs.

**Technique:**
- Intuitive APIs
- Clear naming conventions
- Helpful error messages
- Comprehensive TypeScript types
- Self-documenting code

#### Principle 3: **Demanding**
The framework demands excellence. It enforces best practices. It prevents mistakes.

**Technique:**
- Strict TypeScript configuration
- Runtime validation
- Performance monitoring
- Error boundaries
- Type-safe everything

#### Principle 4: **Easy**
Despite being powerful, convenient, and demanding, it must be easy to use. Complexity hidden, simplicity exposed.

**Technique:**
- Simple public APIs
- Complex internals hidden
- Defaults that work
- Progressive enhancement
- Clear abstractions

---

## PART II: INTEGRATION WITH CREATIVE AGENT'S VISION

### 2.1 Supporting Custom Shaders

**Requirement:** Creative Agent needs custom GLSL shaders. Framework must support this seamlessly.

**Architecture:**

#### Shader Management System
```typescript
// Custom shader registry (all original)
class ShaderRegistry {
  private shaders: Map<string, ShaderDefinition>;
  
  register(name: string, shader: ShaderDefinition): void {
    // Register custom shader
    // Validate GLSL syntax
    // Compile and cache
    // Enable hot reload in dev
  }
  
  get(name: string): CompiledShader {
    // Return compiled shader
    // Handle errors gracefully
    // Provide helpful error messages
  }
  
  // All original implementation
  // No library dependencies
}
```

**Features:**
- Hot reload in development
- Type-safe shader uniforms
- Automatic error detection
- Performance monitoring
- Memory management

#### Shader Component Integration
```typescript
// React component wrapper for custom shaders
interface CustomShaderProps {
  shaderName: string;
  uniforms: Record<string, UniformValue>;
  geometry: Geometry;
  onError?: (error: ShaderError) => void;
}

// Seamless integration with React Three Fiber
// Type-safe uniforms
// Automatic cleanup
// Performance optimized
```

### 2.2 Supporting Custom Geometry

**Requirement:** Creative Agent needs custom geometry generators. Framework must support this.

**Architecture:**

#### Geometry Generator System
```typescript
// Custom geometry generator interface
interface GeometryGenerator {
  generate(params: GeometryParams): Geometry;
  update(geometry: Geometry, params: GeometryParams): void;
  dispose(geometry: Geometry): void;
}

// Registry for custom generators
class GeometryRegistry {
  register(name: string, generator: GeometryGenerator): void;
  generate(name: string, params: GeometryParams): Geometry;
  // All original implementation
}
```

**Features:**
- Type-safe parameters
- Automatic memory management
- Update without recreation
- Performance optimization
- Integration with Three.js

### 2.3 Supporting Animation Choreography

**Requirement:** Creative Agent needs sophisticated animation control. Framework must enable this.

**Architecture:**

#### Animation Choreography System
```typescript
// Animation timeline (all original)
class AnimationTimeline {
  private sequences: AnimationSequence[];
  
  addSequence(sequence: AnimationSequence): void;
  play(): Promise<void>;
  pause(): void;
  seek(time: number): void;
  // Organic easing functions
  // Stagger calculations
  // Performance optimized
}

// Integration with GSAP for orchestration
// But core logic is original
// Custom easing functions
// Performance monitoring
```

**Features:**
- Organic easing (custom implementations)
- Stagger calculations
- Performance monitoring
- Frame-perfect timing
- Memory efficient

### 2.4 Supporting 3D Spatial Navigation

**Requirement:** Creative Agent needs spatial navigation. Framework must support this.

**Architecture:**

#### Spatial Navigation State
```typescript
// Spatial navigation store (Zustand)
interface SpatialNavigationState {
  // Current position in 3D space
  currentPosition: Vector3;
  currentPath: PathId | null;
  currentNode: NodeId | null;
  
  // Camera state
  cameraPosition: Vector3;
  cameraTarget: Vector3;
  cameraTransitioning: boolean;
  
  // Navigation actions
  navigateToNode: (nodeId: NodeId) => void;
  selectPath: (pathId: PathId) => void;
  returnToLanding: () => void;
  
  // All type-safe
  // All performant
  // All original logic
}
```

**Features:**
- Type-safe navigation
- Smooth transitions
- State persistence
- Performance optimized
- Integration with camera system

---

## PART III: WORLD-CLASS CODE STANDARDS

### 3.1 Code Organization

**Principle:** Code organization reflects conceptual organization.

**Structure:**
```
src/
├── framework/           # Core framework (all original)
│   ├── shader/          # Shader management
│   ├── geometry/        # Geometry generation
│   ├── animation/       # Animation system
│   ├── spatial/         # Spatial navigation
│   └── performance/     # Performance monitoring
├── components/
│   ├── 3d/             # 3D components (Creative Agent)
│   ├── ui/             # UI components (Codemonkey)
│   └── simulations/    # Simulations (Simulations Expert)
├── store/              # State management
├── utils/              # Utilities
└── types/              # TypeScript definitions
```

**Rules:**
- Each module has single responsibility
- Dependencies flow one direction
- No circular dependencies
- Clear separation of concerns
- Easy to test

### 3.2 TypeScript Standards

**Principle:** Type safety enables correctness and developer experience.

**Configuration:**
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

**Type Definitions:**
```typescript
// All types are explicit
// No `any` types
// Comprehensive interfaces
// Generic types for reusability
// Branded types for safety
```

### 3.3 Performance Standards

**Principle:** Performance enables the Creative Agent's vision.

**Targets:**
- 60 FPS on desktop
- 30 FPS on mobile
- <3s initial load
- <1s scene initialization
- <100ms interaction response

**Techniques:**
- Code splitting
- Lazy loading
- Memoization
- Virtualization
- Debouncing/throttling
- Web Workers for heavy calculations
- Request animation frame optimization

### 3.4 Error Handling

**Principle:** Errors are handled gracefully, with helpful messages.

**Strategy:**
```typescript
// Error boundary system
class FrameworkErrorBoundary {
  catch(error: Error, context: ErrorContext): void {
    // Log error
    // Report to monitoring
    // Provide helpful message
    // Recover gracefully
  }
}

// Type-safe error handling
// No silent failures
// Helpful error messages
// Recovery strategies
```

---

## PART IV: ALL-ORIGINAL CODE REQUIREMENTS

### 4.1 What Must Be Original

**Core Logic:**
- Shader management system
- Geometry generation system
- Animation choreography system
- Spatial navigation logic
- State management logic
- Performance monitoring
- Error handling
- Type definitions

**What Can Use Libraries:**
- React (UI framework)
- Three.js (3D rendering)
- Zustand (state management - but custom logic on top)
- GSAP (animation - but custom orchestration)
- Astro (build system)

**Principle:** Libraries provide infrastructure. We provide the intelligence.

### 4.2 Original Implementation Examples

#### Custom Shader Loader
```typescript
// All original implementation
class ShaderLoader {
  async loadShader(path: string): Promise<ShaderSource> {
    // Fetch shader file
    // Parse GLSL
    // Validate syntax
    // Extract uniforms
    // Return structured data
    // All original code
  }
  
  compileShader(source: ShaderSource, context: WebGLContext): CompiledShader {
    // Compile vertex shader
    // Compile fragment shader
    // Link program
    // Validate
    // Return compiled shader
    // All original code
  }
}
```

#### Custom Geometry Generator
```typescript
// All original implementation
class ToroidalChamberGenerator implements GeometryGenerator {
  generate(params: ToroidalParams): Geometry {
    // Calculate vertices using parametric equations
    // Generate faces using indices
    // Calculate normals
    // Generate UVs
    // Return geometry
    // All original code
    // No Three.js TorusGeometry dependency
  }
}
```

#### Custom Animation Easing
```typescript
// All original easing functions
function organicEase(t: number): number {
  // Custom cubic bezier implementation
  // (0.34, 1.56, 0.64, 1)
  // All original code
  // No library dependency
}

function pressureFlowEase(t: number): number {
  // Exponential ease-out
  // Represents pressure gradient
  // All original code
}
```

---

## PART V: FRAMEWORK ARCHITECTURE SPECIFICATIONS

### 5.1 Component Architecture

**Principle:** Components are composable, reusable, and type-safe.

**Base Component Pattern:**
```typescript
// Base component interface
interface BaseComponentProps {
  className?: string;
  style?: React.CSSProperties;
  onError?: (error: Error) => void;
}

// 3D Component Pattern
interface Component3DProps extends BaseComponentProps {
  position?: Vector3;
  rotation?: Euler;
  scale?: Vector3;
  visible?: boolean;
}

// All components follow patterns
// All are type-safe
// All are performant
```

### 5.2 State Management Architecture

**Principle:** State management enables spatial navigation and coordination.

**Store Structure:**
```typescript
// Main navigation store
interface NavigationStore {
  // Spatial state
  spatial: SpatialState;
  
  // Content state
  content: ContentState;
  
  // UI state
  ui: UIState;
  
  // Performance state
  performance: PerformanceState;
}

// All stores are type-safe
// All actions are type-safe
// All selectors are memoized
// All updates are optimized
```

### 5.3 Routing Architecture

**Principle:** Routing supports spatial navigation.

**Route Structure:**
```typescript
// Spatial routes
interface SpatialRoute {
  path: string;
  component: React.ComponentType;
  spatialPosition: Vector3;
  cameraTarget: Vector3;
  transitionDuration: number;
}

// Route configuration
const routes: SpatialRoute[] = [
  // Landing page
  { path: '/', component: LandingPage, ... },
  // Path routes
  { path: '/path1/:nodeId', component: NodeView, ... },
  // ...
];

// All routes are type-safe
// All transitions are smooth
// All positions are 3D
```

### 5.4 Performance Architecture

**Principle:** Performance monitoring enables optimization.

**Performance System:**
```typescript
// Performance monitor (all original)
class PerformanceMonitor {
  private metrics: PerformanceMetrics;
  
  measureFrame(): void {
    // Measure frame time
    // Track FPS
    // Identify bottlenecks
    // Report issues
  }
  
  measureComponent(name: string, renderTime: number): void {
    // Track component performance
    // Identify slow components
    // Provide recommendations
  }
  
  // All original implementation
  // Real-time monitoring
  // Helpful reports
}
```

---

## PART VI: INTEGRATION POINTS

### 6.1 Integration with Creative Agent

**Shader Integration:**
- Shader registry accepts Creative Agent's shaders
- Type-safe uniforms
- Hot reload support
- Error reporting

**Geometry Integration:**
- Geometry registry accepts Creative Agent's generators
- Type-safe parameters
- Memory management
- Performance optimization

**Animation Integration:**
- Animation system accepts Creative Agent's choreography
- Organic easing support
- Stagger calculations
- Performance monitoring

### 6.2 Integration with Simulations Expert

**Simulation Integration:**
- Component structure supports simulations
- State management for simulation parameters
- Performance optimization for real-time calculations
- Integration with 3D scene

**Formula Integration:**
- Formula renderer integration
- 3D space positioning
- Animation support
- Type-safe formula definitions

### 6.3 Integration with Integration Agent

**Testing Integration:**
- Test utilities provided
- Mock systems for testing
- Performance testing tools
- Error injection for testing

**Stub Integration:**
- Stub components supported
- Placeholder systems
- Integration reporting
- Coordination tools

---

## PART VII: DEVELOPER EXPERIENCE

### 7.1 API Design

**Principle:** APIs are intuitive, type-safe, and powerful.

**Examples:**
```typescript
// Intuitive API
const shader = useShader('pressure-field', {
  density: 0.5,
  pressure: 1.0,
});

// Type-safe
const geometry = useGeometry('toroidal-chamber', {
  innerRadius: 2,
  outerRadius: 4,
  height: 3,
});

// Powerful
const animation = useAnimation({
  sequences: [...],
  easing: 'organic',
  stagger: 0.1,
});
```

### 7.2 Error Messages

**Principle:** Error messages are helpful and actionable.

**Examples:**
```typescript
// Helpful error message
throw new FrameworkError(
  'Shader compilation failed',
  {
    shader: 'pressure-field',
    error: glError,
    suggestion: 'Check uniform types match GLSL types',
    documentation: '/docs/shaders/pressure-field',
  }
);
```

### 7.3 Documentation

**Principle:** Code is self-documenting, but documentation is comprehensive.

**Requirements:**
- JSDoc comments for all public APIs
- Type definitions are self-documenting
- Examples for common patterns
- Architecture diagrams
- Performance guides

---

## PART VIII: QUALITY STANDARDS

### 8.1 Code Quality

**Standards:**
- All code is original (core logic)
- All code is type-safe
- All code is tested
- All code is documented
- All code is performant

### 8.2 Architecture Quality

**Standards:**
- Architecture supports Creative Agent's vision
- Architecture is extensible
- Architecture is maintainable
- Architecture is performant
- Architecture is beautiful

### 8.3 Performance Quality

**Standards:**
- Meets performance targets
- No memory leaks
- Efficient rendering
- Optimized state updates
- Smooth animations

---

## PART IX: DELIVERY CHECKLIST

### Phase 1: Core Framework
- [ ] Shader management system
- [ ] Geometry generation system
- [ ] Animation choreography system
- [ ] Spatial navigation system
- [ ] Performance monitoring

### Phase 2: Integration
- [ ] Creative Agent integration
- [ ] Simulations Expert integration
- [ ] Integration Agent integration
- [ ] Component architecture
- [ ] State management

### Phase 3: Developer Experience
- [ ] API design
- [ ] Error handling
- [ ] Documentation
- [ ] Examples
- [ ] Tools

### Phase 4: Optimization
- [ ] Performance optimization
- [ ] Memory optimization
- [ ] Bundle size optimization
- [ ] Runtime optimization
- [ ] Build optimization

---

## CONCLUSION

This framework architecture manifests **TEKNE**—the unity of structure and function. Every architectural decision serves both functional and aesthetic purposes. The framework enables Creative Agent's vision. Nothing is arbitrary. Everything is intentional.

**The framework IS the theory's skeleton. The architecture IS the spatial structure.**

World-class code. Powerful, convenient, demanding, easy. The obviousness, effortlessly revealed.

---

**Next Steps:**
1. Implement core framework systems
2. Integrate with Creative Agent
3. Optimize performance
4. Enhance developer experience

**Status:** Ready for implementation

