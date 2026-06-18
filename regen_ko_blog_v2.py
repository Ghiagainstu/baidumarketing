#!/usr/bin/env python3
"""
regen_ko_blog_v2.py — 从 EN 模板 + KO 内容生成正确的韩语博客
用法：python regen_ko_blog_v2.py <slug>
"""
import sys
import re
import os

PROJECT = os.path.dirname(os.path.abspath(__file__))

def extract_ko_meta(ko_html):
    """从现有 KO 文件中提取韩语元数据和正文"""
    meta = {}
    
    # Title
    m = re.search(r'<title>(.*?)</title>', ko_html)
    if m: meta['title'] = m.group(1)
    
    # Description
    m = re.search(r'<meta name="description" content="(.*?)"', ko_html)
    if m: meta['description'] = m.group(1)
    
    # H1
    m = re.search(r'<h1[^>]*>(.*?)</h1>', ko_html, re.DOTALL)
    if m: meta['h1'] = m.group(1).strip()
    
    # OG title
    m = re.search(r'<meta property="og:title" content="(.*?)"', ko_html)
    if m: meta['og_title'] = m.group(1)
    
    # OG description
    m = re.search(r'<meta property="og:description" content="(.*?)"', ko_html)
    if m: meta['og_desc'] = m.group(1)
    
    # Article meta (date, read time, category, author)
    m = re.search(r'<div class="article-meta">(.*?)</div>', ko_html, re.DOTALL)
    if m:
        meta_html = m.group(1)
        spans = re.findall(r'<span>(.*?)</span>', meta_html)
        meta['meta_spans'] = [s.strip() for s in spans if s.strip() and s.strip() != '·']
    
    # Article body (inside article-content)
    m = re.search(r'<article class="article-content">(.*?)</article>', ko_html, re.DOTALL)
    if m:
        body = m.group(1).strip()
        # Remove meta div if present at start
        body = re.sub(r'^\s*<div class="article-meta">.*?</div>\s*', '', body, flags=re.DOTALL)
        # Remove h1 if present at start
        body = re.sub(r'^\s*<h1[^>]*>.*?</h1>\s*', '', body, flags=re.DOTALL)
        meta['body'] = body.strip()
    
    return meta


