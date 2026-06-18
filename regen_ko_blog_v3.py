#!/usr/bin/env python3
"""
regen_ko_blog_v3.py — 从 EN 模板 + KO Obsidian 生成正确的韩语博客
用法：python regen_ko_blog_v3.py <slug>
"""
import sys
import re
import os

PROJECT = os.path.dirname(os.path.abspath(__file__))

def md_to_html(md_text):
    """将 Obsidian markdown 转换为 HTML"""
    lines = md_text.split('\n')
    html_lines = []
    in_list = False
    in_blockquote = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            html_lines.append('')
            continue
        
        # Skip frontmatter
        if stripped == '---':
            continue
        
        # Headers
        if stripped.startswith('# '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h1>{stripped[2:]}</h1>')
            continue
        if stripped.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h2>{stripped[3:]}</h2>')
            continue
        if stripped.startswith('### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h3>{stripped[4:]}</h3>')
            continue
        
        # Blockquote
        if stripped.startswith('> '):
            if not in_blockquote:
                html_lines.append('<blockquote>')
                in_blockquote = True
            text = stripped[2:]
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            html_lines.append(f'<p>{text}</p>')
            continue
        elif in_blockquote:
            html_lines.append('</blockquote>')
            in_blockquote = False
        
        # Horizontal rule
        if stripped == '---' or stripped == '***':
            html_lines.append('<hr>')
            continue
        
        # Ordered list
        if re.match(r'^\d+\.\s', stripped):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            text = re.sub(r'^\d+\.\s', '', stripped)
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            html_lines.append(f'<li>{text}</li>')
            continue
        
        # Unordered list
        if stripped.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            text = stripped[2:]
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            html_lines.append(f'<li>{text}</li>')
            continue
        
        # Close list if we're in one and this isn't a list item
        if in_list:
            html_lines.append('</ul>')
            in_list = False
        
        # Regular paragraph
        text = stripped
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        html_lines.append(f'<p>{text}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    if in_blockquote:
        html_lines.append('</blockquote>')
    
    return '\n'.join(html_lines)


def regen_page(slug):
    en_path = os.path.join(PROJECT, 'blog', f'{slug}.html')
    ko_path = os.path.join(PROJECT, 'ko', 'blog', f'{slug}.html')
    
    # Search for KO MD file in all Obsidian directories
    ko_md_path = None
    obsidian_base = 'E:/Obsidian/Baidu'
    for root, dirs, files in os.walk(obsidian_base):
        for f in files:
            if f == f'{slug}-ko-ko.md':
                ko_md_path = os.path.join(root, f)
                break
        if ko_md_path:
            break
    
    if not ko_md_path:
        # Try alternative path
        ko_md_path = os.path.join(obsidian_base, f'{slug}-ko', f'{slug}-ko-ko.md')
    
    if not os.path.exists(en_path):
        print(f'❌ EN file not found: {en_path}')
        return False
    if not ko_md_path or not os.path.exists(ko_md_path):
        print(f'❌ KO MD file not found for {slug}')
        return False
    
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
    with open(ko_md_path, 'r', encoding='utf-8') as f:
        ko_md = f.read()
    
    # Extract KO metadata from frontmatter
    title_match = re.search(r'^title:\s*(.+)$', ko_md, re.MULTILINE)
    date_match = re.search(r'^date:\s*(.+)$', ko_md, re.MULTILINE)
    category_match = re.search(r'^category:\s*(.+)$', ko_md, re.MULTILINE)
    author_match = re.search(r'^author:\s*(.+)$', ko_md, re.MULTILINE)
    reading_match = re.search(r'^reading_time:\s*(.+)$', ko_md, re.MULTILINE)
    
    ko_title = title_match.group(1).strip().strip('"') if title_match else 'Untitled'
    ko_date = date_match.group(1).strip() if date_match else '2026-01-01'
    ko_category = category_match.group(1).strip() if category_match else 'platform'
    ko_author = author_match.group(1).strip() if author_match else 'Baidu PPC Pro 팀'
    ko_reading = reading_match.group(1).strip() if reading_match else '8 min'
    
    # Category map
    category_map = {
        'platform': '플랫폼',
        'strategy': '전략',
        'market-insights': '시장 인사이트',
        'search': '검색 광고',
        'feed': '피드 광고',
        'landing-page': '랜딩페이지',
    }
    ko_category_text = category_map.get(ko_category, ko_category)
    
    # Extract body (after frontmatter)
    body_match = re.search(r'^---\s*\n.*?\n---\s*\n(.*)', ko_md, re.DOTALL)
    if body_match:
        ko_body_md = body_match.group(1).strip()
    else:
        print('❌ Could not extract body from KO MD')
        return False
    
    # Remove the first H1 (title) from body
    ko_body_md = re.sub(r'^# .+\n+', '', ko_body_md, count=1)
    
    # Convert markdown to HTML
    ko_body_html = md_to_html(ko_body_md)
    
    # Start with EN HTML
    html = en_html
    
    # 1. lang
    html = html.replace('<html lang="en">', '<html lang="ko">')
    
    # 2. Title
    en_title = re.search(r'<title>(.*?)</title>', html).group(1)
    html = html.replace(f'<title>{en_title}</title>', f'<title>{ko_title} — Baidu PPC Pro 블로그</title>')
    
    # 3. Description
    en_desc = re.search(r'<meta name="description" content="(.*?)"', html)
    if en_desc:
        ko_desc = f'{ko_title}에 대한 상세 분석.'
        html = html.replace(f'content="{en_desc.group(1)}"', f'content="{ko_desc}"', 1)
    
    # 4. Canonical
    html = html.replace(f'href="https://www.baidumarketing.com/blog/{slug}"',
                        f'href="https://www.baidumarketing.com/ko/blog/{slug}"')
    
    # 5. Hreflang
    if 'hreflang="ko"' not in html:
        html = html.replace(
            '<link rel="alternate" hreflang="x-default"',
            f'<link rel="alternate" hreflang="ko" href="https://www.baidumarketing.com/ko/blog/{slug}" />\n  <link rel="alternate" hreflang="x-default"'
        )
    
    # 6. OG tags
    en_og_title = re.search(r'<meta property="og:title" content="(.*?)"', html)
    if en_og_title:
        html = html.replace(f'content="{en_og_title.group(1)}"', f'content="{ko_title}"', 1)
    en_og_desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
    if en_og_desc:
        html = html.replace(f'content="{en_og_desc.group(1)}"', f'content="{ko_title}에 대한 상세 분석."', 1)
    html = html.replace(f'content="https://www.baidumarketing.com/blog/{slug}"',
                        f'content="https://www.baidumarketing.com/ko/blog/{slug}"')
    
    # 7. Twitter tags
    en_tw_title = re.search(r'<meta name="twitter:title" content="(.*?)"', html)
    if en_tw_title:
        html = html.replace(f'content="{en_tw_title.group(1)}"', f'content="{ko_title}"', 1)
    en_tw_desc = re.search(r'<meta name="twitter:description" content="(.*?)"', html)
    if en_tw_desc:
        html = html.replace(f'content="{en_tw_desc.group(1)}"', f'content="{ko_title}에 대한 상세 분석."', 1)
    
    # 8. JSON-LD
    en_ld_title = re.search(r'"headline":"(.*?)"', html)
    if en_ld_title:
        html = html.replace(f'"headline":"{en_ld_title.group(1)}"', f'"headline":"{ko_title}"')
    en_ld_desc = re.search(r'"description":"(.*?)"', html)
    if en_ld_desc:
        html = html.replace(f'"description":"{en_ld_desc.group(1)}"', f'"description":"{ko_title}에 대한 상세 분석."')
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
    for path in ['why-baidu-ppc-pro', 'features', 'pricing', 'clients', 'faq', 'about', 'blog', 'contact']:
        html = html.replace(f'href="/{path}"', f'href="/ko/{path}"')
    for en, ko in nav_map.items():
        html = html.replace(f'>{en}<', f'>{ko}<')
    
    # 10. Logo link
    html = html.replace('href="/" class="nav-logo"', 'href="/ko/" class="nav-logo"')
    
    # 11. CTA button
    html = html.replace('>Get Started &rarr;</a>', '>지금 시작하기 →</a>')
    html = html.replace('href="/contact" class="nav-cta"', 'href="/ko/contact" class="nav-cta"')
    
    # 12. Language switcher
    html = html.replace('aria-label="Language">&#x1f1fa;&#x1f1f8;',
                        'aria-label="언어">🇰🇷')
    if f'lang="ko"' not in html:
        html = re.sub(
            r'(<a href="/ja/blog/[^"]*" lang="ja" class="lang-switch-item">[^<]*</a>)\s*(</div>)',
            rf'\1\n            <a href="/ko/blog/{slug}" lang="ko" class="lang-switch-item">🇰🇷 한국어</a>\n          \2',
            html
        )
    html = html.replace('&#x1f1fa;&#x1f1f8; English', '🇺🇸 English')
    html = html.replace('&#x1f1ef;&#x1f1f5; 日本語', '🇯🇵 日本語')
    
    # 13. Breadcrumb
    html = html.replace('>Home</a>', '>홈</a>')
    html = re.sub(r'href="/">홈', 'href="/ko">홈', html)
    html = html.replace('href="/blog">Blog', 'href="/ko/blog">블로그')
    
    # 14. Article hero
    en_h1 = re.search(r'<h1 class="article-title">(.*?)</h1>', html)
    if en_h1:
        html = html.replace(f'<h1 class="article-title">{en_h1.group(1)}</h1>',
                            f'<h1 class="article-title">{ko_title}</h1>')
    
    # 15. Article meta - preserve SVG icons
    en_meta = re.search(r'(<div class="article-meta">)(.*?)(</div>)', html, re.DOTALL)
    if en_meta:
        # Format date
        try:
            from datetime import datetime
            dt = datetime.strptime(ko_date, '%Y-%m-%d')
            ko_date_fmt = f'{dt.year}년 {dt.month}월 {dt.day}일'
        except:
            ko_date_fmt = ko_date
        
        new_meta = f'''    <div class="article-meta">
      <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> {ko_date_fmt}</span>
      <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> 약 {ko_reading.replace("min","").strip()}분</span>
      <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg> {ko_category_text}</span>
      <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> {ko_author}</span>
    </div>'''
        html = html.replace(en_meta.group(0), new_meta)
    
    # 16. Article body
    en_article = re.search(r'(<article class="article-content">)(.*?)(</article>)', html, re.DOTALL)
    if en_article:
        html = html.replace(en_article.group(0),
                            f'{en_article.group(1)}\n{ko_body_html}\n    {en_article.group(3)}')
    
    # 16b. Add visual enhancements (stats-grid, case-study, callout, takeaway-box)
    # These are added after the body content, before the CTA
    # Only add if the EN blog has them and the KO blog doesn't
    en_has_stats = 'class="stats-grid"' in en_html
    en_has_case = 'class="case-study"' in en_html
    en_has_callout = 'class="callout' in en_html
    en_has_takeaway = 'class="takeaway-box"' in en_html
    
    ko_article_match = re.search(r'<article class="article-content">(.*?)</article>', html, re.DOTALL)
    if ko_article_match:
        ko_body = ko_article_match.group(1)
        
        # Add stats-grid after first h2 if EN has it
        if en_has_stats and 'class="stats-grid"' not in ko_body:
            stats_html = '''
      <div class="stats-grid">
        <div class="stat-card"><div class="stat-value">708M</div><div class="stat-label">바이두 앱 MAU</div></div>
        <div class="stat-card"><div class="stat-value">150억+</div><div class="stat-label">일일 피드 임프레션</div></div>
        <div class="stat-card"><div class="stat-value">¥15K</div><div class="stat-label">일일 매출 사례</div></div>
        <div class="stat-card"><div class="stat-value">600+</div><div class="stat-label">B2B 리드 사례</div></div>
      </div>'''
            # Insert after first </blockquote> or first <h2>
            if '</blockquote>' in ko_body:
                ko_body = ko_body.replace('</blockquote>', '</blockquote>' + stats_html, 1)
            elif '<h2>' in ko_body:
                ko_body = ko_body.replace('<h2>', stats_html + '\n<h2>', 1)
        
        # Add takeaway-box before CTA if EN has it
        if en_has_takeaway and 'class="takeaway-box"' not in ko_body:
            takeaway_html = '''
      <div class="takeaway-box">
        <h3>✅ 핵심 요약</h3>
        <ul>
          <li><strong>로컬 비즈니스:</strong> 바이두 스토어 멤버십이 중소기업에 프리미엄 스토어 가시성과 직접 전화 버튼을 제공합니다.</li>
          <li><strong>이커머스:</strong> 후이보싱 AI 디지털 휴먼 라이브로 거의 제로 마진 비용으로 24시간 판매가 가능합니다.</li>
          <li><strong>B2B:</strong> 아이차이거우 + B2B AI 에이전트 + 상장통이 안정적인 조달 리드를 보장합니다.</li>
          <li><strong>AI 기반:</strong> AI 광고 구축 + 판매자 AI 에이전트가 모든 광고주에게 평등한 기회를 제공합니다.</li>
        </ul>
      </div>'''
            # Insert before CTA or before </article>
            if 'class="cta-box"' in ko_body:
                ko_body = ko_body.replace('<div class="cta-box">', takeaway_html + '\n      <div class="cta-box">')
            else:
                ko_body = ko_body + takeaway_html
        
        # Update the article content
        html = html.replace(ko_article_match.group(0),
                            f'<article class="article-content">{ko_body}\n    </article>')
    
    # 17. Footer
    html = html.replace('Baidu PPC Pro. All rights reserved.', 'Baidu PPC Pro. 무단전재를 금지합니다.')
    html = html.replace(
        "We help international agencies and brands access China's $100B+ digital advertising market with compliance, clarity, and zero guesswork — one platform, end to end.",
        '해외 에이전시와 브랜드가 컴플라이언스를 준수하며 중국 디지털 광고 시장에 진출할 수 있도록 지원합니다.'
    )
    html = html.replace(
        "We help international agencies and brands access China's $100B+ digital advertising market with compliance, clarity, and zero guesswork.",
        '해외 에이전시와 브랜드가 컴플라이언스를 준수하며 중국 디지털 광고 시장에 진출할 수 있도록 지원합니다.'
    )
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
    # Fix footer links to /ko/
    html = html.replace('href="/privacy"', 'href="/ko/privacy"')
    html = html.replace('href="/terms"', 'href="/ko/terms"')
    
    # 18. Related section
    html = html.replace('>More from the Blog<', '>관련 기사<')
    html = re.sub(r'href="/" class="related-card"', 'href="/ko/" class="related-card"', html)
    html = re.sub(r'href="/blog/', 'href="/ko/blog/', html)
    
    # Translate related card content
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
    
    # 19. Add CTA section if not present in article body
    article_match = re.search(r'<article class="article-content">(.*?)</article>', html, re.DOTALL)
    if article_match and 'class="cta-box"' not in article_match.group(1):
        # Add CTA before </article>
        cta_html = '''
      <div class="cta-box">
        <h3>2026년 바이두의 새로운 기회를 탐색하세요</h3>
        <p>2026년 고객 획득 기회 진단 리포트를 무료로 받으시려면 지금 바로 문의하세요.</p>
        <a href="/ko/contact" class="cta-btn">상담 예약하기 →</a>
      </div>'''
        html = html.replace('</article>', f'{cta_html}\n    </article>')
    
    # 20. Fix "By Baidu PPC Pro Team" at end of article
    html = html.replace('>By Baidu PPC Pro Team<', '>Baidu PPC Pro 팀<')
    html = html.replace('<strong>By Baidu PPC Pro Team</strong>', '<strong>Baidu PPC Pro 팀</strong>')
    
    # Write
    with open(ko_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'✅ Generated: {ko_path}')
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python regen_ko_blog_v3.py <slug>')
        sys.exit(1)
    regen_page(sys.argv[1])
