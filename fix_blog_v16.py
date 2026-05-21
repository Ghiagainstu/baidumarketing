#!/usr/bin/env python3
"""
fix_blog_v16.py - 用正则表达式精确修复 footer 问题
"""
import sys
import re

def fix_blog_file(path):
    with open(path, 'r', encoding='utf8') as f:
        html = f.read()
    
    slug = path.split('/')[-1].replace('.html', '')
    modified = False
    
    # === 修复1: 从 footer-copy 中移除 toggleLangMenu 函数 ===
    # footer-copy 的错误结构：
    # <div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())
    #   function toggleLangMenu() { ... }
    #   ...
    #   </script> Baidu PPC Pro. All rights reserved.</div>
    
    # 用正则匹配并确保 footer-copy 只包含版权信息
    pattern_footer_copy = r'<div class="footer-copy">&copy; <script>document\.write\(new Date\(\)\.getFullYear\(\)\)\n.*?</script> Baidu PPC Pro\. All rights reserved\.</div>'
    
    match = re.search(pattern_footer_copy, html, re.DOTALL)
    if match:
        old_footer_copy = match.group(0)
        new_footer_copy = '<div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>'
        html = html.replace(old_footer_copy, new_footer_copy, 1)
        modified = True
        print(f"  ✅ 修复 footer-copy (移除 JS 代码)")
    
    # === 修复2: 移除多余的 footer-lang (只保留第一个) ===
    pattern_footer_lang = r'<div class="footer-lang">.*?</div>'
    footer_langs = re.findall(pattern_footer_lang, html, re.DOTALL)
    if len(footer_langs) > 1:
        # 保留第一个，删除其余的
        # 找到第一个的位置，然后删除后续的所有 footer-lang
        first_pos = html.find(footer_langs[0])
        # 从第一个之后开始，删除所有后续的 footer-lang
        after_first = html[first_pos + len(footer_langs[0]):]
        # 删除多余的 footer-lang
        cleaned = re.sub(r'^\s*<div class="footer-lang">.*?</div>\s*', '', after_first, flags=re.DOTALL | re.MULTILINE)
        html = html[:first_pos + len(footer_langs[0])] + cleaned
        modified = True
        print(f"  ✅ 移除多余的 footer-lang ({len(footer_langs) - 1} 个)")
    elif len(footer_langs) == 0:
        # 没有 footer-lang，需要添加一个
        # 在 footer-social 之前添加
        footer_social_pos = html.find('<div class="footer-social">')
        if footer_social_pos != -1:
            insert_pos = footer_social_pos
            new_footer_lang = f'\n    <div class="footer-lang"><a href="/blog/{slug}">English</a> | <a href="/ja/blog/{slug}">日本語</a></div>\n    '
            html = html[:insert_pos] + new_footer_lang + html[insert_pos:]
            modified = True
            print(f"  ✅ 添加 footer-lang")
    
    # === 修复3: 确保 toggleLangMenu 函数在 <script> 标签中 ===
    if 'function toggleLangMenu()' not in html:
        # 在最后一个 </script> 之前添加
        last_script_end = html.rfind('</script>')
        if last_script_end != -1:
            toggle_code = '''
function toggleLangMenu() {
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
            html = html[:last_script_end] + toggle_code + '\n' + html[last_script_end:]
            modified = True
            print(f"  ✅ 添加 toggleLangMenu() 函数")
    
    # === 修复4: 检查并修复 title 长度 ===
    title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if title_match:
        title = title_match.group(1)
        if len(title) > 70:
            # 尝试缩短
            parts = title.rsplit(' — ', 1)
            if len(parts) == 2:
                main_title = parts[0]
                suffix = parts[1]
                if len(main_title) > 60:
                    new_title = main_title[:57] + '... — ' + suffix
                    html = html.replace(f'<title>{title}</title>', f'<title>{new_title}</title>')
                    modified = True
                    print(f"  ✅ 缩短 title: {len(title)} → {len(new_title)} 字符")
    
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
        print("Usage: python fix_blog_v16.py <file-path>")
        sys.exit(1)
    
    path = sys.argv[1]
    success = fix_blog_file(path)
    sys.exit(0 if success else 1)
