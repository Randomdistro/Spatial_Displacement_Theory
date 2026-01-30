# SDT Cross-Reference Map (Phases ↔ Benchmarks ↔ Tools ↔ Data)

**Purpose:** Single-page map connecting Phase documents, benchmarks, investigations, tools, and data assets.  
**Last Updated:** January 2026  

---

## Phase → Benchmark → Data

- **Phase 1: Coulomb Force** → B08 (Orbital Mechanics)  
  - Data: JPL ephemerides (`benchmarks/data/orbits/*.csv`)  
  - Tool: `validate_b08_orbital` (python/cpp depending on build)

- **Phase 2: Rydberg Spectrum** → B02 (Rydberg)  
  - Data: NIST ASD Balmer series (`benchmarks/data/B02_balmer.csv`)  
  - Tool: `validate_b02_rydberg`

- **Phase 3: Fine Structure** → B03 (Fine Structure)  
  - Data: NIST ASD fine-structure lines (`benchmarks/data/B03_fine.csv`)  
  - Tool: `validate_b03_fine`

- **Phase 4: Lamb Shift** → B04 (Lamb Shift)  
  - Data: H 2S-2P 1057.8446 MHz (`benchmarks/data/B04_lamb.csv`)  
  - Tool: `validate_b04_lamb`

- **Phase 5: Hyperfine** → B05 (Hyperfine)  
  - Data: 21 cm line (`benchmarks/data/B05_hyperfine.csv`)  
  - Tool: `validate_b05_hyperfine`

- **Phase 6: Multi-Electron** → B06 (Many-Electron), B28 (Z_eff valence), B29 (I1), B38 (heavy Z_eff), B50 (end-to-end)  
  - Data: NIST ionization energies, radii (`benchmarks/data/B06_multi.csv`, `B29_I1_reference.csv`, `B38_I1_reference.csv`)  
  - Tool: `atomic_calculator` (cpp), `validate_multi_e`

- **Phase 7: Thermodynamics** → B07 (Thermo), B16 (Transport)  
  - Data: κ, η, D datasets (`benchmarks/data/B07_transport.csv`)  
  - Tool: `validate_b07_thermo`, `validate_b16_transport`

- **Phase 9: Oblateness** → B11 (Planetary Oblateness)  
  - Data: GRACE/JPL oblateness (`benchmarks/data/B11_oblateness.csv`)  
  - Tool: `validate_b11_oblateness`

- **Phase 10: Magnetism** → B17 (Magnetism), B35 (Spin/Parity proxy via packing), B36 (Quadrupole moments)  
  - Data: CODATA g-factors; nuclear moments (`benchmarks/data/B17_magnetism.csv`, `B36_quadrupole_reference.csv`)  
  - Tool: `validate_b17_magnetism`

- **Phase 15: Gravitation** → B09 (Grav radiation), B10 (Strong field)  
  - Data: Pulsar decay, Mercury precession, solar deflection (`benchmarks/data/B09_psr.csv`, `B10_mercury.csv`)  
  - Tool: `validate_b09_grav_rad`, `validate_b10_strong_field`

- **Phase 16: CMB / BAO** → B13 (CMB redshift), B15 (BAO)  
  - Data: Planck/WMAP; BAO 147 Mpc (`benchmarks/data/B13_cmb.csv`, `B15_bao.csv`)  
  - Tool: `validate_b13_cmb`, `validate_b15_bao`

- **Phase 17: Nuclear Structure** → B18 (Nuclear), B27 (Radius scaling), B34 (Binding from occlusion), B39 (Radius saturation)  
  - Data: ENSDF radii, AME2020 binding (`benchmarks/data/B27_radii.csv`, `B34_binding_reference.csv`, `B39_radii_series.csv`)  
  - Tool: `validate_b18_nuclear`, `validate_b27_radius`, `validate_b34_binding`

- **Phase 18: Weak / Beta** → B19 (Weak Interactions), B53 (Beta spectra)  
  - Data: CODATA mass differences, beta spectra (`benchmarks/data/B19_beta.csv`)  
  - Tool: `validate_b19_beta`

