# Visual Explainer System

Comprehensive, cross-referenced visual explainer system for SDT covering every paper, phase, benchmark, formula, rule, and concept.

## Components

### Core Components

- **ExplainerRegistry** - Central registry mapping concepts to explainers
- **ExplainerViewer** - Main component for displaying explainers
- **CrossReferenceSidebar** - Shows related concepts
- **CrossReferenceGraph** - Interactive graph visualization

### Visualization Components

- **3D Visualizations** - SpationLattice, NuclearPacking, HelicalOrbitals, PressureField, OrbitalMechanics
- **Animations** - ShuntDynamics
- **Charts** - BenchmarkChart (to be implemented)
- **Formulas** - FormulaTree (to be implemented)

## Usage

```tsx
import { ExplainerRegistryProvider, ExplainerViewer } from './components/explainers';

<ExplainerRegistryProvider>
  <ExplainerViewer explainerId="paper-core-engine" />
</ExplainerRegistryProvider>
```

## Data Structure

Explainers are stored as JSON files in `public/data/explainers/{category}/{id}.json`

Each explainer includes:
- Metadata (title, description, category, domain)
- Content (markdown, formulas, visualizations)
- Cross-references (related papers, phases, benchmarks, formulas)
- Validation data (for benchmarks)

## Cross-References

Cross-references are stored in `public/data/explainers/crossReferences.json` and define relationships between concepts.

## Status

Foundation complete. Currently includes:
- 1 paper explainer (Core Engine)
- 2 rule explainers (Four Primitives, Shunt Dynamics)
- 1 benchmark explainer (k-Law Universality)

More explainers to be added systematically.

