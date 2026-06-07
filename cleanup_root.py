"""
Analyze root bbp files and find their subfolder counterparts.
Recommend which to delete.
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

VAULT = 'E:/Obsidian/Baidu'

# Map root slugs to subfolder paths
# Root file naming: ✅ bpp-baidu-{slug}-{lang}.md
# Subfolder: ✅ bpp-XX-{slug}.md / ✅ bpp-XX-{slug}-{lang}.md

root_files = [f for f in os.listdir(VAULT) if f.startswith('✅ bpp-') and f.endswith('.md')]

# Parse root files
root_slugs = {}
for f in root_files:
    # Remove ✅ bpp- prefix, then parse
    name = f.replace('✅ bpp-', '')
    # Split into parts: baidu-{slug}-{lang}.md or {slug}-{lang}.md
    # Pattern: name-lang.md where lang is en/ja/ko
    if name.endswith('-en.md'):
        slug = name[:-6]  # remove -en.md
        lang = 'en'
    elif name.endswith('-ja.md'):
        slug = name[:-6]
        lang = 'ja'
    elif name.endswith('-ko.md'):
        slug = name[:-6]
        lang = 'ko'
    else:
        slug = name.replace('.md', '')
        lang = 'en'
    
    if slug not in root_slugs:
        root_slugs[slug] = {'en': None, 'ja': None, 'ko': None, 'size': {}}
    root_slugs[slug][lang] = f
    full = os.path.join(VAULT, f)
    root_slugs[slug]['size'][lang] = os.path.getsize(full)

# Find subfolder counterparts
print("=" * 100)
print("ROOT FILE CLEANUP ANALYSIS")
print("=" * 100)

for slug in sorted(root_slugs):
    info = root_slugs[slug]
    print(f"\n{'─' * 100}")
    print(f"Root slug: {slug}")
    
    # Check which subfolders have matching files
    found_in = []
    for folder in sorted(os.listdir(VAULT)):
        fpath = os.path.join(VAULT, folder)
        if not os.path.isdir(fpath):
            continue
        
        for f in os.listdir(fpath):
            if slug in f and f.endswith('.md'):
                found_in.append(f'{folder}/{f}')
    
    if found_in:
        print(f"  Found in subfolders ({len(found_in)} matches):")
        for match in found_in:
            sub_path = os.path.join(VAULT, match)
            sub_size = os.path.getsize(sub_path)
            print(f"    {match} ({sub_size:,} bytes)")
        
        # Compare root vs subfolder sizes
        for lang in ['en', 'ja', 'ko']:
            if info[lang]:
                root_size = info['size'].get(lang, 0)
                # Find matching subfolder file
                sub_lang = None
                for m in found_in:
                    if f'-{lang}.md' in m or m.endswith(f'-{lang}.md'):
                        sub_lang = m
                        break
                if sub_lang:
                    sub_size = os.path.getsize(os.path.join(VAULT, sub_lang))
                    ratio = root_size / max(sub_size, 1)
                    flag = '≈' if 0.8 < ratio < 1.2 else ('⚠ bigger' if ratio > 1.2 else '⚠ smaller')
                    print(f"    {lang}: root={root_size:,} / sub={sub_size:,}  ratio={ratio:.2f} [{flag}]")
    else:
        print(f"  ⚠ NO subfolder match found — DO NOT DELETE")

print("\n" + "=" * 100)
print("SUMMARY: ROOT FILES WITH SUBFOLDER MATCHES")
print("=" * 100)

safe_to_delete = []
no_match = []

for slug in sorted(root_slugs):
    info = root_slugs[slug]
    has_match = False
    for folder in sorted(os.listdir(VAULT)):
        fpath = os.path.join(VAULT, folder)
        if not os.path.isdir(fpath):
            continue
        for f in os.listdir(fpath):
            if slug in f and f.endswith('.md'):
                has_match = True
                break
        if has_match:
            break
    
    files_to_del = [info[l] for l in ['en', 'ja', 'ko'] if info[l]]
    
    if has_match:
        safe_to_delete.extend([os.path.join(VAULT, f) for f in files_to_del])
        print(f"  ✓ {slug} → {len(files_to_del)} files safe to delete")
    else:
        no_match.append(slug)
        print(f"  ⚠ {slug} → NO MATCH, DO NOT DELETE: {files_to_del}")

print(f"\nTotal safe to delete: {len(safe_to_delete)} files")
if no_match:
    print(f"⚠ No match found for: {no_match}")

# Print delete command
if safe_to_delete:
    print(f"\nTo delete {len(safe_to_delete)} root files:")
    for f in safe_to_delete:
        print(f'  rm "{f}"')
