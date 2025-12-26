# SPATIAL DISPLACEMENT THEORY: 3D INTERACTIVE WEBSITE DEVELOPMENT PROMPT
## Comprehensive Agentic Development Specification

**Document Version:** 1.0  
**Date:** December 2025  
**Project:** SDT Interactive 3D Walkthrough Website  
**Agent Count:** 4 (Frontend/3D, Content/Narrative, Physics/Simulation, Integration/Orchestration)  
**Target Platform:** Web (Three.js/WebGL, React/Astro hybrid)  
**Alternative Platform Note:** HSML platform mentioned but not yet implemented—consider for future iteration

---

## EXECUTIVE SUMMARY

This document provides an **excessively detailed prompt** for developing a 3D interactive walkthrough website that serves as the complete structural outline of the Spatial Displacement Theory project. The website will feature:

1. **Landing Page:** Flower of Life motif with animated, interleaved rings that flip and rotate on user choice, creating a perspective-shifting navigation experience
2. **Three Narrative Paths:** 
   - **Path 1:** Short and fast, accessible language, "Do you want to know more?" expansion tags
   - **Path 2:** Highly detailed, comprehensive exploration
   - **Path 3:** Instructional delivery in rigorous physics language for competent scientists
3. **Interactive Elements:** 3D simulations, animations, data charts, narrated demonstrations with formulas and labels overlaid on animations
4. **Agentic Development Split:** Four specialized agents working in parallel with clear handoff points

---

## PART I: PROJECT OVERVIEW & ARCHITECTURE

### 1.1 Website Purpose & Scope

**Primary Objective:**
Create a comprehensive, interactive 3D walkthrough that serves as the **absolute and total structural outline** of the Spatial Displacement Theory project. This is not merely a documentation site—it is a **spatial experience** that mirrors the theory's core principle: space itself is the medium through which understanding flows.

**Core Philosophy:**
- **Spatial Navigation = Conceptual Navigation:** The 3D environment IS the theory structure
- **Choice-Based Learning:** Users choose their depth and path through the material
- **Multi-Modal Presentation:** Text, 3D visuals, animations, data, and narration work together
- **Progressive Disclosure:** Start simple, expand on demand, dive deep when ready

**Target Audiences:**
1. **General Public / Science Enthusiasts:** Path 1 (Short & Fast)
2. **Deep Learners / Students:** Path 2 (Highly Detailed)
3. **Physicists / Researchers:** Path 3 (Rigorous Physics Language)

### 1.2 Technical Architecture

**Recommended Stack:**
- **Framework:** Astro (static generation) + React (interactive components)
- **3D Engine:** Three.js (WebGL) for all 3D rendering
- **Animation:** GSAP (GreenSock) for UI animations, Three.js AnimationMixer for 3D
- **Math Rendering:** KaTeX for formulas
- **Narration:** Web Speech API or pre-recorded audio with Web Audio API
- **State Management:** Zustand or Jotai for global state
- **Routing:** Astro file-based routing + React Router for SPA sections
- **Build:** Vite (via Astro)
- **Deployment:** Vercel/Netlify (edge functions for API endpoints if needed)

**Alternative Consideration:**
- **HSML Platform:** User mentioned developing HSML platform. If available, this could provide a custom declarative language for 3D scenes and interactions. However, since it's not yet implemented, this prompt assumes standard web technologies. **Note for future:** HSML integration could simplify scene definitions and interaction logic.

**Performance Targets:**
- Initial load: <3 seconds
- 3D scene initialization: <1 second after page load
- 60 FPS for all animations
- Progressive loading: Load 3D assets on-demand
- Mobile support: Responsive, touch-friendly controls

### 1.3 Content Structure Overview

The website is organized as a **3D spatial tree** where each node represents a concept, and navigation between nodes is a 3D transition:

```
ROOT (Landing: Flower of Life)
│
├── PATH 1: Short & Fast (Accessible)
│   ├── Node 1.1: What is SDT? (2 min read)
│   │   ├── [Do you want to know more?] → Expands to Node 1.1a
│   │   ├── [Tech Specs] → Expands to Node 1.1b
│   │   └── [Simulation] → Expands to Node 1.1c
│   ├── Node 1.2: Core Insight (3 min read)
│   ├── Node 1.3: Key Results (5 min read)
│   └── ...
│
├── PATH 2: Highly Detailed (Comprehensive)
│   ├── Node 2.1: Complete Axiomatic Foundation
│   ├── Node 2.2: Full Derivation Tree
│   ├── Node 2.3: All 24 Benchmarks
│   └── ...
│
└── PATH 3: Rigorous Physics (Scientific)
    ├── Node 3.1: Master Equation Derivation
    ├── Node 3.2: Mathematical Framework
    ├── Node 3.3: Validation Protocol
    └── ...
```

**Navigation Mechanism:**
- User selects a path at the landing page
- Flower of Life rings animate (flip/rotate) to reveal the chosen path
- Camera transitions through 3D space following the path
- Each node is a "room" or "chamber" in 3D space
- Transitions between nodes are smooth camera movements

---

## PART II: LANDING PAGE SPECIFICATION

### 2.1 Flower of Life Motif Design

