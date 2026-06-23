#!/usr/bin/env python3
"""Generate blog HTML from template + Obsidian MD for all 3 languages."""
import re
import sys
from pathlib import Path

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")
DRAFTS = PROJECT / "blog-drafts"

def read_frontmatter(md_path):
    """Extract frontmatter fields from MD."""
    text = md_path.read_text(encoding="utf-8-sig")
    fm_match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not fm_match:
        return {}, text
    fm_text = fm_match.group(1)
    body = text[fm_match.end():].strip()
    fields = {}
    for line in fm_text.split('\n'):
        m = re.match(r'^(\w+):\s*"?([^"]*)"?$', line)
        if m:
            fields[m.group(1)] = m.group(2)
    return fields, body

def md_to_html(md_text):
    """Convert markdown body to HTML."""
    lines = md_text.split('\n')
    html_parts = []
    first_h1_skipped = False
    in_list = False
    in_ol = False
    in_table = False
    table_rows = []
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            if in_ol:
                html_parts.append('</ol>')
                in_ol = False
            if in_table:
                html_parts.append(build_table(table_rows))
                table_rows = []
                in_table = False
            continue
        
        # Table detection
        if '|' in stripped and stripped.startswith('|'):
            in_table = True
            # Skip separator rows
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                continue
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            table_rows.append(cells)
            continue
        
        if in_table:
            html_parts.append(build_table(table_rows))
            table_rows = []
            in_table = False
        
        # Headings
        if stripped.startswith('### '):
            html_parts.append(f'<h3>{process_inline(stripped[4:])}</h3>')
            continue
        # H1 (skip first occurrence - already in page title)
        if stripped.startswith('# ') and not first_h1_skipped:
            first_h1_skipped = True
            continue
        if stripped.startswith('# '):
            html_parts.append(f'<h2>{process_inline(stripped[2:])}</h2>')
            continue
        if stripped.startswith('## '):
            html_parts.append(f'<h2>{process_inline(stripped[3:])}</h2>')
            continue
        
        # Unordered list
        if re.match(r'^[-*]\s+', stripped):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            item = re.sub(r'^[-*]\s+', '', stripped)
            html_parts.append(f'  <li>{process_inline(item)}</li>')
            continue
        
        # Ordered list
        if re.match(r'^\d+\.\s+', stripped):
            if not in_ol:
                html_parts.append('<ol>')
                in_ol = True
            item = re.sub(r'^\d+\.\s+', '', stripped)
            html_parts.append(f'  <li>{process_inline(item)}</li>')
            continue
        
        # Close lists if we hit non-list content
        if in_list:
            html_parts.append('</ul>')
            in_list = False
        if in_ol:
            html_parts.append('</ol>')
            in_ol = False
        
        # HTML passthrough (divs, blockquotes with classes)
        if stripped.startswith('<div') or stripped.startswith('<blockquote'):
            html_parts.append(stripped)
            continue
        if stripped.startswith('</div>') or stripped.startswith('</blockquote>'):
            html_parts.append(stripped)
            continue
        
        # Regular paragraph
        html_parts.append(f'<p>{process_inline(stripped)}</p>')
    
    # Close any open lists
    if in_list:
        html_parts.append('</ul>')
    if in_ol:
        html_parts.append('</ol>')
    if in_table:
        html_parts.append(build_table(table_rows))
    
    return '\n    '.join(html_parts)

def build_table(rows):
    """Build HTML table from rows."""
    if len(rows) < 2:
        return ''
    html = '<table class="comparison-table">\n'
    html += '  <thead><tr>'
    for cell in rows[0]:
        html += f'<th>{process_inline(cell)}</th>'
    html += '</tr></thead>\n'
    html += '  <tbody>'
    for row in rows[1:]:
        html += '<tr>'
        for cell in row:
            html += f'<td>{process_inline(cell)}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html


def process_inline(text):
    """Convert inline markdown to HTML."""
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Em dash
    text = text.replace(' — ', ' &mdash; ')
    return text

