# sdt_chemistry — Overview

C++20 molecular chemistry module implementing SDT pressure-field bond models. Models chemical bonds as pressure-gradient minima between nuclear displacement fields rather than electron sharing/exchange.

## Subfolders

- **include/sdt/chemistry/** — Headers: bond geometry, element properties, molecular structure, pressure-field bonding, master equation, geometry utilities, data loader, visualiser, designer
- **src/** — Implementations: bonds, elements (full periodic table), molecules, geometry, properties, data loader, visualiser, designer
- **tools/** — CLI tools: compound designer, molecule viewer, batch processor
- **tests/** — Unit tests
- **data/** — Element and molecule reference data files

## Files

- **CMakeLists.txt** — Build configuration
- **README.md** — Module documentation
- **IMPLEMENTATION_SUMMARY.md** — Summary of implemented features and SDT chemistry model
- **VISUALIZER_FEATURES.md** — Molecular visualisation feature guide
