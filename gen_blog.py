"""
Generate blog HTML from Obsidian MD files.
Uses china-digital-marketing-trends-2026.html as template.
"""
import re

TEMPLATE_FILE = 'blog/china-digital-marketing-trends-2026.html'
EN_MD = 'E:/Obsidian/Baidu/01-Market-Insights/ai-marketing-whitepapers-2026-baidu-insights-en.md'
JA_MD = 'E:/Obsidian/Baidu/01-Market-Insights/ai-marketing-whitepapers-2026-baidu-insights-ja.md'
SLUG = 'ai-marketing-whitepapers-2026-baidu-insights'

def extract_fm(content):
    fm = {}
    body_start = 0
    if content.startswith('---'):
        fm_end = content.find('---', 3)
        if fm_end > 0:
            for line in content[3:fm_end].strip().split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    fm[k.strip()] = v.strip().strip('"')
            body_start = fm_end + 3
    return fm, content[body_start:].strip()

def md_body_to_html(body):
    """Convert MD body to article HTML sections."""
    lines = body.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        
        if line.startswith('# '):
            result.append('    <section class="article-hero">')
            result.append(f'      <h1 class="article-title">{line[2:]}</h1>')
            result.append('      <div class="article-meta">Jun 8, 2026 | 7 min read | Market Insights | Baidu PPC Pro Team</div>')
            result.append('    </section>')
            result.append('    <section class="article-section">')
            result.append('      <article class="article-content">')
            result.append(f'        <p>{line[2:]}</p>')
            i += 1
            continue
        
        if line.startswith('## '):
            result.append('      </article>')
            result.append('    </section>')
            result.append('    <section class="article-section">')
            result.append(f'      <h2>{line[3:]}</h2>')
            result.append('      <article class="article-content">')
            i += 1
            continue
        
        if line.startswith('### '):
            result.append(f'        <h3>{line[4:]}</h3>')
            i += 1
            continue
        
        # Multi-line HTML blocks
        if line.strip().startswith('<'):
            block_lines = []
            depth = 0
            while i < len(lines):
                l = lines[i]
                block_lines.append(l)
                if l.strip().startswith('<div') or l.strip().startswith('<table') or l.strip().startswith('<thead') or l.strip().startswith('<tbody') or l.strip().startswith('<tr') or l.strip().startswith('<th') or l.strip().startswith('<td') or l.strip().startswith('<blockquote'):
                    depth += 1
                if l.strip().startswith('</div>') or l.strip().startswith('</table>') or l.strip().startswith('</blockquote>'):
                    depth -= 1
                    if depth <= 0:
                        i += 1
                        break
                i += 1
            result.append('\n'.join(f'        {bl}' for bl in block_lines))
            continue
        
        # Lists
        if line.strip().startswith('- '):
            list_lines = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                item = lines[i].strip()[2:]
                item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                list_lines.append(f'          <li>{item}</li>')
                i += 1
            result.append('        <ul>')
            result.extend(list_lines)
            result.append('        </ul>')
            continue
        
        # Numbered lists
        if re.match(r'^\d+\. ', line.strip()):
            list_lines = []
            while i < len(lines) and re.match(r'^\d+\. ', lines[i].strip()):
                item = re.sub(r'^\d+\. ', '', lines[i].strip())
                item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                list_lines.append(f'          <li>{item}</li>')
                i += 1
            result.append('        <ol>')
            result.extend(list_lines)
            result.append('        </ol>')
            continue
        
        # Separator
        if line.strip() == '---':
            result.append('        <hr>')
            i += 1
            continue
        
        # Paragraph
        para_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#') and not lines[i].strip().startswith('<') and not lines[i].strip().startswith('- ') and not lines[i].strip().startswith('> ') and not re.match(r'^\d+\. ', lines[i].strip()) and not lines[i].strip() == '---' and not lines[i].strip().startswith('|'):
            para_lines.append(lines[i])
            i += 1
        
        if para_lines:
            text = ' '.join(l.strip() for l in para_lines)
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            result.append(f'        <p>{text}</p>')
            continue
        
        i += 1
    
    result.append('      </article>')
    result.append('    </section>')
    return '\n'.join(result)

# Read template
with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
    template = f.read()

# Process EN
with open(EN_MD, 'r', encoding='utf-8') as f:
    en_md = f.read()

en_fm, en_body = extract_fm(en_md)
en_body_html = md_body_to_html(en_body)

title_en = en_fm['title']
desc_en = en_fm.get('description', title_en)
date_str = '2026-06-08'