**Visual Design:**
- **Base Pattern:** Sacred geometry Flower of Life pattern (overlapping circles forming hexagonal flower pattern)
- **3D Implementation:** Interleaved rings (torus geometries) arranged in Flower of Life pattern
- **Color Scheme:** 
  - Base rings: Deep blue (#1a365d) with subtle metallic sheen
  - Directional colorization: Gradient from blue → gold (#d69e2e) indicating "flow direction"
  - Active selection: Bright gold highlight
  - Hover state: Subtle glow effect
- **Stylistic Approach:** 
  - Tasteful, not garish
  - Scientific aesthetic (clean, precise, elegant)
  - Slight directional colorization suggests the "pressure flow" concept central to SDT

**Ring Structure:**
- **Primary Rings:** 7-19 interleaved torus geometries (configurable)
- **Ring Thickness:** 0.02 units (relative to scene scale)
- **Ring Radius:** Variable, following Flower of Life proportions
- **Ring Segments:** 64 segments per ring for smooth appearance
- **Material:** PBR (Physically Based Rendering) material with:
  - Metallic: 0.8
  - Roughness: 0.2
  - Emissive: Subtle glow (0.1 intensity)
  - Normal map: Subtle surface detail

**Animation System:**
- **Idle Animation:** Slow rotation (0.5 RPM) around central axis
  - Each ring rotates at slightly different speed (0.4-0.6 RPM)
  - Creates mesmerizing, organic motion
  - Suggests the "flow" of spation medium
- **Hover Animation:** 
  - Ring scales up 1.1x
  - Emissive intensity increases to 0.3
  - Rotation speed increases 2x
- **Selection Animation (Path Choice):**
  - **Phase 1 (0-0.5s):** Selected ring(s) scale to 1.2x, others fade to 0.3 opacity
  - **Phase 2 (0.5-1.5s):** Rings flip (180° rotation on X-axis) while rotating around Y-axis
  - **Phase 3 (1.5-2.5s):** Camera begins transition, rings continue rotating
  - **Phase 4 (2.5-3.5s):** Rings fade out, new path environment fades in
  - **Easing:** Custom cubic-bezier for organic feel

**Interaction Design:**
- **Hover Detection:** Raycasting from camera to rings
- **Click/Tap:** Selects path
- **Visual Feedback:** 
  - Cursor changes to "pointer" on hover
  - Ring highlights with gold glow
  - Subtle sound effect (optional, can be muted)

### 2.2 Path Selection Interface

**Three Path Options:**
Each path is represented by a **cluster of rings** in the Flower of Life pattern:

1. **Path 1 (Short & Fast):** 
   - **Visual:** 3 rings, lighter blue, faster rotation
   - **Label:** "Quick Tour" (appears on hover)
   - **Description:** "A 15-minute introduction to SDT's core ideas"

2. **Path 2 (Highly Detailed):**
   - **Visual:** 7 rings, medium blue, moderate rotation
   - **Label:** "Deep Dive" (appears on hover)
   - **Description:** "Comprehensive exploration of all SDT concepts"

3. **Path 3 (Rigorous Physics):**
   - **Visual:** 13 rings, darker blue, slower rotation
   - **Label:** "Scientific Framework" (appears on hover)
   - **Description:** "Complete mathematical and physical derivation"

**Selection Mechanism:**
- User hovers over a path cluster
- Rings in that cluster highlight
- Click/tap selects
- Animation sequence begins (see 2.1)

**Text Overlay (Optional):**
- Subtle text appears below Flower of Life:
  - "Choose your journey through Spatial Displacement Theory"
  - Fades in after 2 seconds
  - Fades out on path selection

### 2.3 Camera System & Transitions

**Initial Camera Position:**
- **Type:** PerspectiveCamera
- **FOV:** 60 degrees
- **Position:** (0, 0, 5) - Looking at origin where Flower of Life is centered
- **Target:** (0, 0, 0)
- **Up Vector:** (0, 1, 0)

**Transition Animation (On Path Selection):**
- **Duration:** 3.5 seconds total
- **Phase 1 (0-1s):** Camera moves closer (z: 5 → 2), slight rotation
- **Phase 2 (1-2s):** Camera rotates around Flower of Life (orbital motion)
- **Phase 3 (2-3s):** Camera moves "through" the rings (z: 2 → -2)
- **Phase 4 (3-3.5s):** Camera settles into new position for selected path
- **Easing:** Ease-in-out cubic

**Path-Specific Camera Positions:**
- **Path 1:** Camera at (0, 1, 3) - Elevated, overview perspective
- **Path 2:** Camera at (0, 0, 4) - Centered, detailed view
- **Path 3:** Camera at (0, -1, 5) - Lowered, technical perspective

**Camera Controls:**
- **Orbit Controls:** Enabled (user can rotate/zoom/pan)
- **Constraints:** 
  - Min distance: 1 unit
  - Max distance: 10 units
  - Vertical rotation: ±85 degrees
- **Smooth Damping:** 0.05 (smooth, responsive feel)

---

## PART III: NARRATIVE PATH SPECIFICATIONS

### 3.1 PATH 1: Short & Fast (Accessible Language)

**Target Audience:** General public, science enthusiasts, students new to physics  
**Tone:** Conversational, engaging, non-condescending  
**Pacing:** Fast, touching on key details without overwhelming  
**Structure:** Linear with expansion points

#### 3.1.1 Node 1.1: "What if Space Isn't Empty?"

**Content:**
- **Opening Statement:** "For a century, we've described atoms with probability waves and gravity as curved spacetime. But what if there's a simpler explanation?"
- **Core Question:** "What if space itself is a pressurized medium, and particles are stable structures within it?"
- **Visual:** 3D animation of "empty space" filling with spation medium (particle-like spheres flowing)
- **Duration:** 2 minutes reading time

**Expansion Points:**
- **[Do you want to know more?]** → Expands inline:
  - "Why does this matter?" (1 paragraph)
  - "How is this different from other theories?" (1 paragraph)
  - "What evidence supports this?" (1 paragraph)
- **[Tech Specs]** → Expands to show:
  - Spation density: 5.2×10⁹⁶ kg/m³
  - Bulk modulus: 4.6×10¹¹³ Pa
  - Visualization of pressure field equations
- **[Simulation]** → Opens interactive 3D simulation:
  - User can adjust spation density
  - See pressure waves propagate
  - Observe how matter creates "holes" in the field

**Narration Script:**
> "Imagine space not as emptiness, but as an ocean of tiny particles called 'spations.' When matter exists, it pushes these spations aside, creating pressure gradients. These pressure gradients are what we experience as forces—gravity, electromagnetism, everything."

**3D Animation:**
- **Scene:** Empty 3D space
- **Animation:** Spation particles (small spheres) flow into view, filling space
- **Overlay:** Formula appears: `P(r) = P_∞ - κ·ρ_disp(r)`
- **Labels:** "Spation Medium", "Pressure Field", "Matter Exclusion"

#### 3.1.2 Node 1.2: "The Master Equation"

**Content:**
- **Core Insight:** "One equation replaces Newton, Coulomb, Schrödinger, and Einstein"
- **Equation Display:** Large, animated rendering of master equation
- **Explanation:** Simple language explanation of each term
- **Duration:** 3 minutes reading time

**Expansion Points:**
- **[Do you want to know more?]** → Expands to:
  - "How was this equation derived?" (2 paragraphs)
  - "What are the four axioms?" (bullet list with brief explanations)
- **[Tech Specs]** → Shows:
  - Complete derivation steps
  - Dimensional analysis
  - Numerical values for constants
- **[Simulation]** → Interactive equation explorer:
  - Adjust parameters
  - See how pressure field changes
  - Compare to classical physics predictions

**Narration Script:**
> "At the heart of Spatial Displacement Theory is a single equation that describes how pressure flows through space. This equation, called the master equation, replaces all the separate laws of physics with one unified principle."

**3D Animation:**
- **Scene:** 3D pressure field visualization
- **Animation:** Equation terms appear one by one, each triggering a visual effect
- **Overlay:** Formula: `∇·[K_bulk ∇Δ(x)] = -κ ρ_disp(x) (1 - E(x,n̂))`
- **Labels:** Each term labeled with its physical meaning

#### 3.1.3 Node 1.3: "From Atoms to Galaxies"

**Content:**
- **Universal Law:** "One law works from atomic scale to galactic scale"
- **k-Law Display:** `v(r) = (c/k)√(R/r)`
- **Examples:** Hydrogen atom, Earth orbit, galaxy rotation
- **Duration:** 4 minutes reading time

**Expansion Points:**
- **[Do you want to know more?]** → Expands to:
  - "How does one law work at all scales?" (2 paragraphs)
  - "What is the k-value?" (1 paragraph)
  - "Comparison to quantum mechanics and general relativity" (table)
- **[Tech Specs]** → Shows:
  - Complete derivation of k-law
  - Scale-dependent k-values
  - Error analysis across 53 orders of magnitude
- **[Simulation]** → Scale slider:
  - User drags slider from atomic to galactic scale
  - 3D visualization updates to show appropriate system
  - Velocity calculation updates in real-time
  - Comparison to observed values

**Narration Script:**
> "In conventional physics, we need different laws for atoms and galaxies. But SDT shows that the same principle—pressure balance—works everywhere. The only difference is a single number, k, that changes with scale."

**3D Animation:**
- **Scene:** Split-screen showing atom, planet, galaxy
- **Animation:** All three systems animate simultaneously
- **Overlay:** Same formula applies to all: `v(r) = (c/k)√(R/r)`
- **Labels:** "k ≈ 137 (atoms)", "k ≈ 10⁵ (galaxies)", "Same Law!"

#### 3.1.4 Node 1.4: "No Dark Matter Needed"

**Content:**
- **Galactic Rotation:** "Galaxy rotation curves match observations without dark matter"
- **Mechanism:** Eclipse effect explains flat rotation curves
- **Evidence:** Comparison to observed data
- **Duration:** 3 minutes reading time

**Expansion Points:**
- **[Do you want to know more?]** → Expands to:
  - "What is the eclipse effect?" (2 paragraphs)
  - "How does this differ from dark matter models?" (comparison table)
  - "What about other dark matter evidence?" (bullet list)
- **[Tech Specs]** → Shows:
  - Mathematical derivation of eclipse effect
  - Galaxy model parameters
  - Statistical comparison to observations
- **[Simulation]** → Galaxy rotation simulator:
  - User can adjust galaxy parameters
  - See rotation curve prediction
  - Overlay observed data points
  - Toggle between SDT prediction and dark matter model

**Narration Script:**
> "One of SDT's most striking predictions is that galaxies don't need dark matter. Instead, the way matter blocks pressure from the cosmic microwave background creates the flat rotation curves we observe."

**3D Animation:**
- **Scene:** Galaxy disk with pressure field visualization
- **Animation:** Pressure waves approach galaxy, get occluded by matter
- **Overlay:** Rotation curve graph showing SDT prediction vs. observations
- **Labels:** "Pressure Occlusion", "Eclipse Effect", "No Dark Matter"

#### 3.1.5 Node 1.5: "Validated Predictions"

**Content:**
- **Benchmark Summary:** "16 out of 24 benchmarks certified with <1% error"
- **Key Results:** Atomic physics, gravity, cosmology
- **Visual:** Interactive benchmark dashboard
- **Duration:** 5 minutes reading time

**Expansion Points:**
- **[Do you want to know more?]** → Expands to:
  - "What are the benchmarks?" (list with brief descriptions)
  - "How are they validated?" (validation protocol summary)
  - "What's still being tested?" (remaining benchmarks)
- **[Tech Specs]** → Shows:
  - Complete benchmark data
  - Error analysis
  - Experimental sources
- **[Simulation]** → Benchmark explorer:
  - User selects a benchmark
  - See prediction vs. observation
  - Interactive error analysis
  - Link to detailed report

**Narration Script:**
> "SDT makes specific, testable predictions. So far, 16 benchmarks have been validated with errors less than 1%. These range from atomic spectra to planetary orbits to cosmic structure."

**3D Animation:**
- **Scene:** 3D grid of benchmark "cards"
- **Animation:** Cards flip to reveal results
- **Overlay:** Summary statistics
- **Labels:** "Certified", "In Progress", "Predicted"

**Path 1 Summary:**
- **Total Duration:** ~20 minutes (with expansions: ~45 minutes)
- **Node Count:** 5-7 nodes (expandable)
- **Interactive Elements:** 5+ simulations, 3+ data visualizations
- **Narration:** Full voice-over for all nodes

---

### 3.2 PATH 2: Highly Detailed (Comprehensive Exploration)

**Target Audience:** Deep learners, graduate students, researchers wanting full picture  
**Tone:** Thorough, comprehensive, well-structured  
**Pacing:** Slower, complete coverage of all concepts  
**Structure:** Hierarchical tree with full navigation

#### 3.2.1 Section 2.1: Complete Axiomatic Foundation

**Node 2.1.1: The Four Axioms**
- **Content:** Full exposition of all four SDT axioms
  - Axiom 1: Incompressible Spation Medium
  - Axiom 2: Definitive Hard Shapes (Matter)
  - Axiom 3: Pressure Gradients as Forces
  - Axiom 4: Emergent Time
- **Visual:** 3D visualization of each axiom
- **Duration:** 15 minutes reading time
- **Narration:** Detailed explanation of each axiom
- **3D Animation:** Each axiom demonstrated with interactive simulation

**Node 2.1.2: Master Equation Derivation**
- **Content:** Step-by-step derivation from axioms
- **Visual:** Animated derivation with formula transitions
- **Duration:** 20 minutes reading time
- **Narration:** Complete mathematical narration
- **3D Animation:** Pressure field evolves as equation is built

**Node 2.1.3: Dimensional Foundations**
- **Content:** SDT unit system, conversion factors, primitive constants
- **Visual:** Interactive unit converter
- **Duration:** 10 minutes reading time
- **Narration:** Explanation of dimensional analysis
- **3D Animation:** Scale visualization showing unit relationships

#### 3.2.2 Section 2.2: Atomic Physics (Complete)

**Node 2.2.1: Toroidal Electron Model**
- **Content:** Full description of electron as toroidal vortex
- **Visual:** 3D interactive torus with helical standing waves
- **Duration:** 12 minutes reading time
- **Narration:** Complete physical description
- **3D Animation:** Electron structure rotating, showing helical waves

**Node 2.2.2: Rydberg Spectrum Derivation**
- **Content:** Complete derivation from helical quantization
- **Visual:** Animated energy level diagram
- **Duration:** 15 minutes reading time
- **Narration:** Step-by-step mathematical narration
- **3D Animation:** Orbital transitions with spectral line generation

**Node 2.2.3: Fine Structure**
- **Content:** Relativistic corrections in SDT framework
- **Visual:** 3D visualization of vortex relativistic effects
- **Duration:** 12 minutes reading time
- **Narration:** Explanation of fine structure splitting
- **3D Animation:** Fine structure transitions animated

**Node 2.2.4: Hyperfine Structure**
- **Content:** Magnetic moment overlap mechanism
- **Visual:** 3D visualization of nuclear-electron interaction
- **Duration:** 10 minutes reading time
- **Narration:** Complete hyperfine explanation
- **3D Animation:** Nuclear and electron fields overlapping

**Node 2.2.5: Multi-Electron Atoms**
- **Content:** Occlusion screening, electron-electron interactions
- **Visual:** 3D multi-electron atom visualization
- **Duration:** 15 minutes reading time
- **Narration:** Explanation of screening effects
- **3D Animation:** Multiple electrons with occlusion visualization

#### 3.2.3 Section 2.3: Gravitation & Cosmology (Complete)

**Node 2.3.1: Gravity Without G**
- **Content:** Complete derivation of gravitational acceleration
- **Visual:** 3D pressure field around massive body
- **Duration:** 15 minutes reading time
- **Narration:** Full gravitational derivation
- **3D Animation:** Pressure gradients creating acceleration

**Node 2.3.2: Orbital Mechanics**
- **Content:** Kepler laws from pressure balance
- **Visual:** 3D orbital simulation
- **Duration:** 12 minutes reading time
- **Narration:** Complete orbital mechanics
- **3D Animation:** Planets orbiting with pressure field visualization

**Node 2.3.3: Mercury Perihelion Precession**
- **Content:** Strong-field test of SDT gravity
- **Visual:** 3D Mercury orbit with precession
- **Duration:** 10 minutes reading time
- **Narration:** Precession mechanism explanation
- **3D Animation:** Precessing orbit with formula overlay

**Node 2.3.4: CMB & Cosmology**
- **Content:** Pressure horizon, redshift, BAO scale
- **Visual:** 3D cosmological structure
- **Duration:** 15 minutes reading time
- **Narration:** Complete cosmological framework
- **3D Animation:** Universe evolution with pressure field

**Node 2.3.5: Galactic Rotation (No Dark Matter)**
- **Content:** Eclipse effect, flat rotation curves
- **Visual:** 3D galaxy with pressure occlusion
- **Duration:** 12 minutes reading time
- **Narration:** Detailed eclipse mechanism
- **3D Animation:** Galaxy disk occluding pressure, rotation curve

#### 3.2.4 Section 2.4: All 24 Benchmarks

**Node 2.4.1-2.4.24: Individual Benchmark Reports**
- **Structure:** Each benchmark gets a dedicated node
- **Content:** 
  - Prediction statement
  - Derivation
  - Comparison to observation
  - Error analysis
  - Experimental sources
- **Visual:** Benchmark-specific 3D visualization
- **Duration:** 5-10 minutes per benchmark
- **Narration:** Complete benchmark explanation
- **3D Animation:** Benchmark-specific simulation

**Navigation:** Interactive benchmark map showing all 24 benchmarks with status indicators

**Path 2 Summary:**
- **Total Duration:** ~8-12 hours (comprehensive)
- **Node Count:** 50+ nodes
- **Interactive Elements:** 30+ simulations, 20+ data visualizations
- **Narration:** Full voice-over for all content
- **Structure:** Complete hierarchical tree with search functionality

---

### 3.3 PATH 3: Rigorous Physics (Scientific Framework)

**Target Audience:** Competent physicists, researchers, peer reviewers  
**Tone:** Formal, precise, mathematically rigorous  
**Pacing:** Technical, assumes prior knowledge  
**Structure:** Mathematical derivation tree

#### 3.3.1 Section 3.1: Mathematical Foundation

**Node 3.1.1: Axiomatic System (Formal)**
- **Content:** 
  - Formal statement of four axioms
  - Logical structure
  - Consistency proofs
  - Independence analysis
- **Visual:** Mathematical notation with proof trees
- **Duration:** 20 minutes reading time
- **Narration:** Formal mathematical narration
- **3D Animation:** Abstract mathematical structures visualized

**Node 3.1.2: Master Equation (Complete Derivation)**
- **Content:**
  - Step-by-step mathematical derivation
  - All assumptions stated
  - Approximation analysis
  - Validity conditions
- **Visual:** Animated LaTeX derivation
- **Duration:** 30 minutes reading time
- **Narration:** Complete mathematical narration
- **3D Animation:** Mathematical structure evolving

**Node 3.1.3: Dimensional Analysis & Units**
- **Content:**
  - Complete dimensional analysis
  - Unit system derivation
  - Conversion factors (all derived)
  - Fundamental constants
- **Visual:** Interactive dimensional analysis tool
- **Duration:** 15 minutes reading time
- **Narration:** Technical dimensional analysis
- **3D Animation:** Unit relationships visualized

#### 3.3.2 Section 3.2: Derivation Tree (Complete)

**Node 3.2.1: Atomic Physics Derivation**
- **Content:**
  - Toroidal electron: Complete mathematical model
  - Rydberg: Full derivation from helical quantization
  - Fine structure: Relativistic corrections derived
  - Hyperfine: Magnetic moment calculation
  - Multi-electron: Occlusion mathematics
- **Visual:** Complete derivation trees
- **Duration:** 2 hours reading time (total)
- **Narration:** Full mathematical narration
- **3D Animation:** Mathematical structures with formulas

**Node 3.2.2: Electromagnetism Derivation**
- **Content:**
  - Coulomb force from pressure gradients
  - Maxwell equations as limits
  - Field theory framework
- **Visual:** Complete EM derivation
- **Duration:** 1.5 hours reading time
- **Narration:** Technical EM derivation
- **3D Animation:** EM field structures

**Node 3.2.3: Gravitation Derivation**
- **Content:**
  - Complete gravitational acceleration derivation
  - Orbital mechanics from pressure balance
  - Strong-field corrections
  - Cosmological framework
- **Visual:** Full gravitational derivation
- **Duration:** 2 hours reading time
- **Narration:** Complete gravitational theory
- **3D Animation:** Gravitational structures

**Node 3.2.4: Thermodynamics & Transport**
- **Content:**
  - k-law universality derivation
  - Transport coefficients
  - Statistical mechanics framework
- **Visual:** Thermodynamic derivations
- **Duration:** 1 hour reading time
- **Narration:** Technical thermodynamics
- **3D Animation:** Thermodynamic processes

#### 3.3.3 Section 3.3: Validation Protocol

**Node 3.3.1: Benchmark Framework**
- **Content:**
  - Complete benchmark definitions
  - Validation criteria
  - Error analysis methodology
  - Statistical framework
- **Visual:** Benchmark framework diagram
- **Duration:** 20 minutes reading time
- **Narration:** Technical validation protocol
- **3D Animation:** Validation process flow

**Node 3.3.2: Certified Results (All 16)**
- **Content:**
  - Complete error analysis for each
  - Comparison to alternatives
  - Systematic uncertainties
  - Experimental sources
- **Visual:** Detailed benchmark reports
- **Duration:** 3 hours reading time (total)
- **Narration:** Technical benchmark analysis
- **3D Animation:** Benchmark-specific analyses

**Node 3.3.3: Falsification Criteria**
- **Content:**
  - What would falsify SDT?
  - Critical tests
  - Experimental requirements
- **Visual:** Falsification framework
- **Duration:** 15 minutes reading time
- **Narration:** Technical falsification discussion
- **3D Animation:** Critical test visualizations

**Path 3 Summary:**
- **Total Duration:** ~10-15 hours (rigorous)
- **Node Count:** 30+ nodes (deep, technical)
- **Interactive Elements:** 20+ mathematical visualizations, 15+ derivation explorers
- **Narration:** Full technical narration
- **Structure:** Complete mathematical derivation tree

---

## PART IV: AGENTIC DEVELOPMENT SPLIT

### 4.1 Agent Responsibilities

#### **AGENT 1: Frontend/3D Specialist**
**Primary Responsibilities:**
- Three.js scene setup and management
- Flower of Life 3D model creation and animation
- Camera system and transitions
- 3D node "rooms" and spatial navigation
- WebGL optimization and performance
- Responsive design for mobile/desktop
- Touch controls and accessibility

**Deliverables:**
- `src/components/FlowerOfLife.tsx` - Main landing component
- `src/components/Scene3D.tsx` - Base 3D scene wrapper
- `src/components/CameraController.tsx` - Camera system
- `src/components/NodeRoom.tsx` - 3D node container
- `src/utils/threejs-helpers.ts` - Three.js utilities
- `src/styles/3d-overrides.css` - 3D-specific styles

**Key Technologies:**
- Three.js, React Three Fiber (optional), GSAP
- WebGL shaders (if custom effects needed)
- Performance monitoring tools

**Handoff Points:**
- Provides 3D scene structure for Agent 2 (content) to populate
- Provides animation hooks for Agent 4 (integration) to trigger
- Receives content structure from Agent 2 for node layout

#### **AGENT 2: Content/Narrative Specialist**
**Primary Responsibilities:**
- All three narrative path content creation
- Text content for all nodes
- Narration scripts
- Expansion point definitions
- Content structure and organization
- Markdown/structured content format

**Deliverables:**
- `src/content/path1/` - Path 1 content files
- `src/content/path2/` - Path 2 content files
- `src/content/path3/` - Path 3 content files
- `src/content/narration/` - Narration scripts (text)
- `src/content/expansions/` - Expansion point content
- `src/types/content.ts` - Content type definitions
- Content management system structure

**Key Technologies:**
- Markdown, MDX (for React components in content)
- Content structure (JSON/YAML for metadata)
- Text processing for narration

**Handoff Points:**
- Provides content structure to Agent 1 for 3D layout
- Provides narration scripts to Agent 4 for audio integration
- Provides content to Agent 3 for simulation context

#### **AGENT 3: Physics/Simulation Specialist**
**Primary Responsibilities:**
- All 3D physics simulations
- Interactive calculators
- Data visualizations
- Formula rendering and animation
- Scientific accuracy validation
- Simulation performance optimization

**Deliverables:**
- `src/components/simulations/` - All simulation components
  - `PressureFieldSim.tsx`
  - `OrbitalSim.tsx`
  - `AtomicStructureSim.tsx`
  - `GalaxyRotationSim.tsx`
  - `BenchmarkVisualizer.tsx`
  - etc.
- `src/components/calculators/` - Interactive calculators
- `src/components/charts/` - Data visualization components
- `src/utils/physics/` - Physics calculation utilities
- `src/utils/formula-renderer.ts` - KaTeX formula rendering

**Key Technologies:**
- Three.js for 3D simulations
- D3.js or Chart.js for data visualizations
- KaTeX for math rendering
- Web Workers for heavy calculations (if needed)

**Handoff Points:**
- Provides simulation components to Agent 4 for integration
- Receives content context from Agent 2 for simulation parameters
- Provides 3D simulation meshes to Agent 1 for scene integration

#### **AGENT 4: Integration/Orchestration Specialist**
**Primary Responsibilities:**
- Overall site architecture
- Component integration
- State management
- Routing and navigation
- Narration system (audio/Web Speech API)
- User interaction orchestration
- Performance optimization
- Build system and deployment

**Deliverables:**
- `src/app/` - Main application structure
- `src/store/` - State management (Zustand/Jotai)
- `src/hooks/` - Custom React hooks
- `src/utils/navigation.ts` - Navigation system
- `src/utils/narration.ts` - Narration system
- `astro.config.mjs` - Astro configuration
- `package.json` - Dependencies
- Build and deployment scripts

**Key Technologies:**
- Astro, React, TypeScript
- State management library
- Audio API for narration
- Build tools (Vite)

**Handoff Points:**
- Orchestrates all components from Agents 1, 2, 3
- Manages communication between agents' components
- Handles user interactions and triggers appropriate responses

### 4.2 Development Workflow

**Phase 1: Foundation (Week 1-2)**
1. **Agent 4** sets up project structure (Astro + React)
2. **Agent 1** creates basic 3D scene (Flower of Life placeholder)
3. **Agent 2** creates content structure and first node content
4. **Agent 3** creates first simulation (pressure field)

**Phase 2: Core Features (Week 3-4)**
1. **Agent 1** completes Flower of Life animation and camera system
2. **Agent 2** completes Path 1 content (all nodes)
3. **Agent 3** creates core simulations (orbital, atomic, galaxy)
4. **Agent 4** integrates navigation and state management

**Phase 3: Full Content (Week 5-8)**
1. **Agent 2** completes Path 2 and Path 3 content
2. **Agent 3** creates all remaining simulations
3. **Agent 1** creates all 3D node rooms
4. **Agent 4** integrates narration system

**Phase 4: Polish & Optimization (Week 9-10)**
1. All agents: Performance optimization
2. **Agent 4**: Testing, accessibility, SEO
3. All agents: Bug fixes and refinements
4. **Agent 4**: Deployment setup

### 4.3 Communication Protocol

**Daily Standups:**
- Each agent reports progress
- Identifies blockers
- Coordinates handoffs

**Shared Resources:**
- `docs/agent-coordination.md` - Current status
- `docs/api-contracts.md` - Component interfaces
- `docs/content-structure.md` - Content organization
- GitHub Issues for task tracking

**Code Review:**
- All agents review each other's PRs
- Focus on integration points
- Ensure consistency across paths

---

## PART V: TECHNICAL SPECIFICATIONS

### 5.1 3D Scene Specifications

**Scene Graph Structure:**
```
Scene (THREE.Scene)
├── FlowerOfLife (Group)
│   ├── Ring_1 (TorusGeometry + Mesh)
│   ├── Ring_2 (TorusGeometry + Mesh)
│   └── ... (more rings)
├── Lighting
│   ├── AmbientLight (intensity: 0.4)
│   ├── DirectionalLight (intensity: 0.8, position: [5, 5, 5])
│   └── PointLight (intensity: 0.3, position: [0, 0, 0])
├── Camera (PerspectiveCamera, FOV: 60)
└── Controls (OrbitControls)
```

**Performance Targets:**
- 60 FPS on desktop (GTX 1060 or equivalent)
- 30 FPS on mobile (modern smartphone)
- Scene complexity: <50k vertices total
- Texture memory: <100 MB
- Draw calls: <100 per frame

**Optimization Strategies:**
- Level-of-detail (LOD) for distant objects
- Frustum culling
- Instanced rendering for repeated elements
- Texture compression (KTX2/Basis)
- Geometry simplification for mobile

### 5.2 Content Format Specification

**Node Content Structure (JSON):**
```json
{
  "id": "path1-node1",
  "title": "What if Space Isn't Empty?",
  "path": "path1",
  "readingTime": 2,
  "content": {
    "main": "markdown content here...",
    "expansions": {
      "know-more": "expansion content...",
      "tech-specs": "technical content...",
      "simulation": "simulation-id-reference"
    }
  },
  "narration": {
    "script": "narration text...",
    "audioFile": "path/to/audio.mp3",
    "timing": [0, 5, 10, 15] // seconds
  },
  "visualizations": {
    "3dAnimation": "animation-id",
    "formulas": ["formula1", "formula2"],
    "charts": ["chart-id"]
  },
  "position": [0, 1, 3], // 3D position in scene
  "cameraTarget": [0, 0, 0]
}
```

**Content File Organization:**
```
src/content/
├── path1/
│   ├── node1.json
│   ├── node2.json
│   └── ...
├── path2/
│   └── ...
├── path3/
│   └── ...
└── shared/
    ├── formulas/
    ├── images/
    └── data/
```

### 5.3 Simulation Specifications

**Simulation Component Interface:**
```typescript
interface SimulationProps {
  parameters: Record<string, number>;
  onParameterChange: (key: string, value: number) => void;
  showFormulas: boolean;
  showLabels: boolean;
  narrationEnabled: boolean;
}

interface SimulationState {
  isPlaying: boolean;
  time: number;
  cameraPosition: [number, number, number];
}
```

**Common Simulations:**
1. **PressureFieldSim:** 3D pressure field visualization
2. **OrbitalSim:** Orbital mechanics (atoms to galaxies)
3. **AtomicStructureSim:** Toroidal electron, orbitals
4. **GalaxyRotationSim:** Galaxy with rotation curve
5. **BenchmarkVisualizer:** Interactive benchmark comparison

**Performance:**
- Simulations run at 60 FPS when active
- Pause when not in view (viewport detection)
- Web Workers for heavy calculations
- Progressive quality (lower quality on mobile)

### 5.4 Narration System

**Implementation Options:**
1. **Pre-recorded Audio:** High quality, large file size
2. **Web Speech API (Synthesis):** Real-time, variable quality
3. **Hybrid:** Pre-recorded for important sections, synthesis for expansions

**Narration Features:**
- Play/pause controls
- Speed adjustment (0.5x - 2x)
- Skip to next section
- Highlight text as narration plays
- Volume control
- Mute option

**Audio Format:**
- Format: MP3 or OGG Vorbis
- Bitrate: 128 kbps (acceptable quality, reasonable size)
- Sample rate: 44.1 kHz
- Mono (speech doesn't need stereo)

### 5.5 Formula Rendering

**Technology:** KaTeX (fast, server-side rendering possible)

**Formula Display:**
- Inline formulas: `$...$`
- Block formulas: `$$...$$`
- Animated formulas: Formulas appear term-by-term
- Interactive formulas: Click to expand/collapse steps

**Formula Animation:**
- Terms appear sequentially
- Highlighting as narration mentions them
- Color coding: Known terms (blue), derived terms (green), results (gold)

### 5.6 Data Visualization

**Chart Types:**
- Line charts (rotation curves, spectra)
- Bar charts (benchmark comparisons)
- Scatter plots (prediction vs. observation)
- 3D surface plots (pressure fields)

**Technology:** 
- D3.js for custom visualizations
- Chart.js for standard charts
- Three.js for 3D plots

**Interactivity:**
- Hover tooltips
- Zoom/pan
- Data point selection
- Comparison overlays

---

## PART VI: IMPLEMENTATION CHECKLIST

### 6.1 Agent 1 (Frontend/3D) Checklist

- [ ] Set up Three.js scene with proper lighting
- [ ] Create Flower of Life geometry (interleaved rings)
- [ ] Implement ring animations (idle, hover, selection)
- [ ] Create camera system with smooth transitions
- [ ] Build 3D node "room" system
- [ ] Implement spatial navigation
- [ ] Add touch controls for mobile
- [ ] Optimize for performance (LOD, culling, etc.)
- [ ] Test on multiple devices/browsers
- [ ] Ensure accessibility (keyboard navigation, screen reader support)

### 6.2 Agent 2 (Content/Narrative) Checklist

- [ ] Create content structure (JSON/Markdown format)
- [ ] Write Path 1 content (all nodes)
- [ ] Write Path 2 content (all nodes)
- [ ] Write Path 3 content (all nodes)
- [ ] Write all narration scripts
- [ ] Define all expansion points
- [ ] Create content type definitions (TypeScript)
- [ ] Organize content files
- [ ] Add metadata (reading time, tags, etc.)
- [ ] Review content for accuracy and clarity

### 6.3 Agent 3 (Physics/Simulation) Checklist

- [ ] Create pressure field simulation
- [ ] Create orbital mechanics simulation
- [ ] Create atomic structure simulation
- [ ] Create galaxy rotation simulation
- [ ] Create benchmark visualizer
- [ ] Implement formula renderer (KaTeX)
- [ ] Create data visualization components
- [ ] Build interactive calculators
- [ ] Validate scientific accuracy
- [ ] Optimize simulation performance

### 6.4 Agent 4 (Integration/Orchestration) Checklist

- [ ] Set up Astro project structure
- [ ] Configure React integration
- [ ] Set up state management
- [ ] Implement routing system
- [ ] Create navigation orchestration
- [ ] Integrate narration system
- [ ] Set up build system
- [ ] Configure deployment
- [ ] Implement performance monitoring
- [ ] Add analytics (privacy-respecting)
- [ ] Ensure SEO optimization
- [ ] Test full user flows
- [ ] Implement error handling
- [ ] Add loading states
- [ ] Create fallbacks for unsupported features

---

## PART VII: SUCCESS CRITERIA

### 7.1 Functional Requirements

✅ **Landing Page:**
- Flower of Life renders correctly
- Rings animate smoothly
- Path selection works
- Camera transition is smooth

✅ **Navigation:**
- All three paths accessible
- Smooth transitions between nodes
- User can return to landing page
- Breadcrumb navigation works

✅ **Content:**
- All three narrative styles implemented
- Expansion points work
- Formulas render correctly
- Narration plays synchronously

✅ **Simulations:**
- All simulations run smoothly
- Interactive controls work
- Formulas overlay correctly
- Data visualizations accurate

✅ **Performance:**
- 60 FPS on desktop
- 30 FPS on mobile
- Load time <3 seconds
- No memory leaks

### 7.2 User Experience Requirements

✅ **Accessibility:**
- Keyboard navigation works
- Screen reader compatible
- High contrast mode supported
- Text resizable

✅ **Responsiveness:**
- Works on desktop (1920x1080+)
- Works on tablet (768px+)
- Works on mobile (375px+)
- Touch controls intuitive

✅ **Usability:**
- Clear navigation
- Intuitive controls
- Helpful error messages
- Loading indicators

### 7.3 Scientific Accuracy Requirements

✅ **Content Accuracy:**
- All physics content verified
- Formulas correct
- Simulations match theory
- Data visualizations accurate

✅ **Validation:**
- Benchmarks correctly represented
- Error analysis accurate
- Experimental data properly cited
- Predictions clearly labeled

---

## PART VIII: FUTURE ENHANCEMENTS

### 8.1 HSML Platform Integration

**If HSML platform becomes available:**
- Migrate 3D scene definitions to HSML
- Use HSML for interaction logic
- Leverage HSML's declarative syntax
- Simplify scene management

### 8.2 Advanced Features

- **Multi-user exploration:** Shared 3D spaces
- **VR/AR support:** Immersive experience
- **Offline mode:** Download content for offline use
- **Custom paths:** User-created exploration paths
- **Collaborative annotations:** Users can add notes
- **Export functionality:** Export visualizations, data

### 8.3 Content Expansion

- **Interactive tutorials:** Step-by-step guides
- **Problem sets:** Practice exercises
- **Video content:** Embedded video explanations
- **Community contributions:** User-submitted content
- **Multilingual support:** Translate to other languages

---

## PART IX: APPENDIX

### 9.1 Key SDT Concepts Reference

**For content creators (Agent 2):**

**Core Principles:**
- Space is a pressurized medium (spation)
- Matter excludes spation volume
- Forces arise from pressure gradients
- Time emerges from oscillation counting

**Master Equation:**
```
∇·[K_bulk ∇Δ(x)] = -κ ρ_disp(x) (1 - E(x,n̂))
```

**Universal k-Law:**
```
v(r) = (c/k)√(R/r)
```

**Key Constants:**
- K_bulk = 4.6×10¹¹³ Pa
- ρ_s = 5.2×10⁹⁶ kg/m³
- c = 299,792,458 m/s
- α = 1/137.036

**Benchmark Status:**
- 16/24 certified
- <1% error across 53 orders of magnitude

### 9.2 Technical Resources

**Three.js Documentation:**
- https://threejs.org/docs/

**Astro Documentation:**
- https://docs.astro.build/

**KaTeX Documentation:**
- https://katex.org/docs/

**GSAP Documentation:**
- https://greensock.com/docs/

### 9.3 Content Sources

**Primary Sources:**
- `SDT/Papers/SDT_Foundation/` - Complete theory
- `SDT/README.md` - Project overview
- `QUICK_PROJECT_SUMMARY.md` - Quick reference
- `SDT/benchmarks/` - Benchmark data

**Visualization Sources:**
- `SDT/Code/sdt_atomic_sim/` - Atomic simulations
- `SDT/Code/sdt_chemistry/` - Molecular structures
- `SDT/Code/sdt_orbital_sim/` - Orbital mechanics

---

## CONCLUSION

This prompt provides an **excessively detailed specification** for developing a 3D interactive walkthrough website for Spatial Displacement Theory. The development is split across four specialized agents, each with clear responsibilities and deliverables.

**Key Features:**
1. **Flower of Life Landing Page:** Animated, interactive, beautiful
2. **Three Narrative Paths:** Accessible, detailed, rigorous
3. **Rich Interactivity:** 3D simulations, animations, data charts
4. **Narration System:** Synchronized audio with visual content
5. **Agentic Development:** Four agents working in parallel

**Success Metrics:**
- Functional: All features work as specified
- Performance: 60 FPS, <3s load time
- Accuracy: Scientifically correct content
- Usability: Intuitive, accessible, responsive

**Timeline:** 10 weeks for complete implementation

**Next Steps:**
1. Review and approve this prompt
2. Assign agents (or confirm agent roles)
3. Begin Phase 1: Foundation
4. Daily coordination meetings
5. Weekly progress reviews

---

**Document Status:** READY FOR IMPLEMENTATION  
**Last Updated:** December 2025  
**Version:** 1.0

