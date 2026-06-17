#!/usr/bin/env python3
"""
fix_blog_ko_v2.py — 批量修复韩语博客详情页
1. 修复语言切换器: HTML entities → emoji, 修正链接
2. 修复 aria-label
"""
import re
import os
import glob

PROJECT = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(PROJECT, "ko", "blog")

def fix_file(filepath):
    """修复单个文件"""
    basename = os.path.basename(filepath)
    if basename.startswith("_"):
        return False
    
    # 从文件名提取 slug
    slug = basename.replace(".html", "")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. 修复 HTML entities → emoji
    content = content.replace('&#x1f1f0;&#x1f1f7;', '🇰🇷')
    content = content.replace('&#x1f1fa;&#x1f1f8;', '🇺🇸')
    content = content.replace('&#x1f1ef;&#x1f1f5;', '🇯🇵')
    
    # 2. 修复 aria-label
    content = content.replace('aria-label="言語"', 'aria-label="언어"')
    
    # 3. 修复语言切换器链接 — 找到 ko/blog/ 下的错误 slug 并替换
    # EN link: /blog/SLUG
    content = re.sub(
        r'(href="/blog/)[^"]*(" lang="en")',
        r'\g<1>' + slug + r'\2',
        content
    )
    # JA link: /ja/blog/SLUG
    content = re.sub(
        r'(href="/ja/blog/)[^"]*(" lang="ja")',
        r'\g<1>' + slug + r'\2',
        content
    )
    # KO link: /ko/blog/SLUG
    content = re.sub(
        r'(href="/ko/blog/)[^"]*(" lang="ko")',
        r'\g<1>' + slug + r'\2',
        content
    )
    
    # 4. 修复旧版 nav-cta 格式
    content = content.replace('지금 시작하기 &rarr;', '지금 시작하기 →')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 60)
    print("🇰🇷 批量修复韩语博客详情页 v2")
    print("=" * 60)
    
    files = glob.glob(os.path.join(BLOG_DIR, "*.html"))
    files = [f for f in files if "_template" not in os.path.basename(f)]
    
    fixed = 0
    for filepath in sorted(files):
        basename = os.path.basename(filepath)
        if fix_file(filepath):
            print(f"  ✓ Fixed: {basename}")
            fixed += 1
        else:
            print(f"  - No changes: {basename}")
    
    print("=" * 60)
    print(f"✅ 完成: {fixed}/{len(files)} 个文件已修复")
    print("=" * 60)


if __name__ == "__main__":
    main()
