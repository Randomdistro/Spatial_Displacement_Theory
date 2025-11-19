#!/usr/bin/env python3
"""
SDT Formula Extractor
Extracts all formulas (boxed and tagged equations) from Phase documents
and creates a structured database for validation.
"""

import re
import json
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class Formula:
    """Represents a single formula extracted from a document."""
    formula_id: str
    file_path: str
    line_number: int
    latex: str
    equation_type: str  # 'boxed', 'tagged', 'display'
    tag: Optional[str] = None
    context_before: Optional[str] = None
    context_after: Optional[str] = None
    benchmark_id: Optional[str] = None
    domain: Optional[str] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class FormulaExtractor:
    """Extracts formulas from markdown files."""
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.formulas: List[Formula] = []
        self.formula_counter = defaultdict(int)
        
        # Domain mapping from file names
        self.domain_map = {
            'Phase_1': 'atomic',
            'Phase_2': 'atomic',
            'Phase_3': 'atomic',
            'Phase_4': 'atomic',
            'Phase_5': 'atomic',
            'Phase_6': 'atomic',
            'Phase_27A': 'atomic',
            'Phase_27B': 'atomic',
            'Phase_27C': 'atomic',
            'Phase_7': 'thermodynamic',
            'Phase_14': 'thermodynamic',
            'Phase_10': 'electromagnetic',
            'Phase_11': 'electromagnetic',
            'Phase_12': 'electromagnetic',
            'Phase_15': 'gravitational',
            'Phase_20': 'gravitational',
            'Phase_16': 'cosmological',
            'Phase_17': 'nuclear',
            'Phase_18': 'nuclear',
            'Phase_24': 'galactic',
            'Phase_25': 'galactic',
            'Phase_Y': 'galactic',
        }
        
        # Benchmark mapping
        self.benchmark_map = {
            'Phase_1': 'B08',
            'Phase_2': 'B02',
            'Phase_3': 'B03',
            'Phase_4': 'B04',
            'Phase_5': 'B05',
            'Phase_6': 'B06',
            'Phase_7': 'B07',
            'Phase_9': 'B11',
            'Phase_10': 'B17',
            'Phase_15': 'B10',
            'Phase_16': 'B13',
            'Phase_17': 'B18',
            'Phase_18': 'B19',
            'Phase_21': 'B21',
            'Phase_22': 'B12',
            'Phase_24': 'B14',
            'Phase_25': 'B22',
            'Phase_26': 'B23',
            'Phase_27A': 'B01',
            'Phase_27B': 'B24',
        }
    
    def extract_formulas_from_file(self, file_path: Path) -> List[Formula]:
        """Extract all formulas from a single markdown file."""
        formulas = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return formulas
        
        # Extract phase number for ID prefix
        phase_match = re.search(r'Phase[_\s]*(\d+[A-Z]?)', file_path.name)
        phase_prefix = phase_match.group(0) if phase_match else 'Unknown'
        
        # Determine domain and benchmark
        domain = None
        benchmark_id = None
        for key, val in self.domain_map.items():
            if key in file_path.name:
                domain = val
                break
        for key, val in self.benchmark_map.items():
            if key in file_path.name:
                benchmark_id = val
                break
        
        # Patterns for different equation types
        # Boxed equations: \boxed{...}
        boxed_pattern = r'\\boxed\{([^}]+)\}'
        # Tagged equations: \tag{...}
        tagged_pattern = r'\\tag\{([^}]+)\}'
        # Display math: $$...$$
        display_pattern = r'\$\$([^$]+)\$\$'
        # Inline math with tag: $...$ \tag{...}
        inline_tagged_pattern = r'\$([^$]+)\$[^$]*\\tag\{([^}]+)\}'
        
        in_math_block = False
        current_math = []
        current_line_start = 0
        
        for line_num, line in enumerate(lines, 1):
            # Check for boxed equations
            for match in re.finditer(boxed_pattern, line):
                latex = match.group(1).strip()
                if latex:
                    formula_id = f"{phase_prefix}-EQ{self.formula_counter[phase_prefix] + 1}"
                    self.formula_counter[phase_prefix] += 1
                    
                    # Try to find tag
                    tag_match = re.search(tagged_pattern, line)
                    tag = tag_match.group(1) if tag_match else None
                    
                    formulas.append(Formula(
                        formula_id=formula_id,
                        file_path=str(file_path.relative_to(self.base_dir)),
                        line_number=line_num,
                        latex=latex,
                        equation_type='boxed',
                        tag=tag,
                        context_before=lines[max(0, line_num-3):line_num-1] if line_num > 1 else None,
                        context_after=lines[line_num:min(len(lines), line_num+2)] if line_num < len(lines) else None,
                        benchmark_id=benchmark_id,
                        domain=domain
                    ))
            
            # Check for display math blocks
            if '$$' in line:
                if not in_math_block:
                    # Start of math block
                    in_math_block = True
                    current_math = [line]
                    current_line_start = line_num
                else:
                    # End of math block
                    current_math.append(line)
                    math_content = ''.join(current_math)
                    
                    # Extract content between $$
                    math_match = re.search(r'\$\$([^$]+)\$\$', math_content, re.DOTALL)
                    if math_match:
                        latex = math_match.group(1).strip()
                        if latex:
                            # Check for tag
                            tag_match = re.search(tagged_pattern, math_content)
                            tag = tag_match.group(1) if tag_match else None
                            
                            formula_id = f"{phase_prefix}-EQ{self.formula_counter[phase_prefix] + 1}"
                            self.formula_counter[phase_prefix] += 1
                            
                            formulas.append(Formula(
                                formula_id=formula_id,
                                file_path=str(file_path.relative_to(self.base_dir)),
                                line_number=current_line_start,
                                latex=latex,
                                equation_type='display',
                                tag=tag,
                                context_before=lines[max(0, current_line_start-3):current_line_start-1] if current_line_start > 1 else None,
                                context_after=lines[line_num:min(len(lines), line_num+2)] if line_num < len(lines) else None,
                                benchmark_id=benchmark_id,
                                domain=domain
                            ))
                    
                    in_math_block = False
                    current_math = []
            elif in_math_block:
                current_math.append(line)
        
        return formulas
    
    def extract_all_formulas(self) -> List[Formula]:
        """Extract formulas from all Phase documents."""
        phase_dir = self.base_dir / 'SDT' / 'Papers' / 'SDT_Foundation' / 'Part_I_Axioms_and_Core_Equations'
        
        if not phase_dir.exists():
            print(f"Phase directory not found: {phase_dir}")
            return []
        
        # Find all markdown files
        md_files = list(phase_dir.glob('*.md'))
        md_files.extend(list(phase_dir.glob('Phase_*.md')))
        
        # Also check atomica sentis
        atomica_file = phase_dir / 'atomica sentis.md'
        if atomica_file.exists():
            md_files.append(atomica_file)
        
        print(f"Found {len(md_files)} markdown files to process")
        
        all_formulas = []
        for md_file in md_files:
            print(f"Processing {md_file.name}...")
            formulas = self.extract_formulas_from_file(md_file)
            all_formulas.extend(formulas)
            print(f"  Extracted {len(formulas)} formulas")
        
        # Also process Part II derivations
        derivations_dir = self.base_dir / 'SDT' / 'Papers' / 'SDT_Foundation' / 'Part_II_Derivations'
        if derivations_dir.exists():
            for md_file in derivations_dir.rglob('*.md'):
                print(f"Processing {md_file.name}...")
                formulas = self.extract_formulas_from_file(md_file)
                all_formulas.extend(formulas)
                print(f"  Extracted {len(formulas)} formulas")
        
        return all_formulas
    
    def save_database(self, formulas: List[Formula], output_file: str):
        """Save formulas to JSON database."""
        data = {
            'total_formulas': len(formulas),
            'formulas': [asdict(f) for f in formulas],
            'statistics': {
                'by_domain': defaultdict(int),
                'by_benchmark': defaultdict(int),
                'by_type': defaultdict(int)
            }
        }
        
        for f in formulas:
            if f.domain:
                data['statistics']['by_domain'][f.domain] += 1
            if f.benchmark_id:
                data['statistics']['by_benchmark'][f.benchmark_id] += 1
            data['statistics']['by_type'][f.equation_type] += 1
        
        # Convert defaultdicts to regular dicts for JSON
        data['statistics'] = {
            'by_domain': dict(data['statistics']['by_domain']),
            'by_benchmark': dict(data['statistics']['by_benchmark']),
            'by_type': dict(data['statistics']['by_type'])
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\nSaved {len(formulas)} formulas to {output_file}")
        print(f"Statistics:")
        print(f"  By domain: {data['statistics']['by_domain']}")
        print(f"  By benchmark: {data['statistics']['by_benchmark']}")
        print(f"  By type: {data['statistics']['by_type']}")

def main():
    """Main extraction function."""
    base_dir = Path(__file__).parent.parent.parent
    extractor = FormulaExtractor(base_dir)
    
    print("Starting formula extraction...")
    formulas = extractor.extract_all_formulas()
    
    output_file = base_dir / 'SDT' / 'validation' / 'formula_database.json'
    extractor.save_database(formulas, output_file)
    
    print(f"\nExtraction complete! Found {len(formulas)} formulas total.")

if __name__ == '__main__':
    main()

