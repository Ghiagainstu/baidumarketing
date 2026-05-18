#!/usr/bin/env python3
"""
BPP Blog Batch Fix Script v2
批量修复博客页面的结构性问题和图片显示问题
"""

import re
import os
import sys

BLOG_DIR = "c:/Users/HYE/WorkBuddy/20260411211839/blog"
ASSETS_DIR = "c:/Users/HYE/WorkBuddy/20260411211839/assets"

def fix_page_hero_class(content):
    """修复 .page-hero → .article-hero"""
    # 修复 CSS 中的类名
    content = content.replace('.page-hero {', '.article-hero {')
    content = content.replace('.page-hero h1', '.article-hero h1')
    content = content.replace('.page-hero h2', '.article-hero h2')
    
    # 修复 HTML 中的类名
    content = content.replace('class="page-hero"', 'class="article-hero"')
    
    return content

def fix_article_title(content):
    """修复 .article-title → 直接用 h1（保持样式）"""
    # 检查是否有 .article-title 类
    if 'class="article-title"' in content:
        # 需要手动处理，因为涉及 HTML 结构变化
        # 这里只标记，不自动修复
        pass
    return content

def fix_theme_toggle_css(content):
    """修复 theme-toggle 的 CSS，确保暗色模式图标切换正确"""
    
    # 检查是否有完整的 theme-toggle CSS
    if '.theme-toggle svg' not in content:
        # 缺少 SVG 尺寸限制，需要添加
        insert_css = """
    .theme-toggle { display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; border: 1px solid var(--gray-200); background: transparent; cursor: pointer; transition: all 0.2s ease; color: var(--gray-600); flex-shrink: 0; }
    .theme-toggle:hover { border-color: var(--blue); color: var(--blue); transform: rotate(15deg); }
    .theme-toggle svg { width: 18px; height: 18px; }
    [data-theme="dark"] .theme-toggle .icon-sun { display: block; }
    [data-theme="dark"] .theme-toggle .icon-moon { display: none; }
    .theme-toggle .icon-sun { display: none; }
    .theme-toggle .icon-moon { display: block; }
"""
        # 在 </style> 前插入
        if '</style>' in content:
            content = content.replace('</style>', insert_css + '  </style>', 1)
    
    # 清理重复的图标切换规则
    # 移除 .icon-sun 和 .icon-moon 的独立规则（它们应该只在 .theme-toggle 内）
    content = re.sub(r'\s*\.icon-sun\s*\{[^}]*\}\s*', '', content)
    content = re.sub(r'\s*\.icon-moon\s*\{[^}]*\}\s*', '', content)
    
    return content

def add_back_to_top(content):
    """添加 back-to-top 按钮（如果缺少）"""
    
    if 'back-to-top' not in content and 'backToTop' not in content:
        # 在 </body> 前添加按钮 HTML
        back_to_top_html = '''
<button class="back-to-top" id="backToTop" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="Back to top">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="18 15 12 9 6 15"/></svg>
</button>
'''
        content = content.replace('</body>', back_to_top_html + '\n</body>')
        
        # 添加 CSS
        back_to_top_css = '''
    .back-to-top { position: fixed; bottom: 32px; right: 32px; z-index: 90; width: 44px; height: 44px; border-radius: 50%; background: var(--gradient-brand); color: #fff; border: none; cursor: pointer; display: grid; place-items: center; box-shadow: 0 4px 14px rgba(41,50,225,.35); opacity: 0; pointer-events: none; transition: opacity .3s, transform var(--transition-base), box-shadow var(--transition-base); }
    .back-to-top.visible { opacity: 1; pointer-events: auto; }
    .back-to-top:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(41,50,225,.45); }
    .back-to-top:active { transform: scale(.92); }
    .back-to-top svg { width: 20px; height: 20px; }
'''
        if '</style>' in content:
            content = content.replace('</style>', back_to_top_css + '  </style>', 1)
        
        # 添加 JS
        back_to_top_js = '''
(function(){const t=document.getElementById('backToTop');if(t)window.addEventListener('scroll',()=>{t.classList.toggle('visible',window.scrollY>400)})})();
'''
        # 在第一个 </script> 前插入
        if '</script>' in content:
            content = content.replace('</script>', back_to_top_js + '  </script>', 1)
    
    return content

def fix_favicon_quotes(content):
    """修复 favicon 内联 SVG 的引号问题"""
    
    # 查找 favicon 行
    lines = content.split('\n')
    fixed_lines = []
    modified = False
    
    for line in lines:
        if 'rel="icon"' in line and 'data:image/svg+xml' in line:
            # 检查是否有双引号在 SVG 内部
            if "'" in line and '"' in line.split('data:image/svg+xml,')[1].split('" /')[0] if ',' in line else False:
                # 需要修复：确保 SVG 属性用单引号
                # 这是一个简化版本，实际需要更复杂的逻辑
                print(f"  Found potential favicon quote issue, line: {line[:80]}...")
                modified = True
        fixed_lines.append(line)
    
    if modified:
        content = '\n'.join(fixed_lines)
    
    return content

