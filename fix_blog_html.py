"""
Fix blog HTML: properly replace content in <main> block.
Uses china-digital-marketing-trends-2026.html as template.
"""
import re

SLUG = 'ai-marketing-whitepapers-2026-baidu-insights'

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

def md_body_to_html_body(body):
    """Convert MD body to HTML content for article-content div."""
    lines = body.split('\n')
    result = []
    i = 0
    in_list = False
    
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        
        # H2
        if line.startswith('## '):
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(f'<h2>{line[3:]}</h2>')
            i += 1
            continue
        
        # H3
        if line.startswith('### '):
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(f'<h3>{line[4:]}</h3>')
            i += 1
            continue
        
        # HTML blocks - pass through
        if line.strip().startswith('<'):
            if in_list:
                result.append('</ul>')
                in_list = False
            block = [line]
            # Count depth for div/table
            depth = 0
            for tag in ['<div', '<table', '<thead', '<tbody', '<tr', '<blockquote']:
                if tag in line:
                    depth += 1
            if '</div>' in line or '</table>' in line or '</blockquote>' in line:
                depth -= 1
            
            while depth > 0 and i + 1 < len(lines):
                i += 1
                line = lines[i]
                block.append(line)
                for tag in ['<div', '<table', '<thead', '<tbody', '<tr', '<blockquote']:
                    if tag in line:
                        depth += 1
                if '</div>' in line or '</table>' in line or '</blockquote>' in line:
                    depth -= 1
            
            result.append('\n'.join(block))
            i += 1
            continue
        
        # List items
        if line.strip().startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            item = line.strip()[2:]
            item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
            result.append(f'<li>{item}</li>')
            i += 1
            continue
        
        # Separator
        if line.strip() == '---':
            if in_list:
                result.append('</ul>')
                in_list = False
            i += 1
            continue
        
        # Paragraph
        if in_list:
            result.append('</ul>')
            in_list = False
        
        para = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#') and not lines[i].strip().startswith('<') and not lines[i].strip().startswith('- ') and not lines[i].strip() == '---':
            para.append(lines[i])
            i += 1
        
        if para:
            text = ' '.join(p.strip() for p in para)
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            result.append(f'<p>{text}</p>')
            continue
        
        i += 1
    
    if in_list:
        result.append('</ul>')
    
    return '\n\n'.join(result)

