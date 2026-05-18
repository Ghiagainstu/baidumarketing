#!/usr/bin/env python3
"""
Batch fix for blog files:
1. Add theme-toggle dark mode CSS (missing in 64 files)
2. Fix related article links (absolute → relative)
3. Fix breadcrumb links
"""

import os, re

BLOG = "c:/Users/HYE/WorkBuddy/20260411211839/blog"

def fix_theme_toggle_css(content):
    """Add missing theme-toggle dark mode CSS rules"""
    if '[data-theme="dark"] .theme-toggle .icon-sun' in content:
        return content  # Already fixed
    
    # Add the missing rules before /* Nav mobile */ or @media
    missing_css = '''
    [data-theme="dark"] .theme-toggle .icon-sun { display: block; }
    [data-theme="dark"] .theme-toggle .icon-moon { display: none; }
    .theme-toggle .icon-sun { display: none; }
    .theme-toggle .icon-moon { display: block; }
'''
    
    # Try to insert before /* Nav mobile */ or @media
    if '/* Nav mobile */' in content:
        content = content.replace('    /* Nav mobile */', missing_css + '    /* Nav mobile */')
    elif '@media (max-width: 768px)' in content:
        content = content.replace('    @media (max-width: 768px)', missing_css + '    @media (max-width: 768px)')
    elif '@media (max-width: 900px)' in content:
        content = content.replace('    @media (max-width: 900px)', missing_css + '    @media (max-width: 900px)')
    
    return content

def fix_related_links(content):
    """Convert absolute related article links to relative paths"""
    # Pattern: href="https://baidumarketing.com/blog/slug.html"
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
    fixed_files = []
    
    for f in sorted(os.listdir(BLOG)):
        if not f.endswith('.html'):
            continue
        
        filepath = os.path.join(BLOG, f)
        try:
            if process_file(filepath):
                fixed_files.append(f)
        except Exception as e:
            print(f"ERROR {f}: {e}")
    
    print(f"\n✅ Fixed {len(fixed_files)} files:")
    for f in fixed_files[:10]:
        print(f"  - {f}")
    if len(fixed_files) > 10:
        print(f"  ... and {len(fixed_files) - 10} more")

if __name__ == '__main__':
    main()
