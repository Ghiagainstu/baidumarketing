#!/usr/bin/env python3
"""
fix_blog_format.py — 修复韩语博客正文格式
1. <p>--- </p> → <hr>
2. <strong>问题</strong> → <h3>问题</h3>（独立行的问题）
3. 修复 Key Takeaways 中的英文
4. 修复未闭合的标签
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
    
    # 1. 修复 <p>--- </p> → <hr>
    content = re.sub(r'<p>---\s*</p>', '<hr>', content)
    
    # 2. 修复独立行的 <strong>问题</strong> → <h3>问题</h3>
    # 匹配以 <strong> 开头并以 </strong> 结尾的独立行
    content = re.sub(
        r'^<strong>([^<]+)</strong>\s*$',
        r'<h3>\1</h3>',
        content,
        flags=re.MULTILINE
    )
    
    # 3. 修复 <strong>문장.</strong> text → <p><strong>문장.</strong> text</p>
    # 匹配以 <strong> 开头但不在 <p> 标签内的行
    def fix_strong_line(m):
        line = m.group(0).strip()
        if line.startswith('<p>') or line.startswith('<h'):
            return line
        return f'<p>{line}</p>'
    
    # 匹配独立的 <strong>...</strong> 行
    content = re.sub(
        r'^(<strong>[^<]+</strong>[^\n]*)$',
        fix_strong_line,
        content,
        flags=re.MULTILINE
    )
    
    # 4. 修复 Key Takeaways 中的英文
    content = content.replace(
        '<h3>📝 Key Takeaways</h3>',
        '<h3>📝 핵심 요약</h3>'
    )
    content = content.replace(
        'Baidu advertising platform continues to evolve with new features',
        '바이두 광고 플랫폼은 지속적으로 새로운 기능을 추가하고 있습니다'
    )
    
    # 5. 修复 takeaway-box 中的英文
    content = content.replace(
        '>해외 광고주는 적절한 파트너와 함께 이러한 업데이트의 이점을 누릴 수 있습니다<',
        '>해외 광고주는 적절한 파트너와 함께 이러한 업데이트의 이점을 누릴 수 있습니다<'
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 60)
    print("🇰🇷 修复韩语博客正文格式")
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
