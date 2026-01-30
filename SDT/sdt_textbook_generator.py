#!/usr/bin/env python3
"""
SDT Textbook Generator
Generates a comprehensive textbook-style document from the SDT codebase
covering particles, atoms, nuclear binding, and the facilitator role of electrons.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TextbookChapter:
    """Represents a chapter in the SDT textbook"""
    title: str
    sections: List[Dict[str, Any]] = field(default_factory=list)
    order: int = 0

@dataclass
class TextbookSection:
    """Represents a section within a chapter"""
    title: str
    content: str = ""
    subsections: List[Dict[str, Any]] = field(default_factory=list)
    equations: List[str] = field(default_factory=list)
    figures: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)

class SDTTextbookGenerator:
    """Generates a comprehensive textbook from SDT codebase"""

    def __init__(self, sdt_root: str = "SDT"):
        self.sdt_root = Path(sdt_root)
        self.chapters: Dict[str, TextbookChapter] = {}
        self.equation_counter = 0
        self.figure_counter = 0

    def extract_content_from_papers(self) -> None:
        """Extract content from SDT foundation papers"""
        papers_dir = self.sdt_root / "Papers" / "SDT_Foundation" / "Part_I_Axioms_and_Core_Equations"

        if not papers_dir.exists():
            print(f"Papers directory not found: {papers_dir}")
            return

        # Process each domain
        domains = {
            "00_Foundations": "Foundations",
            "01_Atomic_Physics": "Atomic Physics",
            "02_Electromagnetism": "Electromagnetism",
            "03_Gravitation_and_Cosmology": "Gravitation and Cosmology",
            "04_Thermodynamics": "Thermodynamics",
            "05_Chemistry": "Chemistry",
            "06_Nuclear_Physics": "Nuclear Physics"
        }

        for domain_dir, domain_name in domains.items():
            domain_path = papers_dir / domain_dir
            if domain_path.exists():
                self._process_domain(domain_path, domain_name)

    def _process_domain(self, domain_path: Path, domain_name: str) -> None:
        """Process a single domain directory"""
        chapter = TextbookChapter(title=domain_name, order=len(self.chapters))
        self.chapters[domain_name] = chapter

        # Find all markdown files in this domain
        md_files = list(domain_path.rglob("*.md"))

        for md_file in sorted(md_files):
            if md_file.name == "README.md":
                continue

            try:
                content = md_file.read_text(encoding='utf-8')
                section = self._parse_markdown_section(content, md_file.stem)
                if section:
                    chapter.sections.append(section)
            except Exception as e:
                print(f"Error processing {md_file}: {e}")

    def _parse_markdown_section(self, content: str, title: str) -> Optional[Dict[str, Any]]:
        """Parse markdown content into a textbook section"""
        if not content.strip():
            return None

        # Extract equations (LaTeX math)
        equations = re.findall(r'\$\$([^$]+)\$\$', content)

        # Extract key concepts and theorems
        theorems = re.findall(r'### Theorem.*?:(.*?)(?=\n)', content, re.DOTALL)
        definitions = re.findall(r'### Definition.*?:(.*?)(?=\n)', content, re.DOTALL)

        # Clean up content for textbook format
        cleaned_content = self._clean_markdown_content(content)

        return {
            "title": title.replace('_', ' ').title(),
            "content": cleaned_content,
            "equations": equations,
            "theorems": theorems,
            "definitions": definitions,
            "source_file": title
        }

    def _clean_markdown_content(self, content: str) -> str:
        """Clean markdown content for textbook format"""
        # Remove markdown headers, links, etc.
        content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        content = re.sub(r'\*\*([^\*]+)\*\*', r'\1', content)
        content = re.sub(r'\*([^\*]+)\*', r'\1', content)

        return content.strip()

    def extract_nuclear_calculator_info(self) -> None:
        """Extract information from nuclear calculator"""
        calc_file = self.sdt_root / "Code" / "sdt_navier_cpp" / "NUCLEAR_CALCULATOR_README.md"
        if calc_file.exists():
            content = calc_file.read_text(encoding='utf-8')
            section = self._parse_markdown_section(content, "Nuclear Calculator Validation")

            if "Nuclear Physics" in self.chapters:
                self.chapters["Nuclear Physics"].sections.append(section)

    def generate_textbook_structure(self) -> None:
        """Generate the overall textbook structure"""
        # Create main chapters in logical order
        textbook_structure = [
            "Foundations",
            "Nuclear Physics",
            "Atomic Physics",
            "Chemistry",
            "Electromagnetism",
            "Thermodynamics",
            "Gravitation and Cosmology"
        ]

        # Add introduction chapter
        intro_chapter = TextbookChapter(title="Introduction to Spatial Displacement Theory", order=0)
        intro_content = self._generate_introduction()
        intro_chapter.sections.append({
            "title": "What is SDT?",
            "content": intro_content,
            "equations": [],
            "theorems": [],
            "definitions": []
        })
        self.chapters["Introduction"] = intro_chapter

        # Reorder chapters according to textbook structure
        ordered_chapters = {}
        for i, chapter_name in enumerate(["Introduction"] + textbook_structure):
            if chapter_name in self.chapters:
                chapter = self.chapters[chapter_name]
                chapter.order = i
                ordered_chapters[chapter_name] = chapter

        self.chapters = ordered_chapters

    def _generate_introduction(self) -> str:
        """Generate the introduction chapter content"""
        return """
