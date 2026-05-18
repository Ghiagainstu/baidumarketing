#!/usr/bin/env python3
"""
BPP Blog Batch Fix Script
批量修复博客页面的结构性问题
"""

import re
import os
import sys

BLOG_DIR = "c:/Users/HYE/WorkBuddy/20260411211839/blog"

def fix_theme_toggle_css(content):
    """修复 theme-toggle 的 CSS，确保暗色模式图标切换正确"""
    
    # 确保有完整的 theme-toggle CSS
    # 检查是否有 .theme-toggle svg 尺寸限制
    if '.theme-toggle svg' not in content:
        # 在第一个 </style> 前插入
        insert_css = """
    .theme-toggle { display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; border: 1px solid var(--gray-200); background: transparent; cursor: pointer; transition: all 0.2s ease; color: var(--gray-600); flex-shrink: 0; }
    .theme-toggle:hover { border-color: var(--blue); color: var(--blue); transform: rotate(15deg); }
    .theme-toggle svg { width: 18px; height: 18px; }
    [data-theme="dark"] .theme-toggle .icon-sun { display: block; }
    [data-theme="dark"] .theme-toggle .icon-moon { display: none; }
    .theme-toggle .icon-sun { display: none; }
    .theme-toggle .icon-moon { display: block; }
"""
        content = content.replace('</style>', insert_css + '  </style>', 1)
    
    # 修复暗色模式图标切换逻辑
    # 确保有正确的 icon-sun 和 icon-moon 显示/隐藏规则
    if '[data-theme="dark"] .theme-toggle .icon-sun' not in content:
        # 需要添加
        pass
    
    return content

def fix_class_names(content):
    """修复 CSS 类名不一致问题"""
    
    # page-hero → article-hero
    content = content.replace('class="page-hero"', 'class="article-hero"')
    content = content.replace('.page-hero', '.article-hero')
    
    # article-title → 直接用 h1（如果需要保持样式，改为 .article-hero h1）
    # 这个需要更谨慎，因为可能涉及 HTML 结构变化
    
    return content

def add_back_to_top(content):
    """添加 back-to-top 按钮（如果缺少）"""
    
    if 'back-to-top' not in content:
        # 在 </body> 前添加按钮
        back_to_top_html = """
<button class="back-to-top" id="backToTop" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="Back to top">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="18 15 12 9 6 15"/></svg>
</button>
"""
        content = content.replace('</body>', back_to_top_html + '</body>')
        
        # 添加 CSS
        back_to_top_css = """
    .back-to-top { position: fixed; bottom: 32px; right: 32px; z-index: 90; width: 44px; height: 44px; border-radius: 50%; background: var(--gradient-brand); color: #fff; border: none; cursor: pointer; display: grid; place-items: center; box-shadow: 0 4px 14px rgba(41,50,225,.35); opacity: 0; pointer-events: none; transition: opacity .3s, transform var(--transition-base), box-shadow var(--transition-base); }
    .back-to-top.visible { opacity: 1; pointer-events: auto; }
    .back-to-top:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(41,50,225,.45); }
    .back-to-top:active { transform: scale(.92); }
    .back-to-top svg { width: 20px; height: 20px; }
"""
        content = content.replace('</style>', back_to_top_css + '  </style>', 1)
        
        # 添加 JS
        if 'backToTop' not in content:
            js_code = """
(function(){const t=document.getElementById('backToTop');if(t)window.addEventListener('scroll',()=>{t.classList.toggle('visible',window.scrollY>400)})})();
"""
            # 在 </script> 前插入
            content = content.replace('</script>', js_code + '</script>', 1)
    
    return content

def fix_favicon_quotes(content):
    """修复 favicon 内联 SVG 的引号问题"""
    
    # 检查 favicon 行是否有双引号
    favicon_pattern = r'<link rel="icon" href="data:image/svg\+xml,[^"]*"[[:]\s]*/>'
    
    # 简化检查：查找 favicon 行
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'rel="icon"' in line and 'data:image/svg+xml' in line:
            # 检查是否有双引号在 SVG 内部
            if '"' in line.split('data:image/svg+xml,')[1].split('" /')[0] if ',' in line else False:
                print(f"  Line {i+1}: Found favicon with potential quote issue")
                # 这里需要更复杂的逻辑来修复，暂时跳过
    
    return content

def check_image_urls(content, file_path):
    """检查图片 URL 是否正确"""
    
    # 查找所有 <img> 标签
    img_pattern = r'<img[^>]+src="([^"]+)"'
    imgs = re.findall(img_pattern, content)
    
    for img_src in imgs:
        if img_src.startswith('http'):
            # 检查 URL 是否可访问（这里只检查格式）
            if ' ' in img_src:
                print(f"  Image URL has spaces: {img_src}")
        elif img_src.startswith('../'):
            # 相对路径，检查文件是否存在
            img_path = os.path.join(os.path.dirname(file_path), img_src)
            if not os.path.exists(img_path):
                print(f"  Image file not found: {img_path}")
    
    return content

def process_blog_file(file_path):
    """处理单个博客文件"""
    
    print(f"\nProcessing: {os.path.basename(file_path)}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修复 theme-toggle CSS
    content = fix_theme_toggle_css(content)
    
    # 修复类名
    content = fix_class_names(content)
    
    # 添加 back-to-top 按钮
    content = add_back_to_top(content)
    
    # 修复 favicon 引号
    content = fix_favicon_quotes(content)
    
    # 检查图片 URL
    content = check_image_urls(content, file_path)
    
    # 如果有修改，写回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  Updated!")
    else:
        print("  No changes needed")

def main():
    """主函数"""
    
    if not os.path.exists(BLOG_DIR):
        print(f"Error: Blog directory not found: {BLOG_DIR}")
        sys.exit(1)
    
    # 获取所有 HTML 文件
    html_files = [f for f in os.listdir(BLOG_DIR) if f.endswith('.html')]
    
    print(f"Found {len(html_files)} blog files")
    
    for html_file in sorted(html_files):
        file_path = os.path.join(BLOG_DIR, html_file)
        try:
            process_blog_file(file_path)
        except Exception as e:
            print(f"  Error processing {html_file}: {e}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
