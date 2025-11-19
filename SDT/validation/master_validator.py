#!/usr/bin/env python3
"""
SDT Master Validator
Orchestrates all validation agents and generates comprehensive reports.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from dimensional_validator import DimensionalValidator
from numerical_validator import NumericalValidator

class MasterValidator:
    """Orchestrates all validation processes."""
    
    def __init__(self, base_dir: Path, tolerance: float = 0.008):
        self.base_dir = base_dir
        self.tolerance = tolerance
        self.validation_dir = base_dir / 'SDT' / 'validation'
        self.db_path = self.validation_dir / 'formula_database.json'
        
        # Results storage
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tolerance_percent': tolerance * 100,
            'total_formulas': 0,
            'dimensional_errors': [],
            'numerical_errors': [],
            'summary': {}
        }
    
    def run_dimensional_validation(self):
        """Run dimensional analysis validation."""
        print("\n" + "="*70)
        print("PHASE 2.1: DIMENSIONAL ANALYSIS VALIDATION")
        print("="*70)
        
        validator = DimensionalValidator(str(self.db_path))
        errors = validator.validate_all()
        
        error_path = self.validation_dir / 'dimensional_errors.json'
        validator.save_error_report(str(error_path))
        
        self.results['dimensional_errors'] = errors
        return errors
    
    def run_numerical_validation(self):
        """Run numerical verification validation."""
        print("\n" + "="*70)
        print("PHASE 2.2: NUMERICAL VERIFICATION VALIDATION")
        print("="*70)
        
        validator = NumericalValidator(str(self.db_path), tolerance=self.tolerance)
        errors = validator.validate_all()
        
        error_path = self.validation_dir / 'numerical_errors.json'
        validator.save_error_report(str(error_path))
        
        self.results['numerical_errors'] = errors
        return errors
    
    def generate_summary(self):
        """Generate validation summary statistics."""
        # Load formula database
        with open(self.db_path, 'r', encoding='utf-8') as f:
            db = json.load(f)
        
        total_formulas = db.get('total_formulas', 0)
        self.results['total_formulas'] = total_formulas
        
        dim_errors = len(self.results['dimensional_errors'])
        num_errors = len(self.results['numerical_errors'])
        
        # Count by severity
        critical_num = len([e for e in self.results['numerical_errors'] 
                          if isinstance(e, dict) and e.get('severity') == 'CRITICAL'])
        major_num = len([e for e in self.results['numerical_errors'] 
                        if isinstance(e, dict) and e.get('severity') == 'MAJOR'])
        
        self.results['summary'] = {
            'total_formulas': total_formulas,
            'dimensional_errors': dim_errors,
            'numerical_errors': num_errors,
            'critical_errors': critical_num,
            'major_errors': major_num,
            'validation_rate': (total_formulas - num_errors) / total_formulas * 100 if total_formulas > 0 else 0,
            'within_tolerance_rate': (total_formulas - critical_num) / total_formulas * 100 if total_formulas > 0 else 0
        }
    
    def save_validation_report(self):
        """Save comprehensive validation report."""
        report_path = self.validation_dir / 'validation_report.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# SDT Formula Validation Report\n\n")
            f.write(f"**Generated:** {self.results['timestamp']}\n\n")
            f.write(f"**Tolerance Standard:** {self.results['tolerance_percent']:.1f}%\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Total Formulas Validated:** {self.results['summary']['total_formulas']}\n")
            f.write(f"- **Dimensional Errors:** {self.results['summary']['dimensional_errors']}\n")
            f.write(f"- **Numerical Errors:** {self.results['summary']['numerical_errors']}\n")
            f.write(f"- **Critical Errors (>0.8%):** {self.results['summary']['critical_errors']}\n")
            f.write(f"- **Major Errors:** {self.results['summary']['major_errors']}\n")
            f.write(f"- **Validation Rate:** {self.results['summary']['validation_rate']:.2f}%\n")
            f.write(f"- **Within Tolerance Rate:** {self.results['summary']['within_tolerance_rate']:.2f}%\n\n")
            
            f.write("## Error Details\n\n")
            f.write("See individual error reports:\n")
            f.write("- `dimensional_errors.json` - Dimensional consistency issues\n")
            f.write("- `numerical_errors.json` - Numerical accuracy issues\n\n")
            
            f.write("## Next Steps\n\n")
            f.write("1. Review and fix critical errors (>0.8% tolerance violations)\n")
            f.write("2. Address major errors (benchmark tolerance violations)\n")
            f.write("3. Document minor errors (unknown-variable domains)\n")
            f.write("4. Re-run validation after fixes\n")
        
        # Also save JSON version
        json_path = self.validation_dir / 'validation_report.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\nValidation report saved to {report_path}")
    
    def run_all(self):
        """Run all validation phases."""
        print("="*70)
        print("SDT FORMULA VALIDATION - MASTER VALIDATOR")
        print("="*70)
        print(f"Tolerance: {self.tolerance*100:.1f}%")
        print(f"Formula Database: {self.db_path}")
        
        # Phase 2.1: Dimensional Analysis
        self.run_dimensional_validation()
        
        # Phase 2.2: Numerical Verification
        self.run_numerical_validation()
        
        # Generate summary
        self.generate_summary()
        
        # Save report
        self.save_validation_report()
        
        print("\n" + "="*70)
        print("VALIDATION COMPLETE")
        print("="*70)
        print(f"Total formulas: {self.results['summary']['total_formulas']}")
        print(f"Dimensional errors: {self.results['summary']['dimensional_errors']}")
        print(f"Numerical errors: {self.results['summary']['numerical_errors']}")
        print(f"Critical errors: {self.results['summary']['critical_errors']}")

def main():
    """Main entry point."""
    base_dir = Path(__file__).parent.parent.parent
    validator = MasterValidator(base_dir, tolerance=0.008)
    validator.run_all()

if __name__ == '__main__':
    main()