- **Phase 20: Master Equation / k-law** → B07 (k-law), B20 (z·k²), B45 (P∞ scaling)  
  - Data: Exoplanet/stellar compactness (`benchmarks/data/B20_zk2.csv`)  
  - Tool: `validate_b20_zk2`

- **Phase 21: Screening** → B21 (Screening), B37 (Screening geometry)  
  - Data: Force hierarchy ratios (`benchmarks/data/B21_screening.csv`)  
  - Tool: `validate_b21_screening`

- **Phase 22: Stellar / Exoplanets** → B12 (Stellar structure), B20 (z·k²)  
  - Data: Stellar catalogs (`benchmarks/data/B12_stellar.csv`)  
  - Tool: `star_calculator_complete`

- **Phases 24/25: Galactic Rotation / Pressure Differentials** → B14 (Rotation), B22 (Pressure differentials)  
  - Data: SPARC rotation curves; pressure scaling tables (`benchmarks/data/B14_sparc.csv`, `B22_pressure.csv`)  
  - Tool: `validate_b14_galactic`

- **Phase 26: Scale Interactions** → B23 (Scale dependent interactions)  
  - Data: Force scaling datasets (`benchmarks/data/B23_forces.csv`)  
  - Tool: `validate_b23_scale`

- **Phase 27B: Multi-e Occlusion (Heavy)** → B24 (Multi-e heavy), B38 (Heavy ionization), B50 (End-to-end)  
  - Data: Heavy-element ionization/radius tables (`benchmarks/data/B24_heavy.csv`, `B38_I1_reference.csv`, `B50_reference.csv`)  
  - Tool: `validate_b24_multie`

---

## Investigations → Phases

- `investigations/nuclear_structure_probe/*` → Phases 17, 21, 27B (packing, screening, heavy occlusion)
- `investigations/galactic_rotation/*` → Phases 24, 25 (disk eclipse saturation)
- `investigations/magnetism/*` → Phase 10 (helical wakes, g-factors)
- `investigations/weak_interactions/*` → Phase 18 (beta decay spectra, neutrino wake)

---

## Tools Summary

- **Atomic & Multi-e:** `atomic_calculator` (cpp), `validate_b02_rydberg`, `validate_b03_fine`, `validate_b06_multi`
- **Stellar/Orbital:** `star_calculator_complete`, `validate_b08_orbital`, `validate_b12_stellar`, `validate_b20_zk2`
- **Galactic:** `galactic_rotation` (cpp), `validate_b14_galactic`
- **Nuclear/N-Body:** `sdt_navier_cpp` core solvers; `validate_b18_nuclear`, `validate_b27_radius`
- **Thermo:** `validate_b07_thermo`, `validate_b16_transport`
- **Screening/Occlusion:** `validate_b21_screening`, `validate_b24_multie`, `validate_b37_screening`

---

## Data Index (benchmarks/data/)

- Atomic/ionization: `B02_balmer.csv`, `B03_fine.csv`, `B29_I1_reference.csv`, `B38_I1_reference.csv`, `B50_reference.csv`
- Nuclear: `B27_radii.csv`, `B34_binding_reference.csv`, `B39_radii_series.csv`, `B36_quadrupole_reference.csv`
- Stellar/Orbital: `B12_stellar.csv`, `B20_zk2.csv`, `B08_orbits.csv`
- Galactic: `B14_sparc.csv`, `B22_pressure.csv`
- Screening: `B21_screening.csv`, `B37_screening_reference.csv`

---

## Outstanding Links

- B21 (Screening) ↔ Phase 21: refine geometric derivation of ξ=10⁻⁹.  
- B24/B38/B50 (Heavy multi-e) ↔ Phase 27B: complete Z>20 occlusion maps and ionization ladders.  
- Extended set B25–B74: see `B25_B50_IMPLEMENTATION_PROMPT.md` and `B25_B50_VALIDATION_PROMPT.md` for detailed C++ tasks and validation metrics.
