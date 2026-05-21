#!/usr/bin/env python3
"""
fix_blog_complete.py - 完整修复博客文件的 footer 问题
1. 从 footer-copy 中移除 JS 代码
2. 添加 footer-lang (如果缺失)
3. 在 </body> 之前的 <script> 中添加 toggleLangMenu 函数
4. 修复 title 长度
"""
import sys
import re

def fix_blog_file(path):
    with open(path, 'r', encoding='utf8') as f:
        html = f.read()
    
    slug = path.split('/')[-1].replace('.html', '')
    modified = False
    
    # === 修复1: 从 footer-copy 中移除 JS 代码 ===
    # footer-copy 错误结构：包含 <script> 标签和 JS 代码
    # 正确结构：footer-copy 只包含版权信息和日期脚本
    
    # 匹配错误的 footer-copy (包含 JS 代码)
    pattern_bad_footer_copy = r'<div class="footer-copy">\s*&copy;\s*<script>document\.write\(new Date\(\)\.getFullYear\(\)\)\s*function toggleLangMenu\(\) \{.*?</script>\s*Baidu PPC Pro\. All rights reserved\.\s*</div>'
    
    match = re.search(pattern_bad_footer_copy, html, re.DOTALL)
    if match:
        bad_footer_copy = match.group(0)
        good_footer_copy = '<div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>'
        html = html.replace(bad_footer_copy, good_footer_copy, 1)
        modified = True
        print(f"  ✅ 修复 footer-copy (移除 JS 代码)")
    
    # === 修复2: 添加/修复 footer-lang ===
    footer_lang_count = html.count('<div class="footer-lang">')
    if footer_lang_count == 0:
        # 缺少 footer-lang，在 footer-social 之前添加
        footer_social_pos = html.find('<div class="footer-social">')
        if footer_social_pos != -1:
            insert_pos = footer_social_pos
            new_footer_lang = f'    <div class="footer-lang"><a href="/blog/{slug}">English</a> | <a href="/ja/blog/{slug}">日本語</a></div>\n    '
            html = html[:insert_pos] + new_footer_lang + html[insert_pos:]
            modified = True
            print(f"  ✅ 添加 footer-lang")
    elif footer_lang_count > 1:
        # 有多余的 footer-lang，只保留第一个
        # 找到第一个的位置，删除后续的所有
        first_pos = html.find('<div class="footer-lang">')
        end_first = html.find('</div>', first_pos) + len('</div>')
        
        # 删除后续的 footer-lang
        temp = html[end_first:]
        temp = re.sub(r'\s*<div class="footer-lang">.*?</div>\s*', '', temp, flags=re.DOTALL)
        html = html[:end_first] + temp
        modified = True
        print(f"  ✅ 移除多余的 footer-lang ({footer_lang_count - 1} 个)")
    
    # === 修复3: 确保 toggleLangMenu 函数在 <script> 标签中 ===
    # 检查 toggleLangMenu 是否在 footer-copy 之外的地方定义
    # 先检查是否在 <script> 标签中（正确的位置）
    script_content_match = re.search(r'<script>\s*(let mobileNavOpen.*?)</script>', html, re.DOTALL)
    if script_content_match:
        script_content = script_content_match.group(1)
        if 'function toggleLangMenu()' not in script_content:
            # 需要添加 toggleLangMenu 函数
            # 在 </script> 之前添加
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
            # 找到 <script> 标签的位置
            script_start = html.find('<script>\nlet mobileNavOpen')
            if script_start == -1:
                script_start = html.find('<script>')
            if script_start != -1:
                script_end = html.find('</script>', script_start)
                if script_end != -1:
                    html = html[:script_end] + toggle_code + html[script_end:]
                    modified = True
                    print(f"  ✅ 添加 toggleLangMenu() 函数")
    
    # === 修复4: 检查并修复 title 长度 (<=70 字符) ===
    title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if title_match:
        title = title_match.group(1)
        if len(title) > 70:
            # 尝试缩短 (保留 " — Baidu PPC Pro Blog" 后缀)
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
        print("Usage: python fix_blog_complete.py <file-path>")
        sys.exit(1)
    
    path = sys.argv[1]
    success = fix_blog_file(path)
    sys.exit(0 if success else 1)
