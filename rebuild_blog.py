#!/usr/bin/env python3
"""
rebuild_blog.py — 从 Obsidian MD + 模板生成完整博客 HTML
用法: python rebuild_blog.py <slug> [--lang en|ja|ko|all]

修复清单（2026-06-21）：
- frontmatter 引号自动 strip
- 模板 {{SLUG}} 占位符全局替换（含语言切换器、hreflang、canonical、OG、JSON-LD）
- JA/KO nav/footer 链接文本翻译
- JA/KO stats-grid / callout / takeaway-box 组件文本翻译
- JA/KO footer 版权文字翻译
- JA/KO footer 品牌描述翻译
- JA/KO footer 列标题翻译
"""
import sys
import os
import re
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md_to_html import md_to_html

# ── 翻译字典 ──────────────────────────────────────────────
NAV_TRANSLATIONS = {
    'ja': {
        'Services': 'サービス', 'Pricing': '料金', 'Clients': '導入事例',
        'About': '会社概要', 'About Us': '会社概要', 'Contact': 'お問い合わせ',
        'Submit a Request': 'お問い合わせ', 'Blog': 'ブログ',
        'Privacy Policy': 'プライバシーポリシー', 'Terms of Service': '利用規約',
    },
    'ko': {
        'Services': '서비스', 'Pricing': '요금', 'Clients': '도입 사례',
        'About': '회사 소개', 'About Us': '회사 소개', 'Contact': '문의하기',
        'Submit a Request': '문의하기', 'Blog': '블로그',
        'Privacy Policy': '개인정보 처리방침', 'Terms of Service': '이용약관',
    },
}

FOOTER_HEADERS = {
    'ja': {'Quick Links': 'クイックリンク', 'Contact': 'お問い合わせ', 'Legal': '法的情報'},
    'ko': {'Quick Links': '빠른 링크', 'Contact': '연락처', 'Legal': '법적 정보'},
}

FOOTER_BRAND_DESC = {
    'ja': '海外の代理店やブランドが、コンプライアンスと透明性を備えた中国の1000億ドル超のデジタル広告市場にアクセスできるよう支援します。',
    'ko': '해외 에이전시와 브랜드가 컴플라이언스와 투명성을 갖춘 중국 1000억 달러 규모의 디지털 광고 시장에 접근할 수 있도록 지원합니다.',
}

COPYRIGHT_TEXT = {
    'ja': '無断転載を禁じます',
    'ko': '무단전재를 금지합니다.',
}

STATS_TRANSLATIONS = {
    'ja': {
        '📊 Avg. CPC for Industrial Keywords': '📊 産業用キーワード平均CPC',
        '💰 Lower Cost vs Google Ads': '💰 Google広告比コスト削減',
        '👥 Baidu Monthly Users': '👥 百度月間ユーザー',
        '🏪 Aicgou Annual Membership': '🏪 愛採購年会費',
    },
    'ko': {
        '📊 Avg. CPC for Industrial Keywords': '📊 산업용 키워드 평균 CPC',
        '💰 Lower Cost vs Google Ads': '💰 구글 광고 대비 비용 절감',
        '👥 Baidu Monthly Users': '👥 바이두 월간 사용자',
        '🏪 Aicgou Annual Membership': '🏪 애채구 연간 회비',
    },
}

BREADCRUMB = {
    'en': '<a href="/">Home</a> / <a href="/blog">Blog</a>',
    'ja': '<a href="/ja/">ホーム</a> / <a href="/ja/blog">ブログ</a>',
    'ko': '<a href="/ko/">홈</a> / <a href="/ko/blog">블로그</a>',
}

DATE_DISPLAY = {
    'en': {'2026-06-21': 'Jun 21, 2026'},
    'ja': {'2026-06-21': '2026年6月21日'},
    'ko': {'2026-06-21': '2026년 6월 21일'},
}

READ_TIME_DISPLAY = {
    'en': {'9 min': '9 min', '11 min': '11 min', '10 min': '10 min'},
    'ja': {'9 min': '約11分', '11 min': '約11分', '10 min': '約10分'},
    'ko': {'9 min': '약10분', '11 min': '약11분', '10 min': '약10분'},
}

