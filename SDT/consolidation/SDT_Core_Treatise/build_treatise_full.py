#!/usr/bin/env python3
"""
Build SDT_Core_Treatise_Full.md: single consolidated treatise with TOC, cross-refs, and index.
Then optionally generate PDF if pandoc or md-to-pdf is available.
"""
import re
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "SDT_Core_Treatise_Full.md"
OUT_PDF = BASE / "SDT_Core_Treatise_Full.pdf"

# Chapter order: (file_stem, title). Use None for placeholder.
CHAPTERS = [
    ("Chapter_01", "Introduction, Primitives, and Notation"),
    ("Chapter_02", "Geometry and the Occlusion Foundation"),
    ("Chapter_03", "Master Orbital Equation and Velocity Field"),
    ("Chapter_04", "Redshift–Displacement Identity and Scaling"),
    (None, "Trefoil Topology and Proton Structure"),  # 05
    ("Chapter_06", "Hydrogen System and Atomic Benchmarks"),
    ("Chapter_07", "Solar and Stellar Systems"),
    ("Chapter_08", "Ten Rules and Paradox Resolution"),
    (None, "Classical Tests of Gravitation"),  # 09
    ("Chapter_10", "Nuclear Structure and Binding"),
    ("Chapter_11", "Cosmology and CMB"),
    ("Chapter_12", "Benchmark Suite and Certification"),
    (None, "Standout Formulas Compendium"),  # 13
    ("Chapter_15", "Galactic Systems and Flat Rotation Curves"),
    ("Chapter_16", "References, Constants, and Symbol Index"),
]

def anchor(s):
    """Simple anchor from title."""
    return re.sub(r"[^\w\s-]", "", s).strip().lower().replace(" ", "-")

def bump_headings(text):
    """Increase markdown heading level by 1 (add one #)."""
    lines = []
    for line in text.splitlines():
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            depth, rest = m.group(1), m.group(2)
            lines.append("#" + depth + " " + rest)
        else:
            lines.append(line)
    return "\n".join(lines)

def strip_first_heading(text):
    """Remove the first line if it's # Chapter N: Title."""
    lines = text.strip().splitlines()
    if lines and re.match(r"^#\s+Chapter\s+\d+:", lines[0], re.I):
        return "\n".join(lines[1:]).strip()
    return text.strip()

