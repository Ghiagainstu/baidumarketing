#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量修复所有博客文件的链接格式"""
import glob

fixes = {
    'href="/blog"': 'href="/blog.html"',
    'href="/contact"': 'href="/contact.html"',
    'href="/privacy"': 'href="/privacy.html"',
    'href="/terms"': 'href="/terms.html"',
}

total = 0
for path in sorted(glob.glob('blog/*.html')):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    file_fixes = 0
    for old, new in fixes.items():
        count = html.count(old)
        if count:
            html = html.replace(old, new)
            file_fixes += count
    
    if file_fixes:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        total += file_fixes
        slug = path.split('/')[-1]
        print(f"✅ {slug}: {file_fixes} 处修复")

print(f"\n总计: {total} 处修复")