CTA_TEXT = {
    'en': {
        'title': 'Ready to explore what Baidu can do for your manufacturing business?',
        'text': "Talk to the BPP team. We'll walk you through the realistic options.",
        'btn': 'Contact BPP', 'link': '/contact',
    },
    'ja': {
        'title': '2026年に百度を製造業ビジネスに活用する準備はできていますか？',
        'text': 'BPPのチームが、業界、予算、目標に合わせた現実的な選択肢をご案内します。',
        'btn': 'BPPチームに問い合わせる', 'link': '/ja/contact',
    },
    'ko': {
        'title': '2026년 바이두를 제조업 비즈니스에 활용할 준비가 되셨나요?',
        'text': 'BPP 팀이 업종, 예산, 목표에 맞는 현실적인 옵션을 안내해 드립니다.',
        'btn': 'BPP 팀에 문의하기', 'link': '/ko/contact',
    },
}

RELATED_CARDS = {
    'en': '''<a href="/blog/why-b2b-baidu-search" class="related-card">
          <span>B2B</span><h4>Why Baidu Search Is the Most Underrated B2B Channel</h4>
          <p>Discover why Baidu search ads deliver higher-quality B2B leads than social media.</p>
        </a>
        <a href="/blog/b2b-lead-generation-framework" class="related-card">
          <span>B2B</span><h4>The 5-Step B2B Lead Generation Framework on Baidu</h4>
          <p>A practical guide for overseas companies to generate qualified B2B leads.</p>
        </a>
        <a href="/blog/how-much-does-baidu-ppc-cost" class="related-card">
          <span>Pricing</span><h4>How Much Does Baidu PPC Cost? Complete Pricing Guide</h4>
          <p>Understand Baidu advertising costs, from account setup to CPC benchmarks.</p>
        </a>''',
    'ja': '''<a href="/ja/blog/why-b2b-baidu-search" class="related-card">
          <span>B2B</span><h4>なぜ百度検索はB2Bに最も過小評価されているチャネルなのか</h4>
          <p>百度検索広告が中国でソーシャルメディアより高品質なB2Bリードを生む理由を解説。</p>
        </a>
        <a href="/ja/blog/b2b-lead-generation-framework" class="related-card">
          <span>B2B</span><h4>百度でB2Bリードを獲得する5ステップフレームワーク</h4>
          <p>海外企業が百度広告で適格なB2Bリードを獲得するための実践ガイド。</p>
        </a>
        <a href="/ja/blog/how-much-does-baidu-ppc-cost" class="related-card">
          <span>料金</span><h4>百度PPCの費用はいくら？完全価格ガイド</h4>
          <p>アカウント開設から日予算、CPCベンチマークまで、百度広告のコストを理解する。</p>
        </a>''',
    'ko': '''<a href="/ko/blog/why-b2b-baidu-search" class="related-card">
          <span>B2B</span><h4>왜 바이두 검색이 B2B에 가장 과소평가된 채널인가</h4>
          <p>바이두 검색 광고가 소셜 미디어보다 고품질 B2B 리드를 제공하는 이유.</p>
        </a>
        <a href="/ko/blog/b2b-lead-generation-framework" class="related-card">
          <span>B2B</span><h4>바이두에서 B2B 리드를 확보하는 5단계 프레임워크</h4>
          <p>해외 기업이 바이두 광고로 적격 B2B 리드를 확보하기 위한 실전 가이드.</p>
        </a>
        <a href="/ko/blog/how-much-does-baidu-ppc-cost" class="related-card">
          <span>요금</span><h4>바이두 PPC 비용은 얼마? 완벽 가격 가이드</h4>
          <p>계정 설정부터 CPC 벤치마크까지 바이두 광고 비용을 이해합니다.</p>
        </a>''',
}

RELATED_TITLE = {'en': 'Related Articles', 'ja': '関連記事', 'ko': '관련 기사'}


def strip_quotes(s):
    if s and len(s) >= 2:
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            return s[1:-1]
    return s


