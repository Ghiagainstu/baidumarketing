#!/usr/bin/env python3
"""
Scan all HTML files for SEO tags (canonical, hreflang, x-default, schema)
Usage: python scan_seo_tags.py
"""

import os
import re
from pathlib import Path

WORKSPACE = r"C:\Users\HYE\WorkBuddy\20260411211839"

def scan_file(filepath):
    """Scan a single HTML file for SEO tags"""
    with open(filepath, 'r', encoding='utf-8') as f:
        # Read first 200 lines to speed up scanning
        lines = []
        for i, line in enumerate(f):
            if i >= 200:
                break
            lines.append(line)
    
    content = ''.join(lines)
    
    result = {
        'file': filepath.replace(WORKSPACE, ''),
        'canonical': 'canonical' in content.lower(),
        'hreflang_en': 'hreflang="en"' in content.lower() or "hreflang='en'" in content.lower(),
        'hreflang_ja': 'hreflang="ja"' in content.lower() or "hreflang='ja'" in content.lower(),
        'hreflang_x_default': 'hreflang="x-default"' in content.lower() or "hreflang='x-default'" in content.lower(),
        'schema_json_ld': 'application/ld+json' in content.lower(),
        'og_tags': 'property="og:' in content.lower(),
    }
    
    return result

def main():
    results = []
    
    # Scan root HTML files
    for file in os.listdir(WORKSPACE):
        if file.endswith('.html'):
            filepath = os.path.join(WORKSPACE, file)
            results.append(scan_file(filepath))
    
    # Scan blog directory
    blog_dir = os.path.join(WORKSPACE, 'blog')
    if os.path.exists(blog_dir):
        for file in os.listdir(blog_dir):
            if file.endswith('.html'):
                filepath = os.path.join(blog_dir, file)
                results.append(scan_file(filepath))
    
    # Scan ja directory
    ja_dir = os.path.join(WORKSPACE, 'ja')
    if os.path.exists(ja_dir):
        for file in os.listdir(ja_dir):
            if file.endswith('.html'):
                filepath = os.path.join(ja_dir, file)
                results.append(scan_file(filepath))
        
        # Scan ja/blog directory
        ja_blog_dir = os.path.join(ja_dir, 'blog')
        if os.path.exists(ja_blog_dir):
            for file in os.listdir(ja_blog_dir):
                if file.endswith('.html'):
                    filepath = os.path.join(ja_blog_dir, file)
                    results.append(scan_file(filepath))
    
    # Print results
    print(f"{'File':<50} {'Canonical':<10} {'hreflang-en':<12} {'hreflang-ja':<12} {'x-default':<12} {'Schema':<8} {'OG':<8}")
    print("-" * 120)
    
    for r in results:
        print(f"{r['file']:<50} {'✅' if r['canonical'] else '❌':<10} {'✅' if r['hreflang_en'] else '❌':<12} {'✅' if r['hreflang_ja'] else '❌':<12} {'✅' if r['hreflang_x_default'] else '❌':<12} {'✅' if r['schema_json_ld'] else '❌':<8} {'✅' if r['og_tags'] else '❌':<8}")
    
    # Summary
    total = len(results)
    canonical_count = sum(1 for r in results if r['canonical'])
    hreflang_en_count = sum(1 for r in results if r['hreflang_en'])
    
    print("\n" + "="*120)
    print(f"Summary: {total} files scanned")
    print(f"  Canonical tags: {canonical_count}/{total} ({canonical_count*100//total}%)")
    print(f"  hreflang-en: {hreflang_en_count}/{total} ({hreflang_en_count*100//total}%)")

if __name__ == '__main__':
    main()
