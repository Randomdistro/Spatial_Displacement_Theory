# SDT Website Plan: Comprehensive Architecture

**Document Version:** 2.0
**Date:** December 11, 2025
**Status:** IMPLEMENTATION IN PROGRESS

---

## Implementation Progress

### Completed Components ✓

| Component | File | Status |
|-----------|------|--------|
| **Landing Page** | `src/pages/index.astro` | ✓ World-class with WebGL hero |
| **WebGL Hero Animation** | `src/components/HeroAnimation.tsx` | ✓ Toroidal vortex + pressure field |
| **Orbital Calculator Pro** | `src/components/OrbitalCalculatorPro.tsx` | ✓ Full preset system + Newton comparison |
| **Benchmark Dashboard** | `src/components/BenchmarkDashboard.tsx` | ✓ All 24 benchmarks, filterable |
| **Scale Visualization** | `src/components/ScaleVisualization.tsx` | ✓ 53 orders of magnitude slider |
| **3D Toroidal Electron** | `src/components/ToroidalElectron.tsx` | ✓ Three.js interactive |
| **Theory Portal** | `src/pages/theory/index.astro` | ✓ Complete navigation |
| **Theory Overview** | `src/pages/theory/overview.astro` | ✓ 5-min intro |
| **Tools Portal** | `src/pages/tools/index.astro` | ✓ Calculator showcase |
| **Visualizations Portal** | `src/pages/visualizations/index.astro` | ✓ 3D visualization showcase |
| **Papers Portal** | `src/pages/papers/index.astro` | ✓ De Rerum featured + topics |
| **About Page** | `src/pages/about/index.astro` | ✓ Philosophy + contribution |
| **Base Layout** | `src/layouts/BaseLayout.astro` | ✓ Navigation + footer |
| **Global Styles** | `src/styles/global.css` | ✓ SDT design system |
| **Tailwind Config** | `tailwind.config.mjs` | ✓ Custom colors + typography |
| **Package.json** | `package.json` | ✓ All dependencies |
| **Astro Config** | `astro.config.mjs` | ✓ React + Tailwind |

### To Build Next

- [ ] Individual benchmark report pages
- [ ] De Rerum online reader with ToC
- [ ] ATOMICUS periodic table
- [ ] Code documentation portal
- [ ] API endpoints for calculators
- [ ] Search functionality
- [ ] Dark mode toggle

---

## Executive Summary

This document outlines the comprehensive website plan for Spatial Displacement Theory (SDT), designed to serve as the primary public-facing platform for disseminating the theory, providing interactive tools, and building community engagement.

---

## 1. Strategic Objectives

### Primary Goals
1. **Scientific Credibility** — Present SDT as a rigorous, quantitatively validated alternative physics framework
2. **Accessibility** — Make complex physics accessible to multiple audiences (physicists, students, general public)
3. **Interactivity** — Provide live calculators and visualizations that demonstrate SDT predictions
4. **Community Building** — Enable contributions, discussions, and collaborative validation
5. **Documentation Hub** — Centralize all theory papers, benchmarks, and code documentation

### Target Audiences
| Audience | Primary Need | Priority |
|----------|--------------|----------|
| Academic Physicists | Rigorous derivations, falsifiable predictions | High |
| Graduate Students | Learning resources, calculation tools | High |
| Computational Scientists | Code, APIs, implementation guides | Medium |
| Science Enthusiasts | Accessible explanations, visualizations | Medium |
| Media/Journalists | Clear summaries, key claims | Low |

---

## 2. Site Architecture