# Generate EN HTML
html_en = template
# SEO meta replacements
html_en = html_en.replace(
    '6 Digital Marketing Trends Reshaping China in 2026 — Baidu PPC Pro Blog',
    f'{title_en} — Baidu PPC Pro Blog'
)
html_en = html_en.replace(
    '<meta name="description" content="AI-driven marketing, private domain traffic, and automation are reshaping China\'s digital landscape in 2026. Here is what overseas advertisers need to know.">',
    f'<meta name="description" content="{desc_en}">'
)
html_en = html_en.replace(
    '<meta property="og:title" content="6 Digital Marketing Trends Reshaping China in 2026 — What They Mean for Overseas Advertisers">',
    f'<meta property="og:title" content="{title_en}">'
)
html_en = html_en.replace(
    '<meta property="og:description" content="AI-driven marketing, private domain traffic, and automation are reshaping China\'s digital landscape in 2026. Here is what overseas advertisers need to know.">',
    f'<meta property="og:description" content="{desc_en}">'
)
html_en = html_en.replace(
    '<meta name="twitter:title" content="6 Digital Marketing Trends Reshaping China in 2026 — What They Mean for Overseas Advertisers">',
    f'<meta name="twitter:title" content="{title_en}">'
)
html_en = html_en.replace(
    '<meta name="twitter:description" content="AI-driven marketing, private domain traffic, and automation are reshaping China\'s digital landscape in 2026. Here is what overseas advertisers need to know.">',
    f'<meta name="twitter:description" content="{desc_en}">'
)

# Canonical + OG URL + hreflang
for old_slug in ['china-digital-marketing-trends-2026', 'china-digital-marketing-trends-2026']:
    pattern = f'baidumarketing.com/blog/{old_slug}'
    replacement = f'baidumarketing.com/blog/{SLUG}'
    html_en = html_en.replace(pattern, replacement)
pattern = f'baidumarketing.com/ja/blog/china-digital-marketing-trends-2026'
replacement = f'baidumarketing.com/ja/blog/{SLUG}'
html_en = html_en.replace(pattern, replacement)

# JSON-LD
html_en = html_en.replace('"datePublished":"2026-06-04"', f'"datePublished":"{date_str}"')
html_en = html_en.replace('"dateModified":"2026-06-04"', f'"dateModified":"{date_str}"')
html_en = html_en.replace(
    '"headline":"6 Digital Marketing Trends Reshaping China in 2026',
    f'"headline":"{title_en}'
)

# Replace body
old_main_start = html_en.find('<main>')
old_main_end = html_en.find('</main>') + 7
html_en = html_en[:old_main_start] + '<main>\n' + en_body_html + '\n  </main>' + html_en[old_main_end:]

with open(f'blog/{SLUG}.html', 'w', encoding='utf-8') as f:
    f.write(html_en)
print(f'Created blog/{SLUG}.html ({len(html_en)} bytes)')

# Process JA
with open(JA_MD, 'r', encoding='utf-8') as f:
    ja_md = f.read()

ja_fm, ja_body = extract_fm(ja_md)

# Read JA template
with open('ja/blog/china-digital-marketing-trends-2026.html', 'r', encoding='utf-8') as f:
    ja_template = f.read()

ja_body_html = md_body_to_html(ja_body)
title_ja = ja_fm['title']
desc_ja = ja_fm.get('description', title_ja)

html_ja = ja_template
# Find and replace the title tag
import re as regex
html_ja = regex.sub(
    r'<title>.*? — Baidu PPC Pro Blog</title>',
    f'<title>{title_ja} — Baidu PPC Pro Blog</title>',
    html_ja
)
# Canonical + OG URL
for old_slug in ['china-digital-marketing-trends-2026']:
    html_ja = html_ja.replace(f'baidumarketing.com/blog/{old_slug}', f'baidumarketing.com/blog/{SLUG}')
    html_ja = html_ja.replace(f'baidumarketing.com/ja/blog/{old_slug}', f'baidumarketing.com/ja/blog/{SLUG}')

# Replace meta description
html_ja = regex.sub(
    r'<meta name="description" content="[^"]*">',
    f'<meta name="description" content="{desc_ja}">',
    html_ja
)
html_ja = regex.sub(
    r'<meta property="og:title" content="[^"]*">',
    f'<meta property="og:title" content="{title_ja}">',
    html_ja
)
html_ja = regex.sub(
    r'<meta property="og:description" content="[^"]*">',
    f'<meta property="og:description" content="{desc_ja}">',
    html_ja
)
html_ja = regex.sub(
    r'<meta name="twitter:title" content="[^"]*">',
    f'<meta name="twitter:title" content="{title_ja}">',
    html_ja
)
html_ja = regex.sub(
    r'<meta name="twitter:description" content="[^"]*">',
    f'<meta name="twitter:description" content="{desc_ja}">',
    html_ja
)

# JSON-LD date
html_ja = html_ja.replace('"datePublished":"2026-06-04"', f'"datePublished":"{date_str}"')
html_ja = html_ja.replace('"dateModified":"2026-06-04"', f'"dateModified":"{date_str}"')
html_ja = html_ja.replace(
    '"headline":"6 Digital Marketing Trends Reshaping China in 2026',
    f'"headline":"{title_ja}'
)

# Replace body
ja_main_start = html_ja.find('<main>')
ja_main_end = html_ja.find('</main>') + 7
html_ja = html_ja[:ja_main_start] + '<main>\n' + ja_body_html + '\n  </main>' + html_ja[ja_main_end:]

with open(f'ja/blog/{SLUG}.html', 'w', encoding='utf-8') as f:
    f.write(html_ja)
print(f'Created ja/blog/{SLUG}.html ({len(html_ja)} bytes)')
print('Done!')
