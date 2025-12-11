# SDT Website

Official website for Spatial Displacement Theory.

## Quick Start

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

## Tech Stack

- **Framework:** [Astro](https://astro.build/) - Fast, content-focused static site generator
- **Styling:** [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- **Interactive Components:** [React](https://react.dev/) - For calculators and dynamic UI
- **Math Rendering:** [KaTeX](https://katex.org/) - Fast LaTeX math rendering
- **3D Visualizations:** [Three.js](https://threejs.org/) - WebGL-based 3D graphics

## Project Structure

```
website/
├── src/
│   ├── pages/              # Astro pages (file-based routing)
│   │   ├── index.astro     # Landing page
│   │   ├── theory/         # Theory documentation
│   │   ├── papers/         # Paper library
│   │   ├── tools/          # Interactive calculators
│   │   ├── atomicus/       # Element library
│   │   ├── code/           # Software documentation
│   │   └── about/          # About pages
│   ├── layouts/            # Page layouts
│   │   └── BaseLayout.astro
│   ├── components/         # Reusable components
│   │   └── OrbitalCalculator.tsx
│   ├── styles/             # Global styles
│   │   └── global.css
│   └── content/            # Markdown content (future)
├── public/                 # Static assets
│   └── images/
├── package.json
├── astro.config.mjs
└── tailwind.config.mjs
```

## Development

### Adding New Pages

Create a new `.astro` file in `src/pages/`. The file path becomes the URL:

- `src/pages/foo.astro` → `/foo`
- `src/pages/theory/overview.astro` → `/theory/overview`

### Adding Interactive Components

Create React components in `src/components/` and use them in Astro pages:

```astro
---
import MyComponent from '../components/MyComponent';
---

<MyComponent client:load />
```

The `client:load` directive enables client-side hydration.

### Styling

We use Tailwind CSS with a custom design system defined in `tailwind.config.mjs`. Key custom classes:

- `.btn-primary`, `.btn-secondary`, `.btn-gold` - Buttons
- `.card` - Card components
- `.badge-certified`, `.badge-investigation` - Status badges
- `.equation` - Math equation blocks
- `.nav-link` - Navigation links

### Math Rendering

Use HTML entities or KaTeX in your pages:

```html
<!-- HTML entities -->
<p>&nabla; &middot; F = 0</p>

<!-- KaTeX (requires script setup) -->
<div class="katex">$\nabla \cdot F = 0$</div>
```

## Content Migration

Content is sourced from the main SDT repository:

| Source | Destination |
|--------|-------------|
| `SDT/Papers/SDT_Foundation/` | `/theory/` |
| `SDT/Papers/SDT_Foundation/De_Rerum_Todo_Existens/` | `/papers/de-rerum` |
| `SDT/benchmarks/` | `/papers/benchmarks/` |
| `SDT/ATOMICUS/` | `/atomicus/` |
| `SDT/Code/` | `/code/` |

## Deployment

### Vercel (Recommended)

1. Connect your GitHub repository to Vercel
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Deploy!

### GitHub Pages

```bash
# Build
npm run build

# The dist/ folder can be deployed to GitHub Pages
```

### Manual

```bash
npm run build
# Upload dist/ folder to any static host
```

## Environment Variables

None required for basic operation.

Optional:
- `PUBLIC_SITE_URL` - Override site URL for SEO

## Contributing

1. Create a feature branch
2. Make your changes
3. Test with `npm run dev`
4. Build with `npm run build` to check for errors
5. Submit a pull request

## License

MIT License - Same as main SDT repository

## Links

- [Main SDT Repository](https://github.com/username/SDT)
- [Website Plan](../WEBSITE_PLAN.md)
- [Contact](mailto:spatialdisplacementtheory@gmail.com)
