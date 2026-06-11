"""
generate_blog.py — 标准化博客 HTML 生成脚本
使用 _template-en.html / _template-ja.html + md_to_html.py

用法:
    python generate_blog.py <slug> --template blog/_template-en.html
    python generate_blog.py <slug> --both

示例:
    python generate_blog.py baidu-merchant-agent-human-handoff-setup --both
"""
import re
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md_to_html import md_to_html, post_process

VAULT = 'E:/Obsidian/Baidu'
PROJECT = os.path.dirname(os.path.abspath(__file__))

# Golden source pages for CSS validation — always use these to verify/fix templates
GOLDEN_SOURCES = {
    'en': f'{PROJECT}/blog/ai-marketing-whitepapers-2026-baidu-insights.html',
    'ja': f'{PROJECT}/ja/blog/baidu-merchant-agent-human-handoff-setup.html',
    'ko': f'{PROJECT}/blog/ai-marketing-whitepapers-2026-baidu-insights.html',
}

def extract_style_block(html):
    """Extract the <style>...</style> block from HTML."""
    m = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    return m.group(1) if m else ''

def validate_and_fix_style(template, lang):
    """Validate nav-links CSS in template. If broken, replace entire <style> block from golden source."""
    # Check critical CSS patterns
    issues = []
    if '.nav-links { display: flex' not in template:
        issues.append('nav-links missing display:flex')
    if '.nav-mobile-cta' not in template:
        issues.append('nav-mobile-cta CSS missing')
    if '.lang-switch-btn:hover svg' not in template and lang == 'ja':
        issues.append('lang-switch-btn hover missing')
    
    if not issues:
        return template, []
    
    # Fix: replace entire <style> block from golden source
    golden_path = GOLDEN_SOURCES.get(lang, GOLDEN_SOURCES['en'])
    if os.path.exists(golden_path):
        with open(golden_path, 'r', encoding='utf-8') as f:
            golden_html = f.read()
        golden_style = extract_style_block(golden_html)
        if golden_style:
            template = re.sub(r'<style>.*?</style>', f'<style>\n{golden_style}\n</style>', template, flags=re.DOTALL)
            return template, issues
    
    return template, issues

CATEGORY_MAP = {
    'insights': '01-Market-Insights',
    'platform': '02-Platform',
    'search': '03-Search-Ads',
    'feed': '04-Feed-Ads',
    'strategy': '05-Strategy',
    'landing': '06-Landing-Page',
    'pricing': '07-Pricing-Models',
}

def extract_fm(content):
    fm = {}
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            for line in content[3:end].strip().split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    fm[k.strip()] = v.strip().strip('"')
    return fm

def find_md_file(slug, lang):
    """Find the MD file for a given slug and language."""
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in ('charts', 'pages', 'templates', '.obsidian')]
        for f in files:
            if not f.endswith('.md'):
                continue
            full = os.path.join(root, f)
            with open(full, 'r', encoding='utf-8') as fh:
                content = fh.read(3000)
            fm = extract_fm(content)
            if fm.get('slug') == slug and fm.get('language') == lang:
                return full
    return None

