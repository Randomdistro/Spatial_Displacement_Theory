#!/usr/bin/env python3
"""
Nuclear shell configuration and simulation for Volume 02 (and core chemistry) nuclei.

For each item: ¹H, ¹²C, ¹⁴N, ¹⁶O this script:
1. Builds the SDT nuclear shell configuration (alpha clusters, proton, geometry).
2. Runs the geometric simulation (occlusion, inter-alpha bonds, packing, radii).
3. Appends a concise report for that nucleus.

Output: printed summary and optional markdown report file.
"""

import sys
import math
import importlib.util
from pathlib import Path
from typing import Dict, List, Any

# Phase_01 local imports
R_NUCLEON_FM = 0.84
DIST_INTER_ALPHA_FM = 2.9

def _import_phase01():
    base = Path(__file__).resolve().parent
    spec_01 = importlib.util.spec_from_file_location(
        "geom_01", base / "01_01_icosahedral_base_geometry.py"
    )
    mod_01 = importlib.util.module_from_spec(spec_01)
    spec_01.loader.exec_module(mod_01)
    spec_02 = importlib.util.spec_from_file_location(
        "geom_02", base / "01_02_first_shell_completion.py"
    )
    mod_02 = importlib.util.module_from_spec(spec_02)
    spec_02.loader.exec_module(mod_02)
    spec_03 = importlib.util.spec_from_file_location(
        "geom_03", base / "01_03_second_layer_structure.py"
    )
    mod_03 = importlib.util.module_from_spec(spec_03)
    spec_03.loader.exec_module(mod_03)
    return mod_01, mod_02, mod_03


def run_1H() -> Dict[str, Any]:
    """Hydrogen-1: single proton. No multi-shell configuration."""
    return {
        "symbol": "¹H",
        "name": "Hydrogen-1",
        "nucleons": 1,
        "protons": 1,
        "neutrons": 0,
        "shell_config": "Single proton (no shells)",
        "shells": [{"shell": 0, "radius_fm": 0.0, "n_positions": 1, "description": "1p"}],
        "building_block": "Fundamental",
        "nuclear_field_strength": "1x",
        "occlusion_sr": 0.0,
        "inter_alpha_bonds": 0,
        "notes": "Baseline; no alpha clusters.",
    }


def run_2H(mod_02) -> Dict[str, Any]:
    """Deuteron: p+n in first octahedral space."""
    FirstShell = mod_02.FirstShell
    base_path = Path(__file__).resolve().parent / "01_01_icosahedral_base_geometry.py"
    spec = importlib.util.spec_from_file_location("base_geom", base_path)
    base_geom = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base_geom)
    base = base_geom.IcosahedralBase(r=R_NUCLEON_FM)
    first_shell = FirstShell(base)
    d = first_shell.deuteron
    occ = d.calculate_occlusion()
    k_infer = d.infer_binding_constant()
    return {
        "symbol": "²H",
        "name": "Deuteron",
        "nucleons": 2,
        "protons": 1,
        "neutrons": 1,
        "shell_config": "First octahedral space (p+n)",
        "shells": [{"shell": 0, "radius_fm": 0.0, "n_positions": 2, "description": "1p+1n"}],
        "building_block": "Deuteron",
        "separation_fm": getattr(d, "separation", 2.10),
        "occlusion_sr": round(occ, 4),
        "inferred_k": round(k_infer, 4) if k_infer else None,
        "notes": "First shell completion; binding 2.224 MeV.",
    }


def run_4He(mod_02) -> Dict[str, Any]:
    """Alpha: both octahedral spaces filled."""
    base_path = Path(__file__).resolve().parent / "01_01_icosahedral_base_geometry.py"
    spec = importlib.util.spec_from_file_location("base_geom", base_path)
    base_geom = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base_geom)
    base = base_geom.IcosahedralBase(r=R_NUCLEON_FM)
    first_shell = mod_02.FirstShell(base)
    alpha = first_shell.alpha
    ver = alpha.verify_alpha_binding()
    return {
        "symbol": "⁴He",
        "name": "Alpha particle",
        "nucleons": 4,
        "protons": 2,
        "neutrons": 2,
        "shell_config": "Both octahedral spaces (2p+2n)",
        "shells": [{"shell": 0, "radius_fm": 0.0, "n_positions": 4, "description": "2p+2n"}],
        "building_block": "Alpha",
        "occlusion_sr": None,
        "binding_MeV_exp": 28.296,
        "binding_error_percent": round(ver.get("error_percent", 0), 2),
        "notes": "Fundamental cluster for ¹²C, ¹⁴N, ¹⁶O.",
    }


