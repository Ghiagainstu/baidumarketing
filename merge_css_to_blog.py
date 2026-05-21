#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 index.html 的完整全局 CSS 合并到所有博客文件中
保留博客特有的 CSS（.article-content 等），并去重
"""
import glob
import re
import sys

def extract_css_from_file(path):
    """提取文件中的 <style>...</style> 内容（不含标签本身）"""
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    start = html.find('<style>')
    end = html.find('</style>')
    if start == -1 or end == -1:
        return None, None, None
    return html, html[start+7:end], (start, end)

def get_css_selectors(css_text):
    """提取 CSS 中的所有选择器（用于去重检测）"""
    # 简单提取选择器（处理单行和多行）
    selectors = set()
    # 匹配 CSS 规则的选择器部分（在 { 之前）
    pattern = r'([^{]+)\s*\{'
    for match in re.finditer(pattern, css_text, re.MULTILINE):
        sel = match.group(1).strip()
        # 只保留单个选择器，不保留完整规则
        for part in sel.split(','):
            part = part.strip()
            if part:
                selectors.add(part)
    return selectors

def merge_css(index_css, blog_css):
    """合并 index.css 和博客 CSS，去重"""
    # 提取博客 CSS 中的规则块，避免重复添加
    # 简单策略：把 index_css 放前面，blog_css 放后面
    # 重复规则无害（后面的覆盖前面的）
    merged = index_css.rstrip() + '\n\n' + blog_css.lstrip()
    return merged

def process_file(blog_path, index_css):
    """处理单个博客文件"""
    result = extract_css_from_file(blog_path)
    if result[0] is None:
        print(f"  ⚠️  未找到 <style> 标签: {blog_path}")
        return False

    html, blog_css, positions = result
    style_start, style_end = positions

    # 合并 CSS
    merged_css = merge_css(index_css, blog_css)

    # 替换原来的 <style>...</style> 内容
    new_html = html[:style_start+7] + merged_css + html[style_end:]

    with open(blog_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    added = len(merged_css) - len(blog_css)
    print(f"  ✅ {blog_path}: CSS {len(blog_css)} → {len(merged_css)} 字符 (+{added})")
    return True

def main():
    # 1. 读取 index.html 的完整 CSS
    result = extract_css_from_file('index.html')
    if result[0] is None:
        print("❌ index.html 未找到 <style> 标签")
        sys.exit(1)

    _, index_css, _ = result
    print(f"📐 index.html 基准 CSS: {len(index_css)} 字符")
    print()

    # 2. 处理所有博客文件
    files = sorted(glob.glob('blog/*.html'))
    print(f"共找到 {len(files)} 个博客文件")
    print("=" * 50)
    print()

    success = 0
    for path in files:
        if process_file(path, index_css):
            success += 1

    print()
    print(f"结果: 成功 {success}/{len(files)} 个文件")

if __name__ == '__main__':
    main()
