import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\blog\baidu-ppc-roi-calculator.html')
html = p.read_text(encoding='utf-8')
body = re.search(r'<article class="article-content">(.*?)</article>', html, re.DOTALL).group(1).strip()
print("First 300 chars of body:")
print(body[:300])
print()
print("Has frontmatter:", "---" in body[:100])
