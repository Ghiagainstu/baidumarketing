#!/usr/bin/env python3
"""批量修复所有HTML文件的 .nav-logo CSS"""

import glob

def fix_all():
    html_files = glob.glob('**/*.html', recursive=True)
    
    # 已经手动修复的文件
    manually_fixed = ['index.html', 'pricing.html', 'about.html']
    html_files = [f for f in html_files if all(e not in f for e in manually_fixed)]
    
    fixed = 0
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '.nav-logo {' in content and 'white-space: nowrap' not in content:
                # 查找 ".nav-logo {" 的位置
                start = content.find('.nav-logo {')
                
                # 从 start 开始，查找 "transition: color var(--transition-base);"
                rest = content[start:]
                trans_pos = rest.find('transition: color var(--transition-base);')
                
                if trans_pos != -1:
                    # 插入位置
                    insert_pos = start + trans_pos + len('transition: color var(--transition-base);')
                    
                    # 插入新属性
                    new_content = content[:insert_pos] + '\n      white-space: nowrap;\n      flex-shrink: 0;' + content[insert_pos:]
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"✓ {filepath}")
                    fixed += 1
        except Exception as e:
            print(f"✗ {filepath}: {e}")
    
    print(f"\n修复了 {fixed} 个文件")

if __name__ == '__main__':
    fix_all()
