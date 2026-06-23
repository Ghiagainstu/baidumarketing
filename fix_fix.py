from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\fix_article.py')
content = p.read_text(encoding='utf-8')

# Fix 1: use utf-8-sig to strip BOM
content = content.replace(
    'md_text = md_path.read_text(encoding="utf-8")',
    'md_text = md_path.read_text(encoding="utf-8-sig")'
)

# Fix 2: fix the frontmatter regex to handle titles with colons
content = content.replace(
    "m = re.match(r'^(\\w+):\\s*\"?([^\"]*)\"?$', line)",
    "m = re.match(r'^(\\w+):\\s*\"?(.*?)\"?\\s*$', line)"
)

p.write_text(content, encoding='utf-8')
print('Fixed fix_article.py')
