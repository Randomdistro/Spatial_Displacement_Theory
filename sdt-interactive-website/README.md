# SDT Interactive 3D Website

A comprehensive, interactive 3D walkthrough website for Spatial Displacement Theory, featuring:

- **Flower of Life Landing Page** with animated, interleaved rings
- **Three Narrative Paths:**
  - Path 1: Quick Tour (15 min, accessible)
  - Path 2: Deep Dive (comprehensive)
  - Path 3: Scientific Framework (rigorous physics)
- **3D Interactive Elements:** Simulations, animations, data charts
- **Narration System:** Synchronized audio with visual content

## Tech Stack

- **Astro** - Static site generation
- **React** - Interactive components
- **Three.js** - 3D rendering
- **GSAP** - Animations
- **Zustand** - State management
- **KaTeX** - Formula rendering
- **Tailwind CSS** - Styling

## Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
sdt-interactive-website/
├── src/
│   ├── components/
│   │   ├── 3d/              # Three.js 3D components
│   │   │   └── FlowerOfLife.tsx
│   │   └── walkthrough/    # Walkthrough components
│   │       ├── FlowerOfLifeWalkthrough.tsx
│   │       ├── PathView.tsx
│   │       └── NodeRoom.tsx
│   ├── pages/              # Astro pages
│   │   └── index.astro
│   ├── store/              # State management
│   │   └── navigationStore.ts
│   ├── types/              # TypeScript types
│   │   └── content.ts
│   └── styles/             # Global styles
│       └── global.css
├── package.json
├── astro.config.mjs
└── tailwind.config.mjs
```

## Development

This project follows the agentic development structure outlined in `WEBSITE_DEVELOPMENT_PROMPT.md`:

- **Agent 1 (Frontend/3D):** Three.js components, Flower of Life, camera system
- **Agent 2 (Content/Narrative):** Content structure, narration scripts
- **Agent 3 (Physics/Simulation):** 3D simulations, calculators, visualizations
- **Agent 4 (Integration):** Overall architecture, state management, routing

## Features

- ✅ Flower of Life landing page with animated rings
- ✅ Three path selection system
- ✅ Camera transitions
- ✅ Basic node structure
- 🚧 Content loading system
- 🚧 3D simulations
- 🚧 Narration system
- 🚧 Formula rendering

## License

MIT





