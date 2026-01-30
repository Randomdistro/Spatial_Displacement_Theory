# B25–B50 Benchmarks (Implementation Status)

This repo currently implements a **C++-only** benchmark generator:

- Tool: `SDT/Code/sdt_navier_cpp/tools/benchmarks_b25_b50.cpp`
- Build: from `SDT/Code/sdt_navier_cpp/`
- Output reports: `SDT/benchmarks/B##_validation_report.json`

## How to run

From the C++ build output directory (Windows example):

- Run one benchmark:
  - `benchmarks_b25_b50.exe --benchmark B25`
- Run all (B25–B50):
  - `benchmarks_b25_b50.exe --all`

The executable auto-detects the repo root by searching parent directories for `SDT/benchmarks/`.

## Current status snapshot

- **Certified**: B25, B26, B41, B42
- **Under Investigation**: B34
- **Draft placeholders emitted (no dataset/model yet)**: B27–B33, B35–B40, B43–B50

For a row-by-row view, see `SDT/benchmarks/B25_B50_TrackingSheet.csv`.

