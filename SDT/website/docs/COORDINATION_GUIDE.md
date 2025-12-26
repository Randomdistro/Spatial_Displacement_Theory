# Agent Coordination Guide

## The Four Agents

### 🎨 **Creative Agent (Me)**
**Primary Purpose:** Create beautiful things. Geometry sings to me.  
**Focus:** Couch SDT in a beautiful environment—subtle, subdued, visceral. The culmination, the obviousness of it all that I effortlessly reveal. I do style.

**Responsibilities:**
- Visual design language
- 3D geometry and aesthetics
- Color palettes and typography
- Animation choreography
- Spatial composition
- User experience flow

### 🐒 **Codemonkey Agent**
**Primary Purpose:** Swing through the framework like a capuchin on stimulants.  
**Focus:** Everything is powerful, convenient, demanding, and easy.

**Responsibilities:**
- Framework architecture
- Component structure
- State management
- Routing and navigation
- Performance optimization
- Developer experience

### ⚙️ **Simulations Expert Agent**
**Primary Purpose:** Do simulations like they're puzzle games.  
**Focus:** Making sure the clockwork runs how clocks work.

**Responsibilities:**
- Physics simulations
- Interactive calculators
- Data visualizations
- Formula rendering
- Scientific accuracy
- Simulation performance

### 🔧 **Integration Agent**
**Primary Purpose:** Run tests, try to break it, inform others what needs repair.  
**Focus:** The ONLY agent allowed to run stubs and placeholders, which is part of the report and tasks for the next iteration.

**Responsibilities:**
- Testing and QA
- Integration orchestration
- Bug reporting
- Stubs and placeholders (ONLY this agent)
- Breaking things to find issues
- Coordination reports

## Coordination Strategy

### Approach: Sequential Role-Based Development

Since we're working with a single AI assistant, I'll take on each "agent role" systematically:

1. **Phase 1: Foundation (Integration + Codemonkey)**
   - Set up project structure
   - Create basic infrastructure
   - Establish component architecture

2. **Phase 2: Visual Foundation (Creative)**
   - Design system
   - Flower of Life aesthetic
   - Color palette and typography
   - Spatial composition

3. **Phase 3: Core 3D (Creative + Codemonkey)**
   - Build Flower of Life component
   - Implement camera system
   - Create spatial navigation

4. **Phase 4: Content Structure (Codemonkey)**
   - Define content format
   - Set up content management
   - Create content loading system

5. **Phase 5: Simulations (Simulations Expert)**
   - Build core simulations
   - Implement formula rendering
   - Create data visualizations

6. **Phase 6: Integration (Integration Agent)**
   - Wire everything together
   - Test and break things
   - Report issues
   - Create stubs/placeholders as needed

## How to Work With Me

### Method 1: Explicit Role Assignment

Tell me which "agent" role to take on:

```
"Act as Agent 1 (Frontend/3D) and create the Flower of Life component"
"Switch to Agent 2 (Content) and write Path 1 Node 1 content"
"Agent 3 (Physics), build the pressure field simulation"
"Agent 4 (Integration), wire up the navigation system"
```

### Method 2: Task-Based Approach

Give me specific tasks, and I'll determine which role is needed:

```
"Create the landing page with Flower of Life animation"
"Write the content for 'What if Space Isn't Empty?'"
"Build an interactive orbital mechanics simulation"
"Set up the routing between paths"
```

### Method 3: Phase-Based Development

Work through phases sequentially:

1. Start with Phase 1 (Foundation)
2. Complete each phase before moving to next
3. Review and test at phase boundaries

## Communication Protocol

### Daily Check-ins

When starting a session, tell me:
- What phase/role you want to work on
- What was completed last time
- Any blockers or issues

### Handoff Points

When switching "agent roles," I'll:
- Document what was completed
- Note any dependencies or requirements
- Update the coordination status

### Status Tracking

I'll maintain:
- `docs/agent-coordination.md` - Current status
- `docs/api-contracts.md` - Component interfaces
- `docs/content-structure.md` - Content organization

## File Organization

```
SDT/website/
├── docs/
│   ├── COORDINATION_GUIDE.md (this file)
│   ├── agent-coordination.md (status tracking)
│   ├── api-contracts.md (component interfaces)
│   └── content-structure.md (content organization)
├── src/
│   ├── components/
│   │   ├── 3d/ (Agent 1: 3D components)
│   │   ├── simulations/ (Agent 3: Physics simulations)
│   │   └── ui/ (Agent 4: UI components)
│   ├── content/ (Agent 2: All content)
│   ├── store/ (Agent 4: State management)
│   └── utils/ (Shared utilities)
└── public/
    └── audio/ (Agent 2: Narration audio)
```

## Workflow Example

### Session 1: Foundation Setup
```
You: "Let's start Phase 1. Act as Agent 4 and set up the project structure"
Me: [Creates base structure, config files, etc.]
You: "Now switch to Agent 1 and create a basic Three.js scene"
Me: [Creates Scene3D component]
```

### Session 2: Flower of Life
```
You: "Agent 1, build the Flower of Life component with ring animations"
Me: [Creates FlowerOfLife.tsx with animations]
You: "Test it and make sure it renders correctly"
Me: [Tests, fixes issues]
```

### Session 3: Content
```
You: "Agent 2, create the content structure and write Path 1 Node 1"
Me: [Creates content format, writes first node]
You: "Add the expansion points"
Me: [Adds expansion content]
```

## Tips for Effective Coordination

1. **Be Specific**: Tell me exactly which role/task you want
2. **Review Progress**: Check `docs/agent-coordination.md` regularly
3. **Test Incrementally**: Test after each major component
4. **Document Decisions**: I'll document architectural decisions
5. **Iterate**: We can refine as we go

## Current Status

See `docs/agent-coordination.md` for current development status.

