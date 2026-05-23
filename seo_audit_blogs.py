import os, glob, re

base = 'C:/Users/HYE/WorkBuddy/20260411211839'

issues = []

def audit_blog(filepath, lang):
    rel = os.path.relpath(filepath, base)
    try:
        content = open(filepath, encoding='utf-8').read()
    except Exception as e:
        issues.append((rel, 'FATAL', f'读取失败: {e}'))
        return

    fname = os.path.basename(filepath)
    slug = fname.replace('.html', '')

    # URL prefix
    if lang == 'EN':
        url_prefix = 'https://www.baidumarketing.com/blog/'
    elif lang == 'JA':
        url_prefix = 'https://www.baidumarketing.com/ja/blog/'
    else:
        url_prefix = 'https://www.baidumarketing.com/ko/blog/'

    # 1. Canonical
    canonicals = re.findall(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', content)
    if not canonicals:
        issues.append((rel, 'HIGH', '缺失 canonical 标签'))
    else:
        c = canonicals[0]
        if 'www.baidumarketing.com' not in c:
            issues.append((rel, 'HIGH', f'canonical 缺 www: {c}'))
        if '.html' in c:
            issues.append((rel, 'HIGH', f'canonical 含 .html: {c}'))
        expected = url_prefix + slug
        if c != expected:
            issues.append((rel, 'MED', f'canonical 不匹配: got={c}, expected={expected}'))

    # 2. Hreflang
    hreflangs = re.findall(r'hreflang=["\']([^"\']+)["\']', content)
    if not hreflangs:
        issues.append((rel, 'HIGH', '缺失 hreflang 标签'))
    else:
        # Check x-default
        xdefaults = [h for h in hreflangs if h == 'x-default']
        if not xdefaults:
            issues.append((rel, 'HIGH', '缺失 hreflang=x-default'))

    # 3. JSON-LD
    if 'application/ld+json' not in content:
        issues.append((rel, 'HIGH', '缺失 JSON-LD Schema'))

    # 4. Title tag
    titles = re.findall(r'<title>([^<]+)</title>', content)
    if not titles:
        issues.append((rel, 'HIGH', '缺失 <title> 标签'))
    else:
        t = titles[0]
        if len(t) < 30:
            issues.append((rel, 'LOW', f'Title 太短({len(t)}字符): {t[:50]}'))
        if len(t) > 70:
            issues.append((rel, 'LOW', f'Title 太长({len(t)}字符): {t[:50]}...'))
        if 'Baidu PPC Pro' not in t and 'Baidu PPC' not in t:
            issues.append((rel, 'LOW', f'Title 缺品牌名: {t[:50]}'))

    # 5. Meta description
    descs = re.findall(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content)
    if not descs:
        # Try content then name
        descs = re.findall(r'<meta\s+content=["\']([^"\']+)["\']\s+name=["\']description["\']', content)
    if not descs:
        issues.append((rel, 'HIGH', '缺失 meta description'))
    else:
        d = descs[0]
        if len(d) < 120:
            issues.append((rel, 'LOW', f'Meta desc 太短({len(d)}字符)'))
        if len(d) > 160:
            issues.append((rel, 'LOW', f'Meta desc 太长({len(d)}字符)'))

    # 6. OG tags
    og_tags = ['og:title', 'og:description', 'og:image', 'og:url', 'og:type']
    for tag in og_tags:
        if tag not in content:
            issues.append((rel, 'MED', f'缺失 {tag}'))

    # 7. Twitter Card
    tw_tags = ['twitter:card', 'twitter:title', 'twitter:description']
    for tag in tw_tags:
        if tag not in content:
            issues.append((rel, 'LOW', f'缺失 {tag}'))

    # 8. theme-color / color-scheme
    if 'theme-color' not in content:
        issues.append((rel, 'LOW', '缺失 theme-color'))
    if 'color-scheme' not in content:
        issues.append((rel, 'LOW', '缺失 color-scheme'))

    # 9. H1 tag
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if not h1s:
        issues.append((rel, 'MED', '缺失 <h1> 标签'))

    # 10. Broken internal links (relative .html links)
    broken_links = re.findall(r'href=["\']([^"\']*?)\.html["\']', content)
    for bl in broken_links:
        if bl.startswith('/') or bl.startswith('http'):
            continue  # skip external/absolute
        if bl.startswith('#'):
            continue
        # relative link without .html should be fine in cleanUrls
        # But check if there's href="/blog/xxx.html" style (should be href="/blog/xxx")

    # 11. Missing </script> tags
    script_opens = len(re.findall(r'<script[^>]*>', content))
    script_closes = len(re.findall(r'</script>', content))
    if script_opens != script_closes:
        issues.append((rel, 'HIGH', f'未闭合 <script>: 开={script_opens}, 闭={script_closes}'))

    # 12. GA4 tracking
    if 'G-TCGE7NJT7H' not in content:
        issues.append((rel, 'MED', '缺失 GA4 跟踪代码'))

    # 13. Duplicate canonical/hreflang
    if len(canonicals) > 1:
        issues.append((rel, 'MED', f'多个 canonical 标签({len(canonicals)}个)'))
    if len(descs) > 1:
        issues.append((rel, 'MED', f'多个 meta description({len(descs)}个)'))


# Audit all blogs
blog_dirs = [
    ('blog', 'EN'),
    ('ja/blog', 'JA'),
    ('ko/blog', 'KO'),
]

total_files = 0
for subdir, lang in blog_dirs:
    pattern = os.path.join(base, subdir, '*.html')
    files = glob.glob(pattern)
    for f in files:
        total_files += 1
        audit_blog(f, lang)

# Print results
print(f'=== SEO Audit: {total_files} blog files ===')
print()

# Group by severity
by_sev = {'FATAL': [], 'HIGH': [], 'MED': [], 'LOW': []}
for rel, sev, msg in issues:
    by_sev[sev].append((rel, msg))

for sev in ['FATAL', 'HIGH', 'MED', 'LOW']:
    items = by_sev[sev]
    if items:
        print(f'\n[{sev}] ({len(items)} issues)')
        # Group by file
        from collections import defaultdict
        by_file = defaultdict(list)
        for rel, msg in items:
            by_file[rel].append(msg)
        for f, msgs in sorted(by_file.items()):
            print(f'  {f}:')
            for m in msgs:
                print(f'    - {m}')

print(f'\n=== Summary ===')
print(f'Total files: {total_files}')
for sev in ['FATAL', 'HIGH', 'MED', 'LOW']:
    count = len(by_sev[sev])
    if count:
        print(f'  {sev}: {count}')
print(f'  Total issues: {len(issues)}')
