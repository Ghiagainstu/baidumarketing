#!/usr/bin/env python3
"""
fix_blog_markdown_v2.py — 修复韩语博客中的 Markdown 语法 v2
1. # text → <h1>text</h1>
2. ## text → <h2>text</h2>
3. ### text → <h3>text</h3>
4. > text → <blockquote><p>text</p></blockquote>
5. **text** → <strong>text</strong>
6. - item → <li>item</li>
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
    
    # 1. 修复 # text → <h1>text</h1>
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    
    # 2. 修复 ## text → <h2>text</h2>
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    
    # 3. 修复 ### text → <h3>text</h3>
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    
    # 4. 修复 > text → <blockquote><p>text</p></blockquote>
    # 匹配多行 blockquote
    def fix_blockquote(m):
        lines = m.group(0).split('\n')
        text = '\n'.join(line[2:] if line.startswith('> ') else line[1:] if line.startswith('>') else line for line in lines)
        return f'<blockquote><p>{text.strip()}</p></blockquote>'
    
    content = re.sub(r'^(> .+\n?)+$', fix_blockquote, content, flags=re.MULTILINE)
    
    # 5. 修复 **text** → <strong>text</strong>
    content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
    
    # 6. 修复 - item → <li>item</li>
    # 匹配连续的 - item 行
    def fix_list(m):
        lines = m.group(0).split('\n')
        items = []
        for line in lines:
            if line.startswith('- '):
                items.append(f'<li>{line[2:]}</li>')
            elif line.startswith('-'):
                items.append(f'<li>{line[1:]}</li>')
        return '<ul>\n' + '\n'.join(items) + '\n</ul>'
    
    content = re.sub(r'^(?:- .+\n?)+$', fix_list, content, flags=re.MULTILINE)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 60)
    print("🇰🇷 修复韩语博客 Markdown 语法 v2")
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
