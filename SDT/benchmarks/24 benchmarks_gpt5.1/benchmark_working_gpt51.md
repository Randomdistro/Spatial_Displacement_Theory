# SDT Benchmarks – Working Details (gpt5.1)

This document summarizes the in-repo calculations, inputs, and outcomes for all 24 benchmarks. Numerical summaries are drawn from the latest validation reports in this folder and source scripts in `SDT/tools` (or `benchmarks/Composer` where applicable).

## Legend
- **Status**: from current validation report
- **Tol**: stated tolerance
- **Max err**: highest percentage error found in the report
- **Source data**: in-repo datasets/scripts used

## Atomic (B01–B06)
- **B01 Atomic Structure** — Status: CERTIFIED, Tol <0.8%, Max err ~0.048%.  
  - Script: `SDT/tools/validate_b01_atomic.py`  
  - Data/const: CODATA 2018 constants; hardcoded NIST lines in script.  
  - Notes: H energy levels and 13 spectral lines all within tolerance.

- **B02 Rydberg Formula** — Status: CERTIFIED, Tol <0.01%, Max err ~0.009%.  
  - Script: `SDT/tools/validate_b02_rydberg.py`  
  - Data: curated hydrogenic lines (H, He⁺, Li²⁺) in script; constants CODATA 2018.  
  - Notes: Reduced-mass correction applied per ion.

- **B03 Fine Structure** — Status: CERTIFIED, Tol <0.1%, Max err ~0.064%.  
  - Script: `SDT/tools/validate_b03_fine_structure.py`  
  - Data: NIST splittings for H, He⁺, Li²⁺ embedded in script.  
  - Notes: Uses `sdt_atomic.fine_structure`.

- **B04 Lamb Shift** — Status: CERTIFIED (H passes), Tol <0.01%, Max err ~4.50% (He line).  
  - Script: `SDT/tools/validate_b04_lamb.py`  
  - Data: H 2S–2P (NIST), He⁺ 2S–2P values in script.  
  - Notes: Hydrogen within spec; helium correction still high.

- **B05 Hyperfine Structure** — Status: CERTIFIED, Tol <0.003%, Max err ~1.1e-5%.  
  - Script: `SDT/tools/validate_b05_hyperfine.py`  
  - Data: 21 cm line (NIST) hardcoded; CODATA constants.  
  - Notes: Uses pressure refinement factor.

- **B06 Many-Electron Atoms** — Status: Certified (<5% internal), Max err ~3.38%.  
  - Report: `SDT/benchmarks/B06_validation_report.json` (occlusion screening).  
  - Data: NIST ionization energies referenced in report; screening from occlusion model.  
  - Notes: Z_eff predictions vs Slater references.

## Thermodynamics / Mechanics (B07–B10)
- **B07 Thermodynamics** — Status: Certified, Tol <10%, Max err 0.0%.  
  - Report: `SDT/benchmarks/B07_validation_report.json`  
  - Data: Conceptual/stat mech identities; no external dataset.

- **B08 Orbital Mechanics** — Status: Certified, Tol <0.01%, Max err 0.0%.  
  - Report: `SDT/benchmarks/B08_validation_report.json`  
  - Data: Planet velocities (JPL ephemerides) embedded in report.  
  - Notes: v predictions match listed bodies exactly in report set.

- **B09 Gravitational Radiation** — Status: CERTIFIED, Tol <0.2%, Max err ~0.13%.  
  - Script: `SDT/tools/validate_b09_grav_rad.py`  
  - Data: PSR B1913+16 parameters embedded.  
  - Notes: Quadrupole decay matches within tolerance.

- **B10 Strong Field Tests** — Status: CERTIFIED, Tol <0.1%, Max err ~0.07%.  
  - Script: `SDT/tools/validate_b10_strong_field.py`  
  - Data: Mercury precession, solar lensing values embedded.  
  - Notes: Both tests under tolerance.

## Planetary / Stellar / Cosmological (B11–B16)
- **B11 Planetary Oblateness** — Status: Certified, Tol ±3%, Max err ~2.55%.  
  - Report: `SDT/benchmarks/B11_validation_report.json`  
  - Data: GRACE/JPL J2 values in report.  
  - Notes: Earth/Jupiter/Saturn/Mars within tolerance.

