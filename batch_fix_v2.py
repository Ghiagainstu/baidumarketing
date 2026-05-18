#!/usr/bin/env python3
"""
Batch fix for blog files - improved version
Insert theme-toggle dark mode CSS after .theme-toggle svg line
"""

import os, re

BLOG = "c:/Users/HYE/WorkBuddy/20260411211839/blog"

def fix_theme_toggle_css(content):
    """Add missing theme-toggle dark mode CSS rules after .theme-toggle svg line"""
    if '[data-theme="dark"] .theme-toggle .icon-sun' in content:
        return content  # Already fixed
    
    # Find .theme-toggle svg line and insert after it
    svg_line = '.theme-toggle svg { width: 18px; height: 18px; }'
    if svg_line in content:
        insert = '''
    [data-theme="dark"] .theme-toggle .icon-sun { display: block; }
    [data-theme="dark"] .theme-toggle .icon-moon { display: none; }
    .theme-toggle .icon-sun { display: none; }
    .theme-toggle .icon-moon { display: block; }
'''
        content = content.replace(svg_line, svg_line + insert)
        return content
    
    # Alternative: try to find the line with extra spaces
    pattern = r'\.theme-toggle svg\s*\{[^}]+\}'
    match = re.search(pattern, content)
    if match:
        line = match.group()
        insert = '''
    [data-theme="dark"] .theme-toggle .icon-sun { display: block; }
    [data-theme="dark"] .theme-toggle .icon-moon { display: none; }
    .theme-toggle .icon-sun { display: none; }
    .theme-toggle .icon-moon { display: block; }
'''
        content = content.replace(line, line + insert)
        return content
    
    return content

def fix_related_links(content):
    """Convert absolute related article links to relative paths"""
    pattern = r'href="https://baidumarketing\.com/blog/([^"]+)\.html"'
    
    def replacer(match):
        slug = match.group(1)
        return f'href="../{slug}"'
    
    content = re.sub(pattern, replacer, content)
    return content

def fix_breadcrumb(content):
    """Fix broken breadcrumb links"""
    content = content.replace('href="https://baidumarketing.com/.html"', 'href="../index"')
    content = content.replace('href="https://baidumarketing.com/blog.html"', 'href="../blog"')
    return content

def fix_cta_link(content):
    """Fix CTA button links"""
    content = re.sub(r'href="https://baidumarketing\.com/contact\.html"', 'href="../contact"', content)
    return content

def process_file(filepath):
    """Process a single blog file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Apply fixes
    content = fix_theme_toggle_css(content)
    content = fix_related_links(content)
    content = fix_breadcrumb(content)
    content = fix_cta_link(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    fixed_count = 0
    failed = []
    
    for f in sorted(os.listdir(BLOG)):
        if not f.endswith('.html'):
            continue
        
        filepath = os.path.join(BLOG, f)
        try:
            if process_file(filepath):
                fixed_count += 1
                print(f"Fixed: {f}")
        except Exception as e:
            failed.append((f, str(e)))
            print(f"ERROR {f}: {e}")
    
    print(f"\n✅ Total fixed: {fixed_count} files")
    if failed:
        print(f"\n❌ Failed: {len(failed)} files")
        for f, e in failed[:5]:
            print(f"  {f}: {e}")

if __name__ == '__main__':
    main()
