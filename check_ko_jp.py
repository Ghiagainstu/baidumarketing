"""Check all KO Obsidian files for Japanese content leaks."""
import os, re

# Japanese character ranges (Hiragana, Katakana, common Japanese-only chars)
jp_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')

# Hiragana is a strong signal for Japanese
hiragana = re.compile(r'[\u3040-\u309F]{2,}')
# Katakana mid-word is also strong
katakana = re.compile(r'[\u30A0-\u30FF]{2,}')

root = 'E:/Obsidian/Baidu/'
results = []

for dirpath, dirnames, filenames in os.walk(root):
    for f in filenames:
        if not f.endswith('-ko.md') and not f.endswith('-ko-ko.md'):
            continue
        path = os.path.join(dirpath, f)
        try:
            text = open(path, encoding='utf-8').read()
        except:
            continue
        
        # Check for CTA box content with Japanese
        lines = text.split('\n')
        ja_lines = []
        for line in lines:
            # Skip frontmatter and headings
            if line.startswith('---') or line.startswith('#') or line.startswith('[') or line.startswith('>'):
                continue
            # Check for hiragana (strong Japanese indicator)
            if hiragana.search(line):
                ja_lines.append(line.strip()[:60])
            # Check for katakana sequences that aren't common loanwords
            elif katakana.search(line):
                ja_lines.append(line.strip()[:60])
        
        if ja_lines:
            results.append((path, len(ja_lines), ja_lines[:5]))

print(f"Found {len(results)} KO files with Japanese content:")
for path, count, samples in sorted(results):
    slug = os.path.basename(path)
    print(f"\n{'='*60}")
    print(f"📄 {slug} ({count} lines)")
    print(f"📁 {path.replace(root, '')}")
    for s in samples[:3]:
        # Truncate to 80 chars
        display = s[:80] + ('...' if len(s) > 80 else '')
        print(f"  → {display}")
