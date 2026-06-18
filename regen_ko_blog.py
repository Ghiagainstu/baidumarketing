#!/usr/bin/env python3
"""
regen_ko_blog.py — 从 EN 博客 HTML 自动生成正确的 KO 版本
保留 EN 完整 HTML 结构（CSS/nav/footer/scripts），替换文本为韩语

用法：python regen_ko_blog.py <slug>
"""
import sys
import re
import os

PROJECT = os.path.dirname(os.path.abspath(__file__))

# 韩语导航映射
NAV_MAP = {
    'Why Baidu PPC Pro': '바이두 PPC Pro란',
    'Services': '서비스',
    'Pricing': '요금',
    'Clients': '도입 사례',
    'FAQ': '자주 묻는 질문',
    'About': '회사 소개',
    'Blog': '블로그',
    'Contact': '문의하기',
    'Get Started &rarr;': '지금 시작하기 →',
    'Get Started →': '지금 시작하기 →',
}

# Footer 映射
FOOTER_MAP = {
    'Quick Links': '바로가기',
    'About Us': '회사 소개',
    'Submit a Request': '문의 접수',
    'Legal': '법적 고지',
    'Privacy Policy': '개인정보 처리방침',
    'Terms of Service': '이용약관',
    'Contact': '문의하기',
    'All rights reserved.': '무단전재를 금지합니다.',
    'All rights reserved': '무단전재를 금지합니다',
    'Baidu PPC Pro. All rights reserved.': 'Baidu PPC Pro. 무단전재를 금지합니다.',
    'We help international agencies and brands access China\'s $100B+ digital advertising market with compliance, clarity, and zero guesswork — one platform, end to end.':
        '해외 에이전시와 브랜드가 컴플라이언스를 준수하며 중국 디지털 광고 시장에 진출할 수 있도록 지원합니다.',
}

