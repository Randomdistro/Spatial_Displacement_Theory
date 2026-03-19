# sdt_navier — Overview

Python implementation of the SDT Navier field equations. Covers lattice construction, field equation solving, nuclear binding energy calculations, and magnetic moment predictions.

## Subfolders

- **tests/** — Unit tests for the Python Navier implementation

## Files

- **__init__.py** — Package initialisation and public API exports
- **equations.py** — ✅ SDT Navier field equation implementations: pressure gradient, vorticity, continuity
- **fields.py** — ✅ Field type definitions and TurbineCell models
- **lattice.py** — ✅ Lattice construction for numerical simulations
- **solver.py** — ✅ Iterative solver for field convergence
- **nuclear.py** — ✅ Nuclear binding calculations: deuteron, triton, helion, alpha
- **magnetic_moments.py** — ✅ Magnetic moment prediction from vortex circulation parameters
- **MAGNETIC_MOMENTS_UPDATE.md** — Documentation of magnetic moment calculation updates
- **VALIDATOR_FIXES.md** — Documentation of validator bug fixes
