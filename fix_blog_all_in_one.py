#!/usr/bin/env python3
"""
fix_blog_all_in_one.py - 完整修复博客文件的所有问题
1. 添加 nav-right-group 和 lang-switch（如果缺失）
2. 修复 footer (移除 footer-copy 内的 JS，添加 footer-lang)
3. 添加 toggleLangMenu() 到 script 标签
4. 修复 title 长度 (<=70 字符)
"""
import sys
import re

def fix_blog_file(path):
    with open(path, 'r', encoding='utf8') as f:
        html = f.read()
    
    slug = path.split('/')[-1].replace('.html', '')
    modified = False
    
    # === 修复1: 添加 nav-right-group 和 lang-switch ===
    if 'nav-right-group' not in html:
        # 在 </div></nav> 之前添加 nav-right-group
        # 找到 nav-cta 的位置
        nav_cta_pattern = r'<a href="/contact\.html" class="nav-cta">Get Started &rarr;</a>'
        nav_cta_match = re.search(nav_cta_pattern, html)
        if nav_cta_match:
            nav_cta_end = nav_cta_match.end()
            # 在 nav-cta 之后、</div></nav> 之前插入 nav-right-group
            nav_right_group = f'''
      <div class="nav-right-group">
      <div class="lang-switch">
        <button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="Language">
          🇺🇸
          <svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg>
        </button>
        <div class="lang-switch-menu" id="langSwitchMenu">
            <a href="/blog/{slug}" lang="en" class="lang-switch-item">🇺🇸 English</a>
            <a href="/ja/blog/{slug}" lang="ja" class="lang-switch-item">🇯🇵 日本語</a>
        </div>
      </div>
      
      <a href="/contact.html" class="nav-cta">Get Started &rarr;</a>
      </div>
'''
            # 替换 nav-cta（把它包在 nav-right-group 内）
            old_nav_cta = nav_cta_match.group(0)
            html = html.replace(old_nav_cta, nav_right_group, 1)
            modified = True
            print(f"  ✅ 添加 nav-right-group 和 lang-switch")
        else:
            print(f"  ⚠️ 未找到 nav-cta，无法添加 nav-right-group")
    
    # === 修复2: 修复 footer-copy (移除 JS 代码) ===
    pattern_bad_footer_copy = r'<div class="footer-copy">\s*&copy;\s*<script>document\.write\(new Date\(\)\.getFullYear\(\)\)\s*function toggleLangMenu\(\) \{.*?</script>\s*Baidu PPC Pro\. All rights reserved\.\s*</div>'
    
    match = re.search(pattern_bad_footer_copy, html, re.DOTALL)
    if match:
        bad_footer_copy = match.group(0)
        good_footer_copy = '<div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>'
        html = html.replace(bad_footer_copy, good_footer_copy, 1)
        modified = True
        print(f"  ✅ 修复 footer-copy (移除 JS 代码)")
    
    # === 修复3: 添加/修复 footer-lang ===
    footer_lang_count = html.count('<div class="footer-lang">')
    if footer_lang_count == 0:
        # 缺少 footer-lang，在 footer-social 之前添加
        footer_social_pos = html.find('<div class="footer-social">')
        if footer_social_pos != -1:
            insert_pos = footer_social_pos
            new_footer_lang = f'    <div class="footer-lang"><a href="/blog/{slug}">English</a> | <a href="/ja/blog/{slug}">日本語</a></div>\n'
            html = html[:insert_pos] + new_footer_lang + html[insert_pos:]
            modified = True
            print(f"  ✅ 添加 footer-lang")
    elif footer_lang_count > 1:
        # 移除多余的 footer-lang
        first_pos = html.find('<div class="footer-lang">')
        end_first = html.find('</div>', first_pos) + len('</div>')
        temp = html[end_first:]
        temp = re.sub(r'\s*<div class="footer-lang">.*?</div>\s*', '', temp, flags=re.DOTALL)
        html = html[:end_first] + temp
        modified = True
        print(f"  ✅ 移除多余的 footer-lang ({footer_lang_count - 1} 个)")
    
    # === 修复4: 确保 toggleLangMenu() 在 script 标签中 ===
    if 'function toggleLangMenu()' not in html:
        # 找到 <script> 标签（在 </body> 之前）
        script_pattern = r'(<script>\s*let mobileNavOpen.*?</script>)'
        script_match = re.search(script_pattern, html, re.DOTALL)
        if script_match:
            old_script = script_match.group(1)
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
            new_script = old_script[:-len('</script>')] + toggle_code + '</script>'
            html = html.replace(old_script, new_script, 1)
            modified = True
            print(f"  ✅ 添加 toggleLangMenu() 函数")
    
    # === 修复5: 修复 title 长度 (<=70 字符) ===
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
        print("Usage: python fix_blog_all_in_one.py <file-path>")
        sys.exit(1)
    
    path = sys.argv[1]
    success = fix_blog_file(path)
    sys.exit(0 if success else 1)
