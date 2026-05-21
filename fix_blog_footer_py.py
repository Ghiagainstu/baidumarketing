#!/usr/bin/env python3
"""
fix_blog_footer_py.py - 用 Python 精确修复博客文件的 footer 问题
"""
import sys
import re

def fix_blog_file(path):
    with open(path, 'r', encoding='utf8') as f:
        html = f.read()
    
    slug = path.split('/')[-1].replace('.html', '')
    
    # === 修复1: 替换损坏的 footer-bottom 部分 ===
    # 找到 <div class="footer-bottom"> 的开始位置
    fb_start = html.find('<div class="footer-bottom">')
    if fb_start == -1:
        print(f"  ❌ 未找到 <div class=\"footer-bottom\"> in {path}")
        return False
    
    # 找到 </footer> 的位置 (最后一个)
    footer_end = html.rfind('</footer>')
    if footer_end == -1:
        print(f"  ❌ 未找到 </footer> in {path}")
        return False
    
    # 提取 footer 之前的内容和 footer 之后的内容
    before_footer = html[:fb_start]
    after_footer = html[footer_end + len('</footer>'):]
    
    # 构建正确的 footer-bottom 结构
    correct_footer_bottom = f'''  <div class="footer-bottom">
    <div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>
    <div class="footer-lang"><a href="/blog/{slug}">English</a> | <a href="/ja/blog/{slug}">日本語</a></div>
    <div class="footer-social"><a href="#" class="obf-email-icon" data-u="baidu" data-d="baidumarketing.com" aria-label="Email"><svg viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22,4 12,13 2,4"/></svg></a></div>
  </div>
</div>
</footer>'''
    
    # 重新组装
    html = before_footer + correct_footer_bottom + after_footer
    
    # === 修复2: 在 <script> 标签内添加 toggleLangMenu 函数 ===
    # 检查是否已经有 toggleLangMenu 函数
    if 'function toggleLangMenu()' not in html:
        # 找到最后一个 </script> 标签 (在 </body> 之前)
        # 在 toggleMobileNav 函数之后添加
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
        # 在最后一个 <script> 的 </script> 之前插入
        last_script_end = html.rfind('</script>')
        if last_script_end != -1:
            html = html[:last_script_end] + toggle_code + html[last_script_end:]
            print(f"  ✅ 添加 toggleLangMenu() 函数")
    
    # === 修复3: 检查并修复 title 长度 ===
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
                    print(f"  ✅ 缩短 title: {len(title)} → {len(new_title)} 字符")
    
    # 写回文件
    with open(path, 'w', encoding='utf8') as f:
        f.write(html)
    
    print(f"  ✅ 修复完成: {path}")
    print(f"  ✅ footer-bottom 已修复")
    print(f"  ✅ footer-lang 已统一 (1个)")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_blog_footer_py.py <file-path>")
        sys.exit(1)
    
    path = sys.argv[1]
    success = fix_blog_file(path)
    sys.exit(0 if success else 1)
