# Quarantine Reason: sdt_atomic_sim QM Framework

**Moved**: 2026-03-23
**Files Quarantined**:
- `include/sdt/physics/electron_orbitals.hpp` — Wave functions, probability densities, Laguerre polynomials
- `include/sdt/physics/spectral_transitions.hpp` — QM spectral line framework
- `include/sdt/simulation/atomic_engine.hpp` — QM-based simulation engine
- `include/sdt/visualization/orbital_viewer.hpp` — VTK-based probability cloud renderer
- `include/sdt/io/atomic_data_loader.hpp` — Data loader for QM states
- `include/sdt/core/constants.hpp` — M_E/M_P as bare input constants
- `include/sdt/core/types.hpp` — QuantumNumbers struct, Vec3d from Eigen
- `src/physics/electron_orbitals.cpp` — Full QM radial wavefunctions
- `src/physics/spectral_transitions.cpp` — QM transition calculations
- `src/simulation/atomic_engine.cpp` — QM simulation loop
- `src/visualization/orbital_viewer.cpp` — VTK probability cloud render
- `src/io/atomic_data_loader.cpp` — QM state I/O

**SDT Rules Violated**: R2 (mass as input), R5 (wave functions), R11 (quantum numbers as fundamental)

**Replacement**: New `main.cpp` with self-contained `PressureNodeAtom` class.
Electrons are toroidal vortices at pressure-node minima.
Uses admittance profiles instead of probability densities.
Uses shell indices instead of quantum numbers.
