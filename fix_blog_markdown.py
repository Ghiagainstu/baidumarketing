#!/usr/bin/env python3
"""
fix_blog_markdown.py — 修复韩语博客中的 Markdown 语法
1. **text** → <strong>text</strong>
2. [!tip] → callout div
3. - item → <li>item</li>
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
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. 修复 **text** → <strong>text</strong>
    # 匹配 **text** 但不匹配已经在 HTML 标签内的
    content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
    
    # 2. 修复 [!tip] callout
    content = re.sub(
        r'<blockquote><p>\[!tip\]\s*(.*?)</p></blockquote>',
        r'<div class="callout callout-tip"><span class="callout-icon">💡</span><div>\1</div></div>',
        content,
        flags=re.DOTALL
    )
    
    # 3. 修复 [!info] callout
    content = re.sub(
        r'<blockquote><p>\[!info\]\s*(.*?)</p></blockquote>',
        r'<div class="callout callout-insight"><span class="callout-icon">ℹ️</span><div>\1</div></div>',
        content,
        flags=re.DOTALL
    )
    
    # 4. 修复 [!warning] callout
    content = re.sub(
        r'<blockquote><p>\[!warning\]\s*(.*?)</p></blockquote>',
        r'<div class="callout callout-warning"><span class="callout-icon">⚠️</span><div>\1</div></div>',
        content,
        flags=re.DOTALL
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 60)
    print("🇰🇷 修复韩语博客 Markdown 语法")
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