```
sdt-theory.org/
├── / (Landing Page)
│   ├── Hero: "What if space isn't empty?"
│   ├── Core Insight Section
│   ├── Key Results Carousel
│   ├── Interactive Demo (Orbital Calculator)
│   └── CTA: Explore Theory / Try Calculator / Read Paper
│
├── /theory/ (Theory Portal)
│   ├── /overview/ — High-level introduction (5-min read)
│   ├── /foundations/ — Core axioms and master equation
│   ├── /atomic-physics/ — Hydrogen, fine structure, multi-electron
│   ├── /electromagnetism/ — E&M from pressure deformation
│   ├── /gravitation/ — Gravity without G
│   ├── /cosmology/ — CMB, galactic rotation, dark matter alternative
│   ├── /nuclear/ — Nuclear structure (speculative)
│   └── /predictions/ — Falsifiable predictions summary
│
├── /papers/ (Publication Library)
│   ├── /de-rerum/ — Complete treatise (PDF/HTML)
│   ├── /journal-ready/ — Submission-ready papers
│   ├── /benchmarks/ — 24 benchmark reports
│   └── /archive/ — Historical development phases
│
├── /tools/ (Interactive Calculators)
│   ├── /orbital-calculator/ — Predict orbital velocities (atoms → galaxies)
│   ├── /stellar-calculator/ — Stellar parameters from luminosity
│   ├── /atomic-spectra/ — Spectroscopic predictions
│   ├── /pressure-field/ — 3D pressure visualization
│   └── /occlusion-simulator/ — E(x,n̂) computation demo
│
├── /visualizations/ (Interactive Graphics)
│   ├── /alpha-tori/ — Toroidal electron visualization
│   ├── /void-engine/ — Spation medium animation
│   ├── /orbital-viewer/ — 3D orbital trajectories
│   └── /pressure-cascade/ — Pressure field derivation
│
├── /code/ (Software Portal)
│   ├── /overview/ — Code architecture summary
│   ├── /python/ — Python modules (sdt_core, sdt_navier)
│   ├── /cpp/ — C++ simulators documentation
│   ├── /api/ — REST API for calculations (future)
│   └── /github/ — Link to repository
│
├── /atomicus/ (Element Library)
│   ├── /hydrogen/ through /oganesson/
│   └── Interactive periodic table
│
├── /community/
│   ├── /discussions/ — Forum/GitHub Discussions link
│   ├── /contribute/ — How to contribute
│   ├── /validate/ — Independent validation guide
│   └── /contact/ — Contact form
│
├── /about/
│   ├── /philosophy/ — What SDT is and isn't
│   ├── /timeline/ — Development history
│   ├── /acknowledgments/
│   └── /cite/ — Citation formats (BibTeX, etc.)
│
└── /blog/ (Optional)
    └── Development updates, investigation reports
```

---

## 3. Landing Page Design

### Hero Section
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ╔═══════════════════════════════════════════════════╗    │
│   ║     SPATIAL DISPLACEMENT THEORY                    ║    │
│   ║     ─────────────────────────────────             ║    │
│   ║     What if quantum mechanics isn't fundamental?   ║    │
│   ╚═══════════════════════════════════════════════════╝    │
│                                                             │
│   "Particles are stable toroidal vortices in an            │
│    incompressible medium. All forces arise from            │
│    pressure gradients—not fields or curvature."            │
│                                                             │
│   [EXPLORE THEORY]  [TRY CALCULATOR]  [READ PAPER]         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Key Results Section (Interactive Cards)
```
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ ATOMIC PHYSICS │  │ GRAVITY        │  │ COSMOLOGY      │
│                │  │                │  │                │
│ Fine structure │  │ All 8 planets  │  │ No dark matter │
│ matches QM to  │  │ derived with   │  │ needed for     │
│ <0.1% for He⁺  │  │ <0.5% error    │  │ flat rotation  │
│                │  │                │  │ curves         │
│ [SEE RESULTS]  │  │ [SEE RESULTS]  │  │ [SEE RESULTS]  │
└────────────────┘  └────────────────┘  └────────────────┘
```

### Interactive Demo (Embedded Calculator)
```
┌─────────────────────────────────────────────────────────────┐
│  UNIVERSAL ORBITAL LAW: v(r) = (c/k)√(R/r)                 │
│                                                             │
│  System: [Hydrogen ▼]        k = 137                        │
│  Radius: [═══════○═══] 5.29×10⁻¹¹ m                        │
│                                                             │
│  Predicted velocity: 2.19×10⁶ m/s                          │
│  Observed velocity:  2.19×10⁶ m/s ✓                        │
│  Error: <0.01%                                              │
│                                                             │
│  [HYDROGEN] [EARTH] [JUPITER] [GALAXY] [CUSTOM]            │
└─────────────────────────────────────────────────────────────┘
```

### Benchmark Status Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│  BENCHMARK STATUS                                           │
│                                                             │
│  ████████████████░░░░░░░░ 15/24 CERTIFIED                  │
│                                                             │
│  ✓ B2: Rydberg Spectrum      ✓ B8: Orbital Mechanics       │
│  ✓ B3: Fine Structure        ✓ B11: Planetary Oblateness   │
│  ✓ B5: Hyperfine Structure   ✓ B12: Stellar Structure      │
│  ✓ B6: Many-Electron Atoms   ✓ B13: CMB Redshift           │
│  ✓ B7: k-Law Universality    ✓ B15: BAO Scale              │
│                                                             │
│  [VIEW ALL BENCHMARKS]                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Interactive Tools Specification

### 4.1 Orbital Calculator
**Purpose:** Demonstrate universal k-law across 53 orders of magnitude

**Inputs:**
- System type (atom, planet, star, galaxy, custom)
- Central mass/radius parameters
- Orbital radius

**Outputs:**
- Predicted orbital velocity
- Observed velocity (from database)
- Error percentage
- k-value derived

**Implementation:**
- WebAssembly port of `sdt_navier_cpp` core
- Progressive enhancement: works without JS, enhanced with WASM
- Mobile-responsive sliders

