# SDT Formula Validation Framework

This directory contains tools and results for validating all formulas in the Spatial Displacement Theory framework.

## Structure

- `formula_extractor.py` - Extracts all formulas from Phase documents
- `formula_database.json` - Structured database of all extracted formulas (2,627 formulas)
- `dimensional_validator.py` - Validates dimensional consistency
- `numerical_validator.py` - Validates numerical accuracy (0.8% tolerance)
- `key_formula_validator.py` - Validates specific key formulas with experimental data
- `master_validator.py` - Orchestrates all validation processes
- `formula_errors.md` - Error tracking document
- `key_formula_validation.json` - Results of key formula validation

## Usage

### Extract all formulas
```bash
python formula_extractor.py
```

### Validate key formulas
```bash
python key_formula_validator.py
```

### Run full validation suite
```bash
python master_validator.py
```

## Validation Standards

- **Theoretical Model Tolerance:** <0.8% error
- **Benchmark-Specific Tolerances:** As specified in `certification_protocol.md`
- **Exception Domains:** Exoplanet derivations and similar domains may have errors due to unknown variables

## Current Status

- **Formulas Extracted:** 2,627
- **Key Formulas Validated:** 7
- **Within Tolerance:** 5 (71.4%)
- **Critical Errors:** 2 (under investigation)

## Error Classification

- **CRITICAL:** Violates <0.8% tolerance or dimensional consistency (theoretical fault)
- **MAJOR:** Exceeds benchmark tolerance but <0.8% (needs investigation)
- **MINOR:** Known-variable domain error (exoplanets, etc.) - may indicate unknown variables
- **INFO:** Documentation/clarity issues

