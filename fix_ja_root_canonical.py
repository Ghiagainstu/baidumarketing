#!/usr/bin/env python3
"""
Fix SEO tags for BPP website - Fix JA root files canonical
Usage: python fix_ja_root_canonical.py
"""

import os

WORKSPACE = r"C:\Users\HYE\WorkBuddy\20260411211839"

def add_canonical_to_ja_file(filepath, url_path):
    """Add canonical tag to JA HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if canonical already exists
    if 'rel="canonical"' in content:
        print(f"  ✓ Already has canonical: {os.path.basename(filepath)}")
        return False
    
    canonical_tag = f'<link rel="canonical" href="https://www.baidumarketing.com{url_path}" />\n'
    
    # Find insertion point (after title tag or at beginning of head)
    import re
    title_pattern = r'(<title>.*?</title>\s*)'
    head_pattern = r'(<head>\s*)'
    
    # Try to insert after title tag first
    new_content = re.sub(title_pattern, r'\1' + canonical_tag, content, count=1)
    
    # If not found, insert after <head> tag
    if new_content == content:
        new_content = re.sub(head_pattern, r'\1' + canonical_tag, content, count=1)
    
    if new_content == content:
        print(f"  ✗ Could not find insertion point: {os.path.basename(filepath)}")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ Added canonical: {os.path.basename(filepath)}")
    return True

def main():
    print("="*80)
    print("Fixing JA root files canonical tags")
    print("="*80)
    
    # JA root files mapping
    ja_files = [
        ('index.html', '/ja/'),
        ('about.html', '/ja/about'),
        ('blog.html', '/ja/blog'),
        ('china-geo.html', '/ja/china-geo'),
        ('clients.html', '/ja/clients'),
        ('contact.html', '/ja/contact'),
        ('faq.html', '/ja/faq'),
        ('features.html', '/ja/features'),
        ('pricing.html', '/ja/pricing'),
        ('why-baidu-ppc-pro.html', '/ja/why-baidu-ppc-pro'),
    ]
    
    for filename, url_path in ja_files:
        filepath = os.path.join(WORKSPACE, 'ja', filename)
        if os.path.exists(filepath):
            add_canonical_to_ja_file(filepath, url_path)
        else:
            print(f"  ✗ File not found: ja/{filename}")
    
    print("\n" + "="*80)
    print("JA root files canonical fix completed!")
    print("="*80)

if __name__ == '__main__':
    main()
