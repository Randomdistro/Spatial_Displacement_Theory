# SDT 3D Particle CMB Model

A 3D calculative model for proton, neutron, electron, neutrino, and spation with CMB EM shunt kinetics (pressure-density mechanics). Configurable directional CMB (12-direction icosahedral up to finer resolution) and toggleable SDT arrangements (6π trefoils, helical vortices, pairing).

**Isotope coverage:** Every isotope from hydrogen (Z=1) through tin (Z=50) — 1788+ isotopes.

## Design

- **CMB directional**: 12 (icosahedral), 20 (dodecahedral), 42, or Fibonacci resolutions
- **Pressure**: Solid angle Ω(r), far-field O(r) = R²/(4r²), Core Engine Ḋ = P_CMB A_eff Γ κ (1-η)
- **Particles**: Proton (trefoil), neutron (p+e), electron, neutrino, spation
- **Arrangements**: Trefoil, helical vortex, pairing (L-R chirality) as toggles
- **Nucleus**: Build any (Z, A) from H through Sn with nucleon positions

## Usage

```bash
# From SDT/Code directory
python -m sdt_3d_particle_cmb single --setup proton
python -m sdt_3d_particle_cmb single --setup deuteron
python -m sdt_3d_particle_cmb isotope 6 12          # Carbon-12
python -m sdt_3d_particle_cmb isotope 50 118       # Tin-118 (stable)
python -m sdt_3d_particle_cmb batch --mode toggles
python -m sdt_3d_particle_cmb batch --mode pairing --json
python -m sdt_3d_particle_cmb batch --mode isotopes --element 50  # All tin isotopes
```

## Python API

```python
from sdt_3d_particle_cmb import Simulation, ArrangementConfig, run_batch, setup_deuteron
from sdt_3d_particle_cmb import get_isotope, get_isotopes_for_element, build_nucleus
import numpy as np

# Single nucleus
sim = Simulation(cmb_resolution="12")
sim.add_nucleus(6, 12)  # Carbon-12
result = sim.run()

# All isotopes for an element
from sdt_3d_particle_cmb.batch_runner import run_all_isotopes_element
results = run_all_isotopes_element(50)  # All tin isotopes

# Isotope database
from sdt_3d_particle_cmb.isotopes import get_isotopes_for_element, isotope_count
isotopes = get_isotopes_for_element(26)  # Iron
print(isotope_count())  # 1788
```

## Batch testing

```python
from sdt_3d_particle_cmb.batch_runner import (
    make_arrangement_grid,
    run_batch,
    setup_single_proton,
    setup_deuteron,
)

configs = make_arrangement_grid()  # All 16 toggle combinations
results = run_batch(configs, setup_single_proton, cmb_resolution="12")
```

## Sources

- SDT_CORE_AXIOMS_AND_DATASET.md
- Core_Engine_Mathematical_Proof.md
- Part I Axioms and Core Equations
- Investigation_Structural_Alignments_and_Pairing.md
