#!/usr/bin/env python3
"""
Fix SEO tags for BPP website - Supplemental: Add missing canonical to blog files
Usage: python fix_blog_canonical.py
"""

import os
import re

WORKSPACE = r"C:\Users\HYE\WorkBuddy\20260411211839"

def add_canonical_to_blog(filepath, blog_slug):
    """Add canonical tag to blog HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if canonical already exists
    if 'rel="canonical"' in content:
        print(f"  ✓ Already has canonical: {os.path.basename(filepath)}")
        return False
    
    # Determine if it's JA blog
    if '\ja\blog' in filepath or '\ja/blog' in filepath:
        canonical_url = f"https://www.baidumarketing.com/ja/blog/{blog_slug}"
    else:
        canonical_url = f"https://www.baidumarketing.com/blog/{blog_slug}"
    
    canonical_tag = f'<link rel="canonical" href="{canonical_url}" />\n'
    
    # Find insertion point (after title tag or at beginning of head)
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
    print("Supplemental fix: Adding canonical tags to blog files")
    print("="*80)
    
    # 1. Fix EN blog files
    print("\n[1/2] Processing EN blog files...")
    blog_dir = os.path.join(WORKSPACE, 'blog')
    
    if os.path.exists(blog_dir):
        for filename in os.listdir(blog_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(blog_dir, filename)
                blog_slug = filename.replace('.html', '')
                add_canonical_to_blog(filepath, blog_slug)
    
    # 2. Fix JA blog files
    print("\n[2/2] Processing JA blog files...")
    ja_blog_dir = os.path.join(WORKSPACE, 'ja', 'blog')
    
    if os.path.exists(ja_blog_dir):
        for filename in os.listdir(ja_blog_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(ja_blog_dir, filename)
                blog_slug = filename.replace('.html', '')
                add_canonical_to_blog(filepath, blog_slug)
    
    print("\n" + "="*80)
    print("Supplemental fix completed!")
    print("="*80)

if __name__ == '__main__':
    main()
