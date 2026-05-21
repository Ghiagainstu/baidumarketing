#!/usr/bin/env python3
"""
fix_remaining.py - 修复剩余问题
1. 添加 toggleLangMenu() 函数定义
2. 修复 title 长度 (<=70 字符)
"""
import sys
import re

def fix_blog_file(path):
    with open(path, 'r', encoding='utf8') as f:
        html = f.read()
    
    modified = False
    
    # === 修复1: 添加 toggleLangMenu() 函数定义 ===
    if 'function toggleLangMenu()' not in html:
        # 找到 <script> 标签（在 </body> 之前）
        # 查找包含 toggleMobileNav 的 script 标签
        script_pattern = r'<script>\s*let mobileNavOpen.*?</script>'
        script_match = re.search(script_pattern, html, re.DOTALL)
        
        if script_match:
            old_script = script_match.group(0)
            # 在 </script> 之前添加 toggleLangMenu 函数
            toggle_code = '''function toggleLangMenu() {
    const menu = document.getElementById('langSwitchMenu');
    if (menu) menu.classList.toggle('active');
  }
  document.addEventListener('click', function(e) {
    const menu = document.getElementById('langSwitchMenu');
    const btn = document.querySelector('.lang-switch-btn');
    if (menu && btn && !btn.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.remove('active');
    }
  });
  document.addEventListener('DOMContentLoaded', function() {
    const currentLang = document.documentElement.lang || 'en';
    document.querySelectorAll('.lang-switch-item').forEach(function(item) {
      if (item.getAttribute('lang') === currentLang) {
        item.style.fontWeight = '600';
        item.style.pointerEvents = 'none';
        item.style.opacity = '0.5';
      }
    });
  });

'''
            # 在 <script> 开头之后插入
            new_script = old_script[:len('<script>')] + '\n' + toggle_code + old_script[len('<script>'):]
            html = html.replace(old_script, new_script, 1)
            modified = True
            print(f"  ✅ 添加 toggleLangMenu() 函数定义")
        else:
            print(f"  ⚠️ 未找到 <script> 标签，无法添加 toggleLangMenu()")
    
    # === 修复2: 修复 title 长度 (<=70 字符) ===
    title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if title_match:
        title = title_match.group(1)
        if len(title) > 70:
            # 尝试多种缩短策略
            # 策略1: 保留 " — Baidu PPC Pro Blog" 后缀，缩短标题
            parts = title.rsplit(' — ', 1)
            if len(parts) == 2:
                main_title = parts[0]
                suffix = parts[1]
                # 目标：main_title 最多 60 字符，给 suffix 留 10 字符（" — " + suffix）
                max_main_len = 70 - len(suffix) - 3  # 3 = " — "
                if max_main_len > 0 and len(main_title) > max_main_len:
                    new_title = main_title[:max_main_len-3] + '... — ' + suffix
                    html = html.replace(f'<title>{title}</title>', f'<title>{new_title}</title>')
                    modified = True
                    print(f"  ✅ 缩短 title: {len(title)} → {len(new_title)} 字符")
            
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
        print("Usage: python fix_remaining.py <file-path>")
        sys.exit(1)
    
    path = sys.argv[1]
    success = fix_blog_file(path)
    sys.exit(0 if success else 1)
