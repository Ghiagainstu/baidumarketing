"""
Fill status and published URLs from live site data.
EN: https://www.baidumarketing.com/blog/{slug}
JA: https://www.baidumarketing.com/ja/blog/{slug}
KO: https://www.baidumarketing.com/ko/blog/{slug} (if exists)
"""
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')

VAULT = 'E:/Obsidian/Baidu'
SKIP_DIRS = {'charts', 'pages', 'templates', '.obsidian', 'OCR_Results', 'Baidu_B2B_WhitePaper_2024'}

# Published slugs from live site (fetched from blog listing pages)
EN_SLUGS = {
    'china-digital-marketing-trends-2026', 'baidu-merchant-agent-human-handoff',
    'baidu-industry-insights-tool-guide', 'baidu-marketing-product-updates-june-2026',
    'baidu-url-wildcard-guide', 'baidu-ad-display-name-update',
    'baidu-v-sign-verification-guide', 'baidu-invalid-click-protection',
    'baidu-q1-2026-ai-overtakes-search', 'baidu-brand-info-account-level',
    'baidu-keyword-zero-impression-diagnosis-tool', 'baidu-create-2026-agent-era',
    'faq-international-brands', 'baidu-2026-new-opportunities',
    'b2b-lead-generation-framework', 'baidu-2026-international-brands',
    'why-b2b-baidu-search', 'baidu-ernie-5-1-release',
    'baidu-ad-billing-models-explained', 'rising-cpm-bad-baidu',
    'cpm-ocpm-ecpm-explained', 'baidu-vs-google-ppc-differences',
    'chinese-consumers-decision-journey', 'china-internet-numbers-2025',
    'ai-assistants-vs-baidu', 'baidu-2025-earnings-geo',
    'digital-consumer-9trillion', 'search-vs-ai-usage',
    'baidu-inactive-keyword-cleanup-2025', 'baidu-search-ads-1-1-desktop-images',
    'baidu-ad-creation-workflow-simplified-creative-upgrade',
    'baidu-ads-campaign-upgrade-2025', 'baidu-creative-url-retirement-migration',
    'baidu-user-data-targeting', 'baidu-app-ecosystem',
    'baidu-ecosystem-numbers', 'baidu-feed-ads-explained',
    'baidu-ads-foreign-business', 'native-ads-vs-feed-ads',
    'baidu-pricing-models', 'ocpc-explained',
    'landing-page-bounce-rate', 'keyword-research-baidu',
    'digital-marketing-china', 'baidu-feed-account-structure',
    'feed-landing-page-optimization', 'baidu-custom-form-retirement',
    'baidu-conflicting-negative-keywords-feature', 'baidu-shared-budget-guide',
    'baidu-search-device-bid-coefficient-retirement',
    'baidu-ad-performance-diagnostic-tool', 'baidu-ocpc-skip-data-accumulation',
    'baidu-paid-search-video-ads', 'baidu-search-ad-video-format-guide',
    'baidu-conversion-tracking-dedup', 'baidu-brand-zone-material-pre-review',
    'baidu-landing-page-report', 'baidu-landing-page-audit-rejection-reasons',
    'baidu-click-fraud-ipv4-blocking',
    'baidu-feed-ads-history-operation-records-upgrade',
    'baidu-ppc-account-status-guide', '2020-baidu-b2b-industry-insights',
    'baidu-brand-zone-generic-keywords', 'baidu-ppc-different-domain',
    'baidu-mcc-account-guide', 'baidu-audience-targeting-guide',
    '8-ways-lower-baidu-cpc', 'baidu-keyword-match-types-guide',
    'baidu-brand-protection-guide', 'baidu-ppc-terms-explained',
    'how-much-does-baidu-ppc-cost',
}

# JA slugs (same set, all published articles have JA versions)
JA_SLUGS = EN_SLUGS.copy()

