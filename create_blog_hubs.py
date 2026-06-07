"""
Batch-create blog hub parent pages for all multi-language article groups.
Format: parent page with EN/JA/KO summaries + wiki-links to full articles.
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

VAULT = 'E:/Obsidian/Baidu'
SKIP_DIRS = {'charts', 'pages', 'templates', '.obsidian', 'OCR_Results', 'Baidu_B2B_WhitePaper_2024'}

LANG_LABELS = {
    'en': ('🇺🇸 English', 'Read full article'),
    'ja': ('🇯🇵 日本語', '続きを読む'),
    'ko': ('🇰🇷 한국어', '전문 읽기'),
}

def extract_fm(content):
    fm = {}
    if not content.startswith('---'):
        return fm
    end = content.find('---', 3)
    if end < 0:
        return fm
    for line in content[3:end].strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm

def extract_body(content):
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            return content[end+3:].strip()
    return content.strip()

def make_summary(body, max_chars=200):
    """Extract first meaningful paragraph as summary."""
    text = re.sub(r'<[^>]+>', '', body)
    text = re.sub(r'^#+\s+.*$', '', text, flags=re.MULTILINE)
    text = text.replace('**', '').strip()
    paras = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 30]
    if paras:
        summary = paras[0]
        if len(summary) > max_chars:
            summary = summary[:max_chars].rsplit(' ', 1)[0] + '...'
        return summary
    return text[:max_chars]

def get_wiki_link(filename):
    """Get the wiki-link name (filename without .md)."""
    return filename.replace('.md', '')

# === STEP 1: Group articles by slug ===
by_slug = {}

for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if not f.endswith('.md') or f.startswith('summary-'):
            continue
        full = os.path.join(root, f)
        rel = os.path.relpath(full, VAULT)
        
        with open(full, 'r', encoding='utf-8') as fh:
            content = fh.read()
        
        fm = extract_fm(content)
        if not fm or 'slug' not in fm:
            continue
        if fm.get('type') == 'blog-hub':
            continue
        
        slug = fm['slug']
        lang = fm.get('language', 'en')
        body = extract_body(content)
        
        if slug not in by_slug:
            by_slug[slug] = {}
        by_slug[slug][lang] = {
            'path': full,
            'filename': f,
            'title': fm.get('title', slug),
            'date': fm.get('date', ''),
            'category': fm.get('category', 'insights'),
            'tags': fm.get('tags', ''),
            'body': body,
        }

# === STEP 2: Create parent pages for multi-lang groups ===
created = 0
skipped = 0

for slug, langs in sorted(by_slug.items()):
    if len(langs) < 2:
        continue
    
    # Determine parent directory (same as the first article)
    first_article = list(langs.values())[0]
    parent_dir = os.path.dirname(first_article['path'])
    
    # Determine parent page filename
    # If articles have date prefix like "Jun 5, 2026 - slug-en.md", use "Jun 5, 2026 - slug.md"
    # If articles use "✅ bpp-XX-slug.md" format, use just "slug.md"
    first_filename = first_article['filename']
    
    # Check if filename has date prefix
    date_match = re.match(r'^(\w+ \d+, \d{4}) - ', first_filename)
    if date_match:
        parent_name = f"{date_match.group(1)} - {slug}.md"
    else:
        parent_name = f"{slug}.md"
    
    parent_path = os.path.join(parent_dir, parent_name)
    
    # Skip if already exists
    if os.path.exists(parent_path):
        skipped += 1
        continue
    
    # Get metadata from EN (or first available)
    en_info = langs.get('en', first_article)
    title = en_info['title']
    date = en_info['date']
    category = en_info['category']
    tags = en_info['tags']
    
    # Build language list
    available_langs = sorted(langs.keys())
    
    # Build summaries section
    summaries = []
    for lang in available_langs:
        info = langs[lang]
        label, link_text = LANG_LABELS.get(lang, (f'🌐 {lang.upper()}', 'Read full article'))
        summary = make_summary(info['body'])
        wiki_link = get_wiki_link(info['filename'])
        
        summaries.append(f"""## {label}

{summary}

→ [[{wiki_link}|{link_text}]]""")
    
    summaries_text = '\n\n---\n\n'.join(summaries)
    
    # Build frontmatter
    langs_str = ', '.join(available_langs)
    
    parent_content = f"""---
title: "{title}"
date: {date}
slug: {slug}
category: {category}
tags: {tags}
type: blog-hub
languages: [{langs_str}]
---

# {title}

> 汇总页 — 包含 {' / '.join(l.upper() for l in available_langs)} 语言摘要，链接到各语言完整文章

---

{summaries_text}
"""
    
    with open(parent_path, 'w', encoding='utf-8') as fh:
        fh.write(parent_content)
    
    created += 1
    print(f'  Created: {parent_name}  [{langs_str}]')

print(f'\nResults: {created} created, {skipped} skipped (already exist)')
