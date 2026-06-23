from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\get_publish_args.py')
content = p.read_text(encoding='utf-8')
# Add BOM stripping after reading MD
old = '    md = (DRAFTS / slug / f"{slug}-{lang}.md").read_text(encoding="utf-8")'
new = '    md = (DRAFTS / slug / f"{slug}-{lang}.md").read_text(encoding="utf-8-sig")'
content = content.replace(old, new)
p.write_text(content, encoding='utf-8')
print('Fixed BOM handling')
