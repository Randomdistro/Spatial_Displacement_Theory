"""
SDT Formula Extractor and Registry Generator

Extracts all mathematical formulas from Phase documents and creates a structured registry.
"""

import re
import json
import os
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class Formula:
    """Represents a single mathematical formula."""
    formula_id: str
    phase_doc: str
    section: str
    equation_number: str
    latex: str
    formula_type: str  # definition, derivation, prediction, constant
    physical_domain: str  # atomic, gravitational, thermodynamic, etc.
    dependencies: List[str]  # equation numbers this depends on
    description: str
    line_number: int

class FormulaExtractor:
    """Extracts formulas from Phase documents."""
    
    def __init__(self, phase_dir: str):
        self.phase_dir = Path(phase_dir)
        self.formulas: List[Formula] = []
        self.formula_counter = 0
        
        # Physical domain keywords
        self.domain_keywords = {
            'atomic': ['electron', 'proton', 'hydrogen', 'rydberg', 'spectrum', 'orbital', 'quantum', 'fine structure', 'hyperfine', 'lamb'],
            'gravitational': ['gravitation', 'gravity', 'β', 'beta', 'orbital', 'precession', 'deflection', 'mercury', 'binary', 'pulsar'],
            'thermodynamic': ['temperature', 'entropy', 'heat', 'thermal', 'transport', 'conduction', 'viscosity', 'diffusion', 'prandtl'],
            'electromagnetic': ['electric', 'magnetic', 'field', 'charge', 'current', 'maxwell', 'coulomb', 'gauss', 'em wave'],
            'cosmological': ['cmb', 'redshift', 'cosmic', 'universe', 'galactic', 'rotation', 'bao', 'scale'],
            'nuclear': ['nucleon', 'nuclear', 'proton', 'neutron', 'toroidal', 'vortex', 'femtoscale']
        }
    
    def extract_formulas_from_file(self, filepath: Path) -> List[Formula]:
        """Extract all formulas from a single Phase document."""
        formulas = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return formulas
        
        phase_name = filepath.stem
        current_section = "Introduction"
        
        # Pattern for display math: $$...$$ or \[...\]
        display_pattern = re.compile(r'\$\$([^$]+)\$\$|\\\[([^\]]+)\\\]', re.DOTALL)
        
        # Pattern for inline math: $...$ or \(...\)
        inline_pattern = re.compile(r'\$([^$]+)\$|\\\(([^\)]+)\\\)')
        
        # Pattern for equation tags: \tag{...}
        tag_pattern = re.compile(r'\\tag\{([^}]+)\}')
        
        # Pattern for boxed formulas: \boxed{...}
        boxed_pattern = re.compile(r'\\boxed\{([^}]+)\}')
        
        # Find all display math blocks
        for match in display_pattern.finditer(content):
            latex = match.group(1) or match.group(2)
            start_pos = match.start()
            
            # Find line number
            line_num = content[:start_pos].count('\n') + 1
            
            # Find surrounding context for section
            context_start = max(0, start_pos - 500)
            context_end = min(len(content), start_pos + 500)
            context = content[context_start:context_end]
            
            # Extract section heading
            section_match = re.search(r'^#{1,4}\s+(.+)$', context[:context_start][::-1], re.MULTILINE)
            if section_match:
                current_section = section_match.group(1)[::-1].strip()
            
            # Extract equation number
            eq_num = None
            tag_match = tag_pattern.search(latex)
            if tag_match:
                eq_num = tag_match.group(1).strip()
            
            # Check if boxed (important formula)
            is_boxed = bool(boxed_pattern.search(latex))
            
            # Determine formula type
            formula_type = self._classify_formula_type(latex, context)
            
            # Determine physical domain
            domain = self._classify_domain(latex, context, phase_name)
            
            # Extract dependencies (equation numbers referenced)
            dependencies = self._extract_dependencies(latex, context)
            
            # Create formula
            self.formula_counter += 1
            formula_id = f"F{self.formula_counter:05d}"
            
            formula = Formula(
                formula_id=formula_id,
                phase_doc=phase_name,
                section=current_section,
                equation_number=eq_num or "",
                latex=latex.strip(),
                formula_type=formula_type,
                physical_domain=domain,
                dependencies=dependencies,
                description=self._extract_description(context),
                line_number=line_num
            )
            
            formulas.append(formula)
        
        return formulas
    
    def _classify_formula_type(self, latex: str, context: str) -> str:
        """Classify formula as definition, derivation, prediction, or constant."""
        latex_lower = latex.lower()
        context_lower = context.lower()
        
        if any(word in context_lower for word in ['define', 'definition', 'let', '≡', '=']):
            return 'definition'
        elif any(word in context_lower for word in ['derive', 'derivation', 'from', 'using', 'substitute']):
            return 'derivation'
        elif any(word in context_lower for word in ['predict', 'prediction', 'test', 'validation', 'compare']):
            return 'prediction'
        elif any(word in latex_lower for word in ['=', '≈', '~', '∝']) and len(latex) < 100:
            return 'constant'
        else:
            return 'derivation'  # default
    
    def _classify_domain(self, latex: str, context: str, phase_name: str) -> str:
        """Classify physical domain based on keywords."""
        text = (latex + ' ' + context + ' ' + phase_name).lower()
        
        scores = {}
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[domain] = score
        
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        return 'general'
    
    def _extract_dependencies(self, latex: str, context: str) -> List[str]:
        """Extract equation numbers this formula depends on."""
        dependencies = []
        
        # Look for references like "Eq. 2.5" or "from Eq. 1.3"
        eq_ref_pattern = re.compile(r'(?:eq|equation|from|using|substitute).*?(\d+\.\d+[a-z]?)', re.IGNORECASE)
        
        text = latex + ' ' + context
        for match in eq_ref_pattern.finditer(text):
            dep = match.group(1)
            if dep not in dependencies:
                dependencies.append(dep)
        
        return dependencies
    
    def _extract_description(self, context: str) -> str:
        """Extract a brief description from surrounding context."""
        # Try to find a sentence before or after the formula
        sentences = re.split(r'[.!?]\s+', context)
        for sentence in sentences[:3]:  # First few sentences
            if len(sentence) > 20 and len(sentence) < 200:
                return sentence.strip()
        return ""
    
    def process_all_phases(self):
        """Process all Phase documents in the directory."""
        phase_files = sorted(self.phase_dir.glob("Phase_*.md"))
        
        print(f"Found {len(phase_files)} Phase documents")
        
        for phase_file in phase_files:
            print(f"Processing {phase_file.name}...")
            formulas = self.extract_formulas_from_file(phase_file)
            self.formulas.extend(formulas)
            print(f"  Extracted {len(formulas)} formulas")
        
        print(f"\nTotal formulas extracted: {len(self.formulas)}")
    
    def generate_registry(self, output_file: str):
        """Generate JSON registry of all formulas."""
        registry = {
            'metadata': {
                'total_formulas': len(self.formulas),
                'extraction_date': str(Path().cwd()),
                'phase_documents_processed': len(set(f.phase_doc for f in self.formulas))
            },
            'formulas': [asdict(f) for f in self.formulas],
            'statistics': self._generate_statistics()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        
        print(f"\nRegistry saved to {output_file}")
    
    def _generate_statistics(self) -> Dict:
        """Generate statistics about extracted formulas."""
        stats = {
            'by_phase': defaultdict(int),
            'by_domain': defaultdict(int),
            'by_type': defaultdict(int),
            'with_equation_numbers': 0,
            'with_dependencies': 0
        }
        
        for formula in self.formulas:
            stats['by_phase'][formula.phase_doc] += 1
            stats['by_domain'][formula.physical_domain] += 1
            stats['by_type'][formula.formula_type] += 1
            
            if formula.equation_number:
                stats['with_equation_numbers'] += 1
            if formula.dependencies:
                stats['with_dependencies'] += 1
        
        return dict(stats)

def main():
    """Main execution function."""
    # Path to Phase documents
    phase_dir = Path(__file__).parent.parent / "Papers" / "SDT_Foundation" / "Part_I_Axioms_and_Core_Equations"
    
    if not phase_dir.exists():
        print(f"Error: Phase directory not found: {phase_dir}")
        return
    
    # Create extractor
    extractor = FormulaExtractor(str(phase_dir))
    
    # Process all phases
    extractor.process_all_phases()
    
    # Generate registry
    output_file = Path(__file__).parent.parent / "formula_registry.json"
    extractor.generate_registry(str(output_file))
    
    # Print summary
    print("\n" + "="*60)
    print("EXTRACTION SUMMARY")
    print("="*60)
    stats = extractor._generate_statistics()
    print(f"\nTotal formulas: {len(extractor.formulas)}")
    print(f"\nBy domain:")
    for domain, count in sorted(stats['by_domain'].items(), key=lambda x: -x[1]):
        print(f"  {domain}: {count}")
    print(f"\nBy type:")
    for ftype, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
        print(f"  {ftype}: {count}")
    print(f"\nTop phases by formula count:")
    for phase, count in sorted(stats['by_phase'].items(), key=lambda x: -x[1])[:10]:
        print(f"  {phase}: {count}")

if __name__ == '__main__':
    main()

