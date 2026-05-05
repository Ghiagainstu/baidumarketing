#!/usr/bin/env python3
"""修复所有HTML文件中 .nav-logo 缺少 white-space: nowrap 和 flex-shrink: 0 的问题"""

import os
import glob

def fix_file(filepath):
    """修复单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = False
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 查找 .nav-logo { 规则开始
        if '.nav-logo {' in line and '[data-theme' not in line:
            # 开始收集这个规则块
            rule_lines = [line]
            i += 1
            
            # 收集直到找到结束的 }
            brace_count = line.count('{') - line.count('}')
            while i < len(lines) and brace_count > 0:
                rule_lines.append(lines[i])
                brace_count += lines[i].count('{') - lines[i].count('}')
                i += 1
            
            # 检查是否需要添加 white-space 和 flex-shrink
            rule_text = ''.join(rule_lines)
            
            if 'white-space: nowrap' not in rule_text:
                # 在 transition 行后面插入 white-space 和 flex-shrink
                for j, rule_line in enumerate(rule_lines):
                    if 'transition: color var(--transition-base);' in rule_line:
                        # 在这行后面插入新行
                        rule_lines.insert(j + 1, '      white-space: nowrap;\n')
                        rule_lines.insert(j + 2, '      flex-shrink: 0;\n')
                        modified = True
                        break
            
            new_lines.extend(rule_lines)
        else:
            new_lines.append(line)
            i += 1
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

# 查找所有HTML文件
html_files = glob.glob('**/*.html', recursive=True)

# 排除 index.html（已经手动修复）
html_files = [f for f in html_files if 'index.html' not in f]

fixed_count = 0
for filepath in html_files:
    try:
        if fix_file(filepath):
            print(f"✓ 已修复: {filepath}")
            fixed_count += 1
    except Exception as e:
        print(f"✗ 失败: {filepath} - {e}")

print(f"\n总共修复了 {fixed_count} 个文件（index.html 已手动修复）")
