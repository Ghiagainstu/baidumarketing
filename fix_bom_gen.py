from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\gen_blog_html.py')
content = p.read_text(encoding='utf-8')
# Fix: use utf-8-sig to strip BOM when reading MD files
old = '    text = md_path.read_text(encoding="utf-8")'
new = '    text = md_path.read_text(encoding="utf-8-sig")'
if old in content:
    content = content.replace(old, new)
    p.write_text(content, encoding='utf-8')
    print('Fixed BOM in gen_blog_html.py')
else:
    print('Pattern not found')
