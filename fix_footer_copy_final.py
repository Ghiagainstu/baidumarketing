#!/usr/bin/env python3
"""
fix_footer_copy_final.py - 精确修复 footer-copy 问题
1. 从 footer-copy 中移除 JS 代码
2. 将 toggleLangMenu() 函数定义添加到 </body> 之前的 <script> 标签中
3. 添加/修复 footer-lang
4. 修复 title 长度
"""
import sys
import re

def fix_file(path):
    with open(path, 'r', encoding='utf8') as f:
        html = f.read()
    
    slug = path.split('/')[-1].replace('.html', '')
    modified = False
    
    # === 修复1: 修复 footer-copy (移除 JS 代码) ===
    # footer-copy 的错误结构：包含 <script> 标签和 JS 代码
    # 正确结构：footer-copy 只包含版权信息和日期脚本
    
    # 找到 <div class="footer-copy"> 的位置
    fc_start = html.find('<div class="footer-copy">')
    if fc_start == -1:
        print(f"  ❌ 未找到 footer-copy: {path}")
        return False
    
    # 找到紧随其后的 <script> 标签
    script_start = html.find('<script>', fc_start)
    if script_start == -1:
        print(f"  ⚠️ footer-copy 内未找到 <script>: {path}")
        # 可能已经修复了
        pass
    else:
        # 找到 </script> 的位置
        script_end = html.find('</script>', script_start)
        if script_end == -1:
            print(f"  ❌ 未找到 </script>: {path}")
            return False
        
        # footer-copy 的正确结构（在 </script> 之后）
        # 当前结构：<div class="footer-copy">&copy; <script>...</script> Baidu PPC Pro. All rights reserved.</div>
        # 我们需要把 JS 代码从 <script> 中移出来
        
        # 构造正确的 footer-copy
        good_fc = '<div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>'
        
        # 找到 footer-copy 的结束位置（第一个 </div>，在 script_end 之后）
        fc_end = html.find('</div>', script_end + len('</script>'))
        if fc_end == -1:
            print(f"  ❌ 未找到 footer-copy 的结束 </div>: {path}")
            return False
        
        # 提取 JS 代码（从 <script> 之后到 </script> 之前）
        js_code = html[script_start + len('<script>'):script_end]
        
        # 替换 footer-copy 部分
        html = html[:fc_start] + good_fc + html[fc_end + len('</div>'):]
        modified = True
        print(f"  ✅ 修复 footer-copy (移除 JS 代码)")
        
        # 将 JS 代码添加到 </body> 之前的 <script> 标签中
        # 找到最后一个 <script> 标签
        last_script_start = html.rfind('<script>')
        if last_script_start != -1:
            # 在 <script> 标签之后插入 JS 代码
            insert_pos = last_script_start + len('<script>')
            html = html[:insert_pos] + js_code + '\n' + html[insert_pos:]
            print(f"  ✅ 添加 JS 代码到 <script> 标签")
        else:
            print(f"  ⚠️ 未找到 <script> 标签，无法添加 JS 代码")
    
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
        first_pos = html.find('<div class="footer-lang">')
        end_first = html.find('</div>', first_pos) + len('</div>')
        
        # 删除后续的 footer-lang
        temp = html[end_first:]
        temp = re.sub(r'\s*<div class="footer-lang">.*?</div>\s*', '', temp, flags=re.DOTALL)
        html = html[:end_first] + temp
        modified = True
        print(f"  ✅ 移除多余的 footer-lang ({footer_lang_count - 1} 个)")
    
    # === 修复3: 确保 toggleLangMenu() 在 <script> 标签中 ===
    if 'function toggleLangMenu()' not in html:
        # 找到最后一个 <script> 标签
        last_script_start = html.rfind('<script>')
        if last_script_start != -1:
            # 在 <script> 标签之后插入 toggleLangMenu 函数定义
            insert_pos = last_script_start + len('<script>')
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
            html = html[:insert_pos] + toggle_code + html[insert_pos:]
            modified = True
            print(f"  ✅ 添加 toggleLangMenu() 函数定义")
    
    # === 修复4: 修复 title 长度 (<=70 字符) ===
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
        print("Usage: python fix_footer_copy_final.py <file-path>")
        sys.exit(1)
    
    path = sys.argv[1]
    success = fix_file(path)
    sys.exit(0 if success else 1)