def generate_html(template_path, slug, lang, fm, body_html, cta):
    """Generate complete HTML from template."""
    template = template_path.read_text(encoding="utf-8")
    
    title = fm.get('title', '')
    description = fm.get('description', '')
    date = fm.get('date', '')
    reading_time = fm.get('reading_time', '')
    category = fm.get('category', 'strategy')
    author = fm.get('author', 'Baidu PPC Pro Team')
    
    # Build date string per language
    from datetime import datetime
    try:
        dt = datetime.strptime(date, '%Y-%m-%d')
        if lang == 'ja':
            date_str = f'{dt.year}年{dt.month}月{dt.day}日'
        elif lang == 'ko':
            date_str = f'{dt.year}년 {dt.month}월 {dt.day}일'
        else:
            date_str = dt.strftime('%b %d, %Y')
    except ValueError:
        date_str = date
    
    # Determine URL prefix
    if lang == 'en':
        url_prefix = '/blog/'
        canonical_prefix = 'https://www.baidumarketing.com/blog/'
    else:
        url_prefix = f'/{lang}/blog/'
        canonical_prefix = f'https://www.baidumarketing.com/{lang}/blog/'
    
    # Replace all placeholders
    html = template
    html = html.replace('{{SLUG}}', slug)
    html = html.replace('{{TITLE}}', title)
    html = html.replace('{{DATE}}', date_str)
    html = html.replace('{{READ_TIME}}', reading_time)
    html = html.replace('{{CATEGORY}}', category)
    html = html.replace('{{AUTHOR}}', author)
    html = html.replace('{{BODY}}', body_html)
    html = html.replace('{{CTA_TITLE}}', cta.get('title', ''))
    html = html.replace('{{CTA_TEXT}}', cta.get('text', ''))
    html = html.replace('{{CTA_LINK}}', cta.get('link', ''))
    html = html.replace('{{CTA_BTN}}', cta.get('btn', ''))
    
    # Fix meta tags - title
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title} &mdash; Baidu PPC Pro Blog</title>', html)
    
    # Fix meta description
    html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{description}">', html)
    
    # Fix OG tags
    html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', html)
    html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{description}">', html)
    html = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{canonical_prefix}{slug}">', html)
    
    # Fix Twitter tags
    html = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">', html)
    html = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{description}">', html)
    
    # Fix canonical
    html = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{canonical_prefix}{slug}">', html)
    
    # Fix hreflang
    html = re.sub(r'href="https://www\.baidumarketing\.com/blog/[^"]*"', f'href="https://www.baidumarketing.com/blog/{slug}"', html)
    html = re.sub(r'href="https://www\.baidumarketing\.com/ja/blog/[^"]*"', f'href="https://www.baidumarketing.com/ja/blog/{slug}"', html)
    html = re.sub(r'href="https://www\.baidumarketing\.com/ko/blog/[^"]*"', f'href="https://www.baidumarketing.com/ko/blog/{slug}"', html)
    
    # Fix JSON-LD
    html = re.sub(r'"headline":"[^"]*"', f'"headline":"{title}"', html)
    html = re.sub(r'"description":"[^"]*"', f'"description":"{description}"', html)
    html = re.sub(r'"datePublished":"[^"]*"', f'"datePublished":"{date}"', html)
    html = re.sub(r'"dateModified":"[^"]*"', f'"dateModified":"{date}"', html)
    html = re.sub(r'"@id":"https://www\.baidumarketing\.com/(?:ja/|ko/)?blog/[^"]*"', f'"@id":"{canonical_prefix}{slug}"', html)
    
    return html

# CTA templates
CTAS = {
    'en': {
        'title': 'Ready to explore what Baidu can do for your brand in 2026?',
        'text': 'Talk to the BPP team. We will walk you through the realistic options for your industry, your budget, and your goals \u2014 no pressure, no fluff.',
        'link': '/contact',
        'btn': 'Contact BPP'
    },
    'ja': {
        'title': '2026年に百度をブランドに活かす準備はできていますか？',
        'text': 'BPPのチームが、業界、予算、目標に合った現実的な選択肢をご案内します。高圧的ではなく、実直に。',
        'link': '/ja/contact',
        'btn': 'BPPに問い合わせる'
    },
    'ko': {
        'title': '2026년 바이두를 브랜드에 활용할 준비가 되셨나요?',
        'text': 'BPP 팀이 업종, 예산, 목표에 맞는 현실적인 옵션을 안내해 드립니다. 강요 없이, 솔직하게.',
        'link': '/ko/contact',
        'btn': 'BPP에 문의하기'
    }
}

def main():
    if len(sys.argv) < 2:
        print("Usage: python gen_blog_html.py <slug>")
        sys.exit(1)
    
    slug = sys.argv[1]
    draft_dir = DRAFTS / slug
    
    if not draft_dir.exists():
        print(f"❌ Draft directory not found: {draft_dir}")
        sys.exit(1)
    
    for lang in ['en', 'ja', 'ko']:
        md_path = draft_dir / f"{slug}-{lang}.md"
        template_path = PROJECT / f"{lang}/blog/_template-{lang}.html" if lang != 'en' else PROJECT / f"blog/_template-en.html"
        output_path = PROJECT / f"{lang}/blog/{slug}.html" if lang != 'en' else PROJECT / f"blog/{slug}.html"
        
        if not md_path.exists():
            print(f"❌ MD not found: {md_path}")
            continue
        
        if not template_path.exists():
            print(f"❌ Template not found: {template_path}")
            continue
        
        # Read frontmatter and body
        fm, body = read_frontmatter(md_path)
        
        # Convert body MD to HTML
        body_html = md_to_html(body)
        
        # Generate HTML
        html = generate_html(template_path, slug, lang, fm, body_html, CTAS[lang])
        
        # Write output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding='utf-8')
        print(f"✅ {lang.upper()}: {output_path}")

if __name__ == '__main__':
    main()