def regen_page(slug):
    en_path = os.path.join(PROJECT, 'blog', f'{slug}.html')
    ko_path = os.path.join(PROJECT, 'ko', 'blog', f'{slug}.html')
    ko_content_path = ko_path  # existing KO content

    if not os.path.exists(en_path):
        print(f'❌ EN file not found: {en_path}')
        return False

    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()

    # Extract article content from existing KO file (if it exists)
    ko_article = ''
    if os.path.exists(ko_content_path):
        with open(ko_content_path, 'r', encoding='utf-8') as f:
            ko_html = f.read()
        # Extract content between <article class="article-content"> and </article>
        m = re.search(r'<article class="article-content">(.*?)</article>', ko_html, re.DOTALL)
        if m:
            ko_article = m.group(1).strip()

    # Start with EN HTML
    html = en_html

    # 1. lang="en" -> lang="ko"
    html = html.replace('<html lang="en">', '<html lang="ko">')

    # 2. Fix title
    # Extract slug from EN title and replace
    en_title_match = re.search(r'<title>(.*?)</title>', html)
    if en_title_match:
        en_title = en_title_match.group(1)
        # Will be replaced later with KO title from meta

    # 3. Fix canonical URL
    html = html.replace(f'href="https://www.baidumarketing.com/blog/{slug}"',
                        f'href="https://www.baidumarketing.com/ko/blog/{slug}"')

    # 4. Fix hreflang - add ko
    if 'hreflang="ko"' not in html:
        html = html.replace(
            f'<link rel="alternate" hreflang="x-default"',
            f'<link rel="alternate" hreflang="ko" href="https://www.baidumarketing.com/ko/blog/{slug}" />\n  <link rel="alternate" hreflang="x-default"'
        )

    # 5. Fix OG URL
    html = html.replace(f'content="https://www.baidumarketing.com/blog/{slug}"',
                        f'content="https://www.baidumarketing.com/ko/blog/{slug}"')

    # 6. Fix JSON-LD URL
    html = html.replace(f'"url":"https://www.baidumarketing.com/blog/{slug}"',
                        f'"url":"https://www.baidumarketing.com/ko/blog/{slug}"')
    html = html.replace(f'"@id":"https://www.baidumarketing.com/blog/{slug}"',
                        f'"@id":"https://www.baidumarketing.com/ko/blog/{slug}"')

    # 7. Fix nav links - / -> /ko/
    # Only replace in nav-links section, not in article content
    nav_pattern = r'(<div class="nav-links"[^>]*>)(.*?)(</div>)'
    def fix_nav_links(m):
        content = m.group(2)
        for en_text, ko_text in NAV_MAP.items():
            content = content.replace(f'>{en_text}<', f'>{ko_text}<')
        # Fix hrefs
        content = content.replace('href="/why-baidu-ppc-pro"', 'href="/ko/why-baidu-ppc-pro"')
        content = content.replace('href="/features"', 'href="/ko/features"')
        content = content.replace('href="/pricing"', 'href="/ko/pricing"')
        content = content.replace('href="/clients"', 'href="/ko/clients"')
        content = content.replace('href="/faq"', 'href="/ko/faq"')
        content = content.replace('href="/about"', 'href="/ko/about"')
        content = content.replace('href="/blog"', 'href="/ko/blog"')
        content = content.replace('href="/contact"', 'href="/ko/contact"')
        return m.group(1) + content + m.group(3)
    html = re.sub(nav_pattern, fix_nav_links, html, flags=re.DOTALL)

    # 8. Fix logo link
    html = html.replace('href="/" class="nav-logo"', 'href="/ko/" class="nav-logo"')

    # 9. Fix lang-switch button - add KO emoji
    html = html.replace('aria-label="Language">&#x1f1fa;&#x1f1f8;',
                        'aria-label="언어">🇰🇷')

    # 10. Fix lang-switch menu - add KO link
    lang_menu_pattern = r'(<div class="lang-switch-menu"[^>]*>)(.*?)(</div>)'
    def fix_lang_menu(m):
        content = m.group(2)
        # Add KO link if not present
        if 'lang="ko"' not in content:
            ko_link = f'\n            <a href="/ko/blog/{slug}" lang="ko" class="lang-switch-item">🇰🇷 한국어</a>\n          '
            content = content.rstrip() + ko_link
        # Fix emoji in existing links
        content = content.replace('&#x1f1fa;&#x1f1f8; English', '🇺🇸 English')
        content = content.replace('&#x1f1ef;&#x1f1f5; 日本語', '🇯🇵 日本語')
        return m.group(1) + content + m.group(3)
    html = re.sub(lang_menu_pattern, fix_lang_menu, html, flags=re.DOTALL)

    # 11. Fix nav-cta
    html = html.replace('>Get Started &rarr;</a>', '>지금 시작하기 →</a>')
    html = html.replace('href="/contact" class="nav-cta"', 'href="/ko/contact" class="nav-cta"')

    # 12. Fix breadcrumb
    html = html.replace('>Home</a>', '>홈</a>')
    html = html.replace('href="/">홈', 'href="/ko">홈')
    html = html.replace('href="/blog">Blog', 'href="/ko/blog">블로그')

    # 13. Fix article hero - meta
    html = html.replace('>By Baidu PPC Pro Team<', '>Baidu PPC Pro 팀<')

    # 14. Fix footer
    for en_text, ko_text in FOOTER_MAP.items():
        html = html.replace(f'>{en_text}<', f'>{ko_text}<')
        html = html.replace(f'> {en_text}<', f'> {ko_text}<')
    # Fix footer links
    html = html.replace('href="/features">서비스', 'href="/ko/features">서비스')
    html = html.replace('href="/pricing">요금', 'href="/ko/pricing">요금')
    html = html.replace('href="/about">회사 소개', 'href="/ko/about">회사 소개')
    html = html.replace('href="/faq">자주 묻는 질문', 'href="/ko/faq">자주 묻는 질문')
    html = html.replace('href="/blog">블로그', 'href="/ko/blog">블로그')
    html = html.replace('href="/contact">문의 접수', 'href="/ko/contact">문의 접수')
    html = html.replace('href="/privacy">개인정보 처리방침', 'href="/ko/privacy">개인정보 처리방침')
    html = html.replace('href="/terms">이용약관', 'href="/ko/terms">이용약관')

    # 15. Fix CTA section
    html = html.replace('href="/contact" class="cta-btn"', 'href="/ko/contact" class="cta-btn"')
    html = html.replace('href="/contact" class="cta-button"', 'href="/ko/contact" class="cta-button"')

    # 16. Fix related section links
    html = html.replace('href="/" class="related-card"', 'href="/ko/" class="related-card"')

    # 17. Replace article content if we have KO content
    if ko_article:
        article_pattern = r'(<article class="article-content">)(.*?)(</article>)'
        html = re.sub(article_pattern, r'\g<1>\n' + ko_article + '\n    \3', html, flags=re.DOTALL)

    # Write output
    with open(ko_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'✅ Generated: {ko_path}')
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python regen_ko_blog.py <slug>')
        sys.exit(1)
    regen_page(sys.argv[1])
