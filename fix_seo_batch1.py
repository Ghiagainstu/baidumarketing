#!/usr/bin/env python3
"""
Fix SEO tags for BPP website - Batch 1: Canonical + hreflang + x-default
Usage: python fix_seo_batch1.py
"""

import os
import re
from pathlib import Path

WORKSPACE = r"C:\Users\HYE\WorkBuddy\20260411211839"

def add_canonical_to_file(filepath, url_path):
    """Add canonical tag to HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if canonical already exists
    if 'rel="canonical"' in content:
        print(f"  ✓ Already has canonical: {filepath}")
        return False
    
    # Find the right place to insert canonical (after <title> tag)
    # Pattern: after <title>...</title> tag
    title_pattern = r'(<title>.*?</title>\s*)'
    
    canonical_tag = f'<link rel="canonical" href="https://www.baidumarketing.com{url_path}" />\n'
    
    # Insert after title tag
    new_content = re.sub(title_pattern, r'\1' + canonical_tag, content, count=1)
    
    if new_content == content:
        print(f"  ✗ Could not find insertion point: {filepath}")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ Added canonical: {filepath}")
    return True

def add_hreflang_to_blog(filepath, blog_slug, is_ja=False):
    """Add hreflang tags to blog HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if hreflang already exists
    if 'hreflang="en"' in content or "hreflang='en'" in content:
        print(f"  ✓ Already has hreflang: {filepath}")
        return False
    
    # Determine URLs
    if is_ja:
        en_url = f"https://www.baidumarketing.com/blog/{blog_slug}"
        ja_url = f"https://www.baidumarketing.com/ja/blog/{blog_slug}"
    else:
        en_url = f"https://www.baidumarketing.com/blog/{blog_slug}"
        ja_url = f"https://www.baidumarketing.com/ja/blog/{blog_slug}"
    
    # Find insertion point (after canonical tag or after title tag)
    canonical_pattern = r'(<link rel="canonical" href=".*?" />\s*)'
    title_pattern = r'(<title>.*?</title>\s*)'
    
    hreflang_tags = f'<link rel="alternate" hreflang="en" href="{en_url}" />\n'
    hreflang_tags += f'<link rel="alternate" hreflang="ja" href="{ja_url}" />\n'
    hreflang_tags += f'<link rel="alternate" hreflang="x-default" href="{en_url}" />\n'
    
    # Try to insert after canonical tag first
    new_content = re.sub(canonical_pattern, r'\1' + hreflang_tags, content, count=1)
    
    # If not found, insert after title tag
    if new_content == content:
        new_content = re.sub(title_pattern, r'\1' + hreflang_tags, content, count=1)
    
    if new_content == content:
        print(f"  ✗ Could not find insertion point: {filepath}")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ Added hreflang: {filepath}")
    return True

def main():
    print("="*80)
    print("Batch 1: Fixing canonical, hreflang, and x-default tags")
    print("="*80)
    
    # 1. Fix root directory files (add canonical)
    print("\n[1/2] Adding canonical tags to root files...")
    root_files = [
        ('about.html', '/about'),
        ('blog.html', '/blog'),
        ('china-geo.html', '/china-geo'),
        ('clients.html', '/clients'),
        ('contact.html', '/contact'),
        ('faq.html', '/faq'),
        ('features.html', '/features'),
        ('pricing.html', '/pricing'),
        ('privacy.html', '/privacy'),
        ('terms.html', '/terms'),
        ('why-baidu-ppc-pro.html', '/why-baidu-ppc-pro'),
    ]
    
    for filename, url_path in root_files:
        filepath = os.path.join(WORKSPACE, filename)
        if os.path.exists(filepath):
            add_canonical_to_file(filepath, url_path)
        else:
            print(f"  ✗ File not found: {filepath}")
    
    # 2. Fix blog files (add hreflang)
    print("\n[2/2] Adding hreflang tags to blog files...")
    blog_dir = os.path.join(WORKSPACE, 'blog')
    
    if os.path.exists(blog_dir):
        for filename in os.listdir(blog_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(blog_dir, filename)
                # Extract blog slug from filename
                blog_slug = filename.replace('.html', '')
                add_hreflang_to_blog(filepath, blog_slug, is_ja=False)
    
    # 3. Fix JA blog files (add hreflang)
    ja_blog_dir = os.path.join(WORKSPACE, 'ja', 'blog')
    
    if os.path.exists(ja_blog_dir):
        print("\n[3/3] Adding hreflang tags to JA blog files...")
        for filename in os.listdir(ja_blog_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(ja_blog_dir, filename)
                # Extract blog slug from filename
                blog_slug = filename.replace('.html', '')
                add_hreflang_to_blog(filepath, blog_slug, is_ja=True)
    
    print("\n" + "="*80)
    print("Batch 1 completed!")
    print("="*80)

if __name__ == '__main__':
    main()