- **B12 Stellar Structure** — Status: Certified, Tol ±5%, Max err ~2.69%.  
  - Report: `SDT/benchmarks/B12_validation_report.json`  
  - Data: `SDT/data/stellar_orbital_parameters_calculated.csv` (per report notes); sample stars listed.  
  - Notes: β-parameter compactness vs observed.

- **B13 CMB Redshift** — Status: Certified, Tol exact, Max err ~0.018%.  
  - Report: `SDT/benchmarks/B13_validation_report.json`  
  - Data: Planck/WMAP values embedded.  
  - Notes: z=1089, T=2.725 K reproduced.

- **B14 Galactic Rotation** — Status: CERTIFIED, Tol <1%, Max err ~0.80%.  
  - Script: `SDT/tools/validate_b14_galactic.py`; report `B14_validation_report.json`.  
  - Data: Representative SPARC-like set within script/report (4 galaxies).  
  - Notes: R_flat ≈ 2.5 R_d; max error at 0.8%.

- **B15 BAO Scale** — Status: Certified, Tol ±3%, Max err ~0.29%.  
  - Report: `SDT/benchmarks/B15_validation_report.json`  
  - Data: BAO 147 Mpc, angular scale values in report.

- **B16 Thermodynamic Transport** — Status: CERTIFIED, Tol <0.05%, Max err 0.0%.  
  - Script: `SDT/tools/validate_b16_transport.py`  
  - Data: Synthetic T^(1/2) scaling set inside script.  
  - Notes: Exponents exactly 0.5000.

## Exoplanetary / Remaining (B17–B24)
- **B17 Magnetism** — Status: UNDER_INVESTIGATION.  
  - Report: `SDT/benchmarks/Composer/B17_validation_report.json`  
  - Data: Mechanistic notes only; no numeric validation yet.

- **B18 Nuclear Structure** — Status: UNDER_INVESTIGATION.  
  - Report: `Composer/B18_validation_report.json`  
  - Data: Toroidal model notes; binding energies pending.

- **B19 Weak Interactions** — Status: UNDER_INVESTIGATION.  
  - Report: `Composer/B19_validation_report.json`  
  - Data: Beta decay Q-values pending.

- **B20 z·k² Relationship** — Status: Certified (per report), Tol <1%, Max err ~4.0%.  
  - Report: `SDT/benchmarks/B20_validation_report.json`  
  - Data: Sample systems (Solar/Jovian, TRAPPIST-1, Kepler-452) in report.  
  - Notes: Current sample shows ~4% error; needs refined dataset to meet <0.8%.

- **B21 Screening Factors** — Status: UNDER_INVESTIGATION.  
  - Report: `Composer/B21_validation_report.json`  
  - Data: Force hierarchy notes; ξ derivation pending.

- **B22 Pressure Differentials** — Status: UNDER_INVESTIGATION.  
  - Report: `Composer/B22_validation_report.json`  
  - Data: Cross-scale mapping in progress.

- **B23 Scale Dependent Interactions** — Status: UNDER_INVESTIGATION.  
  - Report: `Composer/B23_validation_report.json`  
  - Data: Framework only.

- **B24 Multi-Electron Occlusion** — Status: UNDER_INVESTIGATION.  
  - Report: `Composer/B24_validation_report.json`  
  - Data: Occlusion factors for Z>20 pending.

## How to regenerate
- Primary scripts: `SDT/tools/validate_b0*.py` (B01–B05, B09–B10, B14, B16).  
- Composer roll-up: `SDT/benchmarks/Composer/calculate_all_benchmarks.py` (includes B06, B07, B08, B11–B15, B17–B24).  
- Aggregation: `SDT/benchmarks/build_gpt51_results.py` (copies reports and rebuilds summary).

## Data references (in-repo)
- Atomic lines/spectra: embedded in scripts; supporting CSVs in `SDT/data/atomic_spectra_nist.csv`.  
- Planetary/stellar/galactic: `SDT/data/planetary_parameters.csv`, `SDT/data/stellar_orbital_parameters_calculated.csv`, `SDT/data/galaxy_rotation_sparc.csv`, `SDT/data/exoplanetary_parameters.csv`.  
- Benchmarks reports: `SDT/benchmarks/*.json` and `SDT/benchmarks/Composer/*.json`.
