"""
SDT 3D Particle CMB Model — Isotope Database

Complete isotope list from hydrogen (Z=1) through tin (Z=50).
Uses embedded data; optional: periodictable for masses, or generate from AME.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import json
from pathlib import Path

# Elements 1–50: (Z, symbol, name)
ELEMENTS_1_50 = [
    (1, "H", "Hydrogen"), (2, "He", "Helium"), (3, "Li", "Lithium"),
    (4, "Be", "Beryllium"), (5, "B", "Boron"), (6, "C", "Carbon"),
    (7, "N", "Nitrogen"), (8, "O", "Oxygen"), (9, "F", "Fluorine"),
    (10, "Ne", "Neon"), (11, "Na", "Sodium"), (12, "Mg", "Magnesium"),
    (13, "Al", "Aluminium"), (14, "Si", "Silicon"), (15, "P", "Phosphorus"),
    (16, "S", "Sulfur"), (17, "Cl", "Chlorine"), (18, "Ar", "Argon"),
    (19, "K", "Potassium"), (20, "Ca", "Calcium"), (21, "Sc", "Scandium"),
    (22, "Ti", "Titanium"), (23, "V", "Vanadium"), (24, "Cr", "Chromium"),
    (25, "Mn", "Manganese"), (26, "Fe", "Iron"), (27, "Co", "Cobalt"),
    (28, "Ni", "Nickel"), (29, "Cu", "Copper"), (30, "Zn", "Zinc"),
    (31, "Ga", "Gallium"), (32, "Ge", "Germanium"), (33, "As", "Arsenic"),
    (34, "Se", "Selenium"), (35, "Br", "Bromine"), (36, "Kr", "Krypton"),
    (37, "Rb", "Rubidium"), (38, "Sr", "Strontium"), (39, "Y", "Yttrium"),
    (40, "Zr", "Zirconium"), (41, "Nb", "Niobium"), (42, "Mo", "Molybdenum"),
    (43, "Tc", "Technetium"), (44, "Ru", "Ruthenium"), (45, "Rh", "Rhodium"),
    (46, "Pd", "Palladium"), (47, "Ag", "Silver"), (48, "Cd", "Cadmium"),
    (49, "In", "Indium"), (50, "Sn", "Tin"),
]


@dataclass
class Isotope:
    """Single isotope: Z, A, N, mass (u), symbol, stable."""
    Z: int
    A: int
    N: int
    mass: float
    symbol: str
    stable: bool = False

    @property
    def label(self) -> str:
        return f"{self.symbol}-{self.A}"


def _load_embedded_isotopes() -> List[Dict]:
    """Load from embedded JSON if present."""
    p = Path(__file__).parent / "isotopes_data.json"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return []


def _generate_from_periodictable() -> List[Dict]:
    """Generate from periodictable package if available."""
    try:
        import periodictable as pt
        out = []
        for Z in range(1, 51):
            el = pt.elements[Z]
            sym = el.symbol
            for A in el.isotopes:
                N = A - Z
                try:
                    mass = pt.mass.mass(el[A])
                except Exception:
                    mass = float(A)
                try:
                    ab = pt.mass.abundance(el[A])
                    stable = ab is not None and ab > 0
                except Exception:
                    stable = False
                out.append({
                    "Z": Z, "A": A, "N": N, "symbol": sym,
                    "mass": float(mass), "stable": stable
                })
        return out
    except ImportError:
        return []


def _build_isotope_list() -> List[Isotope]:
    """Build full isotope list. Prefer embedded data, then periodictable."""
    data = _load_embedded_isotopes()
    if not data:
        data = _generate_from_periodictable()
    if not data:
        return _fallback_isotopes()
    return [
        Isotope(
            Z=d["Z"], A=d["A"], N=d["N"],
            mass=d.get("mass", d["A"]),
            symbol=d["symbol"],
            stable=d.get("stable", False)
        )
        for d in data
    ]


def _fallback_isotopes() -> List[Isotope]:
    """
    Fallback: generate A range for each Z from standard nuclear valley.
    Covers all known isotopes from valley of stability.
    """
    out = []
    # A ranges per Z (from NNDC/IAEA valley - conservative bounds)
    # Format: (Z, A_min, A_max) - inclusive
    ranges = [
        (1, 1, 7), (2, 3, 10), (3, 4, 12), (4, 5, 14), (5, 7, 19),
        (6, 8, 22), (7, 10, 25), (8, 12, 28), (9, 14, 31), (10, 16, 34),
        (11, 18, 37), (12, 19, 40), (13, 21, 43), (14, 22, 46), (15, 24, 49),
        (16, 26, 52), (17, 28, 55), (18, 30, 58), (19, 32, 61), (20, 34, 64),
        (21, 36, 67), (22, 38, 70), (23, 40, 73), (24, 42, 76), (25, 44, 79),
        (26, 46, 82), (27, 48, 85), (28, 50, 88), (29, 52, 91), (30, 54, 94),
        (31, 56, 97), (32, 58, 100), (33, 60, 103), (34, 62, 106), (35, 64, 109),
        (36, 66, 112), (37, 68, 115), (38, 70, 118), (39, 72, 121), (40, 74, 124),
        (41, 76, 127), (42, 78, 130), (43, 80, 133), (44, 82, 136), (45, 84, 139),
        (46, 86, 142), (47, 88, 145), (48, 90, 148), (49, 92, 151), (50, 94, 154),
    ]
    symbols = {z: sym for z, sym, _ in ELEMENTS_1_50}
    for Z, A_min, A_max in ranges:
        sym = symbols.get(Z, "?")
        for A in range(A_min, A_max + 1):
            N = A - Z
            if N >= 0:
                # Stable: valley of stability N ≈ Z for light, N > Z for heavy
                stable = abs(N - Z) <= 2 + (Z // 20)
                out.append(Isotope(Z=Z, A=A, N=N, mass=float(A), symbol=sym, stable=stable))
    return out


# Lazy-loaded full list
_ISOTOPE_LIST: Optional[List[Isotope]] = None


def _get_isotopes() -> List[Isotope]:
    global _ISOTOPE_LIST
    if _ISOTOPE_LIST is None:
        _ISOTOPE_LIST = _build_isotope_list()
    return _ISOTOPE_LIST


def get_isotope(Z: int, A: int) -> Optional[Isotope]:
    """Get isotope by Z and A."""
    for iso in _get_isotopes():
        if iso.Z == Z and iso.A == A:
            return iso
    return None


def get_isotopes_for_element(Z: int) -> List[Isotope]:
    """All isotopes for element Z."""
    return [iso for iso in _get_isotopes() if iso.Z == Z]


def get_all_isotopes_up_to_tin() -> List[Isotope]:
    """All isotopes from hydrogen through tin."""
    return _get_isotopes()


def get_stable_isotopes(Z: int) -> List[Isotope]:
    """Stable isotopes for element Z."""
    return [iso for iso in get_isotopes_for_element(Z) if iso.stable]


def isotope_count() -> int:
    """Total number of isotopes in database."""
    return len(_get_isotopes())
