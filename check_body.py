import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import re

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")
slug = "baidu-ppc-roi-calculator"
lang = "ja"

# Check what body content the generated EN HTML has
en_path = PROJECT / f"blog/{slug}.html"
en_html = en_path.read_text(encoding="utf-8")
body_match = re.search(r'<article class="article-content">(.*?)</article>', en_html, re.DOTALL)
en_body = body_match.group(1).strip() if body_match else "NOT FOUND"
print(f"EN body starts with: {en_body[:200]}")
print(f"EN body has frontmatter: {'---' in en_body[:50]}")

# Check what fix_article.py extracts
ja_path = PROJECT / f"ja/blog/{slug}.html"
ja_html = ja_path.read_text(encoding="utf-8")
body_match_ja = re.search(r'<article class="article-content">(.*?)</article>', ja_html, re.DOTALL)
ja_body = body_match_ja.group(1).strip() if body_match_ja else "NOT FOUND"
print(f"JA body starts with: {ja_body[:200]}")
print(f"JA body has frontmatter: {'---' in ja_body[:50]}")
