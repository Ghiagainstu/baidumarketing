#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量发布韩语博客"""

import os
import re
from datetime import datetime

# 5篇待发布
articles = [
    {
        "slug": "ai-assistants-vs-baidu",
        "ko_path": "E:/Obsidian/Baidu/01-Market-Insights/02-ai-assistants-vs-baidu/02-ai-assistants-vs-baidu-ko.md",
        "en_path": "blog/ai-assistants-vs-baidu.html",
    },
    {
        "slug": "b2b-lead-generation-framework",
        "ko_path": "E:/Obsidian/Baidu/05-Strategy/b2b-lead-generation-framework-ko/b2b-lead-generation-framework-ko-ko.md",
        "en_path": "blog/b2b-lead-generation-framework.html",
    },
    {
        "slug": "baidu-2026-international-brands",
        "ko_path": "E:/Obsidian/Baidu/01-Market-Insights/baidu-2026-international-brands/baidu-2026-international-brands-ko.md",
        "en_path": "blog/baidu-2026-international-brands.html",
    },
    {
        "slug": "baidu-ad-creation-workflow-simplified-creative-upgrade",
        "ko_path": "E:/Obsidian/Baidu/03-Search-Ads/baidu-ad-creation-workflow-simplified-creative-upgrade/baidu-ad-creation-workflow-simplified-creative-upgrade-ko.md",
        "en_path": "blog/baidu-ad-creation-workflow-simplified-creative-upgrade.html",
    },
    {
        "slug": "baidu-app-ecosystem",
        "ko_path": "E:/Obsidian/Baidu/02-Platform/07-baidu-app-ecosystem/07-baidu-app-ecosystem-ko.md",
        "en_path": "blog/baidu-app-ecosystem.html",
    },
]

def read_ko_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'^---\n.*?\n---\n*', '', content, flags=re.DOTALL)
    return content.strip()

def extract_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip().strip('"')
    return fm

def md_to_html_simple(md_text):
    lines = md_text.split('\n')
    html_lines = []
    in_list = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            continue
        if stripped.startswith('### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h3>{stripped[4:]}</h3>')
        elif stripped.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h2>{stripped[3:]}</h2>')
        elif stripped.startswith('# '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h1>{stripped[2:]}</h1>')
        elif stripped.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{stripped[2:]}</li>')
        elif stripped.startswith('<'):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(stripped)
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', stripped)
            html_lines.append(f'<p>{text}</p>')

    if in_list:
        html_lines.append('</ul>')
    return '\n'.join(html_lines)

def create_ko_html(en_html, ko_content, slug, title, date, read_time):
    html = en_html
    html = html.replace('<html lang="en">', '<html lang="ko">')
    html = re.sub(r'<link rel="canonical" href="https://www\.baidumarketing\.com/blog/[^"]*"', f'<link rel="canonical" href="https://www.baidumarketing.com/ko/blog/{slug}"', html)
    html = re.sub(r'<link rel="alternate" hreflang="en" href="[^"]*"', f'<link rel="alternate" hreflang="en" href="https://www.baidumarketing.com/blog/{slug}"', html)
    html = re.sub(r'<link rel="alternate" hreflang="ja" href="[^"]*"', f'<link rel="alternate" hreflang="ja" href="https://www.baidumarketing.com/ja/blog/{slug}"', html)
    if 'hreflang="ko"' not in html:
        html = html.replace('<link rel="alternate" hreflang="x-default"', f'<link rel="alternate" hreflang="ko" href="https://www.baidumarketing.com/ko/blog/{slug}" />\n  <link rel="alternate" hreflang="x-default"')
    html = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="https://www.baidumarketing.com/ko/blog/{slug}"', html)
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title} — Baidu PPC Pro Blog</title>', html)
    html = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{title}"', html)
    html = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{title}"', html)
    html = re.sub(r'<h1 class="article-title">[^<]*</h1>', f'<h1 class="article-title">{title}</h1>', html)
    html = re.sub(r'<span>[A-Z][a-z]{{2}} \d{{1,2}}, \d{{4}}</span>', f'<span>{date}</span>', html)
    html = re.sub(r'<span>[\d]+ min read</span>', f'<span>{read_time}</span>', html)
    html = html.replace('>Home</a>', '>홈</a>')
    html = html.replace('>Blog</a>', '>블로그</a>')
    html = html.replace('href="/blog"', 'href="/ko/blog"')
    html = re.sub(r'<a href="[^"]*" class="nav-logo">', '<a href="/ko/" class="nav-logo">', html)

    nav_links = [
        ('/why-baidu-ppc-pro', '/ko/why-baidu-ppc-pro'),
        ('/features', '/ko/features'),
        ('/pricing', '/ko/pricing'),
        ('/clients', '/ko/clients'),
        ('/faq', '/ko/faq'),
        ('/about', '/ko/about'),
        ('/contact', '/ko/contact'),
    ]
    for old_href, new_href in nav_links:
        html = html.replace(f'href="{old_href}"', f'href="{new_href}"')

    ko_html_content = md_to_html_simple(ko_content)
    html = re.sub(r'<article class="article-content">.*?</article>', f'<article class="article-content">\n{ko_html_content}\n</article>', html, flags=re.DOTALL)
    html = html.replace('href="/contact.html"', 'href="/ko/contact"')
    html = html.replace('href="/privacy"', 'href="/ko/privacy"')
    html = html.replace('href="/terms"', 'href="/ko/terms"')
    html = html.replace('All rights reserved.', '무단 복제를 금합니다.')
    return html

# 处理每篇文章
for article in articles:
    slug = article['slug']
    ko_path = article['ko_path']
    en_path = article['en_path']

    print(f"\n=== {slug} ===")

    if not os.path.exists(ko_path):
        print(f"  SKIP: KO file not found")
        continue

    ko_content = read_ko_content(ko_path)
    ko_fm = extract_frontmatter(ko_path)

    if not os.path.exists(en_path):
        print(f"  SKIP: EN HTML not found")
        continue

    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()

    title = ko_fm.get('title', slug)
    date_str = ko_fm.get('date', '2026-06-19')

    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        date_formatted = f"{dt.year}년 {dt.month}월 {dt.day}일"
    except:
        date_formatted = date_str

    char_count = len(ko_content)
    read_time_min = max(1, char_count // 600)
    read_time = f"약 {read_time_min}분"

    ko_html = create_ko_html(en_html, ko_content, slug, title, date_formatted, read_time)

    out_path = f"ko/blog/{slug}.html"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(ko_html)

    print(f"  OK: {out_path}")
    print(f"  Title: {title}")
    print(f"  Date: {date_formatted}")

print("\nDone!")
