# Design System: SDT Visual Language

**Created by:** Creative Agent  
**Philosophy:** Subtle, subdued, visceral. The obviousness of it all, effortlessly revealed.

---

## Core Aesthetic Principles

### 1. **Geometry Sings**
Every shape, every curve, every intersection has meaning. The Flower of Life isn't decoration—it's the structure of understanding itself.

### 2. **Subtle, Not Shy**
The beauty is in the restraint. Deep blues that whisper, not shout. Gold that glimmers, not blares. The theory reveals itself through elegance, not force.

### 3. **Visceral Understanding**
Users should *feel* the pressure gradients, *sense* the flow of spation, *experience* the displacement. This isn't just visualization—it's embodiment.

### 4. **The Obviousness**
When it's right, it's obvious. The design should make SDT feel inevitable, not revolutionary. Like discovering something that was always there.

---

## Color Palette

### Primary Colors

**Deep Space Blue**
- Base: `#1a365d` (RGB: 26, 54, 93)
- Use: Primary 3D elements, background depth
- Meaning: The spation medium itself—deep, pressurized, foundational

**Metallic Gold**
- Base: `#d69e2e` (RGB: 214, 158, 46)
- Use: Highlights, active states, directional flow
- Meaning: The pressure gradient—energy, direction, revelation

**Subtle Silver**
- Base: `#cbd5e0` (RGB: 203, 213, 224)
- Use: Secondary elements, text on dark
- Meaning: Matter—defined, hard, precise

### Accent Colors

**Pressure Gradient Blue**
- Gradient: `#1a365d` → `#2d5a87` → `#4299e1`
- Use: Pressure field visualizations
- Meaning: The flow of spation

**Eclipse Shadow**
- Base: `#0f172a` (RGB: 15, 23, 42)
- Use: Deep shadows, occluded areas
- Meaning: Matter exclusion, the "holes" in space

**Revelation Gold**
- Gradient: `#d69e2e` → `#f6ad55` → `#fbbf24`
- Use: Active selections, key insights
- Meaning: Understanding, the "aha" moment

### Neutral Palette

**Text Primary:** `#f7fafc` (near white, but not pure)
**Text Secondary:** `#cbd5e0` (silver)
**Background Deep:** `#0a0e1a` (almost black, but with blue tint)
**Background Surface:** `#1a202c` (dark blue-gray)

---

## Typography

### Primary Font: **Inter** (or similar geometric sans)
- Clean, modern, scientific
- Excellent readability at all sizes
- Geometric but human

### Display Font: **Space Grotesk** (or similar)
- For headings, formulas in display mode
- Slightly more character, still precise

### Monospace: **JetBrains Mono**
- For code, formulas, technical content
- Clear distinction between text and math

### Hierarchy

```
H1: 3.5rem (56px) - Landing page, major sections
H2: 2.5rem (40px) - Section headers
H3: 1.875rem (30px) - Subsection headers
H4: 1.5rem (24px) - Node titles
Body: 1.125rem (18px) - Main content
Small: 0.875rem (14px) - Captions, metadata
```

---

## 3D Design Language

### Flower of Life Geometry

**Ring Specifications:**
- **Material:** PBR (Physically Based Rendering)
  - Metallic: 0.8 (subtle metal, not chrome)
  - Roughness: 0.2 (smooth but not mirror)
  - Emissive: 0.1 intensity (gentle glow, not neon)
  - Base color: Deep Space Blue with gold gradient on active

**Ring Structure:**
- Thickness: 0.02 units (relative to scene)
- Segments: 64 (smooth, not faceted)
- Pattern: Sacred geometry Flower of Life
- Interleaving: Rings pass through each other, creating depth

**Animation Philosophy:**
- Slow, organic rotation (0.5 RPM)
- Each ring slightly different speed (0.4-0.6 RPM)
- Creates mesmerizing flow, suggests spation medium
- Hover: Gentle scale (1.1x), increased glow
- Selection: Flip and reveal (180° rotation), not jarring

### Spatial Composition

**Camera Movement:**
- Smooth, orbital motion
- Ease-in-out cubic bezier
- Never jarring, always flowing
- Transitions feel like floating through space

**Node Rooms:**
- Each node is a "chamber" in 3D space
- Subtle boundaries (not walls, more like zones)
- Content floats in space, not pinned to surfaces
- Depth creates hierarchy

**Lighting:**
- Ambient: 0.4 intensity (soft, not harsh)
- Directional: 0.8 intensity from (5, 5, 5)
- Point light: 0.3 intensity at origin (gentle center glow)
- No harsh shadows, everything soft and volumetric

---

## UI Components

### Buttons

**Primary (Path Selection):**
- Background: Transparent with gold border
- Hover: Gold glow, subtle scale
- Active: Gold fill, white text
- Transition: 200ms ease

