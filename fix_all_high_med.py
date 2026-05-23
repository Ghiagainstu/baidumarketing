import os, glob, re

base = 'C:/Users/HYE/WorkBuddy/20260411211839'

# ============================================================
# Helper functions
# ============================================================

def get_slug(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

def make_canonical(slug, lang):
    if lang == 'EN':
        return f'https://www.baidumarketing.com/blog/{slug}'
    elif lang == 'JA':
        return f'https://www.baidumarketing.com/ja/blog/{slug}'
    else:
        return f'https://www.baidumarketing.com/ko/blog/{slug}'

def make_hreflang_tags(slug, lang):
    """Generate hreflang tags. For EN files, link to EN+JA+x-default."""
    if lang == 'EN':
        return (
            f'  <link rel="alternate" hreflang="en" href="https://www.baidumarketing.com/blog/{slug}" />\n'
            f'  <link rel="alternate" hreflang="x-default" href="https://www.baidumarketing.com/blog/{slug}" />'
        )
    elif lang == 'JA':
        return (
            f'  <link rel="alternate" hreflang="ja" href="https://www.baidumarketing.com/ja/blog/{slug}" />\n'
            f'  <link rel="alternate" hreflang="x-default" href="https://www.baidumarketing.com/blog/{slug}" />'
        )
    else:
        return (
            f'  <link rel="alternate" hreflang="ko" href="https://www.baidumarketing.com/ko/blog/{slug}" />\n'
            f'  <link rel="alternate" hreflang="x-default" href="https://www.baidumarketing.com/blog/{slug}" />'
        )

def make_jsonld(slug, lang, title, description):
    url = make_canonical(slug, lang)
    return f'''<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "description": "{description}",
    "url": "{url}",
    "image": "https://www.baidumarketing.com/assets/og-brand-default.png",
    "datePublished": "2026-05-23",
    "dateModified": "2026-05-23",
    "author": {{
      "@type": "Organization",
      "name": "Baidu PPC Pro Team"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Baidu PPC Pro",
      "url": "https://www.baidumarketing.com"
    }}
  }}
</script>'''

def make_og_tags(slug, lang, title, description):
    url = make_canonical(slug, lang)
    return (
        f'  <meta property="og:title" content="{title}" />\n'
        f'  <meta property="og:description" content="{description}" />\n'
        f'  <meta property="og:image" content="https://www.baidumarketing.com/assets/og-brand-default.png" />\n'
        f'  <meta property="og:url" content="{url}" />\n'
        f'  <meta property="og:type" content="article" />'
    )

def make_twitter_tags(title, description):
    return (
        f'  <meta name="twitter:card" content="summary_large_image" />\n'
        f'  <meta name="twitter:title" content="{title}" />\n'
        f'  <meta name="twitter:description" content="{description}" />'
    )

GA4_TAG = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TCGE7NJT7H"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-TCGE7NJT7H');
</script>'''

# ============================================================
# Main fix logic
# ============================================================

def fix_blog(filepath, lang):
    rel = os.path.relpath(filepath, base)
    try:
        content = open(filepath, encoding='utf-8').read()
    except:
        return []

    slug = get_slug(filepath)
    canonical_url = make_canonical(slug, lang)
    fixes = []

    # Extract title from <title> tag
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1).strip() if title_match else slug.replace('-', ' ').title()

    # Extract meta description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content)
    if not desc_match:
        desc_match = re.search(r'<meta\s+content=["\']([^"\']+)["\']\s+name=["\']description["\']', content)
    description = desc_match.group(1).strip() if desc_match else f'Learn about {slug.replace("-", " ")} on Baidu PPC Pro.'

    # 1. Fix missing canonical
    if 'rel="canonical"' not in content and "rel='canonical'" not in content:
        canonical_tag = f'  <link rel="canonical" href="{canonical_url}" />'
        # Insert after <title> tag
        content = re.sub(
            r'(</title>\s*)',
            r'\1' + canonical_tag + '\n',
            content, count=1
        )
        fixes.append('添加 canonical')

    # 2. Fix missing hreflang
    if 'hreflang' not in content:
        hreflang_tags = make_hreflang_tags(slug, lang)
        # Insert after canonical tag
        content = re.sub(
            r'(</link>\s*(?:<link[^>]*rel=["\']icon|<link[^>]*href=["\']data:image))',
            hreflang_tags + '\n\\1',
            content, count=1
        )
        # If no icon link found, insert after canonical
        if 'hreflang' not in content:
            content = re.sub(
                r'(rel="canonical"[^>]*/>\s*)',
                '\\1' + hreflang_tags + '\n',
                content, count=1
            )
        fixes.append('添加 hreflang')

    # 3. Fix missing JSON-LD
    if 'application/ld+json' not in content:
        jsonld = make_jsonld(slug, lang, title, description)
        # Insert before </head>
        content = re.sub(
            r'(</head>)',
            jsonld + '\n\n\\1',
            content, count=1
        )
        fixes.append('添加 JSON-LD')

    # 4. Fix missing OG tags
    og_missing = any(tag not in content for tag in ['og:title', 'og:description', 'og:image', 'og:url', 'og:type'])
    if og_missing:
        og_tags = make_og_tags(slug, lang, title, description)
        # Insert after theme-color
        if 'theme-color' in content:
            content = re.sub(
                r'(<meta\s+name=["\']theme-color["\'][^>]*>\s*)',
                '\\1' + og_tags + '\n',
                content, count=1
            )
        else:
            # Insert before </head>
            content = re.sub(
                r'(</head>)',
                og_tags + '\n\n\\1',
                content, count=1
            )
        fixes.append('添加 OG 标签')

    # 5. Fix missing Twitter Card
    if 'twitter:card' not in content:
        tw_tags = make_twitter_tags(title, description)
        # Insert after OG tags or before </head>
        if 'og:type' in content:
            content = re.sub(
                r'(<meta\s+property=["\']og:type["\'][^>]*>\s*)',
                '\\1' + tw_tags + '\n',
                content, count=1
            )
        else:
            content = re.sub(
                r'(</head>)',
                tw_tags + '\n\n\\1',
                content, count=1
            )
        fixes.append('添加 Twitter Card')

    # 6. Fix missing GA4
    if 'G-TCGE7NJT7H' not in content:
        # Insert at start of <head>
        content = re.sub(
            r'(<head[^>]*>\s*)',
            '\\1' + GA4_TAG + '\n\n',
            content, count=1
        )
        fixes.append('添加 GA4')

    # Save if changes were made
    if fixes:
        open(filepath, 'w', encoding='utf-8').write(content)

    return fixes


# ============================================================
# Process all files
# ============================================================

blog_dirs = [
    ('blog', 'EN'),
    ('ja/blog', 'JA'),
    ('ko/blog', 'KO'),
]

total_fixed = 0
total_files = 0
fix_summary = {}

for subdir, lang in blog_dirs:
    pattern = os.path.join(base, subdir, '*.html')
    files = sorted(glob.glob(pattern))
    for f in files:
        total_files += 1
        fixes = fix_blog(f, lang)
        if fixes:
            total_fixed += 1
            rel = os.path.relpath(f, base)
            fix_summary[rel] = fixes
            for fix_type in fixes:
                fix_summary.setdefault('_counts', {})
                fix_summary['_counts'][fix_type] = fix_summary['_counts'].get(fix_type, 0) + 1

print(f'=== 修复完成 ===')
print(f'扫描文件: {total_files}')
print(f'修复文件: {total_fixed}')
print()

# Print fix counts
counts = fix_summary.pop('_counts', {})
print('修复类型统计:')
for fix_type, count in sorted(counts.items()):
    print(f'  {fix_type}: {count} 个文件')

print()
print('修复详情:')
for f, fixes in sorted(fix_summary.items()):
    print(f'  {f}: {", ".join(fixes)}')