def run_12C(mod_03) -> Dict[str, Any]:
    """Carbon-12: 3 alphas in triangular arrangement."""
    c12 = mod_03.Carbon12Arrangement()
    positions = c12.get_alpha_positions()
    n_bonds = c12.calculate_inter_alpha_bonds()
    occ = c12.calculate_inter_alpha_occlusion()
    # Effective radius: max distance from origin to alpha center + alpha effective radius
    max_r = max(math.sqrt(p[0]**2 + p[1]**2 + p[2]**2) for p in positions)
    return {
        "symbol": "¹²C",
        "name": "Carbon-12",
        "nucleons": 12,
        "protons": 6,
        "neutrons": 6,
        "shell_config": "3 alpha particles, triangular arrangement",
        "shells": [
            {"shell": 0, "radius_fm": 0.0, "n_positions": 4, "description": "1 alpha (central)"},
            {"shell": 1, "radius_fm": round(DIST_INTER_ALPHA_FM, 2), "n_positions": 8, "description": "2 alphas (triangle vertices)"},
        ],
        "building_block": "3α",
        "nuclear_field_strength": "12x",
        "inter_alpha_bonds": n_bonds,
        "inter_alpha_occlusion_sr": round(occ, 4),
        "alpha_positions": [tuple(round(x, 3) for x in p) for p in positions],
        "effective_radius_fm": round(max_r + c12.alpha_effective_radius, 3),
        "notes": "Volume 02 baseline; C-C, C-H bonds.",
    }


def run_14N(mod_03) -> Dict[str, Any]:
    """Nitrogen-14: 3 alphas + 1 proton."""
    n14 = mod_03.Nitrogen14Arrangement()
    positions = n14.get_alpha_positions()
    p_extra = n14.get_proton_position()
    n_bonds = n14.calculate_inter_alpha_bonds()
    occ = n14.calculate_inter_alpha_occlusion()
    max_r = max(math.sqrt(p[0]**2 + p[1]**2 + p[2]**2) for p in positions)
    return {
        "symbol": "¹⁴N",
        "name": "Nitrogen-14",
        "nucleons": 14,
        "protons": 7,
        "neutrons": 7,
        "shell_config": "3 alphas (triangle) + 1 proton at triangle center",
        "shells": [
            {"shell": 0, "radius_fm": 0.0, "n_positions": 4, "description": "1 alpha"},
            {"shell": 1, "radius_fm": round(DIST_INTER_ALPHA_FM, 2), "n_positions": 8, "description": "2 alphas"},
            {"shell": "node", "radius_fm": round(math.sqrt(p_extra[0]**2 + p_extra[1]**2 + p_extra[2]**2), 3), "n_positions": 2, "description": "1p+1n (nodal)"},
        ],
        "building_block": "3α + p",
        "nuclear_field_strength": "14x",
        "inter_alpha_bonds": n_bonds,
        "inter_alpha_occlusion_sr": round(occ, 4),
        "extra_proton_position_fm": tuple(round(x, 3) for x in p_extra),
        "effective_radius_fm": round(max_r + n14.alpha_effective_radius, 3),
        "notes": "Volume 02; biological building block.",
    }


def run_16O(mod_03) -> Dict[str, Any]:
    """Oxygen-16: 4 alphas in tetrahedral arrangement."""
    o16 = mod_03.Oxygen16Arrangement()
    positions = o16.get_alpha_positions()
    n_bonds = o16.calculate_inter_alpha_bonds()
    occ = o16.calculate_inter_alpha_occlusion()
    max_r = max(math.sqrt(p[0]**2 + p[1]**2 + p[2]**2) for p in positions)
    return {
        "symbol": "¹⁶O",
        "name": "Oxygen-16",
        "nucleons": 16,
        "protons": 8,
        "neutrons": 8,
        "shell_config": "4 alpha particles, tetrahedral arrangement",
        "shells": [
            {"shell": 0, "radius_fm": 0.0, "n_positions": 4, "description": "1 alpha"},
            {"shell": 1, "radius_fm": round(DIST_INTER_ALPHA_FM, 2), "n_positions": 12, "description": "3 alphas (tetrahedron)"},
        ],
        "building_block": "4α",
        "nuclear_field_strength": "16x",
        "inter_alpha_bonds": n_bonds,
        "inter_alpha_occlusion_sr": round(occ, 4),
        "alpha_positions": [tuple(round(x, 3) for x in p) for p in positions],
        "effective_radius_fm": round(max_r + o16.alpha_effective_radius, 3),
        "notes": "Volume 02; water, oxides.",
    }