Spatial Displacement Theory (SDT) represents a fundamental rethinking of physics, starting from the question:
"What actually exists in physical space?"

Rather than constructing abstract mathematical formalisms, SDT begins with four irreducible primitives that emerge
directly from physical reality:

1. **SPACE (Spation)**: An incompressible, inviscid superfluid medium filling all space continuously
2. **MATTER (Displacement)**: Geometric structures that exclude spation volume, creating pressure deficits
3. **MOVEMENT (Shunt Dynamics)**: Discrete micro-collisions between matter boundaries and spation
4. **NOW (Time Emergence)**: Time emerges from counting shunt events

From these primitives emerges a single master equation that unifies all physical phenomena:

Ė = P_CMB × A_eff × Γ × κ × (1-η)

This equation describes energy transfer through pressure-mediated geometric interactions, ultimately driven by
the continuous influx of CMB radiation.

**Key Insights:**
- Nuclear binding is the driver of all chemical and physical properties
- Electrons act as facilitators, enabling nuclear geometry to express itself
- All forces emerge from pressure gradients in the spation medium
- Mass and charge are derived quantities, not fundamental properties
- The universe operates through geometric rather than probabilistic mechanisms
"""

    def generate_latex_document(self) -> str:
        """Generate LaTeX textbook document"""
        latex_content = self._generate_latex_preamble()

        # Generate table of contents
        latex_content += "\\tableofcontents\n\\newpage\n\n"

        # Generate chapters
        for chapter_name in sorted(self.chapters.keys(), key=lambda x: self.chapters[x].order):
            chapter = self.chapters[chapter_name]
            latex_content += self._generate_chapter_latex(chapter)

        latex_content += "\\end{document}"

        return latex_content

    def _generate_latex_preamble(self) -> str:
        """Generate LaTeX document preamble"""
        return """\\documentclass[11pt,a4paper]{book}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{amsmath,amssymb,amsthm}
\\usepackage{graphicx}
\\usepackage{hyperref}
\\usepackage{geometry}
\\usepackage{fancyhdr}
\\usepackage{listings}
\\usepackage{xcolor}

\\geometry{margin=1in}

% Define theorem environments
\\newtheorem{theorem}{Theorem}[chapter]
\\newtheorem{definition}{Definition}[chapter]
\\newtheorem{lemma}{Lemma}[chapter]
\\newtheorem{corollary}{Corollary}[chapter]

% Code highlighting
\\lstset{
    language=Python,
    basicstyle=\\ttfamily\\footnotesize,
    keywordstyle=\\color{blue},
    commentstyle=\\color{green!60!black},
    stringstyle=\\color{red},
    numbers=left,
    numberstyle=\\tiny,
    frame=single,
    breaklines=true
}

\\title{Spatial Displacement Theory\\\\A Geometric Approach to Physics}
\\author{James C. Harvey}
\\date{\\today}

\\begin{document}

\\maketitle
\\newpage

\\begin{abstract}
This textbook presents Spatial Displacement Theory (SDT), a comprehensive framework for understanding
physical reality based on four irreducible primitives: SPACE, MATTER, MOVEMENT, and NOW.

From these primitives emerges a single master equation that unifies all physical phenomena, from nuclear
binding to galactic rotation. Nuclear structures drive chemical properties, while electrons facilitate
the expression of nuclear geometry.

All physical quantities—energy, momentum, force, mass, temperature, entropy—are derived from geometric
interactions in the spation medium, with no fundamental constants required beyond the CMB energy source.
\\end{abstract}

