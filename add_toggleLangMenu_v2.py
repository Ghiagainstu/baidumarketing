#!/usr/bin/env python3
"""
add_toggleLangMenu_v2.py - 健壮版：找到最后一个 <script> 标签并添加 toggleLangMenu() 函数
"""
import sys

def fix_file(path):
    with open(path, 'r', encoding='utf8') as f:
        html = f.read()
    
    if 'function toggleLangMenu()' in html:
        print(f"  ⚠️ toggleLangMenu() 已存在，跳过: {path}")
        return True
    
    # 找到最后一个 <script> 标签的位置
    # 策略：找到 </body> 之前的最后一个 <script> 标签
    body_end = html.rfind('</body>')
    if body_end == -1:
        # 没有 </body>，找到最后一个 </script>
        last_script_end = html.rfind('</script>')
        if last_script_end == -1:
            print(f"  ❌ 未找到 <script> 标签: {path}")
            return False
        insert_pos = last_script_end
    else:
        # 在 </body> 之前找最后一个 <script> 标签
        html_before_body = html[:body_end]
        last_script_end = html_before_body.rfind('</script>')
        if last_script_end == -1:
            print(f"  ❌ 未找到 </body> 之前的 <script> 标签: {path}")
            return False
        insert_pos = last_script_end
    
    # 在 </script> 之前插入 toggleLangMenu 函数定义
    # 找到 <script> 标签的开始位置
    script_start = html.rfind('<script>', 0, insert_pos)
    if script_start == -1:
        print(f"  ❌ 未找到 <script> 开始标签: {path}")
        return False
    
    # 读取 <script> 标签后的内容（到 </script> 之前）
    script_content_start = html.find('>', script_start) + 1
    script_content_end = insert_pos  # </script> 的位置
    
    # 构造要插入的函数定义
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
    
    # 在 <script> 标签内、现有代码之前插入函数定义
    # 方法：在 <script> 标签的 > 之后插入
    html = html[:script_content_start] + toggle_func + html[script_content_start:]
    
    with open(path, 'w', encoding='utf8') as f:
        f.write(html)
    
    print(f"  ✅ 添加 toggleLangMenu() 函数定义: {path}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python add_toggleLangMenu_v2.py <file-path>")
        sys.exit(1)
    
    path = sys.argv[1]
    success = fix_file(path)
    sys.exit(0 if success else 1)
