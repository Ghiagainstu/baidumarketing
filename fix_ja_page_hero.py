#!/usr/bin/env python3
"""fix_ja_page_hero.py — Remove stray page-hero section from JA blog pages"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))

def fix_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remove the stray page-hero section
    pattern = r'<section class="page-hero">\s*<div class="container">\s*(?:<span[^>]*>[^<]*</span>\s*)?</div>\s*</section>'
    new_html = re.sub(pattern, '', html)
    
    if new_html != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        return True
    return False

count = 0
for f in glob.glob(os.path.join(ROOT, 'ja', 'blog', '*.html')):
    if '_template' in f:
        continue
    if fix_page(f):
        count += 1
        print(f'  ✅ {os.path.relpath(f, ROOT)}')

print(f'\n✅ Total: {count} pages fixed')
