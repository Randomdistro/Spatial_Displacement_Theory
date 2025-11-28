import re
import os

files = [
    'Phase_1_Core_Engine_Mathematical_Proof.md',
    'Phase_2_Bonding_Geometry_Mathematical_Proof.md',
    'Phase_3_Properties_Reactions_Mathematical_Proof.md',
    'Phase_4_Compound_Designer_Mathematical_Proof.md',
    'Phase_5_Commercial_Features_Mathematical_Proof.md'
]

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
        total = len(content)
        numbers = len(re.findall(r'[0-9]', content))
        pct = 100 * numbers / total if total > 0 else 0
        print(f'{fname}: {total} chars, {numbers} numbers ({pct:.1f}%)')

