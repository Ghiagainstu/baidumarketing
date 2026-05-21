#!/usr/bin/env python3
"""仅修复 JA 博客文件的 nav HTML（不重复合并CSS）"""
import glob

def get_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# 读取 ja/index.html 的正确 nav 模板
ja_idx = get_file('ja/index.html')
nav_start = ja_idx.find('<nav>')
nav_end = ja_idx.find('</nav>') + len('</nav>')
JA_NAV = ja_idx[nav_start:nav_end]

# 需要修复的文件
files = [
    'ja/blog/baidu-ad-creation-workflow-simplified-creative-upgrade.html',
    'ja/blog/baidu-ad-performance-diagnostic-tool.html',
    'ja/blog/baidu-audience-targeting-guide.html',
    'ja/blog/baidu-brand-info-account-level.html',
    'ja/blog/baidu-brand-zone-generic-keywords.html',
    'ja/blog/baidu-click-fraud-ipv4-blocking.html',
    'ja/blog/baidu-conversion-tracking-dedup.html',
    'ja/blog/baidu-creative-url-retirement-migration.html',
    'ja/blog/baidu-feed-ads-history-operation-records-upgrade.html',
    'ja/blog/baidu-landing-page-audit-rejection-reasons.html',
    'ja/blog/baidu-landing-page-report.html',
    'ja/blog/baidu-ocpc-skip-data-accumulation.html',
    'ja/blog/baidu-search-ads-1-1-desktop-images.html',
    'ja/blog/baidu-search-device-bid-coefficient-retirement.html',
    'ja/blog/china-internet-numbers-2025.html',
    'ja/blog/faq-international-brands.html',
]

for path in files:
    slug_raw = path.split('/')[-1].replace('.html', '')
    html = get_file(path)
    
    old_nav_s = html.find('<nav')
    old_nav_e = html.find('</nav>') + len('</nav>')
    if old_nav_s == -1:
        print(f"  ⚠️ {path}: 未找到 <nav>")
        continue
    
    # 生成正确 nav
    new_nav = JA_NAV.replace(
        '<a href="/ja/contact.html" class="nav-mobile-cta">今すぐ始める →</a>',
        ''
    )
    new_nav = new_nav.replace(
        '<a href="/ja/blog.html">ブログ</a>',
        '<a href="/ja/blog.html" class="active">ブログ</a>'
    )
    # 语言切换器 - 博客页用博客 slug
    new_nav = new_nav.replace(
        'href="/" lang="en"',
        f'href="/blog/{slug_raw}" lang="en"'
    )
    new_nav = new_nav.replace(
        'href="/ja/" lang="ja"',
        f'href="/ja/blog/{slug_raw}" lang="ja"'
    )
    
    html = html[:old_nav_s] + new_nav + html[old_nav_e:]
    write_file(path, html)
    print(f"  ✅ {path.split('/')[-1]}: nav 已替换")

print(f"\n完成: {len(files)} 个文件")
