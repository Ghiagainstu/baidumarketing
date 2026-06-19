#!/usr/bin/env python3
"""add_ko_lang_switch.py — Add KO link to EN/JA blog lang-switch-menu"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))

def add_ko_link(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Skip if already has KO link
    if 'lang="ko"' in html and 'lang-switch-item' in html.split('lang="ko"')[0].split('lang-switch-menu')[-1] if 'lang-switch-menu' in html else True:
        # More precise check: look for ko link inside lang-switch-menu
        menu_match = re.search(r'id="langSwitchMenu"[^>]*>(.*?)</div>', html, re.DOTALL)
        if menu_match and 'lang="ko"' in menu_match.group(1):
            return False
    
    # Extract slug from existing JA link
    ja_match = re.search(r'href="/ja/blog/([^"]+)" lang="ja"', html)
    if not ja_match:
        # Try EN blog pattern
        en_match = re.search(r'href="/blog/([^"]+)" lang="en"', html)
        if not en_match:
            return False
        slug = en_match.group(1)
    else:
        slug = ja_match.group(1)
    
    # Check if it's EN or JA page
    is_ja = '/ja/' in filepath
    
    # Find the JA lang-switch-item line and add KO after it
    ja_pattern = r'(<a href="/ja/blog/[^"]*" lang="ja" class="lang-switch-item">[^<]*</a>)'
    if re.search(ja_pattern, html):
        ko_link = f'<a href="/ko/blog/{slug}" lang="ko" class="lang-switch-item">🇰🇷 한국어</a>'
        html = re.sub(ja_pattern, r'\1\n            ' + ko_link, html)
    else:
        # Try EN-only pattern (no JA link yet)
        en_pattern = r'(<a href="/blog/[^"]*" lang="en" class="lang-switch-item">[^<]*</a>)'
        if re.search(en_pattern, html):
            ko_link = f'<a href="/ko/blog/{slug}" lang="ko" class="lang-switch-item">🇰🇷 한국어</a>'
            html = re.sub(en_pattern, r'\1\n            ' + ko_link, html)
        else:
            return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


def main():
    count = 0
    
    # EN blog pages
    for f in glob.glob(os.path.join(ROOT, 'blog', '*.html')):
        if '_template' in f:
            continue
        if add_ko_link(f):
            count += 1
            print(f'  ✅ {os.path.relpath(f, ROOT)}')
    
    # JA blog pages
    for f in glob.glob(os.path.join(ROOT, 'ja', 'blog', '*.html')):
        if '_template' in f:
            continue
        if add_ko_link(f):
            count += 1
            print(f'  ✅ {os.path.relpath(f, ROOT)}')
    
    print(f'\n✅ Total: {count} blog pages updated with KO link')


if __name__ == '__main__':
    main()
