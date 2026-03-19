# sdt_orbital_sim/src — Overview

Implementations for the orbital simulation module.

## Subfolders

- **io/** — Output writers for simulation data
- **visualization/** — Visualisation utilities for orbital trajectories

## Files

- **galaxy_sim.cpp** — 🟡 Galaxy rotation curve simulator using SDT pressure fields with screening. Contains "Newtonian" framing in comments
- **simulation_engine.cpp** — ✅ Core simulation loop: time stepping, state updates, conservation tracking
