#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 JA 博客文件：合并 ja/index.html CSS + 修复 nav HTML
"""
import glob

def get_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# 读取 ja/index.html 的 CSS
ja_idx = get_file('ja/index.html')
css_start = ja_idx.find('<style>')
css_end = ja_idx.find('</style>')
JA_CSS = ja_idx[css_start+7:css_end]

# 提取正确的 nav 模板
nav_start = ja_idx.find('<nav>')
nav_end = ja_idx.find('</nav>') + len('</nav>')
JA_NAV_TEMPLATE = ja_idx[nav_start:nav_end]

# 提取正确的 footer 模板
ft_start = ja_idx.find('<footer>')
ft_end = ja_idx.find('</footer>') + len('</footer>')
JA_FOOTER_TEMPLATE = ja_idx[ft_start:ft_end]

print(f"📐 ja/index.html CSS: {len(JA_CSS)} 字符")
print()

files = sorted(glob.glob('ja/blog/*.html'))
nav_fixed = 0
css_fixed = 0

for path in files:
    slug_raw = path.split('/')[-1].replace('.html', '')
    html = get_file(path)
    
    # === 修复 1: 合并 CSS（所有文件） ===
    old_css_s = html.find('<style>')
    old_css_e = html.find('</style>')
    if old_css_s != -1 and old_css_e != -1:
        old_css = html[old_css_s+7:old_css_e]
        merged = JA_CSS.rstrip() + '\n\n' + old_css.lstrip()
        html = html[:old_css_s+7] + merged + html[old_css_e:]
        css_fixed += 1
    
    # === 修复 2: 替换 nav（仅缺少 nav-right-group HTML 元素的文件） ===
    if 'class="nav-right-group"' not in html:
        old_nav_s = html.find('<nav')
        old_nav_e = html.find('</nav>')
        if old_nav_s != -1:
            old_nav_e += len('</nav>')
            
            # 生成正确 nav：删除 nav-mobile-cta（非首页不应有）
            new_nav = JA_NAV_TEMPLATE.replace(
                '<a href="/ja/contact.html" class="nav-mobile-cta">今すぐ始める →</a>',
                ''
            )
            # Blog 链接 active
            new_nav = new_nav.replace(
                '<a href="/ja/blog.html">ブログ</a>',
                '<a href="/ja/blog.html" class="active">ブログ</a>'
            )
            # 语言切换器链接
            new_nav = new_nav.replace(
                'href="/" lang="en"',
                f'href="/blog/{slug_raw}" lang="en"'
            )
            new_nav = new_nav.replace(
                'href="/ja/" lang="ja"',
                f'href="/ja/blog/{slug_raw}" lang="ja"'
            )
            
            html = html[:old_nav_s] + new_nav + html[old_nav_e:]
            nav_fixed += 1
    
    # === 修复 3: 替换 footer ===
    old_ft_s = html.find('<footer>')
    old_ft_e = html.find('</footer>')
    if old_ft_s != -1 and old_ft_e != -1:
        old_ft_e += len('</footer>')
        
        # 生成 footer，在 footer-copy 后插入 footer-lang
        new_ft = JA_FOOTER_TEMPLATE
        fc_pos = new_ft.find('<div class="footer-copy">')
        if fc_pos != -1:
            fc_end = new_ft.find('</div>', fc_pos) + len('</div>')
            footer_lang_html = f'\n      <div class="footer-lang"><a href="/blog/{slug_raw}">English</a> | <a href="/ja/blog/{slug_raw}">日本語</a></div>'
            new_ft = new_ft[:fc_end] + footer_lang_html + new_ft[fc_end:]
        
        html = html[:old_ft_s] + new_ft + html[old_ft_e:]
    
    # === 修复 4: 确保 toggleLangMenu 存在 ===
    if 'function toggleLangMenu()' not in html:
        script_pos = html.rfind('<script>')
        if script_pos != -1:
            toggle_js = """
  function toggleLangMenu() { var m = document.getElementById('langSwitchMenu'); if (m) m.classList.toggle('open'); }
  document.addEventListener('click', function(e) { var m = document.getElementById('langSwitchMenu'); var b = document.querySelector('.lang-switch-btn'); if (m && b && !b.contains(e.target) && !m.contains(e.target)) m.classList.remove('open'); });
"""
            html = html[:script_pos+8] + toggle_js + html[script_pos+8:]
    
    write_file(path, html)
    slug = path.split('/')[-1]
    print(f"  ✅ {slug}")

print(f"\n结果: nav修复={nav_fixed}, css合并={css_fixed}/61")