def parse_frontmatter(md_content):
    parts = md_content.split('---', 2)
    if len(parts) >= 3:
        fm, body = parts[1].strip(), parts[2].strip()
    else:
        fm, body = '', md_content
    meta = {}
    for line in fm.split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = strip_quotes(v.strip())
    # Remove H1 from body
    lines = body.split('\n')
    if lines and lines[0].startswith('# '):
        body = '\n'.join(lines[1:]).strip()
    return meta, body


def build_enhanced_content(body_md):
    """Convert MD to HTML and add visual components."""
    html = md_to_html(body_md)

    # Add emoji to H2
    emoji_map = {
        'Why Baidu for B2B Manufacturing': '🏭',
        'The Two Channels You Need to Know': '📢',
        'Account Setup: What You Actually Need': '📋',
        'Keyword Strategy for Industrial Manufacturers': '🎯',
        'Landing Pages That Convert Chinese Buyers': '🖥️',
        'Budget Planning: Real Numbers': '💰',
        'What BPP Does for B2B Manufacturers': '🤝',
    }
    for h, e in emoji_map.items():
        html = html.replace(f'<h2>{h}', f'<h2>{e} {h}')

    # Stats grid after first </ol>
    stats = '''
    <div class="stats-grid">
      <div class="stat-card"><div class="stat-number">¥1–5</div><div class="stat-label">📊 Avg. CPC for Industrial Keywords</div></div>
      <div class="stat-card"><div class="stat-number">60–80%</div><div class="stat-label">💰 Lower Cost vs Google Ads</div></div>
      <div class="stat-card"><div class="stat-number">500M+</div><div class="stat-label">👥 Baidu Monthly Users</div></div>
      <div class="stat-card"><div class="stat-number">¥6,980</div><div class="stat-label">🏪 Aicgou Annual Membership</div></div>
    </div>
'''
    pos = html.find('</ol>')
    if pos > 0:
        html = html[:pos+5] + stats + html[pos+5:]

    # Add callout elements based on article content
    # Check if this is a SaaS article (check for both English and translated text)
    is_saas = 'SaaS' in html and ('Landing Page Requirements' in html or 'ランディングページ要件' in html or '랜딩페이지 요건' in html)
    if is_saas:
        # Callout after landing page section - insert before "Budget Planning" heading
        callout_landing = '''
    <div class="callout callout-warning">
      <strong>⚠️ Common Pitfall:</strong> Using your English website as the landing page. Baidu will reject it during review, and even if it passes, conversion rates will be near zero. Chinese enterprise buyers expect localized content with trust signals.
    </div>
'''
        # Try English first, then Japanese, then Korean
        budget_heading_en = '    <h2>Budget Planning for SaaS on Baidu</h2>'
        budget_heading_ja = '    <h2>百度でのSaaS向け予算計画</h2>'
        budget_heading_ko = '    <h2>바이두에서의 SaaS용 예산 계획</h2>'
        
        if budget_heading_en in html:
            html = html.replace(budget_heading_en, callout_landing + '\n' + budget_heading_en)
        elif budget_heading_ja in html:
            html = html.replace(budget_heading_ja, callout_landing + '\n' + budget_heading_ja)
        elif budget_heading_ko in html:
            html = html.replace(budget_heading_ko, callout_landing + '\n' + budget_heading_ko)

        # Callout after budget section - insert before "What BPP Does" heading
        callout_budget = '''
    <div class="callout callout-insight">
      <strong>💡 Key Insight:</strong> SaaS companies should start with category keywords (60% of budget) to build awareness, then shift budget to comparison keywords (25%) as brand recognition grows. Branded keywords (15%) protect your brand terms from competitors.
    </div>
'''
        # Try English first, then Japanese, then Korean
        bpp_heading_en = '    <h2>What BPP Does for SaaS Companies</h2>'
        bpp_heading_ja = '    <h2>BPPがSaaS企業のためにできること</h2>'
        bpp_heading_ko = '    <h2>BPP가 SaaS 기업을 위해 할 수 있는 일</h2>'
        
        if bpp_heading_en in html:
            html = html.replace(bpp_heading_en, callout_budget + '\n' + bpp_heading_en)
        elif bpp_heading_ja in html:
            html = html.replace(bpp_heading_ja, callout_budget + '\n' + bpp_heading_ja)
        elif bpp_heading_ko in html:
            html = html.replace(bpp_heading_ko, callout_budget + '\n' + bpp_heading_ko)

        # Takeaway box before CTA
        takeaway = '''
    <div class="takeaway-box">
      <h3>📋 Key Takeaways for SaaS Companies</h3>
      <ul>
        <li>China SaaS market: $92.9B by 2033, 18.5% CAGR — massive opportunity</li>
        <li>Chinese enterprise buyers start research on Baidu, not Google</li>
        <li>SaaS CPCs are ¥8–25 ($1.10–$3.45) — competitive vs Western markets</li>
        <li>Landing page must be in Chinese with trust signals and free trial CTA</li>
        <li>Budget: ¥5,000–80,000/month depending on SaaS category</li>
        <li>BPP handles account setup, campaign management, and landing page guidance</li>
      </ul>
    </div>
'''
        # Try English first, then Japanese, then Korean
        cta_en = 'No hidden charges.</p>\n\n    <p><strong>Ready to explore'
        cta_ja = '追加料金はなし。</p>\n\n    <p><strong>2026年に百度をSaaSブランドに活かす準備はできていますか？'
        cta_ko = '추가 비용 없음.</p>\n\n    <p><strong>2026년 바이두를 SaaS 브랜드에 활용할 준비가 되셨나요?'
        
        if cta_en in html:
            html = html.replace(cta_en, 'No hidden charges.</p>\n' + takeaway + '\n    <p><strong>Ready to explore')
        elif cta_ja in html:
            html = html.replace(cta_ja, '追加料金はなし。</p>\n' + takeaway + '\n    <p><strong>2026年に百度をSaaSブランドに活かす準備はできていますか？')
        elif cta_ko in html:
            html = html.replace(cta_ko, '추가 비용 없음.</p>\n' + takeaway + '\n    <p><strong>2026년 바이두를 SaaS 브랜드에 활용할 준비가 되셨나요?')
    else:
        # Default callout for other articles (e.g., baidu-ads-b2b-manufacturers)
        callout1 = '''
    <div class="callout callout-warning">
      <strong>⚠️ Common Pitfall:</strong> The document translation and compliance review is where most foreign companies get stuck. Baidu's review process is strict — a single mismatched company name can delay approval by weeks.
    </div>
'''
        html = html.replace(
            'delay approval by weeks.</p>\n\n    <h2>🎯 Keyword',
            'delay approval by weeks.</p>\n' + callout1 + '\n    <h2>🎯 Keyword'
        )

        callout2 = '''
    <div class="callout callout-insight">
      <strong>💡 Key Insight:</strong> These numbers assume a well-optimized campaign with a Chinese-language landing page. Poor landing pages can 3–5× your cost per lead.
    </div>
'''
        html = html.replace(
            '3–5× your cost per lead.</p>\n\n    <h3>Budget Allocation',
            '3–5× your cost per lead.</p>\n' + callout2 + '\n    <h3>Budget Allocation'
        )

        takeaway = '''
    <div class="takeaway-box">
      <h3>📋 Key Takeaways</h3>
      <ul>
        <li>Baidu is where Chinese B2B buyers search — not Google</li>
        <li>Industrial CPCs are ¥1–5, 60–80% lower than Google Ads</li>
        <li>Two channels: Search Ads + Aicgou (Baidu B2B marketplace)</li>
        <li>Landing page must be in Chinese, fast-loading, mobile-ready</li>
        <li>Start with Tier 1 product keywords (80% of budget)</li>
        <li>Budget: ¥3,000–50,000/month depending on volume</li>
      </ul>
    </div>
'''
        html = html.replace(
            'No hidden charges.</p>\n\n    <p><strong>Ready to explore',
            'No hidden charges.</p>\n' + takeaway + '\n    <p><strong>Ready to explore'
        )

    return html