### 4.2 Stellar Calculator
**Purpose:** Predict stellar parameters from luminosity alone

**Inputs:**
- Stellar luminosity (L☉)
- Stellar radius (optional, for validation)

**Outputs:**
- Predicted: Mass, surface gravity, k-value
- Comparison with catalog values
- Error analysis

**Implementation:**
- Python backend (Flask/FastAPI) or client-side JS
- Integration with SIMBAD/Gaia data for validation

### 4.3 Atomic Spectra Calculator
**Purpose:** Predict spectral lines for any element

**Inputs:**
- Element (Z)
- Transition levels (n₁ → n₂)
- Include fine/hyperfine corrections

**Outputs:**
- Predicted wavelength/frequency
- NIST reference value
- Helical standing wave visualization

### 4.4 Pressure Field Visualizer
**Purpose:** Interactive 3D visualization of spation pressure fields

**Features:**
- WebGL-based 3D rendering
- Configurable mass distributions
- Real-time occlusion calculation
- Export capabilities

**Implementation:**
- Three.js or Babylon.js for rendering
- WASM for pressure field computation

### 4.5 Occlusion Simulator
**Purpose:** Demonstrate E(x,n̂) directional occlusion

**Features:**
- Ray-tracing visualization
- Multiple body configurations
- Eclipse saturation demonstration

---

## 5. Documentation Portal Structure

### Theory Navigation
```
FOUNDATIONS
├── Axiom 1: Incompressible Spation Medium
├── Axiom 2: Definitive Hard Shapes
├── Axiom 3: Pressure Gradients as Forces
├── Axiom 4: Emergent Time
└── Master Equation Derivation

ATOMIC PHYSICS
├── Coulomb Force from Pressure Gradients
├── Rydberg Spectrum from Helical Standing Waves
├── Fine Structure from Relativistic Corrections
├── Hyperfine Structure from Magnetic Moment Overlap
└── Multi-Electron Atoms from Occlusion Geometry

GRAVITATION
├── Gravity Without G
├── Planetary Accelerations Derivation
├── Mercury Perihelion Precession
├── Gravitational Lensing
└── Gravitational Waves (Investigation)

[... etc for all 6 domains]
```

### Paper Viewer Features
- LaTeX math rendering (KaTeX/MathJax)
- Collapsible derivation sections
- Cross-reference links
- PDF download options
- Citation copy buttons

---

## 6. Technical Implementation

### Recommended Stack

**Static Site Generator:**
- **Astro** (recommended) — Fast, content-focused, excellent Markdown support
- Alternative: Next.js for more interactivity

**Styling:**
- Tailwind CSS for utility-first styling
- Custom design system for scientific aesthetics

**Interactive Components:**
- React/Preact for calculators
- Three.js for 3D visualizations
- D3.js for data visualizations

**Performance:**
- WebAssembly for heavy calculations
- Edge caching (Cloudflare/Vercel)
- Progressive loading

**Search:**
- Algolia DocSearch or Pagefind
- Full-text search across all papers

**Hosting:**
- Vercel or Cloudflare Pages (recommended)
- GitHub Pages as backup
- Custom domain: sdt-theory.org or spatial-displacement.org

### Content Pipeline
```
/SDT/Papers/ (Markdown)
    ↓
Build script (convert MD → HTML)
    ↓
Astro build
    ↓
Static HTML + JS bundles
    ↓
Deploy to Vercel
```

### API Architecture (Future)
```
/api/v1/
├── /calculate/orbital — Orbital velocity calculation
├── /calculate/stellar — Stellar parameter prediction
├── /calculate/spectra — Spectral line prediction
├── /data/benchmarks — Benchmark results JSON
├── /data/elements — ATOMICUS data
└── /validate — Independent validation endpoint
```

---

## 7. Content Migration Plan

### Phase 1: Core Pages (Week 1-2)
- [ ] Landing page
- [ ] Theory overview
- [ ] About/Philosophy

### Phase 2: Theory Portal (Week 3-4)
- [ ] Convert Part_I papers to web format
- [ ] Add navigation structure
- [ ] LaTeX rendering setup

### Phase 3: Interactive Tools (Week 5-8)
- [ ] Orbital calculator (basic)
- [ ] Stellar calculator
- [ ] Existing HTML visualizations integration

### Phase 4: Documentation (Week 9-10)
- [ ] De Rerum Todo Existens (web version)
- [ ] Benchmark reports
- [ ] Code documentation

### Phase 5: Community Features (Week 11-12)
- [ ] GitHub Discussions integration
- [ ] Contribution guide
- [ ] Contact form

### Phase 6: Polish & Launch
- [ ] SEO optimization
- [ ] Performance audit
- [ ] Analytics setup
- [ ] Social sharing cards

