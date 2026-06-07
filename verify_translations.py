"""
BPP Blog Translation Verification Script
Compares Obsidian MD → HTML coverage for EN/JA/KO
"""
import os, re, sys

# Force UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

VAULT = 'E:/Obsidian/Baidu'
PROJECT = 'c:/Users/HYE/WorkBuddy/20260411211839'

def extract_frontmatter(content):
    fm = {}
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            for line in content[3:end].strip().split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    fm[k.strip()] = v.strip().strip('"')
    return fm

def get_slug_from_filename(filename, fm):
    """Extract slug - prefer frontmatter, fallback to filename"""
    if 'slug' in fm:
        return fm['slug']
    # Remove -en/-ja/-ko suffix and .md
    name = re.sub(r'-(en|ja|ko)\.md$', '', filename)
    name = name.replace('.md', '')
    return name

# Collect all Obsidian articles (grouped by slug)
articles = {}  # slug -> {en_path, ja_path, ko_path, titles}

for folder in sorted(os.listdir(VAULT)):
    fpath = os.path.join(VAULT, folder)
    if not os.path.isdir(fpath):
        continue
    
    for f in os.listdir(fpath):
        if not f.endswith('.md'):
            continue
        full = os.path.join(fpath, f)
        try:
            with open(full, 'r', encoding='utf-8') as fh:
                content = fh.read(8000)
        except:
            continue
        
        fm = extract_frontmatter(content)
        slug = fm.get('slug', get_slug_from_filename(f, fm))
        lang = fm.get('language', 'en')
        title = fm.get('title', 'N/A')
        
        # Determine language from filename if not in frontmatter
        if lang == 'en' and ('-ja' in f or 'summary-ja' in f):
            lang = 'ja'
        elif lang == 'en' and ('-ko' in f or 'summary-ko' in f):
            lang = 'ko'
        
        if slug not in articles:
            articles[slug] = {}
        
        articles[slug][f'{lang}_path'] = f'{folder}/{f}'
        articles[slug][f'{lang}_title'] = title

# Check HTML existence
html_en_dir = os.path.join(PROJECT, 'blog')
html_ja_dir = os.path.join(PROJECT, 'ja', 'blog')
html_ko_dir = os.path.join(PROJECT, 'ko', 'blog')

for slug in articles:
    articles[slug]['html_en'] = os.path.exists(os.path.join(html_en_dir, f'{slug}.html'))
    articles[slug]['html_ja'] = os.path.exists(os.path.join(html_ja_dir, f'{slug}.html'))
    articles[slug]['html_ko'] = os.path.exists(os.path.join(html_ko_dir, f'{slug}.html'))

# Print report
print("=" * 120)
print("BPP BLOG TRANSLATION COVERAGE REPORT")
print("=" * 120)
print()

# Statistics
en_md_count = sum(1 for s in articles if 'en_path' in articles[s])
ja_md_count = sum(1 for s in articles if 'ja_path' in articles[s])
ko_md_count = sum(1 for s in articles if 'ko_path' in articles[s])
en_html_count = sum(1 for s in articles if articles[s].get('html_en'))
ja_html_count = sum(1 for s in articles if articles[s].get('html_ja'))
ko_html_count = sum(1 for s in articles if articles[s].get('html_ko'))

print(f"Total unique articles (by slug): {len(articles)}")
print(f"  EN MD files: {en_md_count}  |  EN HTML: {en_html_count}  |  Coverage: {en_html_count/max(en_md_count,1)*100:.0f}%")
print(f"  JA MD files: {ja_md_count}  |  JA HTML: {ja_html_count}  |  Coverage: {ja_html_count/max(ja_md_count,1)*100:.0f}%")
print(f"  KO MD files: {ko_md_count}  |  KO HTML: {ko_html_count}  |  Coverage: {ko_html_count/max(ko_md_count,1)*100:.0f}%")
print()

# MD missing translations
print("-" * 120)
print("MISSING MD TRANSLATIONS (need to create -ja.md / -ko.md in Obsidian)")
print("-" * 120)
missing_ja_md = []
missing_ko_md = []
for slug in sorted(articles):
    a = articles[slug]
    if 'en_path' in a and 'ja_path' not in a:
        missing_ja_md.append((slug, a['en_path']))
    if 'en_path' in a and 'ko_path' not in a:
        missing_ko_md.append((slug, a['en_path']))

if missing_ja_md:
    print(f"\nMissing JA MD ({len(missing_ja_md)} articles):")
    for slug, path in missing_ja_md:
        print(f"  [{path}]  ->  need {slug}-ja.md")
else:
    print("\nAll EN articles have JA MD translations ✓")

if missing_ko_md:
    print(f"\nMissing KO MD ({len(missing_ko_md)} articles):")
    for slug, path in missing_ko_md:
        print(f"  [{path}]  ->  need {slug}-ko.md")
else:
    print("\nAll EN articles have KO MD translations ✓")

# HTML missing
print()
print("-" * 120)
print("MISSING HTML FILES (MD exists but HTML not generated)")
print("-" * 120)

missing_en_html = [(slug, a.get('en_path','N/A')) for slug, a in articles.items() if 'en_path' in a and not a.get('html_en')]
missing_ja_html = [(slug, a.get('ja_path','N/A')) for slug, a in articles.items() if 'ja_path' in a and not a.get('html_ja')]
missing_ko_html = [(slug, a.get('ko_path','N/A')) for slug, a in articles.items() if 'ko_path' in a and not a.get('html_ko')]

if missing_en_html:
    print(f"\nMissing EN HTML ({len(missing_en_html)}):")
    for slug, path in missing_en_html:
        print(f"  {slug}  (MD: {path})")
else:
    print("\nAll EN MDs have HTML files ✓")

if missing_ja_html:
    print(f"\nMissing JA HTML ({len(missing_ja_html)}):")
    for slug, path in missing_ja_html:
        print(f"  {slug}  (MD: {path})")
else:
    print("\nAll JA MDs have HTML files ✓")

if missing_ko_html:
    print(f"\nMissing KO HTML ({len(missing_ko_html)}):")
    for slug, path in missing_ko_html:
        print(f"  {slug}  (MD: {path})")
else:
    print("\nAll KO MDs have HTML files ✓")

# Full table
print()
print("-" * 120)
print("FULL ARTICLE TABLE")
print("-" * 120)
print(f"{'Slug':50s} {'EN MD':8s} {'JA MD':8s} {'KO MD':8s} {'EN HTML':8s} {'JA HTML':8s} {'KO HTML':8s}")
print("-" * 120)

for slug in sorted(articles):
    a = articles[slug]
    en_md = 'Y' if 'en_path' in a else '-'
    ja_md = 'Y' if 'ja_path' in a else '-'
    ko_md = 'Y' if 'ko_path' in a else '-'
    en_html = 'Y' if a.get('html_en') else '-'
    ja_html = 'Y' if a.get('html_ja') else '-'
    ko_html = 'Y' if a.get('html_ko') else '-'
    
    # Highlight issues
    flags = []
    if en_md == 'Y' and en_html == '-': flags.append('!EN')
    if ja_md == 'Y' and ja_html == '-': flags.append('!JA')
    if ko_md == 'Y' and ko_html == '-': flags.append('!KO')
    flag_str = ' ' + ','.join(flags) if flags else ''
    
    print(f"{slug[:49]:50s} {en_md:8s} {ja_md:8s} {ko_md:8s} {en_html:8s} {ja_html:8s} {ko_html:8s}{flag_str}")

print()
print("Legend: Y = exists, - = missing, !XX = MD exists but HTML missing")