\\newpage
"""

    def _generate_chapter_latex(self, chapter: TextbookChapter) -> str:
        """Generate LaTeX for a single chapter"""
        latex = f"\\chapter{{{chapter.title}}}\n\n"

        for section in chapter.sections:
            latex += f"\\section{{{section['title']}}}\n\n"
            latex += self._format_content_for_latex(section['content'])
            latex += "\n\n"

            # Add equations
            for eq in section.get('equations', []):
                self.equation_counter += 1
                latex += f"\\begin{{equation}}\n{eq}\n\\end{{equation}}\n\n"

            # Add theorems and definitions
            for theorem in section.get('theorems', []):
                latex += f"\\begin{{theorem}}\n{theorem.strip()}\n\\end{{theorem}}\n\n"

            for definition in section.get('definitions', []):
                latex += f"\\begin{{definition}}\n{definition.strip()}\n\\end{{definition}}\n\n"

        return latex

    def _format_content_for_latex(self, content: str) -> str:
        """Format plain text content for LaTeX"""
        # Basic LaTeX escaping
        content = content.replace('&', '\\&')
        content = content.replace('%', '\\%')
        content = content.replace('$', '\\$')
        content = content.replace('#', '\\#')
        content = content.replace('_', '\\_')
        content = content.replace('^', '\\^')

        # Convert markdown-style formatting
        content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
        content = re.sub(r'\*(.*?)\*', r'\\textit{\1}', content)

        return content

    def save_textbook(self, output_file: str = "sdt_textbook.tex") -> None:
        """Save the generated textbook to file"""
        latex_content = self.generate_latex_document()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)

        print(f"Textbook saved to {output_file}")
        print(f"Generated {len(self.chapters)} chapters")
        print(f"Total equations: {self.equation_counter}")

    def audit_file_chain(self) -> Dict[str, Any]:
        """Audit the entire file chain for consistency"""
        audit_results = {
            "total_files": 0,
            "paper_files": 0,
            "code_files": 0,
            "website_files": 0,
            "consistency_issues": [],
            "missing_references": [],
            "orphaned_files": []
        }

        # Count files by type
        for root, dirs, files in os.walk(self.sdt_root):
            for file in files:
                audit_results["total_files"] += 1
                if "Papers" in root:
                    audit_results["paper_files"] += 1
                elif "Code" in root:
                    audit_results["code_files"] += 1
                elif "website" in root:
                    audit_results["website_files"] += 1

        # Check for consistency issues
        self._check_consistency(audit_results)

        return audit_results

    def _check_consistency(self, audit_results: Dict[str, Any]) -> None:
        """Check for consistency issues in the codebase"""
        # Check if all referenced papers exist
        papers_dir = self.sdt_root / "Papers" / "SDT_Foundation" / "Part_I_Axioms_and_Core_Equations"
        if papers_dir.exists():
            for domain_dir in papers_dir.iterdir():
                if domain_dir.is_dir():
                    for paper_dir in domain_dir.iterdir():
                        if paper_dir.is_dir():
                            md_files = list(paper_dir.glob("*.md"))
                            if not md_files:
                                audit_results["missing_references"].append(f"No markdown file in {paper_dir}")

        # Check for orphaned files
        # This would require more complex analysis

    def integrate_with_nuclear_calculator(self) -> None:
        """Integrate the textbook with the nuclear calculator"""
        # This would create a combined system where the calculator includes textbook content
        calculator_dir = self.sdt_root / "Code" / "sdt_navier_cpp"

        # Create an integrated documentation file
        integrated_file = calculator_dir / "SDT_TEXTBOOK_INTEGRATION.md"

        textbook_content = "# SDT Textbook Integration\n\n"
        textbook_content += "This nuclear calculator includes integrated textbook content from Spatial Displacement Theory.\n\n"

        # Add key concepts from the textbook
        for chapter_name, chapter in self.chapters.items():
            textbook_content += f"## {chapter.title}\n\n"
            for section in chapter.sections[:2]:  # Just first 2 sections per chapter for brevity
                textbook_content += f"### {section['title']}\n\n"
                textbook_content += section['content'][:500] + "...\n\n"

        with open(integrated_file, 'w', encoding='utf-8') as f:
            f.write(textbook_content)

        print(f"Integrated textbook saved to {integrated_file}")

def main():
    """Main function to generate SDT textbook"""
    print("SDT Textbook Generator")
    print("======================")

    generator = SDTTextbookGenerator()

    print("1. Extracting content from foundation papers...")
    generator.extract_content_from_papers()

    print("2. Extracting nuclear calculator information...")
    generator.extract_nuclear_calculator_info()

    print("3. Generating textbook structure...")
    generator.generate_textbook_structure()

    print("4. Saving textbook...")
    generator.save_textbook("SDT/sdt_textbook.tex")

    print("5. Auditing file chain...")
    audit = generator.audit_file_chain()
    print(f"   Total files: {audit['total_files']}")
    print(f"   Paper files: {audit['paper_files']}")
    print(f"   Code files: {audit['code_files']}")
    print(f"   Website files: {audit['website_files']}")

    print("6. Integrating with nuclear calculator...")
    generator.integrate_with_nuclear_calculator()

    print("\nTextbook generation complete!")
    print("Files created:")
    print("  - SDT/sdt_textbook.tex (main textbook)")
    print("  - SDT/Code/sdt_navier_cpp/SDT_TEXTBOOK_INTEGRATION.md (integrated documentation)")

if __name__ == "__main__":
    main()
