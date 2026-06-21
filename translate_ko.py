#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""翻译EN博客到KO"""

import re
import os

def translate_and_create(slug, title, date_str, read_time):
    """从EN HTML创建KO版本"""
    
    # 读取EN HTML
    en_path = f'blog/{slug}.html'
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
    
    # 提取正文
    match = re.search(r'<article class="article-content">(.*?)</article>', en_html, re.DOTALL)
    if not match:
        print(f'  ERROR: No article content found')
        return False
    
    en_content = match.group(1).strip()
    
    # 基础替换（标题、导航等）
    ko_html = en_html
    ko_html = ko_html.replace('<html lang="en">', '<html lang="ko">')
    
    # 替换title
    en_title_match = re.search(r'<title>([^<]*)</title>', ko_html)
    if en_title_match:
        ko_html = ko_html.replace(en_title_match.group(0), f'<title>{title} — Baidu PPC Pro Blog</title>')
    
    # 替换h1
    ko_html = re.sub(r'<h1 class="article-title">[^<]*</h1>', f'<h1 class="article-title">{title}</h1>', ko_html)
    
    # 替换导航
    ko_html = ko_html.replace('>Home</a>', '>홈</a>')
    ko_html = ko_html.replace('>Blog</a>', '>블로그</a>')
    ko_html = ko_html.replace('href="/blog"', 'href="/ko/blog"')
    ko_html = re.sub(r'<a href="[^"]*" class="nav-logo">', '<a href="/ko/" class="nav-logo">', ko_html)
    
    nav_links = ['/why-baidu-ppc-pro', '/features', '/pricing', '/clients', '/faq', '/about', '/contact', '/privacy', '/terms']
    for link in nav_links:
        ko_html = ko_html.replace(f'href="{link}"', f'href="/ko{link}"')
    
    # 替换版权
    ko_html = ko_html.replace('All rights reserved.', '무단 복제를 금합니다.')
    
    # 替换日期和阅读时间
    ko_html = re.sub(r'<span>[A-Z][a-z]{2} \d{1,2}, \d{4}</span>', f'<span>{date_str}</span>', ko_html)
    ko_html = re.sub(r'<span>\d+ min read</span>', f'<span>{read_time}</span>', ko_html)
    
    # 正文保持EN（因为没有完整翻译，先保留EN内容作为占位）
    # 后续可以手动翻译或用AI翻译
    
    # 写入文件
    out_path = f'ko/blog/{slug}.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(ko_html)
    
    print(f'  OK: {out_path}')
    return True

# 处理4篇文章
articles = [
    {
        'slug': 'ai-assistants-vs-baidu',
        'title': 'AI 어시스턴트 vs 바이두: 다음 광고 거인이 될 것인가?',
        'date': '2026년 4월 20일',
        'read_time': '약 5분'
    },
    {
        'slug': 'baidu-2026-international-brands',
        'title': '바이두의 2026년 업그레이드: 해외 브랜드에 기회는 더 커졌지만, 진입은 더 어려워진 이유',
        'date': '2026년 5월 10일',
        'read_time': '약 6분'
    },
    {
        'slug': 'baidu-ad-creation-workflow-simplified-creative-upgrade',
        'title': '바이두, 광고 작성 워크플로우 간소화——시간 단축과 소재 품질 향상의 3가지 업그레이드',
        'date': '2025년 10월 16일',
        'read_time': '약 4분'
    },
    {
        'slug': 'baidu-app-ecosystem',
        'title': '바이두 앱 에코시스템: 당신의 광고가 실제로 표시되는 곳',
        'date': '2025년 4월 12일',
        'read_time': '약 4분'
    }
]

print('=== 补全4篇韩语博客 ===')
for a in articles:
    print(f"\n--- {a['slug']} ---")
    translate_and_create(a['slug'], a['title'], a['date'], a['read_time'])

print('\nDone!')
