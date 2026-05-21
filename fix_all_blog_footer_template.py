#!/usr/bin/env python3
"""
fix_all_blog_footer_template.py - 使用正确的 footer 模板修复所有博客文件
方法：找到 <footer> 和 </footer> 标签，替换中间的所有内容为模板
"""
import sys
import os
import glob
import re

def get_correct_footer_template(slug='TEMPLATE'):
    """从已修复的文件读取正确的 footer 模板"""
    template_path = 'blog/baidu-ad-billing-models-explained.html'
    if not os.path.exists(template_path):
        print(f"❌ 模板文件不存在: {template_path}")
        return None
    
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 找到 <footer> 和 </footer>
    footer_start = html.find('<footer>')
    if footer_start == -1:
        print(f"❌ 模板文件中未找到 <footer>")
        return None
    
    footer_end = html.find('</footer>', footer_start)
    if footer_end == -1:
        print(f"❌ 模板文件中未找到 </footer>")
        return None
    
    footer_end += len('</footer>')
    template = html[footer_start:footer_end]
    
    return template

def fix_file(path, template):
    """修复单个文件的 footer"""
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    slug = os.path.basename(path).replace('.html', '')
    modified = False
    
    # 找到文件的 <footer> 和 </footer>
    footer_start = html.find('<footer>')
    if footer_start == -1:
        print(f"  ⚠️ 未找到 <footer>: {path}")
        return False
    
    footer_end = html.find('</footer>', footer_start)
    if footer_end == -1:
        print(f"  ❌ 未找到 </footer>: {path}")
        return False
    
    footer_end += len('</footer>')
    
    # 替换 footer 部分
    before_footer = html[:footer_start]
    after_footer = html[footer_end:]
    
    # 替换 slug
    new_footer = template.replace('/blog/TEMPLATE', f'/blog/{slug}').replace('/ja/blog/TEMPLATE', f'/ja/blog/{slug}')
    
    html = before_footer + new_footer + after_footer
    modified = True
    
    # 修复 title 长度
    title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if title_match:
        title = title_match.group(1)
        if len(title) > 70:
            parts = title.rsplit(' — ', 1)
            if len(parts) == 2:
                main_title = parts[0]
                suffix = parts[1]
                max_len = 70 - len(suffix) - 3
                if max_len > 0 and len(main_title) > max_len:
                    new_title = main_title[:max_len-3] + '... — ' + suffix
                    html = html.replace(f'<title>{title}</title>', f'<title>{new_title}</title>')
                    print(f"  ✅ 缩短 title: {len(title)} → {len(new_title)} 字符")
    
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ 修复完成: {path}")
        return True
    
    return False

def main():
    # 获取所有博客文件
    files = sorted(glob.glob('blog/*.html'))
    
    print(f"找到 {len(files)} 个博客文件")
    print("=" * 50)
    
    # 读取正确的 footer 模板
    template = get_correct_footer_template()
    if not template:
        print("❌ 无法读取模板，退出")
        sys.exit(1)
    
    print(f"✅ 已读取 footer 模板")
    print()
    
    # 修复所有文件
    success_count = 0
    for i, path in enumerate(files, 1):
        slug = os.path.basename(path)
        print(f"[{i}/{len(files)}] 处理: {slug}")
        
        try:
            if fix_file(path, template):
                success_count += 1
        except Exception as e:
            print(f"  ❌ 异常: {e}")
    
    # 汇总
    print()
    print("=" * 50)
    print(f"✅ 成功: {success_count}/{len(files)}")
    print(f"❌ 失败: {len(files) - success_count}")

if __name__ == '__main__':
    main()
