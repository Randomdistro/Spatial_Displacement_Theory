#!/usr/bin/env python3
"""
Concatenate all deprecated papers into a single amalgam file.
"""

import os
from pathlib import Path

# Base directory for deprecated papers
DEPRECATED_BASE = Path(__file__).parent.parent.parent / "Papers" / "SDT_Foundation" / "Deprecated_Papers"

# Output file
OUTPUT_DIR = Path(__file__).parent / "DEPRECATED_PAPERS_AMALGAM"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "DEPRECATED_PAPERS_COMPLETE_AMALGAM.md"

def find_all_markdown_files(base_path: Path) -> list[Path]:
    """Find all .md files recursively"""
    md_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    return sorted(md_files)

def read_file_safe(file_path: Path) -> str:
    """Read file with error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"[ERROR READING FILE: {e}]\n"

def concatenate_papers():
    """Main function to concatenate all deprecated papers"""
    
    print("="*80)
    print("CONCATENATING DEPRECATED PAPERS")
    print("="*80)
    print()
    
    # Find all markdown files
    md_files = find_all_markdown_files(DEPRECATED_BASE)
    
    print(f"Found {len(md_files)} markdown files")
    print()
    
    # Create output file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        # Write header
        out.write("# Deprecated Papers Complete Amalgam\n\n")
        out.write("**Date**: 2026-01-02\n")
        out.write(f"**Total Files**: {len(md_files)}\n")
        out.write("**Source**: SDT/Papers/SDT_Foundation/Deprecated_Papers/\n\n")
        out.write("This file contains all deprecated papers concatenated into a single document.\n")
        out.write("Files are organized by their original directory structure.\n\n")
        out.write("---\n\n")
        
        # Process each file
        for i, file_path in enumerate(md_files, 1):
            # Get relative path from deprecated base
            rel_path = file_path.relative_to(DEPRECATED_BASE)
            
            print(f"[{i}/{len(md_files)}] Processing: {rel_path}")
            
            # Write separator
            out.write("\n" + "="*80 + "\n")
            out.write(f"# File {i}/{len(md_files)}: {rel_path}\n")
            out.write("="*80 + "\n\n")
            
            # Read and write file content
            content = read_file_safe(file_path)
            out.write(content)
            
            # Add separator before next file
            out.write("\n\n" + "-"*80 + "\n\n")
    
    print()
    print("="*80)
    print("CONCATENATION COMPLETE")
    print("="*80)
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Total files processed: {len(md_files)}")
    print(f"Output file size: {OUTPUT_FILE.stat().st_size / 1024 / 1024:.2f} MB")
    print("="*80)

if __name__ == "__main__":
    concatenate_papers()
