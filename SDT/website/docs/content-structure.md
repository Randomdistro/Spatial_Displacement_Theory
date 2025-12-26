# Content Structure Documentation

This document defines how content is organized and structured for the SDT website.

## Content Organization

```
src/content/
├── path1/
│   ├── node1.json
│   ├── node2.json
│   └── ...
├── path2/
│   ├── section1/
│   │   ├── node1.json
│   │   └── ...
│   └── ...
├── path3/
│   ├── section1/
│   │   ├── node1.json
│   │   └── ...
│   └── ...
├── shared/
│   ├── formulas/
│   │   ├── master-equation.json
│   │   ├── k-law.json
│   │   └── ...
│   ├── images/
│   └── data/
│       ├── benchmarks.json
│       └── ...
└── metadata/
    ├── paths.json
    └── navigation.json
```

## Content Format

### Node Content (JSON)

```json
{
  "id": "path1-node1",
  "title": "What if Space Isn't Empty?",
  "path": "path1",
  "readingTime": 2,
  "content": {
    "main": "# What if Space Isn't Empty?\n\nFor a century...",
    "expansions": {
      "know-more": {
        "title": "Do you want to know more?",
        "content": "Why does this matter?...",
        "type": "inline"
      },
      "tech-specs": {
        "title": "Technical Specifications",
        "content": "Spation density: 5.2×10⁹⁶ kg/m³...",
        "type": "modal"
      },
      "simulation": {
        "title": "Interactive Simulation",
        "simulationId": "pressure-field",
        "type": "embedded"
      }
    }
  },
  "narration": {
    "script": "Imagine space not as emptiness, but as an ocean...",
    "audioFile": "path1/node1/narration.mp3",
    "timing": [0, 5, 10, 15],
    "highlights": [
      { "time": 0, "text": "Imagine space" },
      { "time": 5, "text": "ocean of tiny particles" }
    ]
  },
  "visualizations": {
    "3dAnimation": "spation-flow",
    "formulas": ["master-equation", "pressure-field"],
    "charts": [],
    "simulation": "pressure-field"
  },
  "position": [0, 1, 3],
  "cameraTarget": [0, 0, 0],
  "metadata": {
    "tags": ["introduction", "core-concept"],
    "difficulty": "beginner",
    "prerequisites": []
  }
}
```

## Formula Format

### Formula Definition (JSON)

```json
{
  "id": "master-equation",
  "latex": "\\nabla \\cdot [K_{bulk} \\nabla \\Delta(x)] = -\\kappa \\rho_{disp}(x) (1 - E(x,\\hat{n}))",
  "displayMode": "block",
  "terms": [
    {
      "id": "K_bulk",
      "name": "Bulk Modulus",
      "value": "4.6×10¹¹³ Pa",
      "description": "The bulk modulus of the spation medium"
    },
    {
      "id": "rho_disp",
      "name": "Displacement Density",
      "description": "The density of displaced spation"
    }
  ],
  "derivation": {
    "steps": [
      {
        "step": 1,
        "description": "Start with pressure gradient",
        "formula": "..."
      }
    ]
  }
}
```

## Path Metadata

### Path Definition (JSON)

```json
{
  "id": "path1",
  "name": "Short & Fast",
  "description": "A 15-minute introduction to SDT's core ideas",
  "targetAudience": "General Public / Science Enthusiasts",
  "tone": "Conversational, engaging, non-condescending",
  "pacing": "Fast",
  "nodes": [
    "path1-node1",
    "path1-node2",
    "path1-node3",
    "path1-node4",
    "path1-node5"
  ],
  "estimatedDuration": 20,
  "estimatedDurationWithExpansions": 45
}
```

## Navigation Structure

### Navigation Definition (JSON)

```json
{
  "landing": {
    "type": "flower-of-life",
    "paths": [
      {
        "id": "path1",
        "cluster": [1, 2, 3],
        "position": [0, 0, 0],
        "label": "Quick Tour"
      },
      {
        "id": "path2",
        "cluster": [4, 5, 6, 7, 8, 9, 10],
        "position": [2, 0, 0],
        "label": "Deep Dive"
      },
      {
        "id": "path3",
        "cluster": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        "position": [-2, 0, 0],
        "label": "Scientific Framework"
      }
    ]
  },
  "paths": {
    "path1": {
      "layout": "linear",
      "nodes": [
        {
          "id": "path1-node1",
          "position": [0, 1, 3],
          "connections": ["path1-node2"]
        }
      ]
    }
  }
}
```

## Content Creation Guidelines

### Path 1 (Short & Fast)
- **Tone**: Conversational, accessible
- **Length**: 2-5 minutes per node
- **Expansions**: "Do you want to know more?", "Tech Specs", "Simulation"
- **Language**: Avoid jargon, explain concepts simply

### Path 2 (Highly Detailed)
- **Tone**: Thorough, comprehensive
- **Length**: 10-20 minutes per node
- **Expansions**: Full derivations, all details
- **Language**: Technical but accessible

### Path 3 (Rigorous Physics)
- **Tone**: Formal, precise, mathematical
- **Length**: 20-60 minutes per node
- **Expansions**: Complete proofs, all assumptions
- **Language**: Rigorous physics/mathematics

## Narration Guidelines

### Script Format
- Write in second person ("you", "your")
- Use active voice
- Keep sentences short (15-20 words)
- Pause for emphasis (indicated by `...`)
- Highlight key terms

### Timing
- Average speaking rate: 150 words/minute
- Pause for formulas: +2 seconds
- Pause for animations: +3 seconds
- Total timing should match reading time

## Expansion Types

1. **Inline**: Expands within the content flow
2. **Modal**: Opens in a modal overlay
3. **Embedded**: Embeds a simulation/visualization
4. **Sidebar**: Appears in a sidebar panel

## Content Validation

Before adding content, ensure:
- [ ] JSON is valid
- [ ] All required fields present
- [ ] IDs are unique
- [ ] References to formulas/simulations exist
- [ ] Position coordinates are valid
- [ ] Reading time is accurate
- [ ] Narration script matches content

## Content Loading

```typescript
// Content loader utility
import { loadNodeContent, loadPathContent } from '@/utils/content-loader';

// Load single node
const node = await loadNodeContent('path1-node1');

// Load entire path
const path = await loadPathContent('path1');
```

## Content Updates

When updating content:
1. Update the JSON file
2. Update navigation if structure changed
3. Update metadata if needed
4. Test content loading
5. Verify all references work