def translate_components(html, lang):
    """Translate visual component text for JA/KO."""
    if lang not in STATS_TRANSLATIONS:
        return html
    for en, translated in STATS_TRANSLATIONS[lang].items():
        html = html.replace(en, translated)

    # Translate takeaway-box title and callout titles
    if lang == 'ja':
        html = html.replace('📋 Key Takeaways', '📋 重要ポイントまとめ')
        html = html.replace('📋 Key Takeaways for SaaS Companies', '📋 SaaS企業向け重要ポイント')
        html = html.replace('⚠️ Common Pitfall', '⚠️ よくある落とし穴')
        html = html.replace('💡 Key Insight', '💡 重要な洞察')
        # Translate baidu-ads takeaway list items
        html = html.replace('Baidu is where Chinese B2B buyers search — not Google',
                           '中国のB2BバイヤーはGoogleではなく百度で検索する')
        html = html.replace('Industrial CPCs are ¥1–5, 60–80% lower than Google Ads',
                           '産業用CPCは¥1〜5で、Google広告より60〜80%低い')
        html = html.replace('Two channels: Search Ads + Aicgou (Baidu B2B marketplace)',
                           '2つのチャネル：検索広告＋愛採購（百度B2Bマーケットプレイス）')
        html = html.replace('Landing page must be in Chinese, fast-loading, mobile-ready',
                           'ランディングページは中国語、高速、モバイル対応が必須')
        html = html.replace('Start with Tier 1 product keywords (80% of budget)',
                           '層1製品キーワードから始める（予算の80%）')
        html = html.replace('Budget: ¥3,000–50,000/month depending on volume',
                           '月間予算：¥3,000〜50,000（ボリュームによる）')
        # Translate SaaS takeaway list items
        html = html.replace('China SaaS market: $92.9B by 2033, 18.5% CAGR — massive opportunity',
                           '中国SaaS市場：2033年までに929億ドル、CAGR 18.5% — 巨大な機会')
        html = html.replace('Chinese enterprise buyers start research on Baidu, not Google',
                           '中国のエンタープライズバイヤーはGoogleではなく百度から調査を始める')
        html = html.replace('SaaS CPCs are ¥8–25 ($1.10–$3.45) — competitive vs Western markets',
                           'SaaS CPCは¥8〜25（$1.10〜$3.45）— 西洋市場と比較して競争力あり')
        html = html.replace('Landing page must be in Chinese with trust signals and free trial CTA',
                           'ランディングページは中国語で、信頼シグナルと無料トライアルCTAが必要')
        html = html.replace('Budget: ¥5,000–80,000/month depending on SaaS category',
                           '月間予算：¥5,000〜80,000（SaaSカテゴリによる）')
        html = html.replace('BPP handles account setup, campaign management, and landing page guidance',
                           'BPPはアカウント設定、キャンペーン管理、ランディングページガイダンスを担当')
        # Translate SaaS callout content
        html = html.replace('Using your English website as the landing page. Baidu will reject it during review, and even if it passes, conversion rates will be near zero. Chinese enterprise buyers expect localized content with trust signals.',
                           '英語のウェブサイトをランディングページとして使用すること。百度は審査で却下し、通過してもコンバージョン率はほぼゼロになります。中国のエンタープライズバイヤーはローカライズされたコンテンツと信頼シグナルを期待しています。')
        html = html.replace('SaaS companies should start with category keywords (60% of budget) to build awareness, then shift budget to comparison keywords (25%) as brand recognition grows. Branded keywords (15%) protect your brand terms from competitors.',
                           'SaaS企業は認知構築のためにカテゴリキーワード（予算の60%）から始めるべきです。ブランド認知が成長したら比較キーワード（25%）に予算を移行します。ブランドキーワード（15%）はブランド用語を競合から保護します。')
    elif lang == 'ko':
        html = html.replace('📋 Key Takeaways', '📋 핵심 요약')
        html = html.replace('📋 Key Takeaways for SaaS Companies', '📋 SaaS 기업 핵심 요약')
        html = html.replace('⚠️ Common Pitfall', '⚠️ 흔한 함정')
        html = html.replace('💡 Key Insight', '💡 핵심 인사이트')
        html = html.replace('Baidu is where Chinese B2B buyers search — not Google',
                           '중국 B2B 바이어는 구글이 아닌 바이두에서 검색')
        html = html.replace('Industrial CPCs are ¥1–5, 60–80% lower than Google Ads',
                           '산업용 CPC는 ¥1~5로 구글 광고 대비 60~80% 저렴')
        html = html.replace('Two channels: Search Ads + Aicgou (Baidu B2B marketplace)',
                           '두 가지 채널: 검색 광고 + 애채구 (바이두 B2B 마켓플레이스)')
        html = html.replace('Landing page must be in Chinese, fast-loading, mobile-ready',
                           '랜딩페이지는 중국어, 고속, 모바일 대응 필수')
        html = html.replace('Start with Tier 1 product keywords (80% of budget)',
                           '계층 1 제품 키워드부터 시작 (예산의 80%)')
        html = html.replace('Budget: ¥3,000–50,000/month depending on volume',
                           '월 예산: ¥3,000~50,000 (볼륨에 따라)')
    return html


