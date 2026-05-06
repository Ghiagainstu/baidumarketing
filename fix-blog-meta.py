#!/usr/bin/env python3
"""Batch-fix 9 blog posts: add 'By Baidu PPC Pro Team' with person SVG to article-meta."""
import re, os

person_svg = '<span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> By Baidu PPC Pro Team</span>'

files = [
    "baidu-ppc-different-domain",
    "baidu-paid-search-video-ads",
    "baidu-shared-budget-guide",
    "baidu-brand-zone-generic-keywords",
    "baidu-audience-targeting-guide",
    "8-ways-lower-baidu-cpc",
    "baidu-ad-billing-models-explained",
    "baidu-vs-google-ppc-differences",
    "baidu-brand-protection-guide",
]

base = "c:/Users/HYE/WorkBuddy/20260411211839/blog"

for slug in files:
    path = os.path.join(base, f"{slug}.html")
    if not os.path.exists(path):
        print(f"NOT FOUND: {slug}")
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: find the article-meta div that already has some content
    # Replace the closing tag with our extra span + closing tag
    # Match the existing article-meta HTML pattern
    pattern = r'(<div class="article-meta">.*?</span>\s*</div>)'

    def add_team_span(match):
        block = match.group(1)
        # Skip if "By Baidu PPC Pro Team" already exists
        if 'By Baidu PPC Pro Team' in block:
            return block
        # Insert before the closing </div>
        new_block = block.replace('</div>', f'\n    {person_svg}\n      </div>')
        return new_block

    new_content = re.sub(pattern, add_team_span, content, count=1, flags=re.DOTALL)

    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"FIXED: {slug}")
    else:
        print(f"NO CHANGE: {slug}")
