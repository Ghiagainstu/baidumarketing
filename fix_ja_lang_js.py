#!/usr/bin/env python3
"""修复 JA 博客文件 lang-switch JS 类名不匹配（active→open）"""
import glob

count = 0
for path in sorted(glob.glob('ja/blog/*.html')):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    fixed = 0
    if "classList.toggle('active')" in html:
        html = html.replace("classList.toggle('active')", "classList.toggle('open')")
        fixed += 1
    if "classList.remove('active')" in html:
        html = html.replace("classList.remove('active')", "classList.remove('open')")
        fixed += 1
    
    if fixed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1
        print(f"  ✅ {path.split('/')[-1]}: {fixed} 处")

print(f"\n修复: {count} 个文件")