def format_report(results: List[Dict[str, Any]]) -> str:
    """Produce markdown report for all nuclei."""
    lines = [
        "# Nuclear Shell Configuration and Simulation Report",
        "",
        "SDT Phase 01: shell configuration and geometric simulation for each nucleus.",
        "",
        "---",
        "",
    ]
    for r in results:
        lines.append(f"## {r['symbol']} — {r['name']}")
        lines.append("")
        lines.append(f"- **Nucleons:** {r['nucleons']} (Z={r['protons']}, N={r.get('neutrons', r['nucleons']-r['protons'])})")
        lines.append(f"- **Shell configuration:** {r['shell_config']}")
        lines.append(f"- **Building block:** {r['building_block']}")
        if r.get("nuclear_field_strength"):
            lines.append(f"- **Nuclear field strength:** {r['nuclear_field_strength']}")
        if r.get("shells"):
            lines.append("- **Shells:**")
            for sh in r["shells"]:
                lines.append(f"  - Shell {sh.get('shell', '?')}: radius {sh.get('radius_fm', '—')} fm, {sh.get('n_positions', '—')} positions — {sh.get('description', '')}")
        if r.get("inter_alpha_bonds") is not None:
            lines.append(f"- **Inter-alpha bonds:** {r['inter_alpha_bonds']}")
        if r.get("inter_alpha_occlusion_sr") is not None:
            lines.append(f"- **Inter-alpha occlusion:** {r['inter_alpha_occlusion_sr']} sr")
        if r.get("occlusion_sr") is not None and "inter_alpha" not in str(r.get("occlusion_sr")):
            lines.append(f"- **Occlusion:** {r['occlusion_sr']} sr")
        if r.get("effective_radius_fm") is not None:
            lines.append(f"- **Effective radius:** {r['effective_radius_fm']} fm")
        if r.get("binding_MeV_exp") is not None:
            lines.append(f"- **Binding (exp):** {r['binding_MeV_exp']} MeV (error {r.get('binding_error_percent', '—')}%)")
        if r.get("notes"):
            lines.append(f"- **Notes:** {r['notes']}")
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def main():
    base = Path(__file__).resolve().parent
    mod_01, mod_02, mod_03 = _import_phase01()
    
    results = []
    
    # 1H
    r1 = run_1H()
    results.append(r1)
    print("[OK] 1H Hydrogen-1:", r1["shell_config"])

    # 2H (deuteron)
    try:
        r2 = run_2H(mod_02)
        results.append(r2)
        print(f"[OK] 2H: occlusion={r2.get('occlusion_sr')} sr, k_infer={r2.get('inferred_k')}")
    except Exception as e:
        print(f"[SKIP] 2H: {e}")

    # 4He
    try:
        r4 = run_4He(mod_02)
        results.append(r4)
        print(f"[OK] 4He: binding error {r4.get('binding_error_percent')}%")
    except Exception as e:
        print(f"[SKIP] 4He: {e}")

    # 12C
    try:
        r12 = run_12C(mod_03)
        results.append(r12)
        print(f"[OK] 12C: bonds={r12['inter_alpha_bonds']}, occlusion={r12['inter_alpha_occlusion_sr']} sr")
    except Exception as e:
        print(f"[SKIP] 12C: {e}")

    # 14N
    try:
        r14 = run_14N(mod_03)
        results.append(r14)
        print(f"[OK] 14N: bonds={r14['inter_alpha_bonds']}, occlusion={r14['inter_alpha_occlusion_sr']} sr")
    except Exception as e:
        print(f"[SKIP] 14N: {e}")

    # 16O
    try:
        r16 = run_16O(mod_03)
        results.append(r16)
        print(f"[OK] 16O: bonds={r16['inter_alpha_bonds']}, occlusion={r16['inter_alpha_occlusion_sr']} sr")
    except Exception as e:
        print(f"[SKIP] 16O: {e}")
    
    # Write report
    report_md = format_report(results)
    out_path = base.parent.parent.parent / "Molecular_Structures" / "NUCLEAR_SHELL_CONFIG_AND_SIMULATION_REPORT.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report_md, encoding="utf-8")
    print(f"\nReport written: {out_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
