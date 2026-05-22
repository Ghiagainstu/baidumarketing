"""Add GA4 tracking code to all HTML files in the BPP project."""
import os
import re
import glob

GA4_CODE = '''  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-TCGE7NJT7H"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-TCGE7NJT7H');
  </script>
'''

PROJECT_ROOT = r'c:\Users\HYE\WorkBuddy\20260411211839'
EXCLUDE_DIRS = ['.workbuddy', 'node_modules']

# Track stats
total = 0
skipped = 0
modified = 0
errors = 0

html_files = glob.glob(os.path.join(PROJECT_ROOT, '**', '*.html'), recursive=True)

for filepath in html_files:
    # Skip excluded dirs
    if any(f'\\{d}\\' in filepath for d in EXCLUDE_DIRS):
        continue
    
    total += 1
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if GA4 already present
    if 'G-TCGE7NJT7H' in content:
        skipped += 1
        print(f'[SKIP] Already present: {os.path.relpath(filepath, PROJECT_ROOT)}')
        continue
    
    # Insert GA4 right after <head> or <head ...> tag
    # Handle both: <head> and <html lang="en"><head>
    pattern = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
    match = pattern.search(content)
    
    if not match:
        errors += 1
        print(f'[ERROR] No <head> found: {os.path.relpath(filepath, PROJECT_ROOT)}')
        continue
    
    head_tag = match.group(0)
    insert_pos = match.end()
    
    new_content = content[:insert_pos] + '\n' + GA4_CODE + content[insert_pos:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    modified += 1
    print(f'[OK] {os.path.relpath(filepath, PROJECT_ROOT)}')

print(f'\n=== Summary ===')
print(f'Total HTML files: {total}')
print(f'Modified: {modified}')
print(f'Skipped (already present): {skipped}')
print(f'Errors: {errors}')