def rebuild(template_path, md_path, output_path, lang, slug):
    with open(template_path, 'r', encoding='utf-8') as f:
        tpl = f.read()
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    meta, body = parse_frontmatter(md)
    title = meta.get('title', slug)
    desc = meta.get('description', '')
    date = meta.get('date', '2026-06-21')
    rtime = meta.get('reading_time', '9 min')
    author = meta.get('author', 'Baidu PPC Pro Team')

    # Build enhanced HTML content
    content_html = build_enhanced_content(body)
    content_html = translate_components(content_html, lang)

    # ── Template replacements ──
    result = tpl

    # 1. {{SLUG}} 全局替换（语言切换器、hreflang、canonical、OG、JSON-LD）
    result = result.replace('{{SLUG}}', slug)

    # 2. Title
    result = re.sub(r'<title>.*?</title>', f'<title>{title} — Baidu PPC Pro Blog</title>', result)
    result = re.sub(r'<h1 class="article-title">.*?</h1>', f'<h1 class="article-title">{title}</h1>', result, flags=re.DOTALL)

    # 3. Meta
    result = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{desc}"', result)
    result = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{title}"', result)
    result = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{desc}"', result)
    result = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{title}"', result)
    result = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{desc}"', result)

    # 4. JSON-LD
    jl = f'{{"@context":"https://schema.org","@type":"BlogPosting","headline":"{title}","description":"{desc}","datePublished":"{date}","dateModified":"{date}","author":{{"@type":"Organization","name":"{author}"}},"publisher":{{"@type":"Organization","name":"Baidu PPC Pro"}},"mainEntityOfPage":{{"@type":"WebPage","@id":"https://www.baidumarketing.com/blog/{slug}"}}}}'
    result = re.sub(r'<script type="application/ld\+json">.*?</script>', f'<script type="application/ld+json">\n  {jl}\n  </script>', result, flags=re.DOTALL)

    # 5. Article meta (with SVG icons)
    dd = DATE_DISPLAY.get(lang, DATE_DISPLAY['en']).get(date, date)
    rt = READ_TIME_DISPLAY.get(lang, READ_TIME_DISPLAY['en']).get(rtime, rtime)
    meta_html = f'''<div class="article-meta">
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> {dd}</span>
        <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> {rt}</span>
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg> Strategy</span>
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> {author}</span>
      </div>'''
    ms = result.find('<div class="article-meta">')
    if ms > 0:
        me = result.find('</div>', ms) + 6
        result = result[:ms] + meta_html + result[me:]

    # 6. Breadcrumb
    bc = BREADCRUMB.get(lang, BREADCRUMB['en'])
    bs = result.find('<div class="breadcrumb">')
    if bs > 0:
        be = result.find('</div>', bs) + 6
        result = result[:bs] + f'<div class="breadcrumb">{bc}</div>' + result[be:]

    # 7. Article content
    cs = result.find('<article class="article-content">')
    if cs > 0:
        ce = result.find('</article>', cs) + 10
        result = result[:cs] + f'<article class="article-content">\n{content_html}\n      </article>' + result[ce:]

    # 8. CTA (includes </main> tag)
    cta = CTA_TEXT.get(lang, CTA_TEXT['en'])
    ctas = result.find('<div class="cta-box">')
    if ctas > 0:
        # Find the end of CTA section including </main>
        main_end = result.find('</main>', ctas)
        if main_end > 0:
            ctae = main_end + len('</main>')
        else:
            ctae = result.find('</div>\n    </div>', ctas)
            if ctae < 0:
                ctae = result.find('</div>', ctas + 100)
                ctae = result.find('</div>', ctae + 1) + 7
            else:
                ctae += len('</div>\n    </div>')
        result = result[:ctas] + f'''<div class="cta-box">
        <h3>{cta["title"]}</h3>
        <p>{cta["text"]}</p>
        <a href="{cta["link"]}" class="cta-btn">{cta["btn"]}</a>
      </div>
    </div>
  </main>''' + result[ctae:]

    # 9. Related section
    rt_title = RELATED_TITLE.get(lang, 'Related Articles')
    rc = RELATED_CARDS.get(lang, RELATED_CARDS['en'])
    rs = result.find('<section class="related-section">')
    if rs > 0:
        re_end = result.find('</section>', rs) + 10
        result = result[:rs] + f'''<section class="related-section">
    <div class="container">
      <h2>{rt_title}</h2>
      <div class="related-grid">{rc}
      </div>
    </div>
  </section>''' + result[re_end:]

    # 10. Lang attribute
    result = result.replace('<html lang="en">', f'<html lang="{lang}">')

    # 11. Nav/footer link text translation
    if lang in NAV_TRANSLATIONS:
        prefix = f'/{lang}'
        for en_text, tr_text in NAV_TRANSLATIONS[lang].items():
            # Only translate links pointing to this language prefix
            result = result.replace(f'>{en_text}</a>', f'>{tr_text}</a>')

    # 12. Footer headers
    if lang in FOOTER_HEADERS:
        for en_h, tr_h in FOOTER_HEADERS[lang].items():
            result = result.replace(f'<h4>{en_h}</h4>', f'<h4>{tr_h}</h4>')

    # 13. Footer brand description
    if lang in FOOTER_BRAND_DESC:
        old_desc = 'We help international agencies and brands access China'
        # Find and replace the paragraph containing the brand desc
        p_start = result.find(old_desc)
        if p_start > 0:
            p_tag_start = result.rfind('<p>', 0, p_start)
            p_tag_end = result.find('</p>', p_start) + 4
            result = result[:p_tag_start] + f'<p>{FOOTER_BRAND_DESC[lang]}</p>' + result[p_tag_end:]

    # 14. Copyright
    if lang in COPYRIGHT_TEXT:
        result = result.replace('All rights reserved.', COPYRIGHT_TEXT[lang])

    # 12. Nav links (add language prefix)
    if lang in ['ja', 'ko']:
        prefix = f'/{lang}'
        for path in ['/', '/why-baidu-ppc-pro', '/features', '/pricing', '/clients',
                     '/faq', '/about', '/blog', '/contact', '/privacy', '/terms']:
            # Only replace href attributes, not already-prefixed ones
            result = result.replace(f'href="{path}"', f'href="{prefix}{path}"')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f'OK {lang}: {output_path}')


def main():
    parser = argparse.ArgumentParser(description='Rebuild blog HTML from Obsidian MD')
    parser.add_argument('slug', help='Blog slug (e.g. baidu-ads-b2b-manufacturers)')
    parser.add_argument('--lang', default='all', help='Language: en, ja, ko, or all')
    args = parser.parse_args()

    base = os.path.dirname(os.path.abspath(__file__))
    template = os.path.join(base, 'blog', '_template-en.html')
    obsidian_base = 'E:/Obsidian/Baidu/05-Strategy'

    langs = ['en', 'ja', 'ko'] if args.lang == 'all' else [args.lang]

    for lang in langs:
        md_path = os.path.join(obsidian_base, args.slug, f'{args.slug}-{lang}.md')
        if lang == 'en':
            out_path = os.path.join(base, 'blog', f'{args.slug}.html')
        else:
            out_path = os.path.join(base, lang, 'blog', f'{args.slug}.html')

        if not os.path.exists(md_path):
            print(f'SKIP {lang}: {md_path} not found')
            continue

        rebuild(template, md_path, out_path, lang, args.slug)


if __name__ == '__main__':
    main()
