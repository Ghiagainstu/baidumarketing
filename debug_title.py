import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")
slug = "geo-audit-checklist"

# Read JA MD
md_path = PROJECT / "blog-drafts" / slug / f"{slug}-ja.md"
md = md_path.read_text(encoding="utf-8-sig")
fm = {}
m = re.match(r'^---\s*\n(.*?)\n---', md, re.DOTALL)
if m:
    for line in m.group(1).split('\n'):
        kv = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)
        if kv:
            fm[kv.group(1)] = kv.group(2)
print(f"Title from FM: [{fm.get('title', 'NOT FOUND')}]")
print(f"Description: [{fm.get('description', 'NOT FOUND')[:80]}]")

# Check what fix_article.py produces
ja_path = PROJECT / f"ja/blog/{slug}.html"
ja_html = ja_path.read_text(encoding="utf-8")
h1 = re.search(r'<h1[^>]*>(.*?)</h1>', ja_html)
print(f"H1 in generated: [{h1.group(1) if h1 else 'NOT FOUND'}]")

# Check if {{TITLE}} still exists
if '{{TITLE}}' in ja_html:
    print("{{TITLE}} placeholder still exists!")
else:
    print("{{TITLE}} was replaced (but possibly with empty string)")
