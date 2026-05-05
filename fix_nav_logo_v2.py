#!/usr/bin/env python3
"""修复所有HTML文件中 .nav-logo 的 CSS，添加 white-space: nowrap 和 flex-shrink: 0"""

import glob

def fix_file(filepath):
    """修复单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 情况1: .nav-logo 规则在多行中（如 index.html）
    # 查找: transition: color var(--transition-base);
    # 后面没有 white-space: nowrap
    if '.nav-logo {' in content and 'white-space: nowrap' not in content:
        # 在 transition 行后面添加新属性
        old = 'transition: color var(--transition-base);'
        new = 'transition: color var(--transition-base);\n      white-space: nowrap;\n      flex-shrink: 0;'
        content = content.replace(old, new, 1)  # 只替换第一次出现
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# 查找所有HTML文件（排除 index.html 和 pricing.html，已手动修复）
html_files = glob.glob('**/*.html', recursive=True)
exclude = ['index.html', 'pricing.html']
html_files = [f for f in html_files if all(e not in f for e in exclude)]

fixed = 0
for f in html_files:
    try:
        if fix_file(f):
            print(f"✓ {f}")
            fixed += 1
    except Exception as e:
        print(f"✗ {f}: {e}")

print(f"\n修复了 {fixed} 个文件")
