import math

def generate_svg(element_data):
    """
    Generates an SVG string for an atomic structure schematic.
    
    element_data: {
        "symbol": "C",
        "Z": 6,
        "N": 6,
        "core_shape": "3-Alpha", # Triangle
        "valence_shape": "Tetrahedron",
        "valence_count": 4,
        "title": "Carbon-12: Tetrahedral-Alpha Alignment"
    }
    """
    
    width = 400
    height = 400
    cx, cy = width / 2, height / 2
    
    svg_parts = []
    svg_parts.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
    
    # Background
    svg_parts.append(f'<rect width="{width}" height="{height}" fill="#1e1e1e" />')
    
    # Styles
    svg_parts.append("""
    <defs>
        <radialGradient id="protonGrad" cx="30%" cy="30%" r="50%">
            <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#b71c1c;stop-opacity:1" />
        </radialGradient>
        <radialGradient id="neutronGrad" cx="30%" cy="30%" r="50%">
            <stop offset="0%" style="stop-color:#4fc3f7;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#0277bd;stop-opacity:1" />
        </radialGradient>
        <radialGradient id="electronGrad" cx="30%" cy="30%" r="50%">
            <stop offset="0%" style="stop-color:#ffd54f;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#ff6f00;stop-opacity:1" />
        </radialGradient>
        <filter id="glow">
            <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    """)

    # Grid Lines (Spation Field)
    svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="140" stroke="#333" stroke-width="1" fill="none" stroke-dasharray="5,5" />') 
    svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="80" stroke="#444" stroke-width="1" fill="none" />')

    # --- Draw Core (Schematic 3-Alpha Triangle) ---
    # 3 Alphas in a triangle. Each Alpha is 2p+2n.
    # Radius of core visualization
    core_r = 40
    # Positions of 3 Alphas
    alpha_pos = []
    for i in range(3):
        angle = math.radians(i * 120 - 90) # Top, Right, Left
        ax = cx + core_r * math.cos(angle)
        ay = cy + core_r * math.sin(angle)
        alpha_pos.append((ax, ay, angle))
        
        # Draw Alpha Cluster (Simplified as 2p 2n tightly packed)
        # Cluster offset
        sr = 8 # nucleon radius
        
        # Protons (Red)
        svg_parts.append(f'<circle cx="{ax-sr}" cy="{ay-sr}" r="{sr}" fill="url(#protonGrad)" stroke="#fff" stroke-width="0.5" />')
        svg_parts.append(f'<circle cx="{ax+sr}" cy="{ay+sr}" r="{sr}" fill="url(#protonGrad)" stroke="#fff" stroke-width="0.5" />')
        
        # Neutrons (Blue with yellow core dot)
        svg_parts.append(f'<circle cx="{ax+sr}" cy="{ay-sr}" r="{sr}" fill="url(#neutronGrad)" stroke="#fff" stroke-width="0.5" />')
        svg_parts.append(f'<circle cx="{ax-sr}" cy="{ay+sr}" r="{sr}" fill="url(#neutronGrad)" stroke="#fff" stroke-width="0.5" />')
        
        # Electron inside Neutron (The "yellow dot")
        svg_parts.append(f'<circle cx="{ax+sr}" cy="{ay-sr}" r="2" fill="#ffd54f" />')
        svg_parts.append(f'<circle cx="{ax-sr}" cy="{ay+sr}" r="2" fill="#ffd54f" />')

    # Neutrino Flux (Green lines connecting Alphas)
    for i in range(3):
        p1 = alpha_pos[i]
        p2 = alpha_pos[(i+1)%3]
        svg_parts.append(f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="#00e676" stroke-width="2" stroke-opacity="0.6" stroke-dasharray="2,2" />')

    # --- Draw Valence Electrons (Tetrahedron -> Projected as Square/Cross or Triangle+Center?) ---
    # Carbon Tetrahedron is 4 equidistant points. 
    # In 2D projection: 3 surrounding, 1 central? Or 4 in a square?
    # Let's do a "Y" projection: 3 at 120 deg, 1 in center/top.
    # Actually, standard tetrahedral projection is 3 base, 1 apex.
    
    valence_r = 140
    
    # 3 Base Electrons
    v_pos = []
    for i in range(3):
        angle = math.radians(i * 120 + 90) # Inverted Y
        vx = cx + valence_r * math.cos(angle)
        vy = cy + valence_r * math.sin(angle)
        v_pos.append((vx, vy))
        
    # 1 Apex Electron (Center, slightly offset to show perspective?)
    v_pos.append((cx, cy)) # Can't be exact center if core is there.
    # Let's shift it. Tetrahedron: angles 109.5.
    # Let's draw 4 corners of a cube (which forms tetrahedron).
    # 2D projection of tetrahedron vertices on sphere:
    # (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)
    
    # Simple Schematic: Square for C? No, C is Tetra.
    # Let's stick to the Y + Center visual, but clarify it.
    # Let's rotate the 3-Alpha core to match the valence?
    # SDT Theory: "Tetrahedral valence aligns with voids in nuclear structure?"
    
    # For visualization, let's place 4 electrons at corners of a standard view.
    # Top-Left, Top-Right (closer), Bottom-Left, Bottom-Right.
    
    coords = [
        (cx - 100, cy - 100), # Top Left
        (cx + 100, cy - 100), # Top Right
        (cx, cy + 120),       # Bottom (Triangle Base?)
        (cx, cy)              # Center? No, 4 points.
    ]
    
    # Tetra vertices on circle
    # 0, 120, 240 is triangle.
    # Let's use the layout: 4 points on a sphere.
    pts = []
    for i in range(4):
        # Tetrahedron vertices: (sqrt(8/9), 0, -1/3), etc.
        # Simple 2D approximation:
        ang = math.radians(i * 90 + 45) # 4 points square arrangement is easiest to read as "4"
        r = 130
        vx = cx + r * math.cos(ang)
        vy = cy + r * math.sin(ang)
        pts.append((vx, vy))

        # Draw correlation line (dashed yellow) from Center to Electron
        svg_parts.append(f'<line x1="{cx}" y1="{cy}" x2="{vx}" y2="{vy}" stroke="#ffd54f" stroke-width="1" stroke-dasharray="4,4" opacity="0.5" />')
        
        # Draw Electron Vortex (Golden Circle)
        svg_parts.append(f'<circle cx="{vx}" cy="{vy}" r="8" fill="url(#electronGrad)" filter="url(#glow)" />')
        svg_parts.append(f'<text x="{vx+12}" y="{vy+4}" fill="#ffd54f" font-family="Arial" font-size="12">e-</text>')

    # Title
    svg_parts.append(f'<text x="20" y="30" fill="#eee" font-family="Arial" font-size="16" font-weight="bold">{element_data["title"]}</text>')
    
    svg_parts.append('</svg>')
    return "\n".join(svg_parts)

data = {
    "symbol": "C",
    "Z": 6,
    "N": 6,
    "title": "Carbon-12: Core-Valence Alignment"
}

svg_content = generate_svg(data)
with open("carbon_structure.svg", "w") as f:
    f.write(svg_content)

print(f"Generated carbon_structure.svg ({len(svg_content)} bytes)")
