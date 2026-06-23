import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")
slug = "geo-audit-checklist"
lang = "ja"

template_path = PROJECT / f"{lang}/blog/_template-{lang}.html"
template = template_path.read_text(encoding="utf-8")

# Extract body from existing generated HTML
existing_path = PROJECT / f"{lang}/blog/{slug}.html"
existing = existing_path.read_text(encoding="utf-8")
body_match = re.search(r'<article class="article-content">(.*?)</article>', existing, re.DOTALL)
body_html = body_match.group(1).strip() if body_match else ""

# Read MD frontmatter
md_path = PROJECT / "blog-drafts" / slug / f"{slug}-{lang}.md"
md = md_path.read_text(encoding="utf-8-sig")
fm = {}
m = re.match(r'^---\s*\n(.*?)\n---', md, re.DOTALL)
if m:
    for line in m.group(1).split('\n'):
        kv = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)
        if kv:
            fm[kv.group(1)] = kv.group(2)

title = fm.get("title", "")
print(f"Title from FM: [{title}]")
print(f"Template has placeholder: {chr(123) + chr(123) + 'TITLE' + chr(125) + chr(125) in template}")

# Build HTML
html = template
html = html.replace("{{TITLE}}", title)

# Check H1
h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html)
print(f"H1 after replace: [{h1.group(1)[:80] if h1 else 'NONE'}]")

# Check if CTA placeholders are replaced
html = html.replace("{{BODY}}", body_html)
html = html.replace("{{CTA_TITLE}}", "test")
html = html.replace("{{CTA_TEXT}}", "test")
html = html.replace("{{CTA_LINK}}", "/ja/contact")
html = html.replace("{{CTA_BTN}}", "test")
html = html.replace("{{DATE}}", "2026-06-23")
html = html.replace("{{READ_TIME}}", "8 min")
html = html.replace("{{CATEGORY}}", "strategy")
html = html.replace("{{AUTHOR}}", "test")

# Check for any remaining placeholders
remaining = re.findall(r'\{\{[A-Z_]+\}\}', html)
print(f"Remaining placeholders: {remaining}")

# Write test output
out = PROJECT / "ja/blog/_test_output.html"
out.write_text(html, encoding="utf-8")
h1_final = re.search(r'<h1[^>]*>(.*?)</h1>', html)
print(f"Final H1: [{h1_final.group(1)[:80] if h1_final else 'NONE'}]")
out.unlink()
