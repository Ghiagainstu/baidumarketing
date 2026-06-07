"""
Auto-fix Obsidian Baidu blog frontmatter:
- Add missing: title, language, slug, author, date, tags, category, reading_time
- Fix wrong author based on language
- Create summary folders and summary-{lang}.md files
"""
import os, re, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

VAULT = 'E:/Obsidian/Baidu'
SKIP_DIRS = {'charts', 'pages', 'templates', '.obsidian', 'OCR_Results', 'Baidu_B2B_WhitePaper_2024'}

AUTHOR_MAP = {
    'en': 'Baidu PPC Pro Team',
    'ja': 'Baidu PPC Pro チーム',
    'ko': 'Baidu PPC Pro 팀',
}

CATEGORY_MAP = {
    '01-Market-Insights': 'insights',
    '02-Platform': 'platform',
    '03-Search-Ads': 'search',
    '04-Feed-Ads': 'feed',
    '05-Strategy': 'strategy',
    '06-Landing-Page': 'landing',
    '07-Pricing-Models': 'pricing',
    '08-Baidu-Basics': 'strategy',
    '09-China-Search-Landscape': 'insights',
    '10-ByteDance-Douyin': 'insights',
    '11-Offline-Traditional': 'strategy',
    '12-Operations-Compliance': 'search',
    '13-Special-Topics': 'strategy',
}

def extract_fm(content):
    """Extract frontmatter dict and positions"""
    if not content.startswith('---'):
        return {}, 0, 0
    end = content.find('---', 3)
    if end < 0:
        return {}, 0, 0
    fm = {}
    for line in content[3:end].strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, 3, end

def extract_body(content):
    """Extract body after frontmatter"""
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            return content[end+3:].strip()
    return content.strip()

def count_words(text):
    return len(re.findall(r'\S+', text))

def count_chars_no_spaces(text):
    return len(re.sub(r'\s', '', text))

def calc_reading_time(text, lang):
    if lang in ('ja', 'ko'):
        chars = count_chars_no_spaces(text)
        return max(1, round(chars / 600))
    else:
        words = count_words(text)
        return max(1, round(words / 200))

def parse_filename_info(fname):
    """Extract slug and language from filename"""
    name = fname.replace('.md', '')
    
    # Detect language
    lang = 'en'
    if name.endswith('-ja'):
        lang = 'ja'
        name = name[:-3]
    elif name.endswith('-ko'):
        lang = 'ko'
        name = name[:-3]
    elif name.endswith('-en'):
        name = name[:-3]
    
    # Remove ✅ prefix
    slug = name
    for prefix in ['✅ bpp-', '✅ ']:
        if slug.startswith(prefix):
            slug = slug[len(prefix):]
            break
    
    # Clean slug
    slug = slug.strip()
    
    return slug, lang

def make_title_from_slug(slug):
    """Generate a title from slug"""
    # Replace hyphens with spaces, capitalize
    words = slug.replace('-', ' ').split()
    # Skip leading numbers
    clean = []
    for w in words:
        if re.match(r'^\d+$', w):
            continue
        clean.append(w)
    return ' '.join(w.capitalize() for w in clean)