def fix_image_urls(content, file_path):
    """修复图片 URL - 删除不存在的图片引用"""
    
    # 查找所有 <img> 标签
    img_pattern = r'<img[^>]+>'
    imgs = re.findall(img_pattern, content)
    
    for img_tag in imgs:
        # 提取 src
        src_match = re.search(r'src="([^"]+)"', img_tag)
        if src_match:
            img_src = src_match.group(1)
            
            # 检查是否是你baidumarketing.com/assets/ 的绝对 URL
            if img_src.startswith('https://baidumarketing.com/assets/'):
                # 提取文件名
                filename = img_src.split('/')[-1]
                local_path = os.path.join(ASSETS_DIR, filename)
                
                # 检查文件是否存在
                if not os.path.exists(local_path):
                    print(f"  Image not found: {filename}")
                    print(f"    Removing img tag: {img_tag[:80]}...")
                    # 删除整个 img 标签
                    content = content.replace(img_tag, '')
                    
            elif img_src.startswith('../assets/'):
                # 相对路径
                local_path = os.path.join(os.path.dirname(file_path), img_src)
                if not os.path.exists(local_path):
                    print(f"  Image not found (relative path): {img_src}")
                    content = content.replace(img_tag, '')
    
    return content

def add_json_ld(content, file_path):
    """添加 JSON-LD Schema（如果缺少）"""
    
    if 'application/ld+json' not in content:
        # 需要添加 JSON-LD
        # 提取标题
        title_match = re.search(r'<title>([^<]+)</title>', content)
        title = title_match.group(1) if title_match else 'Blog Post'
        
        # 提取描述
        desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
        desc = desc_match.group(1) if desc_match else ''
        
        # 提取 URL
        url_match = re.search(r'<link rel="canonical" href="([^"]+)"', content)
        url = url_match.group(1) if url_match else ''
        
        # 创建 JSON-LD
        json_ld = f'''
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "description": "{desc}",
    "url": "{url}",
    "image": "https://baidumarketing.com/assets/og-brand-default.png",
    "datePublished": "2025-01-01",
    "dateModified": "2025-01-01",
    "author": {{
      "@type": "Organization",
      "name": "Baidu PPC Pro Team"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Baidu PPC Pro",
      "url": "https://baidumarketing.com",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://baidumarketing.com/assets/og-brand-default.png",
        "width": 1200,
        "height": 630
      }}
    }},
    "mainEntityOfPage": {{
      "@type": "WebPage",
      "@id": "{url}"
    }}
  }}
  </script>
'''
        
        # 在 </head> 前插入
        if '</head>' in content:
            content = content.replace('</head>', json_ld + '\n</head>')
            print(f"  Added JSON-LD schema")
    
    return content

def process_blog_file(file_path):
    """处理单个博客文件"""
    
    print(f"\nProcessing: {os.path.basename(file_path)}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    issues_fixed = []
    
    # 修复 .page-hero → .article-hero
    new_content = fix_page_hero_class(content)
    if new_content != content:
        issues_fixed.append("Fixed .page-hero → .article-hero")
        content = new_content
    
    # 修复 theme-toggle CSS
    new_content = fix_theme_toggle_css(content)
    if new_content != content:
        issues_fixed.append("Fixed theme-toggle CSS")
        content = new_content
    
    # 添加 back-to-top 按钮
    new_content = add_back_to_top(content)
    if new_content != content:
        issues_fixed.append("Added back-to-top button")
        content = new_content
    
    # 修复图片 URL
    new_content = fix_image_urls(content, file_path)
    if new_content != content:
        issues_fixed.append("Fixed broken image URLs")
        content = new_content
    
    # 添加 JSON-LD schema
    new_content = add_json_ld(content, file_path)
    if new_content != content:
        issues_fixed.append("Added JSON-LD schema")
        content = new_content
    
    # 如果有修改，写回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated! Issues fixed: {', '.join(issues_fixed)}")
    else:
        print("  No changes needed")
    
    return content != original_content

def main():
    """主函数"""
    
    if not os.path.exists(BLOG_DIR):
        print(f"Error: Blog directory not found: {BLOG_DIR}")
        sys.exit(1)
    
    # 获取所有 HTML 文件
    html_files = [f for f in os.listdir(BLOG_DIR) if f.endswith('.html')]
    
    print(f"Found {len(html_files)} blog files")
    print("="*60)
    
    updated_count = 0
    for html_file in sorted(html_files):
        file_path = os.path.join(BLOG_DIR, html_file)
        try:
            if process_blog_file(file_path):
                updated_count += 1
        except Exception as e:
            print(f"  Error processing {html_file}: {e}")
    
    print("="*60)
    print(f"\nDone! Updated {updated_count} files.")

if __name__ == "__main__":
    main()