def main():
    parts = []

    # ---- Front matter ----
    parts.append("""# Spatial Displacement Theory: Core Axioms, Benchmarks, and Formulas

**Primary source:** *SDT Core Axioms & Mathematical Dataset* (Parts I–III).  
**Supporting sources:** *09_CANONICAL_SDT_FORMULAS.md*, *05_STRUCTURE_MAP.md*, *08_CONSISTENCY_REPORT.md*, treatise sections in *conversation.md*.

---
""")

    # ---- Table of contents ----
    ch_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16]
    toc = ["## Table of contents\n"]
    for i, (stem, title) in enumerate(CHAPTERS):
        ch_num = ch_nums[i]
        a = anchor(title)
        toc.append(f"- [**Chapter {ch_num}:** {title}](#{a})")
    parts.append("\n".join(toc) + "\n\n---\n\n")

    # ---- Chapters ----
    for i, (stem, title) in enumerate(CHAPTERS):
        ch_num = ch_nums[i]
        parts.append(f"\n\n## Chapter {ch_num}: {title}\n\n")
        if stem is None:
            parts.append("*[This chapter is not yet written.]*\n\n")
            continue
        path = BASE / f"{stem}.md"
        if not path.exists():
            parts.append("*[Chapter file not found.]*\n\n")
            continue
        raw = path.read_text(encoding="utf-8")
        body = strip_first_heading(raw)
        body = bump_headings(body)
        parts.append(body)
        parts.append("\n\n")

    # ---- Index ----
    parts.append("""
---
## Index

### Formulas (F1–F17)
| ID | Statement | Chapter |
|----|--------|--------|
| F1 | v² = c² R_c/r; v(r) = (c/k)√(R_phys/r) | 3 |
| F2 | z · k² = 1 | 4 |
| F3 | k = c/v_surface; k_solar = k_proton² | 4 |
| F4 | Trefoil: k_p² = 5 α⁻¹; κ ≈ 0.694 | 5 |
| F5 | Deuteron E_bind ≈ 3 k_e e²/D (p-p-e) | 10 |
| F6 | Pressure hierarchy P_∞, P_conf, ρ_s | 10 |
| F7 | 48 Gyr; z_boundary ≈ 1090 | 11 |
| F8 | v_rot = π v_orb²/c | 7 |
| F9 | O(r) = R²/(4r²) | 2 |
| F10 | a(r) = c² R_c/r² | 3 |
| F11 | Nuclear kinetic/confinement κ = 1/√2 | 10 |
| F12 | μ_p = e c R/(2√2) | 5 |
| F13 | Shapiro Δt = (4R/(Ϟ²c)) ln(4r₁r₂/b²) | 9 |
| F14 | Perihelion Δω = 6πR/(Ϟ²a(1−e²)) | 9 |
| F15 | P_spation(r) = ρ_s c² R_uni/r | 11 |
| F16 | v_escape = √2 × c/Ϟ | 3 |
| F17 | Ϟ(r) = √(r/r_c) | 3 |

### Benchmarks
| ID | Short description | Chapter |
|----|-------------------|--------|
| B1 | Geometric foundation O(r)=R²/(4r²) | 2 |
| B2 | Koppa anchor Ϟ_H = 137.036 | 6 |
| B3 | Centripetal force F = m_e v²/a₀ | 6 |
| B4 | Hydrogen spectrum | 6 |
| B5 | Solar Ϟ three routes; z×k² = 1 | 7 |
| B6 | Solar system orbits | 7 |
| B7 | Jovian system | 7 |
| B8 | Exoplanetary validation | 7 |
| B9 | Ten Rules codified | 8 |
| B10 | Paradox resolution | 8 |
| B11 | Classical tests (light deflection, Shapiro, perihelion) | 9 |
| B12 | CMB interpretation | 11 |
| D-01 | Deuteron binding | 10 |
| S-01 | Screening factor ξ | 12 |

### Symbols (quick reference)
- **Ϟ, k** — velocity ratio c/v_surface; at c-boundary Ϟ = 1. **R, R_phys** — physical radius. **R_c, r_c** — c-boundary radius = R_phys/k². **r** — radial distance. **z** — gravitational redshift; z·k² = 1. **κ** — nuclear virial 1/√2 (nuclear first-principles). **Ω, O** — solid angle, occlusion. See Chapter 16 for full symbol index.

### Rules 1–10 (summary)
1. Occlusion O(r)=R²/(4r²). 2. a(r)=c²R/(Ϟ²r²). 3. Ϟ≡c/v_surface. 4. v(r)=(c/Ϟ)√(R/r). 5. v_surface=c/Ϟ. 6. v_escape=√2×c/Ϟ. 7. Three routes to Ϟ (orbital, spectral, rotation). 8. Superposition. 9. r_c=R/Ϟ²; at r_c Ϟ=1. 10. Scale invariance. See Chapter 8 for full list.

---
*Consolidated from SDT Core Treatise chapters. Verification scratch pad: SCRATCH_PAD_VERIFICATION.md.*
""")

    full = "".join(parts)
    OUT.write_text(full, encoding="utf-8")
    print(f"Wrote {OUT} ({len(full)} chars)")

    # ---- PDF ----
    try:
        import subprocess
        # Try pandoc first
        r = subprocess.run(
            ["pandoc", str(OUT), "-o", str(OUT_PDF), "--pdf-engine=xelatex", "-V", "mainfont=Times New Roman"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(BASE),
        )
        if r.returncode == 0:
            print(f"PDF written: {OUT_PDF}")
        else:
            print("Pandoc failed:", r.stderr or r.stdout)
    except FileNotFoundError:
        print("Pandoc not found. To generate PDF: install pandoc and run:")
        print(f"  pandoc \"{OUT}\" -o \"{OUT_PDF}\" --pdf-engine=xelatex")
    except Exception as e:
        print("PDF generation error:", e)

if __name__ == "__main__":
    main()
