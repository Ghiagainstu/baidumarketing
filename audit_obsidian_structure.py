"""
Audit Obsidian Baidu blog structure against new rules:
1. Full articles: {slug}-{lang}.md with required frontmatter
2. Summary folder: {slug}/ with summary-{lang}.md
3. Required frontmatter: source_url, date, url_en/ja/ko, status, push_date, title, category, tags, slug, language, reading_time, author
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

VAULT = 'E:/Obsidian/Baidu'
SKIP_DIRS = {'charts', 'pages', 'templates', '.obsidian', 'OCR_Results', 'Baidu_B2B_WhitePaper_2024'}

REQUIRED_FM = ['title', 'date', 'category', 'tags', 'slug', 'language', 'author']
RECOMMENDED_FM = ['source_url', 'status', 'push_date', 'reading_time']
URL_FIELDS = ['url_en', 'url_ja', 'url_ko', 'url_jp']

AUTHOR_MAP = {
    'en': 'Baidu PPC Pro Team',
    'ja': 'Baidu PPC Pro チーム',
    'ko': 'Baidu PPC Pro 팀',
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

# Scan all subfolders to find summary directories
summary_dirs = {}  # folder_path -> {en: exists, ja: exists, ko: exists}
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for d in dirs:
        dirpath = os.path.join(root, d)
        contents = os.listdir(dirpath)
        summaries = [f for f in contents if f.startswith('summary-') and f.endswith('.md')]
        if summaries:
            langs = {}
            for s in summaries:
                lang = s.replace('summary-', '').replace('.md', '')
                langs[lang] = os.path.join(dirpath, s)
            summary_dirs[dirpath] = langs

# Scan all full article files
full_articles = []
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if not f.endswith('.md'):
            continue
        if f.startswith('summary-'):
            continue
        full = os.path.join(root, f)
        with open(full, 'r', encoding='utf-8') as fh:
            content = fh.read(5000)
        fm = extract_fm(content)
        if not fm:
            continue
        # Skip non-blog files
        if fm.get('type') == 'summary':
            continue
        if 'slug' not in fm and 'category' not in fm:
            continue
        full_articles.append((full, f, fm))

# === AUDIT ===
print("=" * 120)
print("OBSIDIAN BLOG STRUCTURE AUDIT")
print("=" * 120)

issues = []
ok_count = 0

for full, fname, fm in full_articles:
    rel = os.path.relpath(full, VAULT)
    lang = fm.get('language', 'en')
    slug = fm.get('slug', 'NONE')
    
    file_issues = []
    
    # Check required frontmatter
    for field in REQUIRED_FM:
        if field not in fm or not fm[field]:
            file_issues.append(f'MISSING required: {field}')
    
    # Check recommended frontmatter
    for field in RECOMMENDED_FM:
        if field not in fm or not fm[field]:
            file_issues.append(f'MISSING recommended: {field}')
    
    # Check at least one url field
    has_url = any(fm.get(u) for u in URL_FIELDS)
    if not has_url:
        file_issues.append(f'MISSING published url (none of url_en/ja/ko)')
    
    # Check author matches language
    expected_author = AUTHOR_MAP.get(lang, '')
    actual_author = fm.get('author', '')
    if expected_author and actual_author != expected_author:
        file_issues.append(f'WRONG author: "{actual_author}" (expected "{expected_author}")')
    
    # Check summary exists
    parent_dir = os.path.dirname(full)
    expected_summary_dir = os.path.join(parent_dir, slug)
    if expected_summary_dir in summary_dirs:
        summaries = summary_dirs[expected_summary_dir]
        if lang not in summaries:
            file_issues.append(f'MISSING summary-{lang}.md in {slug}/')
    else:
        file_issues.append(f'NO summary folder: {slug}/')
    
    if file_issues:
        issues.append((rel, lang, slug, file_issues))
    else:
        ok_count += 1

# Report
print(f"\nTotal articles scanned: {len(full_articles)}")
print(f"Fully compliant: {ok_count}")
print(f"With issues: {len(issues)}")

# Summary of issues
from collections import Counter
issue_types = Counter()
for _, _, _, file_issues in issues:
    for i in file_issues:
        # Extract issue type
        if i.startswith('MISSING required:'):
            issue_types['MISSING required: ' + i.split(': ')[1]] += 1
        elif i.startswith('MISSING recommended:'):
            issue_types['MISSING recommended: ' + i.split(': ')[1]] += 1
        elif i.startswith('MISSING published'):
            issue_types['MISSING published url'] += 1
        elif i.startswith('WRONG author'):
            issue_types['WRONG author'] += 1
        elif i.startswith('MISSING summary'):
            issue_types['MISSING summary file'] += 1
        elif i.startswith('NO summary folder'):
            issue_types['NO summary folder'] += 1

print(f"\n{'─' * 80}")
print("ISSUE SUMMARY (by frequency):")
print(f"{'─' * 80}")
for issue, count in issue_types.most_common():
    print(f"  {count:3d}x  {issue}")

# Detailed per-file report (first 50)
print(f"\n{'─' * 120}")
print("DETAILED ISSUES (first 60 files):")
print(f"{'─' * 120}")
for rel, lang, slug, file_issues in sorted(issues)[:60]:
    print(f"\n  {rel}  [lang={lang}, slug={slug}]")
    for issue in file_issues:
        print(f"    ✗ {issue}")

if len(issues) > 60:
    print(f"\n  ... and {len(issues) - 60} more files with issues")
