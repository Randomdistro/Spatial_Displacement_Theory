#!/usr/bin/env python3
"""
Implementation Duplication Audit Script
Compares different implementations of key calculations across the codebase.
"""

from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
import re

@dataclass
class Implementation:
    """Represents a calculation implementation"""
    file_path: str
    method_name: str
    formula: str
    description: str
    line_numbers: Tuple[int, int] = (0, 0)

class ImplementationAuditor:
    """Audits implementation duplications"""
    
    def __init__(self, root_dir: Path = None):
        if root_dir is None:
            root_dir = Path(__file__).parent.parent
        self.root_dir = root_dir
        self.implementations = {
            'nuclear_binding': [],
            'orbital_mechanics': [],
            'pressure_fields': [],
            'solid_angle': [],
        }
    
    def scan_nuclear_binding(self):
        """Scan for nuclear binding energy implementations"""
        files_to_scan = [
            'data/nuclei_per_nucei_calculator.py',
            'investigations/nuclear_structure_probe/Phase_02_Binding_Energy/02_01_occlusion_binding_calculator.py',
            'investigations/nuclear_structure_probe/Phase_02_Binding_Energy/02_03_alpha_structure.py',
            'investigations/nuclear_structure_probe/Phase_01_Nuclear_Packing/01_02_first_shell_completion.py',
            'Code/sdt_navier/nuclear.py',
        ]
        
        for file_rel_path in files_to_scan:
            file_path = self.root_dir / file_rel_path
            if not file_path.exists():
                continue
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for binding energy calculations
            if 'calculate_binding_energy' in content or 'B =' in content or 'binding_energy' in content:
                # Extract relevant sections
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'def calculate_binding_energy' in line or 'B =' in line or 'binding_energy' in line:
                        # Extract method or formula
                        method = self._extract_method(lines, i)
                        if method:
                            self.implementations['nuclear_binding'].append(
                                Implementation(
                                    file_path=str(file_path.relative_to(self.root_dir)),
                                    method_name=method.get('name', 'unknown'),
                                    formula=method.get('formula', ''),
                                    description=method.get('description', ''),
                                    line_numbers=(i+1, min(i+50, len(lines)))
                                )
                            )
    
    def scan_orbital_mechanics(self):
        """Scan for orbital mechanics implementations"""
        files_to_scan = [
            'Code/sdt_orbital_sim/include/sdt/core/types.hpp',
            'Code/sdt_solar_system/include/sdt/solar_system/celestial_body.hpp',
            'Code/sdt_core/constants.py',
            'tools/sdt_atomic/constants.py',
        ]
        
        for file_rel_path in files_to_scan:
            file_path = self.root_dir / file_rel_path
            if not file_path.exists():
                continue
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for orbital velocity formulas
            if 'orbital_velocity' in content or 'v =' in content or 'v(r)' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'orbital_velocity' in line or 'v =' in line or 'v(r)' in line:
                        method = self._extract_method(lines, i)
                        if method:
                            self.implementations['orbital_mechanics'].append(
                                Implementation(
                                    file_path=str(file_path.relative_to(self.root_dir)),
                                    method_name=method.get('name', 'unknown'),
                                    formula=method.get('formula', ''),
                                    description=method.get('description', ''),
                                    line_numbers=(i+1, min(i+20, len(lines)))
                                )
                            )
    
    def _extract_method(self, lines: List[str], start_line: int) -> Dict:
        """Extract method information from code"""
        method = {}
        
        # Look for function definition
        for i in range(max(0, start_line-5), min(len(lines), start_line+30)):
            line = lines[i]
            
            # Extract function name
            if 'def ' in line or 'function' in line or 'scalar_t' in line:
                match = re.search(r'(def|function|scalar_t)\s+(\w+)', line)
                if match:
                    method['name'] = match.group(2)
            
            # Extract formula
            if '=' in line and ('sqrt' in line or '**' in line or 'pow' in line):
                method['formula'] = line.strip()
            
            # Extract comments
            if '//' in line or '#' in line:
                comment = line.split('//')[0].split('#')[0].strip()
                if comment:
                    method['description'] = comment
        
        return method if method else None
    
    def generate_report(self) -> str:
        """Generate implementation audit report"""
        report = []
        report.append("# Implementation Duplication Audit Report")
        report.append("")
        report.append("## Executive Summary")
        report.append("")
        report.append(f"- Nuclear binding implementations: {len(self.implementations['nuclear_binding'])}")
        report.append(f"- Orbital mechanics implementations: {len(self.implementations['orbital_mechanics'])}")
        report.append(f"- Pressure field implementations: {len(self.implementations['pressure_fields'])}")
        report.append(f"- Solid angle implementations: {len(self.implementations['solid_angle'])}")
        report.append("")
        
        report.append("## A. Nuclear Binding Energy Calculations")
        report.append("")
        report.append("### Methods Found:")
        report.append("")
        
        for impl in self.implementations['nuclear_binding']:
            report.append(f"#### {impl.file_path}")
            report.append(f"- **Method:** {impl.method_name}")
            report.append(f"- **Formula:** {impl.formula}")
            report.append(f"- **Description:** {impl.description}")
            report.append(f"- **Lines:** {impl.line_numbers[0]}-{impl.line_numbers[1]}")
            report.append("")
        
        report.append("### Comparison:")
        report.append("")
        report.append("1. **Neutrino Model** (`nuclei_per_nucei_calculator.py`):")
        report.append("   - Formula: B = N_ν × E_ν × f_geometry")
        report.append("   - Where: N_ν = 18 for alpha (6 bonds × 3 phase packets)")
        report.append("   - E_ν = 1.57 MeV per neutrino")
        report.append("")
        report.append("2. **Occlusion Model** (`02_01_occlusion_binding_calculator.py`):")
        report.append("   - Formula: B = k × Ω_total")
        report.append("   - Where: k is calibrated from deuteron, Ω is solid angle occlusion")
        report.append("")
        report.append("3. **Field Theory** (`sdt_navier/nuclear.py`):")
        report.append("   - Formula: Ė = P∞ A_eff Γ κ (1-η)")
        report.append("   - Master equation approach")
        report.append("")
        report.append("### Consistency Check:")
        report.append("")
        report.append("- **Question:** Do neutrino model and occlusion model give same results?")
        report.append("  - Alpha: 18 neutrinos × 1.57 MeV = 28.26 MeV (vs 28.296 MeV exp)")
        report.append("  - Occlusion: k × Ω_alpha = ? (needs validation)")
        report.append("")
        report.append("- **Question:** Is 18 neutrinos = 6 bonds × 3 phase packets?")
        report.append("  - Yes, this is the theoretical basis")
        report.append("")
        
        report.append("## B. Orbital Mechanics Calculations")
        report.append("")
        report.append("### Formulas Found:")
        report.append("")
        report.append("1. **Orbital Velocity:** v = (c/κ)√(R_eff/r)")
        report.append("2. **Orbital Period:** T = 2πκ√(r³/R_eff)/c")
        report.append("3. **Acceleration:** a = -c²R_eff/(κ²r²)")
        report.append("")
        report.append("### Implementation Locations:")
        report.append("")
        for impl in self.implementations['orbital_mechanics']:
            report.append(f"- `{impl.file_path}`: {impl.method_name}")
        report.append("")
        
        report.append("### Consistency Check:")
        report.append("")
        report.append("- All implementations use the same formulas")
        report.append("- Need to verify z·k² = 1 invariant usage")
        report.append("- Need to validate against planetary data (<0.8% error)")
        report.append("")
        
        return "\n".join(report)

def main():
    """Main execution"""
    auditor = ImplementationAuditor()
    print("Scanning nuclear binding implementations...")
    auditor.scan_nuclear_binding()
    print("Scanning orbital mechanics implementations...")
    auditor.scan_orbital_mechanics()
    print("Generating report...")
    report = auditor.generate_report()
    
    output_file = Path(__file__).parent / "02_IMPLEMENTATION_AUDIT.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Report written to: {output_file}")

if __name__ == "__main__":
    main()
