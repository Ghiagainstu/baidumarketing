#!/usr/bin/env python3
"""
final_fix.py - 修复剩余问题：
1. 添加 footer-lang (如果缺失)
2. 缩短 title 到 ≤70 字符
"""
import sys
import re
import os

def fix_file(path):
    with open(path, 'r', encoding='utf8') as f:
        html = f.read()
    
    slug = os.path.basename(path).replace('.html', '')
    modified = False
    
    # === 修复1: 添加 footer-lang (如果缺失) ===
    footer_lang_count = html.count('<div class="footer-lang">')
    if footer_lang_count == 0:
        # 在 footer-social 之前添加
        # 尝试多种可能的 footer-social 格式
        patterns = [
            '<div class="footer-social">',
            '<div class="footer-social">\n',
            '\n<div class="footer-social">',
        ]
        
        insert_pos = -1
        for pattern in patterns:
            pos = html.find(pattern)
            if pos != -1:
                insert_pos = pos
                break
        
        if insert_pos != -1:
            new_footer_lang = f'    <div class="footer-lang"><a href="/blog/{slug}">English</a> | <a href="/ja/blog/{slug}">日本語</a></div>\n    '
            html = html[:insert_pos] + new_footer_lang + html[insert_pos:]
            modified = True
            print(f"  ✅ 添加 footer-lang")
        else:
            print(f"  ❌ 未找到 footer-social，无法添加 footer-lang")
    
    # === 修复2: 缩短 title 到 ≤70 字符 ===
    title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if title_match:
        title = title_match.group(1)
        if len(title) > 70:
            # 策略1: 保留 " — Baidu PPC Pro Blog" 后缀
            parts = title.rsplit(' — ', 1)
            if len(parts) == 2:
                main_title = parts[0]
                suffix = parts[1]
                # 计算主标题最大长度
                max_main_len = 70 - len(suffix) - 3  # 3 = " — "
                if max_main_len > 0 and len(main_title) > max_main_len:
                    new_title = main_title[:max_main_len-3] + '... — ' + suffix
                    html = html.replace(f'<title>{title}</title>', f'<title>{new_title}</title>')
                    modified = True
                    print(f"  ✅ 缩短 title (策略1): {len(title)} → {len(new_title)} 字符")
            
            # 如果还是太长，用策略2: 直接截断
            title_match2 = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
            if title_match2:
                title2 = title_match2.group(1)
                if len(title2) > 70:
                    new_title2 = title2[:67] + '...'
                    html = html.replace(f'<title>{title2}</title>', f'<title>{new_title2}</title>')
                    modified = True
                    print(f"  ✅ 缩短 title (策略2): {len(title2)} → {len(new_title2)} 字符")
    
    if modified:
        with open(path, 'w', encoding='utf8') as f:
            f.write(html)
        print(f"✅ 修复完成: {path}")
        return True
    else:
        print(f"  ⚠️ 文件无需修复: {path}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python final_fix.py <file-path>")
        sys.exit(1)
    
    path = sys.argv[1]
    success = fix_file(path)
    sys.exit(0 if success else 1)