def regen_page(slug):
    en_path = os.path.join(PROJECT, 'blog', f'{slug}.html')
    ko_path = os.path.join(PROJECT, 'ko', 'blog', f'{slug}.html')
    
    if not os.path.exists(en_path):
        print(f'❌ EN file not found: {en_path}')
        return False
    if not os.path.exists(ko_path):
        print(f'❌ KO file not found: {ko_path}')
        return False
    
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
    with open(ko_path, 'r', encoding='utf-8') as f:
        ko_html = f.read()
    
    # Extract KO metadata
    ko = extract_ko_meta(ko_html)
    print(f'  KO title: {ko.get("title", "N/A")[:60]}')
    print(f'  KO body length: {len(ko.get("body", ""))}')
    print(f'  KO meta spans: {ko.get("meta_spans", [])}')
    
    # Start with EN HTML
    html = en_html
    
    # 1. lang
    html = html.replace('<html lang="en">', '<html lang="ko">')
    
    # 2. Title
    if 'title' in ko:
        en_title = re.search(r'<title>(.*?)</title>', html).group(1)
        html = html.replace(f'<title>{en_title}</title>', f'<title>{ko["title"]}</title>')
    
    # 3. Description
    if 'description' in ko:
        en_desc = re.search(r'<meta name="description" content="(.*?)"', html)
        if en_desc:
            html = html.replace(f'content="{en_desc.group(1)}"', f'content="{ko["description"]}"', 1)
    
    # 4. Canonical
    html = html.replace(f'href="https://www.baidumarketing.com/blog/{slug}"',
                        f'href="https://www.baidumarketing.com/ko/blog/{slug}"')
    
    # 5. Hreflang - add ko
    if 'hreflang="ko"' not in html:
        html = html.replace(
            '<link rel="alternate" hreflang="x-default"',
            f'<link rel="alternate" hreflang="ko" href="https://www.baidumarketing.com/ko/blog/{slug}" />\n  <link rel="alternate" hreflang="x-default"'
        )
    
    # 6. OG tags
    if 'og_title' in ko:
        en_og = re.search(r'<meta property="og:title" content="(.*?)"', html)
        if en_og:
            html = html.replace(f'content="{en_og.group(1)}"', f'content="{ko["og_title"]}"', 1)
    if 'og_desc' in ko:
        en_og_desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
        if en_og_desc:
            html = html.replace(f'content="{en_og_desc.group(1)}"', f'content="{ko["og_desc"]}"', 1)
    html = html.replace(f'content="https://www.baidumarketing.com/blog/{slug}"',
                        f'content="https://www.baidumarketing.com/ko/blog/{slug}"')
    
    # 7. Twitter tags
    if 'og_title' in ko:
        en_tw = re.search(r'<meta name="twitter:title" content="(.*?)"', html)
        if en_tw:
            html = html.replace(f'content="{en_tw.group(1)}"', f'content="{ko["og_title"]}"', 1)
    if 'og_desc' in ko:
        en_tw_desc = re.search(r'<meta name="twitter:description" content="(.*?)"', html)
        if en_tw_desc:
            html = html.replace(f'content="{en_tw_desc.group(1)}"', f'content="{ko["og_desc"]}"', 1)
    
    # 8. JSON-LD
    en_ld = re.search(r'"headline":"(.*?)"', html)
    if en_ld and 'og_title' in ko:
        html = html.replace(f'"headline":"{en_ld.group(1)}"', f'"headline":"{ko["og_title"]}"')
    en_ld_desc = re.search(r'"description":"(.*?)"', html)
    if en_ld_desc and 'description' in ko:
        html = html.replace(f'"description":"{en_ld_desc.group(1)}"', f'"description":"{ko["description"]}"')
    html = html.replace(f'"url":"https://www.baidumarketing.com/blog/{slug}"',
                        f'"url":"https://www.baidumarketing.com/ko/blog/{slug}"')
    html = html.replace(f'"@id":"https://www.baidumarketing.com/blog/{slug}"',
                        f'"@id":"https://www.baidumarketing.com/ko/blog/{slug}"')
    html = html.replace('"name":"Baidu PPC Pro Team"', '"name":"Baidu PPC Pro 팀"')
    
    # 9. Nav links
    nav_map = {
        'Why Baidu PPC Pro': '바이두 PPC Pro란',
        'Services': '서비스',
        'Pricing': '요금',
        'Clients': '도입 사례',
        'FAQ': '자주 묻는 질문',
        'About': '회사 소개',
        'Blog': '블로그',
        'Contact': '문의하기',
    }
    # Fix nav hrefs
    for path in ['why-baidu-ppc-pro', 'features', 'pricing', 'clients', 'faq', 'about', 'blog', 'contact']:
        html = html.replace(f'href="/{path}"', f'href="/ko/{path}"')
    # Fix nav text
    for en, ko_text in nav_map.items():
        html = html.replace(f'>{en}<', f'>{ko_text}<')
    
    # 10. Logo link
    html = html.replace('href="/" class="nav-logo"', 'href="/ko/" class="nav-logo"')
    
    # 11. CTA button
    html = html.replace('>Get Started &rarr;</a>', '>지금 시작하기 →</a>')
    html = html.replace('href="/contact" class="nav-cta"', 'href="/ko/contact" class="nav-cta"')
    
    # 12. Language switcher
    html = html.replace('aria-label="Language">&#x1f1fa;&#x1f1f8;',
                        'aria-label="언어">🇰🇷')
    # Add KO link if missing
    if f'lang="ko"' not in html:
        # Find lang-switch-menu and add KO
        html = re.sub(
            r'(<a href="/ja/blog/[^"]*" lang="ja" class="lang-switch-item">[^<]*</a>)\s*(</div>)',
            rf'\1\n            <a href="/ko/blog/{slug}" lang="ko" class="lang-switch-item">🇰🇷 한국어</a>\n          \2',
            html
        )
    # Fix existing lang links
    html = html.replace('&#x1f1fa;&#x1f1f8; English', '🇺🇸 English')
    html = html.replace('&#x1f1ef;&#x1f1f5; 日本語', '🇯🇵 日本語')
    
    # 13. Breadcrumb
    html = html.replace('>Home</a>', '>홈</a>')
    html = re.sub(r'href="/">홈', 'href="/ko">홈', html)
    html = html.replace('href="/blog">Blog', 'href="/ko/blog">블로그')
    
    # 14. Article hero title
    if 'h1' in ko:
        en_h1 = re.search(r'<h1 class="article-title">(.*?)</h1>', html)
        if en_h1:
            html = html.replace(f'<h1 class="article-title">{en_h1.group(1)}</h1>',
                                f'<h1 class="article-title">{ko["h1"]}</h1>')
    
    # 15. Article meta (date, read time, category, author)
    if 'meta_spans' in ko and ko['meta_spans']:
        spans = ko['meta_spans']
        # Find the article-meta div
        en_meta = re.search(r'(<div class="article-meta">)(.*?)(</div>)', html, re.DOTALL)
        if en_meta:
            new_meta_spans = []
            for s in spans:
                if s and s != '·':
                    new_meta_spans.append(f'      <span>{s}</span>')
            new_meta = '\n'.join(new_meta_spans)
            html = html.replace(en_meta.group(0),
                                f'{en_meta.group(1)}\n{new_meta}\n    {en_meta.group(3)}')
    
    # 16. Article body
    if 'body' in ko:
        # Find article-content div and replace content
        en_article = re.search(r'(<article class="article-content">)(.*?)(</article>)', html, re.DOTALL)
        if en_article:
            html = html.replace(en_article.group(0),
                                f'{en_article.group(1)}\n{ko["body"]}\n    {en_article.group(3)}')
    
    # 17. Footer
    footer_map = {
        'Quick Links': '바로가기',
        'About Us': '회사 소개',
        'Submit a Request': '문의 접수',
        'Legal': '법적 고지',
        'Privacy Policy': '개인정보 처리방침',
        'Terms of Service': '이용약관',
    }
    for en_text, ko_text in footer_map.items():
        html = html.replace(f'>{en_text}<', f'>{ko_text}<')
    # Footer links
    for path in ['features', 'pricing', 'about', 'faq', 'blog', 'contact', 'privacy', 'terms']:
        # Only replace in footer area (simple heuristic)
        pass
    # Copyright
    html = html.replace('Baidu PPC Pro. All rights reserved.', 'Baidu PPC Pro. 무단전재를 금지합니다.')
    # Footer description
    html = html.replace(
        "We help international agencies and brands access China's $100B+ digital advertising market with compliance, clarity, and zero guesswork.",
        '해외 에이전시와 브랜드가 컴플라이언스를 준수하며 중국 디지털 광고 시장에 진출할 수 있도록 지원합니다.'
    )
    html = html.replace(
        "We help international agencies and brands access China's $100B+ digital advertising market with compliance, clarity, and zero guesswork — one platform, end to end.",
        '해외 에이전시와 브랜드가 컴플라이언스를 준수하며 중국 디지털 광고 시장에 진출할 수 있도록 지원합니다.'
    )
    
    # 18. CTA section
    html = html.replace('href="/contact" class="cta-btn"', 'href="/ko/contact" class="cta-btn"')
    html = html.replace('href="/contact" class="cta-button"', 'href="/ko/contact" class="cta-button"')
    
    # 19. Related section - translate section title and card text
    html = html.replace('>More from the Blog<', '>관련 기사<')
    # Fix related card links to /ko/
    html = re.sub(r'href="/" class="related-card"', 'href="/ko/" class="related-card"', html)
    html = re.sub(r'href="/blog/', 'href="/ko/blog/', html)
    
    # Translate related card content (generic translations for common cards)
    related_translations = {
        'Why Baidu? The Numbers': '바이두? 숫자로 보는 이유',
        'How Baidu Feed Ads Work': '바이두 피드 광고 작동 방식',
        'Why Baidu Ads for Foreign Businesses': '해외 기업이 바이두 광고를 해야 하는 이유',
        "Baidu's Merchant Agent Full-Chain AI Upgrade": '바이두 상가 지능체, 풀체인 AI 업그레이드',
        'Baidu Search De-Prioritized AI Results': '바이두 검색이 AI 결과를 하향 조정',
        '6 Baidu Product Updates in 7 Days': '바이두 6개 제품 업데이트',
        '708M MAU, 15B daily feed, 3.4B POIs — the scale behind China\'s largest search ecosystem.':
            '7억 8000만 MAU, 150억 일일 피드, 34억 POI — 중국 최대 검색 생태계의 규모.',
        'The discovery complement to search advertising powered by search intent data.':
            '검색 의도 데이터로 구동되는 검색 광고의 발견형 보완.',
        'The case for Baidu advertising as a core channel for international brands.':
            '해외 브랜드의 핵심 채널로서 바이두 광고의 사례.',
        '5 new AI capabilities powering creative, bidding, and analytics.':
            '크리에이티브, 입찰, 분석을 지원하는 5가지 새로운 AI 기능.',
        'Web links and ads back on top — what it means for PPC and SEO.':
            '웹 링크와 광고가 상위로 복귀 — PPC와 SEO에 미치는 영향.',
        'Merchant Agent, Qingge, diagnostics, and more rolled out in one week.':
            '상가 지능체, 경가, 진단 도구가 1주일 내 일제 투입.',
    }
    for en_text, ko_text in related_translations.items():
        html = html.replace(f'>{en_text}<', f'>{ko_text}<')
        html = html.replace(f'>{en_text}</h4>', f'>{ko_text}</h4>')
        html = html.replace(f'>{en_text}</p>', f'>{ko_text}</p>')
    
    # Write
    with open(ko_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'✅ Generated: {ko_path}')
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python regen_ko_blog_v2.py <slug>')
        sys.exit(1)
    regen_page(sys.argv[1])