def generate_html(slug, lang):
    """Generate blog HTML from template + MD."""
    # Find MD file
    md_path = find_md_file(slug, lang)
    if not md_path:
        print(f'  ✗ MD file not found for slug={slug} lang={lang}')
        return None
    
    # Read MD
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    fm = extract_fm(md_content)
    
    # Extract body (skip frontmatter + H1)
    body = md_content
    if body.startswith('---'):
        fm_end = body.find('---', 3)
        if fm_end > 0:
            body = body[fm_end + 3:].strip()
    if body.startswith('# '):
        nl = body.find('\n')
        body = body[nl + 1:].strip() if nl > 0 else ''
    
    # Convert MD to HTML
    body_html = post_process(md_to_html(body))
    
    # Read template
    template_path = f'{PROJECT}/blog/_template-en.html' if lang == 'en' else f'{PROJECT}/ja/blog/_template-ja.html' if lang == 'ja' else f'{PROJECT}/ko/blog/_template-ko.html'
    if not os.path.exists(template_path):
        print(f'  ✗ Template not found: {template_path}')
        return None
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Validate and fix template CSS
    template, css_issues = validate_and_fix_style(template, lang)
    if css_issues:
        print(f'  ⚠ Template CSS issues detected: {", ".join(css_issues)}')
        print(f'  → Auto-fixed from golden source: {GOLDEN_SOURCES.get(lang, GOLDEN_SOURCES["en"])}')
    
    # Fill template
    html = template
    html = html.replace('{{TITLE}}', fm.get('title', slug))
    html = html.replace('{{DATE}}', fm.get('date', ''))
    html = html.replace('{{READ_TIME}}', fm.get('reading_time', ''))
    html = html.replace('{{CATEGORY}}', fm.get('category', ''))
    html = html.replace('{{AUTHOR}}', fm.get('author', ''))
    html = html.replace('{{BODY}}', body_html)
    html = html.replace('{{CTA_TITLE}}', fm.get('cta_title', 'Ready to get started?'))
    html = html.replace('{{CTA_TEXT}}', fm.get('cta_text', 'Talk to the BPP team about your China marketing strategy.'))
    html = html.replace('{{CTA_LINK}}', '/contact' if lang == 'en' else f'/{lang}/contact')
    html = html.replace('{{CTA_BTN}}', 'Contact BPP →' if lang == 'en' else 'お問い合わせ →' if lang == 'ja' else '문의하기 →')
    
    # Update SEO meta
    title = fm.get('title', slug)
    desc = fm.get('description', title)
    
    html = re.sub(r'<title>.*?</title>', f'<title>{title} — Baidu PPC Pro Blog</title>', html)
    html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', html)
    html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', html)
    html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', html)
    html = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">', html)
    html = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{desc}">', html)
    
    # Update canonical and OG URLs
    base = 'baidumarketing.com'
    for old_slug_match in re.findall(r'baidumarketing\.com/(?:ja/|ko/)?blog/[^"]+', html):
        # Replace any existing slug with the correct one
        pass
    html = re.sub(r'baidumarketing\.com/blog/[^"]+', f'baidumarketing.com/blog/{slug}', html)
    html = re.sub(r'baidumarketing\.com/ja/blog/[^"]+', f'baidumarketing.com/ja/blog/{slug}', html)
    
    # Update hreflang
    html = re.sub(r'hreflang="en" href="https://www\.baidumarketing\.com/blog/[^"]*"', f'hreflang="en" href="https://www.baidumarketing.com/blog/{slug}"', html)
    html = re.sub(r'hreflang="ja" href="https://www\.baidumarketing\.com/ja/blog/[^"]*"', f'hreflang="ja" href="https://www.baidumarketing.com/ja/blog/{slug}"', html)
    html = re.sub(r'hreflang="x-default" href="https://www\.baidumarketing\.com/blog/[^"]*"', f'hreflang="x-default" href="https://www.baidumarketing.com/blog/{slug}"', html)
    
    # Update JSON-LD
    html = re.sub(r'"headline":"[^"]*"', f'"headline":"{title}"', html)
    html = re.sub(r'"datePublished":"[^"]*"', f'"datePublished":"{fm.get("date", "")}"', html)
    html = re.sub(r'"dateModified":"[^"]*"', f'"dateModified":"{fm.get("date", "")}"', html)
    
    # Update lang-switch links to use current slug
    html = re.sub(r'href="/blog/[^"]*" lang="en"', f'href="/blog/{slug}" lang="en"', html)
    html = re.sub(r'href="/ja/blog/[^"]*" lang="ja"', f'href="/ja/blog/{slug}" lang="ja"', html)
    
    return html

def main():
    parser = argparse.ArgumentParser(description='Generate blog HTML from template + MD')
    parser.add_argument('slug', help='Blog slug')
    parser.add_argument('--lang', default='en', choices=['en', 'ja', 'ko'], help='Language')
    parser.add_argument('--both', action='store_true', help='Generate both EN, JA and KO')
    args = parser.parse_args()
    
    langs = ['en', 'ja', 'ko'] if args.both else [args.lang]
    
    for lang in langs:
        html = generate_html(args.slug, lang)
        if html:
            out_dir = 'blog' if lang == 'en' else f'{lang}/blog'
            out_path = f'{out_dir}/{args.slug}.html'
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'  ✓ Created {out_path} ({len(html)} bytes)')

if __name__ == '__main__':
    main()
