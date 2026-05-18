#!/usr/bin/env python3
"""
Enhance feed-landing-page-optimization.html to match benchmark standard
"""

import re

FILE = "c:/Users/HYE/WorkBuddy/20260411211839/blog/feed-landing-page-optimization.html"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Fix broken links
# ============================================================

# Fix breadcrumb
content = content.replace(
    '<a href="https://baidumarketing.com/.html">Home</a>',
    '<a href="../index">Home</a>'
)
content = content.replace(
    '<a href="https://baidumarketing.com/blog.html">Blog</a>',
    '<a href="../blog">Blog</a>'
)

# Fix CTA button link
content = content.replace(
    'href="https://baidumarketing.com/contact.html"',
    'href="../contact"'
)

# Fix related article links (convert absolute URLs to relative)
related_fixes = [
    ('https://baidumarketing.com/blog/landing-page-bounce-rate.html', '../landing-page-bounce-rate'),
    ('https://baidumarketing.com/blog/baidu-feed-account-structure.html', '../baidu-feed-account-structure'),
    ('https://baidumarketing.com/blog/baidu-feed-ads-explained.html', '../baidu-feed-ads-explained'),
]
for abs_url, rel_url in related_fixes:
    content = content.replace(f'href="{abs_url}"', f'href="{rel_url}"')

# ============================================================
# 2. Add emoji to H2 headings
# ============================================================
h2_emojis = {
    '>The Big Wins<': '>🚀 The Big Wins<',
    '>Form Optimization<': '>📋 Form Optimization<',
    '>Testing Priorities<': '>🧪 Testing Priorities<',
}
for old, new in h2_emojis.items():
    content = content.replace(old, new)

# ============================================================
# 3. Add emoji to H3 in win-cards
# ============================================================
h3_emojis = [
    ('>Load Speed Under 3 Seconds<', '>⚡ Load Speed Under 3 Seconds<'),
    ('>Match the Creative\'s Promise<', '>🎯 Match the Creative\'s Promise<'),
    ('>Single Clear Action<', '>1️⃣ Single Clear Action<'),
    ('>Trust Signals Front and Center<', '>🛡️ Trust Signals Front and Center<'),
]
for old, new in h3_emojis:
    content = content.replace(old, new)

# ============================================================
# 4. Add callout boxes
# ============================================================

# Insight callout after intro paragraph
intro_paragraph = '<p>A landing page bridges the gap between ad creative and your product or service. For Baidu feed campaigns, small tweaks regularly lift conversion rates by 15-30%.</p>'
insight_callout = '''<p>A landing page bridges the gap between ad creative and your product or service. For Baidu feed campaigns, small tweaks regularly lift conversion rates by 15-30%.</p>

        <div class="callout callout-insight">
          <span class="callout-icon">💡</span>
          <div><strong>Insight:</strong> Feed ad users are in "discovery mode" — they're browsing content, not actively searching. Your landing page needs to immediately answer "Why should I care?" in the first 3 seconds.</div>
        </div>

        <div class="callout callout-tip">
          <span class="callout-icon">✅</span>
          <div><strong>Pro Tip:</strong> Check your landing page load speed using <a href="https://pagespeed.web.dev/" target="_blank">PageSpeed Insights</a>. For China traffic, test from within China using tools like WebPageTest.org with a Shanghai/Shanghai node.</div>
        </div>
'''

if intro_paragraph in content:
    content = content.replace(intro_paragraph, insight_callout)
    print("Added callout boxes after intro")

# Warning callout before "Testing Priorities" section
testing_heading = '>🧪 Testing Priorities<'
warning_callout = '''        
        <div class="callout callout-warning">
          <span class="callout-icon">⚠️</span>
          <div><strong>Warning:</strong> Don't test too many elements at once. If you change headline, CTA color, AND form length simultaneously, you won't know which change drove the improvement. Test one variable at a time.</div>
        </div>

        <h2>🧪 Testing Priorities</h2>
'''
if testing_heading in content:
    content = content.replace(testing_heading, warning_callout)
    print("Added warning callout before Testing Priorities")

# ============================================================
# 5. Add takeaway box before CTA section
# ============================================================
cta_section = '<div class="cta-section">'
takeaway_box = '''        
        <div class="takeaway-box">
          <h3>📊 Key Takeaways</h3>
          <ul>
            <li>Speed matters most — optimize for <3s load time in China</li>
            <li>Match ad creative's promise on the landing page to maintain continuity</li>
            <li>Single clear CTA outperforms multiple options</li>
            <li>Trust signals (logos, certifications) are essential for feed traffic</li>
            <li>Test headline first — it has the biggest impact on conversions</li>
          </ul>
        </div>

        <div class="cta-section">
'''
if cta_section in content:
    content = content.replace(cta_section, takeaway_box)
    print("Added takeaway box before CTA section")

# ============================================================
# 6. Add callout CSS to <style> block
# ============================================================
callout_css = '''
    .callout { border-radius: 12px; padding: 20px 24px; margin: 24px 0; display: flex; gap: 14px; align-items: flex-start; }
    .callout-warning { background: #FEF3C7; border: 1px solid #FCD34D; }
    .callout-tip { background: #D1FAE5; border: 1px solid #6EE7B7; }
    .callout-insight { background: rgba(41,50,225,.06); border: 1px solid rgba(41,50,225,.18); }
    .callout-icon { font-size: 1.3rem; flex-shrink: 0; line-height: 1.6; }
    .takeaway-box { background: linear-gradient(135deg, #EEF0FF 0%, #F5F3FF 100%); border: 1px solid #C7D2FE; border-radius: 12px; padding: 24px; margin: 32px 0; }
    .takeaway-box h3 { font-size: 1rem; font-weight: 700; margin-bottom: 12px; color: var(--blue); display: flex; align-items: center; gap: 8px; }
    .takeaway-box ul { list-style: none; display: flex; flex-direction: column; gap: 8px; }
    .takeaway-box ul li { font-size: .9rem; line-height: 1.6; padding-left: 20px; position: relative; }
    .takeaway-box ul li::before { content: '✓'; position: absolute; left: 0; color: var(--blue); font-weight: 700; }
'''
# Insert before </style>
content = content.replace('  </style>', callout_css + '  </style>')
print("Added callout & takeaway CSS")

# ============================================================
# 7. Fix theme-toggle CSS (ensure dark mode icon switching works)
# ============================================================
# Check if theme-toggle has proper dark mode rules
if '[data-theme="dark"] .theme-toggle .icon-sun' not in content:
    # Add the missing rules before /* Nav mobile */
    old_nav_mobile = '    /* ── Nav extras ── */'
    new_css = '''    [data-theme="dark"] .theme-toggle .icon-sun { display: block; }
    [data-theme="dark"] .theme-toggle .icon-moon { display: none; }
    .theme-toggle .icon-sun { display: none; }
    .theme-toggle .icon-moon { display: block; }

    /* ── Nav extras ── */
'''
    content = content.replace(old_nav_mobile, new_css)
    print("Fixed theme-toggle dark mode CSS")

# ============================================================
# Write back
# ============================================================
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Enhancement complete!")
print("Changes made:")
print("  1. Fixed broken links (breadcrumb, CTA, related articles)")
print("  2. Added emoji to H2 and H3 headings")
print("  3. Added insight + tip callout boxes")
print("  4. Added warning callout")
print("  5. Added takeaway box")
print("  6. Added callout & takeaway CSS")
print("  7. Fixed theme-toggle dark mode CSS")