# Read template
with open('blog/china-digital-marketing-trends-2026.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Read EN MD
with open(f'E:/Obsidian/Baidu/01-Market-Insights/{SLUG}-en.md', 'r', encoding='utf-8') as f:
    en_md = f.read()

en_fm = extract_fm(en_md)
# Get body after frontmatter
en_body = en_md[en_md.find('---', 3) + 3:].strip()
# Remove H1 (title is in article-hero)
if en_body.startswith('# '):
    en_body = en_body[en_body.find('\n') + 1:].strip()

en_html_body = md_body_to_html_body(en_body)

# Build EN HTML
title_en = en_fm['title']
desc_en = en_fm.get('description', title_en)
date_str = '2026-06-08'
read_time = '7 min'
category = 'Market Insights'
author = 'Baidu PPC Pro Team'

html_en = template
# Replace title tag
html_en = re.sub(
    r'<title>.*? — Baidu PPC Pro Blog</title>',
    f'<title>{title_en} — Baidu PPC Pro Blog</title>',
    html_en
)
# Replace description
html_en = re.sub(
    r'<meta name="description" content="[^"]*">',
    f'<meta name="description" content="{desc_en}">',
    html_en
)
# Replace OG title
html_en = re.sub(
    r'<meta property="og:title" content="[^"]*">',
    f'<meta property="og:title" content="{title_en}">',
    html_en
)
# Replace OG description
html_en = re.sub(
    r'<meta property="og:description" content="[^"]*">',
    f'<meta property="og:description" content="{desc_en}">',
    html_en
)
# Replace twitter title
html_en = re.sub(
    r'<meta name="twitter:title" content="[^"]*">',
    f'<meta name="twitter:title" content="{title_en}">',
    html_en
)
# Replace twitter description
html_en = re.sub(
    r'<meta name="twitter:description" content="[^"]*">',
    f'<meta name="twitter:description" content="{desc_en}">',
    html_en
)
# Replace slug in canonical/OG/hreflang
html_en = html_en.replace('china-digital-marketing-trends-2026', SLUG)

# Replace JSON-LD
html_en = html_en.replace('"datePublished":"2026-06-04"', f'"datePublished":"{date_str}"')
html_en = html_en.replace('"dateModified":"2026-06-04"', f'"dateModified":"{date_str}"')
html_en = re.sub(
    r'"headline":"[^"]*"',
    f'"headline":"{title_en}"',
    html_en
)

# Replace article-hero content (breadcrumb + title + meta)
hero_start = html_en.find('<section class="article-hero">')
hero_end = html_en.find('</section>', hero_start) + 10
new_hero = f'''  <section class="article-hero">
    <div class="container">
      <div class="breadcrumb"><a href="/">Home</a> / <a href="/blog">Blog</a></div>
      <h1 class="article-title">{title_en}</h1>
      <div class="article-meta">
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> Jun 8, 2026</span>
        <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> {read_time} read</span>
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg> {category}</span>
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> By {author}</span>
      </div>
    </div>
  </section>'''
html_en = html_en[:hero_start] + new_hero + html_en[hero_end:]

# Replace main content
main_start = html_en.find('<main>')
main_end = html_en.find('</main>') + 7
new_main = f'''  <main>
  <section class="article-section">
    <div class="container">
      <article class="article-content">

{en_html_body}

      </article>
    </div>
  </section>

  <div class="cta-box">
    <div class="container">
      <h3>Ready to navigate China's AI-powered marketing landscape?</h3>
      <p>Talk to the BPP team. We handle the full cycle — from AI tool activation to campaign management — so you can focus on your business.</p>
      <a href="/contact" class="btn-primary">Contact Us Today &rarr;</a>
    </div>
  </div>
  </main>'''
html_en = html_en[:main_start] + new_main + html_en[main_end:]

with open(f'blog/{SLUG}.html', 'w', encoding='utf-8') as f:
    f.write(html_en)
print(f'Fixed blog/{SLUG}.html ({len(html_en)} bytes)')

# Now do JA
with open(f'E:/Obsidian/Baidu/01-Market-Insights/{SLUG}-ja.md', 'r', encoding='utf-8') as f:
    ja_md = f.read()

ja_fm = extract_fm(ja_md)
ja_body = ja_md[ja_md.find('---', 3) + 3:].strip()
if ja_body.startswith('# '):
    ja_body = ja_body[ja_body.find('\n') + 1:].strip()

ja_html_body = md_body_to_html_body(ja_body)
title_ja = ja_fm['title']
desc_ja = ja_fm.get('description', title_ja)

# Read JA template
with open('ja/blog/china-digital-marketing-trends-2026.html', 'r', encoding='utf-8') as f:
    ja_template = f.read()

html_ja = ja_template
html_ja = re.sub(r'<title>.*? — Baidu PPC Pro Blog</title>', f'<title>{title_ja} — Baidu PPC Pro Blog</title>', html_ja)
html_ja = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc_ja}">', html_ja)
html_ja = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title_ja}">', html_ja)
html_ja = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc_ja}">', html_ja)
html_ja = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title_ja}">', html_ja)
html_ja = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{desc_ja}">', html_ja)
html_ja = html_ja.replace('china-digital-marketing-trends-2026', SLUG)
html_ja = html_ja.replace('"datePublished":"2026-06-04"', f'"datePublished":"{date_str}"')
html_ja = html_ja.replace('"dateModified":"2026-06-04"', f'"dateModified":"{date_str}"')
html_ja = re.sub(r'"headline":"[^"]*"', f'"headline":"{title_ja}"', html_ja)

# Fix JA footer
html_ja = html_ja.replace('Baidu PPC Pro. All rights reserved.', 'Baidu PPC Pro. 無断転載を禁じます。')

# Replace article-hero
ja_hero_start = html_ja.find('<section class="article-hero">')
ja_hero_end = html_ja.find('</section>', ja_hero_start) + 10
new_ja_hero = f'''  <section class="article-hero">
    <div class="container">
      <div class="breadcrumb"><a href="/ja">ホーム</a> / <a href="/ja/blog">ブログ</a></div>
      <h1 class="article-title">{title_ja}</h1>
      <div class="article-meta">
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> 2026年6月8日</span>
        <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> 約8分</span>
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg> マーケットインサイト</span>
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> Baidu PPC Pro チーム</span>
      </div>
    </div>
  </section>'''
html_ja = html_ja[:ja_hero_start] + new_ja_hero + html_ja[ja_hero_end:]

# Replace main content
ja_main_start = html_ja.find('<main>')
ja_main_end = html_ja.find('</main>') + 7
new_ja_main = f'''  <main>
  <section class="article-section">
    <div class="container">
      <article class="article-content">

{ja_html_body}

      </article>
    </div>
  </section>

  <div class="cta-box">
    <div class="container">
      <h3>中国のAIマーケティング環境を乗り越える準備はできていますか？</h3>
      <p>Baidu PPC Proチームにご相談ください。AIツールの有効化からキャンペーン管理まで、フルサイクルを処理します。</p>
      <a href="/ja/contact" class="btn-primary">お問い合わせ &rarr;</a>
    </div>
  </div>
  </main>'''
html_ja = html_ja[:ja_main_start] + new_ja_main + html_ja[ja_main_end:]

with open(f'ja/blog/{SLUG}.html', 'w', encoding='utf-8') as f:
    f.write(html_ja)
print(f'Fixed ja/blog/{SLUG}.html ({len(html_ja)} bytes)')
print('Done!')
