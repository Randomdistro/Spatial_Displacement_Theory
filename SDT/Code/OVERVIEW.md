# SDT Code — Overview

Root directory for all Spatial Displacement Theory computational implementations.

## Subfolders

- **sdt_navier_cpp/** — C++20 SDT Navier field equations, nuclear geometry, stellar/galactic/atomic calculators, and 100 certified benchmarks (B01–B100)
- **sdt_navier/** — Python SDT Navier field implementation (equations, lattice, solver, nuclear binding, magnetic moments)
- **sdt_core/** — Python core SDT library (constants, physics, state_28d, orbital examples, zk²=1 tests)
- **sdt_atomic_sim/** — 🔴 C++20 atomic orbital visualisation (currently QM wave-function based — pending quarantine and SDT rewrite)
- **sdt_orbital_sim/** — 🔴 C++20 orbital simulation engine with pressure-field dynamics (contains β and mass_conv contamination)
- **sdt_chemistry/** — C++20 SDT molecular chemistry (bond geometry, element properties, pressure-field bond model)
- **sdt_solar_system/** — C++20 solar system simulation (point particle system, JPL DE421 loader, trajectory viewer)
- **sdt_redshift/** — Python SDT redshift calculator (pressure-gradient displacement model, no expanding universe)
- **sdt_stars/** — Empty placeholder for future stellar structure module
- **sdt_3d_particle_cmb/** — 3D particle CMB pressure visualisation
- **shared/** — Shared C++ headers (include/)
- **dotnet/** — .NET utility (binary output)
- **SDT/** — Documentation, data, and website assets

## Loose Files

- **README.md** — Project-level readme
- **build.bat** — Windows build script
- **calculate_solar_k.py** — 🔴 Derives solar k factor (uses G and M_sun as inputs — needs SDT rewrite)
- **calc_kappa.py** — Calculates κ velocity factors from SDT observables
- **calculate_contraction.py** — Spation contraction factor calculations
- **calculate_precise_contraction.py** — Higher-precision contraction computations
- **calculate_electron_length.py** — Electron characteristic length from SDT
- **calculate_hydrogen_spectrum.py** — Hydrogen spectral lines from Rydberg formula
- **calculate_hydrogen_spectrum_extended.py** — Extended Hydrogen spectrum including fine structure
- **calculate_universal_ratios.py** — Universal ratio relationships in SDT
- **carbon12_electron_parking.py** — Carbon-12 electron parking positions (tetrahedral nuclear geometry)
- **carbon12_electron_parking.png** — Visualisation output from above
- **demo_atomic_calc.cpp** — C++ demo of atomic calculator usage
- **sdt_atomic_properties.hpp** — Standalone atomic properties header (Z_eff, ionisation energies)
- **check_electron_traction.py** — Electron traction force verification
- **check_force_value.py** — Force value cross-check utility
- **check_gamma.py** — Relativistic γ factor verification
- **check_pressure_derivation.py** — Pressure derivation cross-check
- **enrich_atomicus.py** — Enriches atomicus datasheet with SDT properties
- **enrich_atomicus_chemistry.py** — Adds chemistry data to atomicus datasheets
- **enrich_excitations.py** — Adds excitation data to datasheets
- **add_isotope_tables_to_datasheets.py** — Injects isotope tables into element datasheets
- **add_magnetic_properties_to_atomicus.py** — Adds magnetic properties to atomicus
- **add_trefoil_sections_to_atomicus.py** — Adds trefoil vortex sections to element datasheets
- **generate_master_table.py** — Generates master element table from datasheets
- **generate_trefoil_mappings.py** — Generates trefoil winding-mode mappings for all elements
- **generate_trefoil_tables.py** — Generates trefoil configuration tables
- **validate_trefoil_mathematics.py** — Validates trefoil mathematical relationships
- **index_unpaired_electrons.py** — Indexes unpaired electron configurations
- **inject_spectra.py** — Injects spectral data into datasheets
- **parse_atomica.py** — Parses atomica reference data
- **replace_cmb_with_datasheets.py** — Replaces CMB-derived values with datasheet references
- **example_state28d_usage.py** — Example usage of the 28D state vector
- **investigate_*.py** — Various investigation/exploration scripts (18_412, 7_6, 992_scaling, RH_rotation, alpha_rod, c_scaling, cmb_scaling, excitation, neutron_force, overtightened, proton_rotation, spiral, tidal_lock)
- **test_anomaly_hypotheses.py** — 🔴 Tests anomaly hypotheses (contains geodesic/metric tensor references)
- **test_new_pressure.py** — Pressure model test
- **test_torus_model.py** — Torus model verification
- **verify_proton_consistency.py** — Proton parameter consistency checks
- **verify_sdt.py** — General SDT verification script
- **pressure kernel.py** — Pressure kernel computations
- **alpha_tori.html** — Alpha particle torus visualisation
- **pressure_cascade_derivation.html** — Pressure cascade derivation document
- **void_engine.html** — Void engine visualisation
- **kappa_values.txt** — Reference κ values for known bodies
