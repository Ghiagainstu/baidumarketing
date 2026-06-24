"""Fix language switcher issues in all KO and JA blog files."""
import re, os, glob

# Fix KO blogs: /ko/blog/SLUG → /blog/{{SLUG}} (literal SLUG without curlies → proper paths)
print("=== Fixing KO blogs ===")
fixed = 0
for f in glob.glob('ko/blog/*.html'):
    if '_template' in f: continue
    c = open(f, encoding='utf-8').read()
    orig = c
    
    # Get the slug from the URL
    slug_match = re.search(r'/ko/blog/([^/"\']+)', c)
    if not slug_match: continue
    slug = slug_match.group(1)
    
    # Fix language switcher links
    # English link: /ko/blog/SLUG → /blog/{slug}
    c = re.sub(r'href="/ko/blog/SLUG"\s+lang="en"', f'href="/blog/{slug}" lang="en"', c)
    # Japanese link: /ja/blog/SLUG → /ja/blog/{slug}  
    c = re.sub(r'href="/ja/blog/SLUG"\s+lang="ja"', f'href="/ja/blog/{slug}" lang="ja"', c)
    # Korean link: /ko/blog/SLUG → /ko/blog/{slug}
    c = re.sub(r'href="/ko/blog/SLUG"\s+lang="ko"', f'href="/ko/blog/{slug}" lang="ko"', c)
    
    if c != orig:
        open(f, 'w', encoding='utf-8').write(c)
        fixed += 1
print(f'Fixed {fixed} KO blogs')

# Fix JA blogs: corrupted emoji entities in EN link
print("\n=== Fixing JA blogs ===")
fixed = 0
for f in glob.glob('ja/blog/*.html'):
    if '_template' in f: continue
    c = open(f, encoding='utf-8').read()
    orig = c
    
    # Fix corrupted emoji entities
    c = c.replace('&#x1f1fa;&#x1f1f8;#x1f1ef;&#x1f1fa;&#x1f1f8;#x1f1f5; English', '🇺🇸 English')
    c = c.replace('&#x1f1ef;&#x1f1f5; 日本語', '🇯🇵 日本語')
    
    # Fix hardcoded slugs - find and replace the old hardcoded slug with the actual slug
    # The template had baidu-merchant-agent-human-handoff-setup hardcoded
    # We need to detect the actual slug and use it
    slug_match = re.search(r'/ja/blog/([^/"\']+)', c)
    if slug_match:
        slug = slug_match.group(1)
        c = c.replace(f'/blog/baidu-merchant-agent-human-handoff-setup', f'/blog/{slug}')
        c = c.replace(f'/ja/blog/baidu-merchant-agent-human-handoff-setup', f'/ja/blog/{slug}')
        c = c.replace(f'/ko/blog/baidu-merchant-agent-human-handoff-setup', f'/ko/blog/{slug}')
    
    if c != orig:
        open(f, 'w', encoding='utf-8').write(c)
        fixed += 1
print(f'Fixed {fixed} JA blogs')

# Fix ALL files with corrupted CSS <em>, </em>::before
print("\n=== Fixing corrupted CSS <em>, </em>::before ===")
fixed = 0
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.workbuddy' in root: continue
    for f in files:
        if not f.endswith('.html'): continue
        path = os.path.join(root, f)
        c = open(path, encoding='utf-8').read()
        orig = c
        c = c.replace('<em>, </em>::before, <em>::after', '*, *::before, *::after')
        if c != orig:
            open(path, 'w', encoding='utf-8').write(c)
            fixed += 1
            if fixed <= 5:
                print(f'  FIXED: {path}')
print(f'Fixed {fixed} files total with corrupted CSS')

print('\nDone!')
