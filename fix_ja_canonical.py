#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 JA 博客 canonical URL：/blog/SLUG → /ja/blog/SLUG.html"""
import glob

count = 0
for path in sorted(glob.glob('ja/blog/*.html')):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    slug = path.replace('\\', '/').split('/')[-1].replace('.html', '')
    
    old_canon = f'rel="canonical" href="https://www.baidumarketing.com/blog/{slug}"'
    new_canon = f'rel="canonical" href="https://www.baidumarketing.com/ja/blog/{slug}.html"'
    
    found = old_canon in html
    if count == 0:
        print(f"DEBUG: slug={slug}")
        print(f"DEBUG: old={repr(old_canon)}")
        print(f"DEBUG: found={found}")
    
    if found:
        html = html.replace(old_canon, new_canon)
        count += 1
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✅ {path.split("/")[-1]}')

print(f'\n修复: {count} 个文件')
