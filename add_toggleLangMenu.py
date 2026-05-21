#!/usr/bin/env python3
"""
add_toggleLangMenu.py - 在 <script> 标签内添加 toggleLangMenu() 函数定义
"""
import sys

def fix_file(path):
    with open(path, 'r', encoding='utf8') as f:
        html = f.read()
    
    if 'function toggleLangMenu()' in html:
        print(f"  ⚠️ toggleLangMenu() 已存在，跳过: {path}")
        return True
    
    # 找到主要的 <script> 标签（在 </body> 之前）
    # 查找不包含 document.write 的 script 标签
    script_start = html.find('<script>\nlet mobileNav')
    if script_start == -1:
        # 尝试另一种格式
        script_start = html.find('<script>\r\nlet mobileNav')
    if script_start == -1:
        # 尝试查找任何包含 mobileNavOpen 的 script 标签
        script_start = html.find('let mobileNavOpen')
        if script_start != -1:
            # 向前找到 <script>
            script_tag_start = html.rfind('<script>', 0, script_start)
            if script_tag_start != -1:
                script_start = script_tag_start
    
    if script_start == -1:
        print(f"  ❌ 未找到主要的 <script> 标签: {path}")
        return False
    
    # 在 <script> 之后、现有代码之前插入 toggleLangMenu 函数
    # 找到 <script> 的结束位置（> 或 >\n）
    script_tag_end = html.find('>', script_start)
    if script_tag_end == -1:
        print(f"  ❌ 未找到 <script> 标签的结束位置: {path}")
        return False
    
    # 在 > 之后插入新行和函数定义
    insert_pos = script_tag_end + 1
    
    toggle_func = '''
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
    
    html = html[:insert_pos] + toggle_func + html[insert_pos:]
    
    with open(path, 'w', encoding='utf8') as f:
        f.write(html)
    
    print(f"  ✅ 添加 toggleLangMenu() 函数定义: {path}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python add_toggleLangMenu.py <file-path>")
        sys.exit(1)
    
    path = sys.argv[1]
    success = fix_file(path)
    sys.exit(0 if success else 1)