def generate_summary(body, lang, max_chars=150):
    """Extract first paragraph(s) as summary, max chars"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', body)
    # Remove markdown headers
    text = re.sub(r'^#+\s+.*$', '', text, flags=re.MULTILINE)
    # Remove bold markers
    text = text.replace('**', '')
    # Get first meaningful paragraph
    paras = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 30]
    if paras:
        summary = paras[0][:max_chars]
        if len(paras[0]) > max_chars:
            summary += '...'
        return summary
    return text[:max_chars]

def build_fm_lines(fm):
    """Build ordered frontmatter lines"""
    # Preferred order
    order = ['title', 'date', 'source_url', 'source_name', 'source_date',
             'category', 'tags', 'slug', 'language', 'author',
             'status', 'push_date', 'url_en', 'url_ja', 'url_ko',
             'reading_time', 'description', 'type', 'parent']
    
    lines = []
    used = set()
    for key in order:
        if key in fm:
            val = fm[key]
            if isinstance(val, list):
                val = '[' + ', '.join(str(v) for v in val) + ']'
            lines.append(f'{key}: {val}')
            used.add(key)
    
    # Add any remaining keys not in order
    for key in fm:
        if key not in used:
            val = fm[key]
            if isinstance(val, list):
                val = '[' + ', '.join(str(v) for v in val) + ']'
            lines.append(f'{key}: {val}')
    
    return '\n'.join(lines)

# === MAIN ===
changes = []
summaries_created = []

for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    
    for fname in files:
        if not fname.endswith('.md'):
            continue
        if fname.startswith('summary-'):
            continue
        
        full = os.path.join(root, fname)
        rel = os.path.relpath(full, VAULT)
        folder = rel.split(os.sep)[0] if os.sep in rel else 'ROOT'
        
        with open(full, 'r', encoding='utf-8') as fh:
            content = fh.read()
        
        fm, fm_start, fm_end = extract_fm(content)
        body = extract_body(content)
        
        # Skip if no frontmatter at all and no category (non-blog file)
        if not fm and 'category' not in fm:
            # Check if it looks like a blog article by content
            if len(body) < 100:
                continue
        
        modified = False
        fixes = []
        
        # Parse filename for slug and language
        fname_slug, fname_lang = parse_filename_info(fname)
        
        # --- Fix language ---
        if 'language' not in fm or not fm['language'] or fm['language'] == 'en' and fname_lang != 'en':
            # If file has -ja/-ko suffix but language says 'en', fix it
            if fname_lang != 'en':
                fm['language'] = fname_lang
                modified = True
                fixes.append(f'language={fname_lang}')
        lang = fm.get('language', fname_lang)
        
        # --- Fix slug ---
        if 'slug' not in fm or not fm['slug'] or fm['slug'] == 'NONE':
            fm['slug'] = fname_slug
            modified = True
            fixes.append(f'slug={fname_slug}')
        
        # --- Fix title ---
        if 'title' not in fm or not fm['title']:
            # Try to get from first H1 in body
            h1_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
            if h1_match:
                fm['title'] = h1_match.group(1).strip()
            else:
                fm['title'] = make_title_from_slug(fm.get('slug', fname_slug))
            modified = True
            fixes.append('title added')
        
        # --- Fix author ---
        expected_author = AUTHOR_MAP.get(lang, 'Baidu PPC Pro Team')
        if 'author' not in fm or not fm['author']:
            fm['author'] = expected_author
            modified = True
            fixes.append(f'author={expected_author}')
        elif fm['author'] != expected_author:
            # Check if it's the wrong language variant
            if fm['author'] in AUTHOR_MAP.values() and fm['author'] != expected_author:
                fm['author'] = expected_author
                modified = True
                fixes.append(f'author fixed to {expected_author}')
        
        # --- Fix date ---
        if 'date' not in fm or not fm['date']:
            # Try to extract from filename
            date_match = re.search(r'(\w+ \d+, \d{4})', fname)
            if date_match:
                fm['date'] = date_match.group(1)
            else:
                fm['date'] = '2025-01-01'  # placeholder
            modified = True
            fixes.append(f'date={fm["date"]}')
        
        # --- Fix category ---
        if 'category' not in fm or not fm['category'] or fm['category'] == 'NONE':
            cat = CATEGORY_MAP.get(folder, 'insights')
            fm['category'] = cat
            modified = True
            fixes.append(f'category={cat}')
        
        # --- Fix tags ---
        if 'tags' not in fm or not fm['tags']:
            fm['tags'] = '[baidu-ppc, china-marketing]'
            modified = True
            fixes.append('tags added')
        
        # --- Fix reading_time ---
        if 'reading_time' not in fm or not fm['reading_time']:
            rt = calc_reading_time(body, lang)
            fm['reading_time'] = f'{rt} min'
            modified = True
            fixes.append(f'reading_time={rt}min')
        
        # --- Write changes ---
        if modified:
            new_fm = build_fm_lines(fm)
            new_content = f'---\n{new_fm}\n---\n{body}\n'
            
            with open(full, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            
            changes.append((rel, fixes))
        
        # --- Create summary folder and file ---
        slug = fm.get('slug', fname_slug)
        summary_dir = os.path.join(root, slug)
        summary_file = os.path.join(summary_dir, f'summary-{lang}.md')
        
        if not os.path.exists(summary_file):
            os.makedirs(summary_dir, exist_ok=True)
            
            summary_text = generate_summary(body, lang)
            summary_content = f"""---
title: "{fm.get('title', make_title_from_slug(slug))}"
date: {fm.get('date', '2025-01-01')}
slug: {slug}
language: {lang}
category: {fm.get('category', 'insights')}
type: summary
parent: "[[{slug}]]"
---

# {fm.get('title', make_title_from_slug(slug))}

{summary_text}

→ [[{slug}|{'전체 내용 읽기' if lang == 'ko' else '続きを読む' if lang == 'ja' else 'Read full article'}]]
"""
            with open(summary_file, 'w', encoding='utf-8') as fh:
                fh.write(summary_content)
            
            summaries_created.append(os.path.relpath(summary_file, VAULT))

# === REPORT ===
print("=" * 100)
print("AUTO-FIX REPORT")
print("=" * 100)
print(f"\nFrontmatter fixes: {len(changes)} files")
print(f"Summary files created: {len(summaries_created)}")

if changes:
    print(f"\n{'─' * 80}")
    print("FRONTMATTER FIXES:")
    print(f"{'─' * 80}")
    for rel, fixes in sorted(changes):
        print(f"  {rel}")
        for f in fixes:
            print(f"    + {f}")

if summaries_created:
    print(f"\n{'─' * 80}")
    print("SUMMARY FILES CREATED:")
    print(f"{'─' * 80}")
    for s in sorted(summaries_created):
        print(f"  {s}")

# Count by fix type
from collections import Counter
fix_counts = Counter()
for _, fixes in changes:
    for f in fixes:
        key = f.split('=')[0].strip()
        fix_counts[key] += 1

print(f"\n{'─' * 80}")
print("FIX TYPE SUMMARY:")
print(f"{'─' * 80}")
for fix, count in fix_counts.most_common():
    print(f"  {count:3d}x  {fix}")
