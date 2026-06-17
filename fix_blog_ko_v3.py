#!/usr/bin/env python3
"""
fix_blog_ko_v3.py — 批量修复韩语博客详情页
1. 修复语言切换器: HTML entities → emoji, 修正链接指向当前页面
2. 修复 aria-label
3. 修复日期格式
4. 修复阅读时间
"""
import re
import os
import glob

PROJECT = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(PROJECT, "ko", "blog")

# 日期映射
DATE_MAP = {
    'Jul 9, 2020': '2020년 7월 9일',
    'Sep 14, 2022': '2022년 9월 14일',
    'Jun 11, 2026': '2026년 6월 11일',
    'Jun 12, 2026': '2026년 6월 12일',
    'Jun 13, 2026': '2026년 6월 13일',
    'Jun 14, 2026': '2026년 6월 14일',
    'Jun 15, 2026': '2026년 6월 15일',
    'Jun 16, 2026': '2026년 6월 16일',
}

def fix_file(filepath):
    """修复单个文件"""
    basename = os.path.basename(filepath)
    if basename.startswith("_"):
        return False
    
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
    
    # 3. 修复语言切换器链接 — 通用 regex 替换
    # 处理 lang="en" 链接
    content = re.sub(
        r'<a\s+href="[^"]*"\s+lang="en"\s+class="lang-switch-item">',
        f'<a href="/blog/{slug}" lang="en" class="lang-switch-item">',
        content
    )
    # 处理 lang="ja" 链接
    content = re.sub(
        r'<a\s+href="[^"]*"\s+lang="ja"\s+class="lang-switch-item">',
        f'<a href="/ja/blog/{slug}" lang="ja" class="lang-switch-item">',
        content
    )
    # 处理 lang="ko" 链接
    content = re.sub(
        r'<a\s+href="[^"]*"\s+lang="ko"\s+class="lang-switch-item">',
        f'<a href="/ko/blog/{slug}" lang="ko" class="lang-switch-item">',
        content
    )
    
    # 4. 修复日期格式
    for en_date, ko_date in DATE_MAP.items():
        content = content.replace(f'>{en_date}<', f'>{ko_date}<')
        # 也处理 &gt; 格式
        content = content.replace(f'> {en_date}<', f'> {ko_date}<')
    
    # 通用日期格式: Mon DD, YYYY → YYYY년 M월 D일
    month_map = {
        'Jan': '1월', 'Feb': '2월', 'Mar': '3월', 'Apr': '4월',
        'May': '5월', 'Jun': '6월', 'Jul': '7월', 'Aug': '8월',
        'Sep': '9월', 'Oct': '10월', 'Nov': '11월', 'Dec': '12월',
    }
    def replace_date(m):
        month_en, day, year = m.group(1), m.group(2).lstrip('0'), m.group(3)
        month_ko = month_map.get(month_en, month_en)
        return f'>{year}년 {month_ko} {day}일<'
    content = re.sub(r'>(\w{3}) (\d{1,2}), (\d{4})<', replace_date, content)
    
    # 5. 修复阅读时间: N min → N분 읽기
    content = re.sub(r'>(\d+) min<', r'>\1분 읽기<', content)
    
    # 6. 修复作者
    content = content.replace('By Baidu PPC Pro Team', 'Baidu PPC Pro 팀')
    
    # 7. 修复 &rarr; → →
    content = content.replace('&rarr;', '→')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 60)
    print("🇰🇷 批量修复韩语博客详情页 v3")
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
