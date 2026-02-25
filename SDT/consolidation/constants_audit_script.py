#!/usr/bin/env python3
"""
Constants Consolidation Audit Script
Extracts and compares all constant definitions across the codebase.
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict
import json

@dataclass
class ConstantDefinition:
    """Represents a constant definition found in a file"""
    name: str
    value: float
    unit: str = ""
    comment: str = ""
    file_path: str = ""
    line_number: int = 0
    source: str = ""  # CODATA, Phase document, experimental, etc.

@dataclass
class ConstantDiscrepancy:
    """Represents a discrepancy in constant values"""
    name: str
    values: List[Tuple[str, float, str]]  # (file, value, comment)
    recommended_value: float = 0.0
    recommended_source: str = ""

class ConstantsAuditor:
    """Audits constants across the codebase"""
    
    def __init__(self, root_dir: str = None):
        if root_dir is None:
            root_dir = Path(__file__).parent.parent
        self.root_dir = Path(root_dir)
        self.constants: Dict[str, List[ConstantDefinition]] = defaultdict(list)
        self.discrepancies: Dict[str, ConstantDiscrepancy] = {}
        
        # Known canonical values (to be populated from CODATA and Phase docs)
        self.canonical_values = {
            # CODATA 2018
            'C': 299792458.0,
            'H': 6.62607015e-34,
            'H_BAR': 1.054571817e-34,
            'E_CHARGE': 1.602176634e-19,
            'M_E': 9.1093837015e-31,
            'M_P': 1.67262192369e-27,
            'M_N': 1.67492749804e-27,
            'ALPHA': 7.2973525693e-3,
            'A_0': 5.29177210903e-11,
            'R_INF': 10973731.568160,
            
            # SDT Nuclear Parameters
            'R_P': 8.40e-16,
            'R_N': 8.70e-16,
            'KAPPA_P': 1.190e15,
            'GAMMA_P': 0.546,
            'ETA_P_BOUND': 0.0003,
            'KAPPA_N': 1.0 / 8.70e-16,  # 1/R_N
            'GAMMA_E_N': 0.531,
            'ETA_N_BOUND': 0.0019,
            'P_INFINITY_NUCLEAR': 1.65e31,
            'P_CMB': 2.036e-2,
            
            # Experimental Binding Energies (MeV)
            'B_DEUTERON': 2.2246,
            'B_ALPHA': 28.296,
            'B_TRITON': 8.482,
            'B_HELION': 7.718,
            
            # Spation Properties
            'RHO_S': 5.2e96,
            'K_BULK': 4.6e113,
            'R_PLANCK': 1.616255e-35,
        }
        
        self.canonical_sources = {
            'C': 'CODATA 2018 (exact)',
            'H': 'CODATA 2018',
            'H_BAR': 'CODATA 2018',
            'E_CHARGE': 'CODATA 2018',
            'M_E': 'CODATA 2018',
            'M_P': 'CODATA 2018',
            'M_N': 'CODATA 2018',
            'ALPHA': 'CODATA 2018',
            'A_0': 'CODATA 2018',
            'R_INF': 'CODATA 2018',
            'R_P': 'CODATA 2018 (0.84 fm)',
            'R_N': 'CODATA 2018 (0.87 fm)',
            'KAPPA_P': 'Phase 19 (1/R_P)',
            'GAMMA_P': 'Phase 19',
            'ETA_P_BOUND': 'Phase 19',
            'KAPPA_N': 'Phase 19 (1/R_N)',
            'GAMMA_E_N': 'Phase 19',
            'ETA_N_BOUND': 'Phase 19',
            'P_INFINITY_NUCLEAR': 'Phase 19',
            'P_CMB': 'CMB recombination (z=1089.9)',
            'B_DEUTERON': 'Experimental (MeV)',
            'B_ALPHA': 'Experimental (MeV)',
            'B_TRITON': 'Experimental (MeV)',
            'B_HELION': 'Experimental (MeV)',
            'RHO_S': 'Phase 20',
            'K_BULK': 'Phase 20',
            'R_PLANCK': 'CODATA 2018',
        }
    
    def extract_python_constants(self, file_path: Path) -> List[ConstantDefinition]:
        """Extract constant definitions from Python files"""
        constants = []
        
        # Patterns for Python constant definitions
        patterns = [
            # C = 299792458.0  # comment
            (r'^(\s*)([A-Z_][A-Z0-9_]*)\s*=\s*([0-9.eE+-]+)\s*(?:#\s*(.*))?$', 'assignment'),
            # C: float = 299792458.0  # comment
            (r'^(\s*)([A-Z_][A-Z0-9_]*)\s*:\s*\w+\s*=\s*([0-9.eE+-]+)\s*(?:#\s*(.*))?$', 'typed_assignment'),
        ]
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.rstrip()
                    for pattern, pattern_type in patterns:
                        match = re.match(pattern, line)
                        if match:
                            indent, name, value_str, comment = match.groups()
                            try:
                                value = float(value_str)
                                const_def = ConstantDefinition(
                                    name=name,
                                    value=value,
                                    comment=comment or "",
                                    file_path=str(file_path.relative_to(self.root_dir)),
                                    line_number=line_num,
                                    source=""
                                )
                                constants.append(const_def)
                            except ValueError:
                                pass
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return constants
    
    def extract_cpp_constants(self, file_path: Path) -> List[ConstantDefinition]:
        """Extract constant definitions from C++ files"""
        constants = []
        
        # Patterns for C++ constant definitions
        patterns = [
            # constexpr double C = 299792458.0;  // comment
            (r'^\s*(?:inline\s+)?constexpr\s+\w+\s+([A-Z_][A-Z0-9_]*)\s*=\s*([0-9.eE+-]+)\s*;\s*(?://\s*(.*))?$', 'constexpr'),
            # const double C = 299792458.0;  // comment
            (r'^\s*const\s+\w+\s+([A-Z_][A-Z0-9_]*)\s*=\s*([0-9.eE+-]+)\s*;\s*(?://\s*(.*))?$', 'const'),
        ]
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.rstrip()
                    for pattern, pattern_type in patterns:
                        match = re.match(pattern, line)
                        if match:
                            if pattern_type == 'constexpr':
                                name, value_str, comment = match.groups()
                            else:
                                name, value_str, comment = match.groups()
                            
                            try:
                                value = float(value_str)
                                const_def = ConstantDefinition(
                                    name=name,
                                    value=value,
                                    comment=comment or "",
                                    file_path=str(file_path.relative_to(self.root_dir)),
                                    line_number=line_num,
                                    source=""
                                )
                                constants.append(const_def)
                            except ValueError:
                                pass
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return constants
    
    def scan_files(self):
        """Scan all constant definition files"""
        files_to_scan = [
            # C++ files
            'Code/shared/include/sdt/core/constants.hpp',
            'Code/sdt_atomic_sim/include/sdt/core/constants.hpp',
            'Code/sdt_navier_cpp/include/sdt_navier/constants.hpp',
            'Code/sdt_chemistry/include/sdt/chemistry/constants.hpp',
            'Code/sdt_solar_system/include/sdt/solar_system/constants.hpp',
            'Code/sdt_orbital_sim/include/sdt/core/constants.hpp',
            # Python files
            'Code/sdt_core/constants.py',
            'tools/sdt_atomic/constants.py',
            'data/nuclei_per_nucei_calculator.py',
            'investigations/nuclear_structure_probe/Phase_02_Binding_Energy/02_01_occlusion_binding_calculator.py',
        ]
        
        for file_rel_path in files_to_scan:
            file_path = self.root_dir / file_rel_path
            if not file_path.exists():
                print(f"Warning: File not found: {file_rel_path}")
                continue
            
            if file_path.suffix == '.py':
                consts = self.extract_python_constants(file_path)
            elif file_path.suffix == '.hpp':
                consts = self.extract_cpp_constants(file_path)
            else:
                continue
            
            for const in consts:
                self.constants[const.name].append(const)
    
    def identify_discrepancies(self, tolerance: float = 1e-6):
        """Identify discrepancies in constant values"""
        for name, definitions in self.constants.items():
            if len(definitions) <= 1:
                continue
            
            # Group by value (within tolerance)
            value_groups = defaultdict(list)
            for defn in definitions:
                # Find matching group
                matched = False
                for group_value, group_defs in value_groups.items():
                    if abs(defn.value - group_value) < tolerance:
                        group_defs.append(defn)
                        matched = True
                        break
                if not matched:
                    value_groups[defn.value].append(defn)
            
            # If multiple distinct values, it's a discrepancy
            if len(value_groups) > 1:
                values_list = []
                for value, defs_list in value_groups.items():
                    for defn in defs_list:
                        values_list.append((
                            defn.file_path,
                            defn.value,
                            defn.comment
                        ))
                
                # Determine recommended value
                recommended_value = self.canonical_values.get(name, definitions[0].value)
                recommended_source = self.canonical_sources.get(name, "Unknown")
                
                self.discrepancies[name] = ConstantDiscrepancy(
                    name=name,
                    values=values_list,
                    recommended_value=recommended_value,
                    recommended_source=recommended_source
                )
    
    def generate_report(self) -> str:
        """Generate the constants audit report"""
        report = []
        report.append("# Constants Consolidation Audit Report")
        report.append("")
        report.append(f"**Generated:** {Path(__file__).stat().st_mtime}")
        report.append("")
        report.append("## Executive Summary")
        report.append("")
        report.append(f"- Total unique constants found: {len(self.constants)}")
        report.append(f"- Files scanned: {sum(len(defs) for defs in self.constants.values())}")
        report.append(f"- Discrepancies identified: {len(self.discrepancies)}")
        report.append("")
        
        report.append("## Complete Inventory of Constants")
        report.append("")
        report.append("### CODATA 2018 Fundamental Constants")
        report.append("")
        report.append("| Constant | Value | Unit | Source |")
        report.append("|----------|-------|------|--------|")
        
        codata_constants = ['C', 'H', 'H_BAR', 'E_CHARGE', 'M_E', 'M_P', 'M_N', 'ALPHA', 'A_0', 'R_INF']
        for name in codata_constants:
            if name in self.constants:
                defn = self.constants[name][0]
                source = self.canonical_sources.get(name, "Unknown")
                report.append(f"| {name} | {defn.value:.12e} | - | {source} |")
        
        report.append("")
        report.append("### SDT-Specific Constants")
        report.append("")
        report.append("| Constant | Value | Unit | Source |")
        report.append("|----------|-------|------|--------|")
        
        sdt_constants = ['R_P', 'R_N', 'KAPPA_P', 'GAMMA_P', 'ETA_P_BOUND', 'KAPPA_N', 
                        'GAMMA_E_N', 'ETA_N_BOUND', 'P_INFINITY_NUCLEAR', 'P_CMB',
                        'RHO_S', 'K_BULK', 'R_PLANCK']
        for name in sdt_constants:
            if name in self.constants:
                defn = self.constants[name][0]
                source = self.canonical_sources.get(name, "Unknown")
                report.append(f"| {name} | {defn.value:.12e} | - | {source} |")
        
        report.append("")
        report.append("### Experimental Binding Energies")
        report.append("")
        report.append("| Constant | Value | Unit | Source |")
        report.append("|----------|-------|------|--------|")
        
        binding_constants = ['B_DEUTERON', 'B_ALPHA', 'B_TRITON', 'B_HELION']
        for name in binding_constants:
            if name in self.constants:
                defn = self.constants[name][0]
                source = self.canonical_sources.get(name, "Unknown")
                report.append(f"| {name} | {defn.value:.6f} | MeV | {source} |")
        
        report.append("")
        report.append("## Discrepancy Matrix")
        report.append("")
        report.append("### Constants with Multiple Values")
        report.append("")
        
        if self.discrepancies:
            for name, disc in sorted(self.discrepancies.items()):
                report.append(f"#### {name}")
                report.append("")
                report.append(f"**Recommended Value:** {disc.recommended_value:.12e}")
                report.append(f"**Recommended Source:** {disc.recommended_source}")
                report.append("")
                report.append("| File | Value | Comment |")
                report.append("|------|-------|---------|")
                for file_path, value, comment in disc.values:
                    report.append(f"| {file_path} | {value:.12e} | {comment} |")
                report.append("")
        else:
            report.append("No discrepancies found (all constants have consistent values).")
        
        report.append("")
        report.append("## Migration Path")
        report.append("")
        report.append("### Files Requiring Updates")
        report.append("")
        
        # Group files by what needs updating
        files_to_update = defaultdict(set)
        for name, disc in self.discrepancies.items():
            for file_path, value, comment in disc.values:
                if abs(value - disc.recommended_value) > 1e-6:
                    files_to_update[file_path].add(name)
        
        for file_path, constants in sorted(files_to_update.items()):
            report.append(f"#### {file_path}")
            report.append("")
            report.append("Constants to update:")
            for const_name in sorted(constants):
                disc = self.discrepancies[const_name]
                report.append(f"- `{const_name}`: Change to {disc.recommended_value:.12e} (from {disc.recommended_source})")
            report.append("")
        
        return "\n".join(report)

def main():
    """Main execution"""
    auditor = ConstantsAuditor()
    print("Scanning files for constants...")
    auditor.scan_files()
    print(f"Found {len(auditor.constants)} unique constants")
    print("Identifying discrepancies...")
    auditor.identify_discrepancies()
    print(f"Found {len(auditor.discrepancies)} discrepancies")
    print("Generating report...")
    report = auditor.generate_report()
    
    output_file = Path(__file__).parent / "01_CONSTANTS_AUDIT.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Report written to: {output_file}")

if __name__ == "__main__":
    main()
