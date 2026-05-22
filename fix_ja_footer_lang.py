#!/usr/bin/env python3
"""修复 JA 博客 footer-lang 中的反斜杠 bug"""
import glob

count = 0
for path in sorted(glob.glob('ja/blog/*.html')):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    fixed = 0
    
    # Fix footer-lang links: /blog/blog\SLUG → /blog/SLUG
    import re
    # Match: href="/blog/blog\SLUG" or href="/ja/blog/blog\SLUG"
    # Replace the backslash part
    for old, new in [
        ('/blog/blog\\', '/blog/'),
        ('/ja/blog/blog\\', '/ja/blog/'),
    ]:
        count_old = html.count(old)
        if count_old > 0:
            html = html.replace(old, new)
            fixed += count_old
    
    if fixed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1
        print(f'  ✅ {path.replace("\\", "/").split("/")[-1]}: {fixed} 处')

print(f'\n修复: {count} 个文件')
