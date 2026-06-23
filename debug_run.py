import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")
slug = "geo-audit-checklist"
lang = "ja"

template_path = PROJECT / f"{lang}/blog/_template-{lang}.html"
md_path = PROJECT / "blog-drafts" / slug / f"{slug}-{lang}.md"

# Read template
template = template_path.read_text(encoding="utf-8")
print(f"Template has {{{{TITLE}}}}: {'{{TITLE}}' in template}")

# Read MD
md = md_path.read_text(encoding="utf-8-sig")
fm = {}
m = re.match(r'^---\s*\n(.*?)\n---', md, re.DOTALL)
if m:
    for line in m.group(1).split('\n'):
        kv = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)
        if kv:
            fm[kv.group(1)] = kv.group(2)
title = fm.get("title", "")
print(f"Title: [{title}]")
print(f"Title is empty: {title == ''}")

# Do the replacement
html = template
html = html.replace("{{TITLE}}", title)
print(f"After replace, has {{{{TITLE}}}}: {'{{TITLE}}' in html}")
h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html)
print(f"H1 after replace: [{h1.group(1) if h1 else 'NOT FOUND'}]")