**Secondary (Expansions):**
- Text link style
- Gold underline on hover
- Subtle, not aggressive

### Cards/Panels

**Content Cards:**
- Background: `rgba(26, 54, 93, 0.6)` (semi-transparent blue)
- Border: 1px gold, subtle glow
- Backdrop blur: 10px (glassmorphism)
- Padding: Generous (2rem)

**Expansion Panels:**
- Slide in from side
- Same glassmorphism style
- Smooth animation (300ms)

### Form Elements

**Inputs:**
- Transparent background
- Gold border (1px)
- Focus: Gold glow
- Placeholder: Muted silver

**Sliders (Simulation Controls):**
- Track: Dark blue
- Thumb: Gold, glows on hover
- Smooth, responsive

---

## Animation Principles

### Timing

**Fast:** 150ms - Micro-interactions, hover states
**Medium:** 300ms - Panel transitions, expansions
**Slow:** 1000ms+ - Camera movements, major transitions

### Easing

**Default:** `cubic-bezier(0.4, 0, 0.2, 1)` - Smooth, natural
**Ease-out:** `cubic-bezier(0, 0, 0.2, 1)` - Decelerating
**Ease-in:** `cubic-bezier(0.4, 0, 1, 1)` - Accelerating
**Organic:** `cubic-bezier(0.34, 1.56, 0.64, 1)` - Slight bounce, playful

### Principles

1. **Everything flows** - No sudden stops
2. **Respect physics** - Ease in/out, momentum
3. **Subtle motion** - Draw attention, don't distract
4. **Purposeful** - Every animation has meaning

---

## Visual Metaphors

### Pressure Field
- **Visual:** Gradient from deep blue to lighter blue
- **Motion:** Flowing, like water or air
- **Density:** More opaque = higher pressure
- **Direction:** Gold arrows or flow lines

### Matter Exclusion
- **Visual:** Dark voids in the pressure field
- **Edge:** Gold outline (the boundary)
- **Shape:** Hard, defined, geometric
- **Interaction:** Pressure flows around it

### Flow Direction
- **Visual:** Gold gradient along paths
- **Motion:** Particles or lines flowing
- **Speed:** Faster = brighter gold
- **Purpose:** Show where pressure is going

### Understanding/Revelation
- **Visual:** Gold glow expanding
- **Motion:** Gentle pulse, not flash
- **Timing:** Slow, contemplative
- **Feeling:** "Aha" moment, not shock

---

## Responsive Design

### Breakpoints

**Mobile:** 375px - 767px
- Simplified 3D (fewer rings)
- Touch-friendly controls
- Larger tap targets
- Simplified animations

**Tablet:** 768px - 1023px
- Medium complexity 3D
- Hybrid touch/mouse
- Optimized layout

**Desktop:** 1024px+
- Full 3D experience
- All animations
- Precise mouse control
- Maximum detail

### Mobile Considerations

- Reduce ring count (7 instead of 19)
- Simplify materials (fewer textures)
- Lower polygon count
- Touch gestures for camera
- Larger UI elements

---

## Accessibility

### Color Contrast
- Text on background: WCAG AA minimum
- Interactive elements: Clear focus states
- Gold on blue: Tested for visibility

### Motion
- Respect `prefers-reduced-motion`
- Provide pause/play for animations
- Allow users to control animation speed

### Focus States
- Clear gold outline on focus
- Keyboard navigation always possible
- Screen reader friendly

---

## Design Tokens

```css
/* Colors */
--color-space-deep: #1a365d;
--color-gold-primary: #d69e2e;
--color-silver: #cbd5e0;
--color-eclipse: #0f172a;

/* Spacing */
--space-xs: 0.5rem;
--space-sm: 1rem;
--space-md: 2rem;
--space-lg: 4rem;
--space-xl: 8rem;

/* Timing */
--timing-fast: 150ms;
--timing-medium: 300ms;
--timing-slow: 1000ms;

/* Easing */
--ease-default: cubic-bezier(0.4, 0, 0.2, 1);
--ease-organic: cubic-bezier(0.34, 1.56, 0.64, 1);

/* Shadows */
--shadow-subtle: 0 2px 8px rgba(0, 0, 0, 0.3);
--shadow-glow: 0 0 20px rgba(214, 158, 46, 0.3);
```

---

## The Obviousness Test

Before finalizing any design decision, ask:

1. **Does it feel inevitable?** (Not forced)
2. **Does geometry sing?** (Not just functional)
3. **Is it subtle?** (Not garish)
4. **Does it reveal?** (Not obscure)
5. **Is it visceral?** (Can you feel it?)

If the answer to all is yes, it's right.

---

**Remember:** We're not decorating SDT. We're revealing it. The design should make the theory feel obvious, beautiful, and true.