---

## 8. Design Guidelines

### Visual Identity
- **Color Palette:**
  - Primary: Deep blue (#1a365d) — Scientific credibility
  - Accent: Gold (#d69e2e) — Discovery/Insight
  - Background: Off-white (#f7fafc) — Clean, readable
  - Code: Charcoal (#2d3748)

- **Typography:**
  - Headings: Inter or IBM Plex Sans (modern, authoritative)
  - Body: Source Serif Pro (readable for long text)
  - Code/Math: JetBrains Mono

### UI Patterns
- Collapsible derivation sections
- Hover tooltips for terms
- Progress indicators for long articles
- "Jump to section" navigation
- Dark mode support

### Accessibility
- WCAG 2.1 AA compliance
- Screen reader compatible
- Keyboard navigation
- High contrast mode

---

## 9. SEO Strategy

### Target Keywords
- "alternative to quantum mechanics"
- "geometric theory of gravity"
- "dark matter alternative"
- "pressure field physics"
- "spatial displacement theory"
- "toroidal electron model"

### Content Strategy
- Each benchmark gets a dedicated page with schema markup
- Calculator tools generate shareable result URLs
- Theory pages have clear meta descriptions
- Structured data for scientific articles

### Backlink Strategy
- Submit to physics preprint servers (Zenodo, OSF)
- ResearchGate profile with links
- Academic social media presence
- Physics forum discussions (with value-add, not spam)

---

## 10. Analytics & Metrics

### Key Performance Indicators
| Metric | Target | Measurement |
|--------|--------|-------------|
| Monthly unique visitors | 1000+ | Google Analytics |
| Calculator uses | 500+/month | Event tracking |
| Paper downloads | 200+/month | Download tracking |
| Average session duration | >3 min | GA |
| Benchmark validation attempts | 50+/month | Form submissions |
| GitHub stars | 100+ | GitHub API |

### Feedback Collection
- Exit intent surveys
- Calculator result feedback
- Paper helpfulness ratings
- Bug report form

---

## 11. Risk Mitigation

### Technical Risks
| Risk | Mitigation |
|------|------------|
| WASM calculator too slow | Fallback to server-side API |
| Math rendering issues | Pre-render critical equations as SVG |
| Mobile performance | Progressive enhancement, lazy loading |

### Content Risks
| Risk | Mitigation |
|------|------------|
| Theory errors discovered | Clear versioning, errata page |
| Community criticism | Transparent response, documented corrections |
| Misrepresentation | Clear disclaimers about pre-publication status |

---

## 12. Budget Estimate (Optional)

### Zero-Cost Option
- GitHub Pages hosting (free)
- Cloudflare DNS/CDN (free tier)
- No custom domain initially
- Manual content updates

### Low-Cost Option (~$50/year)
- Custom domain ($12-15/year)
- Vercel Pro for analytics ($20/month × 2 = $40)
- Basic monitoring

### Professional Option (~$200/year)
- Premium domain
- Vercel Team
- Algolia DocSearch
- Error monitoring (Sentry)

---

## 13. Next Steps

### Immediate Actions (This Week)
1. [ ] Register domain (sdt-theory.org)
2. [ ] Set up GitHub repository for website
3. [ ] Create Astro project scaffold
4. [ ] Design landing page mockup

### Short-Term (Next 2 Weeks)
1. [ ] Build landing page
2. [ ] Migrate theory overview content
3. [ ] Set up math rendering
4. [ ] Deploy MVP to Vercel

### Medium-Term (Next Month)
1. [ ] Build orbital calculator
2. [ ] Migrate paper content
3. [ ] Set up search
4. [ ] Community features

---

## 14. Appendix: Existing Assets

### HTML Visualizations (Ready to Integrate)
- `SDT/Code/alpha_tori.html` — Toroidal visualization
- `SDT/Code/void_engine.html` — Spation animation
- `SDT/Code/pressure_cascade_derivation.html` — Derivation visual

### Content Sources
- `SDT/README.md` — Main project README (640 lines)
- `SDT/Papers/README_START_HERE.md` — Quick start guide
- `SDT/Papers/SDT_Foundation/De_Rerum_Todo_Existens/DE_RERUM_TODO_EXISTENS_COMPLETE.md` — Full treatise (410KB)
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/` — 52+ theory files
- `SDT/ATOMICUS/` — 118 element files

### Calculators (Port to Web)
- `SDT/Code/sdt_core/` — Python core library
- `SDT/Code/sdt_navier_cpp/` — C++ field solver (WASM candidate)
- `SDT/tools/star_calculator_complete.py` — Stellar calculator

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-11 | Initial comprehensive plan |

---

**Prepared by:** Architecture Agent
**Review Status:** Awaiting approval
**Next Review:** [TBD]