# KO slugs (only the 12 published KO articles)
KO_SLUGS = {
    '2020-baidu-b2b-industry-insights', 'baidu-2026-new-opportunities',
    'baidu-ad-performance-diagnostic-tool', 'baidu-ads-campaign-upgrade-2025',
    'baidu-brand-info-account-level', 'baidu-click-fraud-ipv4-blocking',
    'baidu-conversion-tracking-dedup', 'baidu-feed-ads-history-operation-records-upgrade',
    'baidu-landing-page-audit-rejection-reasons', 'baidu-landing-page-report',
    'baidu-ocpc-skip-data-accumulation', 'baidu-search-device-bid-coefficient-retirement',
}

def extract_fm(content):
    fm = {}
    if not content.startswith('---'):
        return fm, ''
    end = content.find('---', 3)
    if end < 0:
        return fm, ''
    fm_text = content[3:end]
    for line in fm_text.strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, fm_text

# Scan and update
updated = 0
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if not f.endswith('.md') or f.startswith('summary-'):
            continue
        
        full = os.path.join(root, f)
        rel = os.path.relpath(full, VAULT)
        
        with open(full, 'r', encoding='utf-8') as fh:
            content = fh.read()
        
        fm, fm_text = extract_fm(content)
        if not fm:
            continue
        
        slug = fm.get('slug', '')
        lang = fm.get('language', 'en')
        current_status = fm.get('status', '')
        
        # Determine if published
        is_published = False
        if lang == 'en' and slug in EN_SLUGS:
            is_published = True
        elif lang == 'ja' and slug in JA_SLUGS:
            is_published = True
        elif lang == 'ko' and slug in KO_SLUGS:
            is_published = True
        
        if not is_published:
            continue
        
        # Build URL
        base = 'https://www.baidumarketing.com'
        if lang == 'en':
            url_en = f'{base}/blog/{slug}'
            url_ja = f'{base}/ja/blog/{slug}'
            url_ko = f'{base}/ko/blog/{slug}' if slug in KO_SLUGS else ''
        elif lang == 'ja':
            url_en = f'{base}/blog/{slug}'
            url_ja = f'{base}/ja/blog/{slug}'
            url_ko = f'{base}/ko/blog/{slug}' if slug in KO_SLUGS else ''
        elif lang == 'ko':
            url_en = f'{base}/blog/{slug}'
            url_ja = f'{base}/ja/blog/{slug}'
            url_ko = f'{base}/ko/blog/{slug}'
        
        # Check if update needed
        needs_update = False
        if current_status != 'published':
            needs_update = True
        if not fm.get('url_en') and url_en:
            needs_update = True
        if not fm.get('url_ja') and url_ja:
            needs_update = True
        if not fm.get('url_ko') and url_ko:
            needs_update = True
        
        if not needs_update:
            continue
        
        # Update frontmatter
        end = content.find('---', 3)
        fm_lines = content[3:end].strip().split('\n')
        
        new_lines = []
        added_status = False
        added_url_en = False
        added_url_ja = False
        added_url_ko = False
        
        for line in fm_lines:
            if line.startswith('status:'):
                new_lines.append(f'status: published')
                added_status = True
            elif line.startswith('url_en:'):
                if url_en:
                    new_lines.append(f'url_en: {url_en}')
                else:
                    new_lines.append(line)
                added_url_en = True
            elif line.startswith('url_ja:'):
                if url_ja:
                    new_lines.append(f'url_ja: {url_ja}')
                else:
                    new_lines.append(line)
                added_url_ja = True
            elif line.startswith('url_ko:'):
                if url_ko:
                    new_lines.append(f'url_ko: {url_ko}')
                else:
                    new_lines.append(line)
                added_url_ko = True
            else:
                new_lines.append(line)
        
        # Add missing fields
        if not added_status:
            new_lines.append('status: published')
        if not added_url_en and url_en:
            new_lines.append(f'url_en: {url_en}')
        if not added_url_ja and url_ja:
            new_lines.append(f'url_ja: {url_ja}')
        if not added_url_ko and url_ko:
            new_lines.append(f'url_ko: {url_ko}')
        
        new_fm = '\n'.join(new_lines)
        body_start = content.find('---', 3) + 3
        new_content = f'---\n{new_fm}\n---\n{content[body_start:]}'
        
        with open(full, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        
        updated += 1
        print(f'  {rel}  status=published  url_en={url_en}')

print(f'\nTotal updated: {updated} files')
