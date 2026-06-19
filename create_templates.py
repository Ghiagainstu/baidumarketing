"""
Create clean EN and JA blog templates from the best existing blog pages.
Templates contain only nav + CSS + empty main + footer structure.
"""
import re

def extract_section(html, start_tag, end_tag):
    """Extract content between start and end tags."""
    s = html.find(start_tag)
    if s == -1:
        return ''
    e = html.find(end_tag, s)
    if e == -1:
        return ''
    return html[s:e + len(end_tag)]

# Read best EN source
with open('blog/ai-marketing-whitepapers-2026-baidu-insights.html', 'r', encoding='utf-8') as f:
    en_html = f.read()

# Extract EN head (up to </head>)
head_end = en_html.find('</head>') + len('</head>')
en_head = en_html[:head_end]

# Extract EN nav
nav_start = en_html.find('<nav>')
nav_end = en_html.find('</nav>') + len('</nav>')
en_nav = en_html[nav_start:nav_end]

# Extract EN footer
footer_start = en_html.find('<footer>')
footer_end = en_html.find('</footer>') + len('</footer>')
en_footer = en_html[footer_start:footer_end]

# Extract EN related section template
related_start = en_html.find('<section class="related-section">')
related_end = en_html.find('</section>', related_start) + len('</section>')
en_related = en_html[related_start:related_end]

# Build clean EN template
en_template = f"""{en_head}
<body>
  {en_nav}
  <div class="nav-overlay" id="navOverlay" aria-hidden="true" onclick="toggleNav()"></div>

  <main>
  <section class="article-hero">
    <div class="container">
      <div class="breadcrumb"><a href="/">Home</a> / <a href="/blog">Blog</a></div>
      <h1 class="article-title">{{{{TITLE}}}}</h1>
      <div class="article-meta">
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> {{{{DATE}}}}</span>
        <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> {{{{READ_TIME}}}}</span>
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg> {{{{CATEGORY}}}}</span>
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> By {{{{AUTHOR}}}}</span>
      </div>
    </div>
  </section>

  <section class="article-section">
    <div class="container">
      <article class="article-content">

{{{{BODY}}}}

      </article>
    </div>
  </section>

  <div class="cta-box">
    <div class="container">
      <h3>{{{{CTA_TITLE}}}}</h3>
      <p>{{{{CTA_TEXT}}}}</p>
      <a href="{{{{CTA_LINK}}}}" class="btn-primary">{{{{CTA_BTN}}}}</a>
    </div>
  </div>
  </main>

  {en_related}

  {en_footer}
</body>
</html>"""

with open('blog/_template-en.html', 'w', encoding='utf-8') as f:
    f.write(en_template)
print(f'Created blog/_template-en.html ({len(en_template)} bytes)')

# Now create JA template
# Read best JA source
with open('ja/blog/baidu-merchant-agent-human-handoff-setup.html', 'r', encoding='utf-8') as f:
    ja_html = f.read()

# Extract JA head
ja_head_end = ja_html.find('</head>') + len('</head>')
ja_head = ja_html[:ja_head_end]

# Extract JA nav (from the fixed version)
ja_nav_start = ja_html.find('<nav>')
ja_nav_end = ja_html.find('</nav>') + len('</nav>')
ja_nav = ja_html[ja_nav_start:ja_nav_end]

# Extract JA footer
ja_footer_start = ja_html.find('<footer>')
ja_footer_end = ja_html.find('</footer>') + len('</footer>')
ja_footer = ja_html[ja_footer_start:ja_footer_end]

# Extract JA related section
ja_related_start = ja_html.find('<section class="related-section">')
ja_related_end = ja_html.find('</section>', ja_related_start) + len('</section>')
ja_related = ja_html[ja_related_start:ja_related_end]

# Build clean JA template
ja_template = f"""{ja_head}
<body>
  {ja_nav}
  <div class="nav-overlay" id="navOverlay" aria-hidden="true" onclick="toggleNav()"></div>

  <main>
  <section class="article-hero">
    <div class="container">
      <div class="breadcrumb"><a href="/ja">ホーム</a> / <a href="/ja/blog">ブログ</a></div>
      <h1 class="article-title">{{{{TITLE}}}}</h1>
      <div class="article-meta">
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> {{{{DATE}}}}</span>
        <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> {{{{READ_TIME}}}}</span>
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg> {{{{CATEGORY}}}}</span>
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> {{{{AUTHOR}}}}</span>
      </div>
    </div>
  </section>

  <section class="article-section">
    <div class="container">
      <article class="article-content">

{{{{BODY}}}}

      </article>
    </div>
  </section>

  <div class="cta-box">
    <div class="container">
      <h3>{{{{CTA_TITLE}}}}</h3>
      <p>{{{{CTA_TEXT}}}}</p>
      <a href="{{{{CTA_LINK}}}}" class="btn-primary">{{{{CTA_BTN}}}}</a>
    </div>
  </div>
  </main>

  {ja_related}

  {ja_footer}
</body>
</html>"""

with open('ja/blog/_template-ja.html', 'w', encoding='utf-8') as f:
    f.write(ja_template)
print(f'Created ja/blog/_template-ja.html ({len(ja_template)} bytes)')

# Verify templates
for path in ['blog/_template-en.html', 'ja/blog/_template-ja.html']:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    checks = {
        'btn-primary CSS': '.btn-primary' in content,
        'nav-right-group': 'nav-right-group' in content,
        'lang-switch': 'lang-switch-item' in content,
        'comparison-table CSS': 'comparison-table' in content,
        'callout CSS': '.callout' in content,
        'stats-grid CSS': 'stats-grid' in content,
        'cta-box CSS': '.cta-box' in content,
        'GA4': 'G-TCGE7NJT7H' in content,
        '{{BODY}}': '{{BODY}}' in content,
        '{{TITLE}}': '{{TITLE}}' in content,
    }
    print(f'\n{path}:')
    for check, ok in checks.items():
        print(f'  {"✓" if ok else "✗"} {check}')
